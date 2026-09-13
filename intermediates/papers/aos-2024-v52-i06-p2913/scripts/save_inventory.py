"""Reproduce the three original main-text Theorems in the registered p2913 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2913'
SHA='d44c9f40b3fdf103b0df5e0946ef90afc874ebc6b16cb8d87a41057895b4a72a'
URL='https://arxiv.org/pdf/2409.08863v1'
NUMBERS=['3.1','3.2','3.3']
PAGES=[[7],[8],[8,9]]
STATEMENTS=[r'''Assume that the short-range dependence condition holds:
\[
\Theta_{0,2}=\sum_{i\ge0}\delta_{i,2}<\infty.\tag{16}
\]
(i) Under $H_0$, we have, as $n\to\infty$, that
\[
\sup_{x\le0}|\mathbb P(\hat T\le x)-e^{-2x^2}|\to0.\tag{17}
\]
(ii) Under $H_1$, assume $(\tau/n)(1-\tau/n)d\sqrt n\to\infty$. Then, we have, as $n\to\infty$, that
\[
\hat T\to-\infty\quad\text{in probability}.
\]''',r'''Assume that Condition 3.1 holds, $d\gg n^{-1/\theta}$ and $n^{2/\theta}\log(n)\ll k\ll\tau$. Then,
\[
\hat\sigma^2=\sigma_\infty^2+O(1/k)+O_{\mathbb P}(\eta^{2/\min(4,\theta)-1}),
\]
as $n\to\infty$.''',r'''Assume Condition 3.1, $d\gg n^{-1/\theta}$, $n^{2/\theta}\log(n)\ll k\ll\tau$, $n-\tau\ge2k$, and that there exists a constant $K>\rho$ with $d>Kd_*$, where $\rho$ is the tuning parameter from the definition of $\hat\tau$. Let the estimator $\hat\sigma_\infty^2$, used in (9), be consistent for the long-run variance $\sigma_\infty^2$; i. e., $\hat\sigma_\infty^2=\sigma_\infty^2+o_{\mathbb P}(1)$. Then,
\[
\hat\tau=\tau+O_{\mathbb P}(d_*^{-\theta/(\theta-1)}),
\]
as $n\to\infty$.''']
def inventory():
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — original statement'+(' continued' if j else '')) for j,p in enumerate(ps)]) for i,(n,ps,s) in enumerate(zip(NUMBERS,PAGES,STATEMENTS),1)]
    paper=dict(paper_id=PID,title='Change-point analysis with irregular signals',authors=['Tobias Kley','Yuhan Philip Liu','Hongyuan Cao','Wei Biao Wu'],version='arXiv:2409.08863v1, stamped 13 September 2024; submitted manuscript',pdf_pages=39,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=16,main_text_boundary=dict(location='Main text ends after Acknowledgments and NSF funding on PDF page16. Page17 begins Supplementary Material availability/replication listings followed by References, which continue on18. The separate supplement starts19 with Appendix A: Proofs. All appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Independently enumerate actual uppercase small-cap THEOREM3.1–3.3 headings on pages1–16, excluding narrative citations and Corollary3.1. Visually compare all three original statements and the3.3 continuation on9.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local arXivv1 PDF pinned by SHA256; main text ends16, all appendix bodies excluded.',normalization_policy='Normalize line wrapping and mathematical typesetting only. Preserve the one-sided null limit, alternative signal rate, both long-run-variance error terms, strict gap comparability and the localization exponent with its continuation.'),papers=[paper],claims=cs)
def main():
    p=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(p.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved three complete original main-text Theorems; independent inventory review remains separate.')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path);a=ap.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
