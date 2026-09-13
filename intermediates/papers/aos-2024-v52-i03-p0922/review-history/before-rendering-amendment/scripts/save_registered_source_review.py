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
    assert len(pdf) == entry['pdf_pages'] == 102
    assert 'arXiv:2210.08393v4' in pdf[0].get_text()
    assert all(s in pdf[0].get_text() for s in ['Xi Chen', 'Wenbo Jing', 'Weidong Liu', 'Yichen Zhang', '15 Aug 2024'])
    headings = []
    references = []
    for n in range(1, 41):
        page = pdf[n - 1]
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans']).strip()
                match = re.match(r'Theorem (\d+\.\d+)(?=[.\s(])', text)
                if match:
                    if line['spans'][0]['font'] == 'CMBX10': headings.append((n, match[1]))
                    else: references.append((n, match[1]))
    assert headings == [(16,'3.1'),(19,'3.3'),(20,'3.4'),(24,'4.1'),(24,'4.2'),(25,'4.3'),(28,'5.1'),(29,'5.2')]
    assert references == [(16,'3.1'),(30,'5.2')]
    assert [c['claim_id'] for c in inv['claims']] == [PID + '/T' + n for _, n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 40
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert pdf[40].get_text(clip=fitz.Rect(0,0,pdf[40].rect.width,99)).strip() == 'A\nTheoretical Results of the High-dimensional multi-round SMSE'
    assert 'Zhou' in pdf[39].get_text()
    direct = {
        'T3.1': {'D2','D3','D5','D6','D7','D8','D9','D11'},
        'T3.3': {'D2','D3','D5','D6','D7','D8','D9','D13'},
        'T3.4': {'D2','D3','D5','D6','D7','D8','D9','D13'},
        'T4.1': {'D14','D3','D5','D9','D15','D16','D17','D18','D20'},
        'T4.2': {'D14','D3','D5','D9','D15','D16','D17','D18','D21'},
        'T4.3': {'D22','D3','D5','D6','D7','D8','D9','D23'},
        'T5.1': {'D2','D3','D5','D6','D7','D8','D24','D25'},
        'T5.2': {'D2','D3','D5','D6','D7','D8','D24','D25'}}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    continuation_pages = {'4.3':[25,27], '5.1':[28,29], '5.2':[29,30]}
    for claim,(page,n) in zip(inv['claims'],headings):
        assert [e['page'] for e in claim['evidence']] == continuation_pages.get(n,[page])
    members = {m['local_id']: m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 25
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 89
    assert sum(len(c['depends_on']) for c in census['claims']) == 66
    all_theorems = set(direct)
    baseline = {'T3.1','T3.3','T3.4','T5.1','T5.2'}
    heterogeneous = {'T4.1','T4.2'}
    expected_reach = {
        'D1':all_theorems, 'D2':baseline, 'D3':all_theorems,
        'D4':baseline|{'T4.3'}, 'D5':all_theorems,
        'D6':baseline|{'T4.3'}, 'D7':baseline|{'T4.3'}, 'D8':baseline|{'T4.3'},
        'D9':all_theorems-{'T5.1','T5.2'}, 'D10':{'T3.1','T4.1','T4.3'},
        'D11':{'T3.1'}, 'D12':{'T3.3','T3.4','T5.1','T5.2'}, 'D13':{'T3.3','T3.4'},
        'D14':heterogeneous, 'D15':heterogeneous, 'D16':heterogeneous,
        'D17':heterogeneous, 'D18':heterogeneous, 'D19':heterogeneous,
        'D20':{'T4.1'}, 'D21':{'T4.2'}, 'D22':{'T4.3'}, 'D23':{'T4.3'},
        'D24':{'T5.1','T5.2'}, 'D25':{'T5.1','T5.2'}}
    for it in census['interfaces']:
        lid = it['members'][0]['local_id']
        assert {r['claim_id'].split('/')[-1] for r in it['related_theorems']} == expected_reach[lid]
        for relation in it['related_theorems']:
            path = relation['via_local_ids']
            assert path[0] in direct[relation['claim_id'].split('/')[-1]]
            assert path[-1] == lid
            for x,y in zip(path,path[1:]): assert y in members[x]['depends_on']
    for lid,m in members.items():
        expected_kind = ('assumption' if lid in {'D2','D5','D6','D7','D8','D9','D15','D16','D17','D18','D24'} else
                         'source_passage' if lid in {'D1','D4','D14','D22'} else
                         'condition' if lid == 'D3' else 'definition')
        assert m['source_kind'] == expected_kind
    expected_edges = {
        'D1':[], 'D2':['D1'], 'D3':[], 'D4':[], 'D5':[], 'D6':['D1','D5'],
        'D7':['D1','D5'], 'D8':['D5','D6','D7'], 'D9':[], 'D10':[],
        'D11':['D4','D10'], 'D12':['D4'], 'D13':['D12'], 'D14':['D1'],
        'D15':['D14','D5'], 'D16':['D14','D5'], 'D17':['D5','D15','D16'],
        'D18':['D14'], 'D19':['D14'], 'D20':['D19','D10'], 'D21':['D19'],
        'D22':['D4'], 'D23':['D4','D10','D5'], 'D24':['D1'], 'D25':['D12']}
    assert {lid:m['depends_on'] for lid,m in members.items()} == expected_edges
    aux = json.loads((ROOT / 'ambient-conventions.json').read_text())
    assert len(aux['auxiliary_passages']) == 12
    assert len(aux['unresolved_source_conventions']) == 27
    refs = aux['unresolved_statement_references']
    assert len(refs) == 1 and refs[0]['claim_id'] == PID+'/T5.2'
    assert refs[0]['reference'] == 'Section A of Appendix'
    assert refs[0]['status'] == 'outside_main_text_scope'
    assert refs[0]['items'] == ['Proper choices of h_t, lambda_n^(t) and H','Formal definition of r_m']
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
    pages = [1,2,9,10,11,12,13,14,15,16,19,20,21,22,23,24,25,26,27,28,29,30,40]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=41, path='evidence/revalidation/appendix-heading.png', sha256=digest(ROOT / 'evidence/revalidation/appendix-heading.png'), scope='Heading-only crop; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 8 Theorems, 25 source entries, 89 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
