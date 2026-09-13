"""Independently enumerate and check the five source-reviewed theorem statements."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA
EXPECTED='16500150962804eeebb53cc6021d7c03f113a41b98911323cb7be34dad9e3752'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==80
    first=' '.join(pdf[0].get_text().split())
    for v in ['STEREOGRAPHIC MARKOV CHAIN MONTE CARLO','JUN YANG','GARETH O. ROBERTS','arXiv:2205.12112v2','21 Feb 2024']:assert v in first,v
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert registered['version']=='2205.12112v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2205.12112'
    assert [x for x in pdf.get_toc() if x[1] in ['Acknowledgement','Proofs of Main Results','Additional Simulations']]==[[1,'Acknowledgement',24],[1,'Proofs of Main Results',25],[1,'Additional Simulations',62]]
    labels=[];hashes={}
    for n in range(1,25):
        page=pdf[n-1];f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text();hashes[str(n)]=digest(f)
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                text=''.join(x['text'] for x in line['spans']).strip();match=re.match(r'^THEOREM\s+(\d+\.\d+)\b',text)
                if match:
                    assert all(x['font']=='NimbusRomNo9L-Regu' for x in line['spans'])
                    labels.append([n,match[1]])
    expected=[[7,'2.1'],[9,'2.2'],[14,'4.1'],[19,'5.1'],[20,'5.2']];assert labels==expected,labels
    end=(ROOT/'evidence/page-24.txt').read_text();assert 'Acknowledgement.' in end and 'Proofs of Main Results' not in end
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==5
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['claim_id']==PID+'/T'+n and c['label']=='Theorem '+n
        assert [e['page'] for e in c['evidence']]==[page]
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
'2.1':['positive and continuous','SPS is uniformly ergodic if and only if',r'\sup_{x\in\mathbb R^d}\pi(x)(R^2+\|x\|^2)^d<\infty'],
'2.2':['continuous first derivative in all components','SBPS is uniformly ergodic if',r'\limsup_{\{x:\|x\|\to\infty\}}',r'\frac{\partial\log\pi(x)}{\partial x_i}x_i',r'+2d<\frac12'],
'4.1':[r'c\le\lambda_i\le C',r'|\mu_i|\le C',r'R=d^{1/2}',r'\left|\sum_{i=1}^d\mu_i^2-\sum_{i=1}^d(1-\lambda_i)\right|=O(d^\alpha)',r'\alpha\le1','under stationarity',r'\mathbb E_{X\sim\pi_{\mu,\Sigma}}\mathbb E_{\widehat X\mid X}',r'\pi_{\mu,\Sigma}(\widehat X)(R^2+\|\widehat X\|^2)^d',r'\pi_{\mu,\Sigma}(X)(R^2+\|X\|^2)^d',r'\sqrt{\max\{\frac1d\sum_i|1-\lambda_i|,\frac1d\sum_i\mu_i^2\}}',r'\wedge d^{-(\frac12\vee\alpha)}'],
'5.1':['assumptions on the target in Section 5.1','not the standard Gaussian density','SPS chain is in the stationary phase',r'R=\sqrt d','Eq. (15)',r'\lambda=1',r'2\ell^2\cdot\Phi',r'\sqrt{\mathbb E_f\left[((\log f)\')^2\right]-1}'],
'5.2':['assumptions on $\pi$ in Section 5.1','not the standard Gaussian density','RSPS chain',r'X^d(0)\sim\pi',r'X^d(t)=(X_1^d(t),\ldots,X_d^d(t))',r'U^d(t):=X_1^d(\lfloor dt\rfloor)','weak convergence in Skorokhod topology',r'\mathrm dU(t)=(s(\ell))^{1/2}\mathrm dB(t)+s(\ell)\frac{f\'(U(t))}{2f(U(t))}\mathrm dt','speed measure','standard Gaussian cumulative density function']}
    # Apostrophes in raw single-quoted Python strings above need no TeX escaping.
    for n,parts in checks.items():
        for v in parts:assert v.replace("\\'", "'") in s[n],(n,v)
    assert 'if and only if' not in s['2.2'] and 'RSPS' not in s['5.1']
    assert 'Eq. (15)' not in s['5.2'] and '0.234' not in ''.join(s.values())
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2692-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent actual small-cap heading enumeration, visual comparison of all five complete statements, source-specific formula/reference checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,7,9,14,19,20,24],main_text_end_page=24),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Exactly five main-text Theorems, without printed titles. Exclude propositions, lemmas, corollaries, conjectures and supplementary bodies.','T2.1 is an equivalence; T2.2 is a sufficient condition with bound1/2, not the conjectured bound1.','T4.1 preserves both the mismatch-dependent fraction and the additional exponent restriction in the stepsize minimum.','T5.1 concerns SPS ESJD. T5.2 concerns RSPS, not original SPS; the printed text does not repeat Eq.(15), and keeps the phrase cumulative density function.','Inventory validated; interface extraction, local-dependency review and full census validation remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=registered['source_url'],registered_version_alias=registered['version'],checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=5,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original stereographic maps, transformed target, SPS and SBPS algorithms, uniform-ergodicity definitions, Gaussian target class, Section5.1 assumptions, scaling Eq.(15), ESJD and RSPS. Keep SPS/RSPS distinct; record source issues without reading supplementary proofs. Finalize, reproduce and independently review the full census.'))
    print('Five complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
