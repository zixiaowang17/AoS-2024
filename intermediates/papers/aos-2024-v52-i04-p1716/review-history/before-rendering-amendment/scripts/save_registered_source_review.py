"""Record the completed manual source review and independently check its saved artifacts.

Frozen hashes identify reviewed content. Running this script is not itself a
fresh mathematical review or a certification of the paper's proofs.
"""
import datetime,hashlib,json,re,subprocess,sys,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '9c90efd4cc75866fdf551eec848beeccc5c3b458899ab3d1bc778b0eaecc9cc7', 'source-passages.json': '9b7e622bcc67c52b5cc625c57c6f7be6e2eb65e206dc07a531b3136cbd0d1e9b', 'interface-extraction.json': 'd6d3a476fa4ca42ae44b36e7e88df421d93484526e9a6e449fab651b51dc062d', 'ambient-prerequisites.json': 'e5b843cf740ff17f46628875421773d393000971a2c8a802e6d60b37801c57a4', 'unfinalized-census.json': '7d130f7264ab5a05aa3e29af81fdd011909a6f65e94015889f48aede192734c3', 'ranked-interfaces.json': '8dfdebac0553cc800c8da0de2db1dfd71eba5529ba136a8494097676ea3c2414'}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(p for p in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if p['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2304.07003v1.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2304.07003'
    pdf=fitz.open(source);assert len(pdf)==registered['pdf_pages']==42
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']=='https://arxiv.org/pdf/2304.07003v1'
    assert paper['version']=='arXiv:2304.07003v1; title-page version April 17, 2023; arXiv stamp 14 April 2023'
    assert paper['main_text_last_pdf_page']==22 and paper['main_text_boundary']['shared_page_with_appendix']
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    assert all(x in first for x in [paper['title'],'Degui Li','Runze Li','Han Lin Shang','arXiv:2304.07003v1','14 Apr 2023','April 17, 2023'])
    headings=[];texts={}
    for n in range(1,23):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,718.24) if n==22 else page.rect
        texts[n]=page.get_text(clip=clip)
        assert (ROOT/'evidence'/f'page-{n:02}.txt').read_bytes().decode()==texts[n]
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans']);match=re.match(r'^Theorem (\d+)\.',s)
                if match and line['spans'][0]['font']=='URWPalladioL-Bold':headings.append((n,match[1]))
    assert headings==[(8,'1'),(10,'2'),(12,'3'),(12,'4')]
    assert 'disclaimer applies.' in texts[22] and 'Appendix A' not in texts[22]
    assert 'Appendix A: Proofs of the main asymptotic results' in pdf[21].get_text(clip=fitz.Rect(0,710,pdf[21].rect.width,750))
    assert len(inv['claims'])==len(data['claims'])==4
    assert [[e['page'] for e in c['evidence']] for c in data['claims']]==[[8],[10],[12],[12]]
    for original,c in zip(inv['claims'],data['claims']):assert all(c[k]==v for k,v in original.items())
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Independently reconstructed from the source formulas and explicit assumptions.
    local={1:[],2:[1],3:[1],4:[1,2],5:[4,2,1],6:[5],7:[3],8:[3],9:[8,1],10:[3,1],
           11:[],12:[10,11],13:[9,12],14:[7,8,11,1],15:[3],16:[10,11],17:[10,16],18:[15,3],
           19:[17,16],21:[19,17,3,16,1,24],22:[18,15],23:[1,3,15],24:[],25:[21,10]}
    direct={1:{4,5,6,7,12,13,14},2:{1,3,4,5,11,15,16,17},3:{4,5,18,21,22,23,24},4:{1,3,4,5,15,18,22,25}}
    reach={1:set(range(1,15)),2:{1,2,3,4,5,10,11,15,16,17},
           3:{1,2,3,4,5,10,11,15,16,17,18,19,21,22,23,24},
           4:{1,2,3,4,5,10,11,15,16,17,18,19,21,22,24,25}}
    assert {k:set(m['depends_on']) for k,m in members.items()}=={f'D{k}':{f'D{i}' for i in v} for k,v in local.items()}
    for c in data['claims']:
        n=int(c['claim_id'].split('/T')[-1]);assert set(c['depends_on'])=={f'D{i}' for i in direct[n]}
        visited=set();stack=list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in visited:visited.add(lid);stack.extend(members[lid]['depends_on'])
        assert visited=={f'D{i}' for i in reach[n]}
        assert visited=={x['members'][0]['local_id'] for x in data['interfaces'] if any(t['claim_id']==c['claim_id'] for t in x['related_theorems'])}
    t=[c['statement_original'] for c in data['claims']]
    b={k:m['statement_original'] for k,m in members.items()}
    assert t[0].count('jointly')==2 and r'\sqrt{N\vee T}' in t[0]
    assert 'independent standard Brownian bridges' in t[0] and 'upper $\\alpha$-quantile' in t[0]
    assert 'If, in addition' in t[1] and r'o_P\left([\ln(N\vee T)]^{1+\zeta}\right)' in t[1]
    assert r'\mid\widehat K=K_0' in t[2]
    assert 'Assumptions 1 and 2(i)' in t[3] and r'T=O(|\mathcal C_\bullet|^{3/2})' in t[3]
    assert r'|\mathcal C_\bullet|=O(T^2)' in t[3] and r'\frac{1}{|\mathcal C(b_k)|^{1/2}}' in t[3]
    assert r'$\eta_{it}$ are independent over $i$' in t[3]
    assert r'\sum_{j=0}^{\infty}j\left(' in b['D4'] and 'does not depend on $N$' in b['D4']
    assert r'A_i\eta_{is}' in b['D5'] and r'\right\|_O^{2+\iota}' in b['D5']
    assert 'an non-increasing order' in b['D6']
    assert r'\sqrt{N/T}' in b['D9'] and r'\frac{\lfloor Tx\rfloor}{T}' in b['D9']
    assert r'\frac1{\sqrt T}' in b['D10'] and r'\frac{\lfloor Tx\rfloor}{T}' in b['D10']
    assert r'\ln(N\vee T)\ln\ln(N\vee T)' in b['D11'] and r'\ln(NT)' not in b['D11']
    assert r'du>\xi_{NT}' in b['D12'] and r'du\geq\xi_{NT}' in b['D16']
    assert r'-x\sum_{s=1}^T' in b['D14'] and r'\widetilde H_A^\diamond' in b['D14']
    assert r'i\in\widehat{\mathcal C}_\bullet' in b['D17']
    assert r'b_1<b_2<\cdots<b_{K_0}' in b['D18']
    assert r'\widehat\tau_i<\overline\tau_K^{(k)}' in b['D19'] and r'\overline\tau_K^{(K)}=T' in b['D19']
    assert r'\sum_{t=1}^{\widehat\tau_{k|K}}' in b['D21'] and r'\sum_{t=\widehat\tau_{k|K}+1}^T' in b['D21']
    assert 'see Assumption 2(iii)' in b['D21'] and r'\widehat K=\arg\min_{1\leq K\leq\overline K}' in b['D21']
    assert r'\sum_{k=1}^{K_0}d_k=1' in b['D22'] and 'bounded away from zero' in b['D23']
    assert r'for any $\zeta>0$' in b['D24']
    assert r'\sum_{i\in\widehat{\mathcal C}(b_k)}' in b['D25']
    originals=data['claims']+list(members.values())+ambient['unranked_auxiliary_passages']
    for obj in originals:
        s=obj['statement_original']
        assert not re.search(r'[\u4e00-\u9fff]',s) and not any(ord(c)<32 and c!='\n' for c in s)
        assert s.count('$')%2==0
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        assert all(1<=e['page']<=22 for e in obj['evidence'])
        assert all(e.get('before_main_text_end') for e in obj['evidence'] if e['page']==22)
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
        for k in x['source_keywords']:
            assert any(k['source_text'] in s for s in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=4,interfaces=len(data['interfaces']),source_members=len(members),
        direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),
        related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),
        unranked_auxiliary_passages=len(ambient['unranked_auxiliary_passages']))
    assert counts==dict(theorems=4,interfaces=24,source_members=24,direct_theorem_uses=30,related_theorem_connections=56,unranked_auxiliary_passages=7)
    assert len(ambient['source_issues'])==36 and set(ambient['statement_resolution'])=={'shared','1','2','3','4'}
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert len(rebuilt['comparisons'])==6
    for c in rebuilt['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Four complete main-text Theorems were independently enumerated by their actual bold headings and visually compared on pages 8, 10 and 12. Both subparts and alternative limits in Theorem 1, both branches in Theorem 2, the conditional membership event in Theorem 3 and all Theorem 4 restrictions are preserved.',
        source_passages='Twenty-four original source entries preserve the function space and operators, model, both parts of Assumption 1, covariance eigenpairs, null/alternative regions, both CUSUM constructions, prescribed threshold, PE test, true and estimated subject sets, individual break estimates, latent partition, largest-gap clustering, the full fitted-mean/penalized-criterion construction, three separate parts of Assumption 2 and the pooled estimate. Seven auxiliary passages retain source conventions and distinct contexts.',
        dependencies='Independent reconstruction verifies 30 direct uses and 56 related connections. Theorem 2 uses only the local omega definition from (3.8), not the alternative signal condition. Theorem 4 directly cites only Assumption 2(i); its estimator reaches 2(iii) through the explicit tuning-parameter restriction in (4.9). Assumption 2(ii) and prior theorem conclusions are not imported.',
        names_and_highlights='Every interface has literal natural-language source keywords, original source statements, faithful headings and matched selectors. Unnamed fitted quantities remain in the contiguous criterion construction rather than receiving an invented standalone name. Every related theorem has a source-backed explanation along its local dependency path.',
        notation='Visual comparison preserved the strict PE threshold versus non-strict detected-set threshold, floor-centered data CUSUM versus x-centered deterministic alternative, square root over N vee T, eta_is on the right of eta-tilde_Nt, the printed operator-norm subscript in (2.6), half-open clusters, noninteger average break locations in sums, and estimated rather than oracle groups in the pooled estimator.',
        limits='Thirty-six source issues document ambiguous domains, spectral prerequisites, moment uniformity, selection/tie conventions, empty clusters, criterion domains and Theorem 4 scope without repairing source statements or certifying proofs. The main-text endpoint is page 22 before Appendix A. An initial page-23 boundary probe exposed opening appendix lines; these were not retained or used in the census.',
        reproduction='All six content JSON artifacts reproduce byte for byte from retained per-paper scripts. Registered PDF identity, independent theorem enumeration and statement handoff, source-specific checks, graph/path reconstruction, names/highlights, mathematical fragments and both structural validators passed.')
    write('evidence/manual-findings.json',findings)
    pages=[1,4,5,6,7,8,9,10,11,12,22]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
        source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=42,main_text_last_pdf_page=22,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent source heading enumeration and visual comparison of all complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
        counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),
        artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},
        source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,
        review_limits=['Main-text source census; proofs are not certified.','Original ambiguous hypotheses, definitions and notation are preserved with separate issue records.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,
        registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=42,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],
        checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},
        reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,
        reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
