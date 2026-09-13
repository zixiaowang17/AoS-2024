"""Rebuild the manually transcribed original main-text theorem inventory."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1384'
SHA='d86f8493430c8c07106847a073666a82c9aa765fc33cd8f20a9dc25c8615aeae'
claims=[]

def claim(number,pages,text,title=None):
    label=f'Theorem {number}'+(f' ({title})' if title else '')
    claims.append(dict(claim_id=f'{PID}/T{number}',paper_id=PID,claim_kind='theorem',label=label,source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location=f'Theorem {number}, complete original statement'+(' continued across pages' if len(pages)>1 else '')) for p in pages]))

claim('2.1',[7,8],r'''
Suppose $v$ satisfies Assumptions 1, 2, and 3, and let $\hat m,\hat S$ be as in Lemma 2.1. Let $g$ be a function satisfying the following inequality for some $R_g>0$:
\[
\left|g(x)-\int gd\hat\pi\right|\le\exp\left(c_0\sqrt d\|x-\hat m\|_{\hat S^{-1}}/4\right),\quad\forall x:\ \|x-\hat m\|_{\hat S^{-1}}\ge R_g\sqrt d.\tag{2.7}
\]
Then
\[
\left|\int gd\pi-\int gd\hat\pi\right|\lesssim\left(1+\operatorname{Var}_{\hat\pi}(g)^{\frac12}\right)\left(a_3\epsilon+a_4\epsilon^2\right),\tag{2.8}
\]
If additionally, $g$ is even about $\hat m$, then
\[
\left|\int gd\pi-\int gd\hat\pi\right|\lesssim\left(1+\operatorname{Var}_{\hat\pi}(g)^{\frac12}\right)(a_3^2+a_4)\epsilon^2.\tag{2.9}
\]
Finally, if $g$ is linear, then
\[
\left|\int gd\pi-\int gd\hat\pi\right|\lesssim\left(1+\operatorname{Var}_{\hat\pi}(g)^{\frac12}\right)\left(\left(a_3^3+a_3a_4\right)\epsilon^3+a_4^2\epsilon^4\right).\tag{2.10}
\]
In all the above bounds, the suppressed constant is an increasing function of $q$, $c_0^{-1}$, and $R_g$.
''')
claim('2.2',[8],r'''
Suppose $v$ satisfies Assumptions 1, 2, and 3. Define the function
\[
Q(x)=\left\langle\mathbb E_{X\sim\hat\pi}[\nabla^3V(X)],\ \frac12(x-\hat m)\otimes\hat S-\frac16(x-\hat m)^{\otimes3}\right\rangle.\tag{2.11}
\]
If $g$ satisfies (2.7), then
\[
\left|\int gd\pi-\int gd\hat\pi-\int gQd\hat\pi\right|\lesssim\left(1+\operatorname{Var}_{\hat\pi}(g)^{\frac12}\right)(a_3^2+a_4)\epsilon^2.\tag{2.12}
\]
The suppressed constant is an increasing function of $q$, $c_0^{-1}$, and $R_g$.
''','Leading order term in VI approximation error')
claim('3.1',[14],r'''
Suppose $d/\sqrt n$ and $n^{-1}$ are smaller than certain absolute constants. On an event of probability at least $1-\exp(-C(nd)^{1/9})-5e^{-Cn}-n^{-d/4}$, the following results hold.

There exists a unique solution $\hat m,\hat S$ to (1.9) in the region $\mathcal R_V$. Furthermore, if $g$ satisfies (2.7) with $c_0=1/8$, then
\[
\begin{aligned}
\left|\int gd\pi-\int gd\hat\pi\right|&\lesssim_{R_g}\left(1+\operatorname{Var}_{\hat\pi}(g)^{\frac12}\right)\frac d{\sqrt n},\\
\left|\int gd\pi-\int gd\hat\pi-\int gQd\hat\pi\right|&\lesssim_{R_g}\left(1+\operatorname{Var}_{\hat\pi}(g)^{\frac12}\right)\left(\frac d{\sqrt n}\right)^2,
\end{aligned}\tag{3.8}
\]
where $Q$ is defined in (3.7) and (3.6). If $g$ is even about $\hat m$, then
\[
\left|\int gd\pi-\int gd\hat\pi\right|\lesssim_{R_g}\left(1+\operatorname{Var}_{\hat\pi}(g)^{\frac12}\right)\left(\frac d{\sqrt n}\right)^2.\tag{3.9}
\]
If $g$ is linear, then
\[
\left|\int gd\pi-\int gd\hat\pi\right|\lesssim_{R_g}\left(1+\operatorname{Var}_{\hat\pi}(g)^{\frac12}\right)\left(\frac d{\sqrt n}\right)^3.\tag{3.10}
\]
Next, we have
\[
\begin{aligned}
\sup_{A\in\mathcal B(\mathbb R^d)}|\pi(A)-\hat\pi(A)|&\lesssim\frac d{\sqrt n},\\
\sup_{A\in\mathcal B_{s,\hat m}(\mathbb R^d)}|\pi(A)-\hat\pi(A)|&\lesssim\left(\frac d{\sqrt n}\right)^2.
\end{aligned}\tag{3.11}
\]
Finally, let $\bar\theta=\int\theta d\pi(\theta)$ be the mean of $\pi$ and $\Sigma=\int(\theta-\bar\theta)(\theta-\bar\theta)^T d\pi(\theta)$ be the covariance of $\pi$. Then
\[
\begin{aligned}
\sqrt n\|\bar m-\hat m\|&\lesssim\left(\frac d{\sqrt n}\right)^3,\\
n\|\Sigma-\hat S\|&\lesssim\left(\frac d{\sqrt n}\right)^2
\end{aligned}\tag{3.12}
\]
In (3.11) and (3.12), all suppressed constants are absolute.
''')
claim('4.1',[16],r'''
Let $f=g\circ T^{-1}$, where $T$ is as in (4.2), and let $g$ satisfy (2.7). Also, let $\rho\propto e^{-V_0}$ as in (4.3), and $\Delta_f=\int fd\rho-\int fd\gamma$. Then under the conditions of Theorem 2.1, it holds
\[
|\Delta_f|\lesssim(1+\|f_0\|_2)\left(a_3\epsilon+a_4\epsilon^2\right),\tag{4.4}
\]
\[
\left|\Delta_f-\int f(-p_3)d\gamma\right|\lesssim(1+\|f_0\|_2)(a_3^2+a_4)\epsilon^2.\tag{4.5}
\]
If $f$ is orthogonal to all third order Hermite polynomials (in particular, if $f$ is even), then
\[
|\Delta_f|\lesssim(1+\|f_0\|_2)(a_3^2+a_4)\epsilon^2.\tag{4.6}
\]
If $f$ is linear, then
\[
|\Delta_f|\lesssim(1+\|f_0\|_2)\left(\left(a_3^3+a_3a_4\right)\epsilon^3+a_4^2\epsilon^4\right).\tag{4.7}
\]
In all of the above bounds, the suppressed constant is an increasing function of $q$, $c_0^{-1}$, $R_g$.
''')

def main():
    pdf=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='On the approximation accuracy of Gaussian variational inference',authors=['Anya Katsevich','Philippe Rigollet'],version='arXiv:2301.02168v2, 7 January 2024; title-page date 9 January 2024',source_url='https://arxiv.org/pdf/2301.02168v2',pdf_pages=49,pdf_sha256=SHA,main_text_last_pdf_page=22,main_text_boundary=dict(location='Main text ends after Acknowledgments on PDF page 22, before the appendix notation prelude beginning at y=297.2278137207031 PDF points. Appendix prelude and all appendix bodies are excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Verified local arXiv v2 PDF, pages 1-21 and page 22 above the appendix notation prelude; no appendix content.'),papers=[paper],claims=claims)
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
