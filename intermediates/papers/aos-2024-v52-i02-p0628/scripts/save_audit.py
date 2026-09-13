"""Independently verify source enumeration and distinct theorem requirements."""
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
assert len(pdf)==66 and paper['main_text_last_pdf_page']==25
assert not paper['main_text_boundary']['shared_page_with_appendix']
title=pdf[0].get_text()
assert '2210.17439v2' in title and '12 Feb 2024' in title
assert all(a.upper() in title for a in ['Patrick Bastian','Holger Dette','Johannes Heiny'])
assert paper['source_url']=='https://arxiv.org/pdf/2210.17439v2'
assert [1,'Online supplement: proofs',26] in pdf.get_toc()
assert (ROOT/'evidence/appendix-heading-only.png').is_file()
labels=[]
for n in range(25):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(span['text'] for span in line['spans'])
            match=re.fullmatch(r'THEOREM (\d+\.\d+)\.',text.strip())
            if match:
                assert all(span['font']=='NimbusRomNo9L-Regu' for span in line['spans'])
                labels.append((n+1,match.group(1)))
assert labels==[(8,'2.2'),(9,'2.4'),(10,'2.5'),(12,'2.8'),(18,'3.5')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
members=[m for x in data['interfaces'] for m in x['members']]
byid={m['local_id']:m for m in members}
claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
related={x['members'][0]['local_id']:{r['claim_id'].split('/T')[-1] for r in x['related_theorems']} for x in data['interfaces']}
reach={n:{lid for lid,ns in related.items() if n in ns} for n in claims}
assert related['D9']=={'2.2','2.4'}
assert related['D7']==related['D8']=={'2.2','2.4','2.5'}
assert related['D13']==related['D14']=={'2.2','3.5'}
assert related['D17']==related['D18']==related['D19']==related['D20']==related['D22']=={'2.5','2.8'}
assert related['D21']=={'2.5'}
assert related['D23']==related['D24']=={'2.8'}
assert related['D4']==related['D25']==related['D26']=={'3.5'}
assert reach['2.4'].isdisjoint({'D12','D13','D14','D17'})
assert reach['2.8'].isdisjoint({'D7','D8','D9','D13','D14','D21'})
assert reach['3.5'].isdisjoint({'D3','D7','D8','D9','D17','D18','D19','D20','D21','D22','D23','D24'})
assert byid['D16']['depends_on']==[]
assert 'D14' not in byid['D22']['depends_on']
assert r'\alpha\in(0,1-e^{-1})' in claims['2.2']['statement_original']
assert 'with strict inequality' in claims['2.2']['statement_original']
assert r'\sup_{d\in\mathbb N}\max_{i=1}^d|\theta_i|<\Delta' in claims['2.2']['statement_original']
assert set(claims['2.4']['depends_on'])=={'D8','D9','D15'}
assert r'B_n^3(\log(nd))^{1+2/\beta}' in claims['2.5']['statement_original']
assert r'\mathcal H_1(c(\log(nd))^{1/\beta})' in claims['2.5']['statement_original']
assert r'\mathcal H_1(c(\log(nd))^{1/\beta})' in claims['2.8']['statement_original']
assert 'defined in defined in (2.26)' in claims['2.8']['statement_original']
assert r'\mathcal T_{n,\Delta}^{\mathrm{abs}}' in claims['2.8']['statement_original']
assert r'\mathcal T_n^{*,\mathrm{abs}}' not in claims['2.8']['statement_original']
assert r'\log(p)n/p^2\to0' in claims['3.5']['statement_original']
assert r'\inf_{T_\alpha\in\mathcal T_\alpha}\sup_{F\in\mathcal H_1(c_0)}' in claims['3.5']['statement_original']
assert r'\text{ does not reject }H_0' in byid['D25']['statement_original']
assert r'\underline b' in byid['D12']['statement_original']
assert r'\Delta,&\text{otherwise}' in byid['D20']['statement_original']
assert r'\frac{m^2(n-1)}{n(n-m)^2}' in byid['D7']['statement_original']
assert 'columns above the diagonal' in byid['D4']['statement_original']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=5,interfaces=26,source_members=26,direct_theorem_uses=31,related_theorem_connections=74,unranked_auxiliary_passages=7),counts
assert set(ambient['standard_ambient_resolution'])=={'shared','2.2','2.4','2.5','2.8','3.5'}
assert len(ambient['unresolved_source_conventions'])==14
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
for x in data['interfaces']:
    assert x['related_theorems']
    for m in x['members']:
        own=m['statement_original']+' '+m['local_label']
        linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors)
        assert all(s in linked for s in selectors)
for n in [1,4,5,6,7,8,9,10,12,14,15,18,25]:
    shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=66,main_text_last_pdf_page=25,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent enumeration joins each line’s small-cap THEOREM spans across all 25 main pages and finds exactly labels 2.2,2.4,2.5,2.8,3.5. All statements fit on their cited page. Acknowledgements end page 25; Appendix A begins on a separate page 26.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'Inventory and final census pass separate validator invocations. The independent inventory hash is unchanged and every original theorem field survives the handoff.',
  'The title, three authors, arXiv v2 stamp of 12 February 2024, versioned URL, 66-page count, PDF hash and main-text boundary match the pinned source.',
  'All five full theorem bodies were checked visually on pages 8,9,10,12,18. The exact alpha range, strictness and case clauses, growth powers, bounded-kernel refinements and minimax quantifiers are retained.',
  'Twenty-six source passages preserve the iid model, symmetric kernel, U-statistic, first projection, jackknife estimator, Gumbel law, Orlicz quantity, all four regularity assumptions, distribution classes and distinct bootstrap constructions.',
  'The source empty-minimum convention, strict non-degeneracy cutoff, positive-side truncation for every outside value and upper-triangle vech convention are retained.',
  'Independent graph checks confirm that Theorem 2.4 does not inherit (A2),(A3), (A1-prime) or the composite-null class. Its alternative class has only the conditions actually defined in (2.18).',
  'Theorem 2.8 inherits the assumptions and rate (2.24) of Theorem 2.5 but has no jackknife, normalized squared-statistic or Gumbel-calibration requirements. The shared V_0 region has no assumption dependencies.',
  'Bootstrap theorems do not inherit (A3). Their conditional resampling, V-statistic expectation, source truncation and conditional quantile are kept explicit.',
  'The arbitrary-test lower bound uses the printed uniform-level class and covariance specialization, without acquiring any specific test statistic or bootstrap implementation. Its erroneous null nonrejection event is documented without correction.',
  'Seven auxiliary passages and fourteen source notes resolve inherited assumptions, distribution classes, kernel specialization, scale/domain omissions and source inconsistencies. The final graph has 31 direct uses and 74 same-paper connections, with source-backed explanations and matching selectors.'
 ]),
 source_notes=[
  'This census uses the pinned arXiv v2 preprint; equality with journal wording has not been established.',
  'The initial boundary preview incidentally included two introductory lines below the appendix heading. The retained crop was tightened to the heading only; no supplement mathematics, theorem statements or proofs were inspected or used.',
  'Source-fidelity review does not certify proof correctness. In particular, the printed minimax test-class event conflicts with the lower bound, and remains explicitly documented.',
  'Corollaries for particular dependence measures and proofs in the online supplement are outside the Theorem inventory. Their extra assumptions are not imported into the five saved statements.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Original-source transcription and statement-dependency review, without repairing source claims.','Supplement mathematics and proofs were excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
