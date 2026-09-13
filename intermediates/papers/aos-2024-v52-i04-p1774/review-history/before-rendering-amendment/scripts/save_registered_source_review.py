"""Record completed manual source comparison and independently check its artifacts.

Frozen hashes identify reviewed content. Running this script does not conduct a
new mathematical review or certify the paper's proofs and printed equations.
"""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import PID,REPO,ROOT,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '4e84e039b6f8f6c7f0a7857f5c659e943541f53f180202ed2a005b49c4bc4d76', 'source-passages.json': '55e42c053b0f34e68f5faa572c6a68040f72bc4ca085b366549326bfd20f0ae9', 'interface-extraction.json': '32112aaf9a2ce6c808dcefb10077a6469174e6d8a336483d0e69c065814c4bc3', 'ambient-prerequisites.json': '428f6c0fd58e705d2a702a3816857f0d577c757b6adf19c2b43ff04f7de426ff', 'unfinalized-census.json': 'a00785bbdf427e568c1e943647997b805a1635b707f125b6d2cc935fe986e274', 'ranked-interfaces.json': '9ff002e6fc242a998a26eed30d2ab699d55c94a62383a4750f08a1cb9f854deb'}
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
    assert registered['version']=='2301.01766v1.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2301.01766'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    assert paper['source_url']==URL=='https://arxiv.org/pdf/2301.01766v1'
    assert paper['pdf_pages']==registered['pdf_pages']==51 and paper['main_text_last_pdf_page']==15
    ir=json.loads((ROOT/'inventory-review.json').read_text());assert ir['status']=='complete' and ir['source_checked']
    assert ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    headings=ir['printed_label_check'];assert headings==[[3,1],[6,2],[6,3],[8,4],[8,5],[9,6]]
    assert len(inv['claims'])==len(data['claims'])==6
    for original,c in zip(inv['claims'],data['claims']):assert all(c[k]==v for k,v in original.items())
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Reconstructed independently from the source formulas and theorem references.
    local={1:[4],2:[1],3:[2,4],4:[],5:[4],6:[4],7:[4],8:[4],9:[2,1,4],10:[4,6,9],
           11:[4,9,8,15,18],12:[4,9,8,15,16],13:[4,9],14:[4,9,8,15,17],15:[4,9],16:[4,8],17:[4,8],18:[4,8]}
    direct={1:{3,4,9},2:{3,4,5,7,10},3:{1,8,11},4:{3,4,5,7,13},5:{1,8,12},6:{1,8,14}}
    reach={1:{1,2,3,4,9},2:{1,2,3,4,5,6,7,9,10},3:{1,2,4,8,9,11,15,18},
           4:{1,2,3,4,5,7,9,13},5:{1,2,4,8,9,12,15,16},6:{1,2,4,8,9,14,15,17}}
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
    assert r'\phi(x)=(2\pi)^{-d/2}\exp(-\|x\|_2^2/2)' in b['D1']
    assert r'\ell_N(\rho)=-\frac1N\sum_{i=1}^N\log[(\rho*\phi)(X_i)]' in b['D2']
    assert r'\operatorname*{argmin}_{\rho\in\mathcal P(\mathbb R^d)}' in b['D3']
    assert 'finite second moments' in b['D4'] and 'Lebesgue measure' in b['D4']
    assert 'smallest closed set' in b['D5'] and r'T_\#\rho(A)=\rho(T^{-1}(A))' in b['D6']
    assert 'every bounded continuous function' in b['D7']
    assert r'\varphi\in C_c^\infty(\mathbb R^d)' in b['D8'] and r'\frac{d}{dt}' in b['D8']
    assert r'\frac{\phi(x-X_i)}{(\rho*\phi)(X_i)}' in b['D9']
    assert r'\frac{d\widetilde\rho_n}{d\rho_n}=1-\eta[1+\delta\ell_N(\rho_n)]' in b['D10']
    assert r'\rho_{n+1}=[\operatorname{id}-\eta\nabla\delta\ell_N(\widetilde\rho_n)]_\#\widetilde\rho_n' in b['D10']
    assert r'-[1+\delta\ell_N(\rho_t)]\rho_t+\operatorname{div}' in b['D11']
    assert r'\mathcal P_2(\mathbb R^d)' in b['D11'] and '(3.6)' in b['D11']
    assert r'\partial_t\rho_t=-[1+\delta\ell_N(\rho_t)]\rho_t' in b['D12']
    assert r'1-\gamma[1+\delta\ell_N(\rho_n)]' in b['D13']
    assert r'\partial_t\rho_t=\operatorname{div}(\rho_t\nabla\delta\ell_N(\rho_t))' in b['D14']
    assert r'\lim_{\eta\to0}' in b['D15'] and r'\frac1{2\eta}d^2(\rho,\rho_t)' in b['D15']
    assert r'\alpha_t-\int\alpha_td\rho_t' in b['D16'] and r'\alpha_t-\int\alpha_td\rho_t' in b['D18']
    assert r'\inf_{\pi\in\Pi(\rho_0,\rho_1)}' in b['D17'] and r'\int\|x-y\|_2^2\pi(dx,dy)' in b['D17']
    assert r'\|v_t\|^2+' in b['D18']
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert r'\Delta^{m-1}' in a['A1'] and 'Dirac mass' in a['A2']
    assert r'\mu^{(1)},\ldots,\mu^{(m)}\in\mathbb R^d' in a['A4']
    assert r'\rho_0=\frac1m\sum_{l=1}^m\delta_{\mu_0^{(l)}}' in a['A5']
    assert r'=4\int' in a['A6'] and 'Hellinger distance' in a['A6']
    assert 'do not cover Algorithm 1' in a['A7'] and r'\int\delta\ell_N(\rho)d\rho=-1' in a['A8']
    assert 'any minimizer' in a['A9']
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
        assert all(1<=e['page']<=15 for e in obj['evidence'])
        assert all(e.get('before_main_text_end') for e in obj['evidence'] if e['page']==15)
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
    counts=dict(theorems=6,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(a))
    assert counts==dict(theorems=6,interfaces=18,source_members=18,direct_theorem_uses=22,related_theorem_connections=46,unranked_auxiliary_passages=11)
    assert len(ambient['source_issues'])==25 and set(ambient['statement_resolution'])=={'shared',*[str(i) for i in range(1,7)]}
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for c in rebuilt['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Six complete main-text Theorems were independently enumerated and visually compared. Both Theorem 1 parts, weak-limit assumptions in Theorems 2/4, all particle equations and initializations, and the page-7 ending of Theorem 3 are preserved. Appendix theorem references and unnumbered claims are excluded.',
        source_passages='Eighteen original entries preserve Gaussian convolution, likelihood/NPMLE, measure classes and notation, first variation, two explicit measure iterations, three likelihood flow PDEs, the generic metric construction and the three source distances. Eleven auxiliary passages retain simplex/Dirac notation, fixed/equal-weight initializations and source scope statements.',
        dependencies='Independent reconstruction verifies 22 direct uses and 46 related connections. The discrete convergence theorems reach their explicit measure updates, not finite-particle algorithms or continuous-time flows. The particle theorems reach their named flow PDEs, distributional-solution convention and underlying geometries. WFR action does not depend on either component distance merely because the source calls it composite.',
        names_and_highlights='Every interface has literal natural-language source keywords, faithful source headings, original statements and source-backed selectors. Adjacent naming context is archived for the two flow names not spelled out in their defining sentences. Every related theorem has an explanation tied to its same-paper path.',
        notation='Visual comparison preserves omega_t^(j) inside l-indexed sums in Theorems 3/6, omega_t^(l) in Theorem 5, eta versus gamma in Theorem 4/(3.12), the intermediate measure in both stages of (3.7), and the centered reaction fields in the source distance formulas. No original formula was silently repaired.',
        limits='Twenty-five source issues document undefined or unexplained weights, time and measurability conventions, geometric admissibility, the claimed Fisher-Rao/Hellinger identity and version-specific statements. The census verifies source fidelity and dependency interpretation, not correctness of the printed ODEs or proofs. Appendix bodies were not read.',
        reproduction='All six content artifacts reproduce byte for byte from seven retained per-paper scripts. Registered PDF identity, independent heading enumeration, source-specific formula checks, original-statement handoff, graph reconstruction, keywords, selectors, mathematical fragments and structural validators passed.')
    write('evidence/manual-findings.json',findings)
    pages=[1,2,3,4,5,6,7,8,9,15]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png'),**({'before_main_text_end':True} if n==15 else {})) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
        source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=51,main_text_last_pdf_page=15,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent source heading enumeration and visual comparison of all six complete original statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
        counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,review_limits=['Source census of registered arXiv v1; no published-version substitution.','Proofs and printed ODE consistency are not certified; source ambiguities remain explicit.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=51,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
