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
EXPECTED = {
    'theorem-inventory.json': '720d8b346a7b3a7b67093bea38cb1b8bdb2c31005309656eb0aa8dac2d1da53e',
    'source-passages.json': '2a0062e7f10167a93127b5e26d475f6fb70016015d0bbbd91629e0d32a429b97',
    'interface-extraction.json': '8b6e58eeaea290610714d7fd93b1e514cc7861be24120ccd6076152ed4ba278a',
    'ambient-prerequisites.json': '7daa9a7506a77913777f42ea3dad18ea89a6df4dd693690791586fd760afe065',
    'unfinalized-census.json': '4b8401dde1754302ffcbe6004d006b935f0b265e3cdf78a8302c844fcc03c8c7',
    'ranked-interfaces.json': '5e193109bb508d71be5853fafdcf0932803620a8d25093d36489a30fae2a0df1'
}


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
    assert len(pdf) == paper['pdf_pages'] == entry['pdf_pages'] == 26
    first = ' '.join(pdf[0].get_text().upper().split())
    assert all(s in first for s in [paper['title'].upper(), 'YINFENG CHEN', 'YULING JIAO', 'RUI QIU', 'ZHOU YU', '10.1214/24-AOS2390'])
    assert paper['main_text_last_pdf_page'] == 26
    assert paper['main_text_boundary']['shared_page_with_appendix'] is False
    headings = []
    for n, page in enumerate(pdf, 1):
        assert (ROOT / f'evidence/published/page-{n:02}.txt').read_bytes().decode() == page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                text = ''.join(s['text'] for s in line['spans'])
                match = re.fullmatch(r'THEOREM (\d+\.\d+)\.', text)
                if match:
                    headings.append((n, match[1]))
    assert headings == [(7, '3.2'), (10, '3.7'), (11, '3.8'), (14, '4.2'), (16, '4.4'), (17, '4.6')]
    assert 'SUPPLEMENTARY MATERIAL' in pdf[22].get_text() and '[56]' in pdf[25].get_text()
    assert len(inv['claims']) == len(data['claims']) == 6
    for original, final in zip(inv['claims'], data['claims']):
        assert all(final[k] == v for k, v in original.items())
    claims = {c['claim_id'].split('/T')[-1]: c for c in data['claims']}
    members = {m['local_id']: m for x in data['interfaces'] for m in x['members']}
    local = {1: [], 2: [1], 3: [2], 4: [], 5: [4], 6: [3,4,5], 7: [6,4],
             8: [1,4], 9: [6,8], 10: [1,4], 11: [], 12: [4,11], 13: [11],
             14: [11,12,8], 15: [8,25], 16: [8,11,4], 17: [8,18], 18: [],
             19: [], 20: [19,11], 21: [12,8], 22: [21,8], 23: [],
             24: [23,9,16,17,11], 25: [14,11,12,13,8]}
    assert {lid: m['depends_on'] for lid, m in members.items()} == {
        f'D{k}': [f'D{i}' for i in ids] for k, ids in local.items()}
    direct = {'3.2': {3,4,5}, '3.7': {9,8,6,7}, '3.8': {3,10,6},
              '4.2': {9,16,20,8,14,11}, '4.4': {9,16,20,8,14,11,22},
              '4.6': {9,16,20,8,25,11,22,15,24}}
    assert {n: set(c['depends_on']) for n, c in claims.items()} == {
        n: {f'D{i}' for i in ids} for n, ids in direct.items()}
    expected_reach = {
        '3.2': {1,2,3,4,5}, '3.7': {1,2,3,4,5,6,7,8,9},
        '3.8': {1,2,3,4,5,6,10},
        '4.2': {1,2,3,4,5,6,8,9,11,12,14,16,19,20},
        '4.4': {1,2,3,4,5,6,8,9,11,12,14,16,19,20,21,22},
        '4.6': {1,2,3,4,5,6,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25}}
    reach = {}
    for n, c in claims.items():
        seen, stack = set(), list(c['depends_on'])
        while stack:
            lid = stack.pop()
            if lid not in seen:
                seen.add(lid)
                stack.extend(members[lid]['depends_on'])
        reach[n] = seen
    assert reach == {n: {f'D{i}' for i in ids} for n, ids in expected_reach.items()}
    for n in ['4.2', '4.4']:
        assert reach[n].isdisjoint({'D13', 'D17', 'D18', 'D23', 'D24', 'D25'})
    assert 'D9' not in reach['3.8']
    bodies = {lid: m['statement_original'] for lid, m in members.items()}
    t = {n: c['statement_original'] for n, c in claims.items()}
    assert 'Thereafter' in t['3.2'] and r'\bar f_i^*(X)' in t['3.2']
    assert r'\frac{\lambda_j^*}{2\mu_j}' in t['3.7']
    assert r'\mu>|\lambda_1^*+\cdots+\lambda_d^*|' in t['3.8']
    assert r'n\ge V' in t['4.2'] and r'{n-3}' in t['4.2']
    assert r'n\ge V' not in t['4.4']
    assert all(s in t['4.6'] for s in ['Therefore', 'Moreover', 'Corollary 4.5', r'1-(4j-3)\delta', r'E\rho^2', r'\sum_{j=1}^d'])
    assert r'\|\operatorname{Var}\{\boldsymbol f(X)\}-I_d\|_F.' in bodies['D10']
    assert r'\|_F^2' not in bodies['D10']
    assert r'm=d+1' in bodies['D9'] and r'\tilde\mu>-\lambda_1^*' in bodies['D9']
    assert r'\binom n4^{-1}' in bodies['D14'] and r'\binom n4^{-1}' in bodies['D25']
    assert r'h_{\tilde\mu' not in bodies['D14'] and r'h_{\tilde\mu' in bodies['D25']
    assert r'\mathcal I_{4,3}' in bodies['D12'] and r'\mathcal I_{4,3}' in bodies['D13']
    assert r'\kappa(y,\tilde y)\le B' in bodies['D16']
    assert r'\beta\in(0,1]' in bodies['D18']
    assert r'\|f+g\|_{L_2(P_X)}^2' in bodies['D22']
    assert r'\tag{12}' in bodies['D22'] and r'4E\{' in bodies['D21']
    assert r'W_i(x)=\omega_i x+b_i' in bodies['D23']
    assert r'n\ge\mathcal S\mathcal L\log(\mathcal S)' in bodies['D24']
    assert '(A3)' in bodies['D24'] and members['D24']['source_kind'] == 'condition'
    assert members['D2']['source_kind'] == 'assumption'
    assert all(members[f'D{i}']['source_kind'] == 'assumption' for i in [9,16,17,20])
    for item in list(claims.values()) + list(members.values()) + ambient['auxiliary_source_passages']:
        assert all(1 <= e['page'] <= 26 for e in item['evidence'])
        fragments = [item['statement_original']]
        for context in item.get('naming_context', []):
            assert all(1 <= e['page'] <= 26 for e in context['evidence'])
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
    counts = dict(theorems=6, interfaces=len(data['interfaces']), source_members=len(members),
        direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),
        related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),
        unranked_auxiliary_passages=len(ambient['auxiliary_source_passages']))
    assert counts == dict(theorems=6, interfaces=25, source_members=25,
        direct_theorem_uses=32, related_theorem_connections=74, unranked_auxiliary_passages=8)
    assert set(ambient['statement_resolution']) == {'shared', *claims}
    assert len(ambient['source_issues']) == 23
    rebuild = json.loads((ROOT / 'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id'] == PID and len(rebuild['comparisons']) == 6
    for c in rebuild['comparisons']:
        assert c['matches_saved_bytes'] and c['saved_sha256'] == c['regenerated_sha256'] == digest(ROOT / c['artifact'])
    validation = []
    for name in ['theorem-inventory.json', 'ranked-interfaces.json']:
        result = subprocess.run([sys.executable, str(SKILL / 'validate_census.py'), str(ROOT / name)],
            capture_output=True, text=True, check=True)
        validation.append(dict(artifact=name, returncode=result.returncode, stdout=result.stdout))
    findings = dict(
        inventory='All six complete theorem bodies visually reviewed; Theorem 4.6 includes both final consequences. Actual headings independently enumerated across all 26 pages.',
        source_passages='All 25 source passages compared with PDF pages 4–7 and 9–16; eight additional ambient passages preserve probability spaces, norms, tuple conventions, constants and section conventions.',
        dependencies='Independently checked all 32 direct uses and 74 related connections. No ReLU/Holder hypothesis is attached to Theorems 4.2 or 4.4, and neither uses the later-step covariance kernel. Theorem 3.8 does not inherit A1.',
        names_and_highlights='Every interface title comes from an original natural-language keyword or separately evidenced adjacent naming passage. Every member has a meaning-bearing source selector; source kinds distinguish assumptions, conditions, theorem excerpts and definitions.',
        notation='Checked fraktur central M, script G/B/D, calligraphic candidate F and architecture sizes, plain W affine maps and bold vector f against the PDF typography. Original coefficients, penalty powers and probability levels retained.',
        limits='The census preserves source claims and unresolved meanings, including A4 epsilon range, mean-zero convention, C1 and network depth. It does not certify proofs or import excluded supplement content.',
        reproduction='Six saved content artifacts rebuilt byte-for-byte in a fresh directory; source identity and both independent schema validations passed.')
    write('evidence/manual-findings.json', findings)
    pages = [1,4,5,6,7,9,10,11,12,13,14,15,16,17,23]
    evidence = [dict(page=n, path=f'evidence/published/page-{n:02}.png',
        sha256=digest(ROOT / f'evidence/published/page-{n:02}.png')) for n in pages]
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json', dict(schema_version='statistical-paper-audit-v1', paper_id=PID,
        status='complete', audit_kind='source_review', completed_at=now,
        source=dict(pdf_path=str(source), source_url=paper['source_url'], version=paper['version'],
            pdf_sha256=SHA, pdf_pages=26, main_text_last_pdf_page=26, provenance_path='evidence/source-provenance.json'),
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
        registered_pdf_path=str(source), registered_pdf_sha256=SHA, registered_pdf_pages=26,
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
