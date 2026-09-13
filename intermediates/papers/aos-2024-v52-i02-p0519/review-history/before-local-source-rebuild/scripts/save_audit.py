"""Record source review after a separate inventory enumeration and census validation."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text())
PDF=Path(prov['cached_pdf']);WORK=Path(prov['working_pdf']).parent
for name in ['theorem-inventory.json','ranked-interfaces.json']:
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],check=True)
inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
data=json.loads((ROOT/'ranked-interfaces.json').read_text())
ambient=json.loads((ROOT/'ambient-conventions.json').read_text())
review=json.loads((ROOT/'inventory-review.json').read_text())
assert digest(PDF)==paper['pdf_sha256']==prov['pdf_sha256']==digest(WORK/'source.pdf')
assert review['source_checked'] and review['status']=='complete'
assert digest(ROOT/'theorem-inventory.json')==review['inventory_sha256']
pdf=fitz.open(PDF)
assert len(pdf)==34 and paper['main_text_last_pdf_page']==34
assert not paper['main_text_boundary']['shared_page_with_appendix']
assert '2210.13008v3' in pdf[0].get_text() and '27 Jan 2024' in pdf[0].get_text()
assert not any('appendix' in entry[1].lower() for entry in pdf.get_toc())
labels=[]
for n,page in enumerate(pdf,1):
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(span['text'] for span in line['spans']).strip()
            match=re.fullmatch(r'THEOREM\s+(\d+)\.',text,re.I)
            if match:labels.append((n,match.group(1)))
expected=[(3,'1'),(4,'2'),(6,'3'),(6,'4'),(7,'5'),(7,'6'),(8,'7'),(9,'8'),(12,'9'),(12,'10'),(17,'11'),(25,'12')]
assert labels==expected,labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
for original,final in zip(inv['claims'],data['claims']):
    for key in original:assert original[key]==final[key],(key,original['claim_id'])
counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
assert counts==dict(theorems=12,interfaces=16,source_members=16,direct_theorem_uses=45,related_theorem_connections=85,unranked_auxiliary_passages=19),counts
members=[m for x in data['interfaces'] for m in x['members']]
byid={m['local_id']:m for m in members}
claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
related={x['members'][0]['local_id']:{r['claim_id'].split('/T')[-1] for r in x['related_theorems']} for x in data['interfaces']}
# Source-backed separations: general-prior theorem, existential lower bound,
# truth-only optional condition, and generator eigen-pairs without a stochastic prerequisite.
assert related['D9']==related['D10']=={'2','9','10'}
assert related['D8']=={'2','9','10','12'}
assert related['D11']=={'3'} and related['D13']=={'8'}
assert related['D16']==related['D12']=={'6','7','8','10'}
assert related['D15']=={'12'} and related['D14']=={'11','12'}
assert '8' not in related['D4'] and '8' not in related['D1']
assert byid['D5']['depends_on']==['D3']
assert set(claims['4']['depends_on'])=={'D1','D2','D4'}
assert set(claims['12']['depends_on'])=={'D1','D7','D8','D15'}
assert r'\overline f_N\equiv f_{\overline\theta_N}' in claims['2']['statement_original']
assert r'\overline\theta_N=E^\Pi[\theta\mid' in claims['2']['statement_original']
assert r'\|\widetilde P_N-P_{D,f}\|_{H^2\to H^2}' in claims['4']['statement_original']
assert r'B) The conclusions in A)' in claims['8']['statement_original']
assert r'\mathcal O_0$ of $\mathcal O_{(w)}' in claims['8']['statement_original']
assert r'f_0=1/2$ on $\mathcal O\setminus\mathcal O_{00}' in claims['9']['statement_original']
assert r'if in addition (10) holds for $f_0$' in claims['10']['statement_original']
assert r'\|f-f_0\|_{(H_c^1)^*}^2' in claims['11']['statement_original']
assert r'0<b<B-A-2' in claims['12']['statement_original']
assert r'\mathcal F_N\cap\{f:d(f,f_0)\leq\overline\delta_N\}' in claims['12']['statement_original']
assert r'\frac{p_{D,f}(X_0,X_D)}{p_{D,f}(X_0,X_D)}' in byid['D15']['statement_original']
assert r'\frac{p_{D,f_0}(X_0,X_D)}{p_{D,f}(X_0,X_D)}' in byid['D14']['statement_original']
assert set(ambient['standard_ambient_resolution'])=={'shared'}|{str(n) for n in range(1,13)}
for item in data['claims']+members+ambient['auxiliary_passages']:
    assert all(1<=e['page']<=34 for e in item['evidence'])
    for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',item['statement_original'],re.S):
        depth=0
        for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
            depth+=1 if brace=='{' else -1
            assert depth>=0,('unbalanced braces',item)
        assert depth==0,('unbalanced braces',item)
    for ctx in item.get('naming_context',[])+item.get('application_context',[]):
        assert all(1<=e['page']<=34 for e in ctx['evidence'])
for n in [1,2,3,4,5,6,7,8,9,10,12,14,17,21,22,25,26,27,34]:
    shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json']}
evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=34,main_text_last_pdf_page=34,provenance_path='evidence/source-provenance.json'),
    enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='All 34 PDF pages independently searched for complete numbered Theorem heading lines by joining the small-cap spans. Exactly Theorems 1-12 occur. The external citation beginning Theorem 4.3.3 on page 31 is not an environment. Section 3 Proofs is numbered main text, so its Theorems 11 and 12 are included. No attached appendices occur; references end on page 34.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,
    validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
        'The inventory and final census pass separate validator invocations. The original inventory hash matches its source review, and every original theorem field is preserved in the final census.',
        'Title, author, arXiv v3 stamp dated 27 January 2024, 34-page count, versioned URL and PDF SHA-256 match the inspected source. The source outline and final page establish a main text with no attached appendices.',
        'The twelve complete theorem statements were reviewed on pages 3,4,6,7,8,9,12,17,25. All fit on their cited page. All subparts, inherited-hypothesis references, inequalities, rates and constant dependencies are retained.',
        'All sixteen interface passages and their source kinds, natural-language keywords and selectors were checked against the pinned PDF. The model, operator, eigen-pairs, Gaussian prior, projection estimator, first-eigenspace condition, geometric domain and KL neighborhood remain distinct source objects.',
        'Theorem 2 retains the nonlinear link applied to the posterior mean of theta. Its source instruction to consult Theorems 9/10 is archived together with their precise prior and regularity setting. This is not changed to the posterior mean of f or to an arbitrary Gaussian prior.',
        'Theorem 4 retains its existential domain and all-estimator infimum in H2 operator loss. It does not acquire the explicit estimator (63), its truncation or the particular domain used by its proof.',
        'The nested hypotheses of Theorems 6 and 7 are expanded through original source excerpts. The eigenfunction condition (10) is independent of the pairwise coefficient bounds; Theorem 8 uses it as a conclusion, and Theorem 10 only in the faster-rate branch at the truth.',
        'The Gaussian field has the printed N rescaling and indices 0 through K. The cutoff sets O00 and O0 retain their nesting and different roles for the truth and prior. The estimator uses its different indices 0 through J-1 and its original zero extension.',
        'Theorem 11 resolves Proposition 2 branch B, with individual C1 positivity and Hs bounds, and the compact-support Sobolev dual. The source C2 parameter-class ambiguity is recorded rather than silently strengthening the hypotheses.',
        'Theorem 12 retains arbitrary N-dependent priors, two distinct radius sequences, prior mass, sieve tail, test-error bounds and the posterior sieve intersection. Its neighborhood retains the repeated density ratio as printed, with the contrasting proof formula archived separately.',
        'Nineteen auxiliary passages preserve the required main-text conventions and inherited source clauses. Sixteen source notes record material ambiguities independently of original statements. No external or appendix proof content is required by the saved census.',
        'The final graph has 45 direct theorem uses and 85 deduplicated same-paper connections, all with source-backed path explanations and selectors. The separate validation checks the key scope distinctions and balanced mathematical fragments.'
    ]),source_notes=[
        'The audit concerns the pinned arXiv v3 source; equivalence to journal wording has not been established.',
        'The KL-neighborhood variance ratio, the claimed smoothness of enlarged rectangles, and the one-sided projection description of a two-sided estimator compression are retained as source discrepancies rather than repaired.',
        'Other recorded scope issues include the general-prior reset, theta-versus-f prior coordinates, Theorem 4 parameter and operator domains, the exponent reference, volume normalization, spectral indexing, Theorem 11 regularity, and posterior-mean proof shorthand.'
    ],unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
    review_limits=['Source-fidelity and statement-dependency audit; does not certify the proofs or repair the source.','No appended or external supplementary material used.']))
write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
print(json.dumps(counts))
