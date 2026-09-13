"""Independently review frozen source content and dependency scope before completion."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={
 'theorem-inventory.json':'2628fafa6307fcfc73e6e2f59efbed65dc1fb1ba069593ccde343b1eec0c1688',
 'source-passages.json':'59ccf6a5d7b25fc444cdb7922a12af40d1c3546995760d2c7f09fff293129d13',
 'interface-extraction.json':'2580e7a2ec840ea2122d712ba3cbe2662bfcf402af73ca07c27824e54d4d805f',
 'ambient-prerequisites.json':'51f12e441b440d550ad98a44eaacc79523b9786ba086271b662b4a0e46f4aa66',
 'unfinalized-census.json':'b1f3b88fd58a19ad2b09cdcf66d35ee7160f68f91486adafa86a6592d8025f2d',
 'ranked-interfaces.json':'833932e4d7486fa9be6c52de04adda707a9dd78359a79db939f6c85525dda97d'}
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
    assert registered['version']=='2205.14855v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2205.14855'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert ir['printed_label_check']==[[4,'2.1'],[7,'2.2'],[7,'2.3'],[11,'3.1'],[14,'3.2'],[14,'3.3'],[16,'3.4'],[17,'3.5'],[20,'5.1']]
    assert paper['source_url']==URL=='https://arxiv.org/pdf/2205.14855v2'
    assert paper['pdf_pages']==registered['pdf_pages']==50 and paper['main_text_last_pdf_page']==28
    assert paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==9
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Source graph reconstructed without importing extraction or finalizer decisions.
    raw={1:[],2:[1],3:[],4:[3],5:[3],6:[4],7:[4,6],8:[4],9:[4],10:[3],11:[3],12:[],13:[12],14:[4],15:[3],16:[4,15],17:[11,15]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'2.1':ids([1,2]),'2.2':ids([3,4,5,7,8]),'2.3':ids([3,4,5,7,8]),'3.1':ids([3,5,8,9,10,11,13]),'3.2':ids([3,5,10,11,13,14]),'3.3':ids([3,5,9,10,11]),'3.4':ids([5,10,11,12,15,16]),'3.5':ids([5,10,11,12,15,16,17]),'5.1':ids([1,2])}
    expected_reach={'2.1':ids([1,2]),'2.2':ids([3,4,5,6,7,8]),'2.3':ids([3,4,5,6,7,8]),'3.1':ids([3,4,5,8,9,10,11,12,13]),'3.2':ids([3,4,5,10,11,12,13,14]),'3.3':ids([3,4,5,9,10,11]),'3.4':ids([3,4,5,10,11,12,15,16]),'3.5':ids([3,4,5,10,11,12,15,16,17]),'5.1':ids([1,2])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n]
    assert not ids([8,9])&expected_reach['3.2']
    assert not ids([8,12,13,14])&expected_reach['3.3']
    for n in ['3.1','3.2','3.3','3.4','3.5']:assert not ids([1,2,6,7])&expected_reach[n]
    assert not ids([3,12,13])&(expected_reach['2.1']|expected_reach['5.1'])
    s={lid:a['statement_original'] for lid,a in m.items()}
    snippets={
      1:[r'\mathbb R^{p\times(n-1)}',r'\hat Y=(y_1,\ldots,y_{n-1},y_n)','last column removed'],
      2:[r'r\in[p\wedge(n-1)]',r'\sigma_i u_iv_i^T',r'\hat U_r:=(\hat u_1,\ldots,\hat u_r)'],
      3:[r'z^*\in[k]^n',r'X_i=\theta_{z_i^*}^*+\epsilon_i','are noises'],
      4:[r'X=P+E',r'\theta_{z_n^*}^*',r'E:=(\epsilon_1,\ldots,\epsilon_n)'],
      5:[r'\frac1{n/k}\min_{a\in[k]}|\{i:z_i^*=a\}|',r'\beta n/k'],
      6:[r'X_{-i}:=(X_1,\ldots,X_{i-1},X_{i+1},\ldots,X_n)'],
      7:[r'\hat\lambda_{-i,j}',r'r\in[k]',r'\hat U_{-i,1:r}=(\hat u_{-i,1},\ldots,\hat u_{-i,r})'],
      8:[r'\kappa\in[k]',r'\lambda_\kappa>0',r'\lambda_{\kappa+1}=0'],
      9:['1 Perform SVD','2 Perform',r'\operatorname*{argmin}',r'\|\hat U_{1:r}^TX_i-c_{z_i}\|^2'],
      10:[r'\mathbb I\{z_i=\phi(z_i^*)\}',r'\min_{\phi\in\Phi}','bijection'],
      11:[r'\min_{a,b\in[k]:a\ne b}\|\theta_a^*-\theta_b^*\|'],
      12:[r'\mathbb Ee^{tX}\leq\exp(\sigma^2t^2/2)',r'any $t\in\mathbb R$'],
      13:[r'\mathrm{SG}_d(\sigma^2)',r'u^TX\sim\mathrm{SG}(\sigma^2)','any unit vector'],
      14:['same as Step 1 of Algorithm 1','largest index','greater than',r'\hat\lambda_a-\hat\lambda_{a+1}\geq T',r'\|\hat U_{1:\hat r}^TX_i-c_{z_i}\|^2'],
      15:[r'\theta_1^*=-\theta_2^*=\delta\mathbf1_p',r'\overset{\mathrm{iid}}\sim F',r'\delta\in\mathbb R'],
      16:[r'\operatorname*{argmin}_{z\in[2]^n',r'(\hat u_1^TX_i-c_{z_i})^2'],
      17:['positive, continuously differentiable density','mean zero and finite Fisher information',r"\mathcal I:=\int(f'/f)^2f\,dx",r'Assume $\Delta$ is a constant.']}
    for n,parts in snippets.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    assert 'independently' not in s['D3'] and r'z_i\ne' not in s['D10']
    assert 'mean' not in s['D12'] and 'independent' not in s['D13']
    assert r'\delta>0' not in s['D15'] and 'sign(' not in s['D16']
    assert m['D17']['source_kind']=='condition' and m['D17']['source_heading']=='Lemma 3.4 — Assumptions'
    for n in [1,3,15]:assert m['D'+str(n)]['source_kind']=='source_passage'
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==9 and len(ambient['source_issues'])==9
    assert 'dimension of clear' in aux['A2']['statement_original']
    assert '2 Perform' not in aux['A3']['statement_original'] and aux['A3']['depends_on']==['D4']
    assert r'\psi_3:=' in aux['A4']['statement_original'] and r'\sqrt{\frac pn}' in aux['A4']['statement_original']
    assert r'\sigma\leq C\bar\sigma' in aux['A5']['statement_original']
    assert r'\lim_{p\to\infty}\inf_z\sup_{z^*\in[2]^n}' in aux['A6']['statement_original']
    assert r'\Delta=2\sqrt p\delta' in aux['A7']['statement_original']
    assert r'\hat z_i\ne\phi(z_i^*)' in aux['A8']['statement_original']
    assert 'sin' in aux['A9']['statement_original'] and not any('A9' in c['depends_on'] for c in d['claims'])
    assert set(ambient['statement_local_bindings'])=={'T'+n for n in direct}
    for a in aux.values():assert set(a['depends_on'])<=set(m)
    originals=list(m.values())+d['claims']+list(aux.values())
    for obj in originals:
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
    counts=dict(theorems=9,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=9,interfaces=17,source_members=17,direct_theorem_uses=45,related_theorem_connections=56,unranked_auxiliary_passages=9)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Nine complete main-text Theorems: 2.1-2.3, 3.1-3.5 and 5.1. Theorem 2.1 continues onto page 5; Theorem 5.1 belongs to the main-text proof section. All original statements, including both Theorem 3.2 conclusions, were compared with the PDF.',
      source_passages='Seventeen original source entries and nine auxiliary passages preserve generic matrices/SVD, the mixture model, signal/noise matrices and spectrum, cluster size, empirical subspaces, both algorithms, loss, separation, scalar/vector SG conditions, the symmetric model, its estimator and imported Lemma 3.4 assumptions. Original source kinds and terms are retained.',
      dependencies='Independent reconstruction yields 45 direct uses and 56 related connections. Algorithm 2 imports only Algorithm 1 step 1; it has no fixed-r clustering-output dependency. Theorem 3.3 uses r=k and inline Gaussian noise, without acquiring the signal-rank or SG interfaces. Theorems 3.1-3.5 do not acquire leave-one-out proof interfaces.',
      references='Theorem 3.5 imports Theorem 3.4 assumptions and Lemma 3.4 assumptions/rate (31). The psi_3 definition, scalar variance/proxy restrictions, fixed Delta, density regularity, Fisher information and limit-infimum-supremum order are retained. The lemma is not counted as a Theorem.',
      notation='Visual checks preserve the square-root scope in (11)-(12), the k^3.5 and power -0.25 in (27), the squared upper/lower corrections of Theorem 3.4, exact argmin algorithms and the largest adaptive index with >=T. Generic matrices remain distinct from mixture matrices.',
      limits='Nine source issues are recorded without altering quotations, notably the equality/inequality discrepancy in the loss, the sign of the real delta specialization, unspecified SVD endpoint conventions, ratio denominators, threshold wording and empty-set behavior. This is source-faithful census validation, not proof certification.',
      names_and_highlights='All seventeen entries have literal natural-language source terms, faithful source headings and symbol selectors checked against their source passage or related same-paper Theorems. All 56 connections have explanations of the actual symbol or scoped reference; no boilerplate relationship captions are used.',
      reproduction='All six JSON content artifacts reproduce byte for byte from the retained scripts. The source PDF, independently reviewed inventory and complete artifact set are hash-pinned.')
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=[3,4,5,6,7,8,9,11,13,14,16,17,20,28],visually_reviewed_crops=['title.png','model-28.png','equation-12.png','equation-27.png','lemma-3-4.png']))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=50,main_text_last_pdf_page=28,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent small-cap theorem-environment enumeration and visual comparison of all nine original Theorems.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv v2 source; no assumption of equivalence to the published article.','Source discrepancies are retained separately; no appendix-body material is used.','Source and schema validation do not certify mathematical proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=50,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
