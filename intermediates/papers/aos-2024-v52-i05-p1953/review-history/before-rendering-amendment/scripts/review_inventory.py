"""Check the frozen transcription against retained source-review evidence."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='99a3a98a36492c665b2583fd5f4478f536e9201a4478a7b72c581519fc40a990'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==34
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for s in ['Improved covariance estimation','Roberto I. Oliveira','Zoraida F. Rico','arXiv:2209.13485v2','25 Mar 2024']:assert s in first
    boundary=pdf[26].get_text(clip=fitz.Rect(0,0,pdf[26].rect.width,145))
    assert 'The Appendix is divided into four main parts.' in boundary and 'Proof of Lemma 5.3' in boundary
    labels=[];hashes={};propositions=[]
    for n in range(1,27):
        page=pdf[n-1];f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==page.get_text();hashes[str(n)]=digest(f)
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                for s in line['spans']:
                    if s['font']!='CMBX10':continue
                    m=re.fullmatch(r'Theorem (\d+\.\d+)\.?',s['text'].strip())
                    if m:labels.append((n,m[1]))
                    if s['text'].strip()=='Proposition 2.2':propositions.append(n)
    assert labels==[(4,'1.3')] and propositions==[10]
    end=pdf[25].get_text();assert 'End of the argument:' in end and 'otherwise' in end.lower()
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    d=json.loads(f.read_text());assert len(d['claims'])==1
    c=d['claims'][0];s=c['statement_original'];assert c['claim_id']==PID+'/T1.3' and c['source_order']==1
    for phrase in ['There exists a constant','a measurable function','depending on','Assumption 1.2',r'\eta\in[0,1/2)',r'\eta\leq1/C\kappa_4^4',r'n\geq C\,(r(\Sigma)+\log(2/\alpha))',r'\sqrt{\frac{r(\Sigma)}n}+\sqrt{\frac{\log(2/\alpha)}n}',r'\eta^{1-\frac2p}',r'\mathbb R^{d\times d}_{\geq0}']:assert phrase in s,phrase
    assert 'universal' not in s and 'Proposition' not in s
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p1953-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True)
        assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id']],printed_label_check=labels,method='Independent bold-font environment enumeration over all 26 main-text pages, visual comparison of the complete theorem, source-specific formula checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,3,4,8,10,26]),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Proposition 2.2 is not promoted into the inventory by prose calling it Theorem 2.2.','Theorem 1.3 is an existence claim for a measurable estimator; its construction is not part of the original statement.','Original slash notation 1/C kappa_4^4 is preserved, with any intended reciprocal interpretation kept outside the quotation.','The appendix starts on page 27; no appendix-body material is included.']))
    write('evidence/source-provenance.json',dict(d['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2209.13485',registered_version_alias='2209.13485v2.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=1,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract Assumption 1.2, its moment constant, covariance and stable rank; independently review the completed census.'))
    print('Theorem 1.3 independently source-validated; Proposition 2.2 excluded.')
if __name__=='__main__':main()
