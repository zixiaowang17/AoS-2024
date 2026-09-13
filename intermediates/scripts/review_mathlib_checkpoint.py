#!/usr/bin/env python3
"""Check partial audit pins, coverage and recorded link evidence, without certifying research."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def main():
    aggregate = Path(__file__).resolve().parents[1] / 'aggregate'
    progress_path = aggregate / 'mathlib-search-progress.json'
    progress = json.loads(progress_path.read_text())
    census_path = aggregate / progress['source_census']
    assert progress['source_census_sha256'] == hashlib.sha256(census_path.read_bytes()).hexdigest()
    census = json.loads(census_path.read_text())
    interfaces = {a['interface_id']: a for a in census['interfaces']}
    manifest = json.loads((aggregate / progress['source_manifest']).read_text())
    assert progress['mathlib_revision'] == manifest['mathlib_revision']
    assert progress['lean_version'] == manifest['lean_version']
    links = json.loads((aggregate / progress['link_evidence']).read_text())
    declarations = {d['name']: d for d in json.loads(
        (aggregate / progress['declaration_evidence']).read_text())}
    seen = set()
    used_links = set()
    for record in progress['completed']:
        key = record['interface_id']
        assert key in interfaces and key not in seen
        seen.add(key)
        interface = interfaces[key]
        assert record['status'] == 'reviewed'
        assert record['source_interface_sha256'] == digest(interface)
        assert len(record['variant_reviews']) == len(interface['members'])
        for review, member in zip(record['variant_reviews'], interface['members']):
            assert all(review[k] == member[k] for k in ('paper_id', 'local_id'))
            assert review['statement_sha256'] == hashlib.sha256(member['statement_original'].encode()).hexdigest()
            assert review['comparison'].strip()
        audit = record['library_audit']
        assert audit['status'] in {'exact_reuse', 'composable', 'partial_match', 'no_verified_match'}
        assert audit['gap'].strip() and audit['searches']
        assert all(s[k].strip() for s in audit['searches'] for k in ('mechanism', 'query', 'result'))
        if not audit['related_declarations']:
            assert audit['status'] == 'no_verified_match' and audit['no_related_reason'].strip()
        for d in audit['related_declarations']:
            assert d['link_checked'] is True
            evidence = links[d['url']]
            original = declarations[d['name']]
            assert evidence['name'] == d['name'] and evidence['link_checked'] is True
            assert evidence['mathlib_revision'] == progress['mathlib_revision']
            assert all(d[k] == original[k] for k in ('name', 'type', 'declaration_kind', 'module', 'provides'))
            source = aggregate / 'mathlib-evidence/source-files' / (d['module'].replace('.', '/') + '.lean')
            assert hashlib.sha256(source.read_bytes()).hexdigest() == evidence['source_sha256']
            start, end = evidence['source_lines']
            assert '\n'.join(source.read_text().splitlines()[start-1:end]) == evidence['excerpt']
            used_links.add(d['url'])
    pending = progress['pending_interface_ids']
    assert len(set(pending)) == len(pending)
    assert not seen.intersection(pending) and seen.union(pending) == set(interfaces)
    counts = {'total': len(interfaces), 'reviewed': len(seen), 'pending': len(pending)}
    assert counts == progress['counts']
    result = {
        'status': 'passed', 'release_complete': False,
        'checked_at': datetime.now(timezone.utc).isoformat(),
        'scope': 'Partial checkpoint integrity only; does not certify mathematical comparisons or final audit completion.',
        'progress_sha256': hashlib.sha256(progress_path.read_bytes()).hexdigest(),
        'source_census_sha256': progress['source_census_sha256'], 'counts': counts,
        'verified_used_links': len(used_links),
        'checks': ['Pinned census and library', 'Every reviewed variant accounted for',
                   'Original interface and statement hashes', 'Exact inspected declaration records',
                   'Saved source excerpts and opened-link evidence', 'Complete reviewed/pending partition'],
    }
    (aggregate / 'mathlib-checkpoint-validation.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result['counts']), 'links:', len(used_links))


if __name__ == '__main__':
    main()
