"""Independently verify the four visually reviewed theorem statements."""
import datetime,hashlib,json,re,subprocess,sys,tempfile
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
EXPECTED_INVENTORY_SHA='939bb32306c08da30cd081b769370ead274d4f2a800dfa86986255d5d1bd1f26'
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==93 and 'arXiv:2202.03369v2' in pdf[0].get_text()
    headings=[];hashes={}
    for n in range(1,29):
        p=pdf[n-1];clip=fitz.Rect(0,0,p.rect.width,200.71694946289062) if n==28 else p.rect
        text=p.get_text(clip=clip)
        path=ROOT/'evidence'/(f'page-{n:02}.txt' if n<28 else 'page-28-before-appendix.txt')
        assert path.read_bytes().decode()==text
        hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for b in p.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans'])
                m=re.match(r'^Theorem (\d+\.\d+)\.',s)
                if m and line['spans'][0]['font']=='CMBX10':headings.append((n,m[1]))
    assert headings==[(17,'3.1'),(20,'3.2'),(20,'3.3'),(21,'3.4')]
    assert 'Acknowledgements' in text and 'DMS-1712706.' in text and 'Empirical process lemmas' not in text
    assert 'Empirical process lemmas' in pdf[27].get_text(clip=fitz.Rect(0,200,pdf[27].rect.width,220))
    path=ROOT/'theorem-inventory.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED_INVENTORY_SHA
    inv=json.loads(path.read_text())
    assert len(inv['claims'])==4
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==headings
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in inv['claims']}
    assert '(J.1)' in t['3.1'] and '(M.4)' in t['3.1'] and r'\tag{3.4}' in t['3.1']
    assert r'K^{(2)}(0)' in t['3.1'] and r'2K^{(4)}(0)' in t['3.1']
    assert r'b_{0h}=h^{-1/2}' in t['3.1']
    assert r'E(B)_3' in t['3.1'] and 'E(B)' not in t['3.2']
    assert r'\delta_n(n\sqrt h)^{-1/2}g(a)' in t['3.2']
    assert r'c_0=\mathbb P\xi(\boldsymbol Z;\pi_0,\mu_0)' in t['3.2']
    assert r'\int g(a)\varpi(a)w(a)\,da=0' in t['3.2']
    assert r'\lim_{n\to\infty}n^{1/40}/\delta_n=0' in t['3.2']
    assert r'P(T_n>z_{n,1-\alpha})\to1' in t['3.2']
    assert all(r'\mathcal L(N(b_h,V))' in t[n] for n in ['3.3','3.4'])
    assert 'J_4' not in t['3.3'] and r'J_4(1,\mathcal F,L_2)<\infty' in t['3.4']
    for s in t.values():
        assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert not re.search(r'[\u4e00-\u9fff]',s)
        assert not any(ord(c)<32 and c!='\n' for c in s)
        for d,i in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for c in re.findall(r'(?<!\\)[{}]',d+i):
                depth+=1 if c=='{' else -1
                assert depth>=0
            assert depth==0
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1592-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    def write(name,d):(ROOT/name).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent bold-heading enumeration over admitted main text, visual comparison of all four original statements, schema and mathematical-fragment validation, and byte-exact inventory reproduction.',evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,17,20,21,28],boundary_crop='evidence/page-28.png'),notes=[
      'Four Theorems occur in the main text, all complete on their stated pages; no proofs or appendix theorem statements are included.',
      'Theorem 3.1 includes both the distribution approximation (3.3) and the complete mean/variance formula (3.4). Its appendix-labelled references (J.1) and (M.4) are retained as printed.',
      'Theorem 3.2 does not list E(B), retains varpi without a zero subscript, and requires n^(1/40)/delta_n to tend to zero. Its c0 uses blackboard P while its rejection probability uses ordinary P.',
      'Theorems 3.3 and 3.4 print b_h rather than b_0h. Only Theorem 3.4 explicitly adds J4 finiteness. Their preceding paragraphs define different residual-centering bootstrap rules; full dependency review is pending.',
      'The registered arXiv stamp is 22 May 2023 while the manuscript says 23 May 2023. Both dates are recorded.',
      'Appendix-heading hits during initial source location are excluded. Main-text evidence stops above Appendix A on the shared page 28. Full supporting-passage and source-issue resolution remain pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2202.03369v2.pdf',registered_url_alias='https://export.arxiv.org/pdf/2202.03369',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=4,source_pdf_sha256=SHA,next_action='Extract main-text causal and nuisance definitions, I/D/E assumptions, entropy and kernel conventions, Dudley metric and variance formula, and the two bootstrap rules. Preserve all source notation and reference issues before final source audit.'))
    print('Four complete original theorem statements independently validated; full census remains pending.')
if __name__=='__main__':main()
