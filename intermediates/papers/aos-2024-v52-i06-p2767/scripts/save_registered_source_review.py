"""Check frozen source-reviewed content and independently reconstruct theorem reach."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '9b1b2f013556806f68bf9df63b1354bb9edec574989fdddcb75d3d30fb9b1c25', 'source-passages.json': '0ea7846f8659e4a9a2195a50507a68e2d22a805828aa3ee8c1e422fe01f5b6fd', 'interface-extraction.json': 'fbb8c9a200cc115dc489b7e6eb3ab1b9c1bddf36085ca303abb5a39007d6f3e7', 'ambient-prerequisites.json': 'fb6cec8b030a8547efca720f550c4d91088003c1173c0df34e291fd3a11f8bde', 'unfinalized-census.json': '966318f83755448d2c260f779c13e24ea874e92fc21fd8c53edf139a8d39a1a1', 'ranked-interfaces.json': '9e4398f520d1b7882eb76c5012e49f4b2b2dd5940c588bbe1dcc65ac844d6a68'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'\frac12\int|dP-dQ|'],
2:[r'\left(\frac12\int(\sqrt{dP}-\sqrt{dQ})^2\right)^{1/2}'],
3:[r'\chi^2(P\|Q)=\int\frac{(dP-dQ)^2}{dQ}'],
4:['there exists a (possibly randomized) map',r'T_{\mathcal P,n,m,\varepsilon}:\mathcal X^n\to\mathcal X^{n+m}',r'\sup_{P\in\mathcal P}',r'\le\varepsilon'],
5:[r'\inf_T\sup_{P\in\mathcal P}',r'P^{\otimes(n+m)}-P^{\otimes n}\circ T^{-1}','randomized) measurable mappings'],
6:[r'\max\{m\in\mathbb N:\varepsilon^\star(\mathcal P,n,m)\le\varepsilon\}',r'(say $0.1$)',r'\varepsilon\in(0,1)'],
7:[r'\theta-X-T',r'\theta-T-X','if and only if both'],
8:[r'\widehat T_{n+m}=f(T_n)',r'P_{X^{n+m}\mid T_{n+m}}(\cdot\mid\widehat T_{n+m})','5. Output'],
9:[r'\exp(\theta^\top T(x)-A(\theta))',r'\Theta=\{\theta\in\mathbb R^d:A(\theta)<\infty\}','base measure'],
10:['non-empty interior','Under each',r'\mathcal L(T(X))','absolutely continuous','Lebesgue measure'],
11:[r'\sup_{\theta\in\Theta}\mathbb E_\theta',r'\left\|(\nabla^2A(\theta))^{-1/2}(T(X)-\nabla A(\theta))\right\|_2^k',r'$M_k$'],
12:['i.i.d. samples','Definition 4.3',r'T_n(X^n)\triangleq\frac1n\sum_{i=1}^nT(X_i)','Algorithm 1',r'\widehat T_{n+m}=T_n'],
13:[r'P_\theta(dx)=\prod_{i=1}^dp_{\theta_i}(dx_i)','one-dimensional exponential family'],
14:[r'\inf_{\widehat P_n}\sup_{P\in\mathcal P}\mathbb E_P[\chi^2(\widehat P_n,P)]','all possible distribution estimators'],
15:[r'\mathcal P=\prod_{j=1}^d\mathcal P_j',r'P_\theta=\prod_{j=1}^dp_{\theta_j}',r'\prod_{j=1}^d\Theta_j'],
16:[r'P_\theta=\mathcal N(\theta,\Sigma)','unknown mean','known covariance'],
17:[r'\frac1n\sum_{i=1}^nX_i\sim\mathcal N(\theta,\Sigma/n)',r'\widehat T_{n+m}=T_n','algorithm 1','conditioned on the event'],
18:[r'a^\top T(x)=0',r'$\mu$-almost all',r'implies $a=0$'],
19:['product structure as in Theorem 6.4','For each',r'1/(10n)\le H^2(p_{\theta_{j,+}},p_{\theta_{j,-}})\le1/(5n)'],
20:[r'\sum_{i=0}^dp_i=1,p_0=t','perfect knowledge',r't\in[1/(2\sqrt d),1/2]'],
21:[r'\Sigma=UU^\top',r'U\in\mathbb R^{p\times d}',r'U^\top U=I_d','isotropic'],
22:[r'$L$-Lipschitz',r'|f(x)-f(y)|\le L|x-y|',r'for all $x,y\in[0,1]$'],
23:[r'\mathcal P_c\subseteq\mathcal P',r'f(x)\ge c',r'for all $x\in[0,1]$']}
    assert set(checks)==set(range(1,24))
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    for n,label in [(10,'Assumption 1 (Continuity)'),(11,'Assumption 2 (Moment condition Mk)'),(18,'Assumption 3 (Linear independence)'),(19,'Assumption 4')]:
        assert m['D'+str(n)]['source_kind']=='assumption' and m['D'+str(n)]['source_heading']==label
    for n,label in [(4,'Definition 1.1 (Sample Amplification)'),(9,'Definition 4.3 (Exponential family)'),(14,'Definition 5.1 (Chi-squared estimation error)')]:assert m['D'+str(n)]['source_heading']==label
    assert r'\chi^2(P,\widehat P_n)' not in s['D14']
    assert 'continuity' not in s['D19'] and 'alpha' not in s['D19']
    assert 'Assumption 2' not in t['6.3'] and 'Assumption 4' not in t['6.4']
    assert r'\Sigma\succ0' not in t['6.2'] and r'n,m\ge0' in t['5.2']
    assert r'\mathcal P,n)\asymp' not in t['7.3'] and r'\lceil' in t['6.5']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert 'pushforward probability measure' in a['A1'] and r'n^\star(\mathcal P)' in a['A2']
    assert r'\operatorname{Cov}_\theta[T(X)]=\nabla^2A(\theta)' in a['A3']
    assert r'\inf_{T_1}\sup_\theta' in a['A4'] and r'\inf_{T_2}\sup_\theta' in a['A4']
    assert r'r_B(\mathcal P,n,L,\mu)' in a['A5'] and r'r(\mathcal P,n,L)' in a['A5']
    assert r'\mathcal N(0,\Sigma)^{\otimes(n+m)}' in a['A6']
    assert r'X_{n/2+1}' in a['A7'] and r'X_{n/2+1,j}' in a['A8']
    assert r'(\nabla^2A(\theta)[u;u])^{3/2}' in a['A9'] and 'drop Assumption 2' in a['A10']
    assert ambient['unresolved_external_prerequisites']==[]
    # Source-limit witness: a known zero covariance reveals theta exactly from one observation.
    # The printed full-dimension Gaussian RHS is positive for m>0, whereas repetition amplifies perfectly.
    assert any(x['issue_id']=='singular-known-covariance' and 'Sigma=0' in x['note'] for x in ambient['source_issues'])

def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2201.04315v2.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==62
    assert paper['main_text_last_pdf_page']==22 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==11
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent reconstruction from inspected source clauses; no finalizer import.
    raw={1: [], 2: [], 3: [], 4: [1], 5: [1], 6: [4, 5], 7: [], 8: [7], 9: [7], 10: [9], 11: [9], 12: [7, 8, 9], 13: [9, 15], 14: [3], 15: [], 16: [], 17: [7, 8, 16], 18: [9], 19: [2, 15], 20: [], 21: [], 22: [], 23: [22]}
    local={"D"+str(k):ids(v) for k,v in raw.items()}
    direct={k:ids(v) for k,v in {'4.5': [1, 4, 5, 9, 10, 11, 12], '4.6': [1, 4, 5, 10, 11, 12, 13], '5.2': [5, 14], '5.5': [5, 14, 15], '6.2': [1, 5, 16, 17], '6.3': [5, 9, 10, 18], '6.4': [1, 5, 15], '6.5': [5, 15, 19], '7.1': [4, 20], '7.2': [4, 21], '7.3': [6, 22, 23]}.items()}
    expected_reach={k:ids(v) for k,v in {'4.5': [1, 4, 5, 7, 8, 9, 10, 11, 12], '4.6': [1, 4, 5, 7, 8, 9, 10, 11, 12, 13, 15], '5.2': [1, 3, 5, 14], '5.5': [1, 3, 5, 14, 15], '6.2': [1, 5, 7, 8, 16, 17], '6.3': [1, 5, 7, 9, 10, 18], '6.4': [1, 5, 15], '6.5': [1, 2, 5, 15, 19], '7.1': [1, 4, 20], '7.2': [1, 4, 21], '7.3': [1, 4, 5, 6, 22, 23]}.items()}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([8,11,12,13,14,15,17])&expected_reach['6.3']
    assert not ids([7,8,9,10,11,12,13,17])&expected_reach['5.2']
    assert 'D19' not in expected_reach['6.4'] and 'D1' not in local['D19']
    assert 'D16' not in expected_reach['7.2'] and 'D21' not in expected_reach['6.2']
    assert not ids([2,3,7,8,9,10,11,12,13,14,15])&expected_reach['7.3']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==10 and len(ambient['source_issues'])==14
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
        assert obj['evidence'] and all(1<=e['page']<=22 for e in obj['evidence'])
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
                assert all(1<=e['page']<=22 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=11,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=11,interfaces=23,source_members=23,direct_theorem_uses=40,related_theorem_connections=61,unranked_auxiliary_passages=10),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings={'inventory': 'Eleven original main-text Theorems4.5,4.6,5.2,5.5,6.2,6.3,6.4,6.5,7.1,7.2,7.3 independently enumerated by bold font and visually compared. Theorem6.3 includes the constant-dependence continuation on19. Appendix bodies starting23 are excluded.', 'source_passages': 'Twenty-three source entries preserve normalized divergences, amplification existence/error/size definitions, sufficiency and Algorithm1, natural and product exponential families, Assumptions1–4, estimator-first chi-squared risk, Gaussian procedure and the three Section7 examples. Ten auxiliary passages retain source notation and proof machinery separately.', 'dependencies': 'Independent source-clause reconstruction verifies40 direct uses and61 related-theorem connections. Theorem6.3 has no moment-Assumption2 dependency. Assumption4 imports only product structure from6.4. Chi-squared upper-bound theorems do not acquire proof-only shuffling or sufficiency assumptions. Theorem7.3 does not require a learning-risk definition.', 'source_issues': 'Fourteen notes preserve parameter-domain and Hessian limitations, pointwise-versus-minimax TV wording, infimum/attainment/max-size conventions, n=0 and odd-n ambiguity, divergence normalization/orientation, singular known covariance, linear versus affine independence, componentwise moment uniformity, pair existence versus continuity, ceilings and distinct model/rate scopes.', 'names_and_highlights': 'All23 entries have literal source keywords, faithful source headings/kinds and meaningful matching selectors. All61 related-theorem connections have a valid same-paper path and a source-specific explanation. The moment assumption retains the Euclidean double-bar norm.', 'reproduction': 'All six content JSONs reproduce byte for byte in a fresh empty directory. Seven retained scripts support generation and separate inventory/full-source review. Rebuilding is not a new semantic review.', 'limits': 'Source review preserves statements rather than certifying theorem truth. In particular, the exact known-covariance Gaussian formula does not expressly exclude singular Sigma; a zero-covariance witness exposes that missing convention. No source formula is silently repaired.'}
    reviewed_pages=[1,7,8,9,10,11,12,13,14,15,16,18,19,20,21,22]
    crops=[]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=crops))
    evidence=[dict(path=f'evidence/page-{n:02}.png',page=n) for n in reviewed_pages]+crops+[dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=62,main_text_last_pdf_page=22,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-font theorem-heading enumeration and visual comparison of all eleven complete statements, including the continuation of6.3.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv2201.04315v2 stamped18Sep2024, title-page19Sep2024,62pages, pinned bySHA256; not silently exchanged for the published article.','Main text ends on22 after Section7.3 and Funding. Appendix A starts23; all appendix bodies are excluded.','Source review preserves mathematical statements, dependencies and unresolved source notation; it does not certify proofs or solve implicit selection/domain conventions.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=62,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
