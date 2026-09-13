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

EXPECTED_INVENTORY_SHA='c0cd96dbcc6c68517fa98ca726e908b580f6c63512ad112300bf79c8c46ef8ef'


def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    pdf=fitz.open(source)
    assert len(pdf)==22 and '10.1214/24-AOS2392' in pdf[0].get_text()
    headings=[]
    text_hashes={}
    for n,page in enumerate(pdf,1):
        path=ROOT/'evidence'/f'page-{n:02}.txt'
        assert path.read_bytes().decode('utf8')==page.get_text()
        text_hashes[str(n)]=hashlib.sha256(path.read_bytes()).hexdigest()
        assert not re.search(r'^APPENDIX\b',page.get_text(),re.M)
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                m=re.fullmatch(r'THEOREM (\d+\.\d+) \(([^\n]+)\)\.',text)
                if m: headings.append((n,m[1],m[2]))
    assert headings==[(6,'2.1','LSD'),(7,'2.2','No outside eigenvalues'),(10,'2.3','CLT for LSS'),(13,'3.1','Test statistics')]
    assert 'SUPPLEMENTARY MATERIAL' in pdf[20].get_text() and '[19]' in pdf[21].get_text()
    italic=' '.join(s['text'] for b in pdf[10].get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['font']=='Times-Italic')
    assert 'nonoverlapping' in italic and 'contours' in italic
    path=ROOT/'theorem-inventory.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest()==EXPECTED_INVENTORY_SHA
    inv=json.loads(path.read_text())
    assert [(c['evidence'][0]['page'],c['label']) for c in inv['claims']]==[(p,f'Theorem {n} ({t})') for p,n,t in headings]
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
    assert r'F^{c,H}' in inv['claims'][1]['statement_original']
    t=inv['claims'][2]['statement_original']
    assert r'\underline m' in t and r'\bar m' not in t and 'nonoverlapping' in t
    assert r'\mathcal T_L' in inv['claims'][3]['statement_original']
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    with tempfile.TemporaryDirectory(prefix='p1254-inventory-') as temp:
        subprocess.run([sys.executable,str(ROOT/'scripts/save_inventory.py'),'--output-dir',temp],check=True)
        assert (Path(temp)/'theorem-inventory.json').read_bytes()==path.read_bytes()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes=[
        'Independent enumeration of all 22 pages found exactly four small-cap theorem headings. The title contains THEOREMS but is not a theorem heading; citations, proof references, lemmas and definitions are excluded.',
        'All four complete theorem bodies were visually compared against PDF pages 6, 7, 10, 11 and 13. Title, authors, DOI and page range were verified visually on page 1; pages 21 and 22 establish the supplement notice and reference endpoint.',
        'Theorem 2.1 preserves the Stieltjes equation and its companion-positive-imaginary-part uniqueness condition. No extra hypothesis is inserted into the original statement.',
        'Theorem 2.2 prints c and c_n where adjacent prose uses y and y_n. The original c notation is retained; its intended identification is a source ambiguity to record during extraction.',
        'Theorem 2.3 continues in italic prose at the top of page 11: positive closed contours, support enclosure and nonoverlap are part of its complete statement.',
        'The companion Stieltjes transform is UNDERLINED in the PDF, not overlined. The fourth moment is nu_4. PDF font spans confirm kappa, calligraphic I_2 and II, and blackboard T and P. Bold Theta appears in square-root factors while plain Theta appears in their arguments; plain Psi is also retained.',
        'Theorem 2.3 prints the unscaled L^c vector, whose definition on page 10 is an ESD difference integral without a p factor. No scaling is silently added. Existence and domain of the limiting parameters a(z) and d_2 require dependency review.',
        'Theorem 3.1 uses calligraphic T_L and T_F. Its first a subscript prints bold Sigma; subsequent a subscripts use plain Sigma. Both are preserved, without inferring distinct quantities. The p/n restriction is attached only to the first displayed limit.',
        'The theorem inventory was independently schema-validated and reproduced byte-for-byte in a new temporary directory. This certifies the saved inventory only; definitions, dependencies and the full census audit remain pending.'
    ]
    review=dict(paper_id=PID,status='complete',source_checked=True,reviewed_at=now,
        source_pdf_sha256=SHA,inventory_sha256=EXPECTED_INVENTORY_SHA,
        theorem_ids=[c['claim_id'] for c in inv['claims']],
        method='Independent PDF heading enumeration, visual comparison of full bodies, font inspection, schema validation and isolated rebuild.',
        evidence=dict(page_text_sha256=text_hashes,visually_reviewed_pdf_pages=[1,6,7,10,11,13,21,22]),notes=notes)
    (ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'evidence/source-provenance.json').write_text(json.dumps(dict(inv['papers'][0],cached_pdf=str(source),registered_source=True,source_resolution='scripts/resolve_paper_pdf.py',checked_at=now),indent=2)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,theorem_count=4,source_pdf_sha256=SHA,next_action='Extract and review original main-text definitions and Assumptions A-D; resolve Theorem 3.1 test statistics and quadratic-form functionals in Theorem 2.3; finalize and independently audit the full census.'),indent=2)+'\n')
    print('Four complete theorem statements independently checked; full census remains in progress.')

if __name__=='__main__': main()
