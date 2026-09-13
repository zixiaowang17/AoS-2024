"""Rebuild the manually transcribed main-text theorem inventory."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1307'
SHA='b0b01164cab1ebda27f9a4698b232a5557671feb0b1d940fe49cbcc70901247d'
claims=[]

def claim(number,page,text):
    claims.append(dict(claim_id=f'{PID}/T{number}',paper_id=PID,claim_kind='theorem',label=f'Theorem {number}',source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=page,location=f'Theorem {number}, complete printed statement')]))

claim('2.3',6,r'''
Under Assumption H the matrix $\Sigma_\vartheta\in\mathbb R^{p\times p}$ with entries
\[
(\Sigma_\vartheta)_{ij}=(T/2)\langle(-\nabla\cdot a_\vartheta\nabla)^{-1/2}A_i^*K,(-\nabla\cdot a_\vartheta\nabla)^{-1/2}A_j^*K\rangle_{L^2(\mathbb R^d)}
\]
is invertible and $\rho_\delta\mathcal I_\delta\rho_\delta\xrightarrow{\mathbb P}\Sigma_\vartheta$ as $\delta\to0$. Moreover, the augmented MLE satisfies the CLT
\[
(\rho_\delta\mathcal I_\delta\rho_\delta)^{1/2}\rho_\delta^{-1}(\widehat\vartheta_\delta-\vartheta)\xrightarrow{d}\mathcal N(0,\|K\|_{L^2(\mathbb R^d)}^2 I_{p\times p}),\qquad\delta\to0,
\]
or, equivalently,
\[
(M^{1/2}\delta^{1-n_i}(\widehat\vartheta_{\delta,i}-\vartheta_i))_{i=1}^p\xrightarrow{d}\mathcal N(0,\|K\|_{L^2(\mathbb R^d)}^2\Sigma_\vartheta^{-1}).
\]
''')
claim('3.1',7,r'''
Let $(H_X,\|\cdot\|_X)$ be the RKHS of the process $X$ in (3.1). Let $T\ge1$. Then
\[
H_X=\{h\in L^2([0,T];\mathcal H):h\text{ absolutely continuous},\ Ah,h'\in L^2([0,T];\mathcal H)\}
\]
and for $h\in H_X$
\[
\|h\|_X^2=\|Ah\|_{L^2([0,T];\mathcal H)}^2+\|h'\|_{L^2([0,T];\mathcal H)}^2+\|(-A)^{1/2}h(0)\|_{\mathcal H}^2+\|(-A)^{1/2}h(T)\|_{\mathcal H}^2,
\]
as well as
\[
\|h\|_X^2\le3\|Ah\|_{L^2([0,T];\mathcal H)}^2+\|h\|_{L^2([0,T];\mathcal H)}^2+2\|h'\|_{L^2([0,T];\mathcal H)}^2.
\]
''')
claim('3.2',8,r'''
For $K_1,\ldots,K_M\in\mathcal D(A)$ and with $X$ in (3.1) consider the process $X_K$ with $X_K(t)=(\langle X(t),K_k\rangle_{\mathcal H})_{k=1}^M$. Suppose that the Gram matrix $G=(\langle K_k,K_l\rangle_{\mathcal H})_{1\le k,l\le M}$ is non-singular, and let $G_A=(\langle AK_k,AK_l\rangle_{\mathcal H})_{1\le k,l\le M}$. Let $T\ge1$. Then the RKHS $(H_{X_K},\|\cdot\|_{X_K})$ of $X_K$ satisfies $H_{X_K}=H^M$, where
\[
H=\{h\in L^2([0,T]):h\text{ absolutely continuous},h'\in L^2([0,T])\}
\]
and for $h=(h_k)_{k=1}^M\in H_{X_K}$
\[
\|h\|_{X_K}^2\le(3\|G^{-1}\|_{\mathrm{op}}^2\|G_A\|_{\mathrm{op}}+\|G^{-1}\|_{\mathrm{op}})\sum_{k=1}^M\|h_k\|_{L^2([0,T])}^2+2\|G^{-1}\|_{\mathrm{op}}\sum_{k=1}^M\|h_k'\|_{L^2([0,T])}^2.
\]
''')
claim('4.1',9,r'''
Grant Assumption L with $M\ge1$, $T\ge1$ and let $i\in\{1,2,3\}$. Then there exist constants $c_1,c_2>0$ depending only on $K$ and an absolute constant $c_3>0$ such that the following assertions hold:

(i) If $\delta^{n_i-1}/\sqrt{TM}<1$ and $\delta\le c_1$, then
\[
\inf_{\widehat\vartheta_i}\sup_{\substack{\vartheta\in\Theta_i\\|\vartheta-(1,0,0)^\top|\le c_2\frac{\delta^{n_i-1}}{\sqrt{TM}}}}\mathbb P_\vartheta\left(|\widehat\vartheta_i-\vartheta_i|\ge\frac{c_2}2\frac{\delta^{n_i-1}}{\sqrt{TM}}\right)>c_3.
\]

(ii) If $\delta^{n_i-1}/\sqrt{TM}\ge1$ and $\delta\le c_1$, then
\[
\inf_{\widehat\vartheta_i}\sup_{\substack{\vartheta\in\Theta_i\\|\vartheta-(1,0,0)^\top|\le c_2}}\mathbb P_\vartheta(|\widehat\vartheta_i-\vartheta_i|\ge c_2/2)>c_3.
\]

In (i) and (ii), the infimum is taken over all real-valued estimators $\widehat\vartheta_i=\widehat\vartheta_i(X_\delta)$.
''')
claim('4.3',10,r'''
Theorem 4.1 remains valid when the infimum is taken over all real-valued estimators $\widehat\vartheta_i=\widehat\vartheta_i(X_\delta,X_\delta^\Delta,X_\delta^{\nabla\cdot b})$, provided that $K$, $\Delta K$ and $(\nabla\cdot b)K$ are linearly independent and Assumption L holds for $K$, $\Delta K$ and $(\nabla\cdot b)K$.
''')

def main():
    pdf=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='Optimal parameter estimation for linear SPDEs from multiple measurements',authors=['Randolf Altmeyer','Anton Tiepner','Martin Wahl'],version='arXiv:2211.02496v2, 25 July 2024',source_url='https://arxiv.org/pdf/2211.02496v2',pdf_pages=42,pdf_sha256=SHA,main_text_last_pdf_page=24,main_text_boundary=dict(location='Main text ends on PDF page 24 after Lemmas 6.11-6.12 and the concluding proof paragraph for Theorem 4.1. Appendix A begins at y=493.750 PDF points on that same page. Appendix bodies are excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Verified local arXiv v2 PDF, pages 1-23 and main text above Appendix A on page 24; appendix bodies excluded.'),papers=[paper],claims=claims)
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
