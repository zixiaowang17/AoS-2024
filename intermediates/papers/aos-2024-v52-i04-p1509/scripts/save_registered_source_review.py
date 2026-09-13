"""Record the completed manual source review and independent census validation.

Hash pins identify content that was compared with the PDF. A rebuild or a new
hash alone cannot perform or renew this review.
"""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '8a24f229d677f4af2da260d91ad190bb996e3e4d2e199107b11f0d7766835933', 'source-passages.json': '39a9b4383bddb5c6c8dbe98dbfd526b10d0c0488078e52da78a7e9a6a9428bbb', 'interface-extraction.json': 'cd1718991ec43494472c983cc8f6d4068887fe1bea761a01980cfabd5763890a', 'ambient-prerequisites.json': 'ac1935db2f753341cdfd9f0538349bb2083ece58241d28b7909b5ee86cdba399', 'unfinalized-census.json': '52da5302c5967b18f12a9bb6e011cfd7a88a853067d4ea63bdf34e5f513d5b32', 'ranked-interfaces.json': '0d570ccea70ca6186a221e34e072699dc11a2dd780df393298bdba2951d17f4a'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):(ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def main():
    assert len(EXPECTED)==6
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Renew source review for changed content',name)
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    register=json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text());entry=next(x for x in register['papers'] if x['paper_id']==PID)
    assert digest(source)==entry['sha256']==SHA
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text());paper=inv['papers'][0]
    assert paper['version']=='arXiv:2303.13598v3, 4 July 2024' and entry['version']=='2303.13598v3.pdf'
    assert paper['source_url']=='https://arxiv.org/pdf/2303.13598v3' and entry['source_url']=='https://export.arxiv.org/pdf/2303.13598'
    ir=json.loads((ROOT/'inventory-review.json').read_text());assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==digest(ROOT/'theorem-inventory.json')
    pdf=fitz.open(source);assert len(pdf)==entry['pdf_pages']==paper['pdf_pages']==66
    first=' '.join(pdf[0].get_text().upper().split())
    assert all(s in first for s in [paper['title'].upper(),'MATIAS D. CATTANEO','MICHAEL JANSSON','KENICHI NAGASAWA','ARXIV:2303.13598V3'])
    assert paper['main_text_last_pdf_page']==20 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    headings=[]
    for n in range(1,21):
        p=pdf[n-1];clip=fitz.Rect(0,0,p.rect.width,670.2371826171875) if n==20 else p.rect
        source_text=p.get_text(clip=clip);path=ROOT/'evidence'/(f'page-{n:02}.txt' if n<20 else 'page-20-before-appendix.txt')
        assert path.read_bytes().decode()==source_text
        for b in p.get_text('dict',clip=clip)['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans']);m=re.match(r'^THEOREM (\d+)\.',s)
                if m:headings.append((n,m[1]))
    assert headings==[(9,'1')]
    assert source_text.rstrip().endswith('and this is another desirable feature of our proposed method.')
    assert 'APPENDIX A: TECHNICAL RESULTS AND OMITTED DETAILS' in pdf[19].get_text(clip=fitz.Rect(0,670,pdf[19].rect.width,684))
    assert len(inv['claims'])==len(data['claims'])==1
    original=inv['claims'][0];claim=data['claims'][0];assert all(claim[k]==v for k,v in original.items())
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Independently reconstructed from the main-text mathematical roles.
    local={1:[],2:[],3:[],4:[1,2,3],5:[],6:[5],7:[5],8:[4,1,2,3],9:[4,8,1,2,3],10:[4,5],12:[10,4,8,5,15],13:[9,5],14:[13,6,5],15:[]}
    direct={1,3,4,5,6,7,9,12,14,15}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in ids] for k,ids in local.items()}
    assert set(claim['depends_on'])=={f'D{i}' for i in direct}
    reach=set();stack=list(claim['depends_on'])
    while stack:
        lid=stack.pop()
        if lid not in reach:reach.add(lid);stack.extend(members[lid]['depends_on'])
    assert reach=={f'D{i}' for i in [1,2,3,4,5,6,7,8,9,10,12,13,14,15]}
    t=claim['statement_original'];b={lid:m['statement_original'] for lid,m in members.items()};a={x['local_id']:x['statement_original'] for x in ambient['unranked_auxiliary_passages']}
    assert t.startswith('Suppose Assumptions A, B, and C are satisfied. Then (2) and (7) hold, and')
    assert r'\sup_{t\in\mathbb R}' in t and r'=o_{\mathbb P}(1).\tag{8}' in t
    assert r'\widetilde\theta_n^*(\mathsf x)-\widehat\theta_n(\mathsf x)' in t and r'\widehat\theta_n(\mathsf x)-\theta_0(\mathsf x)' in t
    assert 'r_n' not in t and 'confidence' not in t and 'Theorem A.1' not in t
    assert 'greatest convex minorant' in b['D1'] and 'infimum of the empty set' in b['D2'] and r'\sup I' in b['D2']
    assert r'\partial_-' in b['D3'] and r'\mathfrak q' not in b['D3']
    assert r'\psi_0=\theta_0\circ\Phi_0^-' in b['D4'] and r'\Gamma_0=\Psi_0\circ\Phi_0' in b['D4']
    assert r'\Psi_0(x)=\int_0^x\psi_0(v)\,dv' in b['D4'] and r'\Phi_0(x)<\Phi_0(\mathsf x)<u_0' in b['D4']
    assert r'\widehat\Gamma_n\circ\widehat\Phi_n^-' in b['D4'] and r'\partial_-\mathsf{GCM}_{[0,\widehat u_n]}' in b['D4']
    assert r'\mathfrak q=\min\{j\in\mathbb N:\partial^j\theta_0(\mathsf x)\ne0\}' in b['D5'] and 'positive integers' in b['D5']
    assert r'\frac{\partial^{\mathfrak q}\theta_0(\mathsf x)\partial\Phi_0(\mathsf x)}{(\mathfrak q+1)!}v^{\mathfrak q+1}' in b['D6']
    assert all(f'(A{i})' in b['D7'] for i in [1,2,3])
    assert r'\lfloor\mathfrak s\rfloor-\mathfrak q+1' in b['D7'] and r'\partial\Phi_0(\mathsf x)\ne0' in b['D7']
    assert b['D7'].count(r'|x-x\prime|')==0 and b['D7'].count(r'\mathfrak s-\lfloor\mathfrak s\rfloor')==2
    assert 'generic (not necessarily nonparametric)' in b['D8']
    assert r'\widehat\theta_n(\mathsf x)\widehat\Phi_n(x)' in b['D9'] and r'\widehat\theta_n(\mathsf x)\widehat\Phi_n^*(x)' not in b['D9']
    assert r'\widetilde M_{\mathsf x,n}(x-\mathsf x)' in b['D9'] and r'\widetilde\Gamma_n^*\circ\widehat\Phi_n^{*-}' in b['D9']
    assert r'a_n=n^{1/(1+2\mathfrak q)}' in b['D10'] and b['D10'].count(r'\sqrt{na_n}')==2
    assert r'\theta_0(\mathsf x)\sqrt{na_n}' in b['D10'] and r'\widehat\theta_n(\mathsf x)\sqrt{na_n}' in a['A7']
    assert all(f'(B{i})' in b['D12'] for i in range(1,8)) and [e['page'] for e in members['D12']['evidence']]==[8,9]
    assert r'\beta<\mathfrak q+1' in b['D12'] and b['D12'].count(r'\sup_{V\in[1,a_n\delta]}')==2
    assert b['D12'].count(r'\mathbb 1_{\mathcal A_n}')==2 and r'\mathbb E_n^*' not in b['D12']
    assert r'\widehat u_n\ge u_0+o_{\mathbb P}(1)' in b['D12'] and r'\widehat u_n^*\ge\widehat u_n+o_{\mathbb P}(1)' in b['D12']
    assert r'\{0,\widehat u_n\}\subseteq\widehat\Phi_n(I)' in b['D12'] and 'are closed' in b['D12']
    assert r'\widehat\Phi_n(x)-\widehat\Phi_n(x-)' in b['D12'] and r'\widehat\Phi_n^*(x)-\widehat\Phi_n^*(x-)' in b['D12']
    assert r'\sqrt{na_n}\widetilde M_{\mathsf x,n}(va_n^{-1})' in b['D13']
    assert 'for some $c>0$ and every $K>0$' in b['D14']
    assert r'\liminf_{n\to\infty}\mathbb P' in b['D14'] and r'\inf_{|v|>K^{-1}}\widetilde M_{\mathsf x,n}(v)\ge cK^{-(\mathfrak q+1)}' in b['D14']
    assert r'C(|s|\wedge|t|)\mathbb 1(\operatorname{sign}(s)=\operatorname{sign}(t))' in b['D15'] and 'some $C>0$' in b['D15']
    for lid,label in [('D7','Assumption A'),('D12','Assumption B'),('D14','Assumption C')]:assert members[lid]['source_kind']=='assumption' and members[lid]['source_heading']==label
    assert r'r_n=n^{\mathfrak q/(1+2\mathfrak q)}' in a['A2'] and r'\tag{2}' in a['A2']
    assert r'\rightsquigarrow_{\mathbb P}' in a['A3'] and r'\tag{7}' in a['A3']
    assert all(r'\frac1{\partial\Phi_0(\mathsf x)}\partial_-\mathsf{GCM}_{\mathbb R}(\mathcal G_{\mathsf x}+\mathcal M_{\mathsf x}^{\mathfrak q})(0)' in a[lid] for lid in ['A2','A3'])
    assert 'uniform convergence on compacta' in a['A4'] and 'conditional on the original data' in a['A4']
    assert 'Appendix A.4' in a['A6'] and 'deliberately omits the rate term' in a['A8']
    assert 'D11' not in members and 'unnamed original formula' in next(x['note'] for x in ambient['unranked_auxiliary_passages'] if x['local_id']=='A7')
    for item in [claim,*members.values(),*ambient['unranked_auxiliary_passages']]:
        ev=list(item['evidence']);fragments=[item['statement_original']]
        for c in item.get('naming_context',[]):ev.extend(c['evidence']);fragments.append(c['text'])
        assert all(1<=e['page']<=20 and (e['page']<20 or e.get('before_main_text_end') is True) for e in ev)
        for s in fragments:
            assert not re.search(r'[\u4e00-\u9fff]',s) and not any(ord(c)<32 and c!='\n' for c in s)
            assert s.count('$')%2==0 and s.count(r'\[')==s.count(r'\]')
            for display,inline in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
                depth=0
                for brace in re.findall(r'(?<!\\)[{}]',display+inline):
                    depth+=1 if brace=='{' else -1
                    assert depth>=0
                assert depth==0
    for x in data['interfaces']:
        lid=x['members'][0]['local_id'];assert len(x['related_theorems'])==1 and x['related_theorems'][0]['claim_id']==PID+'/T1'
        assert x['related_theorems'][0]['relation']==('direct' if lid in claim['depends_on'] else 'indirect')
        assert set(x['theorem_explanations'])=={PID+'/T1'} and '$' not in x['name']
        assert {e['page'] for e in x['theorem_explanations'][PID+'/T1']['evidence']}>={5,7,9}
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label'];assert any(s in own for s in m['highlight_symbols']+m['highlight_phrases'])
        for k in x['source_keywords']:
            m=members[k['local_id']];assert any(k['source_text'] in s for s in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=1,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['unranked_auxiliary_passages']))
    assert counts==dict(theorems=1,interfaces=14,source_members=14,direct_theorem_uses=10,related_theorem_connections=14,unranked_auxiliary_passages=8)
    assert set(ambient['statement_resolution'])=={'shared','1'} and len(ambient['source_issues'])==18
    assert set(ambient['branch_resolution']['1']['conclusions'])=={'2','7','8'}
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text());assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        r=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True);validation.append(dict(artifact=name,returncode=r.returncode,stdout=r.stdout))
    findings=dict(
      inventory='Independent small-cap heading enumeration across all admitted main-text pages finds only Theorem 1 on page 9. Its original body ends with (8); both incorporated equations (2),(7) are saved separately in full. The following confidence-interval discussion is not appended to the theorem. The Appendix A heading shares page 20 and its body is excluded.',
      source_passages='Fourteen original interface passages and eight auxiliary passages were compared visually with pages 3-9. Assumptions A,B,C are complete, including all three and seven numbered clauses. The population/estimator definitions, corrected primitive, localized increments, drift, Brownian covariance, original rate and conditional limit are preserved.',
      dependencies='Independent reconstruction verifies 10 direct uses and 14 related connections. The theorem incorporates the operators and law in (2),(7), not only the symbols in (8). Its dependencies include all A-C conditions and generic bootstrap inputs, with the unnamed bootstrap-process formula resolved through auxiliary context. Later implementation assumptions, specific examples and appendix proof results are excluded.',
      names_and_highlights='All interface names come from original natural-language terms or original assumption labels. Every member has a meaningful matching source selector and a source-backed theorem explanation. The unnamed bootstrap empirical process is preserved without assigning it a neighboring term that refers to other objects.',
      notation='Visual and font checks distinguish sans-serif fixed x from italic running x, Fraktur q/s, calligraphic Gaussian/drift/covariance/events, estimated processes, hats and tildes. The correction uses unstarred Phi-hat, and the process/drift scale is sqrt(n a_n). The closed image conditions, jump controls, conditional probability and unscaled cdf comparison are retained.',
      limits='Eighteen notes record scope and source conventions. Exact localized domains and extension rules deferred to Appendix A.4 remain unresolved; appendix bodies were not read. The Holder diagonal convention, finite characteristic exponent and pointwise evaluation scope are retained without added hypotheses. This review does not certify proofs.',
      reproduction='All six content artifacts reproduce byte for byte from the retained per-paper scripts in an empty directory. Source identity, independent inventory, original claim identity, manually reconstructed graph, source-specific invariants, math fragments and inventory/census schema checks passed. Rebuilding does not itself renew source review.')
    write('evidence/manual-findings.json',findings)
    pages=[1,3,4,5,6,7,8,9,20];evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png'),**({'before_main_text_end':True} if n==20 else {})) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
      source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=66,main_text_last_pdf_page=20,provenance_path='evidence/source-provenance.json'),
      enumeration=dict(theorem_ids=[PID+'/T1'],printed_label_check=headings,method='Independent actual-heading enumeration and visual comparison of the complete theorem and incorporated formulas.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
      counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,review_limits=['Original source and statement-dependency review, not proof certification.','Appendix bodies and external proofs excluded.','Exact localized-domain conventions deferred to the appendix remain unresolved.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=66,source_version=paper['version'],registered_version_alias=entry['version'],registered_url_alias=entry['source_url'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
