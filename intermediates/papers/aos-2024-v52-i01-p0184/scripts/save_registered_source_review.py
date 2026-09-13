"""Pin the completed manual PDF review; automated checks do not replace it."""
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
    assert len(pdf) == entry['pdf_pages'] == 23
    assert all(s in pdf[0].get_text() for s in ['YEQING ZHOU', 'KAI XU', 'LIPING ZHU', 'RUNZE LI'])
    headings = []
    for p in range(1, 24):
        page = pdf[p - 1]
        assert (ROOT / f'evidence/revalidation/page-{p:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    match = re.match(r'^Theorem (\d+)\.', span['text'])
                    if match and span['font'] == 'NimbusRomNo9L-Medi':
                        headings.append((p, match[1]))
    assert headings == [(9, '1'), (9, '2'), (9, '3'), (11, '4'), (12, '5')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 23
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert 'SUPPLEMENTARY MATERIAL' in pdf[21].get_text() and 'REFERENCES' in pdf[21].get_text()
    assert 'satisfies satisfy' in pdf[9].get_text()
    assert 'In the above displays, the summations' in ' '.join(pdf[5].get_text().split())
    direct = {'T1': {'D1', 'D14', 'D18', 'D8', 'D10'},
              'T2': {'D1', 'D14', 'D18', 'D11', 'D10', 'D12'},
              'T3': {'D1', 'D14', 'D18', 'D12', 'D15'},
              'T4': {'D1', 'D2', 'D7', 'D16', 'D17'},
              'T5': {'D2', 'D3', 'D4', 'D5'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 18
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 55
    for it in census['interfaces']:
        for m in it['members']:
            selectors = m.get('highlight_symbols', []) + m.get('highlight_phrases', [])
            original = m['statement_original'] + '\n' + m['local_label']
            related = [c['statement_original'] for c in census['claims'] if c['claim_id'] in it['theorem_explanations']]
            assert any(s in original for s in selectors), m['local_id']
            assert all(any(s in t for t in [original] + related) for s in selectors), m['local_id']
    ambient = json.loads((ROOT / 'ambient-conventions.json').read_text())
    for auxiliary in ambient['passages']:
        related = {t['claim_id'] for it in census['interfaces']
                   if any(m['local_id'] in auxiliary['used_by_local_ids'] for m in it['members'])
                   for t in it['related_theorems']}
        assert related == set(auxiliary['related_theorem_ids'])
    history = ROOT / 'review-history/before-registered-source-review'
    assert digest(ROOT / 'theorem-inventory.json') == digest(history / 'theorem-inventory.json')
    corrections = json.loads((ROOT / 'source-transcription-corrections.json').read_text())
    for name, sha in corrections['original_files'].items():
        assert digest(history / name) == sha
    for item in audit['artifacts'].values():
        assert digest(ROOT / item['path']) == item['sha256']
    validator = Path('skills/statistical-paper-census/scripts/validate_census.py')
    results = []
    for name in ['theorem-inventory.json', 'ranked-interfaces.json']:
        result = subprocess.run([sys.executable, '-B', str(validator), str(ROOT / name)], text=True, capture_output=True, check=True)
        results.append(dict(artifact=name, returncode=result.returncode, stdout=result.stdout))
    findings = ['The registered PDF matches the 23-page PMC11064990 author manuscript and its original audit hash. Title and Zhou/Xu/Zhu/Li authorship were checked on page 1. Reads and fresh renders used the resolver-provided local file, without searching for a replacement.', 'An independent bold-heading scan over all 23 pages finds exactly Theorems 1-3 on page 9, Theorem 4 on page 11 and Theorem 5 on page 12. Theorem 3 continues on page 10 and Theorem 5 on page 13. Discussion, funding and references reach page 23; page 22 only announces a separate supplement. No appendix body is embedded or used.', 'All five original statements were visually compared, including all formulas and continuations. Theorem 3 retains the constant independent of n, p and q and the standard-normal cdf definition. Theorem 5 retains every integral, both monotonicity assertions and all six extrema. Its second coordinate range prints p rather than q and remains unchanged.', 'The full-vector independence null on page 1 and continuous random-sample setup on page 4 were checked. No independence between coordinates within one vector or unprinted k!=l requirement is imposed. The non-strict indices in the U-statistic display and distinct-element combination convention remain a recorded source inconsistency.', 'Definition 1 preserves the order-five D, order-six R and order-four tau-star permutation kernels. Their different psi anchor indices, 1/480, 1/2880 and 1/24 factors were compared. The source omega formula has its printed greater-than comparisons and the tau-star X arguments contain an extra comma; neither is replaced by a standard corrected kernel.', 'All four unranked auxiliary passages were checked on pages 4 and 9, including permutation sets, coordinate pairs, psi, omega and full observations. Their explicit used-by mappings and resulting theorem reach were verified independently against the finalized graph.', 'The conditional projections, centered recursion, finite factors 40/60/(2/3) and aggregate scaling were checked on pages 4-5. Theorem 4 uses the original local-alternative projection conditions, not the illustrative contamination family or a proof-only proposition.', 'The marginal cdf kernels and variance passages on pages 5-6 were compared. The paper alternates between full variance and leading-term asymptotic variance while Theorem 2 asserts exact unbiasedness; that ambiguity remains recorded. The six-index estimator retains every psi argument and the source distinct-permutation convention, without a fabricated square-root regularization.', 'Assumption 1 on page 7 retains separate p-divergent and q-divergent fourth-moment/cyclic-product limits. Theorems 1-3 retain max(p,q) divergence. Theorem 2 and 3 inherit conditions, not the conclusion of Theorem 1. The product kernel V used in Theorem 3 was checked on page 9.', 'Local-alternative equations (8)-(10) retain c in {1,3,...,d}, the n^(c-2) rate, cyclic fourth product and n*S_h^4 scale. Their own S_h definition is not replaced by the null product-of-marginal-variances identity. The M-hat coordinate-pair/full-observation argument inconsistency remains recorded.', 'One source-wording correction was made after visual comparison: D17 restores the printed repeated phrase satisfies satisfy. A high-resolution crop confirmed the existing D11 wording, including the article before summations. The generator was corrected and all dependent census artifacts regenerated. A structural comparison against the saved pre-review artifacts confirms this is the only census change. All original theorem statements remain byte-identical.', 'All 18 readable source terms/naming contexts, source kinds and selectors were checked. Terms such as Variance and Normal approximation index adjacent original prose rather than inventing names for symbolic helpers. All 25 direct uses, recursive paths and 55 related explanations were reviewed; null conditions reach only Theorems 1-3 and local-alternative conditions only Theorem 4.', 'The remaining source domain and normalization ambiguities are preserved in the audit. No supplementary proof, covariance example, computational shortcut, relative-efficiency proposition or simulation is imported as a theorem prerequisite. Source fidelity review does not certify the mathematical proofs.']
    pages = [1, 4, 5, 6, 7, 9, 10, 11, 12, 13, 21, 22, 23]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results)
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed and independently validated: 5 Theorems, 18 interfaces, 18 source members, 55 related connections; one source-wording correction, original theorem inventory unchanged.')


if __name__ == '__main__':
    main()
