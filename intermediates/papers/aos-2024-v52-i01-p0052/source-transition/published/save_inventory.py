"""Save the published inventory after a separate PDF heading and statement review.

The preserved arXiv inventory is a transcription scaffold, not source authority.
Every body below was compared with the rendered published pages, including all
continuations. Do not promote the old interface census using this script.
"""
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess

import fitz

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parents[1]
REPO = PAPER.parents[3]
PID = PAPER.name
PAGES = [[7, 8], [9, 10], [12], [12, 13], [14], [15], [16],
         [17], [17], [19], [19, 20], [21]]
NUMBERS = ['2.2', '2.7', '2.11', '2.13', '3.1', '3.3', '3.4',
           '4.1', '4.4', '4.6', '4.8', '4.9']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def main():
    pdf = Path(subprocess.check_output(
        ['python3', str(REPO / 'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    assert digest(pdf) == '0e2a08097d0f62a375bcfe5821507276e09d86b68d9e720a0087887d3a574786'
    doc = fitz.open(pdf)
    assert len(doc) == 26
    observed = []
    for i, page in enumerate(doc, 1):
        text = page.get_text()
        assert (ROOT / 'evidence' / f'page-{i:02}.txt').read_bytes().decode('utf8') == text
        for match in re.finditer(r'^THEOREM (\d+\.\d+)\.', text, re.M):
            observed.append((match[1], i))
    assert observed == [(n, pp[0]) for n, pp in zip(NUMBERS, PAGES)]
    history = PAPER / 'source-history/arxiv-2107.01305v2'
    old_path = (history if (history / 'paper-audit.json').exists() else PAPER) / 'theorem-inventory.json'
    old = json.loads(old_path.read_text())
    assert old['papers'][0]['pdf_sha256'] == '8a21eebddf49f561327788c21c73fee3528e235684aa9342be9d8bd50c8a86fc'
    claims = copy.deepcopy(old['claims'])
    # Published copy-editing differences observed in the rendered statement bodies.
    claims[0]['statement_original'] = claims[0]['statement_original'].replace(
        '$P_k(\\theta_*)=0$, and', '$P_k(\\theta_*)=0$ and').replace(
        '$\\theta_*,\\mathsf{G},d,\\tilde{d}$, and', '$\\theta_*,\\mathsf{G},d,\\tilde{d}$ and')
    claims[1]['statement_original'] = claims[1]['statement_original'].replace(
        '(a) In the unprojected orbit recovery model,', '(a) In the unprojected orbit recovery model:').replace(
        '\\leq C\\sigma^{2k}$$', '\\leq C\\sigma^{2k},$$').replace(
        '$K$, and $d_k$', '$K$ and $d_k$').replace(
        '${\\widetilde{K}}$, and $\\tilde{d}_k$', '${\\widetilde{K}}$ and $\\tilde{d}_k$')
    claims[3]['statement_original'] = claims[3]['statement_original'].replace(
        'non-degenerate', 'nondegenerate').replace(
        '$\\mathcal{V}_k$, and $s_k$', '$\\mathcal{V}_k$ and $s_k$').replace(
        '$\\mathcal{\\widetilde{V}}_k$, and $\\tilde{s}_k$',
        '$\\mathcal{\\widetilde{V}}_k$ and $\\tilde{s}_k$').replace('Statement (2.)', 'Statement (2)')
    claims[6]['statement_original'] = claims[6]['statement_original'].replace(
        'non-empty', 'nonempty').replace('non-degenerate', 'nondegenerate')
    claims[11]['statement_original'] = claims[11]['statement_original'].replace(
        '$\\mathop{\\mathrm{trdeg}}(\\mathcal{R}_{\\leq 2}^\\mathsf{G})$, and',
        '$\\mathop{\\mathrm{trdeg}}(\\mathcal{R}_{\\leq 2}^\\mathsf{G})$ and')
    # Commas separating the displayed quantities are present in the journal PDF.
    for index in [5, 8, 10]:
        body = claims[index]['statement_original']
        body = body.replace('\\Big)^2\\\\\ns_2', '\\Big)^2,\\\\\ns_2')
        body = body.replace('\\Big)^2\\\\\ns_3', '\\Big)^2,\\\\\ns_3')
        claims[index]['statement_original'] = body
    for index in [9, 11]:
        body = claims[index]['statement_original']
        body = body.replace('&=S_0\\\\', '&=S_0,\\\\')
        body = body.replace('S_l<2l+1\\\\', 'S_l<2l+1,\\\\')
        body = body.replace('S_l \\geq 2l+1 \\end{cases}', 'S_l \\geq 2l+1, \\end{cases}')
        claims[index]['statement_original'] = body
    mapping = []
    for c, old_claim, number, pages in zip(claims, old['claims'], NUMBERS, PAGES):
        c['claim_id'] = PID + '/T' + number
        c['label'] = 'Theorem ' + number
        c['evidence'] = [
            {'page': p, 'location': c['label'] + (' (continued)' if j else '')}
            for j, p in enumerate(pages)]
        mapping.append({'previous_claim_id': old_claim['claim_id'],
                        'published_claim_id': c['claim_id'], 'published_pdf_pages': pages,
                        'mathematical_statement_comparison': 'Same hypotheses, formulas, conclusions and subparts after visual comparison; journal punctuation and word forms retained.'})
    paper = copy.deepcopy(old['papers'][0])
    paper.update(version='Published version, The Annals of Statistics 52(1), 2024, pp. 52–77; DOI 10.1214/23-AOS2292',
                 source_url='https://projecteuclid.org/journals/annals-of-statistics/volume-52/issue-1/Maximum-likelihood-for-high-noise-group-orbit-estimation-and-single/10.1214/23-AOS2292.pdf',
                 pdf_pages=26, pdf_sha256=digest(pdf), main_text_last_pdf_page=24,
                 main_text_boundary={
                     'location': 'Section 6 (Conclusion) ends on PDF page 24 (printed page 75), followed by Acknowledgments, Funding, a separate-supplement notice and References. References continue through PDF page 26. The appendices are in a separate supplementary PDF and were not opened.',
                     'shared_page_with_appendix': False},
                 intake_review={'status': 'complete', 'theorem_ids': [c['claim_id'] for c in claims],
                                'zero_theorems_confirmed': False})
    inventory = {'schema_version': 'statistical-theorem-inventory-v1',
                 'scope': {'theorem_scope': 'main_text_only'}, 'papers': [paper], 'claims': claims}
    save('theorem-inventory.json', inventory)
    validator = Path('skills/statistical-paper-census/scripts/validate_census.py')
    result = subprocess.run(['python3', '-B', str(validator), str(ROOT / 'theorem-inventory.json')],
                            text=True, capture_output=True, check=True)
    save('inventory-review.json', {
        'paper_id': PID, 'status': 'complete', 'scope': 'published theorem inventory only',
        'source_pdf_path': str(pdf), 'source_pdf_sha256': digest(pdf),
        'inventory_sha256': digest(ROOT / 'theorem-inventory.json'),
        'previous_inventory_sha256': digest(old_path),
        'method': 'Enumerated printed THEOREM headings independently across all 26 PDF pages, excluded in-text references and other result types, and visually checked every statement and continuation against the published PDF before reusing or correcting its transcription. Schema validation is a separate check and does not replace the visual review.',
        'appendices_read': False,
        'visually_reviewed_pdf_pages': [7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 24, 26],
        'statement_mapping': mapping,
        'specific_checks': [
            'Theorem 2.2 includes (a), (b), equations (2.7)–(2.11), all three remainder bounds, and the final paragraph describing parameter dependence.',
            'Theorem 2.7 retains all three unprojected conclusions and projected replacement clause, including (2.4), Proposition 2.6, the pseudo-inverse and sin-theta bound.',
            'Theorems 2.11 and 2.13 retain all constant-rank, genericity and nondegeneracy hypotheses. The bounded domain in 2.11(b) differs from the converse-only restriction in 2.13(b).',
            'Theorem 3.3 retains both expressions for s_3, the zero-inclusive versus positive-frequency sums, conjugates, phases, and constants 1/48, 1/16, 1/12 and 1/8.',
            'Theorems 3.4 and 4.1 retain their distinct thresholds L >= 30 and L >= 10.',
            'Theorem 4.4 is complete on page 17; page 18 begins commentary, not a continuation of its statement.',
            'Published Theorem 4.8 corresponds to old 4.9; published Theorem 4.9 corresponds to old 4.10. The former contains unprojected s_1,s_2,s_3 formulas; the latter projected transcendence degrees.',
            'Theorems 4.6 and 4.9 retain radial-bandlimit bounds >= 2 and >= 4 respectively and both branches of d(S_l). Theorem 4.8 retains bound >= 1 and s_3 coefficient 1/12.',
            'Corollaries, the Fact, Lemma and Proposition environments are excluded; references to external appendices are not additional theorem statements.'
        ],
        'validation': {'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr},
        'remaining_work': 'Re-extract and review published source passages, definitions, assumptions, local dependencies, source names, selectors and explanations before replacing the old census or counting this paper complete.'})
    print(result.stdout.strip())
    print('Saved published inventory and review; old artifacts preserved.')


if __name__ == '__main__':
    main()
