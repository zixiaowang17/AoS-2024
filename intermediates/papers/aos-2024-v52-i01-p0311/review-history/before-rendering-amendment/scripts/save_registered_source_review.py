"""Pin the manual PDF review; machine checks establish provenance and consistency."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import fitz

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
PID = ROOT.name


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = Path(subprocess.check_output([sys.executable, str(REPO / 'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    register = json.loads((REPO / 'corpus/aos/2024/local-pdf-manifest.json').read_text())
    entry = next(p for p in register['papers'] if p['paper_id'] == PID)
    audit = json.loads((ROOT / 'paper-audit.json').read_text())
    inv = json.loads((ROOT / 'theorem-inventory.json').read_text())
    census = json.loads((ROOT / 'ranked-interfaces.json').read_text())
    assert digest(source) == entry['sha256'] == audit['source']['pdf_sha256']
    pdf = fitz.open(source)
    assert len(pdf) == entry['pdf_pages'] == 51
    assert '2204.01803v1' in pdf[0].get_text()
    headings = []
    for n, page in enumerate(list(pdf)[:30], 1):
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                match = re.match(r'^Theorem\s+(\d+\.\d+)(?:\.| \()', ''.join(s['text'] for s in line['spans']))
                if match and line['spans'][0]['font'] == 'CMBX10':
                    headings.append((n, match[1]))
    assert headings == [(6, '3.1'), (20, '6.5')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 30
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    boundary = pdf[30].get_text(clip=fitz.Rect(0, 0, pdf[30].rect.width, 265))
    assert boundary == (ROOT / 'evidence/revalidation/page-31-heading.txt').read_bytes().decode('utf8')
    assert boundary.rstrip().endswith('Appendix A. Auxiliary Summation and Moment Formulas')
    direct = {'T3.1': {'D1', 'D4', 'D9', 'D10'}, 'T6.5': {'D11', 'D12', 'D13'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 13
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 13
    for it in census['interfaces']:
        for member in it['members']:
            selectors = member.get('highlight_symbols', []) + member.get('highlight_phrases', [])
            original = member['statement_original'] + '\n' + member['local_label']
            related = [c['statement_original'] for c in census['claims'] if c['claim_id'] in it['theorem_explanations']]
            assert any(s in original for s in selectors), member['local_id']
            assert all(any(s in t for t in [original] + related) for s in selectors), member['local_id']
    for item in audit['artifacts'].values():
        assert digest(ROOT / item['path']) == item['sha256']
    rebuild = json.loads((ROOT / 'evidence/revalidation/rebuild-check.json').read_text())
    assert len(rebuild['comparisons']) == 6
    for item in rebuild['comparisons']:
        assert item['matches_saved_bytes'] is True
        assert item['saved_sha256'] == item['regenerated_sha256'] == digest(ROOT / item['artifact'])
    validator = Path('skills/statistical-paper-census/scripts/validate_census.py')
    results = []
    for name in ['theorem-inventory.json', 'ranked-interfaces.json']:
        result = subprocess.run([sys.executable, '-B', str(validator), str(ROOT / name)], text=True, capture_output=True, check=True)
        results.append(dict(artifact=name, returncode=result.returncode, stdout=result.stdout))
    findings = ['The registered PDF matches the original 51-page arXiv:2204.01803v1 source by Axel Buecher and Cambyse Pakzad. The title page stamp is 4 April 2022 and manuscript date is April 6, 2022. The audit remains specific to this preprint and does not assume equivalence with the 2024 publication.', 'Independent enumeration of bold Theorem headings on pages 1-30 finds only Theorem 3.1 on page 6 and Theorem 6.5 on page 20. A plain-font Theorem 4.1 at the start of a line on page 6 continues a citation to Leung and Drton and is excluded. The attributed Hall and Heyde theorem is retained because it is printed as a theorem in the main document.', 'The main body ends with Section 6.7 and acknowledgments on page 29; references finish on page 30. A fresh crop on page 31 includes the separate supplement title, abstract and Appendix A heading only. All 30 extracted main-document texts match the registered PDF byte for byte. No appendix body was consulted.', 'Both full theorem statements were visually checked. Theorem 3.1 first assumes H5 and only a diverging dimension, then separately assumes H_(4m-3) and d=o(n^(1/(m-1))) for its joint limit. The product of m-1 standard normal laws, centering sequences and final replacement of delta_n(m) by bar-delta_n(m) remain verbatim.', 'Theorem 6.5 retains its a.s.-finite eta squared, zero-mean square-integrable martingale array, cross-row filtration inclusion, all three displayed conditional convergence conditions, and the mixed-normal conclusion with independent standard normal factor. Its extra punctuation after (6.26) is present in the PDF and retained.', 'Equation (6.24) visibly prints the first power of X_n,r in the truncated conditional expectation. Equations (6.25) and (6.26) use powers two and four. The stored quotation and existing warning preserve this discrepancy rather than replacing it with a conventional squared Lindeberg condition. Source review does not certify the truth of the theorem.', 'All 13 source entries were compared with the PDF. The sampling model has iid observations and continuous marginal cdfs. The displayed H_k copula equality specifies k-wise independence; the adjacent text says dependent and prints an inconsistent inclusion chain. Those source discrepancies remain separate review notes.', 'Ranks on page 3 use weak inequalities and pseudo-observations divide by n+1. The selected product process on page 4 centers at the finite-grid cdf U_n, rather than u_p. The Cramer-von-Mises statistic retains all observation pairs including diagonal terms, and its exact rank-kernel formula matches (2.1).', 'The expectation/variance definition (2.2) prints A as a subset of {2,...,d}; the aggregation (3.1) uses {1,...,d}. The mismatch is preserved and flagged. The explicit nu_n formula, finite-sample bar-delta and asymptotic delta retain their distinct constants and definitions.', 'All six auxiliary passages were checked: weak-convergence notation, fixed m and eventually sufficient d, marginal evaluation by setting outside coordinates to one, empirical copula context, conditional variance (6.25), and pairwise-independence endpoint H2. The marginal-evaluation prose typo should note is retained.', 'The array theorem has its own source binders. No assumption S_n,0=0 or monotonic d_n is added where absent; these source-domain issues remain recorded. The Lyapunov clause is a sufficient condition for the printed Lindeberg clause, not an additional simultaneous premise.', 'All 13 source-based names, naming contexts, highlight selectors, seven direct uses, local dependency paths and 13 explanations were reviewed. The test-statistic theorem does not gain a statement dependency on the generic martingale theorem merely because it is used in the proof. The combined statistic of Corollary 3.2 is not substituted for the inventoried results.', 'Original audit and census artifacts remain unchanged. The inventory and auxiliary writers were made callable without writing during import; the inventory now verifies its registered PDF instead of depending on a previously generated provenance file. Original scripts were archived. The separate rebuild reproduced all six census JSON artifacts byte for byte and used the shared validators.']
    pages = [1, 2, 3, 4, 5, 6, 20, 29, 30]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=31, path='evidence/revalidation/page-31-heading.png', sha256=digest(ROOT / 'evidence/revalidation/page-31-heading.png'), location='Supplement title, abstract and Appendix A heading only.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 2 Theorems, 13 source entries, 13 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
