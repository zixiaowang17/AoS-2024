"""Pin the completed AdaDetect source review and independent validation."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
WORK=Path('[local path omitted]')/ROOT.name
CACHED_PDF=Path('[local-workspace]/minimax/reference/aos2024/pdf/23-AOS2338.pdf')
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def main():
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    ambient=json.loads((ROOT/'ambient-conventions.json').read_text())
    paper=inv['papers'][0]
    assert digest(WORK/'source.pdf')==paper['pdf_sha256']
    assert len(data['claims'])==6 and len(data['interfaces'])==27
    assert sum(len(x['central_claim_uses']) for x in data['interfaces'])==43
    assert sum(len(x['related_theorems']) for x in data['interfaces'])==69
    assert digest(CACHED_PDF)==paper['pdf_sha256']
    for n in [1,5,6,7,8,9,10,11,12,13,14,17,18,19,20,27]:
        shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [
        'theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json',
        'source-passages.json','ambient-conventions.json','inventory-review.json']}
    evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
    write('paper-audit.json',dict(
        schema_version='statistical-paper-audit-v1',paper_id=ROOT.name,status='complete',audit_kind='source_review',
        completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source=dict(pdf_path=str(CACHED_PDF),source_url=paper['source_url'],version=paper['version'],
            pdf_sha256=paper['pdf_sha256'],pdf_pages=58,main_text_last_pdf_page=27,
            matching_tex_archive_sha256=digest(WORK/'source.tar.gz')),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],
            method='Six uncommented Theorem environments in matching-version TeX before the appendix command, checked against PDF pages 9, 10-11, 13, 18 and 20. Main-text references end on page 27; only the Appendix A heading on page 28 was inspected to confirm the boundary.',
            excluded_result_types=['Lemma','Proposition','Corollary','Remark'],supplementary_material_used=False),
        validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
            'The complete six-Theorem inventory was checked against the PDF and independently validated before interface extraction.',
            'All 27 source entries and six ambient passages were reviewed against the main text. Mathematical displays and source numbering were checked visually, with matching-version TeX aiding transcription.',
            'The finalizer derived the same-paper dependency graph and aggregate counts. A separate validator process accepted the census against its pinned inventory.',
            'All 43 direct uses and 69 related-theorem connections were reviewed for statement correspondence, including setting references, arbitrary-score versus fitted-score uses, and the oracle BH alternative.',
            'Every source member has a meaning-bearing highlight in its body or source label. All selectors match that source or a linked same-paper theorem.',
            'Source keywords use author terminology. Adjacent naming contexts preserve original prose; inline p in p-value and 0-1 in loss are plain typographic transcriptions in naming context only.']),
        counts=dict(theorems=6,interfaces=27,source_members=27,direct_theorem_uses=43,related_theorem_connections=69),
        source_notes=[
            'The inspected version is arXiv:2208.06685v3, stamped 25 October 2023, with PDF footer date 26 October 2023. Published-layout identity is not assumed.',
            'Assumptions 1 and 2 impose conditional exchangeability of raw observations and scores respectively. Assumption 3 excludes ties; Assumptions 4 and 5 separately impose independence and positive densities.',
            'The first assertions of Theorems 3.3 and 3.4 concern arbitrary score families. Their final AdaDetect specializations introduce the fitted construction; its permutation invariance is not imposed on the arbitrary-score definition.',
            'Theorem 3.3 concerns score-based p-values, so its AdaDetect correspondence stops before the BH rejection step. PRDS is not added as a premise of Theorems 3.4 or 3.6 merely because it can prove FDR control.',
            'The setting reference in Theorem 3.6 imports the score assumptions from Theorem 3.4, not the random-variable FDR identity. The setting reference in Theorem 5.1 imports the independent-density model from Theorem 4.1, not its optimality conclusion.',
            'Empirical p-values use a strict greater-than comparison and the added one in (10). The fitted score is invariant in the mixed argument, not necessarily in the held-out training argument.',
            'Equation (13) retains the common uniform vector, conditional iid null coordinates, zero alternative coordinates, selected null at 1/(ell+1), and descending order statistics. The displayed tabular text is transcribed as a mathematical array without changing its content.',
            'The average densities in (15)-(17) do not assert iid sampling from a random two-group mixture. The alternative marginals may differ.',
            'Theorem 4.1 retains higher TPR and the parenthetical existence assumption for a threshold attaining mFDR exactly alpha. The ambiguous mFDR numerator is preserved, not corrected using commented-out TeX.',
            'Theorem 5.1 retains both subparts, the delta dependence of constants, all three restrictions in (29), and both conclusions. Risks distinguish null g>=0 from alternative and mixed g<0 errors.',
            'Theorem 5.4 retains the complement on the inclusion event, the enlarged alpha-prime, and its additional assertion for BH on oracle p-values.',
            'Storey and quantile estimators, density estimators, specific neural-network classes, cross-validation procedures, proof-only lemmas and appendix constructions are not counted as requirements of these six theorem statements.'],
        unresolved_source_references=ambient['unresolved_source_conventions'],
        ambient_resolution=ambient['notes'],artifacts=artifacts,evidence=evidence,
        review_limits=['This is a source-fidelity and statement-dependency audit, not a certification of proofs or a resolution of the paper\'s ambiguities.',
            'No appendix body was read or used. The original main-text wording is retained where the excluded appendix is cited.']))
    write('checkpoint.json',dict(paper_id=ROOT.name,stage='complete',inventory_status='validated',census_status='validated',
        source_pdf_path=str(CACHED_PDF),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
    print('Completed AdaDetect: six Theorems, 27 interfaces, 43 direct uses, 69 related connections.')

if __name__=='__main__':main()
