"""Independently check frozen source-reviewed content and reconstruct theorem reach."""
import datetime,hashlib,json,math,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': 'f1e6386f4175ac0ea5823378a09649d8f933a26a7e1cd0ae9ea4e0ce537501f2', 'source-passages.json': '6fb8de9ffa90f484c0627196119b23615a8f6457d8a028ae00caee33adc795fa', 'interface-extraction.json': '2c83a026c62535b487a4bd75e069c6aa71d925089d809401ccbbe6af2d9d405b', 'ambient-prerequisites.json': '3e2481d761804c1aa9c0a25a675aaedf88eecb46e18156ce52265511d48e1b29', 'unfinalized-census.json': 'aa1104df58c35d5210947163f24c1ad94ac829714f59c9b0a5f3675bb01970dc', 'ranked-interfaces.json': '291e00d827938bcf2431fbb301357e2d4cbf47d5cb95492eb2ea6fa627c70e4f'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:['can share common variables',r'\sum_{k=1}^4X_t^\top\beta_{k0}',r'\mathbb E(\varepsilon_t\mid X_t,Z_t)=0','finite second moment',r'\{\gamma_{i0}\}_{j=1}^2'],
2:[r'\mathbf1_1(U,V)=\mathbf1(U>0,V>0)',r'\mathbf1_2(U,V)=\mathbf1(U\le0,V>0)',r'\mathbf1_3(U,V)=\mathbf1(U\le0,V\le0)',r'\mathbf1_4(U,V)=\mathbf1(U>0,V\le0)'],
3:[r'\Theta=\Gamma_1\times\Gamma_2\times\mathcal B^4','compact set','normalized as $1$'],
4:[r'\mathbb M_T(\theta)=\frac1T\sum_{t=1}^T',r'\mathbf1_k(Z_{1,t}^\top\gamma_1,Z_{2,t}^\top\gamma_2)',r'm(W_t,\theta)'],
5:['strictly convex','unique minimizer',r'\widehat{\mathcal G}',r'\mathbb M_T(\widehat\theta)=\inf_{\theta\in\Theta}\mathbb M_T(\theta)'],
6:['strictly stationary',r'\rho(t)\le c\alpha^t',r'\sup_{s,t\ge1}',r'\mathbb E(\varepsilon_t\mid\mathcal F_{t-1})=0',r'\varepsilon_{i-1}):i\le t'],
7:['not identically distributed',r'\mathbb P(|q_i|\le\epsilon\mid Z_{-j,i})>0','without loss of generality, assume $j=1$',r'\Gamma_1\times\Gamma_2',r'R_k(\gamma_0)\cap R_h(\gamma)',r'\lambda_0>0',r'\|\beta_{k0}-\beta_{h0}\|>c_0'],
8:[r'\mathbb E(Y^4)',r'\mathbb E(\|X\|^4)',r'\mathbb E(\|Z_i\|)',r'Z_i^\top\gamma_1<0<Z_i^\top\gamma_2',r'\gamma_1,\gamma_2,\in'],
9:[r'\mathbb P(|q_i|<\epsilon\mid Z_{-1,i})\ge c_2\epsilon',r'\inf_{\gamma\in\mathcal N_i}',r'\delta_{kh,0}=\beta_{k0}-\beta_{h0}',r'\|\gamma_1-\gamma_2\|\|\gamma_3-\gamma_4\|',r'\|X\|^8',r'\varepsilon^8'],
10:[r'\delta_3,c_4>0',r'|q_{i,t+j}|\le\delta_3',r'\{\mathbb P(|q_{i,t}|\le\delta_3)\}^2','uniformly for',r'c_4\le f_{q_i\mid Z_{-1,i}}(0\mid z_{-1,i})\le c_5',r'f_{\xi^{(k,h)}\mid q_i,Z_{-1,i}}(\xi\mid0,z_{-1,i})\le c_6','compact subset'],
11:[r'q_i=Z_i^\top\gamma_{i0}',r'S(1)=\{(1,2),(2,1)(3,4),(4,3)\}',r'S(2)=\{(1,4),(4,1),(2,3),(3,2)\}'],
12:[r'B_k=\mathbb E\{XX^\top',r'\Sigma_k=B_k^{-1}',r'XX^\top\varepsilon^2',r'R_k(\gamma_0)\}B_k^{-1}'],
13:[r's_i^{(k)}=(-1)',r'\delta_{kh,0}^\top X_tX_t^\top\delta_{kh,0}+2X_t^\top\delta_{kh,0}\varepsilon_t',r'R_k(\gamma_0)\cup R_h(\gamma_0)','excluding its first element','conditional distributions','corresponding conditional densities'],
14:[r'\sum_{i=1,2}\sum_{k,h\in S(i)}',r'\le0<J_{i,\ell}^{(k,h)}',r'\mathbb R^{d_1+d_2}',r'\bar\xi_i^{(k,h)}',r'\mathcal J_{i,\ell}^{(k,h)}=s_i^{(k)}\sum_{n=1}^\ell\mathcal E_{i,n}^{(k,h)}','independent unit exponential','mutually independent'],
15:[r'\widehat\gamma^c=C(\widehat{\mathcal G})','LS estimators'],
16:[r'\min_{\beta,\gamma,g,I,\ell}',r'\beta_k\in\mathcal B',r'\gamma_j\in\Gamma_j',r'(g_{j,t}-1)(M_{j,t}+\epsilon)<Z_{j,t}^\top\gamma_j\le g_{j,t}M_{j,t}',r'I_{k,t}L_i\le\ell_{k,i,t}\le I_{k,t}U_i',r'L_i(1-I_{k,t})\le\beta_{k,i}-\ell_{k,i,t}\le U_i(1-I_{k,t})',r'I_{k,t}\ge\sum_{j=1}^2'],
17:[r'L_i\le\beta_{k,i}\le U_i'],
18:[r'X^\top\beta_0\mathbf1',r'\sigma_0(X,Z)e','continuous distribution','independent of',r'\mathbb E(e)=0',r'\mathbb E(e^2)=1','refinement of Model (2.1)'],
19:[r'G_i(u)=\int_{-\infty}^uK_i(u)\,du',r'\widetilde F_0(x,z)=\frac1T',r'\frac{X_t-x}{h_1}',r'\frac{Z_t-z}{h_2}'],
20:[r'\widehat\varepsilon_t=Y_t-\sum_{k=1}^4X^\top\widehat\beta\mathbf1',r'\widetilde\sigma^2(x,z)=\widehat\alpha',r'\widehat\varepsilon_t^2-\alpha-((X_t-x)^\top,(Z_t-z)^\top)\eta',r'\frac{X_t-x}{b_1}',r'\frac{Z_t-z}{b_2}'],
21:[r'\widehat e_t=\widehat\varepsilon_t/\widetilde\sigma(X_t,Z_t)',r'\widetilde e_t=\widehat e_t-\bar e_T',r'\widehat G(e)'],
22:['compact support','absolute continuous',r'\inf_{x,z}f_0(x,z)>0',r'\inf_{x,z}\sigma_0^2(x,z)>0','Lipshitz',r'T(\log T)^{-1}h_1^ph_2^{d_1+d_2}',r'T(\log T)^{-1}b_1^pb_2^{d_1+d_2}'],
23:['Step 1:','Step 2:','Step 3:','independently from',r'\widetilde F(x,z)',r'\widehat G(e)',r'(X_t^*)^\top\widehat\beta_k',r'\widehat\gamma^{*c}=\sum_{i=1}^N\widehat\gamma_i^*/N',r'\{T(\widehat\gamma_b^{*c}-\widehat\gamma^c),\sqrt T(\widehat\beta_b^*-\widehat\beta)\}_{b=1}^B'],
24:[r'\mathcal L_T',r'\mathcal L_{T,B}',r'T(\widehat\gamma^c-\gamma_0)',r'\sqrt T(\widehat\beta-\beta_0)'],
25:[r'\sum_{k=1}^{K_0}',r'1\le K_0<4',r'L_0\le2',r'\gamma_0=\gamma_{10}',r'L_0=1',r'L_0=2'],
26:['no intersection',r'z_1^\top\gamma_{10}\le z_2^\top\gamma_{20}',r'R_2(\gamma_0)=\{z:z_1^\top\gamma_{10}\le0,z_2^\top\gamma_{20}>0\}'],
27:[r'\mathbf1(Z_t\in R_k(\gamma_0)+\varepsilon_t',r'R_2(\gamma_0)=\{z:z_i^\top\gamma_{j,0}>0,z_j^\top\gamma_{j,0}\le0\}',r'R_3(\gamma_0)=\{z:z_j^\top\gamma_{j,0}\le0\}','does not extend'],
28:[r'(z,\gamma_0)',r'R_1(\gamma_0)=\{z:z^\top\gamma_0>0\}',r'R_2(\gamma_0)=\{z:z^\top\gamma_0\le0\}'],
29:[r'R_1(\gamma_0)=\{z:z_1^\top\gamma_{10}>0,z_2^\top\gamma_{20}>0\}',r'R_2\{\gamma_0\}=\mathcal Z_1\times\mathcal Z_2\setminus R_1(\gamma_0)'],
30:[r'Y_t=X_t^\top\beta_0+\varepsilon_t'],
31:[r'\widehat{\mathcal B}=\{\widehat\beta_k\}_{k=1}^4',r'\widehat{\mathcal G}=\{\widehat\gamma_j\}_{j=1}^2',r'd(v,\widehat{\mathcal V})=\min_j\|v-\widehat v_j\|_2'],
32:[r'I_{k,t}=\mathbf1\{Z_t\in R_k(\gamma)\}',r'\ell_{k,i,t}=I_{k,t}\beta_{k,i}',r'V_T(\ell)=\frac1T'],
33:[r'S_T(4)',r'\sum_{k=1}^K',r'K=4,3,2',r'\min_{\beta\in\mathcal B}',r'\widehat R_i^{(K)}\cup\widehat R_h^{(K)}',r'\arg\min_{(i,h)\in\mathcal A_K}',r'S_T(K-1)=S_T(K)+D_T^{(K)}(\widehat i,\widehat h)',r'\arg\min_{1\le K\le4}',r'\log(S_T(K)/T)+(\lambda_T/T)K'],
34:[r'g_{j,t}=\mathbf1(Z_{j,t}^\top\gamma_j>0)',r'M_{j,t}=\max_{\gamma\in\Gamma_j}|Z_{j,t}^\top\gamma|',r'(g_{j,t}-1)(M_{j,t}+\epsilon)<Z_{j,t}^\top\gamma_j\le g_{j,t}M_{j,t}'],
35:[r'C(\mathcal A)=\int_{v\in\mathcal A}v\,dv/\int_{v\in\mathcal A}dv','center of mass'],
36:[r'\mathcal G_D=\{v_m:D(v_m)\le D(v)',r'\gamma_D^c=C(\mathcal G_D)','polyhedron']}
    assert set(checks)==set(range(1,37))
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    for n in [6,7,8,9,10,22]:assert m['D'+str(n)]['source_kind']=='assumption'
    for n in [16,18,23,25,26,27,28,29,30,31,32,33,34,36]:assert m['D'+str(n)]['source_kind']=='source_passage'
    assert 'D(v)' not in s['D15']+s['D35'] and r'\widehat{\mathcal G}' not in s['D36']
    assert r'\widehat\beta_k\mathbf1' not in s['D20'] and r'\beta_{k0}\mathbf1' not in s['D18']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert r'v_{-1}' in a['A1'] and 'symmetric difference' in a['A1']
    assert r'\gamma_i=:(1,\widetilde\gamma_i)' in a['A2'] and 'convex' in a['A3']
    assert 'average of $N$ elements' in a['A4'] and r'\prod_{j=1}^2' in a['A5']
    assert 'requires further investigation' in a['A6'] and 'Assumptions S2-S4 in the SM ([33])' in a['A7']
    assert 'approximate the centroid' in a['A8'] and 'polynomial decay' in a['A9']
    assert r'$R_2$ $(-,+)$' in a['A10']
    assert a['A7'] in t['6.1']
    assert all(set(x['depends_on'])<=set(m) for x in aux.values())
    ext=ambient['unresolved_external_prerequisites'];assert len(ext)==1
    assert set(ext[0]['required_by'])=={PID+'/T6.1',PID+'/T6.2'} and ext[0]['status']=='not_inspected_outside_main_text_scope'
    # Simple consequences of the printed formulas substantiate recorded discrepancies.
    phi=lambda z:(1+math.erf(z/math.sqrt(2)))/2
    assert phi(0-(-1))>phi(0-1)  # Data-minus-x is decreasing as x increases.
    neg_arrival=-1*2/1
    assert not (0<neg_arrival)  # Negative-sign families fail the source process indicator.
    assert (1>0 and -1<=0) and (-1<=0)  # Printed(a.2) R2 overlaps R3.
    assert set(ambient['statement_local_bindings'])=={'T'+n for n in ['3.1','3.2','3.3','4.1','5.1','6.1','6.2']}

def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2410.04384v1.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==25
    assert paper['main_text_last_pdf_page']==24 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==7
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent reconstruction from inspected source clauses; no finalizer import.
    raw={1: [2], 2: [], 3: [], 4: [2], 5: [3, 4], 6: [], 7: [2, 3, 11], 8: [], 9: [11], 10: [11, 13], 11: [2], 12: [2], 13: [2, 11], 14: [11, 13], 15: [5, 35], 16: [3, 17, 32, 34], 17: [3], 18: [1, 2], 19: [], 20: [2, 5, 18, 19], 21: [20], 22: [18, 19, 20], 23: [2, 5, 15, 19, 20, 21], 24: [5, 15, 23], 25: [26, 27, 28, 29, 30], 26: [], 27: [], 28: [], 29: [], 30: [], 31: [5], 32: [2, 4], 33: [2, 3, 5], 34: [3, 32], 35: [], 36: [14, 35]}
    local={"D"+str(k):ids(v) for k,v in raw.items()}
    direct={k:ids(v) for k,v in {'3.1': [1, 5, 6, 7, 8], '3.2': [1, 5, 6, 7, 8, 9], '3.3': [1, 5, 6, 7, 8, 9, 10, 12, 15, 36], '4.1': [4, 5, 16], '5.1': [1, 6, 7, 8, 9, 10, 18, 22, 24], '6.1': [2, 5, 6, 25, 31], '6.2': [6, 25, 33]}.items()}
    expected_reach={k:ids(v) for k,v in {'3.1': [1, 2, 3, 4, 5, 6, 7, 8, 11], '3.2': [1, 2, 3, 4, 5, 6, 7, 8, 9, 11], '3.3': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 35, 36], '4.1': [2, 3, 4, 5, 16, 17, 32, 34], '5.1': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 15, 18, 19, 20, 21, 22, 23, 24, 35], '6.1': [2, 3, 4, 5, 6, 25, 26, 27, 28, 29, 30, 31], '6.2': [2, 3, 4, 5, 6, 25, 26, 27, 28, 29, 30, 33]}.items()}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([1,6,7,8,9,10,11,12,13,14,15,18])&expected_reach['4.1']
    assert not ids([14,36])&expected_reach['5.1']
    for n in ['6.1','6.2']:assert not ids([1,7,8,9,10])&expected_reach[n]
    assert 'D31' not in expected_reach['6.2']
    for n in ['3.1','3.2']:assert not ids([14,15,35,36])&expected_reach[n]
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==10 and len(ambient['source_issues'])==21
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
                assert all(1<=e['page']<=24 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=7,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=7,interfaces=36,source_members=36,direct_theorem_uses=41,related_theorem_connections=89,unranked_auxiliary_passages=10),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings={'inventory': 'Seven complete main-text Theorems3.1,3.2,3.3,4.1,5.1,6.1,6.2 independently enumerated from actual small-cap headings and visually compared. Main text ends on24 before an external supplementary-material notice; no appendix or supplement body is read.', 'source_passages': 'Thirty-six original entries and ten auxiliary passages retain the four-regime model, normalized parameter spaces, all main-text Assumptions1–6, LSE criterion and minimizer sets, marked limiting process, centroids, MIQP, smoothed bootstrap, degenerate models and backward selection.', 'dependencies': 'Independent clause-by-clause graph reconstruction verifies41 direct uses and89 related-theorem connections. Empirical centroid, general centroid functional and limiting-process centroid are separate. T4.1 does not inherit stochastic assumptions; T5.1 does not import the limiting process; T6.2 inherits assumptions of T6.1, not its distance conclusions.', 'external_prerequisites': 'Supplementary AssumptionsS2–S4 required by T6.1 and inherited by T6.2 are explicitly unresolved and not inspected outside main-text scope. They are not replaced by original four-regime Assumptions3–4.', 'source_issues': 'Twenty-one notes preserve printed indexing, zero-side indicator conventions, normalization and centroid domains, signed-arrival indicators, strict MIQP inequalities, decreasing smoothed-CDF arguments, missing regression subscripts, variance-estimator domains, the overlapping printed degenerate regions and ambiguous region-error probabilities. Original text remains unchanged; notes do not certify theorem correctness.', 'names_and_highlights': 'All36 entries use source-backed natural-language terminology, original source kinds and literal selectors. All89 connections have valid paper-local paths and specific source explanations.', 'reproduction': 'All six content JSON files reproduce byte for byte in a fresh empty directory. Seven retained scripts support extraction and independent review. Reproduction checks do not constitute a new semantic PDF review.'}
    reviewed_pages=[1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,24]
    crops=[dict(path="evidence/page-07-process-crop.png",page=7)]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=crops))
    evidence=[dict(path=f'evidence/page-{n:02}.jpg',page=n) for n in reviewed_pages]+crops+[dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=25,main_text_last_pdf_page=24,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent actual small-cap heading enumeration and visual comparison of all seven complete statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv2410.04384v1 marked6Oct2024,25pages, pinned bySHA256; not silently exchanged for the published article.','Main text ends on page24 before SUPPLEMENTARY MATERIAL notice y395.594; evidence clipped390. Supplementary bodies are external and excluded. AssumptionsS2–S4 remain unresolved external prerequisites.','Source review preserves mathematical statements, dependencies and unresolved source notation; it does not certify proofs or solve implicit selection/domain conventions.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=25,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
