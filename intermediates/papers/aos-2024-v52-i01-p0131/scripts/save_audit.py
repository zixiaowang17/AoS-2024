"""Record the completed main-text source review and validation evidence."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
WORK=Path('[local path omitted]')/ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def main():
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=json.loads((ROOT/'ranked-interfaces.json').read_text());paper=inv['papers'][0]
    assert digest(WORK/'source.pdf')==paper['pdf_sha256']
    assert len(data['claims'])==4 and len(data['interfaces'])==14
    assert sum(len(x['central_claim_uses']) for x in data['interfaces'])==13
    assert sum(len(x['related_theorems']) for x in data['interfaces'])==17
    for n in [11,12,25,29,30,38,39]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in ['theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json','source-passages.json','ambient-conventions.json','inventory-review.json']}
    evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
    review=json.loads((ROOT/'inventory-review.json').read_text())
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=ROOT.name,status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source=dict(pdf_path=str(WORK/'source.pdf'),source_url=paper['source_url'],version=paper['version'],pdf_sha256=paper['pdf_sha256'],pdf_pages=149,main_text_last_pdf_page=45,matching_tex_archive_sha256=digest(WORK/'source.tar.gz')),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],method='Four uncommented theorem environments in the expanded main source before the appendix command; each full statement checked against PDF pages 19-20, 26, 35 and 40. The main text ends after Remark 7 above Appendix A on page 45.',excluded_result_types=['Lemma','Proposition','Corollary','Fact','Informal Result'],supplementary_material_used=False,boundary_probe_note=review['notes'][-1]),
        validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
            'The complete four-Theorem inventory was independently source-checked and validated before interface extraction.',
            'All 14 source passages and the six ambient passages were checked against the PDF; matching-version TeX supplied transcription and macros, with printed labels authoritative.',
            'The finalizer derived the local and canonical dependency graphs; an independent validator process accepted the completed census against its pinned inventory.',
            'All member highlight selectors have exact source or linked-theorem matches; every member has a source-body or label match.',
            'All 13 direct uses and 17 related-theorem paths were reviewed for mathematical correspondence. Proof-only information bounds and communication reductions were not added as statement dependencies.']),
        counts=dict(theorems=4,interfaces=14,source_members=14,direct_theorem_uses=13,related_theorem_connections=17),
        source_notes=[
            'The PDF is arXiv:2204.07526v2. Its arXiv stamp is 20 January 2024 and its title-page date is 23 January 2024; no identity with the published layout is assumed.',
            'Symmetric Tensor PCA estimates a vector of norm sqrt(d). Asymmetric Tensor PCA and CCA estimate a rank-one tensor of norm sqrt(d^k). Their observation laws and parameter spaces remain distinct.',
            'Theorem 2 uses b as the memory exponent and eta>0. The other three Theorems use mu and eta>=1.',
            'Theorem 3 imposes lambda asymptotic to d^(-gamma), whereas Theorem 4 imposes lambda squared asymptotic to d^(-gamma). Their gamma restrictions and normalized-overlap thresholds are preserved separately.',
            'Equation (6) describes N observations but writes X_{1:m}; the source notation is preserved and not converted into an additional model parameter.',
            'Equation (30b) prints (2/pi)^(k/2)=(E|Z|)^(k/2), inconsistent for a standard Gaussian. Both expressions remain in the original source statement.',
            'Theorem 4 includes the final promises (31) and (30). Both are recorded; no distinctness requirement for the coordinate indices is invented from the printed set notation.',
            'The named k-NGCA problem includes the kth-moment difference defining lambda in Section 6.1.1. Assumption 4 repeats that condition, but is not explicitly invoked by Theorem 3; its mathematical content is preserved in the problem definition. Assumption 5 is not added.',
            'The three explicit NGCA Assumptions remain separate, including the local-domain guard in Assumption 3 and all nonnegative parameter conditions.',
            'Definition 1 specifies deterministic arbitrary update and output functions. The randomized-protocol discussion is not silently inserted into the definition.',
            'No upper-bound spectral estimator, mixture model, GLM, parity-learning reduction, Hellinger-information quantity, distributed protocol or proof-only proposition is counted as a statement requirement of these four Theorems.'],
        unresolved_source_references=[
            dict(source='Section 2.1 — Hermite polynomials',meaning='The main text identifies orthonormal Gaussian Hermite families but refers to Appendix I.2 for the detailed construction.',action='Preserve the main-text characterization; do not inspect the appendix or invent a leading-coefficient/sign convention.'),
            dict(source='Theorems 1-4',meaning='The normalized overlap divides by the squared norm of the estimator, without an explicit convention at a zero estimate. Theorems 2 and 4 also print any real t despite 1/t^2.',action='Retain the printed statements and record these unresolved domain conventions rather than silently restricting the quantifiers.'),
            dict(source='Assumption 3',meaning='The density-ratio inequality is pointwise on its stated domain although densities are generally defined up to null sets; the main text does not separately select a version.',action='Preserve the pointwise formulation and its guard without substituting an almost-everywhere statement.')],
        ambient_resolution=[
            dict(notation='Tensor products, tensor norm and inner product, standard basis vectors',resolution='Original Section 2.1 definitions are in ambient-conventions.json. Tensor norms and inner products use stacked entries.'),
            dict(notation='Asymptotic comparison, limits and scaling exponents',resolution='The source asymptotic notation is archived, including its polynomial-separation meaning of much-less-than. Theorem exponents and constants remain bound locally.'),
            dict(notation='Probability P_V, sampling measure mu_V, parameter space and estimator range',resolution='The generic iid inference setup is archived; each of the four model passages separately supplies its parameter and sampling-law conventions.'),
            dict(notation='Scalar versus vector standard Gaussian, sign and integers',resolution='The original Section 2.1 conventions are retained. In NGCA assumptions mu_0 is the univariate standard Gaussian; in the CCA density it is the kd-dimensional standard Gaussian.')],
        artifacts=artifacts,evidence=evidence,review_limits=['Source fidelity and dependency audit do not certify the proofs.','Appendix material encountered during the initial boundary probe was excluded from extraction; all definitions used here come from main-text sources.']))
    write('checkpoint.json',dict(paper_id=ROOT.name,stage='complete',inventory_status='validated',census_status='validated',source_pdf_path=str(WORK/'source.pdf'),source_pdf_sha256=paper['pdf_sha256'],remaining_work=None))
    print('Completed: four Theorems, 14 interfaces, 17 related-theorem connections.')

if __name__=='__main__':main()
