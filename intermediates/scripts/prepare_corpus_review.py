"""Reconcile pinned paper artifacts and prepare an explicitly unfinished grouping queue."""
import collections
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, 'skills/statistical-paper-census/scripts')
from validate_census import validate
from publication_contract import claim_source


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    corpus = json.loads((ROOT / 'corpus.json').read_text())
    progress = json.loads((ROOT / 'progress.json').read_text())
    assert progress['counts'] == {'complete': 113}
    expected = [p['paper_id'] for p in corpus['papers']]
    assert len(expected) == len(set(expected)) == 113
    papers, claims, interfaces, pins, issues = [], [], [], [], []
    for pid in expected:
        folder = ROOT / 'papers' / pid
        inventory_path = folder / 'theorem-inventory.json'
        census_path = folder / 'ranked-interfaces.json'
        audit = json.loads((folder / 'paper-audit.json').read_text())
        for path in (inventory_path, census_path):
            assert digest(path) == audit['artifacts'][path.name]['sha256'], path
            assert not validate(path), path
        inv = json.loads(inventory_path.read_text())
        census = json.loads(census_path.read_text())
        assert inv['papers'] == census['papers']
        assert inv['claims'] == [claim_source(c) for c in census['claims']]
        assert [p['paper_id'] for p in inv['papers']] == [pid]
        papers.extend(inv['papers'])
        claims.extend(inv['claims'])
        interfaces.extend(dict(i, input_key=pid + '::' + i['interface_id']) for i in census['interfaces'])
        pins.append(dict(paper_id=pid, files={str(p.relative_to(ROOT)): digest(p) for p in (
            inventory_path, census_path, folder / 'paper-audit.json', folder / 'registered-source-review.json')}))
        for name in ('registered-source-review.json', 'paper-audit.json', 'ambient-prerequisites.json',
                     'ambient-resolution.json'):
            path = folder / name
            if not path.exists():
                continue
            def collect(value, trail=()):
                if isinstance(value, dict):
                    for field, child in value.items():
                        if any(t in field.lower() for t in ('unresolved', 'ambigu', 'source_issue', 'source_note', 'review_limit')) and child:
                            issues.append(dict(paper_id=pid, field=list(trail + (field,)), value=child,
                                               source=str(path.relative_to(ROOT))))
                        else:
                            collect(child, trail + (field,))
                elif isinstance(value, list):
                    for n, child in enumerate(value):
                        collect(child, trail + (n,))
            collect(json.loads(path.read_text()))
    assert len({c['claim_id'] for c in claims}) == len(claims)
    assert len({i['input_key'] for i in interfaces}) == len(interfaces)
    out = ROOT / 'aggregate' / 'working'
    out.mkdir(parents=True, exist_ok=True)
    def save(name, value):
        (out / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    save('theorem-inventory.json', dict(schema_version='statistical-theorem-inventory-v1',
         scope=dict(theorem_scope='main_text_only'), papers=papers, claims=claims))
    assert not validate(out / 'theorem-inventory.json')
    by_name = collections.defaultdict(list)
    for item in interfaces:
        key = re.sub(r'\s+', ' ', item['name'].casefold().replace('–', '-').replace('—', '-')).strip()
        by_name[key].append(item['input_key'])
    save('grouping-candidates.json', dict(status='pending_semantic_review',
         policy='Name matches are search candidates only; no automatic equivalence or merge.',
         candidates=[dict(name=k, input_keys=v, status='pending') for k, v in sorted(by_name.items()) if len(v)>1]))
    save('interface-index.json', [dict(input_key=i['input_key'], interface_id=i['interface_id'], name=i['name'],
         members=i['members'], source_keywords=i['source_keywords'],
         source_censuses=sorted({f"papers/{m['paper_id']}/ranked-interfaces.json" for m in i['members']})) for i in interfaces])
    save('reconciliation.json', dict(status='passed', checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
         scope='Inventory/source identity and exact paper-artifact reconciliation; not semantic grouping or release approval.',
         paper_count=len(papers), theorem_count=len(claims), input_interface_count=len(interfaces),
         source_member_count=sum(len(i['members']) for i in interfaces), inputs=pins,
         aggregate_inventory_sha256=digest(out / 'theorem-inventory.json')))
    save('source-followups.json', dict(status='pending_corpus_review', items=issues))
    print(f'Reconciled {len(papers)} papers, {len(claims)} theorems and {len(interfaces)} interfaces. Grouping remains pending.')


if __name__ == '__main__':
    main()
