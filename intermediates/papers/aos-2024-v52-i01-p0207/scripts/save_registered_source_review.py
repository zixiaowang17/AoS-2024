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
    assert len(pdf) == entry['pdf_pages'] == 63
    assert all(s in pdf[0].get_text() for s in ['Changxiao Cai', 'T. Tony Cai', 'Hongzhe Li', '2211.12612v2'])
    headings = []
    for p in range(1, 21):
        page = pdf[p - 1]
        clip = fitz.Rect(0, 0, page.rect.width, 528) if p == 20 else page.rect
        text = page.get_text(clip=clip)
        suffix = '20-main' if p == 20 else f'{p:02}'
        assert (ROOT / f'evidence/revalidation/page-{suffix}.txt').read_bytes().decode('utf8') == text
        for block in page.get_text('dict', clip=clip)['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    match = re.match(r'^Theorem (\d+)', span['text'])
                    if match and span['font'] == 'SFBX1000':
                        headings.append((p, match[1]))
    assert headings == [(13, '1'), (14, '2'), (19, '3'), (19, '4')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 20
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is True
    assert 'Numerical experiments' in text
    direct = {'T1': {'D14', 'D4', 'D23'}, 'T2': {'D14', 'D4', 'D6'},
              'T3': {'D27', 'D4', 'D31', 'D13'}, 'T4': {'D27', 'D4', 'D6', 'D7', 'D10'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == 32 and len(census['interfaces']) == 31
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 82
    for it in census['interfaces']:
        for m in it['members']:
            selectors = m.get('highlight_symbols', []) + m.get('highlight_phrases', [])
            original = m['statement_original'] + '\n' + m['local_label']
            related = [c['statement_original'] for c in census['claims'] if c['claim_id'] in it['theorem_explanations']]
            assert any(s in original for s in selectors), m['local_id']
            assert all(any(s in t for t in [original] + related) for s in selectors), m['local_id']
    assert set(members['D22']['depends_on']) == {'D18', 'D19', 'D21', 'D1'}
    assert set(members['D22a']['depends_on']) == {'D18', 'D19', 'D30', 'D29', 'D1'}
    assert members['D22']['statement_original'] == members['D22a']['statement_original']
    related = {m['local_id']: {t['claim_id'] for t in it['related_theorems']}
               for it in census['interfaces'] for m in it['members']}
    assert related['D20'] == related['D21'] == {PID + '/T1'}
    assert related['D29'] == related['D30'] == {PID + '/T3'}
    history = ROOT / 'review-history/before-registered-source-review'
    for name in ['theorem-inventory.json', 'ranked-interfaces.json', 'unfinalized-census.json', 'source-passages.json']:
        assert digest(ROOT / name) == digest(history / name)
    corrections = json.loads((ROOT / 'source-transcription-corrections.json').read_text())
    for name, sha in corrections['original_files'].items():
        assert digest(history / name) == sha
    ambient = json.loads((ROOT / 'ambient-conventions.json').read_text())
    assert 'smallset' in ambient['auxiliary_passages'][0]['statement_original']
    assert 'smallset' in pdf[5].get_text()
    for item in audit['artifacts'].values():
        assert digest(ROOT / item['path']) == item['sha256']
    validator = Path('skills/statistical-paper-census/scripts/validate_census.py')
    results = []
    for name in ['theorem-inventory.json', 'ranked-interfaces.json']:
        result = subprocess.run([sys.executable, '-B', str(validator), str(ROOT / name)], text=True, capture_output=True, check=True)
        results.append(dict(artifact=name, returncode=result.returncode, stdout=result.stdout))
    findings = ['The registered local PDF is byte-identical to arXiv:2211.12612v2, 63 pages, with matching title and Changxiao Cai, T. Tony Cai and Hongzhe Li authorship. Its stamp is 25 January 2024. The registered resolver path supplied all fresh PDF reads and renders.', 'Independent main-text heading enumeration finds only Theorems 1 and 2 on pages 13 and 14 and Theorems 3 and 4 on page 19. All four original statements, upper/lower bound titles, exponents, constants and quantifiers were visually compared. Section 5 ends on page 20 above Appendix A; the fresh boundary crop includes its heading and excludes its body.', 'Theorem 3 retains kappa asymptotically comparable to one, uniform beta/gamma ranges and the logarithmic loss. Theorem 4 retains existence of b and its exact dependence on beta, C_beta, q-under, q-over and d. No upper-bound algorithm is imported into either lower bound.', 'Target and source reward laws, common conditional distributions in the covariate-shift model, source iid covariate-arm pairs, observed histories and expected regret were checked on pages 3 and 6-9. Within-vector arm independence is not imposed. The lower-bound history passage on page 14 omits source data while Section 2.1 includes it; both original passages and the unresolved note are retained.', 'Assumptions 1-3 and Definitions 1-2 were checked on pages 7-9. The second pointwise maximum excludes tied maximizers unless all rewards coincide; the margin condition restricts positive gaps. Transfer exponent is the smallest exponent with a positive ball-mass constant; exploration is the infimum over target support. Parameter-class shorthands preserve every original constant and constant K.', 'All bin, tree, visit-count, source-count and empirical-mean passages on pages 9-10 were checked. Closed bins and the closest-center-to-origin rule are retained. The visit count includes s=t although prose says prior to t; equation (8) has an unindexed Y, and tree depth uses the printed strict bound. These are recorded source conventions, not silently corrected.', 'Algorithm 1 and Procedure 1 were checked step by step on pages 11-12, preserving 24 and 25 numbered steps, branches, loop nesting, arm elimination, count updates, weighted reward updates and outputs. Confidence equation (9) and pull threshold (10) retain both zero/nonzero branches, log-plus and 1/0=infinity.', 'Projection (15), Definition 3 and Assumption 4 were compared on pages 15-16. The definition is for an individual Holder function, with two suprema at every integer level and zero projection on zero-mass bins. Assumption 4 requires one common arm self-similar under both target marginal and source law conditional on that arm. Its zero-arm-probability ambiguity is retained.', 'Algorithm 2 and Procedure 2 were checked against pages 17-18, preserving 26 and 21 numbered steps. Source/target sampling branches, all bandwidth and sample-size exponents, uniform target pulls, estimator numerator/denominator in (16), discrepancy maximization, smoothness clipping and source-data split remain intact. Printed grid equalities and ordinary log in the smoothness formula are preserved.', 'Adaptive confidence equation (17) uses beta-hat and its zero-pull branch prints ordinary log. Equation (18) supplies its own pull threshold. The two local Procedure 1 invocations preserve the shared printed body but different parameter substitutions. The adaptive invocation does not gain dependencies on the known gamma/kappa radius, despite the unchanged source initializer reference to (10).', 'All 31 readable titles, 32 source members, exact naming contexts, source kinds and highlight selectors were reviewed. All 15 direct uses, recursive local edges and 82 related explanations were checked. Known-parameter radius, threshold and Algorithm 1 reach only Theorem 1; adaptive radius, threshold and Algorithm 2 only Theorem 3; self-similarity reaches Theorems 3-4.', 'Three auxiliary passages were checked on pages 3, 6 and 9, including original reward-variable regret and the explanatory bin conditional mean. A high-resolution crop confirms that the PDF prints smallset, matching its TeX. A1 now preserves that spelling and its prior incorrect resolution note is fixed. The ambient generator was corrected; all original theorem statements and the entire ranked census remain byte-identical.', 'Existing source ambiguities involving strict floor/ceiling wording, conditional laws, omitted tuning inputs, finite sample budgets, square-root domains and algorithm output notation remain explicit. No appendix experiment, supplementary proof or proof-only construction was imported. This source review does not certify theorem proofs or repair the algorithms.']
    pages = [1, 3, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    for page, suffix in [(20, '20-main'), (6, '06-wording')]:
        evidence.append(dict(page=page, path=f'evidence/revalidation/page-{suffix}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{suffix}.png')))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results)
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed and independently validated: 4 Theorems, 31 interfaces, 32 source members, 82 related connections; one auxiliary spelling/note correction, inventory and census unchanged.')


if __name__ == '__main__':
    main()
