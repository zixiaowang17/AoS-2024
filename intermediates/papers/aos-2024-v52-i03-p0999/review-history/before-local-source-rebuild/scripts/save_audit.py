"""Independently audit the main-text change-point inventory and dependency graph."""
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
data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-conventions.json').read_text());review=json.loads((ROOT/'inventory-review.json').read_text())
assert digest(PDF)==paper['pdf_sha256']==prov['pdf_sha256']==digest(WORK/'source.pdf')
assert review['status']=='complete' and review['source_checked'] and digest(ROOT/'theorem-inventory.json')==review['inventory_sha256']
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==112
assert paper['main_text_last_pdf_page']==33 and not paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split())
assert paper['title'].lower().replace('-',' ') in first.lower().replace('-',' ')
for author in prov['authors']:assert author in first
assert '2207.12453v3' in first and '1 Oct 2023' in first and 'October 3, 2023' in first
assert paper['source_url']=='https://arxiv.org/pdf/2207.12453v3' and paper['version']=='arXiv:2207.12453v3'
assert 'Zhang' in pdf[32].get_text() and 'Appendices' in pdf[33].get_text(clip=fitz.Rect(0,0,pdf[33].rect.width,89))
labels=[];mentions=[];assumptions=[]
for n in range(33):
    page=pdf[n];assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text()
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();m=re.match(r'Theorem (\d+)(?=[.\s(])',text)
            if m:
                if line['spans'][0]['font']=='CMBX10':labels.append((n+1,int(m.group(1))))
                else:mentions.append((n+1,text))
            m=re.match(r'Assumption (\d+)\s*\(',text)
            if m and line['spans'][0]['font']=='CMBX10':assumptions.append((n+1,int(m.group(1))))
assert labels==[(12,3),(17,4),(18,8),(21,10)] and [p for p,s in mentions]==[13,16,17,18]
assert assumptions==[(9,1),(10,2),(11,3),(11,4)],assumptions
assert [(c['evidence'][0]['page'],int(c['claim_id'].split('/T')[-1])) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==4
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
base={1,2,3,4,5,7,8,9,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,28,33,34}
expected={'3':base|{27},'4':{10,11},'8':base|{29,30},'10':base|{29,30,31,32}}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
assert reach['4']=={'D10','D11'}
assert all('D27' not in reach[n] for n in ['8','10'])
assert all(reach[n].isdisjoint({'D10','D11'}) for n in ['3','8','10'])
assert set(byid['D21']['depends_on'])=={'D20'}
assert byid['D19']['depends_on']==['D13','D17','D14','D18']
for lid in ['D2','D3','D4','D12','D13','D14','D15','D16','D17','D18','D20','D21']:assert byid[lid]['source_kind']=='assumption'
assert byid['D1']['source_kind']=='source_passage'
t={n:c['statement_original'] for n,c in claims.items()}
assert [e['page'] for e in claims['3']['evidence']]==[12,13]
assert all(label in t['3'] for label in ['a.1.','a.2.','b.1.','b.2.'])
assert t['3'].count('\n- ')==4
assert r'\sum_{t=r}^{-1}\{-2\varrho_k\epsilon_t\xi_t(k)+\varrho_k^2\xi_t^2(k)\}' in t['3']
assert r'\sum_{t=1}^{r}\{2\varrho_k\epsilon_t\xi_t(k)+\varrho_k^2\xi_t^2(k)\}' in t['3']
assert r'\{(\epsilon_t,v_k^\top X_t)\}_{t\in\mathbb Z}\xrightarrow{\mathcal D}' in t['3']
assert r'\frac{\varpi_k}{\sigma_\infty(k)}' in t['3'] and r'\mathbb B_1(-r)' in t['3'] and 'two independent standard Brownian motions' in t['3']
assert 'possibly nonstationary' in t['4'] and r'\Delta_{m,2}^Z' in t['4']
assert r'\{1/\gamma_1(Z)+1/\gamma_2(Z)\}^{-1}<1' in t['4']
assert r'm\exp\{-c_1x^{\gamma(Z)}m^{\gamma(Z)/2}\}+2\exp\{-c_2x^2\}' in t['4']
assert r'x\ge1' in t['4'] and r'm\ge3' in t['4']
assert r'(e_k-s_k)\gg R\gg\sqrt{e_k-s_k}' in t['8']
assert r'\xrightarrow{P.}' in t['8'] and r'\max_{k=1}^K' in t['8']
assert r'M=\infty' in t['10'] and r'\frac{\kappa_k^2}{\widehat\kappa_k^2}' in t['10'] and r'\mathbb{1}\{\widehat\kappa_k\ne0\}' in t['10']
assert r'\widehat\kappa_k^2$ be the $k$th jump size estimator' in t['10']
assert r'\mathcal X_s' in byid['D5']['statement_original'] and r'\varepsilon_s' in byid['D8']['statement_original']
assert r'\sup_{|v|_2=1}' in byid['D7']['statement_original'] and r'\sup_{t\in\mathbb Z}' in byid['D11']['statement_original']
assert r'\Delta_{m,4}^X' in byid['D13']['statement_original'] and r'\Delta_{m,4}^\epsilon' in byid['D17']['statement_original']
assert r'2\gamma_2^{-1}' in byid['D19']['statement_original']
assert r'\alpha_n\gg s\{\log(pn)\}^{2/\gamma}' in byid['D21']['statement_original']
assert r'\lambda|\mathcal I|^{1/2}|\beta|_1' in byid['D22']['statement_original']
assert r'\mathfrak p\leftarrow(-1,\ldots,-1)^\top\in\mathbb R^n' in byid['D25']['statement_original']
assert r'k\leftarrow n' in byid['D25']['statement_original'] and r'r\in\{2,\ldots,n+1\}' in byid['D25']['statement_original']
assert r'\widehat\beta_{k-1}' in byid['D27']['statement_original'] and r'\widehat\beta_{k+1}' in byid['D30']['statement_original']
assert r'\widehat\beta_{k-1}' not in byid['D30']['statement_original']
assert r'(2S)^{-1/2}' in byid['D30']['statement_original'] and r'R^{-1}\widehat\kappa_k^{-2}' in byid['D30']['statement_original']
assert r'\sum_{i=\lceil nr\rceil}^{-1}' in byid['D32']['statement_original'] and r'\sum_{i=1}^{\lfloor nr\rfloor}' in byid['D32']['statement_original']
assert r'\beta_{\eta_k-1}^*' in byid['D34']['statement_original']
counts=dict(theorems=4,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=4,interfaces=33,source_members=33,direct_theorem_uses=62,related_theorem_connections=87,unranked_auxiliary_passages=13),counts
assert set(ambient['standard_ambient_resolution'])=={'shared',*claims} and len(ambient['unresolved_source_conventions'])==33
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=33 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=33 for e in ctx['evidence']);fragments.append(ctx['text'])
    for text in fragments:
        assert not re.search(r'[\u4e00-\u9fff]',text)
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            depth=0
            for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if b=='{' else -1
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
for n in [5,6,8,9,10,11,19,20]:shutil.copyfile(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
write('source-passages.json',dict(paper_id=PID,members=members))
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-extraction.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
checks=[
 'Source title, four authors, version, both dates, 112-page count and SHA checked. Every archived main-text page matches fresh byte-preserving extraction; appendix material is excluded.',
 'Independent font-aware enumeration finds four Theorems and four numbered Assumptions, excluding ordinary-font mentions. Theorem 3 spans pages 12–13; the other statements end on their starting page.',
 'All original inventory fields remain unchanged after finalization. Theorem 3 retains its four setup bullets, two localization rates, signed random walk, extra process-limit assumption and Brownian construction.',
 'Theorem 4 retains the nonstationary setting, second-moment dependence, uniform tail condition, its distinct combined exponent and both deviation terms.',
 'Theorems 8 and 10 retain inherited assumptions, variance-algorithm inputs, block-count rate and simulated-minimizer scaling. The surrounding vanishing-regime restriction is archived separately.',
 'All parts of Assumptions 1–4b are source-checked, including conditional mean zero, changing supports, fixed K, jump indices, projection-uniform tails, fourth-moment dependence, drift limits and the strengthened signal-to-noise rate.',
 'Lasso, interval loss, penalized partition, DPDU, local refinement, jump estimate, variance algorithm, drift estimate and Gaussian simulation are checked against their complete main-text formulas and algorithm blocks.',
 'Printed pointer bounds, backtracking start, temporary-vector orientation, missing/out-of-range coefficient indices and unrounded local endpoints are retained and explicitly documented.',
 'Independent traversal verifies 62 direct uses and 87 related connections. The Bernstein theorem only reaches the nonstationary scalar definitions; the variance and simulation results do not depend on unused refined locations.',
 'All 33 interface passages have original keywords, source kinds, meaningful selectors and source-specific explanations. Thirteen auxiliary excerpts and thirty-three source notes preserve local conventions and ambiguities without reading proof appendices.'
]
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=112,main_text_last_pdf_page=33,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent font-aware scan of all main-text pages 1–33, checked against the complete statement pages and the appendix boundary. Four CMBX10 theorem headings are distinct from four prose mentions; numbered Assumptions 1–4 are separately enumerated.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=checks),source_notes=ambient['unresolved_source_conventions'],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,review_limits=['Transcription and statement-dependency audit, not proof certification or repair of the printed algorithms.','Pinned preprint inspected; equivalence to the final journal version is not asserted.','All appendices from page 34 are excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
