"""Reproduce both complete original Theorems from the registered author manuscript."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2034'
SHA='0e844805fb9411bbcb3d451a08fd5656e065780fdfb5aea0f1d4339781dd00c9'
URL='https://pmc.ncbi.nlm.nih.gov/articles/PMC12981489/pdf/nihms-2151735.pdf'
STATEMENTS=[r'''Suppose that Assumptions A1 and A2 hold and that $\lambda_{\max}(\Sigma_X)=o(\sqrt{\min(n,p)})$, where $\lambda_{\max}(\Sigma_X)$ is the largest eigenvalue of $\Sigma_X$. Further assume that $\boldsymbol\alpha$ is a $p$-dimensional vector with $\|\boldsymbol\alpha\|=1$ that $k_n\boldsymbol\alpha^\top\Sigma_X\boldsymbol\alpha=o\left(\sqrt{\operatorname{tr}(\Sigma_X^2)}\right)$ and that $k_n=o(\sqrt p)$ as $n\to\infty$. Then:

i. under the null hypothesis $H_0$, $T_n\to N(0,1)$ in distribution as $n\to\infty$;

ii. under the local alternative hypothesis $H_a$ in (7),
\[
T_n-\frac{n\|\boldsymbol\delta_z\|^2+nk_n|\boldsymbol\alpha^T\boldsymbol\delta_z|^2}{\{2\operatorname{tr}(\Omega^2)\}^{1/2}}\overset d\longrightarrow N(0,1)\quad\text{as }n\to\infty,
\]
(8)
where $\boldsymbol\delta_z=\Sigma_X(\boldsymbol\beta-\boldsymbol\beta_0)$, and $\|\cdot\|$ is the Euclidean $L_2$ norm.''',r'''Suppose that Assumptions A1 and A2 hold, and that $\lambda_{\max}(\Sigma_X)=o(\sqrt{\min(n,p)})$. Let
\[
\gamma_0^2=\frac{p}{nS\sqrt{\operatorname{tr}(\Sigma_X^2)}},
\]
then under the alternative hypothesis as specified in the REM model with $s\in[0,1/2]$:

i. further assuming that the random error $\epsilon_i$, $i=1,\ldots,n$, are i.i.d. Gaussian random variables with mean zero and variance $\sigma^2$, then all sequences of tests are asymptotically powerless if $\gamma^2/\gamma_0^2\to0$ as $n\to\infty$;

ii. the proposed test is asymptotically powerful when $\boldsymbol\alpha$ is a $p$-dimensional vector with $\|\boldsymbol\alpha\|=1$ and $k_n\boldsymbol\alpha^\top\Sigma_X\boldsymbol\alpha=o\left(\sqrt{\operatorname{tr}(\Sigma_X^2)}\right)$ if $\gamma^2/\gamma_0^2\to\infty$ as $n\to\infty$.''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+str(i),paper_id=PID,claim_kind='theorem',label='Theorem '+str(i),source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+str(i)+'; complete original statement, including both parts')]) for i,(s,p) in enumerate(zip(STATEMENTS,[6,8]),1)]
    paper=dict(paper_id=PID,title='Testing high-dimensional regression coefficients in linear models',authors=['Alex Zhao','Changcheng Li','Runze Li','Zhe Zhang'],version='Author manuscript nihms-2151735.pdf; available in PMC 2026 March 13; final-edited citation October 2024',pdf_pages=36,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=23,main_text_boundary=dict(location='Section 4 Concluding remarks, supplementary-material notice, Acknowledgments and Funding end on PDF page 23. Appendix: Proofs of Lemmas 2.1 and 2.2 starts on page 24; no appendix material is used in the census. References start on page 30 and detached Tables 1-5 follow on pages 32-36.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerate actual bold Theorem headings throughout pages 1-23 and visually compare both complete two-part statements on pages 6 and 8. Exclude Lemmas 2.1-2.2, Remarks, proof headings, citations and appendix results.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local NIH author manuscript, identified by its source-specific filename and PDF hash; no replacement source or appendix content.',normalization_policy='Preserve original wording, formulas, hypotheses and both parts of each Theorem. Normalize line wrapping and mathematical typesetting only; do not add conditions from other results.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved both complete original Theorems; independent source validation is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
