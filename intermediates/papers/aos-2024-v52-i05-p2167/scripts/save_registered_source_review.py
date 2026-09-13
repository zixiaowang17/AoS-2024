"""Validate frozen source-reviewed content independently of the census builder."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '44a127933d66ac09465676039b9055befaaf6aa90378ade1d18248ea847f80f8', 'source-passages.json': '515f2028bada676ea1b914342868014b195293ede3dbe50a6a94ecd6200c1d14', 'interface-extraction.json': 'c58dfba6828e13d7d0636daa167fc802a5f6b719b9a0346fab95e9cef9dd82b3', 'ambient-prerequisites.json': 'd99078b240a60e8d51c2723d4a3f79d15165203995f27b3c412f0650992ba28e', 'unfinalized-census.json': 'a7d75bbeaa26c8ffc470d3065dd80699d48203b9dbcb9311019f3bf93b4fb504', 'ranked-interfaces.json': '32189dc9f3194964d9e58e60bb6c1c18173ff73ee1ff836906cd03e5b097ad1e'}
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
    assert registered['version']=='2311.18613v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2311.18613'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert ir['printed_label_check']==[[5,'4.1','overview_statement'],[7,'5.8','overview_statement'],[7,'5.1','overview_statement'],[11,'3.1','formal_theorem'],[16,'4.1','formal_theorem'],[20,'5.1','formal_theorem'],[23,'5.4','formal_theorem'],[23,'5.7','formal_theorem'],[24,'5.8','formal_theorem']]
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==83
    assert paper['main_text_last_pdf_page']==25 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==9
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Reconstructed from the source scopes; no extraction/finalizer graph imported.
    raw={1:[],2:[1],3:[],4:[1],5:[1,2],6:[1,2],7:[],8:[1,7],9:[1],10:[1,2,8,9],11:[2,4],12:[2,3,4],13:[],14:[1],15:[14],16:[1,14,15],17:[16],18:[1,2,13,17],19:[16],20:[1,14,15],21:[20],22:[13,19,21],23:[2,15,19,21]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'4.1-overview':ids([4,5,6]),'5.8-overview':ids([4,5,10]),'5.1-overview':ids([1,2,4,8,9]),'3.1':ids([1,2,4,5,11,12,13]),'4.1':ids([1,2,4,5,17,18]),'5.1':ids([1,2,4,8,9]),'5.4':ids([1,2,4,5,8,9,11,13,19,21,22,23]),'5.7':ids([1,2,4,5,8,9,19,21]),'5.8':ids([1,2,4,5,8,9,19,21])}
    expected_reach={'4.1-overview':ids([1,2,4,5,6]),'5.8-overview':ids([1,2,4,5,7,8,9,10]),'5.1-overview':ids([1,2,4,7,8,9]),'3.1':ids([1,2,3,4,5,11,12,13]),'4.1':ids([1,2,4,5,13,14,15,16,17,18]),'5.1':ids([1,2,4,7,8,9]),'5.4':ids([1,2,4,5,7,8,9,11,13,14,15,16,19,20,21,22,23]),'5.7':ids([1,2,4,5,7,8,9,14,15,16,19,20,21]),'5.8':ids([1,2,4,5,7,8,9,14,15,16,19,20,21])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n]
    assert 'D14' not in expected_reach['3.1']|expected_reach['5.1']|expected_reach['4.1-overview']
    assert 'D12' not in expected_reach['5.4'] and 'D23' not in expected_reach['5.7']
    s={lid:a['statement_original'] for lid,a in m.items()}
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==12 and len(ambient['source_issues'])==14
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
        assert obj['evidence'] and all(1<=e['page']<=25 for e in obj['evidence'])
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
                assert all(1<=e['page']<=25 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
    counts=dict(theorems=9,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=9,interfaces=23,source_members=23,direct_theorem_uses=57,related_theorem_connections=86,unranked_auxiliary_passages=12)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Six formal Theorems and three bold labeled overview statements are preserved separately: nine source occurrences, six distinct printed theorem numbers. Heading enumeration excludes citations, Table 1 and proofs. Main text ends with the Discussion on page 25; supplementary and appendix bodies are excluded.',
      source_passages='Twenty-three entries and twelve supporting passages preserve Holder and Besov conventions, latent pushforwards, IPMs, GAN estimator, both model assumptions, separate manifold/density regularity, errors and coverings, wavelet formulas and all specified neural classes.',
      dependencies='Independent reconstruction gives 57 direct uses and 86 related connections. Existential overview classes and arbitrary classes in Theorem 3.1 do not acquire later network prerequisites. Interpolation Theorem 5.1 has no GAN/network dependencies. Uniform and candidate-specific discrimination errors remain distinct.',
      theorem_differences='The overview of 5.1 imposes density regularity on both maps; its formal statement imposes it only on g-star. Theorem 5.8 overview has gamma up to beta+1, while the formal statement prints tilde-beta+1. Subsequent broader-range prose is retained separately. Theorem 5.4 preserves its untilded critical indicator.',
      unresolved_constructions='Exact hat-wavelet implementations and the chi-numerical regularity formula live in appendices. Only the main-text descriptions, bounds, formulas and references are retained. The census does not substitute manifold regularity for the numerical condition or claim a fully specified executable neural construction.',
      source_issues='Fourteen source scope/convention issues remain explicit, including the d=1 zero denominator, delta=0 logarithms, network coefficient/index mismatches, scaling-wavelet name reversal, Holder/Besov endpoints and exact optimizer selections. Original statements are not corrected or certified as proofs.',
      names_and_highlights='Every entry has literal source terms, faithful model/definition/source-passage labels and source-matching selectors. All 86 theorem connections have explicit same-paper definition paths and explanations. Shared terminology does not merge distinct error or network definitions.',
      reproduction='The six content JSON artifacts reproduce byte for byte from the retained per-paper scripts. Independent heading enumeration, source-specific formula checks, graph reconstruction, frozen artifact hashes and schema validation protect the reviewed extraction.')
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=[4,5,6,7,10,11,12,13,14,15,16,17,20,22,23,24,25],visually_reviewed_crops=[]))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=83,main_text_last_pdf_page=25,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent small-cap formal and bold overview heading enumeration, with visual comparison of all nine complete labeled statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv v2 dated March 2025, identified by version and hash; no claim of equivalence to the final 2024 journal article.','Original source conventions and ambiguities are retained separately; no appendix material is used in the census.','Source and schema validation do not certify mathematical proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=83,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(s,m,aux,ambient):
    snippets={
      1:[r'\lfloor\eta\rfloor:=\max',r'\min\{1,\|x-y\|^{\eta-\lfloor\eta\rfloor}\}',r'\max_i\sum_{|\nu|\le\lfloor\eta\rfloor}',r'+\sum_{|\nu|=\lfloor\eta\rfloor}','Hölder space'],
      2:[r'U\sim\mathcal U([0,1]^d)',r'\forall f\in\mathcal H_1^0',r'\int_{[0,1]^d}f(g(u))d\lambda^d(u)'],
      3:[r'\sup_{D\in\mathcal D}\mathbb E_\mu[D(X)]-\mathbb E_\nu[D(g(Z))]','pushforward measure'],
      4:[r'\sup_{D\in\mathcal H_1^\gamma}',r'\mathbb E_{X\sim\mu,Y\sim\nu}[D(X)-D(Y)]'],
      5:[r'\operatorname*{arg\,min}_{g\in\mathcal G}',r'\frac1n\sum_{i=1}^nD(X_i)-D(g(U_i))',r'\mathcal D\subset\mathcal H_1^\gamma',r'\widehat g_{\#U}'],
      6:['There exists',r'\mu=g^\star_{\#U}'],
      7:[r'd(x,\mathcal M)<\epsilon','largest',r'\pi_{\mathcal M}'],
      8:['injective',r'd$-dimensional submanifold','larger than $K^{-1}$'],
      9:[r'\inf_{u\in[0,1]^d}',r'\lambda_{\min}((\nabla g(u))^\top\nabla g(u))^{1/2}\ge K^{-1}'],
      10:['$K$-manifold and $K$-density',r'\mu=g^\star_{\#U}'],
      11:[r'\Delta_{\mathcal G}:=\inf_{g\in\mathcal G}',r'd_{\mathcal H_1^\gamma}'],
      12:[r'\Delta_{\mathcal D}:=\sup_{g\in\mathcal G}',r'-d_{\mathcal D}(g_{\#U},g^\star_{\#U})'],
      13:[r'\operatorname*{arg\,min}\{|A|',r'\exists f_\epsilon\in A',r'\|f-f_\epsilon\|_\infty\le\epsilon'],
      14:['scaling and wavelet function respectively',r'l\in\{1,\ldots,2^p-1\}',r'2^{jp/2}',r'\varphi_j^{\mathrm{per}}',r'\psi_{j0}^{\mathrm{per}},\psi_{j1}^{\mathrm{per}}',r'l\in\{1,\ldots,2^d\}',r'z\in\{0,\ldots,2^j-1\}^d'],
      15:[r'\lfloor\beta\rfloor+3>s',r'2^{jq_2(s+p/2-p/q_1)}(1+j)^{bq_2}',r'\alpha_f(w)',r'\mathcal S\prime' if False else r"\mathcal S'(\mathbb R^p)",r'\|f\|_{\mathcal B_{q_1,q_2}^{s,b}}\le C'],
      16:[r'\|\varphi-\widehat\varphi\|_{\mathcal H^{\lfloor\beta\rfloor+2}}\le CL^{-1}','(A.10)',r'\widehat\alpha(j,l,w)_i',r'|\widehat\alpha(j,l,z)_i|\le C_\eta K2^{-j(\eta+d/2)}',r'\sum_{l=1}^{2^d}'],
      17:[r'L^{-1}=n^{-1}',r'\widehat{\mathcal F}_{\mathrm{per}}^{\beta+1,n^{-\frac1{2\beta+d}}}'],
      18:[r'\mathcal G_{1/n}',r"D(g'(u))",'not really computable in practice'],
      19:['Appendix Section E.1',r'\chi','numerical regularity condition',r'g\in\widehat{\mathcal F}_{\mathrm{per}}'],
      20:['(A.4) and (A.5)',r'L^{-1}=n^{-1}',r'\sum_{l=1}^{2^p}',r'\{-K2^j,\ldots,K2^j\}^p',r'C_\eta K2^{-j(\eta+p/2)}'],
      21:[r'\widetilde\beta+1:=(\beta+1)\wedge d/2',r'\widetilde\delta_n:=n^{-\frac1{2\widetilde\beta+d}}',r'\widehat{\mathcal F}^{\widetilde\beta+1,\widetilde\delta_n}'],
      22:[r'\sup_{g\in\mathcal G}|(\{D\circ g\mid D\in\mathcal D\})_\epsilon|','largest'],
      23:[r'\operatorname*{arg\,max}_{D\in\mathcal B_{\infty,\infty}^{\widetilde\beta+1}(C)}',r'\overline D_g\in\operatorname*{arg\,min}',r'\|D-D_g^\star\|_{\mathcal B_{\infty,\infty}^0}',r'\Delta_{\mathcal D}^g',r'-(\overline D_g(g(U))-\overline D_g(g^\star(U)))']}
    for n,parts in snippets.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    assert m['D6']['source_kind']==m['D10']['source_kind']=='assumption'
    assert m['D8']['source_heading'].startswith('Definition 2.1(i)') and m['D9']['source_heading'].startswith('Definition 2.1(ii)')
    assert m['D19']['source_kind']=='source_passage'
    assert 'regularity condition' not in s['D6']
    assert r'\mathcal H' not in s['D19'] and 'chi-numerical' not in s['D17']
    assert 'd/2' not in s['D17'] and r'\widetilde\beta' in s['D21']
    assert 'Model 2' not in s['D20'] and 'Model 2' not in s['D21']
    a={k:v['statement_original'] for k,v in aux.items()}
    checks={1:[r'n\ge1',r'p\ge2',r'd\in\{1,\ldots,p\}',r'\beta\ge1',r'K>1'],2:[r'\mathbb T^d=\mathbb R^d/\mathbb Z^d','unknown'],3:[r'\le W_1(\mu,\nu)\le(2K+1)', 'compact domains'],4:['only depend on $p,d,\beta$ and $K$'.replace('\b','\\b')],5:['Hausdorff measure','smallest eigenvalue'],6:['two closed sets'],7:['empty boundary',r'd<p'],8:[r'\eta\in(0,\beta+1)',r'\langle f_i,\psi_{jlz}^{\mathrm{per}}\rangle_{L^2}=0',r'\forall j\ge\log_2(\delta^{-1})'],9:['periodised Besov spaces'],10:[r'\gamma\in[1,\infty)',r'\beta+1\ge d/2'],11:[r'\operatorname{supp}(f)\subset B^p(0,K)'],12:[r'O(n^d\log(n))',r'O(n^{d+1}\log(n))','depth $O(1)$','Section A.2.2']}
    for n,parts in checks.items():
        for part in parts:assert part in a['A'+str(n)],(n,part)
    assert set(ambient['statement_local_bindings'])=={'T4.1-overview','T5.8-overview','T5.1-overview','T3.1','T4.1','T5.1','T5.4','T5.7','T5.8'}
    issues={x['issue_id'] for x in ambient['source_issues']}
    assert issues=={'overview-density-scope','overview-gamma-range','delta-endpoint-and-critical-indicator','low-dimension-resolution','optimizer-and-cover-choice','wavelet-conventions','network-indices-and-coarse-mode','appendix-network-construction','appendix-numerical-condition','holder-source-conventions','gan-summation-scope','discriminator-latent-variable','network-versus-holder','endpoint-and-log-scope'}
    refs=ambient['source_claim_references'];assert sum(x['reference_kind']=='overview_relation' for x in refs)==3
    assert sum(x['reference_kind']=='proof_only' for x in refs)==4 and sum(x['reference_kind']=='appendix_reference_unresolved' for x in refs)==2
    for obj in aux.values():assert set(obj['depends_on'])<=set(m)
if __name__=='__main__':main()
