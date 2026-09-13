"""Recheck frozen, visually compared source content without importing extraction decisions."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json':'0764fb4975546abd7c6ad9cb8ab4434b9ace263dd1d5a3b07a1f246847ac9d53','source-passages.json':'1ecf6d3f15f3c2c81853a8d5edd696ae9f913cfb1de8e3d127a11be2dec76915','interface-extraction.json':'c9fb959852740fc002b784a6c4178b3eaef9644c97d33bf1433db28a147d8ef8','ambient-prerequisites.json':'e115101c6fb96ab97913008ab5a5364d2d8739fde49fee98a5b3877b32ace2ea','unfinalized-census.json':'48e07d4e113680ad2434c018bd0966c695a80be67a40836e46ac93e48c31851e','ranked-interfaces.json':'670f1403d0a85fc97d9cd6a711c070dbd5df29b6f6d375d1c2a66548d5e6f669'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def main():
    for n,h in EXPECTED.items():assert digest(ROOT/n)==h,('Changed reviewed content',n)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    reg=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==reg['sha256'] and reg['version']=='2401.06446v2.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());p=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());a=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert p['source_url']==URL and p['pdf_pages']==reg['pdf_pages']==25
    assert p['main_text_last_pdf_page']==21 and p['main_text_boundary']['shared_page_with_appendix']
    assert len(inv['claims'])==len(d['claims'])==2
    for c,o in zip(d['claims'],inv['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==o
    m={v['local_id']:v for x in d['interfaces'] for v in x['members']}
    # Independently reconstructed mathematical-use graph from the original clauses.
    raw={1:[],2:[1],3:[1,2],4:[2,3,20],5:[1,3],6:[2],7:[6],8:[1,7],9:[3,4,10],10:[1,20],11:[3,9],12:[],13:[1,2,3,6,7,12],14:[1,2],15:[1,2,3,5,6],16:[1,2,3,5,8],17:[3,5,8,11,14],18:[3,4,9,11,20],19:[3,4,9,11,18,20],20:[1]}
    local={f'D{k}':ids(v) for k,v in raw.items()}
    direct={'1':ids([3,5,8,11,12,13,14,15,16,17]),'3':ids([3,5,8,11,12,13,14,15,16,17,18,19])}
    reaches={'1':ids(list(range(1,18))+[20]),'3':ids(range(1,21))}
    assert {k:set(v['depends_on']) for k,v in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        found=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in found:found.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert found==actual==reaches[n]
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
    1:['in in each cell',r'n=ghm','we do not assume normality',r'\gamma_{ij}+e_{ijk}'],
    2:[r'(\bar x_{ij}-\bar x_{i.}-\bar x_{.j}+\bar x)',r'(x_{ijk}-\bar x_{ij})',r'p=p_a+p_b+p_{ab}+p_w\ge p_0'],
    3:[r'\boldsymbol x_{ijk}^{(w)T}\boldsymbol\xi_4',r'\dot{\boldsymbol\xi}_4^T,\dot\sigma_e^2','covariates treated as fixed'],
    4:[r'\boldsymbol X^{(ab)}\otimes\boldsymbol1_m',r'\boldsymbol Z_0\boldsymbol e',r'\tag{5}'],
    5:[r'\eta=g/h',r'\dot\tau=\dot\sigma_\alpha^2+\eta\dot\sigma_\beta^2'],
    6:[r'\boldsymbol x_{i(c)}^{(a)}=\boldsymbol x_i^{(a)}-\bar{\boldsymbol x}^{(a)}','and similarly',r'\boldsymbol x_{ijk(c)}^{(w)}'],
    7:[r'\boldsymbol X_{i(c)}^{(a)}=[',r'\bar{\boldsymbol x}_{i.(c)}^{(ab)T}',r'SA_{\boldsymbol x^{(a)},(ab)}',r'SB_{\boldsymbol x^{(b)}}',r'SAB_{\boldsymbol x^{(ab)}}',r'SW_{\boldsymbol x^{(w)}}'],
    8:[r'\hat{\boldsymbol D}_1=g^{-1}',r'\hat{\boldsymbol D}_2=h^{-1}',r'\hat{\boldsymbol D}_3=(gh)^{-1}',r'\hat{\boldsymbol D}_4=n^{-1}','Appendix A'],
    9:[r'-\frac n2\log2\pi',r'-\frac12\log|\boldsymbol V|',r'\boldsymbol V^{-1}',r'\tag{6}'],
    10:[r'\lambda_0=\sigma_e^2',r'\lambda_4=\sigma_e^2+m\sigma_\gamma^2+hm\sigma_\alpha^2+gm\sigma_\beta^2',r'\boldsymbol C_a=\boldsymbol I_a-\bar{\boldsymbol J}_a','Appendix B'],
    11:['differentiate (6)',r'\boldsymbol0_{[(p+5):1]}=\psi(\omega)','Supplementary Section S.2'],
    12:[r'(\boldsymbol a^T\boldsymbol a)^{1/2}',r'\operatorname{trace}(\boldsymbol A\boldsymbol A^T)'],
    13:['1. The model (4)','inside the parameter space',r'm\to\infty','mutually independent',r'4+\delta',r'\lim_{h\to\infty}\sum_{j=1}^h\boldsymbol x_j^{(b)}',r'\boldsymbol X_{ij(c)}^{(ab)}\boldsymbol X_{ij(c)}^{(ab)T}','positive definite',r'2+\delta'],
    14:[r'g\boldsymbol I_{p_a+2},h\boldsymbol I_{p_b+1},gh\boldsymbol I_{p_{ab}+1},n\boldsymbol I_{p_w+1}'],
    15:[r'\phi_{\xi_0}',r'\phi_{\boldsymbol\xi_4}',r'\phi_{\sigma_e^2}',r'\tag{10}',r'\frac{\eta\dot\sigma_\beta^2}{\dot\tau}',r'\frac{\dot\sigma_\alpha^2}{\dot\tau}'],
    16:[r'\boldsymbol0_{[p_a:p_b]}&\boldsymbol0_{[p_b:1]}',r'-\eta^{1/2}\dot\sigma_\beta^2\boldsymbol f_3',r'\mathbb E\alpha_1^3',r'\mathbb Ee_{111}^4-\dot\sigma_e^4'],
    17:[r'\mathbb E\nabla\psi(\dot\omega)',r'\tag{13}',r'\boldsymbol D_1/\dot\sigma_\alpha^2',r'\boldsymbol D_2/\dot\sigma_\beta^2',r'\boldsymbol D_3/\dot\sigma_\gamma^2',r'\boldsymbol D_4/\dot\sigma_e^2',r'1(2\dot\sigma_e^4)'],
    18:[r'\hat{\boldsymbol\xi}(\theta)=\{\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol X\}^{-1}',r'l_R(\theta;\boldsymbol y)',r'\hat{\boldsymbol\xi}_R=\hat{\boldsymbol\xi}(\hat\theta_R)'],
    19:[r'l_A(\boldsymbol\xi,\theta;\boldsymbol y)',r'\psi_A(\omega)',r'l_{A\sigma_e^2}',r'\boldsymbol Z_0\boldsymbol Z_0^T'],
    20:[r'\boldsymbol Z_0=\boldsymbol I_g\otimes\boldsymbol I_h\otimes\boldsymbol I_m',r'\boldsymbol Z_2=\boldsymbol1_g\otimes\boldsymbol I_h\otimes\boldsymbol1_m',r'\tag{3}',r'\boldsymbol J_a=\boldsymbol1_a\boldsymbol1_a^T']}
    for n,tokens in checks.items():
        for tok in tokens:assert tok in s[f'D{n}'],(n,tok)
    assert s['D19'].count(r'(\omega)-\frac12\operatorname{trace}')==4
    assert r'1/(2\dot\sigma_e^4)' not in s['D17']
    assert m['D13']['source_kind']=='condition' and m['D13']['source_heading']=='Condition A'
    for n in [14,15,16]:assert m[f'D{n}']['source_kind']=='theorem_excerpt'
    for n in [1,3,17]:assert m[f'D{n}']['source_kind']=='source_passage'
    assert len(a['source_issues'])==12 and len(a['unranked_auxiliary_passages'])==4
    assert len(a['unresolved_external_prerequisites'])==3
    assert set(a['statement_local_bindings'])=={'T1','T3'}
    for obj in list(m.values())+d['claims']+a['unranked_auxiliary_passages']:
        t=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',t)
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        assert all(1<=e['page']<=21 for e in obj['evidence'])
    for x in d['interfaces']:
        v=x['members'][0];lid=v['local_id']
        assert {u['claim_id'] for u in x['central_claim_uses']}=={PID+'/T'+n for n,ls in direct.items() if lid in ls}
        assert set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
        for r in x['related_theorems']:
            n=r['claim_id'].split('/T')[-1];path=r['via_local_ids']
            assert path[0] in direct[n] and path[-1]==lid and all(b in local[aa] for aa,b in zip(path,path[1:]))
            assert r['relation']==('direct' if lid in direct[n] else 'indirect')
            ex=x['theorem_explanations'][r['claim_id']]
            assert ex['via_local_ids']==path and ex['evidence'] and ex['text'].strip()
            assert 'This theorem directly uses the API.' not in ex['text']
        for kw in x['source_keywords']:
            text=v['statement_original']
            if 'context_id' in kw:
                ctx=next(c for c in v['naming_context'] if c['context_id']==kw['context_id']);text=ctx['text']
                assert all(1<=e['page']<=21 for e in ctx['evidence'])
            assert kw['source_text'] in text
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=2,interfaces=20,source_members=20,direct_theorem_uses=22,related_theorem_connections=38,unranked_auxiliary_passages=4)
    assert sum(len(x['central_claim_uses']) for x in d['interfaces'])==22
    assert sum(len(x['related_theorems']) for x in d['interfaces'])==38
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    sys.path.insert(0,'skills/statistical-census-html/scripts')
    import build_report
    for c in d['claims']:build_report.render_statement(c['statement_original'])
    build_report.verify_highlights(d)
    findings={
    'inventory':'The main text contains exactly Theorems 1 and 3. The complete Theorem 1 continuation, all covariance blocks and the final eta=infinity clause were visually compared. Corollary 2 is excluded without renumbering. The main-text endpoint is page 21 before Appendix A.',
    'source_passages':'Twenty original source entries preserve the balanced non-Gaussian crossed model, all covariate levels and main-text centering examples, Gram blocks, likelihood and score, full Condition A, rate/influence/covariance matrices, B from main-text equation (13), and the REML objective and adjusted score. Four auxiliary passages preserve observation order, working-normality scope, rate context and the exact final reordering.',
    'dependencies':'Independent source-clause reconstruction yields 22 direct uses and 38 related connections. Theorem 3 explicitly applies Theorem 1; its asymptotic representation and covariance definitions therefore remain related. Theorem 1 does not acquire the REML objective or adjusted score. Proof-only lemmas and Corollary 2 are excluded from the theorem inventory.',
    'source_issues':'Twelve notes retain the missing column-mean normalization, a mismatched covariance zero-block dimension, sigma_a and coavriate tokens, the missing division slash in B3, and the four printed REML-score minus signs. Abbreviated centering, unspecified Omega and these formula discrepancies remain three explicit source-ambiguity records.',
    'names_and_highlights':'Every entry has original source terminology, an original passage type/heading, and visible source-backed selectors. All 38 connections retain exact same-paper paths and source-specific explanations. Both theorems and all 20 source annotations pass the strict HTML renderer checks.',
    'reproduction':'All six content JSON files reproduce byte for byte in a fresh empty directory using the retained per-paper scripts. This checks extraction reproducibility and schema consistency, separately from the visual source comparison.',
    'limits':'This is a completed extraction-fidelity review, not proof certification or a corrected formal specification. No appendix body or external supplementary derivation was used to fill a definition. The original source ambiguities are explicit and must remain visible to later semantic/library review.'}
    pages=[1,2,3,4,5,6,7,8,9,19];crop=dict(path='evidence/page-21-main-text.png',page=21,y_end=534)
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=pages,visually_reviewed_crops=[crop]))
    evidence=[dict(path=f'evidence/page-{n:02}.png',page=n) for n in pages]+[crop,dict(path='evidence/manual-findings.json')]
    for e in evidence:assert (ROOT/e['path']).is_file()
    write('evidence/rendering-check.json',dict(paper_id=PID,theorems_rendered=2,source_members_with_visible_highlights=20,all_selectors_matched=True,scope='Source rendering and annotations only; corpus release, mathlib audit and final HTML remain pending.'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=p['version'],pdf_sha256=SHA,pdf_pages=25,main_text_last_pdf_page=21,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent actual-Theorem enumeration across main-text pages 1–21 and visual comparison of both complete statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=a['source_issues'],ambient_resolution=a['statement_local_bindings'],source_claim_references=a['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv v2 source, 25 pages; DOI 10.1214/24-AOS2469.','Main text ends before Appendix A on page 21; page 21 evidence is clipped at y=534.','The review preserves original statements, including source ambiguities; it does not certify corrected formulas or proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=25,source_version=p['version'],registered_version_alias=reg['version'],registered_url_alias=reg['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
