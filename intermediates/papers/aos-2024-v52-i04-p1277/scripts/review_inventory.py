"""Record the independently checked inventory, pinned to the reviewed transcription.

A changed inventory requires renewed source comparison, not just a new expected hash.
"""
import datetime
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
import fitz
from save_inventory import PID, REPO, ROOT, SHA

EXPECTED_INVENTORY_SHA='d85c6082e27c748714910a2abb6f6dd680f7b462253f4f7c59d0aa1f43c7e83f'


def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==61 and 'arXiv:2210.01214v2' in pdf[0].get_text()
    headings=[]
    text_hashes={}
    for n,page in enumerate(list(pdf)[:55],1):
        path=ROOT/'evidence'/f'page-{n:02}.txt'
        assert path.read_bytes().decode('utf8')==page.get_text()
        text_hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        assert not re.search(r'^APPENDIX\b',page.get_text(),re.M)
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                m=re.fullmatch(r'THEOREM (\d+)\.',text)
                if m: headings.append((n,m[1]))
    assert headings==[(6,'2'),(8,'3'),(9,'4'),(12,'11')]
    boundary=pdf[55].get_text(clip=fitz.Rect(0,0,pdf[55].rect.width,146))
    assert '[58]' in boundary and 'APPENDIX' not in boundary
    assert (ROOT/'evidence/page-56-before-appendix.txt').read_bytes().decode()==boundary
    path=ROOT/'theorem-inventory.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED_INVENTORY_SHA
    inv=json.loads(path.read_text())
    assert [(c['evidence'][0]['page'],c['label']) for c in inv['claims']]==[(p,f'Theorem {n}') for p,n in headings]
    for c in inv['claims']:
        s=c['statement_original']
        assert not any(ord(ch)<32 and ch!='\n' for ch in s)
        assert s.count(r'\[')==s.count(r'\]') and len(re.findall(r'(?<!\\)\$',s))%2==0
        for display,inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if brace=='{' else -1
                assert depth>=0
            assert depth==0
    t={c['label']:c['statement_original'] for c in inv['claims']}
    assert r'\mathcal E^n' in t['Theorem 2'] and r'\delta^{1/2}' in t['Theorem 2']
    assert r'\kappa_0(H)=4-2^{2H}' in t['Theorem 3']
    assert 'm_{opt}>m>1/(4H)-2H-1' in t['Theorem 11']
    assert 'uniformly over' in t['Theorem 11']
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1277-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
        'The source is the 61-page arXiv v2 PDF dated 15 February 2024. Its precise versioned URL and version are retained; the local register uses the filename alias 2210.01214v2.pdf and an unversioned export URL for the same verified bytes.',
        'Four actual main-text theorem headings occur on pages 6,8,9,12, numbered 2,3,4,11. All admitted pages were independently enumerated. Numbering gaps reflect other result types, not omitted Theorems.',
        'All four complete bodies were visually compared. Theorem 11 includes the second paragraph, the intermediate m in the iteration condition, both normalized sequences and their uniform boundedness assertion.',
        'Theorem 2 preserves separate maxima for the H and eta rates; the logarithm multiplies only the n-dependent branch of the eta rate. The original experiment and data sigma-algebra use superscript n, not subscript n.',
        'Theorem 3 retains the strict threshold for nu_0, its eta^2 kappa_0(H) 2^(2H) expression and the exact kappa_0(H)=4-2^(2H). Positivity of nu_0 is given in the preceding estimator construction and must be resolved in extraction.',
        'Theorems 2 and 3 belong to the piecewise-constant volatility experiment; Theorems 4 and 11 belong to the continuous rough-volatility model and its more restricted parameter set. These experiments must not be conflated merely because the notation is reused.',
        'Fonts identify Euler-script A,E,D and blackboard P. Hats, iteration superscripts, H endpoints and all powers/logarithms are retained.',
        'References [56]-[58] end above the Appendix A heading at y=146.769 on page 56. Only that upper region was retained as main-text evidence; appendix theorem statements and definitions are excluded.',
        'The independent inventory validator passed and save_inventory.py reproduced identical bytes in an empty temporary directory. Full interface extraction and source audit remain pending.'
    ]
    review=dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent actual-heading enumeration restricted to the main text, visual comparison of every complete body, typography inspection, schema validation and isolated rebuild.',evidence=dict(page_text_sha256=text_hashes,visually_reviewed_pdf_pages=[1,6,8,9,12],boundary_crop='evidence/page-56-boundary.png',before_appendix_text_sha256=hashlib.sha256((ROOT/'evidence/page-56-before-appendix.txt').read_bytes()).hexdigest()),notes=notes)
    (ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'evidence/source-provenance.json').write_text(json.dumps(dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2210.01214v2.pdf',registered_url_alias='https://export.arxiv.org/pdf/2210.01214',checked_at=now),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=4,source_pdf_sha256=SHA,next_action='Extract the separate piecewise-constant and general volatility models and all estimator dependencies, including the main-text definition of kappa in equation (36); keep appendix-only definitions unresolved. Finalize and independently audit the full census.'),indent=2)+'\n')
    print('Four complete theorem statements independently checked; full census remains in progress.')

if __name__=='__main__':main()
