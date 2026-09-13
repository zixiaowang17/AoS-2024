"""Record completed manual source review and independently check the frozen artifacts.

Running this script is not a new mathematical review or proof certification.
The registered source's original notation and unresolved conventions are preserved.
"""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import PID,REPO,ROOT,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': 'd7abf70b9fa33ae5fbd53398720bfe8d2c0d87dda3c8c46461994a8cb423817e', 'source-passages.json': '8c4f02833b25fda95f06b589cb90c1ff43596dfe9a9366670e9f6a626587194e', 'interface-extraction.json': '5a79b6fe741d546872b90f39a5799701d05d02f626fd80a972edd9a51c006c5d', 'ambient-prerequisites.json': 'ce73249bdd2df4de962cd97443ed89e09b3aaa4a88470c4a4838240920aa23d3', 'unfinalized-census.json': 'c36b79a9aae32f40cb352f37956d37148b555b1fb483cddb6494ce1c6b5ba918', 'ranked-interfaces.json': '3569e77a544dc05326c461c1b0d27a4876a7e84521ac249a3dce00f24e682715'}
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
    assert registered['version']=='2307.08136v3.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2307.08136'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    assert paper['source_url']==URL=='https://arxiv.org/pdf/2307.08136v3'
    assert paper['pdf_pages']==registered['pdf_pages']==19 and paper['main_text_last_pdf_page']==18
    ir=json.loads((ROOT/'inventory-review.json').read_text());assert ir['status']=='complete' and ir['source_checked']
    assert ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    headings=ir['printed_label_check'];assert headings==[[6,1],[7,2],[10,3],[10,4],[11,5]]
    assert len(inv['claims'])==len(data['claims'])==5
    for original,c in zip(inv['claims'],data['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Independently reconstructed from the source statements and their local objects.
    local={1:[],2:[1],3:[1],4:[3],5:[3,4],6:[1,3,4,5],7:[4,5],8:[1,4],
        9:[4,6,7,8],10:[1],11:[1,4,9],12:[3,4],13:[1,4,6],14:[4,9,11,12],
        15:[4,9,14],16:[3,4],17:[3,4,6,12,13]}
    direct={1:{3,4,9,10,16},2:{2,3,4,9},3:{3,4,9,11,12,14,15},4:{3,4,9,11},5:{3,4,6,9,11,12,13,14,15,17}}
    reach={1:{1,3,4,5,6,7,8,9,10,16},2:{1,2,3,4,5,6,7,8,9},
        3:{1,3,4,5,6,7,8,9,11,12,14,15},4:{1,3,4,5,6,7,8,9,11},
        5:{1,3,4,5,6,7,8,9,11,12,13,14,15,17}}
    assert {k:set(m['depends_on']) for k,m in members.items()}=={f'D{k}':{f'D{i}' for i in v} for k,v in local.items()}
    for c in data['claims']:
        n=int(c['claim_id'].split('/T')[-1]);assert set(c['depends_on'])=={f'D{i}' for i in direct[n]}
        visited=set();stack=list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in visited:visited.add(lid);stack.extend(members[lid]['depends_on'])
        assert visited=={f'D{i}' for i in reach[n]}
        assert visited=={x['members'][0]['local_id'] for x in data['interfaces'] if any(t['claim_id']==c['claim_id'] for t in x['related_theorems'])}
    b={k:m['statement_original'] for k,m in members.items()}
    assert r'\Omega=[0,2\pi]^2' in b['D1'] and 'opposite endpoints are identified' in b['D1']
    assert 'infinitely differentiable periodic functions' in b['D2']
    assert 'Lebesgue measure $dx$' in b['D3'] and 'weak' in b['D3'] and r'\mathcal X^2' in b['D3']
    assert b['D4'].count(r'\int_\Omega u=0')==2 and r'\sum_{i,j=1}^2' in b['D4']
    assert r'P:L^2(\Omega)^2\to H' in b['D5'] and 'all Schwartz distributions' in b['D5']
    assert r'A=-P\Delta' in b['D6'] and r'\mathcal D(A)\equiv H^2(\Omega)^2\cap V' in b['D6']
    assert r'\|Au\|_{L^2}\simeq\|u\|_{H^2}' in b['D6']
    assert r'B(u,v)=P[(u\cdot\nabla)v]' in b['D7'] and 'topological dual space' in b['D7']
    assert 'time-independent' in b['D8'] and '\nu(0,\\cdot)' in b['D8']
    assert r'\frac{du}{dt}+\nu Au+B(u,u)' in b['D9'] and '\nu(0)' in b['D9']
    assert "space $H$ (rather than just in $V'$" in b['D9']
    assert r'1\leq p<\infty' in b['D10'] and r'C([0,T],\mathcal X)' in b['D10']
    assert r'\delta_T\otimes\lambda_\Omega' in b['D11'] and r'u_\theta(t_i,X_i)' in b['D11']
    assert 'independently of the Gaussian noise' in b['D11'] and r'P_\theta^N' in b['D11']
    assert r"$\Pi'$ on $V\cap H^2(\Omega)^2$" in b['D12']
    assert r"\theta=\theta'/N^{1/(2\alpha+2)}" in b['D12'] and 'continuously imbedded' in b['D12']
    assert '(real parts of the)' in b['D13'] and r'(k_2,-k_1)e^{ik\cdot(\cdot)}' in b['D13']
    assert r'u_\theta(X_i,t_i)' in b['D14'] and 'non-Gaussian' in b['D14']
    assert r'\bar\theta_N=E^\Pi[\theta\mid Z^{(N)}]\in V' in b['D15'] and r'u_{\bar\theta_N}' in b['D15']
    assert r'\frac{\|u(0)-v(0)\|_V}{\|u(0)-v(0)\|_{L^2}}\leq c_P' in b['D16']
    assert 'ordered by increasing eigenvalues' in b['D17'] and r'E_J=\{e_j:j\leq J\}' in b['D17']
    assert r'J=J_N=O(\log\log N)' in b['D17'] and r'\mathcal H\cap E_{J_0}' in b['D17']
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert r'\sum_{i=1}^2u_i\frac{\partial v_j}{\partial x_i}' in a['A1']
    assert 'to be known' in a['A2'] and 'do not consider a SPDE model' in a['A3']
    assert r'$t\in(0,T_p],T_p\geq T$' in a['A4']
    assert r'\|_{L^2(\Omega)^2}^2' in a['A5'] and r'X_{N+1}\sim\lambda_\Omega' in a['A5']
    assert 'uniform control' in a['A6']
    assert r'\|u(0)-v(0)\|_V^2' in a['A7'] and r'\lambda_J\equiv c_P' in a['A7']
    assert r'\mathcal H=(V\cap H^\alpha(\Omega)^2' in a['A8']
    assert 'conclusions of Theorem 3 remain true' in a['A9'] and r'N^{-\alpha/(2\alpha+2)}' in a['A9']
    refs=ambient['source_claim_references']
    assert len(refs)==1 and refs[0]['from_claim_id']==PID+'/T5' and refs[0]['to_claim_id']==PID+'/T3'
    assert refs[0]['reference_kind']=='conclusion_inheritance'
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
        assert all(1<=e['page']<=18 for e in obj['evidence'])
    for x in data['interfaces']:
        m=x['members'][0];own=m['statement_original']+' '+m['local_label']
        selectors=m['highlight_symbols']+m['highlight_phrases'];assert any(s in own for s in selectors)
        linked=own+' '+' '.join(c['statement_original'] for c in data['claims'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems']))
        assert all(s in linked for s in selectors)
        for rel in x['related_theorems']:
            n=int(rel['claim_id'].split('/T')[-1]);assert rel['relation']==('direct' if int(m['local_id'][1:]) in direct[n] else 'indirect')
            path=rel['via_local_ids'];assert int(path[0][1:]) in direct[n] and path[-1]==m['local_id']
            assert all(right in members[left]['depends_on'] for left,right in zip(path,path[1:]))
            ex=x['theorem_explanations'][rel['claim_id']];assert ex['via_local_ids']==path and ex['text'].strip() and ex['evidence']
        for k in x['source_keywords']:assert any(k['source_text'] in s for s in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=5,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(a))
    assert counts==dict(theorems=5,interfaces=17,source_members=17,direct_theorem_uses=30,related_theorem_connections=54,unranked_auxiliary_passages=9)
    assert len(ambient['source_issues'])==22 and set(ambient['statement_resolution'])=={'shared','1','2','3','4','5'}
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for c in rebuilt['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Exactly five main-text Theorem environments on pages 6, 7, 10, 10 and 11. Complete original statements retain both stability branches, all norm comparisons, both posterior events and the posterior mean/trajectory error, minimax quantifiers, and the projected-prior conclusion reference. No proof or other result label is counted.',
        source_passages='Seventeen entries retain periodic domain and function spaces, divergence-free zero-mean fields, projector and Stokes operator, convection, physical and reduced PDEs, strong solutions, observation model, Gaussian prior, eigenfunctions, posterior, Bochner mean, inverse-Poincare condition and projected prior. Nine auxiliary passages preserve standing conventions and scope.',
        dependencies='Independent source-based graph reconstruction confirms 30 direct uses and 54 related connections. Theorem 5 explicitly inherits all Theorem 3 conclusions, including posterior mean and trajectory. The proof uses of Theorems 1 and 2 are not statement edges. Theorem 4 does not depend on a Gaussian prior or posterior.',
        branch_scope='Theorem 1B adds its inverse-Poincare ratio only for the exponential stability estimate. Theorem 3 permits T0=0; Theorem 4 requires T0>0. Single-time observation is an explicit Dirac-design exception. Theorem 5 changes the prior projection and convergence rate without an invented growth lower bound.',
        names_and_highlights='Names use source natural-language terms and archive adjacent naming context for Gaussian prior. Source kinds distinguish Condition 1, original defining prose, models and theorem excerpts. Every member has source-backed selectors and every related theorem has an explanation following its same-paper dependency path.',
        notation='Visual checks preserve the unsquared inverse-Poincare ratio versus its squared Remark 1 comparison, c-prime(c,t), PDE H versus RKHS calligraphic H, L2(Omega)^2 vector-space subscripts, likelihood argument reversal, T_P versus T_p, and the source set notation after span E_J.',
        limits='Twenty-two source issues retain zero-discrepancy conventions, fractional Sobolev and Bochner details, external solution theory, uniform-risk normalization, unspecified radius and projection growth, and eigenbasis conventions. No published-source substitution, external-reference body, appendix or proof certification is used.',
        reproduction='Six content artifacts reproduce byte for byte with retained per-paper scripts. Registered-source identity, main-text boundary, independent heading enumeration, complete inventory handoff, source-specific formulas, graph reconstruction, names, selectors, explanations and structural validation passed.')
    write('evidence/manual-findings.json',findings)
    images=[1,2,4,5,6,7,8,9,10,11,18]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.jpg',sha256=digest(ROOT/f'evidence/page-{n:02}.jpg'),**({'before_main_text_end':True} if n==18 else {})) for n in images]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
        source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=19,main_text_last_pdf_page=18,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent small-cap heading enumeration and visual comparison of all five complete original statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
        counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,review_limits=['Source census of registered arXiv v3; no published-version substitution.','External solution theory and unexpanded conventions remain unresolved within the main-text-only scope.','The census preserves source statements and ambiguities; it does not certify mathematical correctness or proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=19,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
