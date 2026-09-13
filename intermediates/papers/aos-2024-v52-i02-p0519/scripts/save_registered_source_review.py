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
    assert len(pdf) == entry['pdf_pages'] == 34
    assert 'arXiv:2210.13008v3' in pdf[0].get_text()
    assert all(s in pdf[0].get_text() for s in ['RICHARD NICKL'])
    headings = []
    for n in range(1, 35):
        page = pdf[n - 1]
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                match = re.fullmatch(r'THEOREM\s+(\d+)\.', ''.join(s['text'] for s in line['spans']))
                if match:
                    headings.append((n, match[1]))
    assert headings == [(3,'1'),(4,'2'),(6,'3'),(6,'4'),(7,'5'),(7,'6'),(8,'7'),(9,'8'),(12,'9'),(12,'10'),(17,'11'),(25,'12')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 34
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert [1, 'Proofs', 13] in pdf.get_toc()
    assert pdf.get_toc()[-1] == [1, 'References', 32]
    assert '[77]' in pdf[33].get_text()
    direct = {
        'T1': {'D4'},
        'T2': {'D1','D2','D4','D8','D9','D10'},
        'T3': {'D1','D2','D4','D11'},
        'T4': {'D1','D2','D4'},
        'T5': {'D2','D4'},
        'T6': {'D2','D4','D16'},
        'T7': {'D2','D4','D16'},
        'T8': {'D13','D3','D5','D16'},
        'T9': {'D1','D2','D4','D8','D10'},
        'T10': {'D1','D2','D4','D8','D10','D16'},
        'T11': {'D2','D4','D6','D14'},
        'T12': {'D1','D7','D8','D15'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 16
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 85
    assert sum(len(c['depends_on']) for c in census['claims']) == 45
    by_local = {it['members'][0]['local_id']: it for it in census['interfaces']}
    def reach(lid):
        return {r['claim_id'].split('/')[-1] for r in by_local[lid]['related_theorems']}
    all_theorems = {'T'+str(i) for i in range(1,13)}
    assert reach('D2') == reach('D3') == all_theorems
    assert reach('D1') == reach('D4') == all_theorems - {'T8'}
    assert reach('D5') == {'T2','T3','T6','T7','T8','T9','T10'}
    assert reach('D6') == {'T2','T9','T10','T11'}
    assert reach('D7') == {'T2','T9','T10','T11','T12'}
    assert reach('D8') == {'T2','T9','T10','T12'}
    assert reach('D9') == reach('D10') == {'T2','T9','T10'}
    assert reach('D11') == {'T3'}
    assert reach('D12') == reach('D16') == {'T6','T7','T8','T10'}
    assert reach('D13') == {'T8'}
    assert reach('D14') == {'T11','T12'}
    assert reach('D15') == {'T12'}
    assert members['D16']['source_kind'] == 'theorem_excerpt'
    assert members['D7']['depends_on'] == ['D1','D4']
    def check_strings(value):
        if isinstance(value, dict):
            for v in value.values(): check_strings(v)
        elif isinstance(value, list):
            for v in value: check_strings(v)
        elif isinstance(value, str):
            assert not any(ord(c)<32 and c not in '\n\t' for c in value), repr(value)
    check_strings(census)
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
    pages = [1,2,3,4,5,6,7,8,9,10,12,13,14,17,21,22,25,26,27,34]
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
    print('Registered source reviewed: 12 Theorems, 16 source entries, 85 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
