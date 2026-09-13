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
EXPECTED = {'theorem-inventory.json': 'de6bc596a31b21a3accee602553198345204f4248bcf610af537780db3746c09', 'source-passages.json': '11958cc61895f59f32ee10cb773ad94fa427166eca9476fdb0daf127f2a9579b', 'interface-extraction.json': 'a7fc08729bc50d93178bf510edbec8f6388beaec810327239c9d49d3b41266e7', 'ambient-prerequisites.json': '48dbdf55502b45feb882940299b712762fea0015091bb63315fa6af00c9f9f02', 'unfinalized-census.json': '4392bbd4f7f6c4c594ec06f0ffeba881c47a4828f5769eca286a06a1aa50cbcc', 'ranked-interfaces.json': '327ee9307a744c187e96879f9d8239e99f3bce92d8c3c0db92c938c8efc1e550'}

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
    assert paper['version']=='arXiv:2308.04916v3, 29 May 2024' and entry['version']=='2308.04916v3.pdf'
    assert paper['source_url']=='https://arxiv.org/pdf/2308.04916v3' and entry['source_url']=='https://export.arxiv.org/pdf/2308.04916'
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked']
    assert ir['inventory_sha256']==digest(ROOT/'theorem-inventory.json')
    pdf=fitz.open(source)
    assert len(pdf)==paper['pdf_pages']==entry['pdf_pages']==59
    first=' '.join(pdf[0].get_text().upper().split())
    assert all(s in first for s in [paper['title'].upper(),'SERGIOS AGAPIOU','ISMAËL CASTILLO','ARXIV:2308.04916V3'])
    assert paper['main_text_last_pdf_page']==26 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    headings=[]
    for n in range(1,27):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,156.9671630859375) if n==26 else page.rect
        path=ROOT/'evidence'/(f'page-{n:02}.txt' if n<26 else 'page-26-before-appendix.txt')
        assert path.read_bytes().decode()==page.get_text(clip=clip)
        for block in page.get_text('dict',clip=clip)['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                match=re.match(r'^THEOREM (\d+)(?:\.| \()',text)
                if match:
                    assert line['spans'][0]['font']=='NimbusRomNo9L-Regu'
                    headings.append((n,match[1]))
    assert headings==[(7,'1'),(9,'2'),(10,'3'),(10,'4'),(11,'5'),(12,'6'),(13,'7'),(14,'8'),(14,'9'),(15,'10')]
    boundary=pdf[25].get_text(clip=fitz.Rect(0,150,pdf[25].rect.width,179))
    assert 'SUPPLEMENTARY MATERIAL' in boundary
    last=(ROOT/'evidence/page-26-before-appendix.txt').read_text()
    assert 'Acknowledgments.' in last and 'Funding.' in last and 'ANR-23-CE40-0018-01' in last
    assert 'SUPPLEMENTARY' not in last and 'APPENDIX' not in last
    assert len(inv['claims'])==len(data['claims'])==10
    for original, final in zip(inv['claims'],data['claims']):
        assert all(final[k]==v for k,v in original.items())
    claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Independent source-based graph expectations, not imported from the builder.
    local={n:[] for n in range(1,27)}
    local.update({13:[12],15:[12],17:[16],18:[12],19:[11,15,17],25:[24],26:[23,25]})
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in v] for k,v in local.items()}
    direct={
      '1':{1,2,3,5,6,8,11,13},'2':{1,2,3,5,6,8,11,14},
      '3':{1,2,3,5,6,9,11,15},'4':{1,2,3,5,6,10,11,12,15},
      '5':{1,2,3,5,9,15,17,18,19,20},'6':{1,3,4,5,7,8},
      '7':{1,2,3,5,7,9},'8':{1,2,3,5,7,9,21,22},
      '9':{1,3,4,5,7,8,21,23,24,25,26},'10':{1,2,5,7,10,12,15,21}}
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    expected_reach={
      '1':{1,2,3,5,6,8,11,12,13},'2':{1,2,3,5,6,8,11,14},
      '3':{1,2,3,5,6,9,11,12,15},'4':{1,2,3,5,6,10,11,12,15},
      '5':{1,2,3,5,9,11,12,15,16,17,18,19,20},'6':{1,3,4,5,7,8},
      '7':{1,2,3,5,7,9},'8':{1,2,3,5,7,9,21,22},
      '9':{1,3,4,5,7,8,21,23,24,25,26},'10':{1,2,5,7,10,12,15,21}}
    reach={}
    for n,c in claims.items():
        seen,stack=set(),list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in seen:seen.add(lid);stack.extend(members[lid]['depends_on'])
        reach[n]=seen
    assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected_reach.items()}
    assert {'D6','D7'}.isdisjoint(reach['5'])
    assert all('D6' not in reach[str(n)] for n in range(6,11))
    assert {'D2','D9','D11','D12','D15'}.isdisjoint(reach['9'])
    assert {'D3','D4','D6'}.isdisjoint(reach['10'])
    assert all({'D11','D12','D13','D14','D15','D21'}.isdisjoint(reach[n]) for n in ['6','7'])
    t={n:c['statement_original'] for n,c in claims.items()}
    b={lid:m['statement_original'] for lid,m in members.items()}
    assert 'truncated priors at $k=n$' in t['1'] and 'truncated' not in t['2']
    assert r'2\beta+2\nu+1' in t['2']
    assert r'\alpha\ge\beta+1/q' in t['3'] and '$q\ge1$' in t['3']
    assert r'$(\sigma_k)$' in t['4'] and r'$r\in[1,2]$' in t['4']
    assert r'w_l=l^{1+\kappa+\varepsilon}' in t['5'] and r'w_l=l^{(1+\kappa+\varepsilon)/2}' in t['5']
    assert '(14)' not in t['5'] and '(19)' not in t['5']
    assert t['6'].count('•')==2 and t['7'].count('•')==2
    assert 'for large enough' not in t['6'] and t['7'].count('for large enough')==2
    assert r'\frac{1+(1+\kappa)\beta}{2\beta+1}' in t['6']
    assert r'\frac{(1+\kappa)(1+\delta)\beta}{2\beta+1}' in t['6']
    assert r'(\log\log n)^{\frac2{1+2\beta}}' in t['7']
    assert r'\frac{(2+2\kappa)\beta}{1+2\beta}' in t['7']
    assert 'Theorem 7' in t['8'] and 'Theorem 6' in t['9']
    assert r'\|p_f-p_{f_0}\|_{G,1}' in t['9'] and r'M=M(\rho)>0' not in t['9']
    assert '(19)' in t['10'] and '(14)' not in t['10'] and '(6)' not in t['10']
    for n in ['1','2','3','4','10']:assert r'\mathcal L_n' in t[n]
    assert r'\mathcal K_l=\{0,\ldots,2^l-1\}' in b['D1']
    assert r'\sigma_k\zeta_k' in b['D1'] and r's_l\zeta_{lk}' in b['D1']
    assert r'\sigma_k=e^{-(\log k)^2}' in b['D2'] and r's_l=2^{-l^2}' in b['D2']
    assert r'\sigma_k=k^{-1/2-\alpha}' in b['D3'] and r's_l=2^{-l(1/2+\alpha)}' in b['D3']
    assert r'\sigma_k=e^{-a(\log k)^{1+\delta}}' in b['D4']
    assert 'symmetric, positive, bounded and decreasing' in b['D5'] and r'\log(1/h(x))\le c_1(1+\log^{1+\kappa}(1+x))' in b['D5']
    assert r'|x|^q h(x)dx<\infty' in b['D6']
    assert r'\bar H(x)' in b['D7'] and r'\int_x^\infty h(u)du\le c_2/x^2' in b['D7']
    assert r'\sum_{k\ge1}k^{2\beta}f_k^2\le L^2' in b['D8']
    assert r'2^{-l(1/2+\beta)}L' in b['D9']
    assert r'2^{rl(\beta+1/2-1/r)}' in b['D10'] and r'<L^r' in b['D10']
    assert 'conditional distribution' in b['D11']
    assert 'standard Brownian motion' in b['D12']
    assert r'\mathcal N(f_k,1/n)' in b['D13'] and r'\kappa_k\asymp k^{-\nu}' in b['D14']
    assert r'\mathcal N(f_{lk},1/n)' in b['D15']
    assert r'w_l\ge1' in b['D16'] and r'\lim_{l\to\infty}' in b['D17']
    assert r'\mathbb W' in b['D18'] and r'\mathcal N(0,1)' in b['D18']
    assert r'\tau:f\mapsto\sqrt n(f-X^{(n)})' in b['D19']
    assert 'bounded-Lipschitz metric' in b['D20']
    assert r'0<\rho\le1' in b['D21'] and b['D21'].count(r'\left(p_f^{(n)}(X)\right)^\rho')==2
    assert r'\frac{e^{f(x)}}{\int_0^1e^{f(u)}du}' in b['D22']
    assert r'\mathcal X=[0,1]^d' in b['D23'] and r'\Lambda(u)=1/(1+e^{-u})' in b['D24']
    assert r'h_f(x)=\Lambda(f(x))' in b['D25']
    assert r'h_f(x)^y(1-h_f(x))^{1-y}g(x)' in b['D26']
    assert all(members[f'D{i}']['source_kind']=='condition' for i in [5,6,7])
    assert members['D4']['source_kind']=='theorem_excerpt'
    a={p['local_id']:p['statement_original'] for p in ambient['unranked_auxiliary_passages']}
    assert 'Oversmoothed heavy-Tailed priors' in a['A1']
    assert r"\mathcal C^{\beta'}\subset C^\beta\subset\mathcal C^\beta" in a['A3']
    assert 'large enough order/regularity' in a['A5']
    assert r'\sqrt l' in a['A7'] and r'$L^1(G)$ norm on $\mathcal X$' in a['A8']
    assert '(4)–(6) (or (4)–(5))' in a['A9']
    assert set(ambient['branch_resolution'])==set(claims)
    assert ambient['branch_resolution']['8']['referenced_theorem']==PID+'/T7'
    assert ambient['branch_resolution']['9']['referenced_theorem']==PID+'/T6'
    assert len(ambient['branch_resolution']['10'])==1
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
    assert counts==dict(theorems=10,interfaces=26,source_members=26,direct_theorem_uses=82,related_theorem_connections=87,unranked_auxiliary_passages=10)
    assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==23
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:
        assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='All ten complete original Theorems 1-10 were visually compared on pages 7, 9-15. Independent actual-heading enumeration covers main-text pages 1-25 and the upper portion of page 26, excluding proof headings, references, remarks and appendix content.',
        source_passages='Twenty-six supporting passages and ten auxiliary passages were visually checked on pages 3-9 and 11-14. They preserve original prior constructions, scale alternatives, density and tail conditions, coefficient balls, Gaussian experiments, multiscale spaces, posterior transformations and classification definitions.',
        dependencies='Independent reconstruction verifies 82 direct uses and 87 related connections. Theorems 6 and 7 are prior-mass statements without a sampling experiment. Their explicitly referenced parameters and rates are unpacked in Theorems 9 and 8 respectively. Prior examples preceding transformation formulas do not fix a branch in every use.',
        names_and_highlights='Every interface retains a source-derived natural-language term and meaning-bearing original notation or phrase for highlighting. Repeated source keywords do not establish equivalence of scale choices. Explanations cover all related theorems and their paper-local paths.',
        notation='Visual and font checks preserve calligraphic smoothness balls and logarithmic multipliers, the barred survival function, blackboard Gaussian noise, the affine mapsto arrow, and distinct classical Hölder versus Hölder-Zygmund notation. Strict Besov and non-strict Sobolev/Hölder balls remain separate.',
        limits='Twenty-three source notes record the level-zero weight discrepancy, Theorem 4 scale index, Theorem 9 prior-reference and norm-domain ambiguities, one-dimensional versus multivariate conventions, and the effective positive rho range. Original quotes remain unchanged; no mathematical repair, proof certification or appendix import is claimed.',
        reproduction='The retained per-paper scripts reproduced all six content artifacts byte-for-byte in an empty directory. Source identity, inventory handoff, semantic invariants, graph reach, branch choices, math fragments and both schema validations passed. Reproduction itself does not renew source review.')
    write('evidence/manual-findings.json',findings)
    pages=[1,3,4,5,6,7,8,9,10,11,12,13,14,15,26]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png'),**({'before_main_text_end':True} if n==26 else {})) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
      source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=59,main_text_last_pdf_page=26,provenance_path='evidence/source-provenance.json'),
      enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent actual-heading enumeration and visual comparison of every original theorem body.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
      counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),
      artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},
      source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,
      review_limits=['Source transcription and statement-dependency review, not proof certification.','Supplement introduction and appendix bodies excluded.','Explicit source ambiguities are recorded without silently changing their mathematics.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,
      registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=59,source_version=paper['version'],registered_version_alias=entry['version'],registered_url_alias=entry['source_url'],
      checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},
      reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,
      reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
