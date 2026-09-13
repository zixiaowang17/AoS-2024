"""Check frozen source-reviewed content and independently reconstruct theorem reach."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '187436ed57566fc3ee411e46a91cccb8ae22303cf6627a611dad6711930f3d5c', 'source-passages.json': 'b4e4d18e9c1102b3128216cf78784ea799aa80123f54846e518fb168347abbe9', 'interface-extraction.json': '1d54b0cad1c77faa8c67088291e9bd2bebcd6b9b652f698570f56445a1941017', 'ambient-prerequisites.json': '824db2c1bb5ea77ac1b7973c15bb3ec39d02a2c464257b48a5c9690e393c267e', 'unfinalized-census.json': '31c3b9f372dcee560c1ae0083b30f99a9d2097a42dd0a1fbdedc8b988ec62109', 'ranked-interfaces.json': 'fd0edc440adce1e2ef77a893c4af8feb1eb7340d65596d4457c4d898550c4f45'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'P_0^n',r'\mathcal P_\Theta=\{P_\theta^n,\theta\in\Theta\}',r'\mu^n','dominates'],
2:[r'\operatorname{argmin}_{P_\theta^n\in\mathcal P_\Theta}',r'\operatorname{KL}(P_0^n\|P_\theta^n)'],
3:[r'\ell(\theta,X^n)=\log p_\theta^n(X^n)','possibly misspecified'],
4:[r'\Pi(\cdot)',r'\Pi_n(\cdot)',r'\pi(\cdot)',r'\pi_n(\cdot)'],
5:[r'\ell_{stl}^{(3)}(\theta)',r'\ell_{stlk}^{(4)}(\theta)',r'\partial/(\partial\theta_s\partial\theta_t\partial\theta_l)',r'|_{\theta=\theta_*}','all the indexes'],
6:[r'J_{\theta_*}=[j_{st}]=-[\ell_{\theta_*,st}^{(2)}]'],
7:[r'\log\pi_{\theta_*}^{(1)}',r'\log\pi_{\theta_*}^{(2)}',r'\partial/(\partial\theta_s\partial\theta_t)\log\pi(\theta)'],
8:[r'\delta_n\to0',r'h=\delta_n^{-1}(\theta-\theta_*)'],
9:[r'F(-x)=1-F(x)',r'F(x)=1/2+\eta x+O(x^2)',r'\eta\in\mathbb R'],
10:[r'2\phi_d(h;\xi,\Omega)F(\alpha_\eta(h-\xi))',r'P_{\mathrm{SKS}}^n(S)=\int_S',r'w(h-\xi)\in(0,1)','third order odd polynomial'],
11:[r'\theta_*\in\Theta','unique'],
12:[r'\Delta_{\theta_*}^n=O_{P_0^n}(1)',r'v_{st}^n=O_{P_0^n}(1)',r'a_{\theta_*,stl}^{(3),n}=O_{P_0^n}(1)',r'-h_sv_{st}^n\Delta_{\theta_*,t}^n+\frac12v_{st}^nh_sh_t-\frac{\delta_n}6',r'\sup_{h\in K_n}|r_{n,1}(h)|',r'O_{P_0^n}(\delta_n^2M_n^{c_1})',r'K_n=\{\|\theta-\theta_*\|\le M_n\delta_n\}',r'\lambda_{\mathrm{MIN}}(V_{\theta_*}^n)>\eta_1^*',r'\lambda_{\mathrm{MAX}}(V_{\theta_*}^n)<\eta_2^*'],
13:[r'\log\pi^{(1)}=[\log\pi_s^{(1)}]',r'\log\pi(\theta_*+\delta_nh)/\pi(\theta_*)',r'\sup_{h\in K_n}|r_{n,2}(h)|=O(\delta_n^2M_n^{c_2})'],
14:[r'M_n=\sqrt{c_0\log\delta_n^{-1}}','specified later',r'K_n=\{\|\theta-\theta_*\|\le M_n\delta_n\}'],
15:[r'\lim_{\delta_n\to0}P_0^n',r'\Pi_n(\|\theta-\theta_*\|>M_n\delta_n)<\delta_n^2'],
16:['two times continuously differentiable',r'0<\pi(\theta_*)<\infty'],
17:['For every sequence',r'\sup_{\|\theta-\theta_*\|>M_n/\sqrt n}',r'(\ell(\theta)-\ell(\theta_*))/n',r'<-c_5M_n^2/n'],
18:[r'\operatorname{argmax}_{\theta\in\Theta}\{\ell(\theta)+\log\pi(\theta)\}'],
19:[r'\widehat h=\sqrt n(\theta-\widehat\theta)'],
20:[r'\widehat\Omega=(\widehat V^n)^{-1}',r'[j_{\widehat\theta,st}/n]'],
21:[r'2\phi_d(\widehat h;0,\widehat\Omega)F(\widehat\alpha_\eta(\widehat h))',r'\{1/(12\eta\sqrt n)\}(\ell_{\widehat\theta,stl}^{(3)}/n)\widehat h_s\widehat h_t\widehat h_l'],
22:['For every',r'M_n\sqrt d/\sqrt n',r'P_0^n(\widehat A_{n,0})>1-\widehat\epsilon_{n,0}'],
23:[r'\lambda_{\mathrm{MIN}}(\widehat\Omega^{-1})>\bar\eta_1',r'\lambda_{\mathrm{MAX}}(\widehat\Omega^{-1})<\bar\eta_2',r'P_0^n(\widehat A_{n,1})>1-\widehat\epsilon_{n,1}',r'B_\delta(\widehat\theta):=\{\theta\in\Theta:\|\widehat\theta-\theta\|<\delta\}',r'\|\log\pi^{(2)}(\theta)\|<L_{\pi,2}',r'\|\ell^{(3)}(\theta)/n\|<L_3',r'\|\ell^{(4)}(\theta)/n\|<L_4',r'P_0^n(\widehat A_{n,2})>1-\widehat\epsilon_{n,2}','spectral norm'],
24:[r'C\subseteq\{1,\ldots,d\}',r'\bar C=C^c',r'\widehat h=(\widehat h_C,\widehat h_{\bar C})'],
25:[r'\Lambda_C=\widehat\Omega_{\bar CC}\widehat\Omega_{CC}^{-1}',r'\bar\Omega=\widehat\Omega_{\bar C\bar C}-\widehat\Omega_{\bar CC}\widehat\Omega_{CC}^{-1}\widehat\Omega_{C\bar C}',r'\phi_{d-d_C}(\widehat h_{\bar C};\Lambda_C\widehat h_C,\bar\Omega)'],
26:[r'3\ell_{\widehat\theta,srv}^{(3)}\bar\Omega_{rv}',r'3\ell_{\widehat\theta,rvk}^{(3)}\bar\Omega_{rv}\Lambda_{C,ks}',r'3\ell_{\widehat\theta,str}^{(3)}\Lambda_{C,rl}',r'3\ell_{\widehat\theta,srv}^{(3)}\Lambda_{C,rt}\Lambda_{C,vl}',r'\ell_{\widehat\theta,rvk}^{(3)}\Lambda_{C,rs}\Lambda_{C,vt}\Lambda_{C,kl}',r's,t,l\in C'],
27:[r'\{1/(12\eta\sqrt n)\}(1/n)',r'\nu_{1,s}^n\widehat h_s+\nu_{3,stl}^n\widehat h_s\widehat h_t\widehat h_l'],
28:[r'2\phi_{d_C}(\widehat h_C;0,\widehat\Omega_{CC})F(\alpha_{\eta,C}(\widehat h_C))'],
29:[r'\pi_{n,C}(\widehat h_C)=\int\pi_n(\widehat h)\,\mathrm d\widehat h_{\bar C}']}
    assert set(checks)==set(range(1,30))
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    for n,number in [(11,1),(12,2),(13,3),(15,4),(16,7),(17,8),(22,9),(23,10)]:
        assert m['D'+str(n)]['source_kind']=='assumption'
        assert m['D'+str(n)]['source_heading']=='Assumption '+str(number)
    assert r'\mu_n' not in s['D1'] and r'I_{\theta_*}' not in s['D6']
    assert r'\ell' not in s['D12'] and r'\log\frac' not in s['D13']
    assert 'Omega' not in s['D24'] and 'Omega' not in s['D29']
    assert r'\int' not in s['D28'] and r'\widehat\alpha' not in s['D28']
    assert r'\eta>0' not in t['2.1'] and r'\int |G' not in t['4.1']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert 'implicit in the repetition' in a['A1'] and 'universal positive constant' in a['A2']
    assert r'\mathbb E_0^nj_{st}' in a['A3'] and r'\delta_n=n^{-1/2}' in a['A4']
    assert 'zero by definition' in a['A5'] and 'Assumption 7 implies that Assumption 3' in a['A6']
    assert r'\alpha_{\eta,C}(\widehat h_C)=\mathbb E' in a['A7']
    assert r's,t,l\in C' in a['A8'] and r'r,v,k\in\bar C' in a['A8']
    assert r'3\bar\Omega_{rv}\Lambda_{C,ks}\widehat h_s' in a['A8']
    assert 'condition 10 replaces Assumptions 5–6' in a['A9']
    assert 'sufficiently large choice' in a['A10'] and 'for every $D>0$' in a['A11']
    assert all(set(x['depends_on'])<=set(m) for x in aux.values())
    assert set(ambient['statement_local_bindings'])=={'T2.1','T4.1','T4.5'}
    assert ambient['unresolved_external_prerequisites']==[]
    # Witness that the source componentwise third Gaussian moment needs contraction.
    mu=[1.,2.,3.];cov=[[1.,.2,.4],[.2,2.,.7],[.4,.7,3.]]
    full=mu[0]*mu[1]*mu[2]+mu[0]*cov[1][2]+mu[1]*cov[0][2]+mu[2]*cov[0][1]
    printed=mu[0]*mu[1]*mu[2]+3*cov[0][1]*mu[2]
    assert abs(full-printed)>.1

def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2301.03038v3.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==54
    assert paper['main_text_last_pdf_page']==29 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==3
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent reconstruction from inspected source clauses; no finalizer import.
    raw={1: [], 2: [1], 3: [1], 4: [3], 5: [2, 3], 6: [5], 7: [2, 4], 8: [2], 9: [], 10: [9], 11: [2], 12: [1, 2, 8, 14], 13: [2, 4, 8, 14], 14: [8], 15: [2, 4, 8, 14], 16: [2, 4], 17: [2, 3], 18: [3, 4], 19: [18], 20: [6, 18], 21: [5, 9, 18, 19, 20], 22: [2, 18], 23: [5, 7, 18, 20], 24: [19], 25: [20, 24], 26: [5, 18, 24, 25], 27: [9, 24, 26], 28: [9, 24, 25, 27], 29: [4, 19, 24]}
    local={"D"+str(k):ids(v) for k,v in raw.items()}
    direct={k:ids(v) for k,v in {'2.1': [4, 8, 9, 10, 11, 12, 13, 15], '4.1': [4, 11, 16, 17, 18, 19, 21, 22, 23], '4.5': [11, 16, 17, 18, 19, 22, 23, 24, 28, 29]}.items()}
    expected_reach={k:ids(v) for k,v in {'2.1': [1, 2, 3, 4, 8, 9, 10, 11, 12, 13, 14, 15], '4.1': [1, 2, 3, 4, 5, 6, 7, 9, 11, 16, 17, 18, 19, 20, 21, 22, 23], '4.5': [1, 2, 3, 4, 5, 6, 7, 9, 11, 16, 17, 18, 19, 20, 22, 23, 24, 25, 26, 27, 28, 29]}.items()}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([5,6,7,16,17,18,19,20,21,22,23,24,25,26,27,28,29])&expected_reach['2.1']
    assert not ids([8,10,12,13,14,15,24,25,26,27,28,29])&expected_reach['4.1']
    assert not ids([8,10,12,13,14,15,21])&expected_reach['4.5']
    true_marginal=set();stack=['D29']
    while stack:
        lid=stack.pop()
        if lid not in true_marginal:true_marginal.add(lid);stack.extend(local[lid])
    assert not ids([5,6,7,9,10,20,21,25,26,27,28])&true_marginal
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==11 and len(ambient['source_issues'])==16
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
        assert obj['evidence'] and all(1<=e['page']<=29 for e in obj['evidence'])
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
                assert all(1<=e['page']<=29 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=3,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=3,interfaces=29,source_members=29,direct_theorem_uses=27,related_theorem_connections=51,unranked_auxiliary_passages=11),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings={'inventory': 'Three complete main-text Theorems2.1,4.1,4.5 independently enumerated from small-cap headings and visually compared, including both conclusions of4.1. Main text continues onto29 before references; supplementary bodies starting32 are excluded.', 'source_passages': 'Twenty-nine original entries and eleven auxiliary passages preserve the statistical experiment and KL projection, prior/posterior and derivative notation, generic SKS family and its abstract Assumptions1–4, MAP/joint approximation with Assumptions7–10, and the separate marginal construction including all conditional-Gaussian blocks and nu coefficients.', 'dependencies': 'Independent source-clause reconstruction verifies27 direct uses and51 related-theorem connections. Abstract general-theorem arrays are not identified with likelihood derivatives. Assumptions3/4 use a separately archived local set rather than inheriting Assumption2. MAP covariance is separate from Assumption10 regularity. Sufficient Assumptions5–6 are not imported backwards.', 'marginals': 'Theorem4.5 concerns Eq31, which applies F to the conditional mean skewing polynomial. It is not merely exact marginalization of Eq22. The true posterior marginal has no Gaussian-covariance dependency. The marginal TV theorem inherits base assumptions of4.1, not its optional function-G conclusion.', 'source_issues': 'Sixteen notes preserve source-coordinate and log-ratio ambiguities, eta=0 and covariance-event domains, MAP boundary stationarity, likelihood versus posterior Hessians, tensor norm conventions, signed-G integrals, c0 quantifiers, componentwise Gaussian third-moment notation and empty/full coordinate subsets. No original formula is silently repaired and no supplementary theorem is counted.', 'names_and_highlights': 'All29 entries have original natural-language terms or original numbered assumption headings, preserved source kinds and literal matching selectors. All51 connections have a valid paper-local path and specific source explanation. The dominating measure retains the printed superscript mu^n.', 'reproduction': 'All six content JSON files reproduce byte for byte in a fresh empty directory. Seven retained scripts support extraction, finalization, rebuilding and independent source review. Reproduction is not a new semantic review of the PDF.'}
    reviewed_pages=[1,5,6,7,9,11,13,15,18,21,22,23,24,25,29]
    crops=[]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=crops))
    evidence=[dict(path=f'evidence/page-{n:02}.jpg',page=n) for n in reviewed_pages]+crops+[dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=54,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent actual small-cap heading enumeration and visual comparison of all three complete statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv2301.03038v3 marked8Apr2024,54pages, pinned bySHA256; not silently exchanged for the published article.','Main text ends on page29 before REFERENCES y248.679; evidence clipped242. Supplementary bodies starting32 are excluded. No required theorem assumption is imported from a supplementary proof.','Source review preserves mathematical statements, dependencies and unresolved source notation; it does not certify proofs or solve implicit selection/domain conventions.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=54,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
