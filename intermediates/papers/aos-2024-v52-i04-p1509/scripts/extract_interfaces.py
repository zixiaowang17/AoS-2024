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


add('D1','greatest convex minorant',r'''
For an interval $I\subseteq\mathbb R$ and a function $f:I\to\mathbb R$, $\mathsf{GCM}_I(f)$ denotes its greatest convex minorant (on $I$)
''',[3],'Section 1.1 — greatest convex minorant',symbols=[r'\mathsf{GCM}_I(f)'],shape='Greatest convex minorant on a specified interval; original notation passage excerpt. Standard order/convexity meanings are ambient, and no appendix-only modified operator is imported.')
add('D2','generalized inverse',r'''
if $f$ is non-decreasing and right-continuous, then $f^-$ denotes its generalized inverse; that is, $f^-(x)=\inf\{u\in I:f(u)\ge x\}$, where the dependence of $f^-$ on $I$ has been suppressed (and where the infimum of the empty set is $\sup I$).
''',[3],'Section 1.1 — generalized inverse',symbols=[r'f^-(x)=\inf\{u\in I:f(u)\ge x\}'],shape='Generalized inverse of a nondecreasing right-continuous function on its specified interval; infimum of an empty level set is sup I, rather than a silently substituted extended-real convention.')
add('D3','left derivative',r'''
Assuming the relevant derivatives exist, $\partial^q$ denotes the $q$th partial derivative (operator) and $\partial_-$ denotes the left derivative (operator).
''',[3],'Section 1.1 — derivative operators',symbols=[r'\partial_-'],shape='Left derivative applied to a greatest convex minorant. The ordinary derivative index q in this passage is distinct from the later Fraktur characteristic exponent.')
add('D4','generalized Grenander-type estimators',r'''
To define the class of generalized Grenander-type estimators, let $\psi_0=\theta_0\circ\Phi_0^-$, where $\Phi_0$ is non-negative, non-decreasing, and continuous on $I$. Defining
\[
\Gamma_0=\Psi_0\circ\Phi_0,\qquad\Psi_0(x)=\int_0^x\psi_0(v)\,dv,
\]
and assuming that $\Phi_0(x)<\Phi_0(\mathsf x)<u_0$ for every $x<\mathsf x$, we have
\[
\theta_0(\mathsf x)=\partial_-\mathsf{GCM}_{[0,u_0]}(\Gamma_0\circ\Phi_0^-)\circ\Phi_0(\mathsf x)\tag{1}
\]
whenever $\theta_0$ is left-continuous at $\mathsf x$. In the terminology of Westling and Carone (2020), an estimator of $\theta_0(\mathsf x)$ is of the Generalized Grenander-type if it is obtained by replacing $\Gamma_0$, $\Phi_0$, and $u_0$ in the preceding display with estimators $\widehat\Gamma_n$, $\widehat\Phi_n$, and $\widehat u_n$ (say); to be specific, an estimator of the Generalized Grenander-type is of the form
\[
\widehat\theta_n(\mathsf x)=\partial_-\mathsf{GCM}_{[0,\widehat u_n]}(\widehat\Gamma_n\circ\widehat\Phi_n^-)\circ\widehat\Phi_n(\mathsf x),
\]
where $\widehat\Phi_n$ is non-negative, non-decreasing, and right-continuous.
''',[4],'Section 2 — population representation (1) and generalized Grenander-type estimator',{'D1':'Both population representation and estimator apply the greatest convex minorant on the indicated interval.','D2':'Both compose the primitive estimator with a generalized inverse, using the source endpoint convention.','D3':'The target and estimator are obtained by taking the left derivative of the greatest convex minorant.'},symbols=[r'\widehat\theta_n(\mathsf x)',r'\Gamma_0=\Psi_0\circ\Phi_0',r'\psi_0=\theta_0\circ\Phi_0^-'],shape='Original population transformation and estimator based on a primitive, monotone domain transformation and endpoint estimate. The fixed evaluation point is sans-serif x; italic x is a variable. Theta0 and Phi0 are given functions, not density or regression objects unless an example is specifically chosen.')
add('D5','characteristic exponent',r'''
Under regularity conditions, if $\widehat\theta_n(\mathsf x)$ is of the generalized Grenander-type, then its rate of convergence is governed by the flatness of $\theta_0$ around $\mathsf x$, as measured by the characteristic exponent
\[
\mathfrak q=\min\{j\in\mathbb N:\partial^j\theta_0(\mathsf x)\ne0\},
\]
where $\mathbb N$ is the set of positive integers. (When $\theta_0$ is non-decreasing and suitably smooth, $\mathfrak q$ is necessarily an odd integer.)
''',[5],'Section 2 — characteristic exponent',symbols=[r'\mathfrak q=\min\{j\in\mathbb N:\partial^j\theta_0(\mathsf x)\ne0\}'],shape='First nonzero positive-order derivative at the fixed evaluation point. The defining expression requires a finite such order; a flat function with no such derivative is not assigned an invented exponent. Mention of the estimator motivates the quantity but is not needed to define it.')
add('D6','monomial',r'''
where $\mathcal G_{\mathsf x}$ is a scalar multiple of two-sided Brownian motion and where $\mathcal M_{\mathsf x}^{\mathfrak q}$ is a monomial given by
\[
\mathcal M_{\mathsf x}^{\mathfrak q}(v)=\frac{\partial^{\mathfrak q}\theta_0(\mathsf x)\partial\Phi_0(\mathsf x)}{(\mathfrak q+1)!}v^{\mathfrak q+1}.\tag{3}
\]
''',[5],'Section 2 — monomial drift (3)',{'D5':'The degree and coefficient use the first nonzero derivative order of theta0.'},symbols=[r'\mathcal M_{\mathsf x}^{\mathfrak q}(v)',r'\frac{\partial^{\mathfrak q}\theta_0(\mathsf x)\partial\Phi_0(\mathsf x)}{(\mathfrak q+1)!}'],shape='Original monomial drift at the fixed point, with a factorial and derivative of the domain transformation. The adjacent Brownian-motion phrase gives context, not a dependence of this deterministic drift on a random process.')
add('D7','Assumption A',r'''
For some $\delta>0$ and some $\mathfrak s\ge\mathfrak q$, the following are satisfied:

(A1) $I\subseteq\mathbb R$ is an interval and $I_{\mathsf x}^{\delta}=\{x\in\mathbb R:|x-\mathsf x|\le\delta\}\subseteq I$.

(A2) $\theta_0$ is non-decreasing and bounded on $I$, and $\lfloor\mathfrak s\rfloor$ times continuously differentiable on $I_{\mathsf x}^{\delta}$ with
\[
\sup_{x,x'\in I_{\mathsf x}^{\delta}}\frac{|\partial^{\lfloor\mathfrak s\rfloor}\theta_0(x)-\partial^{\lfloor\mathfrak s\rfloor}\theta_0(x')|}{|x-x'|^{\mathfrak s-\lfloor\mathfrak s\rfloor}}<\infty.
\]

(A3) $\Phi_0$ is non-negative, non-decreasing, continuous, and bounded on $I$, and $\lfloor\mathfrak s\rfloor-\mathfrak q+1$ times continuously differentiable on $I_{\mathsf x}^{\delta}$ with $\partial\Phi_0(\mathsf x)\ne0$ and
\[
\sup_{x,x'\in I_{\mathsf x}^{\delta}}\frac{|\partial^{\lfloor\mathfrak s\rfloor-\mathfrak q+1}\Phi_0(x)-\partial^{\lfloor\mathfrak s\rfloor-\mathfrak q+1}\Phi_0(x')|}{|x-x'|^{\mathfrak s-\lfloor\mathfrak s\rfloor}}<\infty.
\]
''',[5],'Assumption A',{'D5':'The smoothness order s is at least the characteristic exponent q, and the Phi0 derivative order depends on q.'},kind='assumption',context='Assumption A.',symbols=[r'\mathfrak s\ge\mathfrak q',r'\partial\Phi_0(\mathsf x)\ne0'],phrases=['Assumption A'],shape='Local smoothness and global bounded monotonicity of the given theta0 and Phi0 on an interval. Keep the different derivative orders, the same Holder exponent, and the printed supremum over all pairs, which does not explicitly exclude the diagonal.')
add('D8','bootstrap analog',r'''
Letting $(\widehat\Gamma_n^*,\widehat\Phi_n^*,\widehat u_n^*)$ denote a generic (not necessarily nonparametric) bootstrap analog of $(\widehat\Gamma_n,\widehat\Phi_n,\widehat u_n)$ and assuming that $\widehat\Phi_n^*$ is non-decreasing and right-continuous, the associated bootstrap analog of $\widehat\theta_n(\mathsf x)$ is
\[
\widehat\theta_n^*(\mathsf x)=\partial_-\mathsf{GCM}_{[0,\widehat u_n^*]}(\widehat\Gamma_n^*\circ\widehat\Phi_n^{*-})\circ\widehat\Phi_n^*(\mathsf x).
\]
''',[5,6],'Section 3 — generic bootstrap analog',{'D4':'The bootstrap inputs replace the original generalized Grenander inputs.','D1':'The bootstrap estimator takes a greatest convex minorant on the bootstrap interval.','D2':'It composes with the generalized inverse of the bootstrap transformation.','D3':'It takes the left derivative of the resulting greatest convex minorant.'},symbols=[r'\widehat\Gamma_n^*',r'\widehat\Phi_n^{*-}'],shape='Generic bootstrap inputs and the ordinary bootstrap estimator. Theorem 1 uses these inputs after a separate drift correction, not the ordinary bootstrap estimator as its asserted valid approximation. No iid or particular resampling law is imposed here.')
add('D9','bootstrap-based distributional approximation',r'''
It turns out, however, that under plausible conditions on $(\widehat\Gamma_n^*,\widehat\Phi_n^*,\widehat u_n^*)$, a valid bootstrap-based distributional approximation can be obtained by employing
\[
\widetilde\theta_n^*(\mathsf x)=\partial_-\mathsf{GCM}_{[0,\widehat u_n^*]}(\widetilde\Gamma_n^*\circ\widehat\Phi_n^{*-})\circ\widehat\Phi_n^*(\mathsf x),
\]
where, for some judiciously chosen $\widetilde M_{\mathsf x,n}$,
\[
\widetilde\Gamma_n^*(x)=\widehat\Gamma_n^*(x)-\widehat\Gamma_n(x)+\widehat\theta_n(\mathsf x)\widehat\Phi_n(x)+\widetilde M_{\mathsf x,n}(x-\mathsf x).
\]
''',[6],'Section 3 — proposed estimator and transformed primitive',{'D4':'The correction uses the original primitive, transformation and estimator evaluated at the fixed point.','D8':'The new primitive starts from the generic bootstrap inputs, with the same bootstrap endpoint and inverse transformation.','D1':'The corrected estimator is still a greatest-convex-minorant slope.','D2':'It uses the original generalized-inverse convention for the bootstrap transformation.','D3':'It takes the left derivative after replacing the primitive.'},kind='source_passage',symbols=[r'\widetilde\theta_n^*(\mathsf x)',r'\widehat\theta_n(\mathsf x)\widehat\Phi_n(x)',r'\widetilde M_{\mathsf x,n}(x-\mathsf x)'],shape='The drift-corrected bootstrap estimator. The correction uses unstarred Phi-hat, not Phi-hat-star, and keeps theta-hat at the fixed evaluation point while x varies. The chosen unscaled drift is supplied here; its restrictions are imposed by Assumption C.')
add('D10','stochastic process',r'''
\[
\begin{aligned}
\widehat G_{\mathsf x,n}^{\mathfrak q}(v)={}&\sqrt{na_n}[\widehat\Gamma_n(\mathsf x+va_n^{-1})-\widehat\Gamma_n(\mathsf x)-\Gamma_0(\mathsf x+va_n^{-1})+\Gamma_0(\mathsf x)]\\
&-\theta_0(\mathsf x)\sqrt{na_n}[\widehat\Phi_n(\mathsf x+va_n^{-1})-\widehat\Phi_n(\mathsf x)-\Phi_0(\mathsf x+va_n^{-1})+\Phi_0(\mathsf x)],\qquad a_n=n^{1/(1+2\mathfrak q)},
\end{aligned}
\]
''',[6],'Section 3.1 — localized empirical process',{'D4':'The increments involve the original primitive and transformation estimators and their population versions.','D5':'The spatial scale a_n is determined by the characteristic exponent.'},context=r'$\widehat G_{\mathsf x,n}^{\mathfrak q}$ is a stochastic process given by',symbols=[r'\widehat G_{\mathsf x,n}^{\mathfrak q}(v)',r'a_n=n^{1/(1+2\mathfrak q)}'],shape='Centered local empirical increments scaled by sqrt(n a_n), with theta0 at the fixed point. The superscript indicates localization; exact domains and extensions referenced only in Appendix A.4 remain unresolved.')
add('D15','centered Gaussian process',r'''
where $\mathcal G_{\mathsf x}$ is a centered Gaussian process whose covariance function is $\mathcal C_{\mathsf x}(s,t)=C(|s|\wedge|t|)\mathbb 1(\operatorname{sign}(s)=\operatorname{sign}(t))$ for some $C>0$.
''',[8],'Assumption B1 — Gaussian limit and covariance',kind='assumption',symbols=[r'\mathcal C_{\mathsf x}(s,t)',r'\mathbb 1(\operatorname{sign}(s)=\operatorname{sign}(t))'],shape='Two-sided Brownian covariance with a positive scale, centered Gaussian law. This defines the limit process independently of the convergence assumptions around it; C is a scalar and calligraphic C is the covariance function.')
add('D12','Assumption B',r'''
For some $\delta>0$, the following are satisfied:

(B1) $\widehat G_{\mathsf x,n}^{\mathfrak q}\rightsquigarrow\mathcal G_{\mathsf x}$ and $\widehat G_{\mathsf x,n}^{\mathfrak q,*}\rightsquigarrow_{\mathbb P}\mathcal G_{\mathsf x}$, where $\mathcal G_{\mathsf x}$ is a centered Gaussian process whose covariance function is $\mathcal C_{\mathsf x}(s,t)=C(|s|\wedge|t|)\mathbb 1(\operatorname{sign}(s)=\operatorname{sign}(t))$ for some $C>0$.

(B2) There exist $\beta<\mathfrak q+1$ and events $\mathcal A_n$ with $\lim_{n\to\infty}\mathbb P[\mathcal A_n]=1$,
\[
\sup_{V\in[1,a_n\delta]}\mathbb E\left[V^{-\beta}\sup_{|v|\in[V,2V]}|\widehat G_{\mathsf x,n}^{\mathfrak q}(v)|\mathbb 1_{\mathcal A_n}\right]=O(1)
\]
and
\[
\sup_{V\in[1,a_n\delta]}\mathbb E\left[V^{-\beta}\sup_{|v|\in[V,2V]}|\widehat G_{\mathsf x,n}^{\mathfrak q,*}(v)|\mathbb 1_{\mathcal A_n}\right]=O(1).
\]

(B3) $\sup_{x\in I}|\widehat\Gamma_n(x)-\Gamma_0(x)|=o_{\mathbb P}(1)$ and $\sup_{x\in I}|\widehat\Gamma_n^*(x)-\widehat\Gamma_n(x)|=o_{\mathbb P}(1)$.

(B4) $\sup_{x\in I}|\widehat\Phi_n(x)-\Phi_0(x)|=o_{\mathbb P}(1)$ and $\sup_{x\in I}|\widehat\Phi_n^*(x)-\widehat\Phi_n(x)|=o_{\mathbb P}(1)$. In addition,
\[
a_n\sup_{x\in I_{\mathsf x}^{\delta}}|\widehat\Phi_n(x)-\Phi_0(x)|=o_{\mathbb P}(1)\qquad\text{and}\qquad a_n\sup_{x\in I_{\mathsf x}^{\delta}}|\widehat\Phi_n^*(x)-\widehat\Phi_n(x)|=o_{\mathbb P}(1).
\]

(B5) For some $u_0>\Phi_0(\mathsf x)$, $\widehat u_n\ge u_0+o_{\mathbb P}(1)$ and $\widehat u_n^*\ge\widehat u_n+o_{\mathbb P}(1)$.

(B6) $\widehat\Phi_n$ and $\widehat\Phi_n^*$ are non-negative, non-decreasing, and right-continuous on $I$. In addition, $\{0,\widehat u_n\}\subseteq\widehat\Phi_n(I)$ and $\{0,\widehat u_n^*\}\subseteq\widehat\Phi_n^*(I)$. Also, $\widehat\Phi_n(I)\cap[0,\widehat u_n]$ and $\widehat\Phi_n^*(I)\cap[0,\widehat u_n^*]$ are closed.

(B7)
\[
\sqrt{na_n}\sup_{x\in I_{\mathsf x}^{\delta}}|\widehat\Phi_n(x)-\widehat\Phi_n(x-)|=o_{\mathbb P}(1)\qquad\text{and}\qquad\sqrt{na_n}\sup_{x\in I_{\mathsf x}^{\delta}}|\widehat\Phi_n^*(x)-\widehat\Phi_n^*(x-)|=o_{\mathbb P}(1).
\]
''',[8,9],'Assumption B',{'D10':'B1-B2 use the original localized empirical process and its scale.','D4':'B3-B7 concern original primitive/transformation estimates, their population targets and the endpoint.','D8':'B3-B7 impose the corresponding requirements on the generic bootstrap inputs.','D5':'B2 bounds beta by the characteristic exponent plus one, and a_n uses that exponent.','D15':'B1 gives convergence to the Gaussian process with the stated positive Brownian covariance scale.'},kind='assumption',context='Assumption B.',symbols=[r'\widehat G_{\mathsf x,n}^{\mathfrak q,*}',r'\sqrt{na_n}',r'\widehat\Phi_n(I)\cap[0,\widehat u_n]'],phrases=['Assumption B'],shape='All seven original clauses, including original and conditional bootstrap process limits, a common high-probability event for two unconditional expectation bounds, uniform/global and faster local consistency, endpoint lower bounds, closed ranges and small jumps. Neither iid sampling nor particular weights are assumed here. The neighborhood notation is the closed interval defined in A1, with B choosing its own delta.')
add('D13','transformation',r'''
where $\widetilde M_{\mathsf x,n}^{\mathfrak q}$ is the following transformation of $\widetilde M_{\mathsf x,n}$:
\[
\widetilde M_{\mathsf x,n}^{\mathfrak q}(v)=\sqrt{na_n}\widetilde M_{\mathsf x,n}(va_n^{-1}).
\]
''',[7],'Section 3.1 — localized transformation of the estimated drift',{'D9':'The unscaled function is the chosen drift inserted into the corrected bootstrap primitive.','D5':'The scaling a_n=n^(1/(1+2q)) uses the characteristic exponent.'},symbols=[r'\widetilde M_{\mathsf x,n}^{\mathfrak q}(v)=\sqrt{na_n}\widetilde M_{\mathsf x,n}(va_n^{-1})'],shape='Deterministic rescaling of the estimated drift, distinct from the deterministic target monomial and the random uncorrected-bootstrap drift. Exact conventions outside the localized domain are not given in main text.')
add('D14','Assumption C',r'''
$\widetilde M_{\mathsf x,n}^{\mathfrak q}\rightsquigarrow_{\mathbb P}\mathcal M_{\mathsf x}^{\mathfrak q}$ and, for some $c>0$ and every $K>0$,
\[
\liminf_{n\to\infty}\mathbb P\left[\inf_{|v|>K^{-1}}\widetilde M_{\mathsf x,n}(v)\ge cK^{-(\mathfrak q+1)}\right]=1.
\]
''',[9],'Assumption C',{'D13':'The first condition concerns the rescaled estimated drift; the second concerns its unscaled version.','D6':'The limiting deterministic function is the original monomial (3).','D5':'The exponent q+1 in the lower bound is fixed by the characteristic exponent.'},kind='assumption',context='Assumption C.',symbols=[r'\widetilde M_{\mathsf x,n}^{\mathfrak q}\rightsquigarrow_{\mathbb P}\mathcal M_{\mathsf x}^{\mathfrak q}',r'\inf_{|v|>K^{-1}}'],phrases=['Assumption C'],shape='Conditional weak convergence of the scaled drift and a global lower bound on the unscaled drift outside every radius K^-1. The same positive c works for every fixed K; the source does not assert a single simultaneous event over all K.')
def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edges=edges),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
