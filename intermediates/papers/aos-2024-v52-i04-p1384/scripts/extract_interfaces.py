"""Rebuild original main-text passages and local dependencies for this paper.

The saved data is manually transcribed; source audit is a separate stage.
"""
import json
from pathlib import Path
from save_inventory import PID, claims

ROOT = Path(__file__).resolve().parents[1]
interfaces, members, edges = [], {}, {}


def add(lid, term, body, pages, heading, deps=None, *, kind='definition',
        symbols=(), phrases=(), context=None, context_pages=None, shape):
    evidence = [dict(page=p, location=heading) for p in pages]
    member = dict(paper_id=PID, local_id=lid, local_label=heading,
        source_heading=heading, source_kind=kind, statement_original=body.strip(),
        relation='exact', depends_on=list(deps or {}), evidence=evidence,
        highlight_symbols=list(symbols), highlight_phrases=list(phrases))
    keyword = dict(paper_id=PID, local_id=lid, source_text=term,
                   label=term[0].upper()+term[1:], kind='term')
    if term not in body:
        assert context and term in context, (lid, term)
        member['naming_context'] = [dict(context_id=lid+'/name', text=context,
            evidence=[dict(page=p, location=heading+' — naming context') for p in (context_pages or pages)])]
        keyword['context_id'] = lid+'/name'
    interfaces.append(dict(interface_id=PID+'/'+lid, rank_group='all', name=keyword['label'],
        lean_role='hypothesis' if kind in ('condition', 'assumption') else 'definition',
        type_shape=shape, semantic_boundary=shape, members=[member], source_keywords=[keyword],
        central_claim_uses=[], dependencies=[], theorem_explanations={}))
    members[lid] = member
    edges[lid] = deps or {}


add('D1','target measure',r'''
Instead, we simply consider a target measure of the form $\pi\propto e^{-nv}$ with $v\in C^4(\mathbb R^d)$, and we impose a requirement on the triple $(v,d,n)$.
''',[2],'Section 1 — target measure',symbols=[r'\pi\propto e^{-nv}'],shape='Normalized target measure with potential nv; v may depend on n and d. The general theorem does not require an iid likelihood representation.')
add('D2','standard Gaussian distribution',r'''
We let $\gamma$ denote the density of the standard Gaussian distribution $\mathcal N(0,I_d)$ in $d$ dimensions, and we write either $\int fd\gamma$ or $\mathbb E[f(Z)]$ or $\gamma(f)$ for the expectation of $f$ under $\gamma$. We write $Z$ to denote a standard multivariate Gaussian random variable $Z\sim\gamma$ in $\mathbb R^d$.
''',[5,6],'Notation — standard Gaussian and expectations',symbols=[r'\gamma',r'\mathcal N(0,I_d)'],shape='The standard Gaussian law, its density and expectation notation. The source uses gamma for both density and measure.')
add('D3','H-weighted operator norm',r'''
A tensor $T$ of order $k$ is an array $T=(T_{i_1i_2\ldots i_k})_{i_1,\ldots,i_k=1}^d$. For two order $k$ tensors $T$ and $S$ we let $\langle T,S\rangle$ be the entrywise inner product. We say $T$ is symmetric if $T_{i_1\ldots i_k}=T_{j_1\ldots j_k}$, for all permutations $j_1\ldots j_k$ of $i_1\ldots i_k$.

Let $H$ be a symmetric positive definite matrix. For a vector $x\in\mathbb R^d$, we let $\|x\|_H$ denote $\|x\|_H=\sqrt{x^THx}$. For an order $k\ge2$ symmetric tensor $T$, we define the $H$-weighted operator norm of $T$ to be
\[
\|T\|_H:=\sup_{\|u\|_H=1}\langle T,u^{\otimes k}\rangle.\tag{1.11}
\]
By Theorem 2.1 of [31], for symmetric tensors, the definition (1.11) coincides with the standard definition of operator norm:
\[
\sup_{\|u_1\|_H=\cdots=\|u_k\|_H=1}\langle T,u_1\otimes\cdots\otimes u_k\rangle=\|T\|_H=\sup_{\|u\|_H=1}\langle T,u^{\otimes k}\rangle.
\]
When $H=I_d$, the norm $\|T\|_{I_d}$ is the regular operator norm, and in this case we omit the subscript.
''',[6],'Notation — tensors, weighted vector and operator norms (1.11)',context='H-weighted operator norm',symbols=[r'\|T\|_H',r'\|x\|_H',r'\langle T,S\rangle'],shape='Exact original tensor contraction and weighted norms. The displayed supremum has no absolute value; this matters for even-order tensors and must not be silently repaired.')
add('D4','Regularity and unique strict minimum',r'''
The potential $v\in C^4$, with unique global minimizer $x=m^*$, and $H_v=\nabla^2v(m^*)\succ0$.
''',[7],'Assumption 1 (Regularity and unique strict minimum)',kind='assumption',context='Regularity and unique strict minimum',symbols=[r'H_v=\nabla^2v(m^*)'],phrases=['Assumption 1'],shape='C4 potential with a unique global minimizer and positive definite Hessian. The superscript star printed here becomes a subscript star elsewhere.')
add('D5','Polynomial growth',r'''
There is some $q,a_3,a_4>0$ such that
\[
\|\nabla^kv(x)\|_{H_v}\le a_k\left(1\vee\sqrt{n/d}\|x-m^*\|_{H_v}\right)^q\quad\forall x\in\mathbb R^d,\quad k=3,4,\tag{2.3}
\]
\[
a_3\frac d{\sqrt n}\le C(q),\qquad a_3\frac d{\sqrt n}+a_4\frac{d^2}n\le1\tag{2.4}
\]
for a certain constant $C(q)<1$ depending only on $q$.
''',[7],r'Assumption 2 (Polynomial growth of $\|\nabla^kv\|_{H_v}$, $k=3,4$.)',{'D3':'The derivative tensors use the H_v-weighted operator norm in (1.11).','D4':'H_v and the unique minimizer are supplied by Assumption 1.'},kind='assumption',context='Polynomial growth',symbols=[r'a_3\frac d{\sqrt n}',r'\|\nabla^kv(x)\|_{H_v}'],phrases=['Assumption 2'],shape='Complete polynomial envelope and both smallness constraints; q is printed strictly positive, while the logistic specialization later uses q=0.')
add('D6','Lower bound on growth',r'''
There exists $c_0>0$ such that
\[
c_0\sqrt{d/n}\|x-m^*\|_{H_v}\le v(x)-v(m^*)\quad\forall x:\ \|x-m^*\|_{H_v}\ge\frac12\sqrt{d/n}.\tag{2.5}
\]
''',[7],'Assumption 3 (Lower bound on growth of v)',{'D3':'The growth comparison uses the H_v-weighted vector norm.','D4':'It is centered at the minimum of v with Hessian H_v.'},kind='assumption',context='Lower bound on growth',symbols=[r'c_0\sqrt{d/n}',r'\frac12\sqrt{d/n}'],phrases=['Assumption 3'],shape='Linear growth lower bound outside the specified half-radius, with c0 positive; convexity is not itself assumed.')
add('D7','first order optimality equations',r'''
Hereafter, we replace $\theta$ by $x$ and let $V=nv$, $\pi\propto e^{-V}$.
\[
\mathbb E[\nabla V(m+S^{1/2}Z)]=0,\qquad\mathbb E[\nabla^2V(m+S^{1/2}Z)]=S^{-1},\tag{1.9}
\]
where $Z\sim\mathcal N(0,I_d)$ and $S^{1/2}$ is the positive definite symmetric square root of $S$; see [20] for this calculation.
''',[4],'Section 1 — first order optimality equations (1.9)',{'D1':'V=nv is the potential of the target measure.','D2':'The expectations are over a standard Gaussian Z.'},context='The focal point of this work are the first order optimality equations for the minimization (1.1):',symbols=[r'V=nv',r'\mathbb E[\nabla V(m+S^{1/2}Z)]'],shape='Two stationarity equations, with the source square-root convention. They are not a global KL-minimizer definition.')
add('D8','region',r'''
\[
\mathcal R_V=\left\{(m,S)\in\mathbb R^d\times\mathbf S_{++}^d:\ S\preceq2H_V^{-1},\ \|H_V^{1/2}S^{1/2}\|^2+\|H_V^{1/2}(m-m_*)\|^2\le8\right\},\tag{2.2}
\]
where $H_V=\nabla^2V(m_*)=n\nabla^2v(m_*)$.
''',[6],'Section 2 — region (2.2)',{'D1':'The rescaled potential is V=nv.','D4':'The region is centered at the unique minimizer, printed m_* here.','D3':'The region uses the unweighted matrix and vector norms from Notation.'},context=r'There exists a unique solution $\hat m,\hat S$ to (1.9) in the region $\mathcal R_V$.',context_pages=[14],symbols=[r'\mathcal R_V',r'H_V=\nabla^2V(m_*)'],shape='The exact neighborhood selecting the canonical solution; S is positive definite. Matrix products need not be symmetric, so the stated standard matrix norm convention remains relevant.')
add('D9','canonical solution',r'''
We call this unique solution $(m,S)$ in $\mathcal R_V$ the “canonical” solution of (1.9). We expect the Gaussian distribution corresponding to this canonical solution to be the minimizer of (1.1), although we have not proved this. Regardless of whether it is true, we will redefine $(\hat m,\hat S)$ to denote the canonical solution. Indeed, whether or not $\hat\pi=\mathcal N(\hat m,\hat S)$ actually minimizes the KL divergence or is only a local minimizer is immaterial for the purpose of approximating $\pi$.
''',[6,7],'Section 2 — canonical solution and redefined Gaussian approximation',{'D7':'The canonical pair solves the first order equations (1.9).','D8':'It is the unique solution within R_V, rather than an arbitrary stationary point.'},symbols=[r'(\hat m,\hat S)',r'\hat\pi=\mathcal N(\hat m,\hat S)'],shape='Author-defined canonical pair and Gaussian measure. Lemma 2.1 provides existence under Assumptions 1 and 2; that sufficient proof condition is not added to the pair definition itself.')
t21=claims[0]['statement_original'];growth=t21[t21.index('Let $g$'):t21.index('\nThen')]
add('D11','condition (2.7)',growth,[7],'Theorem 2.1 — function condition (2.7)',{'D9':'The centering integral and ellipsoidal radius use the canonical Gaussian measure.','D3':'The ellipsoidal radius uses the weighted vector norm with H=hat S inverse.'},kind='condition',context='Next, let us discuss the condition (2.7) on the function',context_pages=[9],symbols=[r'R_g>0',r'\|x-\hat m\|_{\hat S^{-1}}'],shape='Original centered tail condition outside radius R_g sqrt(d). It references c0 from Assumption 3 in general results and sets c0=1/8 in Theorem 3.1. It is not a boundedness condition inside the ball.')
add('D12','variance',r'''
We let $\operatorname{Var}_{\hat\pi}(f)=\int(f-\hat\pi(f))^2d\hat\pi$,
''',[6],'Notation — variance under the Gaussian approximation',{'D9':'The measure hat pi is the redefined canonical Gaussian.'},context='the vanishing variance',context_pages=[3],symbols=[r'\operatorname{Var}_{\hat\pi}(f)'],shape='Variance of a scalar function under the canonical Gaussian measure; the source explicitly defines it in Notation.')
t22=claims[1]['statement_original'];qbody=t22[t22.index('Define the function'):t22.index('\nIf $g$')]
add('D13','Leading order term',qbody,[8],'Theorem 2.2 — function Q (2.11)',{'D1':'The derivative is of V=nv.','D9':'Both the expectation and centering use the canonical Gaussian parameters.','D3':'The formula contracts third-order tensors with the entrywise inner product.'},context='Leading order term in VI approximation error',symbols=[r'Q(x)',r'\nabla^3V(X)'],shape='Explicit cubic correction Q in original coordinates. The formula is already bound within Theorem 2.2; it is extracted because other source statements refer to this named function.')
add('D14','logistic regression',r'''
In logistic regression, we generate $n$ feature vectors $X_i\in\mathbb R^d$ and observe their corresponding labels $Y_i\in\{0,1\}$. The distribution of the labels given the features is modeled as
\[
p(Y_i\mid X_i,\theta)=\exp\left(Y_iX_i^T\theta-\psi(X_i^T\theta)\right),\tag{3.1}
\]
where $\psi(t)=\log(1+e^t)$ and $\theta$ is the unknown coefficient vector. Note that (3.1) is just the probability distribution for $\operatorname{Bern}(\sigma(X_i^T\theta))$, where $\sigma(t)=\psi'(t)=(1+e^{-t})^{-1}$ is the sigmoid. We assume the model is well-specified, so that there is a true $\theta_0\in\mathbb R^d$ such that
\[
Y_i\sim\operatorname{Bern}(\sigma(X_i^T\theta_0)).
\]
''',[11],'Section 3 — logistic label model',symbols=[r'\psi(t)=\log(1+e^t)',r'\sigma(X_i^T\theta_0)'],shape='Well-specified logistic response law. The final displayed marginal-looking notation is interpreted using the preceding explicit conditional model, without editing it.')
add('D15','Gaussian prior',r'''
We assume the features are generated from a standard Gaussian distribution:
\[
X_i\stackrel{\mathrm{i.i.d.}}{\sim}\mathcal N(0,I_d),\quad i=1,\ldots,n.
\]
We consider a Gaussian prior $\theta\sim\mathcal N(0,\Sigma)$ on the coefficient vector $\theta$. The posterior distribution of $\theta$ given the labels $Y_i$ is then $\pi(\theta)\propto e^{-nv(\theta)}$, where
\[
\begin{aligned}
v(\theta)&=\ell(\theta)+\frac1{2n}\theta^T\Sigma^{-1}\theta,\\
\ell(\theta)&:=-\frac1n\sum_{i=1}^n\log p(Y_i\mid X_i,\theta)=-\theta^T\left[\frac1n\sum_{i=1}^nY_iX_i\right]+\frac1n\sum_{i=1}^n\psi(X_i^T\theta)
\end{aligned}\tag{3.2}
\]
Here, $\ell$ is the negative normalized log likelihood, and $\theta^T\Sigma^{-1}\theta/2n$ is the contribution from the log prior. Formally, $\Sigma^{-1}=0$ corresponds to the case of a flat prior. Note that the distribution of the $X_i$ does not enter into the posterior.
''',[12],'Section 3 — Gaussian design, prior and posterior (3.2)',{'D14':'The posterior uses the logistic likelihood and log-partition psi.','D2':'The design law is standard Gaussian.'},symbols=[r'\Sigma^{-1}=0',r'v(\theta)',r'\ell(\theta)'],shape='The Gaussian-prior posterior and its formal zero-precision flat-prior case. Sigma here is prior covariance, unlike the posterior Sigma bound in Theorem 3.1.')
add('D16','well-specified model',r'''
We now summarize the results from Section 2 applied to logistic regression. We assume the set-up from the beginning of the section: well-specified model, i.i.d. Gaussian design, bounded ground truth $\|\theta_0\|\le C$, and Gaussian or flat prior $\mathcal N(0,\Sigma)$, with $\|\Sigma^{-1}\|\le C$. In this setting, Corollary 3.1 shows that Assumptions 1, 2, 3 are satisfied, and that $q=0$, $a_3=a_4=C$.
''',[13],'Section 3.2 — setting immediately preceding Theorem 3.1',{'D14':'Well specification and theta0 refer to the logistic response model.','D15':'Gaussian design and the Gaussian or flat prior refer to the Section 3 posterior.'},kind='condition',symbols=[r'\|\theta_0\|\le C',r'\|\Sigma^{-1}\|\le C'],shape='Section-local hypotheses inherited by Theorem 3.1. The closing statement that general assumptions follow is a result of Corollary 3.1, not an additional conditional assumption in Theorem 3.1.')
add('D17','leading order term',r'''
\[
\mathbb E_{\theta\sim\hat\pi}[\nabla^3V(\theta)]=\sum_{i=1}^nb_i(\theta)X_i^{\otimes3},
\]
where
\[
b_i(\theta)=\mathbb E_{\theta\sim\hat\pi}[\psi^{\prime\prime\prime}(\theta^TX_i)].\tag{3.6}
\]
Using the definition (2.11) of $Q$ and the above expression for $\mathbb E_{\theta\sim\hat\pi}[\nabla^3V(\theta)]$, we get
\[
Q(\theta)=\sum_{i=1}^nb_i(\theta)\left[\frac12X_i^T(\theta-\hat m)X_i^T\hat SX_i-\frac16(X_i^T(\theta-\hat m))^3\right]\tag{3.7}
\]
''',[13],'Section 3.2 — logistic correction (3.6)-(3.7)',{'D13':'The logistic formula explicitly specializes the definition of Q in (2.11).','D15':'Its psi and covariates come from the logistic posterior.'},context=r'We first compute the function $Q$ in the leading order term.',symbols=[r'b_i(\theta)',r'Q(\theta)'],shape='Original logistic correction. The notation b_i(theta) reuses theta as its integration variable and is constant in the external argument; preserve this binding collision in the source.')
add('D18','Borel sets',r'''
Let $\mathcal B(\mathbb R^d)$ be the set of all Borel sets of $\mathbb R^d$, and $\mathcal S_{\hat m}(\mathbb R^d)$ the set of Borel sets symmetric about $\hat m$.
''',[8],'Section 2.2 — Borel and symmetric Borel classes',{'D9':'The symmetry center is the canonical Gaussian mean hat m.'},symbols=[r'\mathcal B(\mathbb R^d)',r'\mathcal S_{\hat m}(\mathbb R^d)'],shape='Ordinary and centrally symmetric Borel classes. Theorem 3.1 prints B_{s,hat m} instead of S_{hat m}; the source correspondence is a separate notation note.')
add('D19','bijection',r"""
For convenience, we choose $T$ so that $T_\#\hat\pi=\gamma$ is the standard Gaussian distribution. Specifically, we let
\[
T(x)=\hat S^{-1/2}(x-\hat m),\tag{4.2}
\]
and we define $\rho=T_\#\pi\propto e^{-V_0}$, where
\[
V_0(x):=V(\hat m+\hat S^{1/2}x)=V(T^{-1}(x)).\tag{4.3}
\]
""",[15],'Section 4.1 — bijection and pushed-forward target (4.2)-(4.3)',{'D9':'The affine transformation uses the canonical Gaussian mean and covariance.','D1':'The target pi has potential V=nv.','D2':'The Gaussian comparison measure is gamma.'},context=r'but we can always change variables via a bijection $T$,',symbols=[r'T(x)=\hat S^{-1/2}(x-\hat m)',r'\rho=T_\#\pi',r'V_0(x)'],shape='VI-centered whitening bijection, target pushforward and rescaled potential. This is not the minimum-centered transform in Section 5.')
add('D21','Hermite polynomials',r'''
Specifically, $\mathbf H_k(x)$ is the tensor of all order $k$ Hermite polynomials, enumerated as $H_k^{(\alpha)}$, $\alpha\in[d]^k$ with some entries repeating. For $k=0,1,2$, the Hermite tensors are given by
\[
\mathbf H_0(x)=1,\quad \mathbf H_1(x)=x,\quad \mathbf H_2(x)=xx^T-I_d.\tag{4.12}
\]
See Appendix E for further details on Hermite series and polynomials. Distinct Hermite polynomials are orthogonal to each other with respect to the Gaussian weight. Using the representation
\[
\mathbf H_k(x)e^{-\|x\|^2/2}=(-1)^k\nabla^ke^{-\|x\|^2/2},\tag{4.13}
\]
''',[17],'Section 4.2 — Hermite tensors and representation (4.12)-(4.13)',{'D2':'The polynomial convention and orthogonality use the standard Gaussian weight.','D3':'\mathbf H_k is a tensor indexed by ordered multi-indices in the source convention.'},symbols=[r'\mathbf H_k(x)',r'H_k^{(\alpha)}'],shape='Main-text tensor indexing and Rodrigues representation, sufficient to identify the third-order Hermite family in Theorem 4.1 without reading Appendix E.')
add('D22','third order multivariate Hermite polynomials',r'''
Next, we reformulate Theorems 2.1 and 2.2. To do so, define $\mathbf A_3=\mathbb E[\nabla^3V_0(Z)]$ and
\[
p_3(x)=\frac16\langle \mathbf A_3,\mathbf H_3(x)\rangle=\left\langle \mathbf A_3,\frac16x^{\otimes3}-\frac12x\otimes I_d\right\rangle.
\]
Here, $\mathbf H_3(x)$ is the $d\times d\times d$ tensor of third order multivariate Hermite polynomials; see Section 4.2 and Appendix E for more details.
''',[15],'Section 4.1 — coefficient A3 and polynomial p3',{'D19':'A3 differentiates the transformed potential V0 in (4.3).','D21':'H3 is the third-order member of the source Hermite tensor convention.','D3':'The displayed contractions use the entrywise tensor inner product.'},symbols=[r'\mathbf A_3=\mathbb E[\nabla^3V_0(Z)]',r'p_3(x)'],shape='Third-order contribution including the 1/6 factor. The informal page-18 formula drops this factor, but the defining page-15 formula and Theorem 4.1 convention are retained.')


def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edges=edges),indent=2,ensure_ascii=False)+'\n')

if __name__=='__main__':main()
