"""Independently enumerate the source and verify the completed four-theorem census."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text())
PDF=Path(prov['cached_pdf']);WORK=Path(prov['working_pdf']).parent
for name in ['theorem-inventory.json','ranked-interfaces.json']:
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],check=True)
inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
data=json.loads((ROOT/'ranked-interfaces.json').read_text())
ambient=json.loads((ROOT/'ambient-conventions.json').read_text())
review=json.loads((ROOT/'inventory-review.json').read_text())
assert digest(PDF)==paper['pdf_sha256']==prov['pdf_sha256']==digest(WORK/'source.pdf')
assert review['status']=='complete' and review['source_checked']
assert digest(ROOT/'theorem-inventory.json')==review['inventory_sha256']
pdf=fitz.open(PDF)
assert len(pdf)==41 and paper['main_text_last_pdf_page']==25
assert not paper['main_text_boundary']['shared_page_with_appendix']
assert '2207.07299v2' in pdf[0].get_text() and '21 Sep 2023' in pdf[0].get_text()
assert 'September 22, 2023' in pdf[0].get_text()
assert paper['source_url']=='https://arxiv.org/pdf/2207.07299v2'
assert prov['authors']==['Jake A. Soloff','Daniel Xiang','William Fithian']
assert [1,'A Proofs',26] in pdf.get_toc()
assert (ROOT/'evidence/appendix-heading-only.png').is_file()
# No text or image access to appendix bodies.
labels=[]
for n in range(25):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                if span['font']=='CMBX10':
                    match=re.fullmatch(r'Theorem (\d+)\.',span['text'].strip())
                    if match:labels.append((n+1,match.group(1)))
expected=[(8,'1'),(10,'4'),(15,'5'),(17,'6')]
assert labels==expected,labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=4,interfaces=11,source_members=11,direct_theorem_uses=22,related_theorem_connections=25,unranked_auxiliary_passages=7),counts
members=[m for x in data['interfaces'] for m in x['members']]
byid={m['local_id']:m for m in members}
claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
related={x['members'][0]['local_id']:{r['claim_id'].split('/T')[-1] for r in x['related_theorems']} for x in data['interfaces']}
assert related['D8']==related['D9']=={'4'}
assert related['D6']==related['D7']==related['D10']=={'6'}
assert related['D4']=={'1','4'} and related['D11']=={'5','6'}
assert related['D5']=={'1','4','5','6'} and byid['D5']['depends_on']==[]
assert byid['D6']['depends_on']==[]
assert 'Only the final sentence' in next(x for x in data['interfaces'] if x['members'][0]['local_id']=='D3')['theorem_explanations'][PID+'/T1']['text']
assert claims['5']['evidence'][1]['page']==16
assert r'\mathbf1\{R_\ell>0\}' in claims['1']['statement_original']
assert r'p_{(k)}\leq\lambda' in claims['4']['statement_original']
assert r'\widehat\pi_0^\lambda p_{(k)}-\frac{\ell k}{m}' in claims['4']['statement_original']
assert r'm^{1/3}(\widehat\ell-\ell)' in claims['5']['statement_original']
assert r'm^{-1/3}|\widehat\ell-\ell|' in claims['5']['statement_original']
assert all(r'\tag{'+str(n)+'}' in claims['5']['statement_original'] for n in range(23,28))
assert r'\mathbb E\left[\tau_{\widehat\ell}\right]\to t_\ell' in claims['5']['statement_original']
assert r'm^{1/3}(\widehat\pi_0-\pi_0)>\varepsilon' in claims['6']['statement_original']
assert r'\frac{\alpha^2}{2\pi_0^2}\cdot|f' in claims['6']['statement_original']
assert r'\right)^{-1/3}\operatorname{Var}(Z)' in claims['6']['statement_original']
assert r'1+\#\{i:p_i>\lambda\}' in byid['D8']['statement_original']
assert 'last minimizer' in byid['D5']['statement_original']
assert r'W(t)-t^2' in byid['D11']['statement_original']
assert set(ambient['standard_ambient_resolution'])=={'shared','1','4','5','6'}
assert len(ambient['unresolved_source_conventions'])==9
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=25 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=25 for e in ctx['evidence'])
        fragments.append(ctx['text'])
    for text in fragments:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,('unbalanced braces',item)
            assert depth==0,('unbalanced braces',item)
for n in [1,2,3,4,5,6,8,10,11,12,15,16,17,25]:
    shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=41,main_text_last_pdf_page=25,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent font-sensitive enumeration of all 25 main pages finds exactly CMBX10 Theorem headings 1,4,5,6. Lemma 2, Remark 3 and Proposition 7 share the numbering sequence but are excluded from the Theorem inventory. Theorem 5 continues from page 15 onto page 16. Figure 8 ends the main text on page 25; the saved heading crop establishes Appendix A on a separate page 26.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,
 validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'Inventory and final census pass separate validator invocations. The independently reviewed inventory hash is unchanged, and every original theorem field survives the handoff.',
  'The title, three authors, arXiv v2 stamp of 21 September 2023, separate title-page date of 22 September 2023, versioned URL, 41-page count and PDF hash match the inspected source.',
  'All four theorem bodies were visually checked on pages 8,10,15,16,17. Theorem 5 retains its full page continuation, all three assumptions, both distributional limits, the additional condition (25), mean convergence and both variance limits.',
  'Eleven interfaces preserve original model, lfdr, monotonicity, maximum criterion, support-line procedure, weighted loss, oracle, null estimate, modified rule, regret and Chernoff definitions. Their natural-language keywords and selectors are source-backed.',
  'Theorem 1 retains its exact last-rejection identity without monotonicity; the shape condition appears only in the final max-lfdr clause. The source empty-rejection convention and reordered labels are resolved.',
  'The constrained rule in Theorem 4 uses the specific plus-one null-proportion estimate and weak cutoff p_(k)<=lambda. Its connection to ordinary SL is conditional on the unconstrained threshold lying below lambda.',
  'Theorems 5 and 6 do not acquire the particular estimator (12), the constrained rule (13), or the proof-only Grenander implementation. Theorem 6 quantifies an arbitrary estimator under its original one-sided error condition.',
  'The negative m exponent in Theorem 5(25), the one-sided condition in Theorem 6(iii), and the exact regret coefficient are preserved rather than repaired. Source-domain omissions and the reversed abstract description of lfdr are recorded separately.',
  'Seven auxiliary passages resolve sorted labels, cost-derived alpha, population threshold, fixed-threshold regret and constrained-versus-unconstrained distinctions. Nine source notes retain limitations without altering original statements.',
  'The final graph has 22 direct uses and 25 deduplicated same-paper connections. Independent scope assertions confirm estimator-specific and regret-specific reach, and all mathematical evidence lies on main pages with balanced TeX grouping braces.'
 ]),
 source_notes=[
  'This is a census of the pinned arXiv v2 preprint; equivalence to journal wording has not been established.',
  'The original asymptotic tail assumptions and any resulting mathematical issues remain source claims. This audit preserves statements and dependencies without certifying the proofs.',
  'Appendix bodies were excluded. All objects needed to state the inventoried theorems are available in the main text.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Source-fidelity and statement-dependency review; does not repair the source or certify its proofs.','No appendix bodies or external supplements were used.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
