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
    assert len(pdf) == entry['pdf_pages'] == 26
    assert 'arXiv:2305.00164v2' in pdf[0].get_text()
    assert all(s in pdf[0].get_text() for s in ['Cai', 'Chen', 'Zhu'])
    headings = []
    for n, page in enumerate(pdf, 1):
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                match = re.match(r'^Theorem\s+(\d+\.\d+)(?:\.| \()', ''.join(s['text'] for s in line['spans']))
                if match:
                    headings.append((n, match[1]))
    assert headings == [(6, '2.1'), (9, '2.2'), (10, '2.3'), (16, '3.1'), (16, '3.2'), (16, '3.3'), (16, '3.4'), (23, '4.1'), (23, '4.2'), (23, '4.3'), (23, '4.4')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 26
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert all(s in pdf[24].get_text() for s in ['Acknowledgments.', 'SUPPLEMENTARY MATERIAL', 'References.'])
    direct = {
        'T2.1': {'D3','D4','D6','D7','D8'}, 'T2.2': {'D1','D3','D4','D6','D7'}, 'T2.3': {'D1','D3','D4'},
        'T3.1': {'D1','D14','D10','D3'}, 'T3.2': {'D1','D15','D5','D10','D6'},
        'T3.3': {'D1','D17','D9','D4'}, 'T3.4': {'D1','D19','D5','D9','D7'},
        'T4.1': {'D1','D30','D22'}, 'T4.2': {'D1','D32','D21','D24'},
        'T4.3': {'D1','D33','D23'}, 'T4.4': {'D1','D36','D21','D25'}
    }
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 37
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 100
    assert sum(len(c['depends_on']) for c in census['claims']) == 45
    by_local = {it['members'][0]['local_id']: it for it in census['interfaces']}
    def reach(lid):
        return {r['claim_id'].split('/')[-1] for r in by_local[lid]['related_theorems']}
    assert reach('D8') == {'T2.1'}
    assert reach('D31') == {'T4.2'} and reach('D35') == {'T4.4'}
    assert all(t.startswith('T3.') for lid in range(11,18) for t in reach('D'+str(lid)))
    assert all(t.startswith('T4.') for lid in range(20,37) for t in reach('D'+str(lid)))
    assert members['D18']['depends_on'] == members['D37']['depends_on'] == []
    def check_strings(value):
        if isinstance(value, dict):
            for v in value.values(): check_strings(v)
        elif isinstance(value, list):
            for v in value: check_strings(v)
        elif isinstance(value, str):
            assert not any(ord(c)<32 and c not in '\n\t' for c in value), repr(value)
    check_strings(census)
    corrections = json.loads((ROOT / 'source-transcription-corrections.json').read_text())
    for correction in corrections['corrections']:
        assert members[correction['local_id']]['naming_context'][0]['text'] == correction['after']
    assert len(corrections['corrections']) == 4
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
    findings = json.loads((ROOT / 'evidence/revalidation/manual-findings.json').read_text())
    pages = [1,2,3,6,7,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,25,26]
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
    print('Registered source reviewed: 11 Theorems, 37 source entries, 100 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
