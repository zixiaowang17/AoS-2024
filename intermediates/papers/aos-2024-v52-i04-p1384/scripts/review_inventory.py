"""Validate the independently enumerated and visually reviewed theorem inventory.

This checker pins a reviewed transcription. Changing the pin requires renewed PDF review.
"""
import datetime, hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
import fitz
from save_inventory import PID, REPO, ROOT, SHA
EXPECTED_INVENTORY_SHA='ee428c51634aa552349cd15c16cea93ee566114247b8ecf7a5ff68e1ff29afa6'

def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==49 and 'arXiv:2301.02168v2' in pdf[0].get_text()
    headings=[];text_hashes={}
    for n in range(1,23):
        page=pdf[n-1]
        clip=fitz.Rect(0,0,page.rect.width,296.2278137207031) if n==22 else page.rect
        text=page.get_text(clip=clip)
        path=ROOT/'evidence'/('page-22-before-appendix.txt' if n==22 else f'page-{n:02}.txt')
        assert path.read_bytes().decode()==text
        text_hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans'])
                match=re.match(r'^Theorem (\d+\.\d+)(?:\.| \()',s)
                if match and line['spans'][0]['font']=='CMBX10':headings.append((n,match[1]))
    assert headings==[(7,'2.1'),(8,'2.2'),(14,'3.1'),(16,'4.1')]
    assert 'Acknowledgments' in text and 'CCF-2106377' in text
    assert 'We review some notation' not in text
    path=ROOT/'theorem-inventory.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED_INVENTORY_SHA
    inv=json.loads(path.read_text())
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==headings
    assert [e['page'] for e in inv['claims'][0]['evidence']]==[7,8]
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
    assert all(r'\tag{'+x+'}' in t['2.1'] for x in ['2.7','2.8','2.9','2.10'])
    assert 'even about' in t['2.1'] and 'linear' in t['2.1'] and 'increasing function' in t['2.1']
    assert r'\frac12(x-\hat m)\otimes\hat S-\frac16(x-\hat m)^{\otimes3}' in t['2.2']
    assert all(r'\tag{'+x+'}' in t['3.1'] for x in ['3.8','3.9','3.10','3.11','3.12'])
    assert r'1-\exp(-C(nd)^{1/9})-5e^{-Cn}-n^{-d/4}' in t['3.1']
    assert r'\bar\theta=\int\theta d\pi(\theta)' in t['3.1'] and r'\|\bar m-\hat m\|' in t['3.1']
    assert r'\mathcal B_{s,\hat m}' in t['3.1']
    assert all(r'\tag{'+x+'}' in t['4.1'] for x in ['4.4','4.5','4.6','4.7'])
    assert 'under the conditions of Theorem 2.1' in t['4.1'] and 'orthogonal to all third order Hermite polynomials' in t['4.1']
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1384-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
      'The 49-page registered source is arXiv:2301.02168v2. The arXiv stamp says 7 January 2024; the title page says 9 January 2024. Both are retained in provenance.',
      'Independent bold-heading enumeration over all admitted pages confirms four Theorems: 2.1, 2.2, 3.1 and 4.1. Theorem 4.1 is included even though it occurs in a proof section. Theorem 2.1 on page 2 is a citation, not an environment.',
      'All four full original bodies were visually compared on pages 7-8, 14 and 16. Theorem 2.1 continues on page 8. All conditional branches, formulas, equation numbers and constant-dependence clauses are retained.',
      'Theorem 3.1 defines the posterior mean as bar-theta but prints bar-m in (3.12); it uses B_{s,hat-m} in (3.11), whereas page 8 names S_{hat-m}. Preserve the printed names, explaining their source correspondence separately.',
      'Theorem 4.1 retains the larger orthogonality class, not just the even-function special case. Its f_0 and p_3 meanings must be resolved from main-text passages during interface extraction.',
      'Main text ends after Acknowledgments on page 22. The appendix notation prelude begins at y=297.2278137207031, before the first lettered appendix heading. The evidence crop stops at y=296.2278137207031 and excludes that prelude and all appendix bodies.',
      'The inventory was independently schema-validated and reproduced byte-for-byte. Full interface extraction, dependencies and source review remain pending.'
    ]
    review=dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent actual-heading enumeration, visual comparison of complete bodies, schema validation and isolated regeneration.',evidence=dict(page_text_sha256=text_hashes,visually_reviewed_pdf_pages=[1,7,8,14,16],boundary_crop='evidence/page-22-boundary.png'),notes=notes)
    (ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2)+'\n')
    (ROOT/'evidence/source-provenance.json').write_text(json.dumps(dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2301.02168v2.pdf',registered_url_alias='https://export.arxiv.org/pdf/2301.02168',checked_at=now),indent=2)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=4,source_pdf_sha256=SHA,next_action='Extract original assumptions, canonical Gaussian solution, logistic model, tensor and Hermite conventions; finalize and independently review the full census.'),indent=2)+'\n')
    print('Four complete original theorem statements independently checked; full census remains pending.')

if __name__=='__main__':main()
