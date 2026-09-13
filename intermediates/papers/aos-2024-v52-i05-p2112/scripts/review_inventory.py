"""Independently enumerate and check the source-pinned four-Theorem inventory."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='02db6d6df5649563e44bd7fd0ac099b2e1846a306b91be51575ee17031414ecf'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==41
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for s in ['Exact Minimax Optimality of Spectral Methods in Phase Synchronization and Orthogonal Group Synchronization','Anderson Ye Zhang','January 9, 2024','arXiv:2209.04962v2','6 Jan 2024']:assert s in first,s
    # Inspect only the appendix heading, never its body.
    assert 'Proofs of Lemma 3, Proposition 3, and Proposition 4' in pdf[31].get_text(clip=fitz.Rect(69,300,550,320))
    labels=[];hashes={}
    for n in range(1,30):
        page=pdf[n-1];clip=None if n<29 else fitz.Rect(0,0,page.rect.width,455)
        f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                for span in line['spans']:
                    m=re.fullmatch(r'Theorem (\d+)\.',span['text'].strip())
                    if m and span['font']=='CMBX10':labels.append((n,m[1]))
    assert labels==[(2,'1'),(5,'2'),(9,'3'),(12,'4')],labels
    last=(ROOT/'evidence/page-29.txt').read_text()
    assert 'Combining' in last and 'References' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert [c['label'] for c in cs]==['Theorem '+str(n) for n in range(1,5)]
    assert [c['source_order'] for c in cs]==[1,2,3,4] and [[e['page'] for e in c['evidence']] for c in cs]==[[2],[5],[9],[12]]
    a,b,c,d=[c['statement_original'] for c in cs]
    for t in [a,b]:
        for v in [r'\frac{np}{\sigma^2}\to\infty',r'\frac{np}{\log n}\to\infty',r'\delta=o(1)','As a consequence',r'\sigma=0','exactly']:assert v in t,v
    assert 'up to a phase' in a and 'up to an orthogonal matrix' in b and r'2\leq d=O(1)' in b
    for t in [c,d]:
        for v in [r'\frac{np}{\log n}>C_1',r'\frac{np}{\sigma^2}>C_2',r'\left(\frac{\sigma^2}{np}\right)^{1/4}+\sqrt{\frac{\log n}{np}}+\frac1{\log(np)}',r'1-n^{-9}-\exp\left(-\frac1{32}\left(\frac{np}{\sigma^2}\right)^{1/4}\right)']:assert v in t,v
    assert r'C_1,C_2,C_3>0' in c and r'C_1,C_2,C_3>0' not in d
    assert r'2\leq d\leq C_0' in d and r'\frac{d(d-1)\sigma^2}{2np}' in b and r'\frac{d(d-1)\sigma^2}{2np}' in d
    for c in cs:
        s=c['statement_original'];assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert 'PROOF' not in s and not any(ord(ch)<32 and ch!='\n' for ch in s)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2112-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True)
        assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-heading enumeration over all main-text pages, visual comparison of both complete statements, source-specific subpart checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[2,5,9,12,29],appendix_heading_clip=dict(page=32,y_min=300,y_max=320)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['The asymptotic and finite-sample versions are separate printed Theorems and all four are retained.','The italic no-additive-noise consequences are part of Theorems 1 and 2.','In Theorems 3 and 4, the square root covers log(n)/(np) only; the reciprocal log(np) term is outside it.','Theorem 4 does not print >0 after the three constants; the original wording is retained.','This gate validates the theorem inventory only; definition and dependency review remains pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2209.04962',registered_version_alias='2209.04962v2.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=4,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract source definitions and assumptions, then independently validate the complete census.'))
    print('All four complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
