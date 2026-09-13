"""Verify frozen, source-reviewed content using independent branch and graph checks."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,REPO,PID,SHA,URL
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '4e31d37e8b2ae54d7401aaf7cc18f5f86bab1923c11cc0a4ff51f701f27c6bea', 'source-passages.json': '5db8c2c8789f48f4cb85608f1c341266406a0410a4b457488d28efe8a7065c90', 'interface-extraction.json': 'c8e7c354c50745009929d84d5c53c05a2aeb633d7959319b13908423c14801eb', 'ambient-prerequisites.json': '3d41c59131f7468ea555c040110fef10aa26674bc6cfee5cbba9ff3eb46b8878', 'unfinalized-census.json': '2b4dc9b2d5498b1ac3058dfe74cef8d9172dd3900dde90245be1cc372b8e2084', 'ranked-interfaces.json': '53e79a30759a8a43361f0ab349b18b4d6fcaa3cc82a4e892946d05cb59c32104'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def ids(ns):return {'D'+str(n) for n in ns}
def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    import review_inventory
    review_inventory.main()
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    registered=next(x for x in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers'] if x['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2110.11816v2.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2110.11816'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    d=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['source_checked'] and ir['status']=='complete' and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']==URL and paper['pdf_pages']==registered['pdf_pages']==40
    assert paper['main_text_last_pdf_page']==22 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    assert len(inv['claims'])==len(d['claims'])==2
    for original,c in zip(inv['claims'],d['claims']):assert {k:v for k,v in c.items() if k!='depends_on'}==original
    m={a['local_id']:a for x in d['interfaces'] for a in x['members']}
    # Independently reconstructed from the original source definitions and statement clauses.
    raw={1:[],2:[1],3:[],4:[2],5:[3],6:[3],7:[],8:[3,4,5,6,7],9:[5],10:[9],11:[2,5,8],12:[],13:[3,12],14:[3,4,5,7,12,13]}
    local={'D'+str(k):ids(v) for k,v in raw.items()}
    direct={'1':ids([2,5,8,9]),'2':ids([2,10,11,14])}
    expected_reach={'1':ids([1,2,3,4,5,6,7,8,9]),'2':ids([1,2,3,4,5,6,7,8,9,10,11,12,13,14])}
    assert {lid:set(a['depends_on']) for lid,a in m.items()}==local
    for c in d['claims']:
        n=c['claim_id'].split('/T')[-1];assert set(c['depends_on'])==direct[n]
        reach=set();stack=list(direct[n])
        while stack:
            lid=stack.pop()
            if lid not in reach:reach.add(lid);stack.extend(local[lid])
        actual={x['members'][0]['local_id'] for x in d['interfaces'] if any(r['claim_id']==c['claim_id'] for r in x['related_theorems'])}
        assert reach==actual==expected_reach[n],n
    assert not ids([10,11,12,13,14]) & expected_reach['1']
    assert ids([10,11,12,13,14]) <= expected_reach['2']
    assert 'D8' not in direct['2'] and 'D8' in expected_reach['2']
    assert not ({'D6','D8'} & local['D14'])
    aux={a['local_id']:a for a in ambient['unranked_auxiliary_passages']}
    assert len(aux)==8 and len(ambient['source_issues'])==9
    source_specific_checks(m,aux,ambient)
    for obj in list(m.values())+d['claims']+list(aux.values()):
        t=obj['statement_original'];assert not re.search(r'[\u4e00-\u9fff]',t)
        assert not any(ord(ch)<32 and ch!='\n' for ch in t)
        assert t.count('$')%2==0 and t.count(r'\[')==t.count(r'\]')
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',t,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        assert obj['evidence'] and all(1<=e['page']<=22 for e in obj['evidence'])
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
                assert all(1<=e['page']<=22 for e in ctx['evidence'])
            else:assert kw['source_text'] in a['statement_original']
        assert x['name']==' · '.join(k['label'] for k in x['source_keywords'])
    counts=dict(theorems=2,interfaces=len(d['interfaces']),source_members=len(m),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in d['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in d['interfaces']),unranked_auxiliary_passages=len(aux))
    assert counts==dict(theorems=2,interfaces=14,source_members=14,direct_theorem_uses=8,related_theorem_connections=23,unranked_auxiliary_passages=8),counts
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert len(rebuilt['comparisons'])==6
    for row in rebuilt['comparisons']:assert row['matches_saved_bytes'] and row['saved_sha256']==row['regenerated_sha256']==digest(ROOT/row['artifact'])
    assert len(list((ROOT/'scripts').glob('*.py')))==7
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
      inventory='Two complete main-text Theorems1 and2, independently enumerated by bold headings. Citations, proof headings, propositions and lemmas are excluded. Main text includes numerical results and acknowledgment through the clipped shared PDF page22; AppendixA begins afterward.',
      source_passages='Fourteen original entries preserve the correlated graph model, null/alternative laws, graph isomorphism and automorphisms, centered matrices, unlabeled tree family, weighted subgraph count, scaling beta, exact statistic, Otter constant, condition(7), threshold, uniform colorings and colorful counts, and the normalized randomized approximation. Eight auxiliary passages retain source conventions and computation provenance.',
      dependencies='Independent reconstruction verifies8 direct uses and23 related connections. Theorem1 defines condition(7) and its threshold inline; Theorem2 imports those specific excerpts. Both use the original observation laws. Exact f_T is indirectly needed by Theorem2 through its threshold, but no proof-only likelihood-ratio, low-degree conjecture or approximation-proposition dependency is added.',
      scope='Preserve conditional aligned-edge independence under the latent permutation, the Bernoulli feasibility range for negative rho, K edges versus K+1 vertices, unrooted isomorphism classes, explicit aut(H) weights and signed centered edge products. The approximation uses2t independent colorings, shared across trees, and the product of two sample averages with beta/r² normalization.',
      source_issues='Nine notes record the pinned arXiv date, latent-mixture and negative-correlation domain, copy multiplicity and signed-count semantics, exact K/sparsity and nonuniform threshold scope, strict versus non-strict error events, implicit algorithmic randomness in P/Q, independent coloring arrays, output/normalization and supplied-parameter requirements, and proof/computation limits including the excluded appendix(54) reference.',
      names_and_highlights='All14 entries retain source natural-language terms, original source kinds/headings and literal meaningful selectors. Condition(7) and tau are explicitly Theorem1 excerpts. Every related theorem has a checked source explanation and exact same-paper path.',
      reproduction='All six content JSON artifacts reproduce byte for byte in a fresh directory. Seven retained scripts preserve extraction, inventory review, definitions, context, finalization, reproduction and independent frozen-hash source review.')
    reviewed_pages=[1,2,3,4,5,6,7,8,15,16,22]
    write('evidence/manual-findings.json',dict(paper_id=PID,findings=findings,appendix_material_used=False,visually_reviewed_pdf_pages=reviewed_pages,visually_reviewed_crops=[]))
    evidence=[dict(path='evidence/page-'+str(n).zfill(2)+'.jpg',page=n) for n in reviewed_pages]
    evidence.append(dict(path='evidence/manual-findings.json'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(source),source_url=URL,version=paper['version'],pdf_sha256=SHA,pdf_pages=40,main_text_last_pdf_page=22,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=ir['printed_label_check'],method='Independent bold-font heading enumeration and visual comparison of both complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark','Conjecture'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],ambient_resolution=ambient['statement_local_bindings'],source_claim_references=ambient['source_claim_references'],evidence=evidence,review_limits=['Registered arXiv:2110.11816v2, marked2 Apr2022, with cover dated April5,2022, pinned by SHA-256. No source substitution.','Main text and acknowledgment end on shared PDF page22, clipped at y565 before AppendixA at y574.126. Appendix bodies, including the forward reference to equation(54), are excluded.','Source and schema validation do not certify proofs, the external algorithm routines or a finite-precision runtime bound, and do not add unstated threshold uniformity.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=40,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
def source_specific_checks(m,aux,ambient):
    s={k:v['statement_original'] for k,v in m.items()}
    checks={
1:['latent uniform random permutation',r'(A_{ij},B_{\pi(i)\pi(j)})','Conditioned on the permutation',r'1\le i<j\le n',r'q\in(0,1)'],
2:['independently generated',r'\mathcal G(n,q,\rho)',r'\mathcal Q$ and $\mathcal P','respectively'],
3:[r'\pi:V(H)\to V(H\prime)',r'\operatorname{aut}(H)','number of automorphisms','isomorphism class'],
4:[r'\overline A=A-\mathbb E[A]',r'\overline B=B-\mathbb E[B]'],
5:['set of unlabeled trees with $K$ edges',r'\mathcal T'],
6:[r'\sum_{S\cong H}\prod_{(i,j)\in S}M_{ij}','subgraphs of $K_n$','weighted adjacency matrix'],
7:[r'\left(\frac{\rho}{q(1-q)}\right)^K',r'\frac{(n-K-1)!}{n!}'],
8:[r'\sum_{[H]\in\mathcal T}',r'\beta\operatorname{aut}(H)W_H(\overline A)W_H(\overline B)'],
9:[r'\lim_{K\to\infty}|\mathcal T|^{1/K}=1/\alpha',r'\alpha\approx0.33833'],
10:[r'n\min\{q,1-q\}\ge n^{-o(1)}',r'\rho^2>\alpha',r'\omega(1)\le K',r'16\log\log n\vee2\log',r'\frac1{n\min\{q,1-q\}}'],
11:[r'\tau=C\mathbb E_{\mathcal P}[f_{\mathcal T}(A,B)]=C\rho^{2K}|\mathcal T|','any fixed constant $0<C<1$'],
12:[r'\mu:[n]\to[K+1]','independently and uniformly',r'\mu(x)\ne\mu(y)',r'\frac{(K+1)!}{(K+1)^{K+1}}'],
13:[r'K+1','\n(30)',r'\sum_{S\cong H}\chi_\mu(V(S))\prod_{(i,j)\in E(S)}M_{ij}'],
14:[r't\triangleq\lceil1/r\rceil',r'$2t$ random colorings',r'\{\mu_i\}_{i=1}^t',r'\{\nu_j\}_{j=1}^t','independent copies',r'\left(\frac1t\sum_{i=1}^tX_H(\overline A,\mu_i)\right)\left(\frac1t\sum_{j=1}^tX_H(\overline B,\nu_j)\right)',r'\frac{\beta}{r^2}Y_{\mathcal T}(A,B)']}
    checks[3][0]=r"\pi:V(H)\to V(H')"
    for n,parts in checks.items():
        for v in parts:assert v in s['D'+str(n)],(n,v)
    assert m['D2']['source_kind']=='source_passage'
    assert m['D10']['source_kind']==m['D11']['source_kind']=='theorem_excerpt'
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());t1=inv['claims'][0]['statement_original']
    assert s['D10'] in t1 and s['D11'] in t1
    assert not any('conjecture' in x.lower() for x in s.values())
    a={k:v['statement_original'] for k,v in aux.items()}
    ac={1:[r'[-\min\{\frac q{1-q},\frac{1-q}q\},1]','allow negative correlation'],2:[r'\mathcal P(f(G_1,G_2)<\tau)','consistent detection'],3:[r'\binom n{|V(H)|}\frac{|V(H)|!}{\operatorname{aut}(H)}','edge-induced','no isolated vertices'],4:[r'a\vee b\triangleq\max\{a,b\}',r'a_n/b_n\to0'],5:['Proposition 3',r'\mathbb E_{\mathcal P}[f_{\mathcal T}]}\xrightarrow{L_2}0','both $\mathcal P$ and $\mathcal Q$'],6:['Algorithm 1','unrooted unlabeled trees','i.i.d. random colorings','Algorithm 2','Output: $Y_{\mathcal T}(A,B)$'],7:['Proposition 4',r'O(n^2(3e/\alpha)^K)',r'n^{2+o(1)}'],8:[r'\mathbb E[X_H(M,\mu)\mid M]=rW_H(M)','unbiased estimator']}
    for n,parts in ac.items():
        for v in parts:assert v in a['A'+str(n)],(n,v)
    for obj in aux.values():assert set(obj['depends_on'])<=set(m)
    assert set(ambient['statement_local_bindings'])=={'T1','T2'}
    assert {x['issue_id'] for x in ambient['source_issues']}=={'registered-version-and-main-boundary','latent-mixture-and-correlation-domain','signed-counts-and-copy-multiplicity','parameter-and-tree-size-scope','threshold-and-inequality-conventions','algorithmic-randomness-in-laws','independent-coloring-averages','scaling-and-algorithm-output','computational-and-proof-scope'}
    refs=ambient['source_claim_references']
    assert sum(x['reference_kind']=='definition_reference' for x in refs)==4
    assert sum(x['reference_kind']=='assumption_reference' for x in refs)==1
    assert sum(x['reference_kind']=='proof_only' for x in refs)==1
    assert sum(x['reference_kind']=='computation_reference' for x in refs)==1
if __name__=='__main__':main()
