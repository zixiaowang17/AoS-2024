"""Independent source enumeration, scope checks and validated census handoff."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text())
PDF=Path(prov['cached_pdf']);WORK=Path(prov['working_pdf']).parent
for name in ['theorem-inventory.json','ranked-interfaces.json']:
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],check=True)
inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
data=json.loads((ROOT/'ranked-interfaces.json').read_text())
ambient=json.loads((ROOT/'ambient-conventions.json').read_text())
review=json.loads((ROOT/'inventory-review.json').read_text())
assert digest(PDF)==paper['pdf_sha256']==prov['pdf_sha256']==digest(WORK/'source.pdf')
assert review['status']=='complete' and review['source_checked']
assert digest(ROOT/'theorem-inventory.json')==review['inventory_sha256']
pdf=fitz.open(PDF)
assert len(pdf)==86 and paper['main_text_last_pdf_page']==30
assert not paper['main_text_boundary']['shared_page_with_appendix']
assert '2208.10158v3' in pdf[0].get_text() and '16 Sep 2023' in pdf[0].get_text()
assert paper['source_url']=='https://arxiv.org/pdf/2208.10158v3'
assert prov['authors']==['Anne van Delft','Holger Dette']
assert any(entry[2]==31 and 'Preliminaries and inequalities' in entry[1] for entry in pdf.get_toc())
assert (ROOT/'evidence/appendix-heading-only.png').is_file()
# Enumerate only the thirty permitted main-text pages. No appendix body access.
labels=[]
for n in range(30):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                if span['font']=='Utopia-Bold':
                    match=re.fullmatch(r'Theorem (\d+\.\d+)\.',span['text'].strip())
                    if match:labels.append((n+1,match.group(1)))
expected=[(16,'3.1'),(18,'3.2'),(20,'3.3'),(20,'3.4'),(21,'3.5'),(21,'3.6'),(22,'4.1'),(22,'4.2'),(24,'4.3'),(24,'4.4'),(25,'4.5')]
assert labels==expected,labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=11,interfaces=41,source_members=41,direct_theorem_uses=204,related_theorem_connections=250,unranked_auxiliary_passages=15),counts
members=[m for x in data['interfaces'] for m in x['members']]
byid={m['local_id']:m for m in members}
claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
related={x['members'][0]['local_id']:{r['claim_id'].split('/T')[-1] for r in x['related_theorems']} for x in data['interfaces']}
# Verify source-derived boundaries between the generic theory and its four applications.
assert related['D25']=={'3.3'}
assert related['D26']==related['D27']=={'3.4'}
assert related['D28']==related['D29']=={'3.5'}
assert related['D30']==related['D31']==related['D32']=={'3.6'}
assert related['D3']=={'3.3','3.6'}
assert related['D19']==related['D20']==related['D21']==related['D22']==related['D23']=={'3.2','4.1','4.2','4.3','4.4','4.5'}
assert related['D24']=={'4.1','4.2'}
assert related['D35']==related['D36']==related['D38']=={'4.3','4.4','4.5'}
assert related['D39']==related['D40']=={'4.3','4.4'}
assert related['D41']=={'4.5'} and related['D34']==related['D37']=={'4.2'}
assert related['D18']==set(claims)
assert 'only' in next(x for x in data['interfaces'] if x['members'][0]['local_id']=='D18')['theorem_explanations'][PID+'/T3.2']['text'].lower()
# High-risk formula and hypothesis checks, based on the visually reviewed source.
assert claims['3.2']['evidence'][1]['page']==19
assert '(B.11)' in claims['3.1']['statement_original'] and '(B.12)' in claims['3.1']['statement_original']
assert r'p\geq6' in claims['3.1']['statement_original']
assert 'such that (3.30) holds' in claims['3.1']['statement_original']
assert r"0<\rho<1" in claims['3.1']['statement_original']
assert r"\phi'(cz)=h(c)\phi'(z)" in claims['3.1']['statement_original']
assert r'\overline{\big(g_{jj}' in claims['3.2']['statement_original']
assert r'\widehat{\mathscr D}^{\top}V_k^{-1}' in claims['3.2']['statement_original']
assert r'\lambda_{ii,1}^{(u,\omega)}>\ldots,\lambda_{ii,d}' in claims['3.5']['statement_original']
assert 'for some' not in claims['3.6']['statement_original']
assert r'\widehat r+q_{\alpha/2}V,\widehat r+q_{1-\alpha/2}V' in claims['4.1']['statement_original']
assert r'\alpha_T\to0' in claims['4.3']['statement_original']
assert r'\sum_{\ell\in\mathbb N}\sum_{k=0}^\infty' in byid['D6']['statement_original']
assert r'\frac1{\lfloor\eta N\rfloor}' in byid['D9']['statement_original']
assert r'V_{i,j}^2' in byid['D23']['statement_original'] and r'\overline{' in byid['D23']['statement_original']
assert r'\mathbb B_d\eta)' in byid['D38']['statement_original']
assert r'\widehat{\mathbb T}_d>q_\alpha' in byid['D40']['statement_original']
assert r'q_{1-\alpha,d_0}' in byid['D41']['statement_original']
assert set(ambient['standard_ambient_resolution'])=={'shared'}|set(claims)
assert len(ambient['unresolved_source_conventions'])==25
assert 'are equivalent under the strict definition' in next(x for x in ambient['unresolved_source_conventions'] if x['key']=='strict_threshold_boundary')['note']
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=30 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=30 for e in ctx['evidence'])
        fragments.append(ctx['text'])
    for text in fragments:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,('unbalanced braces',item)
            assert depth==0,('unbalanced braces',item)
for n in [1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,30]:
    shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=86,main_text_last_pdf_page=30,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent font-sensitive enumeration of the first 30 PDF pages identifies exactly the Utopia-Bold numbered Theorem headings 3.1-3.6 and 4.1-4.5. Plain-font mentions, Corollary 3.1 and other result types are excluded. References finish on page 30; the saved heading-only crop establishes a separate Appendix A on page 31. Appendix bodies were not read.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,
 validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'The source inventory and finalized census pass separate validator invocations. The pinned source-review inventory hash is unchanged, and all original theorem fields are preserved.',
  'The title, two authors, arXiv v3 stamp of 16 September 2023, versioned URL, 86-page count and PDF SHA-256 match the inspected source. All mathematical evidence is on main pages 1-30.',
  'All eleven theorem bodies were visually checked, including the full page-18-to-19 continuation of Theorem 3.2. Theorem 3.1 keeps both phi branches, all quantifiers, and unresolved appendix-only covariance references.',
  'All 41 local passages retain source types, natural-language source keywords, evidence, selectors and dependency reasons. Generic causal, spectral, calculus and self-normalization definitions are separate from the four application measures.',
  'All six numbered assumptions are retained in full. The nonlinear branch requires the actual consistency property (3.30), the coordinate tail (3.28) and analytic homogeneity; p=7 is not silently substituted.',
  'Corollary 3.1 is saved as a full inherited-hypothesis passage, without becoming a Theorem record. Theorem 3.2 and Section 4 inherit the applicable base branch, Frechet maps, factorization, scaling, positive-definite sigma and limiting nonsingularity.',
  'Both self-normalizer covariance formulas keep conjugation on the second factor. Theorem 3.2 retains ordinary transpose, squared-entry matrix notation, scalar roots, and its complete vector and scalar conclusions.',
  'PCA, separability, coherence and restricted stationarity definitions reach only their actual Gaussian-limit theorems. The generic Section 4 results do not acquire all application-specific prerequisites. Gaussian-limit statements do not acquire self-normalization merely from the subsequent pivotal-statistic comments.',
  'The original coherence ratio, marginal-eigenvalue chain punctuation, spectral multiplicity conventions, zero-spectrum issues and missing eta on the stationarity target remain visible as source issues.',
  'Model-selection hypotheses and rules retain the strict threshold, lower quantile in estimator (4.8), upper quantile in (4.11), and alpha_T-to-zero assertion. The equivalence of (4.9) and (2.17) is distinguished from the contradictory equality-at-d* discussion.',
  'Fifteen auxiliary passages resolve ambient notation and inherited source clauses; 25 separate notes record source discrepancies without modifying original statements. The graph has 204 direct uses and 250 deduplicated same-paper connections with explanations and matched selectors.',
  'Independent scope assertions verify that the first-exceedance estimator reaches Theorems 4.3/4.4 but not 4.5; the upper-quantile accuracy rule reaches 4.5 only. All quoted mathematical fragments have balanced TeX grouping braces.'
 ]),
 source_notes=[
  'This census audits the pinned arXiv v3 preprint; equality to journal typesetting has not been established.',
  'Appendix-only formulas (B.11)/(B.12), the precise moment-order recipe in Theorem C.3 and details of the square-root calculus remain unresolved under the required main-text-only scope.',
  'Source discrepancies are recorded as limitations of the original source. This is a statement-fidelity and dependency audit, not proof certification.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Main-text source-fidelity and statement-dependency review; does not repair or certify the proofs.','No appendix bodies or external supplements were used.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
