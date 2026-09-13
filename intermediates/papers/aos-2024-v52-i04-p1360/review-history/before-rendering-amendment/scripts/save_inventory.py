"""Rebuild the manually transcribed original main-text theorem inventory."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1360'
SHA='af1faf7d9821a3f94ea242503fa4d26d7c6adb6c4ec6b0ff34719b8a740c89fc'
claims=[]

def claim(number,title,pages,text):
    claims.append(dict(claim_id=f'{PID}/T{number}',paper_id=PID,claim_kind='theorem',label=f'Theorem {number} ({title})',source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location=f'Theorem {number}, original statement'+(' continued across pages' if len(pages)>1 else '')) for p in pages]))

claim('1','Coverage error expansion for batching',[6],r'''
Suppose that $\psi(\widehat P_1)$ has a valid Edgeworth expansion, in the sense that for some $0<\sigma<\infty$,
\[
P\left(\frac{\sqrt n(\psi(\widehat P_1)-\psi)}{\sigma}\le q\right)=\Phi(q)+\sum_{j=1}^r n^{-j/2}p_j(q)\phi(q)+O\left(n^{-(r+1)/2}\right)\tag{1}
\]
holds uniformly over $q\in\mathbb R$, and $p_j$ is an even polynomial when $j$ is odd and is an odd polynomial when $j$ is even. Here $\Phi$ and $\phi$ are the distribution function and density function of standard normal. Then:

- For any $q\in\mathbb R$, there exists $c_j^{(B,K)}\in\mathbb R$, $j=1,2,\ldots,r$, such that
\[
P(W_B\le q)=P(t_{K-1}\le q)+\sum_{j=1}^r n^{-j/2}c_j^{(B,K)}+O(n^{-(r+1)/2})
\]
Here the coefficients $c_j^{(B,K)}$ depends on $K$, the distribution $P$, the objective function $\psi$ and the value of $q$, but do not depend on $n$.

- $P(-q\le W_B\le q)=P(-q\le t_{K-1}\le q)+O(n^{-1})$.
''')
claim('2','Coverage error expansions for all methods',[7,8],r'''
Suppose that $\psi(\cdot)$ is a statistical functional mapping from distributions in $\mathbb R^d$ to $\mathbb R$ defined by $\psi(\overline P)=f(E_{\overline P}X)$ for a vector $X\sim\overline P$, $X\in\mathbb R^d$. Assume the following Cramer's condition holds for the distribution of $X_1\in\mathbb R^d$ (recall that $X_1,\ldots,X_{nK}$ are drawn i.i.d. from $P$):
\[
\limsup_{|t|\to\infty}|E_P(\exp\{i\langle t,X\rangle\})|<1,\tag{4}
\]
Suppose that for some positive integer $r$, $X$ has finite moments up to order $r+2$ with nonsingular covariance, and $f$ is $r+1$ times differentiable in a neighborhood of $E_PX$ with $\nabla f(E_PX)\ne0$. Then:

- If $K\ge r+3$, then for any $q\in\mathbb R$, there exists $c_j^{(SJ,K)}\in\mathbb R$, $j=1,2,\ldots,r$, such that
\[
P(W_{SJ}\le q)=P(t_{K-1}\le q)+\sum_{j=1}^r n^{-j/2}c_j^{(SJ,K)}+O(n^{-(r+1)/2})
\]
Here the coefficients $c_j^{(SJ,K)}$ depends on $K$, the distribution $P$ that generates each $X_i$, the objective function $f$ and the value of $q$, but does not depend on $n$.

- Suppose that $K\ge4$. Then we have $P(-q\le W_{SJ}\le q)=P(-q\le t_{K-1}\le q)+O(n^{-1})$.

The same result holds if $W_{SJ}$ is replaced by $W_S$, $W_{SB}$ or $W_B$ and the coefficients $c_j^{(SJ,K)}$, $j=1,2,\ldots,r$ are replaced with a different set of coefficients corresponding to each method.
''')
claim('3','Coverage error expansions for batching methods on dependent data bearing recurrent atoms with gaps between successive batches',[9],r'''
Suppose that $X_i$, $i=1,2,\ldots$ is a Harris-recurrent and strictly stationary Markov chain with a recurrent atom $A_0$ and stationary distribution $P$. Moreover, suppose that $n^{\frac{r+1}{2\delta}}\alpha(n)\to0$ as $n\to0$ for some positive integer $r$. Let
\[
\tau=\min\{n>0:X_n\in A_0\},\quad G=\sum_{i=1}^\tau|g(X_i)|
\]
Suppose the uniform Cramer condition holds: there exists $\delta'<1$ such that $|E_P\exp(iuX_1+iv\tau)|<\delta'$ for all $v\in\mathbb R$ and all $u\in\mathbb R^d$ with $\|u\|>c$. Suppose further that $E\tau^{r+3}<\infty$, $EG^{r+3}<\infty$. Suppose that $f$ is $r$ times differentiable in a neighborhood of $E_Pg(X_1)$ and $\nabla f(E_Pg(X_1))\ne0$. Moreover, suppose that $K\ge r+3$.
Then for any $q\in\mathbb R$, there exists $\bar c_j^{(SJ,K)}\in\mathbb R$, $j=1,2,\ldots,r$, such that
\[
P(W_{SJ}\le q)=P(t_{K-1}\le q)+\sum_{j=1}^r n^{-j/2}\bar c_j^{(SJ,K)}+O(n^{-(r+1)/2})
\]
Here the coefficients $\bar c_j^{(SJ,K)}$ depends on $K$, the stationary distribution $P$, the objective function $g$ and the value of $q$, but does not depend on $n$. The same result holds if $W_{SJ}$ is replaced by $W_S$, $W_{SB}$ or $W_B$ and the coefficients $\bar c_j^{(SJ,K)}$, $j=1,2,\ldots,r$ are be replaced with a different set of coefficients corresponding to each method.
''')
claim('4','Coverage error expansions for batching methods on dependent data with gaps between successive batches',[10,11],r'''
Suppose that $X_i$, $i=1,2,\ldots$ is a Harris-recurrent Markov chain and is strictly stationary. Moreover, suppose that $n^{\frac{r+1}{2\delta}}\alpha(n)\to0$ for some positive integer $r$. Let $P$ be the stationary distribution.
Suppose that there exist a set $C$, a positive $\lambda$ and a probability measure $\varphi_C$ concentrated on $C$ such that
\[
P_x\left(\bigcup_{i=1}^\infty\{X_i\in C\}\right)=1
\]
for any $x$ and
\[
P_x(X_2\in A)\ge\lambda\varphi_C(A)
\]
for any $x\in C$, $A\subset C$. For any distribution $\alpha$, define $P_{\alpha,\lambda}$ as the measure of the process $\{(X_i,b_i),i=1,2,\ldots\}$ with initial distribution
\[
P_{\alpha,\lambda}(X_1\in dx,b_1=\delta)=\alpha(dx)(\lambda\delta+(1-\lambda)(1-\delta))
\]
and transition probability
\[
P_{\alpha,\lambda}((x,1),A\times\{\delta\})=
\begin{cases}
(\lambda\delta+(1-\lambda)(1-\delta))P(x,A)&x\notin C\\
(\lambda\delta+(1-\lambda)(1-\delta))\varphi_C(A)&x\in C
\end{cases}
\]
\[
P_{\alpha,\lambda}((x,0),A\times\{\delta\})=
\begin{cases}
(\lambda\delta+(1-\lambda)(1-\delta))P(x,A)&x\notin C\\
(\lambda\delta+(1-\lambda)(1-\delta))Q(x,A)&x\in C
\end{cases}
\]
where $P(x,\dot{\ })$ is the transition probability of $X_i$, $i=1,2,\ldots$ and $Q(x,\cdot)=(1-\lambda)^{-1}(P(x,\cdot)-\lambda\varphi_C(\cdot))$. Let
\[
\tau=\min\{n>0:X_n\in C,b_n=1\},\quad\tilde g(x)=g(x)-Eg(X_1),\quad\Sigma_{g,n}=n^{-1/2}\sum_{i=1}^n\tilde g(X_i),\quad G=\sum_{i=1}^\tau\tilde g(X_i).
\]
Suppose that

(i) $\limsup_{|t|\to\infty}|E_{\varphi_C,\lambda}\exp(itG)|<1$.

(ii) $\sigma_G:=E_{\varphi_C,\lambda}G^2>0$

(iii) $E_{\varphi_C,\lambda}\tau^{r+3}<\infty$, $E_{P,\lambda}\tau^{r+1}<\infty$

(iv) $E_{\varphi_C,\lambda}(\sum_{i=1}^\tau|g(X_i)|)^{r+3}<\infty$, $E_{P,\lambda}(\sum_{i=1}^\tau|g(X_i)|)^{r+1}<\infty$

Then,

- If $K\ge r+3$, then for any $q\in\mathbb R$, there exists $\bar{\bar c}_j^{(SJ,K)}\in\mathbb R$, $j=1,2,\ldots,r$, such that
\[
P(W_{SJ}\le q)=P(t_{K-1}\le q)+\sum_{j=1}^r n^{-j/2}\bar{\bar c}_j^{(SJ,K)}+O(n^{-(r+1)/2})
\]
Here the coefficients $\bar{\bar c}_j^{(SJ,K)}$ depends on $K$, the stationary distribution $P$, the objective function $g$ and the value of $q$, but does not depend on $n$.

- Suppose that $K\ge4$. Then $P(-q\le W_{SJ}\le q)=P(-q\le t_{K-1}\le q)+O(n^{-1})$.

The same result holds if $W_{SJ}$ is replaced by $W_S$, $W_{SB}$ or $W_B$ and the coefficients $\bar{\bar c}_j^{(SJ,K)}$, $j=1,2,\ldots,r$ are be replaced with a different set of coefficients corresponding to each method.
''')
claim('5','Coverage error expansions for batching methods on dependent data using regenerative cycles',[11],r'''
Suppose that the following Cramer's condition holds for the distribution of $Q_i$:
\[
\limsup_{|t|\to\infty}|E[\exp\{i\langle t,Q_1\rangle\}]|<1,\tag{5}
\]
Suppose that for some positive integer $r$, $Q_1$ has finite moments up to order $r+2$ with nonsingular covariance. Suppose that $E[T_2-T_1]>0$. Then:

- If $K\ge r+3$, then for any $q\in\mathbb R$, there exists $\tilde c_j^{(SJ,K)}\in\mathbb R$, $j=1,2,\ldots,r$, such that
\[
P(W_{SJ}\le q)=P(t_{K-1}\le q)+\sum_{j=1}^r n^{-j/2}\tilde c_j^{(SJ,K)}+O(n^{-(r+1)/2})
\]
Here the coefficients $\tilde c_j^{(SJ,K)}$ depends on $K$, the true distribution of $Q_1$, and the value of $q$, but does not depend on $n$.

- Suppose that $K\ge4$. Then we have $P(-q\le W_{SJ}\le q)=P(-q\le t_{K-1}\le q)+O(n^{-1})$.

The same result holds if $W_{SJ}$ is replaced by $W_S$, $W_{SB}$ or $W_B$ and the coefficients $\tilde c_j^{(SJ,K)}$, $j=1,2,\ldots,r$ are be replaced with a different set of coefficients corresponding to each method.
''')
claim('6',r'Unbiasedness of simulation algorithm to estimate coefficients of $n^{-1}$',[12],r'''
Suppose that the conditions of Theorem 2 hold with $r=2$, and the expansion is given as (6) where $W_\cdot$ can be any of $W_S$, $W_B$, $W_{SB}$ and $W_{SJ}$. Then, Algorithm 1 returns an unbiased estimator for $c$.
''')
claim('7','Asymptotic coverages as number of batches grows',[14],r'''
Suppose that we are under the setting introduced in Section 3. In particular, we have i.i.d. data $X_1,\ldots,X_{nK}$ drawn from $P$. Suppose that $\psi(\cdot)$ is continuously Gateaux differantiable at $P$ with influence function $IF$. Suppose that $E\psi(\widehat P_1)-\psi\ne0$ (i.e., $\psi(\widehat P_1)$ is a biased estimator of $\psi$), $\operatorname{Var}(\psi(\widehat P_1))<\infty$, and $\operatorname{Var}_P IF=\sigma^2$, $0<\sigma<\infty$. Fix $n$ and let $K\to\infty$.
Then for any $q>0$,
\[
P(-q\le W_B\le q)\to0,
\]
\[
P(-q\le W_S\le q)\to\Phi\left(q\sqrt{nE(\psi(\widehat P_1)-\psi)^2}/\sigma\right)-\Phi\left(-q\sqrt{nE(\psi(\widehat P_1)-\psi)^2}/\sigma\right),
\]
while
\[
P(-q\le W_{SJ}\le q)\to\Phi(q)-\Phi(-q).
\]
''')

def main():
    pdf=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(pdf.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='Higher-order coverage errors of batching methods via Edgeworth expansions on t-statistics',authors=['Shengyi He','Henry Lam'],version='arXiv:2111.06859v1, 12 November 2021',source_url='https://arxiv.org/pdf/2111.06859v1',pdf_pages=46,pdf_sha256=SHA,main_text_last_pdf_page=22,main_text_boundary=dict(location='Main text and references end on PDF page 22 above the Appendix A heading at y=202.908 PDF points. Appendix bodies are excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Verified local arXiv v1 PDF, pages 1-21 and references above Appendix A on page 22; appendix bodies excluded.'),papers=[paper],claims=claims)
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
