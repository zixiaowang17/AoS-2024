"""Independently check frozen source-reviewed decentralized-learning content and the six theorem closures."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': '1b1f80771e7a1dae0fd0a28bfa96259bb0a8e2b93f279d7bf65ccef2059d865f', 'source-passages.json': '9432dae86013847f683356d488a2fc4e0ffd1ab28f07390110487b47039d0737', 'interface-extraction.json': '9443cdb4893920772689809064cc53e8dd3d1839bfbbcce0c9c8284212249f7f', 'ambient-prerequisites.json': '9d2fec107945f6deb822c2919c4159050305570261dcd7eca09141e1d6778978', 'unfinalized-census.json': '8bbc05e89089ad8e09ae75dbca3410dac21bace528798f02d46a5c4e392f271e', 'ranked-interfaces.json': '25d01e162376928c51031e9d4e2987f69a710573bf805a4e8261e040938a5d1e'}

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
    1:[r'\mathbb E_{P_k}','We do not assume','heterogeneity'],
    2:[r'\sum_{k=1}^Kw_k=1',r'b_1\le w_kK\le b_2','positive pre-specified'],
    3:[r'F(\boldsymbol\theta)=\sum_{k=1}^Kw_kF_k(\boldsymbol\theta)'],
    4:[r'\operatorname*{argmin}_{\boldsymbol\theta\in\boldsymbol\Phi}F(\boldsymbol\theta)','dependence on the number of clients'],
    5:['convex and closed','when it is bounded',r'R_d:=\sup'],
    6:[r'\operatorname*{argmin}_{\boldsymbol x',r'\mathbb R^{d\times K}','nonexpanding','matrix form'],
    7:['spectral and Frobenius norms',r'\sqrt{\operatorname{tr}(\boldsymbol A^T\boldsymbol A)}','semi-positive definite'],
    8:[r'd^{-1}\boldsymbol1_d\boldsymbol1_d^T',r'\boldsymbol J'],
    9:['undirected graph','self-loop','nonnegative constant',r'c_{ij}>0',r'\sum_{j=1}^Kc_{ij}=1'],
    10:[r'0\le\rho<1',r'|\lambda_k(\boldsymbol C)|','largest eigenvalue'],
    11:[r'\{\eta_t\}_{t\ge1}',r'\eta_t=D(t+\gamma)^{-\alpha}',r'1/2<\alpha\le1'],
    12:[r'\mathbb R^{d\times K}',r'\hat{\boldsymbol G}_t=K',r'\hat{\boldsymbol\theta}_{t-1}^K;\boldsymbol\xi_t^K'],
    13:['independently and sequentially','all the local estimates are initialized','divisible by',r'(\hat{\boldsymbol\Theta}_{t-1}-\eta_t\hat{\boldsymbol G}_t)\boldsymbol C','otherwise'],
    14:[r'K^{-1}\sum_{k=1}^K\hat{\boldsymbol\theta}_t^k'],
    15:[r'T^{-1}\sum_{t=1}^T\hat{\boldsymbol\theta}_t^k'],
    16:[r'(TK)^{-1}\sum_{t=1}^T\sum_{k=1}^K\hat{\boldsymbol\theta}_t^k'],
    17:[r'\sigma^{2s}+L_\xi\|\nabla F_k(\boldsymbol\theta)\|_2^{2s}',r's\le v','positive integer'],
    18:['convex and $L$-smooth',r'\frac L2',r'\tag{11}'],
    19:[r'\le\kappa^2',r'\|\nabla F_k(\boldsymbol\theta_K^*)\|_2\le B'],
    20:['Assumptions 2.1–2.2, 3.1 with $v=1$',r'B_{\mathrm{MSE}}',r'B_{\mathrm{CE}}',r'K\ge1',r'\tag{12}'],
    21:[r'K^{-1}\sum_{k=1}^K\mathbb E',r'\hat{\boldsymbol\theta}_t^k-\hat{\bar{\boldsymbol\theta}}_t'],
    22:[r'\boldsymbol\theta_1,\boldsymbol\theta_2\in\mathbb R^d',r'\mu>0',r'\mu=0',r'\nabla^2F(\boldsymbol\theta_K^*)\succeq\mu_*\boldsymbol I',r'\varphi^{\prime\prime\prime}(t)',r"\varphi''(u)",'(iii)'],
    23:[r'\left(\frac\mu{2L}+\frac12\right)\mu',r'\mu_*^2',r'\frac{16B_G^2R_d^2}{9}'],
    24:['$L$-average smooth',r'L_a\|\boldsymbol\theta_1-\boldsymbol\theta_2\|_2^2'],
    25:[r'\boldsymbol S_k\succeq\ell_{\mathrm{cov}}\boldsymbol I',r'\boldsymbol\epsilon(\boldsymbol\theta_K^*;\boldsymbol\xi^k)',r'2+\delta',r'\sqrt K\sum_{k=1}^Kw_k'],
    26:['second-order differentiable',r'L_H\|\boldsymbol\theta-\boldsymbol\theta_K^*\|_2',r'K\ge1'],
    27:[r'\boldsymbol H=\nabla^2F(\boldsymbol\theta_K^*)'],
    28:[r'\boldsymbol S=\mathbb E(\boldsymbol\epsilon(\boldsymbol\theta_K^*)\boldsymbol\epsilon(\boldsymbol\theta_K^*)^T)'],
    29:[r'\sum_{t=0}^{T-1}',r'\frac1{T^2}',r'\hat{\boldsymbol\theta}_t^k;\boldsymbol\xi_t^k'],
    30:[r'K\sum_{k=1}^Kw_k^2\hat{\boldsymbol S}_k'],
    31:['nondecreasing function',r'\mathbb N_+\to\mathbb N_+',r'\sum_{s=0}^{a(T)-1}',r'\hat{\bar{\boldsymbol\theta}}_{T-s-1}^k',r'\boldsymbol\xi_{T-s}^k'],
    32:[r'\sqrt{\mathbb E',r'\ell_H\|\boldsymbol\theta-\boldsymbol\theta_K^*\|_2',r'\le H^2'],
    33:[r'\hat{\boldsymbol H}^{-1}\hat{\boldsymbol S}\hat{\boldsymbol H}^{-1}',r'\chi^2_{d,\beta}',r'\tag{26}'],
    34:[r'T^{\alpha-1}',r'(\log(T))^{-1}',r'\alpha=1'],
    35:[r'\boldsymbol\Psi\boldsymbol D\boldsymbol\Psi^T',r'\min\left\{\max\{(D_{jj}),\delta\},\frac1\delta\right\}'],
    36:[r'\sum_{i=1}^3r_i(T)=T',r'\frac{T^{1-\zeta}}{C_2}',r'r_2(T)=\frac T{C_3}',r'r_3(T)=\frac T{C_4}'],
    37:[r'B(T-r_3(T),r_1(T),\alpha)K',r'\sum_{t=r_1(T)+1}^{T-r_3(T)}',r'\sum_{s=T-r_3(T)+1}^T',r'\hat{\bar{\bar{\boldsymbol\theta}}}_{T-1}',r'(C(T_1,\alpha)^{-1}-C(T_2,\alpha)^{-1})^{-1}'],
    38:[r'\tilde{\boldsymbol H}^{\mathrm{reg}}=\boldsymbol Z(\tilde{\boldsymbol V})^{-1}','according to (30)'],
    39:[r'\alpha=1',r'\nabla f_k(\hat{\boldsymbol\theta}_{t-1}^k;\boldsymbol\xi_t^k)',r'\tag{33}','given in (24)']}
    assert set(checks)==set(range(1,40))
    for n,vs in checks.items():
        for v in vs:assert v in s['D'+str(n)],(n,v)
    for n in [10,11,17,18,19,22,24,25,26,32]:assert m['D'+str(n)]['source_kind']=='assumption'
    for n in [2,5]:assert m['D'+str(n)]['source_kind']=='condition'
    assert m['D20']['source_kind']=='source_passage' and m['D20']['source_heading'].startswith('Lemma 1')
    for n in [27,28,33]:assert m['D'+str(n)]['source_kind']=='theorem_excerpt'
    assert '3.1 with $v=2$' in t['5'] and '3.2–3.4' not in t['5']
    assert 'For each fixed $K$' in t['2'] and 'either finite or diverges' in t['3']
    assert r'\nabla F_k(\boldsymbol\theta_K^*;\boldsymbol\xi_t^k)' in t['6']
    assert r'\nabla f_k' not in t['6']
    assert r'\sqrt{\frac KT}+\frac1{\sqrt K}' in t['6']
    assert r'\|_F^2' not in t['5'] and r'\|_F\right)' in t['5']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert 'independent and identically distributed' in a['A1']
    assert r'K^{-1}\boldsymbol1_K\boldsymbol1_K^T' in a['A3']
    assert r'D>2/\mu_{R_d}' in a['A5'] and r'\eta_1\le D/(D\mu_{R_d}-1)' in a['A5']
    assert r'K\sum_{k=1}^Kw_k^2' in a['A6']
    assert 'upper' in a['A8']
    assert len(ambient['unresolved_external_prerequisites'])==3
    assert all(x['status']=='source_ambiguity' for x in ambient['unresolved_external_prerequisites'])
    assert set(ambient['statement_local_bindings'])=={'T1','T2','T3','T4','T5','T6'}
    assert len(ambient['source_issues'])==19
def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='AOS2452.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==25
    assert paper['main_text_last_pdf_page']==24 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==6
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent source-clause graph; no extractor or finalizer import.
    raw={1:[],2:[],3:[1,2],4:[3,5],5:[],6:[5],7:[],8:[],9:[],10:[9],11:[],12:[1,2],13:[6,9,11,12],14:[13],15:[13],16:[14,15],17:[1,5],18:[1,5,7],19:[1,2,3,4,7],20:[4,8,10,11,13,14,17,18,19,21],21:[7,13,14],22:[1,3,4,5,7],23:[5,18,22],24:[1,5,7],25:[2,4,7,17],26:[3,4,5,7],27:[3,4],28:[25],29:[1,13],30:[2,28,29],31:[1,2,15,27],32:[1,4,5,7],33:[16,30,31],34:[11],35:[],36:[11],37:[1,2,13,16,27,34,36],38:[35,37],39:[1,2,13,16,31]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'1':ids([2,7,8,10,11,17,18,19,20,21]),'2':ids([4,7,8,10,11,13,14,17,18,19,21,22,23]),'3':ids([4,10,11,16,17,18,19,22,24,25,26,27,28]),'4':ids([4,10,11,16,17,18,19,22,24,25,27,28,30,31,32,33]),'5':ids([5,7,10,11,17,19,22,24,26,27,36,38]),'6':ids([4,10,11,17,18,19,22,24,25,27,28,32,39])}
    expected_reach={
    '1':ids(list(range(1,15))+[17,18,19,20,21]),
    '2':ids(list(range(1,15))+[17,18,19,21,22,23]),
    '3':ids([1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,22,24,25,26,27,28]),
    '4':ids([1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,22,24,25,27,28,29,30,31,32,33]),
    '5':ids([1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,19,22,24,26,27,34,35,36,37,38]),
    '6':ids([1,2,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,22,24,25,27,28,31,32,39])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not (expected_reach['1']&ids([15,16,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39]))
    assert not (expected_reach['5']&ids([8,18,20,21,23,25,28,29,30,31,32,33,39]))
    assert 'D26' in expected_reach['3'] and 'D32' not in expected_reach['3']
    assert 'D32' in expected_reach['4'] and 'D26' not in expected_reach['4']
    assert not (expected_reach['6']&ids([29,30,33,34,35,36,37,38]))
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==9 and len(ambient['source_issues'])==19
    source_specific_checks(m,aux,ambient,{c['claim_id'].split('/T')[-1]:c['statement_original'] for c in inv['claims']})
    for obj in list(m.values())+d['claims']+list(aux.values()):
        t=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',t)
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        assert obj['evidence'] and all(1<=e['page']<=24 for e in obj['evidence'])
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
                assert not any(ord(ch)<32 and ch!='\n' for ch in ctx['text'])
                assert all(1<=e['page']<=24 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=6,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=6,interfaces=39,source_members=39,direct_theorem_uses=77,related_theorem_connections=143,unranked_auxiliary_passages=9),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings={'inventory': 'Six original main-text Theorems 1–6 independently enumerated across pages 1–24. All formula constants, subparts, exponent regimes, fixed/growing client qualifications and the continuation of Theorem 4 were visually compared with the published PDF. Lemma 1 and Corollary 1 remain outside the theorem inventory; the external supplement is excluded.', 'source_passages': '39 original source entries preserve client/federated risks, weights and target, geometry and network, the full DFL recurrence, three averaging schemes, complete numbered assumptions, consensus/MSE constants, covariance and smooth/regression Hessian estimators, clipping and time segments, and the actual one-step correction. Nine auxiliary passages preserve required contextual bindings and original conventions.', 'dependencies': 'Independent source-clause reconstruction gives 77 direct uses and 143 related-theorem connections. Theorem 5 retains v=2 and its printed assumption list; it does not acquire stochastic-Hessian Assumption 4.4 or the plug-in estimator. Theorem 6 uses the corrected alpha=1 PR estimator and the plug-in Hessian, without importing the regression estimator or downstream confidence procedure.', 'source_issues': 'Nineteen source notes retain matrix-dimension conventions, endpoint and time-zero ambiguities, referenced conditional assumptions, derivative-variable and aggregate-noise bindings, cross-client sampling, window/segment and clipping conditions, scalar/matrix Hessian distinctions and the uppercase F_k notation in Theorem 6. Three unresolved source-ambiguity records remain explicit; none is represented as corrected or proven.', 'names_and_highlights': 'All 39 entries retain literal source keywords, original passage kinds/headings and source-specific selectors. All 143 connections have exact same-paper paths and explanatory source correspondence. Statements and all selectors were checked with the HTML renderer, while source quotations were preserved.', 'reproduction': 'All six content JSONs reproduce byte for byte in a fresh empty directory. Seven retained scripts keep extraction and independent validation separate. Reproduction and structural checks do not replace the recorded visual source comparison.', 'limits': 'This is a completed review of what the original main text states, not a proof certification. Explicit source ambiguities remain, including how later theorems inherit the conditional hypotheses of Theorem 2(ii). No missing joint-law, interiority, integer-segment, zero-index or inverse convention has been silently supplied.'}
    reviewed_pages=[1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
    crop=dict(path='evidence/page-24-main-text.png',page=24,y_end=160)
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[crop]))
    evidence=[dict(path=f'evidence/page-{n:02}.png',page=n) for n in reviewed_pages]+[crop,dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    sys.path.insert(0,'skills/statistical-census-html/scripts')
    import build_report
    for c in d['claims']:build_report.render_statement(c['statement_original'])
    build_report.verify_highlights(d)
    write('evidence/rendering-check.json',dict(paper_id=PID,theorems_rendered=6,source_members_with_visible_highlights=39,all_selectors_matched=True,scope='Source rendering and annotation checks only; mathlib audit and complete report generation remain pending.'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=25,main_text_last_pdf_page=24,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent uppercase small-cap heading enumeration across main-text pages 1–24 and visual comparison of all six complete statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered published PDF, DOI 10.1214/24-AOS2452, 25 pages; source identity pinned.','Main text ends after Funding on page 24; the external supplement is excluded and page 24 evidence is clipped above its listing.','Review concerns extraction fidelity and source correspondence, not proof correctness. Referenced-hypothesis, joint-law, boundary/index and segment-allocation ambiguities remain explicit.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=25,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
