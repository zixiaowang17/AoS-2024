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
    assert len(pdf) == entry['pdf_pages'] == 24
    assert '10.1214/23-AOS2346' in pdf[0].get_text()
    headings = []
    for n, page in enumerate(pdf, 1):
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                match = re.match(r'^THEOREM\s+(\d+\.\d+)(?:\.| \()', ''.join(s['text'] for s in line['spans']))
                if match:
                    headings.append((n, match[1]))
    assert headings == [(6, '2.1'), (6, '2.2'), (8, '4.1'), (15, '5.2')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 22
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert all(s in pdf[21].get_text() for s in ['Acknowledgments.', 'SUPPLEMENTARY MATERIAL', 'REFERENCES'])
    direct = {'T2.1': {'D4', 'D5', 'D6'}, 'T2.2': {'D4', 'D5', 'D6'},
              'T4.1': {'D3', 'D4', 'D2', 'D10', 'D11'}, 'T5.2': {'D3', 'D4', 'D12', 'D13'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 13
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 27
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
    findings = [
        'The verified local PDF is the original 24-page published article, pages 261-284, DOI 10.1214/23-AOS2346, by Zehao Dou, Zhou Fan and Harrison H. Zhou. Title, authors, metadata and source hash agree; no source-version substitution was made.',
        'Independent heading enumeration finds exactly Theorems 2.1 and 2.2 on PDF page 6, Theorem 4.1 on page 8, and Theorem 5.2 on page 15. Each complete statement was visually compared with fresh registered-PDF renders. Section 6 ends on page 22 before acknowledgments, funding, a separate-supplement notice and references. No supplementary appendix body was read.',
        'The two minimax statements retain beta in [0,1/2), their distinct high/low noise thresholds, sample thresholds, constant-dependence clauses and rates. Their following common paragraph defines the expectation over model (5), infimum over all data-based estimators, and asymptotic-comparison constants, including its printed c0 reference.',
        'Theorem 4.1 retains both oracle and optimization choices, the lower bound on every Fourier magnitude, both terms in the sample-size threshold, and the full two-part bound (19). The simplified bound after the theorem is not substituted. Theorem 5.2 retains Assumption 5.1, constants depending only on c_gen and the norm-dependent sample threshold and logarithm.',
        'The Fourier model and ambient continuous model on pages 4-5 were checked: a zero-mean signal bandlimited to K>=2, normalized real sine/cosine basis, one latent uniform rotation shared by every frequency in each sample, independent real Gaussian noise, and fixed known sigma>0. The loss minimizes over one common rotation; independent frequency alignment is not allowed.',
        'All 13 extracted source passages were checked. The power-law class has both lower and upper magnitude constraints at each frequency. Assumption 5.1 instead bounds the energy of every subset of at least half the frequencies. Neither is silently substituted for the other.',
        'The complex representation on page 7 uses conjugation and complex Gaussian variance 2, with independent real and imaginary parts of variance one. The auxiliary index set (15) includes k=l and all ordered admissible pairs; no distinct-frequency or unordered-pair restriction is introduced.',
        'All three method-of-moments steps on page 8 were checked: subtract 2 sigma squared before taking positive-part square root, retain both conjugated factors in the empirical bispectrum, choose real argument versions, perform least squares over R^K, and reconstruct real coefficient pairs.',
        'The oracle on page 9 centers its half-open argument interval at the true real phase combination. The observable procedure on page 12 first minimizes maximum circular discrepancy, then forms a real lift around its pilot. The circular least-squares alternative and frequency-marching procedure in subsequent remarks are not substituted for either named estimator.',
        'The likelihood on page 14 averages over uniform rotations with the full 2K-dimensional Gaussian normalization and optimizes the empirical negative log-likelihood over all real coefficient vectors. The true-signal-aligned representative selected after Theorem 5.2 is used in its proof and is not part of the estimator definition.',
        'All four auxiliary passages and source-convention notes were checked. Undefined Arg at zero, absent minimizer selection, unspecified ordering of the class constants, and the norm denominator at the zero signal remain unresolved rather than silently repaired. Positive polar coordinates do not add a new positivity premise to the general linear observation model.',
        'All 13 natural-language titles, naming contexts, highlight selectors, 15 direct uses, recursive dependencies and 27 relationship explanations were reviewed. The minimax statements do not acquire proof-only estimator dependencies. Source statements and the original audit artifacts remain unchanged; this review does not certify proofs.',
        'The inventory script previously depended on an older external PDF cache, its manifest, and temporary rendered pages. The previous script was archived; the current version resolves the registered local PDF and renders its evidence directly. scripts/rebuild.py regenerated all six census artifacts byte for byte in a separate directory, without overwriting the existing audit. The reproduction report is stored alongside revalidation evidence.'
    ]
    pages = [1, 4, 5, 6, 7, 8, 9, 12, 14, 15, 22]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 4 Theorems, 13 source entries, 27 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
