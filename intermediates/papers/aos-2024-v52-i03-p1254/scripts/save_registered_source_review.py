"""Record the completed source-content review, with independently checked invariants.

Expected hashes pin the manually inspected content. A rebuild alone does not
perform or renew source review; changed content must be reviewed again.
"""
import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import fitz
from save_inventory import PID, REPO, ROOT, SHA

SKILL = Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': 'c0cd96dbcc6c68517fa98ca726e908b580f6c63512ad112300bf79c8c46ef8ef', 'source-passages.json': '256a3aef95866ca2ebf8725a8fd78d1a336dfc9f2ba25735d52435c6d758ddb8', 'interface-extraction.json': '5d720498bf297aeba4bb6fc03b7285b12f439c5864efb3e03ed34b0ff7222434', 'ambient-prerequisites.json': 'e50cf5fc86005a683c9b40008c83164afac13312f968160a924970aa720b80b7', 'unfinalized-census.json': '4c751469fd6e757c40b309bc9a07eea89e4bd56f8df479d20b9b30e8a69bec9c', 'ranked-interfaces.json': 'f46a4cd6b987835d4437f29179fd533aa6b600e95c9e19a54d8e5d12d4222f6c'}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def main():
    for name, sha in EXPECTED.items():
        assert digest(ROOT / name) == sha, ('Re-review changed artifact', name)
    source = Path(subprocess.check_output(
        [sys.executable, str(REPO / 'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    register = json.loads((REPO / 'corpus/aos/2024/local-pdf-manifest.json').read_text())
    entry = next(x for x in register['papers'] if x['paper_id'] == PID)
    assert digest(source) == entry['sha256'] == SHA
    inv = json.loads((ROOT / 'theorem-inventory.json').read_text())
    data = json.loads((ROOT / 'ranked-interfaces.json').read_text())
    ambient = json.loads((ROOT / 'ambient-prerequisites.json').read_text())
    paper = inv['papers'][0]
    assert paper['version'] == entry['version'] and paper['source_url'] == entry['source_url']
    ir = json.loads((ROOT / 'inventory-review.json').read_text())
    assert ir['status'] == 'complete' and ir['source_checked']
    assert ir['inventory_sha256'] == digest(ROOT / 'theorem-inventory.json')
    pdf = fitz.open(source)
    assert len(pdf) == paper['pdf_pages'] == entry['pdf_pages'] == 22
    first = ' '.join(pdf[0].get_text().upper().split())
    assert all(s in first for s in [paper['title'].upper(), 'HUIQIN LI', 'GUANGMING PAN', 'YANQING YIN', 'WANG ZHOU', '10.1214/24-AOS2392'])
    assert paper['main_text_last_pdf_page'] == 22
    assert paper['main_text_boundary']['shared_page_with_appendix'] is False
    headings = []
    for n, page in enumerate(pdf, 1):
        assert (ROOT / f'evidence/page-{n:02}.txt').read_bytes().decode() == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans'])
                match = re.fullmatch(r'THEOREM (\d+\.\d+) \([^\n]+\)\.', text)
                if match:
                    headings.append((n, match[1]))
    assert headings == [(6, '2.1'), (7, '2.2'), (10, '2.3'), (13, '3.1')]
    assert 'SUPPLEMENTARY MATERIAL' in pdf[20].get_text() and '[19]' in pdf[21].get_text()
    assert len(inv['claims']) == len(data['claims']) == 4
    for original, final in zip(inv['claims'], data['claims']):
        assert all(final[k] == v for k, v in original.items())
    claims = {c['claim_id'].split('/T')[-1]: c for c in data['claims']}
    members = {m['local_id']: m for x in data['interfaces'] for m in x['members']}
    local={1:[],2:[1],3:[1],4:[],5:[4],6:[5],7:[],8:[6],9:[],10:[9,6],11:[6,7],12:[],13:[1,4,7,8],14:[],15:[],16:[1,15],17:[13,12,3,2],18:[6,7,1,17],19:[4,8],20:[4,8],21:[5,8],22:[21],23:[13,19,20,10],24:[22,21,8]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in v] for k,v in local.items()}
    direct={'2.1':{1,2,3,6,7,10,11,12,13,16},'2.2':{6,7,14,17,10,11,12,13},'2.3':{6,7,10,11,12,13,17,18,19,20},'3.1':{22,24,23,12,10,11,13}}
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    expected_reach={'2.1':set(range(1,14))|{15,16},'2.2':set(range(1,15))|{17},'2.3':set(range(1,14))|{17,18,19,20},'3.1':{1,4,5,6,7,8,9,10,11,12,13,19,20,21,22,23,24}}
    reach={}
    for n,c in claims.items():
        seen,stack=set(),list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in seen:
                seen.add(lid)
                stack.extend(members[lid]['depends_on'])
        reach[n]=seen
    assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected_reach.items()}
    t={n:c['statement_original'] for n,c in claims.items()}
    b={lid:m['statement_original'] for lid,m in members.items()}
    assert r'-\frac{1-y}{z}+ym\in\mathbb C^+' in t['2.1']
    assert 'F^{c,H}' in t['2.2'] and 'a>0' in t['2.2']
    assert 'nonoverlapping' in t['2.3'] and len(claims['2.3']['evidence'])==2
    assert r'\underline m' in t['2.3'] and r'\bar m' not in t['2.3']
    assert r'\mathbb T_n^{(2)}' in t['2.3'] and r'\mathcal{II}' in t['2.3']
    assert r'\mathcal T_L' in t['3.1'] and r'p/n\in(0,1)' in t['3.1']
    assert r'a_{\mathbb P,\boldsymbol\Sigma}' in t['3.1'] and r'a_{\mathbb P,\Sigma}' in t['3.1']
    assert r'\mathbf S_n=\frac1n' in b['D6']
    assert r'\mathbb P^{(5)}=(\mathbb P^{(4)}-3(\mathbb P^{(2)})^2)' in b['D8']
    assert r'\nu_4' in b['D10'] and members['D10']['source_kind']=='assumption'
    assert r'(\boldsymbol\Sigma_n\Theta_n)' in b['D13']
    assert r'o(n^{-\ell})' in b['D14'] and r'o(n^{-\ell})' in b['D15']
    assert r'\|F^{\mathbf A_n}-F\|_\infty' in b['D16']
    assert r'+y\int' in b['D17'] and r'\underline m_n^0' in b['D17']
    assert r'L^c(f,\mathbf S_n\Theta_n)=\int' in b['D18']
    assert b['D19'].count(r'\operatorname{tr}')==8 and b['D20'].count(r'\operatorname{tr}')==6
    assert [e['page'] for e in members['D20']['evidence']]==[5,6]
    assert 'missing probabilities are known' in b['D21']
    assert r'p^{-1}\mathcal I_2' in b['D23'] and r'p^{-1}\mathcal{II}' in b['D23']
    assert r'\mathcal T_F=\operatorname{tr}' in b['D24'] and r'\mathbb P^{(2)}' in b['D24']
    for item in list(claims.values()) + list(members.values()) + ambient['auxiliary_source_passages']:
        assert all(1 <= e['page'] <= 22 for e in item['evidence'])
        fragments = [item['statement_original']]
        for context in item.get('naming_context', []):
            assert all(1 <= e['page'] <= 22 for e in context['evidence'])
            fragments.append(context['text'])
        for text in fragments:
            assert not re.search(r'[\u4e00-\u9fff]', text)
            assert not any(ord(ch) < 32 and ch != '\n' for ch in text)
            assert text.count('$') % 2 == 0 and text.count(r'\[') == text.count(r'\]')
            for display, inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$', text, re.S):
                depth = 0
                for brace in re.findall(r'(?<!\\)[{}]', display + inline):
                    depth += 1 if brace == '{' else -1
                    assert depth >= 0
                assert depth == 0
    for x in data['interfaces']:
        lid = x['members'][0]['local_id']
        assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']} == {n for n in claims if lid in reach[n]}
        assert set(x['theorem_explanations']) == {r['claim_id'] for r in x['related_theorems']}
        assert x['related_theorems'] and '$' not in x['name']
        for m in x['members']:
            own = m['statement_original'] + ' ' + m['local_label']
            assert any(s in own for s in m['highlight_symbols'] + m['highlight_phrases'])
        for keyword in x['source_keywords']:
            m = members[keyword['local_id']]
            assert any(keyword['source_text'] in text for text in [m['statement_original']] + [c['text'] for c in m.get('naming_context', [])])
    counts=dict(theorems=len(inv['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_source_passages']))
    assert counts==dict(theorems=4,interfaces=24,source_members=24,direct_theorem_uses=35,related_theorem_connections=64,unranked_auxiliary_passages=5)
    assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==20
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:
        assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='All four full theorem statements visually compared with the published PDF. Independent enumeration covers all 22 pages; the continuation of Theorem 2.3 onto page 11 is retained.',
        source_passages='All 24 source passages visually compared on pages 3-7 and 10-13; five ambient passages checked on pages 2,3,5,12. I_2 contains eight trace terms and II contains six across the page-5/6 boundary. Lemma domain conditions are separately archived.',
        dependencies='All 35 direct and 64 related theorem connections reviewed, with independent local-graph and reach checks. A-D links inherited by Theorems 2.2 and 3.1 are explicitly described as section context. No epsilon-net, proof resolvent decomposition, simulation design or external supplement is imported.',
        names_and_highlights='Every title is a source natural-language term or acronym; naming contexts are separately archived with source pages. Every one of the 24 members has a source-matching selector. Original assumptions and lemma/corollary definitions retain their source headings.',
        notation='Font and visual checks distinguish underlined companion m, kappa, calligraphic I/II and T, blackboard P/T, and bold/plain Sigma/Theta. All source scale, parameter-name and domain issues remain separate from original statements.',
        limits='Twenty source notes preserve unresolved normalization, c/y aliases, auxiliary matrix domain, existence of analytic-parameter limits and test-statistic domains. This is source and dependency review, not proof certification.',
        reproduction='All six content artifacts rebuilt byte-for-byte in an empty directory, independently schema-validated and pinned to the fixed registered PDF hash.')
    write('evidence/manual-findings.json',findings)
    pages=[1,2,3,4,5,6,7,10,11,12,13,21,22]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json', dict(schema_version='statistical-paper-audit-v1', paper_id=PID,
        status='complete', audit_kind='source_review', completed_at=now,
        source=dict(pdf_path=str(source), source_url=paper['source_url'], version=paper['version'],
            pdf_sha256=SHA, pdf_pages=22, main_text_last_pdf_page=22, provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']], printed_label_check=headings,
            method='Independent actual-heading enumeration and visual comparison of all complete theorem bodies.',
            excluded_result_types=['Lemma','Proposition','Corollary','Remark'], appendix_material_used=False),
        counts=counts, validation=dict(status='passed', validator=str(SKILL / 'validate_census.py'), checks=list(findings.values())),
        artifacts={n: dict(path=n, sha256=digest(ROOT / n)) for n in [*EXPECTED, 'inventory-review.json']},
        source_notes=ambient['source_issues'], unresolved_source_references=ambient['excluded_references'],
        ambient_resolution=ambient['statement_resolution'], evidence=evidence,
        review_limits=['Source transcription and statement-dependency review, not proof certification.', 'External supplement and appendix bodies excluded.']))
    write('registered-source-review.json', dict(schema_version='registered-paper-source-review-v1',
        paper_id=PID, status='complete', method='source_content_revalidation', reviewed_at=now,
        registered_pdf_path=str(source), registered_pdf_sha256=SHA, registered_pdf_pages=22,
        source_version=paper['version'], checks={k: True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},
        reviewed_artifacts={n: digest(ROOT / n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},
        findings=findings, evidence=evidence, independent_validation=validation,
        reproduction_check=dict(path='evidence/rebuild-check.json', sha256=digest(ROOT / 'evidence/rebuild-check.json'))))
    write('checkpoint.json', dict(paper_id=PID, stage='complete', inventory_status='validated',
        census_status='validated', source_pdf_path=str(source), source_pdf_sha256=SHA,
        registered_source_review_path='registered-source-review.json', updated_at=now, remaining_work=None))
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
