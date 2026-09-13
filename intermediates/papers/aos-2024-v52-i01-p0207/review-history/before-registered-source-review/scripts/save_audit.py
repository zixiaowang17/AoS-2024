"""Persist the completed main-text source review and its validation evidence."""
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
PDF=Path('[local-workspace]/minimax/reference/aos2024/pdf/23-AOS2341.pdf')
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
    counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),
        source_members=sum(len(x['members']) for x in data['interfaces']),
        direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),
        related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),
        unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
    assert counts==dict(theorems=4,interfaces=31,source_members=32,direct_theorem_uses=15,related_theorem_connections=82,unranked_auxiliary_passages=3)
    related={x['members'][0]['local_id']:{t['claim_id'].split('/T')[-1] for t in x['related_theorems']} for x in data['interfaces']}
    assert all(related[k]=={'1'} for k in ['D20','D21','D23'])
    assert all(related[k]=={'3'} for k in ['D28','D29','D30','D31'])
    assert all(related[k]=={'3','4'} for k in ['D24','D25','D26','D27'])
    assert related['D6']=={'2','4'} and related['D22']=={'1','3'}
    members={m['local_id']:m for x in data['interfaces'] for m in x['members']}
    assert 'D21' in members['D22']['depends_on'] and 'D30' in members['D22a']['depends_on']
    assert 'D21' not in members['D22a']['depends_on']
    for lid,size,page in [('D23',24,11),('D22',25,12),('D31',26,17),('D28',21,18)]:
        steps=members[lid]['algorithm_steps_original']
        assert [s['line'] for s in steps]==list(range(1,size+1))
        assert members[lid]['evidence'][0]['page']==page
    for m in members.values():
        for parts in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',m['statement_original'],re.S):
            level=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(parts)):
                level+=1 if brace=='{' else -1
                assert level>=0,(m['local_id'],'unbalanced math')
            assert level==0,(m['local_id'],'unbalanced math')
    assert r'\tag{16}' in members['D28']['statement_original']
    for n in [3]+list(range(6,20)):
        shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [
        'theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json',
        'ambient-conventions.json','inventory-review.json']}
    evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=ROOT.name,status='complete',
      audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
      source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],
        pdf_pages=paper['pdf_pages'],main_text_last_pdf_page=paper['main_text_last_pdf_page'],provenance_path='evidence/tex-intake.json'),
      enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],
        method='All main-text pages enumerated before interface extraction. Four printed Theorems (1-4) on PDF pages 13, 14 and 19 were checked visually and against matching-version main-text TeX. Section 5 ends on the shared page 20 above Appendix A; the boundary crop excludes the appendix body.',
        excluded_result_types=['Proposition','Lemma','Corollary'],supplementary_material_used=False),
      validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
        'The four complete original Theorem statements were visually checked before extraction; their independently validated inventory hash remains unchanged.',
        'All 31 interfaces, 32 local members and three unranked source passages were reviewed against the main-text PDF and matching-version TeX.',
        'Algorithms 1 and 2 retain their 24 and 26 numbered steps; Procedures 1 and 2 retain 25 and 21 steps, control nesting, inputs, updates and outputs.',
        'The finalizer derives canonical dependencies, counts and same-paper paths. A separate validator process accepted the finalized census and its pinned theorem inventory.',
        'The 15 direct uses and 82 related paths preserve the general/self-similar distinction and the separate known/adaptive algorithm invocations.',
        'Known-parameter U, tau-star and Algorithm 1 reach only Theorem 1. Estimated-smoothness U-hat, tau-hat and Algorithm 2 reach only Theorem 3. Self-similarity reaches only Theorems 3 and 4.',
        'Every member has a literal source or source-label highlight. All selectors match their source or a related same-paper theorem. Mathematical fragments have balanced braces.',
        'Evidence locations were checked against printed PDF pages, including the float order of Algorithm 2 and Procedure 2. Equation (16) includes both indicator factors and its printed number.']),
      counts=counts,
      source_notes=[
        'The inspected source is arXiv:2211.12612v2, stamped 25 January 2024, with 63 PDF pages. No published pagination is assumed. Its PDF remains in the external persistent source cache.',
        'Only main-text TeX inputs were expanded. No appendix experiment, proof or auxiliary result was opened or imported as a statement dependency.',
        'The general and self-similar parameter classes retain all original constants, even where the paper uses shortened Pi notation. Theorem 3 retains kappa asymptotically comparable to one, uniform beta/gamma bounds and the logarithmic factor.',
        'Theorem 4 retains its existence quantifier for b and its exact constant-dependence clause; it does not inherit an upper-bound algorithm.',
        'Assumptions remain source-labelled assumptions. Definition 3 concerns an individual function; Assumption 4 requires one common arm self-similar under both specified measures.',
        'The shared Procedure 1 has two local invocation records, preserving its original body and the adaptive substitutions without importing the known-parameter confidence formula into the adaptive algorithm.',
        'The lower-bound history omission, strict floor/ceiling prose, unindexed reward in (8), grid equalities and ordinary logarithm in the adaptive radius remain explicit source-convention notes.',
        'The initial suspicion of malformed TeX in (16) was rejected after checking its nested subscripts. No brace repair remains in the saved source statement.'],
      unresolved_source_references=ambient['unresolved_source_conventions'],
      ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
      review_limits=['This audit preserves statement content and dependencies; it does not certify the proofs or repair source ambiguities.',
        'Appendix and supplementary proof references are preserved without inspecting their contents.']))
    write('checkpoint.json',dict(paper_id=ROOT.name,stage='complete',inventory_status='validated',census_status='validated',
        source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
