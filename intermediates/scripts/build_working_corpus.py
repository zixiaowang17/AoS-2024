"""Apply explicit reviewed groups to a non-release corpus and recompute global metrics."""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path('skills/statistical-paper-census/scripts')
sys.path.insert(0, str(SKILL))
from census_metrics import DERIVED_FIELDS
from theorem_index import derive_related


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    out = ROOT / 'aggregate/working'
    review_path = ROOT / 'aggregate/grouping-review.json'
    review = json.loads(review_path.read_text())
    assert review['input_index_sha256'] == sha(out / 'interface-index.json')
    reconciliation = json.loads((out / 'reconciliation.json').read_text())
    inventories = json.loads((out / 'theorem-inventory.json').read_text())
    source, claims, metadata = {}, [], {}
    for pin in reconciliation['inputs']:
        for name, expected in pin['files'].items():
            assert sha(ROOT / name) == expected, name
        path = ROOT / 'papers' / pin['paper_id'] / 'ranked-interfaces.json'
        census = json.loads(path.read_text())
        claims.extend(census['claims'])
        for item in census['interfaces']:
            key = pin['paper_id'] + '::' + item['interface_id']
            source[key] = item
            metadata[key] = dict(input_interface_id=item['interface_id'], source_census=str(path.relative_to(ROOT)))
    groups, assigned = [], set()
    for decision in review['groups']:
        assert decision['status'] == 'reviewed'
        keys = decision['input_keys']
        assert len(keys) > 1 and not assigned.intersection(keys)
        assert all(k in source for k in keys)
        groups.append((decision['group_id'], keys, decision))
        assigned.update(keys)
    for key in source:
        if key not in assigned:
            groups.append(('local-' + hashlib.sha256(key.encode()).hexdigest()[:20], [key], None))
    interfaces, aliases, source_relationships = [], [], {}
    for iid, keys, decision in groups:
        originals = [source[k] for k in keys]
        assert len({i['rank_group'] for i in originals}) == 1
        assert len({i['lean_role'] for i in originals}) == 1
        item = copy.deepcopy(originals[0])
        item['interface_id'] = iid
        for field in (*DERIVED_FIELDS, 'related_theorems'):
            item.pop(field, None)
        item['dependencies'] = []
        source_relationships[iid] = [dict(input_key=k,
            central_claim_uses=copy.deepcopy(source[k]['central_claim_uses']),
            related_theorems=copy.deepcopy(source[k]['related_theorems']),
            theorem_explanations=copy.deepcopy(source[k]['theorem_explanations'])) for k in keys]
        if len(keys) > 1:
            for field in ('members', 'central_claim_uses', 'source_keywords'):
                item[field] = [copy.deepcopy(v) for original in originals for v in original[field]]
            labels = list(dict.fromkeys(k['label'] for k in item['source_keywords'] if k.get('kind', 'term') == 'term'))
            item['name'] = ' · '.join(labels)
            # A theorem contributes once even when it directly needs several
            # equivalent local members. Keep every source use in the sidecar.
            unique_uses = {}
            for use in item['central_claim_uses']:
                unique_uses.setdefault(use['claim_id'], use)
            item['central_claim_uses'] = list(unique_uses.values())
            for field in ('type_shape', 'semantic_boundary'):
                item[field] = '\n\n'.join(k + ': ' + source[k][field] for k in keys)
            for key, original in zip(keys, originals):
                for member in item['members']:
                    if any((member['paper_id'], member['local_id']) == (m['paper_id'], m['local_id']) for m in original['members']):
                        note = decision.get('variant_notes', {}).get(key)
                        if note:
                            member['variant_note'] = '\n'.join(v for v in (member.get('variant_note'), note) if v)
                        # Preserve the original relation rather than silently relabelling a specialization.
            item['semantic_boundary'] += '\n\nGrouping review: ' + decision['reason']
        interfaces.append(item)
        aliases.extend(dict(input_key=k, aggregate_interface_id=iid, **metadata[k]) for k in keys)
    assert len(aliases) == len(source)
    data = dict(schema_version='statistical-ranked-interfaces-v4', scope=dict(
        paper_count=113, theorem_scope='main_text_only',
        source_policy='All 113 registered local source versions; exact reviewed inventories reconciled with pinned per-paper censuses.',
        normalization_policy='Preserve original paper statements, local dependencies and source terminology. Only explicit grouping decisions combine interfaces.',
        semantic_ranking_policy='Global direct-paper and direct-theorem demand, recomputed from all included papers.',
        build_order_policy='Recomputed canonical DAG from unchanged same-paper source dependencies.'),
        papers=inventories['papers'], claims=claims, interfaces=interfaces)
    # The reader uses one actual local path per theorem. Select the unchanged
    # source explanation for that path; retain all alternatives in the sidecar.
    related = derive_related(data)
    for item in interfaces:
        selected = {}
        for record in related[item['interface_id']]:
            cid = record['claim_id']
            candidates = [s['theorem_explanations'][cid]
                          for s in source_relationships[item['interface_id']]
                          if cid in s['theorem_explanations']]
            selected[cid] = copy.deepcopy(next(e for e in candidates
                if e['paper_id'] == record['paper_id']
                and e['via_local_ids'] == record['via_local_ids']))
        item['theorem_explanations'] = selected
    def save(name, value):
        (out / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    save('unfinalized-census.json', data)
    subprocess.run([sys.executable, str(SKILL / 'finalize_census.py'), str(out / 'unfinalized-census.json'),
                    str(out / 'ranked-interfaces.json'), '--inventory', str(out / 'theorem-inventory.json')], check=True)
    save('interface-aliases.json', aliases)
    save('source-relationships.json', source_relationships)
    save('build-status.json', dict(status='working_not_release', grouping_status=review['status'],
         pending_grouping_reviews=len(review['unreviewed_input_keys']),
         grouping_review_sha256=sha(review_path), census_sha256=sha(out / 'ranked-interfaces.json'),
         paper_count=113, theorem_count=len(claims), interface_count=len(interfaces),
         checks='Pinned inputs, unchanged inventoried claims, local dependency closure and global metrics pass the producer validator.',
         outstanding=(['Complete semantic grouping review'] if review['unreviewed_input_keys'] else [])
         + ['Independent aggregate review', 'Retained source-note triage', 'Mathlib comparisons', 'Final HTML validation']))
    print('Working aggregate validated; it is not approved for publication.')


if __name__ == '__main__':
    main()
