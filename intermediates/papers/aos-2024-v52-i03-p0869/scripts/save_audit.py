"""Independently check inventory, source correspondence and the paper-local dependency graph."""
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
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==80
assert paper['main_text_last_pdf_page']==27 and not paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split());assert paper['title'] in first
for author in ['Filippo Ascolani','Giacomo Zanella']:assert author in first
assert '2304.06993v2' in first and '30 Oct 2023' in first and 'October 31, 2023' in first
assert paper['source_url']=='https://arxiv.org/pdf/2304.06993v2' and paper['version']=='arXiv:2304.06993v2'
assert '[69]' in pdf[26].get_text() and '1751–1784' in pdf[26].get_text()
assert pdf[27].get_text(clip=fitz.Rect(0,0,pdf[27].rect.width,95)).startswith('Appendix A')
labels=[];plain_references=[]
for n in range(27):
    page=pdf[n];assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf-8')==page.get_text(),(n+1,'cached evidence differs')
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();match=re.match(r'Theorem (\d+(?:\.\d+)*)(?=[.\s(])',text)
            if match:
                if line['spans'][0]['font']=='CMBX10':labels.append((n+1,match.group(1)))
                else:plain_references.append((n+1,text))
assert labels==[(7,'2.4'),(9,'3.1'),(12,'4.2'),(22,'6.1')],labels
assert len(plain_references)==1 and plain_references[0][0]==18
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==4
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
expected={'2.4':[1,2,3,4],'3.1':[5,6,7],'4.2':[3,6,8,9,10,11,12,13,14,15,16,17],'6.1':[6,8,9,10,11,13,14,15,16,17,18,19]}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
assert reach['3.1'].isdisjoint({'D1','D2','D3','D4','D10','D11','D12'})
assert reach['6.1'].isdisjoint({'D3','D12'})
assert reach['4.2'].isdisjoint({'D1','D2','D4','D18','D19'})
assert byid['D7']['source_kind']=='theorem_excerpt'
for lid,label in [('D4','(A1)'),('D14','(B1)'),('D15','(B2)'),('D17','(B3)')]:
    assert byid[lid]['source_kind']=='assumption' and byid[lid]['source_heading']==label
for lid in ['D1','D5','D9']:assert byid[lid]['source_kind']=='source_passage'
t24=claims['2.4']['statement_original'];t31=claims['3.1']['statement_original'];t42=claims['4.2']['statement_original'];t61=claims['6.1']['statement_original']
assert 'Let assumption (A1) holds.' in t24 and r't\in\mathbb N' in t24 and 'Q^{(n)}' in t24
assert t24.count(r'\sup_')==2 and r'\mathcal N(\widetilde\pi,M)' in t24
assert r'\sup_{\psi\notin\Psi}' in t31 and r'\tag{12}' in t31
assert r'N(\mathcal I^{-1}(\psi^*)\Delta_{n,\psi^*},\mathcal I^{-1}(\psi^*))' in t31
assert r'\widetilde\psi=\sqrt n(\psi-\psi^*)' in t31 and r'\nabla\log f(Y_i\mid\psi)' in t31
assert 'continously differentiable' in t31 and 'continuous positive density' in t31
assert '(B1)-(B6)' in t42 and r'\mathcal O_P(1)' in t42
assert r'\liminf_{J\to\infty}' in t61 and r'\to1\qquad\text{as }J\to\infty' in t61
assert r't_{mix}^{(J)}(\epsilon,\mu_J)' in t61 and r'\mathbb R^{lJ+D}' in t61
assert r'i=1,\ldots,n' in byid['D2']['statement_original'] and r'P_{n,1}\cdots P_{n,K}' in byid['D2']['statement_original']
assert r'\mu(A)\leq M\pi(A)' in byid['D3']['statement_original']
assert 'injective and measurable' in byid['D4']['statement_original'] and 'bijective' not in byid['D4']['statement_original']
assert r'\mathcal X\in\mathbb R^K' in byid['D5']['statement_original']
assert 'linearly independent' in byid['D8']['statement_original']
assert r'\pi_J(d\boldsymbol\theta^{(t)}\mid\psi^{(t-1)})\pi_J(d\psi^{(t)}\mid\boldsymbol\theta^{(t)})' in byid['D10']['statement_original']
assert r'\|\mu P_J^t-\pi_J\|_{TV}<\epsilon' in byid['D11']['statement_original']
assert r'\sup_{\mu\in\mathcal N(\pi_J,M)}' in byid['D12']['statement_original']
assert r'\int_{\mathbb R^\ell}f(y\mid\theta)p(\theta\mid\psi)' in byid['D13']['statement_original']
assert r'u_j:\mathbb R^{mJ}\to[0,1]' in byid['D15']['statement_original']
assert r'\operatorname{argmax}\prod_{j=1}^Jg(Y_j\mid\psi)' in byid['D18']['statement_original']
assert r'\operatorname{Unif}(\widehat\psi_J,c/\sqrt J)' in byid['D19']['statement_original']
assert 'closed ball' in byid['D19']['statement_original']
refs=ambient['unresolved_statement_references'];assert {r['reference'] for r in refs}=={'(B4)','(B5)','(B6)'}
for r in refs:
    assert r['status']=='unresolved_outside_main_text' and set(r['claim_ids'])=={PID+'/T4.2',PID+'/T6.1'}
assert not any(m['source_heading'] in {'(B4)','(B5)','(B6)'} for m in members)
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=4,interfaces=19,source_members=19,direct_theorem_uses=20,related_theorem_connections=31,unranked_auxiliary_passages=9),counts
assert set(ambient['standard_ambient_resolution'])=={'shared',*claims} and len(ambient['unresolved_source_conventions'])==20
math_fragments=0
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=27 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=27 for e in ctx['evidence']);fragments.append(ctx['text'])
    for text in fragments:
        assert not re.search(r'[\u4e00-\u9fff]',text)
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
for n in [1,2,4,5,6,7,9,10,11,12,22,27]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
shutil.copy2(WORK/'appendix-heading-only.png',ROOT/'evidence/appendix-heading-only.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=80,main_text_last_pdf_page=27,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent font-aware enumeration of CMBX10 Theorem headings across pages 1-27, checked against source images on pages 7,9,12,22. Exactly 2.4,3.1,4.2,6.1 occur. The ordinary-font figure-caption reference on page 18 is excluded. Appendix A begins on page 28 and only its heading was inspected.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'Title, both authors, arXiv v2 identifier, both source dates, 80-page count and pinned hash checked. Cached main-text pages match fresh byte-preserving extraction.',
  'Both inventory and final census pass validation; all original claim fields remain unchanged from the independently reviewed inventory.',
  'All four full statements checked against pages 7,9,12,22, including the restated Bernstein-von Mises result, its two testing limits, score and random Gaussian mean.',
  'The common target space, exact ordered coordinate scan, warm-start class, A1 transformations and transformed limiting kernels were checked on pages 4-6.',
  'The fixed-dimensional Bayesian model and randomized-test convention were checked on pages 9-10. Source spelling, calligraphic information and ordinary Gaussian N were retained.',
  'The hierarchical model, minimal exponential-family local prior, arbitrary dominated likelihood, exact two-block order and distinct mixing-time definitions were checked on pages 10-11.',
  'The group marginal likelihood, marginal information and B1-B3 were checked on page 12. The separate appendix references B4-B6 are preserved as unresolved rather than replaced with fabricated source statements.',
  'The exact marginal MLE, shrinking uniform ball and conditional local-parameter draws were checked on page 22, including the fixed c and printed l in the dimension.',
  'Independent graph traversal verifies 20 direct uses and 31 related connections. The feasible-start theorem does not acquire the warm-start supremum or a fixed M assumption, and the Bernstein-von Mises theorem acquires no sampler premise.',
  'Every source member has exact source terms, accurate passage kind, matching selectors and a source-backed explanation for every related theorem.',
  'Nine auxiliary passages and twenty convention notes preserve differences in time origins, transformation assumptions, source indexing and the redundant Theorem 6.1 limit syntax.',
  'References end on page 27. No appendix mathematics was used, including the assumptions in Appendix B and all proofs in Appendix C.'
 ]),source_notes=[
  'Audited arXiv:2304.06993v2, not the final journal version; equality of their wording is not established.',
  'B4-B6 remain unresolved under the explicit main-text-only scope. The audit is complete as a source census, not as a fully expanded formalization specification.',
  'A1 says injective and measurable, while later prose says bijective. The original requirement is retained.',
  'Theorem 6.1 has redundant liminf/arrow notation. Its feasible start differs from the worst-case warm-start initialization of Theorem 4.2.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],unresolved_statement_references=refs,ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Source transcription and main-text prerequisite audit, not proof certification or source repair.','The exact B4-B6 definitions are outside the reading scope and remain unresolved.','Pinned preprint audited; equivalence to final journal text is unverified.','All appendix mathematics were excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None,scope_exclusions=['Exact B4-B6 statements are in excluded Appendix B; references retained.']))
print(json.dumps(counts))
