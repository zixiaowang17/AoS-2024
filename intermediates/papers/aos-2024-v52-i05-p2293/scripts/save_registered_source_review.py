"""Verify frozen source-reviewed content and independently reconstructed dependency scopes."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': '4d14363d2f66e4ff235ecd999aeb9b3c2756d93368af1ab961666c6a02a48d04', 'source-passages.json': '58f2fa4f48d20dc22025755e20a1dedf04bbdfc6c5478e09bcf6e9481349f87d', 'interface-extraction.json': '51e1776a6d4de44926d33878e8b4c06014acb664c2a51a7e5a9a7703d680623a', 'ambient-prerequisites.json': 'd23de861b24778ee5a2215f5adb900807d07719222e1d7563e68ca7a2ccf039a', 'unfinalized-census.json': 'c51be4a490b83353384626568c00326e39659df98b9804800a05fbca91b1383f', 'ranked-interfaces.json': '40da725c58ed236cac1b61d1c8985b55f880c27d208c9638f30ceb28732ea118'}
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
    assert registered['version']=='2408.02913v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2408.02913'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==60
    assert paper['main_text_last_pdf_page']==21 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==8
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Reconstructed from original definitions and theorem clauses; no builder graph imported.
    raw={1:[],2:[],3:[],4:[],5:[1,2],6:[5],7:[2,6],8:[1],9:[1],10:[],11:[1],12:[],13:[],14:[],15:[],16:[],17:[],18:[],19:[16,17,18]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'2.1':ids([1,3,4]),'2.2':ids([3,4,7,8,9,10,12]),'2.3':ids([3,4,7,8,11,13]),'2.4':ids([3,4,7,8,10,12]),'2.5':ids([3,4,7,8,11,13]),'3.1':ids([6,7,14]),'3.2':ids([3,4,7,8,15]),'4.1':ids([3,4,7,8,12,16,17,18,19])}
    expected_reach={'2.1':ids([1,3,4]),'2.2':ids([1,2,3,4,5,6,7,8,9,10,12]),'2.3':ids([1,2,3,4,5,6,7,8,11,13]),'2.4':ids([1,2,3,4,5,6,7,8,10,12]),'2.5':ids([1,2,3,4,5,6,7,8,11,13]),'3.1':ids([1,2,5,6,7,14]),'3.2':ids([1,2,3,4,5,6,7,8,15]),'4.1':ids([1,2,3,4,5,6,7,8,12,16,17,18,19])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([2,5,6,7,8,9,10,11,12,13])&expected_reach['2.1']
    assert not ids([9,11,13])&(expected_reach['2.4']|expected_reach['4.1'])
    assert not ids([3,4,8,9,10,11,12,13,15])&expected_reach['3.1']
    assert not ids([9,10,11,12,13,14])&expected_reach['3.2']
    assert 'D10' not in expected_reach['4.1']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==12 and len(ambient['source_issues'])==12
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
    counts=dict(theorems=8,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=8,interfaces=19,source_members=19,direct_theorem_uses=45,related_theorem_connections=72,unranked_auxiliary_passages=12)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Eight complete main-text Theorems: 2.1–2.5, 3.1–3.2 and 4.1. Independent small-cap heading enumeration includes the locally labeled independent-variable theorem attributed to earlier work. All original/truncated branches, moment cases, covariance identities and bandwidth conditions are retained.',
      source_passages='Nineteen source entries preserve norms, causal inputs, partial sums, coupling conventions, uniform dependence, Conditions2.1–2.4, clipping, both decay thresholds, banded quadratic blocks, the zeta1 exponent, the trend model, quantile grid, kernel and local-linear estimator. Twelve supporting passages retain necessary context separately.',
      dependencies='Independent reconstruction confirms 45 direct uses and 72 related connections. T2.1 has no causal/dependence assumptions; T3.1 has no UI or Gaussian-coupling premise. Nonsingularity conditions and the two decay thresholds remain distinct. Theorem references import only their stated definitions or assumptions.',
      scope='T2.2 second branch matches clipped covariance but targets original sums. T2.4 uses centered clipped sums only in its faster time change. T3.2 states an unconditional little-o_P bound at true second moments, importing only the numerical zeta1 definition. T4.1 applies approximation assumptions to noise Zi, with noise sums distinct from deterministic design moments.',
      source_issues='Twelve source notes preserve the uniform-integrability comparison, reversed zeta comparison, nonmonotone second-moment times, overloaded block notation, quantile-grid endpoint inconsistency and implicit kernel conventions. Original statements are not repaired; source review does not certify proofs.',
      names_and_highlights='All nineteen entries have natural-language source terms, original source kinds and labels, literal selectors and complete same-paper theorem explanations. Every one of the 72 dependency paths is checked independently.',
      reproduction='All six content JSON artifacts reproduce byte for byte. Seven retained per-paper scripts include an independent source-review check with frozen hashes, formula assertions, dependency reconstruction and schema validation.')
    reviewed_pages=[2,4,5,6,7,8,11,12,13,14,15,21]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[]))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=60,main_text_last_pdf_page=21,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent small-cap heading enumeration and visual comparison of all eight complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark','Conjecture'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2408.02913v2 dated 7 Aug 2024, pinned by SHA-256. No substitution with another paper version.','Main text ends on PDF page21 before Supplementary Material. Appendix bodies, including deferred proofs and simulation extensions, are excluded.','Source and schema validation do not certify proofs or resolve the explicitly recorded source ambiguities.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=60,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))

def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'\mathbb E(|Y|^p)^{1/p}',r'\|\cdot\|=\|\cdot\|_2'],
2:[r'X_t=g_t(\mathcal F_t)',r'(\varepsilon_i)_{i\in\mathbb Z}','measurable functions'],
3:[r'S_i:=\sum_{j=1}^iX_j'],
4:['common, possibly enriched probability space',r'=_{\mathcal D}(X_i)_{1\le i\le n}'],
5:[r'\sup_i(\mathbb E|X_i-X_{i,\{i-k\}}|^p)^{1/p}',r"\varepsilon'_{i-k}"],
6:[r'\Theta_{i,p}=\sum_{k=i}^\infty\delta_p(k)'],
7:['$p>2$','$A>1$',r'\mu_{p,A}:=\sup_{i\ge0}(i+1)^A\Theta_{i,p}\le C<\infty'],
8:['For any fixed $a>0$',r'\sup_i\mathbb E(|X_i|^p\mathbb I_{\{|X_i|^p\ge an\}})\to0'],
9:[r'm_n\to\infty',r'\min_{1\le i\le n-m_n}\|X_i+\ldots+X_{i+m_n}\|^2=\infty'],
10:[r'(X_j^\oplus-\mathbb E(X_j^\oplus))',r'X_i^\oplus=T_{n^{1/p}}(X_i)',r'T_b(w)=\max\{\min\{w,b\},-b\}'],
11:[r'c>0',r'l_0\in\mathbb N',r'\min_{1\le j\le n-l+1}\|X_j+\ldots+X_{j+l-1}\|^2/l\ge c'],
12:[r'p^2-p-2+(p-2)\sqrt{p^2+10p+1}',r'{4p}'],
13:[r'p^2-4+(p-2)\sqrt{p^2+20p+4}',r'{8p}'],
14:[r'\sum_{1\le s\le t\le n}',r'|s-t|>D_n',r'\sup|a_{s,t}|\le1',r'R_k=\sum_{j=1}^k(V_j-\mathbb E(V_j))',r'\lceil n/D_n\rceil'],
15:[r'\zeta_1=\min\{1,2-4/p\}/(1+2A)'],
16:[r'X_i=\mu(t_i)+Z_i',r'\mu(\cdot)\in C^3[0,1]'],
17:[r't_n<t_{n+1}=1',r't_i=F^{-1}(i/n)',r'F(t)=\int_0^tf(u)\,du'],
18:['smooth symmetric kernel',r'[-\omega,\omega]',r'\int_{\mathbb R}\Psi_K(u;\delta)\,du=O(\delta)',r'|y-u|\le\delta'],
19:[r'S_j(t)=\sum_{i=1}^n(t-t_i)^jK((t-t_i)/h_n)',r'\widehat\mu_{h_n}(t):=\sum_{i=1}^nw_{h_n}(t,i)X_i',r'\frac{S_2(t)-(t-t_i)S_1(t)}{S_2(t)S_0(t)-S_1^2(t)}']}
    for n,parts in checks.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    assert all(m['D'+str(n)]['source_kind']=='condition' for n in [7,8,9,11])
    assert all(m['D'+str(n)]['source_kind']=='theorem_excerpt' for n in [12,13,14])
    assert m['D4']['source_kind']=='source_passage' and m['D18']['source_kind']=='assumption'
    a={k:v['statement_original'] for k,v in aux.items()}
    for n,parts in {1:[r'\mathbb E(X_i)=0'],2:['in probability','stochastically bounded'],3:[r'S_i=\sum_{j=1}^ie_j',r'\mathbb E(S_{i-1}^2)'],4:[r'1\le a,k,j\le\lceil n/m\rceil',r'R_j^2+2B_{\lfloor j/m\rfloor}R_j'],5:['may be negative','two independent standard Brownian motions'],6:['conditional distribution'],7:['multiple constants','solely on $p$'],8:['Condition 2.2 is weaker'],9:[r'A>1/2-1/q'],10:[r'\zeta_2<\zeta_1'],11:[r'O(h_n^3+n^{-1}h_n^{-1})'],12:[r'2\widehat\mu_{h_n}(t)-\widehat\mu_{h_n\sqrt2}(t)']}.items():
        for part in parts:assert part in a['A'+str(n)],(n,part)
    for o in aux.values():assert set(o['depends_on'])<=set(m)
    assert set(ambient['statement_local_bindings'])=={'T2.1','T2.2','T2.3','T2.4','T2.5','T3.1','T3.2','T4.1'}
    assert {x['issue_id'] for x in ambient['source_issues']}=={'coupling-space','truncated-target-and-centering','distinct-nonsingularity-and-decay','uniform-integrability-comparison','variance-time-not-necessarily-monotone','quadratic-bandwidth-and-constants','block-notation-overload','bootstrap-versus-theoretical-rate','reversed-block-exponent-comparison','quantile-grid-endpoint','kernel-normalization-and-denominator','noise-and-sum-notation'}
    refs=ambient['source_claim_references']
    assert sum(x['reference_kind']=='definition_reference' for x in refs)==2
    assert sum(x['reference_kind']=='assumption_reference' for x in refs)==2
    assert sum(x['reference_kind']=='proof_only' for x in refs)==2
if __name__=='__main__':main()
