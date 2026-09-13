"""Verify frozen source-reviewed content and independently reconstruct all theorem paths."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '9c0edbd16e2e66d92bf0bd695885246e2784b8dad9a0b549c85784782737d5db', 'source-passages.json': 'c761627f2ada3217f14a4fbf80a451828f616e603bf13f56b462fd015967617c', 'interface-extraction.json': 'b3e63e691cbcca2c5e27645699194777f9f6e2cb5785f1c27cdb43fd2142431f', 'ambient-prerequisites.json': '1ac1a6688340e4c7d0baef4a344ac6ddecc32ac1479583db47f68215e7c5c2ad', 'unfinalized-census.json': 'b9242882cb41eb82c3a65703a24b70011176327570ece2764ab85027670a28cd', 'ranked-interfaces.json': '630587d9069a7fff0bc7b749856d31acbfbc706655db2ee978a8b9840c80be92'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'\mathcal Y_i=\langle\mathcal A_i,\mathcal X^*\rangle_*+\mathcal E_i',r'\mathcal Y=\mathscr A(\mathcal X^*)+\mathcal E','fixed constants',r'\mathcal A_{i[k_1,\ldots,k_d]}\mathcal X^*_{[k_1,\ldots,k_d,j_1,\ldots,j_m]}'],
2:[r'r_k=\operatorname{rank}(\mathcal M_k(\mathcal A))','Supplement B',r'p_{-k}=\prod_{j\ne k}p_j'],
3:['$k$th largest singular value','leading $r$ left singular vectors','Q part of the QR decomposition'],
4:[r'\llbracket\mathcal S;\mathbf U_1,\ldots,\mathbf U_d\rrbracket',r'\mathbf U_k=\operatorname{SVD}_{r_k}(\mathcal M_k(\mathcal A))',r'\mathcal A\times_k\mathbf B','Supplement B'],
5:[r'\mathcal Z_{\max(\mathbf r)}:=\mathcal Z\times_{k=1}^d P_{\widehat{\mathbf U}_k}',r'\operatorname{arg\,max}_{\mathbf U_k\in\mathbb O_{p_k,r_k},k=1,\ldots,d}'],
6:[r'\frac12\|\mathcal Y-\mathscr A(\mathcal X)\|_{\mathrm F}^2',r'\operatorname{Tucrank}(\mathcal X)\le\mathbf r'],
7:[r'\operatorname{Tucrank}(\mathcal X)=\mathbf r',r'\mathbf V_k=\operatorname{QR}(\mathcal M_k(\mathcal S)^\top)',r'\mathbf U_{d+m}\otimes\cdots\otimes\mathbf U_{k+1}\otimes\mathbf U_{k-1}\otimes\cdots\otimes\mathbf U_1',r'\sum_{k=1}^{d+m}\mathcal T_k(P_{\mathbf U_{k\perp}}\mathcal M_k(\mathcal Z)P_{\mathbf W_k})','reverse operator'],
8:[r'\langle\mathscr A(\mathcal Z_1),\mathcal Z_2\rangle=\langle\mathcal Z_1,\mathscr A^*(\mathcal Z_2)\rangle',r'\sum_{i=1}^n\mathcal Z_{2[i,j_1,\ldots,j_m]}\mathcal A_{i[k_1,\ldots,k_d]}'],
9:[r'\underset{\alpha\in\mathbb R}{\operatorname{arg\,min}}',r'\|\mathscr A P_{T_{\mathcal X^t}}(\mathscr A^*(\mathscr A(\mathcal X^t)-\mathcal Y))\|_{\mathrm F}^2'],
10:['truncated high-order singular value decomposition (T-HOSVD)','sequentially truncated high-order singular value decomposition (ST-HOSVD)','Algorithms 6 and 7 in Supplement A'],
11:['(RGD Update)',r'\mathcal X^t-\alpha_tP_{T_{\mathcal X^t}}\mathscr A^*(\mathscr A(\mathcal X^t)-\mathcal Y)','given in (6)',r'\mathcal H_{\mathbf r}(\mathcal X^{t+0.5})'],
12:[r'1\le r_k\le p_k','smallest number',r'(1-R_{\mathbf r})\|\mathcal Z\|_{\mathrm F}^2\le\|\mathscr A(\mathcal Z)\|_{\mathrm F}^2\le(1+R_{\mathbf r})\|\mathcal Z\|_{\mathrm F}^2',r'0\le R_{\mathbf r}<1'],
13:[r'\lambda:=\min_{k=1,\ldots,d+m}\sigma_{r_k^*}(\mathcal M_k(\mathcal X^*))'],
14:['generated independently',r'N(0,1/n)',r'N(0,\sigma^2/n)'],
15:[r'm=0',r'y_i=\langle\mathcal A_i,\mathcal X^*\rangle+\varepsilon_i',r'\mathbf y\in\mathbb R^n'],
16:[r'\mathscr A^*(\mathbf y)',r'\times_{j<k}(\widehat{\mathbf U}_j^0)^\top\times_{j>k}(\widehat{\mathbf U}_j^0)^\top',r'\widehat{\mathbf U}_k^1(\widehat{\mathbf U}_k^1)^\top'],
17:[r'\mathcal Y_i=\mathcal X^*\times_1\mathbf a_i^\top+\mathcal E_i',r'\mathbf A=[\mathbf a_1,\ldots,\mathbf a_n]^\top',r'\mathcal Y=\mathcal X^*\times_1\mathbf A+\mathcal E'],
18:[r'\mathbf Q_{\mathbf A}\mathbf R_{\mathbf A}',r'\mathcal Y\times_1\mathbf Q_{\mathbf A}^\top',r'\times_{j<k}(\widehat{\mathbf U}_j^0)^\top\times_{j>k}(\widehat{\mathbf U}_j^0)^\top',r'\widetilde{\mathcal X}^0\times_1\mathbf R_{\mathbf A}^{-1}'],
19:[r'\mathbf X^*\in\mathbb R^{p_1\times p_2}',r'y_i=\langle\mathbf A_i,\mathbf X^*\rangle+\varepsilon_i'],
20:[r'\mathcal P_r(\mathbf B)=\mathbf U_{[:,1:r]}\boldsymbol\Sigma_{[1:r,1:r]}\mathbf V_{[:,1:r]}^\top','truncated SVD'],
21:['input rank is also 1','assume $n$ is even',r'\mathcal X^*=\lambda\mathbf u_1\circ\mathbf u_2\circ\cdots\circ\mathbf u_{d+m}',r'\mathcal Y^2_{[i,:,\ldots,:]}=\mathcal Y_{n/2+i}'],
22:[r'\mathcal M_{k-d+1}(\mathcal Y^1)',r'\sum_{i=n/2+1}^n y\prime_i\mathcal A_i',r'\times_{j<k}(\widetilde{\mathbf u}_j^0)^\top\times_{j>k}(\widetilde{\mathbf u}_j^0)^\top',r'\mathscr A^*(\mathcal Y)\times_{k=1}^{d+m}'],
23:[r'0\le\sigma^2<1',r'\|\mathcal X^*\|_{\mathrm F}+\sigma^2=1',r'N(0,\mathbf I_{1+p^d})',r'\mathcal X^*=\sqrt{1-\sigma^2}\mathbf x^{*\otimes d}',r'\operatorname{Uniform}(\{p^{-1/2},-p^{-1/2}\})','is i.i.d. generated'],
24:[r'\frac{R_{2\mathbf r}}{(d+m)(1+R_{2\mathbf r+\mathbf r^*}-R_{2\mathbf r})}\lambda'],
25:[r'\frac{1-R_{2\mathbf r}}{4(d+m)(\sqrt{d+m}+1)(1+R_{2\mathbf r+\mathbf r^*}-R_{2\mathbf r})}\lambda'],
27:[r'\frac{R_{2r}}{(1+R_{2r+r^*}-R_{2r})}\sigma_{r^*}(\mathbf X^*)'],
28:[r'\frac{1-R_{2r}}{8(1+R_{2r+r^*}-R_{2r})}\sigma_{r^*}(\mathbf X^*)'],
29:[r'\widetilde{\mathbf U}_k^0\in\mathbb O_{p_k,r_k}',r'\times_{j<k}(\widetilde{\mathbf U}_j^0)^\top\times_{j>k}(\widetilde{\mathbf U}_j^0)^\top',r'\widehat{\mathcal T}=\widetilde{\mathcal T}\times_{k=1}^d P_{\widetilde{\mathbf U}_k^1}'],
30:['Suppose',r'\operatorname{Tucrank}(\widehat{\mathcal X})\le\mathbf r','loss function value'],
31:['(RGN Update)',r'\underset{\mathcal X\in T_{\mathcal X^t}\mathbb M_{\mathbf r}}{\operatorname{arg\,min}}',r'\|\mathcal Y-\mathscr A P_{T_{\mathcal X^t}}(\mathcal X)\|_2^2',r'\mathcal H_{\mathbf r}(\mathcal X^{t+0.5})']}
    # The source typesets y_i with a prime; the saved transcription uses apostrophe syntax.
    checks[22][1]=r"\sum_{i=n/2+1}^n y'_i\mathcal A_i"
    assert set(checks)=={int(lid[1:]) for lid in m}
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert 'RGN Update' not in s['D11'] and 'RGD Update' not in s['D31']
    assert r'\alpha_t' not in s['D31']
    assert 'ST-HOSVD' not in s['D11']+s['D31']
    assert s['D13'] in t['1'] and s['D24'] in t['1'] and s['D25'] in t['2'] and s['D30'] in t['3']
    assert 'Gaussian' not in s['D1']+s['D12']+s['D29']
    assert r'1/n' not in s['D23']
    for k in ['D13','D24','D25','D27','D28','D30']:assert m[k]['source_kind']=='theorem_excerpt'
    assert m['D12']['source_heading'].startswith('Definition 1') and m['D14']['source_heading'].startswith('Definition 2')
    a={k:v['statement_original'] for k,v in aux.items()}
    assert '(RGD Update)' in a['A3'] and '(RGN Update)' in a['A3'] and 'ST-HOSVD and T-HOSVD' in a['A3']
    assert r'\mathbb O_{p,r}=\{\mathbf U\in\mathbb R^{p\times r}:\mathbf U^\top\mathbf U=\mathbf I_r\}' in a['A1']
    assert r'\check{\mathbf U}_k^t' in a['A4']+a['A5'] and r'\breve' not in a['A4']+a['A5']
    assert a['A6'] in t['1'] and r'\frac1{17}' in a['A8'] and r'R_{2r}(1-R_{2r})' in a['A8']
    assert 'is not a smooth manifold' in a['A9']
    assert all(set(x['depends_on'])<=set(m) for x in aux.values())
    assert set(ambient['statement_local_bindings'])=={'T'+str(i) for i in range(1,11)}
    refs=ambient['source_claim_references']
    assert sum(x['reference_kind']=='guarantee_reference' for x in refs)==4
    assert sum(x['reference_kind']=='proof_only' for x in refs)==3
    assert sum(x['reference_kind']=='object_reference' for x in refs)==4
    assert sum(x['reference_kind']=='estimator_reference' for x in refs)==1

def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2206.08756v3.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2206.08756'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==65
    assert paper['main_text_last_pdf_page']==26 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==10
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independently reconstructed from the reviewed source clauses, not imported from finalizer.
    raw={1:[],2:[],3:[],4:[2,3],5:[2,4],6:[1,2],7:[2,3,4],8:[1],9:[1,7,8],10:[7],11:[1,2,7,8,9],12:[2],13:[2,3],14:[1],15:[1,2],16:[3,4,8,15],17:[1,2,4],18:[3,4,17],19:[1],20:[3],21:[1],22:[3,4,8,21],23:[],24:[12,13],25:[12,13],27:[3,12],28:[3,12],29:[2,3,4],30:[1,2,6,12],31:[1,2,7]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={str(k):ids(v) for k,v in {1:[1,2,5,8,10,11,12,13,24],2:[1,2,5,8,10,12,13,25,31],3:[1,2,5,6,8,12],4:[1,2,5,8,14,30],5:[10,11,13,14,15,16,24,25,31],6:[10,11,13,14,17,18,24,25,31],7:[3,8,11,14,19,20,27,28,31],8:[10,11,13,14,21,22,24,25,31],9:[23],10:[2,4,5,29]}.items()}
    expected_reach={str(k):ids(v) for k,v in {1:[1,2,3,4,5,7,8,9,10,11,12,13,24],2:[1,2,3,4,5,7,8,10,12,13,25,31],3:[1,2,3,4,5,6,8,12],4:[1,2,3,4,5,6,8,12,14,30],5:[1,2,3,4,7,8,9,10,11,12,13,14,15,16,24,25,31],6:[1,2,3,4,7,8,9,10,11,12,13,14,17,18,24,25,31],7:[1,2,3,4,7,8,9,11,12,14,19,20,27,28,31],8:[1,2,3,4,7,8,9,10,11,12,13,14,21,22,24,25,31],9:[23],10:[2,3,4,5,29]}.items()}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([9,11,14,24]) & expected_reach['2']
    assert not ids([10,13,24,25]) & expected_reach['7']
    assert expected_reach['9']==ids([23])
    assert not ids([1,8,9,10,11,12,13,14,24,25,31]) & expected_reach['10']
    assert not ids([7,9,10,11,24,25,31]) & expected_reach['3']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==10 and len(ambient['source_issues'])==13
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
        assert obj['evidence'] and all(1<=e['page']<=26 for e in obj['evidence'])
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
                assert all(1<=e['page']<=26 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=10,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=10,interfaces=30,source_members=30,direct_theorem_uses=71,related_theorem_connections=115,unranked_auxiliary_passages=10),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(inventory='Exactly ten complete main-text Theorems1–10, independently enumerated by bold headings and compared visually, including every branch and printed title. Main text ends before references onpage26; supplementary bodies are excluded.',source_passages='Thirty source entries and ten auxiliary passages preserve regression/contraction, tensor rank and operations, geometry, TRIP, Gaussian design, separate RGD/RGN branches, initialization Algorithms2–4, testing distributions14 and deterministic OHOOI Algorithm5. Full Algorithm1 remains separately archived.',dependencies='Independent reconstruction verifies71 direct uses and115 related connections. RGN-only T2 has no RGD stepsize or additional RGD hypothesis. Matrix T7 uses P_r and does not inherit tensor-only retractions. Testing T9 has only its own hypothesis-test entry. Deterministic T10 has no regression/Gaussian/TRIP dependency.',references='T5/T6/T8 initialization references and T7 Corollary1 references are guaranteed output properties, not input assumptions. T4’s qualified-estimator reference applies to its upper branch, not its lower minimax infimum. T10 proof references from T5/T6 and Hermite calculations for T9 do not add statement dependencies.',source_issues='Thirteen notes preserve the RGN time-zero factor, unstarred expected-error target, dimension-index mismatch, unsquared testing normalization and conditional coupling, deferred supplement definitions, rank-range and rank-deficient conventions, zero line-search/logarithm domains, tensor2-norm print, update order and missing explicit rank-one factor normalization.',names_and_highlights='Every entry has literal author terminology, meaningful source highlights and preserved source kind. All115 related connections have local paths and source-specific explanations. No mathlib availability or proof-correctness claim is made.',reproduction='All six contentJSON files reproduce byte for byte in a fresh empty directory. Seven retained scripts cover inventory, extraction, context, finalization, rebuilding and independent review. Rebuilding reproduces saved decisions; it is not a new semantic source review.')
    reviewed_pages=[1,2,3,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,26]
    crops=[dict(path='evidence/page-18-theorem-crop.jpg',page=18),dict(path='evidence/page-20-theorem-crop.jpg',page=20),dict(path='evidence/page-17-context-crop.jpg',page=17),dict(path='evidence/page-19-context-crop.jpg',page=19)]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=crops))
    evidence=[dict(path='evidence/page-'+str(n).zfill(2)+'.jpg',page=n) for n in reviewed_pages]+crops+[dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=65,main_text_last_pdf_page=26,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-heading enumeration and visual comparison of all ten complete statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv2206.08756v3 marked15Jan2024,65PDFpages, pinned bySHA256; not silently exchanged for the published version.','Main text ends onpage26 at acknowledgements before REFERENCES y328.151; evidence clipped322. All supplement bodies are excluded.','Source validation preserves original statements, references and ambiguities; it does not prove the claims or complete deferred supplementary definitions.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=65,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
