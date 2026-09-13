"""Independently check the dynamic-volatility census against its pinned main text."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());PDF=Path(prov['cached_pdf']);WORK=Path(prov['working_pdf']).parent
for name in ['theorem-inventory.json','ranked-interfaces.json']:
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],check=True)
inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());review=json.loads((ROOT/'inventory-review.json').read_text())
assert digest(PDF)==paper['pdf_sha256']==prov['pdf_sha256']==digest(WORK/'source.pdf')
assert review['status']=='complete' and review['source_checked'] and digest(ROOT/'theorem-inventory.json')==review['inventory_sha256']
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==49
assert paper['main_text_last_pdf_page']==36 and not paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split())
assert paper['title'].lower() in first.lower()
for author in prov['authors']:assert author in first
assert '2211.10203v2' in first and '21 Nov 2022' in first and 'November 18, 2022' in first
assert paper['source_url']=='https://arxiv.org/pdf/2211.10203v2' and paper['version']=='arXiv:2211.10203v2'
assert 'Zheng' in pdf[35].get_text() and 'Supplement to' in pdf[36].get_text(clip=fitz.Rect(0,0,pdf[36].rect.width,143))
labels=[];mentions=[];assumptions=[]
for n in range(36):
    page=pdf[n];assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text()
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();m=re.match(r'Theorem (\d+)(?=[.\s(])',text)
            if m:
                if line['spans'][0]['font']=='SFBX1200':labels.append((n+1,int(m.group(1))))
                else:mentions.append((n+1,text))
            m=re.match(r'Assumption (\d+)',text)
            if m and line['spans'][0]['font']=='SFBX1200':assumptions.append((n+1,int(m.group(1))))
assert labels==[(7,1),(8,2),(10,3),(12,4),(13,5)] and [p for p,s in mentions]==[7,8,10,13]
assert assumptions==[(6,1)],assumptions
assert [(c['evidence'][0]['page'],int(c['claim_id'].split('/T')[-1])) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==5
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
# Independently derived from the source statements, not imported from the finalizer.
expected={'1':{1,2,3,4,5,6,7,9,10},'2':{1,2,3,4,5,6,7,11,12},'3':{1,2,3,4,5,6,7,9,13,14,15,16,17},'4':{1,2,5,6,7,13,14,15,16,17,18,19,20,24},'5':{1,2,5,6,7,8,13,14,15,16,17,18,21,22,23,24}}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
expected_direct={'1':{1,6,10,9,5,4},'2':{1,6,11,12},'3':{1,6,15,17,4,5,9},'4':{1,6,15,24,20,18},'5':{1,6,15,24,22,23,8}}
assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in expected_direct.items()}
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
assert 'D20' not in reach['5'] and 'D19' not in reach['5']
assert 'D9' not in reach['2'] and 'D18' not in reach['1']
assert byid['D23']['depends_on']==['D21','D18'] and 'D22' not in byid['D23']['depends_on']
assert byid['D6']['source_kind']=='assumption' and byid['D24']['source_kind']=='condition' and byid['D1']['source_kind']=='source_passage'
t={n:c['statement_original'] for n,c in claims.items()};b={lid:m['statement_original'] for lid,m in byid.items()};a={x['local_id']:x['statement_original'] for x in ambient['auxiliary_source_passages']}
assert r'\eta(a_p,b_p,p)\to0' in t['1'] and r'L(F^{\mathbf S_n},F^{\mathbf S_n^0})=o_p(1)' in t['1']
assert r'E(M_2^p)\ge E(M_2^{0,p})+\delta' in t['2'] and 'for all $p$ large enough' in t['2']
assert r'M_p=o(\sqrt p)' in t['3'] and r'\delta<\min(a_p,b_p)<a_p+b_p<1-\delta' in t['3']
assert r'0<h_1\le h_2<\infty' in t['4'] and 'finitely many points of discontinuity' in t['4']
assert t['4'].count('y^{-1}')==2 and r'\text{for all }z\in\mathbb C^+' in t['4']
assert 'Under the assumptions of Theorem 4' in t['5'] and r'\frac1{\sqrt p}\|\widetilde{\boldsymbol\Sigma}-\widetilde{\boldsymbol\Sigma}^{or}\|_F=o_p(1)' in t['5']
assert all(f'({i})' in b['D6'] for i in ['i','ii','iii','iv'])
assert r'H\ne\delta(0)' in b['D6'] and r'p/n\to y>0' in b['D6']
assert r't=1,\ldots,T' in b['D3'] and r'\sum_{t=1}^n' in b['D4']
assert r'\sqrt{p(1-a-b)}' in a['A3'] and r'\frac a{1-a-b}' in a['A3']
assert r'\overline\sigma_i^2' in b['D13']
assert r'\operatorname*{argmax}' in b['D14'] and r'\frac{R_{i_0t}^2}{\sigma_{i_0t}^2}+\log(\sigma_{i_0t}^2)' in b['D14']
assert r'\widehat{\overline\sigma}_{i_0}' in b['D14'] and r'\delta\le\overline\sigma^2<C' in b['D14']
assert r'\frac{1-\widehat a-\widehat b+\widehat a\widehat b^{M_p}}{1-\widehat b}' in b['D15']
assert r'\widehat a\widehat b^{j-1}\mathbf R_{t-j}\mathbf R_{t-j}^T' in b['D15']
assert r'\mathbf P_t^{-1/2}\mathbf R_t' in b['D16']
assert r'1-y\left(1+zm_F(z)\right)' in b['D18'] and 'y^{-1}' not in b['D18']
assert r'\frac1p\operatorname{tr}' in b['D20'] and r'\frac1{\operatorname{tr}\big(g(\overline{\boldsymbol\Sigma})\big)}' in a['A9']
assert r'\min(\widetilde\lambda_i,L)' in b['D21'] and 'Ledoit and Wolf (2015)' in b['D22']
assert r'\frac1{(y-1)\check m_{\underline F}(0)}' in b['D23'] and r'\widetilde\lambda_i^\tau=0\text{ and }y>1' in b['D23']
assert r'\left(1-y-y\widetilde\lambda_i^\tau\cdot\check m_F(\widetilde\lambda_i^\tau)\right)^2' in b['D23'] and '\\left|' not in b['D23']
assert r'm_{\underline F}=(y-1)/z+ym_F(z)' in b['D23'] and r'\check m(\lambda)=\lim' in b['D23']
counts=dict(theorems=5,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_source_passages']))
assert counts==dict(theorems=5,interfaces=24,source_members=24,direct_theorem_uses=30,related_theorem_connections=61,unranked_auxiliary_passages=12),counts
assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==27
for item in data['claims']+members+ambient['auxiliary_source_passages']:
    assert all(1<=e['page']<=36 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[]):
        assert all(1<=e['page']<=36 for e in ctx['evidence']);fragments.append(ctx['text'])
    for text in fragments:
        assert not re.search(r'[\u4e00-\u9fff]',text)
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
for n in [2,5,6,7,8,9,10,11,12,13]:shutil.copyfile(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
for n in [9,13]:shutil.copyfile(WORK/f'formula-{n}.png',ROOT/'evidence'/f'formula-{n}.png')
write('source-passages.json',dict(paper_id=PID,members=members))
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-prerequisites.json','inventory-review.json','interface-extraction.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
checks=[
 'Pinned source title, both authors, 49-page count, arXiv version, two printed dates and PDF SHA checked. Fresh extraction matches every archived main-text page byte for byte.',
 'Independent font-aware enumeration finds exactly five Theorems and one numbered Assumption. Four ordinary-font theorem mentions and the Section 5 proof heading are excluded. The actual supplement starts on page 37.',
 'All five complete original statements remain unchanged from the independently validated inventory. Their hypotheses, endpoint quantifiers and formulas were checked on pages 7, 8, 10, 12 and 13.',
 'All four parts of Assumption 1, the dynamic/iid return coupling, sample covariance normalization and covariance-bar typography are preserved. The extra support and function restrictions in Theorem 4 are not strengthened.',
 'The source eta scaling, distinct regimes and expected second-moment gap are checked. Theorem 2 does not gain an unstated stochastic-order or Levy-distance conclusion.',
 'Main-text construction review covers the marginal GARCH variance, random-coordinate QMLE and domain, full projection formula, inverse-square-root returns and adjusted covariance. The positive argmax criterion is preserved.',
 'Stieltjes and generalized resolvent formulas, the matrix function g, clipped eigenvalues, NLS invocation and oracle branches are checked against pages 10–13, including enlarged oracle/QMLE crops.',
 'The inverse-y discrepancy, trace normalization mismatch, ordinary squared oracle denominator, underlined companion F and unindexed boundary-value shorthand remain recorded as source issues.',
 'Independent traversal verifies 30 direct uses and 61 related connections. Theorem 5 inherits the hypotheses of Theorem 4 but not its generalized-transform conclusion, and its oracle does not depend on the numerical NLS algorithm.',
 'All 24 source passages have original terminology, faithful source kinds, meaningful selectors and same-paper explanations. Twelve auxiliary passages preserve unnamed/local definitions and contextual formulas; external NLS details remain explicitly unresolved.'
]
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=49,main_text_last_pdf_page=36,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent font-aware enumeration of main-text pages 1–36, visually checked on all five theorem pages. Actual headings use SFBX1200. Appendix boundary inspected by title-only clip on page 37.',printed_label_check=labels,excluded_result_types=['Lemma','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=checks),source_notes=ambient['source_issues'],unresolved_source_references=ambient['excluded_references'],ambient_resolution=ambient['statement_resolution'],artifacts=artifacts,evidence=evidence,review_limits=['Source transcription and dependency audit, not proof certification or repair of the printed formulas.','Pinned preprint inspected; equivalence to the final journal typesetting is not asserted.','Attached supplement excluded; the externally cited NLS numerical algorithm is retained without inventing its missing construction.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
