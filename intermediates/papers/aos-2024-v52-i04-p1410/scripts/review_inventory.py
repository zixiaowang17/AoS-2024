"""Validate the independently enumerated and visually reviewed theorem inventory.

This checker pins a reviewed transcription. Changing the pin requires renewed PDF review.
"""
import datetime, hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
import fitz
from save_inventory import PID, REPO, ROOT, SHA
EXPECTED_INVENTORY_SHA='1d6cd09be6b0db4e865cb3ef1f4fcc8f60873068a98d8585bb57ba12eb790edc'

def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==31 and 'arXiv:2208.07610v2' in pdf[0].get_text()
    headings=[];text_hashes={}
    for n in range(1,24):
        page=pdf[n-1];text=page.get_text()
        path=ROOT/'evidence'/f'page-{n:02}.txt'
        assert path.read_bytes().decode()==text
        text_hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans'])
                match=re.match(r'^THEOREM (\d+)(?:\.| \()',s)
                if match:
                    assert line['spans'][0]['font']=='NimbusRomNo9L-Regu'
                    headings.append((n,match[1]))
    assert headings==[(7,'1'),(10,'2'),(10,'4')]
    assert 'ZHANG' in text and '2305.16539' in text
    assert 'APPENDIX' not in text
    assert 'APPENDIX A: INVARIANCE AND SUFFICIENCY' in pdf[23].get_text(clip=fitz.Rect(0,0,pdf[23].rect.width,80))
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
    assert r'\inf_{\boldsymbol\Pi_0,\boldsymbol\Pi_1}' in t['1']
    assert r'\min_{\boldsymbol\Pi_0,\boldsymbol\Pi_1}' in t['1']
    assert 'achieve the minimum on the right hand side' in t['1']
    assert 'In other words' in t['1'] and r'q_g^{V_n}(v_n(X^n))' in t['1']
    assert t['2'].count(r'1+\varepsilon')==2 and 'unit element' in t['2']
    assert 'Assumption 1 holds' in t['2'] and 'amenable' in t['2']
    assert 'Part 3 of Assumption 1' in t['4'] and 'for each $g\in G$' in t['4']
    assert 'there exists $h\in G$' in t['4'] and 'if and only if' in t['4']
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1410-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
      'The pinned source is the 31-page arXiv:2208.07610v2 PDF dated 17 October 2023. Main text and references end on page 23, with Appendix A on a separate page 24.',
      'Independent actual-heading enumeration confirms exactly Theorems 1, 2 and 4 on pages 7 and 10. Number 3 belongs to a Corollary and is not a missing Theorem. Proof headings and references do not add claims.',
      'The complete original bodies were visually compared. Theorem 1 retains the distinction between the full-data infimum and the attained reduced-data minimum, both optimal priors, its maximizing statistic and final GROW conclusion.',
      'Theorem 2 retains both 1+epsilon log-likelihood moment conditions under their different probability laws, the identity-element clarification and the unrestricted pair-of-priors infimum.',
      'Theorem 4 assumes only Part 3 of Assumption 1 and per-alternative existence of a finite-KL null member. Its oracle-value constancy and equivalence of the two optimality criteria are both preserved; amenability and the other assumption parts are not inserted.',
      'Inventory schema validation, mathematical-fragment checks and isolated exact regeneration passed. Full supporting-passage extraction and source audit remain pending.'
    ]
    review=dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent actual-heading enumeration, visual comparison of complete bodies, schema validation and isolated regeneration.',evidence=dict(page_text_sha256=text_hashes,visually_reviewed_pdf_pages=[1,7,10,23],boundary_crop='evidence/page-24-appendix-heading.png'),notes=notes)
    (ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2)+'\n')
    (ROOT/'evidence/source-provenance.json').write_text(json.dumps(dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',registered_version_alias='2208.07610v2.pdf',registered_url_alias='https://export.arxiv.org/pdf/2208.07610',checked_at=now),indent=2)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=3,source_pdf_sha256=SHA,next_action='Extract the original group model, mixture and KL conventions, e-statistics and GROW criteria, maximal invariance, amenability and the three separate assumption parts; independently audit all dependencies.'),indent=2)+'\n')
    print('Three complete original theorem statements independently checked; full census remains pending.')

if __name__=='__main__':main()
