#!/usr/bin/env python3
"""Save manually researched batch reviews without replacing completed records.

This assembles evidence records; it does not search or decide mathematical matches.
Run review_mathlib_checkpoint.py after saving to check the full partial checkpoint.
"""
import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def member_comparisons(interface, comparisons):
    """Accept paper-qualified keys when local IDs repeat across papers."""
    members = interface['members']
    qualified = [f"{m['paper_id']}/{m['local_id']}" for m in members]
    if set(comparisons) == set(qualified):
        return [comparisons[key] for key in qualified]
    # Preserve the original batch format, including historical shared prose.
    assert set(comparisons) == {m['local_id'] for m in members}
    return [comparisons[m['local_id']] for m in members]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('batch')
    args = parser.parse_args()
    assert re.fullmatch(r'[a-z0-9-]+', args.batch)
    root = Path(__file__).resolve().parents[1] / 'aggregate'
    batches = root / 'mathlib-evidence/batches'
    path = root / 'mathlib-search-progress.json'
    original = path.read_bytes()
    progress = json.loads(original)
    census_bytes = (root / progress['source_census']).read_bytes()
    assert sha(census_bytes) == progress['source_census_sha256']
    interfaces = {x['interface_id']: x for x in json.loads(census_bytes)['interfaces']}
    declarations = {x['name']: x for x in json.loads((root / progress['declaration_evidence']).read_text())}
    links = json.loads((root / progress['link_evidence']).read_text())
    rows = json.loads((batches / f'{args.batch}-reviews.json').read_text())['rows']
    assert len({row['interface_id'] for row in rows}) == len(rows)
    now = datetime.now(timezone.utc).isoformat()
    revision = progress['mathlib_revision']
    records = []
    for row in rows:
        interface = interfaces[row['interface_id']]
        comparisons = member_comparisons(interface, row['comparisons'])
        related = []
        for name in row['related']:
            declaration = declarations[name]
            start, end = declaration['source_lines']
            module_path = declaration['module'].replace('.', '/') + '.lean'
            url = f'https://github.com/leanprover-community/mathlib4/blob/{revision}/{module_path}#L{start}-L{end}'
            assert links[url]['name'] == name and links[url]['link_checked'] is True
            assert links[url]['mathlib_revision'] == revision
            related.append({**{k: declaration[k] for k in ('name', 'type', 'declaration_kind', 'module', 'provides')},
                            'url': url, 'link_checked': True})
        status = row.get('status', 'partial_match')
        assert status in {'partial_match', 'composable', 'exact_reuse', 'no_verified_match'}
        audit = {'status': status, 'related_declarations': related,
                 'searches': [{'mechanism': 'Archive-pinned local rg search and direct declaration/body inspection',
                               'query': row['query'], 'result': row['result']}], 'gap': row['gap']}
        if not related:
            assert status == 'no_verified_match' and row['no_related_reason'].strip()
            audit['no_related_reason'] = row['no_related_reason']
        records.append({'interface_id': interface['interface_id'], 'status': 'reviewed', 'reviewed_at': now,
                        'source_interface_sha256': sha(json.dumps(interface, sort_keys=True, ensure_ascii=False).encode()),
                        'variant_reviews': [{'paper_id': m['paper_id'], 'local_id': m['local_id'],
                                             'comparison': comparison,
                                             'statement_sha256': sha(m['statement_original'].encode())}
                                            for m, comparison in zip(interface['members'], comparisons)], 'library_audit': audit})
    done = {x['interface_id'] for x in progress['completed']}
    added = [x for x in records if x['interface_id'] not in done]
    added_ids = {x['interface_id'] for x in added}
    assert added_ids <= set(progress['pending_interface_ids'])
    progress['completed'].extend(added)
    progress['pending_interface_ids'] = [x for x in progress['pending_interface_ids'] if x not in added_ids]
    progress['counts'] = {'total': len(interfaces), 'reviewed': len(progress['completed']),
                          'pending': len(progress['pending_interface_ids'])}
    progress['updated_at'] = now
    temporary = path.with_suffix(f'.{args.batch}.{os.getpid()}.tmp')
    write_json(temporary, progress)
    try:
        assert path.read_bytes() == original, 'Checkpoint changed; rerun against current state'
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    write_json(batches / f'{args.batch}-records.json', records)
    handoff = {'added_interface_ids': [x['interface_id'] for x in added],
               'preserved_existing_interface_ids': [x['interface_id'] for x in records if x['interface_id'] in done],
               'counts': progress['counts'], 'updated_at': now}
    write_json(batches / f'{args.batch}-handoff.json', handoff)
    print(json.dumps(handoff))


if __name__ == '__main__':
    main()
