"""Record the completed manual source review and independent checks.

The fixed hashes pin reviewed content. Rebuilding or merely updating a hash
does not perform or renew semantic source review.
"""
import datetime,hashlib,json,re,subprocess,sys,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={
'theorem-inventory.json':'939bb32306c08da30cd081b769370ead274d4f2a800dfa86986255d5d1bd1f26',
'source-passages.json':'99b3915a59fc38a504b93786e5cefcb44486bb07debf95a3b8cfb48d913d3378',
'interface-extraction.json':'7f7eb407919ff53dafd67821bbbfa256b284db0552075d497822cab8e0790d64',
'ambient-prerequisites.json':'7e49bea26b5e64577b556f7e36837fabf252e54175ee1c8957894de5cab9e48c',
'unfinalized-census.json':'deafeb279798a6dacf54c6a091fbfa9bad72660d659d21e4208811878279b2b8',
'ranked-interfaces.json':'bc47143fb1363e26bcab1b06fc37e5517e7b29f02e77de2e3c4cf38027ca3337'}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    register=json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())
    entry=next(x for x in register['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==entry['sha256']
    assert entry['version']=='2202.03369v2.pdf'
    assert entry['source_url']=='https://export.arxiv.org/pdf/2202.03369'
    pdf=fitz.open(source)
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    paper=inv['papers'][0]
    assert len(pdf)==paper['pdf_pages']==entry['pdf_pages']==93
    assert paper['source_url']=='https://arxiv.org/pdf/2202.03369v2'
    assert paper['version']=='arXiv:2202.03369v2, 22 May 2023; manuscript dated 23 May 2023'
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    assert all(s in first for s in [paper['title'],'Charles R. Doss','Guangwei Weng','Lan Wang','Ira Moscovice','Tongtan Chantarat','arXiv:2202.03369v2','22 May 2023','May 23, 2023'])
    assert paper['main_text_last_pdf_page']==28 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    headings=[];texts={}
    for n in range(1,29):
        page=pdf[n-1]
        clip=fitz.Rect(0,0,page.rect.width,200.71694946289062) if n==28 else page.rect
        texts[n]=page.get_text(clip=clip)
        name=f'page-{n:02}.txt' if n<28 else 'page-28-before-appendix.txt'
        assert (ROOT/'evidence'/name).read_bytes().decode()==texts[n]
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans'])
                m=re.match(r'^Theorem (\d+\.\d+)\.',s)
                if m and line['spans'][0]['font']=='CMBX10':headings.append((n,m[1]))
    assert headings==[(17,'3.1'),(20,'3.2'),(20,'3.3'),(21,'3.4')]
    assert 'Acknowledgements' in texts[28] and 'DMS-1712706.' in texts[28]
    assert 'Empirical process lemmas' not in texts[28]
    assert 'Empirical process lemmas' in pdf[27].get_text(clip=fitz.Rect(0,200,pdf[27].rect.width,220))
    # Source-side spot checks support the preceding full visual comparison.
    flat={n:re.sub(r'\s+','',s) for n,s in texts.items()}
    for n,needle in [(13,'P(Sτ∪Sπ∪Sµ)=1.'),(14,'liminfhn≤limsuphn'),
                     (16,'P(S¯π∪S¯µ)=1'),(20,'limn→∞n1/40/δn=0'),
                     (17,'−{θ0(a)−¯m(a))}2'),(20,'N(bh,V)'),(21,'N(bh,V)')]:
        assert needle in flat[n],(n,needle)
    assert any('Z' in span['text'] and span['font']=='CMMIB10'
               for block in pdf[19].get_text('dict')['blocks']
               for line in block.get('lines',[]) for span in line['spans'])
    assert len(inv['claims'])==len(data['claims'])==4
    for original,claim in zip(inv['claims'],data['claims']):
        assert all(claim[k]==v for k,v in original.items())
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Reconstruct statement roles independently of the extraction/finalizer modules.
    local={1:[],2:[1],3:[1],4:[1],5:[],6:[5],7:[2,3,1],8:[7,4],9:[8,4],
           10:[9,8,4,1],11:[5,1],12:[3],13:[5,1],14:[1],15:[6,3],16:[3,2],
           17:[1,3,2],18:[],19:[18],20:[],21:[2,3,4],22:[19],23:[2,3,4],
           24:[21,18],25:[],26:[],27:[17,2,3,21,6],28:[1],29:[8,4,10],30:[9,8,4,10]}
    direct={
        '3.1':[11,12,13,14,15,16,17,20,21,22,23,24,25,27,26,3,10,6],
        '3.2':[11,12,13,14,15,16,17,20,21,22,23,27,26,3,10,6,7,4],
        '3.3':[11,12,13,14,15,16,17,20,21,22,23,24,6,25,27,26,3,28,29],
        '3.4':[11,12,13,14,15,16,17,20,21,22,23,24,18,6,25,27,26,3,28,30]}
    expected_reach={'3.1':set(range(1,28)), '3.2':set(range(1,28))-{24,25},
                    '3.3':set(range(1,30)), '3.4':set(range(1,31))-{29}}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in ids] for k,ids in local.items()}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1]
        assert set(c['depends_on'])=={f'D{i}' for i in direct[n]}
        reach=set();stack=list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(members[lid]['depends_on'])
        assert reach=={f'D{i}' for i in expected_reach[n]}
        assert reach=={x['members'][0]['local_id'] for x in data['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in data['claims']}
    b={lid:m['statement_original'] for lid,m in members.items()}
    assert '(J.1)' in t['3.1'] and '(M.4)' in t['3.1'] and r'\tag{3.4}' in t['3.1']
    assert 'E(B)' not in t['3.2'] and 'J_4' not in t['3.3']
    assert r'J_4(1,\mathcal F,L_2)<\infty' in t['3.4']
    assert r'c_0=\mathbb P\xi(\boldsymbol Z;\pi_0,\mu_0)' in t['3.2']
    assert r'\int g(a)\varpi(a)w(a)\,da=0' in t['3.2']
    assert r'\lim_{n\to\infty}n^{1/40}/\delta_n=0' in t['3.2']
    assert r'P(T_n>z_{n,1-\alpha})\to1' in t['3.2']
    assert r'P(S_\tau\cup S_\pi\cup S_\mu)=1' in b['D17']
    assert r'P(S_{\bar\pi}\cup S_{\bar\mu})=1' in b['D24']
    assert r'c_1^h n^{-1/5}\le\liminf h_n' in b['D20']
    assert r's_n^\infty r_n^\infty=o\{(n\sqrt h)^{-1/2}\}' in b['D23']
    assert r'K_h^{(s)}(x):=K^{(s)}(x/h)' in b['D26']
    assert r'\{\theta_0(a)-\bar m(a))\}^2' in b['D27']
    assert 'centered at the null estimate' in b['D29'] and r'\widehat\theta_h(A_i)' not in b['D29']
    assert r'-\widehat\theta_h(A_i)' in b['D30'] and 'D29' not in members['D30']['depends_on']
    assert all(members[f'D{i}']['source_kind']=='assumption' for i in [*range(11,18),*range(20,25)])
    originals=data['claims']+list(members.values())+ambient['unranked_auxiliary_passages']
    for obj in originals:
        s=obj['statement_original']
        assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert not re.search(r'[\u4e00-\u9fff]',s)
        assert not any(ord(c)<32 and c!='\n' for c in s)
        for display,inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1
                assert depth>=0
            assert depth==0
        for e in obj['evidence']:assert 1<=e['page']<28 or e.get('before_main_text_end') is True
    for x in data['interfaces']:
        m=x['members'][0];lid=m['local_id'];own=m['statement_original']+' '+m['local_label']
        assert any(s in own for s in m['highlight_symbols']+m['highlight_phrases'])
        for r in x['related_theorems']:
            n=r['claim_id'].split('/T')[-1]
            assert r['relation']==('direct' if int(lid[1:]) in direct[n] else 'indirect')
            exp=x['theorem_explanations'][r['claim_id']]
            assert exp['via_local_ids']==r['via_local_ids']
            assert len(exp['text'])>40
        for keyword in x['source_keywords']:
            assert any(keyword['source_text'] in s for s in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=4,interfaces=len(data['interfaces']),source_members=len(members),
        direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),
        related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),
        unranked_auxiliary_passages=len(ambient['unranked_auxiliary_passages']))
    assert counts==dict(theorems=4,interfaces=30,source_members=30,direct_theorem_uses=75,related_theorem_connections=110,unranked_auxiliary_passages=9)
    assert len(ambient['source_issues'])==27
    assert set(ambient['statement_resolution'])=={'shared','3.1','3.2','3.3','3.4'}
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:
        assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Independent bold-heading enumeration finds four main-text Theorems, all complete on pages 17,20,20,21. Visual comparison preserves all hypotheses, distribution formulas and original reference labels. Theorem 3.2 bold observation vector was corrected after font inspection and the inventory was revalidated.',
      source_passages='Thirty interfaces and nine auxiliary passages were checked against main-text pages 9-17 and 20-21. They preserve causal and observed quantities, estimator formulas, all separately numbered I/D/E(A) assumptions, E(B), entropy, metric, convolution, target distribution and both bootstrap procedures.',
      dependencies='Independent source-role reconstruction verifies 75 direct uses and 110 related connections. Theorem 3.2 has no nuisance E(B) dependency; Theorem 3.3 has no explicit J4 addition; Theorem 3.4 retains its added J4 assumption and different residual centering. The replaced null-residual rule is not a prerequisite of the smoother-centered rule.',
      names_and_highlights='Titles use exact natural-language source keywords, with naming context retained where needed. Assumption kinds remain separate from definitions. Every original member has a matching meaningful selector, and every related theorem has a source-backed local-path explanation.',
      notation='Bold observation/covariate vectors, blackboard integration versus ordinary P, calligraphic laws/supports, convolution versus pointwise powers, mixed norms, union conditions, bandwidth limits and the literal rate direction were checked against the PDF. Unbalanced source parenthesis in (3.2) remains preserved.',
      limits='Appendix-labelled references, b_h versus b_0h, unsubscripted varpi, continuity-set and bandwidth/covering-range issues, and the prose/theorem entropy mismatch remain explicit. Initial appendix heading hits were excluded; no appendix body supplies census content. This is a statement/source audit, not proof certification.',
      reproduction='All six JSON content artifacts reproduce byte for byte from the seven retained per-paper scripts. Source hash, exact inventory handoff, independently reconstructed local graph and reach, source-specific checks, mathematical fragments, names/highlights and both schema validations passed.')
    write('evidence/manual-findings.json',findings)
    pages=[1,9,10,11,12,13,14,15,16,17,20,21,28]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
        source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=93,main_text_last_pdf_page=28,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent bold-heading enumeration and visual comparison of all four complete statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
        counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),
        artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},
        source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,
        review_limits=['Source statements and dependencies reviewed; proofs not certified.','Printed appendix references and internal source inconsistencies remain explicit.','Conditional independence of bootstrap signs is not explicitly stated in the quoted algorithm.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,
        registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=93,source_version=paper['version'],registered_version_alias=entry['version'],registered_url_alias=entry['source_url'],
        checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},
        reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},
        findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
