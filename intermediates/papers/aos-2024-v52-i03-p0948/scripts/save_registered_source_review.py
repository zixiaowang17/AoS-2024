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
    assert len(pdf) == entry['pdf_pages'] == 60
    assert 'arXiv:2203.12003v1' in pdf[0].get_text()
    assert all(s in pdf[0].get_text() for s in ['Bingxin Zhao', 'Shurong Zheng', 'Hongtu Zhu', '22 Mar 2022', 'June 13, 2025'])
    headings = []
    references = []
    for n in range(1, 28):
        page = pdf[n - 1]
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans']).strip()
                match = re.match(r'Theorem (\d+)(?=[.\s(])', text)
                if match:
                    if line['spans'][0]['font'] == 'URWPalladioL-Bold': headings.append((n, match[1]))
                    else: references.append((n, match[1]))
    assert headings == [(8,'1'),(9,'2'),(12,'3'),(12,'4')]
    assert references == [(10,'2'),(12,'3'),(13,'4')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 27
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert 'Supplementary Material for' in pdf[27].get_text(clip=fitz.Rect(0,0,pdf[27].rect.width,155))
    assert 'Zhou' in pdf[26].get_text()
    direct = {
        'T1': {'D3','D4','D5','D6','D10','D13','D19'},
        'T2': {'D3','D4','D5','D6','D2','D7','D8','D22','D9','D14','D17','D19'},
        'T3': {'D3','D4','D5','D6','D11','D20'},
        'T4': {'D3','D4','D5','D6','D2','D7','D8','D23','D9','D15','D16','D17','D20'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    evidence_pages = {'1':[8,9], '2':[9,10], '3':[12], '4':[12,13]}
    for claim in inv['claims']:
        assert [e['page'] for e in claim['evidence']] == evidence_pages[claim['claim_id'].split('/T')[-1]]
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 23
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 53
    assert sum(len(c['depends_on']) for c in census['claims']) == 38
    all_theorems = set(direct)
    expected_reach = {
        'D1':all_theorems, 'D2':{'T2','T4'}, 'D3':all_theorems,
        'D4':all_theorems, 'D5':all_theorems, 'D6':all_theorems,
        'D7':{'T2','T4'}, 'D8':{'T2','T4'}, 'D9':{'T2','T4'},
        'D10':{'T1','T2'}, 'D11':{'T3','T4'}, 'D12':{'T4'},
        'D13':{'T1','T2','T4'}, 'D14':{'T2'}, 'D15':{'T4'}, 'D16':{'T4'},
        'D17':{'T2','T4'}, 'D18':all_theorems, 'D19':{'T1','T2'},
        'D20':{'T3','T4'}, 'D21':{'T2','T4'}, 'D22':{'T2'}, 'D23':{'T4'}}
    for it in census['interfaces']:
        lid = it['members'][0]['local_id']
        assert {r['claim_id'].split('/')[-1] for r in it['related_theorems']} == expected_reach[lid]
        for relation in it['related_theorems']:
            path = relation['via_local_ids']
            assert path[0] in direct[relation['claim_id'].split('/')[-1]]
            assert path[-1] == lid
            for x,y in zip(path,path[1:]): assert y in members[x]['depends_on']
    for lid,m in members.items():
        expected_kind = ('condition' if lid in {'D3','D4','D5','D6','D7','D8','D22','D23'} else
                         'source_passage' if lid in {'D1','D2','D19'} else 'definition')
        assert m['source_kind'] == expected_kind
    expected_edges = {
        'D1':[], 'D2':['D1'], 'D3':['D1'], 'D4':['D3'], 'D5':['D4'], 'D6':['D1','D4'],
        'D7':['D2'], 'D8':['D2'], 'D9':['D2'], 'D10':['D4'], 'D11':['D4'], 'D12':['D4'],
        'D13':['D1'], 'D14':['D10'], 'D15':['D11'], 'D16':['D12'], 'D17':['D1'], 'D18':[],
        'D19':['D10','D18'], 'D20':['D11','D5','D6','D18'], 'D21':['D2'],
        'D22':['D21','D7','D10','D13'], 'D23':['D21','D7','D11','D12','D13']}
    assert {lid:m['depends_on'] for lid,m in members.items()} == expected_edges
    aux = json.loads((ROOT / 'ambient-conventions.json').read_text())
    assert len(aux['auxiliary_passages']) == 8
    assert len(aux['unresolved_source_conventions']) == 28
    assert aux['unresolved_statement_references'] == []
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
    pages = [1,4,5,6,7,8,9,10,12,13,22,27]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=28, path='evidence/revalidation/appendix-heading.png', sha256=digest(ROOT / 'evidence/revalidation/appendix-heading.png'), scope='Heading-only crop; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 4 Theorems, 23 source entries, 53 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
