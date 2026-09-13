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
EXPECTED = {'theorem-inventory.json': '08ca1d4906aaa37639a93e0fe3679e486c0ddc7fb9bd25402f28e3c2d927cdf4', 'source-passages.json': '551097e157d7ad3921cb2847c12c2d1b859839fc22a22e25dde143ad87c158e5', 'interface-extraction.json': 'fcec4930f2092de7f350d4bce8f998080bcfb464f7d1e5752303c3f17513e36b', 'ambient-prerequisites.json': '7a91a0abf208124b2c44d501bc2b05afa48e4e5e2ba6d45f794c0e572585546c', 'unfinalized-census.json': 'c49f848eabeb190a781f069a08955e2ee2089275356bc4cf5e9c02deaf8309f3', 'ranked-interfaces.json': '7688b23ebd4cb043480b3af9087f00b4c0539cd84b4821b07bd62938b86f7f70'}

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
    assert paper['version']=='arXiv:2211.02496v2, 25 July 2024' and entry['version']=='2211.02496v2.pdf'
    assert paper['source_url']=='https://arxiv.org/pdf/2211.02496v2' and entry['source_url']=='https://export.arxiv.org/pdf/2211.02496'
    ir = json.loads((ROOT / 'inventory-review.json').read_text())
    assert ir['status'] == 'complete' and ir['source_checked']
    assert ir['inventory_sha256'] == digest(ROOT / 'theorem-inventory.json')
    pdf = fitz.open(source)
    assert len(pdf) == paper['pdf_pages'] == entry['pdf_pages'] == 42
    first = ' '.join(pdf[0].get_text().upper().split())
    assert all(s in first for s in [paper['title'].upper(), 'RANDOLF ALTMEYER', 'ANTON TIEPNER', 'MARTIN WAHL', 'ARXIV:2211.02496V2'])
    assert paper['main_text_last_pdf_page'] == 24
    assert paper['main_text_boundary']['shared_page_with_appendix'] is True
    headings = []
    for n, page in enumerate(list(pdf)[:23], 1):
        assert (ROOT / f'evidence/page-{n:02}.txt').read_bytes().decode() == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans'])
                match = re.fullmatch(r'THEOREM (\d+\.\d+)\.', text)
                if match:
                    headings.append((n, match[1]))
    assert headings == [(6, '2.3'), (7, '3.1'), (8, '3.2'), (9, '4.1'), (10, '4.3')]
    boundary=pdf[23].get_text(clip=fitz.Rect(0,0,pdf[23].rect.width,492.7498779296875))
    assert 'Theorem 4.1 follow' in boundary and 'APPENDIX' not in boundary
    assert (ROOT/'evidence/page-24-before-appendix.txt').read_bytes().decode()==boundary
    assert len(inv['claims']) == len(data['claims']) == 5
    for original, final in zip(inv['claims'], data['claims']):
        assert all(final[k] == v for k, v in original.items())
    claims = {c['claim_id'].split('/T')[-1]: c for c in data['claims']}
    members = {m['local_id']: m for x in data['interfaces'] for m in x['members']}
    local={1:[],2:[1],3:[2],4:[3],5:[4,3],6:[1],7:[6],8:[5,7],9:[5,7,2],10:[9],11:[10,8,9],12:[2,7],13:[2,7],14:[2],15:[7],16:[4,3,2,6,15],17:[2,3],18:[],19:[18],20:[],21:[19,18],22:[1],23:[],24:[1],25:[6]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in v] for k,v in local.items()}
    direct={'2.3':{13,14,15,16,17,12,10,11,7,2},'3.1':{18,19,20},'3.2':{18,19,20,21},'4.1':{22,23,24,25,8},'4.3':{22,23,24,25,8,9}}
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    expected_reach={'2.3':set(range(1,18)),'3.1':{18,19,20},'3.2':{18,19,20,21},'4.1':{*range(1,9),22,23,24,25},'4.3':{*range(1,10),22,23,24,25}}
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
    assert reach['3.1'].isdisjoint({f'D{i}' for i in range(1,18)})
    assert reach['3.2'].isdisjoint({f'D{i}' for i in range(1,18)})
    for n in ['4.1','4.3']:
        assert reach[n].isdisjoint({f'D{i}' for i in range(10,22)})
    t={n:c['statement_original'] for n,c in claims.items()}
    b={lid:m['statement_original'] for lid,m in members.items()}
    assert r'\rho_\delta\mathcal I_\delta\rho_\delta' in t['2.3']
    assert r'M^{1/2}\delta^{1-n_i}' in t['2.3'] and 'or, equivalently' in t['2.3']
    assert t['2.3'].count(r'\|K\|_{L^2(\mathbb R^d)}^2') == 2
    assert all(s in t['3.1'] for s in [r'\|(-A)^{1/2}h(0)\|',r'\|(-A)^{1/2}h(T)\|',r'T\ge1'])
    assert all(s in t['3.2'] for s in [r'K_M\in\mathcal D(A)',r'H_{X_K}=H^M',r'3\|G^{-1}\|_{\mathrm{op}}^2\|G_A\|_{\mathrm{op}}',r'2\|G^{-1}\|_{\mathrm{op}}\sum'])
    assert all(s in t['4.1'] for s in ['(i)','(ii)',r'\delta^{n_i-1}/\sqrt{TM}<1',r'\delta^{n_i-1}/\sqrt{TM}\ge1',r'\delta\le c_1',r'\widehat\vartheta_i(X_\delta)'])
    assert t['4.1'].count(r'>c_3')==2
    assert t['4.3'].startswith('Theorem 4.1 remains valid')
    assert 'Assumption L holds for $K$, $\\Delta K$ and $(\\nabla\\cdot b)K$.' in t['4.3']
    assert r'\delta^{-d/2}' in b['D6']
    assert r'A_i^*K_{\delta,x_k}' in b['D9']
    assert r'X_{\delta,k}^{A_0}(t)' in b['D11']
    assert r'M^{-1/2}\delta^{n_i-1}' in b['D12']
    assert r'A_iK' in b['D13'] and r'A_i^*K' not in b['D13']
    assert r'n_i>1-d/2' in b['D14']
    assert 'independent of $\\delta$ and $M$' in b['D15']
    assert r'o(\delta^{2-2n_i})' in b['D16']
    assert r'(-\xi^\top a_\vartheta\xi)^s' in b['D17']
    assert 'negative self-adjoint closed operator' in b['D18']
    assert r'\int_{-\infty}^t' in b['D19']
    assert 'orthonormal system' in b['D20'] and r'C_Z^{1/2}\mathcal Z' in b['D20']
    assert r'K=\Delta^2\widetilde K' in b['D23']
    assert all(s in b['D24'] for s in [r'\vartheta_1\ge1',r'\vartheta_2\in[0,1]',r'\vartheta_3\le0',r'n_1=2',r'n_2=1',r'n_3=0'])
    assert r'|x_k-x_l|>\delta' in b['D25']
    assert all(members[f'D{i}']['source_kind']=='assumption' for i in [13,14,15,16,22,23,24,25])
    for item in list(claims.values()) + list(members.values()) + ambient['auxiliary_source_passages']:
        assert all(1 <= e['page'] <= 23 for e in item['evidence'])
        fragments = [item['statement_original']]
        for context in item.get('naming_context', []):
            assert all(1 <= e['page'] <= 23 for e in context['evidence'])
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
    assert counts==dict(theorems=5,interfaces=25,source_members=25,direct_theorem_uses=28,related_theorem_connections=49,unranked_auxiliary_passages=8)
    assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==21
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:
        assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Five full theorem bodies visually compared; independent enumeration of all admitted main-text pages confirms labels 2.3,3.1,3.2,4.1,4.3. Main text ends above Appendix A on page 24, after the proof conclusion for Theorem 4.1.',
        source_passages='All 25 original passages and eight auxiliary passages compared with PDF pages 1,3-10,18. The spatial SPDE, kernel scaling, adjoint observation channels, corrected augmented MLE, four H clauses, stationary L setup and all three L clauses are retained separately.',
        dependencies='Independent graph reconstruction checks all 28 direct uses and 49 related connections. The general self-adjoint RKHS statements do not inherit the spatial model, Assumption H or Assumption L. Theorem 4.3 inherits the complete Theorem 4.1 assertion and applies every L clause to all three kernels.',
        names_and_highlights='Every interface uses an original natural-language keyword or separately evidenced naming context and has a matching original-passage highlight. Numbered assumptions retain Assumption labels; no assumption is relabeled as a numbered Definition. Explanations trace actual same-paper dependency paths.',
        notation='Visual comparisons preserve script Hilbert space H versus plain RKHS H, script Fisher information, formal adjoints, squared kernel-norm CLT covariances, both fractional endpoint penalties and all inverse-Gram norm factors. The two local lower-bound neighborhoods and three observation channels are complete.',
        limits='Twenty-one notes preserve unresolved source meaning and apparent source errors separately, including the negative Fourier multiplier, covariance-kernel support convention, Gaussian initial-condition issue and proof equation (6.7). No appendix bodies were used and no proof correctness is certified.',
        reproduction='Six content artifacts rebuilt byte-for-byte in an empty directory. Two independent schema validations, fixed local source hash verification and separately specified graph checks passed. Rebuilding does not renew source review.')
    write('evidence/manual-findings.json',findings)
    pages=[1,3,4,5,6,7,8,9,10,18]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    evidence.append(dict(page=24,path='evidence/page-24-boundary.png',before_main_text_end=True,sha256=digest(ROOT/'evidence/page-24-boundary.png'),note='Crop includes the proof conclusion and appendix heading only; no appendix body.'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json', dict(schema_version='statistical-paper-audit-v1', paper_id=PID,
        status='complete', audit_kind='source_review', completed_at=now,
        source=dict(pdf_path=str(source), source_url=paper['source_url'], version=paper['version'],
            pdf_sha256=SHA, pdf_pages=42, main_text_last_pdf_page=24, provenance_path='evidence/source-provenance.json'),
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
        registered_pdf_path=str(source), registered_pdf_sha256=SHA, registered_pdf_pages=42,
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
