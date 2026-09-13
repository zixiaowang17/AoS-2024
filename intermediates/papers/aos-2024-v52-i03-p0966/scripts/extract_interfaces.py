"""Transcribe transport prerequisites from the main text only; extraction remains in progress."""
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
add('D1','compact, convex set',r'''$\Omega$ is a compact, convex set with nonempty interior such that $\Omega\subseteq[0,1]^d$.''',[8],'Condition (S1)',kind='condition',phrases=['compact, convex set','Condition (S1)'],shape='Standing compact convex Euclidean support with nonempty interior, contained in the unit cube. Applies except where the source explicitly replaces the domain by the torus or by condition C1.')
add('D2','Borel probability measures',r'''Let $\mathcal P(\Omega)$ denote the set of Borel probability measures with support contained in $\Omega$, and $\mathcal P_{\mathrm{ac}}(\Omega)$ the subset of such measures which are absolutely continuous with respect to the Lebesgue measure on $\mathbb R^d$.''',[8],'Section 2.1 — probability measures on a Euclidean support',symbols=[r'\mathcal P(\Omega)',r'\mathcal P_{\mathrm{ac}}(\Omega)'],shape='Borel probability measures supported in a Euclidean set and their Lebesgue-absolutely-continuous subclass. The separate geometric condition S1 is not intrinsic to the definition.')
add('D3',['optimal transport map','Monge problem'],r'''
Given two distributions $P$ and $Q$ with support contained in a set $\Omega\subseteq\mathbb R^d$, an optimal transport map $T_0$ from $P$ to $Q$ is any solution to the Monge problem (Monge, 1781),
\[
\operatorname*{argmin}_{T\in\mathcal T(P,Q)}\int_\Omega\|x-T(x)\|^2\,dP(x),\tag{1}
\]
where $\mathcal T(P,Q)$ is the set of transport maps between $P$ and $Q$, that is, the set of Borel-measurable functions $T:\Omega\to\Omega$ such that $T_{\#}P:=P(T^{-1}(\cdot))=Q$. Equivalently, we write $T_{\#}P=Q$ whenever $X\sim P$ implies $T(X)\sim Q$.
''',[3],'Section 1 — Monge problem (1)',{'D2':'P and Q are probability measures on the common Euclidean support.'},symbols=[r'\mathcal T(P,Q)',r'T_{\#}P',r'T_0'],shape='Squared-Euclidean-cost minimizers among measurable pushforward maps. This definition does not assert existence or uniqueness and does not require smoothness.')
add('D4','couplings',r'''where $\Pi(P,Q)$ denotes the set of joint distributions on $\Omega^2$ with marginal distributions $P$ and $Q$, known as couplings of $P$ and $Q$.''',[8],'Section 2.1 — couplings after (9)',{'D2':'The two marginals are Borel probability measures on the support.'},symbols=[r'\Pi(P,Q)'],shape='Joint probability distributions with fixed marginals. No map-supported or optimality restriction is imposed.')
add('D5','2-Wasserstein distance',r'''
Specifically, it gives rise to the 2-Wasserstein distance,
\[
W_2(P,Q)=\left(\inf_{\pi\in\Pi(P,Q)}\int\|x-y\|^2\,d\pi(x,y)\right)^{\frac12}.\tag{10}
\]
''',[8],'Section 2.1 — Wasserstein distance (10)',{'D4':'The infimum ranges over couplings with the specified marginals.'},symbols=[r'W_2(P,Q)'],shape='Square root of the optimal squared Euclidean transport cost. The torus uses a separately recorded metric cost; neither definition is replaced by the other.')
add('D6',['Kantorovich dual problem','Kantorovich potentials'],r'''
The above problem is an (infinite-dimensional) convex program with linear constraints, and it admits a dual maximization problem, known as the Kantorovich dual problem, given by
\[
W_2^2(P,Q)=\sup_{(\phi,\psi)\in\mathcal K}\int\phi\,dP+\int\psi\,dQ,\tag{11}
\]
where $\mathcal K$ is the set of pairs $(\phi,\psi)\in L^1(\Omega)\times L^1(\Omega)$ such that $\phi(x)+\psi(y)\le\|x-y\|^2$ for all $x,y\in\Omega$. In the present setting of the quadratic optimal transport problem over the compact set $\Omega$, it can be shown that strong duality indeed holds in equation (11), and that the supremum is always achieved by some pair $(\phi_0,\psi_0)\in\mathcal K$. Any such pair of functions is called a pair of Kantorovich potentials.
''',[8],'Section 2.1 — dual problem and potentials (11)',{'D5':'The dual optimizes the squared Wasserstein cost defined in (10).'},symbols=[r'\mathcal K',r'\phi_0',r'\psi_0'],shape='Original Euclidean dual feasibility and maximizing pair. Preserve the printed L1(Omega) convention rather than silently replacing it by L1(P) times L1(Q).')
add('D7','Legendre-Fenchel conjugate',r'''
where for any $f:\Omega\to\mathbb R$,
\[
f^*(y)=\sup_{x\in\Omega}\{\langle x,y\rangle-f(x)\},\qquad y\in\Omega,
\]
denotes the Legendre-Fenchel conjugate of $f$.
''',[9],'Section 2.1 — Legendre-Fenchel conjugate',symbols=[r'f^*(y)',r'\varphi_0^*'],shape='Source conjugation convention with the supremum over Omega and displayed evaluation y in Omega. Later global convex lifts are not silently identified with a different conjugation domain.')
add('D8','semi-dual problem',r'''
Under this reparametrization, the Kantorovich dual problem is equivalent to the so-called semi-dual problem
\[
\inf_{\varphi\in L^1(P)}\int\varphi\,dP+\int\varphi^*\,dQ,\tag{12}
\]
in the sense that $\varphi_0$ solves to the semi-dual problem if and only if $(\|\cdot\|^2-2\varphi_0,\|\cdot\|^2-2\varphi_0^*)$ solves the Kantorovich problem (11).
''',[9],'Section 2.1 — semi-dual problem (12)',{'D6':'The displayed equivalence identifies the associated pair solving the dual problem (11).','D7':'The objective and equivalence use Legendre-Fenchel conjugation.'},symbols=[r'\varphi^*',r'\varphi_0'],shape='Integral minimization over a potential with its conjugate, and the original relation to the Kantorovich pair. Preserve the source phrase solves to.')
add('D9','Brenier potential',r'''Let $p$ and $q$ denote their respective densities, and let $T_0=\nabla\varphi_0$ denote the unique optimal transport map from $P$ to $Q$, with respect to a convex Brenier potential $\varphi_0$.''',[11],'Section 3 — population map and Brenier potential',{'D3':'The population map is the Euclidean Monge optimizer.'},symbols=[r'T_0=\nabla\varphi_0',r'\varphi_0'],shape='Convex potential whose gradient is the population optimal map. No C2 regularity or curvature condition is included in this identity; such conditions are stated separately.')
add('D10','Kantorovich potentials',r'''We also denote by $\phi_0=\|\cdot\|^2-2\varphi_0$ and $\psi_0=\|\cdot\|^2-2\varphi_0^*$ the Kantorovich potentials induced by $\varphi_0$.''',[11],'Section 3 — potentials induced by the Brenier potential',{'D9':'Both potentials are induced by the population Brenier potential.','D7':'The target potential uses the conjugate of the Brenier potential.','D6':'The resulting pair is identified as a pair of Kantorovich dual maximizers.'},symbols=[r'\phi_0=\|\cdot\|^2-2\varphi_0',r'\psi_0=\|\cdot\|^2-2\varphi_0^*'],shape='Specific source and target dual potentials induced by a convex potential. Straight phi and curly varphi designate different mathematical functions.')
add('D11','Hölder spaces',r'''Given a set $\Omega$, which is either a closed subset of $\mathbb R^d$ or the $d$-dimensional flat torus $\Omega=\mathbb T^d:=\mathbb R^d/\mathbb Z^d$, and given real numbers $\alpha>0$, $s\in\mathbb R\setminus\{0\}$, $1\le p,q\le\infty$, the Hölder spaces $\mathcal C^\alpha(\Omega)$, Besov spaces $\mathcal B^s_{p,q}(\Omega)$, homogeneous Sobolev spaces $\dot H^s(\Omega)$, inhomogeneous Sobolev spaces $H^s(\Omega)$, and their respective norms $\|\cdot\|_{\mathcal C^\alpha(\Omega)}$, $\|\cdot\|_{\mathcal B^s_{p,q}(\Omega)}$, $\|\cdot\|_{\dot H^s(\Omega)}$, $\|\cdot\|_{H^s(\Omega)}$, are defined in Appendix A. We drop the suffix $\Omega$ when the underlying space can be understood from context.''',[7],'Notation — named smoothness spaces',kind='source_passage',symbols=[r'\mathcal C^\alpha(\Omega)'],phrases=['Hölder spaces'],shape='Main-text declaration of Hölder notation, within the original sentence listing smoothness spaces. Precise norms and integer-index conventions are deferred to excluded Appendix A; no definition is invented. The Besov and Sobolev names in this sentence do not create theorem dependencies merely by co-occurrence.')
add('D12','Hölder balls',r'''
We also define, for any $M,\gamma>0$,
\[
\mathcal C^\alpha(\Omega;M):=\{f\in\mathcal C^\alpha(\Omega):\|f\|_{\mathcal C^\alpha(\Omega)}\le M\},\tag{7}
\]
''',[7],'Notation — Hölder ball (7)',{'D11':'The norm bound uses the declared Hölder space and norm.'},symbols=[r'\mathcal C^\alpha(\Omega;M)'],context=r'Recall that the Hölder balls $\mathcal C^\alpha(\Omega;\cdot)$ and $\mathcal C^\alpha(\Omega;\cdot,\cdot)$ are defined in equations (7)–(8).',shape='Hölder norm ball without a positivity restriction. Its natural-language name is explicitly supplied before Theorem 10.')
members['D12']['naming_context'][0]['evidence']=[dict(page=16,location='Before Theorem 10 — Hölder balls')]
add('D13','Hölder balls',r'''
\[
\mathcal C^\alpha(\Omega;M,\gamma):=\{f\in\mathcal C^\alpha(\Omega):\|f\|_{\mathcal C^\alpha(\Omega)}\le M,f\ge1/\gamma\text{ over }\Omega\}.\tag{8}
\]
''',[7],'Notation — positive Hölder ball (8)',{'D11':'Membership and the upper norm bound use the same declared Hölder space.'},symbols=[r'\mathcal C^\alpha(\Omega;M,\gamma)'],context=r'Recall that the Hölder balls $\mathcal C^\alpha(\Omega;\cdot)$ and $\mathcal C^\alpha(\Omega;\cdot,\cdot)$ are defined in equations (7)–(8).',shape='Hölder norm and pointwise lower-bound constraints; the displayed set does not require integral one. Density normalization is supplied separately when a theorem calls its members densities. Distinct from (7).')
members['D13']['naming_context'][0]['evidence']=[dict(page=16,location='Before Theorem 10 — Hölder balls')]
add('D14','torus',r'''
Denote by $\mathbb T^d=\mathbb R^d/\mathbb Z^d$ the flat $d$-dimensional torus. Specifically, $\mathbb T^d$ is the set of equivalence classes $[x]=\{x+k:k\in\mathbb Z^d\}$, for all $x\in[0,1)^d$. Abusing notation, we typically write $x$ instead of $[x]$. $\mathbb T^d$ is endowed with the standard metric
\[
d_{\mathbb T^d}(x,y)=\min\{\|x-y+k\|:k\in\mathbb Z^d\},\qquad x,y\in\mathbb T^d.
\]
''',[10],'Section 2.2 — flat torus and metric',symbols=[r'\mathbb T^d',r'd_{\mathbb T^d}(x,y)'],shape='Euclidean space modulo the integer lattice, with the shortest periodic Euclidean displacement metric. This metric differs from using a fixed representative difference.')
add('D15','Borel measures',r'''We identify $\mathcal P(\mathbb T^d)$ with the set of Borel measures $P$ on $\mathbb R^d$ such that $P([0,1)^d)=1$ and which are $\mathbb Z^d$-periodic, in the sense that $P(B)=P(k+B)$ for all $k\in\mathbb Z^d$ and all Borel sets $B\subseteq\mathbb R^d$. Furthermore, $\mathcal P_{\mathrm{ac}}(\mathbb T^d)$ denotes the subset of measures in $\mathcal P(\mathbb T^d)$ which are absolutely continuous with respect to the Lebesgue measure on $\mathbb R^d$.''',[10],'Section 2.2 — periodic representation of torus measures',{'D14':'Periodicity and the unit-cell representation use the flat torus.'},symbols=[r'\mathcal P(\mathbb T^d)',r'\mathcal P_{\mathrm{ac}}(\mathbb T^d)'],shape='Probability on the quotient represented by an integer-periodic measure of unit mass per cell on Rd. The extension is not a probability measure of total mass one on Rd.')
add('D16','Monge problem',r'''
Define for all $P,Q\in\mathcal P_{\mathrm{ac}}(\mathbb T^d)$ the Monge problem
\[
\operatorname*{argmin}_{T\in\mathcal T(P,Q)}\int_{\mathbb T^d}d_{\mathbb T^d}^2(x,T(x))\,dP(x),\tag{14}
\]
where the integral is understood as being taken over $[0,1)^d$.
''',[10],'Section 2.2 — torus Monge problem (14)',{'D14':'The cost is the squared torus metric.','D15':'The integral over a fundamental cell uses the periodic representation of the measures.'},symbols=[r'd_{\mathbb T^d}^2(x,T(x))'],shape='Torus-cost optimal transport over measurable pushforward maps. The reused transport-map notation is interpreted on the quotient, not as the Euclidean cost from (1).')
add('D17','squared Wasserstein distance',r'''
The Kantorovich problem and its dual give rise to the squared Wasserstein distance over $\mathcal P(\mathbb T^d)$,
\[
W_2^2(P,Q)=\inf_{\pi\in\Pi(P,Q)}\int d_{\mathbb T^d}^2(x,y)\,d\pi(x,y)=\sup_{(\phi,\psi)\in\mathcal K_T}\int\phi\,dP+\int\psi\,dQ,\tag{15}
\]
where $\mathcal K_T$ denotes the set of pairs of potentials $(\varphi,\psi)\in L^1(P)\times L^1(Q)$ satisfying the dual constraint $\varphi(x)+\psi(y)\le d_{\mathbb T^d}^2(x,y)$ for all $x,y\in\mathbb T^d$.
''',[10],'Section 2.2 — torus Wasserstein distance and dual (15)',{'D14':'The primal and dual constraints use the periodic cost.','D15':'Marginals and potential integrability refer to torus probability measures.'},symbols=[r'\mathcal K_T',r'W_2^2(P,Q)'],shape='Torus transport cost and dual problem. Couplings have prescribed torus marginals as ambient notation. Preserve the source change from straight phi in the supremum to curly varphi in the following feasibility clause.')
add('D18','optimal transport map',r'''We now denote by $T_0$ the optimal transport map from $P$ to $Q$, with respect to the cost $d_{\mathbb T^d}^2$. As outlined in Proposition 4, $T_0$ is the gradient of a convex potential $\varphi_0:\mathbb R^d\to\mathbb R$, and is uniquely determined $P$-almost everywhere.''',[20],'Section 4.3 — torus population map and convex lift',{'D16':'The population map solves the torus Monge problem.'},symbols=[r'T_0',r'\varphi_0:\mathbb R^d\to\mathbb R'],shape='Convex potential on Rd inducing a torus optimal map; its lift is not itself a periodic scalar function. Proposition 4 supplies the original periodicity and conjugate conventions, retained as auxiliary source context.')
add('D19','Kantorovich potentials',r'''We continue to denote by $\phi_0=\|\cdot\|^2-2\varphi_0$ and $\psi_0=\|\cdot\|^2-2\varphi_0^*$ a corresponding pair of Kantorovich potentials.''',[20],'Section 4.3 — torus Kantorovich potentials',{'D18':'The torus potentials are induced by the convex lift.','D7':'The target-side expression uses the conjugate.','D17':'This pair solves the torus dual problem.'},symbols=[r'\phi_0=\|\cdot\|^2-2\varphi_0',r'\psi_0=\|\cdot\|^2-2\varphi_0^*'],shape='Periodic Kantorovich potentials induced by the convex transport lift. The quadratic subtraction makes these periodic, unlike the Brenier potential itself.')
add('D20','curvature condition',r'''The Brenier potential $\varphi_0$ is a convex function such that $\varphi_0\in\mathcal C^2(\Omega)$ and $(1/\lambda)I_d\preceq\nabla^2\varphi_0(x)\preceq\lambda I_d$ for all $x\in\Omega$.''',[12],'Condition A1(λ)',{'D9':'The Hessian bounds are imposed on the population Brenier potential.','D11':'The condition requires the declared C2 regularity.'},kind='condition',symbols=[r'\nabla^2\varphi_0(x)',r'A1(\lambda)'],context='The main technical result of this section will be stated under the following curvature condition.',shape='Both lower and upper uniform Hessian bounds on a C2 convex Brenier potential. This assumption is not inherited by arbitrary estimated maps or density estimators.')
add('D21','known distribution',r'''Throughout this section, we let $P\in\mathcal P_{\mathrm{ac}}(\Omega)$ denote a known distribution, and $Q\in\mathcal P_{\mathrm{ac}}(\Omega)$ denote an unknown distribution from which an i.i.d. sample $Y_1,\ldots,Y_n\sim Q$ is observed.''',[11],'Section 3 — one-sample observation model',{'D2':'Both population measures have Lebesgue densities.'},kind='source_passage',symbols=[r'Y_1,\ldots,Y_n\sim Q'],shape='One known source measure and iid observations from the unknown target measure. This statistical experiment belongs to the estimation theorems, not the deterministic stability theorem.')
add('D22','empirical measure',r'''Recall that we denote by $Q_n=(1/n)\sum_{i=1}^n\delta_{Y_i}$ the empirical measure.''',[13],'Section 3.2 — empirical measure',symbols=[r'Q_n=(1/n)\sum_{i=1}^n\delta_{Y_i}'],shape='Average of point masses at observations. The same construction is used for P_n with X observations. The definition alone imposes no independence assumption.')
add('D23','Daubechies wavelet system',r'''
To define a basis over the unit cube $\Omega$, we focus on the boundary-corrected $N$-th Daubechies wavelet system, for an integer $N\ge2$, as introduced by Cohen, Daubechies and Vial (1993). In short, given an integer $j_0\ge\log_2N$, their construction leads to respective families of scaling and wavelet functions
\[
\Phi^{\mathrm{bc}}=\{\zeta_{j_0k}^{\mathrm{bc}}:0\le k\le2^{j_0}-1\},\qquad\Psi_j^{\mathrm{bc}}=\{\xi_{jk\ell}^{\mathrm{bc}}:0\le k\le2^{j_0}-1,\ell\in\{0,1\}^d\setminus\{0\}\},\qquad j\ge j_0,
\]
such that $\Psi^{\mathrm{bc}}=\Phi^{\mathrm{bc}}\cup\bigcup_{j=j_0}^\infty\Psi_j^{\mathrm{bc}}$ forms an orthonormal basis of $L^2(\Omega)$, with the property that $\Phi^{\mathrm{bc}}$ spans all polynomials of degree at most $N-1$ over $\Omega$.
''',[15],'Section 3.3 — boundary-corrected wavelet basis',symbols=[r'\Psi^{\mathrm{bc}}',r'\Phi^{\mathrm{bc}}'],shape='Original main-text description of the wavelet system. The detailed construction is deferred to Appendix A. Preserve the printed j0-based upper index at every j; no corrected tensor-index definition or unstated relation between N and alpha is inserted.')
add('D24','truncated wavelet estimator',r'''
The standard truncated wavelet estimator of $q$ (Kerkyacharian and Picard, 1992) with a truncation level $J_n\ge j_0>0$ is then given by
\[
\widetilde q_n^{(\mathrm{bc})}=\sum_{\xi\in\Psi^{\mathrm{bc}}}\widehat\beta_\xi\xi=\sum_{\zeta\in\Phi^{\mathrm{bc}}}\widehat\beta_\zeta\zeta+\sum_{j=j_0}^{J_n}\sum_{\xi\in\Psi_j^{\mathrm{bc}}}\widehat\beta_\xi\xi,\qquad\text{where }\widehat\beta_\xi=\int\xi\,dQ_n,\ \xi\in\Psi^{\mathrm{bc}}.
\]
Notice that $\widetilde q_n^{(\mathrm{bc})}$ is permitted to take on negative values, in which case it does not define a probability density. We instead define the final density estimator $\widehat q_n\equiv\widehat q_n^{(\mathrm{bc})}$ by
\[
\widehat q_n^{(\mathrm{bc})}=\frac{\widetilde q_n^{(\mathrm{bc})}I(\widetilde q_n^{(\mathrm{bc})}\ge0)}{\int\widetilde q_n^{(\mathrm{bc})}I(\widetilde q_n^{(\mathrm{bc})}\ge0)},\qquad\text{over }\Omega,\tag{27}
\]
and we denote by $\widehat Q_n^{(\mathrm{bc})}$ the distribution induced by $\widehat q_n^{(\mathrm{bc})}$. We drop all superscripts “bc” in the sequel whenever the choice of wavelet system is unambiguous.
''',[15],'Section 3.3 — wavelet density estimator (27)',{'D23':'The coefficient sums use the boundary-corrected scaling and wavelet families.','D22':'Empirical coefficients integrate basis functions against the empirical measure.'},symbols=[r'\widehat q_n^{(\mathrm{bc})}',r'\widehat Q_n^{(\mathrm{bc})}'],shape='Empirical truncated series, positive-part normalization and induced measure. The first sum is printed over the entire basis while the following equality truncates levels; preserve this inconsistency rather than silently fixing the first index set.')
add('D25','One-Sample Wavelet Estimators',r'''
Specifically, define
\[
\widehat T_n=\operatorname*{argmin}_{T\in\mathcal T(P,\widehat Q_n)}\int\|x-T(x)\|^2\,dP(x).\tag{26}
\]
''',[15],'Section 3.3 — one-sample plugin transport map (26)',{'D3':'The construction solves the Euclidean Monge problem with estimated target.','D24':'In Theorem 10 the estimated target is the normalized boundary-corrected wavelet measure.'},context='Theorem 10 (One-Sample Wavelet Estimators).',symbols=[r'\widehat T_n'],shape='One-sample transport map to the estimated target measure. Equation (26) permits a general density estimator; the use in Theorem 10 is the explicit wavelet specialization identified in its preamble.')
members['D25']['naming_context'][0]['evidence']=[dict(page=16,location='Before Theorem 10 — wavelet specialization of (26)')]
add('D26','i.i.d. samples',r'''Furthermore, in what follows, $X_1,\ldots,X_n\sim P$ and $Y_1,\ldots,Y_m\sim Q$ denote i.i.d. samples which are independent of each other,''',[25],'Section 5.1 — independent samples',kind='source_passage',symbols=[r'X_1,\ldots,X_n\sim P',r'Y_1,\ldots,Y_m\sim Q'],shape='Two iid samples with cross-sample independence. The same convention is explicitly stated for the torus in Section 4.3; the smooth-domain paragraph states iid observations but does not repeat cross-sample independence.')
members['D26']['application_context']=[dict(text=r'Let $X_1,\ldots,X_n\sim P$ and $Y_1,\ldots,Y_m\sim Q$ denote i.i.d. samples, which are independent of each other,',evidence=[dict(page=20,location='Section 4.3 — independent torus samples')])]
add('D27','kernel density estimators',r'''
Given a kernel $K\in\mathcal C_c^\infty(\mathbb R^d)$ and a bandwidth $h_n>0$, write $K_{h_n}=h_n^{-d}K(\cdot/h_n)$, and define the kernel density estimators of $p$ and $q$ by
\[
\widetilde p_n^{(\mathrm{ker})}=P_n\star K_{h_n}=\int_{\mathbb R^d}K_{h_n}(\cdot-z)\,dP_n(z),\qquad\widetilde q_m^{(\mathrm{ker})}=Q_m\star K_{h_m}=\int_{\mathbb R^d}K_{h_m}(\cdot-z)\,dQ_m(z).
\]
Recall that integration over $\mathbb R^d$ with respect to a measure in $\mathcal P(\mathbb T^d)$ is understood as integration with respect to this measure extended to $\mathbb R^d$ via translation by $\mathbb Z^d$-periodicity. The above estimators may take on negative values, thus we again define the final density estimators by
\[
\widehat p_n^{(\mathrm{ker})}\propto\widetilde p_n^{(\mathrm{ker})}I(\widetilde p_n^{(\mathrm{ker})}\ge0),\qquad\widehat q_m^{(\mathrm{ker})}\propto\widetilde q_m^{(\mathrm{ker})}I(\widetilde q_m^{(\mathrm{ker})}\ge0),
\]
where the proportionality constants are to be chosen such that $\widehat p_n^{(\mathrm{ker})}$ and $\widehat q_m^{(\mathrm{ker})}$ are densities. We also denote their induced probability distributions by $\widehat P_n^{(\mathrm{ker})}$ and $\widehat Q_m^{(\mathrm{ker})}$.
''',[21],'Section 4.3 — periodic kernel density estimators',{'D15':'Convolution integrates the periodic extension of each torus measure.','D22':'The input measures are empirical measures of the observations.'},symbols=[r'\widehat p_n^{(\mathrm{ker})}',r'\widehat P_n^{(\mathrm{ker})}',r'\widehat Q_m^{(\mathrm{ker})}'],shape='Periodic empirical kernel convolution followed by clipping and normalization, with separately indexed sample bandwidths. The Fourier-order assumption K1 is a separate hypothesis, not part of this construction.')
add('D28','even kernel',r'''
$K\in\mathcal C_c^\infty(\mathbb R^d)$ is an even kernel, whose Fourier transform $\mathcal F[K]$ satisfies
\[
\sup_{x\in\mathbb R^d\setminus\{0\}}|\mathcal F[K](x)-1|\|x\|^{-\zeta}\le\kappa.\tag{34}
\]
''',[21],'Condition K1(ζ,κ)',kind='condition',symbols=[r'\mathcal F[K]',r'K1(2\alpha,\kappa)'],phrases=['even kernel'],shape='Smooth compactly supported even kernel with a uniform Fourier approximation bound of order zeta. Theorems instantiate zeta=2alpha. No positivity condition is added to K.')
add('D29','optimal transport map',r'''Furthermore, $\widehat T_{nm}^{(\mathrm{ker})}$ denotes the optimal transport map between these measures.''',[21],'Section 4.3 — transport map between kernel estimates',{'D27':'The preceding measures are the normalized kernel density estimates.','D16':'Optimality uses the torus Monge problem.'},symbols=[r'\widehat T_{nm}^{(\mathrm{ker})}'],shape='Torus optimal map from the estimated source measure to the estimated target measure. The population L2(P) risk uses chosen convex-gradient lifts as described around (33).')
add('D30','compact, convex subset',r'''$\Omega$ is a known compact, convex subset of $\mathbb R^d$, such that $\partial\Omega$ is $\mathcal C^\infty$ and $\mathcal L(\Omega)=1$.''',[23],'Condition (C1)',kind='condition',phrases=['Condition (C1)','compact, convex subset'],symbols=[r'\mathcal L(\Omega)=1'],shape='Known smooth compact convex Euclidean domain of unit Lebesgue volume. This replaces the unit-cube containment in S1 for Section 4.4; imposing both would wrongly collapse the general-domain setting.')
add('D31','mean-zero Brenier potential',r'''There exists $\epsilon_0>0$ such that for any $M,\gamma>0$ and $\epsilon\in(0,\epsilon_0)$, there exists a constant $C>0$ depending only on $\Omega,M,\gamma,\epsilon$ such that for any densities $\widehat p,\widehat q\in\mathcal C^\epsilon(\Omega;M,\gamma)$, the unique mean-zero Brenier potential $\widehat\varphi$ whose gradient pushes forward $\widehat p$ onto $\widehat q$ satisfies $\|\widehat\varphi\|_{\mathcal C^2(\Omega)}\le C$.''',[23],'Condition (C2)',{'D13':'The uniform condition ranges over densities in the positive Hölder ball.','D3':'Brenier potentials here induce Euclidean optimal transport maps.'},kind='condition',phrases=['Condition (C2)','mean-zero Brenier potential'],symbols=[r'\|\widehat\varphi\|_{\mathcal C^2(\Omega)}'],shape='Uniform C2 bound for mean-zero convex transport potentials, quantified over every admissible density pair and small positive smoothness exponent. This is assumed for generic domains, not asserted as a proved consequence of C1.')
add('D32','Neumann Laplacian',r'''
In order to develop a minimax optimal estimator for densities supported on $\Omega$, we will impose Neumann boundary conditions on the densities, and we will introduce an orthonormal basis of $L^2(\Omega)$ generated by the eigenfunctions of the Neumann Laplacian. To elaborate, define $H_N^2(\Omega)$ to be the set of functions $u\in H^2(\Omega)\cap L_0^2(\Omega)$ satisfying
\[
\frac{\partial u}{\partial\nu}=0,\qquad\text{over }\partial\Omega,
\]
where $\nu$ is an outward-pointing normal vector to $\partial\Omega$, and the normal derivative is to be understood in the weak sense. Under condition (C1), it is a standard fact that the negative Laplace operator $-\Delta$ is a self-adjoint bijection of $H_N^2(\Omega)$ onto $L_0^2(\Omega)$, which admits a real and discrete spectrum $0<\lambda_1\le\lambda_2\le\ldots$, with corresponding eigenfunctions $\{\eta_\ell\}_{\ell=1}^\infty\subseteq H_N^2(\Omega)$ (Dunlop et al., 2020; Evans, 2010). The latter form an orthonormal basis of $L_0^2(\Omega)$.
''',[23],'Section 4.4 — mean-zero Neumann eigenbasis',{'D30':'The spectral construction is stated under the smooth unit-volume domain condition.'},symbols=[r'H_N^2(\Omega)',r'\{\eta_\ell\}_{\ell=1}^\infty'],shape='Weak Neumann boundary condition on mean-zero functions and the positive spectrum of the negative Laplacian. The constant eigenfunction is excluded from this spectrum and is restored separately as 1 in the density expansion. The H2 norm definition remains appendix-only.')
add('D33','smooth approximation',r'''Let $\tau\in\mathcal C^\infty(\mathbb R_+)$ be a smooth approximation to the indicator function $I(\cdot<1)$. Specifically, assume that $\tau$ is a nonincreasing and smooth function such that $\tau(x)=1$ for all $x<1/2$, and $\tau(x)=0$ for all $x\ge1$.''',[24],'Section 4.4 — smooth spectral cutoff',kind='condition',symbols=[r'\tau(x)=1',r'\tau(x)=0'],shape='Fixed smooth nonincreasing cutoff equal to one below one-half and zero at and above one. Replacing it by a sharp indicator is explicitly outside the source analysis.')
add('D34','density estimators',r'''
Given an integer $L_n\ge1$, set
\[
\omega_\ell=\tau(\lambda_\ell/\lambda_{L_n}),\qquad\ell=1,2,\ldots,
\]
and define the density estimators
\[
\widetilde p_n^{(\mathrm{lap})}=1+\sum_{\ell=1}^{L_n}\omega_\ell\widehat\alpha_\ell\eta_\ell,\qquad\widetilde q_m^{(\mathrm{lap})}=1+\sum_{\ell=1}^{L_m}\omega_\ell\widehat\beta_\ell\eta_\ell,
\]
where $\widehat\alpha_\ell=\int\eta_\ell\,dP_n$, $\widehat\beta_\ell=\int\eta_\ell\,dQ_m$ for $\ell=1,2,\ldots$.
''',[24],'Section 4.4 — spectral density series',{'D32':'The series uses the mean-zero Neumann eigenfunctions and positive eigenvalues.','D33':'The weights apply the smooth spectral cutoff.','D22':'Coefficients are integrals against the empirical sample measures.'},symbols=[r'\widetilde p_n^{(\mathrm{lap})}',r'\widetilde q_m^{(\mathrm{lap})}'],shape='Smoothed spectral series with a constant-one component. Preserve the shared omega_l notation defined with L_n even in the target series truncated at L_m; the main text does not explicitly print separate target weights.')
add('D35','constrained Hölder spaces',r'''
In order to state convergence rates for these estimators, we will work over the constrained Hölder spaces
\[
\mathcal C_N^s(\Omega)=\left\{u\in\mathcal C^s(\Omega):\frac{\partial\Delta^ju}{\partial\nu}=0\text{ on }\partial\Omega,\ 0\le j\le\left\lfloor\frac{s-1}{2}\right\rfloor\right\},
\]
and the associated balls $\mathcal C_N^s(\Omega;M)=\mathcal C^s(\Omega;M)\cap\mathcal C_N^s(\Omega)$ and $\mathcal C_N^s(\Omega;M,\gamma)=\mathcal C^s(\Omega;M,\gamma)\cap\mathcal C_N^s(\Omega)$, for $M,\gamma,s>0$. Note that $\mathcal C^s(\Omega)=\mathcal C_N^s(\Omega)$ for $s<1$.
''',[24],'Section 4.4 — constrained Hölder spaces',{'D11':'The base regularity is the declared Hölder class.','D12':'One associated ball uses the norm-only bound.','D13':'The density ball also uses the pointwise lower bound.'},symbols=[r'\mathcal C_N^s(\Omega)',r'\mathcal C_N^{\alpha-1}(\Omega;M,\gamma)'],shape='Hölder functions whose iterated Laplacians have vanishing normal derivative up to the printed integer cutoff, with norm and positivity balls. The outward normal is defined on page 23; this does not impose zero mean on densities.')
add('D36','optimal transport map',r'''
As in previous sections, we define the final estimators to be the densities given by
\[
\widehat p_n^{(\mathrm{lap})}\propto\widetilde p_n^{(\mathrm{lap})}I(\widetilde p_n^{(\mathrm{lap})}\ge0),\qquad\widehat q_m^{(\mathrm{lap})}\propto\widetilde q_m^{(\mathrm{lap})}I(\widetilde q_m^{(\mathrm{lap})}\ge0),
\]
and we let $\widehat P_n^{(\mathrm{lap})}$ and $\widehat Q_m^{(\mathrm{lap})}$ be the induced distributions. Furthermore, let $\widehat T_{nm}^{(\mathrm{lap})}$ be the optimal transport map from $\widehat P_n^{(\mathrm{lap})}$ to $\widehat Q_m^{(\mathrm{lap})}$, and $\overline T_m^{(\mathrm{lap})}$ the optimal transport map from $P$ to $\widehat Q_m^{(\mathrm{lap})}$. We omit the superscripts “lap” for the remainder of this section.
''',[24],'Section 4.4 — normalized spectral estimates and transport maps',{'D34':'The density normalization uses the preceding spectral series.','D3':'Both maps solve the Euclidean Monge problem with the indicated source and target.'},symbols=[r'\widehat T_{nm}^{(\mathrm{lap})}',r'\overline T_m^{(\mathrm{lap})}',r'\overline T_m'],shape='Positive-part normalization, induced distributions and their one- and two-sample optimal maps. Barred T_m has the known population source; hatted T_nm has an estimated source.')
add('D37','central limit theorems',r'''
For the various estimators $\widehat P_n$ and $\widehat Q_m$ under consideration, we will derive central limit theorems of the form
\[
\sqrt n\left(W_2^2(\widehat P_n,Q)-W_2^2(P,Q)\right)\rightsquigarrow N(0,\sigma_0^2),\qquad\text{as }n\to\infty,\qquad\text{and}\tag{38}
\]
\[
\sqrt{\frac{nm}{n+m}}\left(W_2^2(\widehat P_n,\widehat Q_m)-W_2^2(P,Q)\right)\rightsquigarrow N(0,\sigma_\rho^2),\qquad\text{as }n,m\to\infty,\ \frac n{n+m}\to\rho,\tag{39}
\]
for some $\rho\in[0,1]$.
''',[26],'Section 5.1 — referenced limit statements (38)–(39)',{'D5':'For a Euclidean support the target is the squared cost (10).','D17':'On the torus the same notation uses the squared cost (15).','D10':'The Euclidean asymptotic variances use the corresponding induced potentials.','D19':'The torus asymptotic variances use the corresponding periodic potentials.'},kind='source_passage',symbols=[r'\sigma_\rho^2',r'\sqrt{\frac{nm}{n+m}}'],shape='The original population-centered Gaussian limits referenced by Theorem 22. Their variance mixture is archived separately. Endpoint sample-size ratios are allowed; nondegeneracy is not added as a hypothesis.')
add('D38','Wasserstein Distance',r'''
\[
\Phi_Q:\mathcal P(\Omega)\to\mathbb R,\qquad\Phi_Q(P)=W_2^2(P,Q),
\]
where $\Omega$ is either $\mathbb T^d$ or a subset of $\mathbb R^d$, and $Q\in\mathcal P_{\mathrm{ac}}(\Omega)$ is given.
''',[27],'Section 5.2 — fixed-target Wasserstein functional',{'D17':'Theorem 24 uses the torus instance of this functional, with cost (15).'},context='Efficiency Lower Bounds for Estimating the Wasserstein Distance.',symbols=[r'\Phi_Q(P)'],shape='Fixed-target squared transport cost as a functional of its source law. Theorem 24 instantiates only its torus branch; the unused Euclidean branch must not be counted as a needed definition there.')
add('D39','differentiable paths',r'''
Using a construction of van der Vaart (1998), we fix two differentiable paths $(P_{t,h_1})_{t\ge0}$ and $(Q_{t,h_2})_{t\ge0}$, for any $(h_1,h_2)\in\mathbb R^2$, with respective score functions $h_1\widetilde\Phi_{(P,Q)}$ and $h_2\widetilde\Psi_{(P,Q)}$, where $\widetilde\Psi_{(P,Q)}(y):=\psi_0(y)-\int\psi_0\,dQ$. These paths are defined in equations (115–116) of Appendix L, and we use them to obtain the following asymptotic minimax lower bound.
''',[28],'Section 5.2 — paths used in Theorem 24',{'D19':'The target-side score is the centered torus Kantorovich potential; the source-side score is similarly identified in Lemma 23.'},kind='source_passage',symbols=[r'P_{t,h_1}',r'Q_{t,h_2}',r'\widetilde\Psi_{(P,Q)}'],shape='Main-text identification of differentiable paths by their scores and an explicit appendix reference. Their actual densities and construction are unresolved because Appendix L is excluded; arbitrary paths with those scores are not substituted.')

add('D40','i.i.d. observations',r'''Let the distributions $P,Q\in\mathcal P_{\mathrm{ac}}(\Omega)$ admit densities $p,q\in L^2(\Omega)$, and let $X_1,\ldots,X_n\sim P$ and $Y_1,\ldots,Y_m\sim Q$ be i.i.d. observations.''',[23],'Section 4.4 — smooth-domain sampling model',{'D2':'Both laws have Lebesgue densities on the Euclidean support.'},kind='source_passage',symbols=[r'X_1,\ldots,X_n\sim P',r'Y_1,\ldots,Y_m\sim Q'],shape='The original smooth-domain sampling statement. It states iid observations but does not repeat the explicit cross-sample independence sentence used for the torus. No torus-domain restriction is inherited.')

# The source gives a general construction, instantiated by these local theorem uses.
members['D25']['relation']='specialization'
members['D38']['relation']='specialization'
def main():
    target=ROOT/'interface-extraction.json'
    target.write_text(json.dumps(dict(paper_id=PID,status='source_review_pending',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source passages for interface review; census remains incomplete.')

if __name__ == "__main__":
    main()
