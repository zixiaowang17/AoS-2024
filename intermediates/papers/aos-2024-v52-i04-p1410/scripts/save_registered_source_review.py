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
EXPECTED = {'theorem-inventory.json': '1d6cd09be6b0db4e865cb3ef1f4fcc8f60873068a98d8585bb57ba12eb790edc', 'source-passages.json': '7883fa9d028173046c185e6386b2048f71a377d5057679efec5892c54a6cd6d6', 'interface-extraction.json': 'e034bac88396f5d80542b0b70db8e85bd7bdd77584dc16645ceb81d1852390ed', 'ambient-prerequisites.json': '844a09d5cc0c89a414c43c9b6888102e6da161f30ac8651d532035e9485e2cca', 'unfinalized-census.json': '0183f320a4511806ee4f6ca73e4eb7c3e7141910ff78315bbb688a374df936f5', 'ranked-interfaces.json': '8cd445e548b5c88384aee6721df835234437fc62913c4c531067c2ac70c1d47a'}

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
    assert paper['version']=='arXiv:2208.07610v2, 17 October 2023' and entry['version']=='2208.07610v2.pdf'
    assert paper['source_url']=='https://arxiv.org/pdf/2208.07610v2' and entry['source_url']=='https://export.arxiv.org/pdf/2208.07610'
    ir = json.loads((ROOT / 'inventory-review.json').read_text())
    assert ir['status'] == 'complete' and ir['source_checked']
    assert ir['inventory_sha256'] == digest(ROOT / 'theorem-inventory.json')
    pdf = fitz.open(source)
    assert len(pdf) == paper['pdf_pages'] == entry['pdf_pages'] == 31
    first = ' '.join(pdf[0].get_text().upper().split())
    assert all(s in first for s in [paper['title'].upper(), 'MURIEL FELIPE PÉREZ-ORTIZ', 'TYRON LARDY', 'RIANNE DE', 'HEIDE', 'PETER D. GRÜNWALD', 'ARXIV:2208.07610V2'])
    assert paper['main_text_last_pdf_page'] == 23
    assert paper['main_text_boundary']['shared_page_with_appendix'] is False
    headings=[]
    for n in range(1,24):
        page=pdf[n-1]
        assert (ROOT/f'evidence/page-{n:02}.txt').read_bytes().decode()==page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                match=re.match(r'^THEOREM (\d+)(?:\.| \()',text)
                if match:
                    assert line['spans'][0]['font']=='NimbusRomNo9L-Regu'
                    headings.append((n,match[1]))
    assert headings==[(7,'1'),(10,'2'),(10,'4')]
    assert 'ZHANG' in pdf[22].get_text() and '2305.16539' in pdf[22].get_text()
    assert 'APPENDIX' not in pdf[22].get_text()
    assert 'APPENDIX A: INVARIANCE AND SUFFICIENCY' in pdf[23].get_text(clip=fitz.Rect(0,0,pdf[23].rect.width,80))
    assert len(inv['claims'])==len(data['claims'])==3
    for original, final in zip(inv['claims'], data['claims']):
        assert all(final[k] == v for k, v in original.items())
    claims = {c['claim_id'].split('/T')[-1]: c for c in data['claims']}
    members = {m['local_id']: m for x in data['interfaces'] for m in x['members']}
    # Source-based expectations are specified separately from extraction and finalization.
    local={1:[],2:[],3:[],4:[],5:[4],6:[4],7:[4],8:[6],9:[],10:[8],11:[10,8],12:[10,8],13:[],14:[4,5,15],15:[4],16:[8,6,4]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in v] for k,v in local.items()}
    direct={'1':{1,2,3,8,10,11},'2':{1,2,3,7,8,9,13,14,16},'4':{3,8,10,11,12,16}}
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    expected_reach={'1':{1,2,3,4,6,8,10,11},'2':{1,2,3,4,5,6,7,8,9,13,14,15,16},'4':{3,4,6,8,10,11,12,16}}
    reach={}
    for n,c in claims.items():
        seen,stack=set(),list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in seen:
                seen.add(lid);stack.extend(members[lid]['depends_on'])
        reach[n]=seen
    assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected_reach.items()}
    assert {'D5','D7','D9','D13','D14','D15'}.isdisjoint(reach['4'])
    assert {'D5','D7','D9','D12','D13','D14','D15','D16'}.isdisjoint(reach['1'])
    assert {'D10','D11','D12'}.isdisjoint(reach['2'])
    t={n:c['statement_original'] for n,c in claims.items()}
    b={lid:m['statement_original'] for lid,m in members.items()}
    assert r'\inf_{\boldsymbol\Pi_0,\boldsymbol\Pi_1}' in t['1'] and r'\min_{\boldsymbol\Pi_0,\boldsymbol\Pi_1}' in t['1']
    assert 'achieve the minimum on the right hand side' in t['1']
    assert r'\int q_g^{V_n}(v_n(X^n))d\boldsymbol\Pi_1^\star(g)' in t['1']
    assert r'\int p_g^{V_n}(v_n(X^n))d\boldsymbol\Pi_0^\star(g)' in t['1']
    assert 'In other words' in t['1']
    assert t['2'].count(r'1+\varepsilon')==2 and 'unit element' in t['2']
    assert r'\mathbf E_1^{\mathbf Q}' in t['2'] and r'\mathbf E^{\mathbf Q^{M_n}}' in t['2']
    assert 'Assumption 1 holds' in t['2'] and 'amenable' in t['2']
    assert 'Part 3 of Assumption 1' in t['4'] and 'for each $g\in G$' in t['4'] and 'there exists $h\in G$' in t['4']
    assert 'is constant' in t['4'] and 'if and only if' in t['4']
    assert r'\mathbf P^T\{T\in B\}' in b['D1']
    assert r'\boldsymbol\Pi^\theta\mathbf P_\theta' in b['D2']
    assert r'\mathbf E^{\mathbf Q}[\ln(dQ/dP)]' in b['D3']
    assert r'gX^n:=(gx_1,\ldots,gx_n)' in b['D4']
    assert 'identity element' in b['D5']
    assert r'\mathbf P_{g\theta}\{X\in gB\}' in b['D6']
    assert 'if and only if' in b['D7'] and r"x=gx'" in b['D7']
    assert r'\mathcal H_0:X^n\sim\mathbf P_g' in b['D8']
    assert r'\lim_{k\to\infty}' in b['D9'] and r'\boldsymbol\Pi_k\{H\in Bg\}' in b['D9'] and r'\sup' not in b['D9']
    assert 'nonnegative real statistics' in b['D10'] and r'\sup_{g\in G}\mathbf E_g^{\mathbf P}[T_n]\le1' in b['D10']
    assert 'Should it exist' in b['D11']
    assert r'\inf_{g\in G}\left\{' in b['D12'] and r'\sup_{T_n\prime' not in b['D12']
    assert 'locally compact' in b['D13'] and 'free, continuous and proper' in b['D14']
    assert r'(g,x^n)\mapsto(gx^n,x^n)' in b['D15']
    assert r'\mu\{gB\}=\chi(g)\mu\{B\}' in b['D16'] and 'single common support' in b['D16']
    assert all(members[f'D{i}']['source_kind']=='assumption' for i in [13,14,16])
    a={p['local_id']:p['statement_original'] for p in ambient['unranked_auxiliary_passages']}
    assert 'independent copies' in a['A1'] and 'measurable function' in a['A1']
    assert 'infimum on the left in (9) is not achieved' in a['A3']
    assert r'\rho\{Bg\}=\rho\{B\}' in a['A6']
    assert r'\frac{\rho\{C_i\}}{\rho\{C_iK\}}\to1' in a['A7']
    for item in list(claims.values()) + list(members.values()) + ambient['unranked_auxiliary_passages']:
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
    counts=dict(theorems=len(inv['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['unranked_auxiliary_passages']))
    assert counts==dict(theorems=3,interfaces=16,source_members=16,direct_theorem_uses=21,related_theorem_connections=29,unranked_auxiliary_passages=9)
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
        inventory='Three full original Theorems 1, 2 and 4 were compared visually on pages 7 and 10. Independent enumeration covers all main-text pages 1-23 and excludes Corollary 3, citations and proof headings. Every optimization formula, moment condition and conclusion is retained.',
        source_passages='Sixteen supporting passages and nine auxiliary passages were compared with pages 1-10 and 18. They preserve image and mixture laws, ordered KL, group actions and invariance, all separate assumption parts, amenability, e-statistics and both GROW criteria.',
        dependencies='Independent graph reconstruction verifies 21 direct uses and 29 related connections. Theorem 1 does not acquire a maximal-invariance or amenability requirement. Theorem 4 includes only Part 3 of Assumption 1, not Parts 1-2. Theorem 2 concerns KL equality and does not acquire downstream e-statistic or martingale conclusions.',
        names_and_highlights='Each interface has a source-derived natural-language keyword and a meaning-bearing source highlight. Named assumption parts retain source identity. All related-theorem explanations follow their actual paper-local paths.',
        notation='Visual checks preserve the full-data infimum versus reduced-data minimum, two separate starred priors, both 1+epsilon moments with their distinct laws, and the for-every-g there-exists-h quantifiers. Original pointwise amenability and the later compact-set formulation are kept separately.',
        limits='Twenty-one source notes record the density and logarithm conventions, topological-group and Polish wording, relative left invariance and common support, and the source reparameterization context. Appendix bodies and external proof details remain excluded. No group-theoretic equivalence or proof is certified.',
        reproduction='All six content artifacts reproduced byte-for-byte in an empty directory. Independent source hash, inventory identity, theorem enumeration, graph, mathematical-fragment and schema checks passed. Rebuild does not renew source review.')
    write('evidence/manual-findings.json',findings)
    pages=[1,2,3,4,5,6,7,9,10,18,23]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    # The separately saved page-24 heading is boundary evidence only, not admitted source content.
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json', dict(schema_version='statistical-paper-audit-v1', paper_id=PID,
        status='complete', audit_kind='source_review', completed_at=now,
        source=dict(pdf_path=str(source), source_url=paper['source_url'], version=paper['version'],
            pdf_sha256=SHA, pdf_pages=31, main_text_last_pdf_page=23, provenance_path='evidence/source-provenance.json'),
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
        registered_pdf_path=str(source), registered_pdf_sha256=SHA, registered_pdf_pages=31,
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
