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


add('D1','manifold',r'''
Throughout the paper, all smooth manifolds $\mathcal M$ are assumed to be embedded in $\mathbb R^d$ and we consider the tangent and normal spaces to $\mathcal M$ as subspaces of $\mathbb R^d$. Thus, a set $\mathcal M\subset\mathbb R^d$ is a $C^p$ manifold (with $p\ge1$) if around any point $x\in\mathcal M$ there exists an open neighborhood $U\subset\mathbb R^d$ and a $C^p$-smooth map $F$ from $U$ to some Euclidean space $\mathbb R^n$ such that the Jacobian $\nabla F(x)$ is surjective and equality $\mathcal M\cap U=F^{-1}(0)$ holds. Then $F=0$ are called the local defining equations for $\mathcal M$, and the tangent and normal spaces to $\mathcal M$ at $x$ are defined by $T_{\mathcal M}(x):=\operatorname{Null}(\nabla F(x))$ and $N_{\mathcal M}(x):=(T_{\mathcal M}(x))^\perp$, respectively.
''',[6],'Section 2.1 — embedded manifold and local defining equations',symbols=[r'T_{\mathcal M}(x)',r'N_{\mathcal M}(x)',r'\mathcal M\cap U=F^{-1}(0)'],shape='Embedded Cp manifold via local full-row-rank defining equations, with tangent and normal subspaces. Theorem 2.7 uses its own local defining map G; the letter F in this generic definition is not the theorem set-valued F.')
add('D2','distance and the projection',r'''
The distance and the projection of a point $x\in\mathbb R^d$ onto a set $Q\subset\mathbb R^d$ are
\[
d(x,Q):=\inf_{y\in Q}\|y-x\|\qquad\text{and}\qquad P_Q(x):=\operatorname*{argmin}_{y\in Q}\|y-x\|,
\]
respectively.
''',[6],'Section 2 — distance and projection',symbols=[r'P_Q(x)',r'd(x,Q)'],shape='Distance and possibly set-valued nearest-point projection. Projection onto tangent subspaces is single-valued; projection onto an embedded manifold is used only in a local neighborhood with the source regularity convention. Later dist(x,M) denotes the same distance.')
add('D3','covariant Jacobian',r'''
A map $F:\mathcal M\to\mathbb R^m$ is called $C^p$ smooth near a point $x$ if there exists a map $\widehat F:U\to\mathbb R^d$ defined on some neighborhood $U\subset\mathbb R^d$ of $x$ that agrees with $F$ on $\mathcal M$ near $x$. In this case, we define the covariant Jacobian $\nabla F(x):T_{\mathcal M}(x)\to\mathbb R^m$ by the expression $\nabla_{\mathcal M}F(x)u=\nabla\widehat F(x)u$ for all $u\in T_{\mathcal M}(x)$.
''',[7],'Section 2.1 — covariant Jacobian',{'D1':'The derivative acts on the tangent space of the embedded manifold.'},symbols=[r'\nabla_{\mathcal M}F(x)u=\nabla\widehat F(x)u'],shape='Derivative of an extension restricted to the tangent space. The source prints the extension codomain R^d despite F having codomain R^m, omits explicit Cp smoothness of the extension in this sentence, and alternates nabla F with nabla_M F; preserve these wording issues.')
add('D4','Fréchet subdifferential',r'''
Namely, consider a function $f:\mathbb R^d\to\mathbb R\cup\{\infty\}$ and a point $x\in\operatorname{dom}f$. The Fréchet subdifferential of $f$ at $x$, denoted $\widehat\partial f(x)$, consists of all vectors $v\in\mathbb R^d$ satisfying the approximation property:
\[
f(y)\ge f(x)+\langle v,y-x\rangle+o(\|y-x\|)\qquad\text{as}\qquad y\to x.
\]
''',[7],'Section 2.2 — Fréchet subdifferential',symbols=[r'\widehat\partial f(x)'],shape='Regular subgradient defined by a first-order lower approximation. Theorem 2.7 requires the regular inclusion -A(xbar) in this set, not merely limiting criticality.')
add('D5','limiting subdifferential',r'''
The limiting subdifferential of $f$ at $x$, denoted $\partial f(x)$, consists of all vectors $v\in\mathbb R^d$ such that there exist sequences $x_i\in\mathbb R^d$ and Fréchet subgradients $v_i\in\widehat\partial f(x_i)$ satisfying $(x_i,f(x_i),v_i)\to(x,f(x),v)$ as $i\to\infty$.
''',[7],'Section 2.2 — limiting subdifferential',{'D4':'The limiting subgradient is obtained from regular subgradients at nearby points, with simultaneous convergence of function values.'},symbols=[r'\partial f(x)',r'(x_i,f(x_i),v_i)\to(x,f(x),v)'],shape='Function-value-attentive limit of regular subgradients. It is not the convex subdifferential unless extra structure justifies that identification.')
add('D6','Active manifold',r'''
Consider a function $f:\mathbb R^d\to\mathbb R\cup\{\infty\}$ and fix a set $\mathcal M\subseteq\operatorname{dom}f$ containing a point $\bar x$ satisfying $0\in\partial f(\bar x)$. Then $\mathcal M$ is called an active $C^p$-manifold around $\bar x$ if there exists a constant $\epsilon>0$ satisfying the following.

• (smoothness) The set $\mathcal M$ is a $C^p$ manifold near $\bar x$ and the restriction of $f$ to $\mathcal M$ is $C^p$-smooth near $\bar x$.

• (sharpness) The lower bound holds:
\[
\inf\{\|v\|:v\in\partial f(x),\ x\in U\setminus\mathcal M\}>0,
\]
where we set $U=\{x\in B_\epsilon(\bar x):|f(x)-f(\bar x)|<\epsilon\}$.

More generally, we say that $\mathcal M$ is an active manifold for $f$ at $\bar x$ for $\bar v\in\partial f(\bar x)$ if $\mathcal M$ is an active manifold for the tilted function $f_v(x)=f(x)-\langle v,x\rangle$ at $\bar x$.
''',[8],'Definition 2.1 (Active manifold)',{'D1':'Smoothness requires the embedded-manifold structure and its local defining equations.','D5':'Criticality and the off-manifold sharpness bound use the limiting subdifferential.'},context='Definition 2.1 (Active manifold).',symbols=[r'\inf\{\|v\|:v\in\partial f(x)',r'f_v(x)=f(x)-\langle v,x\rangle'],shape='Smooth restriction and subgradient separation away from the manifold, localized in both position and function value. The last sentence names bar-v but uses v in the tilt; retain that source notation. Theorem 5.1 only assumes an abstract smooth reduction, not this active-manifold definition.')
add('D7','subdifferentially continuous',r'''
Namely, following [29, Definition 2.1] a function $f$ is called subdifferentially continuous at a point $\bar x$ if for any sequences $(x_i,v_i)\in\operatorname{gph}\partial f$ converging to some pair $(\bar x,\bar v)\in\operatorname{gph}\partial f$, the function values $f(x_i)$ converge to $f(\bar x)$. In particular, functions that are continuous on their domains and closed convex functions are subdifferentially continuous.
''',[12],'Before Theorem 2.7 — subdifferential continuity',{'D5':'The graph in the condition is the limiting subdifferential graph.','D9':'Convergence is tested on pairs in the set-valued subdifferential graph, with argument and subgradient coordinates.'},symbols=[r'(x_i,v_i)\in\operatorname{gph}\partial f'],phrases=['subdifferentially continuous'],shape='Continuity of function values along converging limiting-subgradient graph pairs, at every limiting subgradient specified by the passage. This does not itself impose global lower semicontinuity.')
add('D9','set-valued map',r'''
A set-valued map $F:\mathbb R^d\rightrightarrows\mathbb R^m$ is an assignment that maps a point $x\in\mathbb R^d$ to a set $F(x)\subset\mathbb R^m$. Set-valued maps always admit a set-valued inverse:
\[
F^{-1}(y)=\{x:y\in F(x)\}.
\]
The domain and graph of $F$ are defined, respectively, as
\[
\operatorname{dom}F:=\{x:F(x)\ne\varnothing\}\qquad\text{and}\qquad\operatorname{gph}F:=\{(x,y):y\in F(x)\}.
\]
''',[11],'Section 2.4 — set-valued map, inverse, domain and graph',symbols=[r'F^{-1}(y)=\{x:y\in F(x)\}',r'\operatorname{gph}F'],shape='Set-valued map with graph ordered as (argument,value) and inverse graph with reversed coordinates. These conventions distinguish the inconsistent basepoint orders printed elsewhere.')
add('D8','Smooth invertibility',r'''
Consider a set-valued map $F:\mathbb R^d\rightrightarrows\mathbb R^m$ and a pair $(\bar x,\bar v)\in\operatorname{gph}F$. We say that $F$ is $C^p$ invertible around $(\bar x,\bar v)$ with inverse $\sigma(\cdot)$ if there exists a single-valued $C^p$-smooth map $\sigma(\cdot)$ and a neighborhood $U$ of $(\bar v,\bar x)$ satisfying
\[
U\cap\operatorname{gph}F^{-1}=U\cap\operatorname{gph}\sigma.
\]
''',[11],'Definition 2.6 (Smooth invertibility)',{'D9':'The localization is an equality of inverse graphs under the set-valued inverse convention.'},context='Definition 2.6 (Smooth invertibility).',symbols=[r'U\cap\operatorname{gph}F^{-1}=U\cap\operatorname{gph}\sigma'],shape='A single-valued smooth localization of F inverse, named at the point (xbar,vbar) in gph F. It does not assert F is globally invertible or single-valued.')
add('D10','variational inclusion',r'''
Throughout the section we focus on the problem of finding a point $x^\star$ satisfying the variational inclusion:
\[
0\in A(x)+H(x)\qquad\text{where}\qquad A(x)=\mathbb E_{z\sim\mathcal P}A(x,z).\tag{3.1}
\]
Here $H:\mathbb R^d\rightrightarrows\mathbb R^d$ is an arbitrary set-valued map, $\mathcal P$ is a fixed probability distribution on some measure space $(\mathcal Z,\mathcal F)$, and $A:\mathbb R^d\times\mathcal Z\to\mathbb R^d$ is a measurable map. We will impose the following assumption throughout the rest of the section.
''',[12],'Section 3 — stochastic variational inclusion (3.1)',{'D9':'H is a set-valued map and its sum with the expected A defines the variational inclusion.'},kind='source_passage',symbols=[r'A(x)=\mathbb E_{z\sim\mathcal P}A(x,z)',r'0\in A(x)+H(x)'],shape='Population inclusion with arbitrary deterministic set-valued H and measurable stochastic map A. The same letter A denotes the sampled map with two arguments and its mean with one. H is distinct from the calligraphic H defined locally in Theorem 2.7.')
add('D11','smoothly invertible',r'''
The map $F:=A+H$ is $C^1$-smoothly invertible at $(0,\bar x)$ with inverse $\sigma(\cdot)$.
''',[12],'Assumption A',{'D10':'F is the population inclusion map A+H from (3.1).','D8':'The condition invokes smooth localization of the inverse from Definition 2.6.'},kind='assumption',symbols=[r'F:=A+H',r'\sigma(\cdot)'],shape='C1 solution-map localization. The source prints (0,xbar), reversing the pair order in Definition 2.6; Theorem 3.1 supplies the explicit inverse-graph localization that clarifies the intended role.')
add('D12','Integrability and smoothness',r'''
Suppose that there exists a neighborhood $U$ around $\bar x$ satisfying the following.

1. For almost every $z$, the map $A(\cdot,z)$ is differentiable at every $x\in U$.

2. The second moment bounds hold:
\[
\sup_{x\in U}\mathbb E_{z\sim\mathcal P}\|A(x,z)\|^2<\infty\qquad\text{and}\qquad\sup_{x\in U}\mathbb E_{z\sim\mathcal P}[\|\nabla A(x,z)\|_{\mathrm{op}}^2]<\infty.
\]
''',[13],'Assumption B (Integrability and smoothness)',{'D10':'The differentiability and moment bounds concern the stochastic map A of the population model and its sampling law.'},kind='assumption',context='Assumption B (Integrability and smoothness).',symbols=[r'\sup_{x\in U}',r'\|\nabla A(x,z)\|_{\mathrm{op}}^2'],shape='One common neighborhood and almost-every-z differentiability at every x, with uniform second moments of values and Jacobians. This is weaker than the separate random Lipschitz-Jacobian bound imposed only by Theorem 3.1.')
add('D13','sample average approximations',r'''
The SAA approach to solving (3.1) proceeds as follows. Let $S=\{z_1,\ldots,z_k\}$ be i.i.d samples drawn from $\mathcal P$ and let $x_k$ be a solution of the problem
\[
0\in A_S(x)+H(x)\qquad\text{where}\qquad A_S(x):=\frac1k\sum_{i=1}^k A(x,z_i),\tag{3.2}
\]
assuming one exists.
''',[12,13],'Section 3 — sample average approximation (3.2)',{'D10':'The empirical mean replaces the expected A in (3.1), keeping H unchanged.'},context='We will first show that the solutions of sample average approximations',context_pages=[13],symbols=[r'A_S(x):=\frac1k\sum_{i=1}^k A(x,z_i)'],shape='Empirical variational inclusion, with existence not assumed automatic. Theorem 3.1 additionally selects a measurable local solution with probability tending to one.')
add('D14','divergence',r'''
\[
\Delta_\phi(\mathcal P'\parallel\mathcal P)=\int_{\mathcal Z}\phi\left(\frac{d\mathcal P'}{d\mathcal P}\right)d\mathcal P,
\]
induced by any $C^3$-smooth convex function $\phi:(0,\infty)\to\mathbb R$ satisfying $\phi(1)=0$.
''',[13],'Section 3 — phi-divergence',context=r'We will measure the size of the perturbation with the $\phi$-divergence',symbols=[r'\Delta_\phi'],shape='Divergence of a perturbed law relative to the baseline. The source specifies convex C3 phi and phi(1)=0, without additional normalization of derivatives or an explicit extension at zero or singular laws.')
add('D15','admissible neighborhood',r'''
Define an admissible neighborhood $\mathcal B_\varepsilon$ of $\mathcal P$ to consist of all probability distributions $\mathcal P'$ such that $\Delta_\phi(\mathcal P'\parallel\mathcal P)\le\varepsilon$ and such that there exists a solution $\bar x_{\mathcal P'}\in U$ to the perturbed variational equation $0\in\mathbb E_{z\sim\mathcal P'}[A(x,z)]+H(x)$.
''',[13],'Section 3 — admissible law perturbations',{'D14':'Admissibility bounds the phi-divergence by epsilon.','D10':'The perturbed solution solves the same population inclusion with P replaced by P-prime.'},symbols=[r'\mathcal B_\varepsilon'],shape='Divergence neighborhood restricted to laws admitting a solution in U. The original definition asserts existence, not an explicit unique or measurable choice of a perturbed solution; no extra choice convention is fabricated.')
add('D16','inclusion',r'''
Setting the stage, our goal is to find a point $x$ satisfying the inclusion
\[
0\in F(x),\tag{4.1}
\]
where $F:\mathbb R^d\rightrightarrows\mathbb R^d$ is a set-valued map. Throughout, we fix one such solution $\bar x$ of (4.1).
''',[14],'Section 4 — abstract variational inclusion (4.1)',{'D9':'The abstract problem uses a set-valued map F with the domain and graph conventions from Section 2.4.'},kind='source_passage',symbols=[r'0\in F(x)'],shape='Abstract inclusion and fixed solution for the stochastic-approximation theorem. It is not restricted to the special A+subdifferential examples later in Section 4.1.')
add('D17','Smooth reduction',r'''
Suppose that there exists a $C^p$ manifold $\mathcal M\subset\mathbb R^d$ such that the following properties are true.

(C1) The map $F_{\mathcal M}:\mathcal M\to\mathbb R^d$ defined by
\[
F_{\mathcal M}(x):=P_{T_{\mathcal M}(x)}F(x)
\]
is single-valued on some neighborhood of $\bar x$ in $\mathcal M$.

(C2) There exists a neighborhood $U$ of $(\bar x,0)$ such that
\[
U\cap\operatorname{gph}F=U\cap\operatorname{gph}(F_{\mathcal M}+N_{\mathcal M}).
\]
''',[14],'Assumption C (Smooth reduction)',{'D16':'The reduced map and graph equality refer to the abstract inclusion F.','D1':'The manifold supplies tangent and normal spaces.','D2':'The reduction projects F(x) onto the tangent space.'},kind='assumption',context='Assumption C (Smooth reduction).',symbols=[r'F_{\mathcal M}(x):=P_{T_{\mathcal M}(x)}F(x)',r'F_{\mathcal M}+N_{\mathcal M}'],shape='Single-valued tangent reduction with local graph equality. The preceding prose calls the reduction C1-smooth; the listed clauses do not explicitly require Cp smoothness of F_M. Preserve that regularity gap rather than inserting a missing condition. No active-manifold sharpness assumption is part of C.')
add('D18','generalized gradient mapping',r'''
The stochastic approximation algorithms we consider assume access to a generalized gradient mapping:
\[
G:\mathbb R_{++}\times\mathbb R^d\times\mathbb R^d\to\mathbb R^d.
\]
Given $x_0\in\mathbb R^d$, the algorithm iterates the update
\[
x_{k+1}=x_k-\alpha_kG_{\alpha_k}(x_k,\nu_k),\tag{4.2}
\]
where $\alpha_k>0$ is a control sequence and $\nu_k$ is stochastic noise. We will place relevant assumptions on the noise $\nu_k$ later in Section 6.
''',[15],'Generalized gradient mapping and iteration (4.2)',kind='source_passage',symbols=[r'G_{\alpha_k}(x_k,\nu_k)',r'x_{k+1}=x_k-\alpha_kG_{\alpha_k}(x_k,\nu_k)'],shape='Abstract stochastic update with arbitrary supplied mapping G. The printed forward reference to Section 6 is retained although the noise assumptions are in Section 5. This need not be a forward-backward or subgradient method.')
add('D19','Steplength',r'''
We suppose that there exists a constant $C>0$ and a neighborhood $\mathcal U$ of $\bar x$ such that the estimate
\[
\sup_{x\in \mathcal U_F}\|G_\alpha(x,\nu)\|\le C(1+\|\nu\|),
\]
holds for all $\nu\in\mathbb R^d$ and $\alpha>0$, where we set $\mathcal U_F:=\mathcal U\cap\operatorname{dom}F$.
''',[15],'Assumption D (Steplength)',{'D18':'The bound is on the generalized update mapping G at arbitrary positive step size.','D16':'The local domain \mathcal U_F uses the abstract inclusion domain.'},kind='assumption',context='Assumption D (Steplength).',symbols=[r'\sup_{x\in \mathcal U_F}\|G_\alpha(x,\nu)\|'],shape='Uniform local bound, linear in noise magnitude, for every alpha>0. It is not merely a Lipschitz condition in x or a bound at the realized noise.')
add('D20','Strong (a) and aiming',r'''
We suppose that there exist constants $C,\mu>0$ and a neighborhood $\mathcal U$ of $\bar x$ such that the following hold for all $\nu\in\mathbb R^d$ and $\alpha>0$, where we set $\mathcal U_F:=\mathcal U\cap\operatorname{dom}F$.

(E1) (Tangent comparison) For all $x\in \mathcal U_F$, we have
\[
\|P_{T_{\mathcal M}(P_{\mathcal M}(x))}(G_\alpha(x,\nu)-F(P_{\mathcal M}(x))-\nu)\|\le C(1+\|\nu\|)^2(\operatorname{dist}(x,\mathcal M)+\alpha).
\]

(E2) (Proximal Aiming) For $x\in \mathcal U_F$, we have
\[
\langle G_\alpha(x,\nu)-\nu,x-P_{\mathcal M}(x)\rangle\ge\mu\cdot\operatorname{dist}(x,\mathcal M)-(1+\|\nu\|)^2(o(\operatorname{dist}(x,\mathcal M))+C\alpha).
\]
''',[15],'Assumption E (Strong (a) and aiming)',{'D18':'Both estimates compare the generalized update direction G_alpha with the noise.','D17':'Tangent comparison uses the projected F at the manifold point; C1 makes that projected value single-valued.','D2':'Both estimates use the nearest manifold point and its distance.'},kind='assumption',context='Assumption E (Strong (a) and aiming).',symbols=[r'G_\alpha(x,\nu)-F(P_{\mathcal M}(x))-\nu',r'x-P_{\mathcal M}(x)'],shape='Two original estimates, tangent comparison and inward aiming, with a squared noise factor and little-o remainder. F(P_M(x)) is set-valued before tangent projection; retain the printed expression and interpret its unique projected value using Assumption C, not a fabricated norm of an arbitrary set.')
add('D21','Standing assumptions',r'''
Assume the following.

(J1) The map $G$ is measurable.

(J2) There exist constants $c_1,c_2>0$ and $\gamma\in(1/2,1]$ such that
\[
\frac{c_1}{k^\gamma}\le\alpha_k\le\frac{c_2}{k^\gamma}.
\]

(J3) $\{\nu_k\}$ is a martingale difference sequence w.r.t. to the increasing sequence of $\sigma$-fields
\[
\mathcal F_k=\sigma(x_j:j\le k\text{ and }\nu_j:j<k),
\]
and there exists a function $q:\mathbb R^d\to\mathbb R_+$ that is bounded on bounded sets with
\[
\mathbb E[\nu_k\mid\mathcal F_k]=0\qquad\text{and}\qquad\mathbb E[\|\nu_k\|^4\mid\mathcal F_k]<q(x_k).
\]
We let $\mathbb E_k[\cdot]=\mathbb E[\cdot\mid\mathcal F_k]$ denote the conditional expectation.

(J4) The inclusion $x_k\in\operatorname{dom}F$ holds for all $k\ge1$.
''',[19],'Assumption I (Standing assumptions)',{'D18':'Measurability, step sizes and filtration refer to the generalized stochastic iteration.','D16':'The iterates remain in the domain of the abstract inclusion map.'},kind='assumption',context='Assumption I (Standing assumptions).',symbols=[r'\frac{c_1}{k^\gamma}\le\alpha_k\le\frac{c_2}{k^\gamma}',r'\mathbb E[\|\nu_k\|^4\mid\mathcal F_k]<q(x_k)'],shape='Measurable update, two-sided power step bounds, martingale-difference noise with a strict conditional fourth-moment bound, and domain membership. Original sublabels J1-J4 are retained under Assumption I. Theorem 5.1 narrows gamma to (1/2,1).')
add('D22','decomposable structure',r'''
Fix a point $\bar x\in\operatorname{dom}F$ at which Assumption C holds and let $U$ be a matrix whose column vectors form an orthogonal basis of $T_{\mathcal M}(\bar x)$. We suppose the noise sequence has decomposable structure $\nu_k=\nu_k^{(1)}+\nu_k^{(2)}(x_k)$, where $\nu_k^{(2)}:\operatorname{dom}F\to\mathbb R^d$ is a random function satisfying
\[
\mathbb E_k[\|U^\top\nu_k^{(2)}(x)\|^2]\le C\|x-\bar x\|^2\qquad\text{for all }x\in\operatorname{dom}F\text{ near }\bar x,
\]
and some $C>0$. In addition, we suppose that for all $x\in\operatorname{dom}F$, we have $\mathbb E_k[\nu_k^{(1)}]=\mathbb E_k[\nu_k^{(2)}(x)]=0$ and the following limit holds:
\[
\frac1{\sqrt k}\sum_{i=1}^k U^\top\nu_i^{(1)}\xrightarrow D N(0,\Sigma).
\]
for some symmetric positive semidefinite matrix $\Sigma$.
''',[20],'Assumption J',{'D21':'Conditional expectations E_k use the filtration and noise convention from Assumption I.','D17':'The basepoint and tangent space belong to the reduction in Assumption C.'},kind='assumption',symbols=[r'\nu_k=\nu_k^{(1)}+\nu_k^{(2)}(x_k)',r'U^\top\nu_i^{(1)}'],shape='Noise split with a tangent-projected mean-square remainder and a CLT in tangent coordinates. The source says orthogonal basis, not orthonormal. Sigma therefore has tangent-coordinate dimension, whereas Theorem 5.1 multiplies it directly by ambient Jacobians; preserve the discrepancy.')

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edges=edges),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
