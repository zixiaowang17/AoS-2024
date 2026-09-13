"""Verify frozen source-reviewed statements and independently reconstruct local theorem reach."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': 'e98b076b582e02e1a4b846714fe0d6b28691695b21a5611fdfaf660d3cfd569b', 'source-passages.json': '5bf0574f9c9bc7be4358e395fe71bac0c1afeb80218c3094e02ef1093c99d80a', 'interface-extraction.json': '6164032f175f8807db7f0eb307848c83647f0d5f74726e0c993bf4d729559b5d', 'ambient-prerequisites.json': 'f8d5fb01acf4d49d43818ffffdf7d56d2c3c86fd8faedddc74bf9ac032649a24', 'unfinalized-census.json': 'fd383b1a3513e03da8e90e30bfcd8f8730a517086e1a5397d8b23ec65e0bc63f', 'ranked-interfaces.json': 'b78d554779a65c35d578190997497d68b4da35f2c4de4f4d9f5f1d9c5b5d6e2e'}

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
    1:['known full-dimensional compact convex domain',r'Y_i=f_0(X_i)+\xi_i','i.i.d. errors',r'$N(0,\sigma^2)$','fixed or random'],
    2:[r'\mathcal C(\Omega)','all convex functions'],
    3:[r'\mathcal C_L^B(\Omega)','uniformly Lipschitz','uniformly bounded by $B$'],
    4:[r'\mathcal C_L(\Omega)','no uniform boundedness assumption'],
    5:[r'\mathcal C^B(\Omega)','no Lipschitz assumption'],
    6:['any minimizer',r'\operatorname*{argmin}_{f\in\mathcal F}\sum_{i=1}^n(Y_i-f(X_i))^2'],
    7:[r'r_d\mathfrak B_d\subseteq\Omega\subseteq\mathfrak B_d','positive constant depending on $d$ alone'],
    8:['independent having the uniform distribution'],
    9:[r'\int_\Omega(f-g)^2d\mathbb P'],
    10:['joint distribution of all the observations','true regression function (see (1))'],
    11:[r'\frac1n\sum_{i=1}^n(f(X_i)-g(X_i))^2','(non-random) empirical distribution'],
    12:[r'\mathcal A(\Omega)','all affine functions',r'$\mathfrak L$ is a fixed positive constant'],
    13:[r'\mathcal F^{\mathfrak L}(\Omega)',r'\inf_{g\in\mathcal A(\Omega)}\ell_{\mathbb P_n}(f_0,g)\le\mathfrak L'],
    14:[r'a_i\le v_i^Tx\le b_i','unit vectors','bounded from above by a constant depending on $d$ alone','also assume (3)'],
    15:[r'\mathcal S:=\{(k_1\delta,\ldots,k_d\delta)',r'$n$ denoting the cardinality',r'2\le c_d\delta^{-d}\le n\le C_d\delta^{-d}',r'$\delta\le\kappa_d$'],
    16:['there exist $k$ convex subsets','at most $h$ slabs',r'$F=h$',r'\Omega_1\cap\mathcal S,\ldots,\Omega_k\cap\mathcal S','are disjoint',r'\cup_{i=1}^k(\Omega_i\cap\mathcal S)=\Omega\cap\mathcal S'],
    17:['convex hull of $d+1$ affinely independent points'],
    18:[r'f_0(x):=\|x\|^2',r'$m\le C_dk$',r'(1-C_dk^{-1/d})\Omega',r'\Delta_i\cap\Delta_j','a facet of',r'\sup_{x\in\Omega}|f_0(x)-\tilde f_k(x)|\le C_dk^{-2/d}',r'\mathcal C_{C_d}^{C_d}(\Omega)',r'\Omega=\cup_{i=1}^m\Delta_i'],
    19:['closed balls of radius',r'N(\epsilon,\mathcal F,\ell)'],
    20:['bracketing entropy',r'$L_p$ metric on $\Delta_1\cup\cdots\cup\Delta_k$'],
    21:[r'\mathcal C^\Gamma(\Omega)',r'\int_\Omega|f(x)-\tilde f(x)|^pdx\le t^p'],
    22:[r'$1\le p<\infty$',r'\left(\frac1n\sum_{s\in\Omega\cap\mathcal S}|f(s)|^p\right)^{1/p}',r'N(\epsilon,\mathcal F,\ell_{\mathcal S}(\cdot,\Omega,p))'],
    23:[r'\mathbb E\sup_{g\in\mathcal F:\ell_{\mathbb P_n}(f,g)\le t}',r'\xi_i(g(X_i)-f(X_i))-\frac{t^2}2'],
    24:[r'\operatorname*{argmax}_{t\ge0}H_f(t,\mathcal F)']}
    assert set(checks)==set(range(1,25))
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    for n in [7,14,15]:assert m['D'+str(n)]['source_kind']=='condition'
    assert m['D8']['source_kind']=='assumption'
    assert m['D18']['source_kind']=='source_passage' and m['D18']['source_heading'].startswith('Lemma 3.2')
    for n in [21,23,24]:assert m['D'+str(n)]['source_kind']=='theorem_excerpt'
    assert r'\ell_{\mathbb P_n}^2(f_0,g)\le' not in s['D13']
    assert 'Lemma 3.2' not in t['3.1'] and 'Lemma 3.2' in t['3.6']
    assert 'Gaussian' not in t['4.11'] and 'satisfying (3)' not in t['4.5']
    assert 'closed' not in t['4.1'] and r'\log\frac\Gamma\epsilon' in t['4.5']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert 'positive constants not depending on the sample size' in a['A1']
    assert 'These constants never depend on the sample size' in a['A2']
    assert 'number of facets or extreme points' in a['A3']
    assert r'\inf_{\breve f_n}\sup_{f_0\in\mathcal F}' in a['A4']
    assert r'R_n(\breve f_n,\mathcal F)' in a['A5']
    assert r'\underline f(x)\le g(x)\le\bar f(x)' in a['A6']
    assert r'\middle|\,X_1,\ldots,X_n' in a['A7'] and 'not to' in a['A7']
    assert 'same setting as in Subsection 2.2' in a['A8']
    assert r'$p\in[1,\infty)$' in a['A9']
    assert 'volume at most $1$' in a['A10'] and 'density constants' in a['A11']
    assert len(ambient['unresolved_external_prerequisites'])==1
    assert any(i['issue_id']=='bracketing-scale' for i in ambient['source_issues'])
    # Endpoint witness supporting the recorded scope concern, not a proof audit.
    # d=p=1, Gamma=1, t=2, Omega=Delta=[-1,1] contains constants +/-1.
    # Any shared bracket needs L1 width>=4, while epsilon<1. RHS for C=1 tends to0.
    import math
    e=1-1e-8;assert math.log(1/e)**2*(2/e)**0.5<math.log(2)
def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2006.02044v2.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==67
    assert paper['main_text_last_pdf_page']==24 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==8
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent reconstruction from inspected source clauses; no finalizer import.
    raw={1:[],2:[],3:[2],4:[2],5:[2],6:[],7:[],8:[],9:[8],10:[1],11:[],12:[],13:[2,11,12],14:[7],15:[7],16:[2,15],17:[],18:[3,7,17],19:[],20:[],21:[5],22:[15,19],23:[11],24:[23]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={k:ids(v) for k,v in {'3.1':[1,3,4,5,6,7,8,9,10],'3.3':[1,2,6,10,11,13,14,15],'3.4':[1,2,3,6,10,11,14,15],'3.5':[1,2,6,10,11,14,15,16],'3.6':[1,2,6,10,11,14,15,18],'4.1':[6,11,23,24],'4.5':[2,5,17,20,21],'4.11':[2,7,14,15,19,22]}.items()}
    expected_reach={k:ids(v) for k,v in {'3.1':[1,2,3,4,5,6,7,8,9,10],'3.3':[1,2,6,7,10,11,12,13,14,15],'3.4':[1,2,3,6,7,10,11,14,15],'3.5':[1,2,6,7,10,11,14,15,16],'3.6':[1,2,3,6,7,10,11,14,15,17,18],'4.1':[6,11,23,24],'4.5':[2,5,17,20,21],'4.11':[2,7,14,15,19,22]}.items()}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    for n in ['3.1','3.3','3.4','3.5','3.6']:assert not ids([19,20,21,22,23,24])&expected_reach[n]
    assert 'D18' not in expected_reach['3.1'] and 'D18' in expected_reach['3.6']
    assert not ids([1,2,7,8,9,14,15])&expected_reach['4.1']
    assert not ids([1,7,8,9,10,11,14,15,18])&expected_reach['4.5']
    assert not ids([1,6,8,9,10,11,12,13,16,18,20,21,23,24])&expected_reach['4.11']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==11 and len(ambient['source_issues'])==14
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
        assert obj['evidence'] and all(1<=e['page']<=24 for e in obj['evidence'])
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
                assert all(1<=e['page']<=24 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=8,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=8,interfaces=24,source_members=24,direct_theorem_uses=56,related_theorem_connections=64,unranked_auxiliary_passages=11),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings={
    'inventory':'Eight original main-text Theorems3.1,3.3,3.4,3.5,3.6,4.1(Chatterjee),4.5,4.11 independently enumerated by bold font and visually compared. Section2 Propositions and all Lemmas are excluded as inventory claims. Main text ends24; appendix bodies beginning25 are excluded.',
    'source_passages':'Twenty-four entries preserve original convex regression classes, design/model assumptions, losses, affine-distance class, grid-partition class, referenced Lemma3.2 approximation, covering/bracketing conventions and local objective/radius. Eleven auxiliary passages retain standing constants and proof-only context. Lemma3.2 is a source passage identifying the function in3.6, not an invented definition or theorem.',
    'dependencies':'Independent source-clause graph verifies56 direct uses and64 related-theorem connections. Fixed-design rates inherit2.2 explicitly via3.2. Theorem4.1 keeps its own arbitrary deterministic design and convex class;4.5 and4.11 are deterministic entropy statements. No proof-only Gaussian-supremum or entropy requirements are imposed on the rate theorems. Only3.6 requires the Lemma3.2 function.',
    'source_issues':'Fourteen source notes preserve fraktur notation, model independence and LSE attainment conventions, normalized-body volume error, slab/facet and grid/cell distinctions, affine-distance interpretation, nonunique lemma function, h-uniformity, bracketing-scale endpoint and distinct metrics. Source formulas are not silently repaired.',
    'names_and_highlights':'All24 entries retain exact author keywords, source headings/kinds and matching selectors. All64 connections have a checked paper-local path and a source-specific explanation. Names are natural-language source terms; notation is preserved in statements and selectors.',
    'reproduction':'All six content JSONs reproduce byte for byte in a fresh empty directory. Seven retained scripts support generation and separate inventory/full-source review. Rebuilding is not a new semantic PDF review.',
    'limits':'The census preserves source statements and context rather than certifying theorem truth. The selected function in3.6 is identified only by the main-text existential lemma; its appendix construction remains unresolved and outside scope. Potential source defects are recorded separately.'}
    reviewed_pages=[1,2,3,4,6,9,10,11,12,13,14,17,19,20,24]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages))
    evidence=[dict(path=f'evidence/page-{n:02}.png',page=n) for n in reviewed_pages]+[dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=67,main_text_last_pdf_page=24,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-font enumeration across all24 main-text pages and visual comparison of eight complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv2006.02044v2 stamped3Sep2024,67pages, pinned bySHA256; not silently exchanged for the published article.','Main text ends24 after Discussion, Acknowledgments and Funding. Appendix A starts25 and all appendix bodies are excluded.','Source review does not certify proofs or resolve missing attainment, uniformity, scale and appendix-only selection conventions.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=67,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
