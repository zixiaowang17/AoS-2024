"""Transcribe statement prerequisites from the inspected pinned preprint, without supplements."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
interfaces=[];members={};edges={}
def add(lid,term,body,pages,heading,deps=None,*,kind='definition',symbols=(),phrases=(),context=None,note=None,shape):
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,
        statement_original=body.strip(),relation='exact',depends_on=list(deps or {}),
        evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=list(symbols),highlight_phrases=list(phrases))
    if note:m['variant_note']=note
    terms=term if isinstance(term,list) else [term];keywords=[]
    for t in terms:
        key=dict(paper_id=PID,local_id=lid,source_text=t,label=t[0].upper()+t[1:],kind='term')
        if t not in body:
            assert context and t in context,(lid,t)
            m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=m['evidence'])];key['context_id']=lid+'/name'
        keywords.append(key)
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=' · '.join(k['label'] for k in keywords),
        lean_role='hypothesis' if kind in ('condition','assumption') else 'definition',type_shape=shape,semantic_boundary=shape,
        members=[m],source_keywords=keywords,central_claim_uses=[],dependencies=[],theorem_explanations={}))
    members[lid]=m;edges[lid]=deps or {}
add('D1','diffusion',r'''
Therefore, to simplify the exposition of our main contributions we henceforth assume that $U=1$ in (1) and consider the model
\[
dX_t=\nabla f(X_t)dt+\sqrt{2f(X_t)}dW_t+\nu(X_t)dL_t,\quad t\geq0,\tag{2}
\]
started uniformly at random $X_0\sim Unif(\mathcal O)$. We denote by $\mathbb P_f$ the resulting probability law of $(X_t:t\geq0)$ (in path space).
''',[3],'Section 1 — reflected diffusion, equation (2)',{'D2':'The diffusion takes values in the bounded convex domain with its reflecting boundary.'},kind='source_passage',context=r'We are given discrete observations $X_0,X_D,\ldots,X_{ND},N\in\mathbb N$, of the solution $(X_t:t\geq0)$ of the SDE (2) where $X_0\sim Unif(\mathcal O)$, that is, the diffusion is started in its (constant) invariant distribution.',symbols=[r'\sqrt{2f(X_t)}',r'\mathbb P_f'],shape='Uniformly initialized reflected diffusion with diffusivity f, gradient drift and inward-normal local-time reflection. The potential is fixed to U=1 here; later U denotes an unrelated regularity bound.')
members['D1']['naming_context'][0]['evidence']=[dict(page=5,location='Section 2 — data convention')]
members['D1']['application_context']=[dict(text=r'If $W_t$ is a $d$-dimensional Brownian motion then the corresponding ‘microscopic’ statistical model for a diffusing particle is provided by solutions $(X_t)$ to the stochastic differential equation (SDE)',evidence=[dict(page=2,location='Before equation (1) — Brownian driver')]),dict(text=r'The process is reflected when hitting the boundary $\partial\mathcal O$ of its state space: $L_t$ is a ‘local time’ process acting only when $X_t\in\partial\mathcal O$ and $\nu(x)$ is the (inward) pointing normal vector at $x\in\partial\mathcal O$.',evidence=[dict(page=2,location='After equation (1) — reflection terms')])]
add('D2','bounded convex open subset',r'''
The domain $\mathcal O$ supporting our diffusion process is a bounded convex open subset of $\mathbb R^d$, and to avoid technicalities we assume that the boundary of $\mathcal O$ is smooth, ensuring in particular the existence of all ‘reflecting’ normal vectors $\nu$ at $\partial\mathcal O$.
''',[5],'Section 2 — domain and volume convention',kind='condition',phrases=['bounded convex open subset'],symbols=[],shape='Smooth bounded convex domain with reflecting normal vectors. Volume-one normalization and Lebesgue L2 conventions are separate auxiliary context; the explicit domains (15) are not silently rescaled.')
add('D3','elliptic operator',r'''
For smooth test functions $\phi$, let the elliptic operator $\mathcal L_f$ be given by the action
\[
\mathcal L_f\phi=\nabla\cdot(f\nabla\phi)=\nabla f\cdot\nabla\phi+f\Delta\phi=\sum_{j=1}^d\frac\partial{\partial x_j}\left(f\frac\partial{\partial x_j}\phi\right),\tag{3}
\]
where $\nabla,\nabla\cdot,\Delta$ denote the gradient, divergence and Laplace operator, respectively. Then $u$ solves the heat equation for $\mathcal L_f$ with Neumann boundary conditions $\partial u/\partial\nu=0$ on $\partial\mathcal O$.
''',[5],'Section 2 — divergence-form operator, equation (3)',{'D2':'The operator acts on the stated domain with its smooth reflecting boundary.'},phrases=['elliptic operator'],symbols=[r'\mathcal L_f\phi',r'\partial u/\partial\nu=0'],shape='Divergence-form elliptic operator with scalar coefficient f and homogeneous Neumann boundary condition. Its differential expression and boundary realization are kept distinct in the auxiliary context.')
add('D4','transition operator',r'''
Its fundamental solutions $p_{t,f}(\cdot,\cdot):\mathcal O\times\mathcal O\to[0,\infty)$ describe the probabilities $\int_U p_{t,f}(x,y)dy$ for the position of a diffusing particle to lie in a region $U$ at time $t_0+t$ when it was at $x\in\mathcal O$ at time $t_0$. More generally the transition operator $P_{t,f}$ describes a self-adjoint action on $L^2(\mathcal O)$,
\[
P_{t,f}(\phi)=\int_{\mathcal O}p_{t,f}(\cdot,y)\phi(y)dy,\quad\phi\in L^2(\mathcal O).\tag{4}
\]
The process $(X_t:t\geq0)$ from (2) is the unique Markov random process with these transition probabilities, infinitesimal generator $\mathcal L_f$, and equilibrium (invariant) probability density $d\mu=1$ on $\mathcal O$.
''',[5],'Section 2 — transition density and operator, equation (4)',{'D3':'The density is the fundamental solution of the Neumann heat equation for L_f.','D1':'The same density gives the transition law of reflected diffusion (2).'},phrases=['transition operator'],symbols=[r'P_{t,f}',r'p_{t,f}'],shape='Heat-kernel integral operator, also the transition operator of the reflected process. Observation time D and other times t specialize the same family.')
add('D5','eigen-pairs',r'''
The generator $\mathcal L_f$ with Neumann boundary condition is characterised by an infinite sequence of (orthonormal) eigen-pairs $(e_{j,f},-\lambda_{j,f})\in L^2(\mathcal O)\times(-\infty,0],j\geq0$, where $e_{0,f}$ is the constant eigenfunction corresponding to $\lambda_0=0$. By ellipticity the first eigenvalue satisfies the spectral gap estimate $\lambda_{1,f}>0$ (see (25) below). 
''',[5],'Section 2 — Neumann eigen-pairs',{'D3':'The eigenfunctions and signed eigenvalues belong to the Neumann generator L_f.'},phrases=['eigen-pairs'],symbols=[r'e_{j,f}',r'\lambda_{1,f}'],shape='Orthonormal Neumann generator eigenbasis, with constant zero mode and first positive eigenvalue; The semigroup correspondence is separate explanatory context. Multiplicities are allowed.')
members['D5']['application_context']=[dict(text='The transition operators $P_{t,f}$ from (4) can be described in this eigen-basis via the eigenvalues $\\mu_{j,f}=e^{-t\\lambda_{j,f}}$, and their densities $p_{t,f}$ are uniformly bounded over $\\mathcal O\\times\\mathcal O$.',evidence=[dict(page=5,location='After the Neumann eigen-pairs')])]
add('D6','compact support',r'''
Some more notation: $C(\overline{\mathcal O})$ denotes the space of uniformly continuous functions on $\mathcal O$. The Sobolev and Hölder spaces $H^\alpha(\mathcal O),C^\alpha(\mathcal O)$ of maps defined on $\mathcal O$ are defined as all functions that have partial derivatives up to order $\alpha\in\mathbb N$ defining elements of $L^2(\mathcal O),C(\overline{\mathcal O})$, respectively, and we set $C^\infty(\mathcal O)=\bigcap_{\alpha>0}C^\alpha(\mathcal O)$, $C^0(\mathcal O)=C(\overline{\mathcal O})$ by convention. Attaching the subscript $c$ to any of the preceding spaces denotes the linear subspaces of such functions of compact support within $\mathcal O$. The Sobolev sub-spaces $H_0^k$ of $H^k$ are the completions of $C_c^\infty(\mathcal O)$ for the $H^k$-norms.
''',[5],'Section 2 — compact-support spaces and their completions',phrases=['compact support'],symbols=[r'H_0^k',r'C_c^\infty(\mathcal O)'],shape='Source compact-support function subspaces, distinguished from their Sobolev closures. Theorem 11 uses the continuous dual of H_c^1 with its inherited H1 norm; standard noncompact Sobolev notation remains ambient elsewhere.')
add('D7','parameter space',r'''
A natural Bayesian model for $f$ is obtained by placing a prior probability measure $\Pi$ on a $\sigma$-field $\mathcal S$ of some parameter space
\[
\mathcal F\subset C^2(\mathcal O)\cap\left\{f:f_{min}\leq\inf_{x\in\mathcal O}f(x)\right\},\quad f_{min}>0,
\]
so that unique pathwise solutions to (2) exist for all $f\in\mathcal F$, with transition densities $p_{D,f}$ as after (3).
''',[10],'Section 2.3 — general parameter space',{'D1':'The admissible diffusivities index model (2).','D4':'Their transition densities supply the statistical model.'},phrases=['parameter space'],symbols=[r'\mathcal F',r'f_{min}'],shape='General measurable space of uniformly positive C2 diffusivities. Does not impose the concrete Gaussian prior or the boundary-support restriction used later.')
add('D8','posterior distribution',r'''
If $\mathcal B_{\mathcal O}$ denotes the Borel $\sigma$-field of $\mathcal O$, and if the maps $(f,x,y)\mapsto p_{D,f}(x,y)$ are jointly Borel measurable from $(\mathcal F\times\mathcal O\times\mathcal O,\mathcal S\otimes\mathcal B_{\mathcal O}\otimes\mathcal B_{\mathcal O})\to\mathbb R$, then basic arguments (cf. [24] and also [56]) show that the posterior distribution is given by
\[
\Pi(B\mid X_0,X_D,\ldots,X_{ND})=\frac{\int_B\prod_{i=1}^Np_{D,f}(X_{(i-1)D},X_{iD})d\Pi(f)}{\int_{\mathcal F}\prod_{i=1}^Np_{D,f}(X_{(i-1)D},X_{iD})d\Pi(f)},\qquad B\in\mathcal S.\tag{16}
\]
''',[10],'Section 2.3 — Bayes formula, equation (16)',{'D7':'The prior is a measure on the general measurable parameter space F.','D4':'The Markov likelihood is a product of transition densities.','D1':'The observations are successive points on the reflected diffusion path.'},phrases=['posterior distribution'],symbols=[r'\Pi(B\mid X_0,X_D,\ldots,X_{ND})'],shape='Posterior probability from the product of discrete transition densities with jointly measurable likelihood. The uniform initial law is common to all parameters and cancels.')
add('D9','Gaussian random field',r'''
Take the first $K$ eigenfunctions $\{e_k:0\leq k\leq K\}$ of the Neumann-Laplacian $-\Delta=-\mathcal L_1$ for eigenvalues $0=\lambda_0<\lambda_1\leq\lambda_2<\ldots$, and for $s\geq0$ define a Gaussian random field
\[
\theta(x)=\frac{\zeta(x)}{N^{d/(4s+4+2d)}}\left(g_0+\sum_{1\leq k\leq K}\lambda_k^{-s/2}g_ke_k(x)\right),\quad x\in\mathcal O,\quad g_k\sim^{iid}N(0,1),\quad K\in\mathbb N,
\]
where for some compact subset $\mathcal O_0\subset\mathcal O$, the map $\zeta\in C_c^\infty(\mathcal O)$ is a non-negative cut-off function vanishing on $\mathcal O\setminus\mathcal O_0$ and equal $1$ on some further compact subset $\mathcal O_{00}$ of the interior of $\mathcal O_0$.
''',[10],'Section 2.3 — truncated Gaussian field and cutoff',{'D5':'The field uses the Neumann eigenbasis specialized to coefficient f=1, with its constant mode separated.','D6':'The cutoff is a smooth compactly supported function, with nested compact support sets.'},phrases=['Gaussian random field'],symbols=[r'\theta(x)',r'N^{d/(4s+4+2d)}',r'\mathcal O_{00}'],shape='N-rescaled finite Neumann Gaussian series with smooth cutoff and two nested compact sets. The index set 0 through K contains K+1 terms despite the source calling these the first K eigenfunctions.')
add('D10','prior for the diffusivity',r'''
The prior for the diffusivity $f\in\mathcal F=C^2\cap\{f\geq1/4\}$ (equipped with the trace Borel $\sigma$-algebra $\mathcal S$ of the separable Banach space $C(\overline{\mathcal O})$) is then
\[
f=f_\theta=\frac14+\frac{e^\theta}4,\quad\Pi=Law(f)\tag{17}
\]
which equals $1/2$ on $\mathcal O\setminus\mathcal O_0$. Note that the ‘base case’ $\theta=0$ corresponds to $f=1/2$ and hence to the case where the diffusion in (2) is a standard reflected Brownian motion with generator $\mathcal L_{1/2}=\Delta/2$. The construction can be adapted to any fixed $f_{min}>0$ replacing $1/4$.
''',[10],'Section 2.3 — transformed diffusivity prior, equation (17)',{'D9':'The law is induced by exponentiating the specified cutoff Gaussian field.'},phrases=['prior for the diffusivity'],symbols=[r'f_\theta',r'\Pi=Law(f)'],shape='Exponentially transformed Gaussian-series prior on diffusivities above one quarter and fixed to one half outside the support. The theorem-2 plug-in is the same link evaluated at posterior mean theta, not the posterior mean of f.')
add('D11','estimator',r'''
For $J\in\mathbb N$ take $E_J\equiv\{e_{j,1}:0\leq j\leq J-1\}$ the eigenfunctions of the Neumann Laplacian $\mathcal L_1$ on $\mathcal O$ (including $e_0=1$) and regard $E_J\simeq\mathbb R^J$ as a normed space equipped with the Euclidean norm via Parseval’s identity for $L^2(\mathcal O)$. Given the observations $X_0,X_D,\ldots,X_{ND}$ define a $J\times J$ matrix by
\[
\widehat{\mathbf P}_{j,j'}=\frac1N\sum_{i=1}^Ne_{j,1}(X_{(i-1)D})e_{j',1}(X_{iD}),\quad0\leq j,j'\leq J-1.\tag{62}
\]
Via the injection of $E_J\simeq\mathbb R^J$ into $L^2(\mathcal O)$ we can regard $\widehat{\mathbf P}_J$ as a bounded linear operator $\widehat P_J$ on $L^2$ described by the action
\[
\begin{aligned}
\langle\widehat P e_{j,1},e_{j',1}\rangle_{L^2}&\equiv\widehat{\mathbf P}_{j,j'},&0\leq j,j'\leq J-1\\
&=0&\text{otherwise}.\end{aligned}\tag{63}
\]
''',[21,22],'Section 3.5.1 — transition-operator estimator, equations (62)-(63)',{'D5':'The fixed approximation basis is the Neumann Laplacian eigenbasis at f=1.','D1':'The matrix averages consecutive observation pairs from the diffusion.'},context=r'In this subsection we construct explicit estimator $\widehat P_D$ for the transition operator $P_{D,f}$ and prove Theorem 3.',symbols=[r'\widehat P_J',r"\widehat{\mathbf P}_{j,j'}"],shape='Finite matrix of empirical transition-pair moments, extended by zero outside the first J Laplacian modes. Preserves the displayed input/output matrix orientation and the source notation switches.')
members['D11']['naming_context'][0]['evidence']=[dict(page=21,location='Start of Section 3.5.1')]
add('D12','first block of eigenfunctions',r'''
To this end, define the first block of eigenfunctions $e_l\in H^2(\mathcal O)$ of $-\mathcal L_{f_0}$ from (3) as
\[
E_{1,f_0,\iota}=\sum_{l:\lambda_{l,f_0}=\lambda_{1,f_0}}e_{l,f_0}\iota_l,\tag{9}
\]
where $\lambda_{1,f_0}$ is the first (non-zero) eigenvalue. Note that the last sum is necessarily finite and $\iota=(\iota_l)$ is any vector of scalars.
''',[7],'Section 2.2.1 — first eigenspace combination, equation (9)',{'D5':'The combination ranges over the first positive generator eigenspace, retaining all multiplicities.'},phrases=['first block of eigenfunctions'],symbols=[r'E_{1,f_0,\iota}'],shape='An arbitrary scalar linear combination of all eigenfunctions at the first positive eigenvalue of minus L_f0. Does not assume the eigenvalue is simple.')
add('D13','hyperrectangle',r'''
For example consider $d\geq2$ and a hyperrectangle $\mathcal O_{(w)}=(0,1)^{d-1}\times(0,w)$ for $w$ to be chosen, and define
\[
\mathcal O_{m,w}=\{x\in\mathbb R^d:|x-\mathcal O_{(w)}|_{\mathbb R^d}<1/m\},\quad m\in\mathbb N.\tag{15}
\]
Then the $\mathcal O_{m,w}$ are bounded convex domains that have smooth boundaries $\partial\mathcal O_{m,w}$ for all $m$, and we will show that the conclusion of Proposition 1 remains valid for $m$ large enough.
''',[9],'Section 2.2.2 — enlarged hyperrectangle, equation (15)',phrases=['hyperrectangle'],symbols=[r'\mathcal O_{m,w}',r'\mathcal O_{(w)}'],shape='Distance-neighborhood enlargement of a hyperrectangle. The source assertion of smoothness is preserved; the usual Euclidean distance construction has a boundary-regularity issue recorded separately.')
add('D14','Kullback-Leibler',r'''
For $(X_t:t\geq0)$ the diffusion process (2) with transition densities from (33), the Kullback-Leibler (KL-) divergence in our discrete measurement model with observation distance $D>0$ is defined as
\[
KL(f,f_0)=E_{f_0}\left[\log\frac{p_{D,f_0}(X_0,X_D)}{p_{D,f}(X_0,X_D)}\right],\quad f,f_0\in\mathcal F,\tag{44}
\]
where we regard the $p_{D,f}$ from (33) as joint probability densities on $\mathcal O\times\mathcal O$ (as $vol(\mathcal O)=1$).
''',[17],'Section 3.3 — Kullback-Leibler divergence, equation (44)',{'D1':'The expectation is under the uniformly stationary diffusion law at f0.','D4':'The density ratio compares transition kernels at the same observation distance.','D7':'The parameter arguments belong to the stated class F.'},phrases=['Kullback-Leibler'],symbols=[r'KL(f,f_0)'],shape='One-transition KL divergence with truth f0 in the numerator and expectation, indexed in the source as KL(f,f0). Uniform stationarity and volume one turn transition kernels into joint densities.')
add('D15','small ball probabilities',r'''
For $\delta>0$ define
\[
B_\delta=\left\{f\in\mathcal F:KL(f,f_0)\leq\delta^2,\ Var_{f_0}\left(\log\frac{p_{D,f}(X_0,X_D)}{p_{D,f}(X_0,X_D)}\right)\leq2\delta^2\right\}.
\]
''',[25],'Lemma 3 — definition of the neighbourhood Bδ',{'D14':'The neighborhood constrains the one-transition KL divergence KL(f,f0).','D4':'Its second condition is the printed variance of a log transition-density ratio.'},context='3.3. Information distances and small ball probabilities.',symbols=[r'B_\delta'],shape='Source KL/variance neighborhood used in Theorem 12. The printed numerator and denominator in the variance condition are identical; no f0 is silently inserted into the denominator.')
members['D15']['naming_context'][0]['evidence']=[dict(page=17,location='Section 3.3 heading')]
add('D16','hypothesis on the eigenfunctions',r'''
\[
\inf_{x\in\mathcal O_0}\frac12\Delta E_{1,f_0,\iota}(x)+\mu|\nabla E_{1,f_0,\iota}(x)|_{\mathbb R^d}^2\geq c_0>0,\tag{10}
\]
for some $\mu,c_0>0$ and some vector $\iota$.
''',[7],'Theorem 6 — eigenfunction condition (10)',{'D12':'The condition acts on a scalar combination from the first positive eigenspace.'},kind='theorem_excerpt',context=r'Stability of this transport operator can be reduced to a hypothesis on the eigenfunctions of $P_{t,f_0}$, which in turn can be tackled with techniques from spectral geometry.',symbols=[r'\Delta E_{1,f_0,\iota}(x)',r'|\nabla E_{1,f_0,\iota}(x)|_{\mathbb R^d}^2'],shape='Positive lower bound on one-half the Laplacian plus a weighted squared gradient of a chosen first-eigenspace combination on the compact interior set. Pairwise coefficient regularity bounds are separate inherited theorem hypotheses.')
interfaces[-1]['lean_role']='hypothesis'
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
    print('Saved',len(interfaces),'source-backed interfaces; theorem connections pending.')


if __name__ == '__main__':
    main()
