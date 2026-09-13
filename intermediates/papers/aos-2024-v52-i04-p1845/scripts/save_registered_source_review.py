"""Record completed manual source review and independently check the frozen artifacts.

Running this script is not a new mathematical review or proof certification.
The registered source's original notation and unresolved conventions are preserved.
"""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import PID,REPO,ROOT,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': '7b51e9d16626fd9f259a0c02ebc30483d6f553431fc736d6e8ba46bf787435ca', 'source-passages.json': 'c1f46e384fd9c0c2f514efac4aa4b03f11e0649c61cd04a885ad9b9a7ec94701', 'interface-extraction.json': '552bd877e9ee6b7a86bac25f63438d9e8d7a0358a0c6974b22b6294e955714e1', 'ambient-prerequisites.json': '310bdf947fd3c93aa7992f0caa61ae71270365369a5786df85564cd8bc1c4d81', 'unfinalized-census.json': '9c62df347c6cd6b40786d9fc47b81ff40e25cc8c48d60e7077ffdc8f6a3b5622', 'ranked-interfaces.json': '47008677afd617aef09112e7872c6fc14b1d6397f06308121c1eab27b05b8e7d'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(p for p in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if p['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2203.10418v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2203.10418'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    assert paper['source_url']==URL=='https://arxiv.org/pdf/2203.10418v2'
    assert paper['pdf_pages']==registered['pdf_pages']==79 and paper['main_text_last_pdf_page']==27
    ir=json.loads((ROOT/'inventory-review.json').read_text());assert ir['status']=='complete' and ir['source_checked']
    assert ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    headings=ir['printed_label_check'];assert headings==[[11,'3.3'],[14,'3.5'],[15,'3.6'],[15,'3.7'],[18,'4.1'],[19,'4.2'],[20,'4.3'],[23,'4.5'],[24,'4.6']]
    assert len(inv['claims'])==len(data['claims'])==9
    for original,c in zip(inv['claims'],data['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Independent reconstruction from the source, not imported from the generator.
    local={1:[],2:[],3:[],4:[],5:[],6:[5],7:[6],8:[],9:[],10:[9],11:[1,8],12:[1,8],
        13:[],14:[2],15:[12,14],16:[10,11],17:[1,13],18:[1],19:[10,11,15],20:[],21:[6,10]}
    direct={'3.3':{1,2,3,10,11,13,16},'3.5':{1,2,3,6,7,10,13,16,21},
        '3.6':{1,2,3,6,7,10,13,16,21},'3.7':{1,2,4,6,7,10,13,16,21},
        '4.1':{1,10,11,13,15,17,18,19},'4.2':{13,17,18,19},'4.3':{10,13,17},'4.5':{9,20},'4.6':{9,20}}
    reach={'3.3':{1,2,3,8,9,10,11,13,16},'3.5':{1,2,3,5,6,7,8,9,10,11,13,16,21},
        '3.6':{1,2,3,5,6,7,8,9,10,11,13,16,21},'3.7':{1,2,4,5,6,7,8,9,10,11,13,16,21},
        '4.1':{1,2,8,9,10,11,12,13,14,15,17,18,19},'4.2':{1,2,8,9,10,11,12,13,14,15,17,18,19},
        '4.3':{1,9,10,13,17},'4.5':{9,20},'4.6':{9,20}}
    assert {k:set(m['depends_on']) for k,m in members.items()}=={f'D{k}':{f'D{i}' for i in v} for k,v in local.items()}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])=={f'D{i}' for i in direct[n]}
        visited=set();stack=list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in visited:visited.add(lid);stack.extend(members[lid]['depends_on'])
        assert visited=={f'D{i}' for i in reach[n]}
        assert visited=={x['members'][0]['local_id'] for x in data['interfaces'] if any(t['claim_id']==c['claim_id'] for t in x['related_theorems'])}
    b={k:m['statement_original'] for k,m in members.items()}
    assert r'Y=f_0(X)+\varepsilon' in b['D1'] and r'\mathbb E[|\varepsilon|^p\mid X=x]' in b['D1']
    assert 'some distribution' in b['D2'] and r'\|f_0\|_\infty:=' in b['D2']
    assert r'p\geq1' in b['D3'] and 'for all' in b['D3']
    assert 'symmetric around $0$' in b['D4'] and r'\mathbb E[|\varepsilon|\mid X=x]\leq v_1' in b['D4']
    assert r'\beta=r+s' in b['D5'] and r'0<s\leq1' in b['D5']
    assert r'(\partial f)/' in b['D5'] and r'\partial^rf' in b['D5']
    assert r'\pi:[t]\to[d]' in b['D6'] and r'\mathcal H(d,l-1,\mathcal P)' in b['D6']
    assert r'\mathbb N^+' in b['D6'] and b['D6'].count('C>0')==2
    assert r'(\beta^*,d^*)=\operatorname{argmin}' in b['D7']
    assert r'\frac12x^2' in b['D8'] and r'\tau|x|-\frac12\tau^2' in b['D8']
    assert r'\mathcal L_{L+1}\circ\sigma' in b['D9'] and r'W_ix+b_i' in b['D9']
    assert r'\sigma(x)=\max\{0,x\}' in b['D9'] and r'(d,N,\cdots,N,1)' in b['D9']
    assert r'\{f=T_Mg:g\in\mathcal F_n(d,L,N)\}' in b['D10'] and r'\operatorname{sgn}(u)(|u|\wedge M)' in b['D10']
    assert r'\frac1n\sum_{i=1}^n\ell_\tau(Y_i-f(X_i))' in b['D11']
    assert r'\mathbb E_{X,Y}\{\ell_\tau(Y-f(X))\}' in b['D12']
    assert r'\sqrt{\mathbb E_{X\sim\mathbb P_X}|f(X)|^2}' in b['D13']
    assert 'all measurable functions' in b['D14'] and 'same $M' in b['D14']
    assert r'\operatorname{argmin}_{f\in\Theta}\mathcal R_\tau(f)' in b['D15']
    assert r'+\delta^2' in b['D16'] and 'approximate empirical risk minimizers' in b['D16']
    assert r'\liminf_{n\to\infty}\inf_{\widehat f_n}\sup_{f_0\in\mathcal F}' in b['D17']
    assert r'\varepsilon_i\sim N(0,1)' in b['D17'] and 'all estimators' in b['D17']
    assert r'\mathcal U(d,p,\mathcal F)' in b['D18'] and r'\mathbb E[|\varepsilon|^p\mid X]\leq1' in b['D18']
    assert r'\widehat{\mathcal R}_\tau(f_{0,\tau})' in b['D19'] and r'\text{or }' in b['D19'] and r'n^{-100}' in b['D19']
    assert r'\mathbf1_{\{\alpha_i<K\}}\Delta' in b['D20'] and r'\mathbb N^+' in b['D20']
    assert r'\bar L=c_3\lceil L\log L\rceil' in b['D21'] and 'Proposition 3.4' in b['D21']
    claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
    for lid,num in [('D16','3.3'),('D18','4.1'),('D19','4.1'),('D20','4.5'),('D21','3.5')]:
        assert b[lid] in claims[num]['statement_original'] and members[lid]['source_kind']=='theorem_excerpt'
    for lid in ['D2','D3','D4']:assert members[lid]['source_kind']=='condition'
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert 'i.i.d. observations' in a['A1'] and 'unique referred numbers' in a['A2']
    assert r'\{f(X_i)-Y_i\}^2' in a['A3'] and r'\mathcal R(\widehat f_n)-\mathcal R(f_0)' in a['A4']
    assert r'\operatorname{argmin}_{f\in\mathcal F_n(d,L,N,M)}' in a['A5']
    assert r'c_1=2\max\{2M,(2v_p)^{1/p}\}' in a['A6']
    assert 'depend only on' in a['A7'] and r'c_5(NL)^{-2\gamma^*}' in a['A7']
    assert r'\nu^*=1-\frac1{2p-1}' in a['A8'] and r'\nu^\dagger=1-1/p' in a['A9']
    assert '(almost surely)' in a['A10'] and 'uniform distribution' in a['A10']
    assert r'B_\infty(x,r)' in a['A11'] and r'\|f-f_0\|_n^2' in a['A12']
    assert 'does not require the network weights to be uniformly bounded' in a['A13']
    assert r'\mathcal C(d,\beta)' in a['A14']
    refs=ambient['source_claim_references'];assert len(refs)==1
    assert refs[0]['from_claim_id']==PID+'/T4.2' and refs[0]['to_claim_id']==PID+'/T4.1'
    assert refs[0]['reference_kind']=='hypothesis_and_definition_inheritance'
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
        assert all(1<=e['page']<=27 for e in obj['evidence'])
    for x in data['interfaces']:
        m=x['members'][0];own=m['statement_original']+' '+m['local_label']
        selectors=m['highlight_symbols']+m['highlight_phrases'];assert any(s in own for s in selectors)
        linked=own+' '+' '.join(c['statement_original'] for c in data['claims'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems']))
        assert all(s in linked for s in selectors)
        for rel in x['related_theorems']:
            n=rel['claim_id'].split('/T')[-1];assert rel['relation']==('direct' if int(m['local_id'][1:]) in direct[n] else 'indirect')
            path=rel['via_local_ids'];assert int(path[0][1:]) in direct[n] and path[-1]==m['local_id']
            assert all(right in members[left]['depends_on'] for left,right in zip(path,path[1:]))
            ex=x['theorem_explanations'][rel['claim_id']];assert ex['via_local_ids']==path and ex['text'].strip() and ex['evidence']
        for k in x['source_keywords']:assert any(k['source_text'] in s for s in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=9,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(a))
    assert counts==dict(theorems=9,interfaces=21,source_members=21,direct_theorem_uses=53,related_theorem_connections=83,unranked_auxiliary_passages=14)
    assert len(ambient['source_issues'])==29 and set(ambient['statement_resolution'])=={'shared',*direct}
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for c in rebuilt['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Nine actual main-text Theorems with complete source bodies and continuations: 3.3, 3.5, 3.6, 3.7, 4.1, 4.2, 4.3, 4.5 and 4.6. Diagram labels, citations, Propositions, Lemmas and Remarks are excluded. Main text ends on page 27 before References.',
        source_passages='Twenty-one source entries preserve regression, boundedness, moment and symmetry conditions, smoothness/composition definitions, least component ratio, Huber loss, ReLU and truncated networks, empirical/population loss, population norm, comparison functions and minimizer, two distinct estimator sets, minimax smoothness, experiment family, regions and architecture. Fourteen auxiliary passages resolve source conventions and constants.',
        dependencies='Independent source reconstruction verifies 53 direct uses and 83 related connections. Theorem 4.2 expressly imports definitions and hypotheses from Theorem 4.1. Figure 2 proof arrows do not define the graph. Deterministic Theorems 4.5 and 4.6 connect only to network and region definitions.',
        estimator_scope='Upper bounds concern every member of S_n,tau(delta). Lower bounds assert existence of a bad member of the different S_HN set, whose two alternative branches remain intact. The population minimizer f0,tau need not be f0 and is not restricted to the network class.',
        conditions='General upper-bound design differs from the lower uniform-design experiment. Conditional p-th moments and conditional symmetry/first-moment assumptions remain separate. Theorem 3.7 does not acquire an invented second-moment condition, and its bare S notation and H argument swap are recorded as source ambiguities.',
        names_and_highlights='Natural-language names use literal source keywords with archived naming context where needed. Original source kinds/headings remain distinguishable. Every entry has source-backed selectors, and every related theorem has an explanation tracing its same-paper dependency path.',
        notation='Visual comparison preserves derivative and argmin conventions, squared tolerance, distinct loss normalization, all lower-bound quantifiers and log powers, binary-expansion index and parenthesis issues, point-label mismatch and missing width wording. Positive-integer superscripts were corrected after glyph reinspection and the inventory independently revalidated.',
        limits='Twenty-nine source issues record unexpanded parameter and mathematical conventions without repairing originals. The pseudo-dimension appendix was not read and is not a dependency of the explicit theorem formula. Registered arXiv v2 was not replaced with a published source. No proof certification is claimed.',
        reproduction='All six content artifacts reproduce byte for byte with retained per-paper scripts. Source identity, main-text enumeration, complete inventory handoff, formula and scope checks, independent graphs, names, selectors, explanations and structural validation passed.')
    write('evidence/manual-findings.json',findings)
    images=[1,7,8,9,10,11,12,13,14,15,16,17,18,19,20,23,24,25,27]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.jpg',sha256=digest(ROOT/f'evidence/page-{n:02}.jpg'),**({'before_main_text_end':True} if n==27 else {})) for n in images]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
        source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=79,main_text_last_pdf_page=27,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent bold-heading enumeration and visual comparison of all nine complete original statements, including continuations.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
        counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,review_limits=['Source census of registered arXiv v2; no published-version substitution.','Unexpanded conventions and an unused appendix reference remain recorded within the main-text-only scope.','The census preserves source statements and ambiguities; it does not certify mathematical correctness or proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=79,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
