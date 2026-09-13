"""Record the completed manual source review and independent validation.

Static hashes identify the reviewed content. Running this script or changing
the hashes does not perform a new semantic source review.
"""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={
'theorem-inventory.json':'11eb2a11a9d614fc5e5cc529e152c6603e82877fe61100369c047497a0f0924a',
'source-passages.json':'c65cbd83a940e0bb1dbd5ac7ba48fc6e2e191ba7beb28fe84a3078e0c670c6ea',
'interface-extraction.json':'9c915dbdf3cfa162e761b3d214f0528edac57b8f3e8fdfe289889c280f342904',
'ambient-prerequisites.json':'41368927a577a2a7477fd09ffa9a544a7fac61e2de7e4ed5e9558d50f623bd17',
'unfinalized-census.json':'14902c874be7397b7453c87da105155246e26e7cda79be1711d7ce6fbc531094',
'ranked-interfaces.json':'5f01fbc571ce084efa19d83eb31b729402548b1501bb55861e99cebcc93f57e9'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,d):(ROOT/name).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Renew source review for changed content',name)
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    register=json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())
    entry=next(x for x in register['papers'] if x['paper_id']==PID)
    assert digest(source)==entry['sha256']==SHA
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    paper=inv['papers'][0]
    assert paper['version']=='arXiv:2109.13601v2, 30 August 2023'
    assert paper['source_url']=='https://arxiv.org/pdf/2109.13601v2'
    assert entry['version']=='2109.13601v2.pdf' and entry['source_url']=='https://export.arxiv.org/pdf/2109.13601'
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==digest(ROOT/'theorem-inventory.json')
    pdf=fitz.open(source)
    assert len(pdf)==paper['pdf_pages']==entry['pdf_pages']==86
    first=' '.join(pdf[0].get_text().split())
    assert all(s in first for s in [paper['title'],'Kweku Abraham','Castillo','Roquain','arXiv:2109.13601v2','30 Aug 2023'])
    assert paper['main_text_last_pdf_page']==33 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    headings=[]
    for n in range(1,34):
        p=pdf[n-1];source_text=p.get_text()
        assert (ROOT/'evidence'/f'page-{n:02}.txt').read_bytes().decode()==source_text
        for b in p.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans'])
                m=re.match(r'^Theorem (\d+)(?:\.| \()',s)
                if m and line['spans'][0]['font']=='CMBX10':headings.append((n,m[1]))
    assert headings==[(10,'1'),(11,'2'),(12,'3'),(15,'4'),(16,'5'),(17,'6'),(22,'7'),(23,'8'),(24,'9')]
    assert '[48]' in source_text and '393' in source_text and '424' in source_text
    header=pdf[33].get_text(clip=fitz.Rect(0,0,pdf[33].rect.width,155))
    assert 'This supplementary material' in header and 'S-1.' in header
    assert len(inv['claims'])==len(data['claims'])==9
    for original,claim in zip(inv['claims'],data['claims']):assert all(claim[k]==v for k,v in original.items())
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Independent reconstruction from the statement roles and source definitions.
    local={1:[],2:[],3:[],4:[3,1],5:[3,1],6:[4,5],7:[6,2],8:[1],9:[2],10:[],
           11:[3,1],12:[3,1],13:[3,2,1],14:[1,2],15:[14],16:[14],17:[1,2],
           18:[2],19:[1,14,18],20:[11,19,14],21:[3],22:[2]}
    direct={1:[2,8,9,6,7],2:[2,8,9,3,6,10,11,12],3:[2,8,9,5,13],
            4:[1,2,15,16,18,19,6,7],5:[1,2,15,16,20,11,18,19,6],
            6:[1,2,15,16,18,19,5,13],7:[2,8,9,21,10,11,12],
            8:[17,22,6,7,21],9:[8,17,22,6,7,21]}
    reaches={1:[1,2,3,4,5,6,7,8,9],2:[1,2,3,4,5,6,8,9,10,11,12],
             3:[1,2,3,5,8,9,13],4:[1,2,3,4,5,6,7,14,15,16,18,19],
             5:[1,2,3,4,5,6,11,14,15,16,18,19,20],
             6:[1,2,3,5,13,14,15,16,18,19],7:[1,2,3,8,9,10,11,12,21],
             8:[1,2,3,4,5,6,7,17,21,22],9:[1,2,3,4,5,6,7,8,17,21,22]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in ids] for k,ids in local.items()}
    for claim in data['claims']:
        n=int(claim['claim_id'].split('/T')[-1])
        assert set(claim['depends_on'])=={f'D{i}' for i in direct[n]}
        reach=set();stack=list(claim['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(members[lid]['depends_on'])
        assert reach=={f'D{i}' for i in reaches[n]}
        assert reach=={x['members'][0]['local_id'] for x in data['interfaces'] if any(r['claim_id']==claim['claim_id'] for r in x['related_theorems'])}
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in data['claims']}
    b={lid:m['statement_original'] for lid,m in members.items()}
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert all(r'\overline\Phi(b)' in t[n] for n in ['1','2','3','7'])
    assert all(r'\underline{\lim}_n B_n>1' in t[n] for n in ['3','6'])
    assert r'b=b_n\to-\infty' not in t['2']
    assert [e['page'] for e in data['claims'][3]['evidence']]==[15,16]
    assert [e['page'] for e in data['claims'][7]['evidence']]==[23,24]
    assert 'In each case the risk bound is achieved' in t['4'] and r'|X_i|>a_n^*' in t['4']
    assert 'Finally, if we instead grant Assumption 1B' in t['5']
    assert r'(0,r/2^\zeta)' in t['8'] and r'n^{-\kappa}/(\log n)^{1-1/\zeta}' in t['8']
    assert all(f'({s})' in t['9'] for s in ['i','ii','iii','iv']) and 'polynomial in $n$' in t['9']
    assert 'independent data' in b['D1'] and r'n/s_n\to\infty' in b['D2']
    assert r'1\vee\sum_{i=1}^n\varphi_i(X)' in b['D4']
    assert r'1\vee\sum_{i=1}^n\mathbf1\{\theta_i\ne0\}' in b['D5']
    assert r'|S_\theta|=s_n' in b['D9'] and r'$b\in\mathbb R$' in b['D9']
    assert 'Section S-7' in b['D11'] and 'Section S-8' in b['D12']
    assert r'\Pi_{\widehat w}(\theta_i=0\mid X)<t' in b['D12']
    assert r'\sup_{\theta\in\Theta_n}P_\theta' in b['D13'] and r'>A_ns_n' in b['D13']
    assert 'each $F_a$ is $L$-Lipschitz' in b['D14']
    assert r'(n/s_n)\overline F_0(a_n^*-\delta_n)\to\infty' in b['D14']
    assert r'(n/s_n)\overline F_0(a_n^*)\to0' in b['D14']
    assert r'f_{-a}(-x)=f_a(x)' in b['D15'] and r'f_a(-x)=f_a(x)' in b['D16']
    assert r'$a>0$' in b['D15'] and r'$a\ne0$' in b['D16']
    assert all(members[lid]['source_kind']=='assumption' for lid in ['D14','D15','D16'])
    assert r'e^{-|x|^\zeta/\zeta}' in b['D17'] and 'excluded case' in b['D17']
    assert r'$a_j>0$' in b['D18'] and 'all distinct' in b['D18']
    assert r'F_{a_j}(a_n^*)' in b['D19'] and r'F_{|\theta_i|}(a_n^*)' in b['D19']
    assert r'\overline F_{a_j}' not in b['D19']
    assert r's_n(1-\Lambda_n(\theta))' in b['D20']
    assert r'\bigcup_{0\le s\le s_n}\Theta(a_b,s)' in a['A4']
    assert 'selects exactly' in a['A5'] and 'Section S-9' in a['A6']
    assert r'\alpha_n\to0' in a['A7'] and r'\alpha_n\to0' not in t['5']
    for item in [*data['claims'],*members.values(),*ambient['unranked_auxiliary_passages']]:
        evidence=list(item['evidence']);fragments=[item['statement_original']]
        for context in item.get('naming_context',[]):evidence.extend(context['evidence']);fragments.append(context['text'])
        assert all(1<=e['page']<=33 for e in evidence)
        for s in fragments:
            assert not re.search(r'[\u4e00-\u9fff]',s)
            assert not any(ord(c)<32 and c!='\n' for c in s)
            assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
            for d,i in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
                depth=0
                for brace in re.findall(r'(?<!\\)[{}]',d+i):
                    depth+=1 if brace=='{' else -1
                    assert depth>=0
                assert depth==0
    for x in data['interfaces']:
        lid=x['members'][0]['local_id']
        assert set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']} and '$' not in x['name']
        for r in x['related_theorems']:
            n=int(r['claim_id'].split('/T')[-1])
            assert r['relation']==('direct' if int(lid[1:]) in direct[n] else 'indirect')
            exp=x['theorem_explanations'][r['claim_id']]
            assert exp['via_local_ids']==r['via_local_ids']
            if n==6:assert {15,16,17}<={e['page'] for e in exp['evidence']}
            if n==9:assert {23,24}<={e['page'] for e in exp['evidence']}
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
            assert any(s in own for s in m['highlight_symbols']+m['highlight_phrases'])
        for k in x['source_keywords']:
            m=members[k['local_id']]
            assert any(k['source_text'] in s for s in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=9,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['unranked_auxiliary_passages']))
    assert counts==dict(theorems=9,interfaces=22,source_members=22,direct_theorem_uses=61,related_theorem_connections=92,unranked_auxiliary_passages=7)
    assert set(ambient['statement_resolution'])=={'shared',*[str(i) for i in range(1,10)]}
    assert len(ambient['source_issues'])==24
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Independent bold-heading enumeration over pages 1-33 finds exactly nine main-text Theorems. All complete original statements were visually compared, including the continued threshold attainment of Theorem 4 and both pages of Theorem 8. Theorem 9 remains the printed four-part summary.',
      source_passages='Twenty-two source interfaces and seven auxiliary passages preserve the model, risk definitions, sparse classes, procedures, common and alternative assumptions, signal averages, classification class, large-signal class and summary context. Supporting pages and math notation were visually checked.',
      dependencies='Independent source-role reconstruction verifies 61 direct uses and 92 related connections. Alternative noise branches retain their different risk values; FNR-only results do not acquire an additional combined loss. The classification union keeps the original upper sparsity bound in a_b. Supplemental proof results are not imported.',
      names_and_highlights='All interface titles are original natural-language keywords. Original Definition 1 and Assumption 1 branch labels retain their source kinds. Every member has a meaningful matching selector and each related theorem has a source-backed explanation with its local path.',
      notation='The source lower-limit notation, upper tails versus CDFs, Fraktur combined risk, calligraphic procedure classes, bold italic strength vector, strict versus non-strict thresholds, and exact versus upper-bound sparsity are preserved. Theorem 8 retains its unique-root interval and logarithmic rate factor.',
      limits='Exact S-18/S-29 procedure details and the precise S-9 adaptation statements remain unresolved under the main-text-only scope. Theorem 5 level/uniformity issue and the missing parameter-sign symmetry in Assumption 1B are recorded without changing the original text. Initial supplementary heading hits were excluded and no supplemental theorem body is used.',
      reproduction='All six content artifacts reproduce byte for byte in an empty directory from retained per-paper scripts. Registered source identity, independent inventory, exact claim handoff, reconstructed graph, source-specific invariants, mathematical fragments and inventory/census schema validation passed. This does not certify proofs or renew source review merely by rebuilding.')
    write('evidence/manual-findings.json',findings)
    pages=[1,4,5,7,9,10,11,12,13,14,15,16,17,22,23,24,33]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
      source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=86,main_text_last_pdf_page=33,provenance_path='evidence/source-provenance.json'),
      enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent bold-heading enumeration and visual comparison of all nine complete statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
      counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),
      artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},
      source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,
      review_limits=['Original statement and dependency review, not proof certification.','Supplementary procedure details and precise adaptation statements remain unresolved.','Source level/uniformity and sign-convention issues are preserved, not repaired.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,
      registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=86,source_version=paper['version'],registered_version_alias=entry['version'],registered_url_alias=entry['source_url'],
      checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},
      reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},
      findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
