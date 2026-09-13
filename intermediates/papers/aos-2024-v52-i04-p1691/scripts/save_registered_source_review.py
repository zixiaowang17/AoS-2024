"""Record the completed manual source review and independently check its saved artifacts.

Frozen hashes identify reviewed content. Running this script is not itself a
fresh mathematical review or a certification of the paper's proofs.
"""
import datetime,hashlib,json,re,subprocess,sys,unicodedata
from pathlib import Path
import fitz
from save_inventory import PID,REPO,ROOT,SHA
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={'theorem-inventory.json': '486cab005e49ca17c132e9b3a0436ee6e49062627f3c616269d4a0330b5a08c2', 'source-passages.json': 'c0803c66add47ddfdb0bc0579d87a3c202d429e22046282ea03592814f0b9dac', 'interface-extraction.json': '02d47c85e07ea772b4708ee4afca2de7de405c17202dd7a83e0840d13154ca0d', 'ambient-prerequisites.json': '4930350bd84ae699c31387d78e08f133130edb5bca25710f21e72c71a18d56f7', 'unfinalized-census.json': '0c8ee46a19d525c7a024e16085e3e0b3632641f618aeb9aeb340f9cf1c66b1ce', 'ranked-interfaces.json': '2845789f464596c33d8f8ea152b91784c0979492e054bb2a48f505bcc01a5fa8'}
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
    for name,sha in EXPECTED.items():assert digest(ROOT/name)==sha,('Changed reviewed content',name)
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    manifest=json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())
    registered=next(p for p in manifest['papers'] if p['paper_id']==PID)
    assert digest(source)==SHA==registered['sha256']
    assert registered['version']=='2309.15300v1.pdf' and registered['source_url']=='https://export.arxiv.org/pdf/2309.15300'
    pdf=fitz.open(source);assert len(pdf)==registered['pdf_pages']==67
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked'] and ir['inventory_sha256']==EXPECTED['theorem-inventory.json']
    assert paper['source_url']=='https://arxiv.org/pdf/2309.15300v1'
    assert paper['version']=='arXiv:2309.15300v1, 26 September 2023'
    assert paper['main_text_last_pdf_page']==29 and not paper['main_text_boundary']['shared_page_with_appendix']
    first=' '.join(unicodedata.normalize('NFKC',pdf[0].get_text()).split())
    assert all(x in first for x in ['JUDITH ROUSSEAU','CATIA SCRICCIOLO','arXiv:2309.15300v1','26 Sep 2023'])
    assert paper['title'].lower() in first.lower()
    headings=[];texts={}
    for n in range(1,30):
        texts[n]=pdf[n-1].get_text()
        assert (ROOT/'evidence'/f'page-{n:02}.txt').read_bytes().decode()==texts[n]
        for b in pdf[n-1].get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                s=''.join(x['text'] for x in line['spans']);match=re.match(r'^THEOREM (\d+\.\d+)\.',s)
                if match:headings.append((n,match[1]))
    assert headings==[(10,'3.1'),(13,'4.1'),(15,'4.2'),(16,'4.3'),(17,'4.4'),(18,'4.5'),(20,'5.1'),(21,'5.2')]
    assert '834175' in texts[29]
    assert 'SUPPLEMENTARY MATERIAL' in pdf[29].get_text(clip=fitz.Rect(0,0,pdf[29].rect.width,115))
    assert len(inv['claims'])==len(data['claims'])==8
    assert [[e['page'] for e in c['evidence']] for c in data['claims']]==[[p] for p,_ in headings]
    for original,c in zip(inv['claims'],data['claims']):assert all(c[k]==v for k,v in original.items())
    old=json.loads((ROOT/'prior-review/theorem-inventory.json').read_text())
    assert [c['statement_original'] for c in old['claims']]==[c['statement_original'] for c in inv['claims']]
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    # Reconstructed independently from the main-text definitions and theorem assumptions.
    local={1:[],2:[1],3:[1,25],4:[1,29],5:[1,2,32],6:[32],7:[2],8:[32],9:[],
           10:[26],11:[1,9,10,27],12:[9],14:[],15:[14,31,9,8],16:[],17:[],18:[],
           19:[32],20:[],21:[32],22:[32],23:[29,22],24:[1,2,23],25:[],26:[],27:[30],
           28:[],29:[32],30:[],31:[],32:[]}
    direct={'3.1':{1,2,3,4,5,6,7,9},'4.1':{1,3,4,5,6,7,11,12},
            '4.2':{8,9,11,12,15,16,17,18},'4.3':{3,8,9,12,15,16,17,18},
            '4.4':{8,9,11,12,15,16,17,18,19,20},'4.5':{3,8,9,12,15,16,17,18,19,20},
            '5.1':{1,3,9,21,32},'5.2':{3,8,9,24,28}}
    reach={'3.1':{1,2,3,4,5,6,7,9,25,29,32},
           '4.1':{1,2,3,4,5,6,7,9,10,11,12,25,26,27,29,30,32},
           '4.2':{1,8,9,10,11,12,14,15,16,17,18,26,27,30,31,32},
           '4.3':{1,3,8,9,12,14,15,16,17,18,25,31,32},
           '4.4':{1,8,9,10,11,12,14,15,16,17,18,19,20,26,27,30,31,32},
           '4.5':{1,3,8,9,12,14,15,16,17,18,19,20,25,31,32},
           '5.1':{1,3,9,21,25,32},'5.2':{1,2,3,8,9,22,23,24,25,28,29,32}}
    def canonical(n):return {1:'absolute-moments',25:'couplings',26:'kl-divergence',28:'deconv-D18'}.get(n,f'deconv-D{n}')
    assert {k:set(m['depends_on']) for k,m in members.items()}=={f'D{k}':{f'D{i}' for i in v} for k,v in local.items()}
    for x in data['interfaces']:
        assert all(x['interface_id']==canonical(int(m['local_id'][1:])) for m in x['members'])
    for c in data['claims']:
        n=c['claim_id'].split(':theorem-')[-1];assert set(c['depends_on'])=={f'D{i}' for i in direct[n]}
        visited=set();stack=list(c['depends_on'])
        while stack:
            lid=stack.pop()
            if lid not in visited:visited.add(lid);stack.extend(members[lid]['depends_on'])
        assert visited=={f'D{i}' for i in reach[n]}
        assert {canonical(i) for i in reach[n]}=={x['interface_id'] for x in data['interfaces'] if any(t['claim_id']==c['claim_id'] for t in x['related_theorems'])}
    t={c['label'].split()[-1]:c['statement_original'] for c in data['claims']}
    b={k:m['statement_original'] for k,m in members.items()}
    assert r'\beta|I_{h}^{\ast}(\mathsf{v})|\leq 1' in t['3.1'] and r'\beta|I_{h}^{\ast}(\mathsf{v})|>1' in t['3.1']
    assert 'If, in addition' in t['3.1'] and '(3.6)' in t['3.1']
    assert r'M_{4+\delta}(\mu_{Y})' in t['4.1'] and r'\tilde{\epsilon}_{n}^{-2}' in t['4.1']
    assert 'for every' in t['4.1'] and r'\mu_{X}\in\mathscr{P}_{n}' in t['4.1']
    assert r'(\alpha+1)/[\alpha+(\beta d\vee 1)]' in t['4.1']
    assert 'conditions in (4.1) are satisfied' in t['4.2'] and 'conditions in (4.1) are satisfied' in t['4.4']
    assert '(4.1)' not in t['4.3'] and '(4.1)' not in t['4.5']
    assert all(r'\iota>1' in t[n] and r'\varpi>1' in t[n] for n in ['4.3','4.5'])
    assert 'Assumptions 4.3–4.5' in t['4.4'] and 'Granted the assumptions of Theorem 4.4' in t['4.5']
    assert r'l=0,\,1,\,2' in t['5.1'] and r'-(\beta+l)' in t['5.1']
    assert r'\underline{\lim}' in t['5.1'] and r'(2\beta d\vee 1)+1' in t['5.1']
    assert 'for any estimator' in t['5.1'] and '>C.' in t['5.1']
    assert r'\tilde{\mu}_{1n}' in t['5.2'] and r'n^{-1/(4d+1)}' in t['5.2']
    assert r'l=0,\,1' in b['D4'] and r'\beta-l' in b['D4']
    assert r'M_{4+\delta}(\mu_{Y})' in b['D11']
    assert r'(1+C_{0})' in b['D18'] and 'large enough' in b['D28']
    assert members['D18']['relation']==members['D28']['relation']=='distinct'
    assert r'(16^{2}/15)e^{-\sqrt{|x|/15}}' in b['D22']
    assert r'|u|<1' in b['D22'] and r'|u|>17/15' in b['D22']
    assert r'b_{n}=n^{-1/(2\beta d+1)}' in b['D23'] and r'K=\hat{\tau}' in b['D23']
    assert 'not necessarily non-negative' in b['D24'] and 'for every' in b['D24']
    assert r'O(n^{-1/2})' in b['D24']
    originals=data['claims']+list(members.values())+ambient['unranked_auxiliary_passages']
    for obj in originals:
        s=obj['statement_original']
        assert not re.search(r'[\u4e00-\u9fff]',s) and not any(ord(c)<32 and c!='\n' for c in s)
        assert s.count('$')%2==0
        # Aligned row spacing \\[-3pt] is not a display-math opener.
        assert len(re.findall(r'(?<!\\)\\\[',s))==len(re.findall(r'(?<!\\)\\\]',s))
        for display,inline in re.findall(r'(?<!\\)\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',s,re.S):
            depth=0
            for ch in re.findall(r'(?<!\\)[{}]',display+inline):
                depth+=1 if ch=='{' else -1;assert depth>=0
            assert depth==0
        assert all(1<=e['page']<=29 for e in obj['evidence'])
    for x in data['interfaces']:
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors)
            linked=own+' '+' '.join(c['statement_original'] for c in data['claims'] if int(m['local_id'][1:]) in reach[c['label'].split()[-1]])
            assert all(s in linked for s in selectors),(m['local_id'],selectors)
        for rel in x['related_theorems']:
            n=rel['claim_id'].split(':theorem-')[-1]
            assert rel['relation']==('direct' if any(int(m['local_id'][1:]) in direct[n] for m in x['members']) else 'indirect')
            path=rel['via_local_ids'];assert int(path[0][1:]) in direct[n]
            assert path[-1] in {m['local_id'] for m in x['members']}
            assert all(right in members[left]['depends_on'] for left,right in zip(path,path[1:]))
            ex=x['theorem_explanations'][rel['claim_id']]
            assert ex['via_local_ids']==path and len(ex['text'])>30
        for k in x['source_keywords']:
            m=members[k['local_id']]
            assert k['source_text'] in m['statement_original'] or any(k['source_text'] in c['text'] for c in m.get('naming_context',[]))
    counts=dict(theorems=8,interfaces=len(data['interfaces']),source_members=len(members),
        direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),
        related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),
        unranked_auxiliary_passages=len(ambient['unranked_auxiliary_passages']))
    assert counts==dict(theorems=8,interfaces=30,source_members=31,direct_theorem_uses=62,related_theorem_connections=108,unranked_auxiliary_passages=8)
    assert len(ambient['source_issues'])==29 and set(ambient['statement_resolution'])=={'shared',*t}
    rebuilt=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert len(rebuilt['comparisons'])==6
    for c in rebuilt['comparisons']:assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Eight original main-text Theorems were independently enumerated and visually compared with the registered PDF, including both regularity branches in Theorems 3.1 and 4.1. Stable IDs and all original theorem statements are unchanged. Main text ends at the acknowledgements on page 29; the separate supplement beginning on page 30 is excluded.',
        source_passages='Thirty interfaces retain 31 original source passages. Moment classes, Wasserstein distance, the two Fourier conditions, projected smoothness and bias, convolution/posterior/prior objects, source assumptions and the deconvolution estimators remain distinct. Gaussian and Fourier definitions are explicit. Eight auxiliary passages preserve ambient probability spaces, one-dimensional identities, convergence and sampling context without creating artificial ranked demand.',
        dependencies='Independent graph reconstruction verifies 62 direct uses and 108 related connections. The bias definition does not impose kernel condition (a). Theorems 4.2 and 4.4 assert condition (4.1); Theorems 4.3 and 4.5 do not acquire that conclusion as a hypothesis. Theorem 4.5 inherits the assumptions of 4.4 with stronger prior tails. No proof-only dependency is imported.',
        names_and_highlights='Every interface has natural-language source keywords, a faithful source heading, original passages and matching selectors. Related-theorem explanations follow actual local paths. The shared exponential-tail keyword group preserves its two noninterchangeable source conditions and member-specific links.',
        notation='The moment sieve is for mu_Y, the lower bound uses Fourier derivatives of orders 0,1,2 and a strict liminf inequality, and the upper bound uses the probability-valued approximate minimizer. The cutoff Fourier bound has the entire ratio |x|/15 under its square root. The signed raw estimator has no invented real-part operation.',
        limits='Twenty-nine source issues retain implicit model conventions, distinct tail and regularity conditions, the max-sliced index mismatch, projected signed kernels, fractional-power conventions and approximate-minimizer selection. The external cutoff construction and excluded supplement references remain unresolved. Original source claims are not repaired and proofs are not certified.',
        reproduction='Six JSON content artifacts reproduce byte for byte from retained per-paper scripts. Registered source identity, independent inventory, exact claim handoff, source-specific formula checks, graph and reach, keywords/highlights, mathematical fragments and both structural validators passed.')
    write('evidence/manual-findings.json',findings)
    pages=[1,2,5,6,7,8,9,10,13,14,15,16,17,18,20,21,29]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
        source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=67,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent source heading enumeration and visual comparison of all complete theorem statements.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],appendix_material_used=False),
        counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),
        artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},
        source_notes=ambient['source_issues'],unresolved_source_references=ambient['unresolved_source_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,
        review_limits=['Main-text source census; proofs are not certified.','Original ambiguous hypotheses, definitions and notation are preserved with separate issue records.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,
        registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=67,source_version=paper['version'],registered_version_alias=registered['version'],registered_url_alias=registered['source_url'],
        checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},
        reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,
        reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
