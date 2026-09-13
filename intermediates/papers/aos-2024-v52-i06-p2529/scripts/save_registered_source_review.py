"""Verify frozen source-reviewed content and independently reconstruct dependency reach."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': 'a26bc459b9f4cfe4b8df1403fb828fbc0ae85d793c88074e419b02fd99e6a056', 'source-passages.json': '0852cd371421db701fe6843e1fa2fd00c15d4c87a617e794a61d10cab576a7c8', 'interface-extraction.json': '646fb6d331e013cd54b7b7103ecf5a10221ce5fffd3f785ec5f7f077db467421', 'ambient-prerequisites.json': '78b58f2c411191b54704fd4c2778f0b8cbb6f3bd4087918f7adc2cd2a260841b', 'unfinalized-census.json': 'c0aa3b71ebc8bc66b4b1899eb067c7a9a26ad5c389d264e4898c731b5dd6c5ba', 'ranked-interfaces.json': 'd5cea328ddc4a5cf26f7b8f5f394f82fbf715a7a0303f7bb5454923bf0127802'}
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
    assert registered['version']=='2010.03832v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2010.03832'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==39
    assert paper['main_text_last_pdf_page']==25 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==3
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent clause-by-clause reconstruction; no importing the finalizer's graph.
    raw={1:[],2:[1],3:[1],4:[1],5:[],6:[],7:[],8:[1,3,4,6],9:[3,6],10:[],11:[5,10],12:[7,11],13:[3,5,10],14:[1,2,3,4,5,10,11,13],16:[],17:[5,6,7,16,19],19:[6,16],20:[1,2],22:[3,4,5,10],23:[5,7,8,9,10,11,12,13],24:[3,4,8,27],26:[5,7,22,23,24],27:[1]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'5':ids([1,2,3,4,5,10,11]),'8':ids([2,3,4,8,19,20,27]),'10':ids([5,7,10,13,14,17,20,22,23,24,26,27])}
    expected_reach={'5':ids([1,2,3,4,5,10,11]),'8':ids([1,2,3,4,6,8,16,19,20,27]),'10':ids([1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,19,20,22,23,24,26,27])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([14,19,20,27]) & expected_reach['5']
    assert not ids([5,10,11,12,13,14,17,22,23,24,26]) & expected_reach['8']
    assert 'D17' not in local['D19'] and 'D19' in local['D17']
    assert 'D14' not in local['D22'] and 'D14' not in local['D23']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==8 and len(ambient['source_issues'])==12
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
        assert obj['evidence'] and all(1<=e['page']<=25 for e in obj['evidence'])
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
                assert all(1<=e['page']<=25 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=3,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=3,interfaces=23,source_members=23,direct_theorem_uses=26,related_theorem_connections=40,unranked_auxiliary_passages=8),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(inventory='Exactly three complete main-text Theorems5,8,10, independently enumerated by bold headings and visually compared. Theorem5 spans7–8;8 is on10 and10 is on11. Corollary6 is not added to the inventory. Main text ends before references on page25; appendix bodies are excluded.',source_passages='Twenty-three source entries and eight auxiliary passages preserve index1 regular variation, non-standard standardization, marginal normalization, spectral/Pareto laws, extremal coefficients, tilted subset angular law, simplex/masks, perturbations, estimators, second-order and angular bias assumptions, Gaussian limit definitions and their required joint covariances.',dependencies='Independent reconstruction verifies26 direct uses and40 related connections. Theorem5 does not inherit bias27,second-order30,Hill estimation or unknown-margin assumptions. Theorem8 does not inherit Corollary6 angular bias or the random angular estimator. Theorem10 imports the complete Corollary6 and Theorem8 assumptions. Hill denominators are resolved independently from the moment numerator, avoiding a circular edge.',scope='The Gaussian objects are jointly coupled. Main-text Remark7.1 supplies the complete covariance specialization needed by Theorem10; Remark7.2,Eq34 and the i-in-J sentence after35 supply its required cross covariances. G^0 is the zeroth-moment restriction ofG. No general appendix covariance or proof is read.',source_issues='Twelve notes preserve source ambiguities including the positive-orthant/zero-support conflict, X* versusTheta in condition27, undefined starred weight domain, unindexedalpha inTheorem8, masked-simplex/derivative extensions, zero denominators and ties, and the vector/scalar notation in general covariance35. Source discrepancies remain explicit rather than silently repaired.',names_and_highlights='Every entry has original source terminology, a literal meaningful highlight and source evidence. All40 related-theorem connections have checked local paths and symbol-specific explanations. Assumptions, source passages and theorem excerpts retain their distinct source kinds.',reproduction='All six contentJSON artifacts reproduce byte for byte in an empty directory. Seven retained scripts cover extraction, inventory review, context, finalization, rebuilding and frozen full-source validation. Rebuilding is not represented as a new semantic source review.')
    reviewed_pages=[1,3,4,5,6,7,8,9,10,11,25]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[]))
    evidence=[dict(path='evidence/page-'+str(n).zfill(2)+'.jpg',page=n) for n in reviewed_pages]+[dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=39,main_text_last_pdf_page=25,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold heading enumeration and visual comparison of the three complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2010.03832v2, marked3Jul2024 and datedJuly4,2024;39PDFpages, pinned bySHA256.','Main text ends onPDFpage25, clipped at y520 before References y527.295. Appendix bodies are excluded.','Validation checks the census against this source, not the correctness of its proofs or unresolved notation. General covariance48 is not imported; the needed main-text specialization is preserved.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=39,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={1:[r'a^*(u)\mathbb P(u^{-1}X^*\in\cdot)\xrightarrow{v}\mu^*(\cdot)','homogeneous of order $-1$'],2:[r'\mu^*(\{x\in E:x_i>1\})',r'\mathbb P(X_i^*>u)^{-1}'],3:['independently from $Y$',r'\mathbb P(\Theta\in S^+_{d-1})=1',r'\|\cdot\|=\|\cdot\|_\infty'],4:[r'\tau=\mu^*(\{x\in E:\|x\|>1\})'],5:[r'\partial B_1(0)\cap[0,\infty)^d','positive coefficients'],6:[r'\ell_I(x)=\bigvee_{i\in I}x_i'],7:['0 otherwise',r'v_I^\top X^*=\sum_{i\in I}v_iX_i^*'],8:[r'\tau_I=\mathbb E[\ell_I(\Theta)]\cdot\tau\in[1,|I|]'],9:[r'\frac1{\mathbb E[\ell_I(\Theta)]}',r'\mathbf1\{\theta/\ell_I(\theta)\in A\}\ell_I(\theta)\mathbb P(\Theta\in d\theta)'],10:[r'x\in(0,\infty)^d:x_i=0',r'(1+\delta)^{-1}\le x_i\le1+\delta',r"A'_\delta=\bigcup"],11:[r'\frac1n\sum_{l=1}^n',r'(s\circ X_l^*/u)^{1/\beta}',r'\mathbf1\{\|s\circ X_l^*\|>u\}',r'p\in\mathbb N_0'],12:[r'0^0=1',r'\widehat P_{n,u}(s)=\widehat M_{n,u}(v,s,\beta,0)'],13:[r'\frac1{\mathbb E[\|s\circ\Theta\|]}',r'(Ys\circ\Theta)^{1/\beta}',r'\mathbf1\{Y\|s\circ\Theta\|>1\}'],14:['assumptions of Thm. 5',r'K\cup\{0\}',r'\tau\mathbb E[\|s\circ X^*\|]c',r'\partial B_1^*(0)'],16:['$k$th upper order statistic',r'X_{k:n,i}>0'],17:[r'(X_l/X_{k:n})^{\widehat\alpha}',r'\widetilde P_{n,k,I}',r'n^{-1}\sum_{l=1}^n\mathbf1\{\ell_I(X_l/X_{k:n})>1\}'],19:[r'\widehat\alpha_{k,n,i}',r'\frac1{\widehat\alpha_{n,k,i}}',r'\widetilde P_{n,k,\{i\}}'],20:['auxiliary positive function',r'A_i^*(t)\to0',r'A_i^*(a^*(x))','not identically 0'],22:[r'\tau\mathbb E',r'(Ys\circ\Theta)^{1/\beta}',r'(Yt\circ\Theta)^{1/\gamma}',r'Y(\|s\circ\Theta\|\wedge\|t\circ\Theta\|)>1'],23:[r'\frac{\widehat M_{n,u_n}(v,s,\beta,p)}{\widehat P_{n,u_n}(s)}-c',r'\frac1{\tau_I}\operatorname{Cov}((v^\top\Theta_I^I)^{p_1},(w^\top\Theta_I^I)^{p_2})'],24:[r'\frac\tau{\alpha_i\alpha_j}\mathbb E[\Theta_i\wedge\Theta_j]',r'\frac{2-\tau_{ij}}{\alpha_i\alpha_j}'],26:['joint convergence',r'\frac\tau{\alpha_i}',r'-\log\left(1\wedge\frac{\|\Theta_J\|}{\Theta_i}\right)',r'(\Theta_i\wedge\|\Theta_J\|)',r'=0$ if $i\in J$'],27:[r'\alpha_1,\ldots,\alpha_d>0',r'r_1^{-1}X_1^{\alpha_1}',r'r_d^{-1}X_d^{\alpha_d}']}
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert set(checks)=={int(lid[1:]) for lid in m}
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in inv['claims']}
    assert s['D22'] in t['5'] and s['D24'] in t['8']
    assert m['D14']['source_kind']=='assumption' and m['D20']['source_kind']=='assumption'
    assert r'G^0(s)=G(\cdot,s,\cdot,0)' in m['D22']['naming_context'][0]['text']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert a['A1'] in t['5'] and a['A2'] in t['8'] and a['A8'] in t['10']
    assert a['A3'].split('\n')[1] in s['D17']
    assert r'\widehat\alpha' not in a['A3']
    for v in [r'\operatorname{Cov}(G(v,s,\mathbf1,p_1),\widetilde G(w,t,\mathbf1,p_2))',r'(\mathbb E[\|t\circ\Theta\|])^2','jointly Gaussian']:assert v in a['A4'],v
    assert r'\tau' not in a['A4']
    assert r'\alpha/\widehat\alpha' in a['A5'] and r'\tau r^{-1}\mathbb P(\Theta\in B)' in a['A6']
    for obj in aux.values():assert set(obj['depends_on'])<=set(m)
    assert set(ambient['statement_local_bindings'])=={'T5','T8','T10'}
    assert {x['issue_id'] for x in ambient['source_issues']}=={'registered-version-and-boundary','regular-variation-domain-and-tail-scale','standardization-alpha-indices','positive-orthant-versus-masked-support','corollary-six-centering-and-domain','expectation-centering-and-assumption-imports','masked-weights-and-derivative-extension','zero-divisions-and-strict-exceedances','tilted-spectral-law-and-pair-coefficients','joint-gaussian-coupling-and-appendix-covariance','general-cross-covariance-notation','sequence-and-index-notation'}
    refs=ambient['source_claim_references'];assert sum(x['reference_kind']=='assumption_reference' for x in refs)==3 and sum(x['reference_kind']=='proof_only' for x in refs)==3
if __name__=='__main__':main()
