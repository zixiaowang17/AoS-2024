"""Validate the saved extraction against independently reviewed source scopes."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': '44f8c040d6ef81a8a6cd3799fbb29f2f397f6b9e5678cd4bb73eec7eb3e0358b', 'source-passages.json': '1bac0143eefab701a66195d2b4e9604f9faa3e947a08eb0a5deb035071b150e4', 'interface-extraction.json': '9180a0a51e25dc9dc44cda9d93549013b8e393c5b6c349f7944846264fad4ac1', 'ambient-prerequisites.json': 'cd237134bc305441eedd6b08aa681f6a4bf608d9fda78f602c33e96cd71dac20', 'unfinalized-census.json': '48d0e525b9260a5af9a1d1958bd49f4fe40c245977a04e974d008e255035e710', 'ranked-interfaces.json': '1e76523b9dc003f0430617826869f0eb9634f7cf87d811c47a8b51dda4f6f55f'}
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
    assert registered['version']=='2407.21238v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2407.21238'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==106
    assert paper['main_text_last_pdf_page']==29 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    assert len(inv['claims'])==len(d['claims'])==10
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent reconstruction from source definitions, not imported from builder modules.
    raw={1:[],2:[1],3:[2],4:[2,3],5:[2,3],6:[2,3],7:[1],8:[],9:[1,7],10:[],11:[1],12:[],13:[1],14:[],15:[],16:[1],17:[16],18:[16],19:[16],20:[16],21:[16],22:[16,21],23:[21],24:[3,4,5,6],25:[3,4,5,6,21],26:[1,24],27:[13,24],28:[16,25],29:[2],30:[29],31:[1,24],32:[13,27],33:[16,25],34:[3,29,30],35:[9,26,27],36:[9,26,27],37:[1,3]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={
'3.1':ids([2,3,4,5,6,7,8,9,10,11,12,24,26]),
'3.2':ids([2,3,4,5,6,7,8,10,12,13,14,15,24,27]),
'4.1':ids([2,3,4,5,6,7,8,10,16,17,18,19,20,22,23,25,28]),
'5.1':ids([2,3,4,5,6,7,8,9,10,12,13,14,15,26,27,29,30]),
'5.2':ids([2,3,4,5,6,7,10,16,17,18,19,20,22,23,28,29,30]),
'5.3':ids([7,9,10,11,12,13,14,15,26,27,30,31,32,34]),
'5.4':ids([7,10,16,17,18,19,20,22,23,28,30,33,34]),
'6.1':ids([10,13,14,15,29,35]),'6.2':ids([10,13,14,15,29,36]),'6.3':ids([1,3,10,12,37])}
    expected_reach={
'3.1':ids([1,2,3,4,5,6,7,8,9,10,11,12,24,26]),
'3.2':ids([1,2,3,4,5,6,7,8,10,12,13,14,15,24,27]),
'4.1':ids([1,2,3,4,5,6,7,8,10,16,17,18,19,20,21,22,23,25,28]),
'5.1':ids([1,2,3,4,5,6,7,8,9,10,12,13,14,15,24,26,27,29,30]),
'5.2':ids([1,2,3,4,5,6,7,10,16,17,18,19,20,21,22,23,25,28,29,30]),
'5.3':ids([1,2,3,4,5,6,7,9,10,11,12,13,14,15,24,26,27,29,30,31,32,34]),
'5.4':ids([1,2,3,4,5,6,7,10,16,17,18,19,20,21,22,23,25,28,29,30,33,34]),
'6.1':ids([1,2,3,4,5,6,7,9,10,13,14,15,24,26,27,29,35]),
'6.2':ids([1,2,3,4,5,6,7,9,10,13,14,15,24,26,27,29,36]),
'6.3':ids([1,2,3,10,12,37])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    for n in ['3.2','4.1','5.1','5.2','5.4','6.1','6.2']:assert 'D11' not in expected_reach[n]
    for n in ['4.1','5.2','5.4']:assert not ids([9,12,13,14,15])&expected_reach[n]
    for n in ['6.1','6.2']:assert 'D12' not in expected_reach[n]
    assert 'D22' not in local['D25'] and 'D18' not in local['D22']
    assert not ids([4,5,6,9,13,16])&expected_reach['6.3']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==14 and len(ambient['source_issues'])==15
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
            if e['page']==29:assert e['before_main_text_end']
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
    counts=dict(theorems=10,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=10,interfaces=37,source_members=37,direct_theorem_uses=122,related_theorem_connections=171,unranked_auxiliary_passages=14)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Ten complete main-text Theorems, numbered 3.1,3.2,4.1,5.1–5.4,6.1–6.3; Theorem 6.2 continues across pages 23–24. All bold headings enumerated independently through the clipped main-text endpoint on page 29.',
      source_passages='Thirty-seven source entries and fourteen supporting passages preserve four estimators, design and probability conventions, all eleven assumptions, both Table 3 regimes, all covariance/plug-in formulas and the externally named GREG mean estimator.',
      dependencies='Independent graph reconstruction confirms 122 direct uses and 171 related connections. Conclusion references do not import sufficient hypotheses. Fixed-H and growing-H alternatives are explicitly described separately. Comparison kernels do not acquire an unprinted Assumption 3 through notation.',
      formulas='Normalized sample CDF and uncentered regression slope are preserved. Quantile paths are left continuous. Table 3 footnote marks remain distinct from powers. Table 2 and equation (8) retain expectation placement, and Theorem 6.3 preserves slash division and separate respectively comparisons.',
      unresolved_definitions='The exact plug-in substitutions are referred to supplement Tables 5 and 6; rejective/piPS constructions and GREG are externally cited; bar-X lacks an explicit main-text defining equation. These are recorded as unresolved, without reading appendices or supplying standard replacements.',
      source_issues='Fifteen source scope/convention issues explicitly document branch scope, repeated-index positive definiteness, expectation/moment typography, missing comparison regularity premises, superpopulation centering and implicit correlation existence. No source statement is silently repaired.',
      names_and_highlights='Every entry uses literal source terms, appropriate source kind and heading, and source-backed selectors. All 171 relationships have paper-local explanation paths with the relevant subpart/design scope.',
      reproduction='All six content JSON artifacts regenerate byte for byte using the retained per-paper scripts. Frozen content hashes, independent PDF heading enumeration, source-specific checks, dependency reconstruction and schema validation pass.')
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=[6,8,10,11,12,14,15,16,17,19,20,21,22,23,24,26,29],visually_reviewed_crops=[]))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=106,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-heading enumeration and visual comparison of all ten theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv v2 dated 29 November 2024, pinned by hash; no assertion of equivalence to another journal or preprint version.','Appendix bodies excluded; supplement-only and external definitions remain unresolved.','Source and schema validation do not certify mathematical proofs or repair source ambiguities.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=106,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'\mathcal S','probability distribution',r'\sum_{s\in\mathcal S}P(s)=1'],
2:[r'F_{y,N}(t)=\sum_{i=1}^N1_{[Y_i\le t]}/N',r'\inf\{t\in\mathbb R:F_{y,N}(t)\ge p\}'],
3:[r'/\sum_{i\in s}d(i,s)',r'\widehat F_y(t)\ge p'],
4:[r'(\widehat Q_y(p)/\widehat Q_x(p))Q_{x,N}(p)'],
5:[r'\sum_{i\in s}d(i,s)Y_i\Big/\sum_{i\in s}d(i,s)X_i'],
6:[r'\widehat\beta=\sum_{i\in s}d(i,s)X_iY_i/\sum_{i\in s}d(i,s)X_i^2'],
7:[r'P^*(B\times E)=\int_E\sum_{s\in B}P(s,\omega)dP(\omega)','cylinder subset'],
8:['left continuous functions','right hand limits','ball $\sigma$-field','sup norm metric'],
9:[r'D(P\|R)=\sum_{s\in\mathcal S}',r'\log(P(s,\omega)/R(s,\omega))','for some rejective'],
10:[r'0<\lambda<1'],11:['Given any $k\ge1$',r'(\mathbf V_i-\mathbf T\pi_i)^T(\mathbf V_i-\mathbf T\pi_i)',r'K_1\le N\pi_i/n\le K_2'],
12:[r'\operatorname{supp}(F)=(a_1,a_2)','positive continuous derivatives'],
13:['independently with probability proportional',r'\lfloor N/n\rfloor+1',r'\sum_{r=1}^nN_r=N'],
14:[r'\max_{1\le i\le N}X_i/\min_{1\le i\le N}X_i\le K'],
15:['not a subset of a straight line'],16:[r'\pi_i=m_hr_h/M_hN_{hj}','independently across the strata and the clusters'],
17:[r'\underline{\lim}',r'\overline{\lim}',r'\lambda_h>0',r'\Lambda_h>0',r'N_{hj}^4/M_h',r'(N_{hj}-N_h/M_h)^2/M_h\to0'],
18:[r"E_P\|\mathbf W'_{hjl}\|^2<\infty",r"(X'_{hjl})^2",'not a subset of a straight line'],
19:[r'\operatorname{supp}(F_{y,h})=C_y','positive continuous derivatives',r'\nu\ge1'],
20:[r'\sum_{\nu=1}^\infty\exp(-KH)',r'\sum_{h=1}^HM_h^4/H=O(1)'],
21:[r'F_{y,H}(t)=\sum_{h=1}^H(N_h/N)F_{y,h}(t)',r'\mathbf\Gamma_h=E_P',r'f_{x,H}(t)=dF_{x,H}/dt'],
22:[r'\mathbf\Gamma_1',r'\mathbf\Gamma_2',r'\Theta_1>0',r"\|\mathbf W'_{hjl}\|^2/N=O(1)"],
23:[r'\sup_{C_y}|f_{y,H}(t)-\widetilde f_y(t)|\to0',r'\sup_{C_x}|f_{x,H}(t)-\widetilde f_x(t)|\to0'],
24:[r'\widehat Q_{y,REG}(p)',r'E_P(X_iY_i)/E_P(X_i)^2',r'Q_y(p)/Q_x(p)'],
25:[r'{}^{2}\Theta_2/{}^{2}\Theta_1',r'{}^{2}\Theta_3/{}^{2}\Theta_4','The $\Theta_1$',r'H\to\infty'],
26:[r'\bar\zeta(p)',r'S(p)',r'(\pi_i^{-1}-1)'],
27:[r'\bar X/N',r'X_i^{-1}',r'\gamma=\sum_{r=1}^nN_r(N_r-1)/N(N-1)'],
28:[r'N_h(N_h-n_h)',r"E_P(\zeta'_{hjl}(p_1)-E_P(\zeta'_{hjl}(p_1)))\times",'Table 3'],
29:['known smooth function $J$ on $[0,1]$',r'f:\mathbb R^k\to\mathbb R'],
30:[r'\mathbf a=\lim_{\nu\to\infty}\nabla f',r'\sigma_2^2=\mathbf a\mathbf\Delta\mathbf a^T'],
31:[r'(\pi_i^{-1}-1)\pi_i^{-1}',r'\sum_{i\in s}(1-\pi_i)','Table 5 in Section 2 of the supplement'],
32:[r'A_i/X_i^2',r'\widehat{\bar\zeta}(p)=\sum_{i\in s}\widehat\zeta_i(p)(A_i/NX_i)','Table 5 in Section 2 of the supplement'],
33:[r'N_h^2/n_h-N_h',r'\widehat{\bar\zeta}_h','Table 6 in Section 2 of the supplement'],
34:[r'\widehat{\mathbf a}=\nabla f(\widehat Q_y(p_1),\ldots,\widehat Q_y(p_k))'],
35:[r'1\le u\le4',r'K_u(p_w,p_v)'],36:[r'1\le u\le3',r'K_u^*(p_w,p_v)'],
37:['GREG estimator',r'\sqrt n(\bar y-E_P(Y_i))',r'\sqrt n(\widehat Q_y(0.5)-Q_y(0.5))']}
    for n,parts in checks.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    for n in [10,11,12,14,15,17,18,19,20,22,23]:assert m['D'+str(n)]['source_kind']=='assumption'
    assert m['D37']['source_kind']=='source_passage'
    assert all(m['D'+str(n)]['source_kind']=='theorem_excerpt' for n in [26,27,28,30])
    assert 'Assumption 2' not in s['D27'] and 'Assumption 6' not in s['D20']
    assert 'GREG' not in s['D6'] and 'the sample median' in s['D37']
    assert 'Assumption 3' not in s['D24'] and 'Assumption 7' not in s['D22']
    assert 'not necessarily identical' in aux['A9']['statement_original']
    assert 'independent of the observations in other strata' in aux['A9']['statement_original']
    assert 'i.i.d.' in aux['A3']['statement_original']
    assert r'E_P(X_i)^2' in aux['A8']['statement_original']
    assert set(ambient['statement_local_bindings'])=={'T3.1','T3.2','T4.1','T5.1','T5.2','T5.3','T5.4','T6.1','T6.2','T6.3'}
    assert {x['issue_id'] for x in ambient['source_issues']}=={'conclusion-versus-assumptions','fixed-versus-growing-strata','left-continuous-paths','positive-definiteness-quantifiers','expectation-parentheses','moment-power-typography','undefined-bar-x','supplement-plug-in-definitions','external-sampling-definitions','external-greg-definition','comparison-kernel-existence','median-comparison-scope','slash-division','table-footnotes','smoothness-and-gradient'}
    refs=ambient['source_claim_references']
    assert sum(x['reference_kind']=='appendix_reference_unresolved' for x in refs)==2
    assert sum(x['reference_kind']=='external_definition_unresolved' for x in refs)==1
    assert sum(x['reference_kind']=='conclusion_as_hypothesis' for x in refs)==1
    for obj in aux.values():assert set(obj['depends_on'])<=set(m)
if __name__=='__main__':main()
