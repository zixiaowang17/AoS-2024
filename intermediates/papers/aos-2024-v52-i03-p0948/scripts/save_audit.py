"""Independently verify source identity, theorem census and mathematical dependency paths."""
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
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==60
assert paper['main_text_last_pdf_page']==27 and not paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split());assert paper['title'].lower() in first.lower().replace('block-wise','blockwise')
for author in ['Bingxin Zhao','Shurong Zheng','Hongtu Zhu']:assert author in first
assert '2203.12003v1' in first and '22 Mar 2022' in first and 'June 13, 2025' in first
assert paper['source_url']=='https://arxiv.org/pdf/2203.12003v1' and paper['version']=='arXiv:2203.12003v1'
assert 'Zhou' in pdf[26].get_text()
heading=pdf[27].get_text(clip=fitz.Rect(0,0,pdf[27].rect.width,155));assert 'Supplementary Material for' in heading
labels=[];plain=[];conditions=[]
for n in range(27):
    page=pdf[n]
    assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text(),n+1
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();match=re.match(r'Theorem (\d+)(?=[.\s(])',text)
            if match:
                if line['spans'][0]['font']=='URWPalladioL-Bold':labels.append((n+1,match.group(1)))
                else:plain.append((n+1,text))
            match=re.match(r'Condition (\d+)\.',text)
            if match and line['spans'][0]['font']=='URWPalladioL-Bold':conditions.append((n+1,int(match.group(1))))
assert labels==[(8,'1'),(9,'2'),(12,'3'),(12,'4')]
assert [p for p,t in plain]==[10,12,13]
assert conditions==[(5,1),(6,2),(6,3),(9,4),(12,5),(16,6)],conditions
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==4
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members};claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
source=json.loads((ROOT/'source-passages.json').read_text());assert {m['local_id']:m for m in source['members']}==byid
reach={}
for n,c in claims.items():
    seen=set();stack=c['depends_on'][:]
    while stack:
        lid=stack.pop()
        if lid in seen:continue
        seen.add(lid);stack.extend(byid[lid]['depends_on'])
    reach[n]=seen
expected={
 '1':[1,3,4,5,6,10,13,18,19],
 '2':[1,2,3,4,5,6,7,8,9,10,13,14,17,18,19,21,22],
 '3':[1,3,4,5,6,11,18,20],
 '4':[1,2,3,4,5,6,7,8,9,11,12,13,15,16,17,18,20,21,23]
}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
assert all(reach[n].isdisjoint({'D2','D7','D8','D9','D14','D15','D16','D17','D21','D22','D23'}) for n in ['1','3'])
assert 'D22' not in reach['4'] and 'D21' in reach['4']
assert 'D19' not in reach['4'] and 'D20' not in reach['2']
for lid,label in [('D3','Condition 1(a)'),('D4','Condition 1(b)'),('D5','Condition 1(c)'),('D6','Condition 1(d)'),('D7','Condition 2'),('D8','Condition 3'),('D23','Condition 5')]:
    assert byid[lid]['source_kind']=='condition' and byid[lid]['source_heading']==label
assert byid['D21']['source_kind']=='definition' and byid['D22']['source_kind']=='condition'
t={n:c['statement_original'] for n,c in claims.items()}
assert [e['page'] for e in claims['1']['evidence']]==[8,9]
assert [e['page'] for e in claims['2']['evidence']]==[9,10]
assert [e['page'] for e in claims['4']['evidence']]==[12,13]
assert all(r'\tag{'+str(k)+'}' in t['1'] for k in [2,3,4])
assert r'\boldsymbol\Sigma_{B_l}' in t['1'] and 'are zeros' in t['1']
assert 'is maximized' in t['2'] and r'\tag{5}' in t['2']
assert r'-1-\omega_l\lambda' in t['2'] and r'(\boldsymbol I_{p_l}-\dot a_l\boldsymbol\Sigma_l)' in t['2']
assert r'\min(n_w,p_l)' in t['3'] and r'n^{-1}\mathrm E\operatorname{tr}' in t['3'] and 'n_w^{-1}' not in t['3']
assert t['3'].count('is approximated by')==2
assert r'\lambda v_{w_l}(-\lambda)\boldsymbol\Sigma_l' in t['3']
assert all(r'\boldsymbol Q_'+str(i) in t['4'] for i in range(1,8))
assert r'A_{BW}^2(\lambda)' in t['4'] and r'A_{BZ}^2(\lambda)' in t['4']
assert r'-1-\omega_{z_l}\cdot\lambda' in t['4']
assert r'\boldsymbol\Sigma_l^2' in t['4'] and r'\boldsymbol K_l' in t['4']
assert r'\boldsymbol\epsilon_z' in byid['D2']['statement_original']
assert r'\omega_{w_{ln}}' in byid['D6']['statement_original']
assert r'p^{-1}\cdot\boldsymbol\Sigma_\beta' in byid['D8']['statement_original']
assert r'\sigma_{\epsilon_z}^2' in byid['D8']['statement_original']
assert r'\boldsymbol\epsilon^T\boldsymbol\epsilon' in byid['D9']['statement_original']
assert r'n_w^{-1}' in byid['D15']['statement_original'] and r'\boldsymbol X_l^T\boldsymbol y' in byid['D15']['statement_original']
assert r'n_z^{-1}' in byid['D16']['statement_original'] and r'\boldsymbol X_l^T\boldsymbol y' in byid['D16']['statement_original']
assert r'(\boldsymbol y_z^T\widehat{\boldsymbol S}_Z)^2' in byid['D17']['statement_original']
assert r'(t-z)^{-1}' in byid['D18']['statement_original']
assert r'\boldsymbol\Sigma(\widehat{\boldsymbol\Sigma}_{BW}+\lambda\boldsymbol I_p)^{-1}\boldsymbol\Sigma' in byid['D23']['statement_original']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=4,interfaces=23,source_members=23,direct_theorem_uses=38,related_theorem_connections=53,unranked_auxiliary_passages=8),counts
assert set(ambient['standard_ambient_resolution'])=={'shared',*claims}
assert len(ambient['unresolved_source_conventions'])==28
math_fragments=0
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=27 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=27 for e in ctx['evidence']);fragments.append(ctx['text'])
    for text in fragments:
        assert not re.search(r'[\u4e00-\u9fff]',text)
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            math_fragments+=1;depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,('unbalanced braces',item)
            assert depth==0,('unbalanced braces',item)
assert math_fragments>100
for x in data['interfaces']:
    assert x['related_theorems'] and set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
    for m in x['members']:
        own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors) and all(s in linked for s in selectors)
    for k in x['source_keywords']:
        m=byid[k['local_id']];texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])];assert any(k['source_text'] in text for text in texts)
for n in [1,4,5,6,7,8,9,10,12,13,16,22,27]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
shutil.copy2(WORK/'rates.png',ROOT/'evidence/rates.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=60,main_text_last_pdf_page=27,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent font-aware enumeration across main-text pages 1–27 finds four bold Theorem headings and excludes three regular-font mentions. Theorem 1 continues onto page 9, Theorem 2 onto page 10, and Theorem 4 onto page 13. Six numbered Conditions are independently located; Condition 6 belongs to the excluded Proposition 1, while the four Theorems require only Conditions 1–5.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'Title, three authors, arXiv v1 stamp, two different source dates, 60-page count and SHA-256 are checked; every archived main-text page equals fresh byte-preserving extraction.',
  'Independent theorem inventory was validated before extraction; every original claim field remains unchanged in the finalized census.',
  'Theorem 1 is checked on pages 8–9, retaining both zero-limit traces, quadratic off-block trace, stochastic remainder and Marchenko–Pastur equation.',
  'Theorem 2 is checked on pages 9–10, retaining all three R functions, the fixed-point root, printed derivative formula and complete optimal-tuning assertion.',
  'Theorem 3 is checked on page 12, retaining both approximations and the expectation/companion-transform definition of K_l with its printed n^{-1} factors.',
  'Theorem 4 is checked on pages 12–13, retaining both prediction targets, all seven Q functions, both positive roots, Sigma powers and the derivative denominator.',
  'Dataset declarations and model (1) are checked on pages 4–5; all four parts of Condition 1 and Conditions 2–3 are checked on pages 5–6, including nested ratio indices and bold noise-vector notation.',
  'Training, reference and testing covariances and ridge constructions are checked on page 7; their different sample-size factors remain intact.',
  'Realized heritability, uncentered squared-cosine accuracy, Stieltjes convention, population versus sample spectral laws, and the companion reference transform are checked on pages 6,8,12.',
  'Conditions 4–5 are checked on pages 9 and 12; their shared causal-submatrix notation is separate from their different lists of trace-ratio assumptions.',
  'Independent graph traversal verifies 38 direct uses and 53 related connections. Trace-only Theorems 1 and 3 acquire no response, effect, heritability or regression-estimator prerequisites.',
  'All 23 interfaces preserve source keywords, kinds and statements, match meaningful highlight selectors and have explanations for each derived theorem path.',
  'Eight auxiliary excerpts and twenty-eight source notes preserve local bindings and ambiguities without importing supplementary variants or certifying the source claims.',
  'References end on page 27 and the attached supplement begins on page 28; only its heading is inspected and all extracted mathematics stays within the main text.'
 ]),source_notes=[
  'The pinned file is identified by its hash and printed arXiv stamp. Its title-page date differs from its margin date; final journal equivalence is not established.',
  'Original normalizations, derivative signs, optimality assertion and sample-size conventions are retained, with their ambiguities documented.',
  'Source review verifies transcription and statement relationships, not proofs or the truth of every printed assertion.',
  'Main-text Proposition 1 and its Condition 6 on page 16 concern BLPC estimators. They are not Theorems or prerequisites of the four inventoried Theorems, so they are not added to this census.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Source transcription and statement-prerequisite audit, not proof certification or source repair.','Pinned preprint audited; final journal equivalence and the cause of its date discrepancy are not established.','All attached supplementary mathematics is excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
