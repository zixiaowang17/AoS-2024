"""Transcribe statement prerequisites from the inspected pinned journal paper, without supplements."""
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
add('D1','SDE model with additive noise',r'''
The following parametric form is common for an SDE model with additive noise:
\[
d\mathbf X_t=\mathbf F(\mathbf X_t;\boldsymbol\beta)\,dt+\boldsymbol\Sigma\,d\mathbf W_t,\qquad\mathbf X_0=\mathbf x_0.\tag{1}
\]
''',[1],'Section 1 — additive-noise stochastic differential equation (1)',kind='source_passage',phrases=['SDE model with additive noise'],symbols=[r'd\mathbf X_t',r'\boldsymbol\Sigma\,d\mathbf W_t'],shape='A vector diffusion with a parameterized drift and a state-independent diffusion matrix, started at x_0. Its filtered probability-space specification is preserved as application context. The drift parameter and noise parameter are distinct; only the diffusion covariance is identifiable from the law.')
members['D1']['application_context']=[dict(text=r'''Let $\mathbf X$ in (1) be defined on a complete probability space $(\Omega,\mathcal F,\mathbb P_{\boldsymbol\theta})$ with a complete right-continuous filtration $(\mathcal F_t)_{t\geq0}$, and let the $d$-dimensional Wiener process $\mathbf W=(\mathbf W_t)_{t\geq0}$ be adapted to $\mathcal F_t$. The probability measure $\mathbb P_{\boldsymbol\theta}$ is parameterized by the parameter $\boldsymbol\theta=(\boldsymbol\beta,\boldsymbol\Sigma)$.''',evidence=[dict(page=6,location='Section 2 — filtered experiment and parameterized law')])]
add('D2','parameter space',r'''
Rewrite equation (1) as follows:
\[
d\mathbf X_t=\mathbf A(\boldsymbol\beta)(\mathbf X_t-\mathbf b(\boldsymbol\beta))\,dt+\mathbf N(\mathbf X_t;\boldsymbol\beta)\,dt+\boldsymbol\Sigma\,d\mathbf W_t,\qquad\mathbf X_0=\mathbf x_0,\tag{2}
\]
such that $\mathbf F(\mathbf x;\boldsymbol\beta)=\mathbf A(\boldsymbol\beta)(\mathbf x-\mathbf b(\boldsymbol\beta))+\mathbf N(\mathbf x;\boldsymbol\beta)$. Let $\overline\Theta=\overline\Theta_\beta\times\overline\Theta_\Sigma$ be the parameter space with $\Theta_\beta$ and $\Theta_\Sigma$ being two open convex bounded subsets of $\mathbb R^r$ and $\mathbb R^{d\times d}$, respectively. Functions $\mathbf F,\mathbf N:\mathbb R^d\times\overline\Theta_\beta\to\mathbb R^d$ are locally Lipschitz, and $\mathbf A$, $\mathbf b$ are defined on $\overline\Theta_\beta$ and take values in $\mathbb R^{d\times d}$ and $\mathbb R^d$, respectively. Parameter matrix $\boldsymbol\Sigma$ takes values in $\mathbb R^{d\times d}$. The matrix $\boldsymbol\Sigma\boldsymbol\Sigma^\top$ is assumed to be positive definite and determines the variance of the process. Since any square root of $\boldsymbol\Sigma\boldsymbol\Sigma^\top$ induces the same distribution, $\boldsymbol\Sigma$ is only identifiable up to equivalence classes. Thus, instead of estimating $\boldsymbol\Sigma$, we estimate $\boldsymbol\Sigma\boldsymbol\Sigma^\top$.
''',[6],'Section 2 — drift decomposition and parameter domain',{'D1':'This rewrites the drift of the additive-noise SDE and specifies its parameter domain.'},kind='source_passage',phrases=['parameter space'],symbols=[r'\overline\Theta=\overline\Theta_\beta\times\overline\Theta_\Sigma',r'\mathbf F(\mathbf x;\boldsymbol\beta)',r'\boldsymbol\Sigma\boldsymbol\Sigma^\top'],shape='A linear-plus-nonlinear drift decomposition on the closures of bounded open convex parameter sets. The true parameter is interior, as stated separately. The statistical target replaces the noise square root by its identifiable covariance, but the source does not explicitly redefine the parameter-domain coordinates after this replacement.')
members['D2']['application_context']=[dict(text=r'''We denote the true parameter value by $\boldsymbol\theta_0=(\boldsymbol\beta_0,\boldsymbol\Sigma_0)$ and assume that $\boldsymbol\theta_0\in\Theta$. Sometimes we write $\mathbf A_0$, $\mathbf b_0$, $\mathbf N_0(\mathbf x)$ and $\boldsymbol\Sigma\boldsymbol\Sigma_0^\top$ instead of $\mathbf A(\boldsymbol\beta_0)$, $\mathbf b(\boldsymbol\beta_0)$, $\mathbf N(\mathbf x;\boldsymbol\beta_0)$ and $\boldsymbol\Sigma_0\boldsymbol\Sigma_0^\top$, when referring to the true parameters. We write $\mathbf A$, $\mathbf b$, $\mathbf N(\mathbf x)$ and $\boldsymbol\Sigma\boldsymbol\Sigma^\top$ for any parameter $\boldsymbol\theta$. Sometimes we suppress the parameter to simplify notation, for example, $\mathbb E$ implicitly refers to $\mathbb E_{\boldsymbol\theta}$.''',evidence=[dict(page=6,location='Section 2 — true parameter, covariance shorthand and suppressed arguments')])]
add('D3','one-sided globally Lipschitz continuous',r'''
Function $\mathbf N$ is twice continuously differentiable with respect to $\mathbf x$ and $\boldsymbol\theta$, that is, $\mathbf N\in C^2$. Additionally, it is one-sided globally Lipschitz continuous with respect to $\mathbf x$ on $\mathbb R^d\times\overline\Theta_\beta$, that is, there exists a constant $C>0$ such that
\[
(\mathbf x-\mathbf y)^\top(\mathbf N(\mathbf x;\boldsymbol\beta)-\mathbf N(\mathbf y;\boldsymbol\beta))\leq C\|\mathbf x-\mathbf y\|^2\quad\forall\mathbf x,\mathbf y\in\mathbb R^d.
\]
''',[7],'(A1)',{'D2':'The regularity applies to the nonlinear part of the chosen drift decomposition over the closed parameter domain.'},kind='assumption',phrases=['one-sided globally Lipschitz continuous','(A1)'],symbols=[r'(\mathbf x-\mathbf y)^\top'],shape='Joint C2 regularity of N and a global one-sided Lipschitz bound, uniform over the indicated parameter domain. This is not a two-sided global Lipschitz bound on the drift or a separate explicit smoothness condition on A and b.')
add('D4','polynomial growth',r'''
Function $\mathbf N$ grows at most polynomially in $\mathbf x$, uniformly in $\boldsymbol\theta$, that is, there exist constants $C>0$ and $\chi\geq1$ such that
\[
\|\mathbf N(\mathbf x;\boldsymbol\beta)-\mathbf N(\mathbf y;\boldsymbol\beta)\|^2\leq C(1+\|\mathbf x\|^{2\chi-2}+\|\mathbf y\|^{2\chi-2})\|\mathbf x-\mathbf y\|^2\quad\forall\mathbf x,\mathbf y\in\mathbb R^d.
\]
Additionally, its derivatives are of polynomial growth in $\mathbf x$, uniformly in $\boldsymbol\theta$.
''',[7],'(A2)',{'D2':'The polynomial increment and derivative restrictions concern the nonlinear drift component N.'},kind='assumption',phrases=['polynomial growth','(A2)'],symbols=[r'\chi\geq1',r'2\chi-2'],shape='A polynomially weighted Lipschitz increment condition and polynomial growth of derivatives, uniform in the parameter. The source phrase grows at most polynomially is accompanied by the stronger displayed increment inequality, which is retained.')
add('D5','invariant probability',r'''
The solution $\mathbf X$ of SDE (1) has invariant probability $\nu_0(d\mathbf x)$.
''',[7],'(A3)',{'D1':'The invariant distribution belongs to the continuous-time SDE solution.'},kind='assumption',phrases=['invariant probability','(A3)'],symbols=[r'\nu_0(d\mathbf x)'],shape='Existence of the stated invariant probability, used at the true law in the information matrix. The assumption itself does not explicitly say unique, ergodic, stationary initial distribution, or finite moments of every order.')
add('D6','invertible',r'''
$\boldsymbol\Sigma\boldsymbol\Sigma^\top$ is invertible on $\overline\Theta_\Sigma$.
''',[7],'(A4)',{'D2':'The condition is on the covariance formed from diffusion parameters in the closed noise-parameter domain.'},kind='assumption',phrases=['invertible','(A4)'],symbols=[r'\overline\Theta_\Sigma'],shape='Invertibility over the closed noise parameter domain. The general model already assumes positive-definite covariance; the theorem’s explicit A4 reference is retained. Hypoelliptic extensions mentioned in prose are not included in the stated estimation theorems.')
add('D7','identifiable',r'''
Function $\mathbf F$ is identifiable in $\boldsymbol\beta$, that is, if $\mathbf F(\mathbf x,\boldsymbol\beta_1)=\mathbf F(\mathbf x,\boldsymbol\beta_2)$ for all $\mathbf x\in\mathbb R^d$, then $\boldsymbol\beta_1=\boldsymbol\beta_2$.
''',[7],'(A5)',{'D1':'Identifiability concerns the full SDE drift, not the separate pieces of a chosen splitting.'},kind='assumption',phrases=['identifiable','(A5)'],symbols=[r'\boldsymbol\beta_1=\boldsymbol\beta_2'],shape='Global pointwise identifiability of the drift parameter through F. It is not identifiability of the matrix square root Sigma, and it is not written as equality only almost everywhere under nu_0.')
add('D8','equidistant step size',r'''
Assume a sample $(\mathbf X_{t_k})_{k=0}^N\equiv\mathbf X_{0:t_N}$ from (2) at time steps $0=t_0<t_1<\cdots<t_N=T$. For notational simplicity, we assume equidistant step size $h=t_k-t_{k-1}$.
''',[7],'Section 2.1 — observation grid',{'D1':'The sampled observations come from the SDE solution.'},kind='source_passage',phrases=['equidistant step size'],symbols=[r'h=t_k-t_{k-1}',r't_N=T'],shape='N increments and N+1 observations on an equidistant grid. Numerical approximation statements concern a finite time horizon T; the estimator statements explicitly allow the observed horizon Nh to diverge. Constants from fixed-horizon bounds are not silently assumed uniform in T.')
add('D9','OU process',r'''
\[
d\mathbf X_t^{[1]}=\mathbf A(\mathbf X_t^{[1]}-\mathbf b)\,dt+\boldsymbol\Sigma\,d\mathbf W_t,\qquad\mathbf X_0^{[1]}=\mathbf x_0.\tag{3}
\]
The solution of equation (3) is an OU process given by the following $h$-flow:
\[
\mathbf X_{t_k}^{[1]}=\Phi_h^{[1]}(\mathbf X_{t_{k-1}}^{[1]})=e^{\mathbf A h}\mathbf X_{t_{k-1}}^{[1]}+(\mathbf I-e^{\mathbf A h})\mathbf b+\boldsymbol\xi_{h,k},\tag{5}
\]
where $\boldsymbol\xi_{h,k}\overset{\mathrm{i.i.d.}}\sim\mathcal N_d(\mathbf0,\boldsymbol\Omega_h)$ for $k=1,\ldots,N$ (Vatiwutipong and Phewchean (2019)). The covariance matrix $\boldsymbol\Omega_h$ and the conditional mean of the OU process (5) are provided by
\[
\boldsymbol\Omega_h=\int_0^h e^{\mathbf A(h-u)}\boldsymbol\Sigma\boldsymbol\Sigma^\top e^{\mathbf A^\top(h-u)}\,du
=h\boldsymbol\Sigma\boldsymbol\Sigma^\top+\frac{h^2}2(\mathbf A\boldsymbol\Sigma\boldsymbol\Sigma^\top+\boldsymbol\Sigma\boldsymbol\Sigma^\top\mathbf A^\top)+\mathbf R(h,\mathbf x_0),\tag{6}
\]
\[
\boldsymbol\mu_h(\mathbf x;\boldsymbol\beta):=e^{\mathbf A(\boldsymbol\beta)h}\mathbf x+(\mathbf I-e^{\mathbf A(\boldsymbol\beta)h})\mathbf b(\boldsymbol\beta).\tag{7}
\]
''',[8],'Section 2.3 — linear OU flow, equations (3),(5)-(7)',{'D2':'The OU component uses the linear drift matrix, center and additive noise of the chosen decomposition.'},phrases=['OU process'],symbols=[r'\boldsymbol\Omega_h',r'\boldsymbol\mu_h(\mathbf x;\boldsymbol\beta)',r'\boldsymbol\xi_{h,k}'],shape='Exact linear stochastic flow, its matrix-exponential covariance integral and affine conditional mean. Equation (6) literally gives R(h,x_0) after its second-order terms; this weaker printed remainder is not changed to R(h^3,x_0). Strong-error results require the noise to be coupled to the driving Wiener process, not freshly independent noise unrelated to the target path.')
add('D10','time flow',r'''
\[
d\mathbf X_t^{[2]}=\mathbf N(\mathbf X_t^{[2]})\,dt,\qquad\mathbf X_0^{[2]}=\mathbf x_0.\tag{4}
\]
Thus, there exists a unique function $\mathbf f_h:\mathbb R^d\times\Theta_\beta\to\mathbb R^d$, for $h\geq0$, such that
\[
\mathbf X_{t_k}^{[2]}=\Phi_h^{[2]}(\mathbf X_{t_{k-1}}^{[2]})=\mathbf f_h(\mathbf X_{t_{k-1}}^{[2]};\boldsymbol\beta).\tag{8}
\]
For all $\boldsymbol\beta\in\Theta_\beta$, the time flow $\mathbf f_h$ fulfills the following semigroup properties:
\[
\mathbf f_0(\mathbf x;\boldsymbol\beta)=\mathbf x,\qquad\mathbf f_{t+s}(\mathbf x;\boldsymbol\beta)=\mathbf f_t(\mathbf f_s(\mathbf x;\boldsymbol\beta);\boldsymbol\beta),\qquad t,s\geq0.\tag{9}
\]
''',[8],'Section 2.3 — nonlinear deterministic flow, equations (4),(8)-(9)',{'D2':'The deterministic component is driven by the nonlinear part N of the drift.','D3':'The surrounding flow-existence statement explicitly invokes A1.','D4':'The surrounding flow-existence statement explicitly invokes A2.'},phrases=['time flow'],symbols=[r'\mathbf f_h',r'\mathbf f_{t+s}'],shape='Forward deterministic ODE flow with the semigroup property. The intervening sentence attributes existence to A1-A2; backward/global invertibility is a separate A6 requirement and is not built into the forward-flow definition.')
members['D10']['application_context']=[dict(text='Assumptions (A1) and (A2) ensure the existence and uniqueness of the solution of (4) (Theorem 1.2.17 in Humphries and Stuart (2002)).',evidence=[dict(page=8,location='Section 2.3 — context for the unique forward flow')])]
add('D11','well-defined inverse',r'''
Function $\mathbf f_h^{-1}(\mathbf x;\boldsymbol\beta)$ is defined asymptotically, for all $\mathbf x\in\mathbb R^d$, $\boldsymbol\beta\in\Theta_\beta$, when $h\to0$.
''',[8],'(A6)',{'D10':'The inverse concerns the nonlinear deterministic time flow, not the Gaussian OU map.'},kind='assumption',context='For the S estimator, we need a well-defined inverse.',phrases=['(A6)'],symbols=[r'\mathbf f_h^{-1}(\mathbf x;\boldsymbol\beta)'],shape='The source’s asymptotic existence condition for the inverse flow. It does not specify a common small-step threshold uniform over all states and parameters, growth bounds on the inverse, or a global inverse for every finite step size. The phrase is retained without strengthening it.')
add('D12','Lie–Trotter',r'''
Let Assumptions (A1) and (A2) hold. The Lie–Trotter and Strang splitting approximations of the solution of (2) are given by
\[
\mathbf X_{t_k}^{[\mathrm{LT}]}:=\Phi_h^{[\mathrm{LT}]}(\mathbf X_{t_{k-1}}^{[\mathrm{LT}]})=(\Phi_h^{[1]}\circ\Phi_h^{[2]})(\mathbf X_{t_{k-1}}^{[\mathrm{LT}]})=\boldsymbol\mu_h(\mathbf f_h(\mathbf X_{t_{k-1}}^{[\mathrm{LT}]}))+\boldsymbol\xi_{h,k}.\tag{10}
\]
''',[8],'Definition 2.3 — Lie–Trotter approximation (10)',{'D3':'Definition 2.3 explicitly assumes A1.','D4':'Definition 2.3 explicitly assumes A2.','D9':'The stochastic OU step is applied after the nonlinear step.','D10':'The nonlinear deterministic flow supplies the first step in the composition.'},phrases=['Lie–Trotter'],symbols=[r'\mathbf X_{t_k}^{[\mathrm{LT}]}',r'\Phi_h^{[1]}\circ\Phi_h^{[2]}'],shape='The particular nonlinear-then-OU Lie–Trotter scheme displayed in (10), with the same Gaussian OU innovation. The following Strang formula is stored separately. Reversing the order is discussed in the source but is not substituted into this definition.')
add('D13','Strang',r'''
Let Assumptions (A1) and (A2) hold. The Lie–Trotter and Strang splitting approximations of the solution of (2) are given by
\[
\mathbf X_{t_k}^{[\mathrm S]}:=\Phi_h^{[\mathrm S]}(\mathbf X_{t_{k-1}}^{[\mathrm S]})=(\Phi_{h/2}^{[2]}\circ\Phi_h^{[1]}\circ\Phi_{h/2}^{[2]})(\mathbf X_{t_{k-1}}^{[\mathrm S]})
=\mathbf f_{h/2}(\boldsymbol\mu_h(\mathbf f_{h/2}(\mathbf X_{t_{k-1}}^{[\mathrm S]}))+\boldsymbol\xi_{h,k}).\tag{11}
\]
''',[8],'Definition 2.3 — Strang approximation (11)',{'D3':'Definition 2.3 explicitly assumes A1.','D4':'Definition 2.3 explicitly assumes A2.','D9':'The middle full step is the stochastic OU flow.','D10':'The two outer half-steps are the nonlinear deterministic flow.'},phrases=['Strang'],symbols=[r'\mathbf X_{t_k}^{[\mathrm S]}',r'\Phi_{h/2}^{[2]}\circ\Phi_h^{[1]}\circ\Phi_{h/2}^{[2]}'],shape='Nonlinear half-step, OU full step, nonlinear half-step. The forward scheme is defined without an inverse; Theorem 3.7 separately adds A6. It is not the alternative OU-half/nonlinear-full/OU-half composition.')
add('D14','Lp consistency of a numerical scheme',r'''
The one-step approximation $\widetilde\Phi_h$ of the solution $\mathbf X$ is $L^p$ consistent, $p\geq1$, of order $q_2-1/2\geq0$, if for $k=1,\ldots,N$ and some $q_1\geq q_2+1/2$:
\[
\|\mathbb E[\mathbf X_{t_k}-\widetilde\Phi_h(\mathbf X_{t_{k-1}})\mid\mathbf X_{t_{k-1}}=\mathbf x]\|=R(h^{q_1},\mathbf x),
\]
\[
\left(\mathbb E[\|\mathbf X_{t_k}-\widetilde\Phi_h(\mathbf X_{t_{k-1}})\|^{2p}\mid\mathbf X_{t_{k-1}}=\mathbf x]\right)^{\frac1{2p}}=R(h^{q_2},\mathbf x).
\]
''',[13],'Definition 3.1 (Lp consistency of a numerical scheme)',{'D1':'The one-step error compares the numerical map with the SDE solution started at its exact previous state.','D8':'The error is indexed by the observation grid and common step size h.'},context='Definition 3.1 (Lp consistency of a numerical scheme).',phrases=['Definition 3.1'],symbols=[r'q_1\geq q_2+1/2',r'q_2-1/2\geq0',r'R(h^{q_2},\mathbf x)'],shape='Local conditional mean error and conditional 2p-moment root bounds, evaluated at the exact preceding state. The source calls q2-1/2 the consistency order and requires a mean order at least one-half higher than q2. R denotes a polynomially state-dependent order bound, not a prescribed function.')
add('D15','Bounded moments of a numerical scheme',r'''
A numerical approximation $\widetilde{\mathbf X}$ of the solution $\mathbf X$ has bounded moments, if for all $p\geq1$, there exists constant $C>0$, such that, for $k=1,\ldots,N$:
\[
\mathbb E[\|\widetilde{\mathbf X}_{t_k}\|^{2p}]\leq C(1+\|\mathbf x_0\|^{2p}).
\]
''',[13],'Definition 3.2 (Bounded moments of a numerical scheme)',{'D1':'The approximation is initialized at the same deterministic initial state as the SDE.','D8':'The bound applies to all grid indices through the horizon.'},context='Definition 3.2 (Bounded moments of a numerical scheme).',phrases=['Definition 3.2'],symbols=[r'\mathbb E[\|\widetilde{\mathbf X}_{t_k}\|^{2p}]',r'C(1+\|\mathbf x_0\|^{2p})'],shape='Moment bounds for every p>=1 and every grid point, with a constant that can depend on p and the fixed horizon. The source does not explicitly quantify uniformity in h or in a horizon tending to infinity.')
add('D16','approximate objective functions',r'''
Retaining terms up to order $R(Nh^2,\mathbf x_0)$ from (12) and (14), we establish the approximate objective functions:
\[
\mathcal L_N^{[\mathrm{LT}]}(\boldsymbol\theta):=N\log\det\boldsymbol\Sigma\boldsymbol\Sigma^\top+Nh\operatorname{Tr}\mathbf A(\boldsymbol\beta)
+\frac1h\sum_{k=1}^N(\mathbf X_{t_k}-\boldsymbol\mu_h(\mathbf f_h(\mathbf X_{t_{k-1}};\boldsymbol\beta);\boldsymbol\beta))^\top(\boldsymbol\Sigma\boldsymbol\Sigma^\top)^{-1}
(\mathbf X_{t_k}-\boldsymbol\mu_h(\mathbf f_h(\mathbf X_{t_{k-1}};\boldsymbol\beta);\boldsymbol\beta))
-\sum_{k=1}^N(\mathbf X_{t_k}-\boldsymbol\mu_h(\mathbf f_h(\mathbf X_{t_{k-1}};\boldsymbol\beta);\boldsymbol\beta))^\top(\boldsymbol\Sigma\boldsymbol\Sigma^\top)^{-1}\mathbf A(\boldsymbol\beta)
(\mathbf X_{t_k}-\boldsymbol\mu_h(\mathbf f_h(\mathbf X_{t_{k-1}};\boldsymbol\beta);\boldsymbol\beta)),\tag{22}
\]
\[
\mathcal L_N^{[\mathrm S]}(\boldsymbol\theta):=N\log\det\boldsymbol\Sigma\boldsymbol\Sigma^\top+Nh\operatorname{Tr}\mathbf A(\boldsymbol\beta)+\frac1h\sum_{k=1}^N\mathbf Z_{t_k}(\boldsymbol\beta)^\top(\boldsymbol\Sigma\boldsymbol\Sigma^\top)^{-1}\mathbf Z_{t_k}(\boldsymbol\beta)
-\sum_{k=1}^N\mathbf Z_{t_k}(\boldsymbol\beta)^\top(\boldsymbol\Sigma\boldsymbol\Sigma^\top)^{-1}\mathbf A(\boldsymbol\beta)\mathbf Z_{t_k}(\boldsymbol\beta)
+h\sum_{k=1}^N\operatorname{Tr}D\mathbf N(\mathbf X_{t_k};\boldsymbol\beta).\tag{23}
\]
''',[17],'Section 5 — approximate contrasts (22) and (23)',{'D2':'The contrasts use the drift decomposition and identifiable diffusion covariance.','D8':'They sum over the N observed increments of step size h.','D9':'The LT prediction and the S transformed residual use the OU conditional mean.','D10':'Both contrasts use the nonlinear deterministic flow.','D11':'The S residual in (13) requires the inverse nonlinear half-flow.'},phrases=['approximate objective functions'],symbols=[r'\mathcal L_N^{[\mathrm{LT}]}',r'\mathcal L_N^{[\mathrm S]}',r'\operatorname{Tr}D\mathbf N(\mathbf X_{t_k};\boldsymbol\beta)'],shape='The two approximate objectives actually named by Theorems 5.1 and 5.2. Their complete separate formulas are retained as the original paired source definition. The source says the full objectives (12)/(14) are used in practice, but these are different functions. No unproved equivalence of minimizers is inserted.')
members['D16']['application_context']=[dict(text=r'''We first define
\[
\mathbf Z_{t_k}(\boldsymbol\beta):=\mathbf f_{h/2}^{-1}(\mathbf X_{t_k};\boldsymbol\beta)-\boldsymbol\mu_h(\mathbf f_{h/2}(\mathbf X_{t_{k-1}};\boldsymbol\beta);\boldsymbol\beta).\tag{13}
\]''',evidence=[dict(page=9,location='Section 2.4.1 — transformed S residual referenced by (23)')])]
add('D17','half-vectorization',r'''
With $\boldsymbol\varsigma:=\operatorname{vech}(\boldsymbol\Sigma\boldsymbol\Sigma^\top)=([\boldsymbol\Sigma\boldsymbol\Sigma^\top]_{11},[\boldsymbol\Sigma\boldsymbol\Sigma^\top]_{12},[\boldsymbol\Sigma\boldsymbol\Sigma^\top]_{22},\ldots,[\boldsymbol\Sigma\boldsymbol\Sigma^\top]_{1d},\ldots,[\boldsymbol\Sigma\boldsymbol\Sigma^\top]_{dd})$, we half-vectorize $\boldsymbol\Sigma\boldsymbol\Sigma^\top$ to avoid working with tensors when computing derivatives with respect to $\boldsymbol\Sigma\boldsymbol\Sigma^\top$. Since $\boldsymbol\Sigma\boldsymbol\Sigma^\top$ is a symmetric $d\times d$ matrix, $\boldsymbol\varsigma$ is of dimension $s=d(d+1)/2$. For a diagonal matrix, instead of a half-vectorization, we use $\boldsymbol\varsigma:=\operatorname{diag}(\boldsymbol\Sigma\boldsymbol\Sigma^\top)$.
''',[17,18],'Section 5.2 — covariance coordinates',{'D2':'The vector parameterizes the identifiable covariance rather than its nonunique square root.'},phrases=['half-vectorization'],symbols=[r'\operatorname{vech}(\boldsymbol\Sigma\boldsymbol\Sigma^\top)',r's=d(d+1)/2'],shape='The source lists the upper-triangle-by-column covariance entries as its vech ordering; a lower-triangle convention is not substituted. In the diagonal case the coordinate dimension becomes d, although the preceding general formula says s=d(d+1)/2. The theorem’s diffusion rate applies to these covariance coordinates.')
add('D18','Fisher information matrix',r'''
Let
\[
\mathbf C(\boldsymbol\theta_0):=\begin{bmatrix}C_\beta(\boldsymbol\theta_0)&\mathbf0_{r\times s}\\\mathbf0_{s\times r}&C_\varsigma(\boldsymbol\theta_0)\end{bmatrix},\tag{27}
\]
where
\[
[C_\beta(\boldsymbol\theta_0)]_{i_1,i_2}:=\int(\partial_{\beta_{i_1}}\mathbf F_0(\mathbf x))^\top(\boldsymbol\Sigma\boldsymbol\Sigma_0^\top)^{-1}(\partial_{\beta_{i_2}}\mathbf F_0(\mathbf x))\,d\nu_0(\mathbf x),\qquad1\leq i_1,i_2\leq r,
\]
\[
[C_\varsigma(\boldsymbol\theta_0)]_{j_1,j_2}:=\frac12\operatorname{Tr}((\partial_{\varsigma_{j_1}}\boldsymbol\Sigma\boldsymbol\Sigma_0^\top)(\boldsymbol\Sigma\boldsymbol\Sigma_0^\top)^{-1}(\partial_{\varsigma_{j_2}}\boldsymbol\Sigma\boldsymbol\Sigma_0^\top)(\boldsymbol\Sigma\boldsymbol\Sigma_0^\top)^{-1}),\qquad1\leq j_1,j_2\leq s.
\]
''',[18],'Section 5.2 — limiting information matrix (27)',{'D1':'The drift derivatives concern the original SDE drift F at the true parameter.','D2':'The inverse covariance and true-parameter shorthand follow the model convention.','D5':'The drift block integrates under the true invariant probability nu_0.','D17':'The diffusion block differentiates with respect to the chosen covariance coordinates.'},context='Moreover, the estimators are asymptotically efficient since $\mathbf C$ is the Fisher information matrix for the corresponding continuous-time diffusion',phrases=[],symbols=[r'\mathbf C(\boldsymbol\theta_0)',r'C_\beta(\boldsymbol\theta_0)',r'C_\varsigma(\boldsymbol\theta_0)'],shape='The block-diagonal limiting matrix with stationary drift information and half-trace covariance information. Derivatives of F_0 and the true covariance mean derivatives before evaluating at the true parameter, not differentiation of already fixed constants. The source calls it Fisher information in nearby prose; that identification is recorded without separately certifying efficiency.')
# Source-inspected selector amendment; original statements are unchanged.
members['D4']['highlight_symbols'] = ['\\chi\\geq1', '\\|\\mathbf x\\|^{2\\chi-2}']

def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source interfaces.')


if __name__ == "__main__":
    main()
