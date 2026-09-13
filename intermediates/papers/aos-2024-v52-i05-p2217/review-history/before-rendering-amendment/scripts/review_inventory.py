"""Source check of all four main-text theorem environments before extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='5673ccb3c00dc570ccfd12c349521395ac316099291a91794cbd27b2f415da22'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==24
    first=' '.join(pdf[0].get_text().split())
    for value in ['2024, Vol. 52, No. 5, 2217–2240','10.1214/24-AOS2433','SONGSHAN YANG','SHURONG ZHENG','RUNZE LI']:assert value in first,value
    assert 'SUPPLEMENTARY MATERIAL' in pdf[22].get_text(clip=fitz.Rect(0,110,pdf[22].rect.width,130))
    labels=[];hashes={}
    for n in range(1,24):
        page=pdf[n-1];clip=None if n<23 else fitz.Rect(0,0,page.rect.width,108)
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                ss=line['spans'];text=''.join(s['text'] for s in ss).strip()
                m=re.fullmatch(r'THEOREM (\d+\.\d+)\.',text)
                if m:
                    assert any(v['text']=='HEOREM' and v['font']=='Times-Roman' and 8.7<v['size']<8.9 for v in ss)
                    labels.append([n,m[1]])
    expected=[[5,'2.1'],[5,'2.2'],[7,'2.3'],[8,'2.4']]
    assert labels==expected,labels
    last=(ROOT/'evidence/page-23.txt').read_text();assert 'R01AI170249' in last and 'SUPPLEMENTARY' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==4
    assert [c['source_order'] for c in cs]==list(range(1,5))
    for c,(page,num) in zip(cs,expected):
        assert c['label']=='Theorem '+num and c['evidence'][0]['page']==page and c['claim_id']==PID+'/T'+num
    s={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in cs}
    assert [e['page'] for e in cs[1]['evidence']]==[5,6]
    assert 'almost surely' in s['2.1'] and r'E(w_j^4)=\kappa' in s['2.1']
    for token in [r'\frac{1+2y}{1-y}',r'\frac{n(n-1)(3n-6+p)}{4(n-2)^3(n-2+p)}',r'\beta_w=\kappa-3',r'\mathbf D_0',r'(\pi_1,\ldots,\pi_K)',r'\operatorname{tr}[(\mathbf R\mathbf D_1)^2]',r'\operatorname{tr}(\mathbf R\mathbf D_1)^2']:assert token in s['2.2'],token
    assert s['2.2'].count(r'\begin{aligned}')==2
    assert r'\widehat c=\frac1{1+p/(n-2)}' in s['2.3'] and r'\widetilde{\mathbf R}' in s['2.3']
    assert r'\widehat\sigma_0' not in s['2.4'] and r'c=(1+y)^{-1}' in s['2.4']
    assert r'\Phi(-z_\alpha)=\alpha' in s['2.4'] and 'alternative hypothesis' in s['2.4']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2217-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-heading enumeration, visual comparison of all four complete theorem statements, source-specific checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[5,6,7,8,22,23],main_text_end_clip=dict(page=23,y_max=108)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Four complete theorem environments; Theorem 2.2 crosses pages 5–6 and includes full centering, variance and auxiliary definitions.','Keep the a.s. conclusion of 2.1, arbitrary contrast wording and y=1 singularity in 2.2, and population versus estimated normalization in 2.3–2.4.','This validates the inventory only; source-context extraction remains pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias=URL,registered_version_alias='24-AOS2433-1.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=4,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract the linear correlation model, coefficient estimators, test statistic and complete normalizers; separate reused matrix symbols and source scope ambiguities.'))
    print('All four theorem statements independently source-validated.')
if __name__=='__main__':main()
