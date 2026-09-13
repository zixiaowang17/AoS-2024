"""Transcribe change-point prerequisites from the main text only; extraction remains in progress."""
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
add('D1','high-dimensional linear regression model with change points',r'''
Given a sequence of data $\{(y_t,X_t)\}_{t=1}^n\subset\mathbb R\times\mathbb R^p$, with the dimensionality $p$ being a function of the sample size $n$, assume that
\[
y_t=X_t^\top\beta_t^*+\epsilon_t,\qquad t=1,\ldots,n,\tag{1}
\]
where $\{y_t\}_{t=1}^n$ are the responses, $\{X_t\}_{t=1}^n$ are the covariates, $\{\epsilon_t\}_{t=1}^n$ are the error terms and $\{\beta_t^*\}_{t=1}^n$ are true regression coefficients. Across time, assume that the coefficients sequence $\{\beta_t^*\}_{t=1}^n$ possesses a piecewise-constant pattern, i.e.
\[
\beta_t^*\ne\beta_{t-1}^*,\qquad\text{if and only if}\qquad t\in\{\eta_1,\ldots,\eta_K\},\tag{2}
\]
where $\{\eta_k\}_{k=1}^K\subset\{1,\ldots,n\}$ are called change points, satisfying that
\[
1=\eta_0<\eta_1<\cdots<\eta_K<\eta_{K+1}=n+1.\tag{3}
\]
We refer to the model specified in (1), (2) and (3) as the high-dimensional linear regression model with change points.
''',[1,2],'Section 1 — model (1)–(3)',kind='source_passage',symbols=[r'\beta_t^*',r'\eta_{K+1}=n+1'],shape='Triangular sequence of linear regressions with deterministic piecewise-constant coefficients and integer change points, using the source endpoint convention. Sparsity and conditional-mean assumptions are separate.')
add('D2','Model',r'''Consider the high-dimensional linear regression model with change points specified in (1), (2) and (3), with the covariate sequence $\{X_t\}_{t=1}^n\subset\mathbb R^p$ and noise sequence $\{\epsilon_t\}_{t=1}^n\subset\mathbb R$, such that $\mathbb E[\epsilon_t|X_t]=0$ for any $t\in\{1,\ldots,n\}$.''',[9],'Assumption 1 (Model) — conditional mean',{'D1':'The assumption explicitly invokes the regression and change-point model (1)–(3).'},kind='assumption',phrases=['Assumption 1 (Model)'],symbols=[r'\mathbb E[\epsilon_t|X_t]=0'],context='Assumption 1 (Model).',shape='Conditional mean-zero errors given contemporaneous covariates. This permits dependence between noise and covariates; it does not impose independence of their innovation sequences.')
add('D3','Sparsity',r'''For any $t\in\{1,\ldots,n\}$, assume that there exists a support $S_t\subset\{1,\ldots,p\}$, with $|S_t|\le s$, such that $\beta_{t,j}^*=0$, if $j\notin S_t$.''',[9],'Assumption 1a (Sparsity)',{'D1':'The coordinate support condition applies to the time-varying coefficient vector in (1).'},kind='assumption',symbols=[r'|S_t|\le s'],context='a. (Sparsity)',shape='Uniform sparsity bound with supports allowed to vary across time. No common support or lower bound on nonzero coefficients is imposed.')
add('D4','Change points',r'''
Let the minimal jump size be
\[
\kappa=\min_{k=1,\ldots,K}\kappa_k=\min_{k=1,\ldots,K}|\Psi_k|_2.\tag{19}
\]
Assume that there exists an absolute constant $C_\kappa>0$ such that for any $k\in\{1,\ldots,K\}$, $\kappa_k\le C_\kappa$. Let the minimal spacing be $\Delta=\min_{k=1,\ldots,K+1}(\eta_k-\eta_{k-1})$.
''',[10],'Assumption 1b (Change points)',{'D34':'Jump magnitudes are the Euclidean norms of the original jump vectors.'},kind='assumption',symbols=[r'\kappa_k',r'\Delta'],context='b. (Change points)',shape='Minimum jump size, uniform upper bound on each jump and minimum segment spacing. The fixed number of change points and normalized directions are declared separately in the Assumption 1 preamble.')
add('D5','covariate sequence',r'''
For each $t\in\mathbb Z$, let
\[
X_t=(X_{t1},\ldots,X_{tp})^\top=G(\mathcal F_t^X),\tag{4}
\]
where $G(\cdot)=(g_1(\cdot),\ldots,g_p(\cdot))^\top$ is an $\mathbb R^p$-valued measurable function with input $\mathcal F_t^X=\{\mathcal X_s\}_{s\le t}$, and $\{\mathcal X_t\}_{t\in\mathbb Z}$ is a collection of independent and identically distributed (i.i.d.) random elements. Note that (4) leads to the strict stationarity of $\{X_t\}_{t\in\mathbb Z}$.
''',[5],'Section 1.2 — covariate process (4)',symbols=[r'G(\mathcal F_t^X)',r'\mathcal X_t'],context='Functional dependence of the covariate sequence.',shape='Stationary causal measurable function of an iid innovation history. Script X is the innovation; plain X is the observed vector. The function G is time-invariant.')
add('D7','uniform functional dependence measure',r'''
For any $v\in\mathbb R^p$, any $q>0$ satisfying that $\|v^\top X_1\|_q<\infty$ and any $s\in\mathbb Z$, let
\[
\delta_{s,q}^X(v)=\|v^\top X_1-v^\top X_{1,\{1-s\}}\|_q=\|v^\top X_s-v^\top X_{s,\{0\}}\|_q,\tag{6}
\]
due to the strict stationarity implied by (4). Define the uniform functional dependence measure and its cumulative version as
\[
\delta_{s,q}^X=\sup_{|v|_2=1}\delta_{s,q}^X(v)\qquad\text{and}\qquad\Delta_{m,q}^X=\sum_{s=m}^\infty\delta_{s,q}^X,\qquad m\in\mathbb Z,\tag{7}
\]
respectively.
''',[5],'Section 1.2 — covariate dependence (6)–(7)',{'D5':'Each coupled vector evaluates the same stationary map G after replacement of the specified innovation.'},symbols=[r'\delta_{s,q}^X(v)',r'\Delta_{m,q}^X'],shape='Directional Lq coupling difference, supremum over unit Euclidean directions, and sum over lags. The single-innovation replacement recipe (5) is separately archived as ambient source context; no decay bound is built into this definition.')
add('D8','noise sequence',r'''
For each $t\in\mathbb Z$, let
\[
\epsilon_t=g(\mathcal F_t^\epsilon),\tag{8}
\]
where $g(\cdot)$ is an $\mathbb R$-valued measurable function with input $\mathcal F_t^\epsilon=\{\varepsilon_s\}_{s\le t}$, and $\{\varepsilon_t\}_{t\in\mathbb Z}$ is a collection of i.i.d. random elements. Note that (8) leads to the strict stationarity of $\{\epsilon_t\}_{t\in\mathbb Z}$.
''',[5],'Section 1.2 — noise process (8)',symbols=[r'\epsilon_t=g(\mathcal F_t^\epsilon)',r'\varepsilon_t'],context='Functional dependence of the noise sequence.',shape='Stationary scalar causal process from its own iid innovation history. The observed epsilon and innovation varepsilon are distinct symbols. Independence from covariate innovations is not asserted.')
add('D9','functional dependence measure',r'''
For any $t\in\mathbb Z$ and any integer pair $s_2\le s_1$, let $\varepsilon_t^*$ be an independent copy of $\varepsilon_t$ and $\epsilon_{t,\{s_1,s_2\}}=g(\mathcal F_{t,\{s_1,s_2\}}^\epsilon)$ be a coupled random variable, defined in the same way as that in (5). For any $q>0$ satisfying that $\|\epsilon_1\|_q<\infty$ and any $s\in\mathbb Z$, let the functional dependence measure and its cumulative version be
\[
\delta_{s,q}^\epsilon=\|\epsilon_1-\epsilon_{1,\{1-s\}}\|_q=\|\epsilon_s-\epsilon_{s,\{0\}}\|_q\qquad\text{and}\qquad\Delta_{m,q}^\epsilon=\sum_{s=m}^\infty\delta_{s,q}^\epsilon,\qquad m\in\mathbb Z,\tag{9}
\]
respectively.
''',[5],'Section 1.2 — noise dependence (9)',{'D8':'The coupled noise uses the same map g and its iid innovation history.'},symbols=[r'\Delta_{m,q}^\epsilon'],shape='Lq single-innovation replacement difference and its cumulative lag sum for the scalar stationary noise. The generic replacement recipe is shared with (5), not the covariate process or its assumptions.')
add('D10','nonstationary process',r'''
We therefore introduce the functional dependence measure for a (possibly) nonstationary process $\{Z_t\}_{t\in\mathbb Z}\subset\mathbb R$. Suppose that, for each $t\in\mathbb Z$,
\[
Z_t=g_t(\mathcal F_t^\zeta),\tag{10}
\]
where $g_t(\cdot)$ is a time-dependent $\mathbb R$-valued measurable functions with input $\mathcal F_t^\zeta=\{\zeta_s\}_{s\le t}$, and $\{\zeta_t\}_{t\in\mathbb Z}$ is a collection of i.i.d. random elements.
''',[6],'Section 1.2 — nonstationary causal process (10)',symbols=[r'Z_t=g_t(\mathcal F_t^\zeta)'],shape='Scalar causal process whose measurable generating function may depend on time. No stationarity, regression model, sparsity or change-point assumption is imported.')
add('D11','functional dependence measure',r'''
For any $t\in\mathbb Z$ and any integer pair $s_2\le s_1$, let $\zeta_t^*$ be an independent copy of $\zeta_t$ and $Z_{t,\{s_1,s_2\}}=g_t(\mathcal F_{t,\{s_1,s_2\}}^\zeta)$ be a coupled random variable, defined in the same way as that in (5). For any $q>0$ satisfying that $\sup_t\|Z_t\|_q<\infty$ and any $s\in\mathbb Z$, let the functional dependence measure and its cumulative version be
\[
\delta_{s,q}^Z=\sup_{t\in\mathbb Z}\|Z_t-Z_{t,\{t-s\}}\|_q\qquad\text{and}\qquad\Delta_{m,q}^Z=\sum_{s=m}^\infty\delta_{s,q}^Z,\qquad m\in\mathbb Z,\tag{11}
\]
respectively, and we again impose functional dependence assumptions on the decay rate of $\Delta_{m,q}^Z$.
''',[6],'Section 1.2 — nonstationary dependence (11)',{'D10':'The coupled process evaluates g_t after replacing an innovation in its input history.'},symbols=[r'\Delta_{m,q}^Z',r'\Delta_{m,2}^Z'],shape='Uniform-in-time coupling difference for a nonstationary process and cumulative lag sum. Theorem 4 uses q=2. The generic coupling recipe is ambient; it does not require the stationary covariate model.')
add('D12','Covariate sequence',r'''Assume that the covariate sequence $\{X_t\}_{t=1}^n\subset\mathbb R^p$ is a consecutive subsequence of an infinite sequence $\{X_t\}_{t\in\mathbb Z}\subset\mathbb R^p$, which has marginal mean zero and is of the form (4), with covariance matrix $\Sigma=\operatorname{Cov}(X_1)$.''',[10],'Assumption 2 (Covariate sequence) — preamble',{'D5':'The observed sequence is a segment of the stationary causal construction (4).'},kind='assumption',symbols=[r'\Sigma=\operatorname{Cov}(X_1)'],context='Assumption 2 (Covariate sequence).',shape='Mean-zero stationary covariates and their marginal covariance matrix, within a sample-size-dependent high-dimensional sequence.')
add('D13','Functional dependence',r'''
For the cumulative uniform functional dependence measure $\Delta_{\cdot,\cdot}^X$ defined in (6) and (7), for some absolute constants $\gamma_1,c>0$, assume that there exists an absolute constant $D_X>0$ such that
\[
\sup_{m\ge0}\exp(cm^{\gamma_1})\Delta_{m,4}^X\le D_X.\tag{20}
\]
''',[10],'Assumption 2a (Functional dependence)',{'D7':'The decay condition applies to the uniform covariate coupling measure at fourth moment.'},kind='assumption',symbols=[r'\Delta_{m,4}^X'],context='a. (Functional dependence)',shape='Uniform exponential-power lag decay measured in L4 for all projection directions. This is distinct from the second-moment scalar condition in Theorem 4.')
add('D14','Tail behaviour',r'''
Assume that there exist absolute constants $\gamma_2\in(0,2]$ and $C_X>0$, such that for any $\tau>0$,
\[
\sup_{|v|_2=1}\mathbb P(|v^\top X_1|>\tau)\le2\exp\{-(\tau/C_X)^{\gamma_2}\}.\tag{21}
\]
''',[10],'Assumption 2b (Tail behaviour)',{'D5':'The tail bound concerns one observation of the stationary covariate process.'},kind='assumption',symbols=[r'\sup_{|v|_2=1}'],context='b. (Tail behaviour)',shape='Uniform sub-Weibull upper tails over all unit projection directions, with shape no greater than two. Not merely a coordinatewise tail bound.')
add('D15','Marginal covariance matrix',r'''Assume that the smallest eigenvalue of $\Sigma$ satisfies $0<c_{\min}\le\Lambda_{\min}(\Sigma)$, where $c_{\min}>0$ is an absolute constant. For any $k\in\{1,\ldots,K\}$, assume that there exists an absolute constant $\varpi_k>0$ such that $v_k^\top\Sigma v_k\to\varpi_k$, as $n\to\infty$.''',[10],'Assumption 2c (Marginal covariance matrix)',{'D12':'Sigma is the marginal covariance matrix from the Assumption 2 preamble.','D34':'The limiting quadratic forms use the normalized jump directions.'},kind='assumption',symbols=[r'v_k^\top\Sigma v_k',r'\varpi_k'],context='c. (Marginal covariance matrix)',shape='Uniform positive lower covariance eigenvalue and positive limiting drift along each jump direction. The drift is an asymptotic limit, not an exact finite-sample identity.')
add('D16','Noise sequence',r'''Assume that the noise sequence $\{\epsilon_t\}_{t=1}^n\subset\mathbb R$ is a consecutive subsequence of an infinite sequence $\{\epsilon_t\}_{t\in\mathbb Z}\subset\mathbb R$, which has marginal mean zero and is of the form (8), with variance $\sigma_\epsilon^2=\operatorname{Var}(\epsilon_1)>0$ being an absolute constant.''',[11],'Assumption 3 (Noise sequence) — preamble',{'D8':'The observed noise is a segment of the stationary causal process (8).'},kind='assumption',symbols=[r'\sigma_\epsilon^2=\operatorname{Var}(\epsilon_1)>0'],context='Assumption 3 (Noise sequence).',shape='Marginal mean-zero stationary noise with a fixed positive variance. This does not establish positivity of every directional long-run variance of epsilon times X.')
add('D17','Functional dependence',r'''
For the cumulative functional dependence measure $\Delta_{\cdot,\cdot}^\epsilon$, defined in (9), for some absolute constants $\gamma_1,c>0$, assume there exists an absolute constant $D_\epsilon>0$ such that
\[
\sup_{m\ge0}\exp(cm^{\gamma_1})\Delta_{m,4}^\epsilon\le D_\epsilon.\tag{22}
\]
''',[11],'Assumption 3a (Functional dependence)',{'D9':'The exponential-power lag bound applies to the noise cumulative coupling measure in L4.'},kind='assumption',symbols=[r'\Delta_{m,4}^\epsilon'],context='a. (Functional dependence)',shape='Noise-specific fourth-moment lag decay. Shared gamma notation with the covariates is a worst-case parameter convention, not an assertion of identical dependence structures.')
add('D18','Tail behaviour',r'''Assume that there exist absolute constants $\gamma_2\in(0,2]$ and $C_\epsilon>0$, such that for any $\tau>0$, $\mathbb P(|\epsilon_0|>\tau)\le2\exp\{-(\tau/C_\epsilon)^{\gamma_2}\}$.''',[11],'Assumption 3b (Tail behaviour)',{'D8':'The bound applies to the scalar stationary noise marginal.'},kind='assumption',symbols=[r'\mathbb P(|\epsilon_0|>\tau)'],context='b. (Tail behaviour)',shape='Scalar noise tail bound with shape at most two. It has its own scale constant and permits contemporaneous dependence on covariates.')
add('D19','temporal dependence and tail behaviour',r'''
With the temporal dependence and tail behaviour specified for both the covariate and noise sequences, we introduce the parameter
\[
\gamma=(\gamma_1^{-1}+2\gamma_2^{-1})^{-1}.\tag{23}
\]
''',[11],'Section 3.1 — combined exponent (23)',{'D13':'Gamma_1 is a common worst-case exponent for covariate and noise dependence decay.','D17':'The common dependence exponent also controls the noise sequence.','D14':'Gamma_2 is the common worst-case tail exponent for the covariate and noise marginals.','D18':'The same tail exponent also controls the noise marginal.'},symbols=[r'\gamma=(\gamma_1^{-1}+2\gamma_2^{-1})^{-1}'],shape='Combined dependence/tail exponent for products of covariates and errors, with the factor two retained. It differs from the scalar exponent gamma(Z) bound inline in Theorem 4.')
add('D20','Signal-to-noise ratio',r'''
Assume that there exists a sufficiently large absolute constant $C_{\mathrm{snr}}>0$ such that
\[
\Delta\kappa^2\ge C_{\mathrm{snr}}\{s\log(pn)\}^{2/\gamma-1}\alpha_n,\tag{24}
\]
where $\alpha_n>0$ is any diverging sequence.
''',[11,12],'Assumption 4a (Signal-to-noise ratio)',{'D4':'The left-hand side uses the minimum spacing and minimum jump size.','D3':'The right-hand side uses the coefficient sparsity bound.','D19':'The power is determined by the combined dependence/tail exponent.'},kind='assumption',symbols=[r'\Delta\kappa^2',r'\alpha_n'],context='Assumption 4 (Signal-to-noise ratio).',shape='Baseline signal-spacing lower bound for localization, with a diverging sequence. The stronger inference requirement in part b adds a rate condition on that same sequence.')
add('D21','Signal-to-noise ratio',r'''
In addition to (24), assume that $\alpha_n$ diverges faster than $s\{\log(pn)\}^{2/\gamma}$, i.e.
\[
\alpha_n\gg s\{\log(pn)\}^{2/\gamma}.
\]
''',[12],'Assumption 4b (Signal-to-noise ratio)',{'D20':'Part b explicitly includes the baseline inequality (24) and strengthens the growth of its alpha_n.'},kind='assumption',symbols=[r'\alpha_n\gg s\{\log(pn)\}^{2/\gamma}'],context='Assumption 4 (Signal-to-noise ratio).',shape='Inference-level strengthening of Assumption 4a. It must retain both (24) and the extra growth rate; part b is not an alternative that removes part a.')
members['D21']['naming_context'][0]['evidence']=[dict(page=11,location='Assumption 4 heading')]
add('D22','Lasso',r'''
The estimator $\widehat\beta_{\mathcal I}$ in (13) is defined as
\[
\widehat\beta_{\mathcal I}=\operatorname*{arg\,min}_{\beta\in\mathbb R^p}\left\{\sum_{t\in\mathcal I}(y_t-X_t^\top\beta)^2+\lambda|\mathcal I|^{1/2}|\beta|_1\right\},\tag{14}
\]
where $\lambda>0$ is the Lasso tuning parameter to be specified.
''',[6,7],'Section 2.1 — interval Lasso estimator (14)',symbols=[r'\widehat\beta_{\mathcal I}',r'\lambda|\mathcal I|^{1/2}|\beta|_1'],shape='Squared-error Lasso on an integer interval with a square-root-length-scaled L1 penalty. The construction requires only data, not the stochastic regression assumptions used to prove its guarantees.')
add('D23','loss function',r'''
For any integer interval $\mathcal I\subset(0,n]$, the loss function $\mathcal G(\cdot)$ is defined as
\[
\mathcal G(\mathcal I)=\begin{cases}\sum_{t\in\mathcal I}\{-2y_tX_t^\top\widehat\beta_{\mathcal I}+\widehat\beta_{\mathcal I}^\top X_tX_t^\top\widehat\beta_{\mathcal I}\},&|\mathcal I|\ge\zeta,\\0,&\text{otherwise},\end{cases}\tag{13}
\]
with a to-be-specified $\zeta>0$.
''',[6],'Section 2.1 — interval loss (13)',{'D22':'The loss evaluates the fitted interval Lasso coefficient.'},symbols=[r'\mathcal G(\mathcal I)'],shape='Original fitted quadratic criterion without the sum of squared responses, set to zero for short intervals. The threshold is the same zeta used for the partition penalty; separate tuning values are not substituted.')
add('D24','integer partitions',r'''
Let
\[
\widehat{\mathcal P}=\widehat{\mathcal P}(\zeta)\in\operatorname*{arg\,min}_{\mathcal P}\left\{\sum_{\mathcal I\in\mathcal P}\mathcal G(\mathcal I)+\zeta|\mathcal P|\right\},\tag{12}
\]
where the minimisation is over all possible integer partitions of $\{1,\ldots,n\}$, $\mathcal P$ denotes an integer partition and $\zeta>0$ is a penalisation parameter.
''',[6],'Section 2.1 — penalized partition estimator (12)',{'D23':'The objective sums the specified interval loss over the partition.'},symbols=[r'\widehat{\mathcal P}(\zeta)'],shape='Optimization over all integer partitions with a penalty per segment. This is the mathematical objective implemented by the source DPDU algorithm.')
add('D25','Dynamic Programming with Dynamic Update',r'''
Algorithm 1 Dynamic Programming with Dynamic Update. $\mathrm{DPDU}(\{(y_t,X_t)\}_{t=1}^n,\lambda,\zeta)$

INPUT: Data $\{(y_t,X_t)\}_{t=1}^n$, tuning parameters $\lambda,\zeta>0$.

$\widehat{\mathcal B}\leftarrow\varnothing$, $\mathfrak p\leftarrow(-1,\ldots,-1)^\top\in\mathbb R^n$, $B\leftarrow(-\zeta,\infty,\ldots,\infty)^\top\in\overline{\mathbb R}^{n+1}$

for $r\in\{2,\ldots,n+1\}$ do

$\mathcal M_{\mathrm{temporary}}\leftarrow(0)\in\mathbb R^{p\times p}$, $\mathcal V_{\mathrm{temporary}}\leftarrow(0)\in\mathbb R^p$

for $l\in\{r-1,\ldots,1\}$ do
\[
\mathcal M_{\mathrm{temporary}}\leftarrow\mathcal M_{\mathrm{temporary}}+X_lX_l^\top,\qquad\mathcal V_{\mathrm{temporary}}\leftarrow\mathcal V_{\mathrm{temporary}}+y_lX_l^\top\tag{15}
\]
$\mathcal I\leftarrow[l,r)\cap\mathbb Z$.

if $|\mathcal I|\ge\zeta$ then

$\widehat\beta_{\mathcal I}\leftarrow\operatorname*{arg\,min}_{\beta\in\mathbb R^p}|\mathcal I|^{-1}\{-2\mathcal V_{\mathrm{temporary}}\beta+\beta^\top\mathcal M_{\mathrm{temporary}}\beta\}+\lambda/\sqrt{|\mathcal I|}|\beta|_1$

$\mathcal G(\mathcal I)\leftarrow-2\mathcal V_{\mathrm{temporary}}\widehat\beta_{\mathcal I}+\widehat\beta_{\mathcal I}^\top\mathcal M_{\mathrm{temporary}}\widehat\beta_{\mathcal I}$

else

$\mathcal G(\mathcal I)\leftarrow0$

end if

$b\leftarrow B_l+\zeta+\mathcal G(\mathcal I)$

if $b<B_r$ then

$B_r\leftarrow b$, $\mathfrak p_r\leftarrow l$

end if

end for

end for

$k\leftarrow n$

while $k>1$ do

$h\leftarrow\mathfrak p_k$, $\widehat{\mathcal B}\leftarrow\widehat{\mathcal B}\cup\{h\}$, $k\leftarrow h$

end while

OUTPUT: $\widehat{\mathcal B}$, $\widehat K=|\widehat{\mathcal B}|$, $\{\widehat\beta_k\}_{k=0}^{\widehat K}$
''',[8],'Algorithm 1 — Dynamic Programming with Dynamic Update',{'D24':'The source describes DPDU as a solver for the penalized partition problem (12).','D22':'Each sufficiently long interval is fitted by the Lasso update equivalent to (14).','D23':'The dynamic-programming comparison uses the original loss (13).'},symbols=[r'\widehat{\mathcal B}',r'\mathrm{DPDU}'],shape='Literal algorithm, including dynamic moment updates and pointer backtracking. Preserve the printed pointer length n, update at r=n+1, backtracking start k=n and inclusion of h in the output set; do not silently repair these indexing conventions.')
add('D26','interval',r'''
where $k\in\{1,\ldots\widehat K\}$ and $(s_k,e_k)$ is defined as
\[
s_k=9\widehat\eta_{k-1}/10+\widehat\eta_k/10\qquad\text{and}\qquad e_k=\widehat\eta_k/10+9\widehat\eta_{k+1}/10.\tag{18}
\]
''',[9],'Section 2.2 — local refinement interval (18)',{'D25':'The endpoints are weighted combinations of neighboring preliminary change-point estimates from DPDU.'},symbols=[r's_k',r'e_k'],context=r'Provided the preliminary estimators $\{\widehat\eta_k\}_{k=1}^{\widehat K}$ are good enough, each interval $(s_k,e_k)$ contains one and only one true change point $\eta_k$.',shape='Source local interval with weights nine-tenths and one-tenth. Rounding to integers and definitions of the two exterior estimated endpoints are not printed in this formula; they remain source conventions to resolve explicitly.')
add('D27','final estimators',r'''
The final estimators are defined as
\[
\widetilde\eta_k=\operatorname*{arg\,min}_{s_k<\eta<e_k}Q_k(\eta)=\operatorname*{arg\,min}_{s_k<\eta<e_k}\left\{\sum_{t=s_k}^{\eta-1}(y_t-X_t^\top\widehat\beta_{k-1})^2+\sum_{t=\eta}^{e_k-1}(y_t-X_t^\top\widehat\beta_k)^2\right\},\tag{17}
\]
''',[9],'Section 2.2 — final change-point estimator (17)',{'D26':'The minimization is restricted to the local interval (18).','D22':'The two fixed coefficients are interval Lasso fits on the preliminary segments.'},symbols=[r'\widetilde\eta_k',r'Q_k(\eta)'],shape='Local least-squares split with the preceding and following segment fits held fixed. Preserve the displayed open minimization interval and summation endpoints without guessing rounding or argmin tie-breaking.')
add('D28','long-run variance',r'''
For $k\in\{1,\ldots,K\}$, under the vanishing regime, the long-run variance
\[
\sigma_\infty^2(k)=4\lim_{n\to\infty}\operatorname{Var}\left(n^{-1/2}\sum_{t=1}^n\epsilon_tv_k^\top X_t\right)\tag{25}
\]
''',[12],'Lemma 2 — long-run variance (25)',{'D34':'The directional product uses the normalized jump vector.','D5':'The covariate observation comes from the stationary vector process.','D8':'The scalar factor is the stationary noise process.'},symbols=[r'\sigma_\infty^2(k)'],shape='Original limiting variance definition with factor four and sample-size-dependent jump direction. The source existence assertion assumes Assumptions 1–3, but those proof conditions are not incorporated into the definition itself.')
add('D29','jump size estimator',r'''
for each $k\in\{1,\ldots,\widehat K\}$, let
\[
\widehat\kappa_k=|\widehat\beta_k-\widehat\beta_{k-1}|_2\tag{30}
\]
be the $k$th jump size estimator.
''',[18],'Lemma 7 — jump size estimator (30)',{'D22':'The two coefficient estimates are Lasso fits on neighboring preliminary segments.','D25':'Their segment indices and estimated change-point count come from DPDU.'},symbols=[r'\widehat\kappa_k'],shape='Euclidean difference norm of adjacent fitted coefficient vectors. Equation (30) defines the unsquared jump estimate; Theorem 10 refers to its square with the same estimator wording.')
add('D30','Long-run variance estimators',r'''
Algorithm 2 Long-run variance estimators

INPUT: $\{(y_t,X_t)\}_{t=1}^n$, $\{\widehat\eta_k\}_{k=1}^{\widehat K}$, $\{\widehat\beta_k\}_{k=1}^{\widehat K}$, $\{\widehat\kappa_k\}_{k=1}^{\widehat K}$, $\{(s_k,e_k)\}_{k=1}^{\widehat K}$ and tuning parameter $R\in\mathbb N$

for $k\in\{1,\ldots,\widehat K\}$ do

for $t\in\{s_k,\ldots,e_k-1\}$ do

$Z_t^{(k)}\leftarrow(y_t-X_t^\top\widehat\beta_k)X_t^\top(\widehat\beta_{k+1}-\widehat\beta_k)$, $Z_t^{(k+1)}\leftarrow(y_t-X_t^\top\widehat\beta_{k+1})X_t^\top(\widehat\beta_{k+1}-\widehat\beta_k)$

$Z_t\leftarrow Z_t^{(k)}+Z_t^{(k+1)}$

end for

$S\leftarrow\lfloor(e_k-s_k)/(2R)\rfloor$

for $r\in\{1,\ldots,2R\}$ do

$\mathcal S_r\leftarrow\{s_k+(r-1)S,\ldots,s_k+rS-1\}$

end for

for $r\in\{1,\ldots,R\}$ do

$D_r\leftarrow(2S)^{-1/2}(\sum_{t\in\mathcal S_{2r-1}}Z_t-\sum_{t\in\mathcal S_{2r}}Z_t)$

end for

$\widehat\sigma_\infty^2(k)\leftarrow R^{-1}\widehat\kappa_k^{-2}\sum_{r=1}^RD_r^2$

end for

OUTPUT: $\{\widehat\sigma_\infty^2(k)\}_{k=1}^{\widehat K}$
''',[19],'Algorithm 2 — long-run variance estimator',{'D26':'The blocks partition the source local refinement interval.','D29':'The final average is divided by the squared estimated jump.','D22':'The Z construction uses fitted Lasso coefficients.','D25':'The preliminary change-point and coefficient indices come from DPDU.'},symbols=[r'\widehat\sigma_\infty^2(k)',r'D_r'],shape='Paired-block differences of a residual-product sequence, normalized by the estimated jump squared. Preserve the algorithm indices k and k+1, even though (17) and (30) use k-1 and k and the listed input ends at K-hat.')
add('D31','drift estimators',r'''
For $k\in\{1,\ldots,\widehat K\}$, define the drift estimators
\[
\widehat\varpi_k=\frac1{n\widehat\kappa_k^2}\sum_{t=1}^n(\widehat\beta_k-\widehat\beta_{k-1})^\top X_tX_t^\top(\widehat\beta_k-\widehat\beta_{k-1}).\tag{31}
\]
''',[20],'Proposition 9 — drift estimators (31)',{'D29':'The estimator normalizes by the squared estimated jump.','D22':'The quadratic form uses the adjacent fitted Lasso coefficient difference.'},symbols=[r'\widehat\varpi_k'],shape='Full-sample empirical covariance quadratic form along the estimated normalized jump direction. This definition is used by the simulated minimizer, without treating Proposition 9 as an inventoried Theorem.')
add('D32','Confidence interval construction',r'''
Step 1. Let $B\in\mathbb Z_+$ and $M\in\mathbb R_+$. For $b\in\{1,\ldots,B\}$, let
\[
\widehat u^{(b)}=\operatorname*{arg\,min}_{r\in(-M,M)}\{\widehat\varpi_k|r|+\widehat\sigma_\infty(k)\mathbb W^{(b)}(r)\},\tag{32}
\]
where
\[
\mathbb W^{(b)}(r)=\begin{cases}\frac1{\sqrt n}\sum_{i=\lceil nr\rceil}^{-1}z_i^{(b)},&r<0,\\0,&r=0,\\\frac1{\sqrt n}\sum_{i=1}^{\lfloor nr\rfloor}z_i^{(b)},&r>0,\end{cases}
\]
the quantity $n$ is the sample size and $\{z_i^{(b)}\}_{i=-\lfloor nM\rfloor}^{\lceil nM\rceil}$ are independent standard Gaussian random variables.
''',[20],'Section 4.1 — simulated minimizer (32)',{'D30':'The simulated objective uses the estimated long-run standard deviation from Algorithm 2.','D31':'The objective also uses the estimated drift coefficient (31).'},symbols=[r'\widehat u^{(b)}',r'\widehat u^{(1)}',r'\mathbb W^{(b)}(r)'],context='Confidence interval construction',shape='Minimizer of an estimated V-shaped drift plus a two-sided Gaussian partial-sum process. Theorem 10 sets M=infinity; the displayed Step 1 originally takes finite positive M. The process is stepwise in r, not an interpolated Brownian path.')
add('D33','vanishing regime',r'''(ii) the vanishing regime where $\kappa_k\to0$ as $n\to\infty$.''',[12],'Section 3.2 — vanishing jump regime',{'D34':'The regime concerns the Euclidean norm of each population jump vector.'},symbols=[r'\kappa_k\to0'],shape='Vanishing jump-size regime. Sections 4 and 4.1 restrict their variance and inference discussion to this regime, even though Theorems 8 and 10 refer back to the two-regime Theorem 3.')
add('D34',['jump vector','normalised version'],r'''For any $k\in\{1,\ldots,K\}$, where $K\ge1$ is an absolute constant integer, let the $k$th jump vector and its normalised version be $\Psi_k=\beta_{\eta_k}^*-\beta_{\eta_k-1}^*$ and $v_k=\Psi_k/|\Psi_k|_2=\Psi_k/\kappa_k$, respectively.''',[9],'Assumption 1 — jump vectors and fixed change-point count',{'D1':'The jumps compare coefficients before and at each true change point.'},symbols=[r'\Psi_k',r'v_k'],shape='Signed coefficient jump, its Euclidean normalization and a fixed positive number of change points. The minimal magnitude and spacing condition are in part b; the normalized direction may vary with n.')

def main():
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,status='source_review_pending',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} original source passages; dependency and source review remain.')

if __name__ == "__main__":
    main()
