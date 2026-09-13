"""Verify frozen source-reviewed content and independently reconstruct theorem reach."""
import datetime,hashlib,json,math,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '88f8ab025c051e462d1261eb7ea3d206d4b1b0142d492ba641c8df5a28ff9f8d', 'source-passages.json': '24fe0613dfa3c19f1094dd112b95596cfcd5d35318c86b18c330816061bd8228', 'interface-extraction.json': 'fa1be3bb3480817104f0b7dfaecaa52c80ec5825d64f0b8cbbe439d437f75b90', 'ambient-prerequisites.json': 'e96fb3377573d5ca1de69fce580556a315e5971dc238452ee70ddda0e24a7aea', 'unfinalized-census.json': '808774c118bd05b26ccad2602bd27259f66042d1f1847e72ef3f732866c7f846', 'ranked-interfaces.json': 'bbbeedff94348c1bf5dfea87b81f2f7dad6f9e530d9765ca46608b50d6dd1b74'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:['totally ordered infinite set',r'L_t,U_t>0','typically unknown',r'\forall t\in\mathcal T',r'L_t^*/L_t\xrightarrow{\mathrm{a.s.}}1',r'U_t^*/U_t\xrightarrow{\mathrm{a.s.}}1'],
2:['potentially enriched probability space',r'Z_{t_0}\equiv0',r'(\widehat\theta_t-\theta_t)-Z_t=O(r_t)'],
3:[r'\widehat L_t>0',r'\widehat U_t>0',r'\mathbb P\left(\forall t\in\mathcal T,\ Z_t\in[-\widehat L_t,\widehat U_t]\right)\ge1-\alpha'],
4:[r'r_t=o(\widehat L_t\wedge\widehat U_t)','almost surely'],
5:[r'L_t/\widehat L_t\xrightarrow{\mathrm{a.s.}}1',r'U_t/\widehat U_t\xrightarrow{\mathrm{a.s.}}1'],
6:[r'\mu_t:=\mathbb E(Y_t\mid Y_1^{t-1})',r'\sigma_t^2:=\operatorname{var}(Y_t\mid Y_1^{t-1})',r'\widetilde\sigma_t^2:=\frac1t\sum_{i=1}^t\sigma_i^2','superlinearly'],
7:[r'V_t:=\sum_{i=1}^t\sigma_i^2\to\infty','almost surely'],
8:[r'0<\kappa<1',r'(Y_t-\mu_t)^2>V_t^\kappa',r'\mid Y_1^{t-1}\right]}{V_t^\kappa}<\infty'],
9:[r'0<\eta<1',r'\widehat\sigma_t^2-\widetilde\sigma_t^2',r'\frac{(t\widetilde\sigma_t^2)^\eta}{t}'],
10:[r'\alpha\in(0,1)',r'\liminf_{m\to\infty}\mathbb P(\forall t\ge m,\ \mu_t\in C_t(m))\ge1-\alpha','sharp if the above inequality holds with equality'],
11:[r'\widetilde C_t(m)',r'\frac{2(t\widehat\sigma_t^2\rho_m^2+1)}{t^2\rho_m^2}',r'\frac{\sqrt{t\widehat\sigma_t^2\rho_m^2+1}}\alpha'],
12:[r'\rho_m:=\rho(\widehat\sigma_m^2m\log(m\vee e))',r'-2\log\alpha+\log(-2\log\alpha)+1',r'\widehat\sigma_m^2m\log(m\vee e)'],
13:['independent random variables','Condition L-1',r'\mathbb E|Y_i-\mu_i|^{2+\delta}/\sqrt{V_i}^{2+\delta}',r'\mathbb E|Y_i^2-\mathbb EY_i^2|^{1+\beta}',r'V_i^{1+\beta}',r'\widetilde\mu_t^2=o(V_t)',r'\frac1t\sum_{i=1}^t(\mu_i-\widetilde\mu_t)^2=o(\widetilde\sigma_t^2)',r'\beta\in(0,1)'],
14:[r'\psi:=\mathbb E(Y^1-Y^0)','counterfactual outcome',r'a\in\{0,1\}'],
15:['consistency, positivity, and exchangeability','Kennedy [24, §2.2]'],
16:[r'\mu^a','conditional mean function'],
17:[r'\pi(x):=\mathbb P(A=1\mid X=x)','known propensity score'],
18:[r'f(x,a,y):=\{\mu^1(x)-\mu^0(x)\}',r'\frac a{\pi(x)}-\frac{1-a}{1-\pi(x)}',r'\{y-\mu^a(x)\}'],
19:['not re-randomized','remain in that split',r'T:=|\mathcal D_\infty^{\mathrm{eval}}|',r"T':=|\mathcal D_\infty^{\mathrm{trn}}|=t-T"],
20:[r"\widehat\eta_{T'}\equiv(\widehat\mu_{T'}^1,\widehat\mu_{T'}^0,\overline\pi_{T'})",'or the propensity score itself','built solely from'],
21:[r"\sum_{i=1}^T\widehat f_{T'}(Z_i^{\mathrm{eval}})",r"\sum_{i=1}^{T'}\widehat f_T(Z_i^{\mathrm{trn}})",r'\widehat f_T$ solely from $\mathcal D_\infty^{\mathrm{eval}}'],
22:[r"\frac{\widehat{\operatorname{var}}_T(\widehat f_{T'})+\widehat{\operatorname{var}}_{T'}(\widehat f_T)}2",'sample variance of the pseudo-outcomes','deliberately omit the subscript'],
23:['replaced by their true values','possibly misspecified','need not coincide',r"\widehat f_{T'}$ or $\widehat f_T"],
24:[r'\overline f(x,a,y):=\{\overline\mu^1(x)-\overline\mu^0(x)\}',r'\frac a{\pi(x)}-\frac{1-a}{1-\pi(x)}',r'\{y-\overline\mu^a(x)\}'],
25:[r'\psi_t:=\mathbb E\{Y_t^1-Y_t^0\}',r'\mathbb E(Y_t\mid X_t,A_t=1)-\mathbb E(Y_t\mid X_t,A_t=0)',r'\widetilde\psi_t:=\frac1t\sum_{i=1}^t\psi_i'],
26:[r'\sup_{1\le i<\infty}',r'\widehat\mu_t^a(X_i)-\overline\mu^a(X_i)',r'a\in\{0,1\}'],
27:[r'\frac1t\sum_{i=1}^t',r'\|\widehat\pi_t(X_i)-\pi(X_i)\|_{L_2(\mathbb P)}\sum_{a=0}^1',r'\widehat\mu_t^a(X_i)-\mu^a(X_i)',r'o\left(\sqrt{\frac{\log t}t}\right)'],
28:[r'\pi(X)\in[\delta,1-\delta]','almost surely',r'\delta>0']}
    assert set(checks)=={int(lid[1:]) for lid in m}
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert s['D28'] in t['3.1']
    assert r'-\psi' not in s['D18']+s['D24']
    assert 'hat' not in s['D24']
    assert m['D13']['source_kind']=='assumption' and m['D28']['source_kind']=='theorem_excerpt'
    for n in [2,3,4,5,7,8,9,26,27]:assert m['D'+str(n)]['source_kind']=='condition'
    for n in [26,27]:assert r'$\widetilde{\mathrm{ATE}}$-'+str(n-25) in m['D'+str(n)]['source_heading']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert r'\widehat\sigma_t^2/\widetilde\sigma_t^2' in a['A1'] and 'constructed using' in a['A1']
    assert r'o_{\mathrm{a.s.}}' in a['A2'] and r'\mathbb R^{\ge0}' in a['A3']
    assert r'\mathbb E\{\mathbb E(Y\mid X,A=1)-\mathbb E(Y\mid X,A=0)\}' in a['A4']
    assert 'i.i.d.' in a['A5'] and r'\delta>0' in a['A6']
    assert 'Assumptions L-1, L-2, and L-3' in a['A7'] and 'sample variance' in a['A8']
    assert a['A9'].strip('$') in t['3.3'] and 'uncentered' in a['A10']
    assert 'actually does require' in a['A11'] and 'sample-split version' in a['A11']
    assert a['A12'] in t['2.2']
    assert all(set(x['depends_on'])<=set(m) for x in aux.values())
    # Concrete arithmetic check of the recorded source-domain issue; no repair is applied.
    alpha=.99;assert -2*math.log(alpha)+math.log(-2*math.log(alpha))+1<0
    assert set(ambient['statement_local_bindings'])=={'T'+n for n in ['2.2','2.4','2.8','3.1','3.2','3.3']}
    refs=ambient['source_claim_references'];assert sum(x['reference_kind']=='assumption_reference' for x in refs)==3
    assert sum(x['reference_kind']=='proof_only' for x in refs)==3
    assert sum(x['reference_kind']=='excluded_alternative' for x in refs)==1

def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2103.06476v9.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2103.06476'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==69
    assert paper['main_text_last_pdf_page']==28 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==6
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent source-clause reconstruction, not imported from finalizer.
    raw={1:[],2:[],3:[2],4:[2,3],5:[3],6:[],7:[6],8:[6,7],9:[6],10:[],11:[12],12:[],13:[6,7],14:[],15:[],16:[],17:[],18:[16,17],19:[],20:[18,19],21:[19,20],22:[19,20],23:[16,17,20,21,24],24:[16,17],25:[15],26:[16],27:[16,17],28:[17]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={k:ids(v) for k,v in {'2.2':[1],'2.4':[1,2,3,4,5],'2.8':[1,6,7,8,9,10,11],'3.1':[1,14,15,16,17,20,21,22,23,24,28],'3.2':[1,14,15,16,17,18,20,21,22,28],'3.3':[1,13,21,24,25,26,27]}.items()}
    expected_reach={k:ids(v) for k,v in {'2.2':[1],'2.4':[1,2,3,4,5],'2.8':[1,6,7,8,9,10,11,12],'3.1':[1,14,15,16,17,18,19,20,21,22,23,24,28],'3.2':[1,14,15,16,17,18,19,20,21,22,28],'3.3':[1,6,7,13,15,16,17,18,19,20,21,24,25,26,27]}.items()}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert expected_reach['2.2']==ids([1])
    assert not ids([6,7,8,9,10,11,12,13]) & expected_reach['2.4']
    assert 'D13' not in expected_reach['2.8']
    assert not ids([23,24]) & expected_reach['3.2']
    assert not ids([8,9,10,11,12,22,23,28]) & expected_reach['3.3']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==12 and len(ambient['source_issues'])==14
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
        assert obj['evidence'] and all(1<=e['page']<=28 for e in obj['evidence'])
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
                assert all(1<=e['page']<=28 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=6,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=6,interfaces=28,source_members=28,direct_theorem_uses=41,related_theorem_connections=53,unranked_auxiliary_passages=12),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(inventory='Exactly six complete actual main-text Theorems2.2,2.4,2.8,3.1,3.2,3.3, independently enumerated by bold headings and compared visually. Stale outline theorem labels do not promote Proposition2.5 or Corollary2.6. Main text ends onpage28 before references; appendix bodies are excluded.',source_passages='Twenty-eight source entries and twelve auxiliary passages preserve AsympCS and coverage definitions, four coupling conditions, conditional variance and moment conditions, later-start tuning/boundary, every imported Corollary2.6 hypothesis, causal estimands, identification assumptions, permanent sample splitting, nuisance fitting, cross-fit estimator/variance and moving-effect conditions.',dependencies='Independent reconstruction verifies41 direct uses and53 related connections. T2.2 does not inherit Gaussian/sub-Gaussian or higher-moment proof premises. Abstract T2.4 remains independent of specific Gaussian boundaries. T2.8 uses conditional-moment conditions and start-specific tuning, not independent-data Corollary2.6.',causal_scope='T3.2 preserves common identification/overlap/cross-fitting but changes known propensity and replaces misspecified limits with consistent nuisance functions and the efficientf. T3.3 retains every Corollary2.6 assumption under substitution, all-index uniformity inATE1 and average products inATE2, and full cross-fitting. Its bar-f variance notation remains unresolved rather than equated to fitted variance26.',source_issues='Fourteen notes preserve zero-width/degenerate variance, tuning square-root domain, the superlinearly wording, almost-sure rates, estimated-propensity denominators, named-only causal assumptions, uncentered influence functions, fold-size/variance conventions, oracle variance notation and time-varying function conventions. Source gaps are not silently repaired.',names_and_highlights='Every source entry has literal natural-language author terminology, original source kind and meaningful highlights. All53 related-theorem links have valid local paths and source-specific explanations. No mathlib or proof-correctness verdict is supplied.',reproduction='All six contentJSON files reproduce byte for byte in a fresh empty directory. Seven retained scripts cover inventory, extraction, context, finalization, rebuilding and independent review. Rebuilding is not represented as a new semantic source review.')
    reviewed_pages=[1,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,28]
    crops=[dict(path='evidence/page-'+str(n).zfill(2)+'-theorem-crop.jpg',page=n) for n in [8,18,21]]+[dict(path='evidence/page-'+str(n).zfill(2)+'-label-crop.jpg',page=n) for n in [20,21]]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=crops))
    evidence=[dict(path='evidence/page-'+str(n).zfill(2)+'.jpg',page=n) for n in reviewed_pages]+crops+[dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=69,main_text_last_pdf_page=28,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-heading enumeration and visual comparison of all six full statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv2103.06476v9 marked14Mar2024,69PDFpages, pinned bySHA256; not silently exchanged for the published version.','Main text ends onpage28 at acknowledgements before References y638.557; evidence clipped632. All appendix bodies are excluded.','Source validation preserves statements, references and ambiguities; it does not prove the claims, resolve undefined variance substitutions or reconstruct unprinted causal predicates.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=69,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
