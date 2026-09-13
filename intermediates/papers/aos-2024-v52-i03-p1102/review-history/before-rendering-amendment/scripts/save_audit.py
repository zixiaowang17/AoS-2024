"""Independent source and dependency review for the MARS census."""
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
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==108
assert paper['main_text_last_pdf_page']==25 and paper['main_text_boundary']['shared_page_with_appendix'] is False
first=' '.join(pdf[0].get_text().split());assert paper['title'].upper() in first
assert all(name.upper() in first for name in prov['authors'])
assert '2111.11694v5' in first and '13 Oct 2024' in first
assert paper['source_url']=='https://arxiv.org/pdf/2111.11694v5' and paper['version']=='arXiv:2111.11694v5'
assert 'YEH' in pdf[24].get_text()
assert 'APPENDIX A:' in pdf[25].get_text(clip=fitz.Rect(0,165,pdf[25].rect.width,181))
labels=[];mentions=[]
for n in range(25):
    page=pdf[n];assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text()
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();m=re.match(r'^(THEOREM|Theorem)\s+(\d+\.\d+)',text)
            if m:(labels if m[1]=='THEOREM' else mentions).append((n+1,m[2]))
assert labels==[(9,'3.1'),(10,'3.2'),(11,'3.4'),(12,'3.5'),(12,'3.6'),(12,'3.8'),(13,'3.9')]
assert mentions==[(10,'3.2'),(11,'3.1'),(11,'3.4'),(12,'3.6')]
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert len(inv['claims'])==len(data['claims'])==7
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(original['claim_id'],key)
members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members}
claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
extraction=json.loads((ROOT/'interface-extraction.json').read_text());assert extraction['status']=='extracted'
assert {m['local_id']:m for x in extraction['interfaces'] for m in x['members']}==byid
reach={}
for n,c in claims.items():
    seen=set();stack=c['depends_on'][:]
    while stack:
        lid=stack.pop()
        if lid in seen:continue
        seen.add(lid);stack.extend(byid[lid]['depends_on'])
    reach[n]=seen
# Source-derived mathematical expectations, independent of the finalizer's edge map.
expected={
 '3.1':{1,2,3,4,5,6,12,13,14},'3.2':{1,4,15,22},
 '3.4':{1,2,3,4,5,7,8,9,10,11,12,13,14},
 '3.5':{1,2,3,4,5,6,16,17,18},'3.6':{1,4,15,21},
 '3.8':{1,2,3,4,5,7,8,9,10,11,16,17,18},
 '3.9':{1,2,3,4,5,16,17,18,19,20}}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
direct={'3.1':{3,5,12,13,6,14},'3.2':{15,22},'3.4':{3,5,12,13,11,14,8},'3.5':{3,5,6,16,17,18},'3.6':{15,21},'3.8':{3,5,11,8,16,17,18},'3.9':{19,20}}
assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
for n in ['3.2','3.6']:assert reach[n].isdisjoint({f'D{i}' for i in [3,5,6,7,8,9,10,11,12,13,14,16,17,18,19,20]})
for n in ['3.1','3.4','3.5','3.8','3.9']:assert reach[n].isdisjoint({'D15','D21','D22'})
assert reach['3.9'].isdisjoint({'D6','D7','D8','D9','D10','D11','D12','D13','D14'})
assert 'D6' not in reach['3.4'] and 'D6' not in reach['3.8']
assert 'D20' not in reach['3.5'] and 'D20' not in reach['3.8']
t={n:c['statement_original'] for n,c in claims.items()};b={lid:m['statement_original'] for lid,m in byid.items()};a={x['local_id']:x['statement_original'] for x in ambient['auxiliary_source_passages']}
assert all(len(c['evidence'])==1 for c in claims.values())
for n in ['3.1','3.4']:
    assert r'\frac{3(2s-1)}5' in t[n] and r'C_{\rho,d}\frac{\sigma^2}n[\log n]^2' in t[n]
    assert 'lattice design (15)' in t[n] and r'\sigma^2V^{\frac12}' in t[n]
assert r'\widehat f_{n,V}^{d,s}' in t['3.1'] and r'\widetilde f_{n,V}^{d,s}' in t['3.4']
assert r'\frac{8V^2}{N^2}' in t['3.4'] and r'N=\min_k N_k' in t['3.4']
assert r'\frac{3(2m-1)}4' in t['3.2'] and 'can be omitted when $m=1$' in t['3.2']
assert r'0<\epsilon<\epsilon_m' in t['3.2']
assert r'\left|\log\frac4\epsilon\right|^{2(m-1)}' in t['3.6'] and 'for every $\epsilon>0$' in t['3.6']
for n in ['3.5','3.8']:assert r'=O_p\bigl(n^{-\frac45}(\log n)^{\frac{8(s-1)}5}\bigr)' in t[n]
assert r'\Omega(n^{4/15})' in t['3.8'] and r'c_{B,d,V}' in t['3.8'] and 'possibly depending' in t['3.8']
assert r'\mathfrak M_{n,V}^{d,s}' in t['3.9'] and r'\frac{4(s-1)}5' in t['3.9']
assert r'\log\left(\frac{Vn^{\frac12}}\sigma\right)' in t['3.9'] and r'n\ge c_{B,s}\cdot(\sigma^2/V^2)' in t['3.9']
assert r'\cdot_+:=\max\{\cdot,0\}' in b['D1']
assert r'\sum_{j=1}^d\mathbf1\{\alpha_j=1\}' in b['D2']
assert 'finite (Borel) signed measure' in b['D3'] and r'[0,1)^{|\alpha|}' in b['D3']
assert 'countable number of disjoint measurable subsets' in b['D4']
assert r'[0,1)^{|\alpha|}\setminus\{\mathbf0\}' in b['D5'] and 'leave unpenalized' in b['D5']
assert r'\operatorname*{arg\,min}_f' in b['D6'] and r'V>0' in b['D6']
assert r'l\ne\mathbf0' in b['D7'] and r'y-a_0\mathbf1-M\gamma' in b['D7']
assert r'\widetilde{\mathcal U}_k' in b['D8'] and 'pre-selected positive integers' in b['D8']
assert 'same form as (13) but with different $M$ and $J$' in b['D9']
assert r'\frac{l_k}{N_k}' in b['D9'] and r'[0:(N_k-1)]' in b['D9']
assert r'\tag{14}' in b['D10'] and 'through the equation (14) as before' in b['D11']
assert r'0=u_0^{(k)}' in b['D12'] and r'u_{n_k-1}^{(k)}\le1' in b['D12'] and r'\frac\rho{n_k}' in b['D12']
assert r'e^{\frac{\sigma^2\lambda^2}2}' in b['D13'] and 'independent sub-Gaussian errors' in b['D13']
assert 'expectation is taken over $y_1,\ldots,y_n$' in b['D14']
assert r'|\nu|([0,1]^m)\le1' in b['D15'] and r'\setminus\{\mathbf0\}' not in b['D15']
assert r'B\ge1' in b['D16'] and r'\|p_0\|_\infty\le B' in b['D16']
assert r'\int_0^\infty\bigl(\mathbb P(|\xi_i|>t)\bigr)^{\frac15}' in b['D17']
assert 'i.i.d. errors independent of' in b['D17']
assert r'p_0(x)\,dx' in b['D18'] and 'expectation' not in b['D18']
assert r'\inf_{\widehat f_n}' in b['D19'] and 'all estimators' in b['D19']
assert 'bounded below' in b['D20'] and r'\|p_0\|_\infty\ge b' in b['D20']
assert [e['page'] for e in byid['D20']['evidence']]==[12,13]
assert 'bracketing number' in b['D21'] and 'metric entropy' in b['D22']
assert r'u_{n_k}^{(k)}=1' in a['A5'] and r'[0:(n_k-1)]' in a['A6']
assert 'multiple solutions' in a['A7']
def has_span(n,font,fragment):
    return any(s['font']==font and fragment in s['text'] for block in pdf[n-1].get_text('dict')['blocks'] for line in block.get('lines',[]) for s in line['spans'])
assert has_span(13,'EUFM10','M') and has_span(9,'CMSY10','R') and has_span(10,'CMSY10','D')
assert has_span(3,'CMBX10','0') and has_span(2,'CMBX10','1') and has_span(8,'CMSY10','U')
counts=dict(theorems=7,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_source_passages']))
assert counts==dict(theorems=7,interfaces=22,source_members=22,direct_theorem_uses=32,related_theorem_connections=62,unranked_auxiliary_passages=7),counts
assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==25
for item in data['claims']+members+ambient['auxiliary_source_passages']:
    assert all(1<=e['page']<=25 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[]):
        assert all(1<=e['page']<=25 for e in ctx['evidence']);fragments.append(ctx['text'])
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
for n in [1,2,3,4,6,7,8,9,10,11,12,13,25]:shutil.copyfile(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
write('source-passages.json',dict(paper_id=PID,members=members))
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-prerequisites.json','inventory-review.json','interface-extraction.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
checks=[
 'Pinned title, all three authors, version/date, page count and PDF hashes verified. All 25 archived main-text pages match fresh extraction byte for byte; the reference endpoint and following appendix heading were visually checked.',
 'Independent uppercase-heading enumeration confirms all seven main-text Theorems and excludes four ordinary-case mentions. Complete original bodies on pages 9–13 are preserved unchanged at handoff.',
 'Both fixed-design risk bounds retain their logarithmic powers, variance remainder and the approximate 8V^2/N^2 term. The two entropy results retain distinct epsilon ranges and the m=1 clause.',
 'Random-design rates remain statements in probability for squared population error. The approximate-grid exponent 4/15 and all dependencies of its constant are preserved. The minimax bound retains fraktur M and its original logarithm/sample threshold.',
 'The original signed-measure class, all-zero atom exclusion, exact optimization, coefficient objective and fixed-grid approximation/reconstruction are checked against pages 1–9. Observed grids are kept separate from approximate grids.',
 'The lattice and sub-Gaussian fixed-design model are distinct from iid bounded-density random design with L^{5,1} errors. The Gaussian/lower-density minimax restriction and its prose/formula mismatch are retained.',
 'D_m has a closed-cube total-variation bound including zero, distinct from the MARS complexity ball. Metric and bracketing numbers use the named source quantities with explicitly noted conventional definitions.',
 'Independent mathematical graph expectations verify 32 direct uses and 62 related connections. Entropy statements do not inherit sampling assumptions; risk statements do not inherit proof entropy. The minimax infimum does not depend on either proposed estimator.',
 'The approximate construction depends on the original feasible class and complexity plus the reused coefficient formula, not a chosen exact-estimator solution. Every original source kind, keyword, selector and path explanation is checked.',
 'All evidence remains in main text and all original passages have balanced math and English prose. PDF fonts separately confirm fraktur minimax M, script classes/risks/grids, and bold zero/one notation. Appendix definitions and proofs are not used.'
]
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=108,main_text_last_pdf_page=25,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent uppercase THEOREM-heading enumeration on pages 1–25, followed by visual review of all original statements and required definition passages.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=checks),source_notes=ambient['source_issues'],unresolved_source_references=ambient['excluded_references'],ambient_resolution=ambient['statement_resolution'],artifacts=artifacts,evidence=evidence,review_limits=['Source transcription and statement-dependency audit, not proof certification or correction of source errors.','Pinned preprint inspected; exact equivalence to final journal typesetting is not asserted.','The source lower-density mismatch and unprovided covering/bracketing convention details remain recorded explicitly.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
