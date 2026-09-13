"""Verify frozen, source-reviewed content using independent branch and graph checks."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': 'dff4787c8790d5f041dedcd200c1f00377f29e1c861f24173b96bb41a86df169', 'source-passages.json': '0791bb54c790b5024295f02da283dc7c1448839d8c30206de4a0c405d8c0c3c2', 'interface-extraction.json': 'a7a1662a9525107dfc2af471c56f2aa5168eb90ec7caef1d94c9ba2daa1700aa', 'ambient-prerequisites.json': '10fe29708a9fd0a46032c7fe4d1939aa6a7746c6f631b29bdb23c24a6e34a47b', 'unfinalized-census.json': '7b9ae651c586fb8403827d63f8c5a1aee6b220f2addfa5d59858e344ee596f2f', 'ranked-interfaces.json': '4dfe002aa606e9e961324b875fcea447f9c48e007ad9dd0365370bdcb971460b'}
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
    assert registered['version']=='2110.14067v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2110.14067'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==66
    assert paper['main_text_last_pdf_page']==28 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==4
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independently reconstructed from the original source definitions and statement clauses.
    raw={1:[],2:[],3:[1,2],4:[1,2,3],5:[4],6:[],7:[],8:[6],9:[7],10:[],11:[6],12:[6],13:[7,12],14:[6],15:[14],16:[6,15],17:[],18:[],19:[],20:[7],21:[17],22:[7,20,21],23:[22],24:[22],25:[6,11,16]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'1':ids([1,5,10]),'2':ids([1,5,6,7,8,9,11]),'3':ids([1,5,6,12,13,14,16]),'4':ids([1,5,6,7,9,13,14,16,17,18,19,22,23,24,25])}
    expected_reach={'1':ids([1,2,3,4,5,10]),'2':ids([1,2,3,4,5,6,7,8,9,11]),'3':ids([1,2,3,4,5,6,7,12,13,14,15,16]),'4':ids([1,2,3,4,5,6,7,9,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert 'D6' not in expected_reach['1'] # no stationarity imposed on T1
    assert all('D10' not in expected_reach[n] for n in ['2','3','4']) # no proof-based general-Z import
    assert not ids(range(17,26))&(expected_reach['1']|expected_reach['2']|expected_reach['3'])
    assert 'D8' not in expected_reach['4'] # bootstrap branch uses estimated ratio and Gaussian-Z law
    assert 'D12' in expected_reach['4'] and 'D12' not in direct['4'] # via sample Yule–Walker estimator
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==15 and len(ambient['source_issues'])==13
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
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=4,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=4,interfaces=25,source_members=25,direct_theorem_uses=32,related_theorem_connections=51,unranked_auxiliary_passages=15),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Four complete main-text Theorems1–4. Theorem1 heading is on page10 and body on11; Theorem2 spans14–15 with two branches; Theorem3 is on18; Theorem4 has all three branches on23. Independent bold-font enumeration excludes citations and Lemmas. Acknowledgement ends28; References start29.',
      source_passages='Twenty-five original source entries preserve moment norms, causal/coupling/short-range definitions, stationary covariance and correlation targets and estimators, general linear combinations, AR Yule–Walker and derivative formulas, the full kernel definition, bandwidth bias sequence, conditional probability, residuals, multipliers, bootstrap statistics and Gaussian CDF targets. Fifteen auxiliary passages preserve branch-specific numerical assumptions and source context.',
      dependencies='Independent graph reconstruction checks32 direct uses and51 related connections. T1 has no stationary covariance requirement. T2 and T3 use their own local linearizations without importing the general T1 combination through a proof relationship. T4 imports Lemma4 branchwise and only the v_T definition from Lemma3. General AR coefficients enter T4 through the sample Yule–Walker estimator.',
      scope='Keep all five inequalities in(12) and(17), uniform normalized-sum nondegeneracy, sigma_0>c in the correlation branch, fixed integer p=O(1) and a positive minimum eigenvalue for AR inference. Bootstrap(i) alone has the explicit sixth-root Op rate; (ii) and(iii) give op(1). Exact conditional laws and finite-B empirical quantiles are distinct.',
      source_issues='Thirteen source notes retain the k-versus-l summand in Remark2, repeated unbound j in T2(i) covariance, undefined sigma_k^(i) in(27), triangular-array and stationarity scope, definition-only references, estimator domains, AR interpretation, overloaded symbols, kernel normalization, conditional rates and finite-lag boundaries. These issues are not silently corrected in original statements.',
      names_and_highlights='All25 entries have source-extracted natural-language titles, original source kinds/headings and literal highlights. Keyword combinations keep source definitions unchanged. Every related theorem has an explicit source-backed dependency path and explanation; no generic relationship captions are used.',
      reproduction='All six content JSON files reproduce byte for byte in a fresh directory. Seven saved per-paper scripts include inventory review, extraction, auxiliary context, finalization, rebuild and source review. Frozen hashes prevent later content changes from inheriting this review.')
    reviewed_pages=[7,8,11,12,13,14,15,17,18,21,22,23,28]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[]))
    evidence=[dict(path='evidence/page-'+str(n).zfill(2)+'.jpg',page=n) for n in reviewed_pages]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=66,main_text_last_pdf_page=28,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-font heading enumeration and visual comparison of all four complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark','Conjecture'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2110.14067v2 dated25Feb2023, pinned by SHA-256. No substitution with a different version.','Main text and acknowledgment end on PDF page28. All appendix bodies excluded; main-text Lemma assumptions and numeric definitions are resolved only as required by statements.','Source and schema validation do not certify proofs or resolve the explicitly recorded source ambiguities.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=66,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'\|X\|_m=(E|X|^m)^{1/m}',r'm\ge1'],
2:['non-necessarily identically distributed',r'g_{i,j}(\ldots,e_{i-2},e_{i-1},e_i)','sample size $T$','if $d=1$'],
3:[r'e_{i-k}^\dagger',r'\text{if }k<0',r'\delta_m(k)=\sup_{i\in\mathbb Z,j=1,\ldots,d}',r'\delta_m(k)=0'],
4:[r'm\ge4',r'\alpha>1',r'\beta\ge0',r'EX_{i,j}=0',r'\sum_{l=k}^\infty\delta_m(l)=O(T^\beta)'],
5:['special case of Definition 1',r'\beta=0',r'\sum_{l=k}^\infty\delta_m(k)=O(1)'],
6:['weakly, but not necessarily strictly stationary',r'EX_i=0',r'\sigma_j=EX_iX_{i-j}=EX_0X_{-j}'],
7:[r'\widehat\sigma_j=\frac1T\sum_{i=j+1}^TX_iX_{i-j}'],
8:[r'\rho_j=\sigma_j/\sigma_0'],
9:[r'\widehat\rho_j=\widehat\sigma_j/\widehat\sigma_0'],
10:[r'\max_{i=1,\ldots,p_1}\sum_{j=0}^da_{ij}^2=O(1)',r'p_1=O(T^{\alpha_{p_1}})',r'Z_{i,k}=\sum_{j=0}^da_{kj}(X_iX_{i-j}-EX_iX_{i-j})'],
11:[r'-\frac{\sigma_j}{\sigma_0^2}(X_i^2-\sigma_0)',r'+\frac1{\sigma_0}(X_iX_{i-j}-\sigma_j)'],
12:['weakly stationary','positive integer',r'\sigma_k=\sum_{j=1}^pa_j\sigma_{|k-j|}','exists.'],
13:[r'\widehat\sigma_k=\sum_{j=1}^p\widehat a_j\widehat\sigma_{|j-k|}','equation (16)'],
14:[r'\Sigma=\{\sigma_{|j-k|}\}',r'\gamma=(\sigma_1,\sigma_2,\ldots,\sigma_p)^T',r't_s^{(i)}=1','non-singular'],
15:[r'b_0=-\Sigma^{-2}\gamma',r'b_i=\Sigma^{-1}e_i-\Sigma^{-1}T_i\Sigma^{-1}\gamma',r'b_p=\Sigma^{-1}e_p'],
16:[r'\sum_{k=0}^pb_{jk}(X_iX_{i-k}-\sigma_k^{(i)})'],
17:['symmetric, continuously di-fferentiable',r'K(0)=1',r'K(x)\,dx<\infty',r'\exp(-2\pi itx)',r'FK(x)\ge0',r'FK(x)\,dx<\infty'],
18:[r'k_T\to\infty',r'k_T^{2-\alpha}',r'2<\alpha<3',r'\log(k_T)/k_T',r'\alpha=3',r'1/k_T',r'\alpha>3'],
19:[r'\operatorname{Prob}(\cdot\mid X_1,\ldots,X_T)',r'E(\cdot\mid X_1,\ldots,X_T)'],
20:[r'\widehat\epsilon_i^{(j)}=X_iX_{i-j}-\widehat\sigma_j',r'i=j+1,j+2,\ldots,T'],
21:['joint normal',r'E\varepsilon_j=0',r'K((j_1-j_2)/k_T)'],
22:[r'\widehat\sigma_j^*=\widehat\sigma_j+\frac1T\sum_{i=j+1}^T',r'\widehat\epsilon_i^{(j)}\times\varepsilon_i'],
23:[r'\widehat\rho_j^*=\widehat\sigma_j^*/\widehat\sigma_0^*',r'j\in\mathcal I'],
24:[r'\widehat\Sigma^*=\{\widehat\sigma^*_{|j-k|}\}',r'\widehat\gamma^*=(\widehat\sigma_1^*,\ldots,\widehat\sigma_p^*)^T',r'\widehat\Sigma^{*\dagger}\widehat\gamma^*','Moore-Penrose'],
25:[r'H_\sigma(x)',r'H_\rho(x)',r'H_a(x)','(19)','(21)','(29)',r'\max_{j=1,\ldots,p}|\xi_j|']}
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert r'\dagger' not in s['D13']
    assert r'\sigma_j' not in s['D10']
    assert all(m['D'+str(n)]['source_kind']=='theorem_excerpt' for n in [10,11])
    assert m['D18']['source_kind']=='source_passage'
    for n in [4,12,17]:assert m['D'+str(n)]['source_heading'].startswith('Definition ')
    assert m['D5']['source_heading'].startswith('Remark 2')
    a={k:v['statement_original'] for k,v in aux.items()}
    ac={1:['(11)','(12)',r'12\alpha B',r'8\alpha B'],2:['(17)',r'\frac{12\beta_X}m+12\alpha_X\beta_X',r'0<\alpha_s<\alpha_l<1'],3:['(18)',r'j\in\mathcal H'],4:['(20)',r'\sigma_0>c',r'j\in\mathcal I'],5:['(28)',r'p=O(1)','weakly stationary','smallest eigenvalue'],6:['Definition 2',r'k_T\to\infty',r'm\ge8',r'\alpha_X>2'],7:['(17) and (18)'],8:['(17) and (20)'],9:['conditions of Theorem 3'],10:[r'7\alpha_X\beta_X',r'8\beta_X/m+7\alpha_X\beta_X-1/2'],11:[r'v_T=o(1)',r'k_T\times T^{-1/2}=o(1)','positive number'],12:[r'\mathbf1_{\{a_c\le a_b\}}\ge1-\alpha',r'b^*=\min'],13:['best linear predictor',r'\sum_{j=1}^p\beta_jEX_{i-j}X_{i-k}'],14:[r'\mathcal F_i',r'\mathcal F_{i,k}'],15:[r'p\le d',r'1-\alpha','bootstrap replicates']}
    for n,parts in ac.items():
        for v in parts:assert v in a['A'+str(n)],(n,v)
    for o in aux.values():assert set(o['depends_on'])<=set(m)
    assert set(ambient['statement_local_bindings'])=={'T1','T2','T3','T4'}
    branches=ambient['statement_local_bindings']['T4']['branches']
    assert branches['i']['assumptions']==['A2','A3','A7','A10']
    assert branches['ii']['assumptions']==['A2','A4','A8','A10']
    assert branches['iii']['assumptions']==['A5','A9','A11']
    assert {x['issue_id'] for x in ambient['source_issues']}=={'short-range-tail-summand','gaussian-covariance-lag-indices','undefined-ar-centering','stationarity-and-triangular-arrays','branchwise-lemma-four-import','definition-reference-not-whole-lemma','ratio-and-sample-solution-domains','ar-interpretation-and-order','symbol-overloading','kernel-normalization-and-psd','bootstrap-laws-and-rates','finite-lag-boundary-and-centering','nondegeneracy-and-growth-scope'}
    refs=ambient['source_claim_references'];assert sum(x['reference_kind']=='definition_reference' for x in refs)==5
    assert sum(x['reference_kind']=='assumption_reference' for x in refs)==1
    assert sum(x['reference_kind']=='external_definition_reference' for x in refs)==1
if __name__=='__main__':main()
