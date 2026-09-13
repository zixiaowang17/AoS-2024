#!/usr/bin/env python3
"""Record completion only after corpus, audit, rendering and browser checks pass."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    aggregate = root / 'aggregate'
    records = {}
    for name in ['mathlib-validation.json', 'html-regression-verification.json',
                 'html-reproduction-verification.json', 'html-structure-verification.json']:
        records[name] = json.loads((aggregate / name).read_text())
        assert records[name]['status'] == 'passed', name
    browser_path = root / 'tooling/renderer-review/final-browser/verification.json'
    browser = json.loads(browser_path.read_text())
    assert browser['status'] == 'passed' and browser['visual_inspection']['status'] == 'passed'
    assert browser['report_sha256'] == sha(aggregate / 'report.html')
    progress = json.loads((aggregate / 'mathlib-search-progress.json').read_text())
    assert progress['status'] == 'complete' and progress['counts'] == {'total': 2486, 'reviewed': 2486, 'pending': 0}
    assert records['mathlib-validation.json']['progress_sha256'] == sha(aggregate / 'mathlib-search-progress.json')
    assert records['mathlib-validation.json']['audit_sha256'] == sha(aggregate / 'audited.json')
    structure = records['html-structure-verification.json']
    assert structure['report_sha256'] == sha(aggregate / 'report.html')
    assert records['html-reproduction-verification.json']['report_sha256'] == sha(aggregate / 'report.html')
    assert structure['audit_sha256'] == sha(aggregate / 'audited.json')
    for name, digest in structure['reader_sha256'].items():
        assert sha(aggregate / structure['generation'] / name) == digest
    census = json.loads((aggregate / 'validation.json').read_text())
    assert census['status'] == 'passed'
    for name, digest in census['artifacts'].items():
        assert sha(aggregate / name) == digest, name
    paper_review = json.loads((root / 'audit-record-review.json').read_text())
    assert paper_review['counts'] == {'passed': 113, 'needs_repair': 0, 'pending_paper_census': 0}
    triage = json.loads((aggregate / 'source-note-triage-validation.json').read_text())
    assert triage['status'] == 'passed' and triage['counts']['pending_items'] == 0
    now = datetime.now(timezone.utc).isoformat()
    amendment_path = root / 'tooling/renderer-review/rank-column-amendment.json'
    amendment = json.loads(amendment_path.read_text())
    work_amendment_path = root / 'tooling/renderer-review/work-status-amendment.json'
    work_amendment = json.loads(work_amendment_path.read_text())
    assert work_amendment['assets']['report.css']['before_sha256'] == amendment['after_sha256']
    columns_amendment_path = root / 'tooling/renderer-review/api-columns-amendment.json'
    columns_amendment = json.loads(columns_amendment_path.read_text())
    columns_browser_path = root / 'tooling/renderer-review/api-columns/final-verification.json'
    columns_browser = json.loads(columns_browser_path.read_text())
    assert columns_browser['status'] == 'passed' and columns_browser['visual_inspection']['status'] == 'passed'
    assert columns_browser['report_sha256'] == sha(aggregate / 'report.html')
    assert columns_amendment['audit_sha256'] == sha(aggregate / 'before-three-status/audited.json')
    resize_amendment_path = root / 'tooling/renderer-review/resizable-pane-amendment.json'
    resize_amendment = json.loads(resize_amendment_path.read_text())
    resize_browser_path = root / 'tooling/renderer-review/resizable-pane/final-verification.json'
    resize_browser = json.loads(resize_browser_path.read_text())
    assert resize_browser['status'] == 'passed' and resize_browser['visual_inspection']['status'] == 'passed'
    assert resize_browser['report_sha256'] == sha(aggregate / 'report.html')
    assert resize_amendment['audit_sha256'] == sha(aggregate / 'before-three-status/audited.json')
    three_path = root / 'tooling/renderer-review/three-status-amendment.json'
    three = json.loads(three_path.read_text())
    assert three['audit_sha256'] == sha(aggregate / 'audited.json')
    for name, asset in three['assets'].items():
        assert asset['before_sha256'] == resize_amendment['assets'][name]['after_sha256']
        assert asset['after_sha256'] == sha(Path(asset['path']))
    three.update(status='passed', checked_at=now)
    three_path.write_text(json.dumps(three, indent=2) + '\n')
    work_validation_path = aggregate / 'work-status-validation.json'
    work_validation = json.loads(work_validation_path.read_text())
    assert work_validation['status'] == 'passed'
    assert work_validation['audit_sha256'] == sha(aggregate / 'audited.json')
    assert all(x['all_reference_rows_unchanged'] for x in amendment['reference_row_geometry'])
    amendment.update(status='passed', checked_at=now)
    amendment_path.write_text(json.dumps(amendment, indent=2) + '\n')
    work_amendment.update(status='passed', checked_at=now)
    work_amendment_path.write_text(json.dumps(work_amendment, indent=2) + '\n')
    columns_amendment.update(status='passed', checked_at=now)
    columns_amendment_path.write_text(json.dumps(columns_amendment, indent=2) + '\n')
    resize_amendment.update(status='passed', checked_at=now)
    resize_amendment_path.write_text(json.dumps(resize_amendment, indent=2) + '\n')
    evidence_paths = [root / 'audit-record-review.json', aggregate / 'validation.json',
                      aggregate / 'source-note-triage-validation.json', browser_path, amendment_path,
                      work_amendment_path, three_path, columns_amendment_path, columns_browser_path, resize_amendment_path, resize_browser_path, work_validation_path, aggregate / 'work-status-audit.json',
                      *[aggregate / name for name in records]]
    result = {
        'status': 'passed', 'release_complete': True, 'checked_at': now,
        'counts': structure['counts'], 'report': 'report.html', 'generation': structure['generation'],
        'report_sha256': sha(aggregate / 'report.html'),
        'source_census_sha256': sha(aggregate / 'ranked-interfaces.json'),
        'audit_sha256': sha(aggregate / 'audited.json'),
        'evidence_sha256': {str(p.relative_to(root)): sha(p) for p in evidence_paths},
        'style': 'Approved two-paper reading style preserved with separate Theorems / Papers and Status columns, user-requested green/yellow/red status buttons and About ranking definitions and responsive count/status cells and an adjustable reading pane; desktop/mobile appearance and interactions verified.',
        'work_status_counts': work_validation['counts'],
        'limits': 'Source ambiguities and scoped library gaps remain documented; this census does not certify source proofs or compile the inspected Lean types.'
    }
    (aggregate / 'html-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    baseline_path = root / 'tooling/renderer-review/approved-baseline-recheck.json'
    recheck = json.loads(baseline_path.read_text())
    recheck.pop('reference_css_preserved_except_rank_column', None)
    recheck.update(checked_at=now, final_report_verified=True,
                   scope='Pinned reference preserved; final appearance and interactions passed with reviewed API count/status columns and green/yellow/red status labels.',
                   reference_embedded_css_matches=False,
                   reference_css_preserved_except_rank_column_and_work_status=True,
                   three_status_amendment='tooling/renderer-review/three-status-amendment.json',
                   resizable_pane_amendment='tooling/renderer-review/resizable-pane-amendment.json',
                   api_columns_amendment='tooling/renderer-review/api-columns-amendment.json',
                   work_status_amendment='tooling/renderer-review/work-status-amendment.json',
                   reviewed_amendment='tooling/renderer-review/rank-column-amendment.json',
                   final_verification='aggregate/html-verification.json')
    baseline_path.write_text(json.dumps(recheck, indent=2) + '\n')
    workflow_path = root / 'reviewed-html-workflow.json'
    old = workflow_path.read_bytes()
    workflow = json.loads(old)
    assert all(p['status'] == 'complete' for p in workflow['phases'] if p['id'] != 'html')
    for repair in workflow['required_repairs']:
        if repair.get('component') == 'statistical-census-html/assets/report.css rank columns':
            repair['status'] = 'complete'
    assert all(p['status'] == 'complete' for p in workflow['required_repairs'])
    html = next(p for p in workflow['phases'] if p['id'] == 'html')
    html.update(status='complete', evidence='aggregate/html-verification.json',
                progress=structure['counts'])
    workflow.update(updated_at=now, status='complete', current_phase='complete',
                    next_action=None, blockers=[], active_checks=[],
                    completion_evidence='aggregate/html-verification.json')
    temporary = workflow_path.with_suffix('.html-release.tmp')
    temporary.write_text(json.dumps(workflow, ensure_ascii=False, indent=2) + '\n')
    assert workflow_path.read_bytes() == old
    os.replace(temporary, workflow_path)
    print(json.dumps({'status': 'complete', 'report': str(aggregate / 'report.html'), 'counts': structure['counts']}))


if __name__ == '__main__':
    main()
