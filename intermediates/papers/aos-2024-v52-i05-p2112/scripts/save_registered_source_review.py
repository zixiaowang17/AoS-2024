"""Validate frozen source-reviewed content independently of the census builder."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '02db6d6df5649563e44bd7fd0ac099b2e1846a306b91be51575ee17031414ecf', 'source-passages.json': 'b834b162718affcc0b655784420b3bfafc3982c07ea3d485c176b89ff46810d0', 'interface-extraction.json': '81b3f9d23b757e0e891c143e1442065364f819371f52216dfa7742578de47945', 'ambient-prerequisites.json': '5b9ed464a1f2ca457ee4b88b6023996fc0c6c392dec85ffaa5392a3756af748d', 'unfinalized-census.json': '77319c3c8347aca4c9131bb42ff8903c4f84f4b4fa96a652bcd7a342770822d7', 'ranked-interfaces.json': 'f8cd40017c7ddc35cade3c16556c0d71da727a5f53918cb6aa1d24409dfce775'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2209.04962v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2209.04962'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert ir['printed_label_check']==[[2,'1'],[5,'2'],[9,'3'],[12,'4']]
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==41
    assert paper['main_text_last_pdf_page']==29 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==4
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Reconstructed from the source scopes; no extraction/finalizer graph imported.
    raw={1:[],2:[1],3:[1,2],4:[1],5:[],6:[5],7:[5],8:[5,6,7],9:[5]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'1':ids([2,3,4]),'2':ids([6,8,9]),'3':ids([2,3,4]),'4':ids([6,8,9])}
    expected_reach={'1':ids([1,2,3,4]),'2':ids([5,6,7,8,9]),'3':ids([1,2,3,4]),'4':ids([5,6,7,8,9])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n]
    assert not expected_reach['1']&expected_reach['2']
    s={lid:a['statement_original'] for lid,a in m.items()}
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==12 and len(ambient['source_issues'])==7
    source_specific_checks(s,m,aux,ambient)
    for obj in list(m.values())+d['claims']+list(aux.values()):
        text=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',text)
        assert not any(ord(ch)<32 and ch!='\n' for ch in text)
        assert text.count('$')%2==0 and text.count(r'\[')==text.count(r'\]')
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        assert obj['evidence'] and all(1<=e['page']<=29 for e in obj['evidence'])
    for x in d['interfaces']:
        assert len(x['members'])==1
        a=x['members'][0];lid=a['local_id'];own=a['statement_original']+' '+a['local_label']
        linked=own+' '+' '.join(c['statement_original'] for c in d['claims'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems']))
        selectors=a['highlight_symbols']+a['highlight_phrases'];assert any(v in own for v in selectors) and all(v in linked for v in selectors)
        assert {u['claim_id'] for u in x['central_claim_uses']}=={PID+'/T'+n for n,v in direct.items() if lid in v}
        assert set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
        for rel in x['related_theorems']:
            n=rel['claim_id'].split('/T')[-1];path=rel['via_local_ids']
            assert rel['relation']==('direct' if lid in direct[n] else 'indirect')
            assert path[0] in direct[n] and path[-1]==lid and all(b in local[a] for a,b in zip(path,path[1:]))
            ex=x['theorem_explanations'][rel['claim_id']];assert ex['via_local_ids']==path and ex['text'].strip() and ex['evidence']
            assert 'This theorem directly uses the API.' not in ex['text']
        for kw in x['source_keywords']:
            if 'context_id' in kw:
                ctx=next(v for v in a['naming_context'] if v['context_id']==kw['context_id']);assert kw['source_text'] in ctx['text']
                assert all(1<=e['page']<=29 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
    counts=dict(theorems=4,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=4,interfaces=9,source_members=9,direct_theorem_uses=12,related_theorem_connections=18,unranked_auxiliary_passages=12)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='All four main-text Theorems are preserved: asymptotic phase and orthogonal results, followed by their finite-sample counterparts. Theorem environments were independently enumerated through the main-text prefix of page 29. The italic no-noise consequences in Theorems 1-2 belong to their original statements.',
      source_passages='Nine original entries and twelve supporting passages retain unit-complex and orthogonal parameter spaces, both masked Gaussian models, matrix completions, both spectral estimators, full-rank polar normalization and both source loss definitions.',
      dependencies='Independent reconstruction gives 12 direct uses and 18 related connections. Each theorem depends on its own model, estimator and loss. Population eigenvectors/eigenspaces and first-order approximations are proof-only. The phase and orthogonal dependency sets remain disjoint.',
      degeneracies='The phase estimator returns 1 for zero eigenvector coordinates. The orthogonal estimator returns the identity for singular blocks and invokes the polar map only on full-rank blocks. No invented tie-breaking rule or extension of the polar map is added.',
      source_issues='The orthogonal loss display contains a free j and omits the sum suggested by the prose; it is preserved exactly. Other issues include the unit-circle variable typo, zero-noise division convention, complex/real ambient declarations and finite-sample constant scope. Exact theorem remainders and probability constants are retained.',
      names_and_highlights='All entries use literal source terms and faithful source-passage/definition headings. Source selectors and explanations are checked for every related theorem. Models and the distinct losses are not merged merely because their roles are analogous.',
      reproduction='All six JSON content artifacts reproduce byte for byte from retained per-paper scripts. Source-specific checks and frozen hashes protect the reviewed content; this source census does not certify proofs or silently repair the loss definition.')
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=[1,2,4,5,9,10,11,12,29],visually_reviewed_crops=['theorem-1.png','theorem-2.png','theorem-3.png','theorem-4.png','orthogonal-loss.png']))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=41,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-heading enumeration and visual comparison of all four complete Theorems.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv v2 manuscript identified by version and hash; no claim of byte-equivalence to the final journal article.','Original source conventions and ambiguities are retained separately; no appendix material is used in the census.','Source and schema validation do not certify mathematical proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=41,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(s,m,aux,ambient):
    snippets={
      1:[r'\{x\in\mathbb C:|z|=1\}','unit complex numbers',r'e^{i\theta_j^*}'],
      2:[r'z_j^*\overline{z_k^*}',r'\operatorname{Bernoulli}(p)',r'\mathcal{CN}(0,1)',r'\mathcal N(0,1/2)','independent of each other'],
      3:['leading eigenvector',r'\dfrac{u_j}{|u_j|}',r'1,&\text{if }u_j=0'],
      4:[r'\min_{a\in\mathbb C_1}\frac1n\sum_{j=1}^n',r'z_j^*a','up to a phase'],
      5:[r'd>0',r'UU^T=U^TU=I_d','all orthogonal matrices'],
      6:[r'Z_j^*Z_k^{*T}',r'\mathcal{MN}(0,I_d,I_d)',r'\operatorname{Bernoulli}(p)','all independent of each other'],
      7:['full-rank',r'B=MDV^T',r'B=(MV^T)(VDV^T)',r'\mathcal P(B):=MV^T'],
      8:['largest $d$ eigenvalues',r'\mathcal P(U_j),&\text{if }\det(U_j)\ne0',r'I_d,&\text{if }\det(U_j)=0'],
      9:[r'\min_{O\in O(d)}\frac1n',r'\|\widehat Z_j-Z_j^*O\|_F^2','analogously to (5)']}
    for n,parts in snippets.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    assert r'\sum' not in s['D9'] and r'\widehat Z_j' in s['D9']
    assert 'det' not in s['D5']
    assert m['D2']['source_kind']==m['D6']['source_kind']=='source_passage'
    assert m['D3']['source_kind']==m['D7']['source_kind']==m['D8']['source_kind']=='definition'
    a={k:v['statement_original'] for k,v in aux.items()}
    for part in [r'X_{jj}:=0',r'X_{kj}:=\overline{X_{jk}}',r'W_{kj}:=\overline{W_{jk}}',r'A\circ(z^*z^{*H}+\sigma W)']:assert part in a['A1'],part
    for part in [r'\mathcal W\in\mathbb C^{nd\times nd}',r'\mathcal W_{jj}:=0_{d\times d}',r'\mathcal W_{kj}:=\mathcal W_{jk}^T',r'(A\otimes J_d)\circ(Z^*Z^{*T}+\sigma\mathcal W)']:assert part in a['A2'],part
    assert r'\Omega^{-1}(X-M)^T\Sigma^{-1}(X-M)' in a['A3']
    assert 'functions of $n$' in a['A4'] and 'independent of $n$' in a['A5']
    assert 'all entries being one' in a['A6'] and r'U\circ V\in\mathbb R^{d_1\times d_2}' in a['A7']
    assert 'analogous to (5)' in a['A8'] and 'orthonormal columns' in a['A10']
    assert set(ambient['statement_local_bindings'])=={'T1','T2','T3','T4'}
    refs=ambient['source_claim_references']
    assert sum(x['reference_kind']=='summary_relation' for x in refs)==2
    assert sum(x['reference_kind']=='proof_only' for x in refs)==2
    for a in aux.values():assert set(a['depends_on'])<=set(m)
if __name__=='__main__':main()
