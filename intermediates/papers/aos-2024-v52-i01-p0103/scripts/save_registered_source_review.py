"""Record the completed visual and dependency review of registered p0103.

The automated checks pin this review's sources; they do not perform semantic
review. The inventory, original census and prior audit remain unchanged.
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
    inv = json.loads((ROOT / 'theorem-inventory.json').read_text())
    census = json.loads((ROOT / 'ranked-interfaces.json').read_text())
    assert digest(source) == entry['sha256'] == audit['source']['pdf_sha256']
    pdf = fitz.open(source)
    assert len(pdf) == entry['pdf_pages'] == 67
    assert 'ANDREAS GERHARDUS' in pdf[0].get_text()
    headings = []
    for p in range(1, 26):
        page = pdf[p - 1]
        text = page.get_text(clip=fitz.Rect(0, 0, page.rect.width, 635)) if p == 25 else page.get_text()
        suffix = '25-main' if p == 25 else f'{p:02}'
        assert (ROOT / f'evidence/revalidation/page-{suffix}.txt').read_bytes().decode('utf8') == text
        headings.extend((p, m[1]) for m in re.finditer(r'^THEOREM\s+(\d+)\.', text, re.M))
    assert headings == [(16, '1'), (16, '2'), (20, '3')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 25
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is True
    assert 'SUPPLEMENTARY MATERIAL' in text
    expected_direct = {
        'T1': {'D5', 'D7', 'D10', 'D13p', 'D16'},
        'T2': {'D2', 'D7', 'D3', 'D10', 'D13p', 'D16'},
        'T3': {'D10', 'D22', 'D13p', 'D15', 'D14', 'D19', 'D6'},
    }
    for c in census['claims']:
        assert set(c['depends_on']) == expected_direct[c['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == 23 and len(census['interfaces']) == 22
    assert set(members['D16']['depends_on']) == {'D2', 'D3', 'D7', 'D14'}
    assert set(members['D10']['depends_on']) == {'D4', 'D7', 'D8', 'D9'}
    assert set(members['D22']['depends_on']) == {'D17', 'D13p', 'D15', 'D8', 'D20', 'D21'}
    for it in census['interfaces']:
        for m in it['members']:
            selectors = m.get('highlight_symbols', []) + m.get('highlight_phrases', [])
            original = m['statement_original'] + '\n' + m['local_label']
            related = [c['statement_original'] for c in census['claims'] if c['claim_id'] in it['theorem_explanations']]
            assert any(s in original for s in selectors), m['local_id']
            assert all(any(s in t for t in [original] + related) for s in selectors), m['local_id']
    for item in audit['artifacts'].values():
        assert digest(ROOT / item['path']) == item['sha256']
    results = []
    validator = Path('skills/statistical-paper-census/scripts/validate_census.py')
    for name in ['theorem-inventory.json', 'ranked-interfaces.json']:
        result = subprocess.run([sys.executable, '-B', str(validator), str(ROOT / name)],
                                text=True, capture_output=True, check=True)
        results.append({'artifact': name, 'returncode': result.returncode, 'stdout': result.stdout})
    findings = [
        'The fixed local PDF is byte-identical to the prior reviewed arXiv:2112.08417v2 (67 pages). Its title and Andreas Gerhardus authorship match. All review reads used the local resolver path.',
        'An independent heading scan over main text, including the clipped final page, yields only Theorems 1 and 2 on PDF page 16 and Theorem 3 on page 20. Ordinary references, Lemmas and Algorithms are excluded. Page 25 ends in Discussion and Acknowledgments above Supplementary Material; the fresh render stops after that heading and before its body.',
        'All three original statements were compared with fresh PDF renders. Theorems 1 and 2 print the time-index bound 0 <= t <= p instead of the tau bound used in surrounding definitions; this existing source note and literal transcription are retained. Their fixed-point equivalences and the acyclicity condition of Theorem 2 are intact.',
        'Theorem 2 begins with a directed mixed graph, without assuming ancestralness or maximality. Its DMAG dependency occurs through the ts-DMAG target/projection, rather than an extra input hypothesis. Theorem 1 does assume a DMAG input. Neither statement gains causal Markov, faithfulness, stochastic-solution or finite-lag assumptions from the motivating process.',
        'Theorem 3 retains exactly the three background-knowledge pairs, all four conclusions, and the stronger shared-adjacency qualifier in part 4. It compares endpoint marks in distinct DPAG constructions; no generic information-order summary replaces its actual statements.',
        'D1–D6 and ambient graph conventions were checked on pages 3–4: at most one edge per vertex pair, no self adjacency, four permitted edge types, directed-cycle and almost-directed-cycle conditions, inducing-path maximality, and head/tail versus circle marks. Paths have no repeated vertices; the source counts vertices as length and permits reflexive ancestry.',
        'D7–D10 were checked on pages 5–6: time-series vertices form I times an integer interval; time order constrains directed edges; repeating edges preserves each edge type under every admissible simultaneous time shift; a ts-DAG has time index set Z. The finite maximum edge lag of the motivating process is absent from Definition 3.4 and was not inserted.',
        'D11–D13 and D13p were checked on pages 7–8 and 10: regular/subsampled finite observed windows are distinct source cases; latent variables include unobservable series and unobserved time steps. Projection preserves the described ancestry and separation relationships; the complete MAG projection recipe is an external source reference and remains unresolved. M^p is the later regular-sampling abbreviation.',
        'D14–D16 were checked on pages 11–12 and 14: stationarification keeps a specific edge type only when all admissible shifts contain it, including partially directed/circle edges. A stationarified ts-DMAG need not itself be a ts-DMAG. The canonical ts-DAG uses only stationarified edges, its full infinite-time vertex set, and the two distinct latent-parent time shifts printed in Definition 4.13.',
        'D17–D19 were checked on pages 18–19: background knowledge is Boolean on DMAGs, Markov equivalence means equality of m-separations, and all four parts of the refined-DPAG definition are retained. Circle marks require the stated tail/head witnesses; the empty-subclass case is not silently completed by an invented convention.',
        'D20–D22 were checked on pages 10 and 19: repeating orientations requires matching orientations when a shifted adjacency exists; repeating ancestral relationships is a separate implication. All four cases of Definition 5.4 are retained with their distinct meanings and dependencies.',
        'Reviewed all 18 direct uses, recursive local edges, 49 related connections and source-specific explanations. Standard canonical DAGs (Definition 4.11), comparison terminology (Definition 5.3), ts-DPAGs (Definition 5.7), Algorithm 1 and proof-only Lemmas are not prerequisites needed to state these three Theorems.',
        'All 22 natural-language interface titles, source labels/naming contexts and all selectors were checked against their source passages. Every one of the 23 members has a meaningful source match. The existing inventory, census, original source passages and audit remain byte-for-byte unchanged. This review does not certify theorem proofs or resolve external separation/projection criteria.'
    ]
    pages = [3, 4, 5, 6, 7, 8, 10, 11, 12, 14, 16, 18, 19, 20]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png',
                     sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=25, path='evidence/revalidation/page-25-main.png',
                         before_main_text_end=True, location='Discussion and Acknowledgments above the supplementary heading; supplementary body excluded.',
                         sha256=digest(ROOT / 'evidence/revalidation/page-25-main.png')))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results)
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed and independently validated: 3 Theorems, 22 interfaces, 23 source members, 49 related connections; prior artifacts unchanged.')


if __name__ == '__main__':
    main()
