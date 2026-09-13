"""Verify frozen source-reviewed content and independently reconstruct dependency reach."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '51f4f2517fa5f133cc41fa353e85ee5b78d07fdf9605bdb9691f6f77ebfef651', 'source-passages.json': '838473c7bbf5414abdea00cc01455ab914452f67858a7152e30878d1733239b2', 'interface-extraction.json': '0250a20130f89b459db4a4e2cfa9bbe1a4d22100fb56b8a210e8d6e04c40eb04', 'ambient-prerequisites.json': 'a4a14c108a3eaa9ef6471cb4b63ea3498884916c08582c0c54a0f529b788f0eb', 'unfinalized-census.json': 'e6ea6aaa24fc7bdea4286fb31f0b3816f0a2b83cfb1d12b9c5f67a0e95c66e77', 'ranked-interfaces.json': '18284f86bbc8ad9d1dd7a64cafa274e244e3b9c383b34d063830a97bb30ce9c3'}
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
    assert registered['version']=='2302.06025v3.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2302.06025'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==55
    assert paper['main_text_last_pdf_page']==29 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    assert len(inv['claims'])==len(d['claims'])==14
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent clause-by-clause reconstruction; no importing the finalizer's graph.
    raw={1:[],2:[],3:[1,2],4:[1],5:[1,2,4],6:[3],7:[3],8:[],9:[],10:[],11:[1,2],12:[2,11],13:[1,2,12],14:[2],15:[2],16:[1,14,15],17:[1,2,18,19,20],18:[1,2],19:[1,2],20:[2],21:[1,2,9],22:[1],23:[],24:[1,2,4],25:[]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'1':ids([1,2,6,8,17]),'2':ids([1,2,6,8]),'3':ids([1,2,7,8]),'4':ids([1,2,8,10,13]),'5':ids([2,8,10,14,15,16]),'6':ids([1,2,5,8,9,21]),'7':ids([1,2,3,5,9,10]),'8':ids([1,2,8]),'9':ids([1,2,17]),'10':ids([1,2,20]),'11':ids([1,2,8,22]),'12':ids([1,2,8,23]),'13':ids([1,2,24,25]),'14':ids([6])}
    expected_reach={'1':ids([1,2,3,6,8,17,18,19,20]),'2':ids([1,2,3,6,8]),'3':ids([1,2,3,7,8]),'4':ids([1,2,8,10,11,12,13]),'5':ids([1,2,8,10,14,15,16]),'6':ids([1,2,4,5,8,9,21]),'7':ids([1,2,3,4,5,9,10]),'8':ids([1,2,8]),'9':ids([1,2,17,18,19,20]),'10':ids([1,2,20]),'11':ids([1,2,8,22]),'12':ids([1,2,8,23]),'13':ids([1,2,4,24,25]),'14':ids([1,2,3,6])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([17,18,19,21]) & expected_reach['10']
    assert 'D8' not in expected_reach['7'] and 'D8' not in expected_reach['13']
    assert 'D5' not in expected_reach['13'] and 'D25' in direct['13']
    assert not ids([3,5,6,7,22,23,24]) & expected_reach['8']
    assert 'D20' in local['D17'] and 'D17' not in local['D20']
    assert 'D22' in direct['11'] and 'D23' in direct['12']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==6 and len(ambient['source_issues'])==16
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
        assert obj['evidence'] and all(1<=e['page']<=29 for e in obj['evidence'])
        for e in obj['evidence']:
            if e['page']==29:assert e.get('before_main_text_end') is True
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
                assert all(1<=e['page']<=29 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=14,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=14,interfaces=25,source_members=25,direct_theorem_uses=58,related_theorem_connections=76,unranked_auxiliary_passages=6),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Exactly fourteen original main-text Theorems1–14, independently enumerated by bold headings and visually compared. Weaker-version Theorems1/2 remain separate. All branches, integrals, recursion, query-cost formulas, quantifiers and parameter domains are retained. The final theorem precedes the appendix boundary on page29.',
      source_passages='Twenty-five entries preserve the sequential ridge experiment, complete Definitions1–4, Assumptions1–3, least-squares/confidence/Eluder-UCB definitions, online/offline oracle models and propriety conventions, complete Algorithms1–4, Theorem9 parameter block, nonadaptive and finite-action domains, unit-ball parameter variant and the isolated monotonicity item. Six auxiliary passages preserve source conventions and limitations.',
      dependencies='Independent reconstruction verifies58 direct uses and76 related connections. Conditional Assumption1 use in Theorem6 is restricted to regret; Theorem7 does not import it. Theorem13 imports only its monotonicity item and the ball-parameter regret variant. Theorem10 imports Theorem9 parameters but not Algorithm1 or knowledge of f. Oracle alternatives are not combined as simultaneous guarantees.',
      scope='Bayes path bounds, nonadaptive Bayes risk, finite-action minimax existence and sphere/ball minimax regret remain distinct. Algorithm1 depends on the numerical block of Theorem9, avoiding a conclusion cycle. Chi-square informativity, Brascamp–Lieb and infinite-armed-bandit constructions remain proof context.',
      source_issues='Sixteen explicit notes preserve even-link signed identifiability, the Definition4 accuracy-domain extension, derivative and finite-difference distinctions, oracle conventions, local slope domains, algorithm initialization/integer-budget issues, sequence and radius endpoints, comparator notation and a CDF/inverse typo. No source expression is silently repaired.',
      appendix_limits='Theorem9’s c(.) points to appendix-only Lemma6 and remains unresolved. Even-link algorithm modifications and the detailed unknown-link algorithm are also outside scope. Main-text original statements and references are preserved; source validation does not certify unavailable definitions or prove the theorems.',
      names_and_highlights='All25 entries have original natural-language source terms, literal meaningful selectors and evidence. Numbered definitions/assumptions retain labels, algorithms are source passages, and the numerical block is a theorem excerpt. Every related theorem has a checked local path and source-specific explanation.',
      reproduction='All six contentJSON files reproduce byte for byte in a fresh empty directory. Seven retained scripts cover inventory extraction/review, source passages, context, finalization, rebuilding and frozen full-source checks. Rebuilding reproduces saved decisions rather than performing a new semantic source review.')
    reviewed_pages=[1,3,4,5,6,7,8,9,10,11,12,15,20,21,22,23,24,25,26,27,28,29]
    crops=[dict(path='evidence/page-24-test-crop.jpg',page=24,location='Algorithm3 paired sample means and joint feasibility test')]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=crops))
    evidence=[dict(path='evidence/page-'+str(n).zfill(2)+'.jpg',page=n,**({'before_main_text_end':True} if n==29 else {})) for n in reviewed_pages]+crops+[dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=55,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent SFBX heading enumeration and visual comparison of all fourteen complete theorem statements.',excluded_result_types=['Lemma','Corollary','Example','Definition','Assumption'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2302.06025v3, marked10Jan2024 and dated11Jan2024;55PDFpages, pinned bySHA256.','Main text ends onPDFpage29, clipped at y648 before AppendixA at y654.115. All appendix bodies are excluded.','Validation checks source fidelity, dependency scope and reproducibility, not theorem correctness. Appendix-only c(.) and algorithm details remain unresolved, and apparent source errors are preserved explicitly.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=55,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'\mathcal H_{t-1}=\{(a_s,r_s)\}_{s\le t-1}',r'r_t=f_{\theta^\star}(a_t)+z_t','standard normal distribution','fixed across time',r'\widehat\theta_T=\widehat\theta_T(\mathcal H_T)'],
2:[r'f_{\theta^\star}(a)=f(\langle\theta^\star,a\rangle)',r'f:[-1,1]\to[-1,1]','known link function'],
3:[r'\varepsilon\in(0,1/2]',r'\inf_{\widehat\theta_T\in\mathbb S^{d-1}}\sup_{\theta^\star\in\mathbb S^{d-1}}',r'1-\langle\widehat\theta_T,\theta^\star\rangle','all possible actions','all possible estimators'],
4:[r'\max_{a^\star\in\mathcal A}f_{\theta^\star}(a)',r'\sum_{t=1}^T f_{\theta^\star}(a_t)'],
5:[r'\inf_{a^T}\sup_{\theta^\star\in\mathbb S^{d-1}}',r'\max_{a^\star\in\mathcal A}f(\langle\theta^\star,a^\star\rangle)'],
6:[r'T^\star(f,d,1/2)','Definition 1'],7:[r'T^\star(f,d,1-\varepsilon)',r'\varepsilon\mapsto T^\star_{\mathrm{burn\text{-}in}}'],
8:[r'f(0)=0',r'f(1)=1',r'|f|\le1','either (i)','or (ii) $f$ is even'],
9:['differentiable and locally linear',r'[1-\gamma,1]',r"c_f\le\min_{x\in[1-\gamma,1]}f'(x)\le\max_{x\in[1-\gamma,1]}f'(x)\le C_f"],
10:[r'$L$-Lipschitz',r'|f(x)-f(y)|\le L|x-y|'],
11:[r'\widehat\theta_t^{\mathrm{LS}}',r'\sum_{s<t}(r_s-f(\langle\theta,a_s\rangle))^2'],
12:[r'\mathbb C_t=',r'\mathrm{Est}_t\asymp d',r'f(\langle a_s,\widehat\theta_t^{\mathrm{LS}}\rangle)'],
13:[r'\operatorname*{arg\,max}_{a\in\mathcal A}\max_{\theta\in\mathbb C_t}', 'ties','arbitrary manner'],
14:['beginning of time',r'\widehat\theta_s',r'\mathrm{Est}^{\mathrm{On}}_t'],15:['end of time',r'\widehat\theta_t',r'\mathrm{Est}^{\mathrm{Off}}_t'],
16:['instead of observing',r'(a_1,\widehat\theta_1,a_2,\widehat\theta_2,\cdots)','(5) or (6)'],
17:[r'x_0\in(0,1)',r'L\leftarrow2m\log(2m/\delta)/c_0',r'\operatorname{Unif}(V^\perp\cap\mathbb S^{d-1})',r'\delta/L,\kappa_1/4','InitialActionHypTest','GoodActionHypTest',r'a_0\leftarrow\frac1{\sqrt m}\sum_{i=1}^m v_i'],
18:[r'\min_{z\in[1,1+2\kappa_1]}',r'f\left(\frac{z+\kappa_1}{\sqrt d}\right)-f\left(\frac z{\sqrt d}\right)',r'2\log(2/\delta)/\varepsilon^2',r'|\overline r-f(x)|\le\varepsilon'],
19:[r'\kappa_2^\perp:=\sqrt{1-(1-\kappa_2)^2}',r'\kappa_4:=(\kappa_1^{-1}+2)\kappa_2^\perp',r'\min_{z\in[(1-4\kappa_1)y,(1+4\kappa_1)y]}',r'2\log(4/\delta)/\varepsilon^2',r'|\overline r_--f(z-x)|\le\varepsilon',r'|\overline r_+-f(z+x)|\le\varepsilon'],
20:[r'\kappa_1\in(0,(x_0^{-1}-1)/2)',r'c_0=c',r'Lemma 6',r'\{\varepsilon_i\}_{i\ge0}',r'\text{if }1\le i\le d_0',r'\text{if }d_0+1\le i\le m',r'm=\lceil x_0^2d\rceil'],
21:[r'\langle a_0,\theta^\star\rangle\ge1-\gamma',r'\min\{T,d\sqrt T/c_f\}',r'(-1)^{\lceil t/d\rceil}',r'e_{((t-1)\bmod d)+1}',r'\theta\in\mathbb S^{d-1}:\langle\theta,a_0\rangle\ge1-\gamma',r'a_t=\widehat\theta^{\mathrm{LS}}'],
22:['chosen in advance without knowing the history'],23:['finite subset of $\mathbb B^d$',r'|\mathcal A|=K'],24:[r'\theta^\star\in\mathbb S^{d-1}',r'\theta^\star\in\mathbb B^d','different radii'],25:['Monotonicity: either (i)','or (ii) $f$ is even']}
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert set(checks)==set(range(1,26))
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in inv['claims']}
    assert s['D20'] in t['9'] and 'Algorithm 1' not in s['D20']
    assert s['D25'] in s['D8'] and 'Normalized scale' not in s['D25']
    assert [m['D'+str(i)]['source_kind'] for i in [8,9,10,25]]==['assumption']*4
    assert [m['D'+str(i)]['source_kind'] for i in [17,18,19,21]]==['source_passage']*4
    assert m['D20']['source_kind']=='theorem_excerpt'
    assert 'proper' in m['D16']['naming_context'][0]['text'] and r'\widehat\theta_t\in\mathbb S^{d-1}' in m['D16']['naming_context'][0]['text']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert a['A6'] in t['13']
    for v in [r'\widetilde O(b_n)',r'a_n\lesssim b_n',r'\log^c n']:assert v in a['A1'],v
    assert 'Appendix C' in a['A2'] and 'differentiable' in a['A3'] and 'postponed to the appendix' in a['A4']
    assert r'F^{-1}(f(1/\sqrt d))' in a['A5']
    for obj in aux.values():assert set(obj['depends_on'])<=set(m)
    assert set(ambient['statement_local_bindings'])=={'T'+str(i) for i in range(1,15)}
    assert 'regret' in ambient['statement_local_bindings']['T6']['branches']
    assert {x['issue_id'] for x in ambient['source_issues']}=={'registered-source-and-boundary','even-link-signed-identifiability','accuracy-domain-extension','derivative-form-versus-monotonicity','gaussian-noise-and-oracle-information','oracle-quantifiers-and-domains','learning-assumptions-and-constants','algorithm-four-initialization-and-budget','theorem-nine-parameters-and-ranges','appendix-only-constant-and-algorithms','recursion-and-link-domain','bayes-minimax-and-action-space','unit-ball-endpoints-and-scale','soft-order-versus-ordinary-order','regret-notation-binding','unknown-link-cdf-explanation'}
    refs=ambient['source_claim_references']
    assert sum(x['reference_kind']=='unresolved_appendix_reference' for x in refs)==2
    assert sum(x['reference_kind']=='proof_only' for x in refs)==6
    assert any(x['claim_id']==PID+'/T10' and x['reference_kind']=='assumption_reference' for x in refs)
if __name__=='__main__':main()
