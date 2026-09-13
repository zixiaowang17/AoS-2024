"""Verify frozen source-reviewed content and independently reconstructed dependency scopes."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': '7cc4de36f103c6123bf559ab07ae2ab1f1950bb802d728181086be5186077816', 'source-passages.json': '4fa2deaef79c3567e5816278ccc7deea5029257753bf802498daa7fb50c42a90', 'interface-extraction.json': '68a065138f8459d76cb2f9b74661911579b17ec4ad432274c3ab46ef31321425', 'ambient-prerequisites.json': 'ff31031be1d8fbf51f60dbdee90a776c1115538f2b25b571b274131815bfb5c7', 'unfinalized-census.json': '01af7d80a02b35e81513282d0009525e923eef15859e9408d74a35969f90c7cc', 'ranked-interfaces.json': '2aa0879752dd4ba2a50773314f5a4f97a2d34ce188debaca1626b7a1bfe170f8'}
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
    assert registered['version']=='2308.15728v4.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2308.15728'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==58
    assert paper['main_text_last_pdf_page']==27 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==7
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Reconstructed from original definitions and theorem clauses; no builder graph imported.
    raw={1:[],2:[1],3:[],4:[],5:[4],6:[],7:[],8:[7],9:[],10:[],11:[10],12:[11],13:[7],14:[],15:[],16:[17],17:[],18:[],19:[18],20:[],21:[4]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'1':ids([1,3,5,6]),'2':ids([1,3,5,8]),'3':ids([1,3,8,9]),'4':ids([2,3,5,12]),'5':ids([1,5,8,13,14]),'6':ids([1,3,5,15]),'7':ids([16,19,20,21])}
    expected_reach={'1':ids([1,3,4,5,6]),'2':ids([1,3,4,5,7,8]),'3':ids([1,3,7,8,9]),'4':ids([1,2,3,4,5,10,11,12]),'5':ids([1,4,5,7,8,13,14]),'6':ids([1,3,4,5,15]),'7':ids([4,16,17,18,19,20,21])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([2,7,8,9,10,11,12,13])&expected_reach['1']
    assert not ids([4,5,6,10,11,12,13])&expected_reach['3']
    assert not ids([6,7,8,9,13,15])&expected_reach['4']
    assert not ids([1,2,3,5,6,7,8,9,10,11,12,13,14,15])&expected_reach['7']
    assert 'D3' not in expected_reach['5'] and 'D14' not in expected_reach['2']
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
        assert obj['evidence'] and all(1<=e['page']<=27 for e in obj['evidence'])
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
                assert all(1<=e['page']<=27 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
    counts=dict(theorems=7,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=7,interfaces=21,source_members=21,direct_theorem_uses=29,related_theorem_connections=43,unranked_auxiliary_passages=8)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Seven complete main-text Theorems1–7, independently enumerated by bold PDF spans, including the two-page T3. All finite thresholds, correction terms, primed constants, the exact step-size maximum and T5’s in-particular clause are retained.',
      source_passages='Twenty-one original source entries preserve Bernoulli and graphon sampling, off-diagonal loss, scalar/matrix polynomial classes, general and homogeneous SBM classes, iid-label prior, full randomized Algorithm1, the exact Holder norm/class, co-membership, sparse probability matrices and rectangular Gaussian biclustering definitions. Eight auxiliary passages preserve source context separately.',
      dependencies='Independent reconstruction confirms29 direct uses and43 related connections. Fixed-matrix minimax risks do not import a proof prior or random latent-position distribution. T4 imports its smooth graphon class and arbitrary latent law without requiring a homogeneous SBM. Rectangular Gaussian risk has no Bernoulli or graph-loss dependency.',
      scope='T3 imports the full algorithm, its independent auxiliary randomness and theorem-specific tuning, without T2’s low-SNR premise or an extra degree-D condition. T5 targets pairwise co-membership rather than numeric labels. T7 uses the shared min(k1,k2) label range and all-entry rectangular loss.',
      source_issues='Twelve notes preserve diagonal conventions, singular SNR endpoints, label nonuniqueness, the printed sketch dimension, iteration/degree accounting, algorithm probability and parameter scope, primed-constant text-layer errors, the integer Holder convention, rectangular label typos, Gaussian-noise independence and the distinction between low-degree results and runtime conjectures.',
      names_and_highlights='All21 entries have natural-language source terms, original labels/kinds and literal selectors. Every one of the43 theorem connections has a source-specific explanation and an independently reconstructed same-paper path.',
      reproduction='All six content JSON files reproduce byte for byte from retained per-paper scripts. Seven scripts include frozen-hash source review, formula checks, dependency reconstruction and schema validation; rerunning extraction does not itself perform a new source review.')
    reviewed_pages=[2,4,7,8,9,10,12,13,14,15,16,17,18,27]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[]))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=58,main_text_last_pdf_page=27,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-span heading enumeration and visual comparison of all seven complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark','Conjecture'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2308.15728v4 dated 12 Aug 2024, pinned by SHA-256. No substitution with another paper version.','Main-text proofs end on PDF page27 before References. All appendix bodies are excluded; proof-only constructions and propositions are not promoted into theorem statement dependencies.','Source and schema validation do not certify proofs or resolve the explicitly recorded source ambiguities.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=58,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))

def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'A_{ij}=A_{ji}\sim\operatorname{Bern}(M_{ij})','mutually independent',r'A_{ii}=M_{ii}=0'],
2:['i.i.d. random variables','arbitrary',r'(M_f)_{ij}:=f(\xi_i,\xi_j)'],
3:[r'\frac1{\binom n2}\sum_{1\le i<j\le n}',r'(\widehat M_{ij}-(M_f)_{ij})^2'],
4:[r'g:\mathbb R^N\to\mathbb R','degree at most $D$'],
5:[r'\mathbb R[A]_{\le D}^{n\times n}','degree no more than $D$'],
6:[r'Q=Q^\top\in[0,1]^{k\times k}',r'z\in[k]^n',r'M_{ii}=0'],
7:[r'0\le q<p\le1',r'p\mathbf1(z_i=z_j)+q\mathbf1(z_i\ne z_j)'],
8:[r'\mathbb P_{\mathrm{SBM}(p,q)}',r'z_i\overset{\mathrm{i.i.d.}}\sim\operatorname{Unif}\{1,\ldots,k\}'],
9:[r'B\in\mathbb R^{p\times r}',r'W_{l+1}=W_l-\eta B^\top\widetilde A^{t_1}(\widetilde A^{t_1}BW_l-\widetilde A)',r'W_0=0',r'\widehat M=\widetilde A^{t_1}BW_{t_2}'],
10:[r'\nabla_{00}f(x,y)=f(x,y)',r'\lfloor\gamma\rfloor',r'\gamma-\lfloor\gamma\rfloor',"(|x-x'|+|y-y'|)"],
11:[r'\mathcal H_\gamma(L)',r'\|f\|_{\mathcal H_\gamma}\le L',r'f(x,y)=f(y,x)'],
12:[r'\mathcal F_\gamma(L)',r'0\le f\le1',r'f\in\mathcal H_\gamma(L)'],
13:['unique',r'(Z_M)_{ii}=0',r'\frac{M_{ij}-q}{p-q}'],
14:[r'\ell(\widehat Z,Z)',r'\frac1{\binom n2}\sum_{1\le i<j\le n}'],
15:[r'0<\rho<1',r'[0,\rho]^{n\times n}',r'Q=Q^\top\in[0,\rho]^{k\times k}'],
16:[r'Y=M+E',r'M\in\mathcal M_{k_1,k_2}',r'N(0,1)'],
17:[r'M_{ij}=Q_{z_iz_j}',r'z_1\in[k_1]^{n_1}',r'z_2\in[k_2]^{n_2}'],
18:[r'Q_{ii}=\lambda',r'i\in[k_1\wedge k_2]',r'Q_{ij}=0\text{ otherwise}'],
19:[r'z_1\in[k_1]^n',r'z_2\in[k_2]^n',r'\operatorname{Unif}\{1,\ldots,k_1\wedge k_2\}',r'i\in[n_1]',r'j\in[n_2]'],
20:[r'\frac1{n_1n_2}\sum_{i\in[n_1],j\in[n_2]}'],
21:[r'\mathbb R[Y]_{\le D}^{n_1\times n_2}']}
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert m['D5']['source_kind']==m['D21']['source_kind']=='theorem_excerpt'
    assert m['D9']['source_heading']=='Algorithm 1'
    assert all(m['D'+str(n)]['source_kind']=='definition' for n in set(range(1,22))-{5,21})
    a={k:v['statement_original'] for k,v in aux.items()}
    for n,parts in {1:['Given',r'M\in\mathcal M_k','generative progress'],2:[r'2t_1t_2'],3:['deterministic polynomials','independently generated'],4:[r'\|D\|_F',r'\mathbf1_n'],5:['conjectured'],6:[r'\bigcup_{0\le q\le p\le1}'],7:[r'k^2q(1-p)'],8:[r'p,q\in[0,1]']}.items():
        for v in parts:assert v in a['A'+str(n)],(n,v)
    for o in aux.values():assert set(o['depends_on'])<=set(m)
    assert set(ambient['statement_local_bindings'])=={'T1','T2','T3','T4','T5','T6','T7'}
    assert {x['issue_id'] for x in ambient['source_issues']}=={'loss-normalization-and-diagonal','fixed-matrix-versus-prior-risk','snr-endpoints','unique-labels','sketch-dimension','iteration-count-and-degree','algorithm-probability-and-parameter-scope','printed-prime-constants','holder-integer-and-domain-convention','biclustering-label-notation','biclustering-prior-and-noise','low-degree-versus-runtime'}
    refs=ambient['source_claim_references'];assert sum(x['reference_kind']=='definition_reference' for x in refs)==1
    assert sum(x['reference_kind']=='proof_only' for x in refs)==4
    assert not any(x['reference_kind']=='assumption_reference' for x in refs)
if __name__=='__main__':main()
