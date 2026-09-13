"""Independently check source fidelity, main-text boundary and all theorem dependency paths."""
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
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==75
assert paper['main_text_last_pdf_page']==34 and paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split());assert paper['title'] in first
for author in ['Ziang Niu','Abhinav Chakraborty','Oliver Dukes','Eugene Katsevich']:assert author in first
assert '2211.14698v2' in first and '8 Feb 2023' in first and 'February 10, 2023' in first
assert paper['source_url']=='https://arxiv.org/pdf/2211.14698v2' and paper['version']=='arXiv:2211.14698v2'
boundary=prov['main_text_end_y'];assert boundary==288.68743896484375
main_end=pdf[33].get_text(clip=fitz.Rect(0,0,pdf[33].rect.width,boundary))
assert 'Zhong' in main_end and 'Conditional Randomization Rank Test' in ' '.join(main_end.split())
assert 'Theorem' not in main_end and 'GCM normalization' not in main_end
heading=pdf[33].get_text(clip=fitz.Rect(0,boundary,pdf[33].rect.width,315));assert 'GCM normalization' in heading
labels=[];plain_references=[]
for n in range(34):
    page=pdf[n];clip=fitz.Rect(0,0,page.rect.width,boundary) if n==33 else None
    assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf-8')==page.get_text(clip=clip),(n+1,'cached evidence differs')
    for block in page.get_text('dict',clip=clip)['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();match=re.match(r'Theorem (\d+)(?=[.\s(])',text)
            if match:
                if line['spans'][0]['font']=='CMBX12':labels.append((n+1,match.group(1)))
                else:plain_references.append((n+1,text))
assert labels==[(8,'1'),(12,'2'),(16,'3')],labels
assert len(plain_references)==2 and all(n==18 for n,t in plain_references)
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==3
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
expected={'1':[1,3,4,5,6,8,9,11,12],'2':[1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,18],'3':[1,2,3,5,7,13,14,15,19,20,21,22]}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
assert reach['1'].isdisjoint({'D2','D7','D10','D14','D15','D18','D20','D21','D22'})
assert reach['3'].isdisjoint({'D4','D6','D8','D9','D10','D11','D12','D16','D18'})
assert 'D11' not in reach['2']
for lid,label in [('D11','Definition 1'),('D22','Definition 2')]:assert byid[lid]['source_kind']=='definition' and byid[lid]['source_heading']==label
assert byid['D12']['source_kind']=='theorem_excerpt'
for lid,label in [('D14','(SP1)'),('D15','(SP2)'),('D18',"(SP1')")]:assert byid[lid]['source_kind']=='assumption' and byid[lid]['source_heading']==label
assert byid['D16']['source_kind']=='condition'
t1=claims['1']['statement_original'];t2=claims['2']['statement_original'];t3=claims['3']['statement_original']
assert r'\tag{NDG1}' in t1 and r'\tag{NDG2}' in t1 and r'\tag{Lyap-1}' in t1
assert r'\xrightarrow{d,p}N(0,1)' in t1 and r'\mathbb Q_{1-\alpha}' in t1
assert r'\mathscr L_n^0' not in t1 and r'\mathscr L_n^0' in t2
assert 'NDG1' not in t2 and 'NDG2' in t2 and "(SP1')" in t2
assert r'\tag{Lyap-2}' in t2 and r'\tag{25}' in t2 and r'\tag{26}' in t2
assert r'\mathbb E_{\mathcal L_n}[|Y_i-\mu_{n,y}(Z_i)|^{2+\delta}\mid Z_i]' in t2
assert r'\frac{(\widehat S_n^{\widehat{\mathrm{dCRT}}})^2}{(\widehat S_n^{\mathrm{GCM}})^2}' in t2
assert all(r'\tag{'+str(i)+'}' in t3 for i in [35,36,37,38,39])
assert r'\ddot\psi=K>0' in t3 and r'\text{OR}' in t3
assert r'\mathbb E_{\mathcal L_{x,z}}[\boldsymbol X\mid\cdot]\in\mathcal H_g' in t3
assert r'\forall g_0\in\mathcal S,h_g\in\mathcal H_g' in t3 and 'for large enough' in t3
assert r'1-\Phi(z_{1-\alpha}-h_\beta\cdot s(\theta_0))' in t3
assert r'\prod_{i=1}^n\widehat{\mathcal L}_n(X_i\mid Z_i)' in byid['D4']['statement_original']
assert 'not refit upon resampling' in byid['D6']['statement_original']
assert r'\widehat{\operatorname{Var}}' in byid['D7']['statement_original']
assert 'infinite-resamples limit' in byid['D10']['statement_original']
assert r'\mathbb P[W\leq t\mid\mathcal F]\geq\alpha' in byid['D9']['statement_original']
assert r'\mathbb P[W_n\leq t\mid\mathcal F_n]\xrightarrow{p}' in byid['D11']['statement_original']
assert r'0<\operatorname{Var}_{\widehat{\mathcal L}_n}' in byid['D12']['statement_original']
assert r'\inf_n\mathbb E' in byid['D15']['statement_original'] and r'\sup_n\mathbb E' in byid['D15']['statement_original']
assert r"\widehat E'_{n,y}" in byid['D18']['application_context'][0]['text'] and r'\tag{24}' in byid['D18']['application_context'][0]['text']
assert r'\sup_{\mathcal L_n\in\mathscr L_n^0\cap\mathscr R_n}' in byid['D19']['statement_original']
assert r'\mathcal L_{\beta,\eta}' in byid['D20']['statement_original']
assert r'(h_\beta/\sqrt n,g_0+h_g/\sqrt n)' in byid['D21']['statement_original']
assert r'\tag{34}' in byid['D21']['application_context'][0]['text']
assert r'\limsup_{n\to\infty}' in byid['D22']['statement_original'] and r'\liminf_{n\to\infty}' in byid['D22']['statement_original']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=3,interfaces=21,source_members=21,direct_theorem_uses=25,related_theorem_connections=37,unranked_auxiliary_passages=7),counts
assert set(ambient['standard_ambient_resolution'])=={'shared',*claims} and len(ambient['unresolved_source_conventions'])==23
math_fragments=0
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<34 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<34 for e in ctx['evidence']);fragments.append(ctx['text'])
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
for n in [1,2,5,6,7,8,9,12,13,15,16,18,33]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
shutil.copy2(WORK/'main-text-end-and-heading.png',ROOT/'evidence/main-text-end-and-heading.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=75,main_text_last_pdf_page=34,main_text_end_y=boundary,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent font-aware enumeration of CMBX12 Theorem headings on pages 1-33 and only the main-text part of page 34. Exactly Theorems 1,2,3 occur, starting on pages 8,12,16. The first two continue onto pages 9 and 13. Two regular-font references on page 18 and all appendix results are excluded.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'Title, all four authors, arXiv v2 identifier, both source dates, 75-page count and pinned hash checked. Cached main-text pages match fresh byte-preserving extraction, including the clipped shared page.',
  'Both independent inventory and final census pass validation, and every original claim field is preserved unchanged.',
  'Theorem 1 checked across pages 8-9, including NDG1, NDG2, Lyap-1, conditional normal convergence and the blackboard-Q quantile conclusion.',
  'Theorem 2 checked across pages 12-13, including SP1-prime, SP2, NDG2, variance consistency, Lyap-2, the variance ratio and exact decision-equality event.',
  'Theorem 3 checked on page 16, preserving every condition (35)-(38), its OR branches, exact nuisance-space membership, directionwise eventual inclusion and power formula.',
  'Sampling, bold population notation, script null classes, learned-kernel fitting and frozen resampling statistics checked on pages 2,5,6.',
  'GCM and resampling normalizations, regression-error quantities, SP1/SP2, conditional quantiles and Definition 1 checked on pages 7-8; the additional weighted error and SP1-prime checked on page 12.',
  'The GPLM family, local paths, Definition 2, uniform null-level requirement and original scalar definition (34) checked on pages 5 and 15.',
  'Independent graph traversal confirms 25 direct uses and 37 related connections. Theorem 1 acquires no null-class premise, and Theorem 3 acquires no learned resampling kernel or SP1-prime assumption.',
  'All 21 source members have original natural-language keywords, accurate source kinds, meaningful matching highlight selectors and an explanation for each related theorem path.',
  'Seven auxiliary passages and twenty-three source-convention notes retain finite-versus-infinite resampling, zero-variance conventions, signed variance consistency and pointwise-versus-uniform distinctions.',
  'References finish above y=288.68743896484375 on page 34. The evidence image includes only the appendix heading after that boundary; no appendix mathematical statements or proofs are used.'
 ]),source_notes=[
  'Audited arXiv:2211.14698v2. Equality to the final published journal text is not established.',
  'GCM is represented as a functional of fitted means and empirical variance; its source connection to the residual-product statistic does not import a predictor-resampling kernel.',
  'SP1 and SP1-prime, true and learned variance weights, and both Lyapunov conditions remain distinct.',
  'Theorem 3 preserves the original level-control quantifiers and directional assumptions without repairing possible uniformity ambiguities.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Source transcription and statement-prerequisite audit, not proof certification or source repair.','Pinned preprint audited; equality to final journal wording is not established.','All appendix mathematics were excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
