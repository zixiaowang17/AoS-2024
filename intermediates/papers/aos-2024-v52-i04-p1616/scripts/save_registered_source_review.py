"""Record the fresh PDF source review and independent census validation.

Static hashes pin reviewed content. Running this script does not itself
perform a new semantic review or certify the source proofs.
"""
import datetime,hashlib,json,re,subprocess,sys,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={
'theorem-inventory.json':'268ff5b29670f04643defc849238116786a741498cc19ee784fbe29afa31e991',
'source-passages.json':'ebd7e952528c726c052a89b620c8da22d882de9dc9022c8ebb83f3e98563b3e1',
'interface-extraction.json':'b2c48b744754df924ed7d2f8b4b0c5fbc5ea4dde04199f75fe99f854716ba72f',
'ambient-prerequisites.json':'fdcb4322c9692b8e7bfe5b93ca68c8aac5f301d896005c76a7ee70dabe9ddecd',
'unfinalized-census.json':'70825ea516c5673bdc459746618b2103036e4689f692ca779eeb056b952b5273',
'ranked-interfaces.json':'3914b993d8a64236c47966efb8b0b43c36a5817e647bea275f5862ac04a61608'}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    register=json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())
    entry=next(x for x in register['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==entry['sha256']
    assert entry['version']=='2212.12848v3.pdf' and entry['source_url']=='https://export.arxiv.org/pdf/2212.12848'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    prior=json.loads((ROOT/'prior-review/ranked-interfaces.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    paper=inv['papers'][0];pdf=fitz.open(source)
    assert len(pdf)==paper['pdf_pages']==entry['pdf_pages']==47
    assert paper['source_url']=='https://arxiv.org/pdf/2212.12848v3' and paper['version']=='arXiv:2212.12848v3'
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    assert all(s in first for s in ['GROMOV-WASSERSTEIN DISTANCES','ENTROPIC REGULARIZATION, DUALITY, AND SAMPLE COMPLEXITY','ZHENGXIN ZHANG','ZIV GOLDFELD','YOUSSEF MROUEH','BHARATH K. SRIPERUMBUDUR','arXiv:2212.12848v3','28 Sep 2023'])
    assert paper['main_text_last_pdf_page']==28 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    headings=[];text={}
    for n in range(1,29):
        page=pdf[n-1];text[n]=page.get_text()
        assert (ROOT/'evidence'/f'page-{n:02}.txt').read_bytes().decode()==text[n]
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                s=''.join(x['text'] for x in line['spans']);m=re.match(r'^Theorem (\d+) \(',s)
                if m and line['spans'][0]['font']=='TeXGyreTermesX-Bold':headings.append((n,m[1]))
    assert headings==[(9,'1'),(9,'2'),(11,'3')]
    assert '[ZMGS22]' in text[28] and '7257' in text[28] and '7285' in text[28]
    assert 'Appendix A. Proof of Proposition 1' in pdf[28].get_text(clip=fitz.Rect(0,0,pdf[28].rect.width,100))
    assert len(inv['claims'])==len(data['claims'])==3
    for original,c,old in zip(inv['claims'],data['claims'],prior['claims']):
        assert all(c[k]==v for k,v in original.items())
        assert c['claim_id']==old['claim_id'] and c['statement_original']==old['statement_original']
    oldids={x['interface_id'] for x in prior['interfaces']}
    assert {x['interface_id'] for x in data['interfaces']}==oldids|{'gw-D12'}
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Independent source-role reconstruction, without importing extraction choices.
    local={1:[],3:[1,11],4:[1,10],5:[1,4,11],6:[1,11,5,12],7:[3],8:[],9:[],10:[],11:[],12:[]}
    direct={1:[6,3,7,10],2:[5,8,9],3:[4,8]}
    reach_expected={1:{1,3,4,5,6,7,10,11,12},2:{1,4,5,8,9,10,11},3:{1,4,8,10}}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in deps] for k,deps in local.items()}
    for c in data['claims']:
        n=int(c['claim_id'].split(':theorem-')[-1])
        assert set(c['depends_on'])=={f'D{i}' for i in direct[n]}
        reach=set();stack=list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(members[lid]['depends_on'])
        assert reach=={f'D{i}' for i in reach_expected[n]}
        assert reach=={x['members'][0]['local_id'] for x in data['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
    b={lid:m['statement_original'] for lid,m in members.items()}
    t=[c['statement_original'] for c in data['claims']]
    assert r'\mathsf{S}^{2}_{\varepsilon}' in t[0] and r'M_{2}(\mu)M_{2}(\nu)' in t[0]
    assert 'infimum is achieved' in t[0] and r'[-M_{\mu,' in t[0]
    assert r'9\left\lceil\frac{d_{x}}{2}\right\rceil+11' in t[1]
    assert r'9\left\lceil\frac{d_{x}\vee d_{y}}{2}\right\rceil+11' in t[1]
    assert t[2].count(r'\sup_')==2 and 'without the square' in t[2]
    assert r'(d_{x}\wedge d_{y})\vee 4' in t[2]
    assert r'\int x\,d\mu(x)=\int y\,d\nu(y)=0' in b['D12']
    assert members['D12']['source_kind']=='condition' and members['D7']['source_kind']=='theorem_excerpt'
    assert r'd_{1}' in b['D6'] and r'd_{2}' in b['D6']
    assert 'equals $+\\infty$ otherwise' in b['D11']
    assert r'\|x\|^{\beta}/2\sigma^{2}' in b['D9']
    assert 'are centered' in text[8] and 'Frobenius norms' in text[4]
    assert 'allow c to take negative value' in text[5]
    originals=data['claims']+list(members.values())+ambient['unranked_auxiliary_passages']
    for obj in originals:
        s=obj['statement_original']
        assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert not re.search(r'[\u4e00-\u9fff]',s)
        assert not any(ord(ch)<32 and ch!='\n' for ch in s)
        for display,inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1
                assert depth>=0
            assert depth==0
        assert all(1<=e['page']<=28 for e in obj['evidence'])
    for x in data['interfaces']:
        m=x['members'][0];own=m['statement_original']+' '+m['local_label']
        assert any(s in own for s in m['highlight_symbols']+m['highlight_phrases'])
        for r in x['related_theorems']:
            n=int(r['claim_id'].split(':theorem-')[-1])
            assert r['relation']==('direct' if int(m['local_id'][1:]) in direct[n] else 'indirect')
            exp=x['theorem_explanations'][r['claim_id']]
            assert exp['via_local_ids']==r['via_local_ids'] and len(exp['text'])>40
        for k in x['source_keywords']:
            assert any(k['source_text'] in s for s in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=3,interfaces=len(data['interfaces']),source_members=len(members),
        direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),
        related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),
        unranked_auxiliary_passages=len(ambient['unranked_auxiliary_passages']))
    assert counts==dict(theorems=3,interfaces=11,source_members=11,direct_theorem_uses=9,related_theorem_connections=20,unranked_auxiliary_passages=8)
    assert len(ambient['source_issues'])==24 and set(ambient['statement_resolution'])=={'shared','1','2','3'}
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Fresh PDF review independently enumerates the three bold Theorems and visually checks their complete statements on pages 9 and 11. All existing theorem IDs and original bodies are retained, including both lower bounds and the unsquared-distance clause in Theorem 3.',
      source_passages='Eleven source interfaces and eight auxiliary passages preserve the main-text probability, norm, transport, moment, entropy, empirical and tail conventions. The added centered-marginal condition captures Section 3.2 without editing Theorem 1. All ten prior interface IDs are retained.',
      dependencies='Independent source-role reconstruction verifies nine direct uses and twenty related connections. The decomposition now resolves the full EGW functional and its centering convention; the theorem cost resolves its EOT problem. Empirical theorems acquire neither sample centering nor proof-only regularity assumptions.',
      names_and_highlights='All interface names use literal natural-language source terms; the EOT heading is separately preserved as naming context. The centering passage is a condition, the cost passage is a theorem excerpt, and all definitions have meaningful matching selectors and source-backed related-theorem explanations.',
      notation='Visual review distinguishes the decomposition label S_epsilon^2 from D squared, the Frobenius norm from the operator norm, matrix boxes from norm balls, fourth-moment classes from second-moment products, convolution-free quadratic distortion, and the one/two-sample dimension and logarithmic exponents.',
      limits='The source centering scope, d1/d2 index mismatch, zero-parameter endpoint of the tail definition, and lower-bound support-geometry scope remain explicit. Appendix bodies and proof-only constructions are excluded. This revalidation is not a proof of the paper results.',
      reproduction='Seven retained per-paper scripts reproduce six content JSON artifacts exactly in an empty directory. The source identity, independent inventory, unchanged original claim bodies, reconstructed graph and reach, source-specific invariants, mathematical fragments, keywords/highlights and schema checks passed.')
    write('evidence/manual-findings.json',findings)
    pages=[1,4,5,6,7,8,9,11,28]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
        source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=47,main_text_last_pdf_page=28,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent bold-heading enumeration and visual comparison of all three complete statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
        counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),
        artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},
        prior_artifacts='prior-review',source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,
        review_limits=['Fresh source statement and dependency review, not proof certification.','Source centering, notation and lower-bound support issues are preserved, not silently repaired.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,
        registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=47,source_version=paper['version'],registered_version_alias=entry['version'],registered_url_alias=entry['source_url'],
        checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},
        reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},
        findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
