"""Independently enumerate four PDF Theorems and check their complete original statements."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA
EXPECTED='c6a49fdda565d43a359f258a17e2e2630b36a261410ae91e579fe48449f70e85'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==97
    first=' '.join(pdf[0].get_text().split())
    for x in ['The Projected Covariance Measure for assumption-lean variable significance testing','Anton Rask Lundborg','Ilmun Kim','Rajen D. Shah','Richard J. Samworth','arXiv:2211.02039v4','7 May 2024','May 8, 2024']:assert x in first,x
    reg=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert reg['version']=='2211.02039v4.pdf' and reg['source_url']=='https://export.arxiv.org/pdf/2211.02039'
    assert [x for x in pdf.get_toc() if x[1]=='Proofs']==[[1,'Proofs',34]]
    labels=[];hashes={}
    for n in range(1,30):
        page=pdf[n-1];f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text();hashes[str(n)]=digest(f)
        for b in page.get_text('dict')['blocks']:
            if n==29 and b['bbox'][1]>=202:continue
            for l in b.get('lines',[]):
                ss=l['spans']
                if not ss or ss[0]['font']!='CMBX10':continue
                m=re.match(r'^Theorem (\d+)(?:[ .]|$)',ss[0]['text'])
                if m:labels.append([n,m[1]])
    expected=[[18,'4'],[19,'5'],[21,'6'],[23,'7']];assert labels==expected,labels
    end=' '.join(pdf[28].get_text(clip=fitz.Rect(0,0,pdf[28].rect.width,202)).split());assert 'Acknowledgements' in end and 'which helped to improve the paper.' in end and 'References' not in end
    ref=next(b for b in pdf[28].get_text('blocks') if b[4].strip()=='References');assert 208<ref[1]<209
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==4
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n and c['label']=='Theorem '+n
        assert [e['page'] for e in c['evidence']]==([21,22] if n=='6' else [page])
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
    '4':['Assumption 3',r'\sigma_P^2=0',r'\delta\in(0,2]',r'\mathbb E_P(|\varepsilon_P\xi_P|^{2+\delta}\mid\hat f)/\sigma_P^{2+\delta}=o_{\mathcal P_0}(n^{\delta/2})',r'\inf_{P\in\mathcal P_0}\mathbb E_P(\varepsilon_P^2\mid X,Z)\ge c','any of the following','Algorithm 2','Algorithm 1 and $Y','a linear smoother','a sufficiently stable estimator',r'\sup_{P\in\mathcal P_0}\sup_{t\in\mathbb R}'],
    '5':['positive sequence',r'\mathcal P_1(\epsilon_n):=\{P\in\mathcal P_1:\tau_P\ge\epsilon_n\}',r'\hat m_{a\cdot\hat f}(Z)=a\cdot\hat m_{\hat f}(Z)',r'\sup_{P\in\mathcal P_1}h_P(X,Z)\le C',r'\epsilon_n\cdot n\to\infty',r'\operatorname{Corr}_P(h_P(X,Z),\xi_P\mid\hat f)\le\rho','Algorithm 2','Algorithm 1 and $\hat m$ is sufficiently stable',r'any $\alpha\in(0,1)$'],
    '6':['Assumption 4',r'\|\Pi\hat\beta\|_\infty=0',r'\Lambda_P:=\mathbb E_P\{\operatorname{Cov}_P(\phi(X,Z)\mid Z)\}',r'\Pi x=x,\|x\|_2=1',r'\ge\frac c{K_{XZ}}',r'nK_{XZ}\left\{\tilde K_Z^{-2s/d_Z}+\frac{\tilde K_Z}n\right\}^2\to0',r'\frac{K_{XZ}^{1+2/\delta}}n\to0','where $\delta$ is taken from Assumption 4','either Algorithm 1 or Algorithm 2'],
    '7':['Assumption 4',r'\mathcal P_1(\epsilon_n):=\{P\in\mathcal P:\tau_P\ge\epsilon_n\}',r'\epsilon_n\cdot n^{\frac{4s}{4s+d}}\to\infty',r'K_X\asymp n^{\frac{2d_X}{4s+d}}',r'K_Z\asymp\tilde K_Z\asymp n^{\frac{2d_Z}{4s+d}}',r'$r\ge s\ge3d/4$','according to Algorithm 2',r'\inf_{P\in\mathcal P_1(\epsilon_n)}\mathbb P_P(T>z_{1-\alpha})\to1']}
    for n,vs in checks.items():
        for v in vs:assert v in s[n],(n,v)
    assert '|h_P' not in s['5'] and 'Algorithm 1' not in s['7']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for a,b in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',a+b):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    v=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2851-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/f.name).read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold CMBX10 heading enumeration across main text; visual comparison of four full statements and the21–22 continuation; main-text endpoint crop, source-specific formula checks, validation and exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[18,19,21,22,23],visually_reviewed_crops=[dict(path='evidence/page-29-main-text.png',page=29,y_end=202)],main_text_end_page=29),validation=dict(returncode=v.returncode,stdout=v.stdout),notes=['Four original main-text Theorems4–7; Propositions1–3 and8 and supplementary Theorems are excluded.','Theorem4 has three extra conditions and four alternative algorithm branches. Theorem5 has four conditions and two branches, and retains its one-sided bound onh_P.','Theorem6 continuation includes16, the delta reference, algorithm choice and uniform normality conclusion.','Theorem7 uses Algorithm2 only and the stated spline dimension/separation exponents; significance level is supplied by the algorithm context.','Main text ends beforeReferences at y208.141 on29; supplementary material begins34 and is not read.','Stability conditions and precise Holder-space convention referenced in the main text point to supplementary sections; retain unresolved references during extraction rather than reading those sections.','Full definitions, algorithms, dependency graph and census source review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=reg['source_url'],registered_version_alias=reg['version'],checked_at=now))
    p=ROOT/'checkpoint.json'
    if not p.exists() or json.loads(p.read_text()).get('stage')!='complete':write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=4,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original PCM algorithms1/2, null and signal, regression targets/residuals/MSPEs, Assumptions3/4, spline choices and coefficient projection. Preserve supplementary-only stability and Holder conventions as unresolved. Then finalize, reproduce and source-review the census.'))
    print('Four complete original main-text Theorems independently source-validated.')
if __name__=='__main__':main()
