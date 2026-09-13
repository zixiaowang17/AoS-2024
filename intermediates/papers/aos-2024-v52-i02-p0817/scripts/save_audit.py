"""Independently validate the four main-text statements and their local prerequisites."""
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
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==21
assert paper['main_text_last_pdf_page']==16 and not paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split());assert paper['title'].upper() in first
for author in ['Lasse Fischer','Marta Bofill Roig','Werner Brannath']:assert author in first
assert '2211.11400v3' in first and '21 Dec 2023' in first and 'December 22, 2023' in first
assert paper['source_url']=='https://arxiv.org/pdf/2211.11400v3' and paper['version']=='arXiv:2211.11400v3'
assert 'FDR' in pdf[15].get_text() and 'FDP control' in pdf[15].get_text()
heading=pdf[16].get_text(clip=fitz.Rect(0,0,pdf[16].rect.width,86));assert heading.splitlines()[-1]=='Appendix'
labels=[];plain_references=[]
for n in range(16):
    page=pdf[n];assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf-8')==page.get_text(),(n+1,'cached evidence differs')
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();match=re.match(r'Theorem (\d+(?:\.\d+)*)(?=[.\s(])',text)
            if match:
                if line['spans'][0]['font']=='NimbusRomNo9L-Medi':labels.append((n+1,match.group(1)))
                else:plain_references.append((n+1,text))
assert labels==[(3,'3.2'),(4,'3.5'),(6,'3.9'),(8,'4.2')],labels
assert len(plain_references)==1 and plain_references[0][0]==5
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==4
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
expected={'3.2':[1,2,3,4,5,6,7,8],'3.5':[1,2,3,4,5,6,7,8],'3.9':[1,2,4,5,6,7,8,9],'4.2':[1,2,4,6,8,9,10,11,12,13]}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
for n in ['3.2','3.5','3.9']:assert reach[n].isdisjoint({'D10','D11','D12','D13'})
assert 'D9' not in reach['3.2'] and 'D9' not in reach['3.5']
assert byid['D8']['source_kind']=='theorem_excerpt'
for lid in ['D2','D7','D13']:assert byid[lid]['source_kind']=='definition' and byid[lid]['source_heading'].startswith('Definition ')
t32=claims['3.2']['statement_original'];t35=claims['3.5']['statement_original'];t39=claims['3.9']['statement_original'];t42=claims['4.2']['statement_original']
assert 'arbitrary family' in t32 and 'In addition, if each' in t32
assert r'd_i^\phi=\min\{\phi_I:I\subseteq\mathbb N\text{ with }i\in I\}' in t32
assert r'\phi_I=\max\{d_i:i\in I\}' in t35 and r'\boldsymbol d^\phi=\boldsymbol d' in t35
assert r'I_i=\{j\in\mathbb N:j<i,\phi_{I_j}=0\}\cup\{i\}' in t39
assert r'I_i=\{j\in\mathbb N:j<i,p_j>\alpha_j^{I_j}\}\cup\{i\}' in t42
assert r'd_i=\mathbb 1\{p_i\leq\alpha_i^{I_i}\}' in t42
assert t39.count('\n1.')==1 and '\n2.' in t39 and '\n3.' not in t39
assert all('\n'+str(i)+'.' in t42 for i in [1,2,3])
assert 'defined by (3)' in t42 and 'consonance property' in t42
assert r'\mathbb F=(\mathcal F_i)' in byid['D1']['statement_original']
assert 'almost surely for all' in byid['D1']['statement_original']
assert r'\mathcal F_\infty=\mathcal A' in byid['D5']['statement_original']
assert r'\phi_\varnothing=0' in byid['D4']['application_context'][0]['text']
assert r'\alpha_j^I=\alpha_j^K' in byid['D13']['statement_original']
assert r'\phi_I=1\text{ implies }\phi_K=1' in byid['D7']['statement_original']
assert r'\forall J\subseteq I\text{ with }i\in J' in byid['D9']['statement_original']
assert r'\alpha_i\in[0,1)' in byid['D11']['statement_original']
assert r'\mathcal F_{i-1}' not in byid['D11']['statement_original']
assert r'\mathbb P(p_i\leq x)\leq x' in byid['D10']['statement_original']
assert r'\phi_I=\mathbb 1\{\exists i\in I:p_i\leq\alpha_i^I\}' in byid['D12']['statement_original']
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=4,interfaces=13,source_members=13,direct_theorem_uses=27,related_theorem_connections=34,unranked_auxiliary_passages=6),counts
assert set(ambient['standard_ambient_resolution'])=={'shared',*claims} and len(ambient['unresolved_source_conventions'])==18
math_fragments=0
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=16 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=16 for e in ctx['evidence']);fragments.append(ctx['text'])
    for text in fragments:
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
for n in [1,2,3,4,6,7,8,16]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
shutil.copy2(WORK/'appendix-heading-only.png',ROOT/'evidence/appendix-heading-only.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=21,main_text_last_pdf_page=16,provenance_path='evidence/source-provenance.json'),
 enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent inspection of bold NimbusRomNo9L-Medi headings on pages 1-16 finds exactly Theorems 3.2,3.5,3.9,4.2. The title of Theorem 3.2 is part of its heading; decimal numbering is preserved. A regular-font reference on page 5 is excluded. Main discussion ends on page 16 before the Appendix heading on page 17.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
 counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
  'The title, three authors, arXiv v3 identifier, both printed dates, 21-page count and pinned PDF hash match the source. All cached main-text pages match fresh byte-preserving text extraction.',
  'Both inventory and final census pass validation; the inventory review hash matches, and all original claim fields survive unchanged.',
  'All four complete theorem statements were visually checked on pages 3,4,6,8, preserving the arbitrary-family and additional online clauses, maximum representation and equality, and both recursive shortcut constructions.',
  'The abstract experiment, fixed hypothesis subsets, blackboard-F filtration and almost-sure convention were checked on pages 2-3. Definition 2.1 and the strong all-time FWER definition remain separate concepts.',
  'Intersection hypotheses, binary tests, the empty-test convention, online measurability and level-alpha validity were checked on page 3. These separate requirements are not conflated.',
  'Definition 3.1, the inline closure operation, and consonance (2) were checked on pages 3-4. Future-only extensions and subset-restricted consonance witnesses are preserved.',
  'The p-value setting, current-information thresholds, online sub-adjustments, equation (3) and Definition 4.1 were checked on page 7. Threshold equality under future extensions is kept distinct from rejection persistence.',
  'Independent graph traversal confirms that the first three Theorems do not acquire p-value/threshold assumptions. Consonance is not imposed on Theorems 3.2 or 3.5. Theorem 3.5 does not acquire an admissibility hypothesis from its section title.',
  'All 27 direct uses and 34 related connections have source-backed explanations and matching selectors. Source titles, numbered definitions and theorem excerpts retain their original kinds.',
  'Six auxiliary passages and eighteen source-convention notes preserve weak-versus-strong control, finite-prefix reduction, conditional-validity examples and the two predictability notions. Uncountable-minimum measurability and simultaneous-version issues are recorded explicitly.',
  'The recursive index sets and rejection inequalities were checked exactly, including strict p_j>alpha_j^{I_j} versus non-strict p_i<=alpha_i^{I_i}. No particular spending or ADDIS rule is imported into the general decision-equivalence theorem.',
  'No appendix mathematics is used; proof-only propositions, admissibility results and later concrete procedures are not counted as additional Theorems or generic statement prerequisites.'
 ]),source_notes=[
  'The audited source is arXiv:2211.11400v3 with margin stamp 21 December 2023 and title-page date 22 December 2023. Equality to the final journal wording has not been established.',
  'The arbitrary-family minimum in Theorem 3.2 is over an uncountable index family. Its measurability is not automatic from the stated individual-test assumptions. The predictable finite-prefix case is kept separate.',
  'Almost-sure comparisons across uncountably many subsets need a simultaneous-version interpretation for the closure reduction; the source does not state that convention explicitly.',
  'The two predictability definitions, adaptedness, marginal p-value validity and intersection-test level control are different requirements. No independence or past-only threshold condition is silently added.'
 ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
 review_limits=['Source transcription and statement-prerequisite audit, not proof certification or source repair.','Pinned preprint audited; equality to final journal wording is not established.','All appendix mathematics were excluded.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
