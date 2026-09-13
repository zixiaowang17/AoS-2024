"""Independently enumerate and validate the six original main-text Theorems."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='1b1f80771e7a1dae0fd0a28bfa96259bb0a8e2b93f279d7bf65ccef2059d865f'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==25
    first=' '.join(pdf[0].get_text().split())
    for x in ['2024, Vol. 52, No. 6, 2931–2955','STATISTICAL INFERENCE FOR DECENTRALIZED FEDERATED LEARNING','JIA GU','SONG XI CHEN','10.1214/24-AOS2452']:assert x in first,x
    reg=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert reg['version']=='AOS2452.pdf' and reg['source_url']==URL
    labels=[];hashes={}
    for n in range(1,25):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,160) if n==24 else None
        name=f'page-{n:02}'+('-main-text' if n==24 else '')+'.txt'
        f=ROOT/'evidence'/name;assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                spans=line['spans']
                if not spans:continue
                t=''.join(s['text'] for s in spans)
                m=re.match(r'^THEOREM ([1-6])\.',t)
                if m:labels.append([n,m[1]])
    expected=[[8,'1'],[10,'2'],[12,'3'],[13,'4'],[15,'5'],[17,'6']]
    assert labels==expected,labels
    end=' '.join(pdf[23].get_text(clip=fitz.Rect(0,0,pdf[23].rect.width,160)).split())
    assert end.endswith('grants 12292980, 12292983 and 92358303.')
    listing=' '.join(pdf[23].get_text(clip=fitz.Rect(0,160,pdf[23].rect.width,230)).split())
    assert 'SUPPLEMENTARY MATERIAL' in listing and '10.1214/24-AOS2452SUPP' in listing
    # The supplement is external. No appendix body is accessed.
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==6
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n and c['label']=='Theorem '+n
        assert [e['page'] for e in c['evidence']]==([13,14] if n=='4' else [page])
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
    '1':['Assumptions required in Lemma 1',r'1\le\tau\le t\le T',r'3b_2^2Q',r'2(L_\xi+1)\delta(t,\tilde\rho^2,\tau)',r'\frac{\mathbb I_{\{\tilde\rho>0\}}}{1-\tilde\rho}',r'2\sigma^2b_2^2\delta(t,\tilde\rho^2,\tau)',r'\tilde\rho=\rho^{1/\tau}',r'\kappa^2+2L^2R_d^2',r'\kappa^2+L^2(B_{\mathrm{MSE}}+B_{\mathrm{CE}})',r'\sum_{s=t-\tau+2}^t\eta_s^2',r'\eta_{\lfloor(t-\tau+1)/2\rfloor}^2',r'a\in(0,1)'],
    '2':['3.1 with $v=1$','3.2–3.4',r'0\le t<T',r'(1-\mu_{R_d}\eta_{t+1})',r'c_1=b_2\sigma^2+3b_2^3L_\xi\kappa^2',r'c_2=3b_2(L+\mu)',r'D>2/\mu_{R_d}',r'\eta_1\le D/(D\mu_{R_d}-1)',r'v_1\frac{\eta_t}K+v_2\eta_t^2',r'c_2c_0D/(D\mu_{R_d}-2)',r'(\gamma+1)^2',r'D^{-2}','For each fixed $K$','almost surely'],
    '3':['assumptions required in Theorem 2','4.1, 4.2 and 4.3','either finite or diverges',r'o(T^{2\alpha-1})',r'\alpha<1',r'\sup_{K\ge1}',r'\sqrt{TK}\boldsymbol S^{-1/2}\boldsymbol H',r'\boldsymbol H=\nabla^2F(\boldsymbol\theta_K^*)','defined in Assumption 4.2'],
    '4':['4.1, 4.2 and 4.4',r'K=o(T^{2\alpha-1})',r'Ka(T)\to\infty',r'\sup_{K\ge1}\max_{1\le k\le K}',r'\|\hat{\boldsymbol\Sigma}-\boldsymbol H^{-1}\boldsymbol S\boldsymbol H^{-1}\|_2=o_p(1)',r'\to1-\beta',r'\chi^2_{d,\beta}',r'\hat{\boldsymbol\Sigma}=\hat{\boldsymbol H}^{-1}\hat{\boldsymbol S}\hat{\boldsymbol H}^{-1}'],
    '5':['3.1 with $v=2$, 3.3–3.4, 4.1 and 4.3',r'R_d<\infty',r'K=o(T^\alpha)',r'\frac12<\alpha<1',r'K=o(\log(T)T^{1-\zeta})',r'\alpha=1',r'\zeta\in(0,1/2)',r'\mathbb E\left(\|\tilde{\boldsymbol H}^{\mathrm{reg}}-\boldsymbol H\|_F\right)\to0'],
    '6':['assumptions of Theorem 2','4.1, 4.2 and 4.4',r'\alpha=1','defined in (33)',r'\nabla F_k(\boldsymbol\theta_K^*;\boldsymbol\xi_t^k)',r'\sqrt{\frac KT}+\frac1{\sqrt K}',r'K=o(T)',r'as $T$ and $K\to\infty$']}
    for n,vs in checks.items():
        for v in vs:assert v in s[n],(n,v)
    assert '(iii)' in s['2'] and r'\|_F^2' not in s['5']
    assert '3.2–3.4' not in s['5'] # Do not silently insert the omitted Assumption 3.2.
    assert 'Corollary' not in s['6'] and r'\nabla f_k' not in s['6']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for a,b in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',a+b):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    v=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2931-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/f.name).read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent small-cap theorem-heading enumeration over main-text pages 1–24, visual comparison of all six statements and the continuation of Theorem 4, boundary inspection, source-specific formula/branch checks, structural validation and exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,8,10,12,13,14,15,17],visually_reviewed_crops=[dict(path='evidence/page-24-main-text.png',page=24,y_end=160)],main_text_end_page=24),validation=dict(returncode=v.returncode,stdout=v.stdout),notes=['Exactly six actual Theorems. Lemma 1, Corollary 1, narrative citations and the external supplement are excluded from the inventory.','Theorem 1 retains both parameter-domain alternatives and the full delta formula, including its printed open a-domain.','Theorem 2 retains all three subparts, constants, rate bounds and the fixed-K qualifier for almost sure convergence.','Theorems 3 and 4 retain different Hessian assumptions, client-growth and Hessian-window requirements, and the full coverage statement.','Theorem 5 retains v=2, the printed assumption list without adding Assumption 3.2, both alpha regimes and convergence of expected Frobenius norm (not its square).','Theorem 6 retains uppercase F_k with a data argument as printed and requires both T and K to diverge in its final consequence.','Definitions, dependencies and full registered-source census review remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=reg['source_url'],registered_version_alias=reg['version'],checked_at=now))
    p=ROOT/'checkpoint.json'
    if not p.exists() or json.loads(p.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=6,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original federated risks and weights, decentralized iteration and matrix averages, complete assumption families, consensus/MSE constants, PR average, covariance/Hessian estimators and the one-step correction. Preserve source inconsistencies separately; finalize, reproduce and independently review the full census.'))
    print('All six original main-text Theorems independently source-validated.')
if __name__=='__main__':main()
