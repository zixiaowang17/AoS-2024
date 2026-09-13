"""Independently check frozen source-reviewed irregular-signal content and the three theorem closures."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': 'f54cc7f3587556c1d67391a893fd179b78fad33d528a7374d36ea2a419f4eb5f', 'source-passages.json': 'fc34666b8d216c234c73fc3dd0f279b089f016b61aecde8b7459c9e3d3e5c787', 'interface-extraction.json': '06dd87e442e97945aae2d74837bb1a31f890b81ebca527f43657b6d2c1175c9a', 'ambient-prerequisites.json': 'b9e31edb93a1ee012e810504a3c320e30f442c0a5480fd6761e52abbcb913f6d', 'unfinalized-census.json': 'e780722096c8cc9c55a143e3b0a4f9cc0fa0c5376c7b5587a7242fc26dca8374', 'ranked-interfaces.json': '36b7f032c2a8a6f9f11df81ec35d0be48320e73575f57fec88278c79361b3685'}

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
    1:[r'X_t=\mu_t+Z_t','stationary process with mean $0$',r'0<\sigma_\infty^2'],
    2:[r'\gamma(k)=\operatorname{Cov}(Z_{t+k},Z_t)',r'\sum_{k=-\infty}^{\infty}\gamma(k)<\infty'],
    3:[r'H_0:\mu_1=\cdots=\mu_n','not necessarily zero'],
    4:[r'\tau\in\{2,\ldots,n\}',r'\mu_1=\cdots=\mu_{\tau-1}',r'\mu_\tau,\ldots,\mu_n\ge\mu_1+d','vary arbitrarily'],
    5:['consistent estimator',r'\hat\sigma_\infty^2','defined in (2)'],
    6:[r'\min_{j=1,2,\ldots,n}',r'\sum_{i=1}^j(X_i-\bar X_n)',r'(\sqrt n\hat\sigma_\infty)',r'\bar X_n:=\frac1n\sum_{i=1}^nX_i'],
    7:[r'm:=\lfloor n/k\rfloor',r'k\to\infty',r'k/n\to0',r'\sum_{i=(j-1)k+1}^{jk}X_i'],
    8:[r'\operatorname*{argmin}_{i=1,\ldots,m}R_i',r'\hat\ell:=k\hat L','last observation'],
    9:[r'\hat\mu_0:=\frac1{\hat\ell}\sum_{i=1}^{\hat\ell}X_i'],
    10:[r'R_{s/k}:=\frac1k\sum_{i=s-k+1}^sX_i','extends the one for the non-overlapping blocks'],
    11:[r'\frac k{\hat\ell-k+1}',r'\sum_{s=k}^{\hat\ell}(R_{s/k}-\hat\mu_0)^2'],
    12:[r'z_\alpha',r'\alpha\in(0,1)','standard normal distribution'],
    13:[r'\hat D_j:=\sqrt k(R_j-\hat\mu_0)/\hat\sigma_\infty'],
    14:[r'1&\text{if }\hat D_j\ge z_{1-1/m}',r'0&\text{otherwise.}'],
    15:[r'\operatorname*{argmin}_{t=1,\ldots,m-1}',r'(\hat I_j-\mathbf1_{[t+1,m]}(j))^2',r'\sum_{j=1}^t\hat I_j+\sum_{j=t+1}^m(1-\hat I_j)'],
    16:[r'\hat\mu_1:=\frac1{k\hat\eta}\sum_{i=1}^{k\hat\eta}X_i'],
    17:[r'\hat d:=\min_{i=k(\hat\eta+1)+1,\ldots,n-k+1}',r'\sum_{j=i}^{i+k-1}(X_j-\hat\mu_1)'],
    18:[r'\operatorname*{argmin}_{j=2,\ldots,n}',r'\sum_{t=1}^{j-1}(X_t-\hat\mu_1-\rho\hat d)',r'\rho\in(0,1)'],
    19:[r'Z_t=G(\ldots,\varepsilon_{t-1},\varepsilon_t)','i. i. d.','measurable function'],
    20:['time $t=0$',r"\varepsilon'_0",r'\theta\ge1',r'\delta_{i,\theta}=(\mathbb E|Z_i-Z_{i,\{0\}}|^\theta)^{1/\theta}'],
    21:[r'\Theta_{n,\theta}=\sum_{i\ge n}\delta_{i,\theta}',r'n\ge0'],
    22:['any one of the following',r'\theta>2',r'\theta>4',r'A>2(1/\theta+1+\gamma_\theta)/3',r'\gamma_\theta=(\theta^2-4+(\theta-2)\sqrt{\theta^2+20\theta+4})/(8\theta)',r'2<\theta\le4',r'A>3/2'],
    23:[r'\Theta_{0,2}=\sum_{i\ge0}\delta_{i,2}<\infty'],
    24:[r'\eta:=\lfloor\tau/k\rfloor',r'\eta k+1\le\tau\le(\eta+1)k'],
    25:[r'a_n\ll b_n',r'a_n=o(b_n)',r'd=d_n',r'\tau=\tau_n','user-chosen block size'],
    26:[r'd_*:=\min_{i=k(\eta+1)+1,\ldots,n-k+1}',r'\sum_{j=i}^{i+k-1}(\mu_j-\mu_1)']}
    assert set(checks)==set(range(1,27))
    for n,vs in checks.items():
        for v in vs:assert v in s['D'+str(n)],(n,v)
    for n in [2,3,4,5,22]:assert m['D'+str(n)]['source_kind']=='condition'
    for n in [1,19,25]:assert m['D'+str(n)]['source_kind']=='source_passage'
    assert m['D22']['source_heading']=='Condition 3.1'
    assert m['D23']['source_kind']=='theorem_excerpt'
    assert r'\hat\eta' in s['D17'] and r'\hat\eta' not in s['D26']
    assert r'\hat d' in s['D18'] and r'\rho=1/2' not in s['D18']
    assert 'Condition 3.1' not in t['3.1'] and '(i)' in t['3.1'] and '(ii)' in t['3.1']
    assert r'O(1/k)+O_{\mathbb P}(\eta^{2/\min(4,\theta)-1})' in t['3.2']
    assert r'K>\rho' in t['3.3'] and r'd>Kd_*' in t['3.3']
    assert r'\hat\sigma_\infty^2=\sigma_\infty^2+o_{\mathbb P}(1)' in t['3.3']
    assert r'd_*^{-\theta/(\theta-1)}' in t['3.3']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert 'for fixed $J$' in a['A1'] and r'\max\{i:R_i\le R_m^{(J)}\}' in a['A1']
    assert 'any consistent estimate can be used' in a['A2']
    assert r'\mathbb B_1(u)=\mathbb B(u)-u\mathbb B(1)' in a['A3']
    assert r'-(-0.5\log\alpha)^{1/2}' in a['A4']
    assert r'\rho=1/2' in a['A5']
    assert r'\tau\asymp n' in a['A6'] and 'do not require' in a['A6']
    assert r'd_*\ge d' in a['A7'] and r'd>Kd_*' in a['A7']
    assert r'\tilde\tau' in a['A8'] and r'\rho d' in a['A8'] and r'\rho\hat d' not in a['A8']
    assert r'\delta_{n,\theta}=O(\rho^n)' in a['A9']
    assert ambient['unresolved_external_prerequisites']==[]
    assert set(ambient['statement_local_bindings'])=={'T3.1','T3.2','T3.3'}
    assert len(ambient['source_issues'])==10
    for name in ['true-block-index-boundary','generic-versus-specific-variance','overlapping-window-normalization','ties-and-empty-minima','finite-sample-denominators','dependence-parameters']:
        assert any(i['issue_id']==name for i in ambient['source_issues'])
def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2409.08863v1.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==39
    assert paper['main_text_last_pdf_page']==16 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==3
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent source-clause graph; no extractor or finalizer import.
    raw={1:[2],2:[],3:[1],4:[1],5:[2],6:[1,5],7:[1],8:[7],9:[1,8],10:[1,7],11:[2,8,9,10],12:[],13:[5,7,9],14:[7,12,13],15:[7,14],16:[1,7,15],17:[1,7,15,16],18:[1,16,17],19:[],20:[19],21:[20],22:[19,21],23:[21],24:[4,7],25:[4,7,24],26:[4,7,24]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'3.1':ids([3,4,6,23]),'3.2':ids([2,4,7,11,22,24,25]),'3.3':ids([2,4,5,7,18,22,25,26])}
    expected_reach={'3.1':ids([1,2,3,4,5,6,19,20,21,23]),'3.2':ids([1,2,4,7,8,9,10,11,19,20,21,22,24,25]),'3.3':ids([1,2,4,5,7,8,9,12,13,14,15,16,17,18,19,20,21,22,24,25,26])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not (expected_reach['3.1']&ids([7,8,9,10,11,12,13,14,15,16,17,18,22,24,25,26]))
    assert not (expected_reach['3.2']&ids([3,5,6,12,13,14,15,16,17,18,23,26]))
    assert not (expected_reach['3.3']&ids([3,6,10,11,23]))
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==9 and len(ambient['source_issues'])==10
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
        assert obj['evidence'] and all(1<=e['page']<=16 for e in obj['evidence'])
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
                assert all(1<=e['page']<=16 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=3,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=3,interfaces=26,source_members=26,direct_theorem_uses=19,related_theorem_connections=45,unranked_auxiliary_passages=9),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings={'inventory': 'Three original main-text Theorems 3.1–3.3 independently enumerated across pages 1–16. Both branches of 3.1, both variance error terms of 3.2, and the full continuation of 3.3 on page 9 were visually compared. Corollary 3.1, narrative citations and all appendix bodies are excluded.', 'source_passages': '26 original source entries preserve the one-sided signal model and hypotheses, positive finite long-run variance, minimum CUSUM test, block means and selection, preliminary means and overlapping estimator, normal quantiles and decisions, binary step fit and refined localization, causal noise and functional dependence, complete Condition 3.1, true block index and averaged gap. Nine auxiliary passages preserve original optional choices and limiting interpretations separately.', 'dependencies': 'Independent source-clause reconstruction gives 19 direct uses and 45 related-theorem connections. Theorem 3.1 does not inherit the stronger locating condition or block-estimator rates. Theorem 3.2 studies the specific overlapping variance estimator. Theorem 3.3 permits any consistent variance estimate and uses the full estimated-gap localization procedure, including its preliminary mean but not the optional variance formula.', 'source_issues': 'Ten notes preserve the registered manuscript version, first-change indexing, the contradictory exact-block-boundary convention, arbitrary versus specific variance estimation, overlapping-window normalization, ties and empty minima, finite-sample division problems, distinct dependence parameters and rates, optional defaults and proof/application scope.', 'names_and_highlights': 'All 26 entries preserve literal natural-language source terms and original passage kinds/headings. All selectors match the source entry or a related theorem, and all 45 connections have explicit source correspondence along valid same-paper paths. True and estimated block indices, pointwise gap bounds and averaged gaps remain distinct.', 'reproduction': 'All six content JSONs reproduce byte for byte in a fresh empty directory. Seven retained scripts support separate inventory review, extraction, finalization, full-source validation and reproduction. Rebuilding alone is not a new semantic PDF review.', 'limits': 'The census records original statements and source-definition limitations without certifying proofs or silently choosing missing tie, empty-window, denominator or exact-block-boundary conventions. Application interpretations are not additional mathematical conclusions.'}
    reviewed_pages=[1,3,4,5,6,7,8,9,16]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[]))
    evidence=[dict(path=f'evidence/page-{n:02}.png',page=n) for n in reviewed_pages]+[dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=39,main_text_last_pdf_page=16,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent uppercase small-cap heading enumeration across main-text pages 1–16 and visual comparison of all three complete statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2409.08863v1, stamped 13 September 2024, 39 pages; source identity pinned and not silently replaced.','Main text ends after Acknowledgments on page 16; supplementary availability/references occupy 17–18, and all appendix bodies from page 19 onward are excluded.','Review concerns extraction fidelity and dependency scope, not proof correctness or unprovided finite-sample conventions.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=39,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
