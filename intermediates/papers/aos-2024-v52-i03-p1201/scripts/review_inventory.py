"""Record the completed visual inventory review of the pinned published PDF.

The expected inventory hash identifies the manually inspected transcription.
Changing it requires a new source review, not merely rerunning this script.
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

EXPECTED_INVENTORY_SHA = '720d8b346a7b3a7b67093bea38cb1b8bdb2c31005309656eb0aa8dac2d1da53e'


def main():
    source = Path(subprocess.check_output(
        [sys.executable, str(REPO / 'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SHA
    pdf = fitz.open(source)
    assert len(pdf) == 26
    assert 'DEEP NONLINEAR SUFFICIENT DIMENSION REDUCTION' in pdf[0].get_text()
    assert '10.1214/24-AOS2390' in pdf[0].get_text()
    headings = []
    text_hashes = {}
    for n, page in enumerate(pdf, 1):
        path = ROOT / 'evidence/published' / f'page-{n:02}.txt'
        assert path.read_bytes().decode('utf8') == page.get_text()
        text_hashes[str(n)] = hashlib.sha256(path.read_bytes()).hexdigest()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans'])
                match = re.fullmatch(r'THEOREM (\d+\.\d+)\.', text)
                if match:
                    headings.append((n, match[1]))
    assert headings == [(7, '3.2'), (10, '3.7'), (11, '3.8'), (14, '4.2'), (16, '4.4'), (17, '4.6')]
    assert 'SUPPLEMENTARY MATERIAL' in pdf[22].get_text()
    assert '[56]' in pdf[25].get_text()
    # Typography confirms that the last two consequences remain in Theorem 4.6.
    italic = [s['text'] for b in pdf[16].get_text('dict')['blocks']
              for line in b.get('lines', []) for s in line['spans'] if s['font'] == 'Times-Italic']
    assert 'Therefore' in italic and 'Moreover' in italic
    path = ROOT / 'theorem-inventory.json'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED_INVENTORY_SHA
    inv = json.loads(path.read_text())
    assert [(c['evidence'][0]['page'], c['label'].removeprefix('Theorem ')) for c in inv['claims']] == headings
    for c in inv['claims']:
        text = c['statement_original']
        assert not any(ord(ch) < 32 and ch != '\n' for ch in text)
        assert text.count(r'\[') == text.count(r'\]')
        assert len(re.findall(r'(?<!\\)\$', text)) % 2 == 0
        for display, inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$', text, re.S):
            depth = 0
            for brace in re.findall(r'(?<!\\)[{}]', display + inline):
                depth += 1 if brace == '{' else -1
                assert depth >= 0
            assert depth == 0
    validator = Path('skills/statistical-paper-census/scripts/validate_census.py')
    subprocess.run([sys.executable, str(validator), str(path)], check=True)
    with tempfile.TemporaryDirectory(prefix='p1201-inventory-rebuild-') as temp:
        subprocess.run([sys.executable, str(ROOT / 'scripts/save_inventory.py'), '--output-dir', temp], check=True)
        assert (Path(temp) / 'theorem-inventory.json').read_bytes() == path.read_bytes()
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    notes = [
        'All 26 PDF pages were searched for actual small-cap THEOREM environments. Six headings occur, in source order; citations, proof references, Lemmas 3.1 and 4.1, and Corollaries 4.3 and 4.5 are not theorem-inventory entries.',
        'Complete statement bodies were visually compared on PDF pages 7, 10, 11, 14, 16 and 17. The published title, authors, DOI and pagination were checked on page 1; page 23 has only an external-supplement notice, and references end on page 26.',
        'Theorem 3.2 includes the GMDD matrix, diagonalization convention, nondecreasing negative GMDD values and final centered-function definition. The typography remains italic through that entire passage.',
        'PDF fonts distinguish bold vector f from scalar components and fraktur M (EUFM10) from the calligraphic candidate class F. All distinctions are retained in the transcription.',
        'Theorem 3.7 retains the sign ambiguity and square-root factor with denominator 2 mu_j; the penalized minimizer is not identified with the unit-variance direction without rescaling.',
        'Theorem 3.8 preserves its separate positive-mu and stronger absolute-sum condition, and the exact reference to equation (6). No spectral-gap assumption is added to its printed body.',
        'Theorem 4.2 retains n >= V, delta > 0 and the n-3 denominator. Theorem 4.4 does not repeat n >= V, and no such restriction has been inserted into its original statement.',
        'Theorem 4.6 retains population previous directions inside L_j, the probability 1-(4j-3)delta, the supremum approximation term, the total-risk conclusion and the final expected-error bound. The last two consequences are visibly part of its italic theorem body, not following commentary.',
        'The final clause of Theorem 4.6 explicitly invokes Corollary 4.5. Its ReLU architecture, sample-size condition and Assumption (A3) must be resolved during dependency extraction even though Corollary 4.5 is not a theorem-inventory entry.',
        'No supplemental PDF or appendix body was opened. Definitions and dependencies, ambient conventions and the final census/source audit remain to be completed.',
        'The independent inventory validator passed, and the saved per-paper Python script rebuilt the inventory byte-for-byte in a new temporary directory.'
    ]
    review = dict(paper_id=PID, status='complete', source_checked=True, reviewed_at=now,
        source_pdf_sha256=SHA, inventory_sha256=EXPECTED_INVENTORY_SHA,
        theorem_ids=[c['claim_id'] for c in inv['claims']],
        method='Independent PDF heading enumeration, visual comparison of every complete theorem body and independent schema validation.',
        evidence=dict(page_text_sha256=text_hashes, visually_reviewed_pdf_pages=[1, 7, 10, 11, 14, 16, 17, 23],
                      reference_endpoint_pdf_page=26), notes=notes)
    (ROOT / 'inventory-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False)+'\n')
    prov = dict(inv['papers'][0], cached_pdf=str(source), registered_source=True,
                source_resolution='scripts/resolve_paper_pdf.py', checked_at=now)
    (ROOT / 'evidence/source-provenance.json').write_text(json.dumps(prov, indent=2, ensure_ascii=False)+'\n')
    checkpoint = dict(paper_id=PID, status='in_progress', stage='inventory_validated', updated_at=now,
        theorem_count=6, source_pdf_sha256=SHA,
        next_action='Extract original main-text definitions and conditions, including the Corollary 4.5 assumptions invoked inside Theorem 4.6; review all paper-local dependency paths, then finalize and independently audit the full census.',
        historical_source_search='source-search.json and source-search-checkpoint.json are earlier search records, superseded by the verified fixed local published PDF.')
    (ROOT / 'checkpoint.json').write_text(json.dumps(checkpoint, indent=2)+'\n')
    print('Six source-reviewed theorems saved; full census remains in progress.')


if __name__ == '__main__':
    main()
