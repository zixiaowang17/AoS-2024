"""Reproduce all six complete main-text Theorems from the registered elliptical-test PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2349'
SHA='b9a6c162c4c8845483163754773e65bb696f24444c3621a3c8b5dfdbcc113278'
URL='https://arxiv.org/pdf/2306.10594v2'
NUMBERS=['1','2','3','4','5','6']
STATEMENTS=[r'''If $\kappa_U$ and $\kappa_\Theta$ are characteristic, then so is tensor product kernel $\kappa_U\otimes\kappa_\Theta$; that is, the mapping
\[
\mathcal M(\Omega_{U,\Theta},\mathcal F_{U,\Theta})\to\mathcal H_U\otimes\mathcal H_\Theta,\qquad P_{U,\Theta}\mapsto\int_{\Omega_{U,\Theta}}\kappa_U(\cdot,U)\otimes\kappa_\Theta(\cdot,\Theta)\,dP_{U,\Theta}
\]
is injective.''',r'''If the statistical functional $F\mapsto\Sigma_{U\Theta}(F)$ is Frechet differentiable at $F_0$ with respect to the uniform metric in $\mathcal F$ and conditions in (5.11) are satisfied, then
\[
\sqrt n(\breve\Sigma_{U\Theta}-\Sigma_{U\Theta})\xrightarrow{\mathcal D}N(0,\Gamma),
\]
where $\Gamma:\mathcal H_U\otimes\mathcal H_\Theta\to\mathcal H_U\otimes\mathcal H_\Theta$ is the operator
\[
\Gamma=E[\Sigma_{U\Theta}^\star(X)\otimes\Sigma_{U\Theta}^\star(X)],
\]
and $\Sigma_{U\Theta}^\star(z)$ is given by (5.10).''',r'''Suppose
1. $\Gamma$ has spectral decomposition $\sum_{j=1}^\infty\lambda_j(v_j\otimes v_j)$, where $v_1,v_2,\ldots$ is an orthonormal basis in $\mathcal H_U\otimes\mathcal H_\Theta$;
2. $\Sigma_1$ is a fixed linear operator in $\mathcal H_U\otimes\mathcal H_\Theta$ with expansion $\sum_{j=1}^\infty\sigma_jv_j$ and $\|\Sigma_1\|_{\mathrm{HS}}=c>0$.
Then, under the local alternative hypothesis $H_1^{(n)}:\Sigma_{U\Theta}=n^{-1/2}\Sigma_1$, we have
\[
n\|\breve\Sigma_{U\Theta}\|_{\mathrm{HS}}^2\xrightarrow{\mathcal D}\sum_{j=1}^\infty\lambda_j\widetilde Z_j^2
\]
where $\widetilde Z_j$ are independent $N(\sigma_j/\sqrt{\lambda_j},1)$ random variables.''',r'''Suppose that $\mu$ and $\Sigma$ are known and $\breve\Sigma_{U\Theta}$ is defined as (7.1). Furthermore, suppose the kernels $\kappa_U$ and $\kappa_\Theta$ are bounded: $0\le\kappa_U(u,u')\le M_U$ and $0\le\kappa_\Theta(\theta,\theta')\le M_\Theta$ for all $u,u',\theta,\theta'$. Then,
\[
P\left(\left|\|\breve\Sigma_{U\Theta}\|_{\mathrm{HS}}-\|\Sigma_{U\Theta}\|_{\mathrm{HS}}\right|\ge t+4(M_UM_\Theta/n)^{1/2}\right)\le\exp\left(-\frac{t^2n}{10M_UM_\Theta}\right).
\]
(7.2)''',r'''Suppose $X$ satisfies Assumption 2, and $X_1,\ldots,X_n$ are i.i.d samples of $X$. Further suppose $\Sigma$ satisfies Assumption 1, the density of $W$ satisfies Assumption 3, and the kernel functions $\kappa_U$ and $\kappa_\Theta$ satisfy Assumption 4. Then, for any $\epsilon>0$, we have
\[
P\left(\left|\|\breve\Sigma_{U\Theta}\|_{\mathrm{HS}}-\|\Sigma_{U\Theta}\|_{\mathrm{HS}}\right|\ge[c_7+2c_8/(\epsilon d)]\times[f_3(n,d,u)f_2(n,d,u)+c_5f_1(n,d,u)]+f_4(n,u)\right)\le n(c_6\epsilon)^d+7e^{-u},
\]
where $f_1,f_2,f_3,f_4$ are as defined in (7.6), and $c_1,\ldots,c_{10}$ are some positive absolute constants.''',r'''Suppose all conditions in Theorem 5 are satisfied. If $\log n\prec d\prec n^{1/4}$, then
\[
\|\breve\Sigma_{U\Theta}\|_{\mathrm{HS}}\xrightarrow{P}\|\Sigma_{U\Theta}\|_{\mathrm{HS}}.
\]''']
def inventory():
    pages=[6,13,14,18,19,19]
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement')]) for i,(n,s,p) in enumerate(zip(NUMBERS,STATEMENTS,pages),1)]
    paper=dict(paper_id=PID,title='A nonparametric test for elliptical distribution based on kernel embedding of probabilities',authors=['Yin Tang','Bing Li'],version='arXiv:2306.10594v2; 27 Mar 2024',pdf_pages=25,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=23,main_text_boundary=dict(location='Section10, Acknowledgments and Funding end on PDF page23 before SUPPLEMENTARY MATERIAL at y=547.24. Evidence clipped at y=540. All appendix bodies are in online Supplementary Material and were excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Enumerate every small-cap THEOREM environment in all main-text pages; six labels1–6. Exclude externally cited theorems, Propositions, Lemmas, Corollaries and Assumptions from the theorem inventory.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local hash-verified arXiv v2; appendix bodies excluded.',normalization_policy='Preserve original statements and all subparts, normalize line wrapping and mathematical typesetting. Keep reference (7.1), local alternative and zero-eigenvalue formula as printed; source ambiguities are recorded separately.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all six complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
