"""Preserve the original lattice trend-filtering objects without changing source definitions."""
import json
from save_inventory import ROOT,PID,STATEMENTS
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
add(1,'total variation',r'''Let $U$ be an open, bounded subset of $\mathbb R^d$ and $L^p(U)$ denote the space of real-valued functions on $U$ with finite $L^p$ norm, $\int_U|f(x)|^p\,dx<\infty$.
\[
\operatorname{TV}(f;U)=\sup\left\{\int_U f(x)\operatorname{div}\phi(x)\,dx:\phi\in C_c^\infty(U;\mathbb R^d),\|\phi(x)\|_\infty\le1\text{ for all }x\in U\right\}.
\]
(17)
Above, $C_c^\infty(U;\mathbb R^d)$ denotes the space of infinitely continuously differentiable functions from $U$ to $\mathbb R^d$ with compact support, and $\operatorname{div}(\cdot)$ denotes the divergence operator, $\operatorname{div}\phi=\sum_{j=1}^d\partial\phi_j/\partial x_j$. We call $\operatorname{TV}(f;U)$ the total variation of $f$;''',[11],[],[r'\operatorname{TV}(f;U)',r'\|\phi(x)\|_\infty\le1'],'Anisotropic measure-theoretic variation: vector test fields have pointwise infinity-norm bound, so smooth functions have the integral of the gradient one-norm. Not isotropic Euclidean-norm variation or the lattice seminorm.','Section 3.1 — Measure-theoretic total variation (17)')
add(2,'bounded variation',r'''A function $f\in L^1(U)$ is said to be of bounded variation (BV) provided $\operatorname{TV}(f;U)<\infty$,
Writing $\operatorname{BV}(U)$ for the space of bounded variation functions,''',[11,12],[1],[r'\operatorname{BV}(U)',r'\operatorname{TV}(f;U)<\infty'],'Integrable functions with finite anisotropic variation, understood modulo Lebesgue almost-everywhere equality. This is larger than W^(1,1); weak differentiability is not a premise of Theorem1.','Sections 3.1–3.2 — Bounded variation space')
add(3,'essential variation',r'''For a function $g:[a,b]\to\mathbb R$, we define its total variation as:
\[
\operatorname{TV}(g;[a,b])=\sup_{\substack{a<z_1<\cdots<z_{m+1}<b\\z_1,\ldots,z_{m+1}\in\operatorname{AC}(g)}}\sum_{i=1}^m|g(z_i)-g(z_{i+1})|,
\]
(19)
where the supremum is only taken over the set $\operatorname{AC}(g)$ of points of approximate continuity of $g$. Approximate continuity is a weak notion of continuity that excludes, for example, point discontinuities; see Section 1.7.2 of Evans and Gariepy (2015). Observe that the definition in (19) differs from that given in the introduction in that the latter does not require that the supremum be taken over points of approximate continuity.
Some authors, including Evans and Gariepy (2015), differentiate these definitions by calling the latter the variation of $g$ and (19) the essential variation of $g$. An intuitive way of interpreting their connection is as follows: the essential variation of $g$ is the infimum of the variation achievable by any function $\widetilde g$ that agrees with $g$ Lebesgue almost everywhere.''',[12],[],[r'\operatorname{AC}(g)',r'\operatorname{TV}(g;[a,b])'],'Univariate essential variation, with supremum over finite partitions using approximate-continuity points strictly inside the interval. The formal approximate-continuity definition is externally cited, not supplied in this paper; retain that unresolved reference. This is not the unrestricted pointwise variation used in the introduction.','Section 3.2 — Essential variation (19)')
add(4,'coordinate',r'''where for each $j=1,\ldots,d$, we define $U_{-j}=\{x_{-j}:(x_j,x_{-j})\in U\text{ for some }x_j\}$, and $I_{x_{-j}}=[a_{x_{-j}},b_{x_{-j}}]$, with
\[
a_{x_{-j}}=\inf\{x_j:(x_j,x_{-j})\in U\},\qquad b_{x_{-j}}=\sup\{x_j:(x_j,x_{-j})\in U\}.
\]
Recall $f(\cdot,x_{-j})$ denotes $f$ as function of the $j$th coordinate with all other dimensions fixed at $x_{-j}$.''',[12],[],[r'U_{-j}',r'I_{x_{-j}}',r'f(\cdot,x_{-j})'],'Projection onto all coordinates other than j, interval endpoints and coordinate-restricted function. Open bounded convex U supplies nonempty bounded interval fibers for x_-j in its projection. Values at endpoint coordinates are not used by the strict-interior variation partitions.','Theorem 1 — Coordinate slices',kind='theorem_excerpt')
add(5,'lattice',r'''we assume $n=N^d$, and
\[
\{x_1,\ldots,x_n\}=\{1/N,2/N,\ldots,1\}^d:=Z_{n,d}.
\]
(2)''',[1],[],[r'n=N^d',r'Z_{n,d}'],'Uniform Cartesian lattice in [0,1]^d with N points on each axis; N is integral and k,d are fixed in statistical asymptotics. This lattice is not an assumption of the abstract BV slicing theorem or the generalized-lasso theorem.','Section 1 — Uniform lattice (2)',context='the design points form a $d$-dimensional lattice',context_page=1)
add(6,'difference operator',r'''$D_n^{(k+1)}\in\mathbb R^{(n-k-1)\times n}$ is the difference operator of order $k+1$, which we will also loosely call discrete derivative operator of order $k+1$. This can be defined recursively in the following manner:
\[
D_n^{(1)}=\begin{bmatrix}-1&1&0&\ldots&0&0\\0&-1&1&\ldots&0&0\\&&\vdots&&&\\0&0&0&\ldots&-1&1\end{bmatrix},\qquad D_n^{(k+1)}=D_{n-k}^{(1)}D_n^{(k)},\quad k=1,2,3,\ldots.
\]
(4)''',[2],[],[r'D_n^{(k+1)}',r'D_{n-k}^{(1)}D_n^{(k)}'],'Unscaled forward-difference matrices whose row count decreases with order. The dimension requires enough sample points. Repeated application of the separately printed fixed-length zero-boundary Delta operator is not silently identified with this recursion.','Section 1.1 — Univariate difference matrices (4)')
add(7,'Kronecker product',r'''\[
D_{n,d}^{(k+1)}=\begin{bmatrix}D_N^{(k+1)}\otimes I_N\otimes\cdots\otimes I_N\\I_N\otimes D_N^{(k+1)}\otimes\cdots\otimes I_N\\\vdots\\I_N\otimes I_N\otimes\cdots\otimes D_N^{(k+1)}\end{bmatrix}.
\]
(8)
Here $D_N^{(k+1)}\in\mathbb R^{(N-k-1)\times N}$ is the discrete derivative matrix from (4) (as would be used in $k$th order univariate trend filtering on $N$ points); $I_N\in\mathbb R^{N\times N}$ denotes the identity matrix; and $A\otimes B$ denotes the Kronecker product of matrices $A,B$. Each block of rows in (8) is made up of a total of $d-1$ Kronecker products (a total of $d$ matrices).''',[4],[5,6],[r'D_{n,d}^{(k+1)}',r'D_N^{(k+1)}'],'Stack d Kronecker blocks, placing the (k+1)-order difference matrix in each coordinate position and identities elsewhere. No mixed partial differences, N^(k+1) rescaling, periodic wraparound or boundary penalty is added.','Section 1.2 — KTF penalty matrix (8)')
add(8,'Kronecker total variation',r'''we will also refer to $\|D_{n,d}^{(k+1)}\theta\|_1$ as the $k$th order Kronecker total variation (KTV) of $\theta$.''',[4],[7],[r'\|D_{n,d}^{(k+1)}\theta\|_1'],'Unscaled discrete one-norm penalty from the stacked coordinatewise difference matrix. It is a seminorm with a max-degree polynomial null space, distinct from continuum BV variation.','Section 1.2 — Kronecker total variation')
add(9,'KTF',r'''We can also rewrite the KTF problem (6) in a more compact form, so that it resembles (3):
\[
\underset{\theta\in\mathbb R^n}{\operatorname{minimize}}\quad\frac12\|y-\theta\|_2^2+\lambda\|D_{n,d}^{(k+1)}\theta\|_1,
\]
(7)''',[4],[7],[r'\lambda\|D_{n,d}^{(k+1)}\theta\|_1'],'Squared-loss KTF estimate defined by (7), with nonnegative tuning parameter and no 1/n factor in the objective. Theorem3 explicitly uses this matrix formulation. The separate zero-boundary repeated-difference formulation in(6) has a source convention issue for higher order.','Section 1.2 — KTF estimator (7)')
add(10,'Kronecker total variation',r'''First we define the $k$th order Kronecker total variation (KTV) class, for a radius $\rho>0$, by
\[
\mathcal T_{n,d}^k(\rho)=\{\theta\in\mathbb R^n:\|D_{n,d}^{(k+1)}\theta\|_1\le\rho\}.
\]
(23)''',[13],[8],[r'\mathcal T_{n,d}^k(\rho)'],'Discrete KTV seminorm ball. Radius bounds do not bound the polynomial null-space component. Theorems4–5 use radii C_n subject to different upper limits; they do not impose a fixed canonical scaling.','Section 4.1 — KTV class (23)')
add(11,'Sobolev class',r'''it helps to define the order $k+1$ discrete $\ell_2$-Sobolev class:
\[
\mathcal W_{n,d}^{k+1}(\rho)=\{\theta\in\mathbb R^n:\|D_{n,d}^{(k+1)}\theta\|_2\le\rho\}.
\]
(24)
Observe that $\mathcal W_{n,d}^{k+1}(\rho)$ only considers partial derivatives of order $k+1$ aligned with one of the coordinate axes, rather than considering all mixed derivatives of total order $k+1$, as we would in a traditional Sobolev class.''',[14],[7],[r'\mathcal W_{n,d}^{k+1}(\rho)',r'\|D_{n,d}^{(k+1)}\theta\|_2'],'Discrete coordinatewise difference two-norm ball, not a standard continuum Sobolev norm with all mixed derivatives. Theorem6 concerns its full minimax risk.','Section 4.1 — Discrete Sobolev class (24)')
add(12,'data model',r'''Throughout, we assume the data model in (1) with $\theta_{0i}=f_0(x_i)$, $i=1,\ldots,n$ and i.i.d. normal errors, to be precise:
\[
y_i\sim N(\theta_{0,i},\sigma^2),\qquad\text{independently, for }i=1,\ldots,n.
\]
(29)''',[15],[],[r'y_i\sim N(\theta_{0,i},\sigma^2)'],'Independent homoskedastic Gaussian sequence experiment with mean vector theta_0. Section5 risk and probability statements inherit it; Theorem1 is analytic and has no data model. Sigma is treated as fixed in implicit rate constants.','Section 5 — Gaussian data model (29)')
add(13,'minimax risk',r'''based on estimators $\widehat\theta$ of the mean $\theta_0$ in (29), we define for a subset $K\subseteq\mathbb R^n$,
\[
R(K)=\inf_{\widehat\theta}\sup_{\theta_0\in K}\frac1nE\|\widehat\theta-\theta_0\|_2^2,
\]
which is called the minimax risk over $K$.''',[15],[12],[r'R(K)',r'\inf_{\widehat\theta}'],'Worst-case expected squared empirical loss, minimized over estimators under the Gaussian experiment. This is expectation risk; Theorems2–3 instead state stochastic error bounds in probability.','Section 5 — Minimax risk')
add(14,'minimax linear risk',r'''\[
R_L(K)=\inf_{\widehat\theta\text{ linear}}\sup_{\theta_0\in K}\frac1nE\|\widehat\theta-\theta_0\|_2^2,
\]
called the minimax linear risk over $K$, the infimum being restricted to linear estimators $\widehat\theta$ (that is, of the form $\widehat\theta=Sy$ for a matrix $S\in\mathbb R^{n\times n}$).''',[15],[12],[r'R_L(K)',r'\widehat\theta=Sy'],'Minimax expected squared loss restricted to linear maps of the responses. The smoothing matrix is fixed for the experiment/design, not a response-dependent choice that would make the estimator nonlinear.','Section 5 — Minimax linear risk')
add(15,'generalized lasso estimator',STATEMENTS[1].split('Suppose that',1)[0],[15],[],[r'D\in\mathbb R^{r\times n}',r'\lambda\|D\theta\|_1'],'Generic analysis-lasso squared-loss estimator for any fixed penalty matrix D, using the printed unnormalized objective. It is not restricted to a lattice or the KTF operator.','Theorem 2 — Generalized lasso estimator (30)',kind='theorem_excerpt')
add(16,'incoherent',r'''Suppose that $D$ has rank $q$, and denote by $\xi_1\le\cdots\le\xi_q$ its nonzero singular values. Also let $u_1,\ldots,u_q\in\mathbb R^r$ be the corresponding left singular vectors. Assume that these vectors, except possibly for those in a set $I\subseteq[q]$, are incoherent, meaning that for a constant $\mu\ge1$,
\[
\|u_i\|_\infty\le\mu/\sqrt n,\qquad i\in[q]\setminus I.
\]''',[15],[],[r'\|u_i\|_\infty\le\mu/\sqrt n',r'I\subseteq[q]'],'Source incoherence condition for selected left singular vectors, with the printed sqrt(n) normalization despite their dimension r. I indexes the excluded singular vectors; it is not the null space. This condition is explicit in Theorem2, not independently assumed by Theorem3.','Theorem 2 — Singular values and incoherence',kind='theorem_excerpt')
add(17,'nullity',r'''$\operatorname{nullity}(M)$ denotes the nullity (dimension of the null space) of a matrix $M$''',[11],[],[r'\operatorname{nullity}(M)'],'Dimension of a matrix kernel; Theorem2 uses nullity(D), distinct from the number of omitted nonzero singular vectors |I|. This definition does not import the degrees-of-freedom estimator discussed around it.','Section 2.4 — Matrix nullity')
add(18,'effective degree of smoothness',r'''Throughout, we will make reference to the effective degree of smoothness (or effective smoothness for short), defined by
\[
s=\frac{k+1}d.
\]''',[15],[],[r's=\frac{k+1}d'],'Ratio of difference order to dimension, with fixed nonnegative integer k and positive integer d in the lattice asymptotics. The threshold s=1/2 defines the distinct regimes in Theorems3–5.','Section 5.1 — Effective smoothness')
add(19,'projection estimator',r'''we define a truncated eigenmaps estimator based on $D_{n,d}^{(k+1)}$ as follows. Denote by $\xi_i\ge0$, $i\in[N]^d$ its singular values (noting that $(k+1)^d$ of these are zero), where along each dimension in the multi-index, the singular values are sorted in increasing order. Denote also by $v_i\in\mathbb R^n$, $i\in[N]^d$ its corresponding right singular vectors. Then, for a subset $Q\subseteq[N]^d$, we denote by $V_Q\in\mathbb R^{n\times|Q|}$ the matrix with columns given by $v_i$, $i\in Q$, and define the projection estimator
\[
\widehat\theta=V_QV_Q^Ty.
\]
(34)''',[17],[7],[r'\widehat\theta=V_QV_Q^Ty',r'Q\subseteq[N]^d'],'Orthogonal projection onto a tensor-indexed subset of right singular vectors of the KTF operator, including its zero modes. The source gives coordinatewise singular-value ordering, with choices within degenerate eigenspaces implicit. Do not confuse these right vectors with Theorem2’s left singular vectors.','Section 5.3 — Truncated eigenmaps estimator (34)')
add(20,'multivariate polynomial of max degree',r'''By a multivariate polynomial of degree $k$, we mean (adhering to the standard classification) a sum of terms of the form $b\prod_{j=1}^dx_j^{a_j}$, where the sum of degrees satisfies $\sum_{j=1}^da_j\le k$. By a multivariate polynomial of max degree $k$, we mean the same, but where the degrees satisfy $a_j\le k$, $j=1,\ldots,d$.''',[9],[],[r'\sum_{j=1}^da_j\le k',r'a_j\le k'],'Coordinatewise degree bound for the polynomial projection in Theorem5; it allows mixed monomials and is not the total-degree-k space. The source’s null-space basis has dimension (k+1)^d.','Section 2.1, footnote 4 — Max-degree polynomial space')
add(21,'canonical scalings',r'''we define the canonical scalings for the discrete Sobolev and KTV classes as
\[
B_n^*=n^{\frac12-\frac{k+1}d},
\]
(27)
\[
C_n^*=n^{1-\frac{k+1}d},
\]
(28)''',[14],[],[r'B_n^*',r'C_n^*'],'Two named numerical radius sequences. Theorem6 explicitly invokes B_n-star in its last sentence. Theorems3–5 use general radii; their canonical specializations are in corollaries or remarks and are not added as theorem assumptions.','Section 4.2 — Canonical radius scalings (27)–(28)')
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
