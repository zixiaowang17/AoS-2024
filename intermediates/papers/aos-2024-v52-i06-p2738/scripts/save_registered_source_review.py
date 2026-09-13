"""Check frozen source-reviewed content and independently reconstruct theorem reach."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '51b0517dc6b42a8d072ed29189f2dce2aeaa424f0a496a494e3cf9b7d49bdce7', 'source-passages.json': '116b4e514832b5787e8adff9df99759f240f70c78767b30dcadcd040c05d6266', 'interface-extraction.json': '9d2fb857a2a207114de9dddf46df4dcb66c5fe112f56178437869ed408142b36', 'ambient-prerequisites.json': 'c5b069add3380ebea60ceeb3edaf56c5cc99c95a79462cc1692e277e077f2ca3', 'unfinalized-census.json': '1d069ec50b59e20c7b11ce5a76bddb9846436993ed3a0286300e9c7215b09368', 'ranked-interfaces.json': '42ee437301c3d97b4d2d396f14fa391755e8765fbaa9659a86ec772b6270e44c'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:['centered error independent of',r'\sum_{j=1}^df_{0,j}(X_{i,j})',r'\sum_{j<k}f_{0,jk}(X_{i,j},X_{i,k})',r'f_0(X_i)'],
2:[r'\sup_{x\in[0,1]^d}p(x)=:p_{\max}<\infty','free of $d$','sub-gaussian'],
3:[r'\int_0^1f_{0,j}(x)\,dx=0',r'\int_0^1f_{0,ij}(x,y)\,dx=\int_0^1f_{0,ij}(x,y)\,dy=0',r'\|f_0\|_\infty\le B'],
4:[r'\lfloor\beta\rfloor','times differentiable',r'\beta-\lfloor\beta\rfloor','constant $L$'],
5:['number of hidden layers','maximum number of neurons','active (non-zero) weights',r'\mathcal F_{NN}(d,N,L,W,o)'],
6:[r'c_1dN_1\log N_1,c_2L_1\log L_1',r'c_3d(N_1\log N_1)^2L_1\log L_1',r'c_1d^2N_2\log N_2,c_2L_2\log L_2',r'c_3d^2(N_2\log N_2)^2L_2\log L_2','specially structured neural networks','then add them'],
7:['constant depth',r'c_1dN_1\log N_1,c_2,c_3d(N_1\log N_1)^2',r'c_1\binom d2N_2\log N_2,c_2,c_3\binom d2(N_2\log N_2)^2'],
8:[r'\operatorname{argmin}_{\phi_1\in\mathcal F^1_{NN},\phi_2\in\mathcal F^2_{NN}}',r'\frac1n\sum_{i=1}^n(Y_i-\phi_1(X_i)-\phi_2(X_i))^2',r'\widehat f_{\mathrm{big}}:=\widehat\phi_1+\widehat\phi_2',r'\operatorname{sgn}(\widehat f_{\mathrm{big}})(|\widehat f_{\mathrm{big}}|\wedge B)'],
9:[r'dn^{-\frac{2\beta_1}{2\beta_1+1}}',r'\binom d2n^{-\frac{\beta_2}{\beta_2+1}}',r'\log^{4.5}n=o(1)'],
10:[r'\mathbf S_n:=\{(X_i,Y_i),i\in[n]\}','training sample'],
11:[r'\mathfrak M(n,d,\mathcal F)',r'\mathbb E_f',r'\Sigma(\beta,L)','Assumption 2.3'],
12:[r'S_2\subset[d]\times[d]',r's_i:=|S_i|\ll n',r'\mathcal F_{\mathrm{sp}}',r'$\beta_1$ smooth',r'$\beta_2$ smooth'],
13:[r'\mathcal F_{NN}(1,c_1N_1\log N_1,c_2,c_3N_1^2\log^2N_1,1)',r'\mathcal F_{NN}(2,c_4N_2\log N_2,c_5,c_6N_2^2\log^2N_2,1)'],
14:['From Theorem 2.9',r'\|f_{0,j}-\phi_j^\star\|_\infty\le C_1N_1^{-2\beta_1}',r'\|f_{0,kl}-\phi_{kl}^\star\|_\infty\le C_2N_2^{-\beta_2}',r'\phi^\star=\sum_{j\in S_1}\phi_j^\star+\sum_{(k<l)\in S_2}\phi_{kl}^\star'],
15:[r's_1\left(n^{-\frac{2\beta_1}{2\beta_1+1}}\log^4n+\frac{\log d}n\right)',r's_2\left(n^{-\frac{\beta_2}{\beta_2+1}}\log^4n+\frac{\log d}n\right)=o(1)'],
16:[r'\|\cdot\|_n',r'L_2(\mathbb P_n)'],
17:[r'\|f_j\|_\infty\le B',r'\|f_{jk}\|_\infty\le B','truncate the component neural networks'],
18:[r'\frac1n\sum_i',r'\lambda_{n,1}\sum_j\|\phi_j\|_n',r'\lambda_{n,2}\sum_{k<l}\|\phi_{kl}\|_n','to be specified later'],
19:[r'\rho_{n,1}\le C_1N_1^{-2\beta_1}',r'\rho_{n,2}\le C_2N_2^{-\beta_2}','approximation error','bounded by (3.8)'],
20:[r'C_3\sqrt{\frac{V_{n,1}\log n}{n}+\frac{2\log d}{n}}',r'C_4\sqrt{\frac{V_{n,2}\log n}{n}+\frac{3\log d}{n}}',r'V_{n,1}=N_1^2\log^3N_1',r'V_{n,2}=N_2^2\log^3N_2'],
21:['for any function',r'4(s_1\rho_{n,1}^2+s_2\rho_{n,2}^2)',r'3\lambda_{n,1}\sum_{j\in S_1}',r'3\lambda_{n,2}\sum_{(k<l)\in S_2}',r's_1\lambda_{n,1}^2+s_2\lambda_{n,2}^2',r'\kappa_1^2\sum_{j\in S_1}',r'\kappa_2^2\sum_{(k<l)\in S_2}',r'\le\|\phi-\phi^\star\|_n^2'],
22:[r'\min_{j\in S_1}\|f_j^0\|_2\ge r_n',r'\min_{(j,k)\in S_2}\|f_{j,k}^0\|_2\ge r_n',r'r_n\gtrsim\sqrt',r'\log^4n'],
23:[r'$(n+1)/2$',r'$(n-1)/2$',r'\mathcal D_1',r'\mathcal D_2','by solving (3.5)',r'\|\widehat\phi_j^{\mathrm{init}}\|_n\ge c_1\lambda_{n,1}',r'\|\widehat\phi_{jk}^{\mathrm{init}}\|_n\ge c_2\lambda_{n,2}',r'\frac1n\sum_i','un-penalized',r'\widehat f^{\mathrm{final}}='],
24:['distribution satisfying Assumption 2.1',r'\|\widehat f-f_0\|_{L_2(P_X)}^2',r'\|\widehat f-f_0\|_n^2']}
    assert set(checks)==set(range(1,25))
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    for n,label in [(2,'2.1'),(3,'2.2 (Identifiability and boundedness)'),(4,'2.3'),(9,'2.6'),(15,'3.1'),(21,'3.4'),(22,'3.7')]:
        assert m['D'+str(n)]['source_kind']=='assumption' and m['D'+str(n)]['source_heading']=='Assumption '+label
    assert m['D17']['source_kind']=='condition'
    assert m['D19']['source_kind']==m['D20']['source_kind']=='theorem_excerpt'
    assert m['D23']['source_heading']=='Algorithm 1: Estimation under random design setting'
    assert r'\mathbb E' not in t['3.9'] and r'\log^{4.5}' not in s['D15']
    assert r'\|f_0\|_\infty' not in s['D17'] and 'L_1' not in s['D7']
    assert r'\phi_2\in\mathcal F^1_{NN}' in t['2.7']
    assert 'upto log-factors' in t['3.8'] and r'\|f_j^0\|_2^2' not in s['D22']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert 'independent of $X$' in a['A1'];assert r'$\beta_1$' in a['A2']
    assert r'+\tau_n' in a['A3'] and 'Assumption 2.6' in a['A4']
    assert 'fixed' in a['A5'] and 'second half of the data' in a['A6']
    assert 'ReLU' in a['A7'] and 'gradient descent-based estimator' in a['A8']
    assert 'explicitly in the proof' in a['A9'] and r'\sigma(x)-\sigma(-x)=x' in a['A10']
    assert len(ambient['unresolved_external_prerequisites'])==1
    assert ambient['unresolved_external_prerequisites'][0]['status']=='outside_scope_unresolved'

def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2302.05851v1.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==46
    assert paper['main_text_last_pdf_page']==23 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==7
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent reconstruction from inspected source clauses; no finalizer import.
    raw={1: [], 2: [], 3: [1], 4: [1], 5: [], 6: [5], 7: [5], 8: [3, 7], 9: [4], 10: [1], 11: [1, 4], 12: [4], 13: [5], 14: [12, 13], 15: [12], 16: [], 17: [12], 18: [13, 16, 17], 19: [12, 13], 20: [13], 21: [12, 14, 16, 19, 20], 22: [12], 23: [13, 16, 18, 20], 24: [2]}
    local={"D"+str(k):ids(v) for k,v in raw.items()}
    direct={k:ids(v) for k,v in {'2.7': [1, 2, 3, 4, 6, 9], '2.9': [1, 2, 3, 4, 7, 8, 9, 10], '2.12': [1, 2, 3, 4, 9, 11], '3.2': [2, 3, 4, 12, 15, 16, 17, 18, 19, 20], '3.5': [2, 3, 4, 12, 15, 16, 17, 18, 19, 20, 21], '3.8': [3, 12, 15, 20, 21, 22, 23, 24], '3.9': [2, 3, 12, 15]}.items()}
    expected_reach={k:ids(v) for k,v in {'2.7': [1, 2, 3, 4, 5, 6, 9], '2.9': [1, 2, 3, 4, 5, 7, 8, 9, 10], '2.12': [1, 2, 3, 4, 9, 11], '3.2': [1, 2, 3, 4, 5, 12, 13, 15, 16, 17, 18, 19, 20], '3.5': [1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], '3.8': [1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], '3.9': [1, 2, 3, 4, 12, 15]}.items()}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert 'D7' not in expected_reach['2.7'] and 'D6' not in expected_reach['2.9']
    assert not ids([5,6,7,8,13,14,18,20,21,23])&expected_reach['3.9']
    assert 'D21' not in expected_reach['3.2'] and 'D21' in expected_reach['3.5']
    assert 'D23' in expected_reach['3.8'] and 'D23' not in expected_reach['3.5']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==10 and len(ambient['source_issues'])==15
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
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=7,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=7,interfaces=24,source_members=24,direct_theorem_uses=53,related_theorem_connections=74,unranked_auxiliary_passages=10),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings={'inventory': 'Seven original main-text Theorems2.7,2.9,2.12,3.2,3.5,3.8,3.9 independently enumerated and visually compared. Theorem3.2 includes its continuation and both complete penalty formulas on15. Main text includes Section5 through23; appendix bodies excluded.', 'source_passages': 'Twenty-four original model, assumption and estimator entries plus ten auxiliary passages preserve source terminology, the complete five-step Algorithm1, source smoothness, centering, bounds, approximation witnesses and RSC conditions.', 'dependencies': 'Independent source-clause reconstruction verifies53 direct uses and74 related-theorem connections. Original depth-dependent classes serve2.7; revised constant-depth classes serve2.9. Sparse lower bound3.9 has no neural-network, penalty or RSC dependency. Standing section assumptions are identified as context rather than inserted into original theorem bodies.', 'source_issues': 'Fifteen notes preserve duplicated infimum variables, slash-form exponents, c/C and phi-hat/f-hat mismatches, sparse index ranges, inactive approximants, integer Holder conventions, fixed/random design tension, clipping distinctions, implicit sampling/optimization conventions, sample-split normalization and the unquantified log-factor rate. Original statements are not repaired.', 'names_and_highlights': 'All24 entries have literal source terms or numbered assumption headings, faithful source kinds and matching selectors. Every related theorem has a source-specific explanation and validated same-paper path. Definitions and assumptions remain distinct.', 'reproduction': 'All six content JSONs reproduce byte for byte in a fresh empty directory. Seven retained scripts support extraction, finalization, rebuilding and separate source review. Rebuilding alone does not perform semantic source review.', 'limits': 'The algorithm threshold constants are deferred to an excluded appendix proof and remain explicitly unresolved. The census does not certify proof validity, global optimizer existence, architecture equivalences, missing constants or sampling conventions.'}
    reviewed_pages=[1,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,23]
    crops=[]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=crops))
    evidence=[dict(path=f'evidence/page-{n:02}.png',page=n) for n in reviewed_pages]+crops+[dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=46,main_text_last_pdf_page=23,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent actual small-cap heading enumeration and visual comparison of all seven complete statements, including the continuation of3.2.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv2302.05851v1 marked12Feb2023,46pages, pinned bySHA256; not silently exchanged for the2024 published article.','Main text ends on23 before REFERENCES y650.386; evidence clipped645. Appendix A begins26 and is excluded. Algorithm1 threshold constants remain unresolved where deferred to the proof.','Source review preserves mathematical statements, dependencies and unresolved source notation; it does not certify proofs or solve implicit selection/domain conventions.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=46,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
