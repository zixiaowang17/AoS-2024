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
    assert len(pdf) == entry['pdf_pages'] == 76
    assert 'arXiv:2112.10151v2' in pdf[0].get_text()
    assert all(s in ' '.join(pdf[0].get_text().split()) for s in ['JINYUAN CHANG', 'QIAO HU', 'ERIC D. KOLACZYK', 'QIWEI YAO', 'FENGTING YI', '2 Apr 2024'])
    headings = []
    for n in range(1, 20):
        page = pdf[n - 1]
        clip = fitz.Rect(0, 0, page.rect.width, 313.6376953125) if n == 19 else page.rect
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text(clip=clip)
        for block in page.get_text('dict', clip=clip)['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans']).strip()
                match = re.match(r'THEOREM (\d+)\.', text)
                if match:
                    headings.append((n, match[1]))
    assert headings == [(9,'1'),(12,'2'),(13,'3'),(18,'4')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 19
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is True
    assert pdf[18].get_text(clip=fitz.Rect(0, 313, pdf[18].rect.width, 330)).strip() == 'APPENDIX'
    direct = {
        'T1': {'D2','D4','D5','D8','D10'},
        'T2': {'D2','D4','D5','D14','D16','D11'},
        'T3': {'D2','D4','D5','D8','D16'},
        'T4': {'D4','D17','D18','D19'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    expected_pages = {'T1':[9,10], 'T2':[12], 'T3':[13], 'T4':[18]}
    for claim in inv['claims']:
        assert [e['page'] for e in claim['evidence']] == expected_pages[claim['claim_id'].split('/')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == 19 and len(census['interfaces']) == 12
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 33
    assert sum(len(c['depends_on']) for c in census['claims']) == 20
    assert sum(len(it['central_claim_uses']) for it in census['interfaces']) == 19
    local_reach = {lid:set() for lid in members}
    for theorem, roots in direct.items():
        pending = list(roots)
        seen = set()
        while pending:
            lid = pending.pop()
            if lid in seen: continue
            seen.add(lid)
            local_reach[lid].add(theorem)
            pending.extend(members[lid]['depends_on'])
    all_theorems = set(direct)
    for lid in ['D1','D2','D3','D4','D6','D7']:
        assert local_reach[lid] == all_theorems
    assert local_reach['D5'] == {'T1','T2','T3'}
    assert local_reach['D8'] == {'T1','T3','T4'}
    assert local_reach['D9'] == local_reach['D10'] == {'T1','T2'}
    assert local_reach['D11'] == local_reach['D14'] == {'T2'}
    for lid in ['D12','D13','D15','D16']:
        assert local_reach[lid] == {'T2','T3'}
    for lid in ['D17','D18','D19']:
        assert local_reach[lid] == {'T4'}
    for it in census['interfaces']:
        expected = set().union(*(local_reach[m['local_id']] for m in it['members']))
        assert {r['claim_id'].split('/')[-1] for r in it['related_theorems']} == expected
        if len(it['members']) > 1:
            assert all(m['relation'] == 'distinct' for m in it['members'])
        for relation in it['related_theorems']:
            path = relation['via_local_ids']
            number = relation['claim_id'].split('/')[-1]
            assert path[0] in direct[number]
            assert path[-1] in {m['local_id'] for m in it['members']}
            for x,y in zip(path,path[1:]): assert y in members[x]['depends_on']
    assert members['D17']['depends_on'] == ['D2']
    assert members['D18']['depends_on'] == ['D17','D8']
    assert members['D16']['depends_on'] == ['D15','D12']
    assert members['D5']['source_kind'] == members['D4']['source_kind'] == 'condition'
    assert members['D19']['source_kind'] == 'source_passage'
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
    pages = [1] + list(range(3,14)) + [17,18,19]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=19, path='evidence/revalidation/appendix-heading.png', sha256=digest(ROOT / 'evidence/revalidation/appendix-heading.png'), scope='Heading-only crop; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 4 Theorems, 19 source entries in 12 groups, 33 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
