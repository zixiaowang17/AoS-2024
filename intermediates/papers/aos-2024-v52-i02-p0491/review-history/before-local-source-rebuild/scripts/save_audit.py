"""Record the completed source census only after independent validation."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());PDF=Path(prov['cached_pdf']);WORK=Path(prov['working_pdf']).parent
for name in ['theorem-inventory.json','ranked-interfaces.json']:
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],check=True)
inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-conventions.json').read_text());review=json.loads((ROOT/'inventory-review.json').read_text())
assert digest(PDF)==paper['pdf_sha256']==prov['pdf_sha256']
assert review['source_checked'] and review['status']=='complete'
assert digest(ROOT/'theorem-inventory.json')==review['inventory_sha256']
pdf=fitz.open(PDF)
assert len(pdf)==43 and paper['main_text_last_pdf_page']==24
assert paper['main_text_boundary']['shared_page_with_appendix'] is False
labels=[]
for n in range(24):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                if span['font']=='CMBX10':
                    m=re.fullmatch(r'Theorem (\d+\.\d+)',span['text'].strip())
                    if m:labels.append((n+1,m.group(1)))
assert labels==[(5,'1.2'),(9,'1.8'),(23,'5.1')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=3,interfaces=17,source_members=17,direct_theorem_uses=30,related_theorem_connections=37,unranked_auxiliary_passages=12),counts
members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members};claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
related={x['members'][0]['local_id']:{r['claim_id'].split('/T')[-1] for r in x['related_theorems']} for x in data['interfaces']}
assert all(related[lid]=={'1.2','1.8','5.1'} for lid in ['D1','D2','D3','D4','D5','D6','D7','D17'])
assert related['D8']=={'1.2'}
assert all(related[lid]=={'1.8','5.1'} for lid in ['D9','D10','D11','D13'])
assert all(related[lid]=={'5.1'} for lid in ['D12','D14','D15','D16'])
assert set(claims['1.2']['depends_on'])=={'D1','D2','D3','D5','D7','D8','D17'}
assert set(claims['1.8']['depends_on'])=={'D1','D2','D3','D5','D7','D9','D10','D11','D13','D17'}
assert set(claims['5.1']['depends_on'])=={'D1','D2','D3','D5','D7','D9','D10','D11','D13','D14','D15','D16','D17'}
assert byid['D7']['depends_on']==['D6']
assert byid['D16']['depends_on']==['D7','D15']
assert 'D7' not in byid['D14']['depends_on']
assert r'C_\tau\geq8\overline\sigma^2' in claims['1.2']['statement_original']
assert r'\min_{m\geq0}' in claims['1.2']['statement_original'] and r'\widehat F^{(m^o)}' in claims['1.2']['statement_original']
assert r'|\widehat\sigma^2-\|\varepsilon\|_n^2|\leq C_{Noise}' in claims['1.8']['statement_original']
assert r'c>0' in claims['1.8']['statement_original']
assert r'\widehat\sigma^2\leq\|\varepsilon\|_n^2+C\mathcal R' in claims['5.1']['statement_original']
assert r'c\geq0' in claims['5.1']['statement_original']
assert r'\tau_{two\text{-}step}\geq\widetilde m_{s,\gamma,G}' in claims['5.1']['statement_original']
assert r'On the corresponding event,' in claims['5.1']['statement_original']
assert r'\mid X_i' in byid['D3']['statement_original'] and r'\underline\sigma^2' in byid['D3']['statement_original']
assert r'\frac{X^{(j)}}{\|X^{(j)}\|_n}' in byid['D5']['statement_original']
assert r'\gamma\in[1,\infty)' in byid['D9']['statement_original']
assert r's\in\mathbb N_0' in byid['D9']['statement_original']
assert r'\|\Gamma_J^{-1}v_k\|_1<C_{Cov}' in byid['D11']['statement_original']
assert r'B_m^2:\ a=' in byid['D12']['statement_original']
assert r'\frac{\overline\sigma^2s\log p}n' in byid['D13']['statement_original']
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(e['page']<=24 for e in item['evidence'])
    for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',item['statement_original'],re.S):
        depth=0
        for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
            depth+=1 if brace=='{' else -1
            assert depth>=0,('unbalanced braces',item)
        assert depth==0,('unbalanced braces',item)
for n in [1,3,4,5,6,7,8,9,10,15,21,22,23,24]:
    shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
for name in ['appendix-heading-only','gamma-sparsity','population-bias-assignment']:
    shutil.copy2(WORK/(name+'.png'),ROOT/'evidence'/(name+'.png'))
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=43,main_text_last_pdf_page=24,provenance_path='evidence/source-provenance.json'),
    enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Main pages 1-24 searched and independently enumerated by bold CMBX10 Theorem heading spans. Only Theorems 1.2, 1.8 and 5.1 occur. Each complete statement fits on its recorded page. The main references end on page 24; a heading-only crop from page 25 establishes the Appendix A boundary.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Example','Remark'],appendix_material_used=False),counts=counts,
    validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
        'The original inventory passes an independent validator invocation and its hash matches the source review. The final census preserves all complete theorem records without renumbering or changes to their bodies.',
        'PDF title, author, arXiv v1 stamp, 43-page count and SHA-256 match the pinned source. Main text and references end before Appendix A on page 25; no appendix body is used.',
        'Theorem 1.2 preserves its chained oracle bound, minimum over nonnegative iterations, overbarred noise parameter and C_tau>=8 bar-sigma squared.',
        'Theorem 1.8 preserves the two-sided empirical-noise estimation condition and c>0; Theorem 5.1 preserves the one-sided condition, c>=0, sufficiently large AIC coefficient, lower bound on tau_two-step itself, and the risk conclusion on the corresponding event.',
        'All seventeen interface records were checked against the source. Algorithm 1 uses raw-column normalized correlations, and (1.8) uses the empirical noise estimate with an additive linear iteration threshold.',
        'Both (Sparse) branches retain all their conditions. The support bound, beta-min and little-o condition are distinct from gamma-sparsity and its subset inequality. Rate (1.20) and threshold iteration (3.2) preserve the matching branch.',
        'The local graph resolves empirical and population projections separately. Theorem 1.2 does not acquire (Sparse), (SubGD), (CovB), target rates, or population bias; Theorem 1.8 uses the population L2 norm without an artificial projector dependency.',
        'The lower-bound iteration (3.2) brings the population projector into Theorem 5.1. It depends on the OMP path and bias, not on the noise estimator mentioned in its introductory comparison. Additive AIC and prefix selection remain separate defining steps.',
        'Twelve auxiliary source passages preserve empirical/population norm conventions, coordinate notation, constant dependencies, common high-probability event scope, and source discrepancies. No proof-only balanced oracle or Scaled Lasso requirement is imported.',
        'The final census independently validates 30 direct theorem uses and 37 related-theorem connections. Source keywords and highlight selectors cover every record, and all theorem explanations trace explicit same-paper paths. Mathematical fragments have balanced braces.'
    ]),source_notes=[
        'This is a census of the pinned 2022 arXiv v1 paper, not a claim of textual equivalence with the journal publication.',
        'The source geometric empirical projection is retained despite the dimensionally inconsistent matrix formula (1.26). The malformed population-bias assignment and strict-versus-weak covariance restatement are archived without repair.',
        'Other unresolved source conventions include zero-column normalization, argmin ties, conditional-noise scope, population extension of rank-deficient fits, and empty-support/zeroth-power endpoints. These are source-fidelity notes rather than modifications to the theorems.',
        'The source\'s conditional-expectation interpretation of covariance regression and its claimed OMP greedy-decrease equivalence are recorded separately from the actual defining formulas.'
    ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
    review_limits=['Source-fidelity and statement-dependency audit, not proof certification or mathematical repair.','Appendix bodies on pages 25-43 excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
