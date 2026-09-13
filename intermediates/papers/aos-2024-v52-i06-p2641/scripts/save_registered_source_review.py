"""Independently check source-reviewed content and reconstruct theorem dependencies."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '8de43c5995515c4416c053d76e4490d7ce29a0f00d947da94fef33fdb0fad5d9', 'source-passages.json': 'c35e1a1e2f53bf3084a3a4f081319de3090088972da157b3f538c5598f87bd37', 'interface-extraction.json': '0e7dff322b9349d56f034156a517e8ba6e5525bd1805d1cdb0a1cd05bbb80cf0', 'ambient-prerequisites.json': '847529e2636bf7f7087b900d594ab52d6add03431f5ca65231872bdda073e52b', 'unfinalized-census.json': '109d24cd9cb83a740b546df13bfe7799be358ebf53d1c9761509ba3257db228b', 'ranked-interfaces.json': 'd4f7977f2d5ba44ca0c59cf66c02a46a0443ba6062cc89ea39df28fbdb127752'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'\mathcal X_t=\mathcal F_t\times_1 A_1','not necessarily orthonormal',r'r_k'],
2:[r'\mathcal X\times_k U',r'\sum_{i_k=1}^{d_k}',r'U_{j,i_k}',r"d'_k"],
3:[r'\operatorname{mat}_k(\mathcal A)',r'j+m_2(k-1)',r'k+m_3(i-1)',r'i+m_1(j-1)'],
4:[r'\mathcal A\otimes\mathcal B',r'(\mathcal A)_{i_1,\ldots,i_K}(\mathcal B)_{j_1,\ldots,j_N}'],
5:[r'\|A\|_{\mathrm S}=\sigma_1(A)'],
6:[r'\sum_{i_1=1}^{m_1}',r'(\mathcal A)^2_{i_1,\ldots,i_K}','Frobenius norm'],
7:[r'u_{i_1,i_2}\cdot u_{i_3,i_4}',r'\|U_1\|_{\mathrm{HS}}=\|U_2\|_{\mathrm{HS}}=1',r'U_1=(u_{i_1,i_2})',r'U_2=(u_{i_3,i_4})'],
8:[r'A_k(A_k^\top A_k)^{-1}A_k^\top=U_kU_k^\top',r'A_k=U_k\Lambda_kV_k^\top'],
9:[r'\sum_{t=h+1}^T',r'\mathcal X_{t-h}\otimes\mathcal X_t',r'{T-h}','order-$2K$'],
10:[r'\mathrm{TOPUP}_k',r'\operatorname{mat}_k(\widehat\Sigma_h)',r'd_k\times(dd_{-k}h_0)','predetermined positive integer'],
11:['first $m$ left singular vectors','largest $m$ singular values'],
12:[r'\mathrm{TIPUP}_k',r'\operatorname{mat}_k(\mathcal X_{t-h})\operatorname{mat}_k^\top(\mathcal X_t)',r'd_k\times(d_kh_0)'],
13:['1: Input','2: Let','3: repeat','4: Let','5: until','6: Estimate and output',r'\times_{k-1}(\widehat U_{k-1}^{(j)})^\top',r'\times_{k+1}(\widehat U_{k+1}^{(j-1)})^\top',r'\text{-}\mathrm{INIT}_k',r'\text{-}\mathrm{ITER}_k',r'\widehat{\mathcal F}_t^{\mathrm{iFinal}}',r'\widehat{\mathcal E}_t^{\mathrm{iFinal}}'],
14:['TOPUP operator (2.5)','for both','Algorithm 1','iTOPUP procedure'],
15:['iTIPUP uses','TIPUP operator (2.8)','for both'],
16:['TIPUP for $\widehat U_k$-INIT','TOPUP for $\widehat U_k$-ITER','TIPUP-iTOPUP'],
17:[r'\overline{\mathbb E}[\cdot]=\mathbb E[\cdot\mid\{\mathcal F_1,\ldots,\mathcal F_T\}]'],
18:['independent Gaussian tensors conditionally',r'\mathcal F_t,t\in\mathbb Z',r'\overline{\mathbb E}(u^\top\operatorname{vec}(\mathcal E_t))^2\le\sigma^2\|u\|_2^2'],
19:[r'\Theta_{k,h}',r'\operatorname{mat}_k(\mathcal M_{t-h})\otimes\operatorname{mat}_k(\mathcal M_t)',r'd_k\times d_{-k}\times d_k\times d_{-k}'],
20:[r'\Theta^*_{k,h}',r'\operatorname{mat}_k(\mathcal M_{t-h})\operatorname{mat}_k^\top(\mathcal M_t)'],
21:[r'\sigma_m\left(\overline{\mathbb E}[\mathrm{TOPUP}_k]\right)',r'\operatorname{mat}_1(\Theta_{k,1:h_0})',r'\operatorname{mat}_1(\Phi_{k,1:h_0}^{(cano)})',r'\lambda_k=\sqrt{h_0^{-1/2}\tau_{k,r_k}}'],
22:[r'\sigma_m(\overline{\mathbb E}(\mathrm{TIPUP}_k))',r'\Phi_{k,1:h_0}^{*(cano)}',r'\lambda_k^*=\sqrt{h_0^{-1/2}\tau^*_{k,r_k}}'],
23:[r'\sqrt{d_kd_{-k}r_{-k}}',r'\sqrt{d_{-k}r}',r'\sigma\sqrt{d_k}d_{-k}',r'\sigma d_k\sqrt{d_{-k}}T^{-1/2}'],
24:[r'R_k^{(TOPUP)}=\mathscr R_{k2}+(R_k^{(0)})^2'],
25:[r'R_k^{(ideal)}=\mathscr R_{k2}+\mathscr R_{k1}^2',r'\sqrt{d_k}r_{-k}',r'\sqrt{r_{-k}r}',r'\sigma\sqrt{d_k}r_{-k}',r'\sigma d_k\sqrt{r_{-k}}T^{-1/2}'],
26:[r'd^*_{-k}=\sum_{j\ne k}d_jr_j',r'\lambda_k^{-2}\sigma^2T^{-1}',r'd^*_{-k}+\sqrt{d^*_{-k}d_kr_{-k}}'],
27:[r'R_k^{*(0)}=(\lambda_k^*)^{-2}',r'\|\Theta^*_{k,0}\|_{\mathrm S}^{1/2}+\sigma\sqrt{d_{-k}}'],
28:[r'R_k^{*(ideal)}=(\lambda_k^*)^{-2}',r'\|\Theta^*_{k,0}\|_{\mathrm S}^{1/2}+\sigma\sqrt{r_{-k}}'],
29:[r'R_k^{*(add)}=\sqrt{d^*_{-k}/d_k}R_k^{*(ideal)}'],
30:['unordered group','different vertices','each hyper-edge $e$ is drawn independently','uniformly sampled','sampling independently',r'\mathcal A_{i_1,\ldots,i_m}',r'\mathcal G_m(N,1/2,\kappa)'],
31:[r'm\ge2','fixed integer',r'\limsup_{N\to\infty}',r'\frac{\log\kappa}{\log N}\le\frac12-\delta','for any',r'\delta>0',r'\mathbb P_{H_0^G}(\psi(\mathcal A)=1)',r'\mathbb P_{H_1^G}(\psi(\mathcal A)=0)',r'>1/2'],
32:['mean 0 and independent',r'\lambda\mathcal F_t\times_1 U_1',r'U_k^\top U_k=I',r'0<c_1\le\sigma_{\min}',r'\sigma_{\max}',r'c_2<\infty',r'\frac1{T-1}\sum_{t=2}^T',r'\mathcal F_{t-1,i_1,\ldots,i_K}=c_0>0',r'\overset{\mathrm{i.i.d.}}\sim N(0,\sigma^2)'],
33:[r'\Phi_{k,h}^{(cano)}',r'\mathcal M_{t-h}\times_{k=1}^K U_k^\top',r'\otimes','canonical version'],
34:[r'\Phi_{k,h}^{*(cano)}=U_k^\top\Theta^*_{k,h}U_k',r'\operatorname{mat}_k^\top(\mathcal M_t\times_{k=1}^K U_k^\top)'],
35:['SVD of (2.4)',r'\widehat U_k\text{-}\mathrm{TOPUP}(\mathcal X_{1:T},m)',r'\mathrm{LSVD}_m',r'\widehat\Sigma_h(\mathcal X_{1:T})'],
36:[r'\widehat U_k\text{-}\mathrm{TIPUP}(\mathcal X_{1:T},m)',r'\mathrm{LSVD}_m',r'\operatorname{mat}_k(\mathcal X_{t-h})\operatorname{mat}_k^\top(\mathcal X_t)'],
37:[r'\mathscr R_{k2}',r'\sqrt{r_k}r_{-k}',r'\sqrt{rr_{-k}}',r'\sigma(\sqrt{d_k}+\sqrt{rr_{-k}})',r'\sigma\sqrt{d_k}rT^{-1/2}']}
    assert set(checks)==set(range(1,38))
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    for n in [23,25,37]:
        assert r'\sqrt{d_kr_{-k}}' not in s['D'+str(n)]
    assert r'\sqrt{r_kr_{-k}}' not in s['D37']
    assert r'\sigma\sqrt{d_kd_{-k}}' not in s['D23']
    assert 'widehat' not in s['D27'] and 'overline' not in s['D27']
    assert 'TOPUP' not in s['D25'] and 'TOPUP' not in s['D37']
    assert m['D18']['source_kind']==m['D31']['source_kind']=='assumption'
    for n in [1,13,24,32,37]:assert m['D'+str(n)]['source_kind']=='source_passage'
    a={k:v['statement_original'] for k,v in aux.items()}
    assert r'\mathcal X_t=\mathcal M_t+\mathcal E_t' in a['A1']
    assert 'deterministic loading matrix' in a['A2'] and 'independence between the core process and the noise process' in a['A3']
    assert r'd_{-k}=d/d_k' in a['A4'] and r'\sum_{j\ne k}d_jr_j' in a['A5']
    assert r'\Theta_{k,1:h_0}' in a['A6'] and r'\Phi_{k,1:h_0}^{*(cano)}' in a['A7']
    assert 'descending order' in a['A8'] and 'smallest nontrivial' in a['A9']
    assert 'for all sufficiently large' in a['A10'] and 'vectorization' in a['A11']
    assert 'given ranks' in a['A12'] and r'\mathcal F_t^{(cano)}' in a['A13']
    assert r'\widehat P_k^{(TIPUP)}' in a['A14']
    assert all(set(x['depends_on'])<=set(m) for x in aux.values())
    assert set(ambient['statement_local_bindings'])=={'T3.1','T3.2','T3.3','T3.4','T3.5'}
    assert 'Assumption 2' not in ''.join(t.values())
    assert 'Hypothesis I' not in t['3.5'] and 'polynomial-time' not in t['3.5']

def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2006.02611v3.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==58
    assert paper['main_text_last_pdf_page']==24 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==5
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent reconstruction from the inspected source clauses; no finalizer import.
    raw={1:[2],2:[],3:[],4:[],5:[],6:[],7:[6],8:[1],9:[4],10:[3,9],11:[],12:[3],13:[2,5],14:[13,35],15:[13,36],16:[13,35,36],17:[1],18:[1,17],19:[1,3,4],20:[1,3],21:[3,10,17,19,33],22:[12,17,20,34],23:[5,7,19,20,21],24:[23,37],25:[5,7,19,20,21,23,37],26:[21],27:[5,20,22],28:[5,20,22],29:[28],30:[],31:[30],32:[2],33:[1,2,3,4,8],34:[1,2,3,8,20],35:[3,9,10,11],36:[3,11],37:[5,7,19,20,21]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={k:ids(v) for k,v in {'3.1':[5,8,14,17,18,19,20,21,23,24,25,26],'3.2':[5,8,15,17,18,20,22,27,28,29],'3.3':[5,8,16,18,23,25,26,27],'3.4':[5,31,32],'3.5':[5,32]}.items()}
    expected_reach={
        '3.1':ids([1,2,3,4,5,6,7,8,9,10,11,13,14,17,18,19,20,21,23,24,25,26,33,35,37]),
        '3.2':ids([1,2,3,5,8,11,12,13,15,17,18,20,22,27,28,29,34,36]),
        '3.3':ids([1,2,3,4,5,6,7,8,9,10,11,12,13,16,17,18,19,20,21,22,23,25,26,27,33,34,35,36,37]),
        '3.4':ids([2,5,30,31,32]),'3.5':ids([2,5,32])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([15,16,22,27,28,29,30,31,32,34,36])&expected_reach['3.1']
    assert not ids([4,6,7,9,10,14,16,19,21,23,24,25,26,33,35,37])&expected_reach['3.2']
    assert not ids([14,15,24,28,29,30,31,32])&expected_reach['3.3']
    assert not ids([1,8,18,31])&expected_reach['3.5']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==14 and len(ambient['source_issues'])==13
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
    counts=dict(theorems=5,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=5,interfaces=37,source_members=37,direct_theorem_uses=35,related_theorem_connections=80,unranked_auxiliary_passages=14),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(inventory='Exactly five complete main-text Theorems3.1–3.5, independently enumerated from actual small-cap headings and compared visually, including T3.3 across pages13–14. Main text ends on24 before references; supplements are excluded.',source_passages='Thirty-seven original entries and fourteen auxiliary passages preserve tensor operations, the general model and loading projection, TOPUP/TIPUP constructions, full Algorithm1 and its three branches, conditional noise assumption and expectation, signal moment tensors, distinct strengths/rates, HPC testing/HypothesisI and the separate lower-bound distribution class.',dependencies='Independent source-clause graph reconstruction verifies35 direct uses and80 related-theorem connections. The three algorithm branches stay distinct. T3.3 imports rate definitions, not complete theorem hypotheses. Rcal_k2 is separate from the R_TOPUP formula. Starred rate definitions do not inherit the risk assertion surrounding equation3.16.',source_issues='Thirteen notes preserve conditional-versus-unconditional notation, missing post-stop iterate conventions, T3.3 lag-bound wording, positive signal-strength domains, singular-vector selection, computational-hypothesis quantifiers and the lower-class covariance/independence notation. Enlarged crops verify all ambiguous radical extents in3.7–3.10. No appendix proof is used to repair the source.',lower_bounds='T3.4 assumes HypothesisI and uses a minimum over modes of squared spectral error. T3.5 has unsquared spectral loss and no computational restriction. Both use their own orthonormal-loading, serial-factor, iid-noise class(3.34)–(3.35), without importing general Assumption1 by implication.',names_and_highlights='All37 entries have literal author terminology, preserved source kind/heading and matching source selectors. All80 related links have valid same-paper paths and source-specific explanations. Publication-layout rendering and mathlib availability are outside this stage.',reproduction='All six content JSON files reproduce byte for byte in a fresh empty directory. Seven saved scripts support inventory, extraction, ambient context, finalization, rebuilding and independent source review. Reproduction does not claim a new semantic PDF review.')
    reviewed_pages=[1,2,5,6,7,8,9,10,11,12,13,14,21,22,23,24]
    crops=[dict(path='evidence/page-11-rate-crop.png',page=11),dict(path='evidence/page-11-ideal-crop.png',page=11),dict(path='evidence/page-10-initial-crop.png',page=10)]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=crops))
    evidence=[dict(path=f'evidence/page-{n:02}.jpg',page=n) for n in reviewed_pages]+crops+[dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=58,main_text_last_pdf_page=24,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent actual small-cap heading enumeration and visual comparison of all five complete statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv2006.02611v3 marked18Jul2024,58pages, pinned bySHA256; not silently exchanged for the published article.','Main text ends on page24 before REFERENCES y650.489; evidence clipped644. Supplementary bodies starting28 are excluded.','Source review preserves mathematical statements, dependencies and unresolved source notation; it does not certify proofs or solve implicit selection/domain conventions.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=58,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
