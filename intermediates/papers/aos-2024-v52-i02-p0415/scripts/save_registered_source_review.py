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
    assert len(pdf) == entry['pdf_pages'] == 85
    assert 'arXiv:2110.04924v4' in pdf[0].get_text()
    assert all(s in pdf[0].get_text() for s in ['JELENA BRADIC', 'WEIJIE JI', 'YUQIAN ZHANG'])
    headings = []
    for n, page in enumerate(list(pdf)[:25], 1):
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                match = re.match(r'^THEOREM\s+(\d+)(?:\.| \()', ''.join(s['text'] for s in line['spans']))
                if match:
                    headings.append((n, match[1]))
    assert headings == [(3,'1'),(10,'2'),(11,'3'),(11,'4'),(12,'5'),(13,'6'),(14,'7'),(15,'8'),(16,'9'),(16,'10'),(18,'11')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 25
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert all(s in pdf[22].get_text() for s in ['Discussion.', 'Acknowledgement.', 'SUPPLEMENTARY MATERIAL'])
    assert 'SUPPLEMENTARY MATERIALS' in pdf[25].get_text(clip=fitz.Rect(0,0,pdf[25].rect.width,110))
    assert [e['page'] for e in inv['claims'][3]['evidence']] == [11,12]
    direct = {
        'T1': {'D3','D5'},
        'T2': {'D3','D9','D10','D12','D13','D5','D23','D24','D25','D19','D22','D2'},
        'T3': {'D3','D9','D10','D12','D5','D23','D24','D19','D22','D2'},
        'T4': {'D3','D9','D10','D13','D5','D23NR','D24','D25','D20','D22NR','D2'},
        'T5': {'D3','D9','D10','D13','D5','D23NR','D24','D20','D22NR','D2'},
        'T6': {'D3','D5','D25','D30','D26','D27','D2'},
        'T7': {'D3','D5','D30','D26','D27','D2'}, 'T8': {'D31','D6'},
        'T9': {'D3','D5','D23','D24','D25','D9','D10','D12','D16','D22'},
        'T10': {'D5','D23','D24','D10','D13','D17','D22'}, 'T11': {'D34','D33','D32'}
    }
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 37
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 158
    assert sum(len(c['depends_on']) for c in census['claims']) == 80
    by_local = {it['members'][0]['local_id']: it for it in census['interfaces']}
    def reach(lid):
        return {r['claim_id'].split('/')[-1] for r in by_local[lid]['related_theorems']}
    assert reach('D31') == {'T8'} and reach('D32') == {'T11'}
    assert reach('D23NR') == reach('D22NR') == reach('D21NR') == {'T4','T5'}
    assert 'T10' in reach('D23') and 'T10' not in reach('D23NR')
    assert not {'T3','T5','T7','T10'} & reach('D25')
    assert 'T9' not in reach('D19')
    for lid in ['D9','D10','D12','D23']:
        assert not {'T6','T7','T8','T11'} & reach(lid)
    assert all('T8' not in reach(lid) for lid in members if lid not in ['D6','D31'])
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
    pages = list(range(1,19)) + [23,25]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=26, path='evidence/revalidation/supplement-heading.png', sha256=digest(ROOT / 'evidence/revalidation/supplement-heading.png')))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 11 Theorems, 37 source entries, 158 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
