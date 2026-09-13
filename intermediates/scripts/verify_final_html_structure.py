#!/usr/bin/env python3
"""Check every generated route, source block, source heading and local fragment."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote, urlsplit

from functools import lru_cache
from lxml import html as lxml_html, etree


@lru_cache(maxsize=None)
def selector_path(selector):
    # This verifier uses only tag, class and attribute-presence selectors.
    parts = []
    for token in selector.split():
        if token.startswith('.'):
            name = token[1:]
            assert re.fullmatch(r'[a-z-]+', name)
            parts.append("*[contains(concat(' ', normalize-space(@class), ' '), ' " + name + " ')]")
        else:
            match = re.fullmatch(r'([a-z][a-z0-9]*)?(?:\[([a-z-]+)\])?', token)
            assert match, token
            tag, attribute = match.groups()
            parts.append((tag or '*') + ('[@' + attribute + ']' if attribute else ''))
    return etree.XPath('.//' + '//'.join(parts))


class HtmlNode:
    """Small lxml view for the verifier's fixed queries; avoids a second DOM copy."""
    def __init__(self, element):
        self.element = element
    def select(self, selector):
        return [HtmlNode(e) for e in selector_path(selector)(self.element)]
    def select_one(self, selector):
        matches = self.select(selector)
        return matches[0] if matches else None
    def __getitem__(self, key):
        return self.element.attrib[key]
    def get(self, key, default=None):
        value = self.element.get(key)
        return default if value is None else value.split() if key == 'class' else value
    def get_text(self):
        return self.element.text_content()
    @property
    def string(self):
        return self.get_text()
    @property
    def name(self):
        return self.element.tag
    @property
    def parent(self):
        return HtmlNode(self.element.getparent())
    @property
    def children(self):
        return [HtmlNode(e) for e in self.element if isinstance(e.tag, str)]
    @property
    def style(self):
        return self.select_one('style')
    @property
    def h3(self):
        return self.select_one('h3')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    aggregate = root / 'aggregate'
    report = aggregate / 'report.html'
    raw = report.read_bytes()
    html = raw.decode()
    index = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S).group(1))
    audit = json.loads((aggregate / 'audited.json').read_text())
    baseline = json.loads((root / 'tooling/renderer-review/approved-two-paper-baseline.json').read_text())
    reference = Path(baseline['reference_report']).read_bytes()
    assert sha(reference) == baseline['reference_sha256']
    css = Path(baseline['assets']['report.css']['path']).read_text()
    amendment = json.loads((root / 'tooling/renderer-review/rank-column-amendment.json').read_text())
    work_amendment = json.loads((root / 'tooling/renderer-review/work-status-amendment.json').read_text())
    columns_amendment = json.loads((root / 'tooling/renderer-review/api-columns-amendment.json').read_text())
    resize_amendment = json.loads((root / 'tooling/renderer-review/resizable-pane-amendment.json').read_text())
    three_amendment = json.loads((root / 'tooling/renderer-review/three-status-amendment.json').read_text())
    assert amendment['before_sha256'] == baseline['assets']['report.css']['sha256']
    assert work_amendment['assets']['report.css']['before_sha256'] == amendment['after_sha256']
    assert re.search(r'<style>(.*?)</style>', html, re.S).group(1).strip() == css.strip()
    for name, item in baseline['assets'].items():
        value = Path(item['path']).read_bytes()
        assert resize_amendment['assets'][name]['before_sha256'] == columns_amendment['assets'][name]['after_sha256']
        assert three_amendment['assets'][name]['before_sha256'] == resize_amendment['assets'][name]['after_sha256']
        assert sha(value) == three_amendment['assets'][name]['after_sha256']
        assert (root / 'tooling/skills/statistical-census-html/assets' / name).read_bytes() == value
    apis = {x['route']: x for x in index['interfaces']}
    papers = {x['route']: x for x in index['papers']}
    theorems = [t for p in index['papers'] for t in p['theorems']]
    assert len(apis) == len(audit['interfaces']) == 2486
    assert len(papers) == len(audit['papers']) == 113
    assert len(theorems) == len(audit['claims']) == 637
    assert 'theorems' not in index
    for t in theorems:
        assert t['api_count'] == len({x['route'] for x in t['requirements']})
        assert all(set(x) == {'route', 'relation'} and x['route'] in apis for x in t['requirements'])
    paths = {aggregate / x['url'] for x in [*apis.values(), *papers.values()]}
    assert len(paths) == 2599
    parents = {p.parent for p in paths}
    assert len(parents) == 1
    generation = parents.pop()
    manifest = json.loads((generation / 'manifest.json').read_text())
    assert set(manifest['pages']) == {p.name for p in paths}
    ids = {}
    links = []
    hashes = {}
    sources = {x['interface_id']: x for x in audit['interfaces']}
    assert audit['work_status_policy']['id'] == 'mathematical-work-v2'
    for route, record in apis.items():
        source = sources[route.removeprefix('interface:')]
        assert record['work_status'] == source['library_audit']['work_status']
        assert record['theorem_count'] == len({r['claim_id'] for r in source['related_theorems']})
        assert record['paper_count'] == len({r['paper_id'] for r in source['related_theorems']})
    source_blocks = 0
    highlights = 0
    pdf_urls = {x['source_url'] for x in audit['papers']}
    for route, record in [*apis.items(), *papers.items()]:
        path = aggregate / record['url']
        content = path.read_bytes()
        hashes[path.name] = sha(content)
        page = HtmlNode(lxml_html.fromstring(content))
        assert page.style.string.strip() == css.strip(), path
        page_ids = [e['id'] for e in page.select('[id]')]
        assert len(page_ids) == len(set(page_ids)), path
        ids[path] = set(page_ids)
        for a in page.select('a[href]'):
            href = a['href']
            parsed = urlsplit(href)
            if parsed.scheme:
                assert parsed.scheme == 'https', (path, href)
                if href in pdf_urls:
                    assert a.parent.name in {'h1', 'h2'}, (path, href)
            else:
                links.append((path, (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve(), unquote(parsed.fragment)))
        if route.startswith('interface:'):
            original = sources[route.removeprefix('interface:')]
            assert page.select_one('.work-audit .work-status')['data-work-status'] == original['library_audit']['work_status']
            assert page.select_one('.work-audit p').get_text() == original['library_audit']['work_status_reason']
            blocks = page.select('.original-definition')
            assert len(blocks) == len(original['members']), path
            members = {'variant-' + sha((m['paper_id'] + ':' + m['local_id']).encode())[:16]: m for m in original['members']}
            for block in blocks:
                m = members[block['id']]
                assert block['data-source-kind'] == m['source_kind'], path
                assert block.h3.get_text() == m['source_heading'], path
                assert block.select_one('.symbol-highlight'), (path, m['local_id'])
            for group in page.select('.paper-group'):
                children = [x for x in group.children if getattr(x, 'name', None) == 'section']
                kinds = [('theorems' if 'theorem-group' in x.get('class', []) else 'source') for x in children]
                assert kinds == sorted(kinds, key=lambda x: x == 'theorems'), path
            assert len(page.select('.theorem')) == len(original['related_theorems']), path
            assert page.select_one('.gap').get_text() == original['library_audit']['gap'], path
            assert [a['href'] for a in page.select('.library-links a')] == [d['url'] for d in original['library_audit']['related_declarations']], path
            source_blocks += len(blocks)
            highlights += len(page.select('.symbol-highlight'))
        else:
            assert len(page.select('.theorem')) == record['theorem_count'], path
            assert not page.select('.symbol-highlight'), path
            for heading in page.select('.requirement-heading'):
                route = heading.select_one('a[data-route]')['data-route']
                assert heading.select_one('.work-status')['data-work-status'] == apis[route]['work_status']
    for source, target, fragment in links:
        assert target in ids, (source, target)
        assert not fragment or fragment in ids[target], (source, target, fragment)
    for t in theorems:
        parts = urlsplit(t['url'])
        assert parts.fragment in ids[(aggregate / parts.path).resolve()]
    assert source_blocks == 2655
    evidence = {
        'status': 'passed', 'checked_at': datetime.now(timezone.utc).isoformat(),
        'report_sha256': sha(raw), 'audit_sha256': sha((aggregate / 'audited.json').read_bytes()),
        'counts': {'papers': len(papers), 'theorems': len(theorems), 'interfaces': len(apis),
                   'readers': len(paths), 'source_blocks': source_blocks, 'highlights': highlights,
                   'local_links_and_fragments': len(links)},
        'generation': str(generation.relative_to(aggregate)),
        'index_bytes': len(raw), 'reader_sha256': hashes,
        'checks': ['All routes and local fragments resolve', 'Exact source headings and kinds',
                   'Every source member visibly highlighted', 'Paper readers unhighlighted',
                   'Complete theorem inventory and API relation counts', 'Source blocks before Theorems',
                   'Exact mathlib links and gap text', 'Paper-level PDF links only',
                   'Approved reading style preserved with reviewed rank-column and user-requested work-status changes; embedded CSS identical on every page',
                   'Every API and theorem requirement shows its exact audited three-tier work status and reason',
                   'Theorem and paper counts equal distinct related theorem and paper IDs',
                   'One search record per API; theorem requirements contain only route and relation'],
        'limits': 'Structural coverage; visual and interaction checks are recorded separately.'
    }
    (aggregate / 'html-structure-verification.json').write_text(json.dumps(evidence, indent=2) + '\n')
    print(json.dumps({k: v for k, v in evidence.items() if k != 'reader_sha256'}))


if __name__ == '__main__':
    main()
