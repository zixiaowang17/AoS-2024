"""Independently validate the published source, five statements and two-model graph."""
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
pdf=fitz.open(PDF);assert len(pdf)==paper['main_text_last_pdf_page']==28
assert not paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split())
assert paper['title'].upper() in first
for a in ['YULING YAN','YUXIN CHEN','JIANQING FAN']:assert a in first
assert '10.1214/24-AOS2366' in first and '2024, Vol. 52, No. 2, 729–756' in first
assert paper['source_url'].endswith('/10.1214/24-AOS2366.pdf')
assert 'Published version:' in paper['version']
assert [1,'Supplementary Material',25] in pdf.get_toc()
assert 'SUPPLEMENTARY MATERIAL' in pdf[24].get_text() and 'REFERENCES' in pdf[24].get_text()
assert '24-AOS2366SUPP' in pdf[24].get_text()
assert 'ZHU, Z.' in pdf[27].get_text() and 'ZHOU,' in pdf[27].get_text()
labels=[]
for n,page in enumerate(pdf,1):
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();match=re.match(r'THEOREM (\d+)\.',text)
            if match:labels.append((n,match.group(1)))
assert labels==[(7,'1'),(9,'2'),(11,'3'),(12,'4'),(21,'5')],labels
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
assert reach=={
 '1':{f'D{i}' for i in range(1,11)},
 '2':{f'D{i}' for i in range(1,12)},
 '3':{f'D{i}' for i in [1,2,3,4,5,6,7,9,10,12]},
 '4':{f'D{i}' for i in [1,2,3,4,5,6,7,9,10,12,13]},
 '5':{f'D{i}' for i in [5,14,15,16,17,18]}
},reach
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
assert 'D11' not in reach['4'] and 'D13' not in reach['2']
for n in ['1','2','3','4']:assert reach[n].isdisjoint({f'D{i}' for i in range(14,19)})
assert reach['5'].isdisjoint({f'D{i}' for i in range(1,14)}-{'D5'})
assert byid['D7']['source_kind']=='definition' and byid['D15']['source_kind']=='assumption'
assert byid['D7']['statement_original']!=byid['D15']['statement_original']
t1=claims['1']['statement_original'];t2=claims['2']['statement_original'];t3=claims['3']['statement_original'];t4=claims['4']['statement_original'];t5=claims['5']['statement_original']
for snippet in [r'$p<1-\delta$',r'$p=1$',r'ndp^2\gtrsim\log^9(n+d)',r'\frac{\log^2(n+d)}{\sqrt{nd}\,p}',r'\mathcal N(\mathbf0,\mathbf\Sigma_{U,l}^\star)\{C\}',r'\frac{2(1-p)^2}{np^2}S_{l,i}^{\star2}']:assert snippet in t1,snippet
assert r'\sup_{1\leq l\leq d}' in t2 and r'\mathbf U_{l,\cdot}^\star\mathbf R^\top' in t2
assert r'ndp^2\gtrsim\log^7(n+d)' in t3 and r'\log^9' not in t3
assert r'\sqrt{\frac{\log^7(n+d)}{ndp^2}}' in t3
assert r'ndp^2\gtrsim\log^8(n+d)' in t4 and r'\log^9' not in t4
assert [e['page'] for e in claims['5']['evidence']]==[21,22]
assert r't_0\geq\log(\frac{\sigma_1^{\star2}}{\zeta_{\mathrm{op}}})' in t5
assert r'\kappa^{\natural4}\mu^\natural r+\mu^{\natural2}r\log^2n' in t5
for eq in ['6.12','6.13a','6.13b','6.13c','6.13d']:assert '\\tag{'+eq+'}' in t5
assert r'\mathbf E\mathbf V^\natural(\mathbf\Sigma^\natural)^{-1}' in t5
assert r'\kappa^{\natural2}\frac{\zeta_{\mathrm{op}}\zeta_{\mathrm{op},m}}{\sigma_r^{\natural4}}' in t5
assert r'\omega_i^2S_{j,j}^\star+\omega_j^2S_{i,i}' in byid['D13']['statement_original']
assert r'\operatorname{var}(E_{i,j}^2)=\sigma_{i,j}^2' in byid['D16']['statement_original']
assert r'\mathbf E=[E_{i,j}]_{1\leq i,j\leq n}' in byid['D14']['statement_original']
assert r'\|\mathbf V^\natural\|_{2,\infty}' in byid['D15']['statement_original']
assert r'\|\mathbf M^\natural\|_\infty' in byid['D15']['statement_original']
assert r'\frac1{np^2}' in byid['D10']['statement_original']
assert r'\frac1{np^2}' not in byid['D17']['statement_original']
assert 'nonsingular' in byid['D8']['statement_original']
assert r'\sigma^2\sqrt{n_1n_2}\log n' in ambient['auxiliary_passages'][5]['statement_original']
assert 'sufficiently large (resp., small) constant' in ambient['auxiliary_passages'][0]['statement_original']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=5,interfaces=18,source_members=18,direct_theorem_uses=35,related_theorem_connections=48,unranked_auxiliary_passages=10),counts
assert set(ambient['standard_ambient_resolution'])=={'shared','1','2','3','4','5'} and len(ambient['unresolved_source_conventions'])==22
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=28 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=28 for e in ctx['evidence']);fragments.append(ctx['text'])
    for text in fragments:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,('unbalanced braces',item)
            assert depth==0,('unbalanced braces',item)
for x in data['interfaces']:
    assert x['related_theorems'] and set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
    for m in x['members']:
        own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors) and all(s in linked for s in selectors)
    for k in x['source_keywords']:
        m=byid[k['local_id']];texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])];assert any(k['source_text'] in t for t in texts)
for n in [1,2,3,4,5,6,7,8,9,10,11,12,13,20,21,22,24,25,28]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=28,main_text_last_pdf_page=28,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent inspection of printed THEOREM headings over all 28 journal pages finds exactly Theorems 1-5, with Theorem 5 continuing on PDF page 22. The supplement notice on page 25 links to a separate document and is followed by references through page 28. Citations to later-numbered supplement theorems and other result types are excluded.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'Inventory and final census pass validation; inventory hash agrees with its source review, and all original claim fields survive unchanged.',
  'Published title, three authors, volume/issue/page range, DOI, source URL, 28-page count and PDF digest were checked. No appendix or supplement body is embedded or used.',
  'Five complete statements were checked visually on pages 7,9,11,12,21,22, including the full Theorem 1 covariance, its exact iteration bound, both confidence statements and all Theorem 5 residual bounds.',
  'The PCA signal, random sampling and row-specific sub-Gaussian noise model were checked on pages 1-2; zero-filled matrix, projections and matrix-sign convention on pages 3-4; population spectral scales, Definition 1 and Assumption 1 on pages 5-6.',
  'Algorithm 2 was checked against its source scaling, inclusive update loop and t_0 output. Algorithms 3/4 were checked in full, preserving the unknown S-star_jj term in Algorithm 4 and missing finite-sample failure conventions.',
  'The two cases of the population entry variance in (3.10)-(3.11) were checked on page 10. Theorem 3’s log^7 and Theorem 4’s log^8 sampling conditions are not replaced by Theorem 1’s log^9 condition.',
  'The general rectangular model, n=max(n_1,n_2), singular-value condition number, all three incoherence inequalities and complete bounded-noise Assumption 3 were checked on page 20. Its var(E_ij squared) expression and square index-range mismatch remain literal.',
  'Algorithm 5, R_U and both zeta quantities were checked on page 21. Theorem 5’s star/natural mismatch in the iteration count remains unresolved rather than importing the PCA spectral model.',
  'Independent local graph traversal confirms that Theorems 1-4 have no general-model assumptions and Theorem 5 has no PCA data/noise or variance-ratio assumptions. Only generic projection primitives are shared across the model branches.',
  'The row confidence procedure belongs only to Theorem 2, and the entry confidence procedure only to Theorem 4. Theorem 2 gives uniform marginal coverage error, not a joint simultaneous coverage event.',
  'Ten auxiliary source passages and twenty-two source-convention notes preserve the unusual constant-factor meaning of <<, norm conventions, signal footnote, iteration reference, rate abbreviations, optional sampling estimate and unresolved source formulas. All 35 direct uses and 48 related connections have source-backed explanations and selectors.'
 ]),source_notes=[
  'The source is the published journal paper, not a preprint. Main-text source fidelity does not certify correctness of its proofs or resolve its apparent typographical errors.',
  'Algorithm 4’s population S-star_jj, Assumption 3’s var(E_ij squared), the rectangular noise-index mismatch and Theorem 5’s starred iteration parameter are preserved and explained separately.',
  'The Gaussian signal statement is retained. Footnote 1’s unrestricted sub-Gaussian extension is archived without asserting unchanged fourth-moment-sensitive covariance-entry variance formulas.',
  'Definition 1 and Assumption 2 remain distinct, as do the two noise models, condition numbers and HeteroPCA scalings. No conditions are transferred through proof-only use of Theorem 5.',
  'No appendix or supplement was opened. Generalized supplement Theorems 11-14, external proof references and comparison results are excluded from the main-text inventory.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Main-paper source transcription and statement-dependency audit, not proof certification or source repair.','All appendix and supplement mathematics were excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
