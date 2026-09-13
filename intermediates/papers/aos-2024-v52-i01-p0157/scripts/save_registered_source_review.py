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
    assert len(pdf) == entry['pdf_pages'] == 58
    assert all(s in pdf[0].get_text() for s in ['Ariane Marandon', 'Lihua Lei', 'David Mary', 'Etienne Roquain', '2208.06685v3'])
    headings = []
    for p in range(1, 28):
        page = pdf[p - 1]
        assert (ROOT / f'evidence/revalidation/page-{p:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans'])
                match = re.match(r'^Theorem\s+(\d+\.\d+)\.', text)
                if match and line['spans'][0]['font'] == 'CMCSC10':
                    headings.append((p, match[1]))
    assert headings == [(9, '3.3'), (10, '3.4'), (10, '3.6'), (13, '4.1'), (18, '5.1'), (20, '5.4')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 27
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    heading_text = pdf[27].get_text(clip=fitz.Rect(0, 0, pdf[27].rect.width, 164))
    assert 'SUPPLEMENTARY MATERIAL' in heading_text
    assert (ROOT / 'evidence/revalidation/page-28-heading.txt').read_bytes().decode('utf8') == heading_text
    direct = {
        'T3.3': {'D10', 'D11', 'D7', 'D12', 'D9', 'D5', 'D6'},
        'T3.4': {'D10', 'D11', 'D7', 'D3', 'D2', 'D9', 'D8'},
        'T3.6': {'D10', 'D11', 'D7', 'D3', 'D2', 'D13', 'D9', 'D8'},
        'T4.1': {'D14', 'D15', 'D17', 'D18'},
        'T5.1': {'D14', 'D15', 'D8', 'D16', 'D21', 'D22', 'D23', 'D24'},
        'T5.4': {'D14', 'D15', 'D8', 'D19', 'D20', 'D25', 'D26', 'D27', 'D3'},
    }
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 27
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 69
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
    findings = ['The fixed local PDF is byte-identical to arXiv:2208.06685v3, 58 pages, with matching title and Marandon/Lei/Mary/Roquain authorship. The arXiv stamp is 25 October 2023 and typesetting footer is 26 October 2023. No published-layout identity is assumed.', 'An independent main-text PDF scan distinguished small-cap Theorem headings from ordinary references. It finds exactly Theorems 3.3, 3.4, 3.6, 4.1, 5.1 and 5.4. All full statements were visually compared on pages 9, 10-11, 13, 18 and 20. The final AdaDetect specializations, both parts of 5.1 and final oracle-BH assertion of 5.4 are intact.', 'Conclusion and acknowledgements end on page 25, followed by references through page 27. Fresh page-28 evidence contains only the supplementary title/header. The previous isolated Appendix A heading was also inspected; no appendix body was used in this revalidation.', 'Pages 5-9 establish the original null/test indices, split sizes, raw-data and score exchangeability, and no-ties assumption. These remain distinct. The generic p-value construction does not acquire fitted-score dependencies: Theorem 3.3 adds fitting only for its final AdaDetect specialization, without requiring the subsequent BH rejection step.', 'All four AdaDetect steps and BH equation (4) were checked on pages 6-7. Score invariance permutes the mixed sample, not the held-out training argument. Equation (10) retains strict greater-than comparisons and the added one. Equation (9) retains the raw-score index convention. Measurability and rejection-set conventions are preserved separately.', 'PRDS on page 9 retains conditioning on equality p_i=u and the increasing-set footnote. A conditional version at unattained discrete values remains unresolved. Assumption 1 retains its conditional-distribution existence footnote. PRDS is a conclusion of 3.3 and is not a premise imported into 3.4 or 3.6.', 'Equation (11) retains the floor, random K_i in {1,...,m}, and expectation. Equation (13) retains zero alternative coordinates, the selected null at 1/(ell+1), conditionally iid remaining nulls given one common uniform vector, and descending order statistics. The indicator-guarded cdf subscript issue remains recorded. Theorem 3.6 imports the score setting of 3.4 rather than its FDR identity.', 'Assumptions 4 and 5 on page 12 remain mutual independence and positive densities. Average densities in (15)-(17) average potentially different alternative marginals; they do not assert iid mixture sampling. The r range and m1 denominator degeneracies remain recorded instead of inserting unprinted assumptions.', 'Theorem 4.1 retains the exact-level threshold existence qualification and the printed higher TPR comparison. TPR is not silently replaced by the separately archived TDR/TDP. Section 4.2 prints calibration indices in the mFDR numerator; the source quotation and unresolved index note remain intact.', 'Definition 4.2 retains oracle AdaDetect with ratio r. Equation (19) retains increasing continuous Psi while its prose says strictly monotone. No strictness, direction or optimizer selection convention is supplied to repair the source.', 'All risks and empirical/population minimizers (25)-(27) were checked against page 18. Null loss uses g>=0, alternative and mixed loss use g<0. Theorem 5.1 retains constants depending only on delta, gamma inverse in Delta, all three conditions (29), and both conclusions (30)-(31). It imports the independent-density setting of 4.1, not its optimality conclusion. Section 5 Euclidean observations and the measurable score class were checked on pages 17 and 14.', 'The tail and discrepancy passages (33)-(35) were checked on pages 19-20, including the inverse-tail shift by 2*eta, full maximum interval, and mixed-sample maximum. Theorem 5.4 retains the complement on the inclusion event, the 3/28 exponential constant, alpha-prime enlargement and oracle-p-value BH alternative. Inverse/maximum attainment and level conventions remain unresolved as recorded.', 'All 27 source members, natural-language titles and exact naming contexts, 43 direct uses, recursive edges, 69 related explanations and every highlight selector were reviewed. No proof-only lemmas, particular density/neural estimators, Storey/quantile specializations or cross-validation constructions are counted as statement prerequisites. Existing census, inventory and audit artifacts remain byte-for-byte unchanged; this review does not certify proofs.']
    pages = [1, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 17, 18, 19, 20, 25, 27]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=28, path='evidence/revalidation/page-28-heading.png', sha256=digest(ROOT / 'evidence/revalidation/page-28-heading.png'), location='Supplementary title/header only; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results)
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed and independently validated: 6 Theorems, 27 interfaces, 27 source members, 69 related connections; prior artifacts unchanged.')


if __name__ == '__main__':
    main()
