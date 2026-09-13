"""Validate the census independently of its finalizer and record the completed source review."""
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
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==26
assert paper['main_text_last_pdf_page']==26 and not paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split());assert paper['title'].upper() in first
for author in ['PREDRAG PILIPOVIC','ADELINE SAMSON','SUSANNE DITLEVSEN']:assert author in first
assert '24-AOS2371' in first and 'Vol. 52, No. 2' in first and '842–867' in first
assert paper['source_url']==prov['source_url'] and paper['source_url'].endswith('/10.1214/24-AOS2371.pdf')
assert paper['version']=='Published version: The Annals of Statistics 52(2), 842–867 (2024)'
assert 'SUPPLEMENTARY MATERIAL' in pdf[22].get_text() and 'SUPPA' in pdf[22].get_text() and 'SUPPB' in pdf[22].get_text()
assert 'REFERENCES' in pdf[22].get_text() and 'R CORE TEAM' in pdf[25].get_text()
assert not any('appendix' in row[1].lower() for row in pdf.get_toc())
labels=[]
for n in range(26):
    page=pdf[n];assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf-8')==page.get_text(),(n+1,'cached evidence differs')
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();match=re.match(r'THEOREM (\d+(?:\.\d+)*)(?=[.\s(])',text)
            if match:
                assert line['spans'][0]['font']=='Times-Roman'
                labels.append((n+1,match.group(1)))
assert labels==[(14,'3.3'),(14,'3.5'),(15,'3.7'),(17,'5.1'),(18,'5.2')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==5
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
expected={'3.3':[1,2,3,4,8,14,15],'3.5':[1,2,3,4,8,9,10,12],'3.7':[1,2,3,4,8,9,10,11,13],'5.1':[1,2,3,4,5,6,7,8,9,10,11,16],'5.2':[1,2,3,4,5,6,7,8,9,10,11,16,17,18]}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
for n in ['3.3','3.5','3.7']:assert reach[n].isdisjoint({'D5','D6','D7','D16','D17','D18'})
assert 'D11' not in reach['3.5'] and 'D11' in reach['3.7']
assert reach['5.1'].isdisjoint({'D17','D18'})
for lid in ['D1','D2','D8']:assert byid[lid]['source_kind']=='source_passage'
for lid,num in [('D3',1),('D4',2),('D5',3),('D6',4),('D7',5),('D11',6)]:
    assert byid[lid]['source_kind']=='assumption' and byid[lid]['source_heading']==f'(A{num})'
for lid in ['D12','D13','D14','D15']:assert byid[lid]['source_kind']=='definition' and byid[lid]['source_heading'].startswith('Definition ')
t33=claims['3.3']['statement_original'];t35=claims['3.5']['statement_original'];t37=claims['3.7']['statement_original'];t51=claims['5.1']['statement_original'];t52=claims['5.2']['statement_original']
assert '(1) The one-step' in t33 and '(2)' in t33 and r'q_2-1/2' in t33 and r'^{2p}' in t33 and r'p\geq1' in t33
for t in [t35,t37]:assert r'C\geq1' in t and r'p\geq2' in t and r'R(h,\mathbf x_0)' in t and r'\|^p' in t
assert '(A6)' not in t35 and '(A6)' in t37
for t in [t51,t52]:assert '(22) or (23)' in t and '(12)' not in t and r'h\to0' in t and r'Nh\to\infty' in t
assert r'Nh^2\to0' not in t51 and r'Nh^2\to0' in t52
assert r'\sqrt{Nh}' in t52 and r'\sqrt N' in t52 and r'\mathbf C^{-1}(\boldsymbol\theta_0)' in t52 and r'\boldsymbol\theta_0\in\Theta' in t52
assert r'\overline\Theta=\overline\Theta_\beta\times\overline\Theta_\Sigma' in byid['D2']['statement_original']
assert r'\overline\Theta_\Sigma' in byid['D6']['statement_original']
for lid in ['D10','D11']:
    assert r'\Theta_\beta' in byid[lid]['statement_original'] and r'\overline\Theta_\beta' not in byid[lid]['statement_original']
assert r'+\mathbf R(h,\mathbf x_0)' in byid['D9']['statement_original']
assert r'\Phi_h^{[1]}\circ\Phi_h^{[2]}' in byid['D12']['statement_original']
assert r'\Phi_{h/2}^{[2]}\circ\Phi_h^{[1]}\circ\Phi_{h/2}^{[2]}' in byid['D13']['statement_original']
assert r'q_1\geq q_2+1/2' in byid['D14']['statement_original']
assert r'\mathbf f_{h/2}^{-1}(\mathbf X_{t_k};\boldsymbol\beta)' in byid['D16']['application_context'][0]['text']
assert r'\tag{22}' in byid['D16']['statement_original'] and r'\tag{23}' in byid['D16']['statement_original']
assert r'\operatorname{Tr}D\mathbf N(\mathbf X_{t_k};\boldsymbol\beta)' in byid['D16']['statement_original']
assert r's=d(d+1)/2' in byid['D17']['statement_original'] and r'\operatorname{diag}' in byid['D17']['statement_original']
assert r'\frac12\operatorname{Tr}' in byid['D18']['statement_original'] and r'\,d\nu_0(\mathbf x)' in byid['D18']['statement_original']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=5,interfaces=18,source_members=18,direct_theorem_uses=39,related_theorem_connections=50,unranked_auxiliary_passages=8),counts
assert set(ambient['standard_ambient_resolution'])=={'shared',*claims} and len(ambient['unresolved_source_conventions'])==19
math_fragments=0
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=26 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=26 for e in ctx['evidence']);fragments.append(ctx['text'])
    for text in fragments:
        assert not re.search(r'[\u4e00-\u9fff]',text)
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            math_fragments+=1;depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,('unbalanced braces',item)
            assert depth==0,('unbalanced braces',item)
assert math_fragments>100,math_fragments
for x in data['interfaces']:
    assert x['related_theorems'] and set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
    for m in x['members']:
        own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors) and all(s in linked for s in selectors)
    for k in x['source_keywords']:
        m=byid[k['local_id']];texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])];assert any(k['source_text'] in t for t in texts)
for n in [1,6,7,8,9,10,13,14,15,17,18,23,26]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=26,main_text_last_pdf_page=26,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent enumeration of actual small-cap THEOREM headings across all 26 published PDF pages, checked against the source images on pages 14,15,17,18. Exactly 3.3,3.5,3.7,5.1,5.2 occur. Restated external results are included; citations and other result labels are excluded. Separate supplement links on page 23 were not opened.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'Published title, all authors, volume, issue, page range, DOI, 26-page count and pinned PDF hash checked. Cached page texts match fresh byte-preserving extraction.',
  'Inventory and final census both validate; the independent inventory hash matches and every original claim field survives unchanged.',
  'All five complete theorem statements visually checked on pages 14,15,17,18, including explicit A6, moment orders, approximate-objective references and all asymptotic conditions.',
  'The SDE, filtered experiment, closed parameter domain and true covariance shorthand checked on pages 1 and 6; A1-A5 checked individually on page 7.',
  'The OU integral covariance, affine mean, nonlinear flow, A6 and both exact splitting compositions checked on page 8. The unbarred flow domain and the printed R(h,x_0) covariance remainder are preserved.',
  'Definitions 3.1 and 3.2 checked on page 13, retaining q1>=q2+1/2, conditional errors and all-p moment bounds.',
  'Full objectives and transformed residual checked on page 9; inverse identity and argmin checked on page 10. Their differences from the approximate objectives on page 17 remain explicit.',
  'Half-vectorization order, diagonal alternative, information blocks, true-parameter derivatives and distinct drift/covariance convergence scales checked on pages 17-18.',
  'Independent graph traversal confirms all 39 direct and 50 related connections, with no estimation assumptions imported into generic numerical results and no information matrix imported into consistency.',
  'Every interface has exact source terms, source-kind metadata, meaningful matching highlight selectors and an explanation for every related theorem path.',
  'Eight auxiliary passages and nineteen convention notes preserve essential notation and unresolved source distinctions without changing quoted statements.',
  'The publication ends in references on page 26; supplementary mathematical material and code are separate files and were excluded.'
 ]),source_notes=[
  'The audited source is the published journal article, DOI 10.1214/24-AOS2371, rather than a preprint.',
  'The estimation Theorems explicitly name approximate objectives (22)/(23), while practice uses full objectives (12)/(14). No equivalence of minimizers is assumed.',
  'Inverse existence is stated asymptotically on the open drift domain. Global finite-step invertibility, inverse-growth bounds and behavior at search-boundary parameters are not supplied by that wording.',
  'The inverse-Jacobian identity on page 10 is retained with its original argument, with the argument discrepancy recorded separately.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Source transcription and statement-prerequisite audit, not proof certification or source repair.','Separate supplementary article and code were excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
