"""Verify frozen, source-reviewed content using independent branch and graph checks."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': 'a5dabb65fb4a8cc35782f5f6af7c48d348aaed7f7370a7cfeadd23968d93b7c6', 'source-passages.json': '65694e06a1ce37e54895f1c5e07d68224c51e1dea189105f219c95640b02eda7', 'interface-extraction.json': 'bf61c0fa57e95e09068d740685d784b82b4520a6dca1dade3da0045dd9eb42a0', 'ambient-prerequisites.json': 'd8aa6e0026a6dae27e34c2df67bfdeec167088de16690fb15906d483a28b3434', 'unfinalized-census.json': 'eb41add7fb1164f35c29deef85df798a568c3d45720bf43753bfb718cce50e22', 'ranked-interfaces.json': '80c9720311f340cbf0790e3221dcdd5c027358fbd4883b8b119f598ea90980ea'}
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
    assert registered['version']=='AOS2401-003R2A0.pdf' and registered['source_url']==URL
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==25
    assert paper['main_text_last_pdf_page']==20 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    assert len(inv['claims'])==len(d['claims'])==3
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independently reconstructed from the original source definitions and statement clauses.
    raw={1:[],2:[1],3:[2],4:[3],5:[2,4],6:[3,5],7:[],8:[7],9:[7],10:[9],11:[1,9,10],12:[9,10],13:[1,9],14:[2,12,23],15:[13,14,23],16:[7,11],17:[11,16],18:[1,9],19:[1,7,9,13,16,18],20:[2,12,23],21:[],22:[2,10,17],23:[7]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'4.1':ids([3,4,6]),'4.3':ids([3,8,10,14,15,17,19]),'4.4':ids([3,19,20,21,22])}
    expected_reach={'4.1':ids([1,2,3,4,5,6]),'4.3':ids([1,2,3,7,8,9,10,11,12,13,14,15,16,17,18,19,23]),'4.4':ids([1,2,3,7,9,10,11,12,13,16,17,18,19,20,21,22,23])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert expected_reach['4.1']==ids([1,2,3,4,5,6])
    assert not (ids([4,5,6]) & (expected_reach['4.3']|expected_reach['4.4']))
    assert 'D8' in expected_reach['4.3'] and 'D8' not in expected_reach['4.4']
    assert ids([20,21,22]) <= expected_reach['4.4'] and not (ids([20,21,22]) & expected_reach['4.3'])
    assert 'D14' not in expected_reach['4.4'] and 'D15' not in expected_reach['4.4']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==9 and len(ambient['source_issues'])==11
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
        assert obj['evidence'] and all(1<=e['page']<=20 for e in obj['evidence'])
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
                assert all(1<=e['page']<=20 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=3,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=3,interfaces=23,source_members=23,direct_theorem_uses=15,related_theorem_connections=40,unranked_auxiliary_passages=9),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Three complete main-text Theorems4.1,4.3,4.4 independently enumerated by exact small-cap headings. Proposition4.2 and Proposition4.5 are excluded. The main text ends at manuscript line639 on shared PDF page20 before the mathematical appendix.',
      source_passages='Twenty-three original entries preserve the positive definite kernel, RKHS and dual, AssumptionA and covariance Gaussian limit, data and CMR hypotheses, scores, population/sample projections, Gram matrix, feasible statistic, two weighted measures and the projected spectrum, AssumptionB(i)–(iv), fitted residuals, multiplier bootstrap and its cited almost-sure convergence convention. Nine auxiliary passages preserve relevant context and non-Theorem results.',
      dependencies='Independent reconstruction verifies15 direct uses and40 related connections. Theorem4.1 reaches only the abstract kernel/Hilbert/covariance objects. The applied theorems do not inherit AssumptionA through its proof application. Theorem4.4 references the limit formula of Theorem4.3 without silently inheriting H0, and B(v) and AssumptionC are not imported.',
      scope='Distinguish H_K, L2(P_X) and L2(mu), population Pi and empirical Pi-hat, raw and projected Gram matrices, fitted and true-parameter residual processes, conditional second moments and variances, and abstract versus projected spectral normalizations. Bootstrap holds estimates fixed and resamples bounded iid independent multipliers.',
      source_issues='Eleven notes preserve the registered manuscript identity, eigenbasis normalization and implicit zero-mode conventions, missing explicit H0 in Theorem4.4, its conditional almost-sure strength, the raw-Gram eigenvalue order, Lemma3.4 scaling mismatch, matrix-valued score measure, empirical inverse/domain conventions, boundary-neighborhood ambiguity, later/proof-only hypotheses and joint sampling conventions.',
      names_and_highlights='All23 entries carry original natural-language terms, source labels/kinds and literal meaning-bearing selectors. Every related theorem has a verified same-paper path and a specific correspondence explanation. Assumption passages remain labeled Assumption; the R_infinity formula is explicitly a Theorem4.3 excerpt.',
      reproduction='All six content JSON artifacts reproduce byte for byte in a fresh directory. Seven retained paper-specific scripts preserve inventory extraction/review, original passages, ambient context, finalization, reproducible rebuilding and independent review with frozen hashes and source-specific checks.')
    reviewed_pages=[1,3,6,8,9,10,11,12,13,14,20]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[]))
    evidence=[dict(path='evidence/page-'+str(n).zfill(2)+'.jpg',page=n) for n in reviewed_pages]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=25,main_text_last_pdf_page=20,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent exact small-cap heading enumeration and visual comparison of all three complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark','Conjecture'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered IMS manuscript AOS2401-003R2A0.pdf, marked Submitted to the Annals of Statistics, pinned by SHA-256. No substitution or invented publication date.','Main text ends on PDF page20 at manuscript line639, clipped at y=216 before the mathematical appendix at y=223.09. Appendix bodies are excluded.','Source and schema validation do not certify proofs or resolve the explicitly recorded notation and bootstrap-scope ambiguities.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=25,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:['positive definite kernel',r'\sum_{i=1}^n\sum_{j=1}^nc_ic_jK(x_i,x_j)\ge0'],
2:[r'\mathcal H_K',r'\mathcal B_K=\{h\in\mathcal H_K:\|h\|_K\le1\}'],
3:[r'\|S\|:=\sup_{a\in\mathcal B_K}|S(a)|','separable','Hoffmann-Jorgensen',r'Borel $\sigma$ field'],
4:[r'\sigma^2(a)=\sigma(a,a)\ge0','continuous, positive symmetric bilinear form',r'\sum_{j=1}^\infty\sigma^2(e_j)<\infty',r'\lim_{J\to\infty}\limsup_{n\to\infty}',r'\sum_{j\ge1+J}S_n^2(e_j)\ge\varepsilon'],
5:[r'T_\sigma a(x):=\sigma(a,K_x)',r'T_\sigma\phi_j=\mu_j\phi_j','orthonormal in $\mathcal H_K$'],
6:[r'\sqrt{\mu_j}\langle\phi_j,\cdot\rangle_KU_j','iid standard normals'],
7:[r'\varepsilon:\mathcal Z\times\Theta\longrightarrow\mathbb R^q','case $q=1$','non-overlapping','independent and identically distributed'],
8:[r'E[\varepsilon(Z,\theta_0)\mid X]=0','some unknown',r'H_0:(1)',r'P(E[\varepsilon(Z,\theta)\mid X]=0)<1\text{ for all }\theta\in\Theta'],
9:[r'\frac{\partial\varepsilon(Z,\theta_0)}{\partial\theta}',r'g(X,\theta_0):=E[s(Z,\theta_0)\mid X]'],
10:[r'\Pi a(x)=a(x)-G(a,\theta_0)\Gamma^{-1}g(x,\theta_0)',r"G(a,\theta):=E[a(X)g'(X,\theta)]",r"\Gamma:=E[g(X,\theta_0)g'(X,\theta_0)]",'non-singular'],
11:[r'\Upsilon(x_1,x_2)',r'-E[\Upsilon(X,x_i)K(X,x_j)]-E[\Upsilon(X,x_j)K(X,x_i)]',r'+E[\Upsilon(x_i,X)K(X,\widetilde X)\Upsilon(\widetilde X,x_j)]'],
12:[r'\widehat\Pi a(X_i)=a(X_i)-G_n(a,\widehat\theta)\Gamma_n^{-1}g(X_i,\widehat\theta)',r"G_n(a,\theta)=n^{-1}\sum_{i=1}^ng'(X_i,\theta)a(X_i)",r"\Gamma_n=n^{-1}\sum_{i=1}^ng(X_i,\widehat\theta)g'(X_i,\widehat\theta)"],
13:[r'K(X_i,X_j)/n',r"\widehat{\mathbb K}=\widehat\Pi_{\mathbb G}'\mathbb K\widehat\Pi_{\mathbb G}",r"I_n-\mathbb G(\mathbb G'\mathbb G)^{-1}\mathbb G'"],
14:[r'\widehat R_n(a)=\frac1{\sqrt n}',r'(\widehat\Pi a(X_i))\widehat\varepsilon_i',r'a\in\mathcal H_K'],
15:[r"n\widehat Q_K^\perp=\widehat\varepsilon'\widehat{\mathbb K}\widehat\varepsilon",r'\sup_{a\in\mathcal B_K}(\widehat R_n(a))^2'],
16:[r'\sigma_\varepsilon^2(X,\theta_0):=E[\varepsilon^2(Z,\theta_0)\mid X]',r'd\mu(x):=\sigma_\varepsilon^2(x,\theta_0)dF_X(x)',r'\kappa^\perp:=\int_{\mathcal X}K^\perp(x,x)d\mu(x)<\infty'],
17:[r'T_{K^\perp}:L_2(\mu)\to L_2(\mu)',r'K^\perp(x_1,x_2)f(x_1)d\mu(x_1)',r'\lambda_j\ge0','orthonormal in $L_2(\mu)$',r'L_2(\mu\times\mu)',r'\mu\times\mu\text{-a.s.}'],
18:[r'\Theta_0','neighborhood',r"\sigma_s^2(X,\theta_0)=E[s(Z,\theta_0)s'(Z,\theta_0)\mid X]",r'\kappa_s:=\int_{\mathcal X}K(x,x)d\mu_s(x)',r'\dot s(z,\theta):=(\partial/\partial\theta)s(z,\theta)'],
19:[r'E[K(X,X)]<\infty',r'\lambda_{\max}(\mathbb K)=O_P(n^{-1})','twice continuously differentiable',r'E[\sup_{\theta\in\Theta_0}|s(Z,\theta)|^2]<\infty',r'E[\sup_{\theta\in\Theta_0}|\dot s(Z,\theta)|^2]<\infty',r"E[g(X,\theta)g'(X,\theta)]",r'E[\sup_{\theta\in\Theta_0}(\varepsilon(Z,\theta))^2]<\infty',r'$\Theta$ is compact in $\mathbb R^p$',r'|\widehat\theta-\theta_0|=O_P(n^{-1/2})'],
20:[r'\widehat R_n^*(a)=\frac1{\sqrt n}',r'(\widehat\Pi a(X_i))V_i\widehat\varepsilon_i','zero mean, unit variance, bounded support','independent of the original data'],
21:['a.s. consistency',r'\xrightarrow{d}$ a.s.','[21] or Chapter 2.9 in [55]'],
22:[r'\lambda_j\langle\varphi_j,\Pi a\rangle_{K^\perp}U_j'],
23:[r'\widehat\varepsilon_i=\varepsilon(Z_i,\widehat\theta)',r'i=1,\ldots,n']}
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert m['D4']['source_kind']==m['D19']['source_kind']=='assumption'
    assert m['D8']['source_kind']=='condition' and m['D22']['source_kind']=='theorem_excerpt'
    assert '(v)' not in s['D19'] and 'H_0' not in s['D19']+s['D22']
    assert r'\sqrt{\lambda_j}' not in s['D22']
    assert m['D12']['depends_on']==['D9','D10']
    a={k:v['statement_original'] for k,v in aux.items()}
    ac={1:[r'S_n\in\mathcal H_K^*','each $n\ge1$'],2:['Gaussian vector','covariance matrix'],3:['independent copies','square integrable measurable functions of $X$'],4:[r'R_n(\Pi a)=\frac1{\sqrt n}',r'\varepsilon(Z_i,\theta_0)','infeasible'],5:['Proposition 4.2',r'\Gamma^{-1}\dot G\sqrt n(\widehat\theta-\theta_0)',r'\dot G\ne0'],6:['a.s. consistency','Chapter 2.9'],7:[r'\delta(X)}{\sqrt n}','Assumption B: (v)',r'E[\delta^2(X)/\sigma_\varepsilon^2(X)]',r'E[K^\perp(X,X)\delta^2(X)]'],8:[r'\frac1n\sum_{i=1}^nc_ia(x_i)',r"\sqrt{c'\mathbb Kc}"],9:['conditional score','nonparametric']}
    for n,parts in ac.items():
        for v in parts:assert v in a['A'+str(n)],(n,v)
    for obj in aux.values():assert set(obj['depends_on'])<=set(m)
    assert set(ambient['statement_local_bindings'])=={'T4.1','T4.3','T4.4'}
    assert {x['issue_id'] for x in ambient['source_issues']}=={'registered-version-and-scope','two-hilbert-space-spectra','bootstrap-null-scope','bootstrap-almost-sure-strength','gram-matrix-scaling','lemma34-normalization','matrix-valued-score-measure','projection-domain-and-inverses','boundary-and-neighborhood','later-assumptions-and-proof-only-results','sampling-and-residual-second-moment'}
    refs=ambient['source_claim_references']
    assert sum(x['reference_kind']=='assumption_reference' for x in refs)==3
    assert sum(x['reference_kind']=='definition_reference' for x in refs)==3
    assert sum(x['reference_kind']=='proof_only' for x in refs)==1
    assert sum(x['reference_kind']=='external_definition_reference' for x in refs)==1
if __name__=='__main__':main()
