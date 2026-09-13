"""Record completed manual source review and independently check the frozen artifacts.

Running this script is not a new mathematical review or proof certification.
The source's unresolved supplemental algorithm and notation are preserved.
"""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import PID,REPO,ROOT,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': 'bb179114b7bd4773c56a3597c032027326b02bcf2d586bba60fc77375b8eeb12', 'source-passages.json': '35e498ca9e3316a4b4b32631a627d0d922b2330848df68a86dadc374052761f1', 'interface-extraction.json': '5012041e975864ffaab2e53a0428b9d8edd726d9763fc771a6bbcc3498949467', 'ambient-prerequisites.json': 'd32f5531b6e390a30b3ef53ee7642e0470e265fb38b6546d4df47fd7f28fd6b8', 'unfinalized-census.json': '289e706c41d37e51160450b2b61e1765e306c0f7a8af1823fc52a866ddaa4afa', 'ranked-interfaces.json': 'f96f346fb60f4799ecf92cd488523cf675c1c499f2b3eafe12486999487da4b5'}
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
    assert registered['version']=='2306.16406v4.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2306.16406'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    assert paper['source_url']==URL=='https://arxiv.org/pdf/2306.16406v4'
    assert paper['pdf_pages']==registered['pdf_pages']==96 and paper['main_text_last_pdf_page']==33
    ir=json.loads((ROOT/'inventory-review.json').read_text());assert ir['status']=='complete' and ir['source_checked']
    assert ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    headings=ir['printed_label_check'];assert headings==[[17,1],[26,2]]
    assert len(inv['claims'])==len(data['claims'])==2
    for original,c in zip(inv['claims'],data['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    assert len(data['claims'][0]['source_footnotes'])==1
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Independently reconstructed from source inputs, identities, conditions and recipes.
    local={1:[],2:[],3:[2],4:[2,3],5:[4],6:[1],7:[2,3],8:[3],9:[8,7,5],10:[2,3],
        11:[3,7,8,10],12:[3,8,9,10],13:[11,8],14:[12,8],15:[13,14,2,26],16:[2],
        17:[1,3,5,8,9,10,12],18:[3,10],19:[2,7,8,10,18],20:[1,8,9,10,18],
        21:[8,11,12,19,20],22:[21],23:[1],24:[1],25:[1,23],26:[]}
    direct={1:{1,2,3,4,7,8,9,10,11,13,14,15,16,17,18,19,20,21,22,26},2:{1,6,23,24,25,26}}
    reach={1:{1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,26},2:{1,6,23,24,25,26}}
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
    assert r'r_*:=R(P_*):=\mathbb E_{P_*}[\ell(Z)\mid A=0]' in b['D1']
    assert 'not to be observed' in b['D2'] and r'\mathbb E_Q[\ell(Z)]' in b['D2']
    assert r'K\geq1' in b['D3'] and r'\bar Z_0:=\emptyset' in b['D3']
    assert 'known nonempty subset' in b['D4'] and 'dominated' in b['D4'] and '$Q$-almost every' in b['D4']
    assert r"0\in\mathcal S'_k" in b['D5'] and r'X\perp\!\!\!\perp A' in b['D6']
    assert 'Radon-Nikodym derivative' in b['D7'] and 'relative to' in b['D7']
    assert r'\Pi_*^{0,a}=P_*(A=a)' in b['D8'] and r'\pi_*^0=\rho_*' in b['D8']
    assert r'\sum_{a\in\mathcal S_k}\Pi_*^{k-1,a}' in b['D9'] and r'\pi_*^0(1+\theta_*^{k-1})' in b['D9']
    assert r'\ell_*^K:=\ell' in b['D10'] and 'any value outside' in b['D10']
    assert r"A\in\mathcal S'_{k+1}" in b['D10']
    assert r'\sum_{k=2}^K' in b['D11'] and r'\lambda^{k-1}(\bar z_{k-1})' in b['D11']
    assert r'\ell^1(z_1)' in b['D11'] and r'\pi^0(1+\theta^0)' in b['D12']
    assert r"\frac{\mathbb1(a\in\mathcal S'_1)}{\sum_{b\in\mathcal S'_1}\pi^b}r" in b['D13']
    assert r'\pi^0(1+\theta^0)' in b['D14'] and r'\sigma_{*,\mathrm{GSC}}^2' in b['D15']
    assert 'Supplemental Material' in b['D16'] and not members['D16']['unresolved_reference']['body_inspected']
    assert r'\widehat\pi_v^a:=|I_v|^{-1}\sum_{i\in I_v}' in b['D17']
    assert r'([n]\setminus I_v)\cap J_{k+1}' in b['D17'] and '(11)' in b['D17']
    assert all(f'{n}:' in b['D17'] for n in range(1,10))
    assert r"\widehat\ell_v^k(\bar Z_k)\mid\bar Z_{k-1}=\bar z_{k-1},A\in\mathcal S'_k" in b['D18']
    assert r'\mathbb E_Q[h_v^{k-1}' in b['D19'] and '(12)' in b['D19']
    assert r'\widehat\pi_v^0(1+\widehat\theta_v^{k-1}' in b['D20'] and r'\mid A=0' in b['D20'] and '(13)' in b['D20']
    assert all(f'({n})' in b['D21'] for n in [14,15,16])
    assert r'o_p(n^{-1/2})' in b['D21'] and r'O_p(1)' in b['D22']
    assert r'\mathcal E_*:x\mapsto' in b['D23'] and r'X=x,A=0' in b['D23']
    assert r'\frac{1-a}{\rho}\{\ell(x,y)-\mathcal E(x)\}+\mathcal E(x)-r' in b['D24']
    assert r'\widehat\rho^v:=|I_v|^{-1}\sum_{i\in I_v}' in b['D25'] and r'\widehat{\mathcal E}^{-v}' in b['D25']
    assert all(f'{n}:' in b['D25'] for n in range(1,6))
    assert r'\mathrm{IF}\in L_0^2(P_*)' in b['D26'] and 'smallest asymptotic variance' in b['D26']
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert r'\rho_*:=P_*(A=0)\in(0,1)' in a['A1'] and r'\operatorname{var}_{P_*}' in a['A2']
    assert r'0/0=0' in a['A3'] and 'empty index set' in a['A4']
    assert r'f(x)^pP(dx)' in a['A5'] and r'P^{n,v}' in a['A5']
    assert r"\mathcal S'_k\setminus\{0\}" in a['A6'] and r'\mathcal A=\{0,1\}' in a['A7']
    assert r'\theta^{k-1}(\bar z_{k-1})=\infty' in a['A8'] and 'to be zero' in a['A8']
    assert 'conditional odds' in a['A9'] and 'fixed number $V$' in a['A10']
    assert 'same theoretical properties' in a['A11'] and r'$P^0$' in a['A12']
    assert 'these estimators are treated as fixed' in a['A13'] and r'\theta^0:=' in a['A14']
    assert 'does not exist' in a['A15'] and 'one version' in a['A16']
    assert 'different influence function' in a['A17'] and 'inconsistently' in a['A17']
    originals=list(members.values())+data['claims']+ambient['unranked_auxiliary_passages']+data['claims'][0]['source_footnotes']
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
        assert all(1<=e['page']<=33 for e in obj['evidence'])
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
    counts=dict(theorems=2,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(a))
    assert counts==dict(theorems=2,interfaces=26,source_members=26,direct_theorem_uses=26,related_theorem_connections=28,unranked_auxiliary_passages=17)
    assert len(ambient['source_issues'])==25 and set(ambient['statement_resolution'])=={'shared','1','2'}
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for c in rebuilt['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Independent enumeration found exactly two main-text Theorems, beginning on pages 17 and 26. Complete continued statements, all (18)–(22)/(25)–(26) formulas and branches, and footnote 6 are preserved. Propositions, Corollaries, Lemmas and supplement references are excluded.',
        source_passages='Twenty-six entries preserve both target-risk setups, sequential prefixes and conditions, nuisance functions, pseudo-losses, influence functions and variance, the two main-text algorithms, oracle/product-bias terms, ST.1/ST.2 and RAL terminology. Seventeen auxiliary passages preserve standing conventions, source footnotes, binary populations, version-choice qualifications and allowed alternatives.',
        dependencies='Independent numeric reconstruction verifies 26 direct uses and 28 related connections. The general/dagger formulas remain distinguishable. Theorem 2 reaches only its observed-target risk, DS.1, conditional risk, D_Xcon, specialized algorithm and RAL terminology; it does not inherit ST.1/ST.2 or the general algorithm.',
        branch_scope='DS.0 is additional in the final Theorem 1 clause, making Delta zero. Earlier branches concern r-hat minus Delta. References to DS.0-dagger in the odds identity and algorithm title do not impose it globally. Theorem 2 permits a common inconsistent nuisance limit, retaining its additional leading term before the separate efficient specialization.',
        names_and_highlights='All names use literal source natural-language terms or condition labels. Separate original source headings distinguish conditions, source passages and algorithms. Every member has meaningful source selectors and every related theorem has a same-paper explanation with its dependency path.',
        notation='Visual checks retain pi_v^a without a hat in (19), different t-threshold and Gaussian-tail rates, rho-hat^v versus rho-hat^{-v} in Theorem 2, the two product-bias formulas across the page-14/15 algorithm interruption, in-fold proportions, out-of-fold regressions, the 0/0 and infinite-odds conventions, and the printed P^0 and general Lp formula.',
        limits='The general Algorithm 1 is explicitly outside the main text. Its body and omitted dependencies remain unresolved, without reconstruction from the dagger or specialized algorithm. Regularity definitions deferred to supplementary exposition also remain unresolved. Twenty-five source issues document scope and notation; source review is not proof certification.',
        reproduction='All six content artifacts reproduce byte for byte using seven retained scripts. PDF identity, independent heading enumeration, original-claim/footnote handoff, source-specific formulas, local and related graphs, keywords, selectors, TeX fragments and structural validators passed.')
    write('evidence/manual-findings.json',findings)
    images=['01.png','07.jpg','08.jpg','09.jpg','10.png','12.png','13.png','14.jpg','15.jpg','16.jpg','17.png','18.png','21.jpg','25.jpg','26.jpg','27.png','33.png']
    evidence=[dict(page=int(n[:2]),path=f'evidence/page-{n}',sha256=digest(ROOT/f'evidence/page-{n}'),**({'before_main_text_end':True} if n.startswith('33') else {})) for n in images]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
        source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=96,main_text_last_pdf_page=33,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent actual bold-heading enumeration and visual comparison of both complete multi-page statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
        counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,review_limits=['Source census of registered arXiv v4; no published-version substitution.','Supplementary algorithm and regularity details remain unresolved within the main-text-only scope.','The census preserves source statements and ambiguities; it does not certify mathematical correctness or proofs.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=96,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
