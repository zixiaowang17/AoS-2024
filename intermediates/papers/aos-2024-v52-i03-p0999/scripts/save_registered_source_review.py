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
    assert len(pdf) == entry['pdf_pages'] == 112
    assert 'arXiv:2207.12453v3' in pdf[0].get_text()
    assert all(s in pdf[0].get_text() for s in ['Haotian Xu', 'Daren Wang', 'Zifeng Zhao', 'Yi Yu', '1 Oct 2023', 'October 3, 2023'])
    headings = []; mentions = []; assumptions = []
    for n in range(1,34):
        page = pdf[n-1]
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans']).strip()
                match = re.match(r'^Theorem (\d+)(?=[.\s(])', text)
                if match:
                    if line['spans'][0]['font']=='CMBX10': headings.append((n,match[1]))
                    else: mentions.append((n,text))
                match = re.match(r'^Assumption (\d+)\s*\(',text)
                if match and line['spans'][0]['font']=='CMBX10': assumptions.append((n,match[1]))
    assert headings == [(12,'3'),(17,'4'),(18,'8'),(21,'10')]
    assert [p for p,text in mentions] == [13,16,17,18]
    assert assumptions == [(9,'1'),(10,'2'),(11,'3'),(11,'4')]
    assert [c['claim_id'] for c in inv['claims']] == [PID+'/T'+n for _,n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 33
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is False
    assert 'Zhang' in pdf[32].get_text()
    assert pdf[33].get_text(clip=fitz.Rect(0,0,pdf[33].rect.width,89)).strip() == 'Appendices'
    common = {2,3,4,34,12,13,14,15,16,17,18,21,19,25,22,26}
    direct = {'T3':common|{27,28,33}, 'T4':{10,11},
              'T8':common|{28,29,30,33}, 'T10':common|{28,29,30,32,33}}
    direct = {n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    for claim,(page,n) in zip(inv['claims'],headings):
        assert [e['page'] for e in claim['evidence']] == ([12,13] if n=='3' else [page])
    for old,new in zip(inv['claims'],census['claims']):
        assert all(new[k]==v for k,v in old.items())
    members = {m['local_id']:m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 33
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 87
    assert sum(len(c['depends_on']) for c in census['claims']) == 62
    base = {1,2,3,4,5,7,8,9,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,33,34}
    expected_reach = {'T3':base|{27},'T4':{10,11},'T8':base|{29,30},'T10':base|{29,30,31,32}}
    expected_reach = {n:{f'D{i}' for i in ids} for n,ids in expected_reach.items()}
    for it in census['interfaces']:
        lid = it['members'][0]['local_id']
        assert {r['claim_id'].split('/')[-1] for r in it['related_theorems']} == {n for n,ids in expected_reach.items() if lid in ids}
        assert {u['claim_id'].split('/')[-1] for u in it['central_claim_uses']} == {n for n,ids in direct.items() if lid in ids}
        for relation in it['related_theorems']:
            path = relation['via_local_ids']
            assert path[0] in direct[relation['claim_id'].split('/')[-1]]
            assert path[-1] == lid
            for x,y in zip(path,path[1:]): assert y in members[x]['depends_on']
    assumptions = {2,3,4,12,13,14,15,16,17,18,20,21}
    for lid,m in members.items():
        n=int(lid[1:])
        assert m['source_kind'] == ('assumption' if n in assumptions else 'source_passage' if n==1 else 'definition')
    expected_edges = {
        1:[],2:[1],3:[1],4:[34],5:[],7:[5],8:[],9:[8],10:[],11:[10],
        12:[5],13:[7],14:[5],15:[12,34],16:[8],17:[9],18:[8],
        19:[13,17,14,18],20:[4,3,19],21:[20],22:[],23:[22],24:[23],
        25:[24,22,23],26:[25],27:[26,22],28:[34,5,8],29:[22,25],
        30:[26,29,22,25],31:[29,22],32:[30,31],33:[34],34:[1]}
    assert {lid:m['depends_on'] for lid,m in members.items()} == {f'D{k}':[f'D{i}' for i in ids] for k,ids in expected_edges.items()}
    aux = json.loads((ROOT / 'ambient-conventions.json').read_text())
    assert len(aux['auxiliary_passages']) == 13
    assert len(aux['unresolved_source_conventions']) == 33
    assert aux['unresolved_statement_references'] == []
    assert set(aux['standard_ambient_resolution']) == {'shared','3','4','8','10'}
    for item in list(members.values())+aux['auxiliary_passages']:
        assert all(1<=e['page']<=33 for e in item['evidence'])
    for it in census['interfaces']:
        assert '$' not in it['name']
        for keyword in it['source_keywords']:
            m=members[keyword['local_id']]
            texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])]
            assert any(keyword['source_text'] in s for s in texts)
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
    pages = [1,2,4,5,6,7,8,9,10,11,12,13,17,18,19,20,21,33]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=34, path='evidence/revalidation/appendix-heading.png', sha256=digest(ROOT / 'evidence/revalidation/appendix-heading.png'), scope='Heading-only crop; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 4 Theorems, 33 source entries, 87 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
