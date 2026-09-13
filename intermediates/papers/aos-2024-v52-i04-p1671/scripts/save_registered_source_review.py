"""Record the completed manual source review and independently check its saved artifacts.

Frozen hashes identify reviewed content. Running this script is not itself a
fresh mathematical review or a certification of the paper's proofs.
"""
import datetime,hashlib,json,re,subprocess,sys,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={
'theorem-inventory.json':'8349a57759e496871c0e348cd64e1b05b021fa06a712235eaae9a9f54b540495',
'source-passages.json':'fcf6c386092d4bc776100b3ba2a86d90bab18a2939cdaa90e18ddb23e47689ab',
'interface-extraction.json':'b8f276f0d94e382efc7e4b322a493fc4bbc237742f35fd80df1f4a10d7018a56',
'ambient-prerequisites.json':'17747953c45d597001fccb3bd00dd56717d9416e21fa747df4e4e7d765896707',
'unfinalized-census.json':'39ceb85ab041b58d0bb0cabcdb31653546acfd6a94eb3dd28f14e3ea265cbcd9',
'ranked-interfaces.json':'9c43ca62d837e31438eebac144967976cb522e03e0ae135560a4d8215409bcfe'}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    manifest=json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())
    registered=next(p for p in manifest['papers'] if p['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2209.04419v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2209.04419'
    pdf=fitz.open(source);assert len(pdf)==registered['pdf_pages']==41
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']=='https://arxiv.org/pdf/2209.04419v2'
    assert paper['version']=='arXiv:2209.04419v2, 4 June 2024'
    assert paper['main_text_last_pdf_page']==28 and not paper['main_text_boundary']['shared_page_with_appendix']
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    assert all(x in first for x in [paper['title'],'Weidong Liu','Jiyuan Tu','Xiaojun Mao','Xi Chen','arXiv:2209.04419v2','4 Jun 2024'])
    headings=[];texts={}
    for n in range(1,29):
        texts[n]=pdf[n-1].get_text()
        assert (ROOT/'evidence'/f'page-{n:02}.txt').read_bytes().decode()==texts[n]
        for b in pdf[n-1].get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans']);match=re.match(r'^Theorem (\d+)',s)
                if match and line['spans'][0]['font']=='CMBX10':headings.append((n,match[1]))
    assert headings==[(12,'1'),(12,'2'),(15,'3'),(17,'4')]
    assert '1004–1018' in texts[28] and 'Appendix' not in texts[28]
    assert 'Appendix' in pdf[28].get_text(clip=fitz.Rect(0,0,pdf[28].rect.width,95))
    assert len(inv['claims'])==len(data['claims'])==4
    assert [[e['page'] for e in c['evidence']] for c in data['claims']]==[[12],[12],[15],[17,18]]
    for original,c in zip(inv['claims'],data['claims']):assert all(c[k]==v for k,v in original.items())
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Independent reconstruction from the source-defined objects and algorithm calls.
    local={1:[],2:[],3:[2],4:[3],5:[3],6:[2],7:[],8:[2,5,7],9:[2,8,6],
           10:[],11:[10,9],12:[],13:[],14:[13],15:[13,14,9],16:[]}
    direct={1:{1,9},2:{2,3,4,6,9},3:{11,12},4:{14,15,16}}
    reach={1:{1,2,3,5,6,7,8,9},2:{2,3,4,5,6,7,8,9},
           3:{2,3,5,6,7,8,9,10,11,12},4:{2,3,5,6,7,8,9,13,14,15,16}}
    assert {k:m['depends_on'] for k,m in members.items()}=={f'D{k}':[f'D{i}' for i in v] for k,v in local.items()}
    for c in data['claims']:
        n=int(c['claim_id'].split('/T')[-1]);assert set(c['depends_on'])=={f'D{i}' for i in direct[n]}
        visited=set();stack=list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in visited:visited.add(lid);stack.extend(members[lid]['depends_on'])
        assert visited=={f'D{i}' for i in reach[n]}
        assert visited=={x['members'][0]['local_id'] for x in data['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
    t=[c['statement_original'] for c in data['claims']]
    b={k:m['statement_original'] for k,m in members.items()}
    a={p['local_id']:p['statement_original'] for p in ambient['unranked_auxiliary_passages']}
    assert r'\widetilde s\ge\overline s' in t[1] and r'\widetilde s\ge s' in t[2]
    assert r'f_l(\boldsymbol Q_l^r,\overline Q_l)' in t[1] and 'with respect to the randomness in the algorithm' in t[1]
    assert r'\lambda_N\ge C_1' in t[2] and r'\lambda_N=C_3' in t[3]
    assert r'\gamma_1>0' in t[2] and r'\mathbb P(\boldsymbol\theta^*,C)' in t[2]
    assert r'\frac{\sqrt{\widetilde s\log(1/\delta)}\log p}{m\sqrt n\epsilon}' in t[2]
    assert r'\widetilde s=o(\sqrt{n/\log p})' in t[3]
    assert r'\max_{1\le j\le m}\lambda_j' in t[3] and 'with probability tending to 1.' in t[3]
    assert r'\boldsymbol\Sigma=\mathbb E\boldsymbol X\boldsymbol X^{\mathrm T}' in t[3]
    assert r'\max_{l\in S^c}\frac{|\boldsymbol\omega_{-l}|_1}{\omega_{l,l}}\le1-\Delta_0' in t[3]
    assert 'except for one local machine' in b['D1'] and 'every measurable subset' in b['D1']
    assert r'N_l^+\ge N_l^0+N_l^-+1' in b['D3']
    assert r'-\min\{N_l^++N_l^0-N_l^-' in b['D5']
    assert r'f_l(\boldsymbol Q_l^r,0)=\min' in b['D6']
    assert r'\operatorname{Lap}(4\sqrt{2\widetilde s\log(1/\delta)}/\epsilon)' in b['D8']
    assert r'\operatorname{Peeling}(\mathbb Q,\widetilde s,\epsilon/2,\delta/2)' in b['D9']
    assert r'\epsilon/(4\sqrt{2\widetilde s\log(2/\delta)})' in b['D9']
    assert r'\exp\{\epsilon' in b['D9'] and r'f_l(\boldsymbol Q_l^r,1)/4' in b['D9']
    assert r'\widehat{\boldsymbol Q}=\{\widehat Q_l|l\in\widehat S\}' in b['D9']
    assert r'\text{if }|x|\le\lambda' in b['D10']
    assert r'n_j^{-1}\sum_{i\in\mathcal H_j}' in b['D11']
    assert r'|X_l-\theta_l^*|^3' in b['D12']
    assert r'\frac1{2n_j}' in b['D13'] and r'\lambda|\boldsymbol\theta|_1' in b['D13']
    assert r'|\widehat{\boldsymbol\theta}_j(\lambda)|_0\le\widetilde s' in b['D14']
    assert r'z\perp\boldsymbol X' in b['D16'] and r'\sup_{|\boldsymbol v|_2=1}' in b['D16']
    assert r'\boldsymbol v_{-l}' in a['A1'] and r'a_n=\Theta(b_n)' in a['A1']
    assert r'N_l^-=\sum_{j=1}^m\mathbb I(Q_{l,j}=-1)' in a['A2']
    assert 'randomness comes from the selection' in a['A7']
    originals=data['claims']+list(members.values())+ambient['unranked_auxiliary_passages']
    for obj in originals:
        s=obj['statement_original']
        assert not re.search(r'[\u4e00-\u9fff]',s) and not any(ord(c)<32 and c!='\n' for c in s)
        assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
        for display,inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        assert all(1<=e['page']<=28 for e in obj['evidence'])
    for x in data['interfaces']:
        m=x['members'][0];own=m['statement_original']+' '+m['local_label']
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors)
        linked=own+' '+' '.join(c['statement_original'] for c in data['claims'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems']))
        assert all(s in linked for s in selectors)
        for r in x['related_theorems']:
            n=int(r['claim_id'].split('/T')[-1])
            assert r['relation']==('direct' if int(m['local_id'][1:]) in direct[n] else 'indirect')
            ex=x['theorem_explanations'][r['claim_id']]
            assert ex['via_local_ids']==r['via_local_ids'] and len(ex['text'])>50
        for k in x['source_keywords']:
            assert any(k['source_text'] in s for s in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=4,interfaces=len(data['interfaces']),source_members=len(members),
        direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),
        related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),
        unranked_auxiliary_passages=len(ambient['unranked_auxiliary_passages']))
    assert counts==dict(theorems=4,interfaces=16,source_members=16,direct_theorem_uses=12,related_theorem_connections=37,unranked_auxiliary_passages=8)
    assert len(ambient['source_issues'])==30 and set(ambient['statement_resolution'])=={'shared','1','2','3','4'}
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert len(rebuilt['comparisons'])==6
    for c in rebuilt['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Four original main-text Theorems were independently enumerated and visually reviewed, including the complete Theorem 4 continuation. External theorem citations in Lemma titles and prose were excluded. Main text and references end on page 28; no appendix body was read.',
        source_passages='Sixteen original source interfaces preserve machine-level privacy, the ternary sign matrix, strict majority and its support, distinct stability and utility formulas, Laplace noise, both general algorithms, quantization, the two model-specific algorithms, the local Lasso rule and two distinct distribution spaces. Eight auxiliary passages preserve vote counts, notation, model context and explanatory scope.',
        dependencies='Independent reconstruction checks 12 direct theorem uses and 37 related connections. Only Theorem 1 asserts the DGDP predicate. Theorem 2 targets the realized majority vector and s-bar; the later theorems target population signs. Algorithm bodies link through their actual local calls, without importing proof-only composition or sensitivity results.',
        names_and_highlights='Every interface uses source natural-language keywords, a faithful source heading and a meaningful source selector. The two distribution spaces retain distinct source definitions and keyword titles. Every related theorem has a source-backed direct explanation or a traced local dependency path.',
        notation='Visual comparison preserved strict majority ties, the opposite zero-sign score conventions, half-budget peeling and all exponential factors, unequal local sample sizes, third centered moments, the mean threshold inequality versus regression equality, random maximum penalty and its probability qualifier, and the continued diagonal condition.',
        limits='The printed threshold scope, unused gamma_1, unquantified Delta_0, omega_-l indexing, uncentered covariance notation, algorithm output representation, minimizer/penalty selection and parameter domains remain explicit source issues. No original claim was repaired and no proof correctness is certified.',
        reproduction='Six JSON content artifacts reproduce byte for byte from retained per-paper scripts. Registered source identity, independent inventory, exact claim handoff, source-specific invariants, local graph and reach, names/highlights, mathematical fragments and both structural validators passed.')
    write('evidence/manual-findings.json',findings)
    pages=[1,2,6,7,8,9,10,11,12,13,15,16,17,18,28]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
        source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=41,main_text_last_pdf_page=28,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent source heading enumeration and visual comparison of all complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
        counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),
        artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},
        source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,
        review_limits=['Main-text source census; proofs are not certified.','Original ambiguous hypotheses, definitions and notation are preserved with separate issue records.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,
        registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=41,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],
        checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},
        reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,
        reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
