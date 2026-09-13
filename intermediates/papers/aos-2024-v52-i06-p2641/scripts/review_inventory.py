"""Independently enumerate, source-check and validate the five main-text Theorems."""
import datetime, hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT, REPO, PID, SHA

EXPECTED = '8de43c5995515c4416c053d76e4490d7ce29a0f00d947da94fef33fdb0fad5d9'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d): (ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')

def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source); assert len(pdf)==58
    first=' '.join(pdf[0].get_text().split())
    for v in ['TENSOR FACTOR MODEL ESTIMATION BY ITERATIVE PROJECTION','YUEFENG HAN','RONG CHEN','DAN YANG','CUN-HUI ZHANG','arXiv:2006.02611v3','18 Jul 2024']: assert v in first,v
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='2006.02611v3.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2006.02611'
    boundary=pdf[23].search_for('REFERENCES'); assert len(boundary)==1 and 650<boundary[0].y0<651
    assert [x for x in pdf.get_toc() if x[1]=='Simulation Study']==[[1,'Simulation Study',28]]
    labels=[]; hashes={}
    for n in range(1,25):
        page=pdf[n-1]; clip=fitz.Rect(0,0,page.rect.width,644) if n==24 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==page.get_text(clip=clip); hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(x['text'] for x in line['spans']).strip()
                match=re.match(r'^THEOREM\s+(\d+\.\d+)\.',text)
                if match:
                    assert all(x['font']=='NimbusRomNo9L-Regu' for x in line['spans'])
                    labels.append([n,match[1]])
    expected=[[11,'3.1'],[13,'3.2'],[13,'3.3'],[22,'3.4'],[23,'3.5']]
    assert labels==expected,labels
    end=(ROOT/'evidence/page-24.txt').read_text()
    assert 'Acknowledgements' in end and 'REFERENCES' not in end
    f=ROOT/'theorem-inventory.json'; assert digest(f)==EXPECTED
    inv=json.loads(f.read_text()); cs=inv['claims']; assert len(cs)==5
    for i,(c,(_,n),pages) in enumerate(zip(cs,expected,[[11],[13],[13,14],[22],[23]]),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n and c['label']=='Theorem '+n
        assert [e['page'] for e in c['evidence']]==pages
    s={c['label'].split()[-1]:c['statement_original'] for c in cs}
    checks={
        '3.1':['Suppose Assumption 1 holds',r'h_0\le T/4','(2.2), (3.1), (3.3) and (3.5)',r'R^{(TOPUP)}=\max_{1\le k\le K}R_k^{(TOPUP)}','iTOPUP algorithm',r'C_1^{(TOPUP)}R^{(0)}\le(1-\rho)/4',r'(\rho^m/2)R^{(TOPUP)}',r'\overline{\mathbb E}',r'\frac{3C_1^{(TOPUP)}}{1-\rho}R^{(ideal)}'],
        '3.2':['Suppose Assumption 1 holds',r'h_0\le T/4','(2.2), (3.3) and (3.6)','iTIPUP algorithm',r'\min_{1\le k\le K}\frac{(1-\rho)\lambda_k^{*2}}{8\|\Theta^*_{k,0}\|_{\mathrm S}}',r'(\rho^m/2)R^{*(0)}',r'\overline{\mathbb E}',r'\frac{3C_1^{(TIPUP)}}{1-\rho}R^{*(ideal)}'],
        '3.3':['Assumption 1 holds',r'R^{(0)}', 'as in Theorem 3.1','as in Theorem 3.2','TIPUP-iTOPUP algorithm',r'C_1^{(TOPUP)}R^{*(0)}\le(1-\rho)/4',r'C_{1,K}^{(iter)}(R^{(ideal)}+R^{(add)})\le\rho',r'(\rho^m/2)R^{*(0)}'],
        '3.4':['Hypothesis I',r'0<\delta<1/2',r'd^{1/K}\asymp d_k\ge T',r'r_k$ is fixed',r'\vartheta>0',r'\liminf_{T\to\infty}\frac{\sigma^2d^{1/2-\vartheta}}{T^{1/2}\lambda^2}>0','any randomized polynomial-time estimators',r'\min_{1\le k\le K}\|\widehat P_k-P_k\|_{\mathrm S}^2>\frac13',r'>\frac14'],
        '3.5':[r'\lambda>0',r'd_k\to\infty',r'T\to\infty','universal constant','sufficiently large',r'\inf_{\widehat U_k}',r'\mathbb E\|\widehat P_k-P_k\|_{\mathrm S}',r'(\sigma^2+\sigma\lambda)\sqrt{d_k}\big/(\lambda^2\sqrt{Tr_{-k}})']}
    for n,parts in checks.items():
        for v in parts: assert v in s[n],(n,v)
    for n in ['3.1','3.2','3.3']:
        for v in ['simultaneously for all',r'1\le k\le K',r'm\ge0',r'1-\sum_{k=1}^Ke^{-d_k}',r'(1-\rho^m)(1-\rho)^{-1}']: assert v in s[n],(n,v)
    for n in ['3.1','3.2']:
        assert r'J=\lfloor\log(\max_k d_{-k}/r_{-k})/\log(1/\rho)\rfloor' in s[n]
    assert 'iterations' not in s['3.3'] and 'Assumption 2' not in ''.join(s.values())
    assert 'Hypothesis I' not in s['3.5'] and 'polynomial-time' not in s['3.5']
    for n in ['3.4','3.5']: assert r'\mathscr P(T,d_1,\ldots,d_K,\lambda)' in s[n]
    for c in cs:
        t=c['statement_original']; assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1; assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2641-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True)
        assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent actual small-cap theorem-heading enumeration throughout the main text, visual comparison of all five complete statements and the page 13–14 continuation, formula/quantifier/reference checks, schema validation, and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,11,13,14,22,23,24],main_text_end_page=24,last_page_clip_y=644),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Exactly five actual main-text Theorems 3.1–3.5; Lemma 4.1 is not a Theorem. Supplementary bodies were excluded.','Theorems 3.1–3.2 use conditional expectation (bar-E), floor iteration counts, and a single event uniform over modes and iterations. Theorem 3.3 imports rate definitions, includes the originally named R^(0), and ends on page 14 without an additional iteration-count conclusion.','Theorem 3.4 has a minimum over modes, a squared norm, and strict 1/3 and 1/4 thresholds; Theorem 3.5 has an unsquared norm and no computational hypothesis.','Inventory only: original model and algorithm definitions, rate quantities, Assumption 1, Hypothesis I and its testing problem, and probability space (3.35) remain to be extracted and source-reviewed.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=registered['source_url'],registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=5,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original model, tensor operations, projections, algorithms, conditional Gaussian assumption and rate definitions; separately resolve HPC detection/Hypothesis I and the lower-bound probability space. Build paper-local theorem dependencies, finalize, reproduce and independently source-review all artifacts.'))
    print('Five complete main-text Theorems independently source-validated.')

if __name__=='__main__': main()
