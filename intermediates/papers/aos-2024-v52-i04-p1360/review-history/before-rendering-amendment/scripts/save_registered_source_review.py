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
EXPECTED = {'theorem-inventory.json': '716c67c5f78193d83b1598aa8ac0db7d0a1a85df1b9da1ae85378af2e0700eb7', 'source-passages.json': 'b2fcf178c15e5fbf59b4701a3f45d132279339cb111b9a5721be4732603f0f55', 'interface-extraction.json': '41ad3e1eef4d7495b784d137fa6c6ac2b621cfb560cb2e70358a9b4f31dfcd03', 'ambient-prerequisites.json': 'e6f9fe71ce241d99af46f32f5205a3ce41e7e172a8a594c764e12940c0fab266', 'unfinalized-census.json': '4879b7993b52288cf9cfc99efb456aec30a46a69568b41e9fabf9669d266a6db', 'ranked-interfaces.json': 'b0a94849cda9e09f88a5421a2fc5d5e24fa0a43c16ef5ac74e37889d1bec1f6e'}

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
    assert paper['version']=='arXiv:2111.06859v1, 12 November 2021' and entry['version']=='2111.06859v1.pdf'
    assert paper['source_url']=='https://arxiv.org/pdf/2111.06859v1' and entry['source_url']=='https://export.arxiv.org/pdf/2111.06859'
    ir = json.loads((ROOT / 'inventory-review.json').read_text())
    assert ir['status'] == 'complete' and ir['source_checked']
    assert ir['inventory_sha256'] == digest(ROOT / 'theorem-inventory.json')
    pdf = fitz.open(source)
    assert len(pdf) == paper['pdf_pages'] == entry['pdf_pages'] == 46
    first = ' '.join(pdf[0].get_text().upper().split())
    assert all(s in first for s in [paper['title'].upper(), 'SHENGYI HE', 'HENRY LAM', 'ARXIV:2111.06859V1'])
    assert paper['main_text_last_pdf_page'] == 22
    assert paper['main_text_boundary']['shared_page_with_appendix'] is True
    headings = []
    for n, page in enumerate(list(pdf)[:21], 1):
        assert (ROOT / f'evidence/page-{n:02}.txt').read_bytes().decode() == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans'])
                match = re.match(r'^Theorem (\d+) \(', text)
                if match: assert line['spans'][0]['font']=='CMBX10'
                if match:
                    headings.append((n, match[1]))
    assert headings == [(6, '1'), (7, '2'), (9, '3'), (10, '4'), (11, '5'), (12, '6'), (14, '7')]
    boundary=pdf[21].get_text(clip=fitz.Rect(0,0,pdf[21].rect.width,201.90811157226562))
    assert '56(2):254' in boundary and 'APPENDIX' not in boundary
    assert (ROOT/'evidence/page-22-before-appendix.txt').read_bytes().decode()==boundary
    assert len(inv['claims']) == len(data['claims']) == 7
    for original, final in zip(inv['claims'], data['claims']):
        assert all(final[k] == v for k, v in original.items())
    claims = {c['claim_id'].split('/T')[-1]: c for c in data['claims']}
    members = {m['local_id']: m for x in data['interfaces'] for m in x['members']}
    local={1:[],2:[1],3:[],4:[1],5:[1],6:[1],7:[1,3,4],8:[1,3,5],9:[1,3,4],10:[6,3],11:[],12:[],13:[2],14:[],15:[12],16:[1,3],17:[],18:[1,17],19:[],20:[],21:[17],22:[17],23:[22,1],24:[7,8,9,10,11,12],25:[26],26:[12,7,8,9,10],27:[26,12,8],28:[26,25,27,24],29:[]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in v] for k,v in local.items()}
    direct={'1':{2,3,7,11,16},'2':{2,12,13,14,15,7,8,9,10,11},'3':{17,18,19,20,7,8,9,10,11},'4':{17,18,19,20,21,7,8,9,10,11},'5':{22,23,7,8,9,10,11},'6':{2,12,13,14,15,24,28,7,8,9,10},'7':{2,3,7,8,10,29}}
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    expected_reach={'1':{1,2,3,4,7,11,16},'2':set(range(1,16)),'3':{1,3,4,5,6,7,8,9,10,11,17,18,19,20},'4':{1,3,4,5,6,7,8,9,10,11,17,18,19,20,21},'5':{1,3,4,5,6,7,8,9,10,11,17,22,23},'6':{*range(1,16),24,25,26,27,28},'7':{1,2,3,4,5,6,7,8,10,29}}
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
    assert all('D2' not in reach[n] for n in ['3','4','5'])
    assert {'D9','D11','D16','D18','D21','D23','D28'}.isdisjoint(reach['7'])
    assert 'D18' not in reach['5'] and {'D22','D23'}.isdisjoint(reach['3']|reach['4'])
    assert {'D24','D25','D26','D27','D28'} <= reach['6']
    t={n:c['statement_original'] for n,c in claims.items()}
    b={lid:m['statement_original'] for lid,m in members.items()}
    assert 'holds uniformly' in t['1'] and 'even polynomial when $j$ is odd' in t['1']
    assert all(z in t['2'] for z in [r'K\ge r+3',r'K\ge4','The same result holds',r'$r+1$ times differentiable'])
    assert [e['page'] for e in claims['2']['evidence']]==[7,8]
    assert [e['page'] for e in claims['4']['evidence']]==[10,11]
    assert r'as $n\to0$' in t['3'] and r'$r$ times differentiable' in t['3'] and r'P(-q' not in t['3']
    assert t['4'].count(r'\begin{cases}')==2 and all(z in t['4'] for z in ['(i)','(ii)','(iii)','(iv)',r'E_{P,\lambda}\tau^{r+1}'])
    assert r'E[T_2-T_1]>0' in t['5'] and 'The same result holds' in t['5']
    assert 'conditions of Theorem 2 hold with $r=2$' in t['6'] and 'Algorithm 1' in t['6']
    assert r'Fix $n$ and let $K\to\infty$' in t['7'] and r'W_{SB}' not in t['7']
    assert t['7'].count(r'\sqrt{nE(\psi(\widehat P_1)-\psi)^2}/\sigma')==2
    assert 'i.i.d.' not in b['D1'] and 'i.i.d.' in b['D2']
    assert r'\psi_0' in b['D10']
    assert r'\widehat P_{(i)}' in b['D6'] and r'K\psi(\widehat P)-(K-1)' in b['D6']
    assert r'0<\delta<1' in b['D18'] and r'n^\delta' in b['D18']
    assert r'\alpha(n):=\sigma(' in b['D19'] and members['D19']['source_heading']=='Definition 1 (Mixing coefficient)'
    assert members['D20']['source_heading']=='Definition 2 (Harris recurrence)'
    assert b['D21'].count(r'\begin{cases}')==2
    assert r'\sum_{k=T_i}^{T_{i+1}-1}' in b['D22'] and r'Q_i:=(Y_i,T_{i+1}-T_i)' in b['D23']
    assert r'\frac{E_{\overline P}[Q^{(1)}]}{E_{\overline P}[Q^{(2)}]}' in b['D23']
    assert r'cn^{-1}+O(n^{-3/2})' in b['D24']
    assert r'\phi_\Sigma(x)\left[1+\frac16' in b['D25'] and r'\frac1{72}\chi_{ijk}\chi_{lmn}' in b['D25']
    assert r'18\sigma^{i\alpha}\sigma^{l\beta}\sigma^{jm}\sigma^{kn}' in b['D25']
    assert 'up to order 3' in b['D26'] and 'up to order 4' in b['D26']
    assert r'\stackrel{i.i.d.}{\sim}N(0,\Sigma)' in b['D26']
    assert r'b_2=[v,A_0,A_0,A_0]' in b['D27']
    assert r'\lambda\prime' not in b['D27'] and r'[u,B_i]2\left(' in b['D27']
    assert r'-b_1\frac\lambda c' in b['D28']
    assert r'F_+=\frac{q\sqrt{E_2}}{\sqrt{K(K-1)}}-\sum_{i=2}^d u_iA_{0,i}' in b['D28']
    assert r'y_{xx}^{(-)}=\left.-(F_{xx}+2F_{xy}y_x)/F_y' in b['D28']
    assert r"\phi'_{\tilde\sigma_0}(F_--\mu)" in b['D28']
    assert r'\right]\\' in b['D28'] and r'(p_1(x(A)))' in b['D28']
    assert all(z in b['D28'] for z in ['2:','3:','4:','5:','Output:',r'\tilde\sigma_0=',r'\mu=\sigma_{01}'])
    assert members['D29']['source_kind']=='source_passage'
    for item in list(claims.values()) + list(members.values()) + ambient['auxiliary_source_passages']:
        assert all(1 <= e['page'] <= 21 for e in item['evidence'])
        fragments = [item['statement_original']]
        for context in item.get('naming_context', []):
            assert all(1 <= e['page'] <= 21 for e in context['evidence'])
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
    assert counts==dict(theorems=7,interfaces=29,source_members=29,direct_theorem_uses=58,related_theorem_connections=94,unranked_auxiliary_passages=9)
    assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==30
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:
        assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Seven complete original theorem statements compared with PDF pages 6-12 and 14, including the page continuations of Theorems 2 and 4. Independent bold-heading enumeration covers all admitted main-text pages. References end above Appendix A on page 22.',
        source_passages='All 29 supporting passages and nine auxiliary passages compared with pages 4-14. The four statistic formulas, empirical substitutions, named mixing and Harris definitions, complete split-process construction, regenerative ratios, full Algorithm 1, equation (7) and main-text sectioning coefficients are preserved.',
        dependencies='Independent graph reconstruction checks all 58 direct uses and 94 related connections. Raw iid observations do not propagate into Theorems 3-5. Theorem 5 uses cycle pairs rather than gaps; Theorem 6 inherits Theorem 2 at r=2 and all algorithm inputs. Theorem 7 has no SB or Student-law dependency through the extracted statistic definitions.',
        names_and_highlights='Each interface has an original natural-language term or separately evidenced naming context and source-backed highlights. Original Definition 1 and Definition 2 labels are retained. Every related theorem has a same-paper explanation with the correct sampling substitution or changed asymptotic regime.',
        notation='Visual checks preserve the two variance centers, psi_0 in W_SJ, scalar versus multivariate Cramer conditions, barred coefficient families, different cycle rewards and moment orders, full cumulant contractions and every step of Algorithm 1. A high-resolution crop verifies sigma outside the square roots in Theorem 7; the inline 2 in lambda-prime is multiplication.',
        limits='Thirty source notes preserve the n-to-zero limit, sigma/alpha alias, unspecified measure/kernel conventions, unexplained algorithm c, negative-side formulas, absent plus sign, density-weighted polynomial terminology and cubic v contraction. Appendix-only formulas remain unresolved. The census does not certify proofs or executable unbiasedness.',
        reproduction='All six content artifacts regenerated byte-for-byte in an empty directory. Independent source hash, graph, math-fragment and schema checks passed. A rebuild does not perform or renew source review.')
    write('evidence/manual-findings.json',findings)
    pages=[1,4,5,6,7,8,9,10,11,12,13,14]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    evidence.append(dict(page=22,path='evidence/page-22-boundary.png',before_main_text_end=True,sha256=digest(ROOT/'evidence/page-22-boundary.png'),note='Crop includes the reference endpoint and appendix heading only; no appendix body.'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json', dict(schema_version='statistical-paper-audit-v1', paper_id=PID,
        status='complete', audit_kind='source_review', completed_at=now,
        source=dict(pdf_path=str(source), source_url=paper['source_url'], version=paper['version'],
            pdf_sha256=SHA, pdf_pages=46, main_text_last_pdf_page=22, provenance_path='evidence/source-provenance.json'),
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
        registered_pdf_path=str(source), registered_pdf_sha256=SHA, registered_pdf_pages=46,
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
