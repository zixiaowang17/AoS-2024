"""Independently check the seven source statements and their distinct requirements."""
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
assert len(pdf)==50 and paper['main_text_last_pdf_page']==50
assert not paper['main_text_boundary']['shared_page_with_appendix']
title=' '.join(pdf[0].get_text().split())
assert '2111.02826v4' in title and '1 Oct 2023' in title
assert paper['title'].casefold() in title.casefold()
assert all(a in title for a in ['Nilanjana Laha','Aaron Sonabend-W','Rajarshi Mukherjee','Tianxi Cai'])
assert paper['source_url']=='https://arxiv.org/pdf/2111.02826v4'
assert [1,'Supplement',42] in pdf.get_toc()
assert '12. Supplement' in pdf[42].get_text()
assert 'Due to the size of the Supplement' in pdf[42].get_text()
assert 'References' in pdf[42].get_text() and 'Fig 5:' in pdf[49].get_text()
labels=[]
for n in range(50):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            spans=line['spans'];text=''.join(span['text'] for span in spans).strip()
            if spans and spans[0]['font']=='CMBX10' and text.startswith('Theorem '):
                match=re.match(r'Theorem (\d+)(?:\.| \()',text)
                assert match,(n+1,text)
                labels.append((n+1,match.group(1)))
assert labels==[(12,'1'),(15,'2'),(18,'3'),(23,'4'),(26,'5'),(26,'6'),(27,'7')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==7
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
members=[m for x in data['interfaces'] for m in x['members']]
byid={m['local_id']:m for m in members}
claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
related={x['members'][0]['local_id']:{r['claim_id'].split('/T')[-1] for r in x['related_theorems']} for x in data['interfaces']}
reach={n:{lid for lid,ns in related.items() if n in ns} for n in claims}
all_theorems=set(claims)
for lid in ['D1','D2','D3','D4','D5','D6','D7','D8','D9','D11','D12']:
    assert related[lid]==all_theorems,(lid,related[lid])
assert related['D10']==related['D13']=={'1','3','4','5','6','7'}
assert related['D16']==related['D17']==related['D18']=={'1'}
assert related['D20']==related['D29']=={'2'}
assert related['D19']=={'3','4','5','6','7'}
assert related['D14']==related['D24']=={'4','5','6','7'}
assert related['D25']=={'4','5'} and related['D26']=={'6','7'}
assert related['D27']==related['D28']=={'4'}
assert related['D21']==related['D22']==related['D23']==related['D30']=={'5','6','7'}
assert related['D31']=={'5'}
assert set(claims['1']['depends_on'])=={'D16','D17','D18'}
for n in ['1','2']:assert 'D19' not in reach[n]
assert 'D16' not in reach['3']
assert reach['4'].isdisjoint({'D21','D22','D23','D26','D30','D31'})
for n in ['5','6','7']:assert reach[n].isdisjoint({'D27','D28'})
for n in ['6','7']:assert reach[n].isdisjoint({'D25','D31'})
assert r'\operatorname{int}(\operatorname{dom}(\psi))' in claims['1']['statement_original']
assert r'\widetilde d_1(H_1)=\{1,-1\}' in claims['2']['statement_original']
assert r'a_1=\widetilde d_1(h_1)' in claims['2']['statement_original']
assert r'h_2\equiv(h_1,a_1,y_1,o_2)' in claims['2']['statement_original']
assert r'\frac{\big(V_\psi^*-V_\psi(f_1,f_2)\big)}{(C_\phi/2)^2}' in claims['3']['statement_original']
assert [e['page'] for e in claims['4']['evidence']]==[23,24]
assert r'\mathcal H_2\times\{0,1\}' in claims['4']['statement_original']
assert r"\dfrac{\delta_n^{\alpha'+2-\kappa}}{(\alpha-\alpha')a_n^{\kappa-1}}" in claims['4']['statement_original']
assert r'a_n\delta_n\exp(-\kappa a_n\delta_n/2)' in claims['4']['statement_original']
assert r'a_n=n^a' in claims['5']['statement_original']
assert r'\rho_n\log A_n=o(n)' in claims['5']['statement_original']
assert r'\mathit{Opt}_n<1/2' in claims['6']['statement_original']
assert r'\mathit{Opt}_n<1/2' not in claims['7']['statement_original']
assert r'$n>N_0$' in claims['7']['statement_original']
assert r'N_{[\ ]}(\epsilon,\mathcal U_n,L_2(\mathbb P_n))' in claims['7']['statement_original']
assert r'\log N_{[\ ]}' not in claims['7']['statement_original']
assert 'bounded away from zero' in byid['D26']['statement_original']
assert '1/2' not in byid['D26']['statement_original']
assert r'\mathbb E[Y_1+U_2^*(H_2)' in byid['D7']['statement_original']
assert r'\mathbb E[|Y_1+Y_2|]' in byid['D7']['statement_original']
assert r'$\pi_t(A_t\mid H_t)>C_\pi$' in byid['D3']['statement_original']
assert 'measurable' in byid['D9']['statement_original']
assert r'\mathcal D=(O_1,A_1,Y_1,O_2,A_2,Y_2)' in byid['D1']['statement_original']
assert r'$\|f_u-f_l\|<\epsilon$' in byid['D30']['statement_original']
assert r'P(0<|\eta_1(H_1)-1/2|\leq t)' in byid['D25']['statement_original']
assert r'$\phi(x)+\phi(-x)=C_\phi$' in byid['D19']['statement_original']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=7,interfaces=30,source_members=30,direct_theorem_uses=61,related_theorem_connections=126,unranked_auxiliary_passages=14),counts
assert set(ambient['standard_ambient_resolution'])==all_theorems|{'shared'}
assert len(ambient['unresolved_source_conventions'])==24
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=50 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=50 for e in ctx['evidence'])
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
for n in [1,5,6,7,8,9,12,14,15,16,17,18,20,21,22,23,24,25,26,27,42,43,50]:
    shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=50,main_text_last_pdf_page=50,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent inspection of all bold CMBX10 Theorem headings across the 50-page main-paper PDF finds exactly Theorems 1-7. Ordinary-font mentions, proof citations and other result labels are excluded. Theorem 4 has a type-B continuation on page 24. A supplement notice on physical page 43 links to a separate unopened document; references and main-paper figures continue to page 50.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'The independent inventory and final census pass separate validator calls; the inventory hash matches its prior source review and all original claim fields survive unchanged.',
  'The title, four authors, arXiv v4 stamp of 1 October 2023, versioned URL, 50-page count and PDF digest agree with the inspected source. Physical page 43 corrects the outline’s off-by-one supplement location; no supplement body is embedded or used.',
  'All seven complete theorem statements were visually checked on pages 12,15,18,23,24,26,27, including both hinge-policy branches, the exact regret divisor, all type-dependent approximation rates and every finite-sample growth/probability condition.',
  'The longitudinal record, histories, potential-outcome context, two propensity functions and separate assumptions I-IV were checked on pages 5-7. The conditional-integrability formulas retain their distinct absolute-value scopes.',
  'The source optimal policies, measurable score class, original and surrogate values, maximizing-score rules, regrets and eta maps were checked on pages 7-9. Extended maximizer conventions and the absence of attainment requirements in Definition 1 remain explicit.',
  'Theorem 1 depends on sequential Fisher consistency and the source closedness/strict-concavity conventions. Theorem 3 gives a regret inequality and does not acquire the Fisher-consistency predicate merely because the following prose deduces consistency.',
  'The generic surrogate definition does not inherit Condition 2. That condition is used only by Theorems 3-7; hinge loss and its reward condition are confined to Theorem 2, and the two derivative types are confined to Theorem 4.',
  'Outcome bound A applies to Theorems 4-7; small-noise B to Theorems 4/5; literal strong-separation C to Theorems 6/7. The graph does not treat the source C as an equivalent version of B or repair its center from zero to one half.',
  'Empirical value, fitted product classes and optimization error are resolved for Theorems 5-7. Theorem 5 uses the coordinatewise sup-norm condition (21); Theorem 6 uses logarithmic empirical-L2 condition (23); Theorem 7 retains its inline pair-class bracketing-number bound (24).',
  'Theorem 7 does not inherit Opt_n<1/2 or rho_n<1 from Theorem 6. The general-class theorems do not inherit neural-network, wavelet, Assumption D, derivative-type or optimizer-convergence assumptions from examples or proofs.',
  'Fourteen auxiliary passages and twenty-four source notes resolve effective domains, norm and probability conventions, known propensities, outcome positivity, common noise exponent and source inconsistencies. Independent graph checks cover 61 direct uses and 126 related-theorem connections, with matching source selectors and explanations for every interface.'
 ]),
 source_notes=[
  'The census uses the pinned arXiv v4 preprint; identity with the final journal wording has not been established.',
  'No separate supplement was opened. Its proof references remain references, and unresolved assumptions or claims are not repaired using material outside the main paper.',
  'Source fidelity and dependency validation do not certify proof correctness. The literal positivity quantifier, treatment coding, strict-concavity diagonal, strong-separation center, later value display and entropy quantifier issues remain documented.',
  'The source calls a bracket count bracketing entropy. Its actual N and log N conditions remain distinct, with the stated norms and exponents unchanged.',
  'All source definitions and conditions retain their original labels, with natural-language source keywords and notation kept in the detailed passages. Standard ambient primitives are resolved separately without inventing additional theorem claims.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Main-paper source transcription and statement-dependency review, without proof certification or source repairs.','The separate supplement and any appendix mathematics were excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
