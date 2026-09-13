# -*- coding: utf-8 -*-
"""Check a frozen source-reviewed census; re-execution does not certify proofs."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import PID,REPO,ROOT,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={
 'theorem-inventory.json':'a255b3cca274041f929eb12feb8884d9c2dad1164c4ed2e4663c554483f0fa69',
 'source-passages.json':'8fd62fcb30f54d8ec596fbef7b43d9be9c13cbaa8cedd1bdc68bc2041d148a90',
 'interface-extraction.json':'82292a72ac482e8546641b1a5da634b4cc56e9c7a56de38419409c48cdef372e',
 'ambient-prerequisites.json':'140461fb953ad991b783fba38768bfde25da7af3bc93c032e347be3423bca923',
 'unfinalized-census.json':'b8c702972407dd36fd07e6c63afe708a21e47ad16719dcfc8c8c0cc5517a32cb',
 'ranked-interfaces.json':'30af59efef269484557bc2ece04064672dc89b66c588cbabb934de09d48530f7'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def main():
    assert len(EXPECTED)==6
    for n,sha in EXPECTED.items():assert digest(ROOT/n)==sha,('Changed reviewed content',n)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2109.12002v1.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2109.12002'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL=='https://arxiv.org/pdf/2109.12002v1'
    assert paper['pdf_pages']==registered['pdf_pages']==58 and paper['main_text_last_pdf_page']==30
    assert paper['main_text_boundary']['shared_page_with_appendix']
    assert ir['printed_label_check']==[[10,'1'],[17,'2']]
    assert len(inv['claims'])==len(data['claims'])==2
    for original,c in zip(inv['claims'],data['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Independent source reconstruction: neither extraction nor finalizer is imported.
    raw={1:[],2:[1],3:[1],4:[],5:[1,4],6:[],7:[3,6],8:[5,6],9:[3,6],10:[9,6,1],11:[6,3],12:[6],13:[11],14:[1],15:[8,6,12],16:[8,3,1],17:[11,15,14],18:[10,8,15,12,3],19:[11,13],20:[8,6,16],21:[1,19,20],22:[],23:[22],24:[22,23],25:[3,21,22],26:[14],27:[14],28:[1,3,6,7],29:[1,2,6,20,28],30:[1,2,6,20,28]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'1':ids([3,12,13,15,16,17,18]),'2':ids([1,3,19,21,22,23,24,25,26,27,28,29,30])}
    reach={'1':ids([1,3,4,5,6,8,9,10,11,12,13,14,15,16,17,18]),'2':ids([1,2,3,4,5,6,7,8,11,13,14,16,19,20,21,22,23,24,25,26,27,28,29,30])}
    assert {k:set(m['depends_on']) for k,m in members.items()}==local
    def closure(seeds):
        seen=set();stack=list(seeds)
        while stack:
            lid=stack.pop()
            if lid not in seen:seen.add(lid);stack.extend(local[lid])
        return seen
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n] and closure(direct[n])==reach[n]
        actual={x['interface_id'].split('/')[-1] for x in data['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert actual==reach[n]
    branches={'T1/a':ids([3,12,15,17,18]),'T1/b':direct['1'],'T2/a':ids([1,3,19,21,22,24,25,26,28,29]),'T2/b':ids([1,3,19,21,22,23,24,25,27,28,30])}
    assert branches['T1/a']|branches['T1/b']==direct['1'] and branches['T2/a']|branches['T2/b']==direct['2']
    assert not ids([13,16]) & closure(branches['T1/a'])
    assert not ids([26,29]) & closure(branches['T2/b']) and not ids([27,30]) & closure(branches['T2/a'])
    assert not ids([9,10,15,17,18]) & reach['2'] and 'D2' not in reach['1'] and local['D22']==set()
    b={k:m['statement_original'] for k,m in members.items()}
    snippets={
      1:[r'\mathscr I(\mathcal P,r,\gamma)',r'\gamma\in(0,1)',r'\mathcal P:\mathcal X\times\mathcal X\to\mathbb R'],
      2:[r'\sum_{h=0}^\infty\gamma^h r(X_h)',r'X_0=x','boundedness of reward'],
      3:['i.i.d. sample pairs','any stationary distribution',r'x_i\sim\mu',r"x'_i\sim\mathcal P(\cdot\mid x_i)"],
      4:['convex','closed in',r'\arg\min_{g\in\mathbb G}\|g-f\|_\mu'],
      5:[r'\theta^*=\Pi\big(\mathcal T(\theta^*)\big)',r'\mathcal T(\theta^*)(x):=r(x)+\gamma\,\mathbb E_{X\mid x}'],
      6:[r'\langle\mathcal K(\cdot,x),f\rangle_{\mathbb H}=f(x)',r'\Phi_x=\mathcal K(\cdot,x)'],
      7:[r'\Sigma_{\mathrm{cov}}',r"\Phi_X\otimes\Phi_{X'}",r'\mathbb E_{X\sim\mu}[g(X)f(X)]'],
      8:['projected fixed point (6)',r'\mathbb G=\mathbb H'],
      9:[r'\frac1n\sum_{i=1}^n\Phi_{x_i}\otimes\Phi_{x_i}',r"\Phi_{x_i}\otimes\Phi_{x'_i}"],
      10:[r'(\widehat\Sigma_{\mathrm{cov}}+\lambda_n\mathcal I)r',r'\gamma\widehat\Sigma_{\mathrm{cr}}\widehat\theta',r'\lambda_n>0'],
      11:['non-negative sequence','orthonormal',r'\sum_{j=1}^\infty\mu_j\phi_j(x)\phi_j(z)'],
      12:[r'\sup_{x\in\mathcal X}\sqrt{\mathcal K(x,x)}\leq b'],
      13:[r'\max_{j\geq1}\|\phi_j\|_\infty\leq\kappa','fast rate'],
      14:[r'H:=\frac1{1-\gamma}'],
      15:[r'\|\theta^*-r\|_{\mathbb H}',r'\frac{2\|\theta^*\|_\infty}{b}'],
      16:[r"(\theta^*(X)-r(X)-\gamma\theta^*(X'))^2",'stationary distribution'],
      17:[r'\frac{\sqrt n\,R}{H(\gamma)\,\zeta}',r'\zeta>0','unique smallest positive solution'],
      18:[r'\|\widehat\theta-\theta^*\|_\mu^2',r'\frac{\lambda_n}{1-\gamma}',r'\frac{c_2n\delta^2(1-\gamma)^2}{b^2}','universal constants'],
      19:[r'\kappa=2',r'\sum_{j=1}^\infty\mu_j\leq\frac{b^2}{4}'],
      20:[r'\|\theta^*-r\|_{\mathbb H}',r'\sigma(\theta^*)\leq\bar\sigma'],
      21:['bound (29b)','conditions (29a)'],
      22:['smallest positive solution',r'\frac{\bar R(1-\gamma)}{2\bar\sigma}'],
      23:[r'\max\{j\mid\mu_j\geq\delta_n^2\}'],
      24:[r'\left\{\frac{2\bar\sigma}{\bar R(1-\gamma)}\right\}^2d_n\geq c\,n\,\delta_n^2'],
      25:[r'\inf_{\widehat\theta}\sup_{\mathscr I\in\mathfrak M',r'\mathbb P_{\mathscr I}',r'\geq c_1\bar R^2\delta_n^2','universal constants'],
      26:[r'\frac1{6(1-\gamma)}',r'\frac\gamma{\sqrt{\mu_1}}',r'\frac{1+\gamma}{5(1-\gamma)}'],
      27:[r'\frac1{2\sqrt{\mu_1}}',r'\frac2{\gamma b}',r'\left(\frac18,1\right]'],
      28:['Lebesgue measure',r'L^2(\mu(\mathcal P))','an abbreviation',r'\Sigma_{\mathrm{cov}}(\mathcal P)'],
      29:[r'\|r_A\|_\infty\leq1',r'\theta^*\in\mathbb H_A',r'\mu_j(\mathcal P)=\mu_j\text{ for }j=1,2,\ldots'],
      30:[r'\gamma\|\theta^*\|_{\mu(\mathcal P)}\leq1',r'\mu_j(\mathcal P)\leq\mu_j\text{ for any }j\geq2']}
    # X-prime in the Bellman operator is a conditional successor, not an independent draw.
    snippets[5][-1]=r"\mathcal T(\theta^*)(x):=r(x)+\gamma\,\mathbb E_{X'\mid x}"
    for n,parts in snippets.items():
        for s in parts:assert s in b['D'+str(n)],(n,s)
    assert 'V^*' not in b['D18'] and 'r_A' not in b['D30']
    for n in [12,13]:assert members['D'+str(n)]['source_kind']=='assumption'
    for n in [18,25,28]:assert members['D'+str(n)]['source_kind']=='source_passage'
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert len(a)==12 and len(ambient['source_issues'])==18
    assert 'stationarity' in a['A3'] and r'\Pi(r)' in a['A5']
    assert 'Approximation error' in a['A6'] and 'any measurable function' in a['A7']
    assert 'optimal value function' in a['A8'] and 'regularity condition (31)' in a['A9']
    assert 'pre-specified constants' in a['A10'] and 'not the eigenvalues' in a['A10']
    assert 'no longer independent' in a['A12']
    assert set(ambient['statement_local_bindings'])=={'T1','T2'}
    assert len(ambient['source_claim_references'])==2
    def check_evidence(es):
        assert es
        for e in es:
            assert 1<=e['page']<=30
            if e['page']==30:assert e.get('before_main_text_end') is True
    for obj in list(members.values())+data['claims']+ambient['unranked_auxiliary_passages']:
        s=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',s)
        assert not any(ord(c)<32 and c!='\n' for c in s)
        assert s.count('$')%2==0
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        check_evidence(obj['evidence'])
    for x in data['interfaces']:
        assert len(x['members'])==1
        m=x['members'][0];lid=m['local_id']
        own=m['statement_original']+' '+m['local_label'];selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors)
        linked=own+' '+' '.join(c['statement_original'] for c in data['claims'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems']))
        assert all(s in linked for s in selectors)
        expected_uses={PID+'/T'+n for n,seeds in direct.items() if lid in seeds}
        assert {u['claim_id'] for u in x['central_claim_uses']}==expected_uses
        assert set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
        for rel in x['related_theorems']:
            n=rel['claim_id'].split('/T')[-1]
            assert rel['relation']==('direct' if lid in direct[n] else 'indirect')
            path=rel['via_local_ids'];assert path[0] in direct[n] and path[-1]==lid
            assert all(right in local[left] for left,right in zip(path,path[1:]))
            ex=x['theorem_explanations'][rel['claim_id']]
            assert ex['via_local_ids']==path and ex['text'].strip()
            check_evidence(ex['evidence'])
            assert 'This theorem directly uses the API.' not in ex['text']
        for kw in x['source_keywords']:
            if 'context_id' in kw:
                ctx=next(c for c in m['naming_context'] if c['context_id']==kw['context_id'])
                assert kw['source_text'] in ctx['text'];check_evidence(ctx['evidence'])
            else:assert kw['source_text'] in m['statement_original']
    counts=dict(theorems=2,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(a))
    assert counts==dict(theorems=2,interfaces=30,source_members=30,direct_theorem_uses=20,related_theorem_connections=40,unranked_auxiliary_passages=12)
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for c in rebuilt['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Two complete bold Theorem environments, 1 and 2, on pages 10-11 and 17-18. Font-level enumeration covers all 30 main-text pages; the Theorem 2 citation on page 19 is not an environment. Appendix A starts on shared page 30; all evidence there is clipped at y=295 above its heading.',
      source_passages='Thirty separate source entries preserve the MRP, iid stationary-pair experiment, RKHS and projected target, operator estimates, upper critical inequality and complete probability bound, lower validity conditions, radius, regularity, regimes and full family specifications. Twelve auxiliary passages retain the known-reward convention, stationarity footnote, reward projection alternative, approximation error, estimator scope and lower-bound clarifications.',
      dependencies='Independent source reconstruction gives 20 direct uses and 40 related connections. The upper target is the projected fixed point; its statement does not acquire the true-value definition merely from the error decomposition. The lower result ranges over all measurable estimators and does not acquire the empirical LSTD estimator or the upper critical inequality.',
      branch_scope='The eigenfunction bound and residual noise enter the fast upper branch, not its slow branch. Regimes A and B retain separate parameter ranges and family definitions. Theorem 2 also requires regularity (31), explicitly stated in the adjacent commentary. Section 4.2.1 provides the full statement meaning, while Walsh constructions, packings and Fano bounds remain proof-only.',
      lower_spectrum='The critical radius (30) uses prescribed mu_j. Family A equates every actual eigenvalue with that sequence. Family B only bounds actual eigenvalues for j>=2, without imposing equality or adding a j=1 condition. Its loss uses the stationary law mu(P), although mu elsewhere in the construction denotes Lebesgue measure.',
      notation='Visual comparison retains the squared-root diagonal kernel bound, uncentered Bellman-residual second moment, regularization on both sides of the estimator equation, reversed parameter-pair order in Theorem 2(b), both sample-size conditions, largest-index statistical dimension and all eigengap factors. PDF typefaces distinguish script I for instances, calligraphic I for the identity and blackboard-bold H for the RKHS.',
      names_and_highlights='All thirty entries retain source-extracted natural-language names, exact phrases or math selectors, original source kinds and same-paper explanations for every related theorem. Structural selector checks supplement the retained source comparison; they do not infer mathematical equivalence.',
      reproduction='Six saved content artifacts were regenerated byte-for-byte by the retained paper scripts. The frozen content hashes and independent source-specific assertions preserve the reviewed state. Re-executing the scripts alone is not a new source review or a proof check.')
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,branch_direct_dependencies={k:sorted(v,key=lambda s:int(s[1:])) for k,v in branches.items()},appendix_material_used=False))
    evidence=[dict(path=str(p.relative_to(ROOT)),page=int(p.stem.split('-')[-1]),**({'before_main_text_end':True} if p.stem=='page-30' else {})) for p in sorted((ROOT/'evidence').glob('page-*.jpg'))]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=58,main_text_last_pdf_page=30,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-font enumeration and visual comparison of both full original theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv v1 source; no assumption of equivalence to the published article.','Source ambiguities are preserved separately, not silently repaired or resolved through appendix-body inspection.','Census validation does not certify mathematical correctness or proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=58,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
