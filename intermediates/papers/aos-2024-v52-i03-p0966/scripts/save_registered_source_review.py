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
    assert len(pdf) == entry['pdf_pages'] == 99
    assert 'arXiv:2107.12364v3' in pdf[0].get_text()
    assert all(s in pdf[0].get_text().lower() for s in ['tudor manole','sivaraman balakrishnan','jonathan niles-weed','larry wasserman','16 jun 2024'])
    headings = []
    boundary = 637.536865234375
    for n in range(1,30):
        page = pdf[n-1]
        clip = fitz.Rect(0,0,page.rect.width,boundary) if n == 29 else page.rect
        fresh = page.get_text(clip=clip)
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == fresh
        for block in page.get_text('dict',clip=clip)['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans']).strip()
                match = re.match(r'^THEOREM (\d+)(?=[.\s(])', text)
                if match: headings.append((n,match[1]))
    assert headings == [(9,'1'),(10,'3'),(11,'5'),(12,'6'),(16,'10'),(21,'18'),(24,'20'),(26,'22'),(28,'24')]
    assert [c['claim_id'] for c in inv['claims']] == [PID+'/T'+n for _,n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 29
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is True
    assert 'APPENDIX A: SMOOTHNESS CLASSES AND DENSITY ESTIMATION' in pdf[28].get_text(clip=fitz.Rect(0,boundary,pdf[28].rect.width,651))
    direct = {
        'T1': {1,2,3,7,8}, 'T3': {1,9,11}, 'T5': {15,18,11},
        'T6': {1,2,3,9,10,20,5}, 'T10': {1,21,25,9,20,12,13,7,10,5},
        'T18': {15,18,19,13,26,27,28,29,17}, 'T20': {30,31,35,33,36,9,12,40},
        'T22': {2,15,11,9,18,7,22,24,27,28,26,37}, 'T24': {15,13,19,38,39}}
    direct = {n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    for claim,(page,n) in zip(inv['claims'],headings):
        assert [e['page'] for e in claim['evidence']] == ([21,22] if n=='18' else [page])
    members = {m['local_id']:m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 40
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 109
    assert sum(len(c['depends_on']) for c in census['claims']) == 62
    expected_reach = {
        'T1': {1,2,3,4,5,6,7,8}, 'T3': {1,2,3,9,11}, 'T5': {11,14,15,16,18},
        'T6': {1,2,3,4,5,6,7,9,10,11,20},
        'T10': {1,2,3,4,5,6,7,9,10,11,12,13,20,21,22,23,24,25},
        'T18': {7,11,13,14,15,16,17,18,19,22,26,27,28,29},
        'T20': {2,3,9,11,12,13,22,30,31,32,33,34,35,36,40},
        'T22': {2,3,4,5,6,7,9,10,11,14,15,16,17,18,19,22,23,24,26,27,28,37},
        'T24': {7,11,13,14,15,16,17,18,19,38,39}}
    expected_reach = {n:{f'D{i}' for i in ids} for n,ids in expected_reach.items()}
    for it in census['interfaces']:
        lid = it['members'][0]['local_id']
        assert {r['claim_id'].split('/')[-1] for r in it['related_theorems']} == {n for n,ids in expected_reach.items() if lid in ids}
        for relation in it['related_theorems']:
            path = relation['via_local_ids']
            assert path[0] in direct[relation['claim_id'].split('/')[-1]]
            assert path[-1] == lid
            for x,y in zip(path,path[1:]): assert y in members[x]['depends_on']
    conditions = {1,20,28,30,31,33}
    passages = {11,21,26,37,39,40}
    for lid,m in members.items():
        n=int(lid[1:])
        assert m['source_kind'] == ('condition' if n in conditions else 'source_passage' if n in passages else 'definition')
    expected_edges = {
        1:[],2:[],3:[2],4:[2],5:[4],6:[5],7:[],8:[6,7],9:[3],10:[9,7,6],
        11:[],12:[11],13:[11],14:[],15:[14],16:[14,15],17:[14,15],18:[16],19:[18,7,17],
        20:[9,11],21:[2],22:[],23:[],24:[23,22],25:[3,24],26:[],27:[15,22],28:[],29:[27,16],
        30:[],31:[13,3],32:[30],33:[],34:[32,33,22],35:[11,12,13],36:[34,3],
        37:[5,17,10,19],38:[17],39:[19],40:[2]}
    assert {lid:m['depends_on'] for lid,m in members.items()} == {f'D{k}':[f'D{i}' for i in ids] for k,ids in expected_edges.items()}
    assert members['D25']['relation'] == members['D38']['relation'] == 'specialization'
    aux = json.loads((ROOT / 'ambient-conventions.json').read_text())
    assert len(aux['auxiliary_passages']) == 17
    assert len(aux['unresolved_source_conventions']) == 31
    refs = aux['unresolved_statement_references']
    assert len(refs) == 4 and all(r['status']=='excluded_appendix' for r in refs)
    assert {r['reference'] for r in refs} == {'Appendix A — Hölder norms and spaces','Appendix A — boundary-corrected wavelet construction','Appendix A — H2 Sobolev space','Appendix L, equations (115–116)'}
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
    pages = [1,3,7,8,9,10,11,12,13,15,16,18,20,21,22,23,24,25,26,27,28,29]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=29, path='evidence/revalidation/appendix-heading.png', sha256=digest(ROOT / 'evidence/revalidation/appendix-heading.png'), scope='Heading-only crop; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 9 Theorems, 40 source entries, 109 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
