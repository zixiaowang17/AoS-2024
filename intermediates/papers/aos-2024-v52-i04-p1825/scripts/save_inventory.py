"""Reproduce the five complete original main-text Theorems from registered arXiv v3.

Source symbols and branches are preserved. This script restores the transcription;
it does not perform a new source review or certify proofs.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1825'
SHA='d071d53c213c786036c850189964d704b290290b23a810e54b0b3c64bfa3f1e4'
URL='https://arxiv.org/pdf/2307.08136v3'
STATEMENTS=[r'''Let $T>0$, and for initial conditions $u(0),v(0)\in V$ such that $\|u(0)\|_V+\|v(0)\|_V\leq U<\infty$, consider the corresponding strong solutions $u,v\in C([0,T],V)$, to the 2-dimensional periodic Navier-Stokes equations (10).

A) There exists a constant $c_1$ depending only on $U,\nu,T,\|f\|_{L^2}$ such that $\sup_{0\leq t\leq T}\|u(t)-v(t)\|_{L^2}<c_1$ and
\[
\|u(0)-v(0)\|_{L^2(\Omega)}\leq c_1\left(\log\frac{c_1}{\|u(t)-v(t)\|_{L^2}}\right)^{-1/2},\quad\text{for every }t\in[0,T].
\]
(14)
B) Let further $0<c_P<\infty$ be a (‘inverse Poincaré’) constant such that
\[
\frac{\|u(0)-v(0)\|_V}{\|u(0)-v(0)\|_{L^2}}\leq c_P.
\]
(15)
Then there exists a constant $c_2=c_2(U,\nu,T,\|f\|_{L^2})$ such that
\[
\|u(0)-v(0)\|_{L^2(\Omega)}\leq e^{c_2c_P}\|u(t)-v(t)\|_{L^2(\Omega)},\quad\text{for every }t\in[0,T].
\]
(16)''',r'''There exists a sequence of initial conditions $u_j(0)\in C^\infty(\Omega)^2\cap V$, $j\in\mathbb N$, with corresponding strong solutions $u_j(t)$ to the periodic Navier-Stokes equations (10) on $\Omega$ with $\nu=1/2,f=0$, such that
\[
\|u_j(0)\|_{H^2}\lesssim1,\quad\|u_j(0)\|_{L^2}\simeq j^{-2},\quad\|u_j(t)\|_{L^2}\simeq e^{-j^2t}j^{-2},
\]
(17)
for all $t>0$. In particular, setting $v(0)=0$ and hence $v(t)\equiv0$, we have for some $c'=c'(c,t)>0$ that
\[
\|u_j(0)-v(0)\|_{L^2(\Omega)}\geq c'\frac1{\log\left(\frac1{\|u_j(t)-v(t)\|_{L^2}}\right)},\quad\text{all }j\in\mathbb N,t>0.
\]
(18)''',r'''Consider a Gaussian process prior as in Condition 1 with $\alpha\geq2$, RKHS $\mathcal H$, and resulting posterior distribution (21) arising from observations (19) in the 2-dimensional periodic Navier-Stokes equations (10) with either $0\leq T_0<T$ or $T_0=T>0$. Suppose the ground truth initial condition $\theta_0$ lies in $\mathcal H$. Then for every $T_P\geq T$ there exists a sequence $\eta_N=O(1/\sqrt{\log N})$ as $N\to\infty$ (with constants uniform in $\|\theta_0\|_{\mathcal H}\leq U$) such that
\[
\Pi\left(\theta\in V:\sup_{0<t\leq T_p}\|u_\theta(t,\cdot)-u_{\theta_0}(t,\cdot)\|_{L^2(\Omega)^2}<\eta_N\mid Z^{(N)}\right)\to^{P_{\theta_0}^N}1
\]
(23)
as well as
\[
\Pi\left(\theta\in V:\|\theta-\theta_0\|_{L^2(\Omega)^2}<\eta_N\mid Z^{(N)}\right)\to^{P_{\theta_0}^N}1.
\]
(24)
Moreover, if
\[
\bar\theta_N=E^\Pi[\theta\mid Z^{(N)}]\in V
\]
is the posterior (‘Bochner-’) mean and $u_{\bar\theta_N}$ the solution of the Navier-Stokes equation (10) with initial condition $\bar\theta_N$, then
\[
\|\bar\theta_N-\theta_0\|_{L^2(\Omega)^2}+\sup_{0<t\leq T_p}\|u_{\bar\theta_N}(t,\cdot)-u_{\theta_0}(t,\cdot)\|_{L^2(\Omega)^2}=O_{P_{\theta_0}^N}(\eta_N).
\]
(25)''',r'''Consider periodic solutions of the Navier-Stokes equations (10) with viscosity $\nu=1/2$, forcing $f=0$, and observations $Z^{(N)}$ arising as in (19) with either $0<T_0<T$ or $T_0=T>0$. Then there exists $c=c(U,T)>0$ such that
\[
\liminf_{N\to\infty}\inf_{\widetilde\theta_N}\sup_{\theta\in V:\|\theta\|_{H^2}\leq U}P_\theta^N\left(\|\widetilde\theta_N-\theta\|_{L^2}>\frac{c}{\log N}\right)>1/4,
\]
(26)
where the infimum extends over all estimators $\widetilde\theta_N$ of $\theta$ (i.e., all measurable functions of $Z^{(N)}$ taking values in the space $V$).''',r'''Denote by $(e_j:j\in\mathbb N)\subset V$ an enumeration of the $L^2$-orthonormal basis of $H$ arising from the eigenfunctions of the Stokes operator $A$ from (20), ordered by increasing eigenvalues. Let the prior $\Pi$ be as in Condition 1 and project it onto the span $E_J=\{e_j:j\leq J\}$ with $J=J_N=O(\log\log N)$. Suppose the ground truth initial condition $\theta_0$ lies in $\mathcal H\cap E_{J_0}$ for some arbitrary fixed $J_0\in\mathbb N$. Then the conclusions of Theorem 3 remain true with convergence rate
\[
\eta_N=(\log N)^\beta\times N^{-\alpha/(2\alpha+2)},\quad\text{some }\beta>0.
\]''']
def inventory():
    pages=[6,7,10,10,11]
    claims=[dict(claim_id=PID+f'/T{i}',paper_id=PID,claim_kind='theorem',label=f'Theorem {i}',source_order=i,statement_original=s,evidence=[dict(page=pages[i-1],location=f'Theorem {i}; complete printed statement, all hypotheses and conclusions')]) for i,s in enumerate(STATEMENTS,1)]
    paper=dict(paper_id=PID,title='On posterior consistency of data assimilation with Gaussian process priors: The 2D-Navier–Stokes equations',authors=['Richard Nickl','Edriss S. Titi'],version='arXiv:2307.08136v3; arXiv stamp 9 Jul 2024',pdf_pages=19,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=18,main_text_boundary=dict(location='Main text ends after Acknowledgements on PDF page 18, before REFERENCES at y=328.647. Retained page-18 text and image evidence are clipped at y=327.6. The bibliography is excluded; Section 3 Proofs is in the main text, not an appendix.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Independent enumeration of actual small-cap THEOREM headings on pages 6, 7, 10 and 11, with complete visual comparison. Citations, proof headings, Propositions, Lemmas, Corollaries and Remarks are not inventoried.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v3 only; no website lookup or published-source substitution. Bibliography and appendix material excluded.',normalization_policy='Original wording, formulas, constants, quantifiers and branches preserved; PDF wrapping normalized into LaTeX. T_P versus T_p, the source span notation and the c-prime dependency are not silently corrected.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved five complete main-text Theorems; independent inventory review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
