"""Independently audit the pinned source, four statements and local dependency paths."""
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
assert len(pdf)==76 and paper['main_text_last_pdf_page']==19
assert paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split())
assert '2112.10151v2' in first and '2 Apr 2024' in first
assert paper['title'].casefold() in first.casefold()
for a in ['JINYUAN CHANG','QIAO HU','ERIC D. KOLACZYK','QIWEI','YAO','FENGTING YI']:assert a in first,a
assert paper['source_url']=='https://arxiv.org/pdf/2112.10151v2'
assert [1,'Appendix',19] in pdf.get_toc()
cutoff=prov['main_text_shared_page_cutoff_y'];assert cutoff==313.6376953125
# Only the main-text portion and the previously identified heading itself are inspected.
heading=pdf[18].get_text(clip=fitz.Rect(0,cutoff,pdf[18].rect.width,324.7))
assert heading.strip()=='APPENDIX',heading
labels=[];source_text={}
for n in range(19):
    clip=fitz.Rect(0,0,pdf[n].rect.width,cutoff) if n==18 else pdf[n].rect
    source_text[n+1]=pdf[n].get_text(clip=clip)
    for block in pdf[n].get_text('dict',clip=clip)['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip()
            match=re.match(r'THEOREM (\d+)\.',text)
            if match:labels.append((n+1,match.group(1)))
assert labels==[(9,'1'),(12,'2'),(13,'3'),(18,'4')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==4
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
members=[m for x in data['interfaces'] for m in x['members']]
byid={m['local_id']:m for m in members}
claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
# Independent local DFS, before any canonical keyword grouping.
reach={}
for n,c in claims.items():
    seen=set();stack=list(c['depends_on'])
    while stack:
        lid=stack.pop()
        if lid in seen:continue
        seen.add(lid);stack.extend(byid[lid]['depends_on'])
    reach[n]=seen
expected={
 '1':{f'D{i}' for i in range(1,11)},
 '2':{f'D{i}' for i in range(1,17)}-{'D8'},
 '3':{f'D{i}' for i in [1,2,3,4,5,6,7,8,12,13,15,16]},
 '4':{f'D{i}' for i in [1,2,3,4,6,7,8,17,18,19]}
}
assert reach==expected,reach
assert set(claims['4']['depends_on'])=={'D4','D17','D18','D19'}
assert 'D14' not in reach['3'] # No bootstrap-estimator dependency in Theorem 3.
assert 'D8' not in reach['2'] # Original theta-hat is not the center in Theorem 2.
assert reach['4'].isdisjoint({'D5','D9','D10','D11','D12','D13','D14','D15','D16'})
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    actual={r['claim_id'].split('/T')[-1] for r in x['related_theorems']}
    assert actual=={n for n in claims if reach[n]&lids},(x['name'],actual)
    direct={u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}
    assert direct=={n for n,c in claims.items() if set(c['depends_on'])&lids}
    for m in x['members']:
        if len(x['members'])>1:assert m['relation']=='distinct'
    for k in x['source_keywords']:
        m=byid[k['local_id']];texts=[m['statement_original']]+[z['text'] for z in m.get('naming_context',[])]
        assert any(k['source_text'] in t for t in texts)
assert r'\in\mathcal I\in\mathcal M(\gamma;C_1)' in claims['1']['statement_original']
assert [e['page'] for e in claims['1']['evidence']]==[9,10]
assert r'$\gamma\asymp p^{-1/4}$' in claims['1']['statement_original']
assert claims['1']['statement_original'].count('in distribution.')==3
assert r'\widehat\theta_{\ell_1}^\dagger-\theta_{\ell_1}' in claims['2']['statement_original']
assert r'\nu_\ell^\dagger\nu_\ell^{-1}-1' in claims['2']['statement_original']
assert r'$\delta\in(0,c]$' in claims['2']['statement_original']
assert r'0<\delta\ll(p\log p)^{-1}' in claims['3']['statement_original']
assert r'p^{-1/3}\log^{1/2}p' in claims['3']['statement_original']
assert r'(\widehat{\boldsymbol\theta}-\boldsymbol\theta)' in claims['3']['statement_original']
assert r'\boldsymbol\xi\sim\mathcal N(\mathbf0,\mathbf I_p)' in claims['3']['statement_original']
t4=claims['4']['statement_original']
for phrase in [r'\exp(-|\xi^+|\vee\max_{\ell\in S}|\check\theta_\ell^+|)',r'0\leq\omega_2\leq\omega_1<1/2',r'\gamma p^{3/2-\omega_1-\omega_2}',r'\gamma^3p^{1-2\omega_1}',r'\chi_p^{-8}',r'p^{-1/3+2\omega_1/3}\log^{1/6}p',r'=\max_{\ell\in[p]}|\widehat{\check\theta}_\ell-\check\theta_\ell|']:assert phrase in t4,phrase
assert t4.count('\\widetilde O_p')==3
assert r'\{x-\delta-\alpha(1-2\delta)\}^\tau' in byid['D13']['statement_original']
assert r'\frac1{2N}' in byid['D10']['statement_original'] and r'\frac1{2N}' in byid['D16']['statement_original']
assert r'\min_{\ell\in[p]}\check\theta_\ell=0' in byid['D17']['statement_original']
assert r'\max_{\ell\in S}|\check\theta_\ell^+|=o(\log p)' in byid['D17']['statement_original']
assert r'O_p(p^\epsilon c_p)' in byid['D19']['statement_original']
assert 'some sufficiently small fixed constant' in byid['D19']['statement_original']
assert 'relative sizes between' in byid['D10']['naming_context'][0]['text']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=4,interfaces=12,source_members=19,direct_theorem_uses=19,related_theorem_connections=33,unranked_auxiliary_passages=10),counts
assert set(ambient['standard_ambient_resolution'])=={'shared','1','2','3','4'}
assert len(ambient['unresolved_source_conventions'])==18
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=18 or (e['page']==19 and e.get('before_main_text_end')) for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=18 or (e['page']==19 and e.get('before_main_text_end')) for e in ctx['evidence'])
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
for n in [1,3,4,5,6,7,8,9,10,11,12,13,17,18]:
    shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=76,main_text_last_pdf_page=19,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent enumeration of complete printed THEOREM headings in pages 1-18 and the clipped main-text portion of page 19 finds exactly Theorems 1-4. Theorem 1 continues on page 10. The Appendix begins on the shared page 19 at y=313.6376953125; its heading is used only to establish the boundary. No appendix or embedded supplement body was used.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'Both the source-reviewed inventory and finalized census pass validation. The inventory hash matches its independent review, and every original claim field is preserved unchanged.',
  'Title, five authors, arXiv v2 stamp dated 2 April 2024, versioned source URL, page count and PDF digest were checked. The heading-only crop verifies the shared-page Appendix cutoff.',
  'All four complete Theorem statements were checked visually on pages 9,10,12,13,18: three phase branches, both bootstrap conclusions, the p-dimensional lower-orthant approximation and every sparse error term.',
  'Simple-network conventions, independent-edge beta-model likelihood, the original jittering law, M(gamma;C_1), Condition 1, corrected edge functions and triangle moments/estimator were checked on pages 3-8.',
  'The original lambda coefficients and the two variance components were checked on page 9, including ordered-pair sums, the factor 1/(2N), and N=(p-1)(p-2). Their combined variance was checked on pages 10-11.',
  'The bootstrap sample law, doubly corrected edge functions, sample estimator, population moments, coefficients and combined population variance were checked on pages 11-12. The population center and variance are not replaced by conditional bootstrap or empirical versions.',
  'Independent local-graph traversal confirms that Theorem 2 uses the bootstrap estimator but not original theta-hat, whereas Theorem 3 uses original theta-hat and population nu-dagger but not the bootstrap estimator itself.',
  'The sparse beta-model, support, nonnegative effects, logarithmic residual reparametrization and linear sparse estimates were checked on pages 17-18. Theorem 4 has no dense Condition 1 or bootstrap dependency.',
  'Twelve source-keyword groups retain nineteen separate original passages. Component passages are explicitly distinct rather than equivalent variants. Internal edges survive grouping; group reach was compared with independent local traversal.',
  'Ten auxiliary passages resolve notation and population-law conventions; eighteen source notes retain the malformed membership, chi_p sign scope, error equality chain, log-domain omissions and other source ambiguities without repairing original statements.',
  'All nineteen direct group/theorem uses and thirty-three related connections have matching paths, source explanations and selectors. Every selector matches its original passage/label or a related same-paper theorem.'
 ]),
 source_notes=[
  'The audited source is the pinned arXiv v2 preprint; equality to final journal wording has not been established.',
  'Theorem 1’s extra script-I membership and Theorem 4’s unparenthesized chi_p expression/equality chain remain exactly as printed. Source fidelity is not a certification of those statements as mathematically well posed.',
  'Appendix and supplement references remain references. Proof-only expansions, the later adaptive-delta algorithm, empirical bootstrap variance estimation and applied confidence regions do not become theorem statement requirements.',
  'Fixed s in Theorems 1/2, dimension p in Theorem 3 and growing sparse-support size s in Theorem 4 remain distinct.',
  'Natural-language group titles use source keywords. Shared component grouping does not rewrite any original definition or claim mathematical equivalence between moments, estimators and variance quantities.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Main-text source transcription and statement-dependency review; no proof certification or silent source repairs.','All appendix and supplement mathematics were excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
