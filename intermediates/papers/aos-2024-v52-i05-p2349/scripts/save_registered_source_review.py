"""Verify frozen source-reviewed content and independently reconstructed dependency scopes."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': '446842ec4b5e0be41b7c7530b679e65e33059c65ea2e288676ccd78d4ed8cb82', 'source-passages.json': 'bb39810d1850bbf357776d62895e8582cfd25ead280e6d3d88f1a8d1d1186b20', 'interface-extraction.json': '030caf6c679e1e38edb06032bfe75d8aa38259ce433594eb96769340c002328b', 'ambient-prerequisites.json': '48e84fca86c0caf78c3500d52c2b39ec60056e9eefd26e19d5e8a770d2609532', 'unfinalized-census.json': '22654f6184449697f724e2cca3c3d0defce2325c6849592f57915f351f88b2c0', 'ranked-interfaces.json': '7386150b569148f44abd7c9d9377f61d775ace4dfdc9e1afc5f42421064f3eee'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}

def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2306.10594v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2306.10594'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==25
    assert paper['main_text_last_pdf_page']==23 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==6
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Reconstructed from original definitions and theorem clauses; no builder graph imported.
    raw={1:[],2:[1],3:[2],4:[1],5:[2],6:[],7:[],8:[1,7],9:[6,8],10:[1],11:[2,10],12:[3,9,11],13:[3,11,32],14:[3],15:[],16:[6,8],17:[3,11,16],18:[],19:[6,18],20:[15,16,19],21:[2],22:[3,9,11,12,15,17,20,21],23:[2],24:[3,22],25:[2,3,9],26:[],27:[6,26],28:[6],29:[9,26],30:[2,8],31:[26],32:[8]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'1':ids([2,3,4,5]),'2':ids([3,12,13,15,17,22,23,24]),'3':ids([3,12,13,14,24]),'4':ids([2,6,12,14,25]),'5':ids([9,12,13,14,26,27,28,29,30,31,32]),'6':ids([12,13,14,27,28,29,30,32])}
    expected_reach={'1':ids([1,2,3,4,5]),'2':ids([1,2,3,6,7,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,32]),'3':ids([1,2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,24,32]),'4':ids([1,2,3,6,7,8,9,10,11,12,14,25]),'5':ids([1,2,3,6,7,8,9,10,11,12,13,14,26,27,28,29,30,31,32]),'6':ids([1,2,3,6,7,8,9,10,11,12,13,14,26,27,28,29,30,32])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32])&expected_reach['1']
    assert 'D23' not in expected_reach['3'] and 'D23' in expected_reach['2']
    assert not ids([13,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,32])&expected_reach['4']
    assert not ids([4,5,15,16,17,18,19,20,21,22,23,24,25])&(expected_reach['5']|expected_reach['6'])
    assert 'D31' in expected_reach['5'] and 'D31' not in expected_reach['6']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==8 and len(ambient['source_issues'])==13
    source_specific_checks(m,aux,ambient)
    for obj in list(m.values())+d['claims']+list(aux.values()):
        t=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',t)
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        assert obj['evidence'] and all(1<=e['page']<=23 for e in obj['evidence'])
    for x in d['interfaces']:
        assert len(x['members'])==1
        a=x['members'][0];lid=a['local_id'];own=a['statement_original']+' '+a['local_label']
        linked=own+' '+' '.join(c['statement_original'] for c in d['claims'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems']))
        selectors=a['highlight_symbols']+a['highlight_phrases'];assert any(v in own for v in selectors) and all(v in linked for v in selectors)
        assert {u['claim_id'] for u in x['central_claim_uses']}=={PID+'/T'+n for n,v in direct.items() if lid in v}
        assert set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
        for rel in x['related_theorems']:
            n=rel['claim_id'].split('/T')[-1];path=rel['via_local_ids']
            assert rel['relation']==('direct' if lid in direct[n] else 'indirect')
            assert path[0] in direct[n] and path[-1]==lid and all(b in local[a] for a,b in zip(path,path[1:]))
            ex=x['theorem_explanations'][rel['claim_id']];assert ex['via_local_ids']==path and ex['text'].strip() and ex['evidence']
            assert 'This theorem directly uses the API.' not in ex['text']
        for kw in x['source_keywords']:
            if 'context_id' in kw:
                ctx=next(v for v in a['naming_context'] if v['context_id']==kw['context_id']);assert kw['source_text'] in ctx['text']
                assert all(1<=e['page']<=23 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
    counts=dict(theorems=6,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=6,interfaces=32,source_members=32,direct_theorem_uses=41,related_theorem_connections=98,unranked_auxiliary_passages=8)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Six complete main-text Theorems1–6, enumerated independently by small-cap headings. Preserve T3’s two spectral/shift conditions, T4’s explicit reference(7.1), every T5 rate factor and the exact T6 dimension-growth regime. Corollaries and Lemmas are not additional theorem records.',
      source_passages='Thirty-two source entries preserve radial/angular domains, RKHS and tensor constructions, characteristicness, moment and polar transformations, fixed reference centering, population/sample operators, Frechet and influence definitions, complete Lemma4–5 formulas, kernel conditions, covariance operator and Assumptions1–4 with the rate functions. Eight auxiliary passages preserve problem/calibration context.',
      dependencies='Independent reconstruction confirms41 direct uses and98 related connections. T1 has only abstract kernel/measure/tensor dependencies. T4 uses the literal known-parameter statistic, without estimated moments. T5–T6 have no influence/Frechet or characteristic-kernel assumptions. T6 inherits Theorem5 assumptions without importing its bound-specific functions.',
      scope='T2 is centered at the general population discrepancy, with the full influence function rather than a null-only simplification. T3 uses the Gamma definition and conditional influence-formula context; no complete Theorem2 assumption reference is printed. Its missing local-alternative regularity and zero-eigenvalue conventions remain explicit source issues.',
      source_issues='Thirteen notes preserve whitening/polar domains, tensor indices, embedding/CLT and Frechet-domain requirements, local-alternative ambiguity, E-versus-E0 centering in(7.1), Hilbert-Schmidt versus simple-tensor supremum, implicit MGF/tail quantifiers, feature-space Lipschitz scaling, growing-dimension targets and implementation typos. Statements are not silently repaired or proof-certified.',
      names_and_highlights='Every source entry has natural-language source terms, original source kind and heading, literal selectors and complete same-paper theorem explanations. All98 dependency paths are independently checked; source types distinguish assumptions, conditions and contextual Lemma formulas.',
      reproduction='All six content JSON files reproduce byte for byte. Seven retained per-paper scripts include inventory/source review with frozen hashes, formula assertions, independent graph reconstruction and schema validation.')
    reviewed_pages=[4,5,6,7,10,11,12,13,14,18,19,23]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[]))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=25,main_text_last_pdf_page=23,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent small-cap heading enumeration and visual comparison of all six complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark','Conjecture'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2306.10594v2 dated 27 Mar 2024, pinned by SHA-256. No substitution with another paper version.','Main text, acknowledgments and funding end on PDF page23 before Supplementary Material. All appendix bodies are excluded; local Lemma formulas needed to identify statement objects are preserved as source passages.','Source and schema validation do not certify proofs or resolve the explicitly recorded source ambiguities.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=25,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))

def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'(-\pi/2,\pi/2]',r'(-\pi,\pi]',r'\Omega_U=[0,\infty)'],
2:['positive definite kernels',r'\mathcal H_U',r'\mathcal H_\Theta'],
3:[r'(f\otimes g)(h)=f\langle g,h\rangle_{\mathcal H_\Theta}',r'\widetilde\alpha_r(\widetilde f_s\otimes\widetilde g_s)','completion'],
4:['all probability measures',r'\mathcal F_U\times\mathcal F_\Theta'],
5:['injective',r'P_1=P_2'],
6:[r'\mu(F)=\int x\,dF(x)',r'\Sigma(F)=\int(x-\mu(F))(x-\mu(F))^\top',r'\Sigma(F_n)=\widehat\Sigma'],
7:[r'\arctan(y/x)+\pi',r'x<0,y\ge0',r'-\pi/2,&x=0,y<0'],
8:['is bijective with inverse',r'\operatorname{Arctan}(S_{j+1},v_j)',r'\operatorname{Arctan}(v_d,v_{d-1})',r'\theta=g(v)'],
9:[r'\Sigma^{-1/2}(x-\mu)',r'V(x)=W(x)/U(x)'],
10:[r'\cos^{d-2}(\theta_1)\cos^{d-3}(\theta_2)',r'd\theta)^{-1}',r'P_0'],
11:[r'\widetilde\kappa_\Theta(\cdot,\theta)',r'dP_0(\theta)'],
12:[r'\otimes E_0[\kappa_\Theta',r'E[\kappa_U(\cdot,U)\otimes\widetilde\kappa_\Theta'],
13:[r'\widehat U',r'\widehat\Theta',r'\otimes E_0[\kappa_\Theta'],
14:['sum of eigenvalues',r'\breve\Sigma_{U\Theta}\breve\Sigma_{U\Theta}^*'],
15:['uniform metric',r'A(F-F_0)',r'\|F-F_0\|_{\mathcal F}'],
16:[r'\Sigma(F)^{-1/2}(x-\mu(F))',r'\Theta(x,F)=g(V(x,F))'],
17:[r'\Sigma_{U\Theta}(F)',r'dF(x)',r'dP_0(\theta)'],
18:[r'(1-\epsilon)F_0+\epsilon\delta_z',r'\epsilon=0'],
19:[r'\mu^\star(z)=z-\mu',r'\Sigma^\star(z)=(z-\mu)(z-\mu)^\top-\Sigma',r'(\Sigma^{1/2}\otimes\Sigma+\Sigma\otimes\Sigma^{1/2})^{-1}'],
20:['Frechet differentiable',r'2[(x-\mu)^\top\Sigma^{-1}(x-\mu)]^{1/2}',r'C_i(x)=[\partial g(V(x))/\partial v^\top]B_i(x)',r'\Theta^\star(x,z)=C_1(x)\mu^\star(z)+C_2(x)\operatorname{vec}[\Sigma^\star(z)]'],
21:['second argument',r'\partial\kappa(\cdot,t)/\partial t'],
22:[r'-\Sigma_{U\Theta}',r'\dot\kappa_U(\cdot,U(X))U^\star(X,z)',r'\dot\kappa_\Theta(\cdot,\Theta(X))^\top\Theta^\star(X,z)'],
23:['twice differentiable with a bounded Hessian matrix'],
24:[r'E[\Sigma_{U\Theta}^\star(X)\otimes\Sigma_{U\Theta}^\star(X)]','(5.10)'],
25:[r'\otimes E[\kappa_\Theta(\cdot,\Theta)]','(7.1)'],
26:['doesn’t depend on $d$ or $n$'],
27:[r'c_1\le\lambda_{\min}(\Sigma)\le\lambda_{\max}(\Sigma)\le c_2'],
28:[r'v\in\mathbb S',r'E(e^{\lambda\langle v,X-\mu\rangle})\le e^{\sigma^2\lambda^2/2}'],
29:[r'c^d','absolute constant'],
30:[r'd^{-1}L_V',r'\|\kappa_\Theta(\cdot,g(v))',"L_U|u-u'|"],
31:[r'c_1\sqrt{\frac{d[\log(2d)+u]}n}',r'c_2d\max',r'^{1/4}',r'^{1/2}',r'+c_3\sqrt d',r'f_4(n,u)=c_9\sqrt{\frac un}+c_{10}\sqrt{\frac1n}'],
32:['i.i.d. sample',r'\widehat\Sigma=E_n[(X-\widehat\mu)(X-\widehat\mu)^\top]',r'\widehat\Sigma^{-1/2}(x-\widehat\mu)']}
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert 'E_0' not in s['D25'] and 'E_0' in s['D12'] and 'E_0' in s['D13']
    assert r'\widehat' not in s['D9']
    assert all(m['D'+str(n)]['source_kind']=='assumption' for n in [27,28,29,30])
    assert all(m['D'+str(n)]['source_kind']=='source_passage' for n in [8,10,19,20,22])
    assert m['D23']['source_kind']=='condition' and m['D24']['source_kind']=='theorem_excerpt'
    a={k:v['statement_original'] for k,v in aux.items()}
    for n,parts in {1:['Lebesgue measure',r'|\Lambda|^{-1/2}',r'h(x^\top x)'],2:['finite mean and variance'],3:[r'H_0:\Sigma_{U\Theta}=0',r'T_n=n\|\breve\Sigma'],4:[r'\sup_{f_1\otimes f_2\in\mathcal F}'],5:['Corollary 2','i.i.d. standard normal'],6:[r'\lambda_j^{1/2}'],7:[r'\epsilon=10^{-6}'],8:[r'\gamma_U,\gamma_\Theta>0']}.items():
        for v in parts:assert v in a['A'+str(n)],(n,v)
    for o in aux.values():assert set(o['depends_on'])<=set(m)
    assert set(ambient['statement_local_bindings'])=={'T1','T2','T3','T4','T5','T6'}
    assert {x['issue_id'] for x in ambient['source_issues']}=={'density-and-inverse-domains','polar-exceptional-sets','tensor-index-and-star-conventions','embedding-and-clt-domain','frechet-linear-domain','local-alternative-and-zero-eigenvalues','known-parameter-centering','hilbert-schmidt-versus-simple-tensors','subgaussian-sphere-and-quantifiers','feature-lipschitz-versus-coordinate-smoothness','concentration-parameters-and-constants','growing-dimension-target','implementation-not-theorem-definition'}
    refs=ambient['source_claim_references'];assert sum(x['reference_kind']=='definition_reference' for x in refs)==4
    assert sum(x['reference_kind']=='proof_only' for x in refs)==2
    assert sum(x['reference_kind']=='assumption_reference' for x in refs)==1
if __name__=='__main__':main()
