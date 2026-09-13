"""Verify frozen source-reviewed content and independently reconstructed dependency scopes."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': '28273014aca487001d80d6df675ac352a55176d25069fb581d1d807cc6d5e745', 'source-passages.json': '8c68c8bd537b1df51b3779c60dbbae92895affeeafc2bfb50c17229ba0e0d6ac', 'interface-extraction.json': '6eb527c08ed2dbe61e2500969bf59b5317c5141fefb69e56e2c49dcc3003bc60', 'ambient-prerequisites.json': '8f3b6fa2d76d9708a7edbf2a67b0a73d3689fdda11b6aafaa46e728cd3bfe51b', 'unfinalized-census.json': '85fe5f5b40d6351539cba39420925dc95b18d3b709074a74a6503c2d511a9f99', 'ranked-interfaces.json': 'f199e2a225ff4d67ae130a8768c2b66e68551258c091d82fc03c4a665a840c47'}
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
    assert registered['version']=='2303.03092v3.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2303.03092'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==65
    assert paper['main_text_last_pdf_page']==20 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==4
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Reconstructed from original definitions and theorem clauses; no builder graph imported.
    raw={1:[],2:[1],3:[],4:[],5:[3,4],6:[],7:[4,6],8:[],9:[6,8],10:[6,8,27],11:[9,10],12:[4,6,7],13:[11],14:[3],15:[3],16:[14],17:[2],18:[2],19:[5,18],20:[2],21:[5],22:[15,18,20,21],23:[1,18,21],24:[1,15],25:[15,23],26:[1],27:[8]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'4.2':ids([12,14,15,18,19,20,21,22,26]),'4.3':ids([11,15,16,17,18,19,22,23,25,26]),'4.4':ids([1,11,15,16,17,18,19,22,25,26]),'4.5':ids([13,15,16,17,19,22,24,26])}
    expected_reach={'4.2':ids([1,2,3,4,5,6,7,12,14,15,18,19,20,21,22,26]),'4.3':ids([1,2,3,4,5,6,8,9,10,11,14,15,16,17,18,19,20,21,22,23,25,26,27]),'4.4':ids([1,2,3,4,5,6,8,9,10,11,14,15,16,17,18,19,20,21,22,23,25,26,27]),'4.5':ids([1,2,3,4,5,6,8,9,10,11,13,14,15,16,17,18,19,20,21,22,24,26,27])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([8,9,10,11,13,16,17,23,24,25,27])&expected_reach['4.2']
    assert not ids([7,12])&(expected_reach['4.3']|expected_reach['4.4']|expected_reach['4.5'])
    assert not ids([23,25])&expected_reach['4.5']
    assert 'D24' not in expected_reach['4.3']|expected_reach['4.4']
    assert 'D13' not in expected_reach['4.2']|expected_reach['4.3']|expected_reach['4.4']
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
        assert obj['evidence'] and all(1<=e['page']<=20 for e in obj['evidence'])
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
                assert all(1<=e['page']<=20 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
    counts=dict(theorems=4,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=4,interfaces=27,source_members=27,direct_theorem_uses=37,related_theorem_connections=85,unranked_auxiliary_passages=12)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Four complete main-text Theorems, 4.2–4.5. Independent bold-heading enumeration excludes citations, Propositions, Conditions, Definitions and Remarks. Preserve all sample-size bounds, both T4.4 branches and the full T4.5 lambda interval.',
      source_passages='Twenty-seven source entries and twelve supporting passages preserve the common conditional-mean model, true residuals, population and empirical risks, focused support gates, EILLS and penalized objectives, balanced sampling, Conditions4.1–4.6, spurious-variable set and threshold/signal formulas.',
      dependencies='Independent graph reconstruction confirms 37 direct uses and 85 related connections. Population and empirical risks are separate. T4.2 has no empirical-risk or sub-Gaussian-tail requirement. Statistical theorems refer to the definition of gamma*, not the population objective or the strong-convexity conclusion.',
      scope='T4.4 imports screening sample conditions only in its improved-bound branch. T4.3 provides screening rather than exact support recovery; T4.5 uses the l0-penalized global minimizer and its own high-dimensional sample regime. Balanced observations, uniform weights and cross-environment independence are retained.',
      source_issues='Twelve source notes retain the x-versus-beta typo in (3.8), centered raw-moment covariance convention, pooled whitening, empty support/G conventions, unused c4 and star notation, feasible penalty range and global-minimizer computational limits. Original quotations are not repaired or proof-certified.',
      names_and_highlights='All entries have source-backed names, source kinds, original labels and literal highlight selectors. All 85 theorem connections have source-specific explanations and independently checked same-paper paths.',
      reproduction='The six content JSON artifacts reproduce byte for byte using seven retained per-paper scripts. Frozen hashes, source identity, heading enumeration, formula checks, dependency reconstruction and schema validation pass.')
    reviewed_pages=[6,8,9,10,11,12,13,14,15,16,20]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[]))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=65,main_text_last_pdf_page=20,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent small-cap heading enumeration and visual comparison of all four complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark','Conjecture'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2303.03092v3 dated 29 Nov 2024, pinned by SHA-256. No substitution with another paper version.','Appendix bodies excluded. Unequal-weight extensions, Gumbel approximations and practical tuning guidance are deferred to appendices and excluded.','Source and schema validation do not certify proofs or resolve the explicitly recorded source ambiguities.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=65,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))

def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:[r'\operatorname{Var}_\mu[y\mid\mathbf x_{S^*}]\le\sigma^2',r'\mathbb E_\mu[x_j^2]\le\sigma^2',r'\operatorname{supp}(\boldsymbol\beta^*)'],
2:[r'y^{(e)}-\mathbb E[y^{(e)}\mid\mathbf x_{S^*}^{(e)}]',r'y_i^{(e)}-(\boldsymbol\beta^*)^\top\mathbf x_i^{(e)}'],
3:[r'\mathbf\Sigma^{(e)}=\mathbb E[\mathbf x^{(e)}(\mathbf x^{(e)})^\top]'],
4:[r'R^{(e)}(\boldsymbol\beta)=\mathbb E[|y^{(e)}-\boldsymbol\beta^\top\mathbf x^{(e)}|^2]'],
5:['positive definite',r'\operatorname{supp}(\boldsymbol\beta)\subseteq S','is a subset of'],
6:[r'\sum_{e\in\mathcal E}\omega^{(e)}=1',r'\omega^{(e)}>0'],
7:[r'\mathbb1\{\beta_j\ne0\}',r'\frac{\omega^{(e)}}4|\nabla_jR^{(e)}(\boldsymbol\beta)|^2'],
8:[r'\frac1{n^{(e)}}\sum_{i=1}^{n^{(e)}}','drawn i.i.d.'],
9:[r'\mathbb1\{\beta_j\ne0\}',r'\left|\widehat{\mathbb E}[x_j^{(e)}(y^{(e)}-\boldsymbol\beta^\top\mathbf x^{(e)})]\right|^2'],
10:[r'\frac{\omega^{(e)}}{n^{(e)}}',r'\widehat R^{(e)}(\boldsymbol\beta)'],
11:[r'\widehat{\boldsymbol\beta}_Q',r'\widehat R(\boldsymbol\beta;\omega)+\gamma\widehat J(\boldsymbol\beta;\omega)'],
12:[r'R(\boldsymbol\beta;\omega)+\gamma J(\boldsymbol\beta;\omega)',r'y^{(e)}-\mathbf x^\top\mathbf x^{(e)}'],
13:[r'\ell_0',r'\widehat{\boldsymbol\beta}_L',r'\lambda\|\boldsymbol\beta\|_0'],
14:[r'\frac1{|\mathcal E|}\sum_{e\in\mathcal E}\mathbf\Sigma^{(e)}'],
15:[r'\kappa_L\in(0,1]',r'\kappa_U\in[1,\infty)',r'\kappa_L\mathbf I_p\preceq\mathbf\Sigma^{(e)}\preceq\kappa_U\mathbf I_p'],
16:[r'\mathbf v^\top\mathbf\Sigma^{-1/2}\mathbf x^{(e)}',r'\frac{\sigma_x^2}2\cdot\|\mathbf v\|_2^2'],
17:[r'\lambda\in\mathbb R',r'\mathbb E[e^{\lambda\varepsilon^{(e)}}]\le e^{\frac12\lambda^2\sigma_\varepsilon^2}'],
18:[r'\sum_{e\in\mathcal E}\mathbb E[x_j^{(e)}\varepsilon^{(e)}]\ne0','pooled linear spurious variable'],
19:[r'For any $S\subseteq[p]$',r'S\cap G\ne\varnothing',"\\boldsymbol\\beta^{(e',S)}"],
20:[r'\|\frac1{|\mathcal E|}\sum_{e\in\mathcal E}\mathbb E[\varepsilon^{(e)}\mathbf x_S^{(e)}]\|_2^2'],
21:[r'\boldsymbol\beta^{(e,S)}-\bar{\boldsymbol\beta}^{(S)}',r'\bar{\boldsymbol\beta}^{(S)}=\frac1{|\mathcal E|}'],
22:[r'(\kappa_L)^{-3}',r'\sup_{S:S\cap G\ne\varnothing}(b_S/\bar d_S)'],
23:[r'\min_{j\in S^*}|\beta_j^*|^2',r'\min_{S\subseteq[p],S\cap G\ne\varnothing}\bar d_S'],
24:[r's^*=|S^*|',r'\log(|\mathcal E|)\le C\log p',r'(\kappa_L\beta_{\min})^{-1}\sqrt{(s^*+\log p)s^*\log p}',r'1+1/(\kappa_L\beta_{\min}^2)'],
25:[r's_+^{-0.5}+s_+^{-1}+(\gamma\kappa_Ls_-)^{-0.5}',r's_+^{-1}+(\gamma\kappa_Ls_-)^{-1}+1'],
26:['also independent',r'\omega^{(e)}\equiv1/|\mathcal E|',r'\mathcal U_{\boldsymbol\beta^*,\sigma^2}'],
27:[r'\widehat R^{(e)}(\boldsymbol\beta)=\widehat{\mathbb E}[|y^{(e)}-\boldsymbol\beta^\top\mathbf x^{(e)}|^2]']}
    for n,parts in checks.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    assert r'\widehat' not in s['D4'] and r'\widehat' in s['D27']
    assert r'\mathbf\Sigma^{(e)}' not in s['D16']
    assert all(m['D'+str(n)]['source_kind']=='condition' for n in [15,16,17,19,24,26])
    assert all(m['D'+str(n)]['source_kind']=='theorem_excerpt' for n in [20,21,22,23,25])
    a={k:v['statement_original'] for k,v in aux.items()}
    for n,parts in {1:['conditional expectation invariant','with support set'],2:['linear least squares invariant',r'\operatorname{supp}(\boldsymbol\beta)\subseteq S'],3:['converse is false'],4:[r'n^{(e)}\equiv n','Appendix A'],5:[r'\mathbb E[\mathbf x^{(e)}]=0'],6:[r'G\ne\varnothing'],7:['bias mean',r'S\supseteq S^*'],8:['exponentially'],9:['future studies'],10:[r'x_j\ne0'],11:[r'\frac pn'],12:['running the least squares']}.items():
        for part in parts:assert part in a['A'+str(n)],(n,part)
    for o in aux.values():
        assert set(o['depends_on'])<=set(m)
        for e in o['evidence']:
            if e['page']==20:assert e['before_main_text_end']
    assert set(ambient['statement_local_bindings'])=={'T4.2','T4.3','T4.4','T4.5'}
    assert {x['issue_id'] for x in ambient['source_issues']}=={'population-loss-typo','balanced-sampling','pooled-whitening','focused-support-gate','global-minimizers','empty-support-and-empty-g','pooled-spuriousness','screening-versus-exact-selection','conditional-improved-bound','source-constants-and-stars','penalty-feasibility','conditional-mean-versus-linear-invariance'}
    refs=ambient['source_claim_references'];assert sum(x['reference_kind']=='definition_reference' for x in refs)==3
    assert sum(x['reference_kind']=='assumption_reference' for x in refs)==1
    assert sum(x['reference_kind']=='proof_only' for x in refs)==1
if __name__=='__main__':main()
