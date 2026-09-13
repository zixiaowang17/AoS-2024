"""Independently check the change-acceleration inventory, source passages and graph."""
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
data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());review=json.loads((ROOT/'inventory-review.json').read_text())
assert digest(PDF)==paper['pdf_sha256']==prov['pdf_sha256']==digest(WORK/'source.pdf')
assert review['status']=='complete' and review['source_checked'] and digest(ROOT/'theorem-inventory.json')==review['inventory_sha256']
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==53
assert paper['main_text_last_pdf_page']==26 and paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split())
assert paper['title'].lower() in first.lower()
for author in prov['authors']:assert author.lower() in first.lower()
assert '1710.00915v5' in first and '21 Jun 2024' in first
assert paper['source_url']=='https://arxiv.org/pdf/1710.00915v5' and paper['version']=='arXiv:1710.00915v5'
assert '[48]' in pdf[25].get_text(clip=fitz.Rect(0,0,pdf[25].rect.width,137.4))
assert 'APPENDIX A:' in pdf[25].get_text(clip=fitz.Rect(0,137.4,pdf[25].rect.width,152))
labels=[];mentions=[]
for n in range(26):
    page=pdf[n];clip=fitz.Rect(0,0,page.rect.width,137.4) if n==25 else page.rect
    assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text(clip=clip)
    for block in page.get_text('dict',clip=clip)['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();m=re.match(r'^(THEOREM|Theorem)\s+(\d+\.\d+)',text)
            if m:(labels if m[1]=='THEOREM' else mentions).append((n+1,m[2]))
assert labels==[(8,'3.1'),(12,'5.1'),(17,'6.1')] and mentions==[(16,'5.1')]
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==3
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members}
claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
extraction=json.loads((ROOT/'interface-extraction.json').read_text())
assert {m['local_id']:m for x in extraction['interfaces'] for m in x['members']}==byid
reach={}
for n,c in claims.items():
    seen=set();stack=c['depends_on'][:]
    while stack:
        lid=stack.pop()
        if lid in seen:continue
        seen.add(lid);stack.extend(byid[lid]['depends_on'])
    reach[n]=seen
# Source-derived expected sets kept independent of the finalization script.
expected={'3.1':{1,2,3,4,5,6,7,9,10,11,12,13,14},'5.1':{1,2,3,4,9,15,16,17,18,19,20,21,22,23,24,25,26,27},'6.1':{1,2,3,4,7,8,15,20,21,26,28,29,30,31}}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
expected_direct={'3.1':{5,14,10,9,6},'5.1':{3,4,21,23,15,18,19,24,22,25,26,27},'6.1':{3,4,21,29,30,31,8,28}}
assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in expected_direct.items()}
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
assert reach['3.1'].isdisjoint({'D8','D18','D21','D23','D28'})
assert reach['5.1'].isdisjoint({'D5','D6','D10','D14','D28','D29','D30','D31'})
assert reach['6.1'].isdisjoint({'D5','D6','D9','D10','D11','D12','D13','D14','D17','D18','D19','D22','D23','D24','D25','D27'})
assert byid['D21']['source_kind']=='assumption' and byid['D23']['source_kind']=='assumption'
assert all(byid[lid]['source_kind']=='condition' for lid in ['D29','D30','D31'])
assert byid['D16']['naming_context'][0]['evidence'][0]['page']==9
assert byid['D31']['naming_context'][0]['evidence'][0]['page']==18
t={n:c['statement_original'] for n,c in claims.items()};b={lid:m['statement_original'] for lid,m in byid.items()};a={x['local_id']:x['statement_original'] for x in ambient['auxiliary_source_passages']}
assert [e['page'] for e in claims['5.1']['evidence']]==[12,13]
assert r'b_c(\mathbb S_t)' in t['3.1'] and r'\kappa=0' in t['3.1']
assert 'defined in (9)' in t['3.1'] and 'optimization problem (6)' in t['3.1']
assert r'b_2\ge b_1>1' in t['5.1'] and r'd>1' in t['5.1']
assert r'\frac{(1+\epsilon)^2}{1-\eta(b_1,d)}\mathcal R' in t['5.1']
assert r'\eta(b_1,d)\equiv(b_1+d)/(d(1+b_1))' in t['5.1']
assert r'\frac1{\mathsf D(\Xi_1)}-\frac1{\mathsf D(\Xi_2)}' in t['5.1']
assert r'+3\ell_1+2\ell_2' in t['5.1'] and r'\frac{V^J(\Xi_2)}{(J(\Xi_2))^2}' in t['5.1']
assert r'\frac{|\log(\zeta(\Xi_1))|}{\mathsf D(\Xi_1)}' in t['5.1']
assert 'Subsection 4.2' in t['5.1'] and r'\tag{21}' in t['5.1']
assert r'\sum_{t=t_0+1}^\infty\prod_{s=1}^{t_0}' in t['5.1'] and r'\prod_{s=t_0+1}^t' in t['5.1']
assert all(c in t['6.1'] for c in ['condition (14)','conditions (27) and (28)','condition (29)'])
assert r'\inf_{(\mathcal X,T)\in\mathcal C_\alpha}\mathsf E[T]' in t['6.1'] and r'\lambda^*+\frac{|\log(\alpha)|}{\mathsf D^*}' in t['6.1']
assert r'\Theta_{\mathcal X}' in b['D4'] and r'\Theta^{\mathcal X}' not in b['D4']
assert 'whereas $X_1$ is deterministic' in b['D2']
assert r'\{L_s\}_{0\le s\le t-1}' in b['D3']
assert r'\mathbb S_t=\Phi(X_t,\mathbb S_{t-1})' in b['D5']
assert r'\Delta_t=1\{t>T\}' in b['D11'] and r'1\{T=t\}' in b['D11']
assert 'Equation (B.1) in Appendix B.1' in b['D11']
assert r'1/(1+\Gamma_t)\le J_c^*' in b['D14'] and r'\operatorname*{arg\,min}_{k\in[K]}' in b['D14']
assert r'\inf\{s\ge0:' in b['D17'] and r'\inf\left\{s\ge1:' in b['D17']
assert r'\sigma(S_{2m-1};b_2)\le\tau(S_{2m-1};d)' in b['D18']
assert r'\widetilde T\equiv S_{2N}' in b['D18'] and '\\mathbb S' not in b['D18']
assert r'\min\{t_0,S_1\}' in b['D19'] and r'\Xi_1(t-t_0)' in b['D19']
assert r'0<V_x^I' in b['D21'] and r'0<V_x^J' not in b['D21']
assert r'\sup_{t\ge0,z\in[K]^t,j\in[\ell]}' in b['D23']
assert r'\mathsf D(\Xi)\equiv I(\Xi)+d(\Xi)' in b['D24']
assert r'(1-\pi_0)' in b['D25'] and 'pi_0' not in b['D26']
assert r'\max_{1\le s\le2|\Xi|}' in b['D27']
assert r'do not depend on $\alpha$' in b['D28'] and r'\liminf(x/y)\ge1' in b['D28']
assert 'there exists a block' in b['D30'] and r'\inf_{\mathcal X}\mathsf E[\Theta_{\mathcal X}]' in b['D30']
assert r'\mathsf D^*=O(1)' in b['D31'] and r'\epsilon>0' in b['D31']
assert r'\lfloor(1-\epsilon)|\log(\alpha)|/\mathsf D^*\rfloor' in b['D31']
assert r'\omega(x)\equiv|\log(1-x)|' in a['A3']
# Verify the source font distinction that ordinary extracted text loses.
def has_span(n,font,fragment):
    return any(s['font']==font and fragment in s['text'] for block in pdf[n-1].get_text('dict')['blocks'] for line in block.get('lines',[]) for s in line['spans'])
assert has_span(8,'MSBM10','S') and has_span(10,'CMMI10','S')
assert has_span(12,'CMSS10','D') and has_span(12,'CMSS10','E') and has_span(13,'CMSY10','R')
counts=dict(theorems=3,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_source_passages']))
assert counts==dict(theorems=3,interfaces=31,source_members=31,direct_theorem_uses=25,related_theorem_connections=45,unranked_auxiliary_passages=6),counts
assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==33
for item in data['claims']+members+ambient['auxiliary_source_passages']:
    assert all(1<=e['page']<=26 and (e['page']<26 or e.get('before_main_text_end') is True) for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[]):
        assert all(1<=e['page']<26 for e in ctx['evidence']);fragments.append(ctx['text'])
    for text in fragments:
        assert not re.search(r'[\u4e00-\u9fff]',text)
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,('unbalanced',item)
            assert depth==0,('unbalanced',item)
for x in data['interfaces']:
    assert x['related_theorems'] and set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
    assert '$' not in x['name']
    for m in x['members']:
        own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors) and all(s in linked for s in selectors)
    for k in x['source_keywords']:
        m=byid[k['local_id']];texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])]
        assert any(k['source_text'] in text for text in texts)
for n in [4,5,6,7,8,9,10,11,12,13,16,17,18]:shutil.copyfile(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
write('source-passages.json',dict(paper_id=PID,members=members))
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-prerequisites.json','inventory-review.json','interface-extraction.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
checks=[
 'Source title, both authors, version, date, 53-page count and PDF hash checked. Fresh source extraction matches every archived page, with page 26 clipped above the appendix boundary.',
 'Independent uppercase-heading enumeration finds three Theorems and excludes the ordinary-case citation. Theorem 5.1 spans pages 12–13; the others are complete on pages 8 and 17.',
 'Original inventory fields remain unchanged at census handoff. Theorem 3.1 preserves the Markovian and auxiliary-objective requirements plus the memoryless special case.',
 'Theorem 5.1 retains every term of U and R, the exact threshold ranges, and the modified-assignment expected-time formula (21). Theorem 6.1 retains all four numbered conditions and the admissible-class infimum.',
 'The latent-state model, observed filtration, predictable deterministic policies, response law, general hazard and Markov sufficient-state update are checked against pages 4–6.',
 'The auxiliary cost, delayed termination flag, state/action kernel, stage cost, value function, Bellman operators and optimal procedure are source-checked. The appendix-only phi formula remains explicitly unresolved.',
 'The block convention, posterior/likelihood hitting times, full cyclic assignment, stage recursion, tie behavior and initial-prefix modification are checked against pages 9–11.',
 'The directional information numbers, centered variances, uniform stability quantifiers, block averages, initial and worst-history expected times, and two-block hazard bound are checked against pages 11–13.',
 'The alpha-indexed family, uniform upper hazard bound, existence condition on residual duration and uniform information-window assumption are checked against pages 16–18. Printed epsilon and support/finite-value ambiguities are preserved separately.',
 'Independent graph traversal verifies 25 direct uses and 45 related connections. The universal lower bound does not inherit the proposed cyclic procedure, Markovian assumptions or condition (16).',
 'Every interface has original natural-language terminology, faithful source kind, meaningful selectors and source-specific path explanations. Blackboard-bold state S, plain endpoint S and sans-serif information symbols are independently font-checked.'
]
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=53,main_text_last_pdf_page=26,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent uppercase THEOREM heading enumeration over pages 1–26, with page 26 clipped above y=137.4. Full statement images and the shared-page appendix boundary were checked.',printed_label_check=labels,excluded_result_types=['Lemma','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=checks),source_notes=ambient['source_issues'],unresolved_source_references=ambient['excluded_references'],ambient_resolution=ambient['statement_resolution'],artifacts=artifacts,evidence=evidence,review_limits=['Source transcription and statement-dependency audit, not proof certification or repair of ambiguous source formulas.','Pinned preprint inspected; final journal typesetting equivalence is not asserted.','The predictive-density formula located only in Appendix B.1 remains unresolved under the main-text-only scope.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
