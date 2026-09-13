"""Validate frozen source-reviewed content independently of the census builder."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': 'd94e0a937373f014be400b0558abaa0e5168d35d149d796ae6c4757b7f5e3fff', 'source-passages.json': '5e096fc89efdb4eacd280c4b7ea429b1d1a00de8aab6ca8e72c0998fcefb55ac', 'interface-extraction.json': 'fca227a4859b37a9c3a82e40e17dc5b820379831e0c216ac18bd93f94ffd6d6c', 'ambient-prerequisites.json': 'd68594d7d2e1922319f79805727607e2d256c3cbc792cded92399deda3b61c67', 'unfinalized-census.json': '83e0c29cd620a673303965efaf8ee2a3bad1501227820d8b14a2e8a5a1ae0b15', 'ranked-interfaces.json': 'ea667d62bf12139989cb7186f2ea1dd474be5b0193a295dd2d74c837f0cac35d'}
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
    assert registered['version']=='2309.05482v3.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2309.05482'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert ir['printed_label_check']==[[9,'3.3'],[12,'4.4']]
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==36
    assert paper['main_text_last_pdf_page']==28 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==2
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Reconstructed from the source scopes; no extraction/finalizer graph imported.
    raw={1:[],2:[1],3:[1],4:[3],5:[3],6:[1],7:[3,4],8:[6,7],9:[8],10:[3,4,8],11:[3,4,10]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'3.3':ids([1,2,3,5,6]),'4.4':ids([1,2,9,11])}
    expected_reach={'3.3':ids([1,2,3,5,6]),'4.4':ids([1,2,3,4,6,7,8,9,10,11])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n]
    assert not ids([4,7,8,9,10,11])&expected_reach['3.3']
    assert 'D5' not in expected_reach['4.4']
    s={lid:a['statement_original'] for lid,a in m.items()}
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==11 and len(ambient['source_issues'])==11
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
    counts=dict(theorems=2,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=2,interfaces=11,source_members=11,direct_theorem_uses=9,related_theorem_connections=15,unranked_auxiliary_passages=11)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Both complete main-text Theorems, 3.3 and 4.4, are preserved. Independent bold-heading enumeration covers pages 1-27 and the main-text prefix of page 28. The strict error bound and both randomness sources in 3.3 remain unchanged; 4.4 retains the printed Lemma 4.1 reference.',
      source_passages='Eleven indexed original entries and eleven auxiliary passages preserve the linear model, exchangeable errors, row permutations, projections, generic transferability, p-value recipe, concrete PALMRT statistics, test inversion, CI target, critical-value sweep and all Algorithm 2 instructions. Supporting coefficients, roots, partitions and counting formulas are archived in full.',
      dependencies='Independent graph reconstruction confirms 9 direct uses and 15 related connections. Theorem 3.3 replaces the Algorithm 1 statistic step with generic T, so it has no projection or concrete PALMRT dependency. Theorem 4.4 uses the CI target and construction but does not acquire Condition 3.1 through proof reasoning.',
      source_discrepancies='The printed Lemma/Corollary and Algorithm references, c_b4 projection, overlapping interval indicators, coincident-root counts, incomplete partition and index range, coverage comment and critical-index boundary handling are retained separately. No source formula is repaired by the census.',
      scope='The standing exchangeability condition is linked using Assumption 1.1 and the Section 3 opener. The uniform-draw theorem wording is not rewritten to add the independence used by its proof. The CI is the interval hull of a strict superlevel set; the optional normal-approximation fallback is outside the theorem guarantee.',
      names_and_highlights='All eleven entries use literal source terms, faithful source headings and meaning-bearing selectors. Every related theorem has a source-specific explanation. Assumptions, conditions, Corollary passages and algorithms are not relabeled as numbered definitions.',
      reproduction='All six JSON content artifacts reproduce byte for byte from retained per-paper scripts. Frozen hashes and source-specific checks protect the reviewed content. Rebuilding is not a new semantic review or a proof of the original mathematical assertions.')
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=[2,4,6,8,9,11,12,13,28],visually_reviewed_crops=['theorem-3-3.png','lemma-4-3.png','algorithm-2.png']))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=36,main_text_last_pdf_page=28,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-heading enumeration and visual comparison of both complete Theorems.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv v3 manuscript identified by version and hash; no claim of byte-equivalence to the final journal article.','Original source conventions and ambiguities are retained separately; no appendix material is used in the census.','Source and schema validation do not certify mathematical proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=36,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(s,m,aux,ambient):
    snippets={
      1:[r'y_i=x_i\beta+\mathbf z_i^\top\theta+\epsilon_i','independent of'],
      2:['exchangeable with in law'],
      3:[r'vector $(1,\ldots,n)$','row-permuted versions'],
      4:[r'H^*',r'H^{z_\pi z}',r'H^{x z z_\pi}','column space'],
      5:['For any permutations',r'\varepsilon_\sigma',r'\pi_1\circ\sigma^{-1}',r'\pi_2\circ\sigma^{-1}'],
      6:[r'\frac12\mathbb 1\{T_{b0}=T_{0b}\}',r'\mathbb 1\{T_{b0}>T_{0b}\}',r'\frac{1+\sum_{b=1}^B\omega_b}{B+1}',r'H_0:\beta=0'],
      7:[r'T_{original}=\|(I-H^{x_\pi z z_\pi})y\|_2^2',r'T_{perm}=\|(I-H^{x z z_\pi})y\|_2^2'],
      8:['Algorithm 2',r'y-x\beta',r'\mathbb 1\{T_{0b}(\beta)<T_{b0}(\beta)\}',r'\frac12\mathbb 1\{T_{0b}(\beta)=T_{b0}(\beta)\}'],
      9:[r'\inf\{\beta:f(\beta)>\alpha\}',r'\sup\{\beta:f(\beta)>\alpha\}',r'\min_\beta\mathbb P[\beta\in\mathrm{CI}_\alpha]>1-2\alpha'],
      10:[r'\cup_{b\in A_1}\{s_b,u_b\}',r't_l^+','infinitesimally larger',r'\frac12(m_{l+1}^s-m_{l+1}^u)',r'\frac12(m_l^s-m_l^u)'],
      11:[r'coverage level $1-\alpha$','Lemma 4.3',r'\gamma<0',r'\mathrm{CI}_\alpha=(-\infty,\infty)',r'\mathrm{CI}_\alpha=\emptyset',r'\max(f_{A_1}(.))\leq\gamma',r'\beta_{min}=\min\{t_l:f_{A_1}(t_l)\vee f_{A_1}(t_l^+)>\gamma\}',r'\beta_{max}=\max\{t_l:f_{A_1}(t_l)\vee f_{A_1}(t_{l-1}^+)>\gamma\}']}
    for n,parts in snippets.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    assert r'H^' not in s['D6'] and 'PALMRT' not in s['D5']
    assert 'independent' not in s['D2'] and 'Gaussian' not in s['D2']
    assert m['D2']['source_kind']=='assumption' and m['D2']['source_heading']=='Assumption 1.1'
    assert m['D5']['source_kind']=='condition' and m['D5']['source_heading']=='Condition 3.1'
    assert m['D9']['source_kind']=='source_passage' and m['D9']['source_heading']=='Corollary 4.1'
    assert [int(x) for x in re.findall(r'(?m)^(\d+):',s['D11'])]==list(range(1,20))
    a={k:v['statement_original'] for k,v in aux.items()}
    assert 'identity permutation' in a['A1'] and r'\sigma\circ\sigma^{-1}=\sigma^{-1}\circ\sigma=\pi_0' in a['A2']
    assert 'any design and exchangeable noise' in a['A3']
    for part in [r'c_{b4}=\|(I-H^{x_\pi z_{\pi_b}z})y\|_2^2',r'\frac12\mathbb 1\{\beta\in[s_b,u_b]\}+\mathbb 1\{\beta\in(s_b,u_b)\}',r'c_{b1}=0',r'c_{b1}>0',r'c_{b2}^2\geq c_{b1}(c_{b3}-c_{b4})',r'\frac{c_{b2}-\sqrt{c_{b2}^2-c_{b1}(c_{b3}-c_{b4})}}{c_{b1}}',r'\frac{c_{b2}+\sqrt{c_{b2}^2-c_{b1}(c_{b3}-c_{b4})}}{c_{b1}}']:assert part in a['A4'],part
    for part in [r'\{0,\ldots,B\}',r'A_2=\{b:c_{b1}=0,c_{b3}<c_{b4}\}',r'A_3=\{b:c_{b1}=0,c_{b3}=c_{b4}\}',r'\sum_{b\in A_1}\omega_b(\beta)',r'(B+1)\alpha-1-|A_2|-\frac12|A_3|:=\gamma']:assert part in a['A5'],part
    for part in [r'\frac12\#\{b:s_b\leq\beta\}',r'+\frac12\#\{b:s_b<\beta\}',r'-\frac12\#\{b:u_b\leq\beta\}',r'-\frac12\#\{b:u_b<\beta\}']:assert part in a['A6'],part
    assert 'not always guaranteed' in a['A7'] and r'H^{x_{\pi_2}z_{\pi_2}z_{\pi_1}}' in a['A8']
    assert 'independently and uniformly' in a['A10'] and 'normal approximation' in a['A11']
    assert set(ambient['statement_local_bindings'])=={'T3.3','T4.4'}
    assert any(x['reference_kind']=='proof_only' and x['to_source_label']=='Appendix A' for x in ambient['source_claim_references'])
    for a in aux.values():assert set(a['depends_on'])<=set(m)
if __name__=='__main__':main()
