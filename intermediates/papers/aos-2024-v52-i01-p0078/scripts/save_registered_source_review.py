"""Save the source-content review of the fixed local StarTrek PDF.

This records the completed visual and dependency review. Assertions and schema
validation pin its evidence and do not substitute for that review.
"""
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
    inventory = json.loads((ROOT / 'theorem-inventory.json').read_text())
    census = json.loads((ROOT / 'ranked-interfaces.json').read_text())
    assert digest(source) == entry['sha256'] == audit['source']['pdf_sha256']
    pdf = fitz.open(source)
    assert len(pdf) == entry['pdf_pages'] == 87
    title = pdf[0].get_text()
    assert 'COMBINATORIAL VARIABLE SELECTION' in title and 'LU ZHANG' in title and 'JUNWEI LU' in title
    headings = []
    for page in range(1, 26):
        text = pdf[page - 1].get_text()
        assert (ROOT / f'evidence/revalidation/page-{page:02}.txt').read_bytes().decode('utf8') == text
        headings.extend((page, m[1]) for m in re.finditer(r'^THEOREM\s+(\d+\.\d+)', text, re.M))
    assert headings == [(7, '3.1'), (8, '3.3'), (11, '4.2'), (13, '5.2'), (15, '6.3')]
    assert [c['claim_id'] for c in inventory['claims']] == [PID + '/T' + number for _, number in headings]
    assert 'SUPPLEMENTARY MATERIAL' in pdf[25].get_text(clip=fitz.Rect(0, 0, 612, 80))
    assert inventory['papers'][0]['main_text_last_pdf_page'] == 25
    expected_direct = {
        'T3.1': {'D6', 'D7'}, 'T3.3': {'D6', 'D8'},
        'T4.2': {'D2', 'D5', 'D9', 'D10', 'D11', 'D4b', 'D13', 'D14a'},
        'T5.2': {'D2', 'D5', 'D15', 'D16', 'D4c', 'D19', 'D14b'},
        'T6.3': {'D2', 'D5', 'D20', 'D4d', 'D21', 'D23', 'D14b'},
    }
    for c in census['claims']:
        assert set(c['depends_on']) == expected_direct[c['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for i in census['interfaces'] for m in i['members']}
    assert len(members) == 27 and len(census['interfaces']) == 24
    assert set(members['D19']['depends_on']) == {'D14b', 'D17', 'D18'}
    assert set(members['D23']['depends_on']) == {'D14b', 'D21', 'D22'}
    assert set(members['D4b']['depends_on']) == {'D11', 'D12'}
    assert set(members['D21']['depends_on']) == {'D20', 'D4d'}
    for interface in census['interfaces']:
        for m in interface['members']:
            selectors = m.get('highlight_symbols', []) + m.get('highlight_phrases', [])
            passage = m['statement_original'] + '\n' + m['local_label']
            related = [c['statement_original'] for c in census['claims'] if c['claim_id'] in interface['theorem_explanations']]
            assert any(s in passage for s in selectors), m['local_id']
            assert all(any(s in text for text in [passage] + related) for s in selectors), m['local_id']
    for record in audit['artifacts'].values():
        assert digest(ROOT / record['path']) == record['sha256']
    results = []
    validator = Path('skills/statistical-paper-census/scripts/validate_census.py')
    for name in ['theorem-inventory.json', 'ranked-interfaces.json']:
        result = subprocess.run([sys.executable, '-B', str(validator), str(ROOT / name)],
                                text=True, capture_output=True, check=True)
        results.append({'artifact': name, 'returncode': result.returncode, 'stdout': result.stdout})
    findings = [
        'The fixed local source has the same SHA-256 as the previously reviewed arXiv:2108.09904v2, with the StarTrek title and authors Lu Zhang and Junwei Lu. All source reading in this review used the resolved local PDF.',
        'Fresh enumeration of actual THEOREM headings on PDF pages 1–25 gives exactly 3.1, 3.3, 4.2, 5.2 and 6.3, in that order. Ordinary theorem references are excluded. Page 25 ends in references; a cropped page-26 header confirms that supplementary material starts there without inspecting its body.',
        'All five complete theorem statements were compared with freshly rendered PDF pages. Theorem 3.1 retains the (log d)^5 Delta-infinity scaling, the tail-ratio supremum up to C0 sqrt(log d), and the (log d)^(5/2) Delta-infinity^(1/2) bound. It uses the centered pair specified above the theorem; variance conditions from Remark 3.2 are not inserted.',
        'Theorem 3.3 retains unit marginal variances, off-diagonal absolute covariance bound sigma0 < 1, a common disjoint zero-cross-block partition, and the Delta0 log(d)/fraktur-p tail bound. Its locally bound partition count is distinct from the tested graph component count in Section 5.',
        'Theorem 4.2 retains every term in its additional scaling condition, all three growing dimensions and the d0/d1 factor. Theorem 5.2 retains its estimator (5.1), multiplier quantiles (5.2), and d0/d factor. Theorem 6.3 prints FDP in both conclusions; both occurrences remain unchanged.',
        'D1–D5 were checked on pages 5–6: graph/degree testing, rejection-count FDP and expected FDR, the uncentered maximum statistic, the upper-tail infimum quantile, and every step of Algorithm 2. Absolute-entry sorting, inverse-quantile maximization over 1 <= s <= k_tau, inclusive BH comparison, alpha_(0)=0 and the empty-output branch are preserved. The source does not specify inverse/tie conventions or a full rectangular adaptation.',
        'D6–D8 were checked on page 7: U and V are centered Gaussian vectors; Delta-infinity is the largest absolute entry difference; Delta0 counts all differing covariance entries. Gaussianity, maximum norm and entrywise zero count are not conflated.',
        'D9–D13, D14a and D4b were checked on pages 9–10: iid multitask samples with conditionally independent diagonal Gaussian response noise; maximum row sparsity; debiased Lasso and constrained M construction; scaled-Lasso noise estimate; all covariance, subgaussian and tuning requirements in Assumption 4.1; the strong-hub fraction; and response-specific Gaussian calibration. The source use of columns next to a row-sparsity formula is preserved and noted.',
        'D15–D19, D14b and D4c were checked on pages 11–13: the initial precision estimator is separate from the standardized one-step input; the multiplier in (5.2) uses the initial estimator. The non-hub set uses the printed full row norm. The ordered dependence set retains all zero/nonzero and inequality constraints and permits the expressly mentioned repeated cross-indices.',
        'Assumption 5.1 retains both its signal/scaling condition and dependency/connectivity condition, including divisor p in the cardinality term. The graph component count is fixed in preceding prose. The invoked class U(M,s,r0) is not defined in the inspected main text and is retained as unresolved.',
        'D20–D23 and D4d were checked on page 14: the generic estimator has its stated edgewise linear representation; its centered error statistic differs from (2.2). Assumption 6.1 preserves uniformity over edge sets, the nested probability bound for multiplier approximation, independent normal multipliers, variance lower bound, and both psi1 bounds.',
        'The Section 6 dependency set uses nonzero influence covariance; it does not inherit the extra precision-pattern conditions or k1 != k2 from (5.3). Assumption 6.2 retains zeta2*d^4 and has no graph-component divisor p. The null count and signal fraction explicitly retain the Section 5 conventions.',
        'Read all 24 interface names, 27 original source passages and their selectors/naming contexts, all direct dependencies, recursive local edges and 38 source-specific theorem explanations. Same-paper paths preserve the model-specific calibrations and assumptions; Gaussian comparison theorems do not become dependencies of later theorem statements merely because they are used in proofs.',
        'The Section 1.3 conventions were checked on pages 4–5, including the probability meaning of X_n <= a + o_P(1), psi_l norm, elementwise max/zero-count norms, cardinalities and generic constants. No source content or theorem/census artifact needed modification in this revalidation.'
    ]
    evidence = [dict(page=page, path=f'evidence/revalidation/page-{page:02}.png',
                     sha256=digest(ROOT / f'evidence/revalidation/page-{page:02}.png'))
                for page in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 25]]
    evidence.append(dict(page=26, path='evidence/revalidation/supplement-boundary.png',
                         location='Cropped supplementary heading only; no appendix body read.',
                         sha256=digest(ROOT / 'evidence/revalidation/supplement-boundary.png')))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), method='source_content_revalidation',
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results)
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed and independently validated: 5 Theorems, 24 interfaces, 27 source members, 38 related connections; prior artifacts unchanged.')


if __name__ == '__main__':
    main()
