"""Check the frozen source-reviewed census independently of the extraction builder."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={
 'theorem-inventory.json':'99a3a98a36492c665b2583fd5f4478f536e9201a4478a7b72c581519fc40a990',
 'source-passages.json':'5a460c6de124530a507e7f1c27927c74226d8654cc9b837025fa25c80d4ecd2a',
 'interface-extraction.json':'f94aa703bd05fb2caa7817d9c983c4c4529a8ae4efbf199896ef1cbcdf3b56df',
 'ambient-prerequisites.json':'d195b2607552ed4de16dcd7d9e856b813f84040c2da31109a96e1880d17b09be',
 'unfinalized-census.json':'dbd2ec80276cd4d2f8d906a2836cac5aad3b7c7671ed7a5df765dc770a08cb9e',
 'ranked-interfaces.json':'d350b094d52600d03f7d0e298840f8228716cdd10936e08a01a7a3ae257148b1'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Reviewed content changed',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2209.13485v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2209.13485'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert ir['printed_label_check']==[[4,'1.3']]
    assert paper['source_url']==URL=='https://arxiv.org/pdf/2209.13485v2'
    assert paper['pdf_pages']==registered['pdf_pages']==34 and paper['main_text_last_pdf_page']==26
    assert paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==1
    c=d['claims'][0];assert {k:v for k,v in c.items() if k!='depends_on'}==inv['claims'][0]
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Reconstructed from the inspected source, without importing build_census.py.
    local={'D1':set(),'D2':{'D1','D3'},'D3':{'D1'},'D4':set()}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    assert set(c['depends_on'])==set(local)
    assert [m['D'+str(n)]['source_kind'] for n in range(1,5)]==['definition','assumption','definition','definition']
    s={lid:a['statement_original'] for lid,a in m.items()}
    checks={
      'D1':[r'\Sigma=\mathbb E[XX^\top]','with zero mean','independent and identically distributed'],
      'D2':['i.i.d. copies',r'\mathbb E[\|X\|^p]<+\infty',r'p\geq4',r'\mathbb E[X]=0','non-null',r'\#\{i\in[n]:Y_i\ne X_i\}\leq\eta n',r'\eta\in[0,1)'],
      'D3':[r'\kappa_p:=\sup_{v\in\mathbb R^d,\,\langle v,\Sigma v\rangle=1}',r'\mathbb E[|\langle X,v\rangle|^p]^{\frac1p}'],
      'D4':['non-zero',r'\mathbb R^{d\times d}_{\geq0}',r'r(M)=\frac{\operatorname{tr}(M)}{\|M\|}']}
    for lid,parts in checks.items():
        for part in parts:assert part in s[lid],(lid,part)
    assert s['D3'] in s['D2']
    assert 'positive definite' not in s['D2'] and r'\|v\|=1' not in s['D3']
    assert r'\kappa_p^2' in m['D3']['naming_context'][0]['text']
    assert r'\|M\|^2' not in s['D4']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==4 and len(ambient['source_issues'])==7
    assert 'symmetric positive semidefinite' in aux['A1']['statement_original']
    assert r'[n]:=\{i\in\mathbb N:1\leq i\leq n\}' in aux['A2']['statement_original']
    assert 'operator norm' in aux['A3']['statement_original'] and r'\langle\cdot,\cdot\cdot\rangle' in aux['A3']['statement_original']
    assert 'may differ from the original sample' in aux['A4']['statement_original']
    assert set(ambient['statement_local_bindings'])=={'T1.3'} and ambient['source_claim_references']==[]
    originals=list(m.values())+[c]+list(aux.values())
    for obj in originals:
        text=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',text)
        assert not any(ord(ch)<32 and ch!='\n' for ch in text)
        assert text.count('$')%2==0
        assert len(re.findall(r'(?<!\\)\\\[',text))==len(re.findall(r'(?<!\\)\\\]',text))
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        assert obj['evidence'] and all(1<=e['page']<=26 for e in obj['evidence'])
    assert {x['name'] for x in d['interfaces']}=={'Covariance matrix','I.i.d. sample with contamination','Moment condition','Stable rank'}
    for x in d['interfaces']:
        assert len(x['members'])==1
        a=x['members'][0];lid=a['local_id'];own=a['statement_original']+' '+a['local_label']
        selectors=a['highlight_symbols']+a['highlight_phrases']
        assert any(sel in own for sel in selectors)
        assert all(sel in own+' '+c['statement_original'] for sel in selectors)
        assert len(x['central_claim_uses'])==len(x['related_theorems'])==1
        assert x['central_claim_uses'][0]['claim_id']==c['claim_id']
        rel=x['related_theorems'][0];assert rel['claim_id']==c['claim_id'] and rel['relation']=='direct' and rel['via_local_ids']==[lid]
        assert set(x['theorem_explanations'])=={c['claim_id']}
        ex=x['theorem_explanations'][c['claim_id']];assert ex['via_local_ids']==[lid] and ex['text'].strip() and ex['evidence']
        assert 'This theorem directly uses the API.' not in ex['text']
        for kw in x['source_keywords']:
            if 'context_id' in kw:
                ctx=next(ctx for ctx in a['naming_context'] if ctx['context_id']==kw['context_id'])
                assert kw['source_text'] in ctx['text'] and all(1<=e['page']<=26 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
    counts=dict(theorems=1,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=1,interfaces=4,source_members=4,direct_theorem_uses=4,related_theorem_connections=4,unranked_auxiliary_passages=4)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='One complete main-text Theorem, 1.3, on page 4. All main-text pages 1-26 were inspected for actual result headings. Proposition 2.2 is excluded despite prose citations calling it Theorem. The main text ends on page 26; the Appendix begins on page 27 and no appendix body is used.',
      source_passages='Four separate entries retain the population covariance, full Assumption 1.2, its embedded moment-constant definition, and the trace-to-operator-norm stable rank. The complete assumption and its separately indexed formula are both preserved; the extraction does not rewrite or combine their definitions. Four auxiliary passages supply matrix, norm, trace, finite-set and contamination context.',
      dependencies='Independent reconstruction confirms four direct uses and four related connections. Assumption 1.2 uses the covariance and moment constant; the moment constant uses the covariance; the generic stable rank does not depend on the sampling model. The existentially bound estimator does not import its proof construction or PAC-Bayesian machinery into the statement graph.',
      notation='Visual and font-span comparison confirms the sans-serif estimator with a hat and subscript star, two separate square-root terms, kappa_4 squared versus kappa_p squared, and eta exponent 1-2/p. The moment directions have unit population variance, not unit Euclidean norm. Nonzero covariance is not strengthened to positive definiteness.',
      scope='The contamination mechanism replaces at most eta*n observations; no iid or independence condition is added to Y. The theorem tightens eta<1 to eta<1/2. Kappa_4 is the exponent-four instance of the same moment definition. Original slash notation and the printed sample-size threshold are preserved, with proof-text differences recorded separately rather than silently corrected.',
      names_and_highlights='Every entry has an original-source natural-language term, an exact source label or formula selector, and an explanation naming the corresponding object in Theorem 1.3. The moment naming context distinguishes kappa_p from the square called a hypercontractivity constant. Stable rank retains the paper-specific trace ratio.',
      reproduction='Six content artifacts reproduce byte-for-byte from retained per-paper scripts. Independent checks preserve the reviewed content hashes and source-specific graph. A script rerun is neither a new semantic source review nor a proof certificate.')
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=34,main_text_last_pdf_page=26,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id']],printed_label_check=ir['printed_label_check'],method='Independent bold-font enumeration and visual comparison of the complete original Theorem 1.3.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv v2 source; no assumption of equivalence to the published article.','Source ambiguities remain separate from original quotations; no appendix-body content is used.','Census validation does not certify mathematical correctness or the proof.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=34,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
