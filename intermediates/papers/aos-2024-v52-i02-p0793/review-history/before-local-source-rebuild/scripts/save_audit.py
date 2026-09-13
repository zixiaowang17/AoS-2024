"""Independently check both statements, the main-text boundary and the complete local graph."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());PDF=Path(prov['cached_pdf']);WORK=Path(prov['working_pdf']).parent
for name in ['theorem-inventory.json','ranked-interfaces.json']:
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],check=True)
inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-conventions.json').read_text());review=json.loads((ROOT/'inventory-review.json').read_text())
assert digest(PDF)==paper['pdf_sha256']==prov['pdf_sha256']==digest(WORK/'source.pdf')
assert review['status']=='complete' and review['source_checked'] and digest(ROOT/'theorem-inventory.json')==review['inventory_sha256']
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==48
assert paper['main_text_last_pdf_page']==29 and not paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split());assert paper['title'] in first
for author in ['Edward H. Kennedy','Sivaraman Balakrishnan','James M. Robins','Larry Wasserman']:assert author in first
assert '2203.00837v4' in first and '23 Dec 2023' in first
assert paper['source_url']=='https://arxiv.org/pdf/2203.00837v4' and paper['version']=='arXiv:2203.00837v4'
assert 'Zimmert' in pdf[28].get_text() and 'Lechner' in pdf[28].get_text()
# Only the appendix heading itself is inspected; no appendix body is extracted here.
assert pdf[29].get_text(clip=fitz.Rect(0,0,pdf[29].rect.width,92)).strip()=='Appendices'
labels=[];plain_references=[]
for n in range(29):
    page=pdf[n];assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf-8')==page.get_text(),(n+1,'cached evidence differs')
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();match=re.match(r'Theorem (\d+)\.',text)
            if match:
                if line['spans'][0]['font']=='SFBX1095':labels.append((n+1,match.group(1)))
                else:plain_references.append((n+1,text))
assert labels==[(5,'1'),(24,'2')],labels
assert len(plain_references)==1 and plain_references[0][0]==24
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==2
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members};claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
reach={}
for n,c in claims.items():
    seen=set();stack=c['depends_on'][:]
    while stack:
        lid=stack.pop()
        if lid in seen:continue
        seen.add(lid);stack.extend(byid[lid]['depends_on'])
    reach[n]=seen
assert reach=={'1':{f'D{i}' for i in range(1,5)},'2':{f'D{i}' for i in range(1,13)}},reach
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
assert byid['D12']['source_kind']=='condition'
assert all(byid[lid]['source_kind']=='definition' for lid in ['D5','D6','D7','D8'])
assert not byid['D11']['depends_on'] or 'D7' not in byid['D11']['depends_on']
t1=claims['1']['statement_original'];t2=claims['2']['statement_original']
for snippet in [r'\inf_{\widehat\tau}\sup_{P\in\mathcal P}',r's\equiv(\alpha+\beta)/2',r'$f(x)$ is bounded above',r'constant depending on $(\alpha,\beta,\gamma,d)$']:assert snippet in t1,snippet
assert r'\sup_{P\in\mathcal P}' not in t2
assert r'\epsilon\leq\pi(x)\leq1-\epsilon' in t2 and r'\epsilon\leq\pi(x)' not in t1
for t in [t1,t2]:
    assert r'n^{-1/\left(1+\frac d{2\gamma}+\frac d{4s}\right)}' in t
    assert r'n^{-1/\left(2+\frac d\gamma\right)}' in t
    assert r's<\dfrac{d/4}{1+d/2\gamma}' in t
for snippet in [r'\|d\widehat F^*/dF^*\|_\infty',r'\frac d{4s}\vee\left(1+\frac d{2\gamma}\right)',r'\|\widehat Q^{-1}-Q^{-1}\|',r'\left(\frac d{2s}-\frac d\gamma\right)',r'$k\sim nh^d$',r'Definition 2']:assert snippet in t2,snippet
assert 'largest integer strictly smaller than' in byid['D4']['statement_original']
assert 'Euclidean norm' in byid['D4']['statement_original']
assert r'from distribution $\mathbb P$' in byid['D1']['statement_original']
assert r'\binom{d+\lfloor\gamma\rfloor}{\lfloor\gamma\rfloor}' in byid['D5']['statement_original']
assert r'(-1)^{\ell+m}\sqrt{2m+1}\binom m\ell\binom{m+\ell}\ell' in byid['D5']['statement_original']
assert r'\frac1{h^d}\mathbb 1(\|x-x_0\|\leq h/2)' in byid['D5']['statement_original']
assert r'\widehat\Omega=\int_{v\in[0,1]^d}' in byid['D7']['statement_original']
assert 'separate training sample $D^n$' in byid['D7']['statement_original']
assert r'A\{A-\widehat\pi(X)\}' in byid['D8']['statement_original']
assert r'K_h(X_2)\rho_h(X_1)^{\mathsf T}' in byid['D8']['statement_original']
assert r'K_h(X_2)\rho_h(X_2)^{\mathsf T}' in ambient['auxiliary_passages'][4]['statement_original']
assert r'dF^*(v)=dF(x_0+h(v-1/2))' in byid['D10']['statement_original']
assert r'\Omega^{-1}\int b(v)g^*(v)' in byid['D11']['application_context'][0]['text']
assert r'\|(I-\Pi_b)g\|_{F^*}\lesssim k^{-s/d}' in byid['D12']['statement_original']
assert r'\frac1{n(n-1)}\sum_{i\ne j}' in ambient['auxiliary_passages'][1]['statement_original']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=2,interfaces=12,source_members=12,direct_theorem_uses=14,related_theorem_connections=16,unranked_auxiliary_passages=10),counts
assert set(ambient['standard_ambient_resolution'])=={'shared','1','2'} and len(ambient['unresolved_source_conventions'])==23
math_fragments=0
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=29 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=29 for e in ctx['evidence']);fragments.append(ctx['text'])
    for text in fragments:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            math_fragments+=1;depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,('unbalanced braces',item)
            assert depth==0,('unbalanced braces',item)
assert math_fragments>100,math_fragments
for x in data['interfaces']:
    assert x['related_theorems'] and set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
    for m in x['members']:
        own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors) and all(s in linked for s in selectors)
    for k in x['source_keywords']:
        m=byid[k['local_id']];texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])];assert any(k['source_text'] in t for t in texts)
for n in [1,2,4,5,15,16,18,19,20,22,23,24,25,29]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
shutil.copy2(WORK/'appendix-heading-only.png',ROOT/'evidence/appendix-heading-only.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=48,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent inspection of bold SFBX1095 Theorem headings on pages 1-29 finds exactly Theorems 1 and 2. The plain-font line beginning Theorem 2 on page 24 is an explanatory reference. References end on page 29; the Appendix heading on page 30 marks the excluded boundary.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'The pinned title, four authors, arXiv v4 date stamp, 48-page count and source hash match the inspected PDF. Fresh extraction of pages 1-29 matches every cached evidence text.',
  'Theorem inventory and final census pass structural validation; the inventory review hash matches, and every original claim field survives unchanged.',
  'Both complete theorem statements were checked visually on pages 5 and 24, including all four lower-bound model conditions, A-C and numbered upper-bound conditions, exact strict elbow threshold, both tuning branches and both rates.',
  'The observed-data model, propensity and regressions, CATE, strict Hölder floor and derivative convention were checked on pages 2 and 4. Causal identifying assumptions remain separate from the statistical regression contrast.',
  'Definition 2 was checked on pages 15-16: local kernel, shifted Legendre coefficients, total-degree dimension q, correction basis b_hk, independently trained nuisances, estimated Gram integral, all four correction functions and both empirical/U-statistic aggregates.',
  'The Q-hat correction preserves rho_h(X_1)^T, despite the X_2 argument in the separate main-text bias formula. The treatment first-order correction remains raw A times its residual.',
  'The population weighted projection Q/R, transformed local measure, approximation property (6), and coordinate projection defining the population Omega convention were checked on pages 16,18-20. No normalization factor, integration-domain change or estimated nuisance requirement was added to the population projection.',
  'Independent graph traversal confirms that the lower-bound theorem reaches only the observed model, conditional functions, CATE and Hölder class. All estimator, basis, nuisance, transformed-measure and projection requirements belong to the upper bound.',
  'The theorem’s density-ratio sup-norm wording and ambiguous maximum grouping are preserved. The source’s expectation bound is not replaced by a high-probability claim, and its fixed-factor comparison is not changed to little-o.',
  'All 14 direct uses and 16 related connections have source-backed explanations and matching highlight selectors. Natural-language titles use exact source keywords and original source kinds.',
  'Ten auxiliary passages and twenty-three source-convention notes retain norms, ordered-pair normalization, nuisance-estimator caveats, smoothness-ordering prose, the correction mismatch and attainability limits. All math fragments have balanced braces.',
  'No appendix mathematics is used. The marginal-regression alternative in Appendix A and sufficient submodel conditions in Appendix B remain outside this main-text census.'
 ]),source_notes=[
  'The audited source is arXiv:2203.00837v4 dated 23 December 2023. Equality to the final journal wording has not been established.',
  'The lower bound concerns a broader model than the upper-bound guarantee. The two are not reported as a uniform matching result under only the lower-bound assumptions.',
  'The Q-hat polynomial argument, transformed-measure normalization, Euclidean-ball versus cube domain, density-ratio lower-bound wording and maximum grouping remain unresolved source conventions; quotations are not repaired.',
  'Omega’s population Gram interpretation follows the main-text projection formula; a standalone printed Gram definition and a fully specified nuisance-estimation implementation are not supplied in the inspected text.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Source transcription and statement-prerequisite audit, not proof certification or source repair.','Pinned preprint audited; equality to final journal wording is not established.','All appendix mathematics were excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
