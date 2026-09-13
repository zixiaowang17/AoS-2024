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
    assert len(pdf) == entry['pdf_pages'] == 108
    assert 'arXiv:2111.11694v5' in pdf[0].get_text()
    assert all(s in pdf[0].get_text().lower() for s in ['dohyeong ki','billy fang','adityanand guntuboyina','13 oct 2024'])
    paper=inv['papers'][0]
    assert paper['version']=='arXiv:2111.11694v5'
    assert paper['source_url']=='https://arxiv.org/pdf/2111.11694v5'
    assert paper['title'].upper() in pdf[0].get_text()
    assert 'Published in the Annals of Statistics' in pdf[0].get_text()
    assert digest(source)==paper['pdf_sha256']
    assert paper['main_text_last_pdf_page']==25
    assert paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert 'YEH' in pdf[24].get_text()
    assert 'APPENDIX A:' in pdf[25].get_text(clip=fitz.Rect(0,165,pdf[25].rect.width,181))
    headings=[];mentions=[]
    for n in range(1,26):
        page=pdf[n-1]
        assert (ROOT/f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8')==page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans']).strip()
                match=re.match(r'^(THEOREM|Theorem)\s+(\d+\.\d+)',text)
                if match:(headings if match[1]=='THEOREM' else mentions).append((n,match[2]))
    assert headings==[(9,'3.1'),(10,'3.2'),(11,'3.4'),(12,'3.5'),(12,'3.6'),(12,'3.8'),(13,'3.9')]
    assert mentions==[(10,'3.2'),(11,'3.1'),(11,'3.4'),(12,'3.6')]
    assert [c['claim_id'] for c in inv['claims']]==[PID+'/T'+n for _,n in headings]
    assert len(inv['claims'])==len(census['claims'])==7
    for claim,(page,n) in zip(inv['claims'],headings):assert [e['page'] for e in claim['evidence']]==[page]
    for old,new in zip(inv['claims'],census['claims']):assert all(new[k]==v for k,v in old.items())
    members={m['local_id']:m for it in census['interfaces'] for m in it['members']}
    assert len(members)==len(census['interfaces'])==22
    direct={'3.1':{3,5,12,13,6,14},'3.2':{15,22},'3.4':{3,5,12,13,11,14,8},'3.5':{3,5,6,16,17,18},'3.6':{15,21},'3.8':{3,5,11,8,16,17,18},'3.9':{19,20}}
    direct={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    assert {c['claim_id'].split('/T')[-1]:set(c['depends_on']) for c in census['claims']}==direct
    expected_reach={
        '3.1':{1,2,3,4,5,6,12,13,14},'3.2':{1,4,15,22},
        '3.4':{1,2,3,4,5,7,8,9,10,11,12,13,14},
        '3.5':{1,2,3,4,5,6,16,17,18},'3.6':{1,4,15,21},
        '3.8':{1,2,3,4,5,7,8,9,10,11,16,17,18},
        '3.9':{1,2,3,4,5,16,17,18,19,20}}
    expected_reach={n:{f'D{i}' for i in ids} for n,ids in expected_reach.items()}
    expected_edges={1:[],2:[],3:[1,2],4:[],5:[3,4],6:[3,5],7:[],8:[3],9:[3,5,7,8,2,1],10:[7,2,1],11:[9,10],12:[],13:[],14:[13],15:[1,4],16:[],17:[16],18:[16],19:[3,5,17,18],20:[17,16],21:[15],22:[15]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in ids] for k,ids in expected_edges.items()}
    for it in census['interfaces']:
        lid=it['members'][0]['local_id']
        assert {r['claim_id'].split('/T')[-1] for r in it['related_theorems']}=={n for n,ids in expected_reach.items() if lid in ids}
        assert {u['claim_id'].split('/T')[-1] for u in it['central_claim_uses']}=={n for n,ids in direct.items() if lid in ids}
        assert set(it['theorem_explanations'])=={r['claim_id'] for r in it['related_theorems']}
        for relation in it['related_theorems']:
            path=relation['via_local_ids']
            assert path[0] in direct[relation['claim_id'].split('/T')[-1]] and path[-1]==lid
            for x,y in zip(path,path[1:]):assert y in members[x]['depends_on']
    assert sum(len(c['depends_on']) for c in census['claims'])==32
    assert sum(len(it['related_theorems']) for it in census['interfaces'])==62
    for lid,m in members.items():
        n=int(lid[1:])
        assert m['source_kind']==('assumption' if n in {12,13,16,17,20} else 'source_passage' if n in {21,22} else 'definition')
    aux=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    assert len(aux['auxiliary_source_passages'])==7 and len(aux['source_issues'])==25
    assert aux['excluded_references']==[]
    assert set(aux['statement_resolution'])=={'shared',*direct}
    assert [e['page'] for e in members['D20']['evidence']]==[12,13]
    for item in list(members.values())+aux['auxiliary_source_passages']:
        assert all(1<=e['page']<=25 for e in item['evidence'])
    for it in census['interfaces']:
        assert '$' not in it['name']
        for keyword in it['source_keywords']:
            m=members[keyword['local_id']]
            texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])]
            assert any(keyword['source_text'] in s for s in texts)
    extraction=json.loads((ROOT/'interface-extraction.json').read_text())
    assert {m['local_id']:m for it in extraction['interfaces'] for m in it['members']}==members
    def has_span(n,font,fragment):
        return any(s['font']==font and fragment in s['text'] for block in pdf[n-1].get_text('dict')['blocks'] for line in block.get('lines',[]) for s in line['spans'])
    assert has_span(13,'EUFM10','M') and has_span(9,'CMSY10','R') and has_span(10,'CMSY10','D')
    assert has_span(3,'CMBX10','0') and has_span(2,'CMBX10','1') and has_span(8,'CMSY10','U')
    def check_strings(value):
        if isinstance(value, dict):
            for v in value.values(): check_strings(v)
        elif isinstance(value, list):
            for v in value: check_strings(v)
        elif isinstance(value, str):
            assert not any(ord(c)<32 and c != '\n' for c in value), repr(value)
    for name in ['theorem-inventory.json','source-passages.json','interface-extraction.json','ambient-prerequisites.json','unfinalized-census.json','ranked-interfaces.json']:
        check_strings(json.loads((ROOT/name).read_text()))
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
    pages = [1,2,3,4,6,7,8,9,10,11,12,13,25]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=26, path='evidence/revalidation/appendix-heading.png', sha256=digest(ROOT / 'evidence/revalidation/appendix-heading.png'), scope='Appendix roadmap and heading only; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 7 Theorems, 22 source entries, 62 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
