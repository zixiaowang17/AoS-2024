"""Check source enumeration, statement fidelity and each design-specific dependency set."""
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
assert len(pdf)==25 and paper['main_text_last_pdf_page']==25
assert not paper['main_text_boundary']['shared_page_with_appendix']
title=pdf[0].get_text()
assert '2401.12331v2' in title and '27 Mar 2024' in title
assert all(a.upper() in title for a in ['T. Tony Cai','Dongwoo Kim','Hongming Pu'])
assert paper['source_url']=='https://arxiv.org/pdf/2401.12331v2'
assert [1,'Supplementary Material',23] in pdf.get_toc()
assert [1,'References',24] in pdf.get_toc()
assert "Author's addresses" in str(pdf.get_toc())
labels=[];all_headings=[]
for n in range(25):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(span['text'] for span in line['spans']).strip()
            if text.startswith('THEOREM'):all_headings.append((n+1,text))
            match=re.fullmatch(r'THEOREM (\d+\.\d+) \((.+)\)\.',text)
            if match:
                assert all(span['font']=='NimbusRomNo9L-Regu' for span in line['spans'])
                labels.append((n+1,match.group(1)))
assert len(all_headings)==8
assert labels==[(6,'2.1'),(8,'2.2'),(9,'2.3'),(12,'2.4'),(12,'3.1'),(13,'3.2'),(14,'3.3'),(17,'3.4')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==8
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
members=[m for x in data['interfaces'] for m in x['members']]
byid={m['local_id']:m for m in members}
claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
related={x['members'][0]['local_id']:{r['claim_id'].split('/T')[-1] for r in x['related_theorems']} for x in data['interfaces']}
reach={n:{lid for lid,ns in related.items() if n in ns} for n in claims}
all_theorems=set(claims);transfer={'2.2','2.3','2.4','3.2','3.3','3.4'}
for lid in ['D1','D3','D4','D6']:assert related[lid]==all_theorems
assert related['D2']==related['D7']==transfer
assert related['D17']=={'2.1','3.1'}
assert related['D8']=={'2.1','2.2','2.3','2.4'}
assert related['D9']=={'3.1','3.2','3.3','3.4'}
assert related['D10']==related['D11']==related['D12']=={'2.2','2.4','3.2','3.4'}
assert related['D14']=={'2.4'} and related['D16']=={'3.4'}
for n in ['2.1','3.1']:assert reach[n].isdisjoint({'D2','D7','D10','D11','D12','D14','D16'})
for n in ['2.3','3.3']:assert reach[n].isdisjoint({'D10','D11','D12','D14','D16','D17'})
assert 'D9' not in reach['2.4'] and 'D8' not in reach['3.4']
assert byid['D10']['depends_on']==[]
assert r'\mathcal D^{[s,\ell]}' in claims['3.3']['statement_original']
assert r'T_{m_t+1}^{[s]}=1' in claims['2.2']['statement_original']
assert r'\lceil m_t/2B_t(d_t+1)\rceil^{-1}' in claims['2.2']['statement_original']
assert r'\wedge\lceil2B_sKm_s\rceil^{-1}' in claims['3.2']['statement_original']
assert r'\log^2(Kn_s)' in claims['3.2']['statement_original']
assert r'\frac1{r_{\max}}\sum_{r=1}^{r_{\max}}\widehat g_r^{[t]}' in claims['2.4']['statement_original']
assert r'\frac1{r_{\max}}\sum_{r=1}^{r_{\max}}\widehat g_r^{[t]}' in claims['3.4']['statement_original']
assert [e['page'] for e in claims['2.2']['evidence']]==[8,9]
assert [e['page'] for e in claims['3.1']['evidence']]==[12,13]
assert [e['page'] for e in claims['3.2']['evidence']]==[13,14]
assert 'largest integer strictly smaller' in byid['D3']['statement_original']
assert r'\frac{T-(q-1)b}{b}' in byid['D10']['statement_original']
assert r'\frac{x-(r-1)b}{b}' in byid['D10']['statement_original']
assert r'$(1/m)$-packing and $(1/2m)$-covering' in byid['D10']['statement_original']
assert r'\sum_{j=1}^{m_t}' in byid['D14']['statement_original']
assert r'(\Delta T_j^{[t]})' in byid['D14']['statement_original']
assert r'\{2^r\leq Km_sn_s:r\in\mathbb Z^+\}' in byid['D16']['statement_original']
assert r'$M_s=\log n_s$ and $M_s=\log n_tn_s$' in byid['D16']['statement_original']
assert r'$B_s\geq C_s$' in byid['D16']['statement_original']
assert r'\sum_{(T,Y)\in\mathcal D_{\mathrm{test}}^{[t]}}' in byid['D16']['statement_original']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=8,interfaces=14,source_members=14,direct_theorem_uses=36,related_theorem_connections=68,unranked_auxiliary_passages=12),counts
assert set(ambient['standard_ambient_resolution'])==all_theorems|{'shared'}
assert len(ambient['unresolved_source_conventions'])==18
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
    assert set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
    for m in x['members']:
        own=m['statement_original']+' '+m['local_label']
        linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors)
        assert all(s in linked for s in selectors)
for n in [1,2,3,5,6,7,8,9,11,12,13,14,16,17,23,25]:
    shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=25,main_text_last_pdf_page=25,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent examination of every line beginning with the small-cap THEOREM heading across all 25 main-paper pages finds exactly Theorems 2.1-2.4 and 3.1-3.4. Heading labels, complete statement continuations and the separate-supplement notice were checked against rendered source pages.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'The independent inventory and final census pass separate validator calls. Every original theorem field is unchanged, and the inventory hash matches its prior source review.',
  'Title, all three authors, arXiv v2 stamp of 27 March 2024, versioned source URL, 25-page count and PDF digest match the pinned source. Section 6 proofs are in the main paper; the page-23 supplement notice refers to a separate unopened document.',
  'All eight full theorem statements were visually checked on pages 6,8,9,12,13,14,17. The three page-spanning statements retain their complete continuations, hypotheses, algorithms, constants, bounds and estimator quantifiers.',
  'The full observation and mean/difference model, bounded Hölder convention and pointwise sub-Gaussian assumption were checked against pages 2,3,5,6. They do not impose smoothness on the subject curves or order alpha_delta above alpha_m.',
  'The conventional restriction of P is recorded with both explicit n_s=0 passages. Its graph does not require source samples, the full transfer experiment or any of the named estimation algorithms.',
  'Common and independent design reach is disjoint by theorem family. The generic algorithm chooses a design branch; its definition does not add both design assumptions to a theorem.',
  'The minimax lower bounds quantify arbitrary estimators and have no local-polynomial, conventional, transfer or adaptive algorithm dependencies. Their neighboring upper-bound gap/density conditions are not silently inherited.',
  'Algorithms 1-4 were visually checked on pages 7,8,11,17, retaining every step and the distinction between spacing-weighted and unweighted empirical validation loss. Both adaptive sections explicitly change the total target count to 2n_t.',
  'Theorem 2.4 inherits the common upper-bound assumptions and R_C definitions; Theorem 3.4 inherits the independent assumptions and R_I definitions. Their empirical selection procedures replace the earlier oracle comparisons, and both repetition averages remain intact.',
  'Twelve auxiliary passages resolve sizes, norm/asymptotic conventions, source averaging, inheritance, sample splitting and rate definitions. Eighteen source notes retain unresolved algorithm/domain conventions and printed inconsistencies without repairing source text.',
  'Independent graph and selector checks cover all 14 interfaces, 36 direct uses and 68 deduplicated theorem connections. Every interface has source keywords, original passages, matching highlights and source-backed explanations for all related theorems.'
 ]),
 source_notes=[
  'The inspected artifact is the pinned arXiv v2 preprint; equality with the final journal wording has not been established.',
  'The entire PDF is the main paper. The separate supplement was not opened, and no appendix or supplement result was used to complete a statement or its dependencies.',
  'Source-fidelity and dependency validation do not certify proof correctness or repair the printed algorithms. In particular, empty-interval selection, the free polynomial index, positive dyadic bandwidths and the duplicate threshold assignment remain documented.',
  'The complete original class paragraph is retained for both its full and conventional applications. The latter is interpreted through the paper’s explicit no-source setup, with that projection limitation stated separately.',
  'The source labels R_C and R_I are local scalar rate definitions inside their respective upper-bound Theorems. They are archived and resolved for adaptive reuse without inventing new statistical functionals.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Main-paper source transcription and theorem-statement dependency review; no proof certification.','No separate supplement or appendix inspection.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
