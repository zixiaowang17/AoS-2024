"""Verify frozen, source-reviewed content using independent branch and graph checks."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '576e85d4ffa01d85dd1e269189e9e1b06d9f24f981b3610bd271061de52083cb', 'source-passages.json': '0904c1703bb17a79d414a2861f9a8e9111f04893e5af17ba6b63557919760026', 'interface-extraction.json': '5cb3036e1778b91673512a0dde1b2b174a5c25b2eecc801a9b982363c5508cbe', 'ambient-prerequisites.json': 'db33c6b43e32a78caaf17c72a2dfcd8842216b0357ced4f1277d97779e3085b6', 'unfinalized-census.json': '11f2cf681ef9c6108c21b0e4fda0c1d993e82f12f862bc2ac346f1629fcf43a2', 'ranked-interfaces.json': 'aafcf8235ac74d31dfc81e47fd831b97fdd4380d497bcfa9ef99a70b7dd1238a'}
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
    assert registered['version']=='2112.14758v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2112.14758'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==56
    assert paper['main_text_last_pdf_page']==29 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==6
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independently reconstructed from the original source definitions and statement clauses.
    raw={1:[],2:[1],3:[],4:[],5:[],6:[],7:[5,6],8:[7],9:[7],10:[8],11:[7],12:[],13:[12],14:[12],15:[],16:[],17:[],18:[],19:[7],20:[],21:[]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'1':ids([1,2,3,4]),'2':ids([12,15,16,17]),'3':ids([8,9,12,18]),'4':ids([10,13,18]),'5':ids([10,14,18,19,20]),'6':ids([11,13,18,19,21])}
    expected_reach={'1':ids([1,2,3,4]),'2':ids([12,15,16,17]),'3':ids([5,6,7,8,9,12,18]),'4':ids([5,6,7,8,10,12,13,18]),'5':ids([5,6,7,8,10,12,14,18,19,20]),'6':ids([5,6,7,11,12,13,18,19,21])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids(range(5,22))&expected_reach['1']
    assert not ids([5,6,7,8,9,10,11,18,19,20,21])&expected_reach['2']
    assert not ids([15,16,17])&(expected_reach['3']|expected_reach['4']|expected_reach['5']|expected_reach['6'])
    assert 'D21' not in expected_reach['3']|expected_reach['4']|expected_reach['5']
    assert 'D20' in expected_reach['5'] and 'D20' not in expected_reach['6']
    assert 'D9' not in expected_reach['4']|expected_reach['5']|expected_reach['6']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==11 and len(ambient['source_issues'])==12
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
    counts=dict(theorems=6,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=6,interfaces=21,source_members=21,direct_theorem_uses=25,related_theorem_connections=42,unranked_auxiliary_passages=11),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Six complete main-text Theorems1–6, independently enumerated by bold headings. Include credited Theorem2, the entire essential-variation slicing statement, every tuning/minimax regime, and all italic attainment paragraphs after Theorems5–6 displays. Acknowledgements end before References on page29.',
      source_passages='Twenty-one original entries preserve anisotropic BV and essential variation, coordinate slices, lattice and shrinking-row difference matrices, Kronecker penalty, KTV seminorm/estimator/ball, discrete Sobolev ball, Gaussian experiment, two risks, general lasso/incoherence/nullity, effective smoothness, spectral projection, max-degree polynomials and canonical radius sequences. Eleven auxiliary passages preserve proof context and alternative conventions.',
      dependencies='Independent reconstruction checks25 direct uses and42 related connections. Analytic Theorem1 has no statistical or lattice dependencies. General-matrix Theorem2 has no KTF assumptions. Theorem3 does not import its proof application of Theorem2 as a statement dependency. Minimax theorems need their parameter classes and named projection witnesses, not the KTF estimator itself.',
      scope='Maintain essential versus unrestricted variation, anisotropic versus isotropic TV, coordinatewise discrete Sobolev versus mixed-derivative continuum spaces, OP estimation error versus expected minimax risk, and linear versus unrestricted estimators. All rate terms and positive-radius regimes are preserved, including the critical multiplying logarithm and fixed k,d convention.',
      source_issues='Twelve source notes retain the fixed-length Delta versus shrinking-row boundary mismatch, approximate-continuity external reference, fiber conventions, seminorm/radius domains, left-versus-right singular-vector conventions, projection rounding and null-space retention, canonical-rate floor omission, critical log qualifications and the explanatory norm-inequality typo. Original statements are not silently repaired.',
      names_and_highlights='All21 entries use natural-language source terms, source kinds/headings and literal highlight selectors. Every related theorem has a source-backed same-paper path and explanation. Holder classes and Proposition3 remain original unranked proof context, with no implication-only subset edge.',
      reproduction='All six content JSON artifacts reproduce byte for byte in a fresh directory. Seven saved per-paper scripts retain inventory enumeration, extraction, context, finalization, rebuild and independent source review with frozen hashes and formula checks.')
    reviewed_pages=[2,3,4,9,11,12,13,14,15,16,17,18,29]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[]))
    evidence=[dict(path='evidence/page-'+str(n).zfill(2)+'.jpg',page=n) for n in reviewed_pages]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=56,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-font heading enumeration and visual comparison of all six complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark','Conjecture'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2112.14758v2 dated 5 Apr 2024, pinned by SHA-256. No substitution with a different version.','Main text and acknowledgments end on PDF page29, clipped at y=637 before References at y=643.204. All appendix bodies excluded; proof context is archived without importing proof-only dependencies.','Source and schema validation do not certify proofs or resolve the explicitly recorded source ambiguities.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=56,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'\int_U f(x)\operatorname{div}\phi(x)',r'C_c^\infty(U;\mathbb R^d)',r'\|\phi(x)\|_\infty\le1',r'\operatorname{div}\phi=\sum_{j=1}^d\partial\phi_j/\partial x_j'],
2:[r'f\in L^1(U)',r'\operatorname{TV}(f;U)<\infty',r'\operatorname{BV}(U)'],
3:[r'z_1,\ldots,z_{m+1}\in\operatorname{AC}(g)',r'a<z_1<\cdots<z_{m+1}<b','Section 1.7.2','Lebesgue almost everywhere'],
4:[r'U_{-j}',r'I_{x_{-j}}=[a_{x_{-j}},b_{x_{-j}}]',r'\inf\{x_j',r'\sup\{x_j'],
5:[r'n=N^d',r'\{1/N,2/N,\ldots,1\}^d:=Z_{n,d}'],
6:[r'\mathbb R^{(n-k-1)\times n}',r'D_n^{(k+1)}=D_{n-k}^{(1)}D_n^{(k)}'],
7:[r'D_N^{(k+1)}\otimes I_N',r'I_N\otimes D_N^{(k+1)}',r'\mathbb R^{(N-k-1)\times N}','Kronecker product'],
8:[r'\|D_{n,d}^{(k+1)}\theta\|_1','Kronecker total variation'],
9:[r'\frac12\|y-\theta\|_2^2+\lambda\|D_{n,d}^{(k+1)}\theta\|_1','(7)'],
10:[r'\rho>0',r'\mathcal T_{n,d}^k(\rho)',r'\|D_{n,d}^{(k+1)}\theta\|_1\le\rho'],
11:[r'\mathcal W_{n,d}^{k+1}(\rho)',r'\|D_{n,d}^{(k+1)}\theta\|_2\le\rho','rather than considering all mixed derivatives'],
12:[r'y_i\sim N(\theta_{0,i},\sigma^2)','independently','i.i.d. normal errors'],
13:[r'\inf_{\widehat\theta}\sup_{\theta_0\in K}\frac1nE\|\widehat\theta-\theta_0\|_2^2'],
14:[r'\inf_{\widehat\theta\text{ linear}}',r'\widehat\theta=Sy',r'S\in\mathbb R^{n\times n}'],
15:[r'D\in\mathbb R^{r\times n}',r'\frac12\|y-\theta\|_2^2+\lambda\|D\theta\|_1'],
16:[r'u_1,\ldots,u_q\in\mathbb R^r',r'\|u_i\|_\infty\le\mu/\sqrt n',r'i\in[q]\setminus I'],
17:['dimension of the null space'],
18:[r's=\frac{k+1}d','effective smoothness'],
19:[r'i\in[N]^d',r'(k+1)^d','right singular vectors',r'\widehat\theta=V_QV_Q^Ty'],
20:[r'\sum_{j=1}^da_j\le k',r'a_j\le k','max degree'],
21:[r'B_n^*=n^{\frac12-\frac{k+1}d}',r'C_n^*=n^{1-\frac{k+1}d}']}
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert r'\|\phi(x)\|_2' not in s['D1']
    assert 'weakly differentiable' not in s['D2']
    assert r'D_{n,d}' not in s['D15'] and 'incoherent' not in s['D9']
    assert all(m['D'+str(n)]['source_kind']=='theorem_excerpt' for n in [4,15,16])
    a={k:v['statement_original'] for k,v in aux.items()}
    ac={1:[r'y_i=f_0(x_i)+\epsilon_i','mean zero stochastic errors'],2:[r'\lambda\ge0'],3:['bounded in probability',r'n\to\infty','with $k,d$ fixed'],4:[r'\sup_{a<z_1<\cdots<z_{m+1}<b}'],5:[r'0&\text{else.}',r'(\Delta^2\theta)(x_i)=(\Delta(\Delta\theta))(x_i)','(6)'],6:[r'f\in W^{1,1}(U)',r'\int_U\|\nabla f(x)\|_1'],7:[r'\alpha_1+\cdots+\alpha_d=k',r'\le L\|x-z\|_2','Holder class'],8:[r'\mathcal C_{n,d}^k(L)',r'\theta(x)=f(x)'],9:[r'c_1Ln^{\frac12-\frac{k+1}d}',r'c_2Ln^{1-\frac{k+1}d}','constants depending only on'],10:[r'\|v\|_2\le\sqrt p\|\theta\|_1',r'\sqrt{dn}\rho'],11:[r'(k+1)^d',r'x_1^{a_1}x_2^{a_2}\cdots x_d^{a_d}',r'\{0,\ldots,k\}']}
    for n,parts in ac.items():
        for v in parts:assert v in a['A'+str(n)],(n,v)
    for o in aux.values():assert set(o['depends_on'])<=set(m)
    assert set(ambient['statement_local_bindings'])=={'T1','T2','T3','T4','T5','T6'}
    assert ambient['statement_local_bindings']['T6']['proof_context']==['A7','A8','A9']
    assert {x['issue_id'] for x in ambient['source_issues']}=={'anisotropic-essential-variation','slice-endpoints-and-dimension','difference-boundary-discrepancy','lattice-order-and-seminorm-domains','generalized-lasso-incoherence','risk-versus-probability-bounds','radii-and-truncation-orders','canonical-rate-floor','critical-logarithm-and-linear-rates','singular-basis-and-polynomial-space','holder-embedding-norm-typo','proof-context-not-assumptions'}
    refs=ambient['source_claim_references'];assert sum(x['reference_kind']=='definition_reference' for x in refs)==5
    assert sum(x['reference_kind']=='proof_only' for x in refs)==2
    assert sum(x['reference_kind']=='external_definition_reference' for x in refs)==1
    # Direct finite example checks the recorded boundary discrepancy, not a theorem proof.
    theta=[0,1,2]
    delta=lambda v:[v[i+1]-v[i] for i in range(len(v)-1)]+[0]
    shrinking=lambda v:[v[i+1]-v[i] for i in range(len(v)-1)]
    assert delta(delta(theta))==[0,-1,0] and shrinking(shrinking(theta))==[0]
if __name__=='__main__':main()
