"""Finish source review after an independent validation of the saved census."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());PDF=Path(prov['cached_pdf']);WORK=Path(prov['working_pdf']).parent
for name in ['theorem-inventory.json','ranked-interfaces.json']:
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],check=True)
inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-conventions.json').read_text());review=json.loads((ROOT/'inventory-review.json').read_text())
assert digest(PDF)==paper['pdf_sha256']==prov['pdf_sha256']
assert review['source_checked'] and review['status']=='complete'
assert digest(ROOT/'theorem-inventory.json')==review['inventory_sha256']
pdf=fitz.open(PDF)
assert len(pdf)==36 and paper['main_text_last_pdf_page']==18
assert paper['main_text_boundary']['shared_page_with_appendix'] is True
labels=[]
for n in range(18):
    clip=fitz.Rect(0,0,pdf[n].rect.width,prov['main_text_end_y']) if n==17 else None
    for block in pdf[n].get_text('dict',clip=clip)['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                if span['font']=='NimbusRomNo9L-Medi':
                    m=re.match(r'^Theorem (\d+)(?:$| \()',span['text'].strip())
                    if m:labels.append((n+1,m.group(1)))
assert labels==[(12,'1'),(15,'4'),(17,'5')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
assert [e['page'] for e in inv['claims'][1]['evidence']]==[15,16]
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=3,interfaces=13,source_members=13,direct_theorem_uses=21,related_theorem_connections=32,unranked_auxiliary_passages=12),counts
members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members};claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
related={x['members'][0]['local_id']:{r['claim_id'].split('/T')[-1] for r in x['related_theorems']} for x in data['interfaces']}
assert all(related[lid]=={'1','4','5'} for lid in ['D1','D2','D3','D4','D5','D6','D7','D8','D10'])
assert related['D9']=={'1','4'} and related['D11']==related['D12']=={'4'} and related['D13']=={'5'}
assert set(claims['1']['depends_on'])=={'D1','D3','D4','D5','D8','D9','D10'}
assert set(claims['4']['depends_on'])=={'D1','D3','D4','D5','D9','D10','D11','D12'}
assert set(claims['5']['depends_on'])=={'D1','D3','D4','D8','D10','D13'}
assert byid['D6']['depends_on']==[] and byid['D7']['depends_on']==['D6']
assert set(byid['D8']['depends_on'])=={'D1','D6','D7'}
assert r'\inf_{K\geq1,\,f\in\mathcal F}' in claims['1']['statement_original']
assert r'\frac{2AV^2}{4^{(K-1)/q}}' in claims['4']['statement_original']
assert r'\frac{2^{K+1}p\log^{4/\gamma+1}(n)}n' in claims['4']['statement_original']
assert r'2(2+q)\left(\frac{AV^2}q\right)^{q/(2+q)}' in claims['4']['statement_original']
assert claims['5']['statement_original'].startswith('Suppose Assumptions 2 holds.')
assert r'\log(Np/d)\log^{4/\gamma}(N)}N' in claims['5']['statement_original']
assert r'\boldsymbol x\leq\widehat b' in byid['D4']['statement_original']
assert 'and/or' in byid['D4']['statement_original']
assert r'h(\boldsymbol x)=\sum_{k=1}^Mh_k(\boldsymbol x)' in byid['D6']['statement_original']
assert r'\nu\geq1+2/(q-2)' in byid['D12']['statement_original']
assert 'for any $K\geq1$' in byid['D12']['statement_original']
assert 'without replacement' in byid['D13']['statement_original']
assert 'B$ independent copies' in byid['D13']['statement_original']
for item in data['claims']+members+ambient['auxiliary_passages']:
    for e in item['evidence']:
        assert e['page']<=18
        if e['page']==18:assert e.get('before_main_text_end') is True
    for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',item['statement_original'],re.S):
        depth=0
        for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
            depth+=1 if brace=='{' else -1
            assert depth>=0,('unbalanced braces',item)
        assert depth==0,('unbalanced braces',item)
for n in [1,2,3,5,6,7,8,9,10,11,12,14,15,16,17,18]:
    shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
shutil.copy2(WORK/'appendix-heading-only.png',ROOT/'evidence/appendix-heading-only.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=36,main_text_last_pdf_page=18,main_text_end_y=421,provenance_path='evidence/source-provenance.json'),
    enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Main pages 1-17 and the portion of page 18 above Appendix A were searched. Independent bold-font heading enumeration confirms Theorems 1, 4 and 5; Theorem 4 continues onto page 16. Numbers 2 and 3 label Corollaries. The main-text page-18 image is clipped above Appendix A, and a separate heading-only crop records the boundary.',printed_label_check=labels,excluded_result_types=['Lemma','Corollary','Remark'],appendix_material_used=False),counts=counts,
    validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
        'The original source-reviewed theorem inventory passes a separate validator invocation and its bytes match the inventory-review hash. The final census preserves all three complete theorem records and their source order.',
        'The pinned PDF hash, version stamp, cover date, authors and 36-page count were checked. Appendix A begins on page 18; all extracted statement evidence is above the documented main-text endpoint.',
        'Theorem 1 includes both bounds, the positive-constant declaration, the penalty condition and the additional depth infimum in (11). Theorem 4 includes its full continuation and penalty rate. Theorem 5 retains its printed grammar and N-based complexity term.',
        'Thirteen source interface passages were reviewed against the pinned main-text pages, including the conditional mean, split objective, candidate success probability, recursive tree and node output, finite ridge variation/library, relaxed local norm, pruning, Assumptions 2-4 and the forest.',
        'Twelve auxiliary passages preserve empirical versus population norms, expectation scope, the uniform q convention, sample-size dependent A/V, finite-dictionary notices and the formal empty-node convention.',
        'The separate census validator accepts all local and canonical edges, source keywords, original highlights and every same-paper theorem explanation. Independently specified scope checks confirm 21 direct uses and 32 deduplicated related-theorem connections.',
        'Pruning reaches only Theorems 1 and 4, Assumptions 3/4 reach only Theorem 4, and forest construction reaches only Theorem 5. The general oracle bounds do not acquire Assumption 1, a mu-in-F condition, or consistency corollary regimes.',
        'The finite ridge-expansion sum precedes G and its L2 closure/relaxed norm in the local graph. The source ambiguity between those norm notations is recorded without rewriting the original definitions.',
        'The forest uses without-replacement subsamples of size N and independent randomization copies sharing the original data. Its RHS success probabilities are interpreted using the subsampled-data convention explicitly stated after Theorem 5.',
        'Source ambiguities are kept in a separate analysis artifact, including the finite norm notation, partition indexing, projection endpoints, pruning wording, depth-uniform node-count condition and degenerate split/probability conventions. Mathematical fragments have balanced braces.'
    ]),source_notes=[
        'This is a census of the pinned arXiv v2 source, not an assertion that its wording or numbering matches the journal typesetting.',
        'No proof validation or correction of the source is claimed. A source discrepancy can be faithfully recorded while the census passes source and data-contract validation.',
        'The main-text notices of more general finite-dictionary fits do not supply a separate fully specified theorem version. The concrete node-average output (2) is retained, and no appendix body is read.',
        'The paper-wide internal-node notation is accompanied by a formal empty-node extension in the orthogonal-expansion discussion. Its applicability to split-success probabilities is recorded as unresolved rather than silently choosing a convention.'
    ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
    review_limits=['Source-fidelity and statement-dependency audit, not proof certification or mathematical repair.','Appendix A and B bodies excluded; only the Appendix A heading is used to document the shared-page boundary.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
