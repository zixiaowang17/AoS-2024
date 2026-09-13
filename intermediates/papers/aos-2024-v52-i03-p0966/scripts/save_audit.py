"""Verify source enumeration, complete statements and independently traversed dependencies."""
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
pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==99
assert paper['main_text_last_pdf_page']==29 and paper['main_text_boundary']['shared_page_with_appendix']
first=' '.join(pdf[0].get_text().split())
assert paper['title'].lower() in first.lower()
for author in prov['authors']:assert author.lower() in first.lower()
assert '2107.12364v3' in first and '16 Jun 2024' in first
assert paper['source_url']=='https://arxiv.org/pdf/2107.12364v3'
assert paper['version']=='arXiv:2107.12364v3'
labels=[]
for n in range(29):
    page=pdf[n];clip=fitz.Rect(0,0,page.rect.width,prov['main_text_end_y']) if n==28 else page.rect
    assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text(clip=clip),n+1
    for block in page.get_text('dict',clip=clip)['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip()
            match=re.match(r'^THEOREM (\d+)(?=[.\s(])',text)
            if match:labels.append((n+1,int(match.group(1))))
assert labels==[(9,1),(10,3),(11,5),(12,6),(16,10),(21,18),(24,20),(26,22),(28,24)],labels
assert [(c['evidence'][0]['page'],int(c['claim_id'].split('/T')[-1])) for c in inv['claims']]==labels
heading=pdf[28].get_text(clip=fitz.Rect(0,prov['main_text_end_y'],pdf[28].rect.width,651))
assert 'APPENDIX A: SMOOTHNESS CLASSES AND DENSITY ESTIMATION' in heading
assert len(inv['claims'])==len(data['claims'])==9
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
expected={
 '1':[1,2,3,4,5,6,7,8],
 '3':[1,2,3,9,11],
 '5':[11,14,15,16,18],
 '6':[1,2,3,4,5,6,7,9,10,11,20],
 '10':[1,2,3,4,5,6,7,9,10,11,12,13,20,21,22,23,24,25],
 '18':[7,11,13,14,15,16,17,18,19,22,26,27,28,29],
 '20':[2,3,9,11,12,13,22,30,31,32,33,34,35,36,40],
 '22':[2,3,4,5,6,7,9,10,11,14,15,16,17,18,19,22,23,24,26,27,28,37],
 '24':[7,11,13,14,15,16,17,18,19,38,39]
}
assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()}
for x in data['interfaces']:
    lids={m['local_id'] for m in x['members']}
    assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
    assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
assert reach['6'].isdisjoint({'D21','D22','D24','D26','D27','D40'})
assert reach['20'].isdisjoint({'D1','D14','D15','D16','D17','D18','D19','D26','D27','D28','D29'})
assert reach['24'].isdisjoint({'D1','D3','D5','D6','D9','D10','D20','D21','D22','D23','D24','D27','D28'})
assert 'D20' not in reach['18'] and 'D31' not in reach['10']
for lid in ['D1','D20','D28','D30','D31','D33']:assert byid[lid]['source_kind']=='condition'
for lid in ['D11','D21','D26','D37','D39','D40']:assert byid[lid]['source_kind']=='source_passage'
t={n:c['statement_original'] for n,c in claims.items()}
assert 'Lebesgue-almost every' in t['1'] and r'\varphi_0:\mathbb R^d\to\mathbb R' in t['1']
assert r'\overline{\Omega\'}' not in t['3'] # no escaped apostrophe in the mathematical subdomain
assert r"\overline{\Omega'}\subseteq\Omega^\circ" in t['3'] and t['3'].count(r'\alpha\notin\mathbb N')==2
assert r'\alpha\notin' not in t['5'] and 'mean-zero' not in t['5']
assert r'\int\psi_0\,d(\widehat Q-Q)' in t['6'] and r'\tag{16}' in t['6']
assert r'(\log n)^2/n' in t['10'] and r'\varphi_0^*\in\mathcal C^{\alpha+1}' in t['10']
assert r'\log n/n' in t['18'] and r'(\log n)^2/n' not in t['18']
assert r'\sqrt{\frac{\operatorname{Var}_P[\phi_0(X)]}{n}+\frac{\operatorname{Var}_Q[\psi_0(Y)]}{m}}' in t['18']
assert [e['page'] for e in claims['18']['evidence']]==[21,22]
assert r'L_n^{1/d}' in t['20'] and r'\overline T_m' in t['20'] and r'\widehat T_{nm}' in t['20']
assert t['20'].endswith(',\n\\]')
assert '(38)' in t['22'] and '(39)' in t['22'] and '(iii) (Empirical Measures)' in t['22']
assert r'\varphi_0^*\in\mathcal C^{\alpha+1}(\Omega)' in t['22']
for s in [r'\overline M',r'\overline\gamma',r'\overline u',r'|\mathcal I|<\infty',r'P_{n^{-1/2},h_1}^{\otimes n}\otimes Q_{m^{-1/2},h_2}^{\otimes m}']:assert s in t['24']
assert r'\varphi_0' not in t['24'] and r'\phi_0' in t['24']
assert r'L^1(\Omega)\times L^1(\Omega)' in byid['D6']['statement_original']
assert r'\mathcal K_T' in byid['D17']['statement_original'] and r'(\varphi,\psi)\in L^1(P)\times L^1(Q)' in byid['D17']['statement_original']
assert r'2^{j_0}-1' in byid['D23']['statement_original']
assert r'\sum_{\xi\in\Psi^{\mathrm{bc}}}' in byid['D24']['statement_original']
assert r'\tau(\lambda_\ell/\lambda_{L_n})' in byid['D34']['statement_original'] and r'\lambda_{L_m}' not in byid['D34']['statement_original']
assert r'\left\lfloor\frac{s-1}{2}\right\rfloor' in byid['D35']['statement_original']
assert 'Appendix L' in byid['D39']['statement_original']
counts=dict(theorems=9,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=9,interfaces=40,source_members=40,direct_theorem_uses=62,related_theorem_connections=109,unranked_auxiliary_passages=17),counts
assert set(ambient['standard_ambient_resolution'])=={'shared',*claims}
assert len(ambient['unresolved_source_conventions'])==31 and len(ambient['unresolved_statement_references'])==4
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=28 for e in item['evidence'])
    fragments=[item['statement_original']]
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=28 for e in ctx['evidence']);fragments.append(ctx['text'])
    for text in fragments:
        assert not re.search(r'[\u4e00-\u9fff]',text)
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            depth=0
            for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if b=='{' else -1
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
for n in [7,8,15,20,23,25,27]:shutil.copyfile(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
write('source-passages.json',dict(paper_id=PID,members=members))
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-extraction.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
checks=[
 'Pinned source title, four authors, arXiv version/date, page count and SHA checked against the PDF. Every archived main-text page equals fresh byte-preserving extraction, with page 29 clipped before the appendix.',
 'Independent PDF line enumeration finds exactly nine actual Theorem headings, including background results. Theorem 18 continues to page 22. All original inventory fields survive the finalized handoff unchanged.',
 'Source inspection preserves the different phi glyphs, the interior-domain closure, each regularity qualification, and Theorem 1 inverse identities without source repair.',
 'Theorem 10 squared-logarithmic rate differs from Theorem 18 single-logarithmic rate; both variance terms in Theorem 18 are inside one radical.',
 'Theorem 20 preserves bar versus hat maps, the L_n power and the distinct C1/C2 conditions. Reusing R_K does not import kernel prerequisites.',
 'Theorem 22 original equation references are resolved through full (38)–(39), tuning and variance excerpts, preserving branch-specific conjugate regularity and endpoint sample-size ratios.',
 'Theorem 24 preserves all three barred constants, finite-set suprema and both product experiments. Its appendix-only path construction remains explicitly unresolved.',
 'Forty source passages retain original names, conditions, estimator constructions and meaningful selectors. Independent traversal verifies 62 direct uses and 109 related theorem connections.',
 'Deterministic Theorem 6 has no sampling model; generic-domain Theorem 20 has no torus or kernel dependency; torus Theorem 24 does not inherit the unused Euclidean branch of its cost functional.',
 'Seventeen auxiliary passages and thirty-one source notes retain notation, original ambiguities and excluded references. All quotation evidence is on pages 3–28; no appendix mathematics is used.'
]
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=99,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Fresh PDF line enumeration across pages 1–28 and clipped main-text page 29; visually checked Theorem labels and statement endings. Background Theorems remain included; propositions, lemmas and corollaries remain excluded.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=checks),source_notes=ambient['unresolved_source_conventions'],unresolved_source_references=ambient['unresolved_statement_references'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,review_limits=['Source transcription and statement-prerequisite audit, not proof certification or source repair.','Pinned preprint audited; equivalence to the final journal layout is not asserted.','Precise appendix-only norms, basis construction and local paths are explicitly unresolved under the main-text-only policy.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
