"""Verify frozen, source-reviewed content using independent branch and graph checks."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': 'a88b97e30b05dcbb0d1a32aab3726d0137ed562353e0618f3e8fe8fada657dfc', 'source-passages.json': '07ea7dff588f1f4929e257fd37da84ca82a77b009e247d9c56da24e45765f23c', 'interface-extraction.json': '33df16239065c5ff84c999837bf601387f518783272984c52c23e331743bc68d', 'ambient-prerequisites.json': 'c02091f8aae4d123216b54cc271290c4c350e2582d134ab139ba6081a02bd906', 'unfinalized-census.json': 'cf38cfc3419961918e84d5c5b3d222cdb45daed5f524846d32c267edae2a11df', 'ranked-interfaces.json': '1ce7c914d7eec6fc391bd3c1ee0c2da4eace8f321b25e48c6b2f4c29f532fbe1'}
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
    assert registered['version']=='2206.13668v4.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2206.13668'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==53
    assert paper['main_text_last_pdf_page']==21 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==4
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independently reconstructed from the original source definitions and statement clauses.
    raw={1:[],2:[],3:[],4:[2,3],5:[2,3],6:[4,5],7:[2],8:[1],9:[2,7],10:[],11:[2],12:[2],13:[2]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'5.3':ids([2,7,9,10,11]),'5.5':ids([1,6,8,10,11]),'5.10':ids([2,7,9,10,12]),'5.14':ids([1,6,8,10,12,13])}
    expected_reach={'5.3':ids([2,7,9,10,11]),'5.5':ids([1,2,3,4,5,6,8,10,11]),'5.10':ids([2,7,9,10,12]),'5.14':ids([1,2,3,4,5,6,8,10,12,13])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([1,3,4,5,6,8]) & (expected_reach['5.3']|expected_reach['5.10'])
    assert not ids([7,9]) & (expected_reach['5.5']|expected_reach['5.14'])
    assert 'D11' not in expected_reach['5.10']|expected_reach['5.14']
    assert 'D12' not in expected_reach['5.3']|expected_reach['5.5']
    assert 'D13' in direct['5.14'] and 'D13' not in expected_reach['5.10']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==9 and len(ambient['source_issues'])==10
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
        assert obj['evidence'] and all(1<=e['page']<=21 for e in obj['evidence'])
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
                assert all(1<=e['page']<=21 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=4,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=4,interfaces=13,source_members=13,direct_theorem_uses=21,related_theorem_connections=29,unranked_auxiliary_passages=9),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Four complete main-text Theorems5.3,5.5,5.10,5.14, independently enumerated by small-cap headings. Corollaries5.7/5.15, propositions, lemmas, remarks and proof headings are excluded. Preserve the r=2 branch and both original row sign/permutation identification statements. Main text ends with acknowledgements before references on PDF page21.',
      source_passages='Thirteen original source entries preserve model(1), symmetric tensors, generating functions, separate moment and cumulant definitions and their h_r notation, multilinear action, normalized observational candidates, admissible orthogonal transformations, signed permutations, Definitions5.1/5.8 and condition(14). Nine auxiliary passages retain context and proof/application distinctions.',
      dependencies='Independent reconstruction verifies21 direct uses and29 related connections. Algebraic Theorems5.3/5.10 do not inherit a random-vector model, moment realizability or generating-function assumptions. Statistical Theorems5.5/5.14 keep moment and cumulant interpretations as alternatives and do not import proof-only polynomial or stabilizer constructions. Condition(14) is inline in5.10 and explicitly referenced by5.14.',
      scope='Preserve orthogonal rather than general invertible Q, left multiplication of the unmixing matrix and row ambiguity, transformation sets versus parameter matrices, all-equal versus even-multiplicity index patterns, and distinct full diagonals versus repeated-pair contraction genericity. Population identification is distinct from estimation or independent-component recovery.',
      source_issues='Ten notes retain the registered title spelling, orthogonal domain, G_T-versus-Omega wording, algebraic/statistical scope, alternative h_r choices, implicit tensor/MGF existence regularity, separate genericity conditions, the normalized r=2 applicability limit, reflectional target versus exact stabilizer, and the absence of independence or estimator premises.',
      names_and_highlights='All13 entries have source-derived natural-language terms and literal meaningful highlights. Definitions5.1/5.8 retain original labels; condition(14) is a Theorem5.10 excerpt. Every related theorem has an independently checked local path and source-specific explanation, including the moment/cumulant alternatives.',
      reproduction='All six content JSON artifacts reproduce byte for byte in a fresh directory. Seven retained scripts preserve inventory extraction/review, original passages, context, finalization, reproducible rebuild and independent source review with frozen hashes and source-specific checks.')
    reviewed_pages=[1,5,6,7,8,9,10,11,12,13,21]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[]))
    evidence=[dict(path='evidence/page-'+str(n).zfill(2)+'.jpg',page=n) for n in reviewed_pages]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=53,main_text_last_pdf_page=21,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent small-cap heading enumeration and visual comparison of all four complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark','Conjecture'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2206.13668v4, marked19 Mar2024, pinned by SHA-256. The source title uses components, while the corpus label uses component.','Main text and acknowledgements end on PDF page21, clipped at y572 before REFERENCES at y580.205. Appendix and supplementary bodies are excluded.','Source and schema validation do not certify proofs, moment/cumulant existence beyond the stated conventions or the later estimation results.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=53,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'AY=\varepsilon','is invertible','mean-zero hidden random vector with uncorrelated components'],
2:['arbitrary permutation of the indices',r'S^r(\mathbb R^d)',r'\binom{d+r-1}{r}',r'1\le i_1\le\cdots\le i_r\le d'],
3:[r"M_X(t)=\mathbb E e^{t'X}",r"K_X(t)=\log\mathbb E e^{t'X}"],
4:[r'\mu_r(X)_{i_1\cdots i_r}=\mathbb E X_{i_1}\cdots X_{i_r}',r'\frac{\partial^r}{\partial t_{i_1}\cdots\partial t_{i_r}}M_X(t)\right|_{t=0}'],
5:[r'\kappa_r(X)_{i_1\cdots i_r}=\operatorname{cum}(X_{i_1},\ldots,X_{i_r})',r'\frac{\partial^r}{\partial t_{i_1}\cdots\partial t_{i_r}}K_X(t)\right|_{t=0}'],
6:['moment or cumulant tensor',r'h_r(X)',r'\mu_r(X)$ or $\kappa_r(X)'],
7:[r'(A\bullet T)_{i_1\cdots i_r}',r'\sum_{j_1=1}^d\cdots\sum_{j_r=1}^d A_{i_1j_1}\cdots A_{i_rj_r}T_{j_1\cdots j_r}',r'A\in\mathbb R^{d\times d}'],
8:[r'\operatorname{var}(\varepsilon)=I_d',r"\operatorname{var}(Y)=(A'A)^{-1}",r'\Omega:=\{QA:Q\in O(d)\}',r'\widetilde\varepsilon=Q\varepsilon'],
9:[r'\mathcal G_T(\mathcal V):=\{Q\in O(d):Q\bullet T\in\mathcal V\}',r'subset of $\Omega$',r'I_d\in\mathcal G_T(\mathcal V)'],
10:[r'\operatorname{SP}(d)',r'2^d d!',r'D,P\in O(d)','D$ diagonal','P$ a permutation matrix'],
11:[r'T_{\mathbf i}=0','unless',r'\mathbf i=(i,\ldots,i)',r'\mathcal V^{\mathrm{diag}}'],
12:['each index appears','even number of times','If $r$ is odd','zero tensor',r'\mathcal V^{\mathrm{refl}}'],
13:[r'l=(r-2)/2',r'\sum_{i_1,\ldots,i_l}T_{i_1i_1\cdots i_li_ljj}\ne\sum_{i_1,\ldots,i_l}T_{i_1i_1\cdots i_li_lkk}',r'\text{for all }j\ne k','(14)']}
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert m['D8']['source_kind']=='source_passage'
    assert m['D11']['source_heading'].startswith('Definition 5.1')
    assert m['D12']['source_heading'].startswith('Definition 5.8')
    assert m['D13']['source_kind']=='theorem_excerpt'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in inv['claims']}
    assert s['D13'] in t['5.10']
    assert 'independent' not in t['5.5']+t['5.14']
    assert r'\operatorname{SP}(d)' in t['5.3'] and r'\operatorname{SP}(d)' in t['5.10']
    assert 'If $r=2$' in t['5.3'] and 'some even $r$' in t['5.14']
    assert 'non-zero' not in s['D11'] and 'genericity' not in s['D12']
    a={k:v['statement_original'] for k,v in aux.items()}
    ac={1:[r'h_r(AX)=A\bullet h_r(X)','every $A'],2:[r'\mathcal V(\mathcal I)',r'\operatorname{codim}(\mathcal V)=|\mathcal I|'],3:['Proposition 4.1',r'\Omega_0=\{QA:Q\in\mathcal G_T(\mathcal V)\}'],4:[r'd-1',r'If $r=2$',r'T_{jj}\ne T_{kk}'],5:[r'\langle T,x^{\otimes r}\rangle',r"f_T(x)=x'Tx"],6:['Lemma 5.9',r'f_T(x)=f_T(Dx)',r'\pm1'],7:['central moments, free cumulants and boolean cumulants','extended beyond moments and cumulants'],8:[r'\mathcal V^{\mathrm{refl}}=\mathcal V^{\mathrm{diag}}',r'T_{jj}\ne T_{kk}'],9:['Theorems 5.5 and 5.14',r'AY=BX+\varepsilon','exogenous']}
    for n,parts in ac.items():
        for v in parts:assert v in a['A'+str(n)],(n,v)
    for obj in aux.values():assert set(obj['depends_on'])<=set(m)
    assert set(ambient['statement_local_bindings'])=={'T5.3','T5.5','T5.10','T5.14'}
    assert {x['issue_id'] for x in ambient['source_issues']}=={'registered-title-and-boundary','orthogonal-domain-and-parameter-side','transformations-versus-parameter-set','algebraic-versus-statistical-scope','moment-cumulant-choice','moment-and-generating-function-existence','different-genericity-conditions','even-order-and-normalized-second-order','reflection-pattern-versus-stabilizer','identification-not-estimation-or-independence'}
    refs=ambient['source_claim_references']
    assert sum(x['reference_kind']=='definition_reference' for x in refs)==3
    assert sum(x['reference_kind']=='assumption_reference' for x in refs)==1
    assert sum(x['reference_kind']=='proof_only' for x in refs)==4
if __name__=='__main__':main()
