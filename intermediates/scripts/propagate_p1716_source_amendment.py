"""Propagate the inspected D8 transcription repair, preserving unchanged reviews.

Run after the per-paper amendment, reproduction and corpus reconciliation.
This is a one-time migration with an archived before-state and explicit diff gates.
It does not renew the mathematical/source reviews of unaffected records.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
AGG = ROOT / 'aggregate'
WORK = AGG / 'working'
HISTORY = ROOT / 'review-history/p1716-source-notation/aggregate'
PID = 'aos-2024-v52-i04-p1716'
IID = 'local-ee88b5c894d5c1747323'
OLD = r'\widetilde\nu_t=\frac1N\sum_{i=1}^N\nu_{it}'
NEW = r'\widetilde\nu_t=\frac1N\sum_{i=1}^N\nu_i'


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def item_sha(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def run(script):
    subprocess.run([sys.executable, str(ROOT / 'scripts' / script)], check=True)


def correct_only_member(value):
    result = copy.deepcopy(value)
    def visit(node):
        if isinstance(node, dict):
            if node.get('paper_id') == PID and node.get('local_id') == 'D8' and 'statement_original' in node:
                assert node['statement_original'].count(OLD) == 1
                node['statement_original'] = node['statement_original'].replace(OLD, NEW)
            for child in node.values():
                visit(child)
        elif isinstance(node, list):
            for child in node:
                visit(child)
    visit(result)
    return result


def main():
    now = datetime.now(timezone.utc).isoformat()
    amendment = ROOT / 'papers' / PID / 'evidence/rendering-amendment-review.json'
    assert read(amendment)['status'] == 'passed'
    before_index = read(HISTORY / 'working/interface-index.json')
    assert read(WORK / 'interface-index.json') == correct_only_member(before_index)
    groups = read(AGG / 'grouping-review.json')
    assert groups == read(HISTORY / 'grouping-review.json')
    groups['input_index_sha256'] = sha(WORK / 'interface-index.json')
    groups['source_amendment'] = dict(path=str(amendment.relative_to(ROOT)), sha256=sha(amendment),
        reviewed_at=now, scope='Only unmerged p1716 D8 source transcription changed; all grouping decisions retained.')
    assert not any(PID + '::' + PID + '/D8' in g['input_keys'] for g in groups['groups'])
    save(AGG / 'grouping-review.json', groups)
    run('build_working_corpus.py')
    run('review_working_corpus.py')
    old_census = read(HISTORY / 'ranked-interfaces.json')
    new_census = read(WORK / 'ranked-interfaces.json')
    assert new_census == correct_only_member(old_census), 'Unexpected corpus change'
    assert sha(WORK / 'theorem-inventory.json') == sha(HISTORY / 'theorem-inventory.json')
    for name in ['interface-aliases.json', 'source-relationships.json']:
        assert sha(WORK / name) == sha(HISTORY / name), name

    checkpoint = read(WORK / 'grouping-checkpoint.json')
    assert checkpoint == read(HISTORY / 'working/grouping-checkpoint.json')
    checkpoint.update(reviewed_at=now, grouping_review_sha256=sha(AGG / 'grouping-review.json'),
                      census_sha256=sha(WORK / 'ranked-interfaces.json'))
    checkpoint['source_amendment'] = groups['source_amendment']
    save(WORK / 'grouping-checkpoint.json', checkpoint)

    old_followups = read(HISTORY / 'working/source-followups.json')['items']
    new_followups = read(WORK / 'source-followups.json')['items']
    assert len(old_followups) == len(new_followups)
    changed_notes = []
    for n, (old, new) in enumerate(zip(old_followups, new_followups)):
        if old != new:
            assert new['paper_id'] == PID and new['field'] == ['source_notes']
            assert new['source'] == f'papers/{PID}/paper-audit.json'
            assert new['value'][:-1] == old['value']
            assert new['value'][-1]['issue_id'] == 'mean-average-subscript'
            changed_notes.append(n)
    assert len(changed_notes) == 1
    triage = read(AGG / 'source-note-triage.json')
    assert triage == read(HISTORY / 'source-note-triage.json')
    triage.update(source_followups_sha256=sha(WORK / 'source-followups.json'), reviewed_at=now)
    for decision in triage['decisions']:
        n = decision['item_index']
        if n in changed_notes:
            decision['item_sha256'] = item_sha(new_followups[n])
            decision['reason'] += ' Also reviewed the page-6 mean-average subscript amendment: nu_i is restored verbatim and its mismatch with nu_it remains unresolved.'
            decision['comparison_limits'].append('D8 prints nu_i in the average defining nu-tilde_t; do not silently insert t or infer that the time-dependent mean decomposition is verified by that displayed average.')
            decision.pop('duplicate_of', None)
        elif decision.get('duplicate_of') in changed_notes:
            decision.pop('duplicate_of')
    save(AGG / 'source-note-triage.json', triage)
    run('review_source_note_triage.py')

    # Read the latest mathlib checkpoint, allowing independently saved unchanged reviews.
    progress_path = AGG / 'mathlib-search-progress.json'
    progress_bytes = progress_path.read_bytes()
    progress = json.loads(progress_bytes)
    assert progress['source_census_sha256'] == sha(HISTORY / 'ranked-interfaces.json')
    old_interfaces = {x['interface_id']: x for x in old_census['interfaces']}
    new_interfaces = {x['interface_id']: x for x in new_census['interfaces']}
    assert IID in progress['pending_interface_ids']
    for record in progress['completed']:
        iid = record['interface_id']
        assert old_interfaces[iid] == new_interfaces[iid], iid
        assert record['source_interface_sha256'] == item_sha(new_interfaces[iid]), iid
    for name in ['theorem-inventory.json', 'ranked-interfaces.json', 'source-relationships.json',
                 'interface-aliases.json', 'reconciliation.json', 'source-followups.json']:
        assert sha(AGG / name) == sha(HISTORY / name), name
    assert progress_path.read_bytes() == progress_bytes, 'Checkpoint changed; inspect and resume migration'
    for name in ['theorem-inventory.json', 'ranked-interfaces.json', 'source-relationships.json',
                 'interface-aliases.json', 'reconciliation.json', 'source-followups.json']:
        (AGG / name).write_bytes((WORK / name).read_bytes())
    progress.update(source_census_sha256=sha(AGG / 'ranked-interfaces.json'), updated_at=now)
    progress['source_amendments'] = progress.get('source_amendments', []) + [dict(
        paper_id=PID, local_id='D8', changed_interface_id=IID,
        old_census_sha256=sha(HISTORY / 'ranked-interfaces.json'),
        new_census_sha256=sha(AGG / 'ranked-interfaces.json'),
        preserved_reviewed_interfaces=len(progress['completed']),
        evidence=str(amendment.relative_to(ROOT)),
        preservation_check='Every completed source interface and its hash is unchanged; corrected D8 remains pending.')]
    temporary = progress_path.with_suffix('.source-amendment.tmp')
    save(temporary, progress)
    assert progress_path.read_bytes() == progress_bytes
    os.replace(temporary, progress_path)
    run('review_mathlib_checkpoint.py')
    subprocess.run([sys.executable, 'skills/statistical-paper-census/scripts/validate_census.py',
                    str(AGG / 'ranked-interfaces.json')], check=True)
    validation = read(AGG / 'validation.json')
    assert validation == read(HISTORY / 'validation.json')
    validation['checked_at'] = now
    validation['artifacts'] = {name: sha(AGG / name) for name in validation['artifacts']}
    validation['evidence'] = {name: sha(AGG / name) for name in validation['evidence']}
    validation['source_amendment'] = groups['source_amendment']
    save(AGG / 'validation.json', validation)
    save(AGG / 'p1716-source-amendment-validation.json', dict(status='passed', release_complete=False,
         checked_at=now, source_amendment=groups['source_amendment'],
         old_census_sha256=sha(HISTORY / 'ranked-interfaces.json'), new_census_sha256=sha(AGG / 'ranked-interfaces.json'),
         changed_interface_ids=[IID], changed_note_indices=changed_notes,
         preserved_mathlib_reviews=len(progress['completed']),
         checks=['Exactly one original source statement corrected', 'All 637 theorem statements unchanged',
                 'Every other interface unchanged', 'Group membership, ranks, edges and source relationships unchanged',
                 'Per-paper reproduction and highlight validation', 'Independent corpus preservation validation',
                 'Updated source-note triage', 'All completed mathlib source hashes preserved']))
    print('Source amendment propagated; unchanged reviewed interfaces preserved.')


if __name__ == '__main__':
    main()
