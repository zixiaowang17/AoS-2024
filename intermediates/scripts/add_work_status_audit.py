#!/usr/bin/env python3
"""Add conservative binary next-action statuses to the completed research audit."""
import hashlib
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    root = Path(__file__).resolve().parents[1]
    aggregate = root / 'aggregate'
    snapshot = aggregate / 'before-work-status'
    snapshot.mkdir(exist_ok=True)
    files = ['audited.json', 'mathlib-search-progress.json', 'mathlib-validation.json',
             'mathlib-checkpoint-validation.json', 'html-verification.json',
             'html-reproduction-verification.json', 'html-regression-verification.json',
             'html-structure-verification.json']
    for name in files:
        target = snapshot / name
        if not target.exists():
            target.write_bytes((aggregate / name).read_bytes())
    old = (snapshot / 'audited.json').read_bytes()
    audit = json.loads(old)
    progress_path = aggregate / 'mathlib-search-progress.json'
    progress_raw = progress_path.read_bytes()
    progress = json.loads(progress_raw)
    assert progress['counts']['pending'] == 0
    reviewed = {r['interface_id']: r for r in progress['completed']}
    policy = {
        'id': 'verified-direct-reuse-v1',
        'use_mathlib': 'Direct reuse is verified for the complete interface and its recorded variants, under the stated domains and hypotheses.',
        'needs_work': 'Further assembly, formalization, source clarification, or verification of direct reuse is required.',
        'rule': 'A completed exact_reuse review establishes use_mathlib; all other completed reviews require more work or a final direct-reuse check.',
        'limits': 'This is a conservative next-action audit, not a claim that mathlib lacks an equivalent declaration; composable and partial matches do not establish absence.'
    }
    reasons = {
        'exact_reuse': 'Direct reuse is verified under the recorded hypotheses and domains.',
        'composable': 'Related components are available. Assembly or a final direct-reuse check remains; this status does not claim the interface is absent from mathlib.',
        'partial_match': 'The review establishes a partial match. Resolve the stated gap or verify a complete direct match before treating the interface as ready to use.',
        'no_verified_match': 'The completed search did not verify a matching declaration. Further library review, formalization, or source clarification is needed.'
    }
    rows = []
    for interface in audit['interfaces']:
        current = interface['library_audit']
        status = current['status']
        value = 'use_mathlib' if status == 'exact_reuse' else 'needs_work'
        before = dict(current)
        current.update(work_status=value, work_status_reason=reasons[status])
        stored = reviewed[interface['interface_id']]['library_audit']
        assert all(stored[k] == v for k, v in before.items())
        stored.update(work_status=value, work_status_reason=reasons[status])
        rows.append({'interface_id': interface['interface_id'], 'work_status': value,
                     'basis': status, 'reason': reasons[status], 'specific_gap': current['gap'],
                     'reviewed_audit_sha256': digest(json.dumps(before, sort_keys=True, ensure_ascii=False).encode())})
    audit['work_status_policy'] = policy
    progress['work_status_policy'] = policy
    now = datetime.now(timezone.utc).isoformat()
    progress['updated_at'] = now
    for path, data, expected in [(aggregate / 'audited.json', audit, old), (progress_path, progress, progress_raw)]:
        raw = path.read_bytes()
        if path.name == 'audited.json':
            assert raw == old or json.loads(raw).get('work_status_policy') == policy
        else:
            assert raw == expected
        temporary = path.with_suffix('.work-status.tmp')
        temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        assert path.read_bytes() == raw
        os.replace(temporary, path)
    result = {'status': 'complete', 'checked_at': now, 'policy': policy,
              'source_audit_sha256': digest(old), 'audited_sha256': digest((aggregate / 'audited.json').read_bytes()),
              'source_census_sha256': audit['source_census_sha256'],
              'counts': dict(Counter(r['work_status'] for r in rows)), 'interfaces': rows}
    (aggregate / 'work-status-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result['counts']))


if __name__ == '__main__':
    main()
