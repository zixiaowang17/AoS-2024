"""Check frozen source-reviewed content and independently reconstruct both theorem closures."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': 'fa00dae432a2036c3275d4402bb0acb733539a6e1b9971510b08ac7d9a64f6bf', 'source-passages.json': '7440bbcd8db648644cff2f3a7349ace774e5e3e1ab2a15c598012e7aed5f1ef9', 'interface-extraction.json': '67a71a7223a27564677a6f82007654c18eb1b27e9fcec1ddf8bdac8ebb1be945', 'ambient-prerequisites.json': '403024611567df4a9edd9be77faaf9a5dde61c127ea47344f60eaafe1f0acb7c', 'unfinalized-census.json': 'b4b05657a4362db717721dc1a98d4b15d92524409a3f2215d7b0dda9ba4b71cf', 'ranked-interfaces.json': 'c6c188fb3280cba16621eea32f3a62d4b6025211025e78a582f8ed1df177e1d9'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
    1:['observe a random operator',r'y=T_\xi(\theta^\star)+w','unobserved vector $w$','observed operator'],
    2:['finite-dimensional setting',r'\mathbb R^{n\times d}','positive but finite integers',r'(\Xi,\mathcal E)','linear functionals','measurable'],
    3:['conditionally on',r'\nu(\cdot\mid\xi)','Borel regular conditional probability'],
    4:[r'$\mathbb P$-almost every',r'\int w\,\nu(dw\mid\xi)=0'],
    5:[r'$\mathbb P$-almost every',r'\int(u^Tw)^2\,\nu(dw\mid\xi)\le u^T\Sigma_wu','for any fixed'],
    6:[r'\mathcal P(\Sigma_w)','these two conditions'],
    7:[r'\mathbb P\times\nu',r'$\xi\sim\mathbb P$',r'$w\mid\xi\sim\nu(\cdot\mid\xi)$','observation model (1)'],
    8:['two symmetric positive definite matrices',r'\|\theta\|_{K_e}^2:=\langle\theta,K_e\theta\rangle',r'\|\theta\|_{K_c^{-1}}^2:=\langle\theta,K_c^{-1}\theta\rangle'],
    9:[r'\|\theta\|_{K_c^{-1}}\le\varrho','with radius $R$'],
    10:['all measurable functions',r'\hat\theta(T_\xi,y)','observed pair'],
    11:[r'\inf_{\hat\theta}\sup_{\substack{\theta^\star\in\Theta(\varrho,K_c)\\\nu\in\mathcal P(\Sigma_w)}}',r'\mathbb E_{(\xi,w)\sim\mathbb P\times\nu}',r'\|\hat\theta-\theta^\star\|_{K_e}^2'],
    12:[r'\sup_\Omega\left\{\mathbb E\operatorname{Tr}',r'K_e^{1/2}(\Omega^{-1}+T_\xi^T\Sigma_w^{-1}T_\xi)^{-1}K_e^{1/2}',r'\Omega\succ0',r'\operatorname{Tr}(K_c^{-1/2}\Omega K_c^{-1/2})\le\varrho^2']}
    assert set(checks)==set(range(1,13))
    for n,vs in checks.items():
        for v in vs:assert v in s['D'+str(n)],(n,v)
    assert m['D2']['source_kind']=='assumption'
    for n,label in [(4,'Assumption (N1)'),(5,'Assumption (N2)')]:assert m['D'+str(n)]['source_kind']=='assumption' and m['D'+str(n)]['source_heading']==label
    assert 'Gaussian' not in s['D3'] and r'\Sigma_w\succ0' not in s['D5']
    assert r'\Omega\succeq0' not in s['D12'] and r'\|\theta\|_{K_c^{-1}}^2\le' not in s['D9']
    assert r'\tfrac\varrho2' in t['2'] and r'\frac14' in t['2']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert 'infinite-dimensional sequence space' in a['A1']
    assert 'if the supremum' in a['A2'] and r'\Omega_\star^{-1}' in a['A2']
    assert 'If the supremum in (5) is not attained' in a['A3']
    assert r'\Omega^{-1}+\mathbb E T_\xi^T\Sigma_w^{-1}T_\xi' in a['A4']
    assert r'C(T_\xi)T_\xi^T\Sigma_w^{-1}y' in a['A5']
    assert 'positive definite matrices' in a['A6'] and r'\Omega\succeq0' in a['A6']
    assert r'\mathfrak M^G' in a['A7'] and r'\mathbb P\times N(0,\Sigma_w)' in a['A7']
    assert ambient['unresolved_external_prerequisites']==[]
    assert any(i['issue_id']=='matrix-invertibility' for i in ambient['source_issues'])
    assert any(i['issue_id']=='radius-and-open-feasible-set' for i in ambient['source_issues'])
def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2303.12613v1.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==53
    assert paper['main_text_last_pdf_page']==32 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==2
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent reconstruction from inspected source clauses; no finalizer import.
    raw={1:[],2:[],3:[],4:[2,3],5:[2,3],6:[4,5],7:[1,2,3],8:[],9:[8],10:[1],11:[6,7,8,9,10],12:[2,8]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'1':ids([11,12]),'2':ids([11,12])}
    expected_reach={'1':ids(range(1,13)),'2':ids(range(1,13))}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert direct['1']==direct['2']==ids([11,12])
    assert local['D12']==ids([2,8]) and local['D6']==ids([4,5])
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==7 and len(ambient['source_issues'])==9
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
        assert obj['evidence'] and all(1<=e['page']<=32 for e in obj['evidence'])
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
                assert all(1<=e['page']<=32 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=2,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=2,interfaces=12,source_members=12,direct_theorem_uses=4,related_theorem_connections=24,unranked_auxiliary_passages=7),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings={
    'inventory':'Two original main-text Theorems1(General minimax upper bound) and2(Lower bound) independently enumerated across32 main-text pages and visually compared on8. Preserve the full lower-bound chain, including the halved radius. Appendix bodies beginning33 are excluded.',
    'source_passages':'Twelve original entries retain the observed linear model, finite measurable operator law, conditional-noise kernel and separateN1/N2 conditions, admissible noise class, kernel-composed joint law, SPD norms, parameter ellipse, all-measurable estimator class, minimax risk3 and trace functional5. Seven auxiliary passages preserve proof and application context separately.',
    'dependencies':'Independent source-clause graph gives4 direct uses and24 related-theorem connections. Both Theorems directly useM andPhi; their original definitions resolve all12 source entries. Gaussian noise, priors, conditional-linear/ridge procedures, IID covariates and infinite-dimensional applications are not added as general hypotheses.',
    'source_issues':'Nine source notes preserve conditional versus marginal noise bounds, operator versus latent-index observations, covariance invertibility, radiusR/varrho mismatch and zero-radius endpoint, strictOmega optimization/nonattainment, matrix geometry and expectation order, finite-dimensional scope and proof-only restrictions.',
    'names_and_highlights':'All12 entries carry literal natural-language source keywords, faithful kinds/headings and meaningful matching selectors. All24 related-theorem connections have valid same-paper paths and source-specific explanations. Conditional assumptions remain AssumptionsN1/N2, not invented definitions.',
    'reproduction':'All six content JSONs reproduce byte for byte in a fresh empty directory. Seven retained scripts support extraction and separate inventory/full-source validation. Rebuilds preserve existing source-review records and do not themselves reread the PDF semantically.',
    'limits':'Source review preserves claims and unresolved conventions rather than certifying proofs. In particular, functional5 uses an ordinary inverse ofSigma_w while the conditional-noise assumptions do not explicitly demand nonsingularity. No pseudoinverse or zero-radius convention is silently supplied.'}
    reviewed_pages=[1,3,4,8,9,10,21,22,23,32]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[dict(path='evidence/norms-crop.png',page=4)]))
    evidence=[dict(path=f'evidence/page-{n:02}.png',page=n) for n in reviewed_pages]+[dict(path='evidence/norms-crop.png',page=4),dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=53,main_text_last_pdf_page=32,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-font enumeration over32 main-text pages and visual comparison of both complete original statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv2303.12613v1 stamped22Mar2023,53pages,pinned bySHA256; not silently replaced by published text.','Main text ends32 after simulations and acknowledgements. Appendix A starts33; no appendix body inspected.','Source review does not certify proof correctness or resolve implicit covariance-inverse, positive-radius and attainment conventions.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=53,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
