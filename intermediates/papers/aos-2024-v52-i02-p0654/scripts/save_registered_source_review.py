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
    assert len(pdf) == entry['pdf_pages'] == 25
    assert 'arXiv:2401.12331v2' in pdf[0].get_text()
    assert all(s in pdf[0].get_text() for s in ['T. TONY CAI', 'DONGWOO KIM', 'HONGMING PU', '27 Mar 2024'])
    headings = []
    for n in range(1, 26):
        page = pdf[n - 1]
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                joined = ''.join(span['text'] for span in line['spans']).strip()
                match = re.fullmatch(r'THEOREM (\d+\.\d+) \((.+)\)\.', joined)
                if match:
                    headings.append((n, match[1]))
    assert headings == [(6,'2.1'),(8,'2.2'),(9,'2.3'),(12,'2.4'),(12,'3.1'),(13,'3.2'),(14,'3.3'),(17,'3.4')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 25
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert 'SUPPLEMENTARY MATERIAL' in pdf[22].get_text()
    assert 'Department of Statistics and Data Science' in pdf[24].get_text()
    direct = {
        'T2.1': {'D1','D8','D17'},
        'T2.2': {'D1','D7','D8','D3','D11','D12'},
        'T2.3': {'D1','D2','D7','D8'},
        'T2.4': {'D1','D7','D8','D3','D14'},
        'T3.1': {'D1','D9','D17'},
        'T3.2': {'D1','D7','D9','D3','D11','D12'},
        'T3.3': {'D1','D2','D7','D9'},
        'T3.4': {'D1','D7','D9','D3','D16'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    expected_pages = {'T2.1':[6], 'T2.2':[8,9], 'T2.3':[9], 'T2.4':[12],
                      'T3.1':[12,13], 'T3.2':[13,14], 'T3.3':[14], 'T3.4':[17]}
    for claim in inv['claims']:
        assert [e['page'] for e in claim['evidence']] == expected_pages[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 14
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 68
    assert sum(len(c['depends_on']) for c in census['claims']) == 36
    by_local = {it['members'][0]['local_id']: it for it in census['interfaces']}
    def reach(lid):
        return {r['claim_id'].split('/')[-1] for r in by_local[lid]['related_theorems']}
    all_theorems = set(direct)
    for lid in ['D1','D3','D4','D6']:
        assert reach(lid) == all_theorems
    assert reach('D2') == reach('D7') == all_theorems - {'T2.1','T3.1'}
    assert reach('D8') == {'T2.1','T2.2','T2.3','T2.4'}
    assert reach('D9') == {'T3.1','T3.2','T3.3','T3.4'}
    assert reach('D10') == reach('D11') == reach('D12') == {'T2.2','T2.4','T3.2','T3.4'}
    assert reach('D17') == {'T2.1','T3.1'}
    assert reach('D14') == {'T2.4'}
    assert reach('D16') == {'T3.4'}
    assert members['D17']['depends_on'] == ['D1','D4','D6']
    assert members['D7']['depends_on'] == ['D1','D2','D4','D6']
    assert members['D10']['depends_on'] == []
    assert members['D4']['source_kind'] == members['D8']['source_kind'] == members['D9']['source_kind'] == 'condition'
    assert members['D6']['source_kind'] == 'assumption'
    assert members['D7']['source_kind'] == members['D17']['source_kind'] == 'source_passage'
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
    pages = list(range(1,18)) + [23,25]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=7, path='evidence/revalidation/algorithm-1-fit-crop.png', sha256=digest(ROOT / 'evidence/revalidation/algorithm-1-fit-crop.png'), scope='Magnified check of the polynomial fit and intervalwise thresholding notation.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 8 Theorems, 14 source entries, 68 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
