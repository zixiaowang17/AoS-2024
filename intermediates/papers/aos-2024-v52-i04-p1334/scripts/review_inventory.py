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

EXPECTED_INVENTORY_SHA='726806cfadf96f4d8f3bf8b46bc037c0da11a16aa994cec7aea164f73417c750'


def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==67 and 'arXiv:2111.13551v1' in pdf[0].get_text()
    headings=[]
    text_hashes={}
    for n,page in enumerate(list(pdf)[:64],1):
        path=ROOT/'evidence'/f'page-{n:02}.txt'
        assert path.read_bytes().decode('utf8')==page.get_text()
        text_hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        assert not re.search(r'^APPENDIX\b',page.get_text(),re.M)
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                m=re.match(r'^Theorem (\d+\.\d+)\.',text)
                if m: assert line['spans'][0]['font']=='CMBX10'
                if m: headings.append((n,m[1]))
    assert headings==[(8,'3.3'),(12,'4.9'),(14,'5.2'),(15,'6.3')]
    boundary=pdf[64].get_text(clip=fitz.Rect(0,0,pdf[64].rect.width,399.5511779785156))
    assert 'Proof of Lemma 9.15.' in boundary and 'APPENDIX' not in boundary
    assert (ROOT/'evidence/page-65-before-appendix.txt').read_bytes().decode()==boundary
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
    assert r'p^kk^{3k}+k^{6k}' in t['Theorem 3.3']
    assert r'\mathcal P_{2k^*}^{sym}' in t['Theorem 4.9'] and '[f;I_0]]' in t['Theorem 4.9']
    assert 'suitable numerical constant $M>1$' in t['Theorem 5.2']
    assert t['Theorem 5.2'].count(r'\mathbb E') == 1
    assert r'(c\|E\|_{\psi_2}k)^{c\'k}' not in t['Theorem 6.3']  # an escaped apostrophe would corrupt the exponent
    assert "(c\\|E\\|_{\\psi_2}k)^{c'k}" in t['Theorem 6.3']
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1334-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
        'The source is the 67-page arXiv:2111.13551v1 PDF dated 26 November 2021. Precise versioned URL and PDF hash are pinned; the register filename and unversioned export URL are same-byte aliases.',
        'Independent bold-heading enumeration of pages 1-64 and the admitted crop on page 65 finds exactly Theorems 3.3,4.9,5.2,6.3 on pages 8,12,14,15. Propositions, Lemmas, Corollaries, citations and proof headings are excluded.',
        'All four complete theorem bodies visually compared. Theorem 3.3 retains all five variance-bound terms and k>=2; Theorem 6.3 instead starts at k>=1 and gives a squared-error bound under the separate sub-Gaussian setup.',
        'Theorem 4.9 preserves the local operator-norm bound, the ceiling-defined degree, the best symmetric-polynomial approximation error, subtraction and positive part, and the extra printed closing bracket after I0.',
        'Theorem 5.2 preserves the printed repeated suitable numerical constant M>1, the Wasserstein inequality without an expectation and its subsequent expected coordinate-error inequality. These source issues require separate notes, not silent corrections.',
        'Main text includes numbered proof Sections 8 and 9 through the end of Lemma 9.15 on page 65. Appendix A starts at y=400.551. Its heading is recorded as the boundary; no appendix bodies were read.',
        'Inventory validation and isolated byte-for-byte regeneration passed. Supporting definitions, assumptions, source issues, dependency extraction and complete source review remain pending.'
    ]
    review=dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent actual-heading enumeration, visual comparison of complete bodies, typography check, schema validation and isolated rebuild.',evidence=dict(page_text_sha256=text_hashes,visually_reviewed_pdf_pages=[1,8,12,14,15],boundary_crop='evidence/page-65-boundary.png',before_appendix_text_sha256=hashlib.sha256((ROOT/'evidence/page-65-before-appendix.txt').read_bytes()).hexdigest()),notes=notes)
    (ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'evidence/source-provenance.json').write_text(json.dumps(dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2111.13551v1.pdf',registered_url_alias='https://export.arxiv.org/pdf/2111.13551',checked_at=now),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=4,source_pdf_sha256=SHA,next_action='Extract original Schatten and singular-value definitions, the Hermite estimator, polynomial approximation error, Wasserstein estimator and separate noise assumptions; preserve source inconsistencies and independently review the full census.'),indent=2)+'\n')
    print('Four complete theorem statements independently checked; full census remains in progress.')

if __name__=='__main__':main()
