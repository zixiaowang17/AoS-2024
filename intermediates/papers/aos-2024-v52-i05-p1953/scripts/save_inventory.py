"""Reproduce the complete original main-text Theorem from the registered v2 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p1953'
SHA='c202c41ab1db9c6fc2e0ce713d96dabe773f2fd0a56a792a385538373b3a29cf'
URL='https://arxiv.org/pdf/2209.13485v2'
STATEMENT=r'''There exists a constant $C>0$ such that the following holds. Fix a confidence parameter $1-\alpha\in(0,1)$, a sample size $n\in\mathbb N$ and a contamination parameter $\eta\in[0,1/2)$. Then, there is an estimator (i.e. a measurable function) $\widehat{\mathsf E}_\star:(\mathbb R^d)^n\to\mathbb R^{d\times d}_{\geq0}$, depending on $\alpha$, $\eta$, and $n$, such that, whenever Assumption 1.2 is satisfied, and additionally $\eta\leq1/C\kappa_4^4$ and $n\geq C\,(r(\Sigma)+\log(2/\alpha))$, the following holds with probability $\geq1-\alpha$:
\[
\left\|\widehat{\mathsf E}_\star(Y_1,\ldots,Y_n)-\Sigma\right\|_{\mathrm{op}}\leq C\kappa_4^2\|\Sigma\|_{\mathrm{op}}\left(\sqrt{\frac{r(\Sigma)}n}+\sqrt{\frac{\log(2/\alpha)}n}\right)+C\kappa_p^2\|\Sigma\|_{\mathrm{op}}\,\eta^{1-\frac2p}.
\]'''
def inventory():
    cid=PID+'/T1.3'
    paper=dict(paper_id=PID,title='Improved covariance estimation: optimal robustness and sub-Gaussian guarantees under heavy tails',authors=['Roberto I. Oliveira','Zoraida F. Rico'],version='arXiv:2209.13485v2; arXiv stamp 25 Mar 2024',pdf_pages=34,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=26,main_text_boundary=dict(location='Main text ends with the proof of Theorem 1.3 and its end-of-proof square on PDF page 26. The Appendix introduction and Appendix A heading begin on PDF page 27; no appendix body is read.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[cid],zero_theorems_confirmed=False,method='Enumerated all main-text result headings through page 26. Only Theorem 1.3 is printed as Theorem. Result 2.2 is printed as Proposition despite several prose citations calling it Theorem. Visually compared the complete theorem on page 4.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v2 PDF; main text only, no replacement source or appendix body.',normalization_policy='Preserve complete original wording and formulas, including slash notation in the contamination cutoff. Normalize wrapping and mathematical typesetting only; record interpretations separately.'),papers=[paper],claims=[dict(claim_id=cid,paper_id=PID,claim_kind='theorem',label='Theorem 1.3 (Main result; proof in §6.2)',source_order=1,statement_original=STATEMENT,evidence=[dict(page=4,location='Complete Theorem 1.3, ending before the paragraph Ignoring the kappa_4 factor')])])
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved the complete original Theorem 1.3; independent review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
