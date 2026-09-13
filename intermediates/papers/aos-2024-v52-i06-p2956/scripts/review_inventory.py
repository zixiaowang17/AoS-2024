"""Independently validate the full source inventory, retaining printed labels 1 and 3."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA
EXPECTED='0764fb4975546abd7c6ad9cb8ab4434b9ace263dd1d5a3b07a1f246847ac9d53'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==25
    first=' '.join(pdf[0].get_text().split())
    for x in ['arXiv:2401.06446v2','13 Mar 2024','INCREASING DIMENSION ASYMPTOTICS FOR TWO-WAY CROSSED MIXED EFFECT MODELS','ZIYANG LYU','S.A. SISSON','A.H. WELSH']:assert x in first,x
    reg=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert reg['version']=='2401.06446v2.pdf' and reg['source_url']=='https://export.arxiv.org/pdf/2401.06446'
    labels=[];hashes={}
    for n in range(1,22):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,534) if n==21 else None
        name=f'page-{n:02}'+('-main-text' if n==21 else '')+'.txt'
        f=ROOT/'evidence'/name;assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                spans=line['spans']
                if not spans:continue
                text=''.join(s['text'] for s in spans)
                m=re.match(r'^THEOREM (\d+)\.',text)
                if m:labels.append([n,m[1]])
    assert labels==[[7,'1'],[9,'3']],labels
    # Inspect only the excluded appendix heading to confirm the boundary.
    heading=' '.join(pdf[20].get_text(clip=fitz.Rect(0,534,pdf[20].rect.width,552)).split())
    assert heading.startswith('APPENDIX A:'),heading
    end=' '.join(pdf[20].get_text(clip=fitz.Rect(0,0,pdf[20].rect.width,534)).split())
    assert end.endswith('will be pursued in future work.')
    assert 'COROLLARY 2.' in pdf[7].get_text()
    path=ROOT/'theorem-inventory.json';assert digest(path)==EXPECTED
    inv=json.loads(path.read_text());assert len(inv['claims'])==2
    paper=inv['papers'][0];assert paper['main_text_last_pdf_page']==21 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    for i,(c,n,ps) in enumerate(zip(inv['claims'],['1','3'],[[7,8],[9]]),1):
        assert c['claim_id']==PID+'/T'+n and c['source_order']==i and c['label']=='Theorem '+n
        assert [e['page'] for e in c['evidence']]==ps
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in inv['claims']}
    checks=[
    'Suppose Condition A holds.',r'0\le\eta<\infty','there is a solution',
    r'\psi(\omega)=\boldsymbol0_{[(p+5):1]}',
    r'\operatorname{diag}(g\boldsymbol I_{p_a+2},h\boldsymbol I_{p_b+1},gh\boldsymbol I_{p_{ab}+1},n\boldsymbol I_{p_w+1})',
    r'\boldsymbol B^{-1}\boldsymbol K^{-1/2}\phi+o_p(1)',r'\tag{9}',r'\tag{10}',
    r'\frac1{\dot\tau}\left(\sum_{i=1}^g\alpha_i+\eta\sum_{j=1}^h\beta_j\right)',
    r'\frac{\eta\dot\sigma_\beta^2}{\dot\tau}',r'\frac{\dot\sigma_\alpha^2}{\dot\tau}',
    r'\frac1{2\dot\sigma_\alpha^4}',r'\frac1{2\dot\sigma_\beta^4}',r'\frac1{2\dot\sigma_\gamma^4}',r'\frac1{2\dot\sigma_e^4}',
    r'\boldsymbol x_{ij(c)}^{(ab)}\gamma_{ij}',r'\boldsymbol x_{ijk(c)}^{(w)}e_{ijk}',
    r'\boldsymbol F_{1(a),(b)}=\boldsymbol F_{1(b),(a)}^T',
    r'-\eta^{1/2}\dot\sigma_\beta^2\boldsymbol f_3',r'\eta^{1/2}\mathbb E\beta_1^3',
    r'\boldsymbol0_{[p_a:p_b]}&\boldsymbol0_{[p_b:1]}',
    r'\mathbb E\alpha_1^4-\dot\sigma_\alpha^4',r'\mathbb E\beta_1^4-\dot\sigma_\beta^4',r'\mathbb E\gamma_{11}^4-\dot\sigma_\gamma^4',r'\mathbb Ee_{111}^4-\dot\sigma_e^4',
    r'\boldsymbol D_1^{-1}',r'\boldsymbol D_2^{-1}',r'\boldsymbol D_3^{-1}',r'\boldsymbol D_4^{-1}',
    r'f_1=\dot\tau+\dot\sigma_\alpha^2',r'\boldsymbol f_2=\bar{\boldsymbol x}^{(a)T}\boldsymbol D_1^{-1}',r'\boldsymbol f_3=\bar{\boldsymbol x}^{(b)T}\boldsymbol D_2^{-1}',
    r'\eta=\infty',r'\omega=[\boldsymbol\xi_1^T,\sigma_a^2,\xi_0','asymptotic coavriate matrix.']
    for v in checks:assert v in s['1'],v
    assert s['1'].count(r'\phi_{\boldsymbol\xi_')>=8
    assert 'Corollary' not in s['1'] and r'\hat{\boldsymbol F}' not in s['1']
    assert 'there is a solution' in s['3'] and 'REML estimating equations' in s['3']
    assert r'|\boldsymbol K^{1/2}(\hat\omega_R-\dot\omega)|=O_p(1)' in s['3']
    assert r'\boldsymbol K^{1/2}(\hat\omega_R-\hat\omega)=o_p(1)' in s['3']
    assert s['3'].endswith('so Theorem 1 applies to the REML estimator.')
    for c in inv['claims']:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for a,b in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',a+b):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    v=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2956-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/path.name).read_bytes()==path.read_bytes()
    sys.path.insert(0,'skills/statistical-census-html/scripts')
    from build_report import render_statement
    for c in inv['claims']:render_statement(c['statement_original'])
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=labels,method='Independent actual-Theorem heading enumeration over main-text pages 1–21, including main-text proof sections; visual comparison of full original Theorem 1 and its continuation and Theorem 3; boundary inspection, formula/dimension checks, structural validation, rendering and exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[7,8,9],visually_reviewed_crops=[dict(path='evidence/page-21-main-text.png',page=21,y_end=534,before_main_text_end=True)],main_text_end_page=21),validation=dict(returncode=v.returncode,stdout=v.stdout),notes=['Exactly two actual Theorems, numbered 1 and 3. Corollary 2 is excluded, and no labels are renumbered.','Theorem 1 includes all nine influence-function components, all covariance blocks and the full eta=infinity parameter-reordering clause.','The existence of a solution to estimating equations is not silently strengthened to uniqueness or global maximization.','The printed off-diagonal zero-block dimension, sigma_a notation and coavriate spelling are retained; source issues belong in separate notes.','Theorem 3 preserves normalized ML/REML equivalence and explicitly invokes the conclusion of Theorem 1.','Source definitions and dependencies remain pending. No appendix body is used in the inventory or its evidence.']))
    write('evidence/source-provenance.json',dict(paper,cached_pdf=str(source),registered_source=True,registered_source_url_alias=reg['source_url'],registered_version_alias=reg['version'],checked_at=now))
    p=ROOT/'checkpoint.json'
    if not p.exists() or json.loads(p.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=2,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract the crossed-effect model, covariate decomposition and main-text centering definitions, full Condition A, score and REML equations, parameter/rate matrices and B in main-text proof section. Keep appendix-only references unresolved; finalize and independently review the full census.'))
    print('Both complete original Theorems, numbered 1 and 3, independently source-validated.')
if __name__=='__main__':main()
