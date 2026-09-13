"""Record source review, independent validation and a persistent completion checkpoint."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());PDF=Path(prov['cached_pdf']);WORK=Path(prov['working_pdf']).parent
for n in ['theorem-inventory.json','ranked-interfaces.json']:subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/n)],check=True)
inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0];data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-conventions.json').read_text());review=json.loads((ROOT/'inventory-review.json').read_text())
assert digest(PDF)==paper['pdf_sha256']==prov['pdf_sha256']
assert digest(ROOT/'theorem-inventory.json')==review['inventory_sha256']
pdf=fitz.open(PDF);assert len(pdf)==85 and paper['main_text_last_pdf_page']==25
labels=[]
for n in range(25):
 text=pdf[n].get_text()
 labels.extend((n+1,m.group(1)) for m in re.finditer(r'^THEOREM\s+(\d+)\b',text,re.M))
expected=[(3,'1'),(10,'2'),(11,'3'),(11,'4'),(12,'5'),(13,'6'),(14,'7'),(15,'8'),(16,'9'),(16,'10'),(18,'11')]
assert labels==expected,labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==expected
assert [e['page'] for e in inv['claims'][3]['evidence']]==[11,12]
assert all('Proposition' not in c['label'] and 'Lemma' not in c['label'] for c in inv['claims'])
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=11,interfaces=37,source_members=37,direct_theorem_uses=80,related_theorem_connections=158,unranked_auxiliary_passages=14),counts
related={x['members'][0]['local_id']:{r['claim_id'].split('/T')[-1] for r in x['related_theorems']} for x in data['interfaces']}
assert related['D19']=={'2','3'} and related['D20']=={'4','5'}
assert related['D16']=={'2','3','9'} and related['D17']=={'4','5','10'}
assert related['D13']=={'2','4','5','10'} # Theorem 2's printed NR indicator is deliberate.
assert all(related[lid]=={'4','5'} for lid in ['D21NR','D22NR','D23NR'])
assert all(related[lid]=={'2','3','9','10'} for lid in ['D21','D22','D23'])
assert related['D25']=={'2','4','6','9'}
assert all(related[lid]=={'6','7'} for lid in ['D26','D27','D28','D29','D30'])
assert related['D31']=={'8'}
assert all(related[lid]=={'11'} for lid in ['D32','D33','D34'])
assert related['D6']=={'2','3','4','5','8','9','10'}
members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members};claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
assert set(claims['8']['depends_on'])=={'D31','D6'}
assert set(claims['11']['depends_on'])=={'D32','D33','D34'}
for lid in ['D5','D6','D7','D9','D10','D11','D12','D13','D14','D15','D16','D17','D18','D19','D20','D21','D22','D23','D24','D25','D31']:
 assert '11' not in related[lid],lid
for lid in ['D7','D9','D10','D11','D12','D13','D14','D15','D16','D17','D18','D19','D20','D21','D22','D23','D24']:
 assert not ({'6','7'}&related[lid]),lid
assert r'\frac{s_2\log(d)}N' in claims['2']['statement_original'] and r"s'_2:=" in claims['2']['statement_original']
assert r'\mu_{a,NR}^*\ne\mu_a' in claims['2']['statement_original']
assert r'g(\mathbf U^\top\boldsymbol\delta_c)' in byid['D18']['statement_original']
assert r'\sqrt{2t}' in claims['8']['statement_original']
for n in ['9','10']:
 assert r']^r\}^{1/r}' in claims[n]['statement_original']
 assert r'\left|' not in claims[n]['statement_original']
assert 'Assumptions 1-3' in claims['10']['statement_original'] and 'replaced' not in claims['10']['statement_original']
assert '\\tag{2.7}' in byid['D16']['statement_original']
assert byid['D28']['depends_on']==['D3']
assert byid['D31']['depends_on']==[]
assert set(byid['D33']['depends_on'])=={'D32'}
assert 'D12' not in byid['D13']['depends_on']
assert byid['D23NR']['statement_original']==byid['D23']['statement_original']
assert byid['D23NR'].get('application_context')
for item in data['claims']+members+ambient['auxiliary_passages']:
 for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',item['statement_original'],re.S):
  depth=0
  for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
   depth+=1 if b=='{' else -1
   assert depth>=0,('unbalanced braces',item)
  assert depth==0,('unbalanced braces',item)
for n in [1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,23,25]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
for n in ['supplement-heading-only','theorem2-notation','theorem8-probability','theorem9-moment','theorem10-moment','terminal-convention']:shutil.copy2(WORK/(n+'.png'),ROOT/'evidence'/(n+'.png'))
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=85,main_text_last_pdf_page=25,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Enumerate printed uppercase Theorem environments independently on PDF pages 1-25 and compare their source order with the saved inventory. Visually review full statements on pages 3, 10-16 and 18; include Theorem 4 continuation on page 12. Main references end on page 25 and the supplement title starts page 26.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],supplementary_material_used=False),counts=counts,
 validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
 'All eleven original theorem records remain identical to the independently validated source inventory. The final census pins the unchanged inventory SHA-256.',
 'Pinned source identity, title, authors, arXiv stamp, PDF page count and SHA-256 were checked. Main-text heading enumeration yields exactly Theorems 1-11; Lemma 1 and Proposition 1 are excluded from the theorem inventory.',
 'All 37 local source passages and 14 auxiliary passages were reviewed against main-text pages. The source algorithms retain outer cross-fitting, inner split/swap where present, both treatment paths and the variance outputs.',
 'The independent validator accepts the final census, local DAG, derived metrics, source identity, keyword names, selectors and source-backed explanations for all 158 related-theorem connections.',
 'Algorithm 1 reaches only Theorems 2-3; Algorithm 2 reaches only Theorems 4-5. The averaged DR component fit additionally reaches Theorem 9, and the nested component fit additionally reaches Theorem 10.',
 'General DR Theorems 6-7 do not acquire logistic/Lasso population projections or the sub-Gaussian Assumptions 2-3. Assumption 5 imports the residual definitions with general working models, not the full parametric tail hypothesis.',
 'Theorem 8 depends only on its separate generic imputed-Lasso setup and the shared Orlicz norm. Theorem 11 depends only on its multi-stage model, nuisance definitions and Assumption 6.',
 'Theorems 4-5 retain the explicit nested-model replacement in Assumption 2 via separate local application records. Theorem 10 lacks that instruction, so its literal reference and resulting ambiguity remain visible.',
 'Theorem 2 retains s2 versus s2-prime and the NR indicator. Theorems 9-10 retain the signed r-th powers, and the parametric score retains its delta_c subscript. Magnified source crops corroborate these details.',
 'Theorem 10 imports the rate expression of Theorem 9(c), without importing the correctness condition, Assumption 4 or the DR component-fit algorithm.',
 'Every interface has a natural-language source keyword and a meaning-bearing source selector, plus an explanation following its exact same-paper dependency path. All transcribed mathematical fragments have balanced braces.'
 ]),source_notes=[
 'The audit is source-specific to the May 2023 preprint associated with the 2024 corpus entry. Journal-version equality has not been assumed.',
 'Theorem 4 spans two pages; its complete s1-prime and s2-prime definitions were checked. Theorem 8 preserves both finite-probability and asymptotic bounds. Theorem 9 preserves all three rate branches.',
 'Displayed source discrepancies are archived separately without repairing the original statements. They are limitations for later formalization, not evidence that the paper census is incomplete.',
 'The introductory supplement text exposed by an earlier boundary crop is not used or retained as statement evidence. Only the supplement title crop documents that boundary.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,review_limits=['Source-fidelity and statement-dependency review, not certification of the mathematical proofs.','Embedded supplementary pages 26-85 are excluded from extraction and the final census.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
