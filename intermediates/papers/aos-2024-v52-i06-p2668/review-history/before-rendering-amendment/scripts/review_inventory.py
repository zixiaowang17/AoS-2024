"""Independently enumerate and source-validate the seven main-text Theorems."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA
EXPECTED='f1e6386f4175ac0ea5823378a09649d8f933a26a7e1cd0ae9ea4e0ce537501f2'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==25
    first=' '.join(pdf[0].get_text().split())
    for v in ['STATISTICAL INFERENCE FOR FOUR-REGIME SEGMENTED REGRESSION MODELS','HAN YAN','SONG XI CHEN','arXiv:2410.04384v1','6 Oct 2024']:assert v in first,v
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='2410.04384v1.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2410.04384'
    boundary=pdf[23].search_for('SUPPLEMENTARY MATERIAL');assert any(395<b.y0<396 for b in boundary)
    assert [x for x in pdf.get_toc() if x[1]=='Supplementary Material']==[[1,'Supplementary Material',24]]
    labels=[];hashes={}
    for n in range(1,25):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,390) if n==24 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(x['text'] for x in line['spans']).strip();match=re.match(r'^THEOREM\s+(\d+\.\d+)\b',text)
                if match:
                    assert all(x['font']=='NimbusRomNo9L-Regu' for x in line['spans'])
                    labels.append([n,match[1]])
    expected=[[6,'3.1'],[6,'3.2'],[8,'3.3'],[10,'4.1'],[13,'5.1'],[15,'6.1'],[16,'6.2']];assert labels==expected,labels
    end=(ROOT/'evidence/page-24.txt').read_text();assert 'Acknowledgements' in end and 'SUPPLEMENTARY MATERIAL' not in end and 'REFERENCES' not in end
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==7
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n
        assert c['label']=='Theorem '+n+(' (Asymptotic distribution)' if n=='3.3' else '')
        assert [e['page'] for e in c['evidence']]==[page]
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
'3.1':['Assumptions 1–3',r'\widehat\theta=(\widehat\gamma^\top,\widehat\beta^\top)^\top','for any',r'\widehat\gamma\in\widehat{\mathcal G}',', ,',r'\widehat\theta\xrightarrow{p}\theta_0'],
'3.2':['Assumptions 1–4',r'\|\widehat\beta-\beta_0\|=O_p(1/\sqrt T)',r'\|\widehat\gamma-\gamma_0\|=O_p(1/T)','for any'],
'3.3':['Assumptions 1-5','(i)',r'\sqrt T(\widehat\beta_k-\beta_{k0})\xrightarrow{d}\mathcal N(0,\Sigma_k)',r'T(\widehat\gamma^c-\gamma_0)\xrightarrow{d}\gamma_D^c','(ii)',r'\{\sqrt T(\widehat\beta_k-\beta_{k0})\}_{k=1}^4',r'\{T(\widehat\gamma_i^c-\gamma_{i0})\}_{i=1}^2','asymptotically independent'],
'4.1':['For any small',r'\epsilon>0','in (4.7)','solution of the MIQP','(4.6) and (4.7)',r'\mathbb M_T(\widehat\theta)=\mathbb M_T(\widetilde\theta)','solution in (3.2)'],
'5.1':['Assumptions 1-6',r'\rho(\mathcal L_{T,B},\mathcal L_T)\xrightarrow{p}0',r'B,T\to\infty','any metric','metrizes weak convergence of distributions'],
'6.1':['Model (6.6)',r'1\le K_0<4',r'0\le L_0\le2','Assumption 1 and Assumptions S2-S4 in the SM ([33])','adapt Assumptions 3–4',r'd(\beta_{k0},\widehat{\mathcal B})=O_p(1/\sqrt T)',r'L_0=1',r'd(\gamma_0,\widehat{\mathcal G})=O_p(1/T)',r'L_0=2',r'd(\gamma_{i0},\widehat{\mathcal G})=O_p(1/T)',r'Q_k\subset\{1,\cdots,4\}',r'\cup_{i\in Q_k}R_i(\widehat\gamma)',r'=O(1/T)'],
'6.2':['assumptions of Theorem 6.1',r'\lambda_T\to\infty',r'\lambda_T/T\to0','selected in (6.8)',r'\mathbb P(\widehat K=K_0)\to1',r'\mathbb P\{\widehat R_k^{(\widehat K)}\mathbin{\triangle}R_k(\gamma_0)\}=O(1/T)',r'\|\widehat\beta_k^{(\widehat K)}-\beta_{k0}\|=O_p(1/\sqrt T)']}
    for n,parts in checks.items():
        for v in parts:assert v in s[n],(n,v)
    assert 'Assumptions 1' not in s['4.1'] and r'Z\in' not in s['6.2']
    assert r'\widehat\gamma^c' not in s['3.1']+s['3.2']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2668-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent actual small-cap heading enumeration, visual comparison of all seven complete statements, source-specific formula/reference checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,6,8,10,13,15,16,24],main_text_end_page=24,last_page_clip_y=390),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Exactly seven main-text Theorems; only3.3 has a printed title. Corollaries and prose mentions are excluded.','T3.1 has an original duplicated comma. T3.1/T3.2 permit any boundary minimizer; T3.3 uses the centroid and has two independence/convergence subparts.','T4.1 is an optimization-equivalence statement without an explicit Assumptions1–6 import. T5.1 considers B andT tending to infinity and a weak-convergence-metrizing metric.','T6.1 explicitly refers to supplementary AssumptionsS2–S4; their bodies are outside scope. T6.2 inherits those assumptions. Original ordinary-O regime error rates and implicit set-probability notation are retained.','Inventory only. Definitions, numbered assumptions, limit process, MIQP constraints, smoothed bootstrap, degenerate models and model selection remain to be extracted and source-reviewed.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=registered['source_url'],registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=7,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original model, normalized parameter spaces, LSE solution sets and all main-text Assumptions1–6; preserve covariance/centroid/limit-process, MIQP, smoothed-bootstrap and degenerate-model/selection definitions. Record uninspected supplementary S2–S4 imports as unresolved; finalize, reproduce and independently source-review.'))
    print('Seven complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
