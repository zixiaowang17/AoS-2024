"""Record the completed manual review of the published source and its consistency checks.

This records an already performed source-content review; running it alone does not
substitute for checking the PDF. rebuild.py regenerates content without review status.
"""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in Path(__file__).resolve().parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i03-p1152'
SKILL=Path('skills/statistical-paper-census/scripts')
ARTIFACTS=['theorem-inventory.json','source-passages.json','interface-extraction.json','ambient-prerequisites.json','unfinalized-census.json','ranked-interfaces.json']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,value):(ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def main():
    PDF=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    register=json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())
    entry=next(x for x in register['papers'] if x['paper_id']==PID)
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==digest(ROOT/'theorem-inventory.json')
    assert digest(PDF)==entry['sha256']==paper['pdf_sha256']=='040bf11f4fea87c491051c19fc2b5a4e5398d46dac450a12a39814bf583c1a5e'
    assert paper['version']==entry['version'] and paper['source_url']==entry['source_url']
    pdf=fitz.open(PDF);assert len(pdf)==paper['pdf_pages']==entry['pdf_pages']==26
    first=' '.join(pdf[0].get_text().split());assert paper['title'].upper() in first
    assert all(n in first for n in ['HAIHAN YU','MARK S. KAISER','DANIEL J. NORDMAN','10.1214/24-AOS2388','revised April 2024'])
    assert paper['main_text_last_pdf_page']==22 and paper['main_text_boundary']['shared_page_with_appendix'] is True
    assert 'APPENDIX A:' in pdf[21].get_text(clip=fitz.Rect(0,241.31422424316406,pdf[21].rect.width,253))
    labels=[];other=[]
    for n in range(1,23):
        p=pdf[n-1];clip=fitz.Rect(0,0,p.rect.width,241.31422424316406) if n==22 else p.rect
        assert (ROOT/'evidence'/f'page-{n:02}.txt').read_bytes().decode()==p.get_text(clip=clip)
        for block in p.get_text('dict',clip=clip)['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans']).strip()
                m=re.match(r'^THEOREM\s+(\d+)\.',text)
                if m:labels.append((n,m[1]))
                if text.startswith('COROLLARY '):other.append((n,text))
    assert labels==[(9,'1'),(10,'2'),(13,'3'),(20,'4')]
    assert len(other)==1 and other[0][0]==11 and other[0][1].startswith('COROLLARY 1.')
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==labels
    assert len(inv['claims'])==len(data['claims'])==4
    for original,final in zip(inv['claims'],data['claims']):
        for key in original:assert original[key]==final[key],(original['claim_id'],key)
    members=[m for x in data['interfaces'] for m in x['members']];byid={m['local_id']:m for m in members}
    claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
    extraction=json.loads((ROOT/'interface-extraction.json').read_text())
    assert {m['local_id']:m for x in extraction['interfaces'] for m in x['members']}==byid
    reach={}
    for n,c in claims.items():
        seen=set();stack=c['depends_on'][:]
        while stack:
            lid=stack.pop()
            if lid in seen:continue
            seen.add(lid);stack.extend(byid[lid]['depends_on'])
        reach[n]=seen
    # Independently specified after source review: the bare SEL limit has no fit;
    # M-estimation has no blocks; smooth-profile resampling is an entire-function experiment.
    expected={
     '1':{1,2,3,4,7,8,9,10,11,12,13,14,15},
     '2':{1,2,3,4,5,6,11,12,13,14,15,16,17},
     '3':set(range(1,23)),
     '4':{1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,17,18,19,23,24,25,26}}
    direct={
     '1':{4,7,10,12,13,15},'2':{4,12,13,15,16,17},
     '3':{4,7,10,12,13,15,16,17,22},'4':{4,7,12,13,15,17,23,24,26}}
    assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()},reach
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    for x in data['interfaces']:
        lids={m['local_id'] for m in x['members']}
        assert {r['claim_id'].split('/T')[-1] for r in x['related_theorems']}=={n for n in claims if reach[n]&lids}
        assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if set(c['depends_on'])&lids}
    assert reach['1'].isdisjoint({f'D{i}' for i in [5,6,16,17,18,19,20,21,22,23,24,25,26]})
    assert reach['2'].isdisjoint({f'D{i}' for i in [7,8,9,10,18,19,20,21,22,23,24,25,26]})
    assert reach['4'].isdisjoint({'D10','D20','D21','D22'})
    assert 'D16' not in byid['D19']['depends_on'] and 'D6' not in byid['D8']['depends_on']
    t={n:c['statement_original'] for n,c in claims.items()};b={lid:m['statement_original'] for lid,m in byid.items()};a={x['local_id']:x['statement_original'] for x in ambient['auxiliary_source_passages']}
    assert all(len(c['evidence'])==1 for c in claims.values())
    assert 'Assumptions 1–3' in t['1'] and 'spectral moment condition (2)' in t['1']
    assert r'b/n+n/b^2\to0' in t['1'] and r'\chi_p^2' in t['1']
    for part in ['(i)','(ii)','(iii)','(iv)']:assert part in t['2'] and part in b['D17']
    assert 'there exists a solution sequence' in t['2']
    assert r'\partial^2G_\theta(\cdot)/\partial\theta\partial\theta^\intercal' in t['2']
    assert r'H(\cdot):[-\pi,\pi]\mapsto\mathbb R^+' in t['2']
    assert r'\mathcal N(0_p,\Sigma_{\theta_0})' in t['2']
    assert r'(D_{\theta_0}^\intercal V_{\theta_0}^{-1}D_{\theta_0})^{-1}' in t['2']
    assert 'Under assumptions of Theorem 2' in t['3']
    assert r'b/n+n/b^2\to0' in t['3']
    assert r'\sup_{x\in\mathbb R}' in t['3'] and r'\mathbb P_*(\ell_n^*(\widehat\theta_n)\le x)' in t['3']
    assert r'\xrightarrow{p}0' in t['3']
    assert 'Assumptions for Theorem 3' in t['4']
    assert r'b/n+n/b^2\to\infty' in t['4'] and r'\chi_u^2' in t['4']
    assert r'\mathbb R^p\mapsto\mathbb R^s' in t['4']
    assert r'\partial h(\theta)/\partial\theta|_{\theta=\theta_0}' in t['4']
    assert 'constant rank' not in t['4']
    assert 'absolutely summable autocovariances' in b['D1'] and 'weakly stationary' in b['D1']
    assert r'\mathcal M_\theta\equiv(m_1(\theta),\ldots,m_p(\theta))^\intercal' in b['D3']
    assert 'at the true value' in b['D4']
    assert r'(2\pi n)^{-1}' in b['D5'] and r'\imath=\sqrt{-1}' in b['D5']
    assert r'\sum_{|j|=1}^{\lfloor n/2\rfloor}' in b['D6'] and 'both positive/negative frequencies' in b['D6']
    assert r'N\equiv\lfloor n/b\rfloor' in b['D7'] and r'\frac1{2\pi b}' in b['D7']
    assert r'T_{i,\mathrm{NOL}}(\theta)' in b['D8'] and r'\frac{2\pi}b' in b['D8']
    assert 'conditioning set' in b['D9'] and r'L_n(\theta)=0' in b['D9']
    assert r'\ell_n(\theta)\equiv-2\log[N^N L_n(\theta)]' in b['D10']
    assert r'\sup_{m\in\mathbb Z}' in b['D11'] and r'\mathcal F_{m+k}^\infty' in b['D11']
    assert r'\sup_{t\in\mathbb Z}\mathbb E|X_t|^{4+\delta}' in b['D12'] and r'k^2\alpha(k)^{\delta/(4+\delta)}' in b['D12']
    assert '4th-order stationary series' in b['D12'] and 'strictly' not in b['D12']
    assert 'At the true parameter' in b['D13'] and 'bounded variation' in b['D13']
    assert r'(2\pi)^{-3}' in b['D14'] and r'\operatorname{cum}(X_0,X_{h_1},X_{h_2},X_{h_3})' in b['D14']
    assert r'G_{\theta_0}(-\lambda)' in b['D15'] and r'f_4(\lambda_1,\lambda_2,-\lambda_2)' in b['D15']
    assert r'V_{\theta_0}\equiv V_{\theta_0,1}+V_{\theta_0,2}' in b['D15']
    assert r'T_n(\theta)=\mathcal M_\theta' in b['D16']
    assert r'-\partial\mathcal M_{\theta_0}/\partial\theta' in b['D17']
    assert r'(2\pi/b)' in b['D18'] and r'X_{s-1+i}' in b['D18']
    assert '4π²' in byid['D18']['variant_note']
    assert r'\mathcal C_{\mathrm{OL}}' in b['D20']
    assert 'i.i.d. draws' in b['D21'] and r'\}_{i=1}^N' in b['D21']
    assert r'\sum_{i=1}^N p_iT_{i,\mathrm{OL}}^*(\widehat\theta_n)=\mathcal M_{\widehat\theta_n}' in b['D22']
    assert r'\mathcal M_{\widehat\theta_n}=T_n(\widehat\theta_n)' in b['D22']
    assert r'\max\{L_n(\theta):h(\theta)=\vartheta\}' in b['D23']
    assert r'\widehat\vartheta_n\equiv h(\widehat\theta_n)' in b['D24']
    assert 'as a function of' in b['D25'] and r'\{T_{i,\mathrm{OL}}^*(\theta),\theta\in\Theta\}_{i=1}^N' in b['D25']
    assert r'\max\{L_n^*(\theta):h(\theta)=\widehat\vartheta_n\}' in b['D26']
    assert 'as a function of' in byid['D19']['application_context'][0]['text']
    assert a['A4']==r'Let $\mathbb P_*$ denote the bootstrap probability induced by resampling.'
    assert r'\mathbb R^p\mapsto\mathbb R^s' in a['A5'] and r'\theta\in\mathbb R^p' in a['A5']
    assert r'\vartheta_0=h(\theta_0)\in\mathbb R^s' in a['A6']
    counts=dict(theorems=4,interfaces=len(data['interfaces']),source_members=len(members),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_source_passages']))
    assert counts==dict(theorems=4,interfaces=26,source_members=26,direct_theorem_uses=30,related_theorem_connections=70,unranked_auxiliary_passages=6),counts
    assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==22
    for item in data['claims']+members+ambient['auxiliary_source_passages']:
        assert all(1<=e['page']<=22 for e in item['evidence'])
        fragments=[item['statement_original']]
        for key in ['naming_context','application_context']:
            for ctx in item.get(key,[]):
                assert all(1<=e['page']<=22 for e in ctx['evidence']);fragments.append(ctx['text'])
        for text in fragments:
            assert not re.search(r'[\u4e00-\u9fff]',text)
            assert text.count('$')%2==0 and text.count('\\[')==text.count('\\]')
            for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',text,re.S):
                depth=0
                for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                    depth+=1 if brace=='{' else -1
                    assert depth>=0,('unbalanced',item)
                assert depth==0,('unbalanced',item)
    for x in data['interfaces']:
        assert x['related_theorems'] and set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
        assert '$' not in x['name']
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors) and all(s in linked for s in selectors)
        for k in x['source_keywords']:
            m=byid[k['local_id']];texts=[m['statement_original']]+[c['text'] for c in m.get('naming_context',[])]
            assert any(k['source_text'] in text for text in texts)
    local={1:[],2:[],3:[],4:[1,2,3],5:[1],6:[2,5],7:[1],8:[2,7],9:[8,3],10:[9],11:[],12:[11],13:[2],14:[1],15:[1,2,14],16:[6,3],17:[2,3,1,4],18:[1],19:[2,18],20:[19,16],21:[20,7],22:[21,3,16],23:[9],24:[16],25:[19,7,9],26:[25,24]}
    assert {lid:m['depends_on'] for lid,m in byid.items()}=={f'D{k}':[f'D{i}' for i in ids] for k,ids in local.items()}
    for lid,m in byid.items():
        n=int(lid[1:]);assert m['source_kind']==('assumption' if n in {1,4,12,13,15} else 'condition' if n==17 else 'definition')
    for it in data['interfaces']:
        lid=it['members'][0]['local_id']
        for rel in it['related_theorems']:
            path=rel['via_local_ids'];assert path[0] in claims[rel['claim_id'].split('/T')[-1]]['depends_on'] and path[-1]==lid
            for x,y in zip(path,path[1:]):assert y in byid[x]['depends_on']
    def check_strings(value):
        if isinstance(value,dict):
            for v in value.values():check_strings(v)
        elif isinstance(value,list):
            for v in value:check_strings(v)
        elif isinstance(value,str):assert not any(ord(c)<32 and c!='\n' for c in value),repr(value)
    for name in ARTIFACTS:check_strings(json.loads((ROOT/name).read_text()))
    def has_span(n,font,fragment):
        return any(s['font']==font and fragment in s['text'] for b in pdf[n-1].get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'])
    assert has_span(5,'CMSY10','M') and has_span(10,'CMSY10','N')
    assert has_span(10,'MSAM10','⊺')
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for item in rebuild['comparisons']:
        assert item['matches_saved_bytes'] and item['saved_sha256']==item['regenerated_sha256']==digest(ROOT/item['artifact'])
    transition=json.loads((ROOT/'source-transition-review.json').read_text())
    assert transition['new_source']['pdf_sha256']==digest(PDF)
    assert digest(Path(transition['old_source']['pdf_path']))==transition['old_source']['pdf_sha256']
    findings=json.loads((ROOT/'evidence/manual-findings.json').read_text())
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,'-B',str(SKILL/'validate_census.py'),str(ROOT/name)],text=True,capture_output=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ARTIFACTS+['inventory-review.json']}
    pages=[1,5,6,7,8,9,10,12,13,18,19,20,22]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    evidence[-1]['scope']='Main text above Appendix A only.'
    evidence.append(dict(page=22,path='evidence/appendix-heading.png',sha256=digest(ROOT/'evidence/appendix-heading.png'),scope='Appendix heading only; body excluded.'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=26,main_text_last_pdf_page=22,main_text_end_y=241.31422424316406,provenance_path='evidence/source-provenance.json'),enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Independent published-heading enumeration over pages 1-22, clipped before Appendix A on page 22, followed by visual review of all four full theorem statements.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),source_notes=ambient['source_issues'],unresolved_source_references=ambient['excluded_references'],ambient_resolution=ambient['statement_resolution'],artifacts=artifacts,evidence=evidence,review_limits=['Source transcription and statement-dependency audit, not proof certification or correction of printed errors.','Appendix bodies and supplementary mathematics excluded.'],source_transition=dict(path='source-transition-review.json',sha256=digest(ROOT/'source-transition-review.json'))))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,registered_pdf_path=str(PDF),registered_pdf_sha256=digest(PDF),registered_pdf_pages=26,source_version=paper['version'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=digest(PDF),registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
