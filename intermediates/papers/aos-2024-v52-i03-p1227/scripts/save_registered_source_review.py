"""Record the completed manual source review and independent consistency checks.

Expected hashes pin the inspected data; rerunning this script is not a new
semantic review and cannot certify changed content without another review.
"""
import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import fitz
from save_inventory import PID, REPO, ROOT, prov

SHA='ea45ffa0b45eaf01a2f6bc84b6758bd5363e3fb2d6478610f1e17d132b95a0e7'
SKILL=Path('skills/statistical-paper-census/scripts')
EXPECTED={
 'theorem-inventory.json':'28613d867ecd585d5a27f65f1f4c4566b962d4cdff1a74230acc74e3da5a953e',
 'source-passages.json':'743909bf8cdb24b99b53e43f55359712ce69ce5de7cb621d7ee7a02c29c904af',
 'interface-extraction.json':'71719a9a171a3f35926062545d025090cb9f83021623e667c6abd9a9d4f9ac04',
 'ambient-prerequisites.json':'c15c8a5ec844f2e5cc9ca8f3e011565deb35d693768456195a2b2cda3833bcf6',
 'unfinalized-census.json':'282a7952e7be584055ee7ce6435ed38799b07189771a6a901877ada537dcfe4e',
 'ranked-interfaces.json':'6c28852bd677eda4a5bbe4e185ecc1a2161a3ddcc4de8a5ba3a1fe246a1c313b'
}


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(name,value):
    (ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')


def main():
    for name,sha in EXPECTED.items():
        assert digest(ROOT/name)==sha,('Re-review changed artifact',name)
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    register=json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())
    entry=next(x for x in register['papers'] if x['paper_id']==PID)
    assert digest(source)==entry['sha256']==prov['pdf_sha256']==SHA
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    ambient=json.loads((ROOT/'ambient-prerequisites.json').read_text())
    paper=inv['papers'][0]
    ir=json.loads((ROOT/'inventory-review.json').read_text())
    assert ir['status']=='complete' and ir['source_checked']
    assert ir['inventory_sha256']==digest(ROOT/'theorem-inventory.json')
    assert paper['version']=='arXiv:2212.09009v6, 2 May 2024'
    assert paper['source_url']=='https://arxiv.org/pdf/2212.09009v6'
    assert entry['version']=='2212.09009v6.pdf'
    pdf=fitz.open(source)
    assert len(pdf)==paper['pdf_pages']==entry['pdf_pages']==36
    first=' '.join(pdf[0].get_text().split())
    assert all(s in first for s in ['Locally Simultaneous Inference','Tijana Zrnic','William Fithian','arXiv:2212.09009v6','2 May 2024','05.03.24'])
    assert paper['main_text_last_pdf_page']==27
    assert paper['main_text_boundary']['shared_page_with_appendix'] is False
    headings=[];references=[]
    for n in range(1,28):
        page=pdf[n-1]
        assert (ROOT/f'evidence/page-{n:02}.txt').read_bytes().decode()==page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                match=re.match(r'^Theorem (\d+)\.',text)
                if match:
                    (headings if 'BX' in line['spans'][0]['font'] else references).append((n,match[1]))
    assert headings==[(9,'1'),(10,'2'),(11,'3'),(13,'4'),(16,'5'),(17,'6')]
    assert references==[(16,'5')]
    assert '[36]' in pdf[26].get_text()
    assert 'Deferred proofs' in pdf[27].get_text(clip=fitz.Rect(70,100,550,126))
    assert len(inv['claims'])==len(data['claims'])==6
    for original,final in zip(inv['claims'],data['claims']):
        assert all(final[k]==v for k,v in original.items())
    assert [e['page'] for e in inv['claims'][2]['evidence']]==[11,12]
    claims={c['claim_id'].split('/T')[-1]:c for c in data['claims']}
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    local={1:[],2:[1],3:[1],4:[3],5:[1],6:[5,2],7:[5],8:[7,6,5,2],9:[3],10:[9],
           11:[],12:[],13:[],14:[11],15:[],16:[15],17:[15],18:[],19:[15],20:[],
           21:[20],22:[20],23:[22,21],24:[22],25:[24],26:[24,23,25],27:[24,22],
           28:[27,23],29:[27,23],30:[22,23,25,26,28,29],31:[],32:[31],33:[31,32]}
    assert {lid:m['depends_on'] for lid,m in members.items()}=={f'D{k}':[f'D{i}' for i in ids] for k,ids in local.items()}
    direct={'1':{1,2,3,4,5,6,7},'2':{1,2,4,8,9,10},'3':{11,12,13,14},
            '4':{15,16,17,18,19},'5':{20,21,22,30},'6':{31,32,33}}
    assert {n:set(c['depends_on']) for n,c in claims.items()}=={n:{f'D{i}' for i in ids} for n,ids in direct.items()}
    reach={}
    for n,c in claims.items():
        seen=set();stack=c['depends_on'][:]
        while stack:
            lid=stack.pop()
            if lid not in seen:
                seen.add(lid);stack.extend(members[lid]['depends_on'])
        reach[n]=seen
    expected={'1':range(1,8),'2':range(1,11),'3':range(11,15),
              '4':range(15,20),'5':range(20,31),'6':range(31,34)}
    assert reach=={n:{f'D{i}' for i in ids} for n,ids in expected.items()}
    t={n:c['statement_original'] for n,c in claims.items()}
    b={lid:m['statement_original'] for lid,m in members.items()}
    assert r'\widehat\Gamma^+_\nu' in t['1'] and r'C^{(\alpha-\nu)}' in t['1']
    assert r'A_\nu(P)=\{y:' in t['2'] and r'\hat q=\min' in t['2']
    assert r'4q^\nu([m])' in t['3'] and r'2q^\nu([m])' in t['3']
    assert t['3'].count('- For the')==2 and t['4'].count('- For the')==2
    assert r'C^{\alpha_1}_\gamma\supseteq C^{\alpha_2}_\gamma' in t['4']
    assert r'4w^{\nu/m}_n' in t['4'] and r'2w^{\nu/m}_n' in t['4']
    assert 'min' not in t['4']
    assert 'Algorithm 1 returns exactly' in t['5']
    assert r'2q^\nu(\{X_j\}_{j=1}^d)' in t['5']
    assert r'|\ell(f,z)|\le1' in t['6'] and r'4\operatorname{Gap}_n(\mathcal F)' in t['6']
    assert r'\operatorname{Gap}_n(\widehat{\mathcal F}^+_\nu)' in t['6']
    assert r'P\{y\in A_\nu(P)\}\ge1-\nu' in b['D5']
    assert r'\gamma\in\Gamma_1' in b['D4']
    assert 'nonincreasing' in b['D10']
    assert 'same marginal symmetric zero-mean' in b['D11']
    assert 'do not assume' in b['D11'] and 'independent' in b['D11']
    assert r'\operatorname{supp}(P)\subseteq[0,1]^m' in b['D15']
    assert r'\max_{i\in\mathcal I}|Z_i|' in b['D14']
    assert r'\sup_{v\in\mathcal V}|v^\top Z|' in b['D21']
    assert 'symmetric' not in b['D20']
    assert r'\frac12\|y-X\beta\|_2^2+\lambda\|\beta\|_1' in b['D22']
    assert r'\le2q^\nu' in b['D23']
    assert r'\end{pmatrix}y<\begin{pmatrix}' in b['D24']
    assert r'(X_M^\top)^+s' in b['D24'] and r'(X_M^\top X_M)^{-1}' in b['D24']
    assert r'$P(M,s)$' in b['D24'] and r'\mathcal P(M,s)' not in b['D24']
    assert r'P(M,s)\cap\mathcal B^\infty_\nu' in b['D26']
    assert 'Algorithm 3 in the Appendix' in b['D26']
    assert r'|X_j^\top(y-X_M\beta_{(M,s)}(y))|<\lambda-s_\nu' in b['D28']
    assert r'|\beta_{j\cdot(M,s)}(y)|>s_\nu' in b['D29']
    assert '(Alg. 2)' in b['D30'] and '(Alg. 3)' in b['D30']
    assert r'\mathcal P_{\mathrm{todo}}\setminus\{(M,s)\}' in b['D30']
    assert r'\exists s\text{ s.t. }' in b['D30']
    assert r'\mathcal D=\{z_i\}_{i=1}^n\sim P^n' in b['D31']
    assert 'any valid upper bound' in b['D33'] and 'Rademacher' not in b['D33']
    assert members['D4']['source_kind']==members['D9']['source_kind']=='assumption'
    assert members['D26']['source_kind']=='source_passage'
    for item in list(claims.values())+list(members.values())+ambient['auxiliary_source_passages']:
        assert all(1<=e['page']<=27 for e in item['evidence'])
        fragments=[item['statement_original']]
        for ctx in item.get('naming_context',[]):
            assert all(1<=e['page']<=27 for e in ctx['evidence']);fragments.append(ctx['text'])
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
        assert {u['claim_id'].split('/T')[-1] for u in x['central_claim_uses']}=={n for n,c in claims.items() if lid in c['depends_on']}
        assert set(x['theorem_explanations'])=={r['claim_id'] for r in x['related_theorems']}
        assert x['related_theorems'] and '$' not in x['name']
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
            linked=own+' '+' '.join(claims[r['claim_id'].split('/T')[-1]]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors) and all(s in linked for s in selectors)
        for k in x['source_keywords']:
            m=members[k['local_id']]
            assert any(k['source_text'] in text for text in [m['statement_original']]+[c['text'] for c in m.get('naming_context',[])])
    counts=dict(theorems=6,interfaces=len(data['interfaces']),source_members=len(members),
        direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),
        related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),
        unranked_auxiliary_passages=len(ambient['auxiliary_source_passages']))
    assert counts==dict(theorems=6,interfaces=33,source_members=33,direct_theorem_uses=29,related_theorem_connections=40,unranked_auxiliary_passages=8)
    assert set(ambient['statement_resolution'])=={'shared',*claims} and len(ambient['source_issues'])==25
    rebuild=json.loads((ROOT/'evidence/rebuild-check.json').read_text())
    assert rebuild['paper_id']==PID and len(rebuild['comparisons'])==6
    for c in rebuild['comparisons']:
        assert c['matches_saved_bytes'] and c['saved_sha256']==c['regenerated_sha256']==digest(ROOT/c['artifact'])
    validation=[]
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        result=subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],capture_output=True,text=True,check=True)
        validation.append(dict(artifact=name,returncode=result.returncode,stdout=result.stdout))
    findings=dict(
        inventory='Re-enumerated six bold Theorem headings across all 27 main-text/reference pages and excluded the ordinary-font Theorem 5 reference. Visually compared all complete bodies; the original independently reviewed inventory remains byte-identical.',
        source_passages='Compared 33 original passages with main-text PDF pages 7-17 and preserved eight auxiliary passages. Algorithm 1 is complete; appendix Algorithms 2 and 3 remain unresolved beyond main-text descriptions.',
        dependencies='Independently checked 29 direct uses and 40 related connections. Generic, location-family, bounded-vector, fixed-design LASSO and risk settings remain separate. PoSI coefficient coverage is not a dependency of the exact model-enumeration theorem.',
        names_and_highlights='All interface names are original natural-language source terms, with adjacent naming excerpts where needed. Every member has matching mathematical selectors and the correct source kind; separate quantile and selection definitions are not merged.',
        details='Preserved both branches and factors 4/2, alpha-nu/global minima in Theorem 3, the different random-cardinality correction in Theorem 4, the closed LASSO neighborhood and strict polyhedral inequalities, all queue steps, and signed bounded loss with an arbitrary expected-gap bound in Theorem 6.',
        source_identity='The fixed local PDF is exactly the previously inventoried arXiv v6 source. Version-label and URL aliases in the register are documented; no PDF substitution occurred. The rebuild now resolves the fixed local source directly.',
        validation='All six content artifacts rebuilt byte-for-byte in an empty directory. Independent inventory and census validation passed. This source review does not certify proofs or repair source ambiguities.')
    write('evidence/manual-findings.json',findings)
    pages=[1,7,8,9,10,11,12,13,14,15,16,17,25,27]
    evidence=[dict(page=n,path=f'evidence/page-{n:02}.png',sha256=digest(ROOT/f'evidence/page-{n:02}.png')) for n in pages]
    evidence.append(dict(page=28,path='evidence/appendix-boundary.png',sha256=digest(ROOT/'evidence/appendix-boundary.png'),scope='Appendix heading only; body excluded.'))
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=PID,status='complete',audit_kind='source_review',completed_at=now,
        source=dict(pdf_path=str(source),source_url=paper['source_url'],version=paper['version'],pdf_sha256=SHA,pdf_pages=36,main_text_last_pdf_page=27,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],printed_label_check=headings,method='Independent bold-heading enumeration and visual comparison of all six original theorem bodies.',excluded_result_types=['Lemma','Proposition','Corollary','Example'],appendix_material_used=False),
        counts=counts,validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=list(findings.values())),
        artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in [*EXPECTED,'inventory-review.json']},source_notes=ambient['source_issues'],unresolved_source_references=ambient['excluded_references'],ambient_resolution=ambient['statement_resolution'],evidence=evidence,
        review_limits=['Source transcription and statement dependencies, not proof certification.','Appendix bodies excluded; omitted screening algorithms remain unresolved.']))
    write('registered-source-review.json',dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',method='source_content_revalidation',reviewed_at=now,
        registered_pdf_path=str(source),registered_pdf_sha256=SHA,registered_pdf_pages=36,source_version=paper['version'],
        checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},
        reviewed_artifacts={n:digest(ROOT/n) for n in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence,independent_validation=validation,
        reproduction_check=dict(path='evidence/rebuild-check.json',sha256=digest(ROOT/'evidence/rebuild-check.json'))))
    write('checkpoint.json',dict(paper_id=PID,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(source),source_pdf_sha256=SHA,registered_source_review_path='registered-source-review.json',updated_at=now,remaining_work=None))
    print(json.dumps(counts))


if __name__=='__main__':
    main()
