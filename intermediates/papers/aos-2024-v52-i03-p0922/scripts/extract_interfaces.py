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
add('D1','semiparametric binary response model',r'''
In this paper, we consider the following semiparametric binary response model:
\[
Y=\operatorname{sign}(Y^*)\in\{-1,+1\},\qquad Y^*=X+\boldsymbol Z^\top\boldsymbol\beta^*+\epsilon,\qquad\boldsymbol\beta^*\in\mathbb R^p,\tag{1}
\]
where $Y$ is the binary response variable, $X$ and $\boldsymbol Z$ are covariates and $\epsilon$ denotes a random noise that is not required to be independent of $\boldsymbol Z$.
''',[2],'Section 1 — model (1)',kind='source_passage',phrases=['semiparametric binary response model'],symbols=[r'\boldsymbol\beta^*'],shape='Binary latent-index model with coefficient of X fixed to one. This law-level template does not impose identical distributions across all machines; the homogeneous sampling assumption is separate.')
add('D2','i.i.d. copies',r'''Assume that $\{(y_i,x_i,\boldsymbol z_i,\epsilon_i)\}_{i=1,2,\ldots,n}$ are i.i.d. copies of $(Y,X,\boldsymbol Z,\epsilon)$. Our goal is to estimate $\boldsymbol\beta^*$ given $\{(y_i,x_i,\boldsymbol z_i)\}_{i=1,2,\ldots,n}$.''',[2],'Section 1 — homogeneous sample',{'D1':'The homogeneous observations copy the joint variables in model (1).'},kind='assumption',phrases=['i.i.d. copies'],shape='The baseline iid experiment, superseded by explicitly heterogeneous section settings. Observed data exclude latent errors.')
add('D3','identifiability',r'''
For the identifiability of $\boldsymbol\beta^*$, we assume the following conditions about the distribution of $X$, $\boldsymbol Z$ and $Y$ hold for the entire paper:

(a) The median of the noise conditional on $X$ and $\boldsymbol Z$ is $0$, that is, $\operatorname{median}(\epsilon\mid X,\boldsymbol Z)=0$.

(b) The support of $(X,\boldsymbol Z)$ is not contained in any proper linear subspace of $\mathbb R^{p+1}$.

(c) For almost every $(X,\boldsymbol Z)$, $0<\mathbb P(Y=-1\mid X,\boldsymbol Z)<1$.

(d) The distribution of $X$ conditional on $\boldsymbol Z$ has positive density almost everywhere.
''',[10],'Section 2.1 — conditions (a)–(d)',kind='condition',phrases=['identifiability'],symbols=[r'\operatorname{median}(\epsilon\mid X,\boldsymbol Z)=0'],shape='Four standing distributional conditions applied to the model in each section. The condition is a predicate on a law, not an assertion that a finite-sample estimator is uniquely defined.')
add('D4','equally sized subsets',r'''Under the distributed environment, the data is split into $L$ equally sized subsets (machines) $\{\mathcal D_\ell,\ell=1,2,\ldots,L\}$, where each subset $\mathcal D_\ell$ has $m=n/L$ data points and the index is denoted by $\mathcal H_\ell$, that is, $\mathcal D_\ell=\{y_i,x_i,\boldsymbol z_i,i\in\mathcal H_\ell\}$.''',[12],'Section 2.2 — equal-size data partition',kind='source_passage',phrases=['equally sized subsets'],symbols=[r'm=n/L',r'\mathcal H_\ell'],shape='Partition of observed data into equal batches; the partition itself does not impose identical laws. Unequal m_l in Section 4.1 is a distinct setting.')
add('D5','kernel',r'''
Assume that the function $H(x)$ is the integral of an $\alpha$-order kernel, that is,
\[
\pi_U:=\int_{-1}^1x^\alpha H'(x)\,dx\ne0,\qquad\text{and}\qquad\int_{-1}^1x^kH'(x)\,dx=0,\quad k=1,2,\ldots,\alpha-1,
\]
where $\alpha\geq2$ is a positive integer. Further, assume that the kernel is square-integrable, that is, $\pi_V:=\int_{-1}^1[H'(x)]^2\,dx<\infty$, and also has a bounded and Lipschitz continuous derivative $H''(x)$. Finally, assume that $H(x)=1$ when $x>1$ and $H(x)=0$ when $x<-1$.
''',[14,15],'Assumption 1',kind='assumption',phrases=['Assumption 1'],symbols=[r'\pi_U',r'\pi_V',r'H(x)'],shape='Integrated order-alpha kernel and its regularity, with alpha an integer at least two. Moment cancellation and nonzero alpha moment are preserved; no nonnegative-kernel assumption is added.')
add('D6','distribution density function',r'''Let $\zeta:=X+\boldsymbol Z^\top\boldsymbol\beta^*$. Assume the distribution density function of $\zeta$ conditional on $\boldsymbol Z$, denoted by $\rho(\cdot\mid\boldsymbol Z)$, is positive and bounded uniformly for almost every $\boldsymbol Z$. Furthermore, for any integer $1\leq k\leq\alpha$, the $k$th order derivative of $\rho(\cdot\mid\boldsymbol Z)$ exists and is bounded for almost every $\boldsymbol Z$, where $\alpha$ is the order of $H'(x)$ defined in Assumption 1.''',[15],'Assumption 2',{'D1':'The index uses the covariates and coefficient in model (1).','D5':'The derivative order alpha is explicitly defined by Assumption 1.'},kind='assumption',phrases=['Assumption 2'],symbols=[r'\rho(\cdot\mid\boldsymbol Z)',r'\zeta'],shape='Conditional index density and derivative assumptions for a given model. Preserve the printed boundedness wording; do not replace it with the stronger explicit all-machine uniform bounds of Assumption 6.')
add('D7','conditional cumulative distribution function',r'''Let $F(\cdot\mid\boldsymbol Z)$ denote the conditional cumulative distribution function of the noise $\epsilon$ in (1) given $\boldsymbol Z$, and assume that $\epsilon$ and $X$ are independent given $\boldsymbol Z$. Furthermore, assume that, for $1\leq k\leq\alpha+1$, the $k$th order derivative of $F(\cdot\mid\boldsymbol Z)$ exists and is bounded uniformly for almost every $\boldsymbol Z$.''',[15],'Assumption 3',{'D1':'The conditional law is for the noise in model (1).','D5':'The smoothness order is the same kernel order alpha.'},kind='assumption',phrases=['Assumption 3'],symbols=[r'F(\cdot\mid\boldsymbol Z)'],shape='Conditional noise CDF, conditional independence from X given Z, and derivatives through alpha+1. Does not assume noise independence from Z.')
add('D8','eigenvalue',r'''Define $V:=2\mathbb E[\rho(0\mid\boldsymbol Z)F'(0\mid\boldsymbol Z)\boldsymbol Z\boldsymbol Z^\top]$ and $V_s:=\pi_V\mathbb E[\boldsymbol Z\boldsymbol Z^\top\rho(0\mid\boldsymbol Z)]$, where $\rho$, $F$ are defined in Assumptions 2 and 3 and $\pi_V$ is defined in Assumption 1. Assume that there exists a constant $c_1>1$ such that $c_1^{-1}<\Lambda_{\min}(V)<\Lambda_{\max}(V)<c_1$ and $c_1^{-1}<\Lambda_{\min}(V_s)<\Lambda_{\max}(V_s)<c_1$, where $\Lambda_{\min}$ ($\Lambda_{\max}$) denotes the minimum (maximum) eigenvalue.''',[15],'Assumption 4',{'D5':'The second matrix uses pi_V from the kernel condition.','D6':'Both matrices use the conditional index density at zero.','D7':'V additionally uses the noise-CDF derivative at zero.'},kind='assumption',phrases=['Assumption 4'],symbols=[r'V_s',r'\Lambda_{\min}(V)'],shape='Two population matrices and their printed strict eigenvalue inequalities. V and V_s differ; the min<max inequalities are retained, including their implications for p=1.')
add('D9','sub-Gaussian',r'''Assume that the covariates are sub-Gaussian, that is, there exists $\eta>0$ such that $\sup_{\|\boldsymbol v\|_2=1}\mathbb E e^{\eta(\boldsymbol v^\top\boldsymbol Z)^2}<+\infty$.''',[15],'Assumption 5',kind='assumption',phrases=['Assumption 5','sub-Gaussian'],symbols=[r'\mathbb E e^{\eta(\boldsymbol v^\top\boldsymbol Z)^2}'],shape='Uncentered exponential-square directional moment condition. A property of the covariate law in the active section, not a demand for identical laws across machines.')
add('D10','Smoothed Maximum Score Estimator',r'''
SMSE is defined as
\[
\widehat{\boldsymbol\beta}_{\mathrm{SMSE}}:=\underset{\boldsymbol\beta\in\mathbb R^p}{\operatorname{argmin}}F_h(\boldsymbol\beta)=\underset{\boldsymbol\beta\in\mathbb R^p}{\operatorname{argmin}}\frac1n\sum_{i=1}^n(-y_i)H\left(\frac{x_i+\boldsymbol z_i^\top\boldsymbol\beta}h\right).\tag{4}
\]
''',[12],'Section 2.1 — SMSE (4)',context='To overcome the drawbacks of MSE, Horowitz (1992) proposed a Smoothed Maximum Score Estimator (SMSE)',symbols=[r'\widehat{\boldsymbol\beta}_{\mathrm{SMSE}}'],shape='Smoothed empirical score minimizer for supplied data, bandwidth and smoother H. Nonunique/nonattained argmin conventions are not supplied; this is not a population minimizer or a regularity hypothesis.')
members['D10']['naming_context'][0]['evidence']=[dict(page=11,location='Section 2.1 — introduction of SMSE')]
add('D11','Averaged Smoothed Maximum Score Estimator',r'''
Similarly, the Averaged Smoothed Maximum Score Estimator (Avg-SMSE) is defined by
\[
\widehat{\boldsymbol\beta}_{\texttt{(Avg-SMSE)}}:=\frac1L\sum_{\ell=1}^L\left[\underset{\boldsymbol\beta\in\mathbb R^p}{\operatorname{argmin}}\frac1m\sum_{i\in\mathcal H_\ell}(-y_i)H\left(\frac{x_i+\boldsymbol z_i^\top\boldsymbol\beta}h\right)\right].\tag{6}
\]
''',[12],'Section 2.2 — averaged SMSE (6)',{'D4':'The arithmetic average is over equal-size batches.','D10':'Each term is the SMSE functional applied to a local batch.'},phrases=['Averaged Smoothed Maximum Score Estimator'],symbols=[r'\widehat{\boldsymbol\beta}_{\texttt{(Avg-SMSE)}}'],shape='Unweighted average of batch SMSEs sharing a supplied bandwidth. It does not fix a local-optimal bandwidth or assume Assumption 1 as part of the construction.')
add('D12',['gradient','Hessian'],r'''
Concretely, in the $t$th iteration, for each batch of data $\mathcal D_\ell$, we compute the gradient and Hessian on each local machine $\ell$ by
\[
U_{m,\ell}^{(t)}=\frac1{mh_t}\sum_{i\in\mathcal H_\ell}(-y_i)H'\left(\frac{x_i+\boldsymbol z_i^\top\widehat{\boldsymbol\beta}^{(t-1)}}{h_t}\right)\boldsymbol z_i,
\]
\[
V_{m,\ell}^{(t)}=\frac1{mh_t^2}\sum_{i\in\mathcal H_\ell}(-y_i)H''\left(\frac{x_i+\boldsymbol z_i^\top\widehat{\boldsymbol\beta}^{(t-1)}}{h_t}\right)\boldsymbol z_i\boldsymbol z_i^\top.\tag{8}
\]
''',[13],'Section 2.3 — local derivatives (8)',{'D4':'The derivative sums use the equal-batch indices and local size m.'},phrases=['gradient','Hessian'],symbols=[r'U_{m,\ell}^{(t)}',r'V_{m,\ell}^{(t)}'],shape='Empirical derivative sums evaluated at a supplied iterate with a supplied differentiable smoother. Population U,V,V_s are distinct quantities; these sums do not require population regularity assumptions to be defined.')
add('D13','Multiround Smoothed Maximum Score Estimator',r'''
Compute $U_n^{(t)}=\frac1L\sum_{\ell=1}^LU_{m,\ell}^{(t)}$ and $V_n^{(t)}=\frac1L\sum_{\ell=1}^LV_{m,\ell}^{(t)}$;

Update $\widehat{\boldsymbol\beta}^{(t)}=\widehat{\boldsymbol\beta}^{(t-1)}-(V_n^{(t)})^{-1}U_n^{(t)}$;

Output $\widehat{\boldsymbol\beta}^{(T)}$.
''',[14],'Algorithm 1 — aggregation, update and output',{'D12':'The iteration averages the local derivative quantities defined in (8).'},context='Algorithm 1 Multiround Smoothed Maximum Score Estimator (mSMSE)',symbols=[r'\widehat{\boldsymbol\beta}^{(t)}',r'U_n^{(t)}',r'V_n^{(t)}'],shape='Newton iteration for a supplied initial estimator and bandwidth sequence, using both global gradient and global Hessian averages. The theorem accepts any initial estimator meeting its stated error rate. The source gives no singular-Hessian fallback.')
add('D14','covariate shift',r'''
We first consider a covariate shift setting in Section 4.1, where we assume the marginal distributions of the covariates $X$, $\boldsymbol Z$ are different among the machines, but the regression coefficients $\boldsymbol\beta^*$ remain unchanged.

In this section, we first remove the restriction that the sample size on each machine is the same. Denote the number of observations on the machine $\ell$ to be $m_\ell$, which satisfies $\sum_{\ell=1}^Lm_\ell=n$. Then we have to modify Assumptions 2–4 for different distributions on different machines.
''',[21,22],'Sections 4 and 4.1 — covariate shift and unequal batches',{'D1':'The binary-response model retains a common coefficient while the laws vary by machine.'},kind='source_passage',phrases=['covariate shift'],symbols=[r'\sum_{\ell=1}^Lm_\ell=n'],shape='Common regression coefficient with machine-specific covariate laws and unequal batch sizes. This replaces global identical distribution and equal-size partition assumptions. Section 4.1 also permits machine-specific noise CDFs through Assumption 7.')
add('D15','conditional distribution density function',r'''For $X$ and $\boldsymbol Z$ in $\mathcal H_\ell$, define $\zeta:=X+\boldsymbol Z^\top\boldsymbol\beta^*$, and assume that the conditional distribution density function of $\zeta$, denoted by $\rho_\ell(\cdot\mid\boldsymbol Z)$, is positive and uniformly bounded for almost every $\boldsymbol Z$. Further, for any integer $1\leq k\leq\alpha$, assume that $\rho_\ell^{(k)}(\cdot\mid\boldsymbol Z)$ exists and is uniformly bounded for all $\ell$ and almost every $\boldsymbol Z$, that is, $\exists M_{\rho,k}>0$ such that $\sup_{\zeta,\ell}|\rho_\ell^{(k)}(\zeta\mid\boldsymbol Z)|\leq M_{\rho,k}$.''',[22],'Assumption 6',{'D14':'The density is specific to each machine in the covariate-shift setting.','D5':'The derivative order alpha is the kernel order.'},kind='assumption',phrases=['Assumption 6'],symbols=[r'\rho_\ell(\cdot\mid\boldsymbol Z)'],shape='Machine-indexed conditional index density with explicit uniform derivative bounds across machines; distinct from the homogeneous Assumption 2.')
add('D16','conditional cumulative distribution function',r'''For $X$, $\boldsymbol Z$, $\epsilon$ in $\mathcal H_\ell$, let $F_\ell(\cdot\mid\boldsymbol Z)$ denote the conditional cumulative distribution function of the noise $\epsilon$ given $\boldsymbol Z$, and assume that $\epsilon$ and $X$ are independent given $\boldsymbol Z$. For any integer $1\leq k\leq\alpha+1$, assume that $F_\ell^{(k)}(\cdot\mid\boldsymbol Z)$ exists and is uniformly bounded for all $\ell$ and almost every $\boldsymbol Z$, that is, $\exists M_{F,k}>0$ such that $\sup_{\epsilon,\ell}|F_\ell^{(k)}(\epsilon\mid\boldsymbol Z)|\leq M_{F,k}$. Still, we assume $\operatorname{median}(\epsilon\mid\boldsymbol Z)=0$ on each machine.''',[22],'Assumption 7',{'D14':'The noise law is machine-indexed in Section 4.1.','D5':'Derivatives are required through kernel order alpha+1.'},kind='assumption',phrases=['Assumption 7'],symbols=[r'F_\ell(\cdot\mid\boldsymbol Z)'],shape='Machine-specific noise CDF, conditional independence and median-zero condition, with uniform derivative bounds across machines. The varying F_l must not be collapsed into a single common noise law.')
add('D17','eigenvalues',r'''
Assume that there exists a constant $c_1>1$ such that $c_1^{-1}<\Lambda_{\min}(V_\ell)<\Lambda_{\max}(V_\ell)<c_1$, $c_1^{-1}<\Lambda_{\min}(V_{s,\ell})<\Lambda_{\max}(V_{s,\ell})<c_1$, $\forall\ell$, where
\[
V_\ell:=2\mathbb E_{\boldsymbol Z\in\mathcal H_\ell}(\rho_\ell(0\mid\boldsymbol Z)F'_\ell(0\mid\boldsymbol Z)\boldsymbol Z\boldsymbol Z^\top),\qquad V_{s,\ell}:=\pi_V\mathbb E_{\boldsymbol Z\in\mathcal H_\ell}(\rho_\ell(0\mid\boldsymbol Z)\boldsymbol Z\boldsymbol Z^\top),
\]
with $\pi_V$ defined in Assumption 1.
''',[22],'Assumption 8',{'D5':'The second matrix uses the kernel integral pi_V.','D15':'Both matrices use rho_l at zero.','D16':'V_l additionally uses the machine-specific noise-CDF derivative.'},kind='assumption',context=r'Assumptions 6–8 are parallel to Assumptions 2–4, requiring the uniform boundedness of the higher-order derivatives and the eigenvalues of $V_\ell$ and $V_{s,\ell}$.',phrases=['Assumption 8'],symbols=[r'V_{s,\ell}',r'\Lambda_{\min}(V_\ell)'],shape='Machine-specific population matrices and common strict eigenvalue bounds. The notation E_{Z in H_l} denotes expectation under the machine law, not an empirical sum.')
add('D18','weight matrices',r'''There exist constants $c_w,C_W>0$ such that $c_Wm_\ell/n\leq\|W_\ell\|_2\leq C_Wm_\ell/n$, with $n=\sum_{\ell=1}^Lm_\ell$ and $\sum_{\ell=1}^LW_\ell=I_{p\times p}$.''',[23],'Assumption 9',{'D14':'The weight-size bounds use the potentially unequal local sizes m_l.'},kind='assumption',context=r'To illustrate the choices, we first derive theoretical results for general weight matrices $W_\ell$ that satisfy the following restriction.',phrases=['Assumption 9'],symbols=[r'\|W_\ell\|_2',r'\sum_{\ell=1}^LW_\ell=I_{p\times p}'],shape='Matrix-weight norm bounds and identity sum. The source declares c_w but prints c_W in the lower bound. No positive-definiteness, symmetry or scalar-weight restriction is stated.')
add('D19','objective function',r'''
\[
F_{h,\ell}(\boldsymbol\beta):=\frac1{m_\ell}\sum_{i\in\mathcal H_\ell}(-y_i)H\left(\frac{x_i+\boldsymbol z_i^\top\boldsymbol\beta}h\right).\tag{17}
\]
''',[23],'Section 4.1 — local objective and SMSE (17)',{'D14':'The objective uses each machine size m_l, without equal-size requirements.'},context=r'''where $\widehat{\boldsymbol\beta}_{\mathrm{SMSE},\ell}$ is the SMSE on the $\ell$th machine that minimizes the objective function''',phrases=[],symbols=[r'F_{h,\ell}(\boldsymbol\beta)'],shape='Local empirical objective for machine-specific sample sizes, supplied H and bandwidth. Population regularity and weight constraints are separate theorem hypotheses.')
add('D20','weighted-Averaged SMSE',r'''
Under the modified assumptions, the data on each machine are no longer identically distributed and, therefore, it is natural to allocate a different weight matrix $W_\ell$ to each machine, with $\sum_{\ell=1}^LW_\ell=I_{p\times p}$. Formally, the weighted-Averaged SMSE (wAvg-SMSE) is defined as follows:
\[
\widehat{\boldsymbol\beta}_{\texttt{(wAvg-SMSE)}}:=\sum_{\ell=1}^LW_\ell\widehat{\boldsymbol\beta}_{\mathrm{SMSE},\ell},\tag{16}
\]
''',[23],'Section 4.1 — weighted average (16)',{'D19':'The local SMSEs minimize the machine-specific objectives (17).','D10':'Each weighted summand is the SMSE functional (4) applied to one machine.'},phrases=['weighted-Averaged SMSE'],symbols=[r'\widehat{\boldsymbol\beta}_{\texttt{(wAvg-SMSE)}}'],shape='Matrix-weighted average of local minimizers, with identity-summing weights. Assumption 9 norm bounds are theorem hypotheses, not part of this formula.')
add('D21','weighted mSMSE',r'''
which leads to updating the weighted mSMSE (wmSMSE) in the $t$th iteration by
\[
\widehat{\boldsymbol\beta}^{(t)}_{\texttt{(wmSMSE)}}=\widehat{\boldsymbol\beta}^{(t-1)}_{\texttt{(wmSMSE)}}-\left(\sum_{\ell=1}^LW_\ell\nabla^2F_{h,\ell}(\widehat{\boldsymbol\beta}^{(t-1)}_{\texttt{(wmSMSE)}})\right)^{-1}\left(\sum_{\ell=1}^LW_\ell\nabla F_{h,\ell}(\widehat{\boldsymbol\beta}^{(t-1)}_{\texttt{(wmSMSE)}})\right).\tag{18}
\]
''',[23],'Section 4.1 — weighted multiround update (18)',{'D19':'Both derivative sums are derivatives of the local objectives (17).'},phrases=['weighted mSMSE'],symbols=[r'\widehat{\boldsymbol\beta}^{(t)}_{\texttt{(wmSMSE)}}'],shape='Matrix-weighted Newton update for given initial state, bandwidth and weights. Formula (18) is the defining update; the preceding matrix-valued weighted objective does not itself define a scalar minimization problem. No invertibility fallback is printed.')
add('D22','coefficient shift',r'''
In this section, we consider another type of data heterogeneity by allowing the regression coefficient $\boldsymbol\beta^*$ to be different on different machines, referred to as coefficient shift. This setting is also known as conditional shift in some literature, since the distribution of the response $Y$ conditional on the covariates $(X,\boldsymbol Z)$ depends on $\boldsymbol\beta^*$. Formally, we assume that $y_i=\operatorname{sign}(x_i+\boldsymbol z_i^\top\boldsymbol\beta^*_\ell+\epsilon_i)$ for $i\in\mathcal H_\ell$, $\ell=1,2,\ldots,L$. Without loss of generality, our goal is to estimate the parameter $\boldsymbol\beta^*_1$ on the first machine, and we assume that there exists a nonempty set $\mathcal A^*:=\{\ell:\boldsymbol\beta^*_1=\boldsymbol\beta^*_\ell,\ell=1,\ldots,L\}$ with cardinality $(1-\varepsilon)L$, where $0<\varepsilon<1$. In other words, there are $(1-\varepsilon)L$ machines on which the coefficients $\boldsymbol\beta^*_\ell$ are the same as that on the first machine, while the coefficients on the remaining $\varepsilon L$ machines are shifted away.

To clearly demonstrate the strategy we use to deal with the coefficient shift setting, we assume there is no covariate shift in this section and the local sample size $m$ is identical for all machines, the violation of which is analyzed in the previous Section 4.1.
''',[25],'Section 4.2 — coefficient-shift model',{'D4':'This section explicitly retains equal local sample sizes.'},kind='source_passage',phrases=['coefficient shift'],symbols=[r'\mathcal A^*',r'\boldsymbol\beta^*_1',r'\varepsilon'],shape='Machine-specific coefficients with a target-equal subset of size (1-epsilon)L, no covariate shift and equal batch sizes. This replaces a single globally common coefficient. No minimum separation from shifted coefficients is required in the printed statement.')
add('D23','Multiround Maximum Score Estimator for Coefficient Shift',r'''
Randomly select a subset $\mathcal H_\ell^{(0)}\subset\mathcal H_\ell$, with cardinality $|\mathcal H_\ell^{(0)}|=\lfloor\omega m\rfloor$;

Compute the SMSE $\widehat{\boldsymbol\beta}^{(0)}_{\ell,\mathrm{SMSE}}$ using the subset $\mathcal H_\ell^{(0)}$ with bandwidth $h_0$, and send $\widehat{\boldsymbol\beta}^{(0)}_{\ell,\mathrm{SMSE}}$ back to the first machine;

Compute $\mathcal A=\{\ell:\|\widehat{\boldsymbol\beta}^{(0)}_{\ell,\mathrm{SMSE}}-\widehat{\boldsymbol\beta}^{(0)}_{1,\mathrm{SMSE}}\|_2\leq C_0(\frac{p\log L}{\omega m})^{\frac\alpha{2\alpha+1}}\}$, and let $\widehat{\boldsymbol\beta}^{(0)}_1=\widehat{\boldsymbol\beta}^{(0)}_{1,\mathrm{SMSE}}$;

Compute
\[
\widetilde U_{m,\ell}^{(t)}=\frac1{(1-\omega)mh_t}\sum_{i\in\mathcal H_\ell\setminus\mathcal H_\ell^{(0)}}(-y_i)H'\left(\frac{x_i+\boldsymbol z_i^\top\widehat{\boldsymbol\beta}^{(t-1)}_1}{h_t}\right)\boldsymbol z_i,
\]
\[
\widetilde V_{m,\ell}^{(t)}=\frac1{(1-\omega)mh_t^2}\sum_{i\in\mathcal H_\ell\setminus\mathcal H_\ell^{(0)}}(-y_i)H''\left(\frac{x_i+\boldsymbol z_i^\top\widehat{\boldsymbol\beta}^{(t-1)}_1}{h_t}\right)\boldsymbol z_i\boldsymbol z_i^\top;
\]
Compute $\widetilde U_n^{(t)}=\frac1{|\mathcal A|}\sum_{\ell\in\mathcal A}\widetilde U_{m,\ell}^{(t)}$ and $\widetilde V_n^{(t)}=\frac1{|\mathcal A|}\sum_{\ell\in\mathcal A}\widetilde V_{m,\ell}^{(t)}$;

Update $\widehat{\boldsymbol\beta}^{(t)}_1=\widehat{\boldsymbol\beta}^{(t-1)}_1-(\widetilde V_n^{(t)})^{-1}\widetilde U_n^{(t)}$;

Output $\widehat{\boldsymbol\beta}^{(T)}_1$.
''',[26],'Algorithm 2 — selection and numerical steps',{'D4':'Subsampling and derivative normalization use equal local size m.','D10':'Selection and initialization use local SMSEs on the held-out subsets.','D5':'The selection threshold uses the kernel order alpha.'},context='Algorithm 2 Multiround Maximum Score Estimator for Coefficient Shift',symbols=[r'\mathcal A',r'\widehat{\boldsymbol\beta}^{(t)}_1',r'\widetilde U_{m,\ell}^{(t)}'],shape='Algorithm 2 numerical steps, with local selection then repeated updates on retained machines using complementary observations. Loop and input context is retained separately. The computational definition does not require the true target-equal set as an input.')
add('D24','sparse vector',r'''In this section, we extend (mSMSE) to high-dimensional settings, where the dimension $p$ is much larger than $n$. We assume that $\boldsymbol\beta^*\in\mathbb R^p$ is a sparse vector with $s$ nonzero elements.''',[27],'Section 5 — sparse parameter',{'D1':'The sparse vector is the coefficient of model (1).'},kind='assumption',phrases=['sparse vector'],symbols=[r'\boldsymbol\beta^*\in\mathbb R^p'],shape='Sparse coefficient with s nonzero coordinates. Specific growth conditions are in Theorem 5.1; do not replace them with an invented fixed-dimensional or dense regime.')
add('D25','High-dimensional Multiround Maximum Score Estimator',r'''
Formally, in the $t$th iteration, given $\widehat{\boldsymbol\beta}^{(t-1)}$, the bandwidth $h_t$ and a regularization parameter $\lambda_n^{(t)}$, we compute $\widehat{\boldsymbol\beta}^{(t)}$ by
\[
\widehat{\boldsymbol\beta}^{(t)}=\underset{\boldsymbol\beta\in\mathbb R^p}{\operatorname{argmin}}\left\{\|\boldsymbol\beta\|_1:\left\|V_{m,1}^{(t)}\boldsymbol\beta-\left(V_{m,1}^{(t)}\widehat{\boldsymbol\beta}^{(t-1)}-U_n^{(t)}\right)\right\|_\infty\leq\lambda_n^{(t)}\right\}.\tag{26}
\]
''',[28],'Section 5 — constrained update (26)',{'D12':'The constraint uses the local Hessian on machine 1 and the global mean of local gradients (8).'},context='Algorithm 3 High-dimensional Multiround Maximum Score Estimator',symbols=[r'\lambda_n^{(t)}',r'V_{m,1}^{(t)}',r'\widehat{\boldsymbol\beta}^{(t)}'],shape='Dantzig-style l1 minimization under an infinity-norm linear constraint, with global gradient but a single-machine Hessian. This is not the dense Newton inverse update. Feasibility and argmin selection conventions are not explicitly supplied.')
members['D25']['application_context']=[dict(text=r'''Compute $U_n^{(t)}=\frac1L\sum_{\ell=1}^LU_{m,\ell}^{(t)}$;''',evidence=[dict(page=28,location='Algorithm 3 — step 6')])]
members['D13']['application_context']=[dict(text=r'''for $t=1,2,\ldots,T$ do

Send $\widehat{\boldsymbol\beta}^{(t-1)}$ to each machine;

for $\ell=1,2,\ldots,L$ do

Compute $U_{m,\ell}^{(t)}$, $V_{m,\ell}^{(t)}$ by (8);

Send $U_{m,\ell}^{(t)}$, $V_{m,\ell}^{(t)}$ back to a central machine;''',evidence=[dict(page=14,location='Algorithm 1 — loop and communication steps 2–7')])]
members['D23']['application_context']=[dict(text=r'''Input: Data sets distributed on local machines $\{x_i,\boldsymbol z_i,y_i\}_{i\in\mathcal H_\ell}$ ($\ell=1,2,\ldots,L$), the total number of iterations $T$, bandwidth sequence $\{h_t\}_{t=0}^T$ and preselected constants $\omega$ and $C_0$.

for $\ell=1,2,\ldots,L$ do

for $t=1,2,\ldots,T$ do

for $\ell\in\mathcal A$ do

Send $\widehat{\boldsymbol\beta}^{(t-1)}_1$ to machine $\ell$;

Send $\widetilde U_{m,\ell}^{(t)}$, $\widetilde V_{m,\ell}^{(t)}$ back to the first machine;''',evidence=[dict(page=26,location='Algorithm 2 — input and loop/communication excerpts')])]
# Source-inspected selector amendment; original statements are unchanged.
members['D25']['highlight_symbols'] = ['\\lambda_n^{(t)}', '\\widehat{\\boldsymbol\\beta}^{(t)}']

def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values()),local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
    print('Saved 25 original source interfaces; finalization and source audit remain.')

if __name__ == "__main__":
    main()
