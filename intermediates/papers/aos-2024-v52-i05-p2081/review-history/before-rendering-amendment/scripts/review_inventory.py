"""Independently enumerate and check the source-pinned two-Theorem inventory."""
import datetime,hashlib,json,re,subprocess,sys,tempfile,unicodedata
from pathlib import Path
import fitz
from save_inventory import ROOT,REPO,PID,SHA,URL
EXPECTED='aff5b507d9b18c8af78aad41266da152d54fcb682ace045aa2c4cfc52820d6e4'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==73
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    for s in ['Estimating a density near an unknown manifold: a Bayesian nonparametric approach','Paul Rosa','Judith Rousseau','arXiv:2205.15717v3','17 Jul 2024']:assert s in first,s
    # Inspect only the appendix heading, never its body.
    assert 'Some facts on submanifolds with bounded reach' in pdf[33].get_text(clip=fitz.Rect(69,252,550,274))
    labels=[];hashes={}
    for n in range(1,30):
        page=pdf[n-1];clip=None if n<29 else fitz.Rect(0,0,page.rect.width,599)
        f=ROOT/'evidence'/f'page-{n:02}.txt'
        assert f.read_bytes().decode()==page.get_text(clip=clip);hashes[str(n)]=digest(f)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                for span in line['spans']:
                    m=re.fullmatch(r'Theorem (\d+\.\d+)\.',span['text'].strip())
                    if m and span['font']=='CMBX12':labels.append((n,m[1]))
    assert labels==[(14,'3.1'),(18,'3.4')],labels
    last=(ROOT/'evidence/page-29.txt').read_text()
    assert 'Acknowledgments' in last and 'funding' in last and 'References' not in last
    f=ROOT/'theorem-inventory.json';assert digest(f)==EXPECTED
    inv=json.loads(f.read_text());cs=inv['claims'];assert [c['label'] for c in cs]==['Theorem 3.1','Theorem 3.4']
    assert [c['source_order'] for c in cs]==[1,2] and [[e['page'] for e in c['evidence']] for c in cs]==[[14],[18]]
    a,b=[c['statement_original'] for c in cs]
    for t in [r'\omega>6\beta+(2\beta+D)(D-d)\log(1/\delta)/\log n','Table 1','partial location scale mixture','hybrid location scale mixture','mixture of finite mixtures','Dirichlet process mixture',r'\mathbb E_0^n',r'\mathcal X_n',r'\frac{1}{\sqrt{n\delta^{\frac D{2\alpha_0-\alpha_\perp}}}}',r'n^{-\frac\beta{2\beta+D}}']:assert t in a,t
    for t in [r'\sigma^{2\alpha_0-\alpha_\perp}=o(\delta)',r'\beta_M-4',r'for any $H>0$',r'\mathbb 1_{M^\tau}',r'\|L\|_\infty',r'0<\langle k,\alpha\rangle<\beta',r'D_z^k\overline{(\chi_j f_0)}_{x_j,\delta}',r'\Delta_{1,\delta}^{-1}\bar\Psi_{x_j}^{-1}',r'\tau/64','Section D.1','smooth and bounded functions']:assert t in b,t
    assert b.index('there exists a function')<b.index('for any $H>0$')
    assert 'probability density' not in b
    for c in cs:
        s=c['statement_original'];assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert 'PROOF' not in s and not any(ord(ch)<32 and ch!='\n' for ch in s)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(f)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p2081-inventory-',dir='/private/tmp') as tmp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',tmp],check=True)
        assert (Path(tmp)/'theorem-inventory.json').read_bytes()==f.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in cs],printed_label_check=labels,method='Independent bold-heading enumeration over all main-text pages, visual comparison of both complete statements, source-specific subpart checks, schema validation and byte-exact reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[14,18,29],appendix_heading_clip=dict(page=34,y_min=252,y_max=274)),validation=dict(returncode=result.returncode,stdout=result.stdout),notes=['Theorem 3.1 retains the posterior expectation, maximum of two rates, dimension/offset exponent and all prior alternatives.','Theorem 3.4 retains the full explicit signed-function expansion, the chart rescaling and its appendix-only partition reference. No appendix construction is imported.','The source theorem quantifies existence of g before any H>0; its original scope is retained.','This gate validates the theorem inventory only; definitions and dependencies remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,registered_source_url_alias='https://export.arxiv.org/pdf/2205.15717',registered_version_alias='2205.15717v3.pdf',checked_at=now))
    checkpoint=ROOT/'checkpoint.json'
    if not checkpoint.exists() or json.loads(checkpoint.read_text()).get('stage')!='complete':
        write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',theorem_count=2,source_pdf_path=str(source),source_pdf_sha256=SHA,updated_at=now,next_action='Extract source definitions and assumptions, then independently validate the complete census.'))
    print('Both complete main-text Theorems independently source-validated.')
if __name__=='__main__':main()
