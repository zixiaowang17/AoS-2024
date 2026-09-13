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

EXPECTED_INVENTORY_SHA='08ca1d4906aaa37639a93e0fe3679e486c0ddc7fb9bd25402f28e3c2d927cdf4'


def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==42 and 'arXiv:2211.02496v2' in pdf[0].get_text()
    headings=[]
    text_hashes={}
    for n,page in enumerate(list(pdf)[:23],1):
        path=ROOT/'evidence'/f'page-{n:02}.txt'
        assert path.read_bytes().decode('utf8')==page.get_text()
        text_hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        assert not re.search(r'^APPENDIX\b',page.get_text(),re.M)
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                m=re.fullmatch(r'THEOREM (\d+\.\d+)\.',text)
                if m: headings.append((n,m[1]))
    assert headings==[(6,'2.3'),(7,'3.1'),(8,'3.2'),(9,'4.1'),(10,'4.3')]
    boundary=pdf[23].get_text(clip=fitz.Rect(0,0,pdf[23].rect.width,492.7498779296875))
    assert 'Theorem 4.1 follow' in boundary and 'APPENDIX' not in boundary
    assert (ROOT/'evidence/page-24-before-appendix.txt').read_bytes().decode()==boundary
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
    assert r'\mathcal I_\delta' in t['Theorem 2.3'] and 'or, equivalently' in t['Theorem 2.3']
    assert r'h(T)' in t['Theorem 3.1'] and r'h(0)' in t['Theorem 3.1']
    assert r'3\|G^{-1}\|_{\mathrm{op}}^2\|G_A\|_{\mathrm{op}}' in t['Theorem 3.2']
    assert '(i)' in t['Theorem 4.1'] and '(ii)' in t['Theorem 4.1']
    assert 'Theorem 4.1 remains valid' in t['Theorem 4.3']
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1307-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
        'The source is the 42-page arXiv:2211.02496v2 PDF dated 25 July 2024. The local register filename and export URL are aliases for the same verified bytes; the precise versioned URL is retained in the inventory.',
        'Five actual main-text theorem headings occur on pages 6,7,8,9,10: 2.3,3.1,3.2,4.1,4.3. Independent enumeration covers pages 1-23 and the main-text crop on page 24. Citations, proof headings, Lemmas and Corollaries are not theorem entries.',
        'All five full bodies were visually compared. Theorem 2.3 includes invertibility, Fisher-information convergence and both equivalent CLT displays, with the original norm of K squared in each covariance.',
        'Theorem 3.1 preserves both endpoint terms in its exact norm formula and all three terms in the subsequent inequality. The underlying Hilbert space is script H; the RKHS is plain H_X.',
        'Theorem 3.2 binds its finite process, both Gram matrices and scalar Sobolev space inside the statement. It preserves the squared inverse-Gram norm multiplying G_A and the coefficient 2 in the derivative term.',
        'Theorem 4.1 includes both small-error and constant-error regimes, their distinct local parameter neighborhoods, all constants and the final restriction to estimators of X_delta. No global parameter supremum replaces the local one.',
        'Theorem 4.3 preserves the reference to Theorem 4.1 rather than inventing an expanded original statement. Dependency extraction must inherit all its conditions and conclusions, then apply Assumption L to each of K, Delta K and (nabla dot b)K and include all three observation channels.',
        'Main text ends on page 24 after the proof conclusion for Theorem 4.1. The Appendix A heading at y=493.750 marks the boundary; no appendix bodies are admitted.',
        'The inventory passed the independent validator and rebuilt byte-for-byte in a fresh directory. Definitions, assumption clauses and the final census/source audit remain pending.'
    ]
    review=dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent actual-heading enumeration, visual comparison of complete bodies, typography check, schema validation and isolated rebuild.',evidence=dict(page_text_sha256=text_hashes,visually_reviewed_pdf_pages=[1,6,7,8,9,10],boundary_crop='evidence/page-24-boundary.png',before_appendix_text_sha256=hashlib.sha256((ROOT/'evidence/page-24-before-appendix.txt').read_bytes()).hexdigest()),notes=notes)
    (ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'evidence/source-provenance.json').write_text(json.dumps(dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2211.02496v2.pdf',registered_url_alias='https://export.arxiv.org/pdf/2211.02496',checked_at=now),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=5,source_pdf_sha256=SHA,next_action='Extract the SPDE model, local observations and augmented MLE, all separate clauses of Assumptions H and L, the general stationary convolution/RKHS setup, and inherited Theorem 4.3 conditions; finalize and independently review the full census.'),indent=2)+'\n')
    print('Five complete theorem statements independently checked; full census remains in progress.')

if __name__=='__main__':main()
