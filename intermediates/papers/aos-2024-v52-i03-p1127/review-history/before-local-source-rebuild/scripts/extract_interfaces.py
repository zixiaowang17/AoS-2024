"""Extract original main-text diffusion prerequisites; appendices remain excluded."""
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
add('D1','stochastic differential equation',r'''
For the problem of similarity testing, we assume throughout that a continuous record of observations $(X_t)_{t\in[0,T]}$ is available, where $X$ denotes an Itô diffusion satisfying the one-dimensional homogeneous stochastic differential equation (SDE) of the form
\[
dX_t=b(X_t)dt+\sigma dW_t,\qquad X_0=\xi,\tag{2.1}
\]
with drift $b:\mathbb R\to\mathbb R$, $\sigma>0$, $W=(W_t)_{t\ge0}$ a standard one-dimensional Brownian motion and initial condition $\xi$ independent of $W$.
''',[6],'Section 2 — diffusion observation model (2.1)',kind='assumption',symbols=[r'dX_t=b(X_t)dt+\sigma dW_t',r'X_0=\xi'],shape='Continuous observation of a scalar time-homogeneous diffusion with constant positive diffusion coefficient and initial value independent of its Brownian driver. Stationarity is a separate assumption, not built into this SDE.')
add('D2','drift',r'''
For arbitrary but fixed constants $A,\gamma,\sigma>0$ and $C\ge1$, the drift $b$ belongs to
\[
\Sigma(C,A,\gamma,\sigma):=\left\{b\in\mathrm{Lip}_{\mathrm{loc}}(\mathbb R):|b(x)|\le C(1+|x|)\ \forall x\in\mathbb R\quad\text{and}\quad\frac{b(x)}{\sigma^2}\operatorname{sign}(x)\le-\gamma\ \forall |x|\ge A\right\}.
\]
Here, $\mathrm{Lip}_{\mathrm{loc}}(\mathbb R)$ denotes the local Lipschitz functions on $\mathbb R$, see Appendix D.
''',[6],'Section 2 — drift class',symbols=[r'\Sigma(C,A,\gamma,\sigma)'],shape='Locally Lipschitz drifts with a global linear growth bound and inward drift outside [-A,A]. This is a function class parametrized by the diffusion scale, not an assumption of stationarity. Keep tightened reference-drift parameters in individual theorem statements.')
add('D3','invariant probability density',r'''
For each $b\in\Sigma(C,A,\gamma,\sigma)$ we denote this invariant measure by $\mu_b$ and it is a classical result (cf. [34, Theorem 1.16]) that it admits the invariant probability density
\[
q_b(x):=\frac1{C_{b,\sigma}}\exp\left(\int_0^x\frac{2b(y)}{\sigma^2}\,dy\right)\qquad\text{for all }x\in\mathbb R,
\]
with normalizing constant $C_{b,\sigma}$. For $x<0$ the integral should be read as $\int_0^x f(y)dy=-\int_x^0 f(y)dy$.
''',[6],'Section 2 — invariant measure and density',{'D2':'The invariant density is defined for drifts in Sigma(C,A,gamma,sigma).'},symbols=[r'q_b(x)',r'\mu_b'],shape='Normalized exponential integral density for the drift class and constant sigma. The signed orientation of the integral for negative x is explicit. Its use as a deterministic weight does not require a stationary initial observation.')
add('D4',['stationary and ergodic','law'],r'''
For ease of presentation, we assume that $\xi\sim\mu_b$ such that $X$ is stationary and ergodic. Extensions are possible, see Remark 5.5. Subsequently, we denote by $\mathbb P_b$ the law of $X$ satisfying (2.1) with drift $b$ and by $\mathbb E_b$ the corresponding expectation.
''',[6],'Section 2 — stationary initial law and probability notation',{'D1':'The law concerns the observed solution of (2.1).','D3':'The initial value has the invariant measure mu_b.'},kind='assumption',symbols=[r'\xi\sim\mu_b',r'\mathbb P_b',r'\mathbb E_b'],shape='Stationary experiment and its drift-indexed probability and expectation in Sections 2–5 and 7. Section 6 explicitly replaces the initial law by a fixed x0 and uses an unsubscripted common coupling probability; that experiment must not inherit this stationary-start condition.')
add('D5','bounded function',r'''
For any set $I\subset\mathbb R$ and bounded function $f:I\to\mathbb R$ we denote
\[
\|f\|_I:=\sup_{z\in I}|f(z)|.
\]
''',[7],'Section 2 — supremum norm notation',symbols=[r'\|f\|_I'],shape='Pointwise supremum norm on the specified set, not an essential supremum. The same notation is used for drift differences and kernel bounds; Lebesgue L2 is separate ambient notation.')
add('D6','testing problem',r'''
The precise testing problem we address in this section is given for some $b_0\in\Sigma(C/2,A,\gamma,\sigma)$ by
\[
H_0:\|b-b_0\|_{[-A,A]}=0\tag{3.1}
\]
versus one of the following alternatives:
\[
H_{\ne}:\left\{\|b-b_0\|_{[-A,A]}>0\right\}\cap\Sigma(C,A,\gamma,\sigma),
\]
''',[7],'Section 3 — simple-null and two-sided alternative (3.1)',{'D2':'The reference drift and alternatives are constrained by the drift class.','D5':'Equality and deviation are measured in the pointwise norm on [-A,A].'},symbols=[r'H_{\ne}',r'\|b-b_0\|_{[-A,A]}=0'],shape='Excerpt of the simple-null testing problem and its two-sided alternative. Equality is only on [-A,A], not an imposed equality of drift functions on all of R. The one-sided alternatives on the following lines are not prerequisites of the stored Theorems.')
add('D7','localized deviations',r'''
The idea is now to develop a multiple test in the spirit of [21] that simultaneously tests all locations with likelihood ratio statistics of localized deviations
\[
K_{y,h}(x):=K\left(\frac{x-y}{h}\right),\qquad x\in\mathbb R,
\]
with different scaling parameters $h>0$.
''',[8],'Section 3.1 — localized kernel deviations',symbols=[r'K_{y,h}(x)'],shape='Translated and rescaled kernel without a 1/h amplitude factor. Conditions on the base kernel differ by theorem and are not imposed by this scaling definition.')
add('D8','standardized local log-likelihood statistic',r'''
Thus, the standardized local log-likelihood statistic is given by
\[
\Psi_{T,y,h}^{b_0}(X):=\frac{\int_0^T K_{y,h}(X_s)dX_s-\int_0^T K_{y,h}(X_s)b_0(X_s)ds}{\sigma\sqrt{\int_0^T K_{y,h}(X_s)^2ds}},\tag{3.2}
\]
where $\Psi_{T,y,h}^{b_0}(X):=0$ if the denominator equals zero.
''',[8],'Section 3.1 — local statistic (3.2)',{'D1':'The numerator contains the stochastic integral against the observed diffusion.','D7':'All integrands use the localized kernel K_y,h.'},symbols=[r'\Psi_{T,y,h}^{b_0}(X)'],shape='Drift-centered local statistic normalized by the square root of its quadratic variation, with an explicit zero-denominator convention. This formula is a path statistic and does not require stationary initialization to define it.')
add('D9',['locations','scaling parameters'],r'''
The following result shows that the local statistics $\Psi_{T,y,h}^{b_0}(X)$ in (3.2) can be combined for all $(y,h)$ within
\[
\mathcal T:=\{(y,h)\mid h\in(0,A]\text{ and }y\in[-A+h,A-h]\}\cap(\mathbb Q\times\mathbb Q)\tag{3.3}
\]
in a specific way that enables to construct the desired multiple test.
''',[8],'Section 3.1 — rational location-bandwidth index set (3.3)',context=r'''The idea is now to develop a multiple test in the spirit of [21] that simultaneously tests all locations with likelihood ratio statistics of localized deviations $K_{y,h}(x):=K\left(\frac{x-y}{h}\right)$, $x\in\mathbb R$, with different scaling parameters $h>0$.''',symbols=[r'\mathcal T',r'\mathbb Q\times\mathbb Q'],shape='Countable rational pairs of positive bandwidth and location for intervals contained in [-A,A]. Mention of Psi motivates the index set but is not a prerequisite of its set-builder definition.')
add('D10','quadratic variation',r'''
Define
\[
\widehat\sigma_T(y,h)^2:=\frac1T\int_0^T K_{y,h}(X_s)^2\,ds\quad\text{and}\quad\widehat\sigma_{T,\max}^2:=\frac1T\int_0^T\mathbb1_{[-A,A]}(X_s)^2\,ds.
\]
''',[8,9],'Theorem 3.1 — empirical scale definitions',{'D7':'The local scale averages squared localized kernel values.'},kind='theorem_excerpt',context=r'''Whereas an additive correction for centering under $\mathbb P_{b_0}$ is obvious, we do not divide by the standard deviation of the stochastic integral $\sigma^{-1}\int_0^T K_{y,h}(X_s)dW_s$ for normalizing the variance, but choose its random analogue, the square root of its quadratic variation, which is purely data dependent.''',symbols=[r'\widehat\sigma_T(y,h)^2',r'\widehat\sigma_{T,\max}^2'],shape='Time-normalized occupation integrals supplying empirical quadratic-variation scales. The maximum scale retains the printed squared indicator. The naming context concerns the normalization construction, not an assertion that these time averages equal the unnormalized quadratic variation.')
add('D11','correction',r'''
where $0/0:=0$ in the argument of $\Upsilon(\cdot)$ and
\[
\Upsilon(r):=(2\log(1/r))^{\frac12}\mathbb1_{\{r>0\}}.
\]
''',[9],'Theorem 3.1 — multiscale correction and ratio convention',kind='theorem_excerpt',context=r'''Various variants of identifying the above correction $\Upsilon(\cdot)$ have been established in the theory of multiscale testing, see for example [20], [21] or [44].''',symbols=[r'\Upsilon(r)'],shape='Logarithmic scale correction with the source convention for a zero-over-zero argument. The intended scale ratios lie in [0,1]; the printed indicator expression at zero must not be interpreted as ordinary multiplication of an undefined logarithm.')
add('D12','global test statistic',r'''
With these preliminaries we now define the global test statistic
\[
T_T^{b_0}(X):=\sup_{(y,h)\in\mathcal T}\left(|\Psi_{T,y,h}^{b_0}(X)|-\Upsilon\bigl(\widehat\sigma_T(y,h)^2/\widehat\sigma_{T,\max}^2\bigr)\right).\tag{3.4}
\]
''',[9],'Section 3.1 — global statistic (3.4)',{'D8':'The supremum uses the absolute local centered statistic.','D9':'The supremum runs over the rational location-bandwidth set.','D10':'The correction argument is the empirical local-to-maximum scale ratio.','D11':'The empirical ratio is penalized by Upsilon, with its zero convention.'},symbols=[r'T_T^{b_0}(X)'],shape='Two-sided multiscale statistic for reference drift b0. Its definition is separate from calibration under the stationary null law; T7.1 instantiates the reference drift by b.')
add('D13','quantiles',r'''
Theorem 3.1 ensures that the corresponding quantiles
\[
\kappa_{T,\alpha}^{\ne b_0}:=\min\left\{r\in\mathbb R\mid\mathbb P_{b_0}\left(T_T^{b_0}(X)\le r\right)\ge1-\alpha\right\}\tag{3.5}
\]
''',[9],'Section 3.1 — null-law quantiles (3.5)',{'D4':'Calibration is under the drift-b0 stationary law.','D12':'The quantile concerns the global two-sided statistic.'},symbols=[r'\kappa_{T,\alpha}^{\ne b_0}'],shape='Finite-T lower quantile using the printed minimum and a non-strict CDF inequality. This differs from the limiting similarity threshold kappa_eta,alpha.')
add('D14','resulting test',r'''
An asymptotic power investigation of the resulting test
\[
\phi_T^{b_0}(X)=\mathbb1_{\{T_T^{b_0}(X)>\kappa_{T,\alpha}^{\ne b_0}\}}\tag{3.6}
\]
is given in Section 5.
''',[9],'Section 3.1 — two-sided test (3.6)',{'D12':'The test rejects on a large value of the global statistic.','D13':'The threshold is its finite-T stationary-null quantile.'},symbols=[r'\phi_T^{b_0}(X)'],shape='Indicator test with a strict rejection inequality at the finite-T null-law threshold.')
add('D15','composite null hypothesis',r'''
Therefore, letting $\eta\ge0$ and choosing a reference drift $b_0$ we formulate the composite null hypothesis as
\[
H_0(b_0,\eta):=\left\{b\mid\|b-b_0\|_{[-A,A]}\le\eta\right\}\cap\Sigma(C,A,\gamma,\sigma).
\]
This composite hypothesis will be tested against its complement within $\Sigma(C,A,\gamma,\sigma)$, i.e.
\[
H_1(b_0,\eta):=\left\{b\mid\|b-b_0\|_{[-A,A]}>\eta\right\}\cap\Sigma(C,A,\gamma,\sigma).\tag{4.1}
\]
''',[10],'Section 4 — similarity hypotheses (4.1)',{'D2':'Both hypotheses are intersected with the admissible drift class.','D5':'The similarity band is a supremum-norm bound on [-A,A].'},symbols=[r'H_0(b_0,\eta)',r'H_1(b_0,\eta)'],shape='Closed similarity band and its strict complement inside Sigma. Eta=0 recovers equality on the observation interval; the source description as a singleton does not impose global equality outside it.')
add('D16','localized statistics',r'''
\[
\Lambda_{T,y,h}^\eta(X):=\frac{\eta\int_0^T K_{y,h}(X_s)ds}{\sigma\sqrt{\int_0^T K_{y,h}(X_s)^2ds}},
\]
where $0/0$ is read as zero.
''',[11],'Section 4 — local similarity adjustment after (4.2)',{'D7':'The adjustment uses first and second occupation integrals of K_y,h.'},context=r'''Combining those localized statistics in the same way as in Section 3 for $(y,h)\in\mathcal T$ given in (3.3) then yields the ansatz''',symbols=[r'\Lambda_{T,y,h}^\eta(X)'],shape='Tolerance adjustment subtracted from the absolute local statistic, with explicit zero-over-zero convention. The source phrase localized statistics refers to the adjusted expression (4.2); this member isolates its defined Lambda term.')
add('D17','test statistic',r'''
\[
T_T^\eta(X):=\sup_{(y,h)\in\mathcal T}\left(\left|\Psi_{T,y,h}^{b_0}(X)\right|-\Lambda_{T,y,h}^\eta(X)-\Upsilon\bigl(\widehat\sigma_T(y,h)^2/\widehat\sigma_{T,\max}^2\bigr)\right)\tag{4.3}
\]
as a test statistic for $H_0(b_0,\eta)$ against $H_1(b_0,\eta)$ given in (4.1).
''',[11],'Section 4 — similarity statistic (4.3)',{'D8':'The statistic takes the absolute drift-centered local score.','D9':'The supremum runs over the rational index set.','D10':'The empirical occupation scales form the correction ratio.','D11':'Upsilon supplies the multiscale correction.','D16':'Lambda subtracts the local tolerance adjustment.'},symbols=[r'T_T^\eta(X)'],shape='Similarity statistic with local tolerance and multiscale corrections. The hypothesis names in the following motivation do not enter its formula and do not impose a null-law restriction on its definition.')
inventory=json.loads((ROOT/'theorem-inventory.json').read_text())
claim_text={c['claim_id'].split('/')[-1]:c['statement_original'] for c in inventory['claims']}
add('D18','limiting statistics','where $U_1\\vee U_2$'+claim_text['T4.1'].split('where $U_1\\vee U_2$')[1],[12,13],'Theorem 4.1 — Gaussian limiting statistics',{'D3':'The Gaussian integrals and their normalizers use invariant densities at the two boundary drifts b0 plus or minus eta.','D7':'The integrands contain localized kernel functions.','D9':'Both suprema use the rational location-bandwidth set.','D11':'The local Gaussian ratios use the same correction Upsilon.'},kind='theorem_excerpt',context=r'''The limiting statistics $U_1$ and $U_2$ in Theorem 4.1 are almost surely finite''',symbols=[r'U_1',r'U_2'],shape='Two boundary-drift Gaussian supremum statistics driven by the same W in the source. Do not assume independence of U1 and U2. The L2 norms use Lebesgue measure and the normalizer for the maximum scale is the interval indicator.')
add('D19','quantiles',r'''
\[
\kappa_{\eta,\alpha}:=\min\left\{r\in\mathbb R:\mathbb P\left(U_1\vee U_2+4\sqrt{A\eta/\sigma^2}\le r\right)\ge1-\alpha\right\}\tag{4.6}
\]
''',[13],'Section 4 — limiting similarity quantiles (4.6)',{'D18':'Calibration uses the maximum of the two Gaussian boundary-drift statistics plus the deterministic shift.'},context=r'''The limiting statistics $U_1$ and $U_2$ in Theorem 4.1 are almost surely finite which can be seen analogously to Theorem 3.1 and hence the quantiles''',symbols=[r'\kappa_{\eta,\alpha}'],shape='Lower quantile of the limiting dominating random variable, with the printed minimum and non-strict CDF inequality. This threshold does not depend on T and is not a finite-T null-law quantile.')
add('D20','test',r'''
For the testing problem $H_0(b_0,\eta)$ versus the alternative (4.1), the test
\[
\phi_T^\eta(X)=\mathbb1_{\{T_T^\eta(X)>\kappa_{\eta,\alpha}\}}\tag{4.7}
\]
''',[13],'Section 4 — similarity test (4.7)',{'D17':'The rejection event uses the similarity statistic.','D19':'Its threshold is the limiting dominating-law quantile.'},symbols=[r'\phi_T^\eta(X)'],shape='Indicator test with strict rejection at the limiting threshold. Its use for testing H0 versus H1 is motivation, while its formula is determined by the statistic and threshold.')
add('D21','distance',r'''
When establishing minimax rates and optimal constants it is crucial to specify a distance between a given function $b$ and the null $H_0(b_0,\eta)$. We define this distance as
\[
\Delta_J(b):=\inf_{\widetilde b\in H_0(b_0,\eta)}\left\||b-\widetilde b|\left(\frac{q_b}{\sigma^2}\right)^{\frac\beta{2\beta+1}}\right\|_J\tag{5.1}
\]
with compact $J\subset(-A,A)$ to avoid boundary effects. For $b\notin H_0(b_0,\eta)$ it is given by
\[
\Delta_J(b)=\sup_{x\in J}\left(|b(x)-b_0(x)|-\eta\right)\left[\frac{q_b(x)}{\sigma^2}\right]^{\frac\beta{2\beta+1}}
\]
which corresponds to the boundary cases $\widetilde b=b_0\pm\eta$.
''',[13,14],'Section 5.1 — weighted distance from the similarity null (5.1)',{'D15':'The distance minimizes over the similarity null.','D3':'The pointwise weight depends on the alternative drift through q_b.','D5':'The loss inside the infimum is the supremum norm on J.'},symbols=[r'\Delta_J(b)'],shape='Distance to the similarity null with a drift-dependent density and noise weight, measured on an interior compact set. Preserve the following printed expression without adding a positive part: it can conflict with the nonnegative infimum definition when the violation of the band is outside J.',note='The second displayed expression omits a positive part. The infimum-of-norms definition is nonnegative, while the displayed supremum can be negative if b leaves the similarity band only outside J. Both original expressions are retained; no correction is silently substituted.')
add('D22','Hölder class',r'''
For $\beta,L>0$ the Hölder class $\mathcal H(\beta,L)$ is given by the set of functions $f:\mathbb R\to\mathbb R$ such that for each $k=0,\ldots,\lfloor\beta\rfloor$ the Hölder-condition
\[
\left|f^{(\lfloor\beta\rfloor)}(x)-f^{(\lfloor\beta\rfloor)}(y)\right|\le L|x-y|^{\beta-\lfloor\beta\rfloor}
\]
is valid, where $f^{(n)}$ denotes the $n$-th derivative of $f$ and $\lfloor\beta\rfloor$ the maximal integer strictly smaller than $\beta$.
''',[14],'Section 5.2 — Hölder class and strict lower integer convention',symbols=[r'\mathcal H(\beta,L)',r'\lfloor\beta\rfloor'],shape='Global derivative Hölder condition with the maximal integer strictly smaller than beta, including at integer beta. The printed quantifier over k does not reappear in its displayed condition; do not add sup-norm derivative bounds or replace the author’s integer convention by the usual floor.',note='At beta=1 the printed lower integer is zero, so H(1,L) is the global Lipschitz class with constant L. The displayed inequality does not use the preceding quantified k.')
add('D23','rate',r'''
For this aim, we define the rate
\[
\delta_T=\delta_T(\beta):=\left(\frac{\log T}{T}\right)^{\frac\beta{2\beta+1}}
\]
''',[14],'Section 5.2 — separation rate',symbols=[r'\delta_T(\beta)',r'\delta_T'],shape='Logarithmic nonparametric separation rate indexed by observation horizon and smoothness. It differs from the Hurst-neighborhood sequence delta(T,epsilon) locally bound in Theorem 6.5.')
add('D24','constant',r'''
and constant
\[
c_*=c_*(\beta,L):=\left(\frac{2L^{\frac1\beta}}{(2\beta+1)\|K_\beta\|_{L^2}^2}\right)^{\frac\beta{2\beta+1}}.\tag{5.2}
\]
''',[14],'Section 5.2 — sharp separation constant (5.2)',{'D25':'The constant uses the squared Lebesgue L2 norm of the optimal recovery kernel.'},symbols=[r'c_*(\beta,L)',r'c_*'],shape='Sharp separation constant with a subscript star, depending on beta and L and the optimal-recovery kernel. It is not the arbitrary sufficient constant c(beta,L,K) in Theorem 5.2.')
add('D25','optimal recovery kernel',r'''
Here $K_\beta$ is the unique solution of the following optimization problem:
\[
\text{Minimize }\|K\|_{L^2}\text{ over all }K\in\mathcal H(\beta,1)\text{ with }K(0)\ge1.\tag{5.3}
\]
We call $K_\beta$ the optimal recovery kernel. In the case $0<\beta\le1$ it is not difficult to see that
\[
K_\beta(x)=\mathbb1_{\{|x|\le1\}}\left(1-|x|^\beta\right),
\]
''',[14],'Section 5.2 — optimal recovery kernel (5.3)',{'D22':'The optimization constrains K to the paper’s Holder class with constant one.'},symbols=[r'K_\beta',r'K(0)\ge1'],shape='Unique minimizer of the Lebesgue L2 norm under the Holder constraint and pointwise height lower bound. The explicit supported formula is stated only for beta<=1; do not extend it to every beta.')
add('D26','kernel function',r'''a non-negative continuous kernel function $K$ of bounded variation supported in $[-1,1]$ with $\|K\|_{[-1,1]}\le1$.''',[12],'Theorem 4.1 — kernel condition',{'D5':'The bound is the pointwise supremum norm on [-1,1].'},kind='condition',symbols=[r'\|K\|_{[-1,1]}\le1'],phrases=['non-negative continuous kernel function'],shape='Kernel condition reused by Theorem 7.1 and strengthened to C1 in Section 6.1. Unlike Theorem 3.1 it includes nonnegativity; unlike Theorem 5.2 it has norm at most one and explicitly states continuity. No nonzero-kernel condition is printed.')
add('D27','kernel',r'''a non-negative kernel of bounded variation supported in $[-1,1]$ with $\|K\|_{[-1,1]}=1$.''',[16],'Theorem 5.2 — kernel condition',{'D5':'The unit normalization is in the pointwise supremum norm.'},kind='condition',symbols=[r'\|K\|_{[-1,1]}=1'],phrases=['non-negative kernel'],shape='Kernel condition explicitly inherited in Theorem 5.3. The norm equals one; continuity is not separately restated in this condition. Preserve these differences from the kernel condition in Theorem 4.1.')
add('D28','continuously differentiable',r'''To this aim, we assume in addition the kernel $K$ to be continuously differentiable''',[18],'Section 6.1 — additional kernel differentiability',{'D26':'The preceding sentence requires the kernel to satisfy Theorem 4.1, before adding continuous differentiability.'},kind='condition',phrases=['continuously differentiable'],shape='C1 strengthening of the nonnegative continuous bounded-variation kernel condition from Theorem 4.1, for the pathwise extension only. A derivative of the scaled kernel is used in the extension formula.')
add('D29','pathwise definition',r'''
On the right-hand side, it is perfectly possible to insert any continuous function $f\in \mathcal C([0,T])$. Therefore, we define
\[
\begin{aligned}
\widetilde I_T:\mathcal C([0,T])&\longrightarrow\mathbb R,\\
f&\longmapsto\int_{f(0)}^{f(T)}K_{y,h}(z)dz-\frac{\sigma^2}2\int_0^T(K_{y,h})'(f(s))ds.
\end{aligned}
\]
''',[18],'Section 6.1 — pathwise extension of the stochastic integral',{'D7':'The ordinary integrals use the localized kernel and its derivative.','D28':'Section 6.1 imposes continuous differentiability of the kernel.'},context=r'''To give a pathwise definition, we have to generalize the test statistic.''',symbols=[r'\widetilde I_T'],shape='Ordinary-integral functional on continuous paths obtained from the Ito formula with the fixed sigma^2/2 correction. It also depends on y,h although the source symbol suppresses them. Its definition is deterministic and does not impose stationarity or a fractional-noise law.')
add('D30','real-valued continuous functions',r'''
Let
\[
D_{A,T}:=\{f\in \mathcal C([0,T])\mid -A,A\in f([0,T])\}
\]
be the set of real-valued continuous functions $f$ on $[0,T]$ whose image set $f([0,T])$ contains the interval $[-A,A]$.
''',[18],'Section 6.1 — domain of the pathwise statistic',symbols=[r'D_{A,T}'],shape='Continuous real-valued paths visiting both -A and A, equivalently containing the entire interval in their image. This is a path-domain requirement, not a support restriction on the driving Brownian motion.')
add('D31','pathwise definition',r'''
For any $f\in D_{A,T}$ we denote
\[
\widetilde\Psi_{T,y,h}^{b_0}(f):=\frac{\widetilde I_T(f)}{\sigma\sqrt{\int_0^T K_{y,h}(f(s))^2ds}}-\frac{\int_0^T K_{y,h}(f(s))b_0(f(s))ds}{\sigma\sqrt{\int_0^T K_{y,h}(f(s))^2ds}}.\tag{6.1}
\]
''',[18],'Section 6.1 — extended local statistic (6.1)',{'D29':'The stochastic-integral term is replaced by the pathwise ordinary-integral functional.','D30':'The input f is restricted to the path domain D_A,T.','D7':'The centering and normalizing occupation integrals use the localized kernel.'},context=r'''To give a pathwise definition, we have to generalize the test statistic.''',symbols=[r'\widetilde\Psi_{T,y,h}^{b_0}(f)'],shape='Extension of the local score to continuous paths by substituting the deterministic integral functional. The adjacent naming context identifies the pathwise extension; the stochastic integral in the original Psi is not required to evaluate this extension.')
add('D32','implementation',r'''Additionally, as a consequence of Remark B.1 in Appendix B on implementation, it is sufficient to restrict attention to $\mathcal T_T:=\{(y,h)\in\mathcal T\mid h\ge h_{\min}(T)\}$.''',[19],'Section 6.1 — restricted bandwidth index set',{'D9':'The truncated set restricts the original rational location-bandwidth pairs.'},symbols=[r'\mathcal T_T',r'h_{\min}(T)'],shape='Index set with a minimum bandwidth. The main text gives the set-builder formula but refers to Appendix B for its implementation threshold; its exact h_min(T) choice remains unresolved within the permitted source scope.',note='Remark B.1 is in the excluded supplement. No formula for h_min(T) is supplied in the inspected main text; the source reference is retained without inventing a threshold.')
add('D33','extended test statistic',r'''
Based on those $\widetilde\Psi_{T,y,h}^{b_0}(f)$, the final extended test statistic is given pathwise by
\[
\widetilde T_T^\eta(f):=\sup_{(y,h)\in\mathcal T_T}\left(\left|\widetilde\Psi_{T,y,h}^{b_0}(f)\right|-\Lambda_{T,y,h}^\eta(X)-\Upsilon\bigl(\widehat\sigma_T(y,h)^2/\widehat\sigma_{T,\max}^2\bigr)\right).
\]
Here, $\widehat\sigma_T(y,h)$, $\widehat\sigma_{T,\max}$, $\Lambda_{T,y,h}^\eta(X)$ and $\Upsilon(\cdot)$ are defined as in Section 3 and 4 where no problem occurs as all involved integrals are classical integrals.
''',[19],'Section 6.1 — extended similarity statistic',{'D31':'The local scores are their pathwise extensions.','D32':'The supremum uses the minimum-bandwidth restricted set.','D16':'The source reuses the local tolerance integral, still printing X in the displayed formula.','D10':'The occupation scales are reused as classical integrals.','D11':'The same Upsilon correction is retained.'},symbols=[r'\widetilde T_T^\eta(f)'],shape='Pathwise similarity statistic on D_A,T with a restricted bandwidth set. Preserve the source X in Lambda although f is the functional argument; the surrounding prose describes evaluation by ordinary integrals along the input path.',note='The displayed formula keeps X in Lambda while defining a function of f. The source also claims the path-domain restriction prevents zero denominators, although its inherited kernel condition does not exclude K identically zero. These are recorded source issues, not repaired hypotheses.')
add('D34','fractional Brownian motion',r'''
where $W^H$, $H\in(0,1)$, is a fractional Brownian motion, i.e. a Gaussian process with covariance structure
\[
R_H(t,s)=\mathbb E\left[W_t^H W_s^H\right]=\frac12\left(t^{2H}+s^{2H}-|t-s|^{2H}\right).\tag{6.3}
\]
''',[19],'Section 6.2 — fractional Brownian covariance (6.3)',symbols=[r'R_H(t,s)',r'W_t^H W_s^H'],shape='Fractional Brownian noise with Hurst parameter in (0,1) and the printed covariance. Its marginal covariance does not specify the joint coupling across different Hurst parameters.')
add('D35','same probability space',r'''
Throughout this section we fix a probability space $(\Omega,\mathcal A,\mathbb P)$ that supports a Brownian motion $W=(W_t)_{t\ge0}$. As we are interested in convergence for varying Hurst parameter $H$ it is important that all $W^H$ are defined on the same probability space. Therefore, we define $W^H=(W_t^H)_{t\in[0,T]}$ by
\[
W_t^H:=\int_0^t K_H(t,s)dW_s,
\]
where $K_H$ is some kernel function specified in (I.8). One also has that $W^H|_{H=1/2}=W$ is a standard Brownian motion.
''',[19,20],'Section 6.2 — common-noise coupling across Hurst parameters',{'D34':'The coupled processes have the fractional Brownian covariance specified in (6.3).'},symbols=[r'K_H(t,s)',r'W^H|_{H=1/2}=W'],shape='All fractional noises are built by Volterra integrals against one Brownian motion on the same probability space. The specific K_H is deferred to excluded Appendix I, equation (I.8), so the exact cross-H coupling is not fully defined in the permitted text.',note='The common representation is stated in the main text; the formula for K_H is not. Covariance (6.3) alone cannot replace the joint coupling needed by the probability convergence in Theorem 6.3.')
add('D36','dynamics',r'''
As an example beyond a common semimartingale or Markovian setup with non-trivial dependence structure in the driving noise, we consider dynamics of the form
\[
dX_t^H=b(X_t^H)dt+\sigma dW_t^H,\qquad X_0^H=x_0,\tag{6.2}
\]
''',[19],'Section 6.2 — fractional-noise diffusion model (6.2)',{'D34':'The additive noise is fractional Brownian motion with parameter H.'},kind='assumption',symbols=[r'dX_t^H=b(X_t^H)dt+\sigma dW_t^H',r'X_0^H=x_0'],shape='Scalar additive fractional-noise dynamics with fixed initial condition. The coupling across H and the drift regularity restrictions are separately stated; stationarity is not assumed.')
add('D37','solution process',r'''
As we are interested to compare our results for the case $H=1/2$ with the fractional model, we restrict ourselves to Lipschitz continuous $b\in\Sigma(C,A,\gamma,\sigma)$. For such $b$ we denote the solution process of (6.2) by $X^{H,b}$ and by $X^b$ the solution of (2.1) for drift $b$ and initial condition $x_0$, respectively.
''',[20],'Section 6.2 — coupled solutions with the same fixed initial value',{'D1':'The Brownian comparison solution solves (2.1), here with fixed initial value x0.','D2':'The drift belongs to Sigma and is additionally globally Lipschitz.','D35':'Section 6 uses the common Brownian-driver construction of all fractional noises.','D36':'The fractional member solves (6.2) with the same x0.'},symbols=[r'X^{H,b}',r'X^b'],shape='Pair of fractional and Brownian solutions under the same drift and fixed initial condition, coupled through one Brownian driver. The probability and expectation are the common unsubscripted P,E, not the stationary law P_b of Section 2.')
add('D38','dual bounded Lipschitz metric',r'''Here, $d_{BL}$ denotes the dual bounded Lipschitz metric which metrizes weak convergence and is given in Appendix F.1. The superscript $b$ in $d_{BL}^b$ indicates the dependence of the distribution of $X$ on $b$.''',[24],'Section 7.1 — weak-convergence metric following Theorem 7.1',kind='source_passage',symbols=[r'd_{BL}^b'],shape='Named probability-law metric used by Theorem 7.1, with b marking the observed-process law. The exact bounded-Lipschitz norm/unit-ball convention is deferred to Appendix F.1. Page 25 names the closed unit ball of bounded Lipschitz functions but still refers to that appendix for its definition.',note='The main text identifies the metric and its role. Its exact normalization remains unresolved because the defining Appendix F.1 is excluded; no formula is imported from a different convention.')

if __name__=='__main__':
    for lid,m in members.items():
        assert all(d in members for d in m['depends_on']),(lid,'unknown dependency')
        assert any(s in m['statement_original']+' '+m['local_label'] for s in m['highlight_symbols']+m['highlight_phrases']),(lid,'missing own-source highlight')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,status='extracted_pending_source_audit',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} original source passages and their local dependencies; source audit remains pending.')
