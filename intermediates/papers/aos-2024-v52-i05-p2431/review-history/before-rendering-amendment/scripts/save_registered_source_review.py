"""Verify frozen, source-reviewed content using independent branch and graph checks."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': 'f19bc8f44e7fc74ceb4abab0eabc4f828822996a80630017fb3d631310260f34', 'source-passages.json': '0d363307622a7cb3a407752ed463aa0fe66b4a4d62ee54163fc22855997b3094', 'interface-extraction.json': '02f2806a184873b16707acf91679854cb11f551a3e4a8cff74c5df089a54c0d2', 'ambient-prerequisites.json': 'b7d48eeeaccc4fcb10106e3a9803908242a8f93a543db5536924690d833e8cb3', 'unfinalized-census.json': '50eb131679338c0c6b77dbe157f20e0f057f4124e3a53d31092cda69c6c91fbc', 'ranked-interfaces.json': 'b9092711c6d1b895f63b5f7af660800b5646fc62129d220a971751b6fa077443'}
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
    assert registered['version']=='2311.07773v1.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2311.07773'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==31
    assert paper['main_text_last_pdf_page']==12 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    assert len(inv['claims'])==len(d['claims'])==5
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independently reconstructed from the original source definitions and statement clauses.
    raw={1:[],2:[],3:[],4:[1,2,3],5:[],6:[],7:[2,4,6],8:[4,5],9:[],10:[4,5,8,9,14],11:[2,4],12:[],13:[2],14:[]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'2.2':ids([4,7,8,10,14]),'3.1':ids([4,7,14]),'3.3':ids([4,5,8,9,10,14]),'4.1':ids([2,4,5,8,11,12]),'4.2':ids([4,5,6,7,8,9,13])}
    expected_reach={'2.2':ids([1,2,3,4,5,6,7,8,9,10,14]),'3.1':ids([1,2,3,4,6,7,14]),'3.3':ids([1,2,3,4,5,8,9,10,14]),'4.1':ids([1,2,3,4,5,8,11,12]),'4.2':ids([1,2,3,4,5,6,7,8,9,13])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert all('D10' not in expected_reach[n] for n in ['3.1','4.1','4.2'])
    assert all('D12' not in expected_reach[n] for n in ['2.2','3.1','3.3','4.2'])
    assert 'D9' not in expected_reach['3.1']|expected_reach['4.1']
    assert 'D13' in expected_reach['4.2'] and all('D13' not in expected_reach[n] for n in ['2.2','3.1','3.3','4.1'])
    assert 'D6' not in expected_reach['3.3']|expected_reach['4.1']
    assert 'D14' not in expected_reach['4.1']|expected_reach['4.2']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==8 and len(ambient['source_issues'])==12
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
        assert obj['evidence'] and all(1<=e['page']<=12 for e in obj['evidence'])
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
                assert all(1<=e['page']<=12 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=5,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=5,interfaces=14,source_members=14,direct_theorem_uses=27,related_theorem_connections=45,unranked_auxiliary_passages=8),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Five complete main-text Theorems2.2,3.1,3.3,4.1,4.2, independently enumerated by bold headings. Include the simplified summary and externally credited computational upper bound. Conjecture3.2 remains a conjecture, not a sixth Theorem. Discussion and acknowledgment end before AppendixA on shared PDF page12.',
      source_passages='Fourteen original source entries preserve conditional Bernoulli graph generation, balanced memberships, two layer matrices, alternative and null laws, Hamming loss, recoverability, strong distinguishability, Assumption1, the full low-degree conjecture, conditional alternatives, directed chi-square divergence, the joint edge-count MLE and runtime convention. Eight auxiliary passages preserve contextual variants and source issues.',
      dependencies='Independent reconstruction checks27 direct uses and45 related connections. Computational hardness connects to the conjecture only in the computational summary bullet and Theorem3.3. Chi-square is required by Theorem4.1, not the low-degree theorem merely because it motivates a proof. MLE is used by Theorem4.2; there is no implication-only edge from recovery to detection.',
      scope='Keep latent joint laws distinct from the A marginals used for testing, conditional edge independence distinct from mixture independence, exact balanced priors distinct from iid Bernoulli labels, approximate recovery distinct from exact recovery, and strong detection distinct from weak detection. The statistical limits n*T*rho and computational n*sqrt(T)*rho remain separate.',
      source_issues='Twelve notes retain the p/q assignment mismatch in chi-square prose, reversed Lemma2.1 caption, its two-layer change, positive-versus-negative logarithm typo in the runtime explanation, unresolved runtime scope for unrestricted layer growth, implicit prior independence, even-integer monomials, equality boundaries, MLE ties and missing external algorithm/conjecture regularity detail. Original quotations are not silently repaired.',
      names_and_highlights='All14 entries have natural-language source terms, literal highlights and source kinds/headings that distinguish Assumption1 and Conjecture3.2 from definitions and theorem claims. Every related theorem has a checked same-paper dependency path and specific source correspondence.',
      reproduction='All six content JSON artifacts reproduce byte for byte in a fresh directory. Seven retained scripts preserve inventory extraction/review, definitions, context, finalization, rebuild and independent source review with frozen hashes and formula checks.')
    reviewed_pages=[4,5,6,7,8,10,11,12]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[]))
    evidence=[dict(path='evidence/page-'+str(n).zfill(2)+'.jpg',page=n) for n in reviewed_pages]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=31,main_text_last_pdf_page=12,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-font heading enumeration and visual comparison of all five complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark','Conjecture'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2311.07773v1 marked 13 Nov 2023, with cover dated 15 Nov 2023, pinned by SHA-256. No substitution with a different version.','Main text and acknowledgment end on PDF page12, clipped at y=458 before AppendixA at y=466.815. Appendix bodies are excluded from census evidence and dependencies; no appendix results are imported.','Source and schema validation do not certify proofs, establish the assumed hardness conjecture, or resolve the explicitly recorded source ambiguities.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=31,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'\operatorname{Bernoulli}(B_t(\sigma_i,\sigma_j))',r'1\le i<j\le n',r'1\le t\le T','symmetric binary adjacency matrices'],
2:['both $n$ and $T$ are even',r'\mathcal S_n=\{\sigma\in\{0,1\}^n',r'\sum_{i\in[n]}\sigma(i)=n/2'],
3:[r'\rho\in(0,2/3)',r'B^{(0)}=\begin{bmatrix}\frac32\rho&\frac12\rho',r'B^{(1)}=\begin{bmatrix}\frac12\rho&\frac32\rho'],
4:[r'\sigma\sim\operatorname{Uniform}(\mathcal S_n)',r'\tau\sim\operatorname{Uniform}(\mathcal S_T)',r'B_t=B^{(\tau_t)}','Generate $A$ according to (1)',r'joint distribution of $(A,\sigma,\tau)$'],
5:[r'P_{0,n}=P_0(n,T,\rho)',r'\operatorname{Bernoulli}(\rho)',r'1\le i<j\le n'],
6:[r'n^{-1}\min',r'd_{\mathrm{Ham}}(\widehat\sigma,1-\sigma)','up to label permutation'],
7:[r'\widehat\sigma(A)\in\mathcal S_n',r'P_{1,n}(\ell_n(\widehat\sigma,\sigma)\ge\epsilon)\to0','any positive constant'],
8:[r'\widehat\psi(A)\in\{0,1\}',r'P_{1,n}(\widehat\psi(A)=0)+P_{0,n}(\widehat\psi(A)=1)\to0'],
9:[r'T_n\to\infty',r'\rho_n\to0',r'\rho_n^{-1}=o(n^2)'],
10:['Assumption 1','every polynomial',r'D_n=\log^{1.01}(n)',r'E_{P_{0,n}}\psi^2=1',r'E_{P_{0,n}}\psi=0',r'E_{P_{1,n}}\psi=O(1)','uniformly',r'A\in\mathbb R^{\binom n2\times T_n}'],
11:[r'conditional distribution of $(A,\sigma)$',r'\tau\in\mathcal S_{T_n}',r'P_{\sigma,\tau}',r'distribution of $A$ given $(\sigma,\tau)$'],
12:['distributions $P,Q$','mass function $q(x)$ and $p(x)$ respectively',r'd_{\chi^2}(Q,P)=E_{X\sim P}',r'\frac{q^2(x)}{p(x)}-1'],
13:[r'\operatorname{arg}\max_{\sigma\in\mathcal S_n,\tau\in\mathcal S_{T_n}}',r'2\mid\sigma(i)+\sigma(j)+\tau(t)',r'A_t(i,j)','(4)'],
14:['polynomial-time','polynomial in $n$']}
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert m['D9']['source_kind']=='assumption'
    assert m['D10']['source_kind']=='source_passage' and m['D10']['source_heading'].startswith('Conjecture 3.2')
    assert m['D4']['source_heading'].startswith('Definition 1(1)') and m['D5']['source_heading'].startswith('Definition 1(2)')
    assert all(m['D'+str(n)]['source_heading'].startswith('Definition 2') for n in [6,7,8])
    assert 'exact recovery' not in s['D7'] and 'polynomial' not in s['D13']
    a={k:v['statement_original'] for k,v in aux.items()}
    ac={1:[r'n\to\infty',r'T\to\infty',r'\rho\to0','relate $L$'],2:['Detection implies recovery','if $P_{1,n}$ is asymptotically recoverable',r'(T_n+2,\rho_n)'],3:[r'-1.01',r'T_n\gg\log^{2.02}n',r'(\log n)^{1.4}',r'T_n=O(n^2)'],4:['regularity conditions','can be directly verified'],5:[r'P_{0,n}(E_n)\to0','implies',r'P_{1,n}(E_n)\to0'],6:['[28, 29]','variant of spectral clustering'],7:[r'\operatorname{Bernoulli}(1/2)','additional bookkeeping'],8:[r'T_n^{-1}\rho_n^{-2}\sum_tB_t^2\succeq cI','more general MLSBMs']}
    for n,parts in ac.items():
        for v in parts:assert v in a['A'+str(n)],(n,v)
    for o in aux.values():assert set(o['depends_on'])<=set(m)
    assert set(ambient['statement_local_bindings'])=={'T2.2','T3.1','T3.3','T4.1','T4.2'}
    assert 'No conjecture premise' in ambient['statement_local_bindings']['T2.2']['branches']['information_theoretic']
    assert {x['issue_id'] for x in ambient['source_issues']}=={'joint-versus-observation-marginals','balanced-priors-and-conditional-independence','binary-labels-and-observation-domain','asymptotic-integer-and-boundary-regimes','conditional-computational-hardness','recovery-and-detection-strength','recovery-detection-lemma-caption','chi-square-pmf-naming','conditional-layer-quantifier','runtime-logarithm-sign','mle-domain-and-ties','external-spectral-and-conjecture-details'}
    refs=ambient['source_claim_references'];assert sum(x['reference_kind']=='definition_reference' for x in refs)==2
    assert sum(x['reference_kind']=='assumption_reference' for x in refs)==3
    assert sum(x['reference_kind']=='proof_only' for x in refs)==2
    assert sum(x['reference_kind']=='external_result_reference' for x in refs)==1
if __name__=='__main__':main()
