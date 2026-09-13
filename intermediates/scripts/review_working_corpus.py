"""Independently compare a working aggregate with every pinned original paper census."""
import collections
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    out = ROOT / 'aggregate/working'
    census = json.loads((out / 'ranked-interfaces.json').read_text())
    pins = json.loads((out / 'reconciliation.json').read_text())['inputs']
    aliases = json.loads((out / 'interface-aliases.json').read_text())
    relationships = json.loads((out / 'source-relationships.json').read_text())
    review = json.loads((ROOT / 'aggregate/grouping-review.json').read_text())
    status = json.loads((out / 'build-status.json').read_text())
    assert status['grouping_review_sha256'] == digest(ROOT / 'aggregate/grouping-review.json')
    assert status['census_sha256'] == digest(out / 'ranked-interfaces.json')
    mapping = {a['input_key']: a['aggregate_interface_id'] for a in aliases}
    assert len(mapping) == len(aliases)
    source, papers, claims, original_members = {}, [], [], {}
    for pin in pins:
        for path, h in pin['files'].items():
            assert digest(ROOT / path) == h
        d = json.loads((ROOT / 'papers' / pin['paper_id'] / 'ranked-interfaces.json').read_text())
        papers.extend(d['papers']); claims.extend(d['claims'])
        for i in d['interfaces']:
            source[pin['paper_id'] + '::' + i['interface_id']] = i
            for m in i['members']:
                key = (m['paper_id'], m['local_id'])
                assert key not in original_members
                original_members[key] = m
    assert census['papers'] == papers and census['claims'] == claims
    assert set(mapping) == set(source)
    current = {i['interface_id']: i for i in census['interfaces']}
    assert set(mapping.values()) == set(current)
    groups = {g['group_id']: g for g in review['groups']}
    inverted = collections.defaultdict(list)
    for key, iid in mapping.items():
        inverted[iid].append(key)
    actual_members = set()
    original_owner = {(m['paper_id'], m['local_id']): mapping[k]
                      for k, i in source.items() for m in i['members']}
    expected_paths = collections.defaultdict(dict)
    for claim in claims:
        queue = collections.deque([[lid] for lid in claim['depends_on']])
        seen = set()
        while queue:
            path = queue.popleft()
            key = claim['paper_id'], path[-1]
            if key in seen:
                continue
            seen.add(key)
            expected_paths[original_owner[key]].setdefault(claim['claim_id'], path)
            queue.extend(path + [lid] for lid in original_members[key]['depends_on'])
    for iid, item in current.items():
        keys = inverted[iid]
        if len(keys) > 1:
            assert set(keys) == set(groups[iid]['input_keys'])
        expected_members = {(m['paper_id'], m['local_id']) for k in keys for m in source[k]['members']}
        assert {(m['paper_id'], m['local_id']) for m in item['members']} == expected_members
        assert not actual_members.intersection(expected_members)
        actual_members.update(expected_members)
        for m in item['members']:
            original = original_members[m['paper_id'], m['local_id']]
            expected = dict(original)
            for k in keys:
                if any((m['paper_id'], m['local_id']) == (x['paper_id'], x['local_id']) for x in source[k]['members']):
                    note = groups.get(iid, {}).get('variant_notes', {}).get(k)
                    if note:
                        expected['variant_note'] = '\n'.join(v for v in (original.get('variant_note'), note) if v)
            assert m == expected, (iid, m['local_id'])
        expected_uses = [u for k in keys for u in source[k]['central_claim_uses']]
        first_uses = {}
        for use in expected_uses:
            first_uses.setdefault(use['claim_id'], use)
        assert item['central_claim_uses'] == list(first_uses.values())
        assert relationships[iid] == [dict(input_key=k,
            central_claim_uses=source[k]['central_claim_uses'],
            related_theorems=source[k]['related_theorems'],
            theorem_explanations=source[k]['theorem_explanations']) for k in keys]
        expected_related = [t for k in keys for t in source[k]['related_theorems']]
        expected_claims = {t['claim_id'] for t in expected_related}
        assert {t['claim_id'] for t in item['related_theorems']} == expected_claims
        assert len(item['related_theorems']) == len(expected_claims)
        assert set(item['theorem_explanations']) == expected_claims
        for record in item['related_theorems']:
            cid = record['claim_id']
            candidates = [t for t in expected_related if t['claim_id'] == cid]
            assert record in candidates
            if record['relation'] != 'target':
                assert record['via_local_ids'] == expected_paths[iid][cid]
            explanation = item['theorem_explanations'][cid]
            assert explanation in [source[k]['theorem_explanations'][cid] for k in keys
                                   if cid in source[k]['theorem_explanations']]
            assert explanation['via_local_ids'] == record['via_local_ids']
            assert explanation['paper_id'] == record['paper_id']
        assert item['central_claim_use_count'] == len(first_uses)
        assert item['central_claim_paper_count'] == len({u['paper_id'] for u in expected_uses})
        assert item['supported_claim_count'] == len(expected_claims)
        assert item['supported_claim_paper_count'] == len({t['paper_id'] for t in expected_related})
    assert actual_members == set(original_members)
    assert set(relationships) == set(current)
    rank_groups = collections.defaultdict(list)
    for item in current.values():
        rank_groups[item['rank_group']].append(item)
    for group in rank_groups.values():
        ordered = sorted(group, key=lambda i: (-i['central_claim_paper_count'], -i['central_claim_use_count'], i['name'].casefold(), i['interface_id']))
        assert [i['semantic_rank'] for i in ordered] == list(range(1, len(group) + 1))
    record = dict(status='passed', release_complete=False, reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  scope='Independent exact-preservation and aggregate-count review; source-note triage and downstream release checks are separate.',
                  pending_grouping_reviews=len(review['unreviewed_input_keys']),
                  census_sha256=digest(out / 'ranked-interfaces.json'), grouping_review_sha256=digest(ROOT / 'aggregate/grouping-review.json'),
                  paper_count=len(papers), theorem_count=len(claims), source_member_count=len(actual_members),
                  input_interface_count=len(source), aggregate_interface_count=len(current),
                  checks=['All pinned input hashes', 'Exact paper and claim records', 'Every original member and local dependency',
                          'Only explicit variant notes added', 'All original uses, paths and explanations retained in source-relationships.json',
                          'Reader paths independently traced through original local dependencies', 'Each theorem counted once per group',
                          'Independent global counts and semantic ranking'])
    (out / 'independent-validation.json').write_text(json.dumps(record, indent=2) + '\n')
    print('Independent aggregate preservation and count checks passed; release is still incomplete.')


if __name__ == '__main__':
    main()
