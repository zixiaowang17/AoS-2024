#!/usr/bin/env python3
"""Verify assessment coverage and preservation of the completed research audit.

This checks provenance and consistency, not the truth or proof cost of each estimate.
"""
import copy
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(value):return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
def main():
 root=Path(__file__).resolve().parents[1]/'aggregate';path=root/'audited.json'
 data=json.loads(path.read_text());original_path=root/'before-three-status/audited.json'
 original=json.loads(original_path.read_text());stripped=copy.deepcopy(data);previous=copy.deepcopy(original)
 policy=stripped.pop('work_status_policy');previous.pop('work_status_policy')
 assert policy['id']=='mathematical-work-v2'
 evidence=json.loads((root/'work-status-audit.json').read_text());rows={r['interface_id']:r for r in evidence['interfaces']}
 assert len(rows)==len(data['interfaces'])==2486
 counts=Counter()
 for interface,old in zip(stripped['interfaces'],previous['interfaces']):
  audit=interface['library_audit'];before=old['library_audit'];original_hash=canonical(before)
  decision=audit.pop('work_status');reason=audit.pop('work_status_reason');review=audit.pop('work_status_review')
  assert decision in {'use_mathlib','small_adaptation','new_infrastructure'} and reason.strip()
  assert all(isinstance(review.get(k),str) and review[k].strip() for k in ['basis','available','remaining','comparison_evidence','scope'])
  assert review['prior_review_sha256']==original_hash
  assert review['comparison_evidence']==audit['gap']
  assert review['variant_review_count']==len(interface['members'])
  row=rows[interface['interface_id']]
  assert (row['work_status'],row['reason'],row['specific_gap'],row['review'])==(decision,reason,audit['gap'],review)
  before.pop('work_status');before.pop('work_status_reason');before.pop('work_status_review',None)
  counts[decision]+=1
 assert stripped==previous,'Census or original library research changed beyond assessment fields'
 assert dict(counts)==evidence['counts'] and set(counts)=={'use_mathlib','small_adaptation','new_infrastructure'}
 assert evidence['source_audit_sha256']==sha(original_path) and evidence['audited_sha256']==sha(path)
 # A new work tier must not be a one-to-one renaming of legacy research categories.
 legacy={status:{x['library_audit']['work_status'] for x in data['interfaces'] if x['library_audit']['status']==status} for status in ['composable','partial_match','no_verified_match']}
 assert any(len(values)>1 for values in legacy.values())
 result={'status':'passed','checked_at':datetime.now(timezone.utc).isoformat(),'counts':dict(counts),'audit_sha256':sha(path),'source_audit_sha256':sha(original_path),'policy':policy,
 'checks':['Exactly one three-tier assessment for every interface','Original research, variants, searches, links and census preserved','Each assessment retains comparison evidence, available components, remaining work and scope','Prior-review hashes and per-variant coverage agree','Legacy research categories are not mechanically renamed'],
 'limits':'Consistency and provenance validation only. These are planning estimates from completed pinned evidence, not fresh searches or compiled proof-cost guarantees.'}
 (root/'work-status-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','counts':dict(counts)}))
if __name__=='__main__':main()
