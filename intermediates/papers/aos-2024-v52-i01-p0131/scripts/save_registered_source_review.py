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
    assert len(pdf) == entry['pdf_pages'] == 149
    assert all(s in pdf[0].get_text() for s in ['Rishabh Dudeja', 'Daniel Hsu', '2204.07526v2'])
    headings = []
    for p in range(1, 46):
        page = pdf[p - 1]
        clip = fitz.Rect(0, 0, page.rect.width, 683) if p == 45 else page.rect
        text = page.get_text(clip=clip)
        suffix = '45-main' if p == 45 else f'{p:02}'
        assert (ROOT / f'evidence/revalidation/page-{suffix}.txt').read_bytes().decode('utf8') == text
        for block in page.get_text('dict', clip=clip)['blocks']:
            for line in block.get('lines', []):
                for span in line['spans']:
                    match = re.match(r'^Theorem (\d+)\.', span['text'])
                    if match and span['font'] == 'CMBX10':
                        headings.append((p, match[1]))
    assert headings == [(19, '1'), (26, '2'), (35, '3'), (40, '4')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 45
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is True
    assert 'Proofs of the Information Bound and Geometric Inequalities' in text
    direct = {'T1': {'D1', 'D2'}, 'T2': {'D1', 'D3'},
              'T3': {'D1', 'D5', 'D9', 'D10', 'D11'}, 'T4': {'D1', 'D12', 'D13', 'D14'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 14
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 17
    for it in census['interfaces']:
        for m in it['members']:
            selectors = m.get('highlight_symbols', []) + m.get('highlight_phrases', [])
            original = m['statement_original'] + '\n' + m['local_label']
            related = [c['statement_original'] for c in census['claims'] if c['claim_id'] in it['theorem_explanations']]
            assert any(s in original for s in selectors), m['local_id']
            assert all(any(s in t for t in [original] + related) for s in selectors), m['local_id']
    for item in audit['artifacts'].values():
        assert digest(ROOT / item['path']) == item['sha256']
    validator = Path('skills/statistical-paper-census/scripts/validate_census.py')
    results = []
    for name in ['theorem-inventory.json', 'ranked-interfaces.json']:
        result = subprocess.run([sys.executable, '-B', str(validator), str(ROOT / name)], text=True, capture_output=True, check=True)
        results.append(dict(artifact=name, returncode=result.returncode, stdout=result.stdout))
    findings = [
        'The registered local source matches the original arXiv:2204.07526v2 PDF, its 149 pages, title and Dudeja/Hsu authorship. The title date is 23 January 2024 and arXiv stamp is 20 January 2024; no published-layout equivalence is assumed.',
        'Independent PDF heading enumeration finds exactly four bold Theorem environments on pages 19, 26, 35 and 40. The plain-font Theorem 2 reference on page 28 is excluded. Main text ends after Remark 7 on page 45; the boundary render includes the Appendix A heading but no appendix body.',
        'All four original statements were visually compared with fresh registered-PDF renders, including the continuation of Theorem 1 on page 20 and the final promises of Theorem 4. Theorem 2 uses memory exponent b and eta>0; the others use mu and eta>=1. Vector and tensor overlap thresholds remain distinct.',
        'Theorem 3 scales lambda as d^(-gamma), with gamma>2*ceil((k+1)/2)+kappa. Theorem 4 instead scales lambda squared as d^(-gamma), with gamma>3k/2. Their assumptions and resource inequalities have not been homogenized.',
        'Definition 1 on page 12 retains all N samples, T sequential passes, an initially zero s-bit state, and arbitrary deterministic update/output functions. Pass count is the stated computational resource; no cost of update functions or randomized extension has been inserted.',
        'The symmetric and asymmetric Tensor PCA models on pages 19 and 25 preserve their distinct vector/tensor parameter spaces, normalizations and independent Gaussian entries. Equation (6) prints X_{1:m} while describing N observations; the existing source note remains.',
        'NGCA passages on pages 29-30 preserve the independent scalar/vector sampling model and the first k-1 matching moments with kth-moment difference lambda. Assumption 4 repeats this model condition; Assumption 5 is not a prerequisite of Theorem 3.',
        'The Hermite family on page 12 and coefficients on page 30 remain separate from the three explicitly invoked Assumptions. Gaussian absolute continuity, all parameter conditions and the local guard in Assumption 3 were checked. The unspecified pointwise density version and appendix-only Hermite construction remain unresolved.',
        'CCA pages 38-39 preserve the general k-view cross-moment model separately from the hard likelihood family and coordinate-tensor restriction. Both promises (30) and (31) belong to Theorem 4. No distinct-coordinate requirement is inferred from the printed set notation.',
        'Equation (30b) visibly prints (2/pi)^(k/2)=(E|Z|)^(k/2), an inconsistent identity for a standard Gaussian. The existing original quotation and source note correctly retain both expressions rather than silently repairing the paper.',
        'Ambient conventions on pages 11-12 were compared: tensor norms/inner products use stacked entries, much-less-than means polynomial separation, sign(0)=0, and sampling is iid from the paper-local model. The zero-estimator overlap and real-t quantifier with 1/t^2 remain explicit unresolved source conventions.',
        'All 14 natural-language titles and their exact naming contexts, 14 source members, 13 direct uses, recursive dependencies, 17 related explanations and every highlight selector were checked. Proof-only communication protocols, Hellinger information and upper-bound estimators are not imported as theorem prerequisites. Original audit and census artifacts remain unchanged; proof correctness is outside this review.'
    ]
    pages = [1, 11, 12, 19, 20, 25, 26, 29, 30, 35, 38, 39, 40]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=45, path='evidence/revalidation/page-45-main.png', sha256=digest(ROOT / 'evidence/revalidation/page-45-main.png'), location='Remark 7 and Appendix A heading; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results)
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed and independently validated: 4 Theorems, 14 interfaces, 14 source members, 17 related connections; prior artifacts unchanged.')


if __name__ == '__main__':
    main()
