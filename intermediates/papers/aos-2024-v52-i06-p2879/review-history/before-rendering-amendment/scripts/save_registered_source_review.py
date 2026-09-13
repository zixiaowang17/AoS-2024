"""Independently check frozen source-reviewed ridge/resolvent content and the six theorem closures."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': 'd802b3e53155d7ac49f8547fbdf571819d4a614fb213373ed6b7e5b184df8796', 'source-passages.json': '076c2663435a56365c31b94a0fe80d47359f58dada66739846e4fec3ef76315a', 'interface-extraction.json': '671ac17f76b9097d6e32641d555db39cb6b5eeb270da90119673b9a9d786f979', 'ambient-prerequisites.json': 'd26e23b3407c5e264d5f34a0f8420ed21c0e55401b35c2e6b69ea25f06b24b9e', 'unfinalized-census.json': 'a2cf5dd51f2b2c6ee6850595678cb5b6765c443ed3e04815ebb3e3c99f2d366b', 'ranked-interfaces.json': '3ec1e8c62dedb1246331a020f17680a98e4868280a1ce74ac330cba3a4203efa'}

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
    1:['real, separable Hilbert space',r'\mathcal H\to\mathcal H','associated operator norm'],
    2:['trace-class',r'\|\boldsymbol\Sigma\|=1',r'1=\sigma_1\ge\sigma_2'],
    3:[r'\|\boldsymbol\Sigma^{-1/2}\boldsymbol\beta\|<\infty',r'\boldsymbol\beta=\boldsymbol\Sigma^{1/2}\boldsymbol\theta'],
    4:[r'd_\Sigma:=d_\Sigma(n)\ge n',r'\sum_{l=k}^d\sigma_l\le d_\Sigma\sigma_k',r'1\le k\le\min\{n,d\}'],
    5:['independent but not necessarily identically distributed',r'\operatorname{Var}(z_{ij})=1',r'\sup_{p\ge1}p^{-\frac12}'],
    6:['dependent coordinates','Lipschitz convex',r'\mathbb P(|\varphi(\boldsymbol z_i)-\mathbb E\varphi(\boldsymbol z_i)|\ge t)\le2\exp(-t^2/C_x^2)'],
    7:['one of the following condition holds',r'\boldsymbol x_i=\boldsymbol\Sigma^{1/2}\boldsymbol z_i','Independent sub-Gaussian coordinates','Convex concentration'],
    8:[r'\boldsymbol x_1^\top',r'\boldsymbol x_n^\top',r'\mathbb R^{n\times d}'],
    9:['are independent','i.i.d. samples','mean zero',r'\operatorname{Var}(\varepsilon_i)=\tau^2'],
    10:[r'\frac1n\|\boldsymbol y-\boldsymbol X\boldsymbol b\|^2',r'\boldsymbol X^\top\boldsymbol X+n\lambda\boldsymbol I',r'\tag{1}',r'\tag{2}'],
    11:[r'\lambda\to0+','minimum norm interpolator'],
    12:[r'\operatorname{Cov}(\hat{\boldsymbol\beta}\mid\boldsymbol X)',r'\frac{\tau^2}n',r'\hat{\boldsymbol\Sigma}(\hat{\boldsymbol\Sigma}+\lambda\boldsymbol I)^{-2}'],
    13:[r'\|\mathbb E_{\boldsymbol y}[\hat{\boldsymbol\beta}\mid\boldsymbol X]-\boldsymbol\beta\|_{\boldsymbol\Sigma}^2',r'(\hat{\boldsymbol\Sigma}+\lambda\boldsymbol I)^{-1}\boldsymbol\Sigma(\hat{\boldsymbol\Sigma}+\lambda\boldsymbol I)^{-1}'],
    14:['minimum nonzero eigenvalue',r'\boldsymbol X^\top\boldsymbol X/n'],
    15:['unique non-negative solution',r'n\cdot\left(1-\frac\lambda{\lambda_\star}\right)'],
    16:[r'V_n(\lambda)',r'n-\operatorname{Tr}',r'\tau^2'],
    17:[r'B_n(\lambda)',r'\lambda_\star^2',r'1-n^{-1}\operatorname{Tr}'],
    18:['depending only on the value','for all $x$',r'\Omega_\alpha(g(x))'],
    19:[r'\chi_n(\lambda)',r'\sigma_{\lfloor\eta n\rfloor}d_\Sigma\log^2(d_\Sigma)',r'{n\lambda}'],
    20:[r'\kappa:=\min\left(\frac\lambda{\lambda_\star};1-\frac\lambda{\lambda_\star}\right)>0'],
    21:[r'\mathscr R_0(\zeta,\mu;\boldsymbol Q)',r'\boldsymbol\Sigma^{1/2}\boldsymbol Q\boldsymbol\Sigma^{1/2}',r'(\zeta\boldsymbol I+\mu\boldsymbol\Sigma)^{-1}'],
    22:[r'\rho(\lambda)',r'\boldsymbol\theta\boldsymbol\theta^\top/\|\boldsymbol\theta\|^2',r'\in(0,1]'],
    23:[r"\chi'_n(\kappa)",r'\kappa n\lambda_\star(0)','introduced in the theorem statement'],
    24:[r'\rho(0)',r'\lambda\downarrow0',r'\boldsymbol\theta\boldsymbol\theta^\top/\|\boldsymbol\theta\|^2'],
    25:[r'\boldsymbol\beta_{\le k}:=\sum_{i\le k}',r'\boldsymbol\beta_{>k}:=\boldsymbol\beta-\boldsymbol\beta_{\le k}'],
    26:[r'\mathbb P(A^c\text{ and }E)\le\Delta',r'\mathbb P(A)\ge1-\Delta-\mathbb P(E^c)'],
    27:[r'\delta\in(0,\infty)',r'\lim_{i\to\infty}\frac{\sigma_{\lfloor\delta i\rfloor}}{\sigma_i}=\psi(\delta)','positive and finite'],
    28:[r'\lfloor nx\rfloor','polynomial-decay',r'0<\theta\le1',r'x^\alpha(1+c_\star x^\alpha)^{-1}'],
    29:[r'\lfloor(n/\log n)x\rfloor','rapid-decay',r'x(1+c_\star x)^{-1}'],
    30:[r'\mathscr R_k(\zeta,\mu;\boldsymbol Q)',r'\boldsymbol X_k^\top\boldsymbol X_k',r'\boldsymbol X_0^\top\boldsymbol X_0:=0','bounded spectral norm'],
    31:['unique solution on of',r'$(\mu,\infty)$',r'\mu_\star=\mu+\frac n{1+\mathscr R_0(\zeta,\mu_\star;\boldsymbol I)}']}
    assert set(checks)==set(range(1,32))
    for n,vs in checks.items():
        for v in vs:assert v in s['D'+str(n)],(n,v)
    assert m['D7']['source_kind']=='assumption' and m['D7']['source_heading']=='Assumption 1'
    for n in [4,5,6]:assert m['D'+str(n)]['source_kind']=='assumption'
    for n in [14,28,29]:assert m['D'+str(n)]['source_kind']=='theorem_excerpt'
    assert m['D3']['source_kind']=='condition'
    assert 'identically distributed' in s['D5'] and 'not necessarily' in s['D5']
    assert r'\lambda\to0+' in s['D11'] and r'\kappa:=\min' not in s['D23']
    assert r'\mathscr V_X' in s['D12'] and r'V_n' in s['D16']
    assert r'\mathscr B_X' in s['D13'] and r'B_n' in s['D17']
    assert r'\nu n^{-\alpha}' in t['5'] and r'\nu\sigma_n' not in t['5']
    assert r'\operatorname{rank}(\boldsymbol X)=d' in t['4']
    assert r'\boldsymbol\theta_{\le n}' in t['3'] and r'\boldsymbol\beta_{>n}' in t['3']
    assert r'\mathsf R_0' in t['6'] and r'\mathscr R_0' in t['6']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert r'C_\Sigma:=1-\frac1n' in a['A3'] and r'\in(0,1)' in a['A3']
    assert 'throughout the proof' in a['A6'] and r'\|\boldsymbol\theta\|=1' in a['A6']
    assert 'i.i.d. samples' in a['A8'] and 'top $k$-eigenvectors' in a['A9']
    assert ambient['unresolved_external_prerequisites']==[]
    assert len(ambient['source_issues'])==13
    for name in ['theorem5-spectral-scale','zero-limit-and-rank','signal-domain-and-zero-signal','event-probability-and-bias-error','resolvent-notation-and-scope']:assert any(i['issue_id']==name for i in ambient['source_issues'])
def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2210.08571v3.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==86
    assert paper['main_text_last_pdf_page']==34 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==6
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent source-clause graph; no extractor or finalizer import.
    raw={1:[],2:[1],3:[2],4:[2],5:[1],6:[1],7:[2,3,4,5,6],8:[1],9:[1,2],10:[8,9],11:[10],12:[2,9,10,14],13:[2,10,14],14:[8],15:[2],16:[2,9,15],17:[2,9,15],18:[],19:[2,4],20:[15],21:[2],22:[3,15,21],23:[2,4,15],24:[3,15,21],25:[2],26:[],27:[2],28:[18,25],29:[18,25],30:[2,8,21],31:[21]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'1':ids([7,12,13,15,16,17,18,19,20,22]),'2':ids([3,4,7,12,13,15,16,17,18]),'3':ids([7,11,12,13,14,15,16,17,18,23,24,25,26]),'4':ids([7,8,11,12,13,16,17,18]),'5':ids([7,12,13,15,18,25,27,28,29]),'6':ids([7,18,21,30,31])}
    expected_reach={'1':ids([1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,22]),'2':ids([1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18]),'3':ids([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,21,23,24,25,26]),'4':ids(range(1,19)),'5':ids([1,2,3,4,5,6,7,8,9,10,12,13,14,15,18,25,27,28,29]),'6':ids([1,2,3,4,5,6,7,8,18,21,30,31])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not (expected_reach['6']&ids([9,10,11,12,13,14,15,16,17,19,20,22,23,24,25,26,27,28,29]))
    assert not (expected_reach['5']&ids([16,17,19,20,22,23,24,30,31]))
    assert 'D20' not in expected_reach['3'] and 'D23' in expected_reach['3']
    assert 'D28' in direct['5'] and 'D29' in direct['5']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==9 and len(ambient['source_issues'])==13
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
        assert obj['evidence'] and all(1<=e['page']<=34 for e in obj['evidence'])
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
                assert all(1<=e['page']<=34 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=6,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=6,interfaces=31,source_members=31,direct_theorem_uses=54,related_theorem_connections=110,unranked_auxiliary_passages=9),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings={
    'inventory':'Six original main-text Theorems1–6 independently enumerated across pages1–34. Full Theorem3 and4 continuations retained; Theorem6 in the main-text proof section included. All variance/bias subparts, event qualifications, rank statements, scalar parameter definitions and spectral formulas were visually compared. Appendix bodies excluded.',
    'source_passages':'31 original source entries preserve Hilbert/covariance setting, signal domain, effective-rank envelope, alternative concentration conditions, full Assumption1, feature design and linear model, ridge/ridgeless estimators, conditional and effective bias/variance, parameter ratios, spectral projections, event-probability convention, regular variation and branch-specific coefficient predicates, and population/sample resolvents with their implicit root. Nine auxiliary source passages preserve ambient definitions and proof context separately.',
    'dependencies':'Independent source-clause reconstruction gives54 direct uses and110 related-theorem connections. Theorem6 has no response-noise/ridge-risk dependency; Theorem5 does not acquire deterministic-equivalent formulas as additional statement requirements. Theorem3 uses the ridgeless free-kappa replacement and intersection-probability convention, not the positive-ridge kappa formula.',
    'source_issues':'Thirteen notes preserve the2025 registered revision, zero-limit/rank and inverse-domain caveats, infinite whitened coordinates, alternative concentration assumptions, effective-rank/index conventions, additive bias errors, reused parameter symbols, theorem constant/quantifier issues, spectral scaling limitations and proof-versus-statement scope.',
    'names_and_highlights':'All31 source entries carry literal natural-language source terms, faithful source kinds/headings and matching meaningful selectors. All110 connections have valid same-paper dependency paths and specific source correspondence. Script sample quantities, plain deterministic equivalents and the sans-serif theorem-local R0 shorthand remain distinct.',
    'reproduction':'All six content JSONs reproduce byte for byte in a fresh empty directory. Seven retained scripts support separate inventory review, source extraction, finalization, full-source validation and reproduction. Rebuilding alone does not perform a fresh semantic PDF review.',
    'limits':'Source review preserves original statements and unresolved conventions rather than certifying proofs. In particular, Theorem5 regularization arguments may omit the permitted slowly varying scale, and some zero-root/index/domain conventions are implicit. No corrections or extra premises have been silently substituted.'}
    reviewed_pages=[1,3,4,5,6,7,9,10,11,12,13,14,16,17,23,25]
    crop=dict(path='evidence/page-34-main-text.png',page=34,y_end=615)
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[crop]))
    evidence=[dict(path=f'evidence/page-{n:02}.png',page=n) for n in reviewed_pages]+[crop,dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=86,main_text_last_pdf_page=34,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-font enumeration across main-text pages1–34 and visual comparison of all six complete statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv2210.08571v3 stamped19June2025, title date23June2025,86pages; source identity pinned and not silently replaced by the published2024 PDF.','Main text ends beforeReferences on34; appendices begin38 and all appendix bodies are excluded.','Review concerns extraction fidelity and dependency scope, not proof correctness or unprovided spectral-scale, inverse-domain and zero-limit conventions.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=86,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
