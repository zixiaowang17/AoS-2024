"""Independently enumerate and check the source-pinned two-Theorem inventory."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='d94e0a937373f014be400b0558abaa0e5168d35d149d796ae6c4757b7f5e3fff'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==36
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for s in ['A conformal test of linear models via permutation-augmented regressions','Leying Guan','arXiv:2309.05482v3','27 Dec 2023']:assert s in first,s
    # Inspect only the appendix heading, never its body.
    assert 'Proofs' in pdf[30].get_text(clip=fitz.Rect(85,382,550,403))
    labels=[];hashes={}
    for n in range(1,29):
        page=pdf[n-1];clip=None if n<28 else fitz.Rect(0,0,page.rect.width,478)
        f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                for span in line['spans']:
                    m=re.fullmatch(r'Theorem (\d+\.\d+)\.',span['text'].strip())
                    if m and span['font']=='CMBX12':labels.append((n,m[1]))
    assert labels==[(9,'3.3'),(12,'4.4')],labels
    last=(ROOT/'evidence/page-28.txt').read_text()
    assert 'Acknowledgment' in last and 'Funding' in last and 'References' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert [c['label'] for c in cs]==['Theorem 3.3','Theorem 4.4']
    assert [c['source_order'] for c in cs]==[1,2] and [[e['page'] for e in c['evidence']] for c in cs]==[[9],[12]]
    a,b=[c['statement_original'] for c in cs]
    for s in ['uniformly random permutations','condition 3.1',r'T_{0b}=T(\pi_0,\pi_b;x,Z,\varepsilon)',r'T_{b0}=T(\pi_b,\pi_0;x,Z,\varepsilon)',r'\mathbb P_{H_0}[p_{val}\leq\alpha]<2\alpha',r'all $\alpha>0$','both noise and permutation randomness']:assert s in a,s
    assert 'independent' not in a and 'PALMRT' not in a
    for s in ['Algorithm 2','Lemma 4.1',r'$(1-2\alpha)$','specified mis-coverage level']:assert s in b,s
    assert 'Corollary' not in b
    for c in cs:
        s=c['statement_original'];assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert 'PROOF' not in s and not any(ord(ch)<32 and ch!='\n' for ch in s)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2059-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True)
        assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-heading enumeration over all main-text pages, visual comparison of both complete statements, source-specific subpart checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[9,12,28],appendix_heading_clip=dict(page=31,y_min=382,y_max=403)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Theorem 3.3 retains its generic transferable statistic and strict error bound; independence is not inserted into the quotation.','Theorem 4.4 prints Lemma 4.1 although the referenced interval is in Corollary 4.1. The original wording is preserved.','This inventory gate does not certify the definitions/dependency census.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2309.05482',registered_version_alias='2309.05482v3.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=2,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract source definitions and assumptions, then independently validate the complete census.'))
    print('Both complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
