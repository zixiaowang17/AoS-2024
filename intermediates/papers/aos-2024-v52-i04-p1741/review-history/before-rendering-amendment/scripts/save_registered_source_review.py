"""Record the manual source comparison and independently verify reviewed artifacts.

Frozen hashes identify the reviewed content. Executing this script is not a
new mathematical review, and does not certify any of the paper's proofs.
"""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': 'b9936be921578f5e6b5597a6fea0065ebac237a120fc17b6a30a237d415d2460', 'source-passages.json': 'f1594035906475fc159d275ffbc8f55938129fdc98d5c99f10dfccec1d7462c3', 'interface-extraction.json': '2efe4a7a4993dc3c7190383da3764ac569cb58074002f1dbc4539403e822379f', 'ambient-prerequisites.json': '3d49d0fd9e39ffb050a817a2308aeed8c9f2a122cb87413a204c60096107323b', 'unfinalized-census.json': '0ad4d1fb688421c7b09e7dc007dad43dd2d30e8ea163eba0ec34413bd0a90f83', 'ranked-interfaces.json': '78dcbc6a7c9681128a51096b183b61a516a62f198a619240aaf8876395c21292'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    # This separate inventory review enumerates source headings and checks the
    # PDF/version, clipped boundary, all theorem branches and original statements.
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(p for p in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if p['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    assert paper['source_url']==registered['source_url']==URL and paper['version']==registered['version']
    assert paper['pdf_pages']==registered['pdf_pages']==33
    ir=json.loads((ROOT/'inventory-review.json').read_text());assert ir['status']=='complete' and ir['source_checked']
    assert ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    headings=ir['printed_label_check'];assert headings==[[8,1],[11,2],[16,3],[16,4],[17,5],[18,6],[18,7]]
    assert len(inv['claims'])==len(data['claims'])==7
    for original,c in zip(inv['claims'],data['claims']):assert all(c[k]==v for k,v in original.items())
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Independently reconstructed from source statements and definition inputs.
    local={1:[],2:[],3:[],4:[3],5:[2,3,4],6:[3,4],7:[3],8:[2,4],9:[],10:[5,9,4,6,8],
           11:[2],12:[8,7,4,11],13:[10,9,12,6,2],14:[12,6],15:[14,9,4],16:[1,9,4],
           17:[1],18:[],19:[1,16],20:[],21:[],22:[1],23:[4],24:[23,9,16,2],
           25:[7,4,11],26:[11],27:[26,25,16,11],28:[10,13,27],29:[11],30:[29,25],
           31:[30,27],32:[6,1],33:[11],34:[29,33],35:[27,33]}
    direct={1:{4,9,10,15},2:{1,9,10,16,17,18,19,20,21,22,24},
            3:{1,9,16,17,18,19,20,21,22,24,28,30,31},
            4:{1,16,17,18,19,20,21,22,24,27,28,30,31,32},
            5:{1,16,17,18,19,20,21,22,24,27,28,30,31,32},
            6:{17,18,20,21,26,27,29,30,31,33,34,35},7:{33,34}}
    reach={1:{2,3,4,5,6,7,8,9,10,11,12,14,15},
           2:{1,2,3,4,5,6,8,9,10,16,17,18,19,20,21,22,23,24},
           3:set(range(1,32))-{14,15},4:set(range(1,33))-{14,15},5:set(range(1,33))-{14,15},
           6:{1,2,3,4,7,9,11,16,17,18,20,21,25,26,27,29,30,31,33,34,35},7:{2,11,29,33,34}}
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
    assert r'\int_0^1 f_j(x_j)p_j(x_j)dx_j=0' in b['D1']
    assert r'c_h(u)' in b['D3'] and r'\int_0^1K_h(x,u)dx=1' in b['D3']
    assert r'\widehat\Pi_{jj}\equiv0' in b['D12'] and r'\delta(u_j-x_j)' in b['D12']
    assert r'-\widehat p_k(x_k)' in b['D25'] and r'-\widehat p_k(x_k)' not in b['D12']
    assert 'redefined' in b['D25'] and r'\|v_j\|_{\widehat p}\leq1' in b['D13']
    assert r'f_k^{(r,j)}=f_k^{(r,j-1)}' in b['D15']
    assert r'|\upsilon|\leq1/\alpha' in b['D22'] and r'6\sqrt{c_{r,U}/c_{r,L}}' in b['D24']
    assert r'\sum_{k\in S}\|\eta_k\|_{p^h}^2\ne0' in b['D24']
    assert r'\|\Xi_j\|_{1,\max}' in b['D26'] and r'\gamma^{-1}=|S|\sqrt{nh}' in b['D27']
    assert r'\nu(\widehat{\mathbf f})' in b['D28'] and 'eigenvalues in $[0,1]$' in b['D29']
    assert "\\widetilde\\delta_{jk}''(u_j)^2du_j" in b['D31']
    assert r'\gamma^{8/3}' in b['D31'] and r'\frac{\partial^2}{\partial x_k^2}' in b['D33']
    assert r'\widehat{\mathbf m}^{A}' in b['D32'] and r'\widehat{\mathbf m}^{B}' in b['D32']
    assert r'q\geq0' in b['D34'] and r'\Theta_{kj}(\mathbf x,\mathbf u)' in b['D34']
    assert 'additional constraint' in b['D35'] and "\\Xi_{jk}''(u_j,x_k)^2dx_k" in b['D35']
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert r'\frac{1-\alpha}{2\sqrt{2(1+\alpha)}}' in a['A13']
    assert r'\sqrt{10}c_K\sigma\sqrt{c_{p,U}c_{h,U}}' in a['A9']
    assert 'independent of $n$' in a['A15'] and 'with probability tending to one' in a['A8']
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
        assert all(1<=e['page']<=25 for e in obj['evidence'])
        assert all(e.get('before_main_text_end') for e in obj['evidence'] if e['page']==25)
    for x in data['interfaces']:
        m=x['members'][0];own=m['statement_original']+' '+m['local_label']
        selectors=m['highlight_symbols']+m['highlight_phrases'];assert any(s in own for s in selectors)
        linked=own+' '+' '.join(c['statement_original'] for c in data['claims'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems']))
        assert all(s in linked for s in selectors)
        for r in x['related_theorems']:
            n=int(r['claim_id'].split('/T')[-1]);assert r['relation']==('direct' if int(m['local_id'][1:]) in direct[n] else 'indirect')
            path=r['via_local_ids'];assert int(path[0][1:]) in direct[n] and path[-1]==m['local_id']
            assert all(right in members[left]['depends_on'] for left,right in zip(path,path[1:]))
            ex=x['theorem_explanations'][r['claim_id']];assert ex['via_local_ids']==path and len(ex['text'])>50
        for k in x['source_keywords']:assert any(k['source_text'] in s for s in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=7,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(a))
    assert counts==dict(theorems=7,interfaces=35,source_members=35,direct_theorem_uses=70,related_theorem_connections=146,unranked_auxiliary_passages=15)
    assert len(ambient['source_issues'])==34 and set(ambient['statement_resolution'])=={'shared',*[str(i) for i in range(1,8)]}
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for c in rebuilt['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Seven complete main-text Theorems were independently enumerated and visually compared. Source order, all conditions and conclusions, the two Theorem 6 branches, and distinct pointwise/uniform expansions are preserved. Proposition 1 and the unnumbered CLT, interval and test are excluded.',
        source_passages='Thirty-five original entries preserve the additive model, function spaces, normalized kernels, empirical estimators, penalty and sequential algorithm, A1–A7, expected-density compatibility, distinct uncentered/centered empirical operators, inverse estimation, debiasing, noise decomposition, population inverse, and kernel norms and sparsity summaries. Fifteen auxiliary passages retain constants and conventions without inventing new API names.',
        dependencies='Independent reconstruction verifies 70 direct uses and 146 related connections. Theorems 4 and 5 inherit only the hypotheses of Theorem 3. Theorem 6 has A1, A2, A4, A5 and A7, with the extra optimizer constraint only in its second branch. Theorem 7 reaches only population inverse kernels, their norms and coordinate spaces, without importing empirical estimators or A assumptions.',
        names_and_highlights='All interfaces have original natural-language keywords, source-type headings and source-backed selectors. The sparsity-parameter term is explicitly identified as the author\'s analogy. Each related theorem has an explanation traced along a same-paper dependency path. Symbols remain in statements, not in display-name lists.',
        notation='Visual review distinguishes empirical from population and expected-density centering, tuple from sum norms, uncentered from centered Pi-hat, the u_j derivative in A7 from the x_k derivative in Theorem 6, and positive q in Theorem 7 from the zero-count convention. Enlarged crops confirm C1 and the full square-root extent in c_q.',
        limits='Thirty-four source issues preserve undefined zero-denominator cases, selection and kernel-domain conventions, the spectral assertion, growth and empty-set conditions, and source typographical ambiguities without silently repairing them. The conclusion ends on page 25 above the clipped appendix boundary; no appendix or supplementary body was used.',
        reproduction='All six content artifacts reproduce byte for byte from the seven retained per-paper scripts. PDF identity, independent heading enumeration, original-statement handoff, source-specific formula checks, independent local graph reconstruction, names, highlights and both structural validators passed.')
    write('evidence/manual-findings.json',findings)
    pages=[1,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,25]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png'),**({'before_main_text_end':True} if n==25 else {})) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
        source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=33,main_text_last_pdf_page=25,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent source heading enumeration and visual comparison of all complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
        counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,review_limits=['Main-text source census; proofs are not certified.','Ambiguous source wording and domains are preserved with separate issue records.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=33,source_version=paper['version'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
