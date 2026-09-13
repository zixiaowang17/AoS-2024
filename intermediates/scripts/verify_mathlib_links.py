#!/usr/bin/env python3
"""Open pinned declaration pages and check their displayed source and line ranges.

Input records are manually inspected declarations, not search-generated verdicts.
This verifies links only; it does not establish mathematical equivalence.
"""
import argparse
import hashlib
import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('declarations', type=Path)
    args = parser.parse_args()
    aggregate = Path(__file__).resolve().parents[1] / 'aggregate'
    manifest = json.loads((aggregate / 'mathlib-source-manifest.json').read_text())
    revision = manifest['mathlib_revision']
    root = Path(manifest['source_root'])
    pins = {x['path']: x['sha256'] for x in manifest['verified_files']}
    evidence_dir = aggregate / 'mathlib-evidence'
    evidence_dir.mkdir(exist_ok=True)
    evidence_path = evidence_dir / 'links.json'
    evidence = json.loads(evidence_path.read_text()) if evidence_path.exists() else {}
    pages = {}
    for declaration in json.loads(args.declarations.read_text()):
        path = declaration['module'].replace('.', '/') + '.lean'
        start, end = declaration['source_lines']
        base = f'https://github.com/leanprover-community/mathlib4/blob/{revision}/{path}'
        url = f'{base}#L{start}-L{end}'
        local = (root / path).read_bytes()
        assert hashlib.sha256(local).hexdigest() == pins[path], path
        if base not in pages:
            request = urllib.request.Request(url, headers={'User-Agent': 'annals-census-link-review'})
            with urllib.request.urlopen(request, timeout=40) as response:
                page = response.read()
                assert response.status == 200
                assert response.geturl().split('#')[0] == base
            payloads = [json.loads(s) for s in re.findall(
                r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',
                page.decode(), re.S)]
            payload = next(p['payload'] for p in payloads if 'payload' in p
                           and 'codeViewBlobLayoutRoute.StyledBlob' in p['payload'])
            route = payload['codeViewBlobLayoutRoute']
            assert route['path'] == path and route['refInfo']['currentOid'] == revision
            lines = payload['codeViewBlobLayoutRoute.StyledBlob']['rawLines']
            assert lines == local.decode().splitlines(), path
            pages[base] = (lines, hashlib.sha256(page).hexdigest())
            saved = evidence_dir / 'source-files' / path
            saved.parent.mkdir(parents=True, exist_ok=True)
            saved.write_bytes(local)
        lines, page_hash = pages[base]
        assert 1 <= start <= end <= len(lines)
        excerpt = '\n'.join(lines[start - 1:end])
        assert declaration['source_name'] in excerpt, declaration['name']
        evidence[url] = {
            'name': declaration['name'], 'url': url, 'mathlib_revision': revision,
            'checked_at': datetime.now(timezone.utc).isoformat(),
            'method': 'Opened official GitHub blob; verified revision, path, all displayed source lines and declaration line range against archive-pinned local source.',
            'source_sha256': pins[path], 'response_sha256': page_hash,
            'source_lines': [start, end], 'excerpt': excerpt, 'link_checked': True,
        }
        evidence_path.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + '\n')
        print('Verified', declaration['name'], flush=True)


if __name__ == '__main__':
    main()
