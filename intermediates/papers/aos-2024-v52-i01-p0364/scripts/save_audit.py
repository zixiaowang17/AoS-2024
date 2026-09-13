"""Validate the inspected source inventory, local census and independent recovery checkpoint."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());PDF=Path(prov['cached_pdf']);WORK=Path(prov['working_pdf']).parent
for n in ['theorem-inventory.json','ranked-interfaces.json']:subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/n)],check=True)
inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-conventions.json').read_text());review=json.loads((ROOT/'inventory-review.json').read_text())
assert digest(PDF)==paper['pdf_sha256']==prov['pdf_sha256']
assert digest(ROOT/'theorem-inventory.json')==review['inventory_sha256']
pdf=fitz.open(PDF);assert len(pdf)==80
labels=[]
for n in range(38):
 for b in pdf[n].get_text('dict')['blocks']:
  for line in b.get('lines',[]):
   for span in line['spans']:
    match=re.match(r'Theorem (\d+)\.',span['text'])
    if match and 'BX' in span['font']:labels.append((n+1,match.group(1)))
assert labels==[(10,'1'),(13,'2'),(15,'4'),(20,'6'),(21,'7'),(23,'8'),(24,'9')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert paper['main_text_last_pdf_page']==38
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=7,interfaces=25,source_members=25,direct_theorem_uses=78,related_theorem_connections=103,unranked_auxiliary_passages=10),counts
related={x['members'][0]['local_id']:{t['claim_id'].split('/T')[-1] for t in x['related_theorems']} for x in data['interfaces']}
assert related['D6']=={'1','2'}
assert related['D9']==related['D10']=={'1'}
assert related['D16']==related['D17']==related['D18']=={'4','6','7','9'}
assert related['D21']=={'6','7','9'}
assert related['D22']==related['D23']=={'8','9'}
assert related['D24']==related['D25']=={'9'}
assert related['D20']=={'6','7','8','9'}
assert related['D13']=={'4'}
assert all('8' not in related[lid] for lid in ['D3','D5','D6','D7','D8','D15','D16','D17','D18','D21'])
claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
assert set(claims['8']['depends_on'])=={'D2','D4','D22','D23'}
members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members}
assert byid['D14']['depends_on']==['D12','D11']
assert all(PID+'/T2' in byid[lid]['theorem_application_contexts'] for lid in ['D2','D3','D4','D5','D6','D15'])
assert r'd_k=O(g_s)=(r_e+\sqrt T)S_\psi^{(k)}' in claims['6']['statement_original']
assert r'd_{-k,}^2' in claims['4']['statement_original']
assert r'\operatorname{rank}(\ddot{\mathbf H}_k)=z_k' in claims['2']['statement_original']
assert r'\operatorname{mat}_k(\mathcal X_t-\overline{\mathcal X})\check{\mathbf q}_k^{(i-1)}' in byid['D20']['statement_original']
for item in data['claims']+members+ambient['auxiliary_passages']:
 for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',item['statement_original'],re.S):
  depth=0
  for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
   depth+=1 if brace=='{' else -1
   assert depth>=0,('unbalanced braces',item)
  assert depth==0,('unbalanced braces',item)
for n in [1,4,5,6,7,8,9,10,12,13,14,15,17,18,19,20,21,22,23,24,38]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=80,main_text_last_pdf_page=38,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Search all 38 main-text pages and independently enumerate printed bold Theorem headings. Visually inspect all statement pages and both continuations. Main text ends after the portfolio discussion on page 38; a heading-only crop confirms the appendix starts on page 39.',bold_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],supplementary_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
 'The seven original statements match the separately validated and source-reviewed inventory; its hash remains unchanged at handoff.',
 'PDF page count, SHA-256, source title, authors and pinned arXiv version were checked against the cached source.',
 'Independent bold-font enumeration agrees with the original labels 1, 2, 4, 6, 7, 8 and 9. Theorems 2 and 8 include their page continuations.',
 'All 25 interfaces and ten unranked auxiliary passages were checked against main-text source passages; no appendix body was used.',
 'The finalizer derives the local graph, ranking metrics and relationship paths. A separate validator process accepts 78 direct uses and 103 related-theorem connections.',
 'Full-sum L2 reaches only Theorems 1 and 2, with explicit sample-wise application context for Theorem 2. L2-prime, R2 and selected-scale comparability reach only Theorems 4, 6, 7 and 9.',
 'Theorem 8 retains only E1, F1 and RE2 as explicit hypotheses. Its defined direction reaches the projection and pre-averaging procedures, without importing the assumptions used to prove their convergence.',
 'L1-prime is attached to the final clauses of Theorems 1, 2 and 4 and retained by all-assumptions imports in Theorems 6, 7 and 9.',
 'RE1 reaches only Theorems 6, 7 and 9; RE2 and the population-style covariance reach only Theorems 8 and 9. Sample correlation and threshold rank estimation reach only Theorem 9.',
 'Every interface has exact source keywords, a faithful source-kind label, meaningful highlight selectors and source-backed explanations for every related theorem. Selectors match archived passages, source labels or related same-paper theorem statements.',
 'All theorem symbols are bound inline, resolved to interfaces or recorded in ambient resolution; source ambiguities are explicitly retained rather than repaired. Mathematical fragments have balanced braces.']),
 source_notes=[
 'The audit is specific to the August 2022 preprint; identity with the 2024 journal version has not been established.',
 'Theorem 2 prints H-double-dot-k rather than H-double-dot-k-pre inside rank; Theorem 4 prints a trailing comma in a subscript; Theorem 6 prints an unusual chained equality. All are preserved.',
 'Theorem 7 retains both nested powers and both g_s factors in its rate. Theorem 9 ends at the consistency sentence; subsequent upright pervasive-factor rate simplifications are excluded from its statement.',
 'The original projection algorithm uses q_k in step 2, unlike the q_-k construction in its preceding equations. Both passages are retained and the dimensional mismatch is documented.',
 'Unindexed r and d were not explicitly defined in the inspected main text. The appendix-only tensor indexing conventions and the RE1 trace-square interpretation remain unresolved.',
 'Theorem 6 inline rate hypotheses are archived as an unranked reference for Theorems 7 and 9, avoiding invented names for a new interface.',
 'The fixed-direction covariance formula is not promoted to an actual conditional expectation given a data-dependent direction. No unprinted factor-noise independence is inserted.'],
 unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Source and statement-dependency audit, not proof certification or mathematical repair.','This census uses the pinned preprint and excludes appendices; unresolved source conventions remain visible.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
