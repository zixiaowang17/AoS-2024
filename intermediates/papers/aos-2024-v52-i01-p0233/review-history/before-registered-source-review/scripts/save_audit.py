"""Save the source-checked census after independent validation."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
WORK=Path('[local path omitted]')/ROOT.name
PDF=Path('[local-workspace]/minimax/reference/aos2024/pdf/23-AOS2342.pdf')
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
    counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),
        source_members=sum(len(x['members']) for x in data['interfaces']),
        direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),
        related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),
        unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
    assert counts==dict(theorems=4,interfaces=24,source_members=24,direct_theorem_uses=22,related_theorem_connections=38,unranked_auxiliary_passages=1)
    related={x['members'][0]['local_id']:{t['claim_id'].split('/T')[-1] for t in x['related_theorems']} for x in data['interfaces']}
    assert all(related['D'+str(k)]=={'1','2'} for k in [1,2,3,4,5,6,8])
    assert all(related['D'+str(k)]=={'1'} for k in [7,9,10,11,12])
    assert all(related['D'+str(k)]=={'3','4'} for k in [13,14,15,16,17,18,20])
    assert all(related['D'+str(k)]=={'3'} for k in [19,21,22,23,24])
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    for lid,size,page in [('D12',10,11),('D23',10,18),('D24',3,19)]:
        assert [s['line'] for s in members[lid]['algorithm_steps_original']]==list(range(1,size+1))
        assert members[lid]['evidence'][0]['page']==page
    assert [s['depth'] for s in members['D12']['algorithm_steps_original']]==[0,0,0,0,1,2,2,1,2,0]
    assert [s['depth'] for s in members['D23']['algorithm_steps_original']]==[0,0,0,1,1,2,2,1,2,0]
    assert all('('+str(n)+')' in members['D24']['statement_original'] for n in [1,2,3])
    for m in members.values():
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',m['statement_original'],re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,(m['local_id'],'math brace')
            assert depth==0,(m['local_id'],'math brace')
    for n in [1]+list(range(6,21))+[25,26,28]:
        shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    for n in [11,18]:shutil.copy2(WORK/f'algorithm-{n}.png',ROOT/'evidence'/f'algorithm-{n}.png')
    artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [
        'theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json']}
    evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=ROOT.name,status='complete',audit_kind='source_review',
        completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=28,main_text_last_pdf_page=25,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],
            method='Enumerate numbered THEOREM paragraph starts in the published PDF; visually inspect the four complete statements on PDF pages 12, 13, 19 and 20. Discussion ends on page 25, followed by acknowledgments, a separate-supplement notice and references. No appendix body is embedded.',
            excluded_result_types=['Lemma','Proposition','Corollary','Remark'],supplementary_material_used=False),
        counts=counts,
        validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
            'The four independently validated original Theorem records remain unchanged, with their inventory hash pinned by the finalizer.',
            'All 24 source interfaces and the global notation/variance passage were checked against the published PDF, including original labels, formulas and algorithm control structure.',
            'The finalizer derived the 22 direct theorem uses and 38 related-theorem connections. A separate validator process accepted the finalized census.',
            'Discounted-model dependencies reach only Theorems 1 and 2; finite-horizon dependencies reach only Theorems 3 and 4. No identical-looking coefficient or value notation crosses the two settings.',
            'The ordinary concentrability alternatives reach only their explicitly mentioning upper-bound theorem. Neither lower-bound theorem is made to depend on an upper-bound algorithm or Bernstein penalty.',
            'Algorithms 1 and 2 retain all ten numbered lines and their nested state/action loops. Algorithm 3 retains all three numbered steps and all three subsampling substeps.',
            'All source highlight selectors match the source body, its original label, or a related same-paper Theorem. Mathematical fragments have balanced braces.',
            'The clipped numerator is min(d-star,1/S), not a clipped density ratio. The two penalty formulas preserve their different caps, inner max/sum structures and the discounted 5/N addition.']),
        source_notes=[
            'The source is the published 28-page article, volume 52 issue 1 pages 233-260, DOI 10.1214/23-AOS2342. The title, authors, page count and SHA-256 agree with the external source-cache provenance.',
            'Source statements are transcribed directly from the printed PDF; no arXiv version or supplement is substituted for this version.',
            'The discounted data model is independent transitions under arbitrary d-b with known rewards. The episodic model is iid trajectories generated by pi-b and rho-b, allowing temporal dependence within each trajectory.',
            'Ordinary and clipped concentrability are kept distinct within each setting; the shared notation across settings does not establish mathematical equivalence.',
            'The source chooses a deterministic optimal policy in each setting. The occupancy ratios pertain to that choice, not a uniform class of policies.',
            'Every displayed theorem retains its original probability direction, accuracy event inequality, constant conditions, horizon dependence, and total-sample versus trajectory count.',
            'Algorithm 3 supplies trimmed transition data to Algorithm 2. The count N in the empirical-kernel and penalty definitions is kept in its original D0 context; no equality with the pre-trimming KH count is inserted.',
            'The source omissions of time indices in (41b)/(43), unspecified trimming rounding and the 0/0 convention remain explicit in the source and ambient notes.'],
        unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],
        artifacts=artifacts,evidence=evidence,
        review_limits=['Statement fidelity and dependency review do not certify the source proofs or repair its ambiguities.',
            'The separately linked supplementary material and its appendices were not opened.']))
    write('checkpoint.json',dict(paper_id=ROOT.name,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
