"""Preserve original ridge regression definitions, assumptions and resolvent source passages."""
import json,hashlib
from save_inventory import ROOT,PID,STATEMENTS
REVIEW_ROOT=ROOT
interfaces=[];members={}
def add(n,term,s,pages,deps,symbols,boundary,heading,kind='definition',context=None,context_page=None,phrases=None):
    lid=f'D{n}'
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=phrases or [])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context,(lid,term)
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original naming context')])];kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='definition',type_shape=boundary,semantic_boundary=boundary,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))
add(1,'real, separable Hilbert space',r'''In this paper, we assume the dimension $d\in\mathbb Z_{\ge0}\cup\{\infty\}$. When $d<\infty$, we are in the usual setup of linear model with finite dimensional features. In the case $d=\infty$, we assume that the $\boldsymbol x_i$’s’ are i.i.d. random vectors from a real, separable Hilbert space $\mathcal H$. We will use $\|\boldsymbol x\|$ to denote the norm and $\langle\boldsymbol x_1,\boldsymbol x_2\rangle$ or $\boldsymbol x_1^\top\boldsymbol x_2$ to denote the scalar product in this space. We understand the infinite dimensional matrix $\boldsymbol x\boldsymbol x^\top$ as an operator $\mathcal H\to\mathcal H:\boldsymbol\beta\to\langle\boldsymbol x,\boldsymbol\beta\rangle\boldsymbol x$. Given a linear operator $\boldsymbol A:\mathcal H\to\mathcal H$, we denote by $\|\boldsymbol A\|$ the associated operator norm.''',[5],[],[r'$d=\infty$',r'\|\boldsymbol A\|'],'Original ambient feature space and norms; infinite covariance operators are allowed, while whitened coordinates need not form an H-valued random vector.','Section 2 — Hilbert feature space',kind='source_passage')
add(2,'covariance operator',r'''We will assume the covariance operator $\boldsymbol\Sigma=\mathbb E[\boldsymbol x\boldsymbol x^\top]$ to be trace-class, namely
\[
\operatorname{Tr}(\boldsymbol\Sigma)=\mathbb E\{\|\boldsymbol x_i\|^2\}<\infty,
\]
and, without loss of generality, we also assume $\|\boldsymbol\Sigma\|=1$.

We denote its eigenvalues by $1=\sigma_1\ge\sigma_2\ge\cdots$ in non-increasing order.''',[5],[1],[r'\boldsymbol\Sigma=\mathbb E[\boldsymbol x\boldsymbol x^\top]',r'\operatorname{Tr}(\boldsymbol\Sigma)'],'Original trace-class positive covariance normalized in operator norm, not assumed uniformly bounded below. Eigenvalues are specified in Assumption 1 and its separate tail envelope.','Section 2 — Covariance operator',kind='assumption')
add(3,'ground truth signal',r'''We assume $\|\boldsymbol\beta\|_{\boldsymbol\Sigma^{-1}}:=\|\boldsymbol\Sigma^{-1/2}\boldsymbol\beta\|<\infty$.

Letting $\boldsymbol\beta=\boldsymbol\Sigma^{1/2}\boldsymbol\theta$, $\|\boldsymbol\theta\|<\infty$,''',[5,9],[2],[r'\|\boldsymbol\beta\|_{\boldsymbol\Sigma^{-1}}',r'\boldsymbol\beta=\boldsymbol\Sigma^{1/2}\boldsymbol\theta'],'Original inverse-covariance norm assumption. Domain and nullspace conventions are not silently completed; this is stronger than merely finite prediction norm.','Assumption 1 — Signal condition',kind='condition',context=r'is the ground truth signal.',context_page=4)
add(4,'effective rank',r'''I. There exist $d_\Sigma:=d_\Sigma(n)\ge n$ such that, for all $1\le k\le\min\{n,d\}$
\[
\sum_{l=k}^d\sigma_l\le d_\Sigma\sigma_k.\tag{6}
\]''',[5],[2],[r'd_\Sigma:=d_\Sigma(n)',r'\sum_{l=k}^d\sigma_l'],'Original admissible tail envelope, including index k and the constraint d_Sigma>=n; not a uniquely minimized dimension.','Assumption 1(I)',kind='assumption',context=r'Define the effective rank $d_\Sigma(k)$ as in Eq. (6)',context_page=11)
add(5,'Independent sub-Gaussian coordinates',r'''(a) Independent sub-Gaussian coordinates: $\boldsymbol z_i$ has independent but not necessarily identically distributed coordinates with uniformly bounded sub-Gaussian norm. Namely: each coordinate $z_{ij}$ of $\boldsymbol z_i$ satisfies $\mathbb E[z_{ij}]=0$, $\operatorname{Var}(z_{ij})=1$ and $\|z_{ij}\|_{\psi_2}:=\sup_{p\ge1}p^{-\frac12}(\mathbb E[|z_{ij}|^p])^{\frac1p}\le C_x$.''',[6],[1],[r'\|z_{ij}\|_{\psi_2}'],'Original coordinate alternative (a); independence does not require identical distributions. The infinite coordinate-sequence interpretation retains the source limitation.','Assumption 1(II)(a)',kind='assumption')
add(6,'Convex concentration',r'''(b) Convex concentration: allowing $\boldsymbol z_i$ to have dependent coordinates, the following holds for any $1$-Lipschitz convex function $\varphi:\mathbb R^d\to\mathbb R$, and for every $t>0$
\[
\mathbb P(|\varphi(\boldsymbol z_i)-\mathbb E\varphi(\boldsymbol z_i)|\ge t)\le2\exp(-t^2/C_x^2).
\]''',[6],[1],[r'\mathbb P(|\varphi(\boldsymbol z_i)-\mathbb E\varphi(\boldsymbol z_i)|\ge t)'],'Original alternative (b), permitting dependent coordinates. Do not replace convex concentration by concentration for all Lipschitz functions or by Gaussianity.','Assumption 1(II)(b)',kind='assumption')
assumption=r'''We assume $\mathbb E[\boldsymbol x_i]=0$, $\boldsymbol\Sigma:=\mathbb E[\boldsymbol x_i\boldsymbol x_i^\top]$ is a trace class operator: $\operatorname{Tr}(\boldsymbol\Sigma)<\infty$ and (without loss of generality) $\|\boldsymbol\Sigma\|=1$. We denote its eigenvalues by $1=\sigma_1\ge\sigma_2\ge\cdots$ in non-increasing order. We assume $\|\boldsymbol\beta\|_{\boldsymbol\Sigma^{-1}}:=\|\boldsymbol\Sigma^{-1/2}\boldsymbol\beta\|<\infty$.
We further assume $\boldsymbol x_i=\boldsymbol\Sigma^{1/2}\boldsymbol z_i$ where the following hold.
'''+members['D4']['statement_original']+r'''
II. There exist $C_x>0$, such that one of the following condition holds:
'''+members['D5']['statement_original']+'\n'+members['D6']['statement_original']
add(7,'Assumption 1',assumption,[5,6],[2,3,4,5,6],[r'\boldsymbol x_i=\boldsymbol\Sigma^{1/2}\boldsymbol z_i'],'Complete original Assumption 1. Both coordinate conditions remain alternatives. Explicitly referenced by every stored theorem, including the resolvent theorem.','Assumption 1',kind='assumption',context=r'Assumption 1.',phrases=['Assumption 1'])
add(8,'data matrix',r'''Defining the data matrix
\[
\boldsymbol X=\begin{bmatrix}\boldsymbol x_1^\top\\\boldsymbol x_2^\top\\\vdots\\\boldsymbol x_n^\top\end{bmatrix}\in\mathbb R^{n\times d},
\]''',[4],[1],[r'\boldsymbol X=\begin{bmatrix}'],'Original row-wise feature design. Its definition does not introduce response noise; the common setting gives IID feature rows. For infinite d interpret it as a finite-output operator.','Section 2 — Data matrix')
add(9,'simple linear model',r'''We consider the simple linear model
\[
y_i=\boldsymbol x_i^\top\boldsymbol\beta+\varepsilon_i,\tag{3}
\]
where $\boldsymbol\beta\in\mathbb R^d$ is the ground truth signal. The random features $\boldsymbol x_i\in\mathbb R^d$ and noise $\varepsilon_i$ are independent, and the $(\boldsymbol x_i,\varepsilon_i)$ are i.i.d. samples with $1\le i\le n$. We assume $\boldsymbol x_i,\varepsilon_i$ are mean zero with covariances $\operatorname{Cov}(\boldsymbol x_i)=\boldsymbol\Sigma$ and $\operatorname{Var}(\varepsilon_i)=\tau^2$.''',[4],[1,2],[r'y_i=\boldsymbol x_i^\top\boldsymbol\beta+\varepsilon_i',r'\tau^2'],'Original regression sampling model with independent noise of fixed variance. No Gaussian-noise assumption is made. Keep separate from the design-only resolvent result.','Section 2 — Linear model (3)',kind='source_passage')
add(10,'ridge regression',r'''and use ridge regression for the estimator $\hat{\boldsymbol\beta}$. Denoting by $\boldsymbol X$ the matrix with rows $\boldsymbol x_1,\ldots,\boldsymbol x_n$, we have
\[
\begin{aligned}
\hat{\boldsymbol\beta}_\lambda&:=\operatorname*{argmin}_{\boldsymbol b}\left\{\frac1n\|\boldsymbol y-\boldsymbol X\boldsymbol b\|^2+\lambda\|\boldsymbol b\|^2\right\}\tag{1}\\
&=(\boldsymbol X^\top\boldsymbol X+n\lambda\boldsymbol I)^{-1}\boldsymbol X^\top\boldsymbol y.\tag{2}
\end{aligned}
\]''',[3],[8,9],[r'\hat{\boldsymbol\beta}_\lambda'],'Original ridge objective and inverse solution, with loss factor 1/n and inverse shift n*lambda. The positive-regularization domain is supplied by the Section 3 context.','Introduction — Ridge estimator (1)–(2)')
add(11,'ridgeless regression',r'''We will also be interested in the $\lambda\to0+$ limit of this estimator which (in the overparametrized case) corresponds to the minimum norm interpolator of the data, and refer to it as ‘ridgeless regression.’''',[3],[10],[r'$\lambda\to0+$'],'Original positive-limit convention. Do not use an ordinary inverse of singular sample covariance at lambda=0; interpolation requires the source rank conditions.','Introduction — Ridgeless limit')
add(12,'variance',r'''\[
\mathscr V_X(\hat{\boldsymbol\beta};\boldsymbol\beta)=\operatorname{Tr}(\boldsymbol\Sigma\operatorname{Cov}(\hat{\boldsymbol\beta}\mid\boldsymbol X)),
\]
For ridge regression, we can write explicit forms of variance and bias:
\[
\mathscr V_X(\lambda)=\frac{\tau^2}n\operatorname{Tr}(\boldsymbol\Sigma\cdot\hat{\boldsymbol\Sigma}(\hat{\boldsymbol\Sigma}+\lambda\boldsymbol I)^{-2}),\tag{5a}
\]''',[5],[2,9,10,14],[r'\mathscr V_X(\lambda)',r'\operatorname{Cov}(\hat{\boldsymbol\beta}\mid\boldsymbol X)'],'Original design-conditional estimator variance and its ridge formula, excerpted separately from bias. Its randomness is the design; response noise is averaged out.','Section 2 — Conditional variance (5a)')
add(13,'bias',r'''\[
\mathscr B_X(\hat{\boldsymbol\beta};\boldsymbol\beta)=\|\mathbb E_{\boldsymbol y}[\hat{\boldsymbol\beta}\mid\boldsymbol X]-\boldsymbol\beta\|_{\boldsymbol\Sigma}^2.
\]
For ridge regression, we can write explicit forms of variance and bias:
\[
\mathscr B_X(\lambda)=\lambda^2\langle\boldsymbol\beta,(\hat{\boldsymbol\Sigma}+\lambda\boldsymbol I)^{-1}\boldsymbol\Sigma(\hat{\boldsymbol\Sigma}+\lambda\boldsymbol I)^{-1}\boldsymbol\beta\rangle.\tag{5b}
\]''',[5],[2,10,14],[r'\mathscr B_X(\lambda)'],'Original squared conditional prediction bias, not an unsquared coefficient difference. The two empirical inverses surround population covariance; do not commute them.','Section 2 — Conditional bias (5b)')
add(14,'sample covariance',r'''let $s_{\min}$ be the minimum nonzero eigenvalue of the sample covariance $\hat{\boldsymbol\Sigma}=\boldsymbol X^\top\boldsymbol X/n$.''',[12],[8],[r'\hat{\boldsymbol\Sigma}=\boldsymbol X^\top\boldsymbol X/n',r's_{\min}'],'Original normalized sample covariance and its minimum nonzero eigenvalue. The latter is not the minimum eigenvalue of a singular d-by-d covariance.','Theorem 3 — Sample covariance and eigenvalue',kind='theorem_excerpt')
add(15,'effective regularization',r'''Define the effective regularization $\lambda_\star$ as the unique non-negative solution of
\[
n\cdot\left(1-\frac\lambda{\lambda_\star}\right)=\operatorname{Tr}(\boldsymbol\Sigma(\boldsymbol\Sigma+\lambda_\star\boldsymbol I)^{-1}),\tag{7}
\]''',[6],[2],[r'\lambda_\star',r'\lambda_\star(0)'],'Original scalar fixed-point definition. Positive lambda and zero-limit cases are distinguished in the main text; the zero endpoint cannot be read as a literal 0/0 equation without a convention.','Section 2 — Effective regularization (7)')
add(16,'effective variance',r'''\[
V_n(\lambda):=\frac{\tau^2\operatorname{Tr}(\boldsymbol\Sigma^2(\boldsymbol\Sigma+\lambda_\star\boldsymbol I)^{-2})}{n-\operatorname{Tr}(\boldsymbol\Sigma^2(\boldsymbol\Sigma+\lambda_\star\boldsymbol I)^{-2})},\tag{8}
\]''',[6],[2,9,15],[r'V_n(\lambda)'],'Original deterministic variance equivalent, including its feedback denominator. It is distinct from the sample-conditional variance.','Section 2 — Effective variance (8)',context=r'we then define the effective variance and bias as')
add(17,'bias',r'''\[
B_n(\lambda):=\frac{\lambda_\star^2\langle\boldsymbol\beta,(\boldsymbol\Sigma+\lambda_\star\boldsymbol I)^{-2}\boldsymbol\Sigma\boldsymbol\beta\rangle}{1-n^{-1}\operatorname{Tr}(\boldsymbol\Sigma^2(\boldsymbol\Sigma+\lambda_\star\boldsymbol I)^{-2})},\tag{9}
\]''',[6],[2,9,15],[r'B_n(\lambda)'],'Original deterministic effective bias, not the random bias formula (5b). The source names effective variance and bias together; preserve this particular formula separately.','Section 2 — Effective bias (9)',context=r'we then define the effective variance and bias as')
add(18,'Big-Oh notation',r'''For two functions $f(x)$ and $g(x)$ (where $x$ can be a scalar or a vector), we write $f(x)=O_\alpha(g(x))$ if there exists a constant $C_\alpha$ depending only on the value of $\alpha$ (also $\alpha$ can be either a scalar or a vector) such that $|f(x)|\le C_\alpha|g(x)|$ for all $x$. In particular, if the constant is universal we write $f(x)=O(g(x))$. Similarly, we write $f(x)=\Omega_\alpha(g(x))$ if $|f(x)|\ge C_\alpha|g(x)|$ for all $x$ and some constant $C_\alpha>0$. Finally, we write $f(x)=\Theta_\alpha(g(x))$ if we have both $f(x)=O_\alpha(g(x))$ and $f(x)=\Omega_\alpha(g(x))$.''',[9],[],[r'O_\alpha(g(x))'],'Original deterministic order notation with explicit constant dependencies, used inside high-probability statements; it is not a probabilistic O_P convention.','Section 3 — Big-Oh notation',context=r'Big-Oh notation')
add(19,'ratio between effective dimension and regularization parameter',r'''The ratio between effective dimension and regularization parameter:
\[
\chi_n(\lambda):=1+\frac{\sigma_{\lfloor\eta n\rfloor}d_\Sigma\log^2(d_\Sigma)}{n\lambda}.\tag{24}
\]
Here $\eta$ is a constant that only depends on $C_x$, and hence we will leave it implicit.''',[9],[2,4],[r'\chi_n(\lambda)'],'Original positive-ridge quantity with denominator n*lambda and effective-rank envelope. Its zero-limit replacement is a separate source entry.','Section 3.1 — Ratio (24)')
add(20,'ratio between regularization and effective regularization',r'''The ratio between regularization and effective regularization
\[
\kappa:=\min\left(\frac\lambda{\lambda_\star};1-\frac\lambda{\lambda_\star}\right)>0.\tag{25}
\]''',[9],[15],[r'\kappa:=\min'],'Original interior-regularization separation parameter in Theorem 1; Theorem 3 introduces a different freely chosen positive kappa rather than imposing (25) at lambda=0.','Section 3.1 — Ratio (25)')
add(21,'modified population resolvent',r'''For a positive semi-definite operator $\boldsymbol Q$, define the modified population resolvent:
\[
\mathscr R_0(\zeta,\mu;\boldsymbol Q):=\operatorname{Tr}(\boldsymbol\Sigma^{1/2}\boldsymbol Q\boldsymbol\Sigma^{1/2}(\zeta\boldsymbol I+\mu\boldsymbol\Sigma)^{-1}).\tag{26}
\]''',[9],[2],[r'\mathscr R_0(\zeta,\mu;\boldsymbol Q)'],'Original weighted population resolvent trace. Its script R must not be confused with the effective total-risk notation R_n or the theorem-local sans-serif shorthand.','Section 3.1 — Population resolvent (26)')
add(22,'ratio',r'''Letting $\boldsymbol\beta=\boldsymbol\Sigma^{1/2}\boldsymbol\theta$, $\|\boldsymbol\theta\|<\infty$, we consider the ratio
\[
\rho(\lambda):=\frac{\mathscr R_0(\lambda_\star,1;\boldsymbol\theta\boldsymbol\theta^\top/\|\boldsymbol\theta\|^2)}{\mathscr R_0(\lambda_\star,1;\boldsymbol I)}\in(0,1].\tag{27}
\]''',[9],[3,15,21],[r'\rho(\lambda)',r'\boldsymbol\beta=\boldsymbol\Sigma^{1/2}\boldsymbol\theta'],'Original directional-to-total population resolvent ratio and signal coordinates. The zero-signal normalization is undefined absent an added convention; preserve the source limitation.','Section 3.1 — Directional ratio (27)')
add(23,'ratio between effective dimension and regularization parameter',r'''We replace $\chi_n(\lambda)$ of Eq. (24) by:
\[
\chi'_n(\kappa):=1+\frac{\sigma_{\lfloor\eta n\rfloor}d_\Sigma\log^2(d_\Sigma)}{\kappa n\lambda_\star(0)},\tag{31}
\]
where $\kappa$ will be introduced in the theorem statement.''',[12],[2,4,15],[r"\chi'_n(\kappa)"],'Original ridgeless replacement, with the freely chosen kappa of Theorem 3. Do not inherit the positive-ridge kappa definition (25).','Section 3.3 — Replacement ratio (31)',context=r'The ratio between effective dimension and regularization parameter:',context_page=9)
add(24,'ratio',r'''The quantity $\rho(\lambda)$ defined in Eq. (27) has a well defined limit as $\lambda\downarrow0$, given by
\[
\rho(0):=\frac{\mathscr R_0(\lambda_\star(0),1;\boldsymbol\theta\boldsymbol\theta^\top/\|\boldsymbol\theta\|^2)}{\mathscr R_0(\lambda_\star(0),1;\boldsymbol I)}\in(0,1].
\]''',[12],[3,15,21],[r'\rho(0)'],'Original directional ratio at the overparameterized zero limit. Theta is the same inverse-covariance signal coordinate introduced before (27); zero-signal and zero-root limitations remain explicit.','Section 3.3 — Limiting directional quantity',context='we consider the ratio',context_page=9)
add(25,'orthogonal projection',r'''Let $\boldsymbol\Sigma:=\sum_{i\ge1}\sigma_i\boldsymbol v_i\boldsymbol v_i^\top$ be the eigendecomposition of of $\boldsymbol\Sigma$, and denote by $\boldsymbol\beta_{\le k}:=\sum_{i\le k}\langle\boldsymbol\beta,\boldsymbol v_i\rangle\boldsymbol v_i$ the orthogonal projection of $\boldsymbol\beta$ onto the span of $\boldsymbol v_1,\ldots,\boldsymbol v_k$, and by $\boldsymbol\beta_{>k}:=\boldsymbol\beta-\boldsymbol\beta_{\le k}$ its complement.''',[7],[2],[r'\boldsymbol\beta_{\le k}',r'\boldsymbol\beta_{>n}',r'\boldsymbol\theta_{\le n}'],'Original spectral prefix/tail projection convention, applied to theta as well as beta in Theorem 3. The proposition inequalities following the definition are not imported as assumptions.','Proposition 2.2 — Spectral projection definitions',kind='definition')
add(26,'probability',r'''We say that $A$ happens on the event $E$ with probability at least $1-\Delta$ if $\mathbb P(A^c\text{ and }E)\le\Delta$ (and, as a consequence, $\mathbb P(A)\ge1-\Delta-\mathbb P(E^c)$).''',[12],[],[r'\mathbb P(A^c\text{ and }E)\le\Delta'],'Original event-qualified probability convention. It bounds an intersection and does not assert a conditional probability given E.','Section 3.3 — Event-qualified probability')
add(27,'regularly varying sequence',r'''As special case, Assumption 3 holds if the sorted eigenvalues $(\sigma_1,\sigma_2,\cdots)$ forms a so-called regularly varying sequence, namely for any $\delta\in(0,\infty)$,
\[
\lim_{i\to\infty}\frac{\sigma_{\lfloor\delta i\rfloor}}{\sigma_i}=\psi(\delta),
\]
where $\psi(\delta)$ is positive and finite for any $\delta$. In other words, in the regularly varying case, the ratio $\sigma_j/\sigma_i$ converges when $i,j$ diverge proportionally.''',[16],[2],[r'\lim_{i\to\infty}\frac{\sigma_{\lfloor\delta i\rfloor}}{\sigma_i}'],'Original regular-variation condition, stronger than the preceding polynomial bounded-ratio assumption. That implication is context, not a need to impose every application proposition hypothesis.','Section 4.2 — Regular variation')
add(28,'polynomial-decay',r'''Let $F_\beta(x)=\sum_{k=1}^{\lfloor nx\rfloor}\langle\boldsymbol\beta,\boldsymbol v_k\rangle^2$. If additionally $\boldsymbol\beta$ satisfies the following “polynomial-decay” property: for some $0<\theta\le1$ that
\[
\int_0^\infty x^\alpha\,dF_\beta(x)=O\left(n^{1-\theta}\int_0^\infty x^\alpha(1+c_\star x^\alpha)^{-1}\,dF_\beta(x)\right),
\]''',[17],[18,25],[r'\lfloor nx\rfloor',r'\int_0^\infty x^\alpha\,dF_\beta(x)'],'Original branch-1 coefficient condition and n-scaled spectral cumulative measure. Scalar theta is a decay exponent, not the bold whitened signal. c_star is bound by the same theorem branch.','Theorem 5(1) — Coefficient decay condition',kind='theorem_excerpt',phrases=['polynomial-decay'])
add(29,'rapid-decay',r'''Let $F_\beta(x)=\sum_{k=1}^{\lfloor(n/\log n)x\rfloor}\langle\boldsymbol\beta,\boldsymbol v_k\rangle^2$. If additionally $\boldsymbol\beta$ satisfies the following “rapid-decay” property: for some $0<\theta\le1$ that
\[
\int_0^\infty x\,dF_\beta(x)=O\left(n^{1-\theta}\int_0^\infty x(1+c_\star x)^{-1}\,dF_\beta(x)\right).
\]''',[17],[18,25],[r'\lfloor(n/\log n)x\rfloor',r'\int_0^\infty x\,dF_\beta(x)'],'Original branch-2 condition with its distinct n/log n spectral scale; do not replace it by branch 1. Scalar theta and c_star are local parameters.','Theorem 5(2) — Coefficient decay condition',kind='theorem_excerpt',phrases=['rapid-decay'])
add(30,'resolvent',r'''Extending the previous notation of $\mathscr R_0$ in Eq. (26) to $\mathscr R_k$, we let
\[
\mathscr R_k(\zeta,\mu;\boldsymbol Q)=\operatorname{Tr}(\boldsymbol\Sigma^{1/2}\boldsymbol Q\boldsymbol\Sigma^{1/2}(\zeta\boldsymbol I+\mu\boldsymbol\Sigma+\boldsymbol X_k^\top\boldsymbol X_k)^{-1}),\qquad\mathscr F_k(\zeta,\mu;\boldsymbol Q)=\zeta\mathscr R_k(\zeta,\mu;\boldsymbol Q),\tag{43}
\]
where $\zeta>0$, $\mu\ge0$, $\boldsymbol Q$ is a p.s.d. matrix with bounded spectral norm, and $\boldsymbol X_k=[\boldsymbol x_1,\cdots,\boldsymbol x_k]^\top\in\mathbb R^{k\times d}$ is the partial data matrix comprising the first $k$ rows of $\boldsymbol X$. By convention we set $\boldsymbol X_0^\top\boldsymbol X_0:=0$ when $k=0$.''',[19,23],[2,8,21],[r'\mathscr R_k(\zeta,\mu;\boldsymbol Q)',r'\mathscr R_n(\zeta,\mu;\boldsymbol Q)'],'Original extension of the population resolvent to partial sample designs, with k=0 convention. The adjacent F_k is an auxiliary rescaling, not the effective-risk R_n. Theorem 6 uses k=n.','Section 6 — Sample resolvent (43)',context=r'define the modified population resolvent:',context_page=9)
add(31,'unique solution',r'''Define $\mu_\star:=\mu_\star(\zeta,\mu)$ as the unique solution on of the following equation on $(\mu,\infty)$
\[
\mu_\star=\mu+\frac n{1+\mathscr R_0(\zeta,\mu_\star;\boldsymbol I)}.\tag{44}
\]''',[23],[21],[r'\mu_\star=\mu+\frac n{1+\mathscr R_0(\zeta,\mu_\star;\boldsymbol I)}'],'Original implicit effective resolvent parameter strictly larger than mu. Preserve its defining equation and the source wording; the later ridge change of variables is proof context.','Section 6 — Implicit solution (44)')
def main():
    r=json.loads((REVIEW_ROOT/'inventory-review.json').read_text());assert r['status']=='complete' and r['source_checked']
    assert hashlib.sha256((ROOT/'theorem-inventory.json').read_bytes()).hexdigest()==r['inventory_sha256']
    assert len(interfaces)==len(members)==31
    for x in interfaces:
        m=x['members'][0];assert set(m['depends_on'])<=set(members)
        assert any(v in m['statement_original']+' '+m['local_label'] for v in m['highlight_symbols']+m['highlight_phrases'])
        for ctx in m.get('naming_context',[]):assert not any(ord(ch)<32 and ch!='\n' for ch in ctx['text'])
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
    print('Saved 31 original source entries; full review remains pending.')
if __name__=='__main__':main()
