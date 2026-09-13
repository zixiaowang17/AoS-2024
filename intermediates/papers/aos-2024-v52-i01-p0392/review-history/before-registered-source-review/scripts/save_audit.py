"""Record the completed source review and separately validated paper census."""
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
pdf=fitz.open(PDF);assert len(pdf)==26
labels=[]
for n,page in enumerate(pdf,1):
 for b in page.get_text('dict')['blocks']:
  for line in b.get('lines',[]):
   if any(s['text'].strip()=='Theorem' and s['font']=='CMCSC10' for s in line['spans']):
    match=re.search(r'Theorem\s+(\d+\.\d+)',''.join(s['text'] for s in line['spans']));assert match
    labels.append((n,match.group(1)))
assert labels==[(6,'2.1'),(9,'2.2'),(10,'2.3'),(16,'3.1'),(16,'3.2'),(16,'3.3'),(16,'3.4'),(23,'4.1'),(23,'4.2'),(23,'4.3'),(23,'4.4')]
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=11,interfaces=37,source_members=37,direct_theorem_uses=45,related_theorem_connections=100,unranked_auxiliary_passages=4),counts
related={x['members'][0]['local_id']:{t['claim_id'].split('/T')[-1] for t in x['related_theorems']} for x in data['interfaces']}
white={'3.1','3.2','3.3','3.4'};reg={'4.1','4.2','4.3','4.4'}
assert related['D2']=={'2.1','2.2','2.3'}|white
assert related['D20']==reg
assert all(related[lid]==white for lid in ['D11','D12','D13'])
assert all(related[lid]==reg for lid in ['D26','D27','D28','D29'])
assert related['D8']=={'2.1'}
assert related['D9']==white and related['D10']=={'3.1','3.2'}
assert related['D18']=={'3.4','4.4'}
assert related['D37']=={'3.2','3.4','4.2','4.4'}
assert related['D31']==related['D32']=={'4.2'}
assert related['D34']==related['D35']==related['D36']=={'4.4'}
assert related['D16']=={'3.3','3.4'}
assert related['D21']=={'4.2','4.4'}
for lid,num in [('D14','3.1'),('D15','3.2'),('D17','3.3'),('D19','3.4'),('D22','4.1'),('D23','4.3'),('D24','4.2'),('D25','4.4'),('D30','4.1'),('D33','4.3')]:assert related[lid]=={num}
members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members}
assert byid['D18']['depends_on']==byid['D37']['depends_on']==[]
assert r'Y_e(t)dt' in byid['D16']['statement_original']
assert r'dY_e(t)' not in byid['D16']['statement_original']
assert r'\frac{n+1}{2^{J-j-1}}' in byid['D27']['statement_original']
assert r'\widetilde X_{j,\widehat i_{\widehat j}+5}' in byid['D17']['statement_original']
assert r'\widehat{\mathtt i}' in byid['D28']['statement_original']
assert 'if $i_l=U$ then' in byid['D31']['statement_original'] and 'if $i_r=L-1$ then' in byid['D31']['statement_original']
assert 'if $I_{lo}=1$ then' in byid['D35']['statement_original'] and 'if $I_{hi}-1=n$ then' in byid['D35']['statement_original']
for item in data['claims']+members+ambient['auxiliary_passages']:
 for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',item['statement_original'],re.S):
  depth=0
  for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
   depth+=1 if b=='{' else -1
   assert depth>=0,('unbalanced braces',item)
  assert depth==0,('unbalanced braces',item)
for n in [1,2,3,6,7,9,10,12,13,14,15,16,17,18,19,20,21,22,23,25,26]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
for n in ['block-range-crop.png','regression-notation-crop.png']:shutil.copy2(WORK/n,ROOT/'evidence'/n)
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=26,main_text_last_pdf_page=26,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Search all 26 main-document pages and independently enumerate small-caps Theorem labels from PDF text spans. Visually inspect all statements on pages 6, 9, 10, 16 and 23, and the supplement pointer and reference endpoint on pages 25-26. No theorem crosses a page boundary.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],supplementary_material_used=False),counts=counts,
 validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
 'The eleven original theorem statements remain identical to the independently validated and source-reviewed inventory; its handoff hash is unchanged.',
 'PDF title, authors, arXiv stamp, SHA-256 and page count match the source provenance. Small-caps heading enumeration agrees with all eleven printed labels and their pages.',
 'All 37 interface passages and four unranked source conventions were checked against the main-text PDF. Both full regression algorithms are preserved, including boundary and fallback branches.',
 'The finalizer derives 45 direct uses and 100 related-theorem connections. A separate validator process accepts the inventory, graph, original statements, names, highlights, explanations and aggregate metrics.',
 'White-noise and regression observation models have disjoint theorem reach except for the shared function-class prerequisite. White-noise procedures reach only Theorems 3.1-3.4; regression procedures reach only Theorems 4.1-4.4.',
 'Theorem 2.3 uses arbitrary estimators and has no edge to the later adaptive procedures. The local-modulus interface reaches only Theorem 2.1; proof connections are not promoted to dependencies of Theorem 2.2.',
 'Gaussian-maximum quantiles and tail calibration constants have no observation-model prerequisite. Their cross-model reuse does not import white-noise assumptions into regression.',
 'Confidence benchmarks retain expected length at f alone, with coverage on the pair {f,g}; risk benchmarks retain sup_g inf_estimator max_h ordering. Discrete-design benchmarks are not replaced by white-noise approximations.',
 'Algorithm 1 reaches only Theorem 4.2; Algorithm 2 reaches only Theorem 4.4. Conditional use remains explicit in the surrounding original interval definitions.',
 'The minimum process integral, mixed j indexing and regression block-count exponent are preserved. A magnified crop and PDF glyph baselines distinguish the exponent J-j-1 from a subtraction outside the power.',
 'Every interface has source keywords and meaningful selectors matching its passage, label or related same-paper theorem, plus a source-backed explanation for each related theorem. All mathematical fragments have balanced braces.']),
 source_notes=[
 'This audit is specific to the pinned March 2024 preprint. The separate supplementary document containing proofs and technical lemmas was excluded.',
 'Theorem 2.1 retains all four bounds and constants; Theorem 2.2 retains 274 and 3^7; Theorem 3.2 retains (24 times 2^K_alpha minus 3) times 17.5. The exact alpha placement and constant declarations in the remaining Theorems are preserved.',
 'Source bar-X uses the ordinary integral Y_e(t) dt, not dY_e(t). The shift defining the white-noise minimum estimator contains two un-hatted j indices. Neither is corrected.',
 'The regression block count prints denominator 2^(J-j-1), whereas localization uses 2^(J-j). Font-level inspection confirms the complete exponent. The two formulas remain distinct.',
 'Regression selectors use circumflex-accented typewriter letters. The transcription keeps them distinct from white-noise italic selectors and from the caron-accented no-trigger variable.',
 'Unspecified out-of-domain minimum blocks, coarse-level block-count equality, partial regression blocks, small-n algorithm domains, argmin totality and gamma positivity are retained as explicit source notes.'],
 unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,review_limits=['Source fidelity and statement-dependency audit, not proof certification or mathematical repair.','All findings are specific to the pinned preprint; separate supplementary material was excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
