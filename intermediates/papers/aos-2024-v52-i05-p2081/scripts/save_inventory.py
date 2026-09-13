"""Reproduce both original main-text Theorems of the registered arXiv v3 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2081'
SHA='c0a3de713b451e40884d7bca8d77f7b7056c825a92297c372685e992ff6363eb'
URL='https://arxiv.org/pdf/2205.15717v3'
NUMBERS=['3.1','3.4']
STATEMENTS=[r'''Let $X_1,\ldots,X_n$ be a n-sample from $f_0$ satisfying (14) and (15) with $\omega>6\beta+(2\beta+D)(D-d)\log(1/\delta)/\log n$ and that $\beta_0\leq\beta_\perp\leq\beta_M-4$. Consider the partial location scale mixture or the hybrid location scale mixture prior [either the mixture of finite mixtures or the Dirichlet process mixture] satisfying the conditions displayed in Table 1.
Then, under the conditions stated above,
\[
\mathbb E_0^n[\Pi(\mathrm d_H(f_P,f_0)\geq\varepsilon_n\mid\mathcal X_n)]=o(1)
\]
where
\[
\varepsilon_n\simeq\log^p n\times\left\{\frac{1}{\sqrt{n\delta^{\frac D{2\alpha_0-\alpha_\perp}}}}\vee n^{-\frac\beta{2\beta+D}}\right\},
\]
(16)
with $p>0$ depending on $D$, $\kappa$ and $\beta$, and where we recall that $\beta$, $\alpha_0$ and $\alpha_\perp$ are defined through (5).''',r'''Assume that $\sigma,\delta\leq1$, that $f_0\in\mathcal H_\delta^{\beta_0,\beta_\perp}(M,L)$ satisfies (14) and (15), that $\sigma^{2\alpha_0-\alpha_\perp}=o(\delta)$ and that the manifold satisfies (3) with $\beta_0\leq\beta_\perp\leq\beta_M-4$. Then there exists a function $g:\mathbb R^D\to\mathbb R$ such that, for any $H>0$,
\[
|K_\Sigma g(x)-f_0(x)|\lesssim\sigma^\beta L(x)\mathbb 1_{M^\tau}+(H\log(1/\sigma))^{D/\kappa}\sigma^H\|L\|_\infty\qquad\forall x\in\mathbb R^D.
\]
The function $g$ has the form
\[
g(x)=d_0(x,\sigma,\delta)f_0(x)+\frac1{\delta^{D-d}}\sum_{0<\langle k,\alpha\rangle<\beta}\sigma^{\langle k,\alpha\rangle}\sum_{j=1}^J d_{j,k}(x,\sigma,\delta)D_z^k\overline{(\chi_j f_0)}_{x_j,\delta}(z_{j,x}),
\]
where $z_{j,x}:=\Delta_{1,\delta}^{-1}\bar\Psi_{x_j}^{-1}(x)$, where $(\chi_j)_{j\leq J}$ is a partition of unity, defined in Section D.1, of the set $M^\tau\cap B(0,R_0(\log(1/\sigma))^{1/\kappa})$ associated with a $\tau/64$-packing $(x_j)_{j\leq J}$ of $M^\tau\cap B(0,R_0(\log(1/\sigma))^{1/\kappa})$ and where $d_{j,k}(x,\sigma,\delta)$ are smooth and bounded functions depending on $\chi_j$ and $M$.''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+'; complete original statement')]) for i,(n,s,p) in enumerate(zip(NUMBERS,STATEMENTS,[14,18]),1)]
    paper=dict(paper_id=PID,title='Estimating a density near an unknown manifold: A Bayesian nonparametric approach',authors=['Clément Berenfeld','Paul Rosa','Judith Rousseau'],version='arXiv:2205.15717v3; 17 Jul 2024',pdf_pages=73,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=29,main_text_boundary=dict(location='Section 6 Discussion continues onto PDF page 29, followed by Acknowledgments and funding. Page-29 evidence is clipped at y=599, above References at y=606.2. Appendix A Some facts on submanifolds with bounded reach starts on page 34; no appendix body is used in the census.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerate actual bold Theorem environments throughout pages 1-28 and the main-text prefix of page 29; visually compare both complete original statements. Corollaries, Propositions, Lemmas and proof headings are excluded.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v3 PDF; no replacement source and no appendix body.',normalization_policy='Preserve complete original statements, including the Section D.1 reference in Theorem 3.4 and all hypothesis/rate formulas. Normalize PDF line wrapping and mathematical typesetting only.'),papers=[paper],claims=claims)
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
