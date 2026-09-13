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
    assert len(pdf) == entry['pdf_pages'] == 75
    assert 'arXiv:2212.09201v3' in pdf[0].get_text()
    assert all(s in pdf[0].get_text().lower() for s in ['omar hagrass','bharath k. sriperumbudur','bing li','1 may 2024'])
    paper=inv['papers'][0]
    assert paper['version']=='arXiv:2212.09201v3'
    assert paper['source_url']=='https://arxiv.org/pdf/2212.09201v3'
    assert paper['title'].lower() in ' '.join(pdf[0].get_text().split()).lower()
    assert digest(source)==paper['pdf_sha256']
    assert paper['main_text_last_pdf_page']==55
    assert paper['main_text_boundary']['shared_page_with_appendix'] is True
    end=601.6620483398438
    assert 'Technical results' in pdf[54].get_text(clip=fitz.Rect(0,end,pdf[54].rect.width,end+20))
    assert 'Proofs' in pdf[31].get_text(clip=fitz.Rect(0,230,pdf[31].rect.width,260))
    headings=[]; mentions=[]
    for n in range(1,56):
        page=pdf[n-1]
        clip=fitz.Rect(0,0,page.rect.width,end) if n==55 else page.rect
        assert (ROOT/f'evidence/revalidation/page-{n:02}.txt').read_bytes().decode('utf8')==page.get_text(clip=clip)
        for block in page.get_text('dict',clip=clip)['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans']).strip()
                match=re.match(r'^Theorem\s+(\d+\.\d+)',text)
                if match:(headings if line['spans'][0]['font']=='CMBX10' else mentions).append((n,match[1]))
    assert headings==[(7,'3.1'),(8,'3.2'),(12,'4.1'),(13,'4.2'),(14,'4.3'),(17,'4.6'),(18,'4.7'),(20,'4.10'),(20,'4.11'),(22,'4.12')]
    assert mentions==[(22,'4.11')]
    assert [c['claim_id'] for c in inv['claims']]==[PID+'/T'+n for _,n in headings]
    for claim,(page,n) in zip(inv['claims'],headings):
        assert [e['page'] for e in claim['evidence']]==({'4.3':[14,15],'4.11':[20,21],'4.12':[22,23]}.get(n,[page]))
    for old,new in zip(inv['claims'],census['claims']):
        assert all(new[k]==v for k,v in old.items())
    members={m['local_id']:m for it in census['interfaces'] for m in it['members']}
    assert len(members)==len(census['interfaces'])==32
    direct={
        '3.1':{2,5,11,33,9},'3.2':{2,9,6,11},'4.1':{2,19,17,18},
        '4.2':{2,21,22,19,15,25,9,17},'4.3':{2,21,22,23,24,26,17,11,33,15,25,19,9},
        '4.6':{2,19,29},'4.7':{2,21,22,23,24,26,17,11,33,15,25,19,9,29},
        '4.10':{2,19,29,30},'4.11':{2,21,22,23,24,26,17,33,11,9,15,19,29,30},
        '4.12':{2,21,22,23,24,26,17,33,31,9,15,30,32}}
    direct={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    assert {c['claim_id'].split('/T')[-1]:set(c['depends_on']) for c in census['claims']}==direct
    expected_reach={
        '3.1':{1,2,3,4,5,7,8,9,10,11,13,33},
        '3.2':{1,2,3,6,7,8,9,10,11,13,33},
        '4.1':{1,2,3,7,13,15,17,18,19},
        '4.2':{1,2,3,7,8,9,13,15,16,17,18,19,21,22,25},
        '4.3':{1,2,3,7,8,9,10,11,13,15,16,17,18,19,21,22,23,24,25,26,33},
        '4.6':{1,2,3,7,13,15,17,18,19,27,29},
        '4.7':{1,2,3,7,8,9,10,11,13,15,16,17,18,19,21,22,23,24,25,26,27,29,33},
        '4.10':{1,2,3,7,13,15,17,18,19,27,29,30},
        '4.11':{1,2,3,7,8,9,10,11,13,15,17,18,19,21,22,23,24,26,27,29,30,33},
        '4.12':{1,2,3,7,8,9,10,13,15,17,18,19,21,22,23,24,26,27,29,30,31,32,33}}
    expected_reach={n:{f'D{i}' for i in ids} for n,ids in expected_reach.items()}
    expected_edges={1:[],2:[],3:[],4:[3],5:[1,4],6:[1],7:[3],8:[7],9:[8,7,2],10:[],11:[8,10,33],12:[],13:[],14:[8,12,13],15:[7,3],16:[15],17:[1,15,3],18:[17,15],19:[13,18,17],21:[],22:[],23:[],24:[],25:[16,15],26:[],27:[17,19],28:[27],29:[27],30:[],31:[8,10,33],32:[19,29,30],33:[8,13]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in ids] for k,ids in expected_edges.items()}
    for it in census['interfaces']:
        lid=it['members'][0]['local_id']
        assert {r['claim_id'].split('/T')[-1] for r in it['related_theorems']}=={n for n,ids in expected_reach.items() if lid in ids}
        assert {u['claim_id'].split('/T')[-1] for u in it['central_claim_uses']}=={n for n,ids in direct.items() if lid in ids}
        for relation in it['related_theorems']:
            path=relation['via_local_ids']
            assert path[0] in direct[relation['claim_id'].split('/T')[-1]] and path[-1]==lid
            for x,y in zip(path,path[1:]):assert y in members[x]['depends_on']
    assert sum(len(c['depends_on']) for c in census['claims'])==82
    assert sum(len(it['related_theorems']) for it in census['interfaces'])==159
    assert {it['members'][0]['local_id'] for it in census['interfaces'] if not it['related_theorems']}=={'D12','D14','D28'}
    for lid,m in members.items():
        n=int(lid[1:])
        assert m['source_kind']==('assumption' if n in {2,21,22,23,24,26} else 'source_passage' if n in {1,12} else 'definition')
    aux=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    assert len(aux['auxiliary_source_passages'])==10 and len(aux['source_issues'])==34
    assert aux['excluded_references']==[]
    assert set(aux['statement_resolution'])=={'shared',*direct}
    for item in list(members.values())+aux['auxiliary_source_passages']:
        assert all(1<=e['page']<55 for e in item['evidence'])
    for it in census['interfaces']:
        assert '$' not in it['name']
        for keyword in it['source_keywords']:
            m=members[keyword['local_id']]
            texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])]
            assert any(keyword['source_text'] in s for s in texts)
    assert members['D8']['naming_context'][0]['evidence'][0]['page']==3
    assert members['D10']['naming_context'][0]['evidence'][0]['page']==3
    for lid in ['D21','D22','D23','D24']:assert members[lid]['naming_context'][0]['evidence'][0]['page']==9
    extraction=json.loads((ROOT/'interface-extraction.json').read_text())
    assert {m['local_id']:m for it in extraction['interfaces'] for m in it['members']}==members
    def has_span(n,font,fragment):
        return any(s['font']==font and fragment in s['text'] for block in pdf[n-1].get_text('dict')['blocks'] for line in block.get('lines',[]) for s in line['spans'])
    assert has_span(7,'MSBM10','X') and has_span(6,'EUFM10','I')
    assert has_span(9,'CMSY10','B') and has_span(17,'dsrom10','1')
    assert has_span(12,'CMMIB10','H') and has_span(12,'CMBX10','1')
    correction=audit['registered_source_correction']
    assert digest(ROOT/correction['previous_audit_path'])==correction['previous_audit_sha256']
    historical=json.loads((ROOT/'review-history/before-naming-context-escape-correction/ranked-interfaces.json').read_text())
    assert historical['claims']==census['claims']
    historical_members={m['local_id']:m for it in historical['interfaces'] for m in it['members']}
    fixed=set()
    for lid,m in members.items():
        expected=json.loads(json.dumps(historical_members[lid]))
        for ctx in expected.get('naming_context',[]):
            old=ctx['text']
            ctx['text']=old.replace('\r',r'\r').replace('\t',r'\t').replace('\a',r'\a').replace('\b',r'\b')
            if ctx['text']!=old:fixed.add(lid)
        assert expected==m,lid
    assert fixed=={'D8','D10','D16','D21','D22','D23','D24','D30'}
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
    pages = list(range(1,24))+[32,55]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=55, path='evidence/revalidation/appendix-heading.png', sha256=digest(ROOT / 'evidence/revalidation/appendix-heading.png'), scope='Heading-only crop; appendix body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 10 Theorems, 32 source entries, 159 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
