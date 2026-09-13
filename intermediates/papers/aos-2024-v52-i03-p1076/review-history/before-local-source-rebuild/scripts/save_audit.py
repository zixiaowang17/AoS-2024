"""Independent source and dependency review for the spectral two-sample census."""
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
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==75
assert paper['main_text_last_pdf_page']==55 and paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split())
assert paper['title'].lower() in first.lower()
assert all(name.lower() in first.lower() for name in ['Omar Hagrass','Bharath K. Sriperumbudur','Bing Li'])
assert '2212.09201v3' in first and '1 May 2024' in first
assert paper['source_url']=='https://arxiv.org/pdf/2212.09201v3' and paper['version']=='arXiv:2212.09201v3'
end=prov['main_text_end_y'];assert end==601.6620483398438
assert 'Technical results' in pdf[54].get_text(clip=fitz.Rect(0,end,pdf[54].rect.width,end+20))
assert 'Proofs' in pdf[31].get_text(clip=fitz.Rect(0,230,pdf[31].rect.width,260))
labels=[];mentions=[]
for n in range(55):
    page=pdf[n];clip=fitz.Rect(0,0,page.rect.width,end) if n==54 else page.rect
    assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text(clip=clip)
    for block in page.get_text('dict',clip=clip)['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();m=re.match(r'^Theorem\s+(\d+\.\d+)',text)
            if m:(labels if line['spans'][0]['font']=='CMBX10' else mentions).append((n+1,m[1]))
assert labels==[(7,'3.1'),(8,'3.2'),(12,'4.1'),(13,'4.2'),(14,'4.3'),(17,'4.6'),(18,'4.7'),(20,'4.10'),(20,'4.11'),(22,'4.12')]
assert mentions==[(22,'4.11')]
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==10
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members}
claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
extraction=json.loads((ROOT/'interface-extraction.json').read_text())
assert {m['local_id']:m for x in extraction['interfaces'] for m in x['members']}==byid
assert extraction['status']=='extracted'
reach={}
for n,c in claims.items():
    seen=set();stack=c['depends_on'][:]
    while stack:
        lid=stack.pop()
        if lid in seen:continue
        seen.add(lid);stack.extend(byid[lid]['depends_on'])
    reach[n]=seen
# Independent source-derived expectations: no import of the finalizer's DIRECT map.
expected={
 '3.1':{1,2,3,4,5,7,8,9,10,11,13,33},
 '3.2':{1,2,3,6,7,8,9,10,11,13,33},
 '4.1':{1,2,3,7,13,15,17,18,19},
 '4.2':{1,2,3,7,8,9,13,15,16,17,18,19,21,22,25},
 '4.3':{1,2,3,7,8,9,10,11,13,15,16,17,18,19,21,22,23,24,25,26,33},
 '4.6':{1,2,3,7,13,15,17,18,19,27,29},
 '4.7':{1,2,3,7,8,9,10,11,13,15,16,17,18,19,21,22,23,24,25,26,27,29,33},
 '4.10':{1,2,3,7,13,15,17,18,19,27,29,30},
 '4.11':{1,2,3,7,8,9,10,11,13,15,17,18,19,21,22,23,24,26,27,29,30,33},
 '4.12':{1,2,3,7,8,9,10,13,15,17,18,19,21,22,23,24,26,27,29,30,31,32,33}}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
expected_direct={
 '3.1':{2,5,11,33,9},'3.2':{2,9,6,11},'4.1':{2,19,17,18},
 '4.2':{2,21,22,19,15,25,9,17},'4.3':{2,21,22,23,24,26,17,11,33,15,25,19,9},
 '4.6':{2,19,29},'4.7':{2,21,22,23,24,26,17,11,33,15,25,19,9,29},
 '4.10':{2,19,29,30},'4.11':{2,21,22,23,24,26,17,33,11,9,15,19,29,30},
 '4.12':{2,21,22,23,24,26,17,33,31,9,15,30,32}}
assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in expected_direct.items()}
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
for n in ['4.1','4.6','4.10']:assert reach[n].isdisjoint({'D21','D22','D23','D24','D26','D11','D25'})
assert reach['4.2'].isdisjoint({'D23','D24','D26','D11'})
assert reach['3.2'].isdisjoint({'D4','D5','D19','D26','D29'})
assert reach['4.11'].isdisjoint({'D25','D31','D32'}) and 'D11' not in reach['4.12']
assert {x['members'][0]['local_id'] for x in data['interfaces'] if not x['related_theorems']}=={'D12','D14','D28'}
assert all(byid[lid]['source_kind']=='assumption' for lid in ['D2','D21','D22','D23','D24','D26'])
assert 'D20' not in byid # Unnamed inline feature difference is retained as ambient A10.
t={n:c['statement_original'] for n,c in claims.items()};b={lid:m['statement_original'] for lid,m in byid.items()};a={x['local_id']:x['statement_original'] for x in ambient['auxiliary_source_passages']}
assert [e['page'] for e in claims['4.3']['evidence']]==[14,15]
assert [e['page'] for e in claims['4.11']['evidence']]==[20,21]
assert [e['page'] for e in claims['4.12']['evidence']]==[22,23]
assert r'\mathbb X_N,\mathbb Y_M' in t['3.1'] and r'1-k\delta' in t['3.1'] and r'\liminf_{N,M\to\infty}' in t['3.1']
assert r'k\in\{1,2\}' in t['3.1'] and r'\gamma_2=q_{1-\alpha}' in t['3.1']
assert r'\Phi_{N,M,\alpha}' in t['3.2'] and r'\mathbb E_{P^N\times Q^M}[1-\phi]' in t['3.2']
assert r'\Delta_{N,M}^{1/2\theta}' in t['3.2'] and r'\Delta_{N,M}^{-2}' in t['3.2']
assert r'\text{③}=\mathbf1_n^\top A_2\mathbf1_n' in t['4.1']
assert r'\frac{g_\lambda(\widehat\lambda_i)-g_\lambda(0)}{\widehat\lambda_i}' in t['4.1']
assert r'\boldsymbol H_s=\boldsymbol I_s-' in t['4.1'] and r'\mathbf1_m^\top' in t['4.1']
assert r'\log\frac{24\mathcal N_1(\lambda)}{\delta}' in t['4.2']
assert r'(A_0)$–$(A_2)' in t['4.2'] and r'C_1+C_2' in t['4.2']
assert r'e^{d_1/272C^2}' in t['4.3'] and r'e^{\frac{d_1}{272C}}' in t['4.7']
assert r'1-2\delta' in t['4.3'] and r'1-5\delta' in t['4.7']
assert r'\widetilde\alpha=(w-\widetilde w)\alpha' in t['4.7']
assert all(r'0<w+\widetilde w<1' in t[n] and r'\ge\widehat q' in t[n] for n in ['4.6','4.10'])
assert r'|\Lambda|^2' in t['4.10'] and r'\frac{w\alpha}{|\Lambda|}' in t['4.10']
for n in ['4.11','4.12']:
    assert r'\lambda_i\lesssim i^{-\beta}' in t[n] and r'\lambda_i\lesssim e^{-\tau i}' in t[n]
    assert t[n].count(r'\sup_i\|\phi_i\|_\infty')==2
    assert r'\sqrt{\log(N+M)}\log\log(N+M)' in t[n]
    assert r'\lambda_L=r_7' in t[n] and r'\lambda_U=r_8' in t[n]
    assert r'^{1/2\xi}' in t[n] and r'^{\frac1{2\xi}}' in t[n]
assert t['4.12'].count(r'0<\alpha\le e^{-1}')==2 and r'\mathcal A:=\log|\mathcal K|' in t['4.12']
assert r'\inf_{K\in\mathcal K}\inf_{\theta>\theta_l}' in t['4.12']
assert r'\mathcal A\frac{\sqrt{\log(N+M)}' in t['4.12']
assert 'completely separable' in b['D2'] and 'characteristic' not in b['D2']
assert r'\sqrt{K(x,x)}' in b['D3'] and r'\sup_{f\in\mathscr H:\|f\|_{\mathscr H}\le1}' in b['D4']
assert r'\frac1{N(N-1)}' in b['D5'] and r'\frac2{NM}' in b['D5']
assert r'[f-\mathbb E_Rf]_\sim' in b['D7'] and r'-\mu_R\mathbb E_Rf' in b['D7']
assert r'\mathcal T:=\mathfrak I\mathfrak I^*' in b['D8'] and r'(1\otimes_{L^2(R)}1)' in b['D8']
assert r'\phi_i:=\frac{\mathfrak I^*\widetilde\phi_i}{\lambda_i}' in b['D9'] and r'\overline{\operatorname{Ran}(\mathcal T)}' in b['D9']
assert r'\frac12\int\frac{(dP-dQ)^2}{dP+dQ}' in b['D10']
assert r'\rho^2(P,Q)\ge\Delta' in b['D11'] and r'\sup_' not in b['D11']
assert r'g_\lambda:(0,\infty)\to(0,\infty)' in b['D12']
assert r'g_\lambda(0)\left(I-\sum_{i\ge1}' in b['D13'] and r'\mathcal B' in b['D13']
assert r'4\langle\mathcal T g_\lambda(\mathcal T)u,u\rangle' in b['D14']
assert r'\Sigma_R:=\Sigma_{PQ}=\mathfrak I^*\mathfrak I' in b['D15']
assert r'\frac12\int_{\mathcal X\times\mathcal X}' in b['D15'] and r'\Sigma_{PQ}+\lambda I' in b['D16']
assert r'(X_i)_{i=N-s+1}^N' in b['D17'] and r'n:=N-s' in b['D17']
assert r'\frac1{2s(s-1)}' in b['D18'] and r'\operatorname{Bernoulli}(\frac12)' in b['D18']
assert r'\sum_{1\le i\ne j\le n}\sum_{1\le i' in b['D19'] and r'g_\lambda^{1/2}(\widehat\Sigma_{PQ})' in b['D19']
assert r'xg_\lambda(x)<B_3' in b['D23'] and r'\varphi\in(0,\xi]' in b['D23']
assert r'\inf_{x\in\Gamma}g_\lambda(x)(x+\lambda)\ge C_4' in b['D24']
assert r'\right\|_{\mathcal L^2(\mathscr H)}' in b['D25'] and r'\right\|_{\mathcal L^2(\mathscr H)}^2' not in b['D25']
assert r'M<N<DM' in b['D26']
assert r'\widehat\eta_\lambda(X^\pi,Y^\pi,Z)' in b['D27']
assert r'\frac1D\sum_{\pi\in\Pi_{n+m}}' in b['D28']
assert r'\frac1B\sum_{i=1}^B' in b['D29'] and 'B+1' not in b['D29']
assert r'\lambda_U=2^b\lambda_L' in b['D30']
assert r'\operatorname{Ran}(\mathcal T_K^\theta)' in b['D31'] and r'|\mathcal K|<\infty' in b['D32']
assert r'g_\lambda(x)=x^\theta' in b['D33']
assert r'A(x,y):=K(\cdot,x)-K(\cdot,y)' in a['A10']
assert 'sets of independent samples' in a['A5'] and 'conditioned on' in a['A6']
assert r'\right\|_{\mathscr H}^2' in a['A7'] and r'\sup_{f\in\mathscr H:' in a['A8']
def has_span(n,font,fragment):
    return any(s['font']==font and fragment in s['text'] for block in pdf[n-1].get_text('dict')['blocks'] for line in block.get('lines',[]) for s in line['spans'])
assert has_span(7,'MSBM10','X') and has_span(6,'EUFM10','I')
assert has_span(9,'CMSY10','B') and has_span(17,'dsrom10','1')
assert has_span(12,'CMMIB10','H') and has_span(12,'CMBX10','1')
counts=dict(theorems=10,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_source_passages']))
assert counts==dict(theorems=10,interfaces=32,source_members=32,direct_theorem_uses=82,related_theorem_connections=159,unranked_auxiliary_passages=10),counts
assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==34
for item in data['claims']+members+ambient['auxiliary_source_passages']:
    assert all(1<=e['page']<=55 and (e['page']<55 or e.get('before_main_text_end') is True) for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[]):
        assert all(1<=e['page']<55 for e in ctx['evidence']);fragments.append(ctx['text'])
    for text in fragments:
        assert not re.search(r'[\u4e00-\u9fff]',text)
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,('unbalanced',item)
            assert depth==0,('unbalanced',item)
for x in data['interfaces']:
    assert set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
    assert '$' not in x['name']
    for m in x['members']:
        own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors) and all(s in linked for s in selectors)
    for k in x['source_keywords']:
        m=byid[k['local_id']];texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])]
        assert any(k['source_text'] in text for text in texts)
for n in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]:
    shutil.copyfile(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
write('source-passages.json',dict(paper_id=PID,members=members))
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-prerequisites.json','inventory-review.json','interface-extraction.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
checks=[
 'Pinned title, author line including the middle initial K., version, date, 75-page count and PDF hashes verified. Every archived main-text page matches fresh PDF extraction byte for byte, including the clipped shared page 55.',
 'Independent font-aware Theorem enumeration finds exactly ten environments, with three two-page statements. Numbered Section 7 remains main text; appendix heading and boundary checked without using appendix mathematics.',
 'Every inventoried original claim field is unchanged at handoff. The MMD theorem preserves both thresholds and its liminf conclusion; the minimax theorem preserves both spectral-inverse conditions and the exact-test risk.',
 'The full matrix theorem retains all five circled terms, Gram matrices, bold centering matrices, divided differences and printed dimension/zero-eigenvalue issues.',
 'Oracle and permutation power statements preserve all main and optional inequalities, qualification truncation, sample and permutation budgets, and their differing exponent constants. The unbound delta in Theorem 4.2 remains literal.',
 'Both adaptive statements preserve their uniformity scopes and all four branches. Radicals, log-log factors, endpoint exponents, kernel-family multiplier and the repeated alpha condition are checked against the page images.',
 'Source passages for embeddings, centered operators, eigenfunction versions, separation classes, sample splitting, estimated covariance and the conditional statistic are checked against pages 1–11. The inline feature difference stays in ambient context without an invented display name.',
 'The four regularizer assumptions are unpacked separately with their common domain/constant context. Effective dimensions, strict B, conditional permutation CDFs, dyadic grid and kernel-specific alternatives are checked against pages 12–21.',
 'Independent direct-edge and transitive-path expectations verify 82 direct uses and 159 related connections. Level-only statements do not inherit A1–A4 or power restrictions. The adaptive theorems do not inherit effective-dimension inequalities merely used in proofs.',
 'All source terms, kinds, highlights, explanation paths, math delimiters and evidence bounds validated. Source typography distinctions are separately checked using PDF fonts; no appendix-only formula is required to resolve the stored statements.'
]
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=75,main_text_last_pdf_page=55,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent CMBX10 Theorem-heading enumeration over pages 1–55, with the last page clipped above Appendix A. Full statement and definition images visually checked.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=checks),source_notes=ambient['source_issues'],unresolved_source_references=ambient['excluded_references'],ambient_resolution=ambient['statement_resolution'],artifacts=artifacts,evidence=evidence,review_limits=['Source transcription and statement-dependency audit, not proof certification or correction of apparent source errors.','Pinned preprint inspected; exact equivalence to final journal typesetting is not asserted.','Printed formula, domain, quantile-tie and uniformity ambiguities remain explicitly recorded rather than resolved by adding hypotheses.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
