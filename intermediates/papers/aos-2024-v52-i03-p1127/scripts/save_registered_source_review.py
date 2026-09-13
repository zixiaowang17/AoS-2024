"""Pin the manual PDF review; machine checks establish provenance and consistency."""
import datetime
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
    assert len(pdf) == entry['pdf_pages'] == 153
    assert 'arXiv:2203.13776v3' in pdf[0].get_text()
    assert all(s in pdf[0].get_text().lower() for s in ['johannes brutsche','angelika rohde','16 apr 2024'])
    paper=inv['papers'][0]
    assert paper['version']=='arXiv:2203.13776v3'
    assert paper['source_url']=='https://arxiv.org/pdf/2203.13776v3'
    assert paper['title'].upper() in ' '.join(pdf[0].get_text().split())
    assert digest(source)==paper['pdf_sha256']
    assert paper['main_text_last_pdf_page']==31
    assert paper['main_text_boundary']['shared_page_with_appendix'] is False
    data=census
    ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    assert 'MR1385671' in pdf[30].get_text()
    boundary=pdf[31].get_text(clip=fitz.Rect(0,125,pdf[31].rect.width,180))
    assert 'SUPPLEMENT TO' in boundary and 'DIFFUSIONS' in boundary
    labels=[];mentions=[]
    for n in range(31):
        page=pdf[n];assert (ROOT/'evidence/revalidation'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans']).strip();m=re.match(r'^Theorem\s+(\d+\.\d+)',text)
                if m:
                    is_heading=any(s['font']=='CMCSC10' and 'Theorem' in s['text'] for s in line['spans'])
                    (labels if is_heading else mentions).append((n+1,m[1]))
    assert labels==[(9,'3.1'),(12,'4.1'),(15,'5.1'),(16,'5.2'),(16,'5.3'),(17,'5.4'),(19,'6.1'),(20,'6.3'),(21,'6.5'),(23,'7.1')]
    assert mentions==[(6,'1.16'),(9,'3.1'),(10,'3.1')]
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
    assert len(inv['claims'])==len(data['claims'])==10
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
            if lid in seen:continue
            seen.add(lid);stack.extend(byid[lid]['depends_on'])
        reach[n]=seen
    # Independently specified from the mathematical statement-resolution review.
    # The deterministic map has no experiment; the fractional pair has no stationary start;
    # arbitrary-test lower bounds have no proposed statistic or calibration dependency.
    expected={
     '3.1':{1,2,3,4,5,7,8,9,10,11},
     '4.1':{1,2,3,4,5,7,8,9,10,11,15,16,17,18,26},
     '5.1':{1,2,3,4,5,15,21,22,23,24,25},
     '5.2':{1,2,3,4,5,7,8,9,10,11,15,16,17,18,19,20,21,22,23,24,25,27},
     '5.3':{1,2,3,4,5,7,8,9,10,11,15,16,17,18,19,20,21,22,23,24,25,27},
     '5.4':{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,21,22,23,24,25},
     '6.1':{5,7,9,10,11,16,26,28,29,30,31,32,33},
     '6.3':{1,2,5,7,9,10,11,16,22,26,28,29,30,31,32,33,34,35,36,37},
     '6.5':{1,2,3,5,15,21,22,23,24,25,34,35,36,37},
     '7.1':{1,2,3,4,5,7,8,9,10,11,12,26,38}}
    direct={
     '3.1':{2,4,5,7,8,9,10,11},'4.1':{2,3,4,7,9,11,15,17,18,26},
     '5.1':{2,4,15,21,22,23,24},'5.2':{2,4,15,20,21,22,23,24,25,27},
     '5.3':{2,4,15,20,21,22,23,24,27},'5.4':{2,4,6,14,21,22,23,24,25},
     '6.1':{30,33},'6.3':{2,22,30,33,37},'6.5':{2,15,21,22,23,24,37},
     '7.1':{2,3,4,7,9,11,12,26,38}}
    assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    for x in data['interfaces']:
        lids={m['local_id'] for m in x['members']}
        assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
        assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
    for n in ['6.1','6.3','6.5']:assert 'D4' not in reach[n]
    assert reach['6.1'].isdisjoint({f'D{i}' for i in [1,2,3,4,34,35,36,37]})
    for n in ['5.1','6.5']:assert reach[n].isdisjoint({f'D{i}' for i in [8,12,13,14,17,18,19,20,26,27,28,29,30,31,32,33]})
    assert 'D15' not in reach['7.1'] and 'D26' not in reach['3.1']
    t={n:c['statement_original'] for n,c in claims.items()};b={lid:m['statement_original'] for lid,m in byid.items()};a={x['local_id']:x['statement_original'] for x in ambient['auxiliary_source_passages']}
    assert all(len(c['evidence'])==1 for c in claims.values())
    assert r'\mathbb1_{[-A,A]}(X_s)^2' in t['3.1'] and 'asymptotically tight' in t['3.1']
    assert r'$0/0:=0$ in the argument' in t['3.1'] and r'\mathbb1_{\{r>0\}}' in t['3.1']
    assert r'\|K\|_{[-1,1]}\le1' in t['3.1'] and 'non-negative' not in t['3.1']
    assert r'\Sigma(C/2-\eta,A,\gamma+\eta/\sigma^2,\sigma)' in t['4.1']
    assert r'\limsup_{T\to\infty}\sup_{b\in H_0(b_0,\eta)}' in t['4.1']
    assert r'4\sqrt{A\eta/\sigma^2}\ge r' in t['4.1']
    assert 'U_1:=' in t['4.1'] and 'U_2:=' in t['4.1']
    for sign in ['+','-']:
        assert 'q_{b_0'+sign+r'\eta}' in t['4.1']
        assert r'\|\mathbb1_{[-A,A]}\sqrt{q_{b_0'+sign+r'\eta}}\|_{L^2}^2' in t['4.1']
    assert r'\mathbb E_b[\psi_T]\le\alpha' in t['5.1']
    assert r'(1-\epsilon_T)c_*\delta_T' in t['5.1'] and r'\epsilon_T\sqrt{\log T}=\infty' in t['5.1']
    assert r'\eta>0' in t['5.2'] and r'\|K\|_{[-1,1]}=1' in t['5.2']
    assert r'(1+\epsilon_T)c\delta_T' in t['5.2'] and r'$K=K_\beta$' in t['5.2'] and r'$c=c_*$' in t['5.2']
    assert r'(b,L)\in[\beta_1,\beta_2]\times[L_1,L_2]' in t['5.3']
    assert 'sharp adaptivity' in t['5.3'] and r'\inf_{L\in[L_1,L_2]}' in t['5.3']
    assert r'(1-\epsilon_T)c_*\delta_T' in t['5.4'] and '(1+' not in t['5.4']
    assert 'given in (3.6)' in t['5.4'] and r'b\in H_{\ne}' in t['5.4']
    assert t['6.1']==r'The mapping $\widetilde T_T^\eta:D_{A,T}\longrightarrow\mathbb R$ is continuous with respect to the topology of uniform convergence.'
    assert 'for $T$ sufficiently large' in t['6.3'] and t['6.3'].count(r'\liminf')==4
    assert r'\middle|\,X^{H,b},X^b\in D_{A,T}' in t['6.3']
    assert r'\delta(T):=\delta(T,\epsilon)>0' in t['6.5']
    assert r'\sup_{H:\,|H-\frac12|<\delta(T)}\sup_{\psi_T^H}\inf_' in t['6.5']
    assert r'\mathbb E\left[\psi_T^H(X^{H,b})\right]\le\alpha+\epsilon' in t['6.5']
    assert 'where $\\sup_{\\psi_T^H}$ is taken over tests' in t['6.5']
    assert 'two-sided Brownian motion' in t['7.1'] and r'W$ on $[-A,A]' in t['7.1']
    assert r'Z_b(y,h):=' in t['7.1'] and r'\sigma_{b,\max}:=' in t['7.1']
    assert r'\sup_{b\in\Sigma(C,A,\gamma,\sigma)}' in t['7.1'] and r'd_{BL}^b' in t['7.1']
    assert 'initial condition $\\xi$ independent of $W$' in b['D1']
    assert 'stationary' not in b['D1'] and r'X_0=\xi' in b['D1']
    assert r'\frac{b(x)}{\sigma^2}\operatorname{sign}(x)\le-\gamma' in b['D2']
    assert r'|b(x)|\le C(1+|x|)' in b['D2'] and 'local Lipschitz' in b['D2']
    assert r'\frac1{C_{b,\sigma}}' in b['D3'] and r'\int_0^x f(y)dy=-\int_x^0 f(y)dy' in b['D3']
    assert r'\xi\sim\mu_b' in b['D4'] and r'\mathbb P_b' in b['D4']
    assert r'\sup_{z\in I}|f(z)|' in b['D5']
    assert r'\|b-b_0\|_{[-A,A]}=0' in b['D6'] and r'\Sigma(C/2,A,\gamma,\sigma)' in b['D6']
    assert r'K\left(\frac{x-y}{h}\right)' in b['D7'] and r'\frac1h' not in b['D7']
    assert 'if the denominator equals zero' in b['D8'] and r'\int_0^T K_{y,h}(X_s)dX_s' in b['D8']
    assert r'\cap(\mathbb Q\times\mathbb Q)' in b['D9'] and r'h\in(0,A]' in b['D9']
    assert r'\mathbb1_{[-A,A]}(X_s)^2' in b['D10'] and r'\frac1T' in b['D10']
    assert r'\Upsilon(r):=(2\log(1/r))^{\frac12}' in b['D11']
    assert r'\tag{3.4}' in b['D12'] and r'\Lambda' not in b['D12']
    assert r'\min\left\{r\in\mathbb R\mid\mathbb P_{b_0}' in b['D13']
    assert r'T_T^{b_0}(X)>\kappa_{T,\alpha}^{\ne b_0}' in b['D14']
    assert r'\|b-b_0\|_{[-A,A]}\le\eta' in b['D15'] and r'\|b-b_0\|_{[-A,A]}>\eta' in b['D15']
    assert r'\eta\int_0^T K_{y,h}(X_s)ds' in b['D16'] and 'read as zero' in b['D16']
    assert r'\Lambda_{T,y,h}^\eta(X)' in b['D17'] and r'\tag{4.3}' in b['D17']
    assert b['D18']=='where $U_1\\vee U_2$'+t['4.1'].split('where $U_1\\vee U_2$')[1]
    assert r'\min\left\{r\in\mathbb R:' in b['D19'] and r'\le r\right)\ge1-\alpha' in b['D19']
    assert r'T_T^\eta(X)>\kappa_{\eta,\alpha}' in b['D20']
    assert r'\inf_{\widetilde b\in H_0(b_0,\eta)}' in b['D21'] and r'\frac\beta{2\beta+1}' in b['D21']
    assert r'\left(|b(x)-b_0(x)|-\eta\right)' in b['D21'] and r'_+' not in b['D21']
    assert 'maximal integer strictly smaller than' in b['D22'] and 'for each $k=0,\\ldots,\\lfloor\\beta\\rfloor$' in b['D22']
    assert r'\delta_T=\delta_T(\beta)' in b['D23']
    assert r'2L^{\frac1\beta}' in b['D24'] and r'\|K_\beta\|_{L^2}^2' in b['D24']
    assert r'K(0)\ge1' in b['D25'] and r'\mathbb1_{\{|x|\le1\}}\left(1-|x|^\beta\right)' in b['D25']
    assert 'continuous kernel' in b['D26'] and r'\le1' in b['D26']
    assert 'continuous' not in b['D27'] and r'\|K\|_{[-1,1]}=1' in b['D27']
    assert 'continuously differentiable' in b['D28']
    assert r'\mathcal C([0,T])' in b['D29'] and r'\int_{f(0)}^{f(T)}K_{y,h}(z)dz-\frac{\sigma^2}2' in b['D29']
    assert r'-A,A\in f([0,T])' in b['D30'] and r'\mathcal C([0,T])' in b['D30']
    assert r'\widetilde I_T(f)' in b['D31'] and r'\tag{6.1}' in b['D31']
    assert r'h\ge h_{\min}(T)' in b['D32'] and 'Appendix B' in b['D32']
    assert r'\Lambda_{T,y,h}^\eta(X)' in b['D33'] and r'\sup_{(y,h)\in\mathcal T_T}' in b['D33']
    assert r't^{2H}+s^{2H}-|t-s|^{2H}' in b['D34']
    assert r'\int_0^t K_H(t,s)dW_s' in b['D35'] and '(I.8)' in b['D35']
    assert r'X_0^H=x_0' in b['D36'] and 'stationary' not in b['D36']
    assert 'initial condition $x_0$' in b['D37'] and 'Lipschitz continuous' in b['D37']
    assert 'Appendix F.1' in b['D38'] and 'distribution of $X$ on $b$' in b['D38']
    assert r'\mathcal C(K)' in a['A1'] and 'Lebesgue measure' in a['A1']
    assert r'\eta=0' in a['A4'] and 'Remark H.6 and H.7' in a['A6']
    assert r'\mathcal F_{BL}(E)' in a['A8'] and 'closed unit ball' in a['A8']
    def has_span(n,font,fragment):
        return any(s['font']==font and fragment in s['text'] for block in pdf[n-1].get_text('dict')['blocks'] for line in block.get('lines',[]) for s in line['spans'])
    assert has_span(7,'CMSY10','C') and has_span(18,'CMSY10','C')
    assert has_span(25,'CMSY10','F') and has_span(19,'CMMI10','D')
    assert has_span(14,'CMSY10','H') and has_span(8,'CMSY10','T')
    counts=dict(theorems=10,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_source_passages']))
    assert counts==dict(theorems=10,interfaces=38,source_members=38,direct_theorem_uses=76,related_theorem_connections=160,unranked_auxiliary_passages=9),counts
    assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==32
    assert len(ambient['excluded_references'])==5
    for item in data['claims']+members+ambient['auxiliary_source_passages']:
        assert all(1<=e['page']<=31 for e in item['evidence'])
        fragments=[item['statement_original']]
        for ctx in item.get('naming_context',[]):
            assert all(1<=e['page']<=31 for e in ctx['evidence']);fragments.append(ctx['text'])
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
    expected_edges={1:[],2:[],3:[2],4:[1,3],5:[],6:[2,5],7:[],8:[1,7],9:[],10:[7],11:[],12:[8,9,10,11],13:[4,12],14:[12,13],15:[2,5],16:[7],17:[8,9,10,11,16],18:[3,7,9,11],19:[18],20:[17,19],21:[15,3,5],22:[],23:[],24:[25],25:[22],26:[5],27:[5],28:[26],29:[7,28],30:[],31:[29,30,7],32:[9],33:[31,32,16,10,11],34:[],35:[34],36:[34],37:[1,2,35,36],38:[]}
    assert {lid:m['depends_on'] for lid,m in byid.items()}=={f'D{k}':[f'D{i}' for i in ids] for k,ids in expected_edges.items()}
    for lid,m in byid.items():
        n=int(lid[1:])
        assert m['source_kind']==('assumption' if n in {1,4,36} else 'theorem_excerpt' if n in {10,11,18} else 'condition' if n in {26,27,28} else 'source_passage' if n==38 else 'definition')
    for it in census['interfaces']:
        lid=it['members'][0]['local_id']
        for relation in it['related_theorems']:
            path=relation['via_local_ids']
            assert path[0] in claims[relation['claim_id'].split('/T')[-1]]['depends_on'] and path[-1]==lid
            for x,y in zip(path,path[1:]):assert y in byid[x]['depends_on']
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
    pages = [1,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,24,25,31]
    evidence = [dict(page=p, path=f'evidence/revalidation/page-{p:02}.png', sha256=digest(ROOT / f'evidence/revalidation/page-{p:02}.png')) for p in pages]
    evidence.append(dict(page=32, path='evidence/revalidation/appendix-heading.png', sha256=digest(ROOT / 'evidence/revalidation/appendix-heading.png'), scope='Supplement title only; supplement body excluded.'))
    review = dict(schema_version='registered-paper-source-review-v1', paper_id=PID, status='complete',
                  method='source_content_revalidation', reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  registered_pdf_path=str(source), registered_pdf_sha256=entry['sha256'], registered_pdf_pages=len(pdf),
                  source_version=audit['source']['version'],
                  checks={k: True for k in ['theorem_inventory', 'original_statements', 'source_passages', 'dependencies', 'names_and_highlights']},
                  reviewed_artifacts={name: digest(ROOT / name) for name in ['paper-audit.json', 'theorem-inventory.json', 'ranked-interfaces.json']},
                  findings=findings, evidence=evidence, independent_validation=results,
                  reproduction_check=dict(path='evidence/revalidation/rebuild-check.json', sha256=digest(ROOT / 'evidence/revalidation/rebuild-check.json')))
    (ROOT / 'registered-source-review.json').write_text(json.dumps(review, indent=2, ensure_ascii=False) + '\n')
    print('Registered source reviewed: 10 Theorems, 38 source entries, 160 relationships; six artifacts reproducible.')


if __name__ == '__main__':
    main()
