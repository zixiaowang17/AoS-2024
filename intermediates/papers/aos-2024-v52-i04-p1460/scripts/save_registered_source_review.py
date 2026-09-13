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
EXPECTED = {'theorem-inventory.json': '62efa9021de464d0cde9e3b6e338cf286ebfbf4acb546cdedeab877269fc0ba1', 'source-passages.json': 'a888694949091c0b20008138a72267485051f9b36359c79e706febea2f711c05', 'interface-extraction.json': 'e77397b047ae875bc6c584e5290646b87d380492a854024f80be728df6537569', 'ambient-prerequisites.json': '46f111517a7be809c7bb535be5342376c204853e6eb7eabdfb327afeb767a3f5', 'unfinalized-census.json': '2aff25c9e754142a82d0b292590da34454f5f27677e5ea1ebeab231396280284', 'ranked-interfaces.json': '90b54b904db978b3e2b3c5c1a4c1e6bb4eef4c8fcad7081c9c6ae4586894d236'}

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
    assert paper['version']=='arXiv:2211.00488v1, 1 November 2022' and entry['version']=='2211.00488v1.pdf'
    assert paper['source_url']=='https://arxiv.org/pdf/2211.00488v1' and entry['source_url']=='https://export.arxiv.org/pdf/2211.00488'
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==digest(ROOT/'theorem-inventory.json')
    pdf=fitz.open(source)
    assert len(pdf)==paper['pdf_pages']==entry['pdf_pages']==74
    first=' '.join(pdf[0].get_text().upper().split())
    assert all(s in first for s in [paper['title'].upper(),'ANDREA MONTANARI','YUCHEN WU','ARXIV:2211.00488V1'])
    assert paper['main_text_last_pdf_page']==28 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    headings=[]
    for n in range(1,29):
        page=pdf[n-1]
        assert (ROOT/f'evidence/page-{n:02}.txt').read_bytes().decode()==page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                match=re.match(r'^Theorem (\d+\.\d+)(?:\.| \()',text)
                if match and line['spans'][0]['font']=='SFBX1095':headings.append((n,match[1]))
    assert headings==[(7,'3.1'),(8,'3.2'),(8,'3.3'),(9,'4.1'),(9,'4.2'),(10,'4.3'),(11,'4.4'),(12,'4.5'),(14,'5.1')]
    last=pdf[27].get_text()
    assert '[ZSF22]' in last and '853' in last and 'APPENDIX' not in last.upper()
    assert 'Appendix A' in pdf[28].get_text(clip=fitz.Rect(0,0,pdf[28].rect.width,94))
    assert len(inv['claims'])==len(data['claims'])==9
    for original,final in zip(inv['claims'],data['claims']):assert all(final[k]==v for k,v in original.items())
    claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # The following expectations were reconstructed from the source independently of the builder.
    local={1:[2],2:[],3:[1],4:[1],5:[],6:[5],7:[3],8:[7],9:[],10:[],11:[10],12:[11],13:[11],14:[],15:[14],16:[4],17:[],18:[4],19:[4,10],20:[19,16],21:[],22:[4],23:[],24:[14],25:[5]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in v] for k,v in local.items()}
    direct={'3.1':{3,5,6,7,8,9},'3.2':{3,5,6},'3.3':{3,5,6,9},'4.1':{12,13,14,15},'4.2':{4,5,6},'4.3':{4,13,17,18,25},'4.4':{4,12,16,17,19,20,25},'4.5':{4,12,16,17,21,25},'5.1':{22,23,24}}
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    expected_reach={'3.1':{1,2,3,5,6,7,8,9},'3.2':{1,2,3,5,6},'3.3':{1,2,3,5,6,9},'4.1':{10,11,12,13,14,15},'4.2':{1,2,4,5,6},'4.3':{1,2,4,5,10,11,13,17,18,25},'4.4':{1,2,4,5,10,11,12,16,17,19,20,25},'4.5':{1,2,4,5,10,11,12,16,17,21,25},'5.1':{1,2,4,14,22,23,24}}
    reach={}
    for n,c in claims.items():
        seen,stack=set(),list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in seen:seen.add(lid);stack.extend(members[lid]['depends_on'])
        reach[n]=seen
    assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected_reach.items()}
    assert {'D1','D2','D4','D6','D17','D25'}.isdisjoint(reach['4.1'])
    assert 'D17' not in reach['4.2']
    assert {'D7','D8'}.isdisjoint(reach['3.3'])
    assert all({'D6','D14','D15'}.isdisjoint(reach[n]) for n in ['4.3','4.4','4.5'])
    assert all({'D13','D18'}.isdisjoint(reach[n]) for n in ['4.4','4.5'])
    assert {'D19','D20'}.isdisjoint(reach['4.5'])
    t={n:c['statement_original'] for n,c in claims.items()};b={lid:m['statement_original'] for lid,m in members.items()}
    assert all(f'\n{i}. ' in t['3.1'] for i in [1,2,3])
    assert r'4+\varepsilon' in t['3.1'] and r'\boldsymbol\Omega\ne\boldsymbol I_r' in t['3.1']
    assert r'\boldsymbol\Omega\boldsymbol\Lambda_0\overset d=\boldsymbol\Lambda_0' in t['3.1']
    assert r'\tag{7}' in t['3.2'] and r'\tag{8}' in t['3.2'] and 'mutually independent' in t['3.2']
    assert 'Theorem 3.1, claim 3' in t['3.3'] and 'fourth' not in t['3.3']
    assert t['3.3'].count(r'\lim_{n,d\to\infty}')==2
    assert r'\boldsymbol Q^*(s)' in t['4.1'] and 'deterministic countable set' in t['4.1']
    assert r'\mathcal F(q_\Theta^2,\boldsymbol Q)' in t['4.1']
    assert [e['page'] for e in claims['4.2']['evidence']]==[9,10]
    assert 'bounded fourth moment' in t['4.2'] and 'achieved by the null estimators' in t['4.2']
    assert r'\tag{16}' in t['4.3'] and 'limits exist and are equal' in t['4.3']
    assert t['4.4'].count('for all but countably many')==2
    assert r'\lim_{\varepsilon\to0+}\limsup_{n,d\to\infty}' in t['4.4'] and 'independent of everything else' in t['4.4']
    assert 'at least one' in t['4.5'] and all(f'({v})' in t['4.5'] for v in ['a','b','c'])
    assert r'dn^{-3}(\log n)^{-6}\to\infty' in t['4.5']
    assert r'd(\log d)^{8/5}/n^{6/5}\to0' in t['4.5'] and '(For condition (b)' in t['4.5']
    assert 'global maximum' in t['4.5'] and r'\frac{\gamma^2}{4s}' in t['4.5'] and r'+\mathsf I(\gamma)' in t['4.5']
    assert [e['page'] for e in claims['5.1']['evidence']]==[14,15]
    assert r'q_\Theta<q_\Theta^{\mathrm{info}}(k)' in t['5.1'] and r'q_\Theta>q_\Theta^{\mathrm{info}}(k)' in t['5.1']
    assert r'\mathrm{p\text{-}lim}' in t['5.1'] and r'\liminf_{n,d\to\infty}\mathbb E' in t['5.1']
    assert 'fixed probability distributions' in b['D2'] and 'mutually independent' in b['D2']
    assert r's_n=1/\sqrt n' in b['D3'] and r's_n=1/\sqrt[4]{nd}' in b['D4']
    assert r'\boldsymbol Q_\Lambda' in b['D5'] and r'\boldsymbol\Lambda_0\boldsymbol\Lambda_0^{\mathsf T}' in b['D5']
    assert 'invertible' in b['D6'] and r'\boldsymbol Q_\Theta=q_\Theta\boldsymbol I_r' in b['D6']
    assert r'\widehat{\boldsymbol\Lambda}_s^{\mathsf T}\widehat{\boldsymbol\Lambda}_s/n=\boldsymbol I_r' in b['D7']
    assert r'\boldsymbol P,\widehat{\boldsymbol P}\in\mathcal O(n)' in b['D8']
    assert r'\|\boldsymbol P(\boldsymbol I-\widehat{\boldsymbol P})\|_{\mathrm{op}}' in b['D8']
    assert r'\boldsymbol\Omega\ne\boldsymbol I_r' in b['D9']
    assert r'W_{ii}\sim\mathsf N(0,2/n)' in b['D10'] and r'W_{ij}\sim\mathsf N(0,1/n)' in b['D10']
    assert r'\frac{q_\Theta}{n}' in b['D11']
    assert r'\min_{\widehat{\boldsymbol M}' in b['D12'] and r'\inf_{\widehat{\boldsymbol M}' in b['D16']
    assert r'\frac1n\mathbb E\log' in b['D13'] and r'\frac1n\mathbb E\log' in b['D18']
    assert r'-\frac s4\|\boldsymbol Q\|_F^2' in b['D14']
    assert r'\sqrt s\boldsymbol z^{\mathsf T}\boldsymbol Q^{1/2}\boldsymbol\lambda+s\boldsymbol\lambda^{\mathsf T}\boldsymbol Q\boldsymbol\Lambda_0-\frac s2\boldsymbol\lambda^{\mathsf T}\boldsymbol Q\boldsymbol\lambda' in b['D14']
    assert r'\boldsymbol Q^*(s)\in\operatorname*{argmax}' in b['D15']
    assert r'\boldsymbol\Theta_0\otimes\boldsymbol\Theta_0\otimes\boldsymbol\Theta_0' in b['D17'] and 'sub-Gaussian' in b['D17']
    assert members['D17']['source_kind']=='assumption' and members['D17']['source_heading']=='Assumption 4.1'
    assert r'\frac{\sqrt\varepsilon}{n}' in b['D19'] and 'independent of everything else' in b['D19']
    assert r'\mu_\Theta;\varepsilon' in b['D20']
    assert 'global maximum' in b['D21'] and 'first stationary point' in b['D21']
    assert r'\operatorname{Cov}(\boldsymbol\Theta_1)=q_\Theta\boldsymbol I_k' in b['D22']
    assert r'\max_{\pi\in \mathfrak S_k}' in b['D23']
    assert r'\boldsymbol Q_0:=\boldsymbol1_k\boldsymbol1_k^{\mathsf T}/k^2' in b['D24']
    assert r'\mathcal F(q_\Theta^2,\boldsymbol Q)>\mathcal F(q_\Theta^2,\boldsymbol Q_0)' in b['D24']
    assert r'\boldsymbol Q_\Lambda' not in b['D25']
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert 'positive semi-definite' in a['A2'] and r'\boldsymbol M=\boldsymbol M^{1/2}\boldsymbol M^{1/2}' in a['A2']
    assert r'\boldsymbol z\sim\mathsf N(0,\boldsymbol I_r)' in a['A5'] and 'independent of each other' in a['A5']
    assert r'\boldsymbol\Sigma=\boldsymbol I_d' in a['A6'] and 'open problem' in a['A7']
    assert ambient['branch_resolution']['4.5']['connective']=='at least one'
    assert ambient['branch_resolution']['5.1']['threshold_equality']=='Not covered.'
    for item in list(claims.values()) + list(members.values()) + ambient['unranked_auxiliary_passages']:
        assert all(1 <= e['page'] <= 28 for e in item['evidence'])
        fragments = [item['statement_original']]
        for context in item.get('naming_context', []):
            assert all(1 <= e['page'] <= 28 for e in context['evidence'])
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
    assert counts==dict(theorems=9,interfaces=25,source_members=25,direct_theorem_uses=41,related_theorem_connections=70,unranked_auxiliary_passages=9)
    assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==22
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Nine complete original Theorems 3.1-3.3, 4.1-4.5 and 5.1 were visually checked on pages 7-12 and 14-15. Bold-heading enumeration covers all main-text pages 1-28. Continued statements, the attributed Theorem 4.1 and every conditional or alternative clause are retained.',
      source_passages='Twenty-five supporting passages and nine auxiliary passages were compared against pages 3, 5-14. They preserve fixed independent factor laws, exact strong/weak scales, moment conventions, estimator and subspace loss, GOE, the symmetric experiment, information and risk functionals, free energy, Assumption 4.1, perturbation and clustering definitions.',
      dependencies='Independent reconstruction verifies 41 direct uses and 70 related connections. The symmetric background theorem does not acquire a Theta prior or Assumption 4.1. Theorem 4.2 allows a nonzero prior mean. Theorems 4.4-4.5 inherit conditions from Theorem 4.3 without importing its mutual-information conclusion. Theorem 4.5 does not acquire the side channel merely from its proof.',
      names_and_highlights='Each interface retains source-derived natural-language terms and meaningful source expression selectors. Assumption and theorem-excerpt identities are preserved, and every related-theorem explanation follows its exact local path.',
      notation='Visual and font checks retain bold matrix/vector variables, upright mutual-information notation, the scalar-channel sans-serif information symbol, normalized GOE variances, Fraktur permutation group, strict threshold improvement and the distinct error normalizations. The source statements retain the unbound s, the projection-group assignment and the printed maximum condition.',
      limits='Twenty-two notes record source inconsistencies and ambiguities, including Theorem 3.1 moment scope, absent extra hypotheses in Theorem 3.3, Theorem 4.1 parameter binding, Theorem 4.5(c) unbounded objective, and the non-interchangeable limit/exception/branch qualifiers. Appendix bodies and external proofs are excluded; this is not proof certification.',
      reproduction='All six content files reproduced byte-for-byte from the retained per-paper scripts in an empty directory. Source hash, independent inventory, full claim identity, semantic invariants, graph, math-fragment and schema checks passed. A rebuild alone does not renew source review.')
    write('evidence/manual-findings.json',findings)
    pages=[1,3,5,6,7,8,9,10,11,12,13,14,15,28]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
      source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=74,main_text_last_pdf_page=28,provenance_path='evidence/source-provenance.json'),
      enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent bold-heading enumeration and visual comparison of all complete theorem bodies.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
      counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),
      artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,
      review_limits=['Source transcription and statement-dependency review, not proof certification.','Appendix bodies and external proofs excluded.','Apparent source errors and ambiguous hypotheses are preserved and documented.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,
      registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=74,source_version=paper['version'],registered_version_alias=entry['version'],registered_url_alias=entry['source_url'],
      checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
