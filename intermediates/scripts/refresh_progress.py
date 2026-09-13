#!/usr/bin/env python3
"""Reconcile the complete corpus with independently validated per-paper artifacts."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import os
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path('skills/statistical-paper-census/scripts')
sys.path.insert(0, str(SKILL))
from validate_census import validate
from registered_source_gate import check_registered_source


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect_paper(paper, registered):
    pid = paper['paper_id']
    folder = ROOT / 'papers' / pid
    row = dict(paper_id=pid, title=paper['title'], issue=paper['issue'], status='queued',
               artifact_directory='papers/' + pid, theorem_count=None, api_count=None, errors=[])
    audit_path = folder / 'paper-audit.json'
    if not audit_path.exists():
        if (folder / 'checkpoint.json').exists():
            row['status'] = 'source_acquired'
        elif (folder / 'theorem-inventory.json').exists():
            row['status'] = 'incomplete'
        inventory_path = folder / 'theorem-inventory.json'
        review_path = folder / 'inventory-review.json'
        if inventory_path.exists() and review_path.exists():
            try:
                review = json.loads(review_path.read_text())
                inventory = json.loads(inventory_path.read_text())
                errors = validate(inventory_path)
                if review.get('paper_id') != pid or review.get('status') != 'complete':
                    errors.append('Inventory source review is incomplete or belongs to another paper')
                if review.get('inventory_sha256') != digest(inventory_path):
                    errors.append('Inventory bytes differ from the source-reviewed artifact')
                if [p.get('paper_id') for p in inventory.get('papers', [])] != [pid]:
                    errors.append('Inventory must contain exactly the assigned paper')
                if errors:
                    row['status'] = 'validation_failed'
                    row['errors'].extend(errors)
                else:
                    row['status'] = 'inventory_validated'
                    row['inventory_theorem_count'] = len(inventory['claims'])
            except (OSError, ValueError, KeyError, TypeError) as error:
                row['status'] = 'validation_failed'
                row['errors'].append(str(error))
        return row
    try:
        audit = json.loads(audit_path.read_text())
        if audit.get('paper_id') != pid or audit.get('status') != 'complete':
            row['status'] = 'incomplete'
            return row
        for name in ('theorem-inventory.json', 'ranked-interfaces.json'):
            path = folder / name
            row['errors'].extend(name + ': ' + e for e in validate(path))
            expected = audit.get('artifacts', {}).get(name, {}).get('sha256')
            if digest(path) != expected:
                row['errors'].append(name + ': current bytes differ from the reviewed artifact')
        census = json.loads((folder / 'ranked-interfaces.json').read_text())
        if [p.get('paper_id') for p in census['papers']] != [pid]:
            row['errors'].append('Census must contain exactly the assigned paper')
        if any(c.get('paper_id') != pid for c in census['claims']):
            row['errors'].append('Census contains another paper\'s theorem')
        for x in census['interfaces']:
            if any(m.get('paper_id') != pid for m in x['members']):
                row['errors'].append('Census contains another paper\'s source member')
        source = audit['source']
        for field in ('version', 'pdf_sha256', 'pdf_pages', 'source_url'):
            if source.get(field) != census['papers'][0].get(field):
                row['errors'].append('Reviewed source ' + field + ' differs from census')
        pdf = Path(source['pdf_path'])
        row['source_cached'] = pdf.is_file()
        if pdf.is_file() and digest(pdf) != source['pdf_sha256']:
            row['errors'].append('Cached source PDF differs from its reviewed hash')
        if audit.get('validation', {}).get('status') != 'passed':
            row['errors'].append('Missing completed source-audit validation record')
        if not row['errors']:
            row.update(status='complete', theorem_count=len(census['claims']),
                       api_count=len(census['interfaces']), audit_kind=audit['audit_kind'],
                       version=source['version'], audit_sha256=digest(audit_path),
                       census_sha256=digest(folder / 'ranked-interfaces.json'))
            row.update(check_registered_source(folder, audit, registered, ROOT.parents[1]))
        else:
            row['status'] = 'validation_failed'
    except (OSError, ValueError, KeyError, TypeError) as error:
        row['status'] = 'validation_failed'
        row['errors'].append(str(error))
    return row


def main():
    corpus = json.loads((ROOT / 'corpus.json').read_text())
    source = ROOT / corpus['source_inventory']['path']
    if digest(source) != corpus['source_inventory']['sha256']:
        raise ValueError('Pinned corpus source inventory changed')
    papers = corpus['papers']
    if len(papers) != 113 or len({p['paper_id'] for p in papers}) != 113:
        raise ValueError('Corpus must account for exactly113 distinct papers')
    expected = {p['paper_id'] for p in papers}
    register_path = ROOT.parents[1] / 'corpus/aos/2024/local-pdf-manifest.json'
    register = json.loads(register_path.read_text())
    registered = {p['paper_id']: p for p in register['papers']}
    if set(registered) != expected or len(register['papers']) != 113:
        raise ValueError('Local PDF register must match all 113 corpus paper IDs')
    unexpected = {p.name for p in (ROOT / 'papers').iterdir() if p.is_dir()} - expected
    if unexpected:
        raise ValueError('Unlisted paper artifact directories: ' + ', '.join(sorted(unexpected)))
    rows = [inspect_paper(p, registered[p['paper_id']]) for p in papers]
    counts = dict(collections.Counter(r['status'] for r in rows))
    state = dict(schema_version='aos-paper-audit-progress-v1', phase='paper_census',
                 required_paper_count=113, policy={'processing_order': 'one_paper_at_a_time',
                 'theorem_scope': 'main_text_only', 'appendices': 'excluded',
                 'completion_requires_registered_source_revalidation': True},
                 source_register={'path': str(register_path), 'sha256': digest(register_path)},
                 checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 next_paper_id=next((r['paper_id'] for r in rows if r['status'] != 'complete'), None),
                 counts=counts, papers=rows)
    fd, name = tempfile.mkstemp(prefix='.progress-', dir=ROOT)
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(json.dumps(state, ensure_ascii=False, indent=2)+'\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, ROOT / 'progress.json')
    finally:
        Path(name).unlink(missing_ok=True)
    print(json.dumps({'counts': counts, 'next_paper_id': state['next_paper_id']}))
    return 1 if counts.get('validation_failed') else 0


if __name__ == '__main__':
    raise SystemExit(main())
