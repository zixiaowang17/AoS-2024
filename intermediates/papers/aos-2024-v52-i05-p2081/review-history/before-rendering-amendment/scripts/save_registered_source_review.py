"""Validate frozen source-reviewed content independently of the census builder."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': 'aff5b507d9b18c8af78aad41266da152d54fcb682ace045aa2c4cfc52820d6e4', 'source-passages.json': '0c7680dfa8ff88c105e52f048393bade8be73fb66991b1c4dc75dda2f11cd535', 'interface-extraction.json': 'bb1a48dc1e8c2d268627972666cf235ddec0d191fb10dbfd1a33893bdcba5212', 'ambient-prerequisites.json': 'e286d99300f3c36158d527403ea7abe0a762ae1be7996823e5f968a1546a9a27', 'unfinalized-census.json': '094c5ba2e7b46d8d65f1de56e24ddf9c4735dcf643abc286c1fb656f473fa607', 'ranked-interfaces.json': 'a77ab43bddb685903d49954088975aecd21f56fd2beb040f12d3cefc2371f878'}
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
    assert registered['version']=='2205.15717v3.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2205.15717'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert ir['printed_label_check']==[[14,'3.1'],[18,'3.4']]
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==73
    assert paper['main_text_last_pdf_page']==29 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==2
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Reconstructed from the source scopes; no extraction/finalizer graph imported.
    raw={1:[],2:[],3:[],4:[3],5:[4],6:[5],7:[2,5,6],8:[7],9:[2,3,4,8],10:[],11:[10],12:[],13:[],14:[10,12,13],15:[11,12,13],16:[],17:[14],18:[15,16],19:[2,3,6,10]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'3.1':ids([1,3,6,9,11,12,13,14,15,16,17,18]),'3.4':ids([2,3,6,7,8,9,19])}
    expected_reach={'3.1':ids(range(1,19)),'3.4':ids([2,3,4,5,6,7,8,9,10,19])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n]
    assert 'D19' not in expected_reach['3.1']
    assert not ids([1,11,12,13,14,15,16,17,18])&expected_reach['3.4']
    s={lid:a['statement_original'] for lid,a in m.items()}
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==14 and len(ambient['source_issues'])==12
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
    counts=dict(theorems=2,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=2,interfaces=19,source_members=19,direct_theorem_uses=19,related_theorem_connections=28,unranked_auxiliary_passages=14)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Both complete original main-text Theorems, 3.1 and 3.4, are retained. Independent bold-heading enumeration covers pages 1-28 and the main-text prefix of page 29. Theorem 3.1 keeps the expected posterior probability, both rate terms and all four prior combinations; Theorem 3.4 keeps its explicit expansion and appendix reference.',
      source_passages='Nineteen original entries and fourteen supporting passages preserve weighted mixed-derivative Holder regularity, harmonic-mean anisotropy, local and rescaled charts, normalized manifold pullbacks, Gaussian mixtures, both weight priors, both scale constructions, all conditions (3)-(15) needed by the statements, and the geometric Gaussian operator.',
      dependencies='Independent graph reconstruction confirms 19 direct uses and 28 related connections. The posterior-contraction theorem does not acquire K_Sigma from its proof. The approximation theorem does not acquire priors or the Hellinger correction in Corollary 3.5. Auxiliary (14)-(15), scale matrices and regularity assumptions retain their indexed prerequisite expansions.',
      prior_branches='Table 1 is preserved as four explicit combinations. MFM adds (9), DPM does not; (10) is common. Partial scales use (11), including a polynomial upper tail, whereas hybrid scales use (12)-(13), including expected exponential tails. The graph union represents conditional uses, not simultaneous assumptions.',
      source_issues='Twelve source issues are retained separately, including the offset boundary wording, appendix-only reach/chart/partition definitions, zero-order division and swapped pullback indices in (15), mixture integration domains, prior aliases, covariance squares, local chart inverses and coefficient/quantifier scope. No appendix body or invented formula is used.',
      names_and_highlights='Every entry has literal author terminology, faithful source headings, meaning-bearing source selectors and source-specific theorem explanations. Definition 2.1 keeps mixed derivative requirements and Definition 2.2 keeps delta^(D-d) normalization.',
      reproduction='All six JSON content artifacts reproduce byte for byte from the retained per-paper scripts. Independent source-specific checks and frozen hashes protect the reviewed state; this is a source census, not proof certification.')
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=[6,8,9,11,12,13,14,18,29],visually_reviewed_crops=['theorem-3-1.png','theorem-3-4.png','density-conditions.png']))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=73,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-heading enumeration and visual comparison of both complete Theorems.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv v3 manuscript identified by version and hash; no claim of byte-equivalence to the final journal article.','Original source conventions and ambiguities are retained separately; no appendix material is used in the census.','Source and schema validation do not certify mathematical proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=73,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(s,m,aux,ambient):
    snippets={
      1:[r'(\sqrt{f(x)}-\sqrt{g(x)})^2','two positive functions'],
      2:['distance less than',r'd(z,M)\leq\delta'],
      3:[r'\beta^{-1}=\frac1D\sum_i\beta_i^{-1}',r'\alpha_i=\beta/\beta_i',r'\alpha_1+\cdots+\alpha_D=D'],
      4:[r'\langle k,\alpha\rangle<\beta',r'|D^kf(x)|\leq L(x)',r'\beta-\alpha_{max}',r'\frac{\beta-\langle k,\alpha\rangle}{\alpha_i}\wedge1'],
      5:[r'\boldsymbol\beta=(\beta,\ldots,\beta)',r'\mathcal H_{iso}^{\beta}'],
      6:['closed submanifold','reach bounded from below','Appendix A',r'\Psi_{x_0}:V_{x_0}\to M'],
      7:[r'\Psi_{x_0}(v)+N_{x_0}(v,\eta)','isometry','diffeomorphism','to its image',r'\beta_M-1',r'\tau/2'],
      8:[r'\bar\Psi_{x_0}(v,\delta\eta)',r'\mathcal W_{x_0,\delta}',r'\tau/2\delta'],
      9:[r'supported on $M^\delta$',r'\delta^{D-d}f\circ\bar\Psi_{x_0,\delta}',r'\delta^{D-d}L\circ\bar\Psi_{x_0,\delta}',r'\mathcal H_{an}^{\boldsymbol\beta_{0,\perp}}'],
      10:[r'\det^{1/2}(2\pi\Sigma)',r'\|z\|_{\Sigma^{-1}}^2','positive definite'],
      11:[r'O^T\Lambda O',r'\delta_{(\mu_k,O_k,\Lambda_k)}',r'K\in\mathbb N\cup\{+\infty\}'],
      12:[r'A>0',r'\operatorname{Beta}(1,A)',r'\prod_{i<k}(1-V_i)'],
      13:[r'\alpha_K>0',r'K\sim\pi_K',r'\mathcal D(\alpha_K,\ldots,\alpha_K)'],
      14:['common accross components',r'\delta_{(\mu_k,O_k)}','either a Dirichlet process prior or a mixture of finite mixtures'],
      15:['conditionally',r'H_1(d\mu,dO)\otimes Q_2(d\lambda)',r'\widetilde\Pi_\Lambda'],
      16:['Haar measure',r'b_2>2D-1',r'e^{-c_1\|\mu\|^{b_1}}',r'(1+\|\mu\|)^{-b_2}'],
      17:[r'b_4>D(D-1)/2',r'\sum_{i=1}^D\lambda_i^{-d/2}',r'\lambda_i<x',r'x^{-b_4}'],
      18:[r'for all $b>0$',r'x_1^2\leq x_2',r'[x_1,x_1(1+x_1^b)]^d',r'[x_2,x_2(1+x_1^b)]^{D-d}',r'x_1^{B_0}',r'e^{-c_2x_1^{-d/2}}',r'\mathbb E_{\widetilde\Pi_\Lambda}',r'\lambda_i\leq x',r'e^{-c_4x^{b_4}}'],
      19:[r'\int_{M^\tau}',r'\varphi_{\Sigma(y)}(x-y)f(y)']}
    for n,parts in snippets.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    assert r'\frac12' not in s['D1'] and r'\frac1{\sqrt2}' not in s['D1']
    assert 'independent' not in s['D16']
    for n,label in [(4,'Definition 2.1'),(9,'Definition 2.2')]:assert m['D'+str(n)]['source_heading']==label and m['D'+str(n)]['source_kind']=='definition'
    for n in [16,17,18]:assert m['D'+str(n)]['source_kind']=='condition'
    a={k:v['statement_original'] for k,v in aux.items()}
    for part in [r'\frac dD\beta_0^{-1}',r'\frac{D-d}D\beta_\perp^{-1}',r'\alpha_0=\beta/\beta_0',r'\alpha_\perp=\beta/\beta_\perp']:assert part in a['A1'],part
    assert r'\tau/8' in a['A3'] and 'exponential map' in a['A3'] and r'\forall x_0\in M' in a['A3']
    assert r'\beta_M>4' in a['A4'] and 'constants appearing in the subsequent conditions do not' in a['A4']
    for part in [r'\delta=\delta_n\leq\tau/2',r'\omega>6\beta',r'\omega/\langle k,\alpha\rangle',r'\bar f_{\delta,x_0}',r'\bar f_{x_0,\delta}',r'\omega/\beta',r'0\leq\langle k,\alpha\rangle<\beta']:assert part in a['A5'],part
    assert 'log n' not in a['A5']
    assert r'-\log\Pi_K(K=x)\simeq x(\log x)^r' in a['A6'] and r'r=0,1' in a['A6']
    for part in [r'\Sigma(x)=O_x^\top\Delta_{\sigma,\delta}^2O_x',r'\sigma^{\alpha_0}\operatorname{Id}_d',r'\delta\sigma^{\alpha_\perp}\operatorname{Id}_{D-d}',r'T_x=T_{\operatorname{pr}_M(x)}M']:assert part in a['A7'],part
    assert 'independent and identically distributed' in a['A8'] and 'Lebesgue' in a['A8']
    assert 'triangular array' in a['A9'] and 'coordinate functions' in a['A11'] and 'bounded open subset' in a['A12']
    assert set(ambient['statement_local_bindings'])=={'T3.1','T3.4'}
    branches={(x['weight_family'],x['scale_family']):x['conditions'] for x in ambient['prior_condition_branches']}
    assert branches=={('MFM','partial'):['9','10','11'],('DPM','partial'):['10','11'],('MFM','hybrid'):['9','10','12','13'],('DPM','hybrid'):['10','12','13']}
    assert any(x['reference_kind']=='proof_only' and x['to_claim_id']==PID+'/T3.4' for x in ambient['source_claim_references'])
    assert len(ambient['unresolved_appendix_references'])==2
    for a in aux.values():assert set(a['depends_on'])<=set(m)
if __name__=='__main__':main()
