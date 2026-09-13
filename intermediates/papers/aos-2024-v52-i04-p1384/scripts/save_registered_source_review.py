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
EXPECTED = {'theorem-inventory.json': 'ee428c51634aa552349cd15c16cea93ee566114247b8ecf7a5ff68e1ff29afa6', 'source-passages.json': '44ce3c2e5e571deb9063d2324337896085b3b916091ddc2f4b74054e2f8efd78', 'interface-extraction.json': '558d2fdb0ffbafd0233d04d924d601db444b1a5b50f1d57bd8a0b379aba71430', 'ambient-prerequisites.json': '5d6694436ebf301fc9e59067cb372ed73f66b0ce2890aee0767a37a102f875e0', 'unfinalized-census.json': '9e50091944325e936e1ce74c890ee18c52e84b12137030747e57faf546c33910', 'ranked-interfaces.json': '03b8e1e5c2afdd079b01878964feb6d2395cbf0df5c8401947aa19a3c918dcbd'}

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
    assert paper['version']=='arXiv:2301.02168v2, 7 January 2024; title-page date 9 January 2024' and entry['version']=='2301.02168v2.pdf'
    assert paper['source_url']=='https://arxiv.org/pdf/2301.02168v2' and entry['source_url']=='https://export.arxiv.org/pdf/2301.02168'
    ir = json.loads((ROOT / 'inventory-review.json').read_text())
    assert ir['status'] == 'complete' and ir['source_checked']
    assert ir['inventory_sha256'] == digest(ROOT / 'theorem-inventory.json')
    pdf = fitz.open(source)
    assert len(pdf) == paper['pdf_pages'] == entry['pdf_pages'] == 49
    first = ' '.join(pdf[0].get_text().upper().split())
    assert all(s in first for s in [paper['title'].upper(), 'ANYA KATSEVICH', 'PHILIPPE RIGOLLET', 'ARXIV:2301.02168V2'])
    assert paper['main_text_last_pdf_page'] == 22
    assert paper['main_text_boundary']['shared_page_with_appendix'] is True
    headings=[]
    for n in range(1,23):
        page=pdf[n-1]
        clip=fitz.Rect(0,0,page.rect.width,296.2278137207031) if n==22 else page.rect
        path=ROOT/('evidence/page-22-before-appendix.txt' if n==22 else f'evidence/page-{n:02}.txt')
        assert path.read_bytes().decode()==page.get_text(clip=clip)
        for block in page.get_text('dict',clip=clip)['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                match=re.match(r'^Theorem (\d+\.\d+)(?:\.| \()',text)
                if match and line['spans'][0]['font']=='CMBX10':headings.append((n,match[1]))
    assert headings==[(7,'2.1'),(8,'2.2'),(14,'3.1'),(16,'4.1')]
    boundary=pdf[21].get_text(clip=fitz.Rect(0,0,pdf[21].rect.width,296.2278137207031))
    assert 'Acknowledgments' in boundary and 'CCF-2106377' in boundary
    assert 'We review some notation' not in boundary
    assert len(inv['claims'])==len(data['claims'])==4
    for original, final in zip(inv['claims'], data['claims']):
        assert all(final[k] == v for k, v in original.items())
    claims = {c['claim_id'].split('/T')[-1]: c for c in data['claims']}
    members = {m['local_id']: m for x in data['interfaces'] for m in x['members']}
    # Independently specified after comparing each definition and theorem with the PDF.
    local={1:[],2:[],3:[],4:[],5:[3,4],6:[3,4],7:[1,2],8:[1,4,3],9:[7,8],11:[9,3],12:[9],13:[1,9,3],14:[],15:[14,2],16:[14,15],17:[13,15],18:[9],19:[9,1,2],21:[2,3],22:[19,21,3]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in v] for k,v in local.items()}
    direct={'2.1':{4,5,6,9,11,12},'2.2':{4,5,6,9,11,12,13},'3.1':{16,7,8,9,11,12,17,18},'4.1':{4,5,6,9,11,19,21,22}}
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    expected_reach={'2.1':{1,2,3,4,5,6,7,8,9,11,12},'2.2':{1,2,3,4,5,6,7,8,9,11,12,13},'3.1':{1,2,3,4,7,8,9,11,12,13,14,15,16,17,18},'4.1':{1,2,3,4,5,6,7,8,9,11,19,21,22}}
    reach={}
    for n,c in claims.items():
        seen,stack=set(),list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in seen:
                seen.add(lid);stack.extend(members[lid]['depends_on'])
        reach[n]=seen
    assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected_reach.items()}
    assert all({'D14','D15','D16','D17','D18'}.isdisjoint(reach[n]) for n in ['2.1','2.2','4.1'])
    assert {'D5','D6','D19','D21','D22'}.isdisjoint(reach['3.1'])
    assert all({'D19','D21','D22'}.isdisjoint(reach[n]) for n in ['2.1','2.2'])
    t={n:c['statement_original'] for n,c in claims.items()}
    b={lid:m['statement_original'] for lid,m in members.items()}
    assert [e['page'] for e in claims['2.1']['evidence']]==[7,8]
    assert all(r'\tag{'+x+'}' in t['2.1'] for x in ['2.7','2.8','2.9','2.10'])
    assert all(r'\tag{'+x+'}' in t['3.1'] for x in ['3.8','3.9','3.10','3.11','3.12'])
    assert 'On an event of probability at least' in t['3.1']
    assert r'1-\exp(-C(nd)^{1/9})-5e^{-Cn}-n^{-d/4}' in t['3.1']
    assert r'\bar\theta=\int\theta d\pi(\theta)' in t['3.1'] and r'\|\bar m-\hat m\|' in t['3.1']
    assert r'\mathcal B_{s,\hat m}' in t['3.1'] and r'\mathcal S_{\hat m}' in b['D18']
    assert 'orthogonal to all third order Hermite polynomials' in t['4.1']
    assert 'under the conditions of Theorem 2.1' in t['4.1']
    assert r'\sup_{\|u\|_H=1}\langle T,u^{\otimes k}\rangle' in b['D3']
    assert r'\|x\|_H=\sqrt{x^THx}' in b['D3']
    assert r'H_v=\nabla^2v(m^*)\succ0' in b['D4']
    assert r'q,a_3,a_4>0' in b['D5'] and r'C(q)<1' in b['D5']
    assert r'a_3\frac d{\sqrt n}+a_4\frac{d^2}n\le1' in b['D5']
    assert r'\frac12\sqrt{d/n}' in b['D6']
    assert r'S\preceq2H_V^{-1}' in b['D8'] and r'\|H_V^{1/2}S^{1/2}\|^2' in b['D8']
    assert 'although we have not proved this' in b['D9'] and 'redefine' in b['D9']
    assert r'\|x-\hat m\|_{\hat S^{-1}}\ge R_g\sqrt d' in b['D11']
    assert r'\Sigma^{-1}=0' in b['D15'] and r'\frac1{2n}\theta^T\Sigma^{-1}\theta' in b['D15']
    assert r'\|\theta_0\|\le C' in b['D16'] and r'\|\Sigma^{-1}\|\le C' in b['D16'] and r'q=0' in b['D16']
    assert r'b_i(\theta)=\mathbb E_{\theta\sim\hat\pi}' in b['D17']
    assert r'\rho=T_\#\pi' in b['D19'] and r'T(x)=\hat S^{-1/2}(x-\hat m)' in b['D19']
    assert r'\mathbf H_k(x)e^{-\|x\|^2/2}=(-1)^k\nabla^ke^{-\|x\|^2/2}' in b['D21']
    assert r'p_3(x)=\frac16\langle \mathbf A_3,\mathbf H_3(x)\rangle' in b['D22']
    assert all(members[f'D{i}']['source_kind']=='assumption' for i in [4,5,6])
    a={p['local_id']:p['statement_original'] for p in ambient['unranked_auxiliary_passages']}
    assert r'\epsilon=d/\sqrt n' in a['A1']
    assert r'\|f\|_2=(\int f^2d\gamma)^{1/2}' in a['A3']
    assert r'f_0=f-\gamma(f)' in a['A4']
    assert r'\frac23H_V^{-1}\preceq\hat S\preceq2H_V^{-1}' in a['A5']
    assert 'allowed to depend on both' in a['A6']
    assert r'\operatorname*{argmin}' in a['A7']
    for item in list(claims.values()) + list(members.values()) + ambient['unranked_auxiliary_passages']:
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
    counts=dict(theorems=len(inv['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['unranked_auxiliary_passages']))
    assert counts==dict(theorems=4,interfaces=20,source_members=20,direct_theorem_uses=29,related_theorem_connections=51,unranked_auxiliary_passages=8)
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
        inventory='Four full original Theorems 2.1, 2.2, 3.1 and 4.1 were visually compared on pages 7-8, 14 and 16. Independent font-aware heading enumeration includes all admitted main-text pages and excludes citations. Theorem 2.1 continuation and every formula, branch and constant-dependence clause are retained.',
        source_passages='Twenty supporting passages and eight auxiliary passages were compared with pages 1-17. All three numbered assumptions, canonical pair and region, logistic posterior and local sampling assumptions, corrections Q and p3, tensor norms and Hermite conventions are preserved. Epsilon, Gaussian L2 norm and centering f0 remain explicit ambient passages.',
        dependencies='Independent source-based graph specification and reach reconstruction verify 29 direct uses and 51 related connections. The logistic model is confined to Theorem 3.1. Derived Assumptions 2-3 are not imposed as extra logistic hypotheses, and proof-only remainders or contraction constructions are excluded.',
        names_and_highlights='Every interface uses an original natural-language keyword, with separately archived naming context where necessary, and a source-backed highlight. Assumptions retain their labels. All related theorems have source-specific explanations and paper-local paths.',
        notation='Visual comparison preserves the m-star placement switch, the missing absolute value in the tensor supremum, q>0 versus q=0, prior versus posterior Sigma, the bound variable in b_i(theta), bar-theta versus bar-m and the symmetric Borel class alias. The defining p3 retains its one-sixth factor and bold tensor notation.',
        limits='Twenty-one source notes separate original statements from interpretation. The canonical solution is not assumed to be a global KL minimizer. Ordinary well-definedness of expectations is recorded without editing hypotheses. Appendix notation and all appendix bodies are excluded; no proof or library availability is certified.',
        reproduction='All six content artifacts reproduced byte-for-byte in an empty directory. Independent schema, inventory identity, source hash, source boundary, graph and mathematical-fragment checks passed. Reproduction does not renew source review.')
    write('evidence/manual-findings.json',findings)
    pages=[1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    evidence.append(dict(page=22,path='evidence/page-22-boundary.png',before_main_text_end=True,sha256=digest(ROOT/'evidence/page-22-boundary.png'),note='Crop ends after Acknowledgments, before the appendix notation prelude; no appendix content.'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json', dict(schema_version='statistical-paper-audit-v1', paper_id=PID,
        status='complete', audit_kind='source_review', completed_at=now,
        source=dict(pdf_path=str(source), source_url=paper['source_url'], version=paper['version'],
            pdf_sha256=SHA, pdf_pages=49, main_text_last_pdf_page=22, provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']], printed_label_check=headings,
            method='Independent actual-heading enumeration and visual comparison of all complete theorem bodies.',
            excluded_result_types=['Lemma','Proposition','Corollary','Remark'], appendix_material_used=False),
        counts=counts, validation=dict(status='passed', validator=str(SKILL / 'validate_census.py'), checks=list(findings.values())),
        artifacts={n: dict(path=n, sha256=digest(ROOT / n)) for n in [*EXPECTED, 'inventory-review.json']},
        source_notes=ambient['source_issues'], unresolved_source_references=ambient['unresolved_source_references'],
        ambient_resolution=ambient['statement_resolution'], evidence=evidence,
        review_limits=['Source transcription and statement-dependency review, not proof certification.', 'External supplement and appendix bodies excluded.']))
    write('registered-source-review.json', dict(schema_version='registered-paper-source-review-v1',
        paper_id=PID, status='complete', method='source_content_revalidation', reviewed_at=now,
        registered_pdf_path=str(source), registered_pdf_sha256=SHA, registered_pdf_pages=49,
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
