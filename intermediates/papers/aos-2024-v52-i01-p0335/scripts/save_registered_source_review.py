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
    assert len(pdf) == entry['pdf_pages'] == 94
    assert '2109.03204v4' in pdf[0].get_text()
    assert 'ILSANG OHN' in pdf[0].get_text() and 'LIZHEN LIN' in pdf[0].get_text()
    headings = []
    for n, page in enumerate(list(pdf)[:29], 1):
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                match = re.match(r'^THEOREM\s+(\d+\.\d+)(?:\.| \()', ''.join(s['text'] for s in line['spans']))
                if match:
                    headings.append((n, match[1]))
    assert headings == [(8, '2.1'), (12, '3.1'), (13, '3.3'), (13, '3.4'), (14, '3.5'), (15, '3.6'), (17, '4.1'), (20, '5.1'), (21, '5.2'), (22, '5.3'), (23, '6.1'), (23, '6.2'), (26, '7.1'), (26, '7.2')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 29
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert all(s in pdf[26].get_text() for s in ['Acknowledgments.', 'SUPPLEMENTARY MATERIAL', 'REFERENCES'])
    direct = {'T2.1': ['D3', 'D7', 'D4', 'D6', 'D8', 'D9'], 'T3.1': ['D9', 'D10', 'D11'], 'T3.3': ['D1', 'D7', 'D5', 'D6', 'D4', 'D11', 'D15', 'D16', 'D12'], 'T3.4': ['D7', 'D10', 'D11', 'D13', 'D14', 'D15', 'D12'], 'T3.5': ['D7', 'D11', 'D13', 'D14', 'D15', 'D17', 'D12'], 'T3.6': ['D7', 'D10', 'D11', 'D13', 'D14', 'D15', 'D18', 'D12'], 'T4.1': ['D7', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31'], 'T5.1': ['D7', 'D20', 'D22', 'D23', 'D25', 'D24'], 'T5.2': ['D7', 'D32', 'D35', 'D36', 'D37', 'D38', 'D40'], 'T5.3': ['D7', 'D32', 'D35', 'D36', 'D33', 'D39', 'D40'], 'T6.1': ['D7', 'D11', 'D13', 'D15', 'D42'], 'T6.2': ['D7', 'D10', 'D11', 'D13', 'D15', 'D12', 'D43'], 'T7.1': ['D45', 'D44', 'D1', 'D4', 'D6', 'D46', 'D47', 'D48', 'D49', 'D12'], 'T7.2': ['D45', 'D46', 'D47', 'D48', 'D12']}
    for claim in census['claims']:
        assert set(claim['depends_on']) == set(direct[claim['claim_id'].split('/')[-1]])
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 49
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 178
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
    findings = ['The registered 94-page PDF is arXiv:2109.03204v4, stamped 11 March 2024, by Ilsang Ohn and Lizhen Lin. The title, authors, version and SHA-256 match the existing audit. The source remains this specific preprint; no identity with the journal version is assumed.', 'Independent main-document heading enumeration finds exactly 14 Theorems in source order. Complete statements were compared with registered-PDF page renders, including the final sentence of Theorem 5.2 on page 22. Main results end on page 26; acknowledgments, funding and a separate-supplement notice precede references on page 27, and references end on page 29. Only the supplement title/introduction heading crop on page 30 was inspected to confirm the boundary; no appendix body was read.', 'Theorem 2.1 retains the disjoint parameter-space assumption, adaptive mixture, individual argmins, normalized exponential weights and the full normalizing constant. Theorem 3.1 retains both suprema and its individual-model eta-plus-zeta contraction threshold. Sampling expectation of posterior mass is not replaced by an almost-sure convergence statement.', 'Theorems 3.3 and 7.1 preserve their initial bounds and separate additional assumptions for the final rate consequences. Assumption A2 and B3 apply only to the last consequence in Theorem 3.3. Theorem 7.1 initially assumes E1, then adds E2 and E3. Its c_2/rho coefficient and Lambda_n quantifier without a star are preserved.', 'Theorems 3.4, 3.5 and 3.6 retain their distinct hypothesis lists. Theorem 3.5 explicitly requires n epsilon_n squared to diverge and assumes A2 plus B; A1 is not added. Underlined diverging sequences, H1 positivity and the approximation threshold in the less-expressive model set remain intact.', 'Theorem 4.1 retains the architecture cardinality and depth/width growth restrictions, 1<=B_n with a polynomial upper bound, and the sup_f followed by inf_theta inside the oracle expression. Its loss uses the empirical design-point distance, while approximation uses the supremum norm. Neither Holder smoothness nor the subsequent Corollary 4.2 conditions are imported.', 'Theorem 5.1 retains the pair-index oracle rate and all three assertions. The first two use full Assumption D, whereas its final overestimation assertion assumes only D2 and D3. Their common parent scope and the distinct cell-count, prior-tail and near-oracle weight clauses are preserved in the source passages.', 'Theorem 5.2 retains its explicit rate, dimension growth, sparsity and model-index restrictions. Theorem 5.3 imports those assumptions, adds the signal-restricted covariance class and a diverging signal lower bound, and concludes recovery within multiplicative H1/H2 constants strictly greater than one. It does not assert exact model selection.', 'The ivB results retain their specific assumptions: Theorem 6.1 uses A2, B1 and B3; Theorem 6.2 uses A, B1 and B3. Neither adds B2 or ideal-penalty assumptions. The ivB penalty is a sup-inf difference of KL terms; the large-penalty model set and maximal complexity of its complement are distinct source constructions.', 'All 49 source entries and eight auxiliary passages were checked. The general setup distinguishes the dominated sampling experiment, countable model indices, disjoint parameter spaces and their potentially overlapping natural images. The hierarchical prior, hierarchical variational family, Bayesian posterior and KL projection remain separate definitions. The local negative-ELBO optimizer is preserved where used, without turning the theorem proving its representation into an extra premise.', 'The neural-network passages preserve the composition of affine maps and ReLUs, full parameter dimensions, bounded parameter spaces, architecture prior weights and product-uniform variational family. The Gaussian regression law uses independent unit-variance errors at fixed design points. The factor model uses independent Gaussian observations with covariance L L-transpose plus identity, exact row-support cells, rowwise spike-and-slab priors and variational families, and separate basic and signal-restricted truth classes.', 'Assumptions A, B, D and E retain their original parent constant and quantifier scopes with each subclause. The approximation budgets differ: A2 and D2 use sampling-law KL divergence; E2 uses n times squared metric distance. Reusing the oracle rate formula in E does not import A2. Quasi-likelihood expectations remain under the actual sampling law.', 'The source inconsistencies already documented in ambient-conventions.json were confirmed: potentially unordered uniform interval endpoints in (4.4), Pi_n,m versus Pi_n in (7.2), and the Lambda_n-star versus Lambda_n scope mismatch in Assumption E and Theorem 7.1. Countable-simplex conventions, zero/infinite normalizers, zero-mass conditioning, argmin selections, infinite KL differences and empty-sieve maxima remain unresolved. No mathematical repair was inserted into a source quotation.', 'All 49 source-backed titles, naming contexts and highlight selectors, all 94 direct uses, recursive edges and 178 theorem explanations were reviewed. Different assumptions sharing a name remain separate entries. The graph preserves theorem-local application inputs, avoids proof-only dependencies and keeps the original statements unchanged. This review does not certify the proofs.', 'The prior scripts were archived before adding an isolated rebuild entry point. The inventory writer now resolves and verifies the registered local PDF instead of depending on the old provenance cache, and imports do not overwrite artifacts. All six census JSON artifacts regenerated byte for byte in a separate directory and passed structural validation. Existing source content and audit artifacts remain unchanged.']
    pages = [1, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=30, path='evidence/revalidation/page-30-heading.png', sha256=digest(ROOT / 'evidence/revalidation/page-30-heading.png')))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 14 Theorems, 49 source entries, 178 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
