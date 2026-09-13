"""Independent source and dependency audit of the four Chapter 3 spectral-EL Theorems."""
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
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==295
assert paper['main_text_first_pdf_page']==99 and paper['main_text_last_pdf_page']==136
assert paper['main_text_boundary']['shared_page_with_appendix'] is False
chapter=' '.join(pdf[98].get_text().split())
assert paper['source_title'].upper() in chapter
assert all(name in chapter for name in prov['authors'])
assert 'Modified from a manuscript under review by The Annals of Statistics' in chapter
assert '2023' in pdf[0].get_text() and 'Haihan Yu' in pdf[0].get_text()
assert paper['source_url']=='https://dr.lib.iastate.edu/server/api/core/bitstreams/e6a497df-d997-456c-bb15-3dd802a6555a/content'
assert paper['version']=='Iowa State dissertation, August 2023, Chapter 3 (author manuscript)'
assert 'Zhu, K. (2016)' in pdf[135].get_text()
assert 'Appendix A: Additional numerical results' in pdf[136].get_text(clip=fitz.Rect(0,105,pdf[136].rect.width,126))
labels=[];mentions=[]
for n in range(99,137):
    page=pdf[n-1];assert (ROOT/'evidence'/f'page-{n:03}.txt').read_bytes().decode('utf8')==page.get_text()
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();m=re.match(r'^Theorem\s+(\d+(?:\.\d+)+)',text)
            if m:
                heading=any(s['font']=='NimbusRomNo9L-Medi' and 'Theorem' in s['text'] for s in line['spans'])
                (labels if heading else mentions).append((n,m[1]))
assert labels==[(112,'3.5.1'),(115,'3.6.1'),(118,'3.6.2'),(129,'3.8.1')]
assert mentions==[(112,'3.5.1'),(118,'3.5.1'),(129,'3.8.1'),(129,'2.1'),(129,'3.8.1')]
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
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
# Independently specified after source review: the bare SEL limit has no fit;
# M-estimation has no blocks; smooth-profile resampling is an entire-function experiment.
expected={
 '3.5.1':{1,2,3,4,7,8,9,10,11,12,13,14,15},
 '3.6.1':{1,2,3,4,5,6,11,12,13,14,15,16,17},
 '3.6.2':set(range(1,23)),
 '3.8.1':{1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,23,24,25,26}}
direct={
 '3.5.1':{4,7,10,12,13,15},'3.6.1':{4,12,13,15,16,17},
 '3.6.2':{4,7,10,12,13,15,16,17,22},'3.8.1':{4,7,12,13,15,17,23,24,26}}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
assert reach['3.5.1'].isdisjoint({f'D{i}' for i in [5,6,16,17,18,19,20,21,22,23,24,25,26]})
assert reach['3.6.1'].isdisjoint({f'D{i}' for i in [7,8,9,10,18,19,20,21,22,23,24,25,26]})
assert reach['3.8.1'].isdisjoint({'D10','D20','D21','D22'})
assert 'D16' not in byid['D19']['depends_on'] and 'D6' not in byid['D8']['depends_on']
t={n:c['statement_original'] for n,c in claims.items()};b={lid:m['statement_original'] for lid,m in byid.items()};a={x['local_id']:x['statement_original'] for x in ambient['auxiliary_source_passages']}
assert all(len(c['evidence'])==1 for c in claims.values())
assert 'Assumptions 3.5.1-3.5.3' in t['3.5.1'] and 'spectral moment condition (3.2)' in t['3.5.1']
assert r'b/n+n/b^2\to0' in t['3.5.1'] and r'\chi_p^2' in t['3.5.1']
for part in ['(i)','(ii)','(iii)','(iv)']:assert part in t['3.6.1'] and part in b['D17']
assert 'there exists a solution sequence' in t['3.6.1']
assert r'\partial^2G_\theta(\cdot)/\partial\theta\partial\theta^\intercal' in t['3.6.1']
assert r'H(\cdot):[-\pi,\pi]\mapsto\mathbb R^+' in t['3.6.1']
assert r'\mathcal N(0_p,\Sigma_{\theta_0})' in t['3.6.1']
assert r'(D_{\theta_0}^\intercal V_{\theta_0}^{-1}D_{\theta_0})^{-1}' in t['3.6.1']
assert 'Under assumptions of Theorem 3.6.1' in t['3.6.2']
assert r'b/n+n/b^2\to0' in t['3.6.2']
assert r'\sup_{x\in\mathbb R}' in t['3.6.2'] and r'\mathbb P_*(\ell_n^*(\widehat\theta_n)\le x)' in t['3.6.2']
assert r'\xrightarrow{p}0' in t['3.6.2']
assert 'Assumptions for Theorem 3.6.2' in t['3.8.1']
assert r'b/n+n/b^2\to\infty' in t['3.8.1'] and r'\chi_u^2' in t['3.8.1']
assert r'\mathbb R^p\mapsto\mathbb R^s' in t['3.8.1']
assert r'\partial h(\theta)/\partial\theta|_{\theta=\theta_0}' in t['3.8.1']
assert 'constant rank' not in t['3.8.1']
assert 'absolutely summable autocovariances' in b['D1'] and 'weakly stationary' in b['D1']
assert r'\mathcal M_\theta\equiv(m_1(\theta),\ldots,m_p(\theta))^\intercal' in b['D3']
assert 'at the true value' in b['D4']
assert r'(2\pi n)^{-1}' in b['D5'] and r'\imath=\sqrt{-1}' in b['D5']
assert r'\sum_{|j|=1}^{\lfloor n/2\rfloor}' in b['D6'] and 'both positive/negative frequencies' in b['D6']
assert r'N\equiv\lfloor n/b\rfloor' in b['D7'] and r'\frac1{2\pi b}' in b['D7']
assert r'T_{i,\mathrm{NOL}}(\theta)' in b['D8'] and r'\frac{2\pi}b' in b['D8']
assert 'conditioning set' in b['D9'] and r'L_n(\theta)=0' in b['D9']
assert r'\ell_n(\theta)\equiv-2\log[N^N L_n(\theta)]' in b['D10']
assert r'\sup_{m\in\mathbb Z}' in b['D11'] and r'\mathcal F_{m+k}^\infty' in b['D11']
assert r'\sup_{t\in\mathbb Z}\mathbb E|X_t|^{4+\delta}' in b['D12'] and r'k^2\alpha(k)^{\delta/(4+\delta)}' in b['D12']
assert '4th-order stationary series' in b['D12'] and 'strictly' not in b['D12']
assert 'At the true parameter' in b['D13'] and 'bounded variation' in b['D13']
assert r'(2\pi)^{-3}' in b['D14'] and r'\operatorname{cum}(X_0,X_{h_1},X_{h_2},X_{h_3})' in b['D14']
assert r'G_{\theta_0}(-\lambda)' in b['D15'] and r'f_4(\lambda_1,\lambda_2,-\lambda_2)' in b['D15']
assert r'V_{\theta_0}\equiv V_{\theta_0,1}+V_{\theta_0,2}' in b['D15']
assert r'T_n(\theta)=\mathcal M_\theta' in b['D16']
assert r'-\partial\mathcal M_{\theta_0}/\partial\theta' in b['D17']
assert r'(2\pi/b)' in b['D18'] and r'X_{s-1+i}' in b['D18']
assert '4π²' in byid['D18']['variant_note']
assert r'\mathcal C_{\mathrm{OL}}' in b['D20']
assert 'iid draws' in b['D21'] and r'\}_{i=1}^N' in b['D21']
assert r'\sum_{i=1}^N p_iT_{i,\mathrm{OL}}^*(\widehat\theta_n)=\mathcal M_{\widehat\theta_n}' in b['D22']
assert r'\mathcal M_{\widehat\theta_n}=T_n(\widehat\theta_n)' in b['D22']
assert r'\max\{L_n(\theta):h(\theta)=\vartheta\}' in b['D23']
assert r'\widehat\vartheta_n\equiv h(\widehat\theta_n)' in b['D24']
assert 'as a function of' in b['D25'] and r'\{T_{i,\mathrm{OL}}^*(\theta),\theta\in\Theta\}_{i=1}^N' in b['D25']
assert r'\max\{L_n^*(\theta):h(\theta)=\widehat\vartheta_n\}' in b['D26']
assert 'as a function of' in byid['D19']['application_context'][0]['text']
assert r'\mathbb P_*' in a['A4'] and r'=1-\alpha' in a['A4']
assert r'\mathbb R^s\mapsto\mathbb R^s' in a['A5'] and r'\theta\in\mathbb R' in a['A5']
assert r'\vartheta_0=h(\theta_0)\in\mathbb R^s' in a['A6']
counts=dict(theorems=4,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_source_passages']))
assert counts==dict(theorems=4,interfaces=26,source_members=26,direct_theorem_uses=30,related_theorem_connections=70,unranked_auxiliary_passages=6),counts
assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==22
for item in data['claims']+members+ambient['auxiliary_source_passages']:
    assert all(99<=e['page']<=136 for e in item['evidence'])
    fragments=[item['statement_original']]
    for key in ['naming_context','application_context']:
        for ctx in item.get(key,[]):
            assert all(99<=e['page']<=136 for e in ctx['evidence']);fragments.append(ctx['text'])
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
for n in [99,105,106,108,109,110,111,112,114,115,117,118,128,129,136]:
    shutil.copyfile(WORK/f'page-{n:03}.png',ROOT/'evidence'/f'page-{n:03}.png')
write('source-passages.json',dict(paper_id=PID,members=members))
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-prerequisites.json','inventory-review.json','interface-extraction.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
checks=[
 'Pinned original institutional PDF hash, page count, Chapter 3 title, all three authors, dissertation year and explicit Annals submission status checked. Published and manuscript titles remain distinct in provenance.',
 'All 38 archived Chapter 3 main-text/reference pages match fresh PDF extraction byte for byte. The next-page Appendix A heading is checked without using appendix mathematics; other dissertation chapters remain excluded.',
 'Fresh bold-font heading enumeration independently confirms exactly four main-text Theorems and excludes five ordinary-font mentions. Full original statements remain unchanged from the separately validated inventory.',
 'All original theorem formulas and hypotheses were compared with rendered pages 112,115,118,129: moment assumptions, block conditions, estimator derivatives and full covariance, both bootstrap CDF suprema, smooth parameter and Jacobian rank.',
 'The 26 original source members, their naming/application context and six ambient source passages were checked against relevant main-text pages. Source labels distinguish assumptions, definitions and theorem-excerpted regularity conditions.',
 'The real spectral framework, moment vector, both signs of Fourier frequencies, non-overlapping likelihood blocks, full-data M-estimation and overlapping bootstrap blocks retain their distinct formulas and roles.',
 'Independent mathematical dependency expectations confirm all 30 direct uses and 70 related connections. The SEL limit does not acquire the M-estimator, M-estimation does not acquire block likelihoods, and smooth profiling does not acquire a fixed-fit resampling experiment.',
 'The OL periodogram prefactor mismatch, contradictory block limit in Theorem 3.8.1, introductory dimension mismatch, profile-max attainment and unspecified neighborhood rank condition are recorded without changing original mathematics.',
 'Every member has natural-language source keywords, a meaningful selector and source-backed explanations along all related theorem paths. Source evidence for definitions, naming and application context is restricted to PDF 99–136.',
 'Source and artifact hashes are pinned; original math delimiters and braces are balanced; inventory and census validation pass. This audit checks source transcription and statement dependencies, not theorem correctness or final-journal equivalence.'
]
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=295,main_text_first_pdf_page=99,main_text_last_pdf_page=136,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent bold-font Theorem-heading enumeration restricted to Chapter 3 PDF 99–136, followed by visual review of all full statements and required source definitions.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=checks),source_notes=ambient['source_issues'],unresolved_source_references=ambient['excluded_references'],ambient_resolution=ambient['statement_resolution'],artifacts=artifacts,evidence=evidence,review_limits=['Source transcription and statement-dependency audit; not proof certification or correction of source errors.','Corresponding dissertation author manuscript inspected; final journal theorem-by-theorem equivalence remains unverified.','Other dissertation chapters and all appendices are excluded. Printed normalization, dimension and limit conflicts remain explicit.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
