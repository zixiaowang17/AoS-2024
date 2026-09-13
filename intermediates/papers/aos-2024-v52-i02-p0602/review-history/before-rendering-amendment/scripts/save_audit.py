"""Independently check source enumeration, inventory fidelity and model-specific reach."""
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
assert len(pdf)==111 and paper['main_text_last_pdf_page']==37
assert not paper['main_text_boundary']['shared_page_with_appendix']
title=pdf[0].get_text()
assert '2208.13074v2' in title and '4 Jul 2023' in title
assert all(a in title for a in ['Jiaqi Li','Likai Chen','Weining Wang','Wei Biao Wu'])
assert paper['source_url']=='https://arxiv.org/pdf/2208.13074v2'
assert [1,'Appendix Simulation and Application',38] in pdf.get_toc()
assert (ROOT/'evidence/appendix-heading-only.png').is_file()
labels=[]
for n in range(37):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                if span['font']=='CMBX10':
                    match=re.fullmatch(r'Theorem (\d+)',span['text'].strip())
                    if match:labels.append((n+1,match.group(1)))
assert labels==[(10,'1'),(15,'2'),(21,'3'),(30,'4')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
members=[m for x in data['interfaces'] for m in x['members']]
byid={m['local_id']:m for m in members}
claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
related={x['members'][0]['local_id']:{r['claim_id'].split('/T')[-1] for r in x['related_theorems']} for x in data['interfaces']}
reach={n:{lid for lid,ns in related.items() if n in ns} for n in claims}
assert reach['4']=={'D'+str(n) for n in range(25,41)}
assert all(related['D'+str(n)]=={'4'} for n in range(25,41))
assert related['D4']==related['D10']==related['D11']==related['D12']=={'1','2','3'}
assert related['D9']=={'1','3'} and related['D8']=={'1','2'}
assert related['D2']=={'1'}
assert all(related['D'+str(n)]=={'2'} for n in range(13,17))
assert all(related['D'+str(n)]=={'3'} for n in range(17,24))
assert 'D24' not in byid
assert set(claims['2']['depends_on'])=={'D1','D5','D7','D10','D11','D12','D13','D14','D15','D16'}
assert set(claims['4']['depends_on'])=={'D25','D26','D27','D28','D29','D35','D36','D37','D38','D40'}
assert claims['1']['evidence'][1]['page']==11
assert all(r'\tag{'+str(n)+'}' in claims['1']['statement_original'] for n in [14,15,16])
assert r'\delta_p^2\geq3\omega' in claims['2']['statement_original']
assert r'/(1+\Gamma_k)' in claims['2']['statement_original']
assert r'\widehat\gamma_k-\gamma_{k^*}' in claims['2']['statement_original']
assert r'(p\log(n))^{1/4}(bn)^{-1/2}' in claims['2']['statement_original']
assert all(r'\tag{'+str(n)+'}' in claims['3']['statement_original'] for n in [35,36,37])
assert r'(nS)^{4/q}p^{2/q}\log^3(pn)' in claims['3']['statement_original']
assert r'\frac{2v}{q\xi}' in claims['4']['statement_original']
assert r'\frac{(2+q)v}{2q\xi}+\frac{3q}{q-4}' in claims['4']['statement_original']
assert r'\log^{8v}(pn)=o(c_{p,n})' in claims['4']['statement_original']
assert r'\min_{0\leq k\leq K}' in byid['D16']['statement_original']
assert r'\widehat\mu^{(l)}_{\widehat\tau_k-bn}-\widehat\mu^{(r)}_{\widehat\tau_k+bn-1}' in byid['D15']['statement_original']
assert r'\sigma_j^2=\sigma_{j,j}\geq c_\sigma' in byid['D5']['statement_original']
assert r'\sigma(\ell)=\sigma(\ell,\ell)' in byid['D32']['statement_original']
assert r"\mathbf1_{j\in\mathcal L_s\cap\mathcal L_{s'}}\Xi_{i,i'}" in byid['D23']['statement_original']
assert r'\text{if }i=0\text{ or }s=0' in byid['D31']['statement_original']
assert r"k\geq0,\ell'\in\mathbb Z\big)" in byid['D31']['statement_original']
assert r'0<\zeta\leq1' in byid['D40']['statement_original']
assert r'0\leq\zeta' not in byid['D40']['statement_original']
assert r"\mathbf1_{\ell_1,\ell_2\in\mathcal B_s\cap\mathcal B_{s'}\cap\mathcal L_0}" in byid['D40']['statement_original']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=4,interfaces=39,source_members=39,direct_theorem_uses=34,related_theorem_connections=59,unranked_auxiliary_passages=10),counts
assert set(ambient['standard_ambient_resolution'])=={'shared','1','2','3','4'}
assert len(ambient['unresolved_source_conventions'])==15
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=37 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=37 for e in ctx['evidence'])
        fragments.append(ctx['text'])
    for text in fragments:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,('unbalanced braces',item)
            assert depth==0,('unbalanced braces',item)
for x in data['interfaces']:
    assert x['related_theorems']
    for m in x['members']:
        own=m['statement_original']+' '+m['local_label']
        linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors)
        assert all(s in linked for s in selectors)
for n in [1,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,21,25,26,27,28,29,30,37]:
    shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=111,main_text_last_pdf_page=37,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent font-sensitive enumeration of all 37 main pages finds exactly CMBX10 Theorem headings 1,2,3,4. Theorem 1 continues from page 10 onto page 11. Main references end on page 37; the saved heading crop establishes Appendix A on a separate page 38.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'Inventory and final census pass separate validator invocations. The independent inventory hash is unchanged and all original theorem fields survive the handoff.',
  'The four authors, arXiv v2 stamp of 4 July 2023, versioned URL, 111-page count, source hash and main-text endpoint match the pinned source.',
  'All theorem bodies were visually checked on pages 10,11,15,21,30. The full continuation of Theorem 1 and all three parts and optional stronger localization clause of Theorem 2 are retained.',
  'The 39 source passages were inspected against rendered main pages. Numbered Assumptions keep their source type, and natural-language names, naming contexts and all highlight selectors are source-backed.',
  'Theorem 2 imports condition (15) but not the separate log-bandwidth condition of Theorem 1. Its algorithm threshold is an input rather than a mandatory Gaussian critical quantile.',
  'Theorem 3 uses Assumptions 1-3 and 5, the localized null, neighborhood sizes, normalized statistic and its own printed Gaussian covariance. Assumptions 4,6,7 and the spatial consistency Proposition are not added.',
  'Theorem 4 reaches exactly the 16 general-model interfaces D25-D40. Independent assertions exclude all VMA, diagonal-filter and earlier Gaussian-law interfaces from its reach.',
  'The general and linear moment, temporal-dependence and scale conditions remain separate. The covariance free index, missing zero-lag case, coupling domains, random lattice design and variance-versus-standard-deviation conflict are documented without rewriting formulas.',
  'Ten auxiliary source passages resolve norms, asymptotics, section conventions, condition (15), optional calibration, temporal locations, signal sign, product index and bandwidth. Fifteen source notes record remaining interpretation limits.',
  'The final graph has 34 direct theorem uses and 59 deduplicated same-paper connections. Every interface has a source-backed explanation for every related theorem, and all statement evidence stays in the main text with balanced mathematical grouping.'
 ]),
 source_notes=[
  'This is a census of the pinned arXiv v2 preprint; identity with journal wording has not been established.',
  'Complete means source-fidelity and statement-dependency review is complete. It does not certify the paper’s proof correctness or silently resolve ambiguous source formulas.',
  'Appendix bodies are excluded. References to appendix-only variance estimation or detailed covariance calculations are recorded, without importing those constructions.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Source statements and their prerequisites were reviewed; the original source’s mathematical inconsistencies remain documented.','No appendix body or external supplement was read.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
