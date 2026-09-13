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
EXPECTED = {'theorem-inventory.json': 'd85c6082e27c748714910a2abb6f6dd680f7b462253f4f7c59d0aa1f43c7e83f', 'source-passages.json': '57ccc8a33421c901f88e68f3a5451e66f209c1f91b4bf5c09ac07848e784aa2a', 'interface-extraction.json': 'a689e2d5c77e48f54070dd5be595449278d6aa8932795633daffb6a91eb3dbad', 'ambient-prerequisites.json': 'cf269335a9ca7e07a1a8d95cf6a6b4b8edd4a97bc6ab067ba1198716a427bf05', 'unfinalized-census.json': 'f4e71de2ec1b1c8db22d18fa5aa7be78d13a6fe1a8ddf7df0096150d5bbfc850', 'ranked-interfaces.json': 'a23f57f1f8b17f44a0653d5ed72b981f003b84e5c65511302788948e75735bbe'}

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
    assert paper['version']=='arXiv:2210.01214v2, 15 February 2024' and entry['version']=='2210.01214v2.pdf'
    assert paper['source_url']=='https://arxiv.org/pdf/2210.01214v2' and entry['source_url']=='https://export.arxiv.org/pdf/2210.01214'
    ir = json.loads((ROOT / 'inventory-review.json').read_text())
    assert ir['status'] == 'complete' and ir['source_checked']
    assert ir['inventory_sha256'] == digest(ROOT / 'theorem-inventory.json')
    pdf = fitz.open(source)
    assert len(pdf) == paper['pdf_pages'] == entry['pdf_pages'] == 61
    first = ' '.join(pdf[0].get_text().upper().split())
    assert all(s in first for s in [paper['title'].upper(), 'CARSTEN H. CHONG', 'MARC HOFFMANN', 'YANGHUI LIU', 'MATHIEU ROSENBAUM', 'ARXIV:2210.01214V2'])
    assert paper['main_text_last_pdf_page'] == 56
    assert paper['main_text_boundary']['shared_page_with_appendix'] is True
    headings = []
    for n, page in enumerate(list(pdf)[:55], 1):
        assert (ROOT / f'evidence/page-{n:02}.txt').read_bytes().decode() == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans'])
                match = re.fullmatch(r'THEOREM (\d+)\.', text)
                if match:
                    headings.append((n, match[1]))
    assert headings == [(6, '2'), (8, '3'), (9, '4'), (12, '11')]
    boundary=pdf[55].get_text(clip=fitz.Rect(0,0,pdf[55].rect.width,146))
    assert '[58]' in boundary and 'APPENDIX' not in boundary
    assert (ROOT/'evidence/page-56-before-appendix.txt').read_bytes().decode()==boundary
    assert len(inv['claims']) == len(data['claims']) == 4
    for original, final in zip(inv['claims'], data['claims']):
        assert all(final[k] == v for k, v in original.items())
    claims = {c['claim_id'].split('/T')[-1]: c for c in data['claims']}
    members = {m['local_id']: m for x in data['interfaces'] for m in x['members']}
    local={1:[],2:[],3:[],4:[],5:[2,3,4],6:[5],7:[1,3],8:[7],9:[2,3,4],10:[9,4,5],11:[10,9],12:[11,4],13:[7],14:[13],15:[1,14],16:[14],17:[15,16],18:[17,14],19:[7],20:[19],21:[20,13,17],22:[20,18],23:[22,21,13,17],24:[21,23,13]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in v] for k,v in local.items()}
    direct={'2':{4,5,6},'3':{4,5,12},'4':{7,8},'11':{7,13,24}}
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    expected_reach={'2':{2,3,4,5,6},'3':{2,3,4,5,9,10,11,12},'4':{1,3,7,8},'11':{1,3,7,*range(13,25)}}
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
    assert reach['4'].isdisjoint({'D2','D4','D5','D12'})
    assert reach['11'].isdisjoint({'D2','D4','D5','D9','D10','D11','D12'})
    t={n:c['statement_original'] for n,c in claims.items()}
    b={lid:m['statement_original'] for lid,m in members.items()}
    assert r'\delta^{1/2}' in t['2'] and r'\delta^{1/2}' in t['3']
    assert r'\delta' not in t['4'] and r'\delta' not in t['11']
    assert r'\nu_0<\inf_{(H,\eta)\in\mathcal D}\eta^2\kappa_0(H)2^{2H}' in t['3']
    assert 'm_{opt}>m>1/(4H)-2H-1' in t['11']
    assert r'\mathcal E^n' in b['D5'] and 'non-empty interior' in b['D5']
    assert r'(0,3/4)\times(0,\infty)' in b['D7']
    assert r'\bar\varepsilon_m=\log' in b['D9'] and 'chi-square' in b['D9']
    assert r'6\operatorname{Var}(\bar\varepsilon_m)' in b['D11']
    assert r'\log\left[' in b['D12'] and r'\log_2' not in b['D12']
    assert 'when this set is empty' in b['D12'] and 'when this set is empty' not in b['D21']
    assert r'\widetilde d_{j,p,k,n}' in b['D19']
    assert r'2^{-j-p+1}\operatorname{Var}(\log\xi^2)' in b['D20']
    assert r'\widehat j_n=\left\lfloor\frac1{2\widehat H_n^{(0)}+1}\log_2n\right\rfloor' in b['D21']
    assert r'\sum_{a=2}^S' in b['D18']
    assert r'\{1,\ldots,2S\}^s' in b['D15'] and r'\{1,\ldots,S\}^{s_1}' in b['D16']
    assert r'\mathfrak W' in b['D15'] and r'\overline\sum_{b_1+b_2=2a}' in b['D17']
    assert r'\widehat\eta_n^c(\widehat H_n^{(m)},\widehat\eta_n^{(m-1)})' in b['D24']
    assert members['D14']['source_kind']=='condition'
    for item in list(claims.values()) + list(members.values()) + ambient['auxiliary_source_passages']:
        assert all(1 <= e['page'] <= 55 for e in item['evidence'])
        fragments = [item['statement_original']]
        for context in item.get('naming_context', []):
            assert all(1 <= e['page'] <= 55 for e in context['evidence'])
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
    assert counts==dict(theorems=4,interfaces=24,source_members=24,direct_theorem_uses=11,related_theorem_connections=32,unranked_auxiliary_passages=5)
    assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==22
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:
        assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Four full theorem bodies visually compared; independent enumeration of every admitted main-text page confirms labels 2,3,4,11. Main text ends above the Appendix A heading on page 56.',
        source_passages='All 24 original passages and five auxiliary passages reviewed against pages 1,5-12,30-31. Both complete estimator constructions, both minimax criteria, kappa formula (36), fraktur Gaussian integrals and overlined index sum are preserved.',
        dependencies='Independent checks cover all 11 direct uses and 32 related connections. General-model Theorems 4 and 11 do not inherit the piecewise-constant experiment, delta grid or coarse estimators. Kappa is an estimator dependency; Gaussian proof expansions and latent target energies are not imported into that graph.',
        names_and_highlights='Every interface has an original natural-language keyword or separately evidenced naming context and matching source highlights. Source headings distinguish models, conditions, original definitions inside lemmas and estimator constructions; no theorem is renamed as a Definition.',
        notation='Visual and PDF-font checks preserve Euler-script A/E/D, blackboard P, fraktur W, bold multi-indices, overlined sum, estimated squared coefficients and both sequential update indices. Natural log versus log_2 and all source indexing discrepancies are retained.',
        limits='Twenty-two notes record unresolved source domains, implicit ranges, log and square-root conventions, estimator index inconsistencies and excluded references. The census preserves the claimed statements and does not certify proofs.',
        reproduction='All six census artifacts rebuilt byte-for-byte in an empty directory. Both independent schema validations and the fixed local PDF hash check passed; rebuild does not renew source review.')
    write('evidence/manual-findings.json',findings)
    pages=[1,5,6,7,8,9,10,11,12,30,31]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    evidence.append(dict(page=56,path='evidence/page-56-boundary.png',before_main_text_end=True,sha256=digest(ROOT/'evidence/page-56-boundary.png'),note='Crop includes the reference endpoint and appendix heading only; no appendix body.'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json', dict(schema_version='statistical-paper-audit-v1', paper_id=PID,
        status='complete', audit_kind='source_review', completed_at=now,
        source=dict(pdf_path=str(source), source_url=paper['source_url'], version=paper['version'],
            pdf_sha256=SHA, pdf_pages=61, main_text_last_pdf_page=56, provenance_path='evidence/source-provenance.json'),
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
        registered_pdf_path=str(source), registered_pdf_sha256=SHA, registered_pdf_pages=61,
        source_version=paper['version'], registered_version_alias=entry['version'], registered_url_alias=entry['source_url'], checks={k: True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},
        reviewed_artifacts={n: digest(ROOT / n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},
        findings=findings, evidence=evidence, independent_validation=validation,
        reproduction_check=dict(path='evidence/rebuild-check.json', sha256=digest(ROOT / 'evidence/rebuild-check.json'))))
    write('checkpoint.json', dict(paper_id=PID, stage='complete', inventory_status='validated',
        census_status='validated', source_pdf_path=str(source), source_pdf_sha256=SHA,
        registered_source_review_path='registered-source-review.json', updated_at=now, remaining_work=None))
    print(json.dumps(counts))


if __name__ == '__main__':
    main()
