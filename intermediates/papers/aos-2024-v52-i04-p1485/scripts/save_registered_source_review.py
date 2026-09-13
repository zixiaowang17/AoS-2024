"""Pin the completed manual PDF review and run independent census checks.

Expected hashes identify the actually reviewed content. Changed content requires
renewed source inspection; neither rebuilding nor editing a pin performs that review.
"""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED = {'theorem-inventory.json': 'b92b493ebdbdd8ae58d7a88dfdc5ee2bf128bce75c78cf4b82742dcbf3dc0299', 'source-passages.json': '23f6690a70fd5818b9eb2e06440ef563a01bfed906d134846a681699d86e51a1', 'interface-extraction.json': '49501c4cbee74543cc3e2549a49e379eb4402761b9f5cd9362708637594d357b', 'ambient-prerequisites.json': '55902cb73beca310b09c21aaf95ed2bc5b3e9f80fa67d6d92685838ebaab7fa1', 'unfinalized-census.json': '508bbf5c5ea5432deda62fc3be08d5ed9d3bf9fe68c3eb8dabcf35f9a7d8a7ac', 'ranked-interfaces.json': '930fb22b04c8c6988ec399b389e4ba354c026d13d932f4037572102e5852a224'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):(ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed content requires renewed review',name)
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    register=json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())
    entry=next(x for x in register['papers'] if x['paper_id']==PID)
    assert digest(source)==entry['sha256']==SHA
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    paper=inv['papers'][0]
    assert paper['version']=='arXiv:2301.06632v1, 16 January 2023' and entry['version']=='2301.06632v1.pdf'
    assert paper['source_url']=='https://arxiv.org/pdf/2301.06632v1' and entry['source_url']=='https://export.arxiv.org/pdf/2301.06632'
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==digest(ROOT/'theorem-inventory.json')
    pdf=fitz.open(source);assert len(pdf)==paper['pdf_pages']==entry['pdf_pages']==47
    first=' '.join(pdf[0].get_text().upper().split())
    assert all(x in first for x in [paper['title'].upper(),'DAMEK DAVIS','DMITRIY DRUSVYATSKIY','LIWEI JIANG','ARXIV:2301.06632V1'])
    assert paper['main_text_last_pdf_page']==26 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    headings=[]
    for n in range(1,27):
        page=pdf[n-1];clip=fitz.Rect(0,0,page.rect.width,488.0146179199219) if n==26 else page.rect
        source_text=page.get_text(clip=clip)
        path=ROOT/'evidence'/(f'page-{n:02}.txt' if n<26 else 'page-26-before-appendix.txt')
        assert path.read_bytes().decode()==source_text
        for block in page.get_text('dict',clip=clip)['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                match=re.match(r'^Theorem (\d+\.\d+) \(',text)
                if match:
                    assert line['spans'][0]['font']=='CMBX12'
                    headings.append((n,match[1]))
    assert headings==[(12,'2.7'),(13,'3.1'),(14,'3.2'),(20,'5.1')]
    assert '[37]' in source_text and 'Lin Xiao' in source_text and 'Proofs from Section 2' not in source_text
    assert 'Proofs from Section 2' in pdf[25].get_text(clip=fitz.Rect(0,488,pdf[25].rect.width,510))
    assert len(inv['claims'])==len(data['claims'])==4
    for old,new in zip(inv['claims'],data['claims']):assert all(new[k]==v for k,v in old.items())
    claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Independent reconstruction of the actual statement paths, not imported from extraction code.
    local={1:[],2:[],3:[1],4:[],5:[4],6:[1,5],7:[5,9],8:[9],9:[],10:[9],11:[10,8],12:[10],13:[10],14:[],15:[14,10],16:[9],17:[16,1,2],18:[],19:[18,16],20:[18,17,2],21:[18,16],22:[21,17]}
    direct={'2.7':{1,2,4,5,6,7,8,9},'3.1':{8,9,10,11,12,13},'3.2':{8,10,11,12,15},'5.1':{1,2,3,8,16,17,18,19,20,21,22}}
    expected_reach={'2.7':{1,2,4,5,6,7,8,9},'3.1':{8,9,10,11,12,13},'3.2':{8,9,10,11,12,14,15},'5.1':{1,2,3,8,9,16,17,18,19,20,21,22}}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in v] for k,v in local.items()}
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    reach={}
    for n,c in claims.items():
        seen,stack=set(),list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in seen:seen.add(lid);stack.extend(members[lid]['depends_on'])
        reach[n]=seen
    assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected_reach.items()}
    assert 'D13' not in reach['3.2']
    assert {'D4','D5','D6','D7','D10','D11','D12','D13','D14','D15'}.isdisjoint(reach['5.1'])
    assert 'D3' not in reach['2.7']  # The theorem uses an ordinary x-Jacobian, not a covariant Jacobian.
    t={n:c['statement_original'] for n,c in claims.items()};b={lid:m['statement_original'] for lid,m in members.items()}
    assert r'$-A(\bar x)\in\widehat\partial f(\bar x)$' in t['2.7'] and 'unique multiplier vector' in t['2.7']
    assert 'if and only if' in t['2.7'] and r'$(0,\bar x)$' in t['2.7'] and r'\Sigma^\dagger' in t['2.7']
    assert r'\mathcal H(x,y):=A(x)+\nabla\widehat f(x)+\nabla G(x)^\top y' in t['2.7']
    assert 'nonsingular on' in t['2.7'] and r'C^{p+1}' in t['2.7']
    assert 'square integrable' in t['3.1'] and r'\tag{3.3}' in t['3.1']
    assert r'\frac{\operatorname{lip}(\sigma)^{-1}}{2\mathbb E L}' in t['3.1'] and r'\sqrt{\frac{\epsilon_1}{2\mathbb E L}}' in t['3.1']
    assert 'measurable selection' in t['3.1'] and r'\Pr[x_k\in B_{\epsilon_2}(\bar x)]\to1' in t['3.1']
    assert 'symmetric, quasiconvex, and lower semicontinuous' in t['3.2']
    assert r'\lim_{c\to\infty}\liminf_{k\to\infty}\sup_' in t['3.2'] and r'\mathcal B_{c/k}' in t['3.2']
    assert 'Assumption A and B' in t['3.2'] and 'Lipschitz' not in t['3.2']
    assert 'Assumption C, D, E, I, and J' in t['5.1'] and r'\gamma\in(\frac12,1)' in t['5.1']
    assert 'probability one' in t['5.1'] and r'\tag{5.1}' in t['5.1'] and r'$(\bar x,0)$' in t['5.1']
    assert r'\bar x_k=\frac1k\sum_{i=1}^k x_i' in t['5.1']
    assert r'\nabla\sigma(0)\cdot\Sigma\cdot\nabla\sigma(0)^\top' in t['5.1'] and r'\Sigma U' not in t['5.1']
    assert r'})^\dagger' in t['5.1']
    assert all(r'\mathsf N' in t[n] for n in ['3.1','3.2']) and r'\xrightarrow D N' in t['5.1']
    assert 'surjective' in b['D1'] and r'T_{\mathcal M}(x):=\operatorname{Null}(\nabla F(x))' in b['D1']
    assert r'\operatorname*{argmin}_{y\in Q}' in b['D2']
    assert r'\widehat F:U\to\mathbb R^d' in b['D3'] and r'F:\mathcal M\to\mathbb R^m' in b['D3']
    assert r'f(y)\ge f(x)+\langle v,y-x\rangle+o(\|y-x\|)' in b['D4']
    assert r'(x_i,f(x_i),v_i)\to(x,f(x),v)' in b['D5']
    assert r'|f(x)-f(\bar x)|<\epsilon' in b['D6'] and r'f_v(x)=f(x)-\langle v,x\rangle' in b['D6']
    assert 'for any sequences' in b['D7'] and 'the function values' in b['D7']
    assert r'$(\bar x,\bar v)\in\operatorname{gph}F$' in b['D8'] and r'$(\bar v,\bar x)$' in b['D8']
    assert r'F^{-1}(y)=\{x:y\in F(x)\}' in b['D9']
    assert 'arbitrary set-valued map' in b['D10'] and 'measurable map' in b['D10']
    assert r'$(0,\bar x)$' in b['D11']
    assert 'For almost every' in b['D12'] and 'at every' in b['D12'] and r'\|\nabla A(x,z)\|_{\mathrm{op}}^2' in b['D12']
    assert 'assuming one exists' in b['D13'] and [e['page'] for e in members['D13']['evidence']]==[12,13]
    assert r'\phi:(0,\infty)\to\mathbb R' in b['D14'] and r'\phi(1)=0' in b['D14']
    assert 'there exists a solution' in b['D15'] and r'\mathbb E_{z\sim\mathcal P\prime}' not in b['D15']
    assert r'\tag{4.1}' in b['D16'] and 'one such solution' in b['D16']
    assert '(C1)' in b['D17'] and '(C2)' in b['D17'] and r'F_{\mathcal M}+N_{\mathcal M}' in b['D17']
    assert r'x_{k+1}=x_k-\alpha_kG_{\alpha_k}(x_k,\nu_k)' in b['D18'] and 'Section 6' in b['D18']
    assert all(r'\mathcal U_F:=\mathcal U\cap\operatorname{dom}F' in b[lid] for lid in ['D19','D20'])
    assert r'G_\alpha(x,\nu)-F(P_{\mathcal M}(x))-\nu' in b['D20']
    assert r'(1+\|\nu\|)^2(o(\operatorname{dist}(x,\mathcal M))+C\alpha)' in b['D20']
    assert all(f'(J{i})' in b['D21'] for i in range(1,5))
    assert r'\gamma\in(1/2,1]' in b['D21'] and r'\mathbb E[\|\nu_k\|^4\mid\mathcal F_k]<q(x_k)' in b['D21']
    assert 'orthogonal basis' in b['D22'] and 'orthonormal' not in b['D22']
    assert r'U^\top\nu_i^{(1)}\xrightarrow D N(0,\Sigma)' in b['D22'] and 'positive semidefinite' in b['D22']
    for lid,heading in {11:'Assumption A',12:'Assumption B (Integrability and smoothness)',17:'Assumption C (Smooth reduction)',19:'Assumption D (Steplength)',20:'Assumption E (Strong (a) and aiming)',21:'Assumption I (Standing assumptions)',22:'Assumption J'}.items():
        assert members[f'D{lid}']['source_kind']=='assumption' and members[f'D{lid}']['source_heading']==heading
    a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert 'To this end' in a['A1'] and 'closed ball' in a['A1']
    assert r'\operatorname{epi}f' in a['A2'] and r'h\searrow0' in a['A3']
    assert 'Moore-Penrose pseudoinverse' in a['A6'] and 'i.i.d. observations' in a['A7']
    assert r'C^1' in a['A8'] and 'active manifold in concrete examples' in a['A8']
    for item in list(claims.values())+list(members.values())+ambient['unranked_auxiliary_passages']:
        evidence=list(item['evidence']);fragments=[item['statement_original']]
        for context in item.get('naming_context',[]):evidence.extend(context['evidence']);fragments.append(context['text'])
        assert all(1<=e['page']<=26 and (e['page']<26 or e.get('before_main_text_end') is True) for e in evidence)
        for text in fragments:
            assert not re.search(r'[\u4e00-\u9fff]',text)
            assert not any(ord(ch)<32 and ch!='\n' for ch in text)
            assert text.count('$')%2==0 and text.count(r'\[')==text.count(r'\]')
            for display,inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
                depth=0
                for brace in re.findall(r'(?<!\\)[{}]',display+inline):
                    depth+=1 if brace=='{' else -1
                    assert depth>=0
                assert depth==0
    for x in data['interfaces']:
        lid=x['members'][0]['local_id']
        assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if lid in reach[n]}
        assert set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
        assert x['related_theorems'] and '$' not in x['name']
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
            assert any(s in own for s in m['highlight_symbols']+m['highlight_phrases'])
        for k in x['source_keywords']:
            m=members[k['local_id']]
            assert any(k['source_text'] in text for text in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=len(inv['claims']),interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['unranked_auxiliary_passages']))
    assert counts==dict(theorems=4,interfaces=22,source_members=22,direct_theorem_uses=30,related_theorem_connections=33,unranked_auxiliary_passages=8)
    assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==23
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Independent actual-heading enumeration across main text and references finds exactly Theorems 2.7,3.1,3.2,5.1 on pages 12,13,14,20. Each complete original body was visually compared, including all hypotheses, formulas and final conclusions. The references/Appendix A boundary shares page 26; only the reference region is retained.',
      source_passages='Twenty-two original passages and eight auxiliary conventions were compared with PDF pages 6-8,11-15,19-20. They preserve distinct regular and limiting subdifferentials, active-manifold sharpness, local inverse graphs, stochastic population/empirical inclusions, admissible law perturbations, and every referenced abstract-update assumption.',
      dependencies='Independent local and direct graph reconstruction verifies 30 direct uses and 33 related connections. Theorem 3.2 does not inherit Theorem 3.1 SAA or extra Jacobian assumptions. Theorem 5.1 uses the abstract reduction and update, without imposing active-manifold sharpness, subdifferentials or the concrete forward-backward examples.',
      names_and_highlights='Every interface has original natural-language source terms and matching meaningful source expression selectors. Numbered definitions and assumptions retain their actual identities. Explanations name the explicit symbol or referenced condition and follow the stored same-paper path.',
      notation='Visual comparison distinguishes calligraphic H from the set-valued H, calligraphic neighborhoods in Assumptions D/E from the basis matrix U, and the two printed Gaussian fonts. Matrix restrictions, pseudoinverses, norms, conditional moment inequalities and the strict theorem exponent are retained.',
      limits='Twenty-three notes preserve source issues without modifying original statements: reversed inverse basepoints, extension codomain/regularity wording, missing explicit Cp reduction smoothness, tangent-coordinate covariance mismatch, orthogonal versus orthonormal basis, degenerate divergence and radius conventions, and original numbering/forward references. No appendix bodies or external proofs are used; correctness of proofs is not certified.',
      reproduction='All six content artifacts reproduced byte for byte from retained per-paper scripts in an empty directory. Source identity, independent inventory, full claim preservation, manual semantic invariants, graph reach, math-fragment checks and inventory/census schema validation passed. Rebuilding alone does not perform source review.')
    write('evidence/manual-findings.json',findings)
    pages=[1,6,7,8,11,12,13,14,15,19,20,26]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png'),**({'before_main_text_end':True} if n==26 else {})) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
      source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=47,main_text_last_pdf_page=26,provenance_path='evidence/source-provenance.json'),
      enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent bold-heading enumeration and visual comparison of every complete theorem statement.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
      counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),
      artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,
      review_limits=['Source transcription and statement-dependency review, not proof certification.','Appendix bodies and external proofs excluded.','Original source issues and ambiguous conventions retained and documented.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,
      registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=47,source_version=paper['version'],registered_version_alias=entry['version'],registered_url_alias=entry['source_url'],
      checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
