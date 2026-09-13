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
    assert len(pdf) == entry['pdf_pages'] == 50
    assert 'arXiv:2111.02826v4' in pdf[0].get_text()
    assert all(s in pdf[0].get_text() for s in ['Nilanjana Laha', 'Aaron Sonabend-W', 'Mukherjee', 'Tianxi Cai', '1 Oct 2023'])
    headings = []
    for n in range(1, 51):
        page = pdf[n - 1]
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                spans = line['spans']
                joined = ''.join(span['text'] for span in spans).strip()
                if spans and spans[0]['font'] == 'CMBX10' and joined.startswith('Theorem '):
                    match = re.match(r'Theorem (\d+)(?:\.| \()', joined)
                    assert match, (n, joined)
                    headings.append((n, match[1]))
    assert headings == [(12,'1'),(15,'2'),(18,'3'),(23,'4'),(26,'5'),(26,'6'),(27,'7')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 50
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert 'Due to the size of the Supplement' in pdf[42].get_text()
    assert 'References' in pdf[42].get_text() and 'Fig 5:' in pdf[49].get_text()
    base = {'D3','D4','D5','D7'}
    direct = {
        'T1': {'D16','D17','D18'},
        'T2': base | {'D8','D12','D20','D29'},
        'T3': base | {'D13','D19'},
        'T4': base | {'D13','D14','D24','D25','D27','D28'},
        'T5': base | {'D13','D14','D19','D22','D23','D24','D25','D31'},
        'T6': base | {'D13','D19','D22','D23','D24','D26','D30'},
        'T7': base | {'D13','D19','D22','D23','D24','D26','D30'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    expected_pages = {'T1':[12], 'T2':[15], 'T3':[18], 'T4':[23,24], 'T5':[26], 'T6':[26], 'T7':[27]}
    for claim in inv['claims']:
        assert [e['page'] for e in claim['evidence']] == expected_pages[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 30
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 126
    assert sum(len(c['depends_on']) for c in census['claims']) == 61
    by_local = {it['members'][0]['local_id']: it for it in census['interfaces']}
    def reach(lid):
        return {r['claim_id'].split('/')[-1] for r in by_local[lid]['related_theorems']}
    all_theorems = set(direct)
    for lid in ['D1','D2','D3','D4','D5','D6','D7','D8','D9','D11','D12']:
        assert reach(lid) == all_theorems
    assert reach('D10') == reach('D13') == all_theorems - {'T2'}
    assert reach('D19') == {'T3','T4','T5','T6','T7'}
    assert reach('D14') == reach('D24') == {'T4','T5','T6','T7'}
    for lid in ['D21','D22','D23','D30']:
        assert reach(lid) == {'T5','T6','T7'}
    assert reach('D26') == {'T6','T7'}
    assert reach('D25') == {'T4','T5'}
    assert reach('D16') == reach('D17') == reach('D18') == {'T1'}
    assert reach('D20') == reach('D29') == {'T2'}
    assert reach('D27') == reach('D28') == {'T4'}
    assert reach('D31') == {'T5'}
    assert members['D11']['depends_on'] == ['D2','D9']
    assert members['D21']['depends_on'] == ['D11','D1','D19']
    assert members['D26']['depends_on'] == ['D14']
    assert members['D27']['depends_on'] == members['D28']['depends_on'] == ['D19']
    for lid in ['D3','D4','D5','D7','D24','D25','D26']:
        assert members[lid]['source_kind'] == 'assumption'
    assert members['D19']['source_kind'] == members['D20']['source_kind'] == members['D31']['source_kind'] == 'condition'
    assert members['D16']['source_kind'] == 'definition'
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
    pages = [1] + list(range(5,28)) + [42,43,50]
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
    print('Registered source reviewed: 7 Theorems, 30 source entries, 126 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
