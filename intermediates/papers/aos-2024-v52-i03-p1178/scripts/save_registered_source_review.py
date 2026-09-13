"""Pin the manual PDF review; machine checks establish provenance and consistency."""
import datetime
import itertools,math
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

import fitz

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
PID = ROOT.name


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = Path(subprocess.check_output([sys.executable, str(REPO / 'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    register = json.loads((REPO / 'corpus/aos/2024/local-pdf-manifest.json').read_text())
    entry = next(p for p in register['papers'] if p['paper_id'] == PID)
    audit = json.loads((ROOT / 'paper-audit.json').read_text())
    inv = json.loads((ROOT / 'theorem-inventory.json').read_text())
    census = json.loads((ROOT / 'ranked-interfaces.json').read_text())
    assert digest(source) == entry['sha256'] == audit['source']['pdf_sha256']
    pdf = fitz.open(source)
    assert len(pdf) == entry['pdf_pages'] == 73
    assert 'arXiv:2305.11672v2' in pdf[0].get_text()
    assert all(s in pdf[0].get_text().lower() for s in ['torben sell','thomas b. berrett','timothy i. cannings','2 may 2024'])
    paper=inv['papers'][0]
    assert paper['version']=='arXiv:2305.11672v2'
    assert paper['source_url']=='https://arxiv.org/pdf/2305.11672v2'
    assert paper['title'].upper() in ' '.join(pdf[0].get_text().split())
    assert 'Submitted to the Annals of Statistics' in pdf[0].get_text()
    assert digest(source)==paper['pdf_sha256']
    assert paper['main_text_last_pdf_page']==22
    assert paper['main_text_boundary']['shared_page_with_appendix'] is False
    data=census
    ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    assert 'Funding.' in pdf[21].get_text()
    assert 'S1. Additional results and proofs of the claims in Section 2' in pdf[22].get_text(clip=fitz.Rect(90,55,515,83))
    labels=[];mentions=[]
    for n in range(1,23):
     page=pdf[n-1];assert (ROOT/'evidence/revalidation'/f'page-{n:02}.txt').read_bytes().decode('utf8')==page.get_text()
     for block in page.get_text('dict')['blocks']:
      for line in block.get('lines',[]):
       text=''.join(s['text'] for s in line['spans']).strip()
       m=re.match(r'^THEOREM\s+(\d+)\.',text)
       if m:labels.append((n,m[1]))
       m=re.match(r'^Theorem\s+(\d+)',text)
       if m:mentions.append((n,m[1]))
    assert labels==[(9,'1'),(12,'2')] and mentions==[(2,'1'),(9,'1'),(12,'1')]
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
    assert len(inv['claims'])==len(data['claims'])==2
    for original,final in zip(inv['claims'],data['claims']):
     for key in original:assert original[key]==final[key],(original['claim_id'],key)
    members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members}
    claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
    extraction=json.loads((ROOT/'interface-extraction.json').read_text())
    assert {m['local_id']:m for x in extraction['interfaces'] for m in x['members']}==byid
    reach={}
    for n,c in claims.items():
     seen=set();stack=c['depends_on'][:]
     while stack:
      lid=stack.pop()
      if lid not in seen:seen.add(lid);stack.extend(byid[lid]['depends_on'])
     reach[n]=seen
    # Independently reviewed prerequisites: the minimax result does not consume HAM or Definition3+.
    expected={'1':set(range(1,28)),'2':set(range(1,31))}
    direct={'1':{1,3,5,6,9,15,19,21,24,25,26,27},'2':{1,3,5,9,15,16,19,21,25,26,27,28,30}}
    assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    for x in data['interfaces']:
     lids={m['local_id'] for m in x['members']}
     assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
     assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
    assert reach['1'].isdisjoint({'D28','D29','D30'})
    assert not set(byid['D28']['depends_on'])&{'D11','D14','D17','D24','D30'}
    t={n:c['statement_original'] for n,c in claims.items()};b={lid:m['statement_original'] for lid,m in byid.items()};a={x['local_id']:x['statement_original'] for x in ambient['auxiliary_source_passages']}
    assert all(len(c['evidence'])==1 for c in claims.values())
    for text in t.values():
     assert r'\boldsymbol\gamma\in[0,\infty)^d' in text and r'\boldsymbol\beta\in(0,1]^d' in text
     assert r'\Omega_\star\in\mathcal I(\{0,1\}^d)\setminus\{\{\mathbf0_d\},\emptyset\}' in text
     assert r'O_1=o_1,\ldots,O_n=o_n' in text
     assert r'\gamma_\omega(2\beta_\omega+d_\omega)+\alpha\beta_\omega' in text
     assert r'\log_+^{\frac{1+\alpha}2}' in text
    assert r'c_{\mathrm E}\in[0,1/4]' in t['1'] and r'C_{\mathrm L}>1' in t['1']
    assert r'\max_{\omega\in\Omega_\star}\alpha\beta_\omega\le\min_{\omega\in\Omega_\star}d_\omega' in t['1']
    assert r'(8d)^{(1+d)(1+\|\boldsymbol\gamma\|_\infty)}' in t['1']
    assert r'1+6\cdot4^{d/\beta_\omega}' in t['1']
    assert r'\inf_{\widehat C\in\mathcal C_n}\sup_{Q\in\mathcal Q\prime' not in t['1']
    assert r"\inf_{\widehat C\in\mathcal C_n}\sup_{Q\in\mathcal Q'_{\mathrm{Miss}}}" in t['1']
    assert r'\cdot R+\mathbb1_{\{\Omega_\star\cap\mathcal N^c\ne\emptyset\}}' in t['1']
    assert r'c_{\mathrm E}\in(0,1/4]' in t['2'] and r'C_{\mathrm L}\ge1' in t['2']
    assert r'\Omega_\star\subseteq\mathcal N' in t['2']
    assert r'\log^{\frac{4(\gamma_\omega(2\beta_\omega+d_\omega)+\alpha\beta_\omega)}{\beta_\omega\gamma_\omega}}' in t['2']
    assert r'\omega\in U(\Omega_\star)\cap\mathcal N' in t['2']
    assert r'Q\in\mathcal Q^+_{\mathrm{Miss}}' in t['2'] and r'\widehat C_{\mathrm{HAM}}' in t['2']
    assert r'(16|\Omega_\star|)' not in t['2'] and r'4^{d/\beta_\omega}' not in t['2']
    assert r'\omega\ne\omega\prime' not in b['D1'] and r'd_\omega:=\|\omega\|_1' in b['D1']
    assert r'x^\omega:=x\odot\omega+\mathbf0_d\odot(\mathbf1_d-\omega)\in\mathbb R^d' in b['D2']
    assert r'P\equiv P_Q' in b['D3'] and 'observation indicator' in b['D3']
    assert r'\eta(x):=\mathbb P_P(Y=1\mid X=x)' in b['D4']
    assert 'independent and identically distributed triples' in b['D5'] and 'fully observed test point' in b['D5']
    assert 'measurable function' in b['D6'] and r'\mathcal C_n' in b['D6']
    assert r'\mid D_n' in b['D7']
    assert r'C^{\mathrm{Bayes}}(x)=\mathbb1_{\{\eta(x)\ge1/2\}}' in b['D8']
    assert r'|2\eta(x)-1|' in b['D9'] and r'\mathcal E_P' in b['D9']
    assert r'\mathbb P_Q(O=o)>0' in b['D10'] and r'\omega\preceq o' in b['D10']
    assert r'\sum_{\omega\prime' not in b['D11'] and r'\mid X^\omega=x^\omega' in b['D11']
    assert r'f_{\mathbf0_d}(x)' in b['D11'] and r'\tag{6}' in b['D11']
    assert r'\mu_\omega(A)=\mu' in b['D12'] and r'\mu_{\omega\mid o}(A)=\mathbb P_Q' in b['D13']
    assert r'\sigma_\omega^2:=\min_{o\in\mathcal O:o\succeq\omega}' in b['D14'] and r'\{f_\omega^2(X)\mid O=o\}' in b['D14']
    assert 'incomparable' in b['D15'] and r'\mathcal I' in b['D15']
    assert r'U(\Omega):=\{0,1\}^d\setminus\{\Omega\cup L(\Omega)\}' in b['D16']
    assert r'\sigma_\omega^2\ge c_{\mathrm E}' in b['D17'] and r'\omega\in U(\Omega_\star)' in b['D17']
    assert r'\inf_{r\in(0,1)}' in b['D18'] and r'\frac{\nu\big(B_r(x)\big)}{r^s}' in b['D18']
    assert r'\gamma_\omega:=\min\{\gamma_j:\omega_j=1\}' in b['D19']
    assert r'\mu_\omega\left(' in b['D20'] and r'\rho_{\mu_{\omega\mid o},d_\omega}(x)<\xi' in b['D20']
    assert r'\beta_\omega:=\min\{\beta_j:\omega_j=1\}' in b['D21']
    assert r'\|x_1^\omega-x_2^\omega\|_2^{\beta_\omega}' in b['D22']
    assert r'|\eta(x)-1/2|<t' in b['D23'] and r'0<|\eta' not in b['D23']
    assert all(s in b['D24'] for s in [r'\mathcal Q_{\mathrm E}',r'\mathcal Q_{\mathrm L}',r'\mathcal P_{\mathrm S}',r'\mathcal P_{\mathrm M}'])
    assert r'\mathbb1_{\{\omega\preceq o_i\}}' in b['D25'] and r'n_\omega>0' in b['D26']
    assert b['D27']==r'Finally, for $x\in\mathbb R$, we write $\log_+(x):=\log(x\vee e)$.'
    assert re.findall(r'^(\d+):',b['D28'],re.M)==[str(i) for i in range(1,22)]
    assert r'\widehat f_{\mathbf0}(\cdot)' in b['D28'] and r'1+\lfloor n_\omega^' in b['D28']
    assert r'2^{-4}\cdot n_\omega^{-\frac{\beta_\omega\gamma_\omega}{2[' in b['D28']
    assert r'(X_{(n_\omega)}^\omega(x),Y_{(n_\omega)_\omega}(x))' in b['D28']
    assert r'U(\{\omega\})\cap\widehat\Omega=\emptyset' in b['D28']
    assert r'\widehat\sigma_\omega^2\ge\tau_\omega' in b['D28']
    assert r'\widehat\Omega\cup L(\widehat\Omega)' in b['D28']
    assert r'\widehat\eta(x_0)\ge1/2' in b['D28']
    assert '(9) holds and' in b['D29'] and r'\max_{\widetilde o\in\mathcal O:\omega\preceq\widetilde o}\mu_{\omega\mid\widetilde o}' in b['D29']
    assert 'replace' in b['D30'] and r'\mathcal Q_{\mathrm L}^+' in b['D30']
    assert 'open Euclidean ball' in a['A2'] and r'\omega\prime' not in a['A5']
    assert 'orthogonal' in a['A6']
    # Check the two recorded algorithm ambiguities with elementary source-formula examples.
    universe=set(itertools.product([0,1],repeat=2))
    def le(x,y):return all(a<=b for a,b in zip(x,y))
    def U(x):return {y for y in universe if not le(y,x)}
    assert (1,0) in U((0,1)) and not le((0,1),(1,0))
    assert 1+math.floor(1**(2/3))==2
    counts=dict(theorems=2,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_source_passages']))
    assert counts==dict(theorems=2,interfaces=30,source_members=30,direct_theorem_uses=25,related_theorem_connections=57,unranked_auxiliary_passages=6),counts
    assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==27
    for item in data['claims']+members+ambient['auxiliary_source_passages']:
        assert all(1<=e['page']<=22 for e in item['evidence'])
        fragments=[item['statement_original']]
        for key in ['naming_context','application_context']:
            for ctx in item.get(key,[]):
                assert all(1<=e['page']<=22 for e in ctx['evidence']);fragments.append(ctx['text'])
        for text in fragments:
            assert not re.search(r'[\u4e00-\u9fff]',text)
            assert text.count('$')%2==0 and text.count('\\[')==text.count('\\]')
            for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
                depth=0
                for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                    depth+=1 if brace=='{' else -1
                    assert depth>=0,('unbalanced',item)
                assert depth==0,('unbalanced',item)
    for x in data['interfaces']:
        assert x['related_theorems'] and set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
        assert '$' not in x['name']
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors) and all(s in linked for s in selectors)
        for k in x['source_keywords']:
            m=byid[k['local_id']];texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])]
            assert any(k['source_text'] in text for text in texts)
    local={1:[],2:[],3:[],4:[3],5:[3,2],6:[5],7:[3,5,6],8:[4],9:[7,8,4],10:[3,4,2,1],11:[4,2,1],12:[10,4,2],13:[10,2,1],14:[10,11,1],15:[1],16:[15,1],17:[10,14,11,15,16],18:[],19:[],20:[10,12,13,18,19,1],21:[],22:[11,21,2,4],23:[4],24:[17,20,22,23,15,3],25:[1],26:[25],27:[],28:[5,2,1,19,21,25,26,16],29:[20,13,18,19,1],30:[24,29]}
    assert {lid:m['depends_on'] for lid,m in byid.items()}=={f'D{k}':[f'D{i}' for i in ids] for k,ids in local.items()}
    assert all(m['source_kind']=='definition' for m in members)
    assert len(ambient['excluded_references'])==3
    for it in census['interfaces']:
        lid=it['members'][0]['local_id']
        for rel in it['related_theorems']:
            path=rel['via_local_ids'];assert path[0] in claims[rel['claim_id'].split('/T')[-1]]['depends_on'] and path[-1]==lid
            for x,y in zip(path,path[1:]):assert y in byid[x]['depends_on']
    history=ROOT/'review-history/before-naming-context-escape-correction'
    previous=json.loads((history/'paper-audit.json').read_text())
    assert digest(history/'paper-audit.json')==audit['registered_source_correction']['previous_audit_sha256']
    for item in previous['artifacts'].values():assert digest(history/item['path'])==item['sha256']
    def repair_context(value):
        if isinstance(value,dict):return {k:repair_context(v) for k,v in value.items()}
        if isinstance(value,list):return [repair_context(v) for v in value]
        if isinstance(value,str):return value.replace('\x08oldsymbol',r'\boldsymbol')
        return value
    for name in ['theorem-inventory.json','source-passages.json','interface-extraction.json','ambient-prerequisites.json','unfinalized-census.json','ranked-interfaces.json']:
        assert repair_context(json.loads((history/name).read_text()))==json.loads((ROOT/name).read_text())
    def check_strings(value):
        if isinstance(value, dict):
            for v in value.values(): check_strings(v)
        elif isinstance(value, list):
            for v in value: check_strings(v)
        elif isinstance(value, str):
            assert not any(ord(c)<32 and c != '\n' for c in value), repr(value)
    for name in ['theorem-inventory.json','source-passages.json','interface-extraction.json','ambient-prerequisites.json','unfinalized-census.json','ranked-interfaces.json']:
        check_strings(json.loads((ROOT/name).read_text()))
    for it in census['interfaces']:
        for member in it['members']:
            selectors = member.get('highlight_symbols', []) + member.get('highlight_phrases', [])
            original = member['statement_original'] + '\n' + member['local_label']
            related = [c['statement_original'] for c in census['claims'] if c['claim_id'] in it['theorem_explanations']]
            assert any(s in original for s in selectors), member['local_id']
            assert all(any(s in t for t in [original] + related) for s in selectors), member['local_id']
    for item in audit['artifacts'].values():
        assert digest(ROOT / item['path']) == item['sha256']
    rebuild = json.loads((ROOT / 'evidence/revalidation/rebuild-check.json').read_text())
    assert len(rebuild['comparisons']) == 6
    for item in rebuild['comparisons']:
        assert item['matches_saved_bytes'] is True
        assert item['saved_sha256'] == item['regenerated_sha256'] == digest(ROOT / item['artifact'])
    validator = Path('skills/statistical-paper-census/scripts/validate_census.py')
    results = []
    for name in ['theorem-inventory.json', 'ranked-interfaces.json']:
        result = subprocess.run([sys.executable, '-B', str(validator), str(ROOT / name)], text=True, capture_output=True, check=True)
        results.append(dict(artifact=name, returncode=result.returncode, stdout=result.stdout))
    findings = json.loads((ROOT / 'evidence/revalidation/manual-findings.json').read_text())
    pages = [1,3,4,5,6,7,8,9,10,11,12,19,22]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=23, path='evidence/revalidation/appendix-heading.png', sha256=digest(ROOT / 'evidence/revalidation/appendix-heading.png'), scope='Supplementary S1 heading only; body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 2 Theorems, 30 source entries, 57 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
