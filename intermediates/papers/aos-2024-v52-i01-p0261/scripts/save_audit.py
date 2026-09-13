"""Persist the completed source review after independent census validation."""
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
PDF=Path('[local-workspace]/minimax/reference/aos2024/pdf/23-AOS2346.pdf')
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
    for name in ['theorem-inventory.json','ranked-interfaces.json']:
        subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/name)],check=True)
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());paper=inv['papers'][0]
    data=json.loads((ROOT/'ranked-interfaces.json').read_text());ambient=json.loads((ROOT/'ambient-conventions.json').read_text())
    assert digest(PDF)==paper['pdf_sha256']
    assert digest(ROOT/'theorem-inventory.json')==json.loads((ROOT/'inventory-review.json').read_text())['inventory_sha256']
    counts=dict(theorems=len(data['claims']),interfaces=len(data['interfaces']),source_members=sum(len(x['members']) for x in data['interfaces']),
        direct_theorem_uses=sum(len(x['central_claim_uses']) for x in data['interfaces']),related_theorem_connections=sum(len(x['related_theorems']) for x in data['interfaces']),unranked_auxiliary_passages=len(ambient['auxiliary_passages']))
    assert counts==dict(theorems=4,interfaces=13,source_members=13,direct_theorem_uses=15,related_theorem_connections=27,unranked_auxiliary_passages=4)
    related={x['members'][0]['local_id']:{t['claim_id'].split('/T')[-1] for t in x['related_theorems']} for x in data['interfaces']}
    assert all(related['D'+str(k)]=={'2.1','2.2','4.1','5.2'} for k in [1,2,3,4])
    assert related['D5']==related['D6']=={'2.1','2.2'}
    assert all(related['D'+str(k)]=={'4.1'} for k in [7,8,9,10,11])
    assert related['D12']==related['D13']=={'5.2'}
    for x in data['interfaces']:
        for m in x['members']:
            for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',m['statement_original'],re.S):
                depth=0
                for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                    depth+=1 if brace=='{' else -1
                    assert depth>=0,(m['local_id'],'unbalanced math')
                assert depth==0,(m['local_id'],'unbalanced math')
    for n in [1,4,5,6,7,8,9,12,13,14,15,16,22,23,24]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    artifacts={n:dict(path=n,sha256=digest(ROOT/n)) for n in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json']}
    evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=ROOT.name,status='complete',audit_kind='source_review',
        completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source=dict(pdf_path=str(PDF),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=24,main_text_last_pdf_page=22,provenance_path='evidence/source-provenance.json'),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Enumerate all printed THEOREM starts across the published article and visually check the complete four statements on PDF pages 6, 8 and 15. Section 6 ends on page 22 before acknowledgments, funding, the separate-supplement notice and references. No embedded appendix is present.',excluded_result_types=['Lemma','Proposition','Corollary','Remark'],supplementary_material_used=False),
        counts=counts,
        validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
            'The four complete original Theorem records, including titles and all constant/sample-size conditions, remain identical to the independently reviewed inventory.',
            'All 13 original interface passages and four source auxiliaries were visually checked against the published PDF; original mathematical content, labels and source terminology are preserved.',
            'The finalizer derived 15 direct uses and 27 related-theorem paths. A separate validator process accepted the finalized census and pinned inventory.',
            'The all-estimator minimax conventions and power-law class reach Theorems 2.1 and 2.2 only. No constructive estimator or proof lemma is imported into their statement dependencies.',
            'The oracle and optimization procedures remain distinct definitions and both reach Theorem 4.1. The circular pilot distance is not substituted for the real least-squares objective.',
            'The likelihood estimator and Assumption 5.1 reach Theorem 5.2 only; the stronger power-law class is not an added prerequisite of that theorem.',
            'Every source member has a source-body or source-label highlight. All selectors match the source or a related same-paper Theorem. All extracted mathematical fragments have balanced braces.',
            'The complex Gaussian normalization, positive known noise, K>=2, bispectrum index set including k=l, and expectation abbreviation are preserved in the auxiliary source passages.']),
        source_notes=[
            'The source is the published article, volume 52 issue 1 pages 261-284, DOI 10.1214/23-AOS2346. The PDF metadata, title/authors, page count and SHA-256 agree with the external cache provenance.',
            'Statements were transcribed from the published PDF; no separate supplement or arXiv version was substituted.',
            'The risk aligns the signal with a single circular rotation across all Fourier frequencies. It does not align each frequency independently.',
            'The generic parameter class imposes upper and lower magnitude bounds at every frequency. Assumption 5.1 instead controls energy in every subset containing at least half the frequencies.',
            'The full method-of-moments procedure retains magnitude estimation, conjugated empirical bispectrum, choice of argument versions, real least-squares phase estimation and real coefficient reconstruction.',
            'The oracle uses true phases. The observable optimization procedure uses a circular maximum-discrepancy pilot followed by a real argument lift. The proof-only frequency-marching alternative is not substituted.',
            'The likelihood integrates over uniform latent rotations and minimizes over all real coefficient vectors. The signal-aligned representative used later in the proof is not part of the estimator definition.',
            'Zero-argument conventions, minimizer selection, constant-ordering details and the zero-signal denominator in Theorem 5.2 are recorded as source ambiguities rather than silently repaired.'],
        unresolved_source_references=ambient['unresolved_source_conventions'],ambient_resolution=ambient['standard_ambient_resolution'],artifacts=artifacts,evidence=evidence,
        review_limits=['The audit preserves statement content and dependencies; it does not certify the proofs or resolve unstated source conventions.',
            'The separately linked supplementary appendices were not opened.']))
    write('checkpoint.json',dict(paper_id=ROOT.name,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
    print(json.dumps(counts))
if __name__=='__main__':main()
