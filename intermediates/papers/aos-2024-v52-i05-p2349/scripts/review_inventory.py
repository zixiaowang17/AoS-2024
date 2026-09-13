"""Source check of all six main-text theorem environments before extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='446842ec4b5e0be41b7c7530b679e65e33059c65ea2e288676ccd78d4ed8cb82'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==25
    first=' '.join(pdf[0].get_text().split())
    for value in ['A NONPARAMETRIC TEST FOR ELLIPTICAL DISTRIBUTION','YIN TANG','BING LI','2306.10594v2','27 Mar 2024']:assert value in first,value
    assert 'SUPPLEMENTARY MATERIAL' in pdf[22].get_text(clip=fitz.Rect(0,546,pdf[22].rect.width,561))
    labels=[];hashes={}
    for n in range(1,24):
        page=pdf[n-1];clip=None if n<23 else fitz.Rect(0,0,page.rect.width,540)
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                ss=line['spans'];text=''.join(s['text'] for s in ss).strip()
                m=re.fullmatch(r'THEOREM (\d+)\.',text)
                if m:
                    assert any(v['text']=='HEOREM' and v['font']=='NimbusRomNo9L-Regu' and 8.7<v['size']<8.9 for v in ss)
                    labels.append([n,m[1]])
    expected=[[6,'1'],[13,'2'],[14,'3'],[18,'4'],[19,'5'],[19,'6']]
    assert labels==expected,labels
    last=(ROOT/'evidence/page-23.txt').read_text();assert 'Acknowledgments.' in last and 'SUPPLEMENTARY MATERIAL' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==6
    assert [c['source_order'] for c in cs]==list(range(1,7))
    for c,(page,num) in zip(cs,expected):
        assert c['label']=='Theorem '+num and c['evidence'][0]['page']==page and c['claim_id']==PID+'/T'+num
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
'1':['are characteristic',r'\mathcal M(\Omega_{U,\Theta},\mathcal F_{U,\Theta})','is injective'],
'2':['uniform metric','(5.11)',r'\sqrt n(\breve\Sigma_{U\Theta}-\Sigma_{U\Theta})',r'E[\Sigma_{U\Theta}^\star(X)\otimes\Sigma_{U\Theta}^\star(X)]','(5.10)'],
'3':['orthonormal basis',r'\|\Sigma_1\|_{\mathrm{HS}}=c>0',r'\Sigma_{U\Theta}=n^{-1/2}\Sigma_1',r'N(\sigma_j/\sqrt{\lambda_j},1)'],
'4':['defined as (7.1)',"0\\le\\kappa_U(u,u')\\le M_U",r't+4(M_UM_\Theta/n)^{1/2}',r'\frac{t^2n}{10M_UM_\Theta}'],
'5':['Assumption 2','Assumption 1','Assumption 3','Assumption 4',r'[c_7+2c_8/(\epsilon d)]',r'f_3(n,d,u)f_2(n,d,u)+c_5f_1(n,d,u)',r'n(c_6\epsilon)^d+7e^{-u}'],
'6':['all conditions in Theorem 5',r'\log n\prec d\prec n^{1/4}',r'\xrightarrow{P}']}
    for n,parts in checks.items():
        for part in parts:assert part in s[n],(n,part)
    assert 'H_0' not in s['2'] and 'Theorem 2' not in s['3']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2349-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-heading enumeration, visual comparison of all six complete theorem statements, source-specific checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[6,13,14,18,19,23],main_text_end_clip=dict(page=23,y_max=540)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Eight complete theorem environments; no appendix theorem is imported.','Preserve the full local alternative, reference (7.1), all concentration factors and Theorem6 growth regime.','This validates the inventory only; source-context extraction remains pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2306.10594',registered_version_alias='2306.10594v2.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=8,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract causal dependence, truncation, elliptical-test conventions, quadratic forms and local-linear smoothing; review theorem-specific scopes.'))
    print('All six theorem statements independently source-validated.')
if __name__=='__main__':main()
