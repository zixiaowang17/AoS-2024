"""Record the independent PDF inventory comparison and verify its fixed transcription."""
import datetime, hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
import fitz
from save_inventory import PID, REPO, ROOT, SHA
EXPECTED='9c90efd4cc75866fdf551eec848beeccc5c3b458899ab3d1bc778b0eaecc9cc7'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)==SHA
    pdf=fitz.open(source);assert len(pdf)==42
    first=' '.join(pdf[0].get_text().split())
    assert all(s in first for s in ['arXiv:2304.07003v1','14 Apr 2023','This version: April 17, 2023','Degui Li','Runze Li','Han Lin Shang'])
    boundary=pdf[21].get_text(clip=fitz.Rect(0,710,pdf[21].rect.width,750))
    assert 'Appendix A: Proofs of the main asymptotic results' in boundary
    headings=[];hashes={}
    for n in range(1,23):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,718.24) if n==22 else page.rect
        path=ROOT/'evidence'/f'page-{n:02}.txt';s=page.get_text(clip=clip)
        assert path.read_bytes().decode()==s
        hashes[str(n)]=digest(path)
        if n==22:assert 'disclaimer applies.' in s and 'Appendix A' not in s
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                text=''.join(x['text'] for x in line['spans'])
                m=re.match(r'^Theorem (\d+)\.',text)
                if m and line['spans'][0]['font']=='URWPalladioL-Bold':headings.append((n,int(m[1])))
    assert headings==[(8,1),(10,2),(12,3),(12,4)]
    path=ROOT/'theorem-inventory.json';assert digest(path)==EXPECTED
    inv=json.loads(path.read_text());claims=inv['claims'];assert len(claims)==4
    assert [c['claim_id'] for c in claims]==[PID+f'/T{n}' for _,n in headings]
    assert [[e['page'] for e in c['evidence']] for c in claims]==[[p] for p,_ in headings]
    t=[c['statement_original'] for c in claims]
    assert '(i) Under' in t[0] and '(ii) Under' in t[0] and all(f'({n})' in t[0] for n in ['3.10','3.11','3.12'])
    assert 'independent standard Brownian bridges' in t[0] and 'upper $\\alpha$-quantile' in t[0]
    assert t[0].count('jointly')==2 and r'\sqrt{N\vee T}' in t[0]
    assert all(f'({n})' in t[1] for n in ['4.2','4.3','4.4','4.5'])
    assert 'If, in addition' in t[1] and r'\geq c_\delta' in t[1]
    assert r'o_P\left([\ln(N\vee T)]^{1+\zeta}\right)' in t[1]
    assert 'arbitrarily small positive number' in t[1]
    assert 'Assumptions 1 and 2 are satisfied' in t[2] and r'\mid\widehat K=K_0' in t[2]
    assert 'Assumptions 1 and 2(i)' in t[3] and 'Assumptions 1 and 2 are' not in t[3]
    assert r'|\mathcal C_\bullet|=O(T^2)' in t[3] and r'T=O(|\mathcal C_\bullet|^{3/2})' in t[3]
    assert r'\frac{1}{|\mathcal C(b_k)|^{1/2}}' in t[3] and r'\|\delta_i\|^2\to\infty' in t[3]
    assert r'$\eta_{it}$ are independent over $i$' in t[3]
    assert r'\widehat b_k=b_k,k=1,\cdots,K_0' in t[3]
    for s in t:
        assert s.count('$')%2==0
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        assert not re.search(r'[\u4e00-\u9fff]',s) and not any(ord(c)<32 and c!='\n' for c in s)
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
    result=subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],capture_output=True,text=True,check=True)
    with tempfile.TemporaryDirectory(prefix='p1716-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED,theorem_ids=[c['claim_id'] for c in claims],printed_label_check=headings,
        method='Independent bold-heading enumeration across all admitted main-text pages, visual comparison of four complete statements, source-specific quantifier/formula checks, structural validation and byte-exact reproduction.',
        evidence=dict(page_text_sha256=hashes,visually_reviewed_pdf_pages=[1,8,10,12,22],page22_clip_y_max=718.24),validation=dict(returncode=result.returncode,stdout=result.stdout),
        notes=['All four theorem statements end on their starting pages; prose citations are excluded.',
               'Theorem 1 retains the joint-limit null result and both alternative results, with distinct limit regimes.',
               'Theorem 2 preserves the initial detection statement and stronger uniform localization branch with little-o in probability.',
               'Theorem 3 preserves conditional membership consistency given the estimated group count.',
               'Theorem 4 assumes only Assumption 2(i), retains both size-growth conditions and cross-subject independence, and asserts exact joint break recovery.',
               'The source title-page date and arXiv margin date differ; both are retained.',
               'An initial boundary probe on page 23 exposed opening appendix lines; no appendix result or proof was used or retained in this census. All saved evidence ends before the Appendix A heading on page 22.',
               'Full source-passage and dependency review remains pending.']))
    write('evidence/source-provenance.json',dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',checked_at=now))
    write('checkpoint.json',dict(paper_id=PID,stage='inventory_validated',inventory_status='validated',updated_at=now,theorem_count=4,source_pdf_path=str(source),source_pdf_sha256=SHA,next_action='Extract all main-text definitions and assumptions used by the four theorems, preserve source issues, reconstruct local dependencies, and independently validate the full census.'))
    print('Four complete main-text Theorems independently source-validated; interface census remains pending.')
if __name__=='__main__':main()
