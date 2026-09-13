"""Independently check six main-text theorem environments before interface extraction."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='576e85d4ffa01d85dd1e269189e9e1b06d9f24f981b3610bd271061de52083cb'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==56
    first=' '.join(pdf[0].get_text().split())
    for v in ['2112.14758v2','5 Apr 2024','Veeranjaneyulu Sadhanala','Yu-Xiang Wang','Addison J. Hu','Ryan J. Tibshirani']:assert v in first,v
    assert 'References' in pdf[28].get_text(clip=fitz.Rect(0,637,pdf[28].rect.width,pdf[28].rect.height))
    labels=[];hashes={}
    for n in range(1,30):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,637) if n==29 else None
        f=ROOT/'evidence'/f'page-{n:02}.txt';assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        rows={}
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                for span in line['spans']:
                    if span['font']=='NimbusRomNo9L-Medi':rows.setdefault(round(span['bbox'][1],1),[]).append(span)
        for y,spans in sorted(rows.items()):
            bold=' '.join(s['text'] for s in sorted(spans,key=lambda s:s['bbox'][0]))
            match=re.match(r'^Theorem\s+(\d+)\s*\.?$',bold)
            if match:labels.append([n,match[1]])
    expected=[[12,'1'],[15,'2'],[16,'3'],[16,'4'],[18,'5'],[18,'6']]
    assert labels==expected,labels
    last=(ROOT/'evidence/page-29.txt').read_text();assert 'Acknowledgements' in last and 'References' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert len(cs)==6
    for i,(c,(page,n)) in enumerate(zip(cs,expected),1):
        assert c['source_order']==i and c['label'].startswith('Theorem '+n) and c['claim_id']==PID+'/T'+n
        assert [e['page'] for e in c['evidence']]==[page]
    s={str(i):c['statement_original'] for i,c in enumerate(cs,1)}
    checks={
'1':['open, bounded, convex',r'\operatorname{BV}(U)',r'\int_{U_{-j}}',r'I_{x_{-j}}=[a_{x_{-j}},b_{x_{-j}}]','essential variation sense'],
'2':[r'u_1,\ldots,u_q\in\mathbb R^r',r'\mu/\sqrt n',r'\frac{\log r}n',r'\operatorname{nullity}(D)',r'\frac{|I|}n'],
'3':[r'C_n>0',r'\sqrt{\log n}',r'\frac{2s-1}{2s+1}',r'\frac\lambda nC_n'],
'4':[r'C_n\le n',r'\frac{C_n}n',r'\frac2{2s+1}'],
'5':[r'C_n\le\sqrt n',r'C_n^2/n\log(1+n/C_n^2)',r'\tau^d\asymp(C_nn^{s-1/2})^{1/s}',r'Q=[k+1]^d','without the additional log factor'],
'6':[r'\frac1{2s+1}','Holder embedding in (26)',r'\tau^d\asymp(B_n^2n^{2s})^{1/(2s+1)}',r'B_n\asymp L_nB_n^*',r'L_n^{2/(2s+1)}n^{-2s/(2s+1)}']}
    for n,parts in checks.items():
        for v in parts:assert v in s[n],(n,v)
    assert 'Wang et al. 2016' in cs[1]['label']
    assert 'estimator' not in s['1']
    for c in cs:
        t=c['statement_original'];assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2400-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True);assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-font heading enumeration, visual comparison of all six full statements, source-specific formula checks, schema validation and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[12,15,16,18,29],main_text_end_page=29),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['All six main-text Theorem environments; appendix bodies excluded.','Preserve essential variation, the credited generalized-lasso theorem, all three KTF tuning regimes, three minimax linear regimes, and the full T5–T6 attainment paragraphs.','Inventory validation only; source-context extraction remains pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2112.14758',registered_version_alias='2112.14758v2.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=6,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract anisotropic and essential variation, lattice difference operators, KTF/KTV/Sobolev classes, Gaussian risk definitions and projection estimators; independently review all source dependencies and rate qualifications.'))
    print('All six theorem statements independently source-validated.')
if __name__=='__main__':main()
