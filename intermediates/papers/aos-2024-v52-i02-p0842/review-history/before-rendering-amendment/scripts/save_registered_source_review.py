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
    assert '10.1214/24-AOS2371' in pdf[0].get_text()
    assert all(s in pdf[0].get_text() for s in ['PREDRAG PILIPOVIC', 'ADELINE SAMSON', 'SUSANNE DITLEVSEN', '842–867'])
    headings = []
    for n in range(1, 27):
        page = pdf[n - 1]
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans']).strip()
                match = re.match(r'THEOREM (\d+(?:\.\d+)*)(?=[.\s(])', text)
                if match: headings.append((n, match[1]))
    assert headings == [(14,'3.3'),(14,'3.5'),(15,'3.7'),(17,'5.1'),(18,'5.2')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 26
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert all(s in pdf[22].get_text() for s in ['SUPPLEMENTARY MATERIAL','24-AOS2371SUPPA','24-AOS2371SUPPB','REFERENCES'])
    assert 'R CORE TEAM' in pdf[25].get_text()
    direct = {
        'T3.3': {'D1','D3','D4','D8','D14','D15'},
        'T3.5': {'D1','D3','D4','D8','D12'},
        'T3.7': {'D1','D3','D4','D8','D11','D13'},
        'T5.1': {'D1','D2','D3','D4','D5','D6','D7','D8','D11','D16'},
        'T5.2': {'D1','D2','D3','D4','D5','D6','D7','D8','D11','D16','D17','D18'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    for claim,(page,_) in zip(inv['claims'],headings):
        assert [e['page'] for e in claim['evidence']] == [page]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 18
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 50
    assert sum(len(c['depends_on']) for c in census['claims']) == 39
    for it in census['interfaces']:
        lid = it['members'][0]['local_id']
        if lid in {'D1','D2','D3','D4','D8'}: expected = set(direct)
        elif lid in {'D5','D6','D7','D16'}: expected = {'T5.1','T5.2'}
        elif lid in {'D9','D10'}: expected = {'T3.5','T3.7','T5.1','T5.2'}
        elif lid == 'D11': expected = {'T3.7','T5.1','T5.2'}
        elif lid == 'D12': expected = {'T3.5'}
        elif lid == 'D13': expected = {'T3.7'}
        elif lid in {'D14','D15'}: expected = {'T3.3'}
        else: expected = {'T5.2'}
        assert {r['claim_id'].split('/')[-1] for r in it['related_theorems']} == expected
        for relation in it['related_theorems']:
            path = relation['via_local_ids']
            assert path[0] in direct[relation['claim_id'].split('/')[-1]]
            assert path[-1] == lid
            for x,y in zip(path,path[1:]): assert y in members[x]['depends_on']
    for lid,m in members.items():
        expected_kind = 'assumption' if lid in {'D3','D4','D5','D6','D7','D11'} else 'source_passage' if lid in {'D1','D2','D8'} else 'definition'
        assert m['source_kind'] == expected_kind
    expected_edges = {'D1': [], 'D2': ['D1'], 'D3': ['D2'], 'D4': ['D2'],
        'D5': ['D1'], 'D6': ['D2'], 'D7': ['D1'], 'D8': ['D1'],
        'D9': ['D2'], 'D10': ['D2','D3','D4'], 'D11': ['D10'],
        'D12': ['D3','D4','D9','D10'], 'D13': ['D3','D4','D9','D10'],
        'D14': ['D1','D8'], 'D15': ['D1','D8'], 'D16': ['D2','D8','D9','D10','D11'],
        'D17': ['D2'], 'D18': ['D1','D2','D5','D17']}
    assert {lid:m['depends_on'] for lid,m in members.items()} == expected_edges
    aux = json.loads((ROOT / 'ambient-conventions.json').read_text())
    assert len(aux['auxiliary_passages']) == 8
    assert len(aux['unresolved_source_conventions']) == 19
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
    pages = [1,6,7,8,9,10,13,14,15,16,17,18,23,26]
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
    print('Registered source reviewed: 5 Theorems, 18 source entries, 50 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
