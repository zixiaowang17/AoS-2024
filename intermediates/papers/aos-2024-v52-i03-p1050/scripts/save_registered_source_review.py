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
    assert len(pdf) == entry['pdf_pages'] == 53
    assert 'arXiv:1710.00915v5' in pdf[0].get_text()
    assert all(s in pdf[0].get_text().lower() for s in ['yanglei song','georgios fellouris','21 jun 2024'])
    headings = []; mentions = []
    for n in range(1,27):
        page = pdf[n-1]
        clip = fitz.Rect(0,0,page.rect.width,137.4) if n==26 else page.rect
        assert (ROOT / f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8') == page.get_text(clip=clip)
        for block in page.get_text('dict',clip=clip)['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans']).strip()
                match = re.match(r'^(THEOREM|Theorem)\s+(\d+\.\d+)', text)
                if match: (headings if match[1]=='THEOREM' else mentions).append((n,match[2]))
    assert headings == [(8,'3.1'),(12,'5.1'),(17,'6.1')]
    assert mentions == [(16,'5.1')]
    assert [c['claim_id'] for c in inv['claims']] == [PID+'/T'+n for _,n in headings]
    assert inv['papers'][0]['main_text_last_pdf_page'] == 26
    assert inv['papers'][0]['main_text_boundary']['shared_page_with_appendix'] is True
    assert '[48]' in pdf[25].get_text(clip=fitz.Rect(0,0,pdf[25].rect.width,137.4))
    assert 'APPENDIX A:' in pdf[25].get_text(clip=fitz.Rect(0,137.4,pdf[25].rect.width,152))
    direct = {'T3.1':{5,14,10,9,6},'T5.1':{3,4,21,23,15,18,19,24,22,25,26,27},'T6.1':{3,4,21,29,30,31,8,28}}
    direct = {n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    for claim in census['claims']:
        assert set(claim['depends_on']) == direct[claim['claim_id'].split('/')[-1]]
    for claim,(page,n) in zip(inv['claims'],headings):
        assert [e['page'] for e in claim['evidence']] == ([12,13] if n=='5.1' else [page])
    for old,new in zip(inv['claims'],census['claims']):
        assert all(new[k]==v for k,v in old.items())
    members = {m['local_id']:m for it in census['interfaces'] for m in it['members']}
    assert len(members) == len(census['interfaces']) == 31
    assert sum(len(it['theorem_explanations']) for it in census['interfaces']) == 45
    assert sum(len(c['depends_on']) for c in census['claims']) == 25
    expected_reach = {
        'T3.1':{1,2,3,4,5,6,7,9,10,11,12,13,14},
        'T5.1':{1,2,3,4,9,15,16,17,18,19,20,21,22,23,24,25,26,27},
        'T6.1':{1,2,3,4,7,8,15,20,21,26,28,29,30,31}}
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
    for lid,m in members.items():
        n=int(lid[1:])
        assert m['source_kind'] == ('assumption' if n in {21,23} else 'source_passage' if n in {1,2,3,4,28} else 'condition' if n in {29,30,31} else 'definition')
    expected_edges = {
        1:[],2:[1],3:[1,2],4:[1,2],5:[4],6:[4],7:[2,1],8:[7,4],9:[1,4],
        10:[7,9,5,4],11:[7,9,5,3],12:[11,10],13:[11,12],14:[12,13],15:[2],16:[3],
        17:[9,16],18:[15,17],19:[18,15],20:[3],21:[20],22:[15,20,21],23:[4,15],
        24:[22,23],25:[4,15],26:[4,15],27:[4,15],28:[4,3],29:[4,28],30:[26,2,4,28],31:[20,4,28]}
    assert {lid:m['depends_on'] for lid,m in members.items()} == {f'D{k}':[f'D{i}' for i in ids] for k,ids in expected_edges.items()}
    aux = json.loads((ROOT / 'ambient-prerequisites.json').read_text())
    assert len(aux['auxiliary_source_passages']) == 6
    assert len(aux['source_issues']) == 33
    refs=aux['excluded_references']
    assert len(refs)==1 and refs[0]['status']=='appendix_definition_unresolved'
    assert refs[0]['source']=='Appendix B.1, equation (B.1): predictive response density phi'
    assert set(aux['statement_resolution']) == {'shared','3.1','5.1','6.1'}
    for item in list(members.values())+aux['auxiliary_source_passages']:
        assert all(1<=e['page']<26 for e in item['evidence'])
    for it in census['interfaces']:
        assert '$' not in it['name']
        for keyword in it['source_keywords']:
            m=members[keyword['local_id']]
            texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])]
            assert any(keyword['source_text'] in s for s in texts)
    assert members['D16']['naming_context'][0]['evidence'][0]['page']==9
    assert members['D31']['naming_context'][0]['evidence'][0]['page']==18
    def has_span(n,font,fragment):
        return any(s['font']==font and fragment in s['text'] for b in pdf[n-1].get_text('dict')['blocks'] for ln in b.get('lines',[]) for s in ln['spans'])
    assert has_span(8,'MSBM10','S') and has_span(10,'CMMI10','S')
    assert has_span(12,'CMSS10','D') and has_span(12,'CMSS10','E') and has_span(13,'CMSY10','R')
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
    pages = [1,4,5,6,7,8,9,10,11,12,13,16,17,18,26]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=26, path='evidence/revalidation/appendix-heading.png', sha256=digest(ROOT / 'evidence/revalidation/appendix-heading.png'), scope='Heading-only crop; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 3 Theorems, 31 source entries, 45 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
