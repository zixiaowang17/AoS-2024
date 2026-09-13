"""Save the completed source review after independent census validation."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import fitz
ROOT=Path(__file__).resolve().parents[1]
WORK=Path('[local path omitted]')/ROOT.name
PDF=Path('[local-workspace]/minimax/reference/aos2024/pdf/23-AOS2349.pdf')
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def main():
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],check=True)
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    ambient=json.loads((ROOT/'ambient-conventions.json').read_text())
    assert digest(PDF)==paper['pdf_sha256']
    assert digest(ROOT/'theorem-inventory.json')==json.loads((ROOT/'inventory-review.json').read_text())['inventory_sha256']
    pdf=fitz.open(PDF);labels=[]
    assert len(pdf)==94
    for i in range(29):
        for match in re.finditer(r'^THEOREM\s+(\d+\.\d+)',pdf[i].get_text(),re.M):labels.append((i+1,match.group(1)))
    expected=[(8,'2.1'),(12,'3.1'),(13,'3.3'),(13,'3.4'),(14,'3.5'),(15,'3.6'),(17,'4.1'),(20,'5.1'),(21,'5.2'),(22,'5.3'),(23,'6.1'),(23,'6.2'),(26,'7.1'),(26,'7.2')]
    assert labels==expected
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in inv['claims']]==expected
    counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
    assert counts==dict(theorems=14,interfaces=49,source_members=49,direct_theorem_uses=94,related_theorem_connections=178,unranked_auxiliary_passages=8)
    related={x['members'][0]['local_id']:{t['claim_id'].split('/T')[-1] for t in x['related_theorems']} for x in data['interfaces']}
    assert related['D10']=={'3.1','3.4','3.6','6.2'}
    assert related['D11']=={'3.1','3.3','3.4','3.5','3.6','6.1','6.2'}
    assert related['D13']=={'3.4','3.5','3.6','6.1','6.2'}
    assert related['D14']=={'3.4','3.5','3.6'}
    assert related['D15']=={'3.3','3.4','3.5','3.6','6.1','6.2'}
    assert all(related['D'+str(i)]=={'5.1'} for i in range(19,26))
    assert all(related['D'+str(i)]=={'4.1'} for i in range(26,32))
    assert all(related['D'+str(i)]=={'5.2','5.3'} for i in list(range(32,39))+[40])
    assert related['D39']=={'5.3'}
    assert related['D41']==related['D42']=={'6.1','6.2'}
    assert related['D43']=={'6.2'}
    assert all(related['D'+str(i)]=={'7.1','7.2'} for i in range(44,49))
    assert related['D49']=={'7.1'} and related['D16']=={'3.3'}
    members=[m for x in data['interfaces'] for m in x['members']]
    by_id={m['local_id']:m for m in members}
    for lid in ['D10','D11','D13','D14','D15','D22','D23','D25','D46','D47','D48']:
        m=by_id[lid]
        assert m['statement_original'].startswith(m['source_scope_original']['text'])
        assert all(e in m['evidence'] for e in m['source_scope_original']['evidence'])
    assert r'\operatorname{Unif}(-\psi_{1,j},\psi_{2,j})' in by_id['D29']['statement_original']
    assert r'\mathcal E_n(Q,\Pi_{n,m},\mathrm p_n^\natural)' in by_id['D45']['statement_original']
    assert r'\operatorname{KL}(Q,\Pi_n)' in by_id['D45']['statement_original']
    for item in data['claims']+members+ambient['auxiliary_passages']:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',item['statement_original'],re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,item.get('local_id',item.get('claim_id'))
            assert depth==0,item.get('local_id',item.get('claim_id'))
    for n in [1,4,5,6,7,8,10,11,12,13,14,15,16,17,19,20,21,22,23,24,25,26,27,29]:
        shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    shutil.copy2(WORK/'appendix-heading.png',ROOT/'evidence/appendix-heading.png')
    plan=json.loads((ROOT/'dependency-review-plan.json').read_text())
    plan['status']='complete'
    if 'pending_source_passages' in plan:
        plan['completed_source_passages']=plan.pop('pending_source_passages')
    plan['completed']=['All 14 original main-text Theorem statements are source-checked and independently validated.','All 49 source interfaces and eight auxiliary passages are extracted and source-reviewed.','The complete local dependency graph, 94 direct uses and 178 related-theorem connections are validated, including source names, highlights and explanations.']
    plan['remaining_completion_gates']=[]
    write('dependency-review-plan.json',plan)
    artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json','interface-draft.json','dependency-review-plan.json']}
    evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=ROOT.name,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=94,main_text_last_pdf_page=29,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Enumerate every printed THEOREM heading in main-document pages 1-29, distinguish references and other result types, and visually check all complete statements. Theorem 5.2 continues onto page 22. The source outline, final reference page and separate supplement title/table-of-contents crop bound the excluded material beginning on page 30.',printed_label_check=labels,excluded_result_types=['Lemma','Proposition','Corollary','Example','Remark'],supplementary_material_used=False),
        counts=counts,
        validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
            'All fourteen original theorem records remain identical to the separately source-reviewed inventory; both artifacts pass separate validator-process invocations.',
            'The cached PDF hash, source version and 94-page count match the pinned provenance. All statement evidence stays within pages 1-29.',
            'Source review covers 49 interfaces and eight auxiliary passages, including complete parent quantifier scopes on each extracted A/B/D/E subcondition.',
            'The finalizer derives the local graph and all 94 direct and 178 related connections. Source keywords, readable names, correspondence explanations and literal source-backed highlight selectors pass validation.',
            'A1 reaches only Theorems 3.1, 3.4, 3.6 and 6.2. B2 reaches only 3.4, 3.5 and 3.6. The weaker assumptions of 3.3, 3.5, 6.1 and 6.2 remain intact.',
            'D conditions and combinatorial constructions reach only Theorem 5.1. Its final clause is documented as requiring D2/D3, without D1.',
            'All concrete neural-network definitions, prior, variational family and Gaussian regression inputs reach only Theorem 4.1. No Holder class or Assumption C is added.',
            'Sparse-factor inputs reach only 5.2/5.3; the stronger signal class reaches only 5.3. Imported assumptions of 5.2 are source excerpts rather than an edge to its proved conclusion.',
            'ivB constructions reach only 6.1/6.2; the maximum sieve complexity reaches only 6.2. E conditions and quasi-posterior constructions reach only 7.1/7.2 and inherit none of A/B.',
            'Printed endpoint-sign, prior-subscript and true-class scope discrepancies remain explicit source issues. All 71 original source statements have balanced mathematical braces.']),
        source_notes=[
            'The inspected version is arXiv:2109.03204v4, stamped 11 March 2024. Title and authors match the corpus entry; identity with the later journal document is not asserted.',
            'The uniform interval signs in (4.4), mismatched prior argument in (7.2), and Lambda_n versus Lambda_n-star scope in Theorem 7.1 are retained for subsequent review.',
            'The original statements retain nested infima/suprema, product/mixed priors, all selection conclusions, underlined sequences and natural superscripts for quasi-posteriors.',
            'The general KL projection is the primary posterior definition. Alternative optimizer decompositions remain source context; proof equivalences are not extra theorem prerequisites.',
            'Numerical examples, algorithm implementations, testing constructions and other appendix results are excluded. A supplement pointer on page 27 is part of the main document; the separate supplement begins on page 30.'],
        unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
        review_limits=['This audit verifies source fidelity and mathematical statement dependencies; it does not certify the proofs or resolve source errors.','Findings are specific to the pinned preprint. Appendix bodies are not used.']))
    write('checkpoint.json',dict(paper_id=ROOT.name,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
    print(json.dumps(counts))

if __name__=='__main__':main()
