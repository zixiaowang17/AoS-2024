"""Validate frozen source-reviewed content independently of the census builder."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={
 'theorem-inventory.json':'dff2e31dd002eb0b518c1ed3944ee9301516da2b115cc828ac24f3d0045c0f0c',
 'source-passages.json':'50847d348c94c41c38cd5026e049a036f0a05df256d1c17a4e0d3ab945b971bc',
 'interface-extraction.json':'239c76ade9285c0c0481eec323366727f1d991ff482186c9de5c766492cb8cec',
 'ambient-prerequisites.json':'502eca237d05e4d9ef7e50ce99a3475cc1bd166382c38906b84a7cdcc3be3bb4',
 'unfinalized-census.json':'69372a7cbc61ec261d20e2bb94b213ade7614288742e5981d57daf3c796d1df0',
 'ranked-interfaces.json':'d4512808f04ccb25fafb2cf37ae8a846c8a2cf322be9a8fbf0447dd4abeac806'}
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
    assert registered['version']=='nihms-2151735.pdf' and registered['source_url']==URL
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert ir['printed_label_check']==[[6,'1'],[8,'2']]
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==36
    assert paper['main_text_last_pdf_page']==23 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==2
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Reconstructed from the source scopes; no extraction/finalizer graph imported.
    raw={1:[],2:[1],3:[1,2],4:[1,2],5:[4],6:[4],7:[4],8:[5,6,7],9:[1],10:[1],11:[1,2],12:[1],13:[8],14:[2,12]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'1':ids([1,2,3,8,9,10,11]),'2':ids([1,9,10,12,13,14])}
    expected_reach={'1':ids(range(1,12)),'2':ids([1,2,4,5,6,7,8,9,10,12,13,14])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n]
    assert not ids([3,11])&expected_reach['2']
    assert not ids([12,13,14])&expected_reach['1']
    s={lid:a['statement_original'] for lid,a in m.items()}
    snippets={
      1:['independent from',r'\mathbb E(\varepsilon\mid\mathbf x)=0',r'\operatorname{Var}(\varepsilon\mid\mathbf x)=\sigma^2',r'b_0'],
      2:['independent and identically distributed',r'H_0:\boldsymbol\beta=\boldsymbol\beta_0','is known'],
      3:[r'\mathbf x_i-\boldsymbol\mu_X',r'\mu_Y',r'\Sigma_X(\boldsymbol\beta-\boldsymbol\beta_0)'],
      4:[r'\mathbf x_i-\bar{\mathbf x}',r'y_i-\bar y','slight abuse of notation'],
      5:[r'\frac2{n(n-1)}\sum_{i<j}',r'k_n\boldsymbol\alpha^\top\mathbf z_i\mathbf z_j^\top\boldsymbol\alpha','positive number'],
      6:[r'\widehat\Sigma_Z','sample covariance'],
      7:[r'\widehat{\Sigma_Z^2}',r'\sum_{i\ne j}',r'(\mathbf z_i\mathbf z_j^\top)^2',r'\left(\frac1{n(n-1)}\sum_{i\ne j}\mathbf z_i\mathbf z_j^\top\right)^2'],
      8:[r'\frac{nW_n}{\sqrt{2\widehat{\operatorname{tr}(\Omega^2)}}}',r'\operatorname{tr}(\widehat{\Sigma_Z^2})',r'2k_n\boldsymbol\alpha^\top\widehat{\Sigma_Z^2}\boldsymbol\alpha',r'k_n^2(\boldsymbol\alpha^\top\widehat\Sigma_Z\boldsymbol\alpha)^2'],
      9:[r'\Gamma=\Sigma_X^{1/2}','variance one','bounded fourth order moments',r'\sum_{i=1}^s l_{\alpha_i}\leq4'],
      10:['i.i.d. random variables','mean zero','bounded fourth order moments'],
      11:[r'n^{-1/2}\delta\mathbf u',r'|\delta|\leq C',r'\|\mathbf u\|=1','nonnegative constant independent of $p$'],
      12:[r'S=p^{1-s}','nonzero coefficients','i.i.d. sub-Gaussian distributions',r'variance $\gamma^2$','uniformly randomly generated'],
      13:[r'T_n>z_a','right $a$ quantile'],
      14:[r'P_0(T=1)+\mathbb E_\pi[\mathbb I(T=0)]','type I error','type II error']}
    for n,parts in snippets.items():
        for part in parts:assert part in s['D'+str(n)],(n,part)
    assert r'\bar{\mathbf x}' not in s['D3'] and r'\boldsymbol\mu_X)\{' not in s['D4']
    assert 'independent coordinates' not in s['D9'] and 'Gaussian' not in s['D10']
    assert 'proxy' not in s['D12'] and r'\boldsymbol\beta-\boldsymbol\beta_0' not in s['D12']
    for n in [9,10]:assert m['D'+str(n)]['source_kind']=='assumption'
    assert m['D11']['source_kind']=='condition'
    for n in [1,2,12,13]:assert m['D'+str(n)]['source_kind']=='source_passage'
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==10 and len(ambient['source_issues'])==10
    assert r'\Omega=\Sigma_Z+k_n\Sigma_Z^{1/2}\boldsymbol\alpha\boldsymbol\alpha^\top\Sigma_Z^{1/2}' in aux['A1']['statement_original']
    assert aux['A1']['depends_on']==['D3'] and r'\widehat' not in aux['A1']['statement_original']
    assert r'\frac2{n^2}' in aux['A2']['statement_original']
    assert 'nonsingular' in aux['A4']['statement_original']
    assert r'\mathbf z^0' in aux['A5']['statement_original'] and r'\mathbf z_0' not in aux['A5']['statement_original']
    assert r'\sigma^2=1' in aux['A6']['statement_original']
    assert 'goes to infinity in probability' in aux['A7']['statement_original']
    assert r'\frac1{n-1}' in aux['A8']['statement_original'] and r'\bar{\mathbf z}' in aux['A8']['statement_original']
    assert set(ambient['statement_local_bindings'])=={'T1','T2'}
    assert any(x['reference_kind']=='proof_only' and x['to_claim_id']==PID+'/T1' for x in ambient['source_claim_references'])
    for a in aux.values():assert set(a['depends_on'])<=set(m)
    for obj in list(m.values())+d['claims']+list(aux.values()):
        text=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',text)
        assert not any(ord(ch)<32 and ch!='\n' for ch in text)
        assert text.count('$')%2==0 and text.count(r'\[')==text.count(r'\]')
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        assert obj['evidence'] and all(1<=e['page']<=23 for e in obj['evidence'])
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
                assert all(1<=e['page']<=23 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
    counts=dict(theorems=2,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=2,interfaces=14,source_members=14,direct_theorem_uses=13,related_theorem_connections=23,unranked_auxiliary_passages=10)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Both original main-text Theorems are complete, each with its two distinct parts. Theorem 1 has null and local-alternative normal limits; Theorem 2 has lower and upper detection bounds. All main-text theorem headings through page 23 were independently enumerated.',
      source_passages='Fourteen original entries and ten auxiliary passages preserve the iid linear model, hypotheses, both score versions, W_n, the sample covariance, separate squared-covariance estimator, studentized statistic, A1-A2, local alternative, REM, rejection rule and prior-average risk. Unnamed population normalization and source conventions remain available as auxiliary passages.',
      dependencies='Independent reconstruction confirms 13 direct uses and 23 related connections. Theorem 1 uses both sample-based T_n and the population covariance in its shift. Theorem 2 does not acquire the deterministic local alternative or population-score interface, and Theorem 1 does not acquire the REM or all-tests risk.',
      subparts='Gaussian errors belong only to Theorem 2(i). Its part (ii) does not explicitly print k_n=o(sqrt(p)); the proof-only reference to Theorem 1 is recorded without importing that condition. A1 factorizes coordinate moments only through total degree four; full coordinate independence is not inserted.',
      notation='Visual review distinguishes the hat on Sigma_Z squared from the square of Sigma-hat_Z, checks both lines of (6), retains matrix squares and off-diagonal pairs, and distinguishes the population trace in (8) from the estimated denominator in (5). The page-11 population comparison notation is z^0, with superscript zero.',
      limits='Ten source conventions or ambiguities are retained, including population covariance aliasing, score reuse, normalization domains, finite/asymptotic variance notation, nonsingularity for the score equivalence, REM support/tail conventions and the asymptotic testing criterion. No appendix content or unquoted correction is added.',
      names_and_highlights='Every entry uses literal source terms and faithful definition/assumption/source-passage headings. Symbol and assumption-label selectors are checked against the original passage or related Theorem, and every connection has a source-specific explanation.',
      reproduction='All six JSON content artifacts reproduce byte for byte from the retained per-paper scripts. Frozen hashes and independent source-specific checks protect the reviewed state; rerunning scripts alone is not a new semantic audit or proof certification.')
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=[1,3,4,5,6,8,11,23],visually_reviewed_crops=['theorem-1.png','theorem-2.png','covariance-estimator.png','assumptions.png','risk.png','power-context.png','practical-covariance.png']))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1])) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=36,main_text_last_pdf_page=23,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-heading enumeration and visual comparison of both complete Theorems.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered NIH author manuscript identified by filename and hash; no claim of byte-equivalence to the final typeset journal article.','Original source conventions and ambiguities are retained separately; no appendix material is used in the census.','Source and schema validation do not certify mathematical proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=36,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
