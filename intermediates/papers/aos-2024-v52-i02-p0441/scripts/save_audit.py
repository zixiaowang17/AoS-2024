"""Complete the source audit only after independent census validation."""
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
pdf=fitz.open(PDF);assert len(pdf)==86 and paper['main_text_last_pdf_page']==25
labels=[]
for n in range(25):
 for b in pdf[n].get_text('dict')['blocks']:
  for line in b.get('lines',[]):
   for span in line['spans']:
    if span['font']=='NimbusRomNo9L-Medi':
     match=re.match(r'^Theorem (\d+\.\d+)$',span['text'].strip())
     if match:labels.append((n+1,match.group(1)))
assert labels==[(11,'4.2'),(20,'6.9')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=2,interfaces=12,source_members=12,direct_theorem_uses=14,related_theorem_connections=15,unranked_auxiliary_passages=11),counts
related={x['members'][0]['local_id']:{r['claim_id'].split('/T')[-1] for r in x['related_theorems']} for x in data['interfaces']}
assert all(related[lid]=={'4.2','6.9'} for lid in ['D1','D2','D3'])
assert all(related[lid]=={'4.2'} for lid in ['D4','D5','D6','D7'])
assert all(related[lid]=={'6.9'} for lid in ['D8','D9','D10','D11','D12'])
members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members};claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
assert set(claims['4.2']['depends_on'])=={'D1','D2','D3','D4','D5','D6','D7'}
assert set(claims['6.9']['depends_on'])=={'D1','D2','D3','D8','D9','D11','D12'}
assert byid['D7']['depends_on']==byid['D3']['depends_on']==byid['D12']['depends_on']==[]
assert byid['D8']['depends_on']==['D2']
assert r'\left(|y_i-' in claims['6.9']['statement_original']
assert r'\left(y_i-\boldsymbol\theta^\top\boldsymbol f_i+' in claims['6.9']['statement_original']
assert r'\nu^*' in claims['4.2']['statement_original'] and r'\nu_\star' in claims['4.2']['statement_original']
assert r'\max_{0\leq\beta,\gamma,\tau_q}\min_{0\leq\alpha,\tau_g}' in claims['4.2']['statement_original']
assert r'\frac\lambda{2(1-\lambda)}\gamma^2' in claims['4.2']['statement_original']
assert r'\sqrt{\mathbb E[\sigma^2(G)]-\mu_0^2-\mu_1^2}' in byid['D10']['statement_original']
assert r'\sqrt{\psi_{1,d}}+C' in byid['D8']['statement_original']
assert r'\cos^{-1}(\boldsymbol W\boldsymbol W^\top)' in byid['D9']['statement_original']
for item in data['claims']+members+ambient['auxiliary_passages']:
 for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',item['statement_original'],re.S):
  depth=0
  for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
   depth+=1 if b=='{' else -1
   assert depth>=0,('unbalanced braces',item)
  assert depth==0,('unbalanced braces',item)
for n in [1,4,10,11,12,15,16,17,18,19,20,22,25]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
for name in ['supplement-title','risk-limit','scalar-objective','comparison-objectives','activation-coefficients']:shutil.copy2(WORK/(name+'.png'),ROOT/'evidence'/(name+'.png'))
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=86,main_text_last_pdf_page=25,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Search main pages 1-25 and independently enumerate bold Theorem headings from PDF font spans. The only printed environments are Theorem 4.2 on page 11 and Theorem 6.9 on page 20; neither spans a page boundary. Main references end on page 25, before the supplementary title on page 26.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],supplementary_material_used=False),counts=counts,
 validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
 'Both complete original theorem statements remain unchanged from the source-reviewed inventory, with its SHA-256 pinned by the final census.',
 'PDF title, authors, arXiv stamp, page count and SHA-256 match the pinned provenance. Bold-heading enumeration independently confirms both printed theorem labels and their main-text pages.',
 'Theorem 4.2 retains the complete scalar objective, nested supremum, indicator, root equation, saddle-solution assertion, risk formula and probability-scope sentence. The source root-star positions and nonnegative optimization domain are preserved.',
 'Theorem 6.9 retains both positive-penalty objectives and the iff probability-limit conclusion. Its Phi_B formula lacks the absolute residual bars, as confirmed in the source crop.',
 'All twelve interface records and eleven auxiliary source passages were reviewed against main-text pages. The activation residual coefficient square root and J matrix formula were checked visually.',
 'The finalizer derives fourteen direct uses and fifteen related-theorem connections. A separate validator process accepts the original-statement handoff, graph, metrics, keywords, highlights and explanations.',
 'Only the data model, random features and shifted activation are shared between the two theorem dependency closures. Theorem 4.2 does not acquire the event E_W, J, Gaussian surrogate features or proof-specific constraint sets.',
 'Theorem 6.9 includes its explicit weight-matrix event and its section-wide dimensional limit convention. Its signal-normalization scope is recorded as a source limitation rather than silently importing Assumption 1(b).',
 'The nested scalar optimization variables and both Phi quantities remain inline definitions in their original theorem records; no synthetic definition or proof theorem was substituted for them.',
 'Every interface has literal natural-language source keywords, matching meaning-bearing selectors, and a source-backed explanation for every related theorem. Mathematical fragments have balanced braces.'
 ]),source_notes=[
 'This census is specific to the February 2024 preprint, not an assertion of equality with the journal typesetting.',
 'The theorem in the proof-outline section is included under the all-Theorems policy. Its supporting propositions, corollaries and lemmas are not separate theorem inventory entries.',
 'The source uses a superscript epsilon for the robust ERM coefficient vector. It uses a superscript star for the scalar root definition and a subscript star for the root in the final risk formula.',
 'The source limitations include Phi_B missing absolute-value bars, unspecified scalar boundary extensions, root-domain notation, signal-regime scope, and independence statements not explicitly supplied in the main-text definitions.',
 'No supplementary definitions or proof content is used in the census. The main-text notice and title crop document the supplement boundary and its differently worded title.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,review_limits=['Source-fidelity and statement-dependency audit, not proof certification or mathematical repair.','Supplementary pages 26-86 excluded; the complete main-text formula for S is retained without reading its appendix reference.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
