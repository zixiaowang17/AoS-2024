"""Validate the saved extraction against independently reviewed source scopes."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': '5673ccb3c00dc570ccfd12c349521395ac316099291a91794cbd27b2f415da22', 'source-passages.json': 'afe7a608f663eeb891eaf80d9bea3477f869cba9072135f75fff7c9819cfe064', 'interface-extraction.json': '556df1ab6b20ff6b26e5fa3da2f6ce69f5a27a7026eb1629fa2595c7de1522ce', 'ambient-prerequisites.json': 'cf97949950513603b6244b81b36793ef7b7b10ad53a35e2dd201befa649fd6c9', 'unfinalized-census.json': 'b1910b3a44e1b3f83c93fd84808774f22c5a8d9dd9cf6ec5985a3b08c2b1a6b5', 'ranked-interfaces.json': '39a1f98645b271104441efa36b67906ce9bb45857b3bc3a643e2511b05b803a1'}
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
    assert registered['version']=='24-AOS2433-1.pdf' and registered['source_url']==URL
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==24
    assert paper['main_text_last_pdf_page']==23 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==4
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent reconstruction from source definitions, not imported from builder modules.
    raw={1:[],2:[1],3:[1],4:[3],5:[2],6:[4,5],7:[],8:[1],9:[4],10:[4,7],11:[3,8],12:[4,10],13:[7,11,12],14:[2,4,6],15:[2,14],16:[3],17:[14,16],18:[1,7],19:[3]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'2.1':ids([4,6,7,8]),'2.2':ids([4,6,7,8,9,10,11,12,13]),'2.3':ids([1,4,6,7,8,9,15,16,17,19]),'2.4':ids([1,4,6,7,8,9,15,16,18,19])}
    expected_reach={'2.1':ids([1,2,3,4,5,6,7,8]),'2.2':ids([1,2,3,4,5,6,7,8,9,10,11,12,13]),'2.3':ids([1,2,3,4,5,6,7,8,9,14,15,16,17,19]),'2.4':ids([1,2,3,4,5,6,7,8,9,14,15,16,18,19])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    for n in ['2.3','2.4']:assert not ids([10,11,12,13])&expected_reach[n]
    assert 'D17' not in expected_reach['2.4'] and 'D18' not in expected_reach['2.3']
    assert 'D19' not in expected_reach['2.1']|expected_reach['2.2']
    assert 'D10' not in local['D6'] and 'D5' not in local['D10']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==10 and len(ambient['source_issues'])==13
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
        assert obj['evidence'] and all(1<=e['page']<=23 for e in obj['evidence'])
        for e in obj['evidence']:
            if e['page']==23:assert e.get('before_main_text_end',False)
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
    counts=dict(theorems=4,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=4,interfaces=19,source_members=19,direct_theorem_uses=33,related_theorem_connections=49,unranked_auxiliary_passages=10)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Four complete main-text Theorems, numbered 2.1–2.4. Theorem 2.2 spans pages 5–6 with eleven centering terms, eight additive variance terms and full auxiliary matrix/kernel definitions. Independent small-cap heading enumeration excludes proof headings, citations and Lemma 2.5.',
      source_passages='Nineteen entries and ten supporting passages preserve the exact linear inverse-correlation model, pooled covariance, sample correlation, unpenalized estimator, iid fourth-moment assumption, distinct sample/population B, full CLT normalizers, fitted precision and null/alternative test statistics.',
      dependencies='Independent reconstruction confirms 33 direct uses and 49 related connections. T2.3–T2.4 inherit T2.2 assumptions without acquiring its contrast-specific nu, sigma, D0 or D1. T2.4 replaces H0 by H1 and uses population rather than estimated normalizers.',
      scope='The later Discussion explicitly supplies bounded correlation spectral norm for T2.3–T2.4, finite active K and inclusion of the true basis set. Those passages are preserved separately from the original theorem wording. Conditions for simplified power comparisons are not inserted into the full theorem.',
      source_issues='Thirteen source issues remain explicit: theta-hat reuse for raw/corrected/penalized fits, implicit inverse and scale existence, the y=1 singularity, arbitrary zero contrast, trace powers, a.s. versus proof o_p wording, n scaling and local-alternative ambiguity. No source statement is repaired or proof certified.',
      names_and_highlights='Every entry retains literal source terms, source kind and heading, and source-backed selectors. All 49 related theorem connections have explicit paper-local paths and explanations; reused notation does not merge distinct definitions.',
      reproduction='All six content JSON artifacts reproduce byte for byte using the seven saved per-paper scripts. Frozen hashes, source-specific formula checks, independent heading enumeration, reconstructed dependency graph and schema validation pass.')
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=[4,5,6,7,8,22,23],visually_reviewed_crops=[]))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=24,main_text_last_pdf_page=23,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent small-cap heading enumeration and visual comparison of all four complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Published journal PDF registered as 24-AOS2433-1.pdf, pinned by hash and its ScholarSphere download URL.','Supplementary and appendix bodies excluded. Penalties and HBIC are named externally; no theorem for arbitrary penalized fits is inferred.','Source and schema validation do not certify mathematical proofs or repair source ambiguities.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=24,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:['finite and positive definite',r'H_0:\boldsymbol\mu_1=\boldsymbol\mu_2',r'H_1:\boldsymbol\mu_1\ne\boldsymbol\mu_2'],
2:[r'(n_1+n_2-2)^{-1}',r'\sum_{m=1}^2\sum_{i=1}^{n_m}',r'(\mathbf x_{mi}-\bar{\mathbf x}_m)^T'],
3:[r'\mathbf\Sigma=\mathbf D^{1/2}\mathbf R\mathbf D^{1/2}',r'\operatorname{diag}(\mathbf S)'],
4:[r'\mathbf R^{-1}=\theta_1\mathbf A_1+\cdots+\theta_K\mathbf A_K','symmetric matrix bases'],
5:[r'\widehat{\mathbf R}=[\operatorname{diag}(\mathbf S)]^{-1/2}\mathbf S[\operatorname{diag}(\mathbf S)]^{-1/2}'],
6:[r'\operatorname{tr}[\widehat{\mathbf R}',r'p^{-1}\operatorname{tr}(\widehat{\mathbf R}\mathbf A_k\widehat{\mathbf R}\mathbf A_l)',r'\widehat{\boldsymbol\theta}=\mathbf B^{-1}\mathbf b'],
7:[r'y_{n-2}=p/(n-2)','exists and is finite'],
8:['independent and identically distributed',r'E(w_j)=0',r'E(w_j^2)=1',r'E(w_j^4)=\kappa'],
9:[r'p^{-1}\operatorname{tr}(\mathbf R\mathbf A_i\mathbf R\mathbf A_j)','bounded'],
10:[r'p^{-1}\operatorname{tr}(\mathbf R\mathbf A_k\mathbf R\mathbf A_\ell)',r'y_{n-2}p^{-2}\operatorname{tr}(\mathbf R\mathbf A_k)\operatorname{tr}(\mathbf R\mathbf A_\ell)'],
11:[r'2(\mathbf e_i^T\mathbf R\mathbf e_j)^3',r'\beta_w=\kappa-3',r'g(i,j,\beta_w,\mathbf R)=2(\mathbf e_i^T\mathbf R\mathbf e_j)^2'],
12:[r'\mathbf D_1=\eta_1\mathbf A_1+\cdots+\eta_K\mathbf A_K',r'(\eta_1,\ldots,\eta_K)=(\pi_1,\ldots,\pi_K)\mathbf B^{-1}'],
13:[r'\frac{n(n-1)}{4(n-2)^3}\operatorname{tr}(\mathbf D_0\mathbf D_1)',r'\frac{n(2n-1)}{(n-2)^2(n-2+p)}',r'\frac{(n_1-1)p}{n_1(n-2)^2}',r'\frac{(n_2-1)p}{n_2(n-2)^2}',r'\frac{3n(n-1)\operatorname{tr}(\mathbf R\mathbf D_1)}{4(n-2)^4}',r'\frac{5n(n-1)}{4(n-2)^2(n-2+p)}',r'\frac{n(n-1)(3n-6+p)}{4(n-2)^3(n-2+p)}',r'\frac{1+2y}{1-y}',r'\operatorname{tr}[(\mathbf R\mathbf D_1)^2]',r'y[n^{-1}\operatorname{tr}(\mathbf R\mathbf D_1)^2]',r'2\mathbf e_\ell^T\mathbf R^2\mathbf e_\ell+\beta_w'],
14:[r'\widehat{\mathbf R}_L^{-1}=\widehat\theta_1\mathbf A_1',r'\widehat{\mathbf\Omega}=[\operatorname{diag}(\mathbf S)]^{-1/2}\widehat{\mathbf R}_L^{-1}'],
15:[r'T_n=(\bar{\mathbf x}_1-\bar{\mathbf x}_2)^T\widehat{\mathbf\Omega}(\bar{\mathbf x}_1-\bar{\mathbf x}_2)'],
16:[r'4n^2p(n_1n_2)^{-1}',r'(nn_1^{-2}+nn_2^{-2})',r'\frac{n(n-1)}{4(n-2)^2}',r'a_{h,\ell}=2(\mathbf e_h^T\mathbf R\mathbf e_\ell)^3'],
17:[r'\widetilde{\mathbf R}=\{\operatorname{diag}[\widehat{\mathbf R}_L]\}^{-1/2}',r'in $\sigma_0^2$ and $\mu_0$'],
18:[r'H_1:\boldsymbol\mu_1\ne\boldsymbol\mu_2',r'c=(1+y)^{-1}',r'\delta_n=\boldsymbol\mu_d^T\mathbf\Sigma^{-1}\boldsymbol\mu_d'],
19:['Theorems 2.3–2.4','bounded spectral norm','future work']}
    for n,parts in checks.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    assert 'n(\bar' not in s['D15']
    assert r'\widehat{\mathbf R}' not in s['D10'] and r'y_{n-2}' not in s['D6']
    assert r'\beta_w' not in s['D16'] and r'\mathbf A_0' not in s['D11']
    assert m['D19']['source_kind']=='condition'
    assert m['D7']['source_kind']=='assumption'
    assert all(m['D'+str(i)]['source_kind']=='theorem_excerpt' for i in [8,9,10,11,12,13,16,17,18])
    a={k:v['statement_original'] for k,v in aux.items()}
    for n,parts in {1:[r'n=n_1+n_2',r'T=n('],2:[r'[(n+p-2)/(n-2)]\widehat\theta_k','final estimate'],3:[r'\widehat{\boldsymbol\theta}=\min',r'\sum_{k=1}^Kp_\lambda(|\theta_k|)','HBIC','SCAD','MCP'],4:[r'\delta_n=o(1)',r'\gamma\in(0,1)'],5:[r'p^{-2}\operatorname{tr}(\mathbf R^2)=o(1)'],6:['set of true basis matrices','included in the candidate set'],7:['number of active basis matrices','finite',r'K\to\infty','future research'],8:['bounded spectral norm'],9:[r'\mathbf\Sigma^{-1/2}',r'N(\sqrt n\mathbf a^T\boldsymbol\mu_d'],10:['proof of Theorem 2.1']}.items():
        for part in parts:assert part in a['A'+str(n)],(n,part)
    assert set(ambient['statement_local_bindings'])=={'T2.1','T2.2','T2.3','T2.4'}
    assert {x['issue_id'] for x in ambient['source_issues']}=={'sample-versus-population-b','coefficient-estimator-overloading','inverse-existence','unit-aspect-ratio','zero-contrast-scale','trace-power-placement','almost-sure-versus-proof','test-statistic-scaling','null-and-alternative-inheritance','later-spectral-condition','local-alternative-scope','finite-active-bases','directional-whitening'}
    refs=ambient['source_claim_references'];assert sum(x['reference_kind']=='assumption_reference' for x in refs)==3
    assert sum(x['reference_kind']=='proof_only' for x in refs)==2
    for o in aux.values():assert set(o['depends_on'])<=set(m)
if __name__=='__main__':main()
