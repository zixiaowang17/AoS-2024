"""Verify frozen source-reviewed content and independently reconstructed dependency scopes."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': '87b508b19af4bec9ed1d10ffbc2602626b4f40729ab55eec20cbaa4292f949ba', 'source-passages.json': '9d0f0f8b8b077e683e8411450170b596a7bd15412342793d149b30d914a38243', 'interface-extraction.json': '4afd4523ef30c088957c27625754bdc77ed64f2c1263e621878a9bd535b54fec', 'ambient-prerequisites.json': 'b3b335d19fb588f7e0ccf1893e63cc89fa042ef2868cb63c9ac680fa04c4d24d', 'unfinalized-census.json': 'b7fb8442e122d378e46f41a12355012892aeda3abd1a4d45b6b6b47d60bc6a56', 'ranked-interfaces.json': '12925c0940e417db9e0dc37d15740840ec835d8f156df3ba66a242bd94b4ac8f'}
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
    assert registered['version']=='2305.16539v4.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2305.16539'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==47
    assert paper['main_text_last_pdf_page']==29 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==11
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Reconstructed from original definitions and theorem clauses; no builder graph imported.
    raw={1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[5],10:[],11:[],12:[],13:[12],14:[1,2],15:[5,8,13],16:[13],17:[7,8],18:[5,13],19:[],20:[7,8,13,17],21:[20],22:[],23:[2,4]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'3.1':ids([1,2,3,4,11]),'3.4':ids([2,3,4,11]),'4.2':ids([10,11,12,14]),'4.4':ids([5,6,8,9,13,15,16,17]),'4.7':ids([5,8,9,11,12,13,15,16,17,18]),'4.9':ids([4,12,19]),'5.3':ids([5,9,11,12,15,16,20,21]),'5.5':ids([11,12,16,21]),'6.1':ids([1,2,3,4,11]),'6.2':ids([2,3,4,11]),'6.7':ids([2,4,22,23])}
    expected_reach={'3.1':ids([1,2,3,4,11]),'3.4':ids([2,3,4,11]),'4.2':ids([1,2,10,11,12,14]),'4.4':ids([5,6,7,8,9,12,13,15,16,17]),'4.7':ids([5,7,8,9,11,12,13,15,16,17,18]),'4.9':ids([4,12,19]),'5.3':ids([5,7,8,9,11,12,13,15,16,17,20,21]),'5.5':ids([7,8,11,12,13,16,17,20,21]),'6.1':ids([1,2,3,4,11]),'6.2':ids([2,3,4,11]),'6.7':ids([2,4,22,23])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([1,2,3,11,13,14])&expected_reach['4.9']
    assert not ids([1,11,12,13])&expected_reach['6.7']
    assert not ids([12,13])&(expected_reach['3.1']|expected_reach['3.4'])
    assert not ids([1,2,5,9,14,15,18])&expected_reach['5.5']
    assert 'D11' not in expected_reach['4.4']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==14 and len(ambient['source_issues'])==14
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
    counts=dict(theorems=11,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=11,interfaces=23,source_members=23,direct_theorem_uses=59,related_theorem_connections=73,unranked_auxiliary_passages=14)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Eleven complete main-text Theorems in source order: 3.1,3.4,4.2,4.4,4.7,4.9,5.3,5.5,6.1,6.2,6.7. All equivalence clauses and exceptions retained; T6.2 spans pages 24–25. Heading enumeration excludes cited external theorems, proofs, Lemmas, Propositions, Corollaries and Conjectures.',
      source_passages='Twenty-three source entries and fourteen supporting passages preserve original p/e-variable definitions, JA, AC, convex and setwise orders, density-ratio law, optimization domains, split measures, SHINE and uniform-power separation. Assumptions and theorem excerpts retain their actual source kinds.',
      dependencies='Independent reconstruction confirms 59 direct uses and 73 related connections. T4.9 has no JA or e-variable premise; T6.7 has common domination and no pivotality. T5.5 inherits the convergent SHINE conditions without requiring a global maximum or importing the e-variable optimization domain.',
      scope='Full-theorem relationships record use in at least one clause, not a conjunction of all clause assumptions. T4.9 adds AC only in its two-observation refinement; T5.3 adds N for maximal convergence; T6.1 and T6.2 remove JA in their specified equivalences. T5.5 keeps possibly different moment indices j and j-prime.',
      source_issues='Fourteen explicit source issues retain zero-mass and atomic split conventions, scalar/vector and reciprocal distinctions, maximal versus maximum, implicit density/log domains, the contextual N reading in T5.5, and the infinite-hull uniform-separation limitation. Statements are transcribed, not repaired or proof-certified.',
      closure_formula='Visual crop of T6.7 confirms two inner closed operators and an outer closure of their sum in the first condition. The tight-Q clause instead asserts disjointness of the individually closed sets. Positive infimum log e-power is kept distinct from pointwise positivity.',
      names_and_highlights='Every source entry has literal natural-language naming evidence, original source identity and literal highlight selectors. All 73 theorem connections have source-specific explanations and checked same-paper paths.',
      reproduction='All six content JSON artifacts reproduce byte for byte with the saved per-paper scripts. Frozen hashes, independent heading enumeration, formula checks, graph reconstruction and schema validation pass.')
    reviewed_pages=[2,3,5,6,9,10,11,12,13,14,15,20,22,24,25,29]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=['evidence/theorem-6-7-crop.png']))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.extend([dict(path='evidence/theorem-6-7-crop.png',page=25),dict(path='evidence/manual-findings.json')])
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=47,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent small-cap heading enumeration and visual comparison of all eleven complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark','Conjecture'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2305.16539v4 dated 1 Dec 2024, pinned by SHA-256. No substitution with another paper version.','Appendix bodies excluded. Total variation, tightness, martingale and Radon–Nikodym foundations remain stated ambient prerequisites.','Source and schema validation do not certify proofs or resolve the explicitly recorded source ambiguities.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=47,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))

def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:['same distribution under all'],
2:[r'\mathbb E^P[X]\le1',r'\mathbb E^P[X]=1',r'\mathbb E^Q[X]>1',r'\mathbb E^Q[\log X]>0','for each'],
3:[r'P(X\le\alpha)\le\alpha',r'P(X\le\alpha)=\alpha',r'Q(X\le\alpha)\ge\alpha','with strict inequality for some','by truncation'],
4:['finite set','usual sense of convex hull and span'],
5:[r'\int\phi\,d\mu\le\int\phi\,d\nu','every convex function'],
6:[r'\mu(A)\le\nu(A)','every Borel set'],
7:[r'\int|x|\mu(dx)<\infty',r'\int_{\mathbb R^d}x\mu(dx)/\mu(\mathbb R^d)'],
8:[r'\mathcal I_d^+',r'x_1=\cdots=x_d\ge0',r'\mathbb R_+\mathbf1_d'],
9:['(Pareto) maximal element','there exists no',r'\nu\ne\mu','maximum element',r'for each $\nu\in\mathcal N$'],
10:[r'\boldsymbol\mu(\mathcal X)=\boldsymbol\nu(\mathcal Y)',r'\int_{\mathcal X}\kappa(x;\cdot)\boldsymbol\mu(dx)=\boldsymbol\nu(\cdot)',r'\boldsymbol\mu\circ T^{-1}=\boldsymbol\nu'],
11:[r'\mu\gg\sum_{i=1}^d\mu_i','atomless and independent of',r'(d\mu_1/d\mu,\ldots,d\mu_d/d\mu)'],
12:[r'P_1,\ldots,P_L\ll Q'],
13:[r'\frac{dP_1}{dQ}',r'\frac{dP_L}{dQ}',r'\bigg|_Q','with mean'],
14:[r'\mathbb E^Q[\log X]','pivotal exact e-variable'],
15:[r'\mathcal I_L^+','smaller than',r'\mu\in\mathcal M_\gamma'],
16:['does not give positive mass to any hyperplane',r'\gamma(\partial\mathbb H)=0'],
17:[r'\mathcal I_L^+\not\subseteq\mathbb H_x',r'-\mathbf1\in\mathbb H_x','closed complement',r'\mu_{\mathbb H_x^c}:=\gamma-\mu_x','barycenters','if (N) holds','unique measure'],
18:[r'\mathbb E^G\left[-\log\frac{dF}{dG}\right]',r'\bigg|_G\preceq_{\mathrm{cx}}',r'\bigg|_Q'],
19:[r'\mathcal P^n:=\{P_1^n,\ldots,P_L^n\}',r'\mathcal Q^n:=\{Q^n\}'],
20:[r'\mu^{(0)}=\delta_{\mathbf1}',r'\mu_1^{(0)}=\gamma','Proposition 4.3','unique decomposition',r'\operatorname{bary}(\mu_k^{(s+1)})',r'\sum_{k=1}^{2^{s+1}}'],
21:['first coordinate',r'X_0=1',r'j=2k-1,2k',r'\frac{\mu_j^{(s+1)}(\mathbb R^L)}{\mu_{2k-1}^{(s+1)}(\mathbb R^L)+\mu_{2k}^{(s+1)}(\mathbb R^L)}','nonnegative martingale',r'X_\infty\mathbf1'],
22:[r'R\in\Pi(\mathcal X)',r'P\ll R',r'Q\ll R'],
23:[r'\inf_{Q\in\mathcal Q}\mathbb E^Q[\log X]>0',r'\overline{\overline{\operatorname{Span}}\mathcal P+\overline{\operatorname{Conv}}\mathcal Q}',r'\overline{\operatorname{Span}}\mathcal P\cap\overline{\operatorname{Conv}}\mathcal Q=\varnothing','total variation distance','tight']}
    for n,parts in checks.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    assert all(m['D'+str(n)]['source_kind']=='assumption' for n in [12,16])
    assert all(m['D'+str(n)]['source_kind']=='theorem_excerpt' for n in [22,23])
    assert m['D17']['source_kind']=='source_passage' and m['D11']['source_heading'].startswith('Definition 2.2')
    assert '(JA)' not in s['D22']+s['D23'] and 'pivotal' not in s['D23']
    assert 'Lemma 2.1' not in s['D21']
    a={k:v['statement_original'] for k,v in aux.items()}
    for n,parts in {1:['Polish space','disjoint subsets'],2:['jointly atomless','unless otherwise stated'],3:[r'\mu(A)=1','does not imply'],4:[r'P\ll Q\ll P'],5:[r'\mathbb E[Y\mid X]=X'],6:['monotone selection'],7:[r'L=2'],8:['dimension of the null'],9:['not always obtain an exactly maximal element'],10:['not necessarily unique','we do not discuss'],11:[r'(X(x))^{-1}\times\mathbf1'],12:['reference measure'],13:[r'\inf_{Q\in\mathcal Q}',r'\varepsilon+\sup_{P\in\mathcal P}'],14:['stronger assumption','for all']}.items():
        for part in parts:assert part in a['A'+str(n)],(n,part)
    assert not aux['A4']['depends_on'] and not aux['A5']['depends_on']
    assert set(ambient['statement_local_bindings'])=={'T'+n for n in ['3.1','3.4','4.2','4.4','4.7','4.9','5.3','5.5','6.1','6.2','6.7']}
    assert {x['issue_id'] for x in ambient['source_issues']}=={'exactness-pivotality-power','ja-exceptions','ac-direction-and-refinement','maximal-versus-maximum','closed-complement','split-measure-uniqueness','zero-mass-barycenters','scalar-vector-coupling','shine-rate-assumption-scope','distinct-moment-indices','reciprocal-and-log-domain','infinite-hull-separation','nested-total-variation-closures','products-and-dimensions'}
    refs=ambient['source_claim_references'];assert sum(x['reference_kind']=='assumption_reference' for x in refs)==1
    assert sum(x['reference_kind']=='proof_only' for x in refs)==2
    for o in aux.values():assert set(o['depends_on'])<=set(m)
if __name__=='__main__':main()
