#!/usr/bin/env python3
"""Publish the complete reviewed audit without changing its frozen source census."""
import copy
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    aggregate = root / 'aggregate'
    progress_path = aggregate / 'mathlib-search-progress.json'
    progress_bytes = progress_path.read_bytes()
    progress = json.loads(progress_bytes)
    checkpoint = json.loads((aggregate / 'mathlib-checkpoint-validation.json').read_text())
    assert checkpoint['status'] == 'passed'
    assert checkpoint['progress_sha256'] == sha(progress_bytes)
    assert not progress['pending_interface_ids'] and progress['counts']['pending'] == 0
    census_path = aggregate / 'ranked-interfaces.json'
    census_bytes = census_path.read_bytes()
    assert sha(census_bytes) == progress['source_census_sha256']
    census = json.loads(census_bytes)
    records = {r['interface_id']: r for r in progress['completed']}
    assert len(records) == len(progress['completed']) == len(census['interfaces'])
    audited = copy.deepcopy(census)
    audited.update(schema_version='ranked-mathlib-audit-v4',
                   source_census_sha256=sha(census_bytes),
                   mathlib_revision=progress['mathlib_revision'],
                   lean_version=progress['lean_version'])
    if 'work_status_policy' in progress:
        audited['work_status_policy'] = progress['work_status_policy']
    for interface in audited['interfaces']:
        interface['library_audit'] = records[interface['interface_id']]['library_audit']
    target = aggregate / 'audited.json'
    temporary = aggregate / '.audited.release.tmp.json'
    temporary.write_text(json.dumps(audited, ensure_ascii=False, indent=2) + '\n')
    validator = root / 'tooling/skills/ranked-mathlib-audit/scripts/validate_audit.py'
    command = [sys.executable, str(validator), str(temporary), '--census', str(census_path)]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    assert progress_path.read_bytes() == progress_bytes and census_path.read_bytes() == census_bytes
    if target.exists():
        assert target.read_bytes() == temporary.read_bytes(), 'Existing release differs'
        temporary.unlink()
    else:
        os.replace(temporary, target)
    now = datetime.now(timezone.utc).isoformat()
    evidence = {
        'status': 'passed', 'checked_at': now, 'audit_complete': True,
        'html_release_complete': False, 'counts': progress['counts'],
        'source_census_sha256': sha(census_bytes), 'audit_sha256': sha(target.read_bytes()),
        'progress_sha256': sha(progress_bytes), 'verified_used_links': checkpoint['verified_used_links'],
        'mathlib_revision': progress['mathlib_revision'], 'lean_version': progress['lean_version'],
        'validator': str(validator), 'validator_sha256': sha(validator.read_bytes()),
        'validator_exit_code': result.returncode, 'validator_output': result.stdout.strip(),
        'checks': ['No pending interfaces', 'All per-variant comparisons retained in checkpoint',
                   'Only library_audit added to each ordered census interface',
                   'Pinned inventory and source census validated by companion validator',
                   'All declaration links backed by checkpoint-verified source evidence'],
        'limits': 'Records preserve printed ambiguities and scoped mathematical comparisons; validation does not certify source proofs or compile the manually inspected Lean types.'
    }
    (aggregate / 'mathlib-validation.json').write_text(json.dumps(evidence, indent=2) + '\n')
    workflow_path = root / 'reviewed-html-workflow.json'
    old = workflow_path.read_bytes()
    workflow = json.loads(old)
    phase = next(p for p in workflow['phases'] if p['id'] == 'mathlib_audit')
    phase.update(status='complete', progress=progress['counts'], next_interface=None,
                 evidence='aggregate/mathlib-validation.json')
    next(p for p in workflow['phases'] if p['id'] == 'html')['status'] = 'in_progress'
    workflow.update(updated_at=now, current_phase='html',
                    next_action='Generate and verify the full HTML against the approved two-paper baseline, including all routes and representative desktop/mobile interactions.')
    temp_workflow = workflow_path.with_suffix('.release.tmp')
    temp_workflow.write_text(json.dumps(workflow, ensure_ascii=False, indent=2) + '\n')
    assert workflow_path.read_bytes() == old
    os.replace(temp_workflow, workflow_path)
    print(json.dumps({'audit': str(target), 'counts': progress['counts'], 'status': 'passed'}))


if __name__ == '__main__':
    main()
