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
    assert len(pdf) == entry['pdf_pages'] == 73
    assert 'arXiv:2202.06117v4' in pdf[0].get_text()
    assert all(s in ' '.join(pdf[0].get_text().split()) for s in ['PAROMITA DUBEY', 'YAQING CHEN', 'HANS-GEORG MÜLLER', '27 Feb 2024'])
    headings = []
    for n in range(1, 34):
        page = pdf[n - 1]
        clip = fitz.Rect(0, 0, page.rect.width, 106.52787780761719) if n == 33 else page.rect
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text(clip=clip)
        for block in page.get_text('dict', clip=clip)['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans']).strip()
                match = re.match(r'THEOREM (\d+(?:\.\d+)*)\.', text)
                if match: headings.append((n, match[1]))
    assert headings == [(11,'4.1'),(12,'5.1'),(13,'5.2'),(14,'5.3'),(17,'6.1'),(17,'6.2'),(18,'6.3')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 33
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is True
    assert pdf[32].get_text(clip=fitz.Rect(0,106,pdf[32].rect.width,120)).strip() == 'SUPPLEMENTARY MATERIAL'
    direct = {
        'T4.1': {'D1','D2','D3','D4','D5','D6'},
        'T5.1': {'D10','D11','D7','D12'},
        'T5.2': {'D10','D11','D8','D4'},
        'T5.3': {'D10','D11','D14','D5','D9','D13'},
        'T6.1': {'D10','D18','D19','D20','D15','D17','D23'},
        'T6.2': {'D10','D18','D19','D20','D22','D28'},
        'T6.3': {'D10','D18','D19','D20','D15','D24','D25','D23','D26','D27'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    for claim,(page,_) in zip(inv['claims'],headings):
        assert [e['page'] for e in claim['evidence']] == [page]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 28
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 70
    assert sum(len(c['depends_on']) for c in census['claims']) == 43
    by_local = {it['members'][0]['local_id']: it for it in census['interfaces']}
    def reach(lid):
        return {r['claim_id'].split('/')[-1] for r in by_local[lid]['related_theorems']}
    assert reach('D1') == reach('D2') == set(direct)
    assert reach('D10') == set(direct) - {'T4.1'}
    assert reach('D3') == reach('D6') == {'T4.1'}
    assert reach('D4') == {'T4.1','T5.2','T5.3'}
    assert reach('D5') == {'T4.1','T5.3'}
    assert reach('D7') == reach('D11') == {'T5.1','T5.2','T5.3'}
    assert reach('D8') == {'T5.2','T5.3'}
    assert reach('D12') == {'T5.1'}
    for lid in ['D9','D13','D14']: assert reach(lid) == {'T5.3'}
    for lid in ['D15','D16','D17','D18','D19','D20','D23']:
        assert reach(lid) == {'T6.1','T6.2','T6.3'}
    for lid in ['D21','D22','D24']: assert reach(lid) == {'T6.2','T6.3'}
    for lid in ['D25','D26','D27']: assert reach(lid) == {'T6.3'}
    assert reach('D28') == {'T6.2'}
    for it in census['interfaces']:
        for relation in it['related_theorems']:
            path = relation['via_local_ids']
            number = relation['claim_id'].split('/')[-1]
            assert path[0] in direct[number]
            assert path[-1] == it['members'][0]['local_id']
            for x,y in zip(path,path[1:]): assert y in members[x]['depends_on']
    for lid in ['D10','D11','D14','D18','D19','D20']:
        assert members[lid]['source_kind'] == 'assumption'
    assert members['D23']['source_kind'] == 'theorem_excerpt'
    assert members['D24']['depends_on'] == ['D23']
    assert members['D8']['depends_on'] == ['D7','D4']
    assert members['D26']['depends_on'] == ['D15','D17','D23']
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
    pages = [1,7,8,9] + list(range(11,19)) + [32,33]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=33, path='evidence/revalidation/supplement-heading.png', sha256=digest(ROOT / 'evidence/revalidation/supplement-heading.png'), scope='Heading-only crop; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 7 Theorems, 28 source entries, 70 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
