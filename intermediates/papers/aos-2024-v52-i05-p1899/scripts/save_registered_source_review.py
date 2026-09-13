# -*- coding: utf-8 -*-
"""Check a frozen, source-reviewed census and retain its independent review evidence.

This records the completed source comparison. Re-execution checks that the reviewed
content has not changed; it does not prove the paper's mathematical claims.
"""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import PID,REPO,ROOT,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': 'd24637d6390d7921fa7b2596828a44ad809d69ae75bcad012a0bec72cfa94dd2', 'source-passages.json': 'd12af6d86c775dca691866182141f3c3948fb28c3330ff492d5611f284553f70', 'interface-extraction.json': 'bc0709fb15511d1f0d9035bbe9f23b3da636461a177ff2af8d4c800ab554235e', 'ambient-prerequisites.json': 'e8eb3370259495a620d0adc70a115de83b0aeda1ac9b356c3148ab941864620e', 'unfinalized-census.json': '77c058bce84b25f5afc98f47ef0f1466f5831407334207fab0b33eab654bf5db', 'ranked-interfaces.json': '5011b337e8f634d85d43e79bd47174032a3f8820f4fbcbcc07091cafca265422'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(numbers):return {'D'+str(n) for n in numbers}
def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2207.00120v1.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2207.00120'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL=='https://arxiv.org/pdf/2207.00120v1'
    assert paper['pdf_pages']==registered['pdf_pages']==80 and paper['main_text_last_pdf_page']==25
    assert paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(data['claims'])==20
    for original,c in zip(inv['claims'],data['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Reconstruct the paper-local graph from the inspected source, independently
    # of extract_interfaces.py and finalize_paper.py; neither module is imported.
    local_nums={1:[],2:[1],3:[2],4:[3],5:[],6:[],7:[],8:[1,4],9:[8,3,4],10:[8,4],11:[8,3,4],12:[9,10],13:[3,4],14:[1,2,13,4],15:[14],16:[13,4,15],17:[13,15],18:[17],19:[3,15],20:[17,18,9],21:[16],22:[21,10],23:[16,17,18,21,12],24:[23,11],25:[20,9],26:[22,23,24,10,11,12],27:[],28:[15,13,2],29:[15,13,2],30:[2,4],31:[30,13],32:[30,13],33:[30,13],34:[30,4],35:[2,4],36:[23,12],37:[3,28,29],38:[3,28,29],39:[2,3,4],40:[2,4],41:[2,13,4]}
    direct_nums={
        '3.1':[4,5,9,20,41], '3.2':[4,10,11,12,22,23,24,41],
        '4.1':[3,4,13,20,25,29,30], '4.2':[3,4,13,22,23,24,26,29,30],
        '4.3':[3,4,5,9,13,20,25,28,29,30,31,32],
        '4.4':[4,10,11,12,13,22,23,24,26,28,29,30,33],
        '4.5':[3,4,10,11,12,13,22,23,24,26,28,29,30,31,34],
        '4.6':[3,4,11,12,13,23,24,26,28,29,30,31,32,34],
        '5.1':[5,18,19,20,23,24,25,26,27,35,37],
        '5.2':[5,19,20,25,27,35,37], '5.3':[5,19,21,23,26,27,35,37],
        '5.4':[4,5,11,19,24,26,27,35,37],
        '5.5':[2,3,4,5,13,23,26,30,36,37], '5.6':[2,3,4,5,13,23,26,30,36,37],
        '6.1':[7,19,21,26,27,38,39],
        '6.2':[2,3,4,6,7,13,23,26,30,36,38,39,40],
        '6.3':[2,3,4,6,7,13,23,26,30,36,38,40],
        '6.4':[2,3,4,23,26,30,36,38,39,40],
        '6.5':[2,3,4,5,13,23,26,30,36,38,39],
        '6.6':[2,3,4,7,11,24,26,30,38,39]}
    local={'D'+str(n):ids(v) for n,v in local_nums.items()}
    direct={n:ids(v) for n,v in direct_nums.items()}
    assert {k:set(v['depends_on']) for k,v in members.items()}==local
    reach={}
    for n,seeds in direct.items():
        seen=set();stack=list(seeds)
        while stack:
            node=stack.pop()
            if node not in seen:seen.add(node);stack.extend(local[node])
        reach[n]=seen
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        actual={x['interface_id'].split('/')[-1] for x in data['interfaces'] if any(t['claim_id']==c['claim_id'] for t in x['related_theorems'])}
        assert actual==reach[n],(n,actual^reach[n])
    for n in ['3.1','3.2']:assert not (ids([25,26,28,29]) & reach[n])
    for n in ['4.1','4.2']:assert 'D29' in reach[n] and 'D28' not in reach[n]
    assert {n for n,r in reach.items() if 'D35' in r}=={'5.1','5.2','5.3','5.4'}
    assert {n for n,r in reach.items() if 'D38' in r}=={'6.1','6.2','6.3','6.4','6.5','6.6'}
    assert {n for n,r in reach.items() if 'D40' in r}=={'6.2','6.3','6.4'}
    assert {n for n,r in reach.items() if 'D39' in r}=={'6.1','6.2','6.4','6.5','6.6'}
    assert 'D36' not in reach['6.6'] and all('D27' not in reach[n] for n in direct if n.startswith('4.'))
    assert {n for n,r in reach.items() if 'D31' in r}=={'4.3','4.5','4.6'}
    assert {n for n,r in reach.items() if 'D32' in r}=={'4.3','4.6'}
    assert {n for n,r in reach.items() if 'D33' in r}=={'4.4'}
    assert {n for n,r in reach.items() if 'D34' in r}=={'4.5','4.6'}
    b={k:m['statement_original'] for k,m in members.items()}
    snippets={
      1:[r'X_n^s:=\{X_n^k:k\in s\}',r'\mathcal F_n^s:=\sigma(X_m^s:m\in[n])',r'\mathcal F^s:=\sigma(\mathcal F_n^s,n\in\mathbb N)'],
      2:['finite family',r'\mathcal Q^s:=\{P^s:P\in\mathcal Q\}',r'$X^{s_1}$ and $X^{s_2}$ are independent'],
      3:['non-empty, disjoint',r'\mathcal A(P):=\{e\in\mathcal K:P^e\in\mathcal G^e\}'],
      4:[r'P^e\in\mathcal H^e\cup\mathcal G^e',r'\mathcal H_0\equiv\mathcal P_\emptyset',r'\mathcal A(P)\in\Psi'],
      5:[r'\Psi_{l,u}:=\{A\subseteq\mathcal K:l\leq|A|\leq u\}',r'$u=K$'],
      6:[r'e\triangle e\'',r'e\triangle e\'\in\mathcal K'],
      7:[r'\text{if }e,e\'\in A\text{ then }e\cap e\'=\emptyset'],
      8:[r'\{T=n\}\in\mathcal F_n',r'\{T=n,D=A\}\in\mathcal F_n',r'$\Psi$-valued'],
      9:[r'P(D\setminus\mathcal A(P)\ne\emptyset)\leq\gamma',r'P(\mathcal A(P)\setminus D\ne\emptyset,D\ne\emptyset)\leq\delta'],
      10:[r'P(D\ne\emptyset)\leq\alpha',r'\forall P\in\mathcal H_0',r'P(D=\emptyset)\leq\beta',r'\forall P\in\mathcal P_\Psi\setminus\mathcal H_0'],
      11:[r'P(D\setminus\mathcal A(P)\ne\emptyset)\leq\gamma',r'P(\mathcal A(P)\setminus D\ne\emptyset)\leq\delta'],
      12:[r'\mathcal D_\Psi(\alpha,\beta)\cap\mathcal C_{\Psi\setminus\emptyset}(\gamma,\delta)'],
      13:[r'P\in\mathcal P_\Psi\setminus\mathcal H_0:e\notin\mathcal A(P)',r'P\in\mathcal P_\Psi:e\in\mathcal A(P)'],
      14:[r'P\in\mathcal G_{\Psi,e}\cup\mathcal H_0',r'Q\in\mathcal H_{\Psi,e}\cup\mathcal H_0',r'\mathcal F_n^s','mutually absolutely continuous'],
      15:[r'\frac{dP^s}{dQ^s}(\mathcal F_n^s)',r'Z_n(P^s,Q^s):=\log\Lambda_n(P^s,Q^s)'],
      16:[r'P\in\mathcal G_{\Psi,e}^{s_e}',r'P\in\mathcal H_0^{s_e}'],
      17:[r'P\in\mathcal G_{\Psi,e}^{s\'_e}',r'P\in\mathcal H_{\Psi,e}^{s\'_e}'],
      18:[r'\Lambda_{e,\mathrm{iso}}(n)>1','based on the from'],
      19:[r'P\in\mathcal G^e',r'P\in\mathcal H^e',r'\Lambda_{(1)}(n)\geq\cdots\geq\Lambda_{(|\mathcal K|)}(n)',r'p(n):=|\{e\in\mathcal K:\Lambda_e(n)>1\}|'],
      20:[r'D_{\mathrm{iso}}(n)\in\Psi',r'\Lambda_{e,\mathrm{iso}}(n)\notin(1/A_e,B_e)',r'D^*:=D_{\mathrm{iso}}(T^*)'],
      21:[r'\Lambda_{e,\mathrm{det}}(n)\leq1/C_e',r'\text{for every }e',r'\Lambda_{e,\mathrm{det}}(n)\geq D_e',r'\text{for some }e'],
      22:[r'T^*_{\mathrm{det}}:=\min\{T_0,T_{\mathrm{det}}\}',r'D^*_{\mathrm{det}}=\emptyset\quad\Longleftrightarrow\quad T_0<T_{\mathrm{det}}'],
      23:[r'T^*:=\min\{T_0,T_{\mathrm{joint}}\}',r'T_0<T_{\mathrm{joint}}',r'T_{\mathrm{joint}}<T_0',r'D_{\mathrm{iso}}(n)\in\Psi\setminus\emptyset'],
      24:[r'A_e=C_e,B_e=D_e',r'\chi^*_{\mathrm{fwer}}'],
      25:[r'\log A_e\sim|\log\delta|',r'\log B_e\sim|\log\gamma|','(8)'],
      26:[r'\chi^*_{\mathrm{det}}\in\mathcal D_\Psi',r'\chi^*_{\mathrm{fwer}}\in\mathcal E_\Psi',r'\log C_e\sim|\log\beta|',r'\log D_e\sim|\log\alpha|','(9)'],
      27:[r'A_e=A,\quad B_e=B,\quad C_e=C,\quad D_e=D','not needed for any of the results in Section 4','Theorem 6.1'],
      28:[r'P\in\mathcal G_{\Psi,e}',r'Q\in\mathcal H_{\Psi,e}\cup\mathcal H_0',r'\max_{1\leq m\leq n}Z_m(P^s,Q^s)\geq n\rho',r'\rho>\mathcal I(Q^s,P^s)','(11)'],
      29:[r'\sum_{n=1}^\infty P(Z_n(P^s,Q^s)<n\rho)<\infty',r'\sum_{n=1}^\infty Q(Z_n(Q^s,P^s)<n\rho)<\infty',r'\rho<\mathcal I(P^s,Q^s)','(12)'],
      30:[r'\inf_{Q\in\mathcal Q}\mathcal I(P^s,Q^s)',r'\min_{Q\in\mathcal Q}\mathcal I(P,Q;s)','whenever the quantities'],
      31:[r'\min_{e\in\mathcal A(P)}',r'\mathcal H_{\Psi,e};s\'_e','(15)'],
      32:[r'\min_{e\notin\mathcal A(P)}',r'\mathcal G_{\Psi,e};s\'_e','(16)'],
      33:[r'\min_{e\in\mathcal K}',r'\mathcal I(P,\mathcal G_{\Psi,e};s_e)','(17)'],
      34:[r'\max_{e\in\mathcal A(P)}',r'=\mathcal I(P,\mathcal H_0)','(18)'],
      35:[r'P=P^1\otimes\cdots\otimes P^K',r'\text{for every }P\in\mathcal P_\Psi','(21)'],
      36:[r'\limsup\frac{\mathbb E_P[T^*]}{\inf\{\mathbb E_P[T]',r'\mathcal C_\Psi(\alpha,\beta,\gamma,\delta)','(22)'],
      37:[r'\mathcal K=\{\{k\}:k\in[K]\}','distributional assumptions (11)-(12)'],
      38:[r'\mathcal K=\{\{i,j\}:1\leq i<j\leq K\}','independent (resp. dependent)','conditions (11) and (12)'],
      39:['disjoint and independent',r'\Longleftrightarrow',r'\{i,j\}\notin\mathcal A(P)',r'\forall i\in s_1,j\in s_2','(23)'],
      40:[r'v_0,v_1,\ldots,v_{L(P)}',r'P=P^{v_0}\otimes P^{v_1}\otimes\cdots\otimes P^{v_{L(P)}}','independent sources'],
      41:[r'a_e:=|\mathcal H_{\Psi,e}^{s\'_e}|',r'b_e:=|\mathcal G_{\Psi,e}^{s\'_e}|',r'c_e:=|\mathcal H_0^{s_e}|',r'd_e:=|\mathcal G_{\Psi,e}^{s_e}|','(7)']}
    for n,parts in snippets.items():
        for s in parts:
            s=s.replace("\\'", "'")
            assert s in b['D'+str(n)],(n,s)
    assert '(12)' not in b['D28'] and '(11)' not in b['D29']
    assert ',D\\ne\\emptyset' not in b['D11'] and 'e\\ne' not in b['D7']
    for n in [14,25,26,27,28,29,35,39]:assert members['D'+str(n)]['source_kind']=='assumption'
    for n in [31,32,33,34]:assert members['D'+str(n)]['source_kind']=='theorem_excerpt'
    for n in [4,37,38,40]:assert members['D'+str(n)]['source_kind']=='source_passage'
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert len(a)==23 and len(ambient['source_issues'])==24
    assert r'\limsup_n(x_n/y_n)\leq1' in a['A1']
    assert 'standing assumption' in a['A5'] and '(11)-(12)' in a['A5']
    assert 'do not assume' in a['A10'] and 'independence assumption (21)' in a['A10']
    assert r"s_k=s'_k=\{k\}" in a['A11'] and r'\operatorname{ARE}_P' in a['A11']
    assert r"e\subseteq s_e\cap s'_e" in a['A15'] and r"\mathcal H_0^{s'_e}" in a['A16']
    assert a['A17'].count('•')==4 and r'D\ne\emptyset' in a['A17']
    assert r'P(D\ne\mathcal A(P))\leq\gamma\wedge\delta' in a['A18']
    assert r'\emptyset\notin\Psi' in a['A19'] and 'coincides' in a['A19']
    assert 'first-order asymptotic approximation' in a['A20'] and 'local' not in a['A20']
    assert 'coincide and reduce to' in a['A22'] and 'superscript' in a['A23']
    assert set(ambient['statement_local_bindings'])=={'T'+n for n in direct}
    assert len(ambient['source_claim_references'])==3
    originals=list(members.values())+data['claims']+ambient['unranked_auxiliary_passages']
    for obj in originals:
        s=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',s)
        assert not any(ord(c)<32 and c!='\n' for c in s)
        assert s.count('$')%2==0
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        for e in obj['evidence']:assert 1<=e['page']<=25
    for x in data['interfaces']:
        assert len(x['members'])==1
        m=x['members'][0];lid=m['local_id']
        own=m['statement_original']+' '+m['local_label'];selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors)
        linked=own+' '+' '.join(c['statement_original'] for c in data['claims'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems']))
        assert all(s in linked for s in selectors)
        expected_uses={PID+'/T'+n for n,seeds in direct.items() if lid in seeds}
        assert {u['claim_id'] for u in x['central_claim_uses']}==expected_uses
        assert set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
        for rel in x['related_theorems']:
            n=rel['claim_id'].split('/T')[-1]
            assert rel['relation']==('direct' if lid in direct[n] else 'indirect')
            path=rel['via_local_ids'];assert path[0] in direct[n] and path[-1]==lid
            assert all(right in local[left] for left,right in zip(path,path[1:]))
            ex=x['theorem_explanations'][rel['claim_id']]
            assert ex['via_local_ids']==path and ex['text'].strip() and ex['evidence']
            assert 'This theorem directly uses the API.' not in ex['text']
        for kw in x['source_keywords']:
            if 'context_id' in kw:
                ctx=next(c for c in m['naming_context'] if c['context_id']==kw['context_id'])
                assert kw['source_text'] in ctx['text'] and all(1<=e['page']<=25 for e in ctx['evidence'])
            else:assert kw['source_text'] in m['statement_original']
    counts=dict(theorems=20,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(a))
    assert counts==dict(theorems=20,interfaces=41,source_members=41,direct_theorem_uses=201,related_theorem_connections=484,unranked_auxiliary_passages=23)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for c in rebuilt['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Twenty complete small-cap Theorem environments, 3.1-3.2, 4.1-4.6, 5.1-5.6 and 6.1-6.6, in source order. Theorems 5.2 and 6.2 continue on the next page. Corollaries are excluded. Main text ends after Conclusion and Funding on page 25; Appendix A begins on page 26.',
      source_passages='Forty-one separate original source entries preserve data/filtrations, finite global laws, unit hypotheses, prior families, four error classes, finite-time likelihoods, detection/isolation and local statistics, stopping rules, calibrations, distributional and information conditions, ARE and the dependence partition. Twenty-three auxiliary passages resolve scope, error events, reference laws and singleton notation.',
      dependencies='Independent local-graph and direct-use reconstruction confirms 201 direct theorem uses and 484 related connections. Theorems 3.1-3.2 do not acquire later calibrations or (11)-(12). Theorems 4.1-4.2 reach only (12); all four Section 4.4 results reach both. Independence (21) reaches only 5.1-5.4. Condition (23) reaches 6.1,6.2,6.4,6.5,6.6 with optional examples distinguished from mandatory assumptions.',
      scope='References to earlier theorems are restricted to the referenced numerical thresholds or numbered conditions. Theorem 4.5 adds (15) only for its familywise conclusion. Theorem-local T1,... formulas are not merged across papers or theorem numbers. Theorem 6.6 retains familywise optimality and does not acquire the joint ARE definition.',
      notation='Visual comparison confirms signal versus nonsignal extrema, min versus max in (15)-(18), full-sequence independence, projected-law cardinalities, strict likelihood tests, the conditional false-negative event, first-order lesssim, and expected-test-size divided by optimal size in ARE. Remark 2.1 supplies H^k,G^k; Remark 3.1 supplies singleton statistic aliases.',
      names_and_highlights='Every entry has original natural-language naming evidence and meaning-bearing highlights. Source kinds distinguish assumptions, theorem excerpts, definitions and neutral context. Every related theorem has a source-based path explanation outside its unchanged original statement.',
      limits='Twenty-four source issues retain apparent notation/domain inconsistencies: empty prior shorthand, disjoint self-pairs, projected-family richness, reference-law existence, ties, empty extrema, threshold calibration paths, partition choices and printed membership/ell aliases. These are documented without silently repairing the registered preprint or consulting appendix bodies.',
      reproduction='All six census content artifacts reproduced byte for byte in an empty directory. The retained per-paper scripts provide a standard rebuild.py entry point. Reproduction and schema validation do not replace the source comparison or certify proofs.')
    write('evidence/manual-findings.json',findings)
    images=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,25]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.jpg',sha256=digest(ROOT/f'evidence/page-{n:02}.jpg')) for n in images]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=80,main_text_last_pdf_page=25,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent small-cap heading enumeration and visual comparison of all twenty full original statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv v1 source; no assumption of equivalence to the published article.','Source ambiguities are preserved, not silently repaired or resolved through appendix-body inspection.','Census validation does not certify mathematical correctness or proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=80,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
