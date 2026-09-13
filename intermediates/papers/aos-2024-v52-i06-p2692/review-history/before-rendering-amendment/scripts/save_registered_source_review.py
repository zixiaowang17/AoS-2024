"""Check frozen source-reviewed content and independently reconstruct theorem reach."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '16500150962804eeebb53cc6021d7c03f113a41b98911323cb7be34dad9e3752', 'source-passages.json': '60a1f90f75bd99097ac597bec695fa703f44112128bf6cd10622af2a20795b8b', 'interface-extraction.json': 'e9584dd3d079aa51dc7310459a1c5d60ae27fc9ba313be45b87efe5c6b67d093', 'ambient-prerequisites.json': 'cc117c5e39e035f80475345c798ab52141e8af06680c239d7c6627dd9884eef8', 'unfinalized-census.json': '495af7eb49ec45788c78b99a7930fa995cce167b2c86e3a073b7b1ea353a3b78', 'ranked-interfaces.json': '617cddff07ec94ff381239f4da5a39963312f601f0ced097c400590dc51f311e'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def source_specific_checks(m,aux,ambient,t):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:['unit sphere',r'\mathbb R^{d+1}',r'R\in\mathbb R^+',r'R\frac{z_1}{1-z_{d+1}}',r'J_{\mathrm{SP}}(x)\propto(R^2+\|x\|^2)^d',r'\frac{2Rx_i}{\|x\|^2+R^2}',r'\frac{\|x\|^2-R^2}{\|x\|^2+R^2}'],
2:[r'x=\mathrm{SP}(z)',r'\pi_S(z)\propto\pi(x)(R^2+\|x\|^2)^d'],
3:[r'z:=\mathrm{SP}^{-1}(x)',r'\mathcal N(0,h^2I_{d+1})',r'\frac{(z^T\cdot\mathrm d\widetilde z)z}{\|z\|^2}',r'\frac{z+\mathrm dz}{\|z+\mathrm dz\|}',r'\widehat X:=\mathrm{SP}(\widehat z)',r'\pi(\widehat X)(R^2+\|\widehat X\|^2)^d',r'\pi(x)(R^2+\|x\|^2)^d','otherwise'],
4:[r'\forall\epsilon>0',r'N\in\mathbb N',r'\|P^N(x,\cdot)-\pi\|_{\mathrm{TV}}\le\epsilon,\forall x\in E',"chain's (unique) invariant distribution"],
5:[r'v^{(0)}\cdot z^{(0)}=0',r'\|v^{(0)}\|=1',r'\sin(t)v^{(i-1)}+\cos(t)z^{(i-1)}',r'\cos(t)v^{(i-1)}-\sin(t)z^{(i-1)}',r'\max\{0,[-v\cdot\nabla_z\log\pi_S(z)]\}',r'\mathrm{Exponential}(\lambda_{\mathrm{refresh}})',r'\mathrm{Uniform}\{v:z^{(i)}\cdot v=0,\|v\|=1\}',r'v_{\mathrm{temp}}-2',r'\widetilde\nabla_z\log\pi_S(z^{(i)})\cdot\widetilde\nabla_z\log\pi_S(z^{(i)})',r'\sum_{j=1}^i\tau_j\ge T','exit'],
6:['transition semi-group',r'\forall\epsilon>0',r'\|P^T(x,\cdot)-\pi\|_{\mathrm{TV}}\le\epsilon,\forall x\in E'],
7:[r'-\frac12(x-\mu)^T\Sigma^{-1}(x-\mu)',r'\Sigma=\operatorname{Diag}(\lambda_1,\ldots,\lambda_d)',r'\mu=(\mu_1,\ldots,\mu_d)^T'],
8:[r'\pi(x)=\prod_{i=1}^df(x_i)'],
9:['Without loss of generality',r'\mathbb E_f(X^2)=\int x^2f(x)\,\mathrm dx=1',r'\mathbb E_f(X^6)<\infty'],
10:[r"f'/f",'Lipschitz continuous',r"\lim_{x\to\pm\infty}xf'(x)=0",r"\left(\frac{f'(X)}{f(X)}\right)^8",r"\left(\frac{f''(X)}{f(X)}\right)^4",r"\left(\frac{Xf'(X)}{f(X)}\right)^4"],
11:['full support',r'\mathbb R'],
12:[r'\frac1{\sqrt{d-1}}',r'\frac1{\left(1-\frac{\ell^2}{2d}\frac{4\lambda}{(1+\lambda)^2}\right)^2}-1',r'\frac1{\sqrt{1+h^2(d-1)}}=1-\frac{\ell^2}{2d}\frac{4\lambda}{(1+\lambda)^2}','fixed constant'],
13:[r'\mathbb E_{X\sim\pi}\mathbb E_{\widehat X\mid X}',r'\|\widehat X-X\|^2\left(1\wedge',r'\pi(\widehat X)(R^2+\|\widehat X\|^2)^d',r'\pi(X)(R^2+\|X\|^2)^d'],
14:[r"\mathrm d\widetilde z',\mathrm d\widetilde z''",r"\mathrm dz':=\mathrm d\widetilde z-",r"\mathrm dz'':=\mathrm d\widetilde z-",r"\widehat X:=(\widehat X'_1,\widehat X''_{2:d})",r'\pi(\widehat X)(R^2+\|\widehat X\|^2)^d','otherwise']}
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert set(checks)==set(range(1,15))
    for n in [8,9,10,11]:assert m['D'+str(n)]['source_kind']=='assumption'
    for n in [3,5,7,14]:assert m['D'+str(n)]['source_kind']=='source_passage'
    assert m['D13']['source_kind']=='definition' and m['D13']['source_heading'].startswith('Definition 5.1')
    assert 'isotropic' not in s['D11'] and 'mean zero' not in s['D9']
    assert "\\widehat X'_1" not in s['D3'] and 'pi_S' not in s['D3']
    assert r"\mathrm dz':=\mathrm d\widetilde z'-" not in s['D14']
    assert r"\mathrm dz'':=\mathrm d\widetilde z''-" not in s['D14']
    a={k:v['statement_original'] for k,v in aux.items()}
    assert r'\mathbb S^d\setminus N' in a['A1']
    assert 'independently of $x$' in a['A2'] and 'refresh rate is constant' in a['A2']
    assert r'\lambda_{\mathrm{refresh}}>0' in a['A3'] and 'joint density' in a['A3']
    assert r'R=\sqrt{\lambda d}' in a['A4']
    assert 'conditional on the current state' in a['A5'] and 'two independent proposals' in a['A5']
    assert a['A6'] in t['5.2'] and 'cumulative density function' in a['A6']
    assert 'conjecture' in a['A7'] and 'open problem' in a['A7']
    assert 'step size $h$ on the unit sphere' in a['A8']
    assert r'\mathbb E[\|\widehat X-X\|^2]\cdot\mathbb E' in a['A9']
    assert 'not irreducible' in a['A10']
    assert all(set(x['depends_on'])<=set(m) for x in aux.values())
    assert set(ambient['statement_local_bindings'])=={'T2.1','T2.2','T4.1','T5.1','T5.2'}
    assert ambient['unresolved_external_prerequisites']==[]
    assert len([x for x in ambient['source_claim_references'] if x['reference_kind']=='proof_only'])==5
    assert 'lambda_{\\mathrm{refresh}}' not in t['2.2'] and 'Eq. (15)' not in t['5.2']

def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2205.12112v2.pdf'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==80
    assert paper['main_text_last_pdf_page']==24 and paper['main_text_boundary']['shared_page_with_appendix'] is False
    assert len(inv['claims'])==len(d['claims'])==5
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independent reconstruction from inspected source clauses; no finalizer import.
    raw={1: [], 2: [1], 3: [1], 4: [], 5: [1, 2], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: [], 13: [3], 14: [1]}
    local={"D"+str(k):ids(v) for k,v in raw.items()}
    direct={k:ids(v) for k,v in {'2.1': [3, 4], '2.2': [5, 6], '4.1': [3, 7], '5.1': [3, 8, 9, 10, 11, 12, 13], '5.2': [8, 9, 10, 11, 12, 14]}.items()}
    expected_reach={k:ids(v) for k,v in {'2.1': [1, 3, 4], '2.2': [1, 2, 5, 6], '4.1': [1, 3, 7], '5.1': [1, 3, 8, 9, 10, 11, 12, 13], '5.2': [1, 8, 9, 10, 11, 12, 14]}.items()}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([2,4,5,6,8,9,10,11,12,13,14])&expected_reach['4.1']
    assert not ids([2,4,5,6,7,14])&expected_reach['5.1']
    assert not ids([2,3,4,5,6,7,13])&expected_reach['5.2']
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']};assert len(aux)==10 and len(ambient['source_issues'])==14
    source_specific_checks(m,aux,ambient,{c['claim_id'].split('/T')[-1]:c['statement_original'] for c in inv['claims']})
    for obj in list(m.values())+d['claims']+list(aux.values()):
        t=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',t)
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        assert obj['evidence'] and all(1<=e['page']<=24 for e in obj['evidence'])
    for x in d['interfaces']:
        assert len(x['members'])==1
        a=x['members'][0];lid=a['local_id'];own=a['statement_original']+' '+a['local_label']
        linked=own+' '+' '.join(c['statement_original'] for c in d['claims'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems']))
        selectors=a['highlight_symbols']+a['highlight_phrases'];assert any(v in own for v in selectors) and all(v in linked for v in selectors)
        assert {u['claim_id'] for u in x['central_claim_uses']}=={PID+'/T'+n for n,v in direct.items() if lid in v}
        assert set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
        for rel in x['related_theorems']:
            n=rel['claim_id'].split('/T')[-1];path=rel['via_local_ids']
            assert rel['relation']==('direct' if lid in direct[n] else 'indirect')
            assert path[0] in direct[n] and path[-1]==lid and all(b in local[a] for a,b in zip(path,path[1:]))
            ex=x['theorem_explanations'][rel['claim_id']];assert ex['via_local_ids']==path and ex['text'].strip() and ex['evidence']
            assert 'This theorem directly uses the API.' not in ex['text']
        for kw in x['source_keywords']:
            if 'context_id' in kw:
                ctx=next(v for v in a['naming_context'] if v['context_id']==kw['context_id']);assert kw['source_text'] in ctx['text']
                assert all(1<=e['page']<=24 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=5,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=5,interfaces=14,source_members=14,direct_theorem_uses=19,related_theorem_connections=25,unranked_auxiliary_passages=10),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings={'inventory': 'Five complete main-text Theorems2.1,2.2,4.1,5.1,5.2 independently enumerated from small-cap headings and visually compared. Main text ends on24 after Acknowledgement; supplementary proofs starting25 are excluded.', 'source_passages': 'Fourteen original entries and ten auxiliary passages preserve the radius-indexed stereographic map and inverse, transformed target, complete SPS/SBPS/RSPS algorithms, both uniform-ergodicity definitions, Gaussian target, all Section5.1 assumptions, Eq15 scaling and exact ESJD.', 'dependencies': 'Independent source-clause reconstruction verifies19 direct uses and25 related-theorem connections. SPS has no imported SBPS gradient or transformed-density definition when its acceptance ratio is printed directly. T4.1 does not import GSPS or Section5.1 assumptions. T5.2 uses RSPS and does not inherit original SPS or ESJD as statement dependencies.', 'source_issues': 'Fourteen source notes preserve refreshment and velocity-space ambiguities, north-pole/zero-gradient/stopping conventions, nondegenerate SPS scale, Gaussian-bound denominator conventions, conflicting surrounding examples, score domains, scaling branch restrictions and unprimed RSPS increments. Source assertions are not certified as correct algorithms.', 'diffusion': 'T5.1 proves an exact ESJD limit for SPS, distinct from the earlier product-of-expectations approximation. T5.2 states a diffusion limit for RSPS; the original SPS analogue remains a conjecture. The original Phi wording and the implicit continuing ell scaling are preserved and explained separately.', 'names_and_highlights': 'All14 entries have literal natural-language source terms, original kinds/headings and matching selectors. Every one of25 related links has a valid same-paper path and a source-specific explanation.', 'reproduction': 'All six content JSON files reproduce byte for byte in an empty directory. Seven retained scripts support inventory, extraction, ambient context, finalization, rebuilding and independent source review. Rebuilding is not a new semantic source review.'}
    reviewed_pages=[1,2,5,6,7,8,9,10,14,15,16,17,19,20,21,24]
    crops=[]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=crops))
    evidence=[dict(path=f'evidence/page-{n:02}.jpg',page=n) for n in reviewed_pages]+crops+[dict(path='evidence/manual-findings.json')]
    for item in evidence:assert (ROOT/item['path']).is_file()
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=80,main_text_last_pdf_page=24,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent actual small-cap heading enumeration and visual comparison of all five complete statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv2205.12112v2 marked21Feb2024,80pages, pinned bySHA256; not silently exchanged for the published article.','Main text ends with Acknowledgement on page24. Supplementary proofs starting25 and additional simulations starting62 are excluded. No required theorem assumption is imported from a supplementary proof.','Source review preserves mathematical statements, dependencies and unresolved source notation; it does not certify proofs or solve implicit selection/domain conventions.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=80,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
