"""Check the pinned source, complete statements, source boundaries and dependency graph."""
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
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==73
assert paper['main_text_last_pdf_page']==33 and paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split())
assert paper['title'].upper() in first
for author in ['PAROMITA DUBEY','YAQING CHEN','HANS-GEORG MÜLLER']:assert author in first
assert '2202.06117v4' in first and '27 Feb 2024' in first
assert paper['source_url']=='https://arxiv.org/pdf/2202.06117v4'
assert paper['version']=='arXiv:2202.06117v4'
assert [1,'Supplementary Material',33] in pdf.get_toc()
cut=prov['main_text_shared_page_cutoff_y'];assert cut==106.52787780761719
# Inspect only the heading rectangle, never the supplement body below it.
heading=pdf[32].get_text(clip=fitz.Rect(0,cut,pdf[32].rect.width,118))
assert 'SUPPLEMENTARY MATERIAL' in heading
main33=pdf[32].get_text(clip=fitz.Rect(0,0,pdf[32].rect.width,cut))
assert 'Funding' in main33 and 'SUPPLEMENTARY MATERIAL' not in main33
labels=[]
for n in range(33):
    page=pdf[n];clip=fitz.Rect(0,0,page.rect.width,cut) if n==32 else page.rect
    text=page.get_text(clip=clip)
    assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_text()==text,(n+1,'cached evidence differs')
    for block in page.get_text('dict',clip=clip)['blocks']:
        for line in block.get('lines',[]):
            line_text=''.join(s['text'] for s in line['spans']).strip();match=re.match(r'THEOREM (\d+(?:\.\d+)*)\.',line_text)
            if match:labels.append((n+1,match.group(1)))
assert labels==[(11,'4.1'),(12,'5.1'),(13,'5.2'),(14,'5.3'),(17,'6.1'),(17,'6.2'),(18,'6.3')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==7
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
 '4.1':[1,2,3,4,5,6],
 '5.1':[1,2,7,10,11,12],
 '5.2':[1,2,4,7,8,10,11],
 '5.3':[1,2,4,5,7,8,9,10,11,13,14],
 '6.1':[1,2,10,15,16,17,18,19,20,23],
 '6.2':[1,2,10,15,16,17,18,19,20,21,22,23,24,28],
 '6.3':[1,2,10,15,16,17,18,19,20,21,22,23,24,25,26,27]
}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
for n in ['6.1','6.2','6.3']:
    assert reach[n].isdisjoint({'D3','D4','D5','D6','D7','D8','D9','D11','D12','D13','D14'})
for n in ['4.1','5.1','5.2','5.3']:assert reach[n].isdisjoint({f'D{i}' for i in range(15,29)})
assert 'D14' in reach['5.3'] and all('D14' not in reach[n] for n in claims if n!='5.3')
assert 'D28' not in reach['6.3'] and 'D27' not in reach['6.2']
for lid in ['D10','D11','D14','D18','D19','D20']:assert byid[lid]['source_kind']=='assumption'
assert byid['D23']['source_kind']=='theorem_excerpt'
assert 'continuous density' in byid['D11']['statement_original'] and 'continuous density' not in byid['D19']['statement_original']
t41=claims['4.1']['statement_original'];t51=claims['5.1']['statement_original'];t52=claims['5.2']['statement_original'];t53=claims['5.3']['statement_original'];t61=claims['6.1']['statement_original'];t62=claims['6.2']['statement_original'];t63=claims['6.3']['statement_original']
for part in ['(a)','(b)','(c)','(d)']:assert part in t41
for snippet in [r'R_{\omega_\oplus}\geq1/2',r'R_{\gamma(s)}(u)\geq R_{\gamma(t)}(u)',r'P_1=P_2',r'bijective isometric measurable']:assert snippet in t41,snippet
assert r'\mathbb G_P' in t51 and 'zero-mean Gaussian process' in t51
assert r'\sqrt n\sup_{\omega\in\Omega}|\widehat R_\omega-R_\omega|=O_{\mathbb P}(1)' in t52
assert 'non-empty' in t53 and r'\rho_H(\widehat{\mathcal M}_\oplus,\mathcal M_\oplus)=o_{\mathbb P}(1)' in t53
for snippet in [r'L=2\sum_{j=1}^\infty Z_j^2\mathbb E_V(\lambda_j^V)',r'\sqrt{w_x(u)w_x(v)}',r'P=P_1=P_2',r"with $V'\sim P$"]:assert snippet in t61,snippet
assert 'Assumptions 1, 4, 5 and 6' in t61 and 'Assumptions 1, 4, 5 and 6' in t62
assert r'\widehat\Gamma_{m,n}(t)' in t63
assert t63.count(r'$K\to\infty$')==2
assert 'for every $t$ which is a continuity point' in t63
for snippet in [r'\frac n{n+m}-c=O((n+m)^{-1/2})',r'\frac m{n+m}-(1-c)=O((n+m)^{-1/2})',r'\widetilde\beta_{nm}^w\to1']:assert snippet in t63,snippet
assert r'\frac1n\sum_{i=1}^n' in byid['D7']['statement_original']
assert r'\frac1{n-1}' in byid['D8']['statement_original']
assert r'\inf_{d(\omega,\widetilde\omega)>\varepsilon}' in byid['D14']['statement_original']
assert r'F^X_\omega(u)=\mathbb P(d(x,X)\leq u)' in byid['D15']['statement_original']
assert r'\frac1{m-1}' in byid['D16']['statement_original']
assert r'\frac{nm}{n+m}' in byid['D17']['statement_original']
assert r'\sup_{x\in\Omega}\sup_u|\widehat w_x(u)-w_x(u)|=o_{\mathbb P}(1)' in byid['D18']['application_context'][0]['text']
assert r'nm/(n+m)a_{nm}\to\infty' in byid['D22']['statement_original']
assert r'Y_{\Pi_j}=\{V_{\Pi_j(n+1)},V_{\Pi_j(2)},\ldots,V_{\Pi_j(n+m)}\}' in byid['D25']['statement_original']
assert r'\overline q_\alpha=\inf\{t\geq0:' in byid['D26']['statement_original']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=7,interfaces=28,source_members=28,direct_theorem_uses=43,related_theorem_connections=70,unranked_auxiliary_passages=4),counts
assert set(ambient['standard_ambient_resolution'])=={'shared',*claims} and len(ambient['unresolved_source_conventions'])==22
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=32 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=32 for e in ctx['evidence']);fragments.append(ctx['text'])
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
for n in [1,7,8,9,11,12,13,14,15,16,17,18]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=73,main_text_last_pdf_page=33,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent inspection of printed THEOREM headings on main-text pages 1-32 and the clipped top of page 33 finds exactly Theorems 4.1,5.1,5.2,5.3,6.1,6.2,6.3. The embedded Supplementary Material begins on shared page 33 at y=106.52787780761719 and is excluded. Other result types and references to results are not counted.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'Inventory and final census pass validation; the reviewed inventory hash matches and all original claim fields survive unchanged.',
  'The title, three authors, arXiv v4 version stamp, 73-page count and PDF digest match the pinned source. Cached main-text evidence exactly matches fresh extraction with the shared-page cutoff.',
  'The seven complete statements were visually checked on pages 11,12,13,14,17,18, including every branch of Theorems 4.1 and 6.3, the Gaussian process covariance and the precise random-series law.',
  'The random-object model, fixed and random-anchor distance profiles, generalized inverse, strong-negative-type formulations, logistic signed rank, support-restricted median and transport mode were checked on pages 7-9 and 11.',
  'The full-sample profile, leave-one-out rank, finite-sample median, Assumptions 1-3 and both directed Hausdorff distances were checked on pages 12-14. The printed median-separation formula and density support convention remain literal.',
  'All four two-sample empirical profiles, their distinct denominators, both weighted sample averages, harmonic-size scaling and uniform estimated-weight convergence were checked on pages 14-15.',
  'The population discrepancy, oracle critical value, uniform random permutations, empirical permutation CDF and quantile were checked on page 16. The inconsistent second entry in the permuted second group remains preserved.',
  'Assumptions 4-6, the discrepancy-defined alternatives, oracle power, mixture reference law and permutation power were checked on pages 17-18. Nonnegative weights were not silently inserted into Assumption 4.',
  'Independent graph traversal confirms that the transport branch does not inherit the two-sample model; the two-sample branch does not inherit ranks, medians, strong negative type, or the distinct Assumption 2. Assumption 3 reaches only Theorem 5.3.',
  'The null critical value is separately recorded from oracle power, and oracle power remains distinct from permutation power. Theorem 6.3 uses the null and mixture quantiles without importing oracle-power conclusions as premises.',
  'All 43 direct uses and 70 related connections have source-backed explanations. Natural-language names use source keywords; every member has matching source or theorem highlight selectors and its original source kind.',
  'Four auxiliary source passages and twenty-two convention notes record unresolved source wording and distinguish it from mathematical interpretation. No supplement mathematics or proof expansion was used.'
 ]),source_notes=[
  'The audited source is arXiv:2202.06117v4 dated 27 February 2024. Its equivalence to the final journal wording has not been established.',
  'The unrestricted h formulation of strong negative type, median-separation formula versus prose, profile-anchor mismatch, scalar-rank extra argument, permutation split index and estimated-CDF subscript remain source issues rather than corrected quotations.',
  'The source does not fully specify nonnegativity of weights, the covariance eigenvalue operator, global density/support continuity, probability over composite alternatives or all quantile endpoint conventions. These limitations are preserved in the source-convention record.',
  'The census includes every main-text result labeled Theorem. Proposition 1, examples, simulation claims, discussion assertions and all embedded supplement results remain outside that inventory.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Source transcription and statement-prerequisite audit, not proof certification or source repair.','Pinned preprint audited; equality to final journal wording is not established.','All appendix and supplement mathematics were excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
