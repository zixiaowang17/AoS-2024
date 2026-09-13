"""Check frozen reviewed content independently of the extraction graph and builder."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={
 'theorem-inventory.json':'e095eac5b303dead90e1a454a6b97bf1f5ac0e3e6072c5659341ef74f8981364',
 'source-passages.json':'ad429c3e1411583e288890e9a502922febe47cf6f40f0d2cb6a172116484f6cf',
 'interface-extraction.json':'78ff11ce96765972a543c031d405526c5ab3d2d68430ec5a35916dcc421481cf',
 'ambient-prerequisites.json':'71d5a8088d69f103e7d67471a989b2d92cf556358d8ac6f8021100cc99cc72ea',
 'unfinalized-census.json':'f2329752ce630cc3ea554446a9f22f261b7dfbf04a2ca540f41c4fff3e899e61',
 'ranked-interfaces.json':'15aff2f3c091fcd227e4857883332ed262cdcd1cdf7b39297e6098c0a54f8fef'}
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
    assert registered['version']=='2011.08661v3.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2011.08661'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert ir['printed_label_check']==[[10,'2'],[11,'3'],[13,'4'],[14,'5']]
    assert paper['source_url']==URL=='https://arxiv.org/pdf/2011.08661v3'
    assert paper['pdf_pages']==registered['pdf_pages']==67 and paper['main_text_last_pdf_page']==27
    assert paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==4
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independently reconstructed source graph; no extraction/finalizer module is imported.
    raw={1:[],2:[1],3:[1],4:[1],5:[],6:[1,5],7:[6],8:[4,6],9:[1],10:[5,6,9],12:[8,9],13:[9,10,12],14:[1,10,13],15:[1],16:[1],17:[7],18:[1],19:[4],21:[7,9,10,12],22:[6,8,13],23:[2,4,6,19],24:[9,14],25:[8,13,21,24],26:[1,10,18,24,25],27:[7],28:[19]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'2':ids([3,6,7,8,9,13,14,15,16,17,18,19,21,22]),'3':ids([2,3,4,6,7,8,9,13,14,15,16,17,19,21,22,23]),'4':ids([3,6,8,15,16,17,18,24,25,26,27,28]),'5':ids([2,3,4,6,7,8,12,15,16,17,19,23,24,25])}
    expected_reach={'2':ids([1,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,21,22]),'3':ids([1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,19,21,22,23]),'4':ids([1,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,21,24,25,26,27,28]),'5':ids([1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,19,21,23,24,25])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n]
    assert 'D2' not in expected_reach['2']|expected_reach['4']
    assert 'D18' not in expected_reach['3']|expected_reach['5']
    assert not ids([26,27,28]) & expected_reach['5']
    assert not ids([24,25,26,27,28]) & (expected_reach['2']|expected_reach['3'])
    s={lid:a['statement_original'] for lid,a in m.items()}
    snippets={1:['i.i.d. copies',r'\mathbf X\in\mathbb R^{n\times p}'],2:[r'\tau:=\mathbb E\{Y(1)-Y(0)\}',r'Y=Y(T)'],3:[r'\{Y(1),Y(0)\}',r'T\mid X'],4:[r'r_t(x)=\mathbb E\{Y(t)\mid X=x\}'],5:[r'\{1+\exp(-u)\}^{-1}'],6:[r'\pi(x)=\psi(x^\top\gamma)',r'c_\pi<\pi(X)<1-c_\pi','almost surely'],7:[r's:=|\{j:\gamma_j\ne0\}|'],8:[r'\{1-\pi(x)\}r_1(x)+\pi(x)r_0(x)'],9:['independent auxiliary datasets','independent of the main dataset',r'n_A',r'n_B'],10:[r'\mathcal D_B',r'\hat\pi(x)=\psi(x^\top\hat\gamma)','default option'],12:[r'\tilde\mu',r'\mathcal D_B'],13:[r'\operatorname{argmin}_{\boldsymbol\mu\in\mathbb R^n}',r'\frac1{n_A}\mathbf X_A^\top',r'\frac1n\mathbf X^\top',r'\widehat{\boldsymbol\mu}=\mathbf0','no feasible'],14:[r'\frac{T_i(Y_i-\hat\mu_i)}{\hat\pi_i}',r'\frac{(1-T_i)(Y_i-\hat\mu_i)}{1-\hat\pi_i}'],15:[r'\mathbb EY(t)',r'\alpha^2\sigma_Y^2/2',r'\max_{t=0,1}|\mathbb EY(t)|\leq m_Y'],16:[r'\mathbb EZ=0',r'\|u\|_2=1',r'\alpha u^\top Z'],17:[r'\log(p)/n=a_n',r'p\geq2',r's\geq1'],18:[r'\frac1n\sum_{i=1}^n\mathbb E\{Y_i(1)-Y_i(0)\mid X_i\}'],19:[r'\varepsilon(t):=Y(t)-r_t(X)',r'\varepsilon_i(t)=Yi'],21:[r'\|\hat\gamma-\gamma\|_1',r'\|\hat\gamma-\gamma\|_2',r'c_{\hat\pi}\leq\hat\pi_{Ai}',r'\mathcal D_B',r'<c_{\tilde\mu}',r'\alpha^2c_{\tilde\mu}^2/2'],22:[r'(\hat\mu_i-\mu_{\mathrm{ORA},i})^2',r'\pi_i(1-\pi_i)'],23:[r'r_1(X)-r_0(X)-\tau',r'\frac{T\varepsilon(1)}{\pi(X)}'],24:['multiple of $3$',r'\mathcal D_{j+1}',r'\mathcal D_{j+2}',r'\frac13('],25:[r'\mathbb R^{n/3}',r'\Omega_j(',r'(\widehat{\boldsymbol\mu}_1,\widehat{\boldsymbol\mu}_2,\widehat{\boldsymbol\mu}_3)'],26:[r'\frac3n\sum_{i\in I_j}',r'-\widehat\tau_{\mathrm{DIPW},j}',r'(\hat\sigma_1+\hat\sigma_2+\hat\sigma_3)/\sqrt3',r'z_\alpha'],27:[r's=b_n\sqrt n/\log p'],28:[r'\min_{t=0,1}\operatorname{Var}(\varepsilon(t))\geq\sigma_\varepsilon^2']}
    snippets[19][-1]=r'\varepsilon_i(t)=Y_i(t)-r_t(X_i)'
    for n,parts in snippets.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    assert 'tau' not in s['D4'] and 'positive definite' not in s['D16']
    for n in [3,6,15,16,17,27,28]:assert m['D'+str(n)]['source_kind']=='assumption'
    for n in [1,9,12,25]:assert m['D'+str(n)]['source_kind']=='source_passage'
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==14 and len(ambient['source_issues'])==12
    assert r'\frac{T_iY_i(1-\hat\pi_i)}{\hat\pi_i}' in aux['A3']['statement_original']
    assert r'n=n_A' in aux['A6']['statement_original']
    assert r'\mathcal D:=(\mathbf X,\mathcal D_A,\mathcal D_B)' in aux['A7']['statement_original']
    assert r'\frac{\mathbb E\{\varepsilon_i(1)^2\mid X_i\}}{\pi_i}' in aux['A8']['statement_original']
    assert r'\pi_i' not in aux['A9']['statement_original']
    assert r'\right|^3' in aux['A10']['statement_original'] and r'r_1(X)-r_0(X)-\tau' in aux['A10']['statement_original']
    assert r'\tilde\mu_j(X_i)' in aux['A12']['statement_original'] and r'\widehat' not in aux['A12']['statement_original']
    assert set(ambient['statement_local_bindings'])=={'T2','T3','T4','T5'} and len(ambient['source_claim_references'])==2
    for a in aux.values():assert set(a['depends_on'])<=set(m)
    originals=list(m.values())+d['claims']+list(aux.values())
    for obj in originals:
        text=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',text)
        assert not any(ord(ch)<32 and ch!='\n' for ch in text)
        assert text.count('$')%2==0
        assert len(re.findall(r'(?<!\\)\\\[',text))==len(re.findall(r'(?<!\\)\\\]',text))
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
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
            assert path[0] in direct[n] and path[-1]==lid
            assert all(b in local[a] for a,b in zip(path,path[1:]))
            ex=x['theorem_explanations'][rel['claim_id']];assert ex['via_local_ids']==path and ex['text'].strip() and ex['evidence']
            assert 'This theorem directly uses the API.' not in ex['text']
        for kw in x['source_keywords']:
            if 'context_id' in kw:
                ctx=next(v for v in a['naming_context'] if v['context_id']==kw['context_id']);assert kw['source_text'] in ctx['text']
                assert all(1<=e['page']<=27 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
    counts=dict(theorems=4,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=4,interfaces=26,source_members=26,direct_theorem_uses=56,related_theorem_connections=83,unranked_auxiliary_passages=14)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Four complete main-text Theorems, 2-5. Theorem 3 continues onto page 12, and Theorem 4 onto page 14. All main-text headings through the clipped page-27 endpoint were checked. Lemma 1, Corollary 6, citations and appendix results are excluded.',
      source_passages='Twenty-six original source entries and fourteen auxiliary passages preserve the model, targets, seven assumptions, logistic link and fitted propensity, oracle correction, auxiliary sampling, initial fit, full quadratic program, DIPW, residuals, events, local moments, cyclic folds and confidence interval. Unnamed local formulas remain explicit source context with listed prerequisites; they are not renamed or silently discarded.',
      dependencies='Independent reconstruction confirms 56 direct uses after explicit expansion of unnamed local formulas and 83 related connections. Theorem 3 inherits Theorem 2 setup and bias part (i), not its Gaussian conclusion (ii). Theorem 5 inherits only Theorem 4 estimator construction/tuning and does not acquire Assumptions 6-7 or its interval.',
      targets='The population target tau occurs in Theorems 3 and 5; the conditional observed-covariate target bar-tau occurs in Theorems 2 and 4. The regression definition does not acquire tau merely through the following contrast identity. Theorem 5 initial tilde-mu differs from the optimized concatenated mu-hat.',
      notation='Source comparison retains true versus estimated propensity denominators, strict true overlap versus non-strict fitted overlap, zero fallback on infeasibility, both norms in Omega, conditional moments given auxiliary B, all logarithms under the Theorem 4 square root, and its all-alpha conditional coverage event. Three-fold roles are cyclic; independence of the estimates is not asserted.',
      limits='Twelve source conventions or ambiguities are recorded separately, including undefined main-text z_alpha tail convention, zero variance denominators, c_epsilon versus sigma_epsilon, and the unrestricted e_n sequence. No appendix definition or proof correction is inserted into the original statements.',
      names_and_highlights='Every indexed entry uses literal natural-language source terms with original source-kind labels, verified symbol/phrase selectors and explanations of its actual same-paper connection. Local unnamed transformed outcomes and moments remain available in the auxiliary artifact rather than receiving invented titles.',
      reproduction='Six content artifacts reproduce byte-for-byte from the retained per-paper scripts. Frozen hashes and independent source-specific checks protect the reviewed state. Re-execution alone does not perform a new semantic review or certify proofs.')
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=67,main_text_last_pdf_page=27,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-font enumeration and visual comparison of all four complete original Theorems.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv v3 source; no assumption of equivalence to the published article.','Original source ambiguities are retained separately; no appendix-body material is used.','Source and schema validation do not certify mathematical proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=67,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
