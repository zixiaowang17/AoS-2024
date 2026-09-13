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
    assert len(pdf) == entry['pdf_pages'] == 28
    assert '10.1214/24-AOS2366' in pdf[0].get_text()
    assert all(s in ' '.join(pdf[0].get_text().split()) for s in ['YULING YAN', 'YUXIN CHEN', 'JIANQING FAN', '729–756'])
    headings = []
    for n in range(1, 29):
        page = pdf[n - 1]
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans']).strip()
                match = re.match(r'THEOREM (\d+)\.', text)
                if match: headings.append((n, match[1]))
    assert headings == [(7,'1'),(9,'2'),(11,'3'),(12,'4'),(21,'5')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 28
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert 'SUPPLEMENTARY MATERIAL' in pdf[24].get_text() and 'REFERENCES' in pdf[24].get_text()
    assert '24-AOS2366SUPP' in pdf[24].get_text() and '756' in pdf[27].get_text()
    direct = {
        'T1': {'D1','D2','D4','D6','D7','D8','D9','D10'},
        'T2': {'D1','D2','D4','D6','D7','D8','D9','D11'},
        'T3': {'D1','D2','D6','D7','D9','D10','D12'},
        'T4': {'D1','D2','D6','D7','D9','D13'},
        'T5': {'D14','D15','D16','D17','D18','D5'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    expected_pages = {'T1':[7], 'T2':[9], 'T3':[11], 'T4':[12], 'T5':[21,22]}
    for claim in inv['claims']:
        assert [e['page'] for e in claim['evidence']] == expected_pages[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 18
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 48
    assert sum(len(c['depends_on']) for c in census['claims']) == 35
    by_local = {it['members'][0]['local_id']: it for it in census['interfaces']}
    def reach(lid):
        return {r['claim_id'].split('/')[-1] for r in by_local[lid]['related_theorems']}
    assert reach('D5') == set(direct)
    for lid in ['D1','D2','D3','D4','D6','D7','D9','D10']:
        assert reach(lid) == {'T1','T2','T3','T4'}
    assert reach('D8') == {'T1','T2'}
    assert reach('D11') == {'T2'}
    assert reach('D12') == {'T3','T4'}
    assert reach('D13') == {'T4'}
    for lid in ['D14','D15','D16','D17','D18']:
        assert reach(lid) == {'T5'}
    for it in census['interfaces']:
        for relation in it['related_theorems']:
            path = relation['via_local_ids']
            number = relation['claim_id'].split('/')[-1]
            assert path[0] in direct[number]
            assert path[-1] == it['members'][0]['local_id']
            for x,y in zip(path,path[1:]): assert y in members[x]['depends_on']
    assert members['D7']['source_kind'] == 'definition'
    for lid in ['D9','D15','D16']: assert members[lid]['source_kind'] == 'assumption'
    assert members['D17']['depends_on'] == ['D14','D5']
    assert members['D18']['depends_on'] == ['D14','D17']
    assert members['D15']['depends_on'] == members['D16']['depends_on'] == ['D14']
    assert members['D10']['depends_on'] == ['D4','D5']
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
    pages = list(range(1,14)) + [20,21,22,24,25,28]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=7, path='evidence/revalidation/iteration-crop.png', sha256=digest(ROOT / 'evidence/revalidation/iteration-crop.png'), scope='Magnified iteration formula (3.6), confirming sqrt(nd) times p.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 5 Theorems, 18 source entries, 48 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
