"""Record the completed manual source review and run independent artifact checks.

The assertions verify provenance and consistency, not mathematical fidelity by
themselves. The findings below record the PDF inspection performed before this run.
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
HISTORY = ROOT / 'review-history/before-registered-source-review'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def main():
    source = Path(subprocess.check_output(
        [sys.executable, str(REPO / 'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    register = load(REPO / 'corpus/aos/2024/local-pdf-manifest.json')
    entry = next(p for p in register['papers'] if p['paper_id'] == PID)
    audit = load(ROOT / 'paper-audit.json')
    inventory = load(ROOT / 'theorem-inventory.json')
    census = load(ROOT / 'ranked-interfaces.json')
    assert digest(source) == entry['sha256'] == audit['source']['pdf_sha256']
    pdf = fitz.open(source)
    assert len(pdf) == entry['pdf_pages'] == 28
    assert '10.1214/23-AOS2342' in pdf[0].get_text()
    headings = []
    for n, page in enumerate(pdf, 1):
        text = page.get_text()
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == text
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                match = re.match(r'^THEOREM\s+(\d+)\.', ''.join(s['text'] for s in line['spans']))
                if match:
                    headings.append((n, match[1]))
    assert headings == [(12, '1'), (13, '2'), (19, '3'), (20, '4')]
    assert [c['claim_id'] for c in inventory['claims']] == [PID + '/T' + n for _, n in headings]
    assert inventory['papers'][0]['main_text_last_pdf_page'] == 25
    assert inventory['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert all(s in pdf[24].get_text() for s in ['Acknowledgments.', 'SUPPLEMENTARY MATERIAL', 'REFERENCES'])
    assert digest(ROOT / 'theorem-inventory.json') == digest(HISTORY / 'theorem-inventory.json')

    # Confirm the only change in the extraction artifacts is the reviewed D3 omission.
    before = 'The Q-function (or action-state function) of policy can be defined analogously as follows:'
    after = r'The Q-function (or action-state function) of policy $\pi$ can be defined analogously as follows:'

    def correct(value):
        if isinstance(value, str):
            return value.replace(before, after)
        if isinstance(value, list):
            return [correct(v) for v in value]
        if isinstance(value, dict):
            return {k: correct(v) for k, v in value.items()}
        return value

    for name in ['source-passages.json', 'interface-draft.json', 'unfinalized-census.json', 'ranked-interfaces.json']:
        assert load(ROOT / name) == correct(load(HISTORY / name)), name
    corrections = load(ROOT / 'source-transcription-corrections.json')
    for previous in corrections['previous_artifacts']:
        assert digest(HISTORY / previous['path']) == previous['sha256']

    direct = {
        'T1': {'D3', 'D5', 'D12', 'D11', 'D8', 'D7'},
        'T2': {'D1', 'D3', 'D5', 'D6', 'D8'},
        'T3': {'D15', 'D17', 'D24', 'D22', 'D20', 'D19'},
        'T4': {'D13', 'D15', 'D17', 'D18', 'D20'},
    }
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 24
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 38
    assert after in members['D3']['statement_original']
    for it in census['interfaces']:
        for member in it['members']:
            lid = member['local_id']
            allowed = {'T1', 'T2'} if int(lid[1:]) <= 12 else {'T3', 'T4'}
            assert all(cid.split('/')[-1] in allowed for cid in it['theorem_explanations'])
            selectors = member.get('highlight_symbols', []) + member.get('highlight_phrases', [])
            original = member['statement_original'] + '\n' + member['local_label']
            related = [c['statement_original'] for c in census['claims'] if c['claim_id'] in it['theorem_explanations']]
            assert any(s in original for s in selectors), lid
            assert all(any(s in t for t in [original] + related) for s in selectors), lid

    validator = Path('skills/statistical-paper-census/scripts/validate_census.py')
    results = []
    for name in ['theorem-inventory.json', 'ranked-interfaces.json']:
        result = subprocess.run([sys.executable, '-B', str(validator), str(ROOT / name)],
                                text=True, capture_output=True, check=True)
        results.append(dict(artifact=name, returncode=result.returncode, stdout=result.stdout))
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    for item in audit['artifacts'].values():
        item['sha256'] = digest(ROOT / item['path'])
    note = ('Registered-source revalidation restored one omitted policy symbol pi in D3, '
            'on PDF page 7 (published page 239). The theorem inventory and mathematical '
            'dependency graph are unchanged. Previous artifacts and extraction scripts '
            'are archived under review-history/before-registered-source-review; the '
            'correction is recorded in source-transcription-corrections.json.')
    if note not in audit['source_notes']:
        audit['source_notes'].append(note)
    audit['transcription_revalidated_at'] = now
    (ROOT / 'paper-audit.json').write_text(json.dumps(audit, indent=2, ensure_ascii=False) + '\n')

    findings = [
        'The registered local PDF is the same 28-page published article inspected by the earlier audit: title, five authors, volume 52(1), pages 233-260 and DOI 10.1214/23-AOS2342 agree. Its hash is unchanged; no arXiv or supplement version is substituted.',
        'Fresh PDF text matches all 28 cached revalidation pages byte for byte. Independent line-heading enumeration finds exactly Theorems 1-4 on PDF pages 12, 13, 19 and 20. Their full statements were visually checked. Main discussion ends on page 25 before acknowledgments, a separate-supplement notice and references; no appendix body was consulted.',
        'Theorem 1 retains gamma in [1/2,1), positive delta below one, epsilon in (0,1/(1-gamma)], its explicit iteration threshold, success probability at least 1-2 delta, the cubic effective-horizon sample bound, and the ordinary-concentrability alternative. Theorem 2 retains gamma in [2/3,1), S>=2, clipped coefficient >=8 gamma/S, its stated epsilon upper bound and strict error >epsilon with probability >=1/8.',
        'Theorem 3 uses K trajectories, a cubic H bound and success probability exceeding 1-12 delta. Theorem 4 instead bounds N=KH with H^4, uses error >=epsilon and probability >=1/4, and prints H>=12 with no separately stated S>=2. Original quantifiers and constant conditions were preserved rather than completed by inference.',
        'All 24 source bodies were compared with the PDF: discounted models, policies, values and occupancies on pages 7-8; independent transitions and Definitions 1-2 on pages 8-9; empirical model, Bellman operator and Bernstein penalty on page 10; and all ten lines of Algorithm 1 on page 11. D3 had omitted pi after the words of policy before equation (11); this single transcription error was corrected and propagated through the saved generator.',
        'Finite-horizon counterparts on pages 14-17 preserve time-indexed transition and reward kernels, undiscounted value sums, stepwise occupancy, and iid behavior-policy trajectories whose starting distribution may differ from the test distribution. Definitions 3-4 remain separate from Definitions 1-2 despite reusing coefficient notation.',
        'Both clipped coefficients use min(d-star,1/S) in the numerator, not clipping of the ratio. The source fixes one deterministic optimal policy rather than maximizing concentrability across all policies. Ordinary coefficients are alternatives only in their respective upper-bound theorems.',
        'The two Bernstein formulas were visually checked: discounted penalty (28) has an inner maximum, cap 1/(1-gamma) and additive 5/N; episodic penalty (55) adds square-root and linear terms before capping at H. The global variance definition and 0/0=0 convention on pages 6-7 are preserved in the unranked auxiliary passage.',
        'Algorithm 2 preserves all ten lines, terminal value zero and backward recursion. Algorithm 3 preserves its three lines and all three subsampling substeps, the first/remaining K/2 split, equation (56), random transition subsampling and final call to Algorithm 2. Generic input D0 and its N transitions are not silently identified with pre-trimming KH.',
        'Existing source-convention notes were checked: missing h subscripts in (41b)/(43), unspecified odd-K and trimming-count rounding, random-split prose versus ordered halves in Algorithm 3, delta absent from that algorithm input list, and unspecified positive-over-zero convention. These ambiguities are reported separately without editing quotations.',
        'All 24 natural-language names and their source naming contexts, all highlight selectors, 22 direct theorem uses, recursive local dependencies and 38 source-backed explanations were reviewed. Discounted and finite-horizon dependency paths stay separate. Neither lower-bound theorem is assigned an upper-bound algorithm or penalty dependency. Mathematical proof correctness is outside this source review.'
    ]
    pages = [1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 25]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png',
                     sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    review = dict(
        schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
        method='source_content_revalidation', reviewed_at=now,
        registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
        source_version=audit['source']['version'],
        checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
        reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
        findings=findings, evidence=evidence, independent_validation=results)
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Source review complete: 4 Theorems, 24 source entries, 38 connections; one omitted pi restored.')


if __name__ == '__main__':
    main()
