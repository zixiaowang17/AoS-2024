"""Save source-fidelity review and independent validation for the pinned preprint."""
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
PDF=Path('[local-workspace]/minimax/reference/aos2024/pdf/23-AOS2347.pdf')
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
    for n in ['theorem-inventory.json','ranked-interfaces.json']:
        subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/n)],check=True)
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-conventions.json').read_text())
    assert digest(PDF)==paper['pdf_sha256']
    assert digest(ROOT/'theorem-inventory.json')==json.loads((ROOT/'inventory-review.json').read_text())['inventory_sha256']
    counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),
        direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
    assert counts==dict(theorems=3,interfaces=14,source_members=14,direct_theorem_uses=12,related_theorem_connections=21,unranked_auxiliary_passages=4)
    related={x['members'][0]['local_id']:{t['claim_id'].split('/T')[-1] for t in x['related_theorems']} for x in data['interfaces']}
    assert related['D2']=={'2.4','2.5','3.2'}
    assert all(related['D'+str(k)]=={'2.4','2.5'} for k in [1,3,4,5,9])
    assert all(related['D'+str(k)]=={'2.4'} for k in [6,7,8])
    assert related['D10']==related['D11']=={'2.5'}
    assert all(related['D'+str(k)]=={'3.2'} for k in [12,13,14])
    for x in data['interfaces']:
        for m in x['members']:
            for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',m['statement_original'],re.S):
                depth=0
                for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                    depth+=1 if brace=='{' else -1
                    assert depth>=0,(m['local_id'],'math braces')
                assert depth==0,(m['local_id'],'math braces')
    for n in [1,2,3,4,5,6,7,9,10,11,12,19]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json']}
    evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=ROOT.name,status='complete',audit_kind='source_review',
        completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=31,main_text_last_pdf_page=19,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Enumerate printed main-text Theorems on pages 1-19, using the outline and heading-only crop to bound the appendices beginning on page 20. Visually verify complete statements 2.4, 2.5 and 3.2 on pages 6, 7 and 11.',excluded_result_types=['Definition','Proposition','Corollary'],supplementary_material_used=False),
        counts=counts,
        validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
            'All three complete theorem statements remain identical to the separately validated and source-reviewed inventory.',
            'All 14 source interfaces and four auxiliary passages were checked against the pinned main-text PDF, including grouping set operations, optimization constraints and Algorithm 2.',
            'The finalizer derived the same-paper graph, 12 direct uses and 21 related-theorem connections. A separate validator process accepted the census and its pinned inventory.',
            'The Gaussian regression model and grouping-risk definitions reach only the statistical Theorems 2.4 and 2.5. The general convex objective, projection and warm-start algorithm reach only Theorem 3.2.',
            'The common feasible coefficient space reaches all three theorems; no path imports a true coefficient, Gaussian noise or grouping sensitivity into the algorithm-convergence theorem.',
            'The global L0-Fusion and oracle least-squares estimators reach only Theorem 2.4. The separated/balanced and sensitivity-restricted subclasses reach only Theorem 2.5.',
            'Every member has a source-body or source-label highlight, and every selector matches its source or a linked same-paper theorem. Extracted mathematical fragments have balanced braces.',
            'The main-text projection definition is complete as a set-valued argmin. The appendix-only computational subroutine remains unexpanded.']),
        source_notes=[
            'The inspected source is arXiv:2201.01036v1, stamped 4 January 2022. Its title and authors match the corpus entry. The census is explicitly version-specific and does not assert equality with the later 2024 publication.',
            'The PDF and its hash are retained in the external source cache; repository evidence contains only main-text extracts, inspected images, provenance and the appendix-heading crop.',
            'Nonzero coefficient groups exclude the zero class. Group count and support size are distinct, and the feasible problem gives upper bounds rather than exact counts.',
            'Grouping sensitivity measures prediction separation per grouping discrepancy. The grouping distance is defined by injections and is not silently symmetrized.',
            'The minimax ratio r is defined within Theorem 2.5. The post-theorem restricted-eigenvalue conjecture is not imposed as a hypothesis.',
            'Algorithm 2 uses a general convex lower-bounded objective and set-valued projection. Theorem 3.2 concerns its infinite sequence and limit c, not convergence to a specified global minimizer.',
            'Potential nonunique or unattained minima, oracle group-collapse discrepancies, arbitrary initialization, stopping-rule conventions and denominator edge cases are retained as explicit unresolved source details.',
            'Screening, CoSaMP, MIO formulations and proof-only stationary-point results are not counted as prerequisites of these theorem statements.'],
        unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
        review_limits=['The audit checks source statement fidelity and dependencies rather than certifying the proofs or repairing unstated conventions.',
            'No appendix statement or implementation is used in the census. The pinned preprint may differ from the published article.']))
    write('checkpoint.json',dict(paper_id=ROOT.name,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
