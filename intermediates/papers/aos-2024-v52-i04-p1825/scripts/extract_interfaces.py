"""Restore original main-text definitions; source review is recorded separately."""
import json
from save_inventory import PID, ROOT
interfaces=[]
members={}
def add(n,term,s,pages,deps,symbols,description,heading,kind='definition',context=None,context_page=None):
    lid=f'D{n}'
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=[])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original naming context')])]
        kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='definition',type_shape=description,semantic_boundary=description,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))

add(1,'two-dimensional flat torus',r'''Throughout we denote by $\Omega=[0,2\pi]^2$ the two-dimensional flat torus, i.e., opposite endpoints are identified and all functions are periodic: $u(\cdot+2\pi e_i)=u(\cdot)$ for $i=1,2$ where $e_1=(1,0),e_2=(0,1)$ are the canonical basis vectors in the plane.''',[4],[],[r'\Omega=[0,2\pi]^2',r'u(\cdot+2\pi e_i)'],'Periodic square with opposite sides identified. Its canonical coordinate basis is distinct from the Stokes eigenbasis denoted by e_j later.','Section 2.1 — Two-dimensional flat torus')
add(2,'infinitely differentiable periodic functions',r'''We define $C^\infty(\Omega)$ as the space of infinitely differentiable periodic functions with fundamental periodic domain $\Omega$.''',[4],[1],[r'C^\infty(\Omega)'],'Smooth periodic scalar functions; vector-valued C-infinity(Omega)^2 is used explicitly in Theorem 2.','Section 2.1 — Infinitely differentiable periodic functions')
add(3,'Sobolev spaces',r'''We also require the usual $L^2(\Omega)$ spaces of square integrable functions for Lebesgue measure $dx$, as well as the Sobolev spaces $H^m(\Omega),m\in\mathbb N$, of functions $f\in L^2(\Omega)$ whose (weak) partial derivatives up to order $m$ lie in $L^2(\Omega)$. When considering two-dimensional vector fields $v=(v_1,v_2):\Omega\to\mathbb R^2$ with components $v_1,v_2$ lying in some function space $\mathcal X$, we will write $v\in\mathcal X^2$ – or sometimes even only $v\in\mathcal X$ when no confusion may arise.''',[4],[1],[r'H^m(\Omega)',r'L^2(\Omega)',r'\mathcal X^2'],'Lebesgue L2 and integer-order weak-derivative Sobolev spaces, with the explicit vector-field shorthand. Fractional H^alpha in Condition 1 uses an unexpanded standard convention.','Section 2.1 — Sobolev spaces and vector fields')
add(4,'spaces of vector fields',r'''The divergence operation
\[
\nabla\cdot v=\frac{\partial}{\partial x_1}v_1+\frac{\partial}{\partial x_2}v_2
\]
for smooth vector fields extends to a linear operation $\nabla\cdot$ in the sense of (periodic Schwartz) distributions. We can then define spaces of vector fields
\[
H=\left\{u\in L^2(\Omega)^2:\nabla\cdot u=0,\int_\Omega u=0\right\},
\]
(4)
as well as
\[
V=\left\{u\in(H^1(\Omega))^2:\nabla\cdot u=0,\int_\Omega u=0\right\},
\]
(5)
and equip these spaces with inner products $\langle\cdot,\cdot\rangle_H\equiv\langle\cdot,\cdot\rangle_{L^2}$ and
\[
\langle u,v\rangle_V\equiv\langle\nabla u,\nabla v\rangle_{L^2}=\sum_{i,j=1}^2\int_\Omega\frac{\partial u_i(x)}{\partial x_j}\frac{\partial v_i(x)}{\partial x_j}\,dx,
\]
where $\nabla$ is the gradient operator. The resulting norms are denoted by $\|\cdot\|_H,\|\cdot\|_V$, respectively.''',[4],[3],[r'\nabla\cdot u=0',r'\int_\Omega u=0',r'\langle u,v\rangle_V'],'Two distinct divergence-free, zero-mean spaces: H uses L2 and V uses first weak derivatives with the gradient inner product. H is not the Gaussian RKHS calligraphic H.','Section 2.1 — Spaces of vector fields (4)–(5)')
add(5,'Helmholtz-Leray',r'''The ‘Helmholtz-Leray’ $L^2$-projector $P:L^2(\Omega)^2\to H$ extends to act on all Schwartz distributions.''',[4],[3,4],[r'P:L^2(\Omega)^2\to H'],'Orthogonal L2 projection to divergence-free zero-mean fields, with the source-stated distributional extension.','Section 2.1 — Helmholtz-Leray projector')
add(6,'Stokes operator',r'''The Stokes operator is then $A=-P\Delta$ where $\Delta=\nabla\cdot\nabla$ is the Laplacian. In the case of periodic boundary conditions one in fact has $A=-\Delta$ on its domain
\[
\mathcal D(A)\equiv H^2(\Omega)^2\cap V,
\]
(see (9.15) in [38]). The operator $A$ then has ‘graph norm’
\[
\|u\|_{\mathcal D(A)}\equiv\|Au\|_{L^2}\simeq\|u\|_{H^2},
\]
(see (9.13) in [38]).''',[4],[1,3,4,5],[r'A=-P\Delta',r'\mathcal D(A)',r'\|Au\|_{L^2}'],'Periodic Stokes operator, its H2 divergence-free domain and the stated equivalent graph norm. The pressure formulation is not required to define A.','Section 2.1 — Stokes operator')
add(7,'bilinear form',r'''Next, using appropriate versions of Sobolev inequalities (p.243 in [38] or Ch.6 in [8]) and recalling (2), we can realise the bilinear form
\[
B(u,v)=P[(u\cdot\nabla)v],\quad\text{as }B:V\times V\to V',
\]
(6)
where $V'$ is the topological dual space of $V$ with the usual dual pairing $\langle\cdot,\cdot\rangle_{V,V'}$ arising from the action of the $L^2$-inner product.''',[4,5],[4,5],[r'B(u,v)',r"V'"],'Projected convective bilinear form valued in the topological dual of V. Its componentwise convection is retained as auxiliary source formula (2).','Section 2.1 — Bilinear form (6)')
add(8,'incompressible Navier-Stokes equations',r'''Now let $\nu>0$ be a fixed viscosity constant and $f\in V$ a forcing term. To expedite proofs we take $f$ to be time-independent but this is not necessary. We are interested in (spatially) periodic vector fields $u=u_\theta=(u_\theta(t,x):t\in(0,T],x\in\Omega)$ that solve the incompressible Navier-Stokes equations represented by the system of non-linear partial differential equations
\[
\begin{aligned}
\frac{\partial}{\partial t}u-\nu\Delta u+(u\cdot\nabla)u&=f-\nabla p&&\text{on }(0,T]\times\Omega,\\
\nabla\cdot u&=0&&\text{on }(0,T]\times\Omega,\\
\int_\Omega u(t,\cdot)&=0&&\text{for all }t\in(0,T],\\
u(0,\cdot)&=\theta&&\text{on }\Omega,
\end{aligned}
\]
(9)
where $\theta\in V$ is an initial condition and $p$ is a scalar pressure term.''',[5],[1,4],[r'\nu>0',r'u=u_\theta',r'\nabla p'],'Physical pressure formulation with zero divergence, zero spatial mean, positive viscosity, time-independent forcing in V, and initial condition. It fixes the standing parameters for the reduced equation.','Section 2.1 — Incompressible Navier-Stokes equations (9)',kind='source_passage')
add(9,'non-linear evolution equation',r'''we see that in order to find such a weak solution, it suffices to find a solution $u\in V$ of the non-linear evolution equation in $V'$ given by
\[
\begin{aligned}
\frac{du}{dt}+\nu Au+B(u,u)&=f\\
u(0)&=\theta.
\end{aligned}
\]
(10)
When this equation holds in the space $H$ (rather than just in $V'$), we speak of a ‘strong’ solution. See Ch.9 in [38] or Ch.5 in [8] for details. For the problem of recovering the initial condition studied below, we shall content ourselves with the information provided by the solutions of the reduced equation (10), but it is not difficult to see (from the Helmholtz decomposition theorem) that (10) and (9) are in fact equivalent equations.''',[5],[4,6,7,8],[r'\frac{du}{dt}+\nu Au+B(u,u)',r'u(0)'],'Reduced periodic Navier-Stokes equation with the source strong-solution convention: equality in H, rather than only V-prime. Additional analytic solution theory is referenced externally, not invented as a new definition.','Section 2.1 — Non-linear evolution equation and strong solutions (10)')
add(10,'function spaces',r'''To formulate an existence result for strong solutions of (10), consider function spaces
\[
L^p((0,T],\mathcal X)\equiv\left\{u:(0,T]\times\Omega\to\mathbb R^2:\int_0^T\|u(t,\cdot)\|_{\mathcal X}^p\,dt<\infty\right\},\quad1\leq p<\infty,
\]
with corresponding Bochner-integral norm for $\mathcal X$-valued maps, where $\mathcal X$ is a normed linear space of vector fields over $\Omega$ to be specified. Similarly we define the spaces $L^\infty((0,T],\mathcal X)$ and $C([0,T],\mathcal X)$ of time-bounded or -continuous $\mathcal X$ valued maps.''',[5],[1],[r'L^p((0,T],\mathcal X)',r'C([0,T],\mathcal X)'],'Source Bochner-integrable, time-bounded and time-continuous function-space conventions. The theorem fixes X=V for its continuous strong solutions. Measurability and essential-supremum conventions are not fully expanded.','Section 2.1 — Time-dependent function spaces')
add(11,'statistical observations',r'''For $u=u_\theta$ a (strong) solution of the PDE (10) with unknown initial condition $u(0)=\theta\in V$, the statistical observations are assumed to consist of the random vectors $Z^{(N)}=(Y_i,t_i,X_i)_{i=1}^N$
\[
Y_i=u_\theta(t_i,X_i)+\varepsilon_i,\quad\varepsilon_i\sim^{i.i.d.}N(0,I_{\mathbb R^2}),\quad i=1,\ldots,N,
\]
(19)
with $(t_i,X_i)_{i=1}^N$ drawn iid from the uniform distribution $\lambda$ on $(T_0,T]\times\Omega$, independently of the Gaussian noise vectors $\varepsilon_i$. Here $(T_0,T]$ is the time horizon where measurements are taken and the (fixed) constants $T_0,T$ are such that $0\leq T_0<T$. We include by convention the case $0<T_0=T$ of a single temporal measurement $(T_0,T]\equiv\{T\}$ is; in this case $\lambda=\delta_T\otimes\lambda_\Omega$ where $\delta_T$ is Dirac measure at $\{T\}$ and $\lambda_\Omega$ the uniform distribution on $\Omega$. The law on $(\mathbb R^2\times(T_0,T]\times\Omega)^N$ of the data vector $Z^{(N)}=(Y_i,t_i,X_i)_{i=1}^N$ when $u_\theta$ arises from the initial condition $\theta$ will be denoted by $P_\theta^N$.''',[8],[1,4,9],[r'Z^{(N)}',r'u_\theta(t_i,X_i)',r'P_\theta^N'],'Independent random space-time design and Gaussian measurement noise; includes the single-time Dirac-design convention. Viscosity and forcing are known, and the dynamics are deterministic. Theorem 4 narrows this model to strictly positive observation times.','Section 2.2 — Statistical observations (19)',kind='source_passage')
add(12,'centred Gaussian random vector field',r'''Consider a Borel probability measure $\Pi'$ on $V\cap H^2(\Omega)^2$ arising as the law of the centred Gaussian random vector field $(\theta'(x)=(\theta'_1(x),\theta'_2(x)):x\in\Omega)$ with reproducing kernel Hilbert space (RKHS) $\mathcal H$ continuously imbedded into $V\cap H^\alpha(\Omega)^2$ for some $\alpha\geq2$. Then take as prior $\Pi=\Pi_N$ for $\theta$ the law of the rescaled random vector field $\theta=\theta'/N^{1/(2\alpha+2)}$.''',[8],[3,4],[r'\Pi=\Pi_N',r'\mathcal H',r"\theta=\theta'/N^{1/(2\alpha+2)}"],'Base centered Gaussian law with H2 support and RKHS embedding of order alpha, rescaled by a sample-size-dependent factor. The RKHS is calligraphic H and need not equal the full Sobolev space; the following example is not an extra assumption.','Condition 1',kind='condition')
add(13,'eigenfunctions',r'''for instance we could define the prior for $\theta'$ immediately as a Gaussian series expansion (e.g., (B.1) in [32]) for the (real parts of the) $H$-orthonormal eigenfunctions
\[
e_k\propto(k_2,-k_1)e^{ik\cdot(\cdot)},\quad k\in\mathbb Z^2\setminus\{(0,0)\},
\]
(20)
of the Stokes operator.''',[8],[1,4,6],[r'e_k',r'(k_2,-k_1)'],'Source complex Fourier form, with real parts specified in the prose and normalization only proportional. Theorem 5 separately orders a real L2-orthonormal eigenbasis by eigenvalues.','Section 2.2 — Eigenfunctions of the Stokes operator (20)',kind='source_passage')
add(14,'posterior distribution',r'''Algorithmically we first compute the posterior distribution for the initial state $\theta$, which in the model (19) is of the form
\[
d\Pi(\theta\mid Z^{(N)})\propto e^{\ell_N(\theta)}d\Pi(\theta);\quad\ell_N(\theta)=-\frac12\sum_{i=1}^N|Y_i-u_\theta(X_i,t_i)|^2,\quad\theta\in V,
\]
(21)
where $|\cdot|=|\cdot|_{\mathbb R^2}$ is the Euclidean norm. Even though the prior is Gaussian, the non-linearity of the map $\theta\to u_\theta$ renders $\Pi(\cdot\mid Z^{(N)})$ a non-Gaussian random probability measure in the function space $V$.''',[9],[4,9,11,12],[r'\ell_N(\theta)',r'd\Pi(\theta\mid Z^{(N)})'],'Bayesian posterior weighted by the nonlinear Gaussian observation likelihood. The source writes u_theta(X_i,t_i), reversing the arguments in (19); this is preserved as a notation issue.','Section 2.2 — Posterior distribution (21)')
add(15,'posterior (‘Bochner-’) mean',r'''Moreover, if
\[
\bar\theta_N=E^\Pi[\theta\mid Z^{(N)}]\in V
\]
is the posterior (‘Bochner-’) mean and $u_{\bar\theta_N}$ the solution of the Navier-Stokes equation (10) with initial condition $\bar\theta_N$, then''',[10],[4,9,14],[r'\bar\theta_N',r'u_{\bar\theta_N}'],'The posterior mean initial condition and its nonlinear forward solution. This plug-in trajectory is not identified with the posterior mean trajectory. The source definition is excerpted from Theorem 3, whose full body remains in the inventory.','Theorem 3 — Posterior mean',kind='theorem_excerpt')
add(16,'inverse Poincaré',r'''B) Let further $0<c_P<\infty$ be a (‘inverse Poincaré’) constant such that
\[
\frac{\|u(0)-v(0)\|_V}{\|u(0)-v(0)\|_{L^2}}\leq c_P.
\]
(15)''',[6],[3,4],[r'c_P',r'\|u(0)-v(0)\|_V'],'Additional named hypothesis in Theorem 1B. The ratio is unsquared; a constant for one pair of distinct initial conditions differs from a uniform constant over a statistical parameter class. Zero denominators remain unspecified.','Theorem 1B — Inverse Poincaré condition (15)',kind='theorem_excerpt')
add(17,'Gaussian prior',r'''Denote by $(e_j:j\in\mathbb N)\subset V$ an enumeration of the $L^2$-orthonormal basis of $H$ arising from the eigenfunctions of the Stokes operator $A$ from (20), ordered by increasing eigenvalues. Let the prior $\Pi$ be as in Condition 1 and project it onto the span $E_J=\{e_j:j\leq J\}$ with $J=J_N=O(\log\log N)$. Suppose the ground truth initial condition $\theta_0$ lies in $\mathcal H\cap E_{J_0}$ for some arbitrary fixed $J_0\in\mathbb N$.''',[11],[3,4,6,12,13],[r'E_J',r'J=J_N',r'\mathcal H\cap E_{J_0}'],'Projected Gaussian prior and fixed spectral truth support in Theorem 5. Preserve the source set notation alongside the word span and the upper-bound-only J_N condition. The replacement rate and inherited conclusions remain in the original theorem.','Theorem 5 — Projected Gaussian prior',kind='theorem_excerpt',context=r'''If we use a Gaussian prior that has a slowly growing expansion in the eigenfunctions from (20), and if the true initial condition $\theta_0$ is ‘band-limited’ in the Stokes spectrum, then we can indeed obtain convergence rates that approach the ‘parametric’ rate $1/\sqrt N$ of finite-dimensional models as we increase the regularity of the prior, $\alpha\to\infty$.''',context_page=10)

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    for name,data in [('source-passages.json',dict(paper_id=PID,status='extracted',scope='Original main-text source passages; source review is a separate gate.',source_passages=list(members.values()))),('interface-extraction.json',dict(paper_id=PID,status='extracted',interfaces=interfaces))]:
        (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(members)} source entries; validation status is recorded separately.')
if __name__=='__main__':main()
