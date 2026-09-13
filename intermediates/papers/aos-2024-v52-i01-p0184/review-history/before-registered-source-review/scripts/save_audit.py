"""Save the source review after census and auxiliary-definition validation."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
WORK=Path('[local path omitted]')/ROOT.name
PDF=Path('[local-workspace]/minimax/reference/aos2024/pdf/23-AOS2339.pdf')
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def main():
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],check=True)
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    ambient=json.loads((ROOT/'ambient-conventions.json').read_text())
    paper=inv['papers'][0]
    assert digest(PDF)==paper['pdf_sha256']
    assert digest(ROOT/'theorem-inventory.json')==json.loads((ROOT/'inventory-review.json').read_text())['inventory_sha256']
    assert len(data['claims'])==5 and len(data['interfaces'])==18
    assert sum(len(x['central_claim_uses']) for x in data['interfaces'])==25
    assert sum(len(x['related_theorems']) for x in data['interfaces'])==55
    related={x['members'][0]['local_id']:{t['claim_id'].split('/T')[-1] for t in x['related_theorems']} for x in data['interfaces']}
    assert related['D18']==related['D14']=={'1','2','3'}
    assert related['D17']=={'4'} and related['D15']=={'3'}
    assert related['D12']=={'2','3'}
    assert all(related[k]=={'1','2','3','4','5'} for k in ['D3','D4','D5'])
    for n in [1,4,5,6,7,9,10,11,12,13,21,22,23]:
        shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [
        'theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json',
        'ambient-conventions.json','inventory-review.json']}
    evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=ROOT.name,status='complete',
      audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],
        pdf_pages=23,main_text_last_pdf_page=23,provenance_path='evidence/source-provenance.json'),
      enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],
        method='Numbered Theorem paragraph starts enumerated across all 23 pages and checked against the five visual source statements. Theorem 3 spans pages 9-10 and Theorem 5 spans pages 12-13. Discussion/funding/supplement notice/references occupy pages 21-23; no appendix body is embedded.',
        excluded_result_types=['Proposition','Lemma','Corollary'],supplementary_material_used=False),
      validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
        'The five original Theorems were checked against their complete PDF statements and validated before interface extraction. Their inventory hash remains unchanged.',
        'All 18 source entries and four unranked auxiliary passages were checked against the main-text PDF, including source indices, signs and scaling factors.',
        'The finalizer derived counts and local dependency paths. An independent validator process accepted the completed census and its pinned source inventory.',
        'All 25 direct uses and 55 related-theorem paths were reviewed against the statements and their section conventions.',
        'The independence null and Assumption 1 reach only Theorems 1-3. Conditions (8)-(10) reach only Theorem 4. Theorem 5 has the three explicit rank kernels without null or asymptotic assumptions.',
        'Every source member has a source-body or source-label highlight. Every selector is present in that source or a linked same-paper theorem.',
        'Four auxiliary definitions retain their exact formulas and derived related-theorem IDs; none is replaced by an external standard convention.']),
      counts=dict(theorems=5,interfaces=18,source_members=18,direct_theorem_uses=25,related_theorem_connections=55,unranked_auxiliary_passages=4),
      source_notes=[
        'The PDF is the cached PMC11064990 author manuscript, with creation metadata dated 29 November 2023. Its bytes, page count and title/authors match the prior download manifest. It is not assumed to match the published pagination.',
        'Theorem 3 includes its page-10 continuation stating that the constant is independent of n, p and q. Theorem 5 retains every integral and all three subparts, including its printed second-coordinate range ending at p.',
        'The definition of the independence null concerns the two full vectors. No within-vector independence assumption is invented.',
        'The order-five Hoeffding, order-six Blum-Kiefer-Rosenblatt and order-four Bergsma-Dassios-Yanagimoto kernels remain separate. Their adjustment factors are respectively 40, 60 and 2/3.',
        'Where a source object has only a symbolic name, the adjacent author wording or section heading supplies the indexing term. Variance, Asymptotic analysis under the null and Normal approximation index the original auxiliary-function passages; they are not asserted as new mathematical definitions or source-given names for A, V1/V2 or V.',
        'The original psi, omega and permutation definitions are saved as unranked local auxiliaries with explicit use mappings. These mappings preserve dependencies without inventing natural-language names for the author\'s symbolic helpers.',
        'The null variance passage and the local-alternative variance scale remain distinct. No null product-of-marginal-variances identity is imposed on dependent alternatives.',
        'Theorems 2 and 3 inherit the conditions of Theorem 1, rather than its conclusion as a premise. Theorem 4 uses (8)-(10), not the illustrative contamination model or Proposition 4.',
        'Theorem 5 defines M_h within its statement. Those conclusions are not turned into assumed APIs, and the subsequent approximate power expression and relative-efficiency propositions are not counted as Theorems.',
        'No supplementary proof, computational shortcut, covariance-structure sufficient condition, simulation or distance-correlation comparison is imported as an additional statement requirement.'],
      unresolved_source_references=ambient['unresolved_source_conventions'],
      ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
      review_limits=['Source fidelity and dependency review do not certify the source proofs or repair its mathematical ambiguities.',
        'The separate supplementary material was not opened. Source references to it are retained without extracting its contents.']))
    write('checkpoint.json',dict(paper_id=ROOT.name,stage='complete',inventory_status='validated',census_status='validated',
        source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
    notes=json.loads((ROOT/'extraction-review-notes.json').read_text())
    notes['status']='resolved_into_completed_census'
    notes['remaining_work']=None
    notes['completed_audit_path']='paper-audit.json'
    write('extraction-review-notes.json',notes)
    print('Completed: five Theorems, 18 source entries, four local auxiliaries, 55 related connections.')

if __name__=='__main__':main()
