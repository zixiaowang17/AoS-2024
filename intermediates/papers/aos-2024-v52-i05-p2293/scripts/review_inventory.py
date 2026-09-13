"""Source check of all eight main-text theorem environments before extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='4d14363d2f66e4ff235ecd999aeb9b3c2756d93368af1ab961666c6a02a48d04'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==60
    first=' '.join(pdf[0].get_text().split())
    for value in ['GAUSSIAN APPROXIMATION FOR NON-STATIONARY TIME SERIES','SOHAM BONNERJEE','SAYAR KARMAKAR','WEI BIAO WU','2408.02913v2','7 Aug 2024']:assert value in first,value
    assert 'SUPPLEMENTARY MATERIAL' in pdf[20].get_text(clip=fitz.Rect(0,421,pdf[20].rect.width,440))
    labels=[];hashes={}
    for n in range(1,22):
        page=pdf[n-1];clip=None if n<21 else fitz.Rect(0,0,page.rect.width,416)
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                ss=line['spans'];text=''.join(s['text'] for s in ss).strip()
                m=re.fullmatch(r'THEOREM (\d+\.\d+)\.',text)
                if m:
                    assert any(v['text']=='HEOREM' and v['font']=='NimbusRomNo9L-Regu' and 8.7<v['size']<8.9 for v in ss)
                    labels.append([n,m[1]])
    expected=[[5,'2.1'],[7,'2.2'],[7,'2.3'],[8,'2.4'],[8,'2.5'],[11,'3.1'],[13,'3.2'],[15,'4.1']]
    assert labels==expected,labels
    last=(ROOT/'evidence/page-21.txt').read_text();assert 'Acknowledgments.' in last and 'SUPPLEMENTARY MATERIAL' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==8
    assert [c['source_order'] for c in cs]==list(range(1,9))
    for c,(page,num) in zip(cs,expected):
        assert c['label']=='Theorem '+num and c['evidence'][0]['page']==page and c['claim_id']==PID+'/T'+num
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    checks={
'2.1':['independent but possibly not identically distributed',r'\gamma\ge2',r'\min\{|X_i|^\gamma/n^{\gamma/p},|X_i|^2/n^{2/p}\}',r'\mathbb E(S_i^2)'],
'2.2':['Conditions 2.2, 2.3, and 2.1',r'p^2-p-2+(p-2)\sqrt{p^2+10p+1}',r'{4p}',r'\operatorname{Cov}(X_s^\oplus,X_t^\oplus)',r'\left|S_i-\sum_{j=1}^iY_j^\oplus\right|'],
'2.3':['Conditions 2.2, 2.4 and 2.1',r'p^2-4+(p-2)\sqrt{p^2+20p+4}',r'{8p}',r'\operatorname{Cov}(Y_s,Y_t):=\operatorname{Cov}(X_s,X_t)'],
'2.4':['Conditions 2.2 and 2.1',r'\mathbb E(S_j^{\oplus2})',r'\mathbb E(S_j^2)',r'\sqrt{\log n}'],
'2.5':['Under conditions of Theorem 2.3',r'\mathbb E(S_j^2)'],
'3.1':[r'\sum_{1\le s\le t\le n}',r'|s-t|>D_n',r'\sup|a_{s,t}|\le1',r'\lceil n/D_n\rceil',r'D_n^{p/4}',r'D_n^{p/2-1}',r'\mu_{4,A}^4','depending only on'],
'3.2':['$A>1$','Condition 2.2',r'n^{(1-A\zeta_1)/2}'],
'4.1':['for $Z_i$',r'\mathbb E(S_{i-1}^2)',r'[\omega h_n,1-\omega h_n]',r'h_n^4=O(n^{1/p-1})',r'nh_n\to\infty',r'\beta=\int u^2K(u)\,du/2']}
    for n,parts in checks.items():
        for part in parts:assert part in s[n],(n,part)
    assert 'Condition' not in s['2.1'] and '2.3' not in s['2.4']
    assert r'\mathbb P^*' not in s['3.2']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2293-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-heading enumeration, visual comparison of all eight complete theorem statements, source-specific checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[5,6,7,8,11,13,15,21],main_text_end_clip=dict(page=21,y_max=416)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Eight complete theorem environments; no appendix theorem is imported.','Both original/truncated branches, distinct A thresholds, quadratic-form moment cases and the full local-linear bound are preserved.','This validates the inventory only; source-context extraction remains pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2408.02913',registered_version_alias='2408.02913v2.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=8,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract causal dependence, truncation, Gaussian approximation conventions, quadratic forms and local-linear smoothing; review theorem-specific scopes.'))
    print('All eight theorem statements independently source-validated.')
if __name__=='__main__':main()
