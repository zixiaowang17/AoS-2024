"""Pin the manual PDF review; machine checks establish provenance and consistency."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata

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
    assert len(pdf) == entry['pdf_pages'] == 80
    assert '2208.04012v1' in pdf[0].get_text()
    assert 'Weilin Chen' in pdf[0].get_text() and 'Clifford Lam' in unicodedata.normalize('NFKC', pdf[0].get_text())
    headings = []
    for n, page in enumerate(list(pdf)[:38], 1):
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                match = re.match(r'^Theorem\s+(\d+)\.', ''.join(s['text'] for s in line['spans']))
                if match:
                    headings.append((n, match[1]))
    assert headings == [(10, '1'), (13, '2'), (15, '4'), (20, '6'), (21, '7'), (23, '8'), (24, '9')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 38
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert 'Table 7:' in pdf[37].get_text()
    assert 'Appendix: Basic Tensor Manipulations' in pdf[38].get_text(clip=fitz.Rect(0,0,pdf[38].rect.width,115))
    direct = {'T1': ['D2', 'D3', 'D4', 'D5', 'D15', 'D6', 'D8', 'D7', 'D10', 'D9'], 'T2': ['D2', 'D3', 'D4', 'D5', 'D15', 'D6', 'D8', 'D7', 'D14', 'D11'], 'T4': ['D2', 'D3', 'D4', 'D5', 'D15', 'D16', 'D17', 'D8', 'D7', 'D11', 'D12', 'D14', 'D13', 'D18'], 'T6': ['D2', 'D3', 'D4', 'D5', 'D15', 'D16', 'D17', 'D8', 'D21', 'D18', 'D7', 'D20'], 'T7': ['D2', 'D3', 'D4', 'D5', 'D15', 'D16', 'D17', 'D8', 'D21', 'D18', 'D7', 'D20'], 'T8': ['D2', 'D4', 'D22', 'D23'], 'T9': ['D2', 'D3', 'D4', 'D5', 'D15', 'D16', 'D17', 'D8', 'D21', 'D22', 'D18', 'D7', 'D20', 'D23', 'D24', 'D25']}
    for claim in census['claims']:
        assert set(claim['depends_on']) == set(direct[claim['claim_id'].split('/')[-1]])
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 25
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 103
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
    findings = ['The registered 80-page PDF is arXiv:2208.04012v1, stamped 8 August 2022, by Weilin Chen and Clifford Lam. Title, authors, version and SHA-256 match the pinned existing source. The review does not equate this preprint with the later journal publication.', 'Independent enumeration across main-text PDF pages 1-38 finds exactly seven Theorems, numbered 1, 2, 4, 6, 7, 8 and 9. Complete statements were visually checked, including the page continuations of Theorems 2 and 8. Section 6.4 ends after the portfolio tables and interpretation on page 38. The heading-only crop on page 39 confirms the start of Appendix Section 7; no appendix body was inspected.', 'Theorems 1, 2 and 4 retain their first loading-space assertions and distinct final eigenvector-alignment assertions under the additional L1-prime assumption. Their normalized factor sums, eigenvalue matrices, rank clauses, rotations, sample scales and complete error expressions were checked. Theorem 2 retains the printed missing pre subscript in its rank clause, and Theorem 4 retains the trailing comma in the d-minus-k subscript.', 'Theorem 6 retains every imported Theorem 4 assumption, RE1, its own displayed rate restrictions, b_k=o(1), the assumed first-step o_P(1) requirement and the additional iterative condition. Its unusual d_k=O(g_s)=(r_e+sqrt(T))S_psi expression is preserved. Theorem 7 retains its known-rank condition, reference to the m-th direction and the nested rate with both outer and inner g_s and loading-strength factors.', 'Theorem 8 retains only its explicitly listed E1, F1 and RE2 assumptions. The estimated direction is resolved as a defined object, without importing all of Theorem 6 rate hypotheses. Theorem 9 imports Theorem 6 assumptions, adds RE2 and its own two restrictions, preserves both eigenvalue cases and the full a_T(delta)=o(1) expression, and concludes consistency only for the stated eta_T=C a_T(0) choice. Subsequent pervasive-factor simplifications are outside the theorem.', 'All 25 source entries and ten auxiliary passages were checked. The tensor model retains mode-specific dimensions and loadings; the main-text fiber and unfolding formulas are preserved without importing the appendix indexing map. The error decomposition allows weak cross-fiber dependence through a shared component, and E2 and F1 use their separately specified general linear processes. No unprinted factor/noise independence is added.', 'The factor-strength, signal-cancellation and fourth-moment assumptions remain separate. L1 defines column norm exponents and a normalized Gram limit. L2 restricts full column sums; L2-prime restricts the maximum sampled-row sum scale. R2 has both a cross-sectional noise eigenvalue lower bound and a temporal coefficient-matrix spectral condition. RE1 retains all four trace/quadratic-form limits and the printed square placement.', 'The all-fiber PCA and selected-sample estimators were checked against pages 9-15. The maximum ratio selects one sample; pre-averaging aggregates covariance matrices of selected samples before eigenanalysis. Theorem 2 applies its assumptions to every chosen sample. Selected-scale comparability before Theorem 4 is an assumption of that population-parameter restatement, not a guaranteed effect of the algorithm and not an added hypothesis of Theorem 2.', 'The projected-data construction uses the other-mode Kronecker product and centered observations. The iterative algorithm and one-column pre-averaging initialization were checked against pages 17-18. Its printed step-2 k versus minus-k direction mismatch and idealized eigenvector sign convention remain documented. Neither a sample tie-breaking rule nor a correction of that dimension mismatch is invented.', 'The covariance in (5.4) explicitly treats the estimated direction as fixed; it is not silently relabeled as a conditional expectation. The sample and population-style correlation matrices remain distinct. The core rank estimate uses eigenvalues strictly greater than 1+eta_T and a maximum index. Zero denominators, nonpositive diagonal entries and an empty rank-selection set remain unresolved source conventions.', 'Page 9 revealed four missing tilde accents on the summed noise vector in D9: its definition, normalization and two entries of the stacked matrix. The accents were restored in the saved extraction and regenerated JSON. Individual-fiber noise symbols were left unchanged. The prior JSON and scripts were archived before correction; a recursive artifact comparison verified only the intended source and relationship changes.', 'The D7 explanation for Theorem 9 was clarified: the loading SVD reference direction occurs in the small-error conditions inherited from Theorem 6, rather than in the eigenvalue conclusion itself. Page 20 evidence was added. All 25 natural-language titles, naming passages and highlight selectors, 78 direct uses, recursive local dependencies and 103 related-theorem explanations were reviewed. The theorem inventory and dependency counts are unchanged.', 'The source conventions concerning bare d and r, the L1-prime description of Gram eigenvalues as singular values, the traced-square notation, [d_k]/[r_k] and the narrow explicit hypothesis list of Theorem 8 remain visible. Original statement wording is preserved; this is not a proof verification or a repair of the paper.', 'The per-paper scripts now provide an isolated rebuild entry point that verifies the fixed registered PDF. Old scripts remain archived. All six census JSON artifacts regenerated byte for byte and passed independent structural validation in a separate directory. The reproduction check does not substitute for this manual source review.']
    pages = [1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 38]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.extend([dict(page=9,path='evidence/revalidation/page-09-fiber-sums.png',sha256=digest(ROOT/'evidence/revalidation/page-09-fiber-sums.png')),dict(page=39,path='evidence/revalidation/page-39-heading.png',sha256=digest(ROOT/'evidence/revalidation/page-39-heading.png'))])
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 7 Theorems, 25 source entries, 103 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
