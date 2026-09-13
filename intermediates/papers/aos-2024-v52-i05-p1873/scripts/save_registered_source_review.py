"""Check the frozen census after an independent source and dependency review.

Execution checks retained review evidence; it does not certify mathematical proofs.
"""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import PID,REPO,ROOT,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': '269b267b5c612714f0d1d938a7f1d86ded73b77a27f714f3b2bd48ed738af055', 'source-passages.json': '48bbb09da7b1da7a75846b6f16e7da5a21824f35afbdf61a179ebc5ee1e39d67', 'interface-extraction.json': 'f47a8ef3f0fb9c4be173bf1a2e0fb0d02c6d6e69a393a9bd1c53a2a4d0140ff2', 'ambient-prerequisites.json': '2f721f4aa5ac8391ed83d8e4d6ff34995fc9d4e4152009d40fd7ab199183af18', 'unfinalized-census.json': 'a7831d7cb9494cab8eb0e0035ec21f92ad04ad0d6cd99c32528dd15c56829561', 'ranked-interfaces.json': 'eadbd324305922eb3cfc22b0728a45092c3c0aedfd4d84c98dd445c695ca39e2'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    assert len(EXPECTED)==6
    for n,sha in EXPECTED.items():assert digest(ROOT/n)==sha,('Changed reviewed content',n)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(p for p in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if p['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2207.06107v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2207.06107'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    assert paper['source_url']==URL=='https://arxiv.org/pdf/2207.06107v2'
    assert paper['pdf_pages']==registered['pdf_pages']==103 and paper['main_text_last_pdf_page']==34
    ir=json.loads((ROOT/'inventory-review.json').read_text());assert ir['status']=='complete' and ir['source_checked']
    assert ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    headings=ir['printed_label_check'];assert headings==[[5,'1.9'],[7,'1.11'],[9,'1.17'],[9,'1.18'],[10,'1.20'],[29,'5.3']]
    assert len(inv['claims'])==len(data['claims'])==6
    for original,c in zip(inv['claims'],data['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    groups={m['local_id']:x['interface_id'] for x in data['interfaces'] for m in x['members']}
    # Independent graph reconstruction from the source; no generator graph is imported.
    local={'D1':[],'D2':[],'D3':['D2'],'D4':['D1'],'D5':['D4'],'D6':['D4','D5','D7'],'D7':[],
      'D8':['D5','D7'],'D8g':['D7'],'D9':[],'D10':['D9'],'D11':['D9','D10'],'D12':['D4'],
      'D13':['D1'],'D14':[],'D15':['D1'],'D16':['D11','D12'],'D17':['D16'],'D18':['D1','D7'],'D19':[],'D20':[]}
    direct={'1.9':{'D5','D11','D12','D13','D14','D19'},
      '1.11':{'D4','D8','D9','D10','D11','D12','D13','D14','D16'},
      '1.17':{'D4','D8','D9','D13','D14','D16','D19'},
      '1.18':{'D2','D3','D8g','D9','D10','D11','D13','D14','D16'},
      '1.20':{'D2','D3','D4','D8','D8g','D9','D10','D11','D12','D14','D15','D16','D19','D20'},
      '5.3':{'D1','D4','D6','D7','D8','D13','D14','D16','D17','D18'}}
    reach={'1.9':{'D1','D4','D5','D9','D10','D11','D12','D13','D14','D19'},
      '1.11':{'D1','D4','D5','D7','D8','D9','D10','D11','D12','D13','D14','D16'},
      '1.17':{'D1','D4','D5','D7','D8','D9','D10','D11','D12','D13','D14','D16','D19'},
      '1.18':{'D1','D2','D3','D4','D7','D8g','D9','D10','D11','D12','D13','D14','D16'},
      '1.20':{'D1','D2','D3','D4','D5','D7','D8','D8g','D9','D10','D11','D12','D14','D15','D16','D19','D20'},
      '5.3':{'D1','D4','D5','D6','D7','D8','D9','D10','D11','D12','D13','D14','D16','D17','D18'}}
    assert {k:set(m['depends_on']) for k,m in members.items()}=={k:set(v) for k,v in local.items()}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        visited=set();stack=list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in visited:visited.add(lid);stack.extend(members[lid]['depends_on'])
        assert visited==reach[n],(n,visited)
        assert {groups[l] for l in visited}=={x['interface_id'] for x in data['interfaces'] if any(t['claim_id']==c['claim_id'] for t in x['related_theorems'])}
    assert 'D13' not in reach['1.20'] and 'D15' in reach['1.20']
    assert 'D8g' in reach['1.18'] and 'D8' not in reach['1.18'] and 'D5' not in reach['1.18']
    assert 'D6' in reach['5.3'] and all('D6' not in r for n,r in reach.items() if n!='5.3')
    b={k:m['statement_original'] for k,m in members.items()}
    assert r'\hat x_t(i):=x_t(i)/\sqrt N' in b['D1']
    assert r'\hat Y_i:=' in b['D2'] and r't\in[[k]]' in b['D2'] and r'\frac1N\sum_{i=1}^Ny_t(i)' in b['D2']
    assert b['D3'].count(r'(\hat Y_t\hat Y_t\')^{-1/2}'.replace('\\\'',"'"))==2
    assert r'\sum_{t=1}^kP_t' in b['D4'] and 'random projections' in b['D4']
    assert r'\frac1N\sum_{i=1}^N\delta_{\lambda_i(H)}' in b['D5']
    assert r'G(z):=(H-z)^{-1}' in b['D6'] and r'\mu_N(dz)' in b['D6']
    assert 'no matter the dimension' in b['D7'] and r'N^{-1}\operatorname{Tr}A' in b['D7']
    assert r'N\int f(\lambda)\mu_N(d\lambda)' in b['D8']
    assert b['D8g']=='Similarly, we can define LSS for any square matrix.'
    assert r'\int_{\mathbb R}(x-z)^{-1}d\mu(x)' in b['D9'] and r'-(m_\mu(z))^{-1}' in b['D9']
    assert 'unique analytic functions' in b['D10'] and all(x in b['D10'] for x in ['(9)','(10)','(11)',r'(k-1)F_{\mu_t}',r'\omega_t(i\eta)'])
    assert all(x in b['D11'] for x in ['(12)','(13)','analogues of (8)',r'm_\boxplus:=-1/F_\boxplus'])
    assert r'y_t\delta_1+(1-y_t)\delta_0' in b['D12'] and '(almost surely)' in b['D12']
    assert 'i.i.d. columns' in b['D13'] and r'\ell\in\mathbb N' in b['D13'] and 'for all $N,a,b$' in b['D13']
    assert r'\hat y_t\in[0,1)' in b['D14'] and r'y-\max_ty_t\geq c' in b['D14']
    assert 'Keeping the first two assumptions' in b['D15'] and 'continuous distributions' in b['D15'] and r'4+\delta' in b['D15']
    assert all(x in b['D16'] for x in [r'\bigcup_{a=1}^6C_a',r'\bigcup_{a=3}^7C_a',r'\Im z\leq\epsilon_2',r'\gamma_1^0&:=\gamma(',r'\gamma_2^0&:=\gamma(',r'\overline{\mathcal C^0}','counterclockwise','nonintersecting',r'\operatorname{supp}(\mu_\boxplus)\setminus0'])
    assert r'|\Im z|\geq N^{-K}' in b['D17'] and 'large (but fixed)' in b['D17']
    assert all(x in b['D18'] for x in [r'x>2N^K',r'x<N^K',r'\mathbb E(\xi\cdot\Xi)',r'\prod_{t=1}^k',r'\operatorname{tr}(X_tX_t\')^{-1}'.replace('\\\'',"'"),r'\chi^{(n)}(x)'])
    assert r'{2x}' in b['D19'] and r'\pi' not in b['D19'] and 'mu_N' not in b['D19']
    assert b['D20'].count(r'(Y_tY_t\')^{-1/2}'.replace('\\\'',"'"))==2 and r'\mu=0' in b['D20']
    for lid in ['D13','D14','D15']:assert members[lid]['source_kind']=='assumption'
    assert members['D10']['source_kind']=='source_passage' and members['D10']['source_heading']=='Proposition 1.5'
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert r'\sum_{t=1}^kp_t=p' in a['A1'] and 'independent' in a['A1']
    assert r'Y_t:=(y_t(1),\ldots,y_t(N))' in a['A2']
    assert r'T_tT_t\'=\Sigma_{tt}\succ0'.replace('\\\'',"'") in a['A3'] and '$x_i$' in a['A3']
    assert r'y_t:=p_t/N' in a['A4'] and r'p_{\max}:=\max_tp_t' in a['A5']
    assert 'Any quantities that are not explicit constant or fixed may depend on $N$' in a['A6']
    assert r'C^{-1}b\leq|a|\leq Cb' in a['A6'] and r'|a|/b\to\infty' in a['A6']
    assert '(8)' in a['A7'] and 'nonnegative imaginary part' in a['A7']
    assert 'i.i.d. columns' in a['A8'] and r'\mathbb E[|X_{ab}|^2]=1/N' in a['A8'] and 'C_\ell' not in a['A8']
    assert r'\frac{\operatorname{Tr}B^2-a_1}{b_1}' in a['A9'] and r'b_1=4\sum_{r\ne s}^k' in a['A9']
    assert r'\hat y\in(0,1)' in a['A10'] and r'b_2=-2\log(1-y)' in a['A10']
    assert r'\sqrt' not in a['A9']+a['A10']
    assert r'(X_tX_t\')^{-2}X_t'.replace('\\\'',"'") in a['A11']
    assert '$N$-dependent' in a['A12'] and 'does not enclose $0$' in a['A13']
    assert 'invertible with high probability' in a['A14'] and r'\lambda_1(A)\geq' in a['A15']
    refs=ambient['source_claim_references'];assert len(refs)==2
    assert refs[0]['substitutions']=={'B':'B-hat','N':'N-1'} and refs[0]['to_auxiliary_ids']==['A9','A10']
    assert refs[1]['to_claim_ids']==[PID+'/T1.11',PID+'/T1.17',PID+'/T1.18']
    assert refs[1]['replacement']=='Assumption 1.19, with Assumption 1.7 retained'
    originals=list(members.values())+data['claims']+ambient['unranked_auxiliary_passages']
    for obj in originals:
        s=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',s)
        assert not any(ord(c)<32 and c!='\n' for c in s)
        assert s.count('$')%2==0
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        for e in obj['evidence']:
            assert 1<=e['page']<=34
            if e['page']==34:assert e.get('before_main_text_end') is True
    for x in data['interfaces']:
        lids={m['local_id'] for m in x['members']}
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label'];selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors)
            linked=own+' '+' '.join(c['statement_original'] for c in data['claims'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems']))
            assert all(s in linked for s in selectors)
        for rel in x['related_theorems']:
            n=rel['claim_id'].split('/T')[-1]
            assert rel['relation']==('direct' if lids & direct[n] else 'indirect')
            path=rel['via_local_ids'];assert path[0] in direct[n] and path[-1] in lids
            assert all(right in members[left]['depends_on'] for left,right in zip(path,path[1:]))
            ex=x['theorem_explanations'][rel['claim_id']];assert ex['via_local_ids']==path and ex['text'].strip() and ex['evidence']
        for k in x['source_keywords']:
            m=members[k['local_id']];assert any(k['source_text'] in s for s in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=6,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(a))
    assert counts==dict(theorems=6,interfaces=20,source_members=21,direct_theorem_uses=54,related_theorem_connections=79,unranked_auxiliary_passages=15)
    assert sum(len(c['depends_on']) for c in data['claims'])==55
    assert len(ambient['source_issues'])==25
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for c in rebuilt['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(inventory='Six complete main-text Theorems: 1.9, 1.11, 1.17, 1.18, 1.20 and 5.3. The last is in the proof section and remains included. Appendix A starts partway down page 34; retained page evidence ends above it.',source_passages='Twenty source groups with twenty-one original members, including separate H-specific and generic LSS passages. Fifteen auxiliary passages resolve the observation model, dimensions, asymptotic conventions, inherited Corollaries and Q_t.',dependencies='Independent reconstruction confirms 55 local direct uses, deduplicated to 54 group/Theorem uses, and 79 related connections. The source definition of the contours reaches the original Bernoulli convolution even in the tilde theorem; this is distinct from an H-specific LSS premise.',inheritance='Theorem 1.18 retains both Corollaries with simultaneous B and N substitutions. Theorem 1.20 retains three Theorems and two Corollaries with their branch-specific conditions, replacing the stronger moment assumption. Its dependency closure contains D15 and never D13.',notation='Visual comparison confirms the all-N trace normalization, y multiplying the entire second fraction in Theorem 1.17, the tilde -1/z correction, the product cutoff expectation, the truncated contour convention and the derivative scope in K.',names_and_highlights='Every source member has meaning-bearing source-backed selectors; every group has original natural-language naming evidence and an explanation for every related theorem. Original Definition, Assumption, Proposition and neutral passage headings remain distinct.',limits='Twenty-five source issues preserve apparent density/centering/scale errors, contour inconsistencies, singular inverse and zero-eigenvalue conventions, overloaded symbols and other unresolved meanings without rewriting source statements. No proof certification, appendix-body audit or published-version substitution is claimed.',reproduction='All six content artifacts reproduce byte for byte using the retained per-paper scripts. Inventory handoff, independent graph reconstruction, source identity and structural validation passed.')
    write('evidence/manual-findings.json',findings)
    images=[1,2,3,4,5,6,7,8,9,10,11,17,18,29,34]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.jpg',sha256=digest(ROOT/f'evidence/page-{n:02}.jpg'),**({'before_main_text_end':True} if n==34 else {})) for n in images]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=103,main_text_last_pdf_page=34,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent actual bold-heading enumeration and visual comparison of all six statements, including the page-6 continuation.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=refs,evidence=evidence,review_limits=['Registered arXiv v2 source; no assumption of equivalence to the published article.','Source inconsistencies are preserved and documented, not resolved by reading appendices.','Census validation does not certify mathematical correctness or proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=103,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
