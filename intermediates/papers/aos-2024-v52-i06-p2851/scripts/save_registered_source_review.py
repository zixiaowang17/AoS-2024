"""Independently check frozen source-reviewed PCM content and the four theorem closures."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': 'c6a49fdda565d43a359f258a17e2e2630b36a261410ae91e579fe48449f70e85', 'source-passages.json': '112676f82e10d9c21eb7a69d8a12dc670831313af1f74198247ed40685ac6abb', 'interface-extraction.json': '14c4c666174af44b32fff9352a96faaaca04004b01503efca9cc5e7c9adc25ae', 'ambient-prerequisites.json': '32bd183d4cf3fd9592927556f9daf5ac2aca3d65bb6367ee809b1c78faf0c87b', 'unfinalized-census.json': '97ec96e040919011490108629016fdee2df7de8212f8df3c7dae717e100c22cb', 'ranked-interfaces.json': '24357f5a79f230bd22fefcf1df2007c33c611bb9c55321e0baa28993589cbded'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
    1:['conditional mean independence',r'\mathbb E(Y\mid X,Z)=\mathbb E(Y\mid Z)'],
    2:[r'\tau:=\mathbb E',r'\{\mathbb E(Y\mid X,Z)-\mathbb E(Y\mid Z)\}^2','if and only if'],
    3:['permit the family',r'X_{P,n}=Y_{P,n}R_{P,n}','continuity points',r'\sup_{P\in\mathcal P}'],
    4:['independent datasets','sample used to construct','any additional randomness'],
    5:[r'z_\alpha','standard normal distribution',r'\Phi'],
    6:[r'm(\cdot):=\mathbb E(Y\mid Z=\cdot)'],
    7:[r'g_P(x,z):=\mathbb E_P(Y\mid X=x,Z=z)'],
    8:[r'h(X,Z):=\mathbb E(Y\mid X,Z)-\mathbb E(Y\mid Z)',r'v(X,Z):=\operatorname{Var}(Y\mid X,Z)','orthogonal to functions'],
    9:[r'm_{\hat f}(\cdot):=\mathbb E(\hat f(X,Z)\mid Z=\cdot,\hat f)'],
    10:[r'_{i=1}^{2n}',r'\operatorname{sgn}(\hat\rho)',r'\max\{\tilde v(X_i,Z_i),0\}+c',r'\hat c:=0',r'\hat f(x,z):=\hat h(x,z)/\hat v(x,z)',r'\sum_{i\in\mathcal I_1}L_i^2',r'T>z_{1-\alpha}'],
    11:[r'_{i=1}^{4n}','steps 3 (i) and 3 (ii)',r'$\mathcal D_3$ and $\mathcal D_4$, respectively'],
    12:[r'\varepsilon_{P,i}:=Y_i-m_P(Z_i)'],
    13:[r'\xi_{P,i}:=\hat f(X_i,Z_i)-m_{P,\hat f}(Z_i)','without a subscript'],
    14:[r'\sigma_P^2:=\operatorname{Var}_P(\xi_P\mid\hat f)'],
    15:[r'\mathcal E_{P,1}:=\frac1n',r'\{m_P(Z_i)-\hat m(Z_i)\}^2'],
    16:[r'\mathcal E_{P,2}:=\frac1{n\sigma_P^2}',r'\{m_{P,\hat f}(Z_i)-\hat m_{\hat f}(Z_i)\}^2'],
    17:[r'\mathcal E_{P,1}=o_{\mathcal P}(1)',r'\mathcal E_{P,2}=o_{\mathcal P}(1)',r'\mathcal E_{P,1}\mathcal E_{P,2}=o_{\mathcal P}(n^{-1})',r'\xi_{P,i}^2=o_{\mathcal P}(1)',r'\sup_{P\in\mathcal P}\operatorname{Var}_P(Y\mid X,Z)\le C'],
    18:['conditions (ii) and (iii) of Proposition S15 in Section S2'],
    19:[r'd:=d_X+d_Z',r'degree $r-1$',r'\mathcal S^{d_Z}_{r,N}',r'K_X:=(N+r)^{d_X}',r'\phi^X(x)\otimes\phi^Z(z)',r'u\otimes v:=\operatorname{vec}(uv^\top)',r'K_{XZ}:=K_XK_Z',r'\mathcal S^{d_Z}_{2r-1,N}',r'\tilde K_Z:=(N+2r-1)^{d_Z}'],
    20:['OLS',r'\hat v\equiv1',r'\phi(X,Z)',r'\phi^Z(Z)',r'\psi(Z)','always non-negative'],
    21:[r'\mathcal H^d_s',r'\|\cdot\|_{\mathcal H_s}','Definition S24'],
    22:[r'C\ge1',r'c\in(0,1]',r'\mathbb E_P(\varepsilon_P^2\mid X,Z)\ge c',r'\mathbb E_P(|\varepsilon_P|^{2+\delta}\mid X,Z)\le C',r'\sup_{(x,z)\in[0,1]^d}p_P(x,z)\le C',r'\inf_{(x,z)\in[0,1]^d}p_P(x,z)\ge c',r'p_{X\mid Z,P}(x\mid\cdot)\in \mathcal H^{d_Z}_s',r'\|p_{X\mid Z,P}(x,\cdot)\|_{\mathcal H_s}'],
    23:[r'x-\mathbf1\otimes\bar x',r'K_X^{-1}\sum_{\ell=1}^{K_X}x_{(k-1)K_X+\ell}'],
    24:[r'\hat\beta:=\hat\beta_{XZ}-\mathbf1\otimes\hat\beta_Z',r'\hat f(x,z)=\hat\beta^\top\phi(x,z)','partition of unity'],
    25:[r'\hat m_{a\cdot\hat f}(Z)=a\cdot\hat m_{\hat f}(Z)',r'$a>0$'],
    26:['Algorithm 1','linear smoother'],
    27:['conditional independence','entire conditional distribution']}
    assert set(checks)==set(range(1,28))
    for n,vs in checks.items():
        for v in vs:assert v in s['D'+str(n)],(n,v)
    for n,label in [(17,'Assumption 3'),(22,'Assumption 4')]:assert m['D'+str(n)]['source_kind']=='assumption' and m['D'+str(n)]['source_heading']==label
    assert m['D18']['source_kind']=='condition' and m['D21']['source_kind']=='source_passage'
    for n in [25,26]:assert m['D'+str(n)]['source_kind']=='theorem_excerpt'
    assert r'\hat m' not in s['D12'] and r'g_P' not in s['D12']
    assert r'\operatorname{Var}_P(\xi_P\mid\hat f)' in s['D14']
    assert '|h_P' not in t['5'] and r'\sup_{P\in\mathcal P_1}h_P(X,Z)\le C' in t['5']
    assert 'any of the following' in t['4'] and 'Suppose further that either' in t['5']
    assert 'Assumption 3' not in t['6']+t['7'] and 'sufficiently stable' not in t['6']+t['7']
    assert 'Algorithm 1' not in t['7'] and 'Algorithm 2' in t['7']
    assert r'\Pi x=x,\|x\|_2=1' in t['6']
    assert r'K_{XZ}^{1+2/\delta}' in t['6'] and r'n^{\frac{4s}{4s+d}}' in t['7']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert r'0/0:=0' in a['A1'] and r'\operatorname{sgn}(0):=0' in a['A1']
    assert 'independent and identically distributed' in a['A3']
    assert 'With the exception of Theorem 7' in a['A5'] and r'\mathcal D_3=\mathcal D_4' in a['A5']
    assert 'inconsistent estimator' in a['A6'] and r'\Pi x=0' in a['A7']
    assert 'proof of Theorem 6' in a['A8'] and 'known smoothness parameter' in a['A9']
    assert len(ambient['unresolved_external_prerequisites'])==3
    assert {i['issue_id'] for i in ambient['source_issues']}=={'registered-source','mean-versus-full-independence','training-split-assignment','conditioning-and-residuals','zero-and-correlation-conventions','theorem5-one-sided-bound','spline-overrides','spline-coordinate-conventions','assumption4-quantifiers','supplementary-definitions','rates-and-branch-scope'}
def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2211.02039v4.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==97
    assert paper['main_text_last_pdf_page']==29 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==4
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independently transcribed from source clauses; no extraction/finalizer imports.
    raw={1:[6,7],2:[8],3:[],4:[],5:[],6:[],7:[],8:[6,7],9:[4],10:[4,5],11:[4,5,10],12:[6],13:[9],14:[4,13],15:[6],16:[9,14],17:[3,13,14,15,16],18:[],19:[],20:[10,19],21:[],22:[6,7,12,19,21],23:[19],24:[19,20],25:[],26:[10],27:[]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'4':ids([1,3,4,5,10,11,12,13,14,17,18,26,27]),'5':ids([2,3,4,5,8,10,11,13,17,18,25]),'6':ids([1,5,10,11,19,20,22,23,24]),'7':ids([2,5,11,19,20,22])}
    expected_reach={'4':ids([1,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,26,27]),'5':ids([2,3,4,5,6,7,8,9,10,11,13,14,15,16,17,18,25]),'6':ids([1,4,5,6,7,10,11,12,19,20,21,22,23,24]),'7':ids([2,4,5,6,7,8,10,11,12,19,20,21,22])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    for n in ['6','7']:assert not (expected_reach[n]&ids([13,14,15,16,17,18,25,26,27]))
    assert local['D12']==ids([6]) and local['D13']==ids([9])
    assert 'D27' in direct['4'] and 'D27' not in expected_reach['5']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==9 and len(ambient['source_issues'])==11
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
                assert not any(ord(ch)<32 and ch!='\n' for ch in ctx['text'])
                assert all(1<=e['page']<=29 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=4,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=4,interfaces=27,source_members=27,direct_theorem_uses=39,related_theorem_connections=62,unranked_auxiliary_passages=9),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings={
    'inventory':'Four original main-text Theorems 4–7 independently enumerated across pages 1–29, with the full Theorem 6 continuation on page 22. All hypotheses, disjunctive algorithm branches, moment/correlation conditions, growth rates and conclusions were compared with the registered PDF. Propositions and all supplementary bodies are excluded.',
    'source_passages':'27 original source entries preserve the two distinct null notions, squared signal, regression targets, conditioning convention, complete Algorithms 1/2, residuals, normalized MSPEs, Assumptions 3/4, stability reference, spline spaces and regression choices, Holder reference, coefficient projection and contrast, and theorem-local learner conditions. Nine auxiliary passages retain ambient and proof context separately.',
    'dependencies':'Independent source-clause reconstruction gives 39 direct uses and 62 related-theorem connections. Alternatives remain disjunctive. The spline results retain their algorithm overrides without acquiring Assumption 3 or sufficient stability as extra premises. Assumption 4 response residuals do not depend on the learned projection residual.',
    'source_issues':'Eleven notes record source version, mean versus full independence, exact D3/D4 regression assignment, training-sample conditioning, response versus projection residuals, zero/correlation conventions, the one-sided h bound, spline overrides/coordinate ordering, delta quantifier scope, excluded supplementary definitions and rate/branch scope.',
    'names_and_highlights':'All 27 entries have literal natural-language source keywords, original source kinds/headings and matching meaningful selectors. All 62 connections have valid same-paper dependency paths and source-specific explanations. Spline and Holder spaces retain their printed calligraphic symbols.',
    'reproduction':'All six content JSONs reproduce byte for byte in a fresh empty directory. Seven retained scripts separate source extraction, inventory review, full-source review and reproduction. Rebuilding alone does not constitute a fresh semantic PDF review.',
    'limits':'Source fidelity and dependency validation do not certify proofs. Precise sufficient-stability, Holder and spline-endpoint definitions remain unresolved supplementary references. One-sided bounds, zero-division limitations and delta quantifier ambiguity are preserved rather than silently repaired.'}
    reviewed_pages=[1,3,4,7,8,11,17,18,19,20,21,22,23]
    crop=dict(path='evidence/page-29-main-text.png',page=29,y_end=202)
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[crop]))
    evidence=[dict(path=f'evidence/page-{n:02}.png',page=n) for n in reviewed_pages]+[crop,dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=97,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-font enumeration over main-text pages 1–29 and visual comparison of all four complete original statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv 2211.02039v4, 97 pages, pinned by SHA256; not silently replaced by published text.','Main text ends after acknowledgements before References on page 29; supplementary Proofs begin on page 34 and all supplementary bodies are excluded.','Source review preserves unresolved stability/Holder/spline definitions, the printed one-sided bound and moment quantifier order. It does not certify proof correctness.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=97,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
