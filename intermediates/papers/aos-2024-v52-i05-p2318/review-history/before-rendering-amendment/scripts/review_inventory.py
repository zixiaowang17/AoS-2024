"""Independently check seven main-text theorem environments before interface extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='7cc4de36f103c6123bf559ab07ae2ab1f1950bb802d728181086be5186077816'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==58
    first=' '.join(pdf[0].get_text().split())
    for v in ['2308.15728v4','12 Aug 2024','Yuetian Luo','Chao Gao','Computational Lower Bounds for Graphon Estimation']:assert v in first,v
    assert 'References' in pdf[26].get_text(clip=fitz.Rect(0,250,pdf[26].rect.width,269))
    labels=[];hashes={}
    for n in range(1,28):
        page=pdf[n-1];clip=None if n<27 else fitz.Rect(0,0,page.rect.width,244)
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        rows={}
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                for span in line['spans']:
                    if span['font']=='SFBX1095':rows.setdefault(round(span['bbox'][1],1),[]).append(span)
        for y,spans in sorted(rows.items()):
            bold=' '.join(s['text'] for s in sorted(spans,key=lambda s:s['bbox'][0]))
            match=re.match(r'^Theorem\s+(\d+)\.',bold)
            if match:labels.append([n,match[1]])
    expected=[[4,'1'],[10,'2'],[12,'3'],[14,'4'],[16,'5'],[17,'6'],[18,'7']]
    assert labels==expected,labels
    last=(ROOT/'evidence/page-27.txt').read_text();assert '(41)' in last and 'References' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==7
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['label']=='Theorem '+n and c['claim_id']==PID+'/T'+n
        assert [e['page'] for e in c['evidence']]==([12,13] if n=='3' else [page])
    s={str(i):c['statement_original'] for i,c in enumerate(cs,1)}
    checks={
'1':[r'2\le k\le\sqrt n',r'\frac{ck}{nD^4}','Here the notation','degree no more than'],
'2':[r'\frac{(p-q)^2}{q(1-p)}',r'\frac{r}{(D(D+1))^2}',r'\frac{r(2-r)}{(1-r)^2n}','Here the notation'],
'3':[r"t_1=t_2=C'\log n",r"C''\left(\left(\frac{n(p-q)}k+C''\sqrt n\right)^{2t_1}k\vee(C''n)^{t_1+1}\right)",r'n\ge Ck\log^3n',r'1-n^{-\bar C}',r'\frac{c(k+\log n)\log^2n}{n}'],
'4':[r'\gamma>0.5',r'\sup_{\mathbb P_\xi}',r'n^{-\frac{2\gamma+1}{2\gamma+2}}/D^4'],
'5':[r'\frac1{2(D(D+1))^2}',r'\frac1k-\frac1{k^2}-\frac3n','In particular',r'\frac{n(p-q)^2}{k^2q(1-p)}','the lower bound (24) holds'],
'6':[r'\rho\ge\frac{ck^2}{n}',r"c'>0",r"\frac{c'\rho k}{nD^4}"],
'7':[r'\frac{k_1^2\wedge k_2^2}{n_1\vee n_2}',r'\frac{\lambda^2}{k_1^2\wedge k_2^2}',r'\frac{r(2-r)\lambda^2}{(1-r)^2(n_1\vee n_2)}']}
    for n,parts in checks.items():
        for v in parts:assert v in s[n],(n,v)
    assert 'C_1' not in s['3'] and 'C_2' not in s['3']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2318-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-font heading enumeration, visual comparison of all seven full statements, source-specific formula checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[4,10,12,13,14,16,17,18,27],main_text_end_clip=dict(page=27,y_max=244)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['All seven main-text Theorem environments; appendix bodies excluded.','T3 spans PDF pages12–13; visual primed constants take precedence over erroneous text-layer subscripts. T5 includes its in-particular clause.','Inventory validation only; source-context extraction remains pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2308.15728',registered_version_alias='2308.15728v4.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=7,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract original graphon/SBM and biclustering models, losses, polynomial classes, prior distributions, Algorithm1 and smooth graphon definitions; independently review scope and source issues.'))
    print('All seven theorem statements independently source-validated.')
if __name__=='__main__':main()
