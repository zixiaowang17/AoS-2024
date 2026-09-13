"""Verify pinned source, preserved inventory and independently enumerated dependency reach."""
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
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==102
assert paper['main_text_last_pdf_page']==40 and not paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split());assert paper['title'].lower() in first.lower().replace('semi-parametric','semiparametric')
for author in ['Xi Chen','Wenbo Jing','Weidong Liu','Yichen Zhang']:assert author in first
assert '2210.08393v4' in first and '15 Aug 2024' in first
assert paper['source_url']=='https://arxiv.org/pdf/2210.08393v4' and paper['version']=='arXiv:2210.08393v4'
assert 'Zhou' in pdf[39].get_text()
heading=pdf[40].get_text(clip=fitz.Rect(0,0,pdf[40].rect.width,99));assert 'Theoretical Results of the High-dimensional' in heading
labels=[];plain=[];assumptions=[]
for n in range(40):
    page=pdf[n]
    assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text(),n+1
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();match=re.match(r'Theorem (\d+\.\d+)(?=[.\s(])',text)
            if match:
                if line['spans'][0]['font']=='CMBX10':labels.append((n+1,match.group(1)))
                else:plain.append((n+1,text))
            match=re.match(r'Assumption (\d+)\.',text)
            if match and line['spans'][0]['font']=='CMBX10':assumptions.append((n+1,int(match.group(1))))
assert labels==[(16,'3.1'),(19,'3.3'),(20,'3.4'),(24,'4.1'),(24,'4.2'),(25,'4.3'),(28,'5.1'),(29,'5.2')]
assert len(plain)==2 and [p for p,t in plain]==[16,30]
assert assumptions==[(14,1),(15,2),(15,3),(15,4),(15,5),(22,6),(22,7),(22,8),(23,9)],assumptions
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==8
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members};claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
reach={}
for n,c in claims.items():
    seen=set();stack=c['depends_on'][:]
    while stack:
        lid=stack.pop()
        if lid in seen:continue
        seen.add(lid);stack.extend(byid[lid]['depends_on'])
    reach[n]=seen
expected={
 '3.1':[1,2,3,4,5,6,7,8,9,10,11],
 '3.3':[1,2,3,4,5,6,7,8,9,12,13],
 '3.4':[1,2,3,4,5,6,7,8,9,12,13],
 '4.1':[1,3,5,9,10,14,15,16,17,18,19,20],
 '4.2':[1,3,5,9,14,15,16,17,18,19,21],
 '4.3':[1,3,4,5,6,7,8,9,10,22,23],
 '5.1':[1,2,3,4,5,6,7,8,12,24,25],
 '5.2':[1,2,3,4,5,6,7,8,12,24,25]
}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
assert all(reach[n].isdisjoint({'D2','D4','D6','D7','D8','D12','D13'}) for n in ['4.1','4.2'])
assert 'D10' in reach['4.1'] and 'D10' not in reach['4.2']
assert 'D2' not in reach['4.3'] and 'D13' not in reach['4.3']
assert all(reach[n].isdisjoint({'D9','D10','D13','D21'}) for n in ['5.1','5.2'])
for lid,n in [('D5',1),('D6',2),('D7',3),('D8',4),('D9',5),('D15',6),('D16',7),('D17',8),('D18',9)]:
    assert byid[lid]['source_kind']=='assumption' and byid[lid]['source_heading']==f'Assumption {n}'
assert byid['D3']['source_kind']=='condition'
t={n:c['statement_original'] for n,c in claims.items()}
assert r'\frac{2^{t-1}}3' in t['3.3'] and r'\delta_{m,0}^{2^{t-1}}' in t['4.3']
assert [e['page'] for e in claims['4.3']['evidence']]==[25,27]
assert r'\lambda_h^{-\frac1{2(2\alpha+1)}}' in t['3.4']
assert r'\min_\ell m_\ell\gtrsim' in t['4.1']
assert r'\overline V_W^{-\top}' in t['4.2'] and r'\overline U_W' in t['4.2']
assert r'\delta_0^{2^t/\alpha}' in t['4.2'] and 'sufficiently large $T$' in t['4.2']
assert r'\frac{p\log L}m' in t['4.3'] and r'\frac{p\log L}{\omega m}' in t['4.3']
assert r'\varepsilon\delta_{m,0}^2' in t['4.3']
assert r'\overline B' in t['5.1'] and r'\frac{s^2\log m}{mh_1^3}' in t['5.1']
assert r'\sqrt{\frac{s\log p}{mh_1^3}}\delta_{m,0}' in t['5.1']
assert r'\sqrt{\frac{s^2\log p}{mh_1^3}}\delta_{m,0}' in t['5.1']
assert 'with probability tending to one' in t['5.1'] and 'where $r_m$ is an infinitesimal quantity' in t['5.2']
assert r'\operatorname{median}(\epsilon\mid X,\boldsymbol Z)=0' in byid['D3']['statement_original']
assert r'\pi_U:=\int_{-1}^1x^\alpha H' in byid['D5']['statement_original']
assert r'\Lambda_{\min}(V)<\Lambda_{\max}(V)' in byid['D8']['statement_original']
assert r'c_w,C_W>0' in byid['D18']['statement_original'] and r'c_Wm_\ell/n' in byid['D18']['statement_original']
assert r'\lfloor\omega m\rfloor' in byid['D23']['statement_original'] and r'\frac1{(1-\omega)mh_t}' in byid['D23']['statement_original']
assert r'V_{m,1}^{(t)}' in byid['D25']['statement_original'] and r'\|\boldsymbol\beta\|_1' in byid['D25']['statement_original']
assert byid['D25']['depends_on']==['D12']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=8,interfaces=25,source_members=25,direct_theorem_uses=66,related_theorem_connections=89,unranked_auxiliary_passages=12),counts
assert set(ambient['standard_ambient_resolution'])=={'shared',*claims}
assert len(ambient['unresolved_source_conventions'])==27
assert len(ambient['unresolved_statement_references'])==1 and ambient['unresolved_statement_references'][0]['claim_id']==PID+'/T5.2'
math_fragments=0
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=40 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=40 for e in ctx['evidence']);fragments.append(ctx['text'])
    for text in fragments:
        assert not re.search(r'[\u4e00-\u9fff]',text)
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            math_fragments+=1;depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,('unbalanced braces',item)
            assert depth==0,('unbalanced braces',item)
assert math_fragments>250
for x in data['interfaces']:
    assert x['related_theorems'] and set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
    for m in x['members']:
        own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors) and all(s in linked for s in selectors)
    for k in x['source_keywords']:
        m=byid[k['local_id']];texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])];assert any(k['source_text'] in t for t in texts)
for n in [1,2,9,10,11,12,13,14,15,16,19,20,21,22,23,24,25,26,27,28,29,30,40]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=102,main_text_last_pdf_page=40,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent font-aware enumeration of CMBX10 Theorem headings on all main-text pages 1–40; eight statements, including continuations on pages 27,29,30. Proposition 3.2, Corollary 3.5, ordinary-font mentions and appendix mathematics are excluded.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'Pinned v4 title, author names, margin date, page count and hash agree with the inspected PDF. All forty saved text pages match fresh byte-preserving extraction.',
  'Independent main-text enumeration finds eight Theorems and nine Assumptions, with the exact printed labels and source order. The inventory was validated before interface extraction.',
  'Every original theorem field survives the finalizer unchanged. Theorem 4.3 is continued after the intervening Algorithm 2 page; Theorems 5.1 and 5.2 retain both pages.',
  'Visual review checks all eight statements, including double-exponential exponents, negative bandwidth exponent, weighted inverse transpose, sample-size factors, and the distinct logarithms in Theorem 5.1.',
  'All Assumptions 1–9 are checked against pages 14,15,22,23; source kinds, strict bounds, kernel conditions and machine-indexed distributions are preserved.',
  'Main-text standing identification conditions, normalization, sampling, data partitions and section changes are checked on pages 2,9–12,21–22,25,27.',
  'Empirical objectives, local derivatives and algorithms are checked on pages 12–14,23,26,28. Sparse iterations use a single-machine Hessian and do not inherit a dense matrix inverse update.',
  'Independent graph traversal verifies 66 direct uses and 89 related connections. The weighted Newton method does not inherit the local-minimizer functional; coefficient shift does not inherit global identical distribution.',
  'Every one of the 25 source interfaces has original natural-language keywords, meaningful source selectors, and source-specific explanations covering all derived paths.',
  'Twelve auxiliary source excerpts preserve notation, unnamed constants, inherited assumption clauses and explicit appendix-only references without inventing API names.',
  'Theorem 5.2 remains the complete abbreviated main-text statement; its appendix-only tuning and r_m definition are explicitly unresolved and no appendix mathematics is used.',
  'Reference-page ending and the Appendix A heading establish the boundary between pages 40 and 41; all extracted mathematical evidence is on pages 1–40.'
 ]),source_notes=[
  'This is a source and statement-prerequisite audit of arXiv:2210.08393v4, not certification of its proofs or equality to the final journal wording.',
  'The source ambiguities in weighted matrices, unsuffixed local size, inherited coefficient-shift assumptions and sparse tuning are retained explicitly.',
  'Original Theorem and Assumption labels remain separate from proposed computational interfaces.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],unresolved_statement_references=ambient['unresolved_statement_references'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Source transcription and statement-prerequisite audit, not proof certification or source repair.','Pinned preprint audited; equality to final journal wording is not established.','All appendix mathematics are excluded; deferred details are explicitly marked unresolved.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
