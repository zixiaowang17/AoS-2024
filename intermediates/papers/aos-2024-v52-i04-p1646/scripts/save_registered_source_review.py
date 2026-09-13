"""Record the completed source review and independent census validation.

Fixed hashes identify manually reviewed content; updating or rerunning this
script does not itself review source mathematics or certify proofs.
"""
import datetime,hashlib,json,re,subprocess,sys,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={
'theorem-inventory.json':'7bb5e5c39662bfcbf7d74fcc3ea9091df02f65c107bf368016a7557b1e6dfa51',
'source-passages.json':'cdaf093a5e4c143ae057b20af1dedff00df37076472770ea1e84f9b10df219a4',
'interface-extraction.json':'c145ea71953daa128ff9ab73987dc3061f93e6f48f3a0c6dd94af0e20b0824a0',
'ambient-prerequisites.json':'20f8ac6da48b3da298990b7c5406dd9889282cb693706b54127cc5869a5fee8f',
'unfinalized-census.json':'b18751592f61786bcec3d6b79198640c566a8bd2c37d03a74bb5d81b15572d3c',
'ranked-interfaces.json':'7475467d421dc098f6d42a07e6d67aa1a6bf04a0f3443c654640b344dbac1ddb'}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed artifact',name)
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    register=json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())
    entry=next(x for x in register['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==entry['sha256']
    assert entry['version']=='2112.13479v1.pdf' and entry['source_url']=='https://export.arxiv.org/pdf/2112.13479'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    paper=inv['papers'][0];pdf=fitz.open(source)
    assert len(pdf)==paper['pdf_pages']==entry['pdf_pages']==45
    assert paper['version']=='arXiv:2112.13479v1, 27 December 2021'
    assert paper['source_url']=='https://arxiv.org/pdf/2112.13479v1'
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    assert all(s in first for s in [paper['title'],'Yong He','Xin-Bing Kong','Lorenzo Trapani','Long Yu','arXiv:2112.13479v1','27 Dec 2021'])
    assert paper['main_text_last_pdf_page']==31 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    headings=[];texts={}
    for n in range(1,32):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,321.86700439453125) if n==31 else page.rect
        texts[n]=page.get_text(clip=clip)
        name=f'page-{n:02}.txt' if n<31 else 'page-31-before-appendix.txt'
        assert (ROOT/'evidence'/name).read_bytes().decode()==texts[n]
        for b in page.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans']);m=re.match(r'^Theorem (\d+)\.',s)
                if m and line['spans'][0]['font']=='LMRoman10-Bold':headings.append((n,m[1]))
    assert headings==[(11,'1'),(12,'2'),(13,'3')]
    assert 'in press..' in texts[31] and 'Further assumptions' not in texts[31]
    assert 'Further assumptions' in pdf[30].get_text(clip=fitz.Rect(0,322,pdf[30].rect.width,339))
    assert len(inv['claims'])==len(data['claims'])==3
    assert [[e['page'] for e in c['evidence']] for c in data['claims']]==[[11],[12,13],[13,14]]
    for original,c in zip(inv['claims'],data['claims']):assert all(c[k]==v for k,v in original.items())
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Source-role reconstruction independent of the extraction/finalizer modules.
    local={1:[],2:[1],3:[2,1],4:[],5:[1],6:[],7:[1],8:[1],9:[3],10:[9],
           11:[9,4],12:[1],13:[10],14:[13],15:[13],16:[13],17:[10],18:[]}
    direct={1:[5,6,11,12,14,15,16],2:[5,6,11,12,14,15,16,7,8],3:[6,11,12,17,18,7,8]}
    expected_reach={1:set(range(1,17))-{7,8},2:set(range(1,17)),3:{1,2,3,4,6,7,8,9,10,11,12,17,18}}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in deps] for k,deps in local.items()}
    for c in data['claims']:
        n=int(c['claim_id'].split('/T')[-1])
        assert set(c['depends_on'])=={f'D{i}' for i in direct[n]}
        reach=set();stack=list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(members[lid]['depends_on'])
        assert reach=={f'D{i}' for i in expected_reach[n]}
        assert reach=={x['members'][0]['local_id'] for x in data['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
    t=[c['statement_original'] for c in data['claims']]
    b={lid:m['statement_original'] for lid,m in members.items()}
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert all('B1-B4' in s for s in t)
    assert all('C1-C2' in s for s in t[:2]) and 'C1' not in t[2] and 'C3' not in t[1]
    assert r'=1,\tag{3.28}' in t[1] and r'=\exp(-\exp(-v)),\tag{3.23}' in t[0]
    assert t[1].count('under (3.7) it holds that')==2
    assert r'\min(p_1,m)\to\infty' in t[2] and r'\min(p_1,p_2,m)\to\infty' in t[2]
    assert r'\frac{T_m^{1/2}}{(\ln\ln T_m)}' in t[1]
    assert r'\frac{g\left(p_1^{1-\delta}\right)}{\sqrt{\ln T_m}}' in t[2]
    assert r'\frac{p_1}{\sqrt{mp_2}}' in b['D4']
    assert r'\frac1{Tp_1}\sum_{t=1}^T X_t' in b['D2']
    assert r'\sum_{t=\tau+1}^{m+\tau}' in b['D3']
    assert r'p_1^{-1}\sum_{j=1}^{p_1}\widehat\lambda_{j,\tau}' in b['D9']
    assert r'y_\tau=z_\tau+\psi_\tau' in b['D10']
    assert r'Z_{T_m}=\max_{1\le\tau\le T_m}y_\tau' in b['D17'] and '|y' not in b['D17']
    assert r'a_{T_m}=\frac{b_{T_m}}{1+b_{T_m}^2}' in b['D18']
    assert r'\alpha_{T_m}=\sqrt{2\ln\ln T_m}' in a['A4']
    assert r'\beta=\ln p_1/\ln(p_2m)' in a['A3']
    assert r'O_{a.s.}' in a['A2'] and r'\to c_0<\infty' in a['A2']
    assert 'Assumption C3.' in a['A7'] and r't^*=O(m)' in a['A7']
    assert members['D5']['source_kind']==members['D6']['source_kind']=='assumption'
    assert members['D11']['source_kind']=='condition'
    assert 'supplement for Assumptions B1-B4' in texts[7]
    assert 'Assumption C3.' in texts[12] and 'C1-C2' in texts[12]
    assert 'Assumptions B1-B4 and C2' in texts[13]
    unresolved={x['reference']:x for x in ambient['unresolved_source_references']}
    for i in range(1,5):assert unresolved['Assumption B'+str(i)]['status']=='excluded_not_imported'
    assert len(members)==18 and not any(m['source_heading'].startswith('Assumption B') for m in members.values())
    originals=data['claims']+list(members.values())+ambient['unranked_auxiliary_passages']
    for obj in originals:
        s=obj['statement_original']
        assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        assert not re.search(r'[\u4e00-\u9fff]',s)
        assert not any(ord(ch)<32 and ch!='\n' for ch in s)
        for display,inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        assert all(1<=e['page']<31 or e.get('before_main_text_end') is True for e in obj['evidence'])
    for x in data['interfaces']:
        m=x['members'][0];own=m['statement_original']+' '+m['local_label']
        assert any(s in own for s in m['highlight_symbols']+m['highlight_phrases'])
        for r in x['related_theorems']:
            n=int(r['claim_id'].split('/T')[-1])
            assert r['relation']==('direct' if int(m['local_id'][1:]) in direct[n] else 'indirect')
            exp=x['theorem_explanations'][r['claim_id']]
            assert exp['via_local_ids']==r['via_local_ids'] and len(exp['text'])>40
        for k in x['source_keywords']:
            assert any(k['source_text'] in s for s in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=3,interfaces=len(data['interfaces']),source_members=len(members),
        direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),
        related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),
        unranked_auxiliary_passages=len(ambient['unranked_auxiliary_passages']))
    assert counts==dict(theorems=3,interfaces=18,source_members=18,direct_theorem_uses=23,related_theorem_connections=43,unranked_auxiliary_passages=9)
    assert len(ambient['source_issues'])==30 and set(ambient['statement_resolution'])=={'shared','1','2','3'}
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Independent bold-heading enumeration and visual source comparison preserve all three main-text Theorems, including Theorem 2 on pages 12-13 and Theorem 3 on pages 13-14. The printed equalities, assumption lists, power-condition denominators and almost-all-realizations clauses remain unchanged.',
        source_passages='Eighteen source interfaces and nine auxiliary passages preserve the matrix model and zero-factor conventions, projected spectrum, rate and tuning choices, main-text assumptions, separate alternatives, transformation, randomization, conditional law, monitoring statistics and two normalizer families.',
        dependencies='Independent source-role reconstruction verifies 23 direct uses and 43 related connections. Theorem 3 has no C1 or partial-sum dependency; Theorems 1 and 2 retain their three distinct weighted regimes. Theorem 2 alternative explanations preserve its restricted parts (ii) and (iii). B1-B4 remain unresolved supplementary references rather than invented interface nodes.',
        names_and_highlights='All titles are original natural-language source terms, with separate naming context where required. Main-text assumptions remain assumptions, the rate restriction remains a condition, and model passages are not relabeled as numbered definitions. Every member has a meaningful source selector and every related theorem has an explicit source-backed path explanation.',
        notation='The source square-root scope in (1.3), full-T initial estimator, moving-window endpoints, mean-eigenvalue normalization, uncentered partial sums, trimmed regime, one-sided raw maximum, conditional convergence notation and iterated-log versus log normalizers were checked visually and by source-specific invariants.',
        limits='Supplementary assumptions B1-B4, implicit data-independent randomization, zero-trace behavior, the initial estimator online scope and row-product notation, the null equation reference, and C3/C1 assumption-list issues remain explicit. No appendix body or Section 4 extension replaces an original theorem. This census is not proof certification.',
        reproduction='All six content JSON artifacts reproduce byte for byte from the seven retained per-paper scripts. Registered source identity, independent inventory, exact claim handoff, local graph and reach, source-specific formula and branch checks, mathematical fragments, names/highlights and both schema validations passed.')
    write('evidence/manual-findings.json',findings)
    pages=[1,2,6,7,8,9,10,11,12,13,14,31]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
        source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=45,main_text_last_pdf_page=31,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent bold-heading enumeration and visual comparison of every complete theorem, including continuations.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
        counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),
        artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},
        source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,
        review_limits=['Main-text source statements and dependencies reviewed; proofs not certified.','B1-B4 bodies are excluded and unresolved.','Printed source notation, conditioning and assumption-list issues remain explicit.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,
        registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=45,source_version=paper['version'],registered_version_alias=entry['version'],registered_url_alias=entry['source_url'],
        checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},
        reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},
        findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
