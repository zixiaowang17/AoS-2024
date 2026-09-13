"""Record the completed source comparison and independent validation.

The static hashes pin manually reviewed content. Executing this script or
changing a hash does not perform a new semantic review.
"""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={
'theorem-inventory.json':'ea3fb55fb768adf3498c8c01a28a37f03037f5f3eca062122653c125a9bb7f54',
'source-passages.json':'69a240838663bdbef0e93d48cb1a63335d24637d93c5834ae86cfca0ae8ab1ff',
'interface-extraction.json':'9af3d68818b78c28d79bef5b1235bed4dfe52e70fdab0c291d7addca3e982e4a',
'ambient-prerequisites.json':'5b42b758e1c5d0b9aa215697af5e4f62adf3edf1e3b8380f902e3119bdfe329b',
'unfinalized-census.json':'fe87e0d2f9c68f89848d7156a82d90f1710307ca118bb09f5e8517f4b5033d43',
'ranked-interfaces.json':'514d98429607e3619bb3652ed9efb5ece4bf6cf8c66269bb98e0d757ea6aa5ae'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):(ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
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
    assert paper['version']=='arXiv:2303.16711v3, 27 September 2023; manuscript dated 28 September 2023'
    assert paper['source_url']=='https://arxiv.org/pdf/2303.16711v3'
    assert entry['version']=='2303.16711v3.pdf' and entry['source_url']=='https://export.arxiv.org/pdf/2303.16711'
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==digest(ROOT/'theorem-inventory.json')
    pdf=fitz.open(source)
    assert len(pdf)==paper['pdf_pages']==entry['pdf_pages']==83
    first=' '.join(pdf[0].get_text().split())
    assert all(s in first for s in [paper['title'],'Alex Luedtke','Incheoul Chung','arXiv:2303.16711v3','September 28, 2023'])
    assert paper['main_text_last_pdf_page']==30 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    headings=[]
    for n in range(1,31):
        p=pdf[n-1]
        clip=fitz.Rect(0,0,p.rect.width,637.9385986328125) if n==30 else p.rect
        source_text=p.get_text(clip=clip)
        path=ROOT/'evidence'/(f'page-{n:02}.txt' if n<30 else 'page-30-before-appendix.txt')
        assert path.read_bytes().decode()==source_text
        for b in p.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans'])
                m=re.match(r'^Theorem (\d+) \(',s)
                if m:
                    assert line['spans'][0]['font']=='CMBX10'
                    headings.append((n,m[1]))
    assert headings==[(6,'1'),(14,'2'),(15,'3'),(15,'4'),(16,'5'),(19,'6')]
    assert 'Zheng, W.' in source_text and '459' in source_text and 'Appendices' not in source_text
    assert 'Appendices' in pdf[29].get_text(clip=fitz.Rect(0,638,pdf[29].rect.width,658))
    assert len(inv['claims'])==len(data['claims'])==6
    for original,claim in zip(inv['claims'],data['claims']):
        assert all(claim[k]==v for k,v in original.items())
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Reconstructed from the source mathematical roles, independently of the generator.
    local={1:[],2:[],3:[2],4:[3,2],5:[4],6:[4],7:[5],8:[5,7],9:[6,5,7],
           10:[],11:[10,8],12:[10,8],13:[2,3],14:[],15:[11,14],16:[10,8,14],
           17:[5,7,1],18:[10,17],19:[],20:[10,17],21:[4,17,1],
           22:[21,10,17],23:[22],24:[21,23,10,5]}
    direct={1:[1,4,6,8,9],2:[1,4,8,11,12,13],3:[1,4,8,12,14,15],
            4:[1,4,8,12,14,16],5:[4,17,18,19,20],6:[2,4,17,21,22,24]}
    reaches={1:[1,2,3,4,5,6,7,8,9],2:[1,2,3,4,5,7,8,10,11,12,13],
             3:[1,2,3,4,5,7,8,10,11,12,14,15],4:[1,2,3,4,5,7,8,10,12,14,16],
             5:[1,2,3,4,5,7,10,17,18,19,20],6:[1,2,3,4,5,7,10,17,21,22,23,24]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in ids] for k,ids in local.items()}
    for claim in data['claims']:
        n=int(claim['claim_id'].split('/T')[-1])
        assert set(claim['depends_on'])=={f'D{i}' for i in direct[n]}
        reach=set();stack=list(claim['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in reach:
                reach.add(lid);stack.extend(members[lid]['depends_on'])
        assert reach=={f'D{i}' for i in reaches[n]}
        actual={x['members'][0]['local_id'] for x in data['interfaces'] if any(r['claim_id']==claim['claim_id'] for r in x['related_theorems'])}
        assert actual==reach
    t={c['claim_id'].split('/T')[-1]:c['statement_original'] for c in data['claims']}
    b={lid:m['statement_original'] for lid,m in members.items()}
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert '(4) holds' in t['2'] and r'\mathcal D_n^j=o_P' in t['2'] and r'\mathcal R_n^j=o_p' in t['2']
    assert r'\widehat\nu_n-\nu(P_0)' in a['A4'] and r'\bar\nu_n' in t['2']
    assert r'\|\phi_0\|_{L^2(P_0;\mathcal H)}>0' in t['3']
    assert r'\|\phi_0\|_{L^2(P_0;\mathcal H)}>0' not in t['4']
    assert '(i)' in t['3'] and '(ii)' in t['3'] and 'asymptotically conservative' in t['3']
    assert '(25) holds' in t['5'] and [e['page'] for e in data['claims'][4]['evidence']]==[16,17]
    assert r'\frac12\sum_{j=1}^2\mathcal B_n^{j,\beta_n}+P_n\phi_0^{\beta_n}+O_p' in a['A8']
    assert r'\beta\in\ell^2\cap(0,1]^{\mathbb N}' in t['6'] and 'Also,' in t['6']
    assert r'\mathbb H^\beta+\dot\nu_0^\beta(s)' in t['6'] and r'>\alpha' in t['6']
    assert 'is a closed subspace' in b['D6']
    assert r'\mathcal H\times\mathcal Z' in b['D8']
    assert r'\sum_{k=1}^\infty\beta_k^2P\dot\nu_P(h_k)^2' in b['D17']
    assert r'\beta_k\dot\nu_P^*(h_k)(z)h_k' in b['D17']
    assert r'[\nu(\widehat P_n^j)+P_n^j\phi_n^{j,\beta}]' in b['D18']
    assert r'[\Gamma_\beta\circ\nu(\widehat P_n^j)+P_n^j\phi_n^{j,\beta}]' in b['D22']
    assert r'P_n^j\dot\nu_n^{j,*}(h_k)' in b['D24']
    assert r'\ell^2_*:=\ell^2\cap[0,1]^{\mathbb N}' in a['A6']
    assert r'v_k=0' in a['A3'] and 'for $h$ in the image' in a['A10']
    assert r'E_0[\langle\phi_0^\beta(Z),h\rangle_{\mathcal H}^2]' in a['A12']
    for n,lo,hi in [(14,397,429),(19,404,452)]:
        spans=[s for block in pdf[n-1].get_text('dict')['blocks'] for line in block.get('lines',[]) for s in line['spans'] if lo<s['bbox'][1]<hi]
        assert any('E' in s['text'] and s['font']=='CMMI10' for s in spans)
    for item in [*data['claims'],*members.values(),*ambient['unranked_auxiliary_passages']]:
        evidence=list(item['evidence']);fragments=[item['statement_original']]
        for context in item.get('naming_context',[]):
            evidence.extend(context['evidence']);fragments.append(context['text'])
        assert all(1<=e['page']<=30 and (e['page']<30 or e.get('before_main_text_end') is True) for e in evidence)
        for s in fragments:
            assert not re.search(r'[\u4e00-\u9fff]',s)
            assert not any(ord(c)<32 and c!='\n' for c in s)
            assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
            for display,inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
                depth=0
                for brace in re.findall(r'(?<!\\)[{}]',display+inline):
                    depth+=1 if brace=='{' else -1
                    assert depth>=0
                assert depth==0
    for x in data['interfaces']:
        lid=x['members'][0]['local_id']
        assert set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
        assert '$' not in x['name']
        for r in x['related_theorems']:
            n=int(r['claim_id'].split('/T')[-1])
            assert r['relation']==('direct' if int(lid[1:]) in direct[n] else 'indirect')
            explanation=x['theorem_explanations'][r['claim_id']]
            assert explanation['via_local_ids']==r['via_local_ids']
            if n in [2,5]:
                assert (6 if n==2 else 16) in [e['page'] for e in explanation['evidence']]
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
            assert any(s in own for s in m['highlight_symbols']+m['highlight_phrases'])
        for k in x['source_keywords']:
            m=members[k['local_id']]
            assert any(k['source_text'] in s for s in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=6,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['unranked_auxiliary_passages']))
    assert counts==dict(theorems=6,interfaces=24,source_members=24,direct_theorem_uses=34,related_theorem_connections=66,unranked_auxiliary_passages=12)
    assert set(ambient['statement_resolution'])=={'shared','1','2','3','4','5','6'} and len(ambient['source_issues'])==24
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:
        assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        r=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=r.returncode,stdout=r.stdout))
    findings=dict(
      inventory='Independent bold-heading enumeration across admitted pages finds six Theorems in source order. Every complete original statement was compared visually, including the page-17 continuation of Theorem 5. Theorem 4 ends on page 15. Referenced conclusions (4) and (25) are preserved separately in full.',
      source_passages='Twenty-four original interface passages and twelve auxiliary passages were compared with the main-text PDF. They preserve the model, derivative and influence definitions, sample split, both estimators, error terms, bias, operator class, confidence sets, conditional bootstrap and fixed-regularization local alternatives.',
      dependencies='Independent reconstruction verifies 34 direct uses and 66 related connections. Theorems 3 and 4 inherit the hypotheses of Theorem 2, not its regularity conclusion. Theorems 5 and 6 have no original-EIF dependency. Theorem 6 does not acquire Theorem 5 rate assumptions or a mandatory bootstrap threshold.',
      names_and_highlights='All 24 entries use original natural-language source keywords. Definition passages and Lemma excerpts retain their source kind and heading. Each member has a meaningful matching selector; every related theorem has a source-backed explanation and the verified local path.',
      notation='Visual and font inspection preserves ordinary E_0, blackboard Gaussian H, calligraphic Hilbert H and error terms, script submodel collection, hats/bars/tildes, and the o_p/o_P case difference in Theorem 2. Formula (30) retains squared beta weights and the fitted adjoint. The finite-dimensional zero-padding convention is explicit.',
      limits='Twenty-four notes retain the source closed-image assertion, missing adjoint star in Lemma 1, original versus transformed estimator targets, fixed versus varying beta, and inverse-on-image scope. Appendix bodies were not opened. This is a statement and dependency review, not proof certification.',
      reproduction='All six content artifacts reproduce byte for byte from the retained per-paper scripts in an empty directory. Source identity, independent inventory, exact original-claim handoff, graph reconstruction, notation invariants, math-fragment checks and inventory/census validation passed. Reproduction alone does not renew source review.')
    write('evidence/manual-findings.json',findings)
    pages=[1,3,4,5,6,7,8,9,13,14,15,16,17,18,19,30]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png'),**({'before_main_text_end':True} if n==30 else {})) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
      source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=83,main_text_last_pdf_page=30,provenance_path='evidence/source-provenance.json'),
      enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent bold-heading enumeration and visual comparison of all six complete statements and incorporated formulas.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
      counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),
      artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},
      source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,
      review_limits=['Original-source and statement-dependency review, not proof certification.','Appendix bodies and external proofs excluded.','Source closed-image assertion and missing adjoint notation are preserved, not resolved.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,
      registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=83,source_version=paper['version'],registered_version_alias=entry['version'],registered_url_alias=entry['source_url'],
      checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},
      reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},
      findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
