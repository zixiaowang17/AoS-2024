"""Reproduce four manually transcribed main-text Theorems from the registered PDF.

This preserves the source statements; reproduction is not a new semantic review.
"""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1716'
SHA='2ebdf2c6b0ed3a1bc4ffe17b29a85db7e97362a9ff4c37926dfd1703ebee7af1'
STATEMENTS=[r'''Suppose that Assumption 1 is satisfied and there exists $\kappa\geq0$ such that $N=O(T^\kappa)$.

(i) Under $H_0$, as $N,T\to\infty$ jointly,
\[
\widehat Z_{NT}\xrightarrow{d}\sup_{0\leq x\leq1}\sum_{i=1}^{\infty}\lambda_i B_i^2(x),
\]
(3.10)
where $\lambda_i$, $i=1,2,\cdots$, are the eigenvalues defined in (2.7) and $B_i(\cdot)$, $i=1,2,\cdots$, are independent standard Brownian bridges defined on $[0,1]$.

(ii) Under $H_A^\diamond$, as $T\to\infty$,
\[
P\left(Z_{NT}^\diamond\geq\sqrt{N\vee T}\right)\to1;
\]
(3.11)
and, under $\widetilde H_A^\diamond$, as $N,T\to\infty$ jointly,
\[
P\left(\widehat Z_{NT}\geq z_\alpha\right)\to1,
\]
(3.12)
where $z_\alpha$ is the upper $\alpha$-quantile of $\sup_{0\leq x\leq1}\sum_{i=1}^{\infty}\lambda_i B_i^2(x)$.''',
r'''Suppose that Assumption 1 is satisfied,
\[
\min_{i\in\mathcal C_\bullet}\frac{T\omega_{Ti}^2\|\delta_i\|^2}{\xi_{NT}}\to\infty
\]
(4.2)
with $\omega_{Ti}$ defined in (3.8), and there exists $\kappa\geq0$ such that $N=O(T^\kappa)$. Then we have
\[
P\left(\widehat{\mathcal C}_\circ=\mathcal C_\circ,\widehat{\mathcal C}_\bullet=\mathcal C_\bullet\right)\to1.
\]
(4.3)
If, in addition, (4.2) is strengthened to
\[
\min_{i\in\mathcal C_\bullet}(\omega_{Ti}\|\delta_i\|)\geq c_\delta,
\]
(4.4)
where $c_\delta$ is a positive constant, we have
\[
\max_{i\in\mathcal C_\bullet}|\widehat\tau_i-\tau_i|=o_P\left([\ln(N\vee T)]^{1+\zeta}\right),
\]
(4.5)
where $\zeta$ is an arbitrarily small positive number.''',
r'''Suppose that the latent structure (4.6) and Assumptions 1 and 2 are satisfied. In addition, there exists $\kappa\geq0$ such that $N=O(T^\kappa)$. Then we have
\[
P\left(\widehat K=K_0\right)\to1,
\]
(4.11)
and
\[
P\left(\widehat{\mathcal C}(b_k)=\mathcal C(b_k):k=1,\cdots,K_0\mid\widehat K=K_0\right)\to1.
\]
(4.12)''',
r'''Suppose that the latent structure (4.6) and Assumptions 1 and 2(i) are satisfied, $|\mathcal C_\bullet|=O(T^2)$, $T=O(|\mathcal C_\bullet|^{3/2})$, and
\[
\min_{1\leq k\leq K_0}\frac{1}{|\mathcal C(b_k)|^{1/2}}\sum_{i\in\mathcal C(b_k)}\|\delta_i\|^2\to\infty.
\]
(4.14)
In addition, $\eta_{it}$ are independent over $i$. Then, as $T$ and $|\mathcal C_\bullet|$ tend to infinity jointly,
\[
P\left(\widehat b_k=b_k,k=1,\cdots,K_0\right)\to1.
\]
(4.15)''']
PAGES=[8,10,12,12]
def inventory():
    claims=[dict(claim_id=f'{PID}/T{i}',paper_id=PID,claim_kind='theorem',label=f'Theorem {i}',source_order=i,statement_original=s,evidence=[dict(page=p,location=f'Theorem {i}; complete statement, ending before the following commentary.')]) for i,(s,p) in enumerate(zip(STATEMENTS,PAGES),1)]
    paper=dict(paper_id=PID,title='Detection and Estimation of Structural Breaks in High-Dimensional Functional Time Series',authors=['Degui Li','Runze Li','Han Lin Shang'],version='arXiv:2304.07003v1; title-page version April 17, 2023; arXiv stamp 14 April 2023',pdf_pages=42,pdf_sha256=SHA,source_url='https://arxiv.org/pdf/2304.07003v1',main_text_last_pdf_page=22,
        main_text_boundary=dict(location='Section 7 and Acknowledgements end on PDF page 22 at "The usual disclaimer applies." Appendix A heading begins at y=719.24 points on that page. Retained page-22 source evidence is clipped above y=718.24; appendix material is excluded.',shared_page_with_appendix=True),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerated actual bold Theorem headings throughout main-text pages 1–22 (page 22 clipped before Appendix A), excluding prose citations. Visually compared the complete four statements on pages 8, 10 and 12.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Verified registered local PDF; appendices and supplements excluded.',normalization_policy='Preserve original wording, hypotheses and conclusions; normalize line wrapping and mathematical typography only.',semantic_ranking_policy='All main-text Theorems; no selection by importance.',build_order_policy='Paper-local dependency order after source extraction.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path);a=parser.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
