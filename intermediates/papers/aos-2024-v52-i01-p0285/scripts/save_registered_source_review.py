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
    assert len(pdf) == entry['pdf_pages'] == 31
    assert '2201.01036v1' in pdf[0].get_text()
    headings = []
    for n, page in enumerate(list(pdf)[:19], 1):
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                match = re.match(r'^THEOREM\s+(\d+\.\d+)(?:\.| \()', ''.join(s['text'] for s in line['spans']))
                if match:
                    headings.append((n, match[1]))
    assert headings == [(6, '2.4'), (7, '2.5'), (11, '3.2')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 19
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert [1, 'Appendices', 20] in pdf.get_toc()
    assert pdf[19].get_text(clip=fitz.Rect(0, 0, pdf[19].rect.width, 85)).strip() == '20\nAppendices.'
    direct = {'T2.4': {'D1', 'D6', 'D8', 'D5', 'D9'}, 'T2.5': {'D1', 'D9', 'D10', 'D11', 'D5'}, 'T3.2': {'D14', 'D12'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 14
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 21
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
    findings = ['The registered local PDF is arXiv:2201.01036v1, 31 pages, with the 4 January 2022 stamp, title and authors Wen Wang, Shihao Wu, Ziwei Zhu, Ling Zhou and Peter X.-K. Song. It matches the original audit hash. This is a source-version-specific census, not an assertion that its statements match the later 2024 publication.', 'Fresh text for pages 1-19 was compared byte for byte against the registered PDF. Independent THEOREM line enumeration finds exactly 2.4 on page 6, 2.5 on page 7 and 3.2 on page 11. All three complete statements were visually checked. Page 19 ends with Discussion and acknowledgments; the outline and heading-only crop confirm Appendices begins on page 20. No appendix body was read.', 'Theorem 2.4 retains K=K0 and s=s0, the probability of disagreement between the grouped and oracle estimators, all constants in its exponential bound, the sufficient sensitivity condition with d1>27 and the n,p asymptotic grouping-risk conclusion.', 'Theorem 2.5 defines its ratio r inside the statement. Its numerator is the largest normalized squared design-column norm and its denominator minimizes grouping sensitivity over the separated/balanced class. Both minimax inequalities, their logarithmic floor expression and the full parameter range remain intact. The subsequent restricted-eigenvalue conjecture is not a theorem premise.', 'Theorem 3.2 retains L>l, a real limiting objective value c, every positive integer M, the minimum squared successive-iterate distance and the denominator M(L-l). The source asserts decreasing objective values toward c, not convergence to a specified global optimizer.', 'All 14 source entries were compared with the PDF. D2 omitted the article in Define the parameter space on page 5; that word was restored in the source quotation and extraction script. The formula, all three theorem records and the dependency graph remain unchanged. Prior artifacts and scripts were archived before the correction.', 'The linear model on page 2 includes Gaussian scalar errors and iid observations, grouped nonzero coefficients and unrestricted nuisance coefficients. The passage does not explicitly impose conditional error independence from the covariates; no extra design or conditional-law assumption is inserted.', 'The feasible class and L0-Fusion optimization on pages 3-5 bound the number of distinct nonzero coefficient values and support size separately. The zero class is excluded from the grouping operator. Definition 2.1 uses an injection from the smaller grouping into the larger one; neither its direction nor its set unions are replaced by a symmetric metric.', 'Grouping sensitivity on page 5 minimizes prediction discrepancy over incorrectly grouped feasible alternatives and divides by n times max(d,1). The oracle on page 6 retains both the group-equality constraint and the collapsed-design least-squares expression. Possible failure of attainment or equality between those formulations is recorded separately, without adding rank or fitted-nonzero conditions.', 'The classes on page 7 separately impose sensitivity at least ell and separated signal strengths with balanced group sizes. Their original group labels and denominator edge cases remain explicit. The four source auxiliaries preserve matrix dimensions, estimator naming, K0 versus s0, notation and the projection implementation reference.', 'The general convex objective on page 9 is bounded below and has a gradient Lipschitz condition on Theta(K,s). Page 10 defines set-valued projection and all inputs, three steps and output of Algorithm 2. Arbitrary initialization versus the restricted smoothness domain, and finite stopping versus the theorem infinite sequence, remain unresolved source conventions. The appendix projection subroutine is not opened.', 'All 14 source-derived titles and naming contexts, highlight selectors, 12 direct uses, recursive dependencies and 21 relationship explanations were checked. The deterministic convergence theorem does not depend on Gaussian sampling, true groupings, screening, MIO constraints or proof-only stationary-point results. Source review does not certify proofs.', 'The saved inventory generator now resolves the registered local PDF and renders its own main-text evidence and appendix-heading crop. A separate rebuild regenerated all six census JSON artifacts byte for byte after the quotation correction. Rebuild validation does not replace manual source review.']
    pages = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 19]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=20, path='evidence/revalidation/page-20-heading.png', sha256=digest(ROOT / 'evidence/revalidation/page-20-heading.png'), location='Appendix heading only; body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 3 Theorems, 14 source entries, 21 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
