"""Validate frozen source-reviewed content independently of the census builder."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '1e35d6f0bc3a58a5c680a1c86f8e5366e5b52bcd023f1de570135e283ce2a21e', 'source-passages.json': 'c4e04fd5752458d4931a6d7cb310b275209d3eadcaee129c4c7eca8f0e5323b4', 'interface-extraction.json': 'ebf6bd5c47ab799e0b278694d2d6550c3a152e748034f2e054432b5fc9bc3809', 'ambient-prerequisites.json': '5f6360181c4adeb668b4e2acead02749d53e2fd6c9e927f72ecf08abc21a707e', 'unfinalized-census.json': 'efdec0ba168ab757c767945521ad3471b5e55338a4bf8d59df3f5ee9f3c4a9ed', 'ranked-interfaces.json': '63963a126f63e1ac843d49cb58d224c0fdd4e97e772545a3a6aebd3547cbbaff'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2301.10600v3.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2301.10600'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert ir['printed_label_check']==[[11,'3.3'],[12,'3.5'],[14,'4.1'],[15,'4.2'],[15,'4.3'],[21,'4.11'],[22,'4.12']]
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==52
    assert paper['main_text_last_pdf_page']==29 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    assert len(inv['claims'])==len(d['claims'])==7
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Reconstructed from the source scopes; no extraction/finalizer graph imported.
    raw={1:[],2:[1],3:[1,2],4:[1,2],5:[],6:[5],7:[],8:[1,2,4],9:[],10:[5],11:[5],12:[5],13:[10],14:[],15:[1,2,4,5,6,13,14]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'3.3':ids([1,3,5,6,7]),'3.5':ids([1,3,5,6]),'4.1':set(),'4.2':ids([1,2,5,8]),'4.3':ids([4,9]),'4.11':ids([1,2,6,10,11,12,13,14]),'4.12':ids([1,2,3,6,10,11,12,15])}
    expected_reach={'3.3':ids([1,2,3,5,6,7]),'3.5':ids([1,2,3,5,6]),'4.1':set(),'4.2':ids([1,2,4,5,8]),'4.3':ids([1,2,4,9]),'4.11':ids([1,2,5,6,10,11,12,13,14]),'4.12':ids([1,2,3,4,5,6,10,11,12,13,14,15])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n]
    assert 'D7' not in expected_reach['3.5'] and 'D5' not in expected_reach['4.3']
    assert not expected_reach['4.1'] and 'D8' not in expected_reach['4.12']
    s={lid:a['statement_original'] for lid,a in m.items()}
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==14 and len(ambient['source_issues'])==8
    source_specific_checks(s,m,aux,ambient)
    for obj in list(m.values())+d['claims']+list(aux.values()):
        text=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',text)
        assert not any(ord(ch)<32 and ch!='\n' for ch in text)
        assert text.count('$')%2==0 and text.count(r'\[')==text.count(r'\]')
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
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
                assert all(1<=e['page']<=29 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
    counts=dict(theorems=7,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=7,interfaces=15,source_members=15,direct_theorem_uses=31,related_theorem_connections=41,unranked_auxiliary_passages=14)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Seven printed Theorems in the main text are retained in full, including the classical Theorem 4.1. Small-cap theorem headings were independently enumerated on pages 1 through the main-text prefix of page 29; appendix bodies are excluded.',
      source_passages='Fifteen entries and fourteen supporting passages preserve the author kernel/privacy conventions, DQM and Fisher information, LAMN, fixed-channel MLE, hard truncation, separate C1-C3, full consistent quantizer, finite channel matrix domain and the complete six-step estimator.',
      dependencies='Independent reconstruction gives 31 direct uses and 41 related connections. Theorem 4.1 retains no ranked direct dependencies because its raw-model and likelihood quantities are ambient or locally bound. Theorem 3.5 imports only the information definition from Theorem 3.3, not its LAMN conclusion. Theorem 4.3 has no DQM assumption.',
      hypotheses='Theorem 3.3 uses weak convergence and allows singular limiting information; Theorem 3.5 requires positivity at finite n and at every weak accumulation point. C1-C3 remain distinct. The quantizer error vanishes along every convergent parameter sequence, not only pointwise.',
      estimators='Private MLEs preserve their exact likelihood and measurable-maximizer requirements. Hard truncation is zero outside the l1 ball. The two-step estimator retains all six steps, conditional pmfs, n2 normalization and arbitrary fallback; Theorem 4.12 assumes consistency and uses sqrt(n) local-alternative scaling.',
      source_issues='Eight scope/convention issues are recorded separately. The noisy moment mean need not lie in the stated inverse domain; Theorem 4.11 prints a nonnegative difference at different parameters; the bounded set in Lemma 4.5 is called a cone. Source statements are preserved without correction or proof certification.',
      names_and_highlights='Every entry has literal author terminology, faithful source-kind labels and meaningful matching selectors. DQM is the source acronym for C1; the original Definition 1 and assumptions are retained separately. All 41 theorem relations have source-specific paths and explanations.',
      reproduction='All six content JSON files reproduce byte for byte from the retained per-paper scripts. Independent source-specific checks, graph reconstruction, inventory validation and frozen hashes protect the reviewed extraction; rebuilding alone is not a new source review.')
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=[4,5,9,10,11,12,14,15,16,17,18,19,20,21,22,29],visually_reviewed_crops=[]))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=52,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent small-cap-heading enumeration and visual comparison of all seven complete Theorems.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv v3 manuscript identified by version and hash; no claim of byte-equivalence to the final journal article.','Original source conventions and ambiguities are retained separately; no appendix material is used in the census.','Source and schema validation do not certify mathematical proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=52,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(s,m,aux,ambient):
    snippets={
      1:[r'\mathfrak P(\mathcal X\to\mathcal Z)',r'[QP](dz):=\int_{\mathcal X}',r'Q[RP]=[QR]P',r'Q\mathcal P=\{QP:P\in\mathcal P\}',r'Q(dz\mid T(x))'],
      2:[r'\forall A\in\mathcal G,\forall x,x\prime' if False else r"\forall A\in\mathcal G,\forall x,x'\in\mathcal X",r'\bigcup_{(\mathcal Z,\mathcal G)}','no a priori restrictions'],
      3:['previous $Z_j$',r'Q_i(dz_i\mid x_i,z_{1:i-1})',r'for all $z_{1:i-1}',r'Q_{z_{1:i-1}}\in\mathcal Q_\alpha'],
      4:[r'\bigotimes_{i=1}^nQ_i(dz_i\mid x_i)','some marginal kernels',r'Q_i\in\mathcal Q_\alpha'],
      5:['interior point',r'\sigma','dominating measure',r'\frac12h^Ts_\theta(x)\sqrt{p_\theta(x)}',r'o(\|h\|^2)','score at'],
      6:[r'\mathbb E_\theta[s_\theta]=0',r'\mathbb E_\theta[s_\theta s_\theta^T]','exists and is finite'],
      7:['positive definite $p\\times p$ matrices','nonnegative-definite','probability for every',r'\Sigma_\theta^{1/2}\Delta','is independent of'],
      8:['Lemma D.2',r'\nu(dz):=Q(dz\mid x^*)',r'\int_{\mathcal X}q(z\mid x)p_\theta(x)\mu(dx)',r'[e^{-\alpha},e^\alpha]','measurable maximizer'],
      9:[r'\Pi_\tau(y):=y\mathbf1_{\{\|y\|_1\le\tau\}}'],
      10:['at every',r's_\theta','dominating measure'],
      11:[r'(x,\theta)\mapsto p_\theta(x)',r'(x,\theta)\mapsto s_\theta(x)','are measurable'],
      12:[r'\theta\mapsto s_\theta\sqrt{p_\theta}',r'L^2(\mu,\|\cdot\|_2)','is continuous'],
      13:['Condition (C1)',r'\dot p_\theta(x):=s_\theta(x)p_\theta(x)',r'0<\mu(B_{l,m}(\theta))<\infty',r'\frac{\int_{B_j}\dot p_\theta(y)\mu(dy)}{\mu(B_j)}','for every sequence','whose limit is also',r'\sqrt{P_\theta(K(\theta)^c)}'],
      14:[r'\mathcal M_\alpha(\ell,k)',r'\sum_{i=1}^{\ell}Q_{ij}=1','any given row',r"e^{-\alpha}Q_{ij'}\le Q_{ij}\le e^\alpha Q_{ij'}"],
      15:['1. Fix a preliminary','is identifiable','2. Consider a non-interactive',r'\forall\varepsilon>0,\forall\theta\in\Theta','3. Fix a consistent quantizer','4. Let',r'\operatorname*{arg\,max}','5. Generate','6. Let','where it exists, and defined arbitrarily otherwise',r'\frac1{n_2}\sum_{i=n_1+1}^n',r'n_2=n-n_1',r'\mathbf1_{\widehat T_{n_1}^{-1}(\{j\})}(x)',r'P_\theta(\widehat T_{n_1}^{-1}(\{j\}))']}
    for n,parts in snippets.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    for lid in ['D10','D11','D12']:assert m[lid]['source_kind']=='assumption'
    for lid in ['D5','D7','D13']:assert m[lid]['source_kind']=='definition' and 'Definition ' in m[lid]['source_heading']
    assert 'positive definite' not in s['D5'] and 'positive' not in s['D10']+s['D11']+s['D12']
    assert 'DQM' not in s['D9'] and 'sqrt n' not in s['D15']
    a={k:v['statement_original'] for k,v in aux.items()}
    checks={
      1:[r'\mathcal Z^{(0)}=\varnothing=\mathcal G^{(0)}',r'A\times\varnothing=A'],
      2:['set theoretically',r'\sup\{a\in\mathbb R',r'\exists(\mathcal Z,\mathcal G)'],
      3:['at every point'],
      4:['absolutely continuous part',r'\theta\notin\Theta'],
      5:[r'J_p','identity matrix','weak convergence'],
      6:[r'\frac1n\sum_{i=1}^nI_\theta(Q_{z_{1:i-1}}\mathcal P)'],
      7:['dominated by',r'\Theta\subseteq\mathbb R^p'],
      8:[r'G=\{g(x):x\in\mathcal X\}',r'f^{-1}:G\to\Theta'],
      9:['Conditions (C1) and (C2)',r'p=1',r'\mathfrak P(\mathbb N\times\Theta\to\mathbb N)',r'\max_{Q\in\mathcal Q_\alpha([k(\theta)]\to[k(\theta)])}',r'for every $\theta_0'],
      10:[r'e^{2\alpha}',r'\operatorname{tr}[I_\theta(\mathcal P)]',r"\operatorname{tr}[I_{\theta'}(\mathcal P)]",r'2\left\|\|\dot p_',r'+3\|p_',r'=:','Conditions (C1) and (C3)'],
      11:[r'\dot{\mathbf p}_\theta',r'M_{i,y}:=Q(\{i\}\mid y)',r'0\le v_j\le1',r'g_\theta(0):=0',r'\sum_{i=1}^{\ell}g_\theta(Q_{i\cdot}^T)','convex and sublinear'],
      12:['conditional on', 'are iid with counting density'],
      13:[r'\bigotimes_{i=n_1+1}^n',r'\bigotimes_{j=1}^{n_1}Q_0',r'\mathcal Z_0^{n_1}\to\mathbb N'],
      14:[r"d_0(x,x')=1",r'\alpha\in(0,\infty)','Hamming distance']}
    for n,parts in checks.items():
        for part in parts:assert part in a['A'+str(n)],(n,part)
    assert set(ambient['statement_local_bindings'])=={'T3.3','T3.5','T4.1','T4.2','T4.3','T4.11','T4.12'}
    issues={x['issue_id'] for x in ambient['source_issues']}
    assert issues=={'empty-product','unrestricted-output-class','moment-inverse-domain','cross-parameter-lower-bound','bounded-cone','appendix-density-reference','compact-consistency','conditional-efficiency'}
    refs=ambient['source_claim_references']
    assert sum(x['reference_kind']=='definition_reference' for x in refs)==3
    assert sum(x['reference_kind']=='proof_only' for x in refs)==2
    assert sum(x['reference_kind']=='appendix_reference_unresolved' for x in refs)==1
    for obj in aux.values():assert set(obj['depends_on'])<=set(m)
if __name__=='__main__':main()
