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
add('D1','locally stationary function-valued process',r'''
Let $\{X_{t,T}\mid t=1,\ldots,T;T\in\mathbb N\}$ be a sequence of $V$-valued stochastic processes indexed by $T\in\mathbb N$, and let $\{X_t^{(u)}\mid t\in\mathbb Z;u\in[0,1]\}$ be a $V$-valued stationary stochastic process such that, for some $p>0$ and constants $C_p>0$, $\zeta>0$,
\[
\|X_{t,T}-X_t^{(t/T)}\|_{V,p}\leq C_pT^{-\zeta}\quad\text{and}\quad\|X_t^{(u)}-X_t^{(v)}\|_{V,p}\leq C_p|u-v|^\zeta
\]
uniformly in $t=1,\ldots,T$ and $u,v\in[0,1]$. Then we call the $V$-valued process $\{X_{t,T}\mid t=1,\ldots,T;T\in\mathbb N\}$ locally stationary with approximation rate $\zeta$.
''',[4],'Definition 2.1 (locally stationary function-valued process of rate ζ)',context='Definition 2.1 (locally stationary function-valued process of rate ζ).',symbols=[r'\|X_{t,T}-X_t^{(t/T)}\|_{V,p}',r'|u-v|^\zeta'],shape='Banach-valued triangular array with stationary approximants at rescaled time u, uniform Lp approximation rate and uniform Holder comparison. The main convergence results fix zeta=1.')
add('D2','time-varying spectral density operators',r'''
Provided $\sup_{t,T}\|X_{t,T}\|_{V,p}<\infty$ and $\sup_{u\in[0,1]}\|X_t^{(u)}\|_{V,p}<\infty$, $p\geq2$, the local second-order dynamics of $\{X_{t,T}\mid t=1,\ldots,T;T\in\mathbb N\}$ can be approximated by those of the auxiliary process $\{X_t^{(u)}\mid t\in\mathbb Z;u\in[0,1]\}$. More specifically, for fixed $T$, the instantaneous $h$th lag covariance operator at time $t$ of $\{X_{t,T}\mid t=1,\ldots,T,T\in\mathbb N\}$ is then an element of $S_1(\mathcal H)$ and is given by $\mathscr C_{t,h}^{(T)}=\mathbb E(X_{t+h,T}\otimes X_{t,T})$, $h\in\mathbb Z$, and the $h$th lag covariance operator at a fixed time $u$ of the auxiliary process is given by
\[
\mathscr C_h^{(u)}=\mathbb E(X_h^{(u)}\otimes X_0^{(u)}),\quad h\in\mathbb Z,\tag{2.1}
\]
where $\mathscr C_h^{(\cdot)}:[0,1]\to S_1(\mathcal H)$ is Lipschitz continuous with respect to the trace-class norm $\|\cdot\|_{S_1}$. Furthermore, for fixed $h\in\mathbb Z$, $\|\mathscr C_{t,h}^{(T)}-\mathscr C_h^{(t/T)}\|_{S_1}=O(T^{-\zeta})$ uniformly in $t=1,\ldots,T$.

In order to capture the full second-order dynamics of function-valued processes effectively, a time-frequency approach is taken. Under regularity conditions given below, the collection of time-varying spectral density operators belongs to the space of continuous functions from the time-frequency plane onto the cone of non-negative definite trace-class operators, i.e.,
\[
\mathscr F=\{\mathscr F_{u,\omega}\}_{u\in[0,1],\omega\in[-\pi,\pi]}\in C([0,1]\times[-\pi,\pi],S_1(\mathcal H)^+),\tag{2.2}
\]
where $\mathscr F_{u,\omega}=\frac1{2\pi}\sum_{h\in\mathbb Z}\mathscr C_h^{(u)}e^{-i\omega h}\in S_1(\mathcal H)^+$.
''',[4],'Section 2.1 — lag covariances and spectral density, equations (2.1)-(2.2)',{'D1':'The covariance and spectral family use the stationary approximating process at each u.'},phrases=['time-varying spectral density operators'],symbols=[r'\mathscr C_h^{(u)}',r'\mathscr F_{u,\omega}'],shape='Operator Fourier series of local lag second moments, with trace-class topology and nonnegative cone. The displayed moments are uncentered; a missing centering requirement is not silently inserted. Regularity and summability are separate assumptions.')
members['D2']['application_context']=[dict(text=r'We will mainly focus on the case where $V$ is a separable Hilbert space, i.e., $V=\mathcal H$.',evidence=[dict(page=4,location='After Definition 2.1')])]
add('D3','eigendecomposition',r'''
For fixed $(u,\omega)\in[0,1]\times[-\pi,\pi]$, let $\{\dot\lambda_i^{(u,\omega)}:i\geq1\}$, denote the sequence of eigenvalues in descending order and let $\{\varphi_i^{(u,\omega)}:i\geq1\}$ denote the corresponding eigenfunctions. We consider the following representation of the eigendecomposition of the operator
\[
\mathscr F_{u,\omega}=\sum_{j=1}^\infty\lambda_j^{(u,\omega)}\Pi_j^{(u,\omega)}\in S_1(\mathcal H)^+,\tag{2.3}
\]
where $\lambda_1^{(u,\omega)}>\lambda_2^{(u,\omega)}>\ldots>0$ are the distinct eigenvalues and where $\Pi_j^{(u,\omega)}=\sum_{k\in\{i:\dot\lambda_i^{(u,\omega)}=\lambda_j^{(u,\omega)}\}}\varphi_k^{(u,\omega)}\otimes\varphi_k^{(u,\omega)}$ denotes the projection operator onto the $j$th eigenspace.
''',[4],'Section 2.1 — eigenvalues and eigenspace projections, equation (2.3)',{'D2':'The decomposition belongs to the time-varying spectral density operator.'},phrases=['eigendecomposition'],symbols=[r'\lambda_j^{(u,\omega)}',r'\Pi_j^{(u,\omega)}'],shape='Distinct spectral eigenvalues and full eigenspace projectors, distinguished from the dotted list counted with multiplicity. Later simple-eigenvalue assumptions are preserved rather than inferred from this indexing.')
add('D4','representations',r'''
We consider processes that admit representations of the form
\[
X_{t,T}=\mathbb G(t,T,\mathfrak f_t),\tag{3.1}
\]
where $\mathfrak f_t=(\epsilon_t,\epsilon_{t-1},\ldots)$ for an i.i.d. sequence $\{\epsilon_t\mid t\in\mathbb Z\}$ of random elements taking values in some measurable space $S$, and where $\mathbb G:\mathbb Z\times\mathbb N\times S^\infty\to\mathcal H$ is a measurable function. The type of mixing conditions we impose are generalizations of those in [4] to nonstationary processes, which are of the same nature as the physical dependence measure introduced in [34]. To this end, consider $\mathfrak f_{t,\{k\}}=(\epsilon_t,\epsilon_{t-1},\ldots,\epsilon_{k+1},\epsilon'_k,\epsilon_{k-1},\ldots)$ for some independent copy $\epsilon'_k$ of $\epsilon_k$, and denote the corresponding filtrations by $\mathscr G_t=\sigma(\mathfrak f_t)$ and $\mathscr G_{t,\{k\}}=\sigma(\mathfrak f_{t,\{k\}})$, respectively.
''',[10],'Section 3.1 — causal representations and replaced innovations, equation (3.1)',kind='source_passage',phrases=['representations'],symbols=[r'\mathfrak f_{t,\{k\}}',r'\mathscr G_{t,\{k\}}'],shape='Measurable causal innovation representation and sigma fields after replacing the innovation at absolute index k. The conditional-expectation dependence measure is not replaced by a different coupling formula.')
add('D5','dependence measure',r'''
The process $\{X_{t,T}\}_{t\in\mathbb Z,T\in\mathbb N}$ satisfies Definition 2.1, $\sup_{t,T}\|X_{t,T}\|_{\mathcal H,p}<\infty$ for some $p>0$, and admits the representation (3.1). The series’ dependence structure is specified through the dependence measure
\[
\nu_{\mathcal H,p}^{X_{\cdot,\cdot}}(k,T)=\sup_{t\in\mathbb Z}\left\|X_{t,T}-\mathbb E[X_{t,T}\mid\mathscr G_{t,\{k\}}]\right\|_{\mathcal H,p}\tag{3.2}
\]
The dependence structure of the process satisfies $\sum_{k=0}^\infty\sup_{T\in\mathbb N}\nu_{\mathcal H,p}^{X_{\cdot,\cdot}}(k,T)<\infty$
''',[10],'Assumption 3.1',{'D1':'The assumption expressly requires Definition 2.1.','D4':'It requires representation (3.1) and the replacement sigma field.'},kind='assumption',phrases=['dependence measure','Assumption 3.1'],symbols=[r'\nu_{\mathcal H,p}^{X_{\cdot,\cdot}}(k,T)'],shape='Uniform moment and summable nonstationary dependence condition using the printed absolute-index replacement and supremum over t, without changing k to t-k.')
add('D6','auxiliary process',r'''
Let $p>0$. The auxiliary process $\{X_t^{(u)}\}_{t\in\mathbb Z,u\in[0,1]}$ is continuous in $u\in[0,1]$ and satisfies $\sup_{u\in[0,1]}\|X_t^{(u)}\|_{\mathcal H,p}<\infty$. For all $u\in[0,1]$, it admits a representation $X_t^{(u)}=G(u,\mathfrak f_t)$ where $G:[0,1]\times S^\infty\to\mathcal H$ is a measurable function. The series’ dependence structure satisfies

I) $\sum_{k=0}^\infty\nu_{\mathcal H,p}^{X_\cdot^\cdot}(k)<\infty$ where $\nu_{\mathcal H,p}^{X_\cdot^\cdot}(k)=\sup_{u\in[0,1]}\|X_k^{(u)}-\mathbb E[X_k^{(u)}\mid\mathscr G_{k,\{0\}}]\|_{\mathcal H,p}$;

II) There exists an orthonormal basis $\{e_\ell\}$ of $\mathcal H$ such that $\sum_{\ell\in\mathbb N}\sum_{k=0}^\infty\nu_{\mathbb C,p}^{X_\cdot^\cdot(e_\ell)}(k)<\infty$, where
\[
\nu_{\mathbb C,p}^{X_\cdot^\cdot(e_\ell)}(k)=\sup_{u\in[0,1]}\left\|\langle e_\ell,X_k^{(u)}\rangle-\mathbb E[\langle e_\ell,X_k^{(u)}\rangle\mid\mathscr G_{k,\{0\}}]\right\|_{\mathbb C,p}.\tag{3.3}
\]
''',[10,11],'Assumption 3.2',{'D1':'The stationary approximants come from Definition 2.1.','D4':'The filter uses the same innovation history and replacement-at-zero sigma field.'},kind='assumption',phrases=['auxiliary process','Assumption 3.2'],symbols=[r'\nu_{\mathbb C,p}^{X_\cdot^\cdot(e_\ell)}(k)',r'\mathscr G_{k,\{0\}}'],shape='Hilbert-norm and coordinate-summed dependence requirements for the approximants. Condition II is retained for the trace-class theorems; the source relaxation to I for Hilbert-Schmidt convergence is not applied.')
add('D7','smoothness conditions',r'''
$\sum_{\ell\in\mathbb N}\sum_{k=0}^\infty k^\iota\nu_{\mathbb C,p}^{X_\cdot^\cdot(e_\ell)}(k)<\infty$, $\iota\geq2$ and for almost every $\omega$, the mapping $u\mapsto\mathscr F_{u,\omega}$ is twice Fréchet differentiable with $\sup_u\|\frac{\partial^2}{\partial u^2}\mathscr F_{u,\omega}\|_{S_1}<\infty$.
''',[11],'Assumption 3.3',{'D6':'The weighted summability uses coordinate dependence coefficients (3.3).','D2':'Time differentiability acts on the spectral density in trace norm.'},kind='assumption',context='To control the bias of functionals of the partial sum estimator that is introduced below, we furthermore impose the following smoothness conditions.',phrases=['Assumption 3.3'],symbols=[r'k^\iota',r'\frac{\partial^2}{\partial u^2}\mathscr F_{u,\omega}'],shape='Weighted coordinate dependence summability and almost-every-frequency twice Frechet differentiability in time, bounded uniformly in time. No uniform-frequency bound is inserted.')
add('D8','weights',r'''
\[
\widetilde w_{b_f,s,t}^{(\omega)}=(2\pi)^{-1}w(b_f(s-t))e^{i\omega(s-t)}\tag{3.7}
\]
for some function $w:\mathbb R\to\mathbb R$ supported on the interval $[-1,1]$, and $b_f=b(N)$ is a bandwidth parameter.
''',[12],'Section 3.2 — lag-window weights, equation (3.7)',context='and where the weights are defined by',symbols=[r'\widetilde w_{b_f,s,t}^{(\omega)}'],shape='Complex lag-window weights with real compactly supported window and bandwidth b_f. Additional window regularity is a separate assumption.')
add('D9','sequential estimator',r'''
To be precise, for $\eta\in[0,1]$, we define the sequential estimator of $\mathscr F_{u,\omega}$ by
\[
\begin{aligned}
\widehat{\mathscr F}_{u,\omega}(\eta)=\frac1{\lfloor\eta N\rfloor}\Bigg\{&\sum_{s=1}^{\lfloor\eta N\rfloor}\Big(X_{t(u)+s}\otimes\Big[\sum_{t=1}^{\lfloor\eta N\rfloor}\widetilde w_{b_f,s,t}^{(\omega)}X_{t(u)+t}+f(\eta,N)\widetilde w_{b_f,s,\lfloor\eta N\rfloor+1}^{(\omega)}X_{t(u)+\lfloor\eta N\rfloor+1}\Big]\\
&+f(\eta,N)X_{t(u)+\lfloor\eta N\rfloor+1}\otimes\Big[\sum_{t=1}^{\lfloor\eta N\rfloor}\widetilde w_{b_f,\lfloor\eta N\rfloor+1,t}^{(\omega)}X_{t(u)+t}+\widetilde w_{b_f,\lfloor\eta N\rfloor+1,\lfloor\eta N\rfloor+1}^{(\omega)}X_{t(u)+\lfloor\eta N\rfloor+1}\Big]\Bigg\},
\end{aligned}\tag{3.6}
\]
where $f(\eta,N)=(\eta N-\lfloor\eta N\rfloor)$, $t(u)=t_N(u)=\lfloor uT\rfloor-\lfloor N/2\rfloor$, $N=N(T)$ defines the neighborhood over which the process is approximately stationary,
''',[11,12],'Section 3.2 — sequential spectral estimator, equation (3.6)',{'D8':'Every weighted term uses (3.7).','D1':'The X observations belong to the locally stationary array; its T index is suppressed here.'},symbols=[r'\widehat{\mathscr F}_{u,\omega}(\eta)',r'f(\eta,N)',r't_N(u)'],shape='Printed sequential windowed estimator including floor denominator and three interpolation terms. The final self-product has the single outer interpolation factor as printed. Zero-denominator convention and claimed continuity are separate source context.')
members['D9']['application_context']=[dict(text=r'We also remark that if $\lfloor\eta N\rfloor=0$ then $\widehat{\mathscr F}_{u,\omega}(\eta)=0$. This yields the process $\{\widehat{\mathscr F}(\eta)\mid\eta\in I\}=\{\widehat{\mathscr F}_{u,\omega}(\eta)\mid u\in[0,1],\omega\in[0,\pi],\eta\in I\}$.',evidence=[dict(page=12,location='Before and in equation (3.8)')])]
add('D10','weight function',r'''
$w$ is an even bounded piecewise continuous function with compact support on $[-1,1]$ with $\lim_{x\to0}w(x)=1$ and $w(x)-1=O(x^\iota)$, $\iota\geq2$, as $x\to0$.
''',[12],'Assumption 3.4',kind='assumption',context='We conclude this section stating the assumptions on the weight function and the parameter $b_f$ in (3.7) that are required for the development of the asymptotic theory in the subsequent discussion.',phrases=['Assumption 3.4'],symbols=[r'w(x)-1=O(x^\iota)'],shape='Even bounded piecewise continuous lag window with compact support and order-iota flatness at zero. Positive definiteness of its finite lag matrices is not explicitly assumed.')
add('D11','bandwidth',r'''
Let $\zeta=1$. Assume that $N=T^\alpha$, the bandwidth satisfies $b_f\simeq N^{-\kappa},1/(2\iota+1)<\kappa<1$ and the parameters $M$ and $N$ satisfy $N\to\infty$, $M\to\infty$ as $T\to\infty$ such that $M=o(N^{1-\kappa})$ and $N^{1-\kappa}=o(M^3)$. More specifically, we have the following cases
\[
\begin{cases}
\alpha<\dfrac2{(2\iota+1)\kappa-1+3}\text{ and }M=o(N^{(2\iota+1)\kappa-1})&\text{if }\dfrac1{2\iota+1}<\kappa\leq\dfrac1{\iota+1},\\
\alpha<\dfrac2{4-\kappa}&\text{if }\dfrac1{\iota+1}\leq\kappa<1.
\end{cases}
\]
''',[13],'Assumption 3.5',{'D1':'Zeta is the approximation rate in Definition 2.1.','D8':'b_f and N are the bandwidth and neighborhood length of the lag-window estimator.','D13':'M counts the rescaled-time grid points used in the discrete time average.'},kind='assumption',phrases=['bandwidth','Assumption 3.5'],symbols=[r'M=o(N^{1-\kappa})',r'N^{1-\kappa}=o(M^3)'],shape='Joint asymptotic restrictions on T,N,M,b_f with zeta=1 and both kappa regimes including their common endpoint. Alpha here is a growth exponent, distinct from the later testing level. Iota is the common order in Assumptions 3.3 and 3.4.')
add('D12','normalizing sequence',r'''
\[
\rho_T^2=\frac{Nb_f}{k_f},\tag{3.11}
\]
with $\kappa_f=\int_{-1}^1w^2(x)dx$.
''',[12],'Section 3.2 — normalizing sequence, equation (3.11)',{'D8':'The normalization uses the bandwidth and window in (3.7).'},context='and the normalizing sequence is given by',symbols=[r'\rho_T^2'],shape='Scaling by neighborhood length, bandwidth and integrated squared window. The display writes k_f while the following prose defines kappa_f; the mismatch is retained.')
add('D13','equidistant points',r'''
\[
U_M=\{u_1,\ldots,u_M\}\tag{3.15}
\]
denotes an increasingly dense set of distinct equidistant points $u_1<u_2<\ldots<u_M$ in the unit interval $(0,1)$ where $u_1=\frac N{2T}$ and $u_M=1-\frac N{2T}$, and where $M=M(T)\to\infty$ as $T\to\infty$ at an appropriate rate.
''',[14],'Section 3.3 — rescaled-time grid, equation (3.15)',phrases=['equidistant points'],symbols=[r'U_M',r'u_1=\frac N{2T}'],shape='Equally spaced interior grid with M points, trimmed by half a window at each boundary. N is the neighborhood length; separate rate assumptions govern the sequences.')
add('D14','bounded linear operators',r'''
Let $1\leq r\leq\infty$ and consider the mapping $\Upsilon:[0,1]\times[0,\pi]\to\mathcal L(C_{S_r})$, $(u,\omega)\mapsto\Upsilon_{u,\omega}$ that satisfies

i) $\sup_{\eta\in I}\|\Upsilon_{u,\omega}(B(\eta))\|_{S_r}\leq\|\Upsilon_{u,\omega}\|_\infty\sup_{\eta\in I}\|B(\eta)\|_{S_r}$, $\forall(u,\omega)\in[0,1]\times[0,\pi]$ and all $B\in C_{S_r}$;

ii) $\int_0^\pi\sup_{u\in[0,1]}\|\Upsilon_{u,\omega}\|_\infty^p d\omega<\infty$;

iii) $\Upsilon_{\cdot,\omega}:[0,1]\to\mathcal L(S_1)$ is twice Fréchet differentiable with $\int_0^\pi\sup_{u\in[0,1]}\|\frac{\partial^2}{\partial u^2}\Upsilon_{u,\omega}\|_{\mathcal L(S_1)}d\omega<\infty$.

If the mapping $\Upsilon$ is a function of $\mathscr F$, then we assume that this holds on a set on which the Fréchet derivatives of $u\mapsto\mathscr F_{u,\omega}$ are well-defined.
''',[15],'Assumption 3.6',kind='assumption',context='Firstly, we require the introduction of the following mappings from the square $[0,1]\times[0,\pi]$ onto the space $\mathcal L(C_{S_r})$, the space of bounded linear operators from $C_{S_r}$ onto $C_{S_r}$. We denote the corresponding operator norm by $\|\cdot\|_\infty$.',phrases=['Assumption 3.6'],symbols=[r'\Upsilon_{u,\omega}',r'\mathcal L(C_{S_r})'],shape='Operator field with path-space bound, frequency-integrated p bound and twice differentiable time dependence. The printed switch from operators on C_Sr to S1 in iii is retained. Dependence on F is conditional, not mandatory.')
add('D15','spectrum',r'''
More specifically, let $\Omega$ be an open set in $\mathbb C$ with smooth boundary $\partial\Omega$ and let $A\in L^1_{S_r(\mathcal H)^+}([0,1]\times[0,\pi]\times I)$, where we slightly abuse notation to restrict the codomain to the cone of positive semi-definite elements of the Banach space $S_r(\mathcal H)^\dagger$. Now, let $\sigma(A_{u,\omega}(\eta))$ denote the spectrum of the operator $A_{u,\omega}(\eta)\in S_r(\mathcal H)^+$ and define
\[
\sigma(A)=\cup_{u,\omega,\eta}\sigma(A_{u,\omega}(\eta))\tag{3.20}
\]
as the “spectrum” of $A$. Then we consider the set $\mathbb D_r$ of functions of which the spectrum is enclosed in the interior of $\partial\Omega$, that is,
\[
\mathbb D_r=\{A\in L_{S_r(\mathcal H)^+}([0,1]\times[0,\pi]\times I)\mid\sigma(A)\subset\Omega,\operatorname{dist}(\partial\Omega,\sigma(A))>0\}.\tag{3.21}
\]
Let $D\subset\mathbb C$ denote an open set with $D\supset\overline\Omega$ and $\phi:D\to\mathbb C$ be a holomorphic function, then the Riesz-Dunford integral of the elements in $\mathbb D_r$ is well-defined; we refer to Appendix E for more details.
''',[15],'Section 3.4 — spectral domain, equations (3.20)-(3.21)',phrases=['spectrum'],symbols=[r'\mathbb D_r',r'\operatorname{dist}(\partial\Omega,\sigma(A))>0'],shape='Union spectrum of a nonnegative operator field and separated-contour domain for holomorphic calculus. The L notation in (3.21) omits the preceding superscript one. Appendix E is not read; missing regularity or analyticity at zero is not supplied.')
add('D16','holomorphic functional calculus',r'''
For a mapping $\Upsilon$ satisfying Assumption 3.6, we now define the mapping
\[
\begin{aligned}
\mathscr G_\Upsilon:\mathbb D_r&\to L^1_{C_{S_r}}([0,1]\times[0,\pi]),\\
A&\mapsto\mathscr G_\Upsilon(A):\begin{cases}[0,1]\times[0,\pi]\to C_{S_r},\\(u,\omega)\mapsto\{\mathscr G_{\Upsilon,u,\omega}(A)(\eta)\mid\eta\in[0,1]\}\end{cases}
\end{aligned}\tag{3.22}
\]
by
\[
\mathscr G_{\Upsilon,u,\omega}(A)(\eta)=\Upsilon_{u,\omega}\big(\eta^{x-1}\phi(\eta A(\eta)_{u,\omega})\big)\tag{3.23}
\]
where $x\geq1$ is introduced for technical reasons, and where we do not reflect the dependence of $\mathscr G_\Upsilon$ on the function $\phi$ because it will always be clear from the context.
''',[15,16],'Section 3.4 — transformed operator field, equations (3.22)-(3.23)',{'D14':'The transformation requires an operator field satisfying Assumption 3.6.','D15':'Its domain and evaluation of phi use the preceding separated-spectrum calculus setup.'},context=r'Because other applications also require functionals of $\widehat{\mathscr F}$ such as $\widehat{\mathscr F}^{1/2}=\{\widehat{\mathscr F}_{u,\omega}^{1/2}\mid u\in[0,1],\omega\in[0,\pi]\}$, we will define $\mathscr G_\Upsilon$ in a more general form using holomorphic functional calculus.',symbols=[r'\mathscr G_{\Upsilon,u,\omega}(A)(\eta)',r'\eta^{x-1}\phi(\eta A(\eta)_{u,\omega})'],shape='Generic transformation by a scalar analytic function and Upsilon, with factor eta^(x-1). F and F-hat are theorem instantiations rather than prerequisites of the generic definition on A.')
members['D16']['naming_context'][0]['evidence']=[dict(page=15,location='Before equation (3.20)')]
add('D17','linear maps',r'''
We define the linear maps
\[
\begin{aligned}
L_{U_M}^{a,b}:L^1_{C_{S_1}}([0,1]\times[0,\pi])&\to C_{S_1},\\
A&\mapsto L_{U_M}^{a,b}(A):\begin{cases}I\to S_1(\mathcal H),\\\eta\mapsto\frac1M\sum_{u\in U_M}\int_a^b A_{u,\omega}(\eta)d\omega\end{cases}
\end{aligned}\tag{3.25}
\]
\[
\begin{aligned}
L^{a,b}:L^1_{C_{S_1}}([0,1]\times[0,\pi])&\to C_{S_1},\\
A&\mapsto L^{a,b}(A):\begin{cases}I\to S_1(\mathcal H),\\\eta\mapsto\int_0^1\int_a^b A_{u,\omega}(\eta)d\omega du\end{cases}
\end{aligned}\tag{3.26}
\]
''',[16],'Section 3.4 — discrete and continuous integration, equations (3.25)-(3.26)',{'D13':'The discrete map uses the specified time grid U_M.'},phrases=['linear maps'],symbols=[r'L_{U_M}^{a,b}',r'L^{a,b}'],shape='Paired source maps: discrete time averaging with frequency integration, and full time-frequency integration. They are different maps. Evaluation on a grid needs a representative or additional regularity beyond an L1 equivalence class; that source issue is recorded separately.')
add('D18','mixing condition exhibiting polynomial decay',r'''
for some $0<\rho<1$,
\[
\sum_{r\in\mathbb N}\sum_{j=l}^\infty\nu_{\mathbb C,p}^{X_\cdot^\cdot(e_r)}(j)=O((l+1)^{-\rho}).\tag{3.28}
\]
''',[16],'Theorem 3.1(b) — coordinate dependence tail, equation (3.28)',{'D6':'The tail uses coordinate dependence coefficients from Assumption 3.2 II.'},kind='theorem_excerpt',context=r'To prove (3.30), we make use of the mixing condition exhibiting polynomial decay, where the speed of the decay is controlled by the parameter $\rho$ in condition (3.28).',symbols=[r'\nu_{\mathbb C,p}^{X_\cdot^\cdot(e_r)}(j)',r'(l+1)^{-\rho}'],shape='Coordinate-summed dependence tail for some 0<rho<1 as bound in Theorem 3.1(b). The tail exponent rho is distinct from rho_T and from Assumption 3.3 weighted summability.')
interfaces[-1]['lean_role']='hypothesis'
members['D18']['naming_context'][0]['evidence']=[dict(page=17,location='After equation (3.30)')]
add('D19','Fréchet differentiable mappings',r'''
Furthermore, let $W$ denote a separable Banach space and consider $k$ Fréchet differentiable mappings $\Psi_1,\Psi_2,\ldots,\Psi_k:C_{S_1}\to C_W$.
''',[17],'Corollary 3.1 — outer mappings',kind='condition',phrases=['Fréchet differentiable mappings'],symbols=[r'\Psi_1,\Psi_2,\ldots,\Psi_k:C_{S_1}\to C_W'],shape='Outer Frechet differentiable maps on continuous trace-class paths, with values in paths over a separable Banach space. The Corollary also assumes Theorem 3.1 for k operator fields; that inherited condition is resolved separately for each consuming theorem.')
add('D20','mappings',r'''
Note that formally
\[
\mathscr T_{j,T}=\Psi_j\circ L_{U_M}^{a,b}\circ\mathscr G_{\Upsilon_j},\quad\mathscr T_j=\Psi_j\circ L^{a,b}\circ\mathscr G_{\Upsilon_j}\tag{3.31}
\]
define mappings from $L^1_{C_{S_1}}([0,1]\times[0,\pi])$ onto $C_W$.
''',[17],'Section 3.4 — population and discrete functionals, equation (3.31)',{'D19':'Psi_j is an outer Frechet differentiable map from Corollary 3.1.','D17':'The two compositions use the discrete and continuous integration maps respectively.','D16':'Both act on the transformed operator field defined by (3.23).'},phrases=['mappings'],symbols=[r'\mathscr T_{j,T}',r'\mathscr T_j'],shape='Paired discrete and population functionals defined by their compositions. They need not be the same map. The later expanded displays use h and eta factors differently; those source expansions will be archived separately without overwriting (3.31).')
add('D21','limiting process',r'''
Let $W=\mathbb R$ or $W=\mathbb C$. In our applications, there exist functions $g_{11},\ldots,g_{kk}\in C(I,\mathbb R_{\geq0})$, and a matrix $\sigma\in\mathbb R^{k\times k}$ such that the limiting process in (3.33) satisfies
\[
\left\{\left(\Psi'_{j,(L^{a,b}\circ\mathscr G)}\big(h(\eta)\eta^{x-1}\mathbb W_{\mu_{\Upsilon_j}}(\eta)\big)\right)_{j=1,\ldots,k}\right\}_{\eta\in I}\overset{\mathscr D}=\left\{\sigma\mathbf g(\eta)\mathbb B(\eta)\right\}_{\eta\in I},\tag{3.34}
\]
where $\mathbf g=\operatorname{diag}(g_{11},\ldots,g_{kk})$, the symbol $\overset{\mathscr D}=$ denotes equality in distribution, and where $\mathbb B$ is a $k$-dimensional vector of independent real- or proper complex-valued Brownian motions.
''',[18],'Section 3.4 — factorization of the limiting process, equation (3.34)',{'D19':'The left side uses the derivative of each outer map Psi_j.','D17':'The source subscript identifies the integral-map composition.','D16':'The derivative point refers to the transformed operator field.'},kind='condition',phrases=['limiting process'],symbols=[r'\sigma\mathbf g(\eta)\mathbb B(\eta)',r'\mathbf g=\operatorname{diag}(g_{11},\ldots,g_{kk})'],shape='Required distributional factorization into a fixed real mixing matrix, diagonal time functions and independent scalar Brownian motions. The derivative point is abbreviated in the source. Brownian W parameters come from Theorem 3.1; their appendix-only covariance formulas remain unresolved.')
add('D22','linear',r'''
Additionally, in our applications the mappings $\mathscr T_1,\mathscr T_2,\ldots,\mathscr T_k$ in (3.33) are “linear” in the sense that
\[
\mathscr T_j\big(\{\eta G(\eta)\mid\eta\in I\}\big)=\{f_j(\eta)\mathscr T_j(G(\cdot))\mid\eta\in I\},\quad j=1,\ldots,k,\tag{3.35}
\]
where $f_1,\ldots,f_k\in C(I,\mathbb R)$ are known functions (defined by the specific problem) satisfying $f_j(1)=1$ and $\{\eta G(\eta)\mid\eta\in I\}$ and $\{G(\eta)\mid\eta\in I\}$ are processes in $L^1_{C_{S_1}}([0,1]\times[0,\pi])$.
''',[18],'Section 3.4 — source “linear” scaling condition, equation (3.35)',{'D20':'The scaling requirement concerns the defined functionals T_j.'},kind='condition',phrases=['linear'],symbols=[r'f_j(1)=1',r'f_j(\eta)\mathscr T_j(G(\cdot))'],shape='The author\'s quoted linear condition is a specified time-scaling identity with known f_j, not general additivity of T_j. The right side prints a path-valued functional without evaluation at eta; that source notation is not silently normalized.')
add('D23','self-normalization approach',r'''
More specifically, let $\nu$ denote a measure on the interval $(0,1)$, define the quantities
\[
\widehat{\mathscr D}_j(\eta):=\mathscr T_{j,T}(\widehat{\mathscr F})(\eta)-\mathscr T_j(\mathscr F)(\eta),\tag{3.36}
\]
\[
V_{i,j}^2=\int_0^1\big(\widehat{\mathscr D}_i(\eta)-f_i(\eta)\widehat{\mathscr D}_i(1)\big))\overline{\big(\widehat{\mathscr D}_j(\eta)-f_j(\eta)\widehat{\mathscr D}_j(1)\big)}\nu(d\eta),\tag{3.37}
\]
and note that
\[
\widehat{\mathscr D}_i(\eta)-f_i(\eta)\widehat{\mathscr D}_i(1)=\mathscr T_{i,T}(\widehat{\mathscr F})(\eta)-f_i(\eta)\mathscr T_{i,T}(\widehat{\mathscr F})(1).
\]
''',[18],'Section 3.4 — errors and self-normalizer entries, equations (3.36)-(3.37)',{'D20':'The errors and their centered paths use the paired functionals T_j,T and T_j.','D22':'The cancellation uses the source scaling functions f_j.','D9':'The empirical functionals are evaluated at the sequential spectral estimator.','D2':'The population functionals are evaluated at the true spectral family.'},context='We remark that condition (3.34) in Theorem 3.2 ensures a self-normalization approach is feasible',symbols=[r'\widehat{\mathscr D}_j(\eta)',r'V_{i,j}^2'],shape='The error paths and conjugated Gram-integral entries defining the matrix V_k. Superscript 2 is the source entry notation; diagonal V_jj is its scalar square root. The extra closing parenthesis in (3.37) is retained as printed. The measure nu differs from coherence singular values and from a model-accuracy threshold.')
members['D23']['naming_context'][0]['evidence']=[dict(page=19,location='Remark 3.4(a) — self-normalization interpretation')]
add('D24','statistic',r'''
\[
\frac{\widehat r-r}V=\frac{\mathscr T_{1,T}(\widehat{\mathscr F})(1)-\mathscr T_1(\mathscr F)}{V_{11}}\overset{\mathscr D}{\longrightarrow}\mathbb T=\frac{g(1)\mathbb B(1)}{\left(\int_0^1|g(\eta)\mathbb B(\eta)-f(\eta)g(1)\mathbb B(1)|^2\nu(d\eta)\right)^{1/2}},\tag{4.1}
\]
where $V=V_{11}$ is defined in (3.37), $\mathbb B$ denotes a standard Brownian motion and where the functions $f=f_1$, $g=g_{11}$ and the measure $\nu$ are known, and depend on the concrete application (see Section 3.5 for some examples). Consequently, the distribution of the statistic $\mathbb T$ on the right-hand side of (4.1) is pivotal and its quantiles can be readily simulated.
''',[22],'Section 4.1 — scalar pivotal statistic, equation (4.1)',{'D23':'V is the diagonal self-normalizer from (3.37).','D21':'The known function g and standard Brownian motion are the scalar specialization of (3.34).','D22':'The known function f is the scalar scaling function from (3.35).'},phrases=['statistic'],symbols=[r'\mathbb T',r'V=V_{11}'],shape='Scalar Brownian-ratio limiting statistic and its empirical counterpart, with a known application-specific distribution. The quantiles in Section 4 refer to this distribution. The source labels it pivotal subject to the nondegeneracy conditions inherited from Theorem 3.2.')
add('D25','normalized measure of total variation',r'''
From (2.5), we can define a normalized measure of total variation explained by the principal $d$ directions over $[0,1]\times[a,b]$ by
\[
s_d=\mathscr T(\mathscr F):=\frac{\int_0^1\int_a^b\sum_{j=1}^d\lambda_j^{(u,\omega)}d\omega du}{\int_0^1\int_a^b\sum_{j=1}^\infty\lambda_j^{(u,\omega)}d\omega du},\tag{2.7}
\]
where the last equality defines the functional $\mathscr T$ of the spectral density operator $\mathscr F$ explicitly.
''',[5],'Section 2.2.1 — principal-component variation ratio, equation (2.7)',{'D3':'The numerator and denominator use the spectral eigenvalues defined in (2.3).'},phrases=['normalized measure of total variation'],symbols=[r'\sum_{j=1}^d\lambda_j^{(u,\omega)}'],shape='Integrated principal-component ratio over the specified time-frequency interval. The source uses its undotted eigenvalue convention; the later trace denominator and no-multiplicity assumptions are recorded without altering this formula.')
add('D26','separable component decomposition',r'''
Alternatively, we may view this object as an element of the product space $S_2(\mathcal H_2\otimes\mathcal H_2,\mathcal H_1\otimes\mathcal H_1)$, say $F_{u,\omega}$, in which case we have the spectral decomposition $F_{u,\omega}=\sum_{j=1}^\infty\delta_j^{(u,\omega)}f_j^{(u,\omega)}\otimes g_j^{(u,\omega)}$ where $\{f_j^{(u,\omega)}\}_{j\geq1}$ is an ONB of $\mathcal H_1\otimes\mathcal H_1$ and $\{g_j^{(u,\omega)}\}_{j\geq1}$ is an ONB of $\mathcal H_2\otimes\mathcal H_2$. If we view $F_{u,\omega}$ as an element of $S_2(\mathcal H_1)\otimes S_2(\mathcal H_2)$, we can write the latter as $F_{u,\omega}=\sum_{j=1}^\infty\delta_j^{(u,\omega)}A_j^{(u,\omega)}\otimes B_j^{(u,\omega)}$ such that a self-adjoint version $\mathscr F_{u,\omega}\in S_2(\mathcal H,\mathcal H)$ is given by
\[
\mathscr F_{u,\omega}=\sum_{j=1}^\infty\delta_j^{(u,\omega)}A_j^{(u,\omega)}\widetilde\otimes B_j^{(u,\omega)},\tag{2.9}
\]
We refer to (2.9) as the separable component decomposition of $\mathscr F_{u,\omega}$. It is worth emphasizing that (2.9) and (2.8) are different decompositions of the same operator. The operator is called separable of degree $d$ if all but the first $d$ scores $\delta_j^{(u,\omega)}$ are zero.
''',[6],'Section 2.2.2 — rearranged spectral decomposition, equation (2.9)',{'D2':'The rearranged object is the same time-varying spectral density operator.'},phrases=['separable component decomposition'],symbols=[r'\delta_j^{(u,\omega)}',r'\widetilde\otimes'],shape='Singular-component decomposition after tensor rearrangement for H=H1 tensor H2. Delta scores are not eigenvalues lambda of the original operator. The Kronecker identification and its complex-space convention are preserved in application context.')
members['D26']['application_context']=[dict(text=r'Let $\mathcal H=\mathcal H_1\otimes\mathcal H_2$, then it is known that we have the following isometric isomorphisms $\mathcal H_1\otimes\mathcal H_2\otimes\mathcal H_1\otimes\mathcal H_2\cong S_2(\mathcal H,\mathcal H)\cong S_2(\mathcal H_2\otimes\mathcal H_2,\mathcal H_1\otimes\mathcal H_1)\cong S_2(\mathcal H_1)\otimes S_2(\mathcal H_2)$.',evidence=[dict(page=5,location='Section 2.2.2 — tensor identification')]),dict(text=r'Furthermore, we recall the definition of the Kronecker tensor product $A\widetilde\otimes B$, which satisfies $(A\widetilde\otimes B)C=ACB^\dagger$, $A,B,C\in S_r(\mathcal H)$, and which essentially entails a permutation of the dimensions, i.e., for $a,a\prime\in\mathcal H_1$, $b,b\prime\in\mathcal H_2$, we have $((a\otimes a\prime)\widetilde\otimes(b\otimes b\prime))=((a\otimes b)\otimes(a\prime\otimes b\prime))$.',evidence=[dict(page=6,location='Before equation (2.8) — Kronecker convention')])]
add('D27','separability',r'''
We therefore define
\[
s_d=\mathscr T(\mathscr F):=\frac{\int_0^1\int_a^b\sum_{j=1}^d(\delta_j^{(u,\omega)})^2du d\omega}{\int_0^1\int_a^b\sum_{j=1}^\infty(\delta_j^{(u,\omega)})^2du d\omega}\tag{2.10}
\]
as the (normalized) degree $d$ separability and are interested in investigating how much variation can be explained by a $d$-separable approximation.
''',[6],'Section 2.2.2 — normalized separability measure, equation (2.10)',{'D26':'The ratio uses squared scores from the rearranged decomposition (2.9).'},phrases=['separability'],symbols=[r'(\delta_j^{(u,\omega)})^2'],shape='Ratio of integrated squared separable scores. The display prints integration limits and differentials in inconsistent order; it is retained as printed, with the theorem formula separately preserved.')
add('D28','cross-spectra',r'''
The diagonal gives the time-varying component spectra, while the other entries give the time-varying cross-spectra, which satisfy $\mathscr F_{u,\omega}^{ij}=\mathbb E(Z_{u,\omega}^i\otimes Z_{u,\omega}^j)\in S_1(\mathcal H_j,\mathcal H_i)$. Let $P_i^{\mathcal H}$, $i=1,2$, denote the orthogonal projection of $\mathcal H=\mathcal H_1\oplus\mathcal H_2$ onto $\mathcal H_i$. Then observe that
\[
\mathscr F_{u,\omega}^{ij}=P_i^{\mathcal H}\mathscr F_{u,\omega}P_j^{\mathcal H}
\]
so that $\mathscr F_{u,\omega}^{ij}$ is simply the restriction of $\mathscr F_{u,\omega}$ to $\mathcal H_i$ and $\mathcal H_j$, $i,j=1,2$.
''',[6,7],'Section 2.2.3 — component and cross-spectral blocks',{'D2':'The blocks are compressions of the full spectral density on the direct-sum space.'},phrases=['cross-spectra'],symbols=[r'\mathscr F_{u,\omega}^{ij}',r'P_i^{\mathcal H}'],shape='Blocks of the spectral density on H1 direct-sum H2. The source also equates these densities with moments of the cumulative orthogonal-increment process Z; that equality is not silently changed to a derivative of the increment covariance.')
add('D29','canonical coherence',r'''
In what follows, we introduce a notion of time-varying functional canonical coherence. To make this more precise, consider finding functions $g\in\mathcal H_1$ and $h\in\mathcal H_2$ such that the co-variation between $Z_{u,\omega}^1$ and $Z_{u,\omega}^2$ is maximized, that is,
\[
\sup_{\|g\|_{\mathcal H_1}=1,\|h\|_{\mathcal H_2}=1}\operatorname{Cov}(\langle Z_{u,\omega}^1,g\rangle_{\mathcal H_1},\langle Z_{u,\omega}^2,h\rangle_{\mathcal H_2})=\sup_{\|g\|_{\mathcal H_1}=1,\|h\|_{\mathcal H_2}=1}\langle\mathscr F_{u,\omega}^{12}(h),g\rangle_{\mathcal H_1}=\nu_1^{u,\omega}.\tag{2.11}
\]
Here $\nu_1^{u,\omega}$ is the largest singular value of the operator $\mathscr F_{u,\omega}^{12}$, since the supremum is attained for the eigenfunctions belonging to the largest eigenvalue of $\mathscr F_{u,\omega}^{11}$ and $\mathscr F_{u,\omega}^{22}$, respectively, i.e., $g=\varphi_{11,1}^{(u,\omega)}$ and $h=\varphi_{22,1}^{(u,\omega)}$. This leads to the following notion of first order canonical coherence at time $u$ and frequency $\omega$
\[
\mathscr R_1^{u,\omega}=\frac{\operatorname{Cov}(\langle Z_{u,\omega}^1,\varphi_{11,1}^{(u,\omega)}\rangle_{\mathcal H_1},\langle Z_{u,\omega}^2,\varphi_{22,1}^{(u,\omega)}\rangle_{\mathcal H_2})}{\sqrt{\operatorname{Var}(\langle Z_{u,\omega}^1,\varphi_{11,1}^{(u,\omega)}\rangle_{\mathcal H_1})\operatorname{Var}(\langle Z_{u,\omega}^2,\varphi_{22,1}^{(u,\omega)}\rangle_{\mathcal H_2})}}=\frac{\nu_1^{u,\omega}}{\sqrt{\lambda_{11,1}^{u,\omega}\lambda_{22,1}^{u,\omega}}}
\]
where $\lambda_{ii,1}^{u,\omega}$ is the largest eigenvalue of the operator $\mathscr F_{u,\omega}^{ii}$ $(i=1,2)$.

Repeating the maximization argument in (2.11) on sequences of orthogonal complements, we find that the $d$th order canonical coherence at time $u$ and frequency $\omega$ is given by the variable
\[
\mathscr R_d^{u,\omega}=\nu_d^{u,\omega}/\sqrt{\lambda_{11,d}^{u,\omega}\lambda_{22,d}^{u,\omega}}.
\]
We may therefore define as a measure of $d$th order canonical coherence over the time-frequency interval $[0,1]\times[a,b]$ by
\[
s_d=\mathscr T(\mathscr F):=\int_0^1\int_a^b\mathscr R_d^{u,\omega}d\omega du.
\]
''',[7],'Section 2.2.3 — canonical coherence and its integral',{'D28':'The ratio uses singular values of cross-spectral blocks and eigenvalues of the marginal blocks.'},phrases=['canonical coherence'],symbols=[r'\mathscr R_d^{u,\omega}',r'\nu_d^{u,\omega}'],shape='The original coherence ratio of cross-block singular value to the square root of matching marginal eigenvalues, and its time-frequency integral. The claimed marginal-eigenvector maximization is preserved as a source assertion, not assumed valid for arbitrary cross-spectra or replaced by another canonical-correlation definition.')
add('D30','square root distance',r'''
To be more precise, denote the square root distance between two operators $A$ and $B$ in $S_1(\mathcal H)^+$ by
\[
d_R(A,B)=\|A^{1/2}-B^{1/2}\|_{S_2(\mathcal H)}.\tag{2.12}
\]
''',[8],'Section 2.2.4 — square root distance, equation (2.12)',phrases=['square root distance'],symbols=[r'd_R(A,B)',r'\|A^{1/2}-B^{1/2}\|_{S_2(\mathcal H)}'],shape='Hilbert-Schmidt distance between nonnegative operator square roots. The square roots are the nonnegative roots; this definition is distinct from an unrestricted holomorphic formula at zero.')
add('D31','restriction',r'''
More specifically, let $\mathscr F_{u,\omega,d}=\sum_{j=1}^d\Pi_j^{(u,\omega)}\mathscr F_{u,\omega}$ be the restriction of $\mathscr F_{u,\omega}$ to the space spanned by the first $d$ leading functional principal components, and define $\widehat{\mathscr F}_{u,\omega,d}(\eta)$ similarly.
''',[21],'Section 3.5.4 — spectral restriction',{'D3':'The restriction uses leading spectral projectors.','D9':'The empirical restriction is defined similarly for the sequential spectral estimator.'},phrases=['restriction'],symbols=[r'\mathscr F_{u,\omega,d}',r'\widehat{\mathscr F}_{u,\omega,d}(\eta)'],shape='Restriction to leading principal components for the population and empirical spectral fields. The source does not spell out identification of varying subspaces or whether roots are taken on a restricted space; the zero-spectrum issue is retained separately.')
add('D32','measure of deviation from stationarity',r'''
Now, define
\[
r_d(\eta)=\int_0^\pi\int_0^1d_R^2(\ddot{\mathscr F}_{\omega,d},\eta\mathscr F_{u,\omega,d})du d\omega\quad\text{and}\quad\widehat r_d(\eta)=\frac1M\sum_{u\in U_M}\int_0^\pi d_R^2(\widehat{\ddot{\mathscr F}}_{\omega,d}(\eta),\eta\widehat{\mathscr F}_{u,\omega,d}(\eta))d\omega
\]
where $d_R$ is the square root distance defined in (2.12), and where
\[
\widehat{\ddot{\mathscr F}}_{\omega,d}^{1/2}(\eta)=\frac1M\sum_{u\in U_M}(\eta\widehat{\mathscr F}_{u,\omega,d}(\eta))^{1/2}\quad\text{and}\quad\ddot{\mathscr F}_{\omega,d}^{1/2}(\eta)=\int_0^1(\eta\mathscr F_{u,\omega,d})^{1/2}du.\tag{3.46}
\]
''',[21],'Section 3.5.4 — sequential stationarity measures, equation (3.46)',{'D30':'Both quantities use the squared square root distance (2.12).','D31':'The population and empirical operators are the preceding spectral restrictions.','D13':'The empirical average uses grid U_M.'},context='3.5.4. A measure of deviation from stationarity based on the square root distance',symbols=[r'r_d(\eta)',r'\widehat r_d(\eta)',r'\ddot{\mathscr F}_{\omega,d}^{1/2}(\eta)'],shape='Paired restricted stationarity deviations with mean-square-root targets. The population definition of r_d omits eta on the dotted target while (3.46) defines an eta-dependent root; the source difference is retained rather than silently reconciled.')
add('D33','functional',r'''
To be precise, consider the class, say $\mathscr P$, of locally stationary functional time series models introduced in Section 2.1. Suppose that $X=\{X_{t,T}\mid t=1,\ldots,T;T\in\mathbb N\}$ is an element of the class $\mathscr P$, but that we want to work under an additional structural assumption. We denote by $\mathscr P'\subset\mathscr P$ the class of models satisfying this assumption. A typical example is a finite rank assumption on the operators in (2.3) made in (dynamic) FPCA, but several other examples were also given in Section 2.2. We assume that we can measure the deviation between an “optimal” model from the class $\mathscr P'$ and the “true” model in $\mathscr P$ by a functional of the spectral density operator defined in (2.2), say
\[
r=\mathscr T(\mathscr F),\tag{2.14}
\]
where $\mathscr T$ defines a mapping from the set of all time-varying spectral density operators onto the non-negative real line. Note that $r=0$ if the process $X$ is already an element of the class $\mathscr P'$.
''',[8],'Section 2.3 — general model-deviation functional, equation (2.14)',{'D2':'The generic model deviation is a nonnegative functional of the spectral family, without selecting a particular application.'},phrases=['functional'],symbols=[r'r=\mathscr T(\mathscr F)',r'\mathscr P\prime'],shape='General nonnegative model-deviation functional, zero on the restricted class. The finite-rank example is background and does not make the generic functional depend on a PCA construction.')
# Use an exact source expression rather than a typographic variant of the prime.
members['D33']['highlight_symbols']=[r'r=\mathscr T(\mathscr F)']
add('D34','hypotheses',r'''
Alternatively, it might also be of interest to investigate if the model deviation (measured by $r$) is smaller than a pre-specified constant, say $\Delta>0$. In order to make this decision a test for the hypotheses
\[
H_0:r\leq\Delta\text{ versus }H_1:r>\Delta\tag{2.15}
\]
would be desirable.
''',[8,9],'Section 2.3 — relevant model-deviation hypotheses, equation (2.15)',{'D33':'The hypotheses concern the nonnegative deviation functional r from (2.14).'},kind='condition',phrases=['hypotheses'],symbols=[r'H_0:r\leq\Delta',r'H_1:r>\Delta'],shape='Relevant deviation null at or below a strictly positive threshold, with a strict upper alternative. The direction is retained despite nearby prose discussing a desire to justify small deviation.')
add('D35','increasing sequence',r'''
More generally, consider an increasing sequence of (possibly simpler) model classes
\[
\mathscr P_1\subset\mathscr P_2\subset\mathscr P_3\subset\ldots\subset\mathscr P\tag{2.16}
\]
approximating the “true” model from the class $\mathscr P$, and let $r_d=\mathscr T_d(\mathscr F)$, $d\in\mathbb N$, denote a measure of the form (2.14) for the deviation between the “optimal” model in $\mathscr P_d$ and the given locally stationary functional time series in the class $\mathscr P$. In certain applications, we have $r_d\in[0,1]$ such that $s_d=1-r_d\in[0,1]$ satisfies $s_1<s_2<s_3<\ldots$ and $\lim_{d\to\infty}s_d=1$. Note that $s_d$ can be interpreted as a measure for the quality of the approximation of the process by models from the class $\mathscr P_d$, which is $1$ if the process is in fact an element of the class $\mathscr P_d$ (in this case the sequence is terminating).
''',[9],'Section 2.4 — model classes and approximation quality, equation (2.16)',{'D33':'The r_d are instances of the general deviation functional for the nested model classes.'},kind='source_passage',phrases=['increasing sequence'],symbols=[r's_d=1-r_d',r'\lim_{d\to\infty}s_d=1'],shape='Nested model classes and a strictly increasing accuracy sequence converging to one, with the source terminating-sequence convention. Section 4 uses T_d to denote accuracy rather than deviation; that notation change is retained.')
members['D35']['application_context']=[dict(text=r'As $s_d$ specifies the quality of approximation of the model from the class $\mathscr P_d$, it might be of interest to investigate if $s_{d_0}$ is larger than $\nu$, where $\nu\in(0,1)$ is a pre-specified constant (for example 95%). In order to make this decision at a controlled type I error we propose to construct a test for the hypotheses $H_0^{(d_0)}:s_{d_0}\leq\nu$ versus $H_1^{(d_0)}:s_{d_0}>\nu$.',evidence=[dict(page=9,location='Equation (2.17) and preceding threshold convention')])]
add('D36','minimal model complexity',r'''
If the quality of approximation of the given model by models from the class $\mathscr P_d$ is quantified by the measure $s_d$, we can define $d^*$ by
\[
d^*=\min\{d\in\mathbb N\mid s_d>v\}=\min\{d\in\mathbb N\mid1-s_d<1-v\}\tag{2.18}
\]
as the minimal model complexity such that $s_d^*>v$, and an important problem is to estimate $d^*$ from the given data.
''',[9,10],'Section 2.4 — minimal model complexity, equation (2.18)',{'D35':'The minimum uses the accuracy sequence of the nested models.'},phrases=['minimal model complexity'],symbols=[r'd^*=\min\{d\in\mathbb N\mid s_d>v\}'],shape='First positive integer with accuracy strictly above the threshold. The display uses Latin v and the following prose prints s_d^*; neither is silently changed. Later equality-boundary claims are retained separately.')
members['D36']['application_context']=[dict(text=r'$H_0:d^*\leq d_0\qquad H_1:d^*>d_0$.',evidence=[dict(page=10,location='Equation (2.19)')]),dict(text=r'$H_0:d^*>d_0\quad\text{versus}\quad H_1:d^*\leq d_0$.',evidence=[dict(page=24,location='Equation (4.9)')])]
add('D37','decision rule',r'''
This is equivalent to rejecting whenever
\[
\widehat r>\Delta-q_\alpha V=\Delta+q_{1-\alpha}V,\tag{4.3}
\]
and the following result describes the asymptotic properties of this decision rule.
''',[22],'Section 4.1 — relevant-deviation rejection rule, equation (4.3)',{'D24':'V and the quantiles q are supplied by the scalar pivotal distribution (4.1).','D34':'Delta is the positive threshold for the relevant deviation hypotheses.'},phrases=['decision rule'],symbols=[r'\widehat r>\Delta-q_\alpha V'],shape='One-sided rejection rule using the deviation estimate, its self-normalizer and a limiting-distribution quantile. The source equality between lower and upper quantile forms is preserved.')
add('D38','random variables',r'''
Assume that $s_d=\mathscr T_d(\mathscr F)=\mathscr T_d(\mathscr F)(1)$ for some functional $\mathscr T_d$, and define by $\widehat s_d=\mathscr T_{d,T}(\widehat{\mathscr F})(1)$ the corresponding estimator introduced in Section 3.2. As a consequence of the second part of Theorem 3.2, we obtain for $d=1,2,\ldots$ the convergence
\[
\frac{\widehat s_d-s_d}{V_{d,d}}=\frac{\mathscr T_{d,T}(\widehat{\mathscr F})(1)-\mathscr T_d(\mathscr F)(1)}{V_{dd}}\overset{\mathscr D}{\longrightarrow}\mathbb T_d=\frac{\mathbb B_d(1)}{\left(\int_0^1|f_d(\eta)\mathbb B_d\eta)-g_{dd}(1)\mathbb B_d(1)|^2\nu(d\eta)\right)^{1/2}},\tag{4.4}
\]
where $\mathbb B_d$ denotes a standard Brownian motion and $V_{dd}$ is defined in (3.37). We note that the limiting distribution in (4.4) depends only on $d$ through the functions $f_d$, $g_{dd}$ and the measure $\nu$ (which are known), and that the random variables $\mathbb T_1,\mathbb T_2,\ldots$ are not necessarily independent.
''',[23],'Section 4.2 — accuracy estimators and limiting variables, equation (4.4)',{'D20':'The accuracy and its estimate use the paired population and discrete functionals.','D23':'The denominator is the diagonal self-normalizer V_dd.','D21':'The known diagonal g and scalar Brownian motions are from the assumed limit representation.','D35':'s_d denotes the accuracy of the dth nested model.'},phrases=['random variables'],symbols=[r'\mathbb T_d',r'\widehat s_d=\mathscr T_{d,T}(\widehat{\mathscr F})(1)'],shape='Source family of scalar limiting variables and accuracy estimates. Formula (4.4) has the printed f_d/g_dd mismatch relative to (4.1), and an unclosed Brownian argument; those are retained. The variables need not be independent.')
add('D39','test statistic',r'''
For the construction of an estimator of $d^*$ let
\[
\widehat{\mathbb T}_d=\frac{\widehat s_d-\nu}{V_{d,d}}=\frac{\widehat s_d-s_d}{V_{d,d}}+\frac{s_d-\nu}{V_{d,d}}
\]
denote the test statistic for the hypotheses in (2.17) with $d_0=d$ (note that $H_0^{(d)}:s_d\leq\nu$ is rejected if $\widehat{\mathbb T}_d>q_{1-\alpha}$; see (4.3)).
''',[23,24],'Section 4.2.1 — threshold-centered test statistic',{'D38':'The statistic uses the accuracy estimate and its self-normalizer.','D35':'Nu is the target accuracy threshold from (2.17).'},phrases=['test statistic'],symbols=[r'\widehat{\mathbb T}_d'],shape='Threshold-centered accuracy statistic for each model index d. The unknown d* is mentioned as its eventual estimation target, not as an input required to compute the statistic.')
add('D40','estimator',r'''
We now define
\[
\widehat d=\min\{d\mid\widehat{\mathbb T}_d>q_\alpha\}\tag{4.8}
\]
as an estimator of $d^*$, where $q_\alpha$ is the $\alpha$-quantile of the distribution of $\mathbb T_d$ in (4.4). The following result provides consistency of the estimator $\widehat d$.
''',[24],'Section 4.2.1 — minimal-complexity estimator, equation (4.8)',{'D39':'The estimator finds the first threshold-centered statistic above its critical value.','D38':'The critical value is a quantile of the application-specific limiting variable T_d.'},phrases=['estimator'],symbols=[r'\widehat d=\min\{d\mid\widehat{\mathbb T}_d>q_\alpha\}'],shape='First model index whose statistic exceeds the lower alpha quantile, as printed. The quantile is not changed to 1-alpha. Its dependence on d and the range of the minimum come from surrounding source context; no finite search cutoff or tie rule is added.')
add('D41','decision rule',r'''
Therefore, it follows from (4.4) and the discussion in Section 4.1 that the decision rule, which rejects the null hypothesis in (4.9) (or equivalently in (2.17)) whenever
\[
\widehat s_{d_0}>\nu+q_{1-\alpha,d_0}V_{d_0,d_0},\tag{4.11}
\]
defines a reasonable test, where we recall that $q_{1-\alpha,d_0}$ denotes the $(1-\alpha)$-quantile of the distribution of the random variable $\mathbb T_{d_0}$ defined in (4.4).
''',[25],'Section 4.2.3 — accuracy rejection rule, equation (4.11)',{'D38':'The statistic uses the accuracy estimate, self-normalizer and d0-specific limiting quantile.','D35':'The threshold nu is the desired approximation accuracy.'},phrases=['decision rule'],symbols=[r'\widehat s_{d_0}>\nu+q_{1-\alpha,d_0}V_{d_0,d_0}'],shape='Accuracy-based test with the upper application-specific quantile. It differs from the first-exceedance estimator (4.8). The source equivalence of the two hypothesis formulations is recorded with its strict-boundary issue.')
# Preserve source-local empirical notation in addition to the population definitions.
members['D3'].setdefault('application_context',[]).append(dict(
    text=r'where $\widehat\lambda_1^{(u,\omega)}(\eta)$ and $\widehat\Pi_1^{(u,\omega)}(\eta)$ denote the largest eigenvalue and corresponding projector of $\widehat{\mathscr F}_{u,\omega}(\eta)$, respectively,',
    evidence=[dict(page=14,location='After equation (3.14) — empirical spectral notation')]))
members['D29'].setdefault('application_context',[]).append(dict(
    text=r'''As a sequential estimator of a measure of $d$-th order functional canonical coherence over the time-frequency interval $[0,1]\times[a,b]$, consider
\[
\widehat s_d(\eta)=\mathscr T_T(\widehat{\mathscr F})(\eta)=\frac1M\sum_{u\in U_M}\int_a^b\widehat{\mathscr R}_d^{u,\omega}(\eta)d\omega,
\]
where $(\widehat{\mathscr R}_d^{u,\omega}(\eta))^2=(\widehat\nu_d^{u,\omega}(\eta))^2/(\widehat\lambda_{11,d}^{(u,\omega)}(\eta)\widehat\lambda_{22,d}^{(u,\omega)}(\eta))$, and where $\widehat\nu_d(\eta)$, $\widehat\lambda_{11,d}^{(u,\omega)}(\eta)\widehat\lambda_{22,d}^{(u,\omega)}(\eta)$ are the sequential estimators of the quantities $\nu_d(\eta)$, $\lambda_{11,d}^{(u,\omega)}(\eta)\lambda_{22,d}^{(u,\omega)}(\eta)$ which were defined in Section 2.2.3.''',
    evidence=[dict(page=20,location='Section 3.5.3 — empirical coherence'),dict(page=21,location='Section 3.5.3 — continuation defining the squared ratio')]))
# Correct a typesetting-only prime transcription, without altering the tensor identities.
for ctx in members['D26'].get('application_context',[]):
    ctx['text']=ctx['text'].replace(r'a\prime',r'a^{\prime}').replace(r'b\prime',r'b^{\prime}')
interfaces[-1]['type_shape']=interfaces[-1]['semantic_boundary']=(
    'Accuracy-based test with the upper application-specific quantile. It differs from the first-exceedance estimator (4.8). '
    'For the strict threshold definition (2.18), monotonicity makes (4.9) equivalent to (2.17), including equality at s_d0=nu. '
    'The separate equality case s_d*=nu in (4.6) conflicts with that strict definition and is documented in the ambient source notes.')
(ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
(ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
print('Saved',len(interfaces),'source-backed interfaces; extraction and theorem connections remain in progress.')
