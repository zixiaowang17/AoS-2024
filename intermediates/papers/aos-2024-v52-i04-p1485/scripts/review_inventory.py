"""Validate the independently enumerated and visually reviewed theorem inventory.

This checker pins a reviewed transcription. Changing the pin requires renewed PDF review.
"""
import datetime, hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
import fitz
from save_inventory import PID, REPO, ROOT, SHA
EXPECTED_INVENTORY_SHA='b92b493ebdbdd8ae58d7a88dfdc5ee2bf128bce75c78cf4b82742dcbf3dc0299'

def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==47 and 'arXiv:2301.06632v1' in pdf[0].get_text()
    headings=[];text_hashes={}
    for n in range(1,27):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,488.0146179199219) if n==26 else page.rect
        text=page.get_text(clip=clip)
        path=ROOT/'evidence'/(f'page-{n:02}.txt' if n<26 else 'page-26-before-appendix.txt')
        assert path.read_bytes().decode()==text
        text_hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans'])
                match=re.match(r'^Theorem (\d+\.\d+) \(',s)
                if match:
                    assert line['spans'][0]['font']=='CMBX12'
                    headings.append((n,match[1]))
    assert headings==[(12,'2.7'),(13,'3.1'),(14,'3.2'),(20,'5.1')]
    assert '[37]' in text and 'Lin Xiao' in text and 'APPENDIX' not in text.upper()
    boundary=pdf[25].get_text(clip=fitz.Rect(0,488,pdf[25].rect.width,510))
    assert 'Proofs from Section 2' in boundary
    path=ROOT/'theorem-inventory.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED_INVENTORY_SHA
    inv=json.loads(path.read_text())
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==headings
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
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in inv['claims']}
    assert r'$-A(\bar x)\in\widehat\partial f(\bar x)$' in t['2.7']
    assert 'unique multiplier vector' in t['2.7'] and 'if and only if' in t['2.7']
    assert r'$(0,\bar x)$' in t['2.7'] and r'\Sigma^\dagger' in t['2.7']
    assert r'\tag{3.3}' in t['3.1'] and 'square integrable' in t['3.1']
    assert r'\frac{\operatorname{lip}(\sigma)^{-1}}{2\mathbb E L}' in t['3.1']
    assert r'\sqrt{\frac{\epsilon_1}{2\mathbb E L}}' in t['3.1'] and 'measurable selection' in t['3.1']
    assert 'symmetric, quasiconvex, and lower semicontinuous' in t['3.2']
    assert r'\lim_{c\to\infty}\liminf_{k\to\infty}\sup_{\mathcal P\prime' not in t['3.2']
    assert r'\lim_{c\to\infty}\liminf_{k\to\infty}\sup_' in t['3.2'] and r'\mathcal B_{c/k}' in t['3.2']
    assert 'Assumption C, D, E, I, and J' in t['5.1']
    assert r'\gamma\in(\frac12,1)' in t['5.1'] and 'probability one' in t['5.1']
    assert r'\nabla\sigma(0)\cdot\Sigma\cdot\nabla\sigma(0)^\top' in t['5.1']
    assert r'\Sigma U' not in t['5.1'] and r'$(\bar x,0)$' in t['5.1']
    assert 'Moreover' in t['5.1'] and r'})^\dagger' in t['5.1']
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1485-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
      'The registered source is arXiv:2301.06632v1, 16 January 2023, 47 pages. References end above Appendix A on page 26; only the region before y=489.0146179199219 is retained. No appendix bodies were read.',
      'Independent bold-heading enumeration confirms exactly Theorems 2.7, 3.1, 3.2 and 5.1 on pages 12, 13, 14 and 20. Propositions, corollaries, lemmas and proof references are excluded.',
      'All four complete original statements were visually compared. Theorem 2.7 includes the multiplier existence/uniqueness and both directions of invertibility. Theorem 3.1 retains its random Lipschitz bound and both radius bounds. Theorem 3.2 retains the local minimax limit order and the full loss class.',
      'Theorem 5.1 retains all five referenced assumptions, the strict gamma range, almost-sure convergence, tangent coercivity, normal limit and the final pseudoinverse formula.',
      'Theorem 2.7 prints invertibility around (0,x-bar), while the definition and Theorem 5.1 use (x-bar,0). Assumption J defines a tangent-coordinate covariance but Theorem 5.1 multiplies it by ambient Jacobians without a basis transformation. These original source issues are retained for separate extraction notes.',
      'Inventory schema validation, mathematical-fragment checks and isolated exact regeneration passed. Supporting definitions and full source audit remain pending.'
    ]
    review=dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent actual-heading enumeration, visual comparison of complete bodies, schema validation and isolated regeneration.',evidence=dict(page_text_sha256=text_hashes,visually_reviewed_pdf_pages=[1,12,13,14,20,26],boundary_crop='evidence/page-26.png'),notes=notes)
    (ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2)+'\n')
    (ROOT/'evidence/source-provenance.json').write_text(json.dumps(dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2301.06632v1.pdf',registered_url_alias='https://export.arxiv.org/pdf/2301.06632',checked_at=now),indent=2)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=4,source_pdf_sha256=SHA,next_action='Extract the manifold and subdifferential definitions, smooth localization, SAA model and assumptions, divergence neighborhoods, and abstract stochastic-update assumptions; preserve source notation and covariance-coordinate discrepancies.'),indent=2)+'\n')
    print('Four complete original theorem statements independently checked; full census remains pending.')

if __name__=='__main__':main()
