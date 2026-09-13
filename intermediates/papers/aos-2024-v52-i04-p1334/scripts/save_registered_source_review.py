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
EXPECTED = {'theorem-inventory.json': '726806cfadf96f4d8f3bf8b46bc037c0da11a16aa994cec7aea164f73417c750', 'source-passages.json': 'bd380f09b4b8ce0bc315c8956db354908d5d21d15765f52f5b16ca2b3baa4916', 'interface-extraction.json': 'faf5461920ea90d62ec2a46c06914daf12ca3e41b2950bb5821899decb11ce8f', 'ambient-prerequisites.json': '702d692d6d5c0b2bf6b48a6725626526b541b446eec080b2261ec6965aec132e', 'unfinalized-census.json': 'c0f4e3a1dcc73d0c7965e9dc25f1208db770c57d6f91b377b2fc632c77949558', 'ranked-interfaces.json': 'cbc9b70b89815cecb8f0d33e9bfe6c286d54081e2e61eacda17f2021cd04b80d'}

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
    assert paper['version']=='arXiv:2111.13551v1, 26 November 2021' and entry['version']=='2111.13551v1.pdf'
    assert paper['source_url']=='https://arxiv.org/pdf/2111.13551v1' and entry['source_url']=='https://export.arxiv.org/pdf/2111.13551'
    ir = json.loads((ROOT / 'inventory-review.json').read_text())
    assert ir['status'] == 'complete' and ir['source_checked']
    assert ir['inventory_sha256'] == digest(ROOT / 'theorem-inventory.json')
    pdf = fitz.open(source)
    assert len(pdf) == paper['pdf_pages'] == entry['pdf_pages'] == 67
    first = ' '.join(pdf[0].get_text().upper().split())
    assert all(s in first for s in [paper['title'].upper(), 'SOL`ENE TH´EPAUT', 'NICOLAS VERZELEN', 'ARXIV:2111.13551V1'])
    assert paper['main_text_last_pdf_page'] == 65
    assert paper['main_text_boundary']['shared_page_with_appendix'] is True
    headings = []
    for n, page in enumerate(list(pdf)[:64], 1):
        assert (ROOT / f'evidence/page-{n:02}.txt').read_bytes().decode() == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans'])
                match = re.match(r'^Theorem (\d+\.\d+)\.', text)
                if match: assert line['spans'][0]['font']=='CMBX10'
                if match:
                    headings.append((n, match[1]))
    assert headings == [(8, '3.3'), (12, '4.9'), (14, '5.2'), (15, '6.3')]
    boundary=pdf[64].get_text(clip=fitz.Rect(0,0,pdf[64].rect.width,399.5511779785156))
    assert 'Proof of Lemma 9.15.' in boundary and 'APPENDIX' not in boundary
    assert (ROOT/'evidence/page-65-before-appendix.txt').read_bytes().decode()==boundary
    assert len(inv['claims']) == len(data['claims']) == 4
    for original, final in zip(inv['claims'], data['claims']):
        assert all(final[k] == v for k, v in original.items())
    claims = {c['claim_id'].split('/T')[-1]: c for c in data['claims']}
    members = {m['local_id']: m for x in data['interfaces'] for m in x['members']}
    local={1:[],2:[1],3:[],4:[3],5:[3],6:[3],7:[],8:[],9:[1,7,8],10:[],11:[10],12:[],13:[],14:[],15:[9,4],16:[],17:[16,15],18:[17,16],19:[1,20],20:[]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in v] for k,v in local.items()}
    direct={'3.3':{2,4,9},'4.9':{2,5,6,10,11,12},'5.2':{2,3,13,14,18},'6.3':{19,20,9,4,5}}
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    expected_reach={'3.3':{1,2,3,4,7,8,9},'4.9':{1,2,3,5,6,10,11,12},'5.2':{1,2,3,4,7,8,9,13,14,15,16,17,18},'6.3':{1,3,4,5,7,8,9,19,20}}
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
    assert 'D2' not in reach['6.3']
    assert all('D19' not in reach[n] and 'D20' not in reach[n] for n in ['3.3','4.9','5.2'])
    t={n:c['statement_original'] for n,c in claims.items()}
    b={lid:m['statement_original'] for lid,m in members.items()}
    assert r'k\ge2' in t['3.3'] and r'p^kk^{3k}+k^{6k}' in t['3.3']
    assert r'\operatorname{Var}(U_k)' in t['3.3']
    assert r'4\le q\le p' in t['4.9'] and r'\lceil\log(4\lceil q/2\rceil)\rceil' in t['4.9']
    assert r'\mathcal P_{2k^*}^{sym}' in t['4.9'] and r'[f;I_0]]' in t['4.9']
    assert r'-q^{1/2}\|f\|_{\infty,I_0}\big]_+' in t['4.9']
    assert r'f:\mathbb R^+\mapsto\mathbb R$' in t['4.9']
    assert 'suitable numerical constant $M>1$' in t['5.2']
    assert t['5.2'].count(r'\mathbb E')==1
    assert r'W(\mu_{\widehat\sigma},\mu_{\sigma(\mathbf A)})' in t['5.2']
    assert r'k\ge1' in t['6.3'] and r'\operatorname{Var}' not in t['6.3']
    assert "(c\\|E\\|_{\\psi_2}k)^{c'k}" in t['6.3']
    assert r'pq\|\mathbf A\|_\infty^{4k-4}+q\|\mathbf A\|_\infty^{4k-2}' in t['6.3']
    assert 'standard normal distribution' not in b['D1'] and 'standard normal distribution' in b['D2']
    assert r'\sigma_1(\mathbf A)\ge\sigma_2(\mathbf A)' in b['D3']
    assert r'\sum_{i=1}^q\sigma_i^s(\mathbf A)' in b['D4']
    assert r'f:\mathbb R^+\mapsto\mathbb R^+' in b['D6']
    assert r'(-1)^rH_r(y)\phi(y)' in b['D7']
    assert r'i_{k+1}=i_1' in b['D8']
    assert r'H_{N_{rs}(i,j)}(\mathbf Y_{rs})' in b['D9']
    assert r'\inf_{f\in\mathcal F}|f-g|_{\infty,I}' in b['D11']
    assert r'q^{-1}\sum_{i=1}^q\delta_{\sigma_i}' in b['D13']
    assert r'\int_{\mathbb R}|F_{\mu_1}(t)-F_{\mu_2}(t)|dt' in b['D14']
    assert r'q^{-1}[M(pq)^{1/4}]^{-2k}U_k' in b['D15']
    assert r'[0,b(pq)^{1/4}]' in b['D16'] and r'd=\lceil M(pq)^{1/4}/\zeta\rceil' in b['D16']
    assert r'\widehat U' in b['D17'] and r'p>0' in b['D17'] and r'p\ge0' not in b['D17']
    assert r'\frac{i}{q+1}' in b['D18'] and r'M(qp)^{1/4}' in b['D18']
    assert r'\mathbb E[E]=0' in b['D19'] and r'\operatorname{Var}(E)=1' in b['D19']
    assert '[39]' in b['D20'] and members['D20']['source_kind']=='source_passage'
    aux={a['local_id']:a['statement_original'] for a in ambient['auxiliary_source_passages']}
    assert r'j_{k+1}=j_1' in aux['A2'] and r'\overline m-\widehat m' in aux['A6']
    assert r'P(x^2)' in aux['A7']
    for item in list(claims.values()) + list(members.values()) + ambient['auxiliary_source_passages']:
        assert all(1 <= e['page'] <= 64 for e in item['evidence'])
        fragments = [item['statement_original']]
        for context in item.get('naming_context', []):
            assert all(1 <= e['page'] <= 64 for e in context['evidence'])
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
    assert counts==dict(theorems=4,interfaces=20,source_members=20,direct_theorem_uses=19,related_theorem_connections=37,unranked_auxiliary_passages=8)
    assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==26
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:
        assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Four complete original theorem statements visually compared with pages 8,12,14,15. Independent bold-heading enumeration covers all admitted main-text pages and confirms 3.3,4.9,5.2,6.3. The main-text proof of Lemma 9.15 ends above Appendix A on page 65.',
        source_passages='All 20 source passages and eight auxiliary passages compared with pages 1,5,7,10-15,35,42. Schatten versus entrywise norms, Hermite occurrence counts, uniform approximation, empirical measures, Wasserstein distance, moment vector, grid, fitting program, quantiles and both noise laws are preserved.',
        dependencies='Independent graph reconstruction checks all 19 direct uses and 37 related connections. Theorem 6.3 shares the Hermite statistic but does not inherit Gaussian noise or unbiasedness. Theorem 5.2 retains the whole original estimator and flags the unresolved hat U versus hat m connection; page 42 supplies corroborating context without rewriting the displayed program.',
        names_and_highlights='All 20 interfaces have original natural-language keywords or separately evidenced naming context and matching source highlights. Every related theorem has a same-paper explanation. Symmetric-polynomial meaning is corroborated on main-text page 35; the external psi_2 norm passage is not presented as a supplied formula.',
        notation='Visual checks preserve bold matrix versus scalar noise E, overlined m in the auxiliary proof passage, c-prime exponent, all five Gaussian variance terms, all three sub-Gaussian squared-error terms and the q-normalized empirical measure. Source typos remain in original statements and are explained separately.',
        limits='Twenty-six source notes record the extra bracket in Theorem 4.9, the repeated constant and missing expectation in Theorem 5.2, grid scaling and aliases, strict-positive optimizer issue, opposite singular-value ordering, cyclic-index mismatch and external norm convention. This is a source census, not a correctness certificate or executable repair of the estimator.',
        reproduction='All six content artifacts reproduced byte-for-byte in an empty directory. Registered source hash, independent graph invariants and both schema validations passed. Regeneration does not renew the source review.')
    write('evidence/manual-findings.json',findings)
    pages=[1,5,7,8,10,11,12,13,14,15,35,42]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    evidence.append(dict(page=65,path='evidence/page-65-boundary.png',before_main_text_end=True,sha256=digest(ROOT/'evidence/page-65-boundary.png'),note='Crop includes the proof conclusion and appendix heading only; no appendix body.'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json', dict(schema_version='statistical-paper-audit-v1', paper_id=PID,
        status='complete', audit_kind='source_review', completed_at=now,
        source=dict(pdf_path=str(source), source_url=paper['source_url'], version=paper['version'],
            pdf_sha256=SHA, pdf_pages=67, main_text_last_pdf_page=65, provenance_path='evidence/source-provenance.json'),
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
        registered_pdf_path=str(source), registered_pdf_sha256=SHA, registered_pdf_pages=67,
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
