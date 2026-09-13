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
add('D1','convex functions',r'''
The drift function $f$ is assumed to be in $\mathcal F$, the collection of convex functions defined on $[0,1]$ with a unique minimizer $Z(f)=\operatorname*{arg\,min}_{0\leq t\leq1}f(t)$. The minimum value of the function $f$ is denoted by $M(f)$, i.e., $M(f)=\min_{0\leq t\leq1}f(t)=f(Z(f))$.
''',[2],'Section 1 — convex function class, minimizer and minimum',kind='source_passage',phrases=['convex functions'],symbols=[r'\mathcal F',r'Z(f)',r'M(f)'],shape='Real convex functions on the unit interval with a unique attained minimizer and its minimum value; no added differentiability or endpoint-continuity assumption.')
add('D2','white noise model',r'''
We first focus on the white noise model, which is given by
\[
dY(t)=f(t)dt+\varepsilon dW(t),\quad0\leq t\leq1,\tag{1.1}
\]
where $W(t)$ is a standard Brownian motion, and $\varepsilon>0$ is the noise level.
''',[2],'Section 1 — white noise model, equation (1.1)',{'D1':'The drift belongs to the convex function class specified immediately after (1.1).'},kind='source_passage',phrases=['white noise model'],symbols=[r'\varepsilon',r'dY(t)'],shape='Gaussian white-noise observation experiment on [0,1] with positive noise level, distinct from the finite regression experiment.')
add('D3',['function-specific benchmarks','minimizer'],r'''
\[
R_z(\varepsilon;f)=\sup_{g\in\mathcal F}\inf_{\widehat Z}\max_{h\in\{f,g\}}\mathbb E_h|\widehat Z-Z(h)|,\tag{1.2}
\]
''',[2],'Section 1.1 — minimizer estimation benchmark, equation (1.2)',{'D2':'The estimator and expectations belong to the white-noise experiment.','D1':'The two-point risk evaluates the unique minimizer functional.'},context='we define the function-specific benchmarks for estimation of the minimizer and minimum respectively by',symbols=[r'R_z(\varepsilon;f)'],shape='Supremum over a competing function outside the two-point minimax absolute-error risk; preserve sup_g inf_estimator max_h order.')
add('D4',['function-specific benchmarks','minimum'],r'''
\[
R_m(\varepsilon;f)=\sup_{g\in\mathcal F}\inf_{\widehat M}\max_{h\in\{f,g\}}\mathbb E_h|\widehat M-M(h)|.\tag{1.3}
\]
''',[2],'Section 1.1 — minimum estimation benchmark, equation (1.3)',{'D2':'The estimator and expectations belong to the white-noise experiment.','D1':'The loss evaluates the minimum functional.'},context='we define the function-specific benchmarks for estimation of the minimizer and minimum respectively by',symbols=[r'R_m(\varepsilon;f)'],shape='Function-specific two-point minimum-estimation risk with absolute loss and sup-inf-max ordering.')
add('D5','confidence intervals',r'''
Let $\mathcal I_{z,\alpha}(\mathcal F)$ and $\mathcal I_{m,\alpha}(\mathcal F)$ be, respectively, the collection of confidence intervals for the minimizer $Z(f)$ and the minimum $M(f)$ with guaranteed coverage probability $1-\alpha$ for all $f\in\mathcal F$. Let $L(CI)$ be the length of a confidence interval $CI$.
''',[3],'Section 1.1 — coverage classes and interval length',{'D1':'Coverage is for Z(f) or M(f) over the indicated function class.','D2':'Probabilities of these white-noise confidence procedures use experiment (1.1).'},phrases=['confidence intervals'],symbols=[r'\mathcal I_{z,\alpha}',r'\mathcal I_{m,\alpha}',r'L(CI)'],shape='Target-indexed honest confidence-interval classes in the white-noise experiment and ordinary interval length, applied also to a two-point class.')
add('D6',['minimum expected lengths','minimizer'],r'''
\[
L_{z,\alpha}(\varepsilon;f)=\sup_{g\in\mathcal F}\inf_{CI\in\mathcal I_{z,\alpha}(\{f,g\})}\mathbb E_f L(CI),\tag{1.6}
\]
''',[3],'Section 1.1 — minimizer confidence-length benchmark, equation (1.6)',{'D5':'The infimum is over intervals covering both f and g, but length is evaluated only at f.'},context='Let $\mathcal I_{z,\alpha}(\mathcal F)$ and $\mathcal I_{m,\alpha}(\mathcal F)$ be, respectively, the collection of confidence intervals for the minimizer $Z(f)$ and the minimum $M(f)$ with guaranteed coverage probability $1-\alpha$ for all $f\in\mathcal F$. Let $L(CI)$ be the length of a confidence interval $CI$. The minimum expected lengths at $f$ of all confidence intervals in $\mathcal I_{z,\alpha}(\{f,g\})$ and $\mathcal I_{m,\alpha}(\{f,g\})$ with the hardest alternative $g\in\mathcal F$ for $f$ are given by',symbols=[r'L_{z,\alpha}(\varepsilon;f)'],shape='Worst competing-function benchmark for expected minimizer interval length at f, with two-point coverage constraint.')
add('D7',['minimum expected lengths','minimum'],r'''
\[
L_{m,\alpha}(\varepsilon;f)=\sup_{g\in\mathcal F}\inf_{CI\in\mathcal I_{m,\alpha}(\{f,g\})}\mathbb E_f L(CI).\tag{1.7}
\]
''',[3],'Section 1.1 — minimum confidence-length benchmark, equation (1.7)',{'D5':'The infimum uses minimum intervals with two-point coverage and expected length only at f.'},context='The minimum expected lengths at $f$ of all confidence intervals in $\mathcal I_{z,\alpha}(\{f,g\})$ and $\mathcal I_{m,\alpha}(\{f,g\})$ with the hardest alternative $g\in\mathcal F$ for $f$ are given by',symbols=[r'L_{m,\alpha}(\varepsilon;f)'],shape='Worst competing-function benchmark for expected minimum interval length at f, distinct from worst-case length over the pair.')
add('D8','local moduli of continuity',r'''
For any given convex function $f\in\mathcal F$, we define the following local moduli of continuity, one for the minimizer, and the other for the minimum,
\[
\omega_z(\varepsilon;f)=\sup\{|Z(f)-Z(g)|:\|f-g\|_2\leq\varepsilon,\ g\in\mathcal F\},\tag{2.1}
\]
\[
\omega_m(\varepsilon;f)=\sup\{|M(f)-M(g)|:\|f-g\|_2\leq\varepsilon,\ g\in\mathcal F\},\tag{2.2}
\]
''',[6],'Section 2.1 — local moduli, equations (2.1)-(2.2)',{'D1':'Both moduli compare the corresponding functional over the convex class within an L2 ball.'},phrases=['local moduli of continuity'],symbols=[r'\omega_z',r'\omega_m'],shape='Two source-defined functional moduli over a continuous L2 neighborhood; these are not discrete-design moduli and carry no observation-model assumption themselves.')
add('D9','water-filling process',r'''
For $f\in\mathcal F$, $u\in\mathbb R$ and $\varepsilon>0$, let $f_u(t)=\max\{f(t),u\}$ and define
\[
\rho_m(\varepsilon;f)=\sup\{u-M(f):\|f-f_u\|_2\leq\varepsilon\},\tag{2.7}
\]
''',[7],'Section 2.1 — vertical water-filling quantity, equation (2.7)',{'D1':'The clipped function and height are measured above the convex function minimum.'},context='Obtaining $\rho_m(\varepsilon;f)$ and $\rho_z(\varepsilon;f)$ can be viewed as a water-filling process.',symbols=[r'\rho_m(\varepsilon;f)',r'f_u(t)'],shape='Supremal vertical clipping height at a given L2 budget. This source-defined quantity does not assume or invoke the white-noise experiment.')
add('D10','width of the water surface',r'''
\[
\rho_z(\varepsilon;f)=\sup\{|t-Z(f)|:f(t)\leq\rho_m(\varepsilon;f)+M(f),\ t\in[0,1]\}.\tag{2.8}
\]
''',[7],'Section 2.1 — horizontal water-filling quantity, equation (2.8)',{'D9':'The permitted level set is determined by the vertical clipping height rho_m.','D1':'The distance is from the unique minimizer Z(f).'},context='As illustrated in Figure 1, $\rho_m(\varepsilon;f)$ measures the depth of the water (CD), and $\rho_z(\varepsilon;f)$ captures the width of the water surface (FC).',symbols=[r'\rho_z(\varepsilon;f)'],shape='Maximum one-sided distance from the minimizer in a clipped sublevel set; preserve the formula rather than replacing it by full sublevel-set diameter.')
add('D11','Sample Splitting',r'''
Let $B_1(t)$ and $B_2(t)$ be two independent standard Brownian motions, and both be independent of the observed data $Y$. For $t\in[0,1]$, let
\[
\begin{aligned}
Y_l(t)&=Y(t)+\frac{\sqrt2}2\varepsilon B_1(t)+\frac{\sqrt6}2\varepsilon B_2(t),\\
Y_s(t)&=Y(t)+\frac{\sqrt2}2\varepsilon B_1(t)-\frac{\sqrt6}2\varepsilon B_2(t),\\
Y_e(t)&=Y(t)-\sqrt2\varepsilon B_1(t).
\end{aligned}\tag{3.1}
\]
Then $Y_l(\cdot)$, $Y_s(\cdot)$ and $Y_e(\cdot)$ are independent and can be written as
\[
\begin{aligned}
dY_l(t)&=f(t)dt+\sqrt3\varepsilon dW_1(t),\\
dY_s(t)&=f(t)dt+\sqrt3\varepsilon dW_2(t),\\
dY_e(t)&=f(t)dt+\sqrt3\varepsilon dW_3(t),
\end{aligned}\tag{3.2}
\]
where $W_1,W_2$ and $W_3$ are independent standard Brownian motions.
''',[12],'Section 3.1.1 — Sample Splitting',{'D2':'Additional Brownian noise produces three independent copies of the white-noise observation, each with noise variance multiplied by three.'},context='Sample Splitting',symbols=[r'Y_l(t)',r'Y_s(t)',r'Y_e(t)'],shape='Explicit randomized orthogonal Gaussian splitting of the white-noise observation; not a partition of the design points.')
members['D11']['naming_context'][0]['evidence']=[dict(page=11,location='Section 3.1.1 heading')]
add('D12','Localization',r'''
For $j=0,1,\ldots,$ and $i=0,1,\ldots,2^j$, let
\[
m_j=2^{-j},\ t_{j,i}=i\cdot m_j,\ \text{and }i_j^*=\max\{i:Z(f)\in[t_{j,i-1},t_{j,i}]\}.\tag{3.3}
\]
That is, at level $j$ for $j=0,1,\ldots,$ the $i_j^*$-th subinterval is the one containing the minimizer $Z(f)$. For $j=0,1,\ldots,$ and $i=1,2,\ldots,2^j$, define
\[
X_{j,i}=\int_{t_{j,i-1}}^{t_{j,i}}dY_l(t),
\]
where $Y_l$ is one of the three independent copies constructed above through sample splitting. For convenience, we define $X_{j,i}=+\infty$ for $j=0,1,\ldots,$ and $i\in\mathbb Z\setminus\{1,2,\ldots,2^j\}$.

Let $\widehat i_0=1$ and for $j=1,2,\ldots,$ let
\[
\widehat i_j=\operatorname*{arg\,min}_{2\widehat i_{j-1}-2\leq i\leq2\widehat i_{j-1}+1}X_{j,i}.
\]
''',[12,13],'Section 3.1.2 — Localization',{'D11':'The dyadic interval selector uses increments of the localization copy Y_l.'},context='Localization',symbols=[r'\widehat i_j',r'm_j',r'X_{j,i}'],shape='Recursive selection among two children and two neighboring dyadic intervals, with infinite out-of-range increments and i_0=1.')
add('D13','Stopping Rule',r'''
For $j=0,1,\ldots,$ and $i=1,2,\ldots,2^j$, let
\[
\widetilde X_{j,i}=\int_{t_{j,i-1}}^{t_{j,i}}dY_s(t).
\]
Again, for convenience, we define $\widetilde X_{j,i}=+\infty$ for $j=0,1,\ldots,$ and $i\in\mathbb Z\setminus\{1,2,\ldots,2^j\}$. Let the statistic $T_j$ be defined as
\[
T_j=\min\{\widetilde X_{j,\widehat i_j+6}-\widetilde X_{j,\widehat i_j+5},\widetilde X_{j,\widehat i_j-6}-\widetilde X_{j,\widehat i_j-5}\},
\]
where we use the convention $+\infty-x=+\infty$ and $\min\{+\infty,x\}=x$, for any $-\infty\leq x\leq\infty$.

Let $\sigma_j^2=6m_j\varepsilon^2$.

Finally, the iterations stop at level $\widehat j$ where
\[
\widehat j=\min\{j:T_j/\sigma_j\leq2\}.
\]
The subinterval containing the minimizer $Z(f)$ is localized to be $[t_{\widehat j,\widehat i_{\widehat j}-1},t_{\widehat j,\widehat i_{\widehat j}}]$.
''',[13,14],'Section 3.1.3 — Stopping Rule',{'D11':'The independent copy Y_s supplies stopping increments.','D12':'The contrasts use the current dyadic selector and interval scale.'},context='Stopping Rule',symbols=[r'T_j',r'\widehat j',r'\widetilde X_{j,i}'],shape='First dyadic scale where the smaller of the two remote adjacent-increment contrasts falls below two standard deviations; source infinity arithmetic is retained.')
members['D13']['excerpt_selection']='Defining passages for increments, T_j, sigma_j and stopping level; the intervening Gaussian-law explanation and proof intuition are omitted.'
add('D14',['estimator','minimizer'],r'''
The estimator of $Z(f)$ is given by the midpoint of the interval $[t_{\widehat j,\widehat i_{\widehat j}-1},t_{\widehat j,\widehat i_{\widehat j}}]$, i.e.,
\[
\widehat Z=\frac{t_{\widehat j,\widehat i_{\widehat j}}+t_{\widehat j,\widehat i_{\widehat j}-1}}2.\tag{3.5}
\]
''',[14],'Section 3.1.4 — white-noise minimizer estimator, equation (3.5)',{'D13':'The estimator is the midpoint of the stopped dyadic interval.'},context='We begin with the minimizer $Z(f)$. The estimator of',symbols=[r'\widehat Z'],shape='Stopped dyadic-interval midpoint in the white-noise construction, distinct from the two-branch discrete-design estimator.')
add('D15',['confidence interval','minimizer'],r'''
To construct the confidence interval for $Z(f)$, one needs to take a few steps to the left and to the right at level $\widehat j$. Let $K_\alpha=\left\lceil\frac{\log\alpha}{\log\Phi(-2)}\right\rceil$ and define
\[
L=\max\{0,\widehat i_{\widehat j}-12\times2^{K_\alpha}+1\},\quad U=\min\{2^{\widehat j},\widehat i_{\widehat j}+12\times2^{K_\alpha}-2\}.
\]
The $1-\alpha$ confidence interval for $Z(f)$ is given by
\[
CI_{z,\alpha}=[t_{\widehat j,L},t_{\widehat j,U}].\tag{3.6}
\]
''',[14],'Section 3.1.4 — white-noise minimizer interval, equation (3.6)',{'D13':'Endpoints enlarge the stopped dyadic interval.','D37':'The enlargement uses the Gaussian-tail calibration K_alpha.'},context='We begin with the minimizer $Z(f)$.',symbols=[r'CI_{z,\alpha}'],shape='Stopped-level neighboring-interval expansion clipped to [0,1], calibrated by K_alpha.')
# The term minimizer is in the immediately preceding paragraph on the same page.
members['D15']['naming_context'][0]['text']='We begin with the minimizer $Z(f)$.'
add('D16','minimum',r'''
For estimation of and confidence interval for the minimum $M(f)$, define
\[
\overline X_{j,i}=\int_{t_{j,i-1}}^{t_{j,i}}Y_e(t)dt.
\]
''',[14],'Section 3.1.4 — estimation-copy integral',{'D11':'The integral is formed from the estimation copy Y_e.','D12':'Its endpoints use the dyadic grid.'},symbols=[r'\overline X_{j,i}'],shape='Printed ordinary integral of the process Y_e(t) against dt; the source does not print dY_e(t), and this discrepancy is not repaired.')
add('D17',['estimator','minimum'],r'''
Let $\widetilde i_{\widehat j}=\widehat i_{\widehat j}+2\left(\mathbf1\{\widetilde X_{\widehat j,\widehat i_{\widehat j}+6}-\widetilde X_{j,\widehat i_{\widehat j}+5}\leq2\sigma_{\widehat j}\}-\mathbf1\{\widetilde X_{\widehat j,\widehat i_{\widehat j}-6}-\widetilde X_{j,\widehat i_{\widehat j}-5}\leq2\sigma_{\widehat j}\}\right)$ and define the final estimator of the minimum $M(f)$ by
\[
\widehat M=\frac1{m_{\widehat j}}\overline X_{\widehat j,\widetilde i_{\widehat j}}.\tag{3.7}
\]
''',[14],'Section 3.1.4 — white-noise minimum estimator, equation (3.7)',{'D13':'The selected scale and stopping contrasts determine the shifted block.','D16':'The reported minimum is the estimation-copy integral divided by interval length.'},symbols=[r'\widehat M',r'\widetilde i_{\widehat j}'],shape='Two-block directional shift followed by an estimation-copy block average; retain the printed un-hatted j in the two subtracted contrast terms.')
add('D18','maximum',r'''
Let $F_n$ be the cumulative distribution function of $\widetilde v_n=\max\{v_1,\ldots,v_n\}$, where $v_1,\ldots,v_n\overset{\mathrm{i.i.d.}}\sim N(0,1)$, and define
\[
S_{n,\beta}=F_n^{-1}(1-\beta).\tag{3.9}
\]
In other words, $S_{n,\beta}$ is the $(1-\beta)$ quantile of the distribution of the maximum of $n$ i.i.d. standard normal variables.
''',[15],'Section 3.1.4 — Gaussian-maximum quantile, equation (3.9)',symbols=[r'S_{n,\beta}'],shape='Quantile of the maximum of n independent standard Gaussians, shared by white-noise and regression intervals without importing either observation model.')
add('D19',['confidence interval','minimum'],r'''
We now construct confidence interval for $M(f)$. Recall that $K_\alpha=\left\lceil\frac{\log\alpha}{\log\Phi(-2)}\right\rceil$. Compared with the confidence interval for the minimizer, we take four more blocks on each side at the level $(\widehat j-K_{\alpha/4}-1)_+$. More specifically, we define
\[
t_L=t_{(\widehat j-K_{\alpha/4}-1)_+,\widehat i_{(\widehat j-K_{\alpha/4}-1)_+}-5},\quad t_R=t_{(\widehat j-K_{\alpha/4}-1)_+,\widehat i_{(\widehat j-K_{\alpha/4}-1)_+}+4}.
\]
Set
\[
\widetilde K_\alpha=\max\{4,2+\lceil\log_2(2+z_{\alpha/3})\rceil\}.\tag{3.8}
\]
Note that at level $\widehat j+\widetilde K_{\alpha/4}$, the indices of the intervals with right endpoints $t_L,t_R$ respectively are
\[
i_L=t_L\cdot2^{\widehat j+\widetilde K_{\alpha/4}}\quad\text{and}\quad i_R=t_R\cdot2^{\widehat j+\widetilde K_{\alpha/4}}.
\]
Note also that $i_R-i_L=9\times2^{1+\widetilde K_{\alpha/4}+K_{\alpha/4}}$, which only depends on $\alpha$. Define an intermediate estimator of the minimum $M(f)$ by
\[
\widehat f_1=\frac1{m_{\widehat j+\widetilde K_{\alpha/4}}}\min_{i_L<i\leq i_R}\overline X_{\widehat j+\widetilde K_{\alpha/4},i}.
\]
Let
\[
f_{lo}=\widehat f_1-z_{\alpha/4}\frac{\sqrt3\varepsilon}{\sqrt{m_{\widehat j+\widetilde K_{\alpha/4}}}}-\frac{\sqrt3\varepsilon}{\sqrt{m_{\widehat j+\widetilde K_{\alpha/4}}}},\quad f_{hi}=\widehat f_1+S_{i_R-i_L,\alpha/4}\cdot\frac{\sqrt3\varepsilon}{\sqrt{m_{\widehat j+\widetilde K_{\alpha/4}}}}.
\]
Then the $(1-\alpha)$ level confidence interval for $M(f)$ is defined as
\[
CI_{m,\alpha}=[f_{lo},f_{hi}].\tag{3.10}
\]
''',[15],'Section 3.1.4 — white-noise minimum interval, equations (3.8)-(3.10)',{'D13':'The interval looks back from the white-noise stopping level.','D16':'Its intermediate minimum uses the estimation-copy block integrals.','D18':'The upper endpoint uses a Gaussian-maximum quantile.','D37':'Both look-back and look-forward levels use the Gaussian-tail calibration constants.'},symbols=[r'CI_{m,\alpha}'],shape='Multiscale minimum interval using a coarse location window and finer estimation-copy integrals; original endpoint indices and asserted block-count equality are retained.')
members['D19']['excerpt_selection']='Full construction with the separately archived definition of S_n,beta omitted between the intermediate estimator and endpoint formulas.'
add('D37','confidence interval',r'''
Let $K_\alpha=\left\lceil\frac{\log\alpha}{\log\Phi(-2)}\right\rceil$
\[
\widetilde K_\alpha=\max\{4,2+\lceil\log_2(2+z_{\alpha/3})\rceil\}.\tag{3.8}
\]
''',[14,15],'Section 3.1.4 — tail-calibration constants',context='To construct the confidence interval for $Z(f)$',symbols=[r'K_\alpha',r'\widetilde K_\alpha'],shape='Scalar look-back and refinement calibrations from standard-normal quantiles, reused in both models; they do not depend on white-noise data.')
members['D37']['excerpt_selection']='The original definition of K_alpha from page 14 and the separate displayed definition of K-tilde-alpha on page 15.'
add('D20','nonparametric regression',r'''
The procedures and results presented in the previous sections can be extended to nonparametric regression, where we observe
\[
y_i=f(x_i)+\sigma z_i,\quad i=0,1,2,\ldots,n,\tag{4.1}
\]
with $x_i=i/n$, and $z_i\overset{\mathrm{i.i.d.}}\sim N(0,1)$. The noise level $\sigma$ is assumed to be known. The tasks are the same as before: construct optimal estimators and confidence intervals for the minimizer and minimum of $f\in\mathcal F$.
''',[16],'Section 4 — nonparametric regression model, equation (4.1)',{'D1':'The same convex class and extremum functionals are used under a different observation experiment.'},kind='source_passage',phrases=['nonparametric regression'],symbols=[r'y_i',r'\sigma'],shape='n+1 independent Gaussian observations at i/n, i=0,...,n, with known noise scale; preserve discretization rather than replacing it by white noise.')
add('D21','confidence intervals',r'''
Denote by $\mathcal I_{z,\alpha,n}(\mathfrak F)$ and $\mathcal I_{m,\alpha,n}(\mathfrak F)$ respectively the collections of $(1-\alpha)$ level confidence intervals for $Z(f)$ and $M(f)$ on a function class $\mathfrak F$ under the regression model (4.1)
''',[17],'Section 4.1 — regression coverage classes',{'D20':'Coverage probabilities use the discrete-design Gaussian regression experiment.','D1':'The targets are the minimizer and minimum functionals.'},phrases=['confidence intervals'],symbols=[r'\mathcal I_{z,\alpha,n}',r'\mathcal I_{m,\alpha,n}'],shape='Regression confidence-interval classes indexed by a supplied function class, including two-point classes in the benchmark definitions.')
for lid,target,symbol,formula in [
 ('D22','minimizer',r'\widetilde R_{z,n}',r'\widetilde R_{z,n}(\sigma;f)=\sup_{g\in\mathcal F}\inf_{\widehat Z}\max_{h\in\{f,g\}}\mathbb E_h|\widehat Z-Z(h)|,'),
 ('D23','minimum',r'\widetilde R_{m,n}',r'\widetilde R_{m,n}(\sigma;f)=\sup_{g\in\mathcal F}\inf_{\widehat M}\max_{h\in\{f,g\}}\mathbb E_h|\widehat M-M(h)|,'),
 ('D24','minimizer',r'\widetilde L_{z,\alpha,n}',r'\widetilde L_{z,\alpha,n}(\sigma;f)=\sup_{g\in\mathcal F}\inf_{CI\in\mathcal I_{z,\alpha,n}(\{f,g\})}\mathbb E_f L(CI),'),
 ('D25','minimum',r'\widetilde L_{m,\alpha,n}',r'\widetilde L_{m,\alpha,n}(\sigma;f)=\sup_{g\in\mathcal F}\inf_{CI\in\mathcal I_{m,\alpha,n}(\{f,g\})}\mathbb E_f L(CI).')]:
 add(lid,'benchmarks',r'\['+'\n'+formula+'\n'+r'\]',[17],'Section 4.1 — regression '+target+(' risk' if lid in ['D22','D23'] else ' confidence-length')+' benchmark, equation (4.2)',{'D20':'The competing-function risk and expected length use regression observations at the fixed design points.'} if lid in ['D22','D23'] else {'D21':'The infimum is over two-point honest regression confidence intervals; expected length is evaluated at f alone.'},context='we define similar benchmarks for the nonparametric regression model (4.1) with $n+1$ equally spaced observations.',symbols=[symbol],shape='Discrete-design '+target+(' two-point minimax risk with sup-inf-max order.' if lid in ['D22','D23'] else ' function-specific expected-length benchmark with two-point coverage.'))
add('D26','Data Splitting',r'''
Let $z_{1,0},z_{1,1},\ldots,z_{1,n},z_{2,0},z_{2,1},\ldots,z_{2,n}$ be i.i.d. standard normal random variables, and all be independent of the observed data $\{y_1,...,y_n\}$. We construct the following three sequences:
\[
\begin{aligned}
y_{l,i}&=y_i+\frac{\sqrt2}2\sigma z_{1,i}+\frac{\sqrt6}2\sigma z_{2,i},\\
y_{s,i}&=y_i+\frac{\sqrt2}2\sigma z_{1,i}-\frac{\sqrt6}2\sigma z_{2,i},\\
y_{e,i}&=y_i-\sqrt2\sigma z_{1,i},
\end{aligned}\tag{4.3}
\]
for $i=0,\ldots,n$. For convenience, let $y_{l,i}=y_{s,i}=y_{e,i}=\infty$ for $i\notin\{0,1,\ldots,n\}$. It is easy to see that these random variables are all independent with the same variance $3\sigma^2$ for $i\in\{0,1,\ldots,n\}$. We will use $\{y_{l,i}\}$ for localization, $\{y_{s,i}\}$ for devising the stopping rule, and $\{y_{e,i}\}$ for constructing the final estimation and inference procedures.
''',[17],'Section 4.2.1 — Data Splitting',{'D20':'Gaussian augmentation is applied to each regression observation with known sigma.'},context='Data Splitting',symbols=[r'y_{l,i}',r'y_{s,i}',r'y_{e,i}'],shape='Three independent Gaussian copies at every design point, with variance 3 sigma squared; preserve the printed independence reference omitting y_0.')
add('D27','block',r'''
Let $J=\lfloor\log_2(n+1)\rfloor$. For $j=0,1,\ldots,J$, $i=1,2,\ldots,\left\lfloor\frac{n+1}{2^{J-j-1}}\right\rfloor$, the $i$-th block at level $j$ consists of $\{x_{(i-1)2^{J-j}},x_{(i-1)2^{J-j}+1},\ldots,x_{i\cdot2^{J-j}-1}\}$. Denote the sum of the observations in the $i$-th block at level $j$ for the sequence $u$ ($u=l,s,e$) as
\[
Y_{j,i,u}=\sum_{k=(i-1)2^{J-j}}^{i\cdot2^{J-j}-1}y_{u,k},\quad\text{for }u=l,s,e.
\]
Again, let $Y_{j,i,u}=+\infty$ when $i\in\mathbb Z\setminus\left\{1,2,\ldots,\left\lfloor\frac{n+1}{2^{J-j-1}}\right\rfloor\right\}$, for $u=l,s,e$.
''',[17,18],'Section 4.2.1 — regression block sums',{'D26':'The block sums use each of the three augmented observation sequences.'},symbols=[r'Y_{j,i,u}',r'J=\lfloor\log_2(n+1)\rfloor'],shape='Dyadic design-point block sums with horizon J; the printed denominator 2^(J-j-1) in the block-count bound is retained despite allowing twice as many blocks as the localization cap.')
add('D28','Localization',r'''
We now use $\{y_{l,i},i=0,\ldots,n\}$ to construct a localization procedure. Let $\widehat{\mathtt i}_0=1$, and for $j=1,2,\ldots,J$, let
\[
\widehat{\mathtt i}_j=\operatorname*{arg\,min}_{\max\{2\widehat{\mathtt i}_{j-1}-2,1\}\leq i\leq\min\{2\widehat{\mathtt i}_{j-1}+1,\lfloor(n+1)/2^{J-j}\rfloor\}}Y_{j,i,l}.
\]
''',[18],'Section 4.2.2 — Localization',{'D27':'The selector minimizes localization-copy sums over neighboring valid design blocks.'},context='Localization',symbols=[r'\widehat{\mathtt i}_j'],shape='Finite-horizon dyadic block localization with explicit lower and upper candidate bounds; the cap uses 2^(J-j), unlike the preceding block-definition bound.')
add('D29','Stopping Rule',r'''
Similar to the stopping rule for the white noise model, define the statistic $T_j$ as
\[
T_j=\min\{Y_{j,\widehat{\mathtt i}_j+6,s}-Y_{j,\widehat{\mathtt i}_j+5,s},Y_{j,\widehat{\mathtt i}_j-6,s}-Y_{j,\widehat{\mathtt i}_j-5,s}\}.
\]
Let $\widetilde\sigma_j^2=6\times2^{J-j}\sigma^2$.

Define
\[
\check j=\begin{cases}
\min\{j:T_j\leq2\widetilde\sigma_j\}&\text{if }\{j:T_j\leq2\widetilde\sigma_j\}\cap\{0,1,2,\ldots,J\}\ne\varnothing\\
\infty&\text{otherwise}
\end{cases}
\]
and terminate the algorithm at level $\widehat{\mathtt j}=\min\{J,\check j\}$. So, either $T_j$ triggers the stopping rule for some $0\leq j\leq J$ or the algorithm reaches the highest possible level $J$.
With the localization strategy and the stopping rule, the final block, the $\widehat{\mathtt i}_{\widehat{\mathtt j}}$-th block at level $\widehat{\mathtt j}$, is given by $\{x_k:(\widehat{\mathtt i}_{\widehat{\mathtt j}}-1)2^{J-\widehat{\mathtt j}}\leq k\leq\widehat{\mathtt i}_{\widehat{\mathtt j}}2^{J-\widehat{\mathtt j}}-1\}$.
''',[18],'Section 4.2.3 — Stopping Rule',{'D28':'The remote-block contrasts are centered around the current localized block.','D27':'The stopping-copy block sums, scale and maximum level J come from the regression block construction.'},context='Stopping Rule',symbols=[r'\check j',r'\widehat{\mathtt j}',r'\widetilde\sigma_j'],shape='Threshold stopping with explicit no-trigger infinity state and finite cap J; it is not the unbounded white-noise stopping time.')
members['D29']['excerpt_selection']='Defining contrast, variance and stopping passages; the Gaussian-law explanation (4.4) between them is omitted.'
add('D30',['estimator','minimizer'],r'''
The estimator of $Z(f)$ is given as follows:
\[
\widehat Z=\begin{cases}
-\frac1{2n}+\frac1n(2^{J-\widehat{\mathtt j}}\widehat{\mathtt i}_{\widehat{\mathtt j}}-2^{J-\widehat{\mathtt j}-1}),&\check j<\infty\\
\frac1n\operatorname*{arg\,min}_{\widehat{\mathtt i}_{\widehat{\mathtt j}}-2\leq i\leq\widehat{\mathtt i}_{\widehat{\mathtt j}}+2}y_{e,i-1}-\frac1n,&\check j=\infty.
\end{cases}\tag{4.5}
\]
''',[19],'Section 4.2.4 — regression minimizer estimator, equation (4.5)',{'D29':'The branch is selected by threshold triggering versus forced termination at J.','D26':'The no-trigger branch searches nearby observations in the estimation copy.'},context='we use it to construct estimators and confidence intervals for the minimizer $Z(f)$ and the minimum $M(f)$.',symbols=[r'\widehat Z'],shape='Stopped-block midpoint when a threshold triggers, otherwise local argmin among estimation-copy observations; both branches are retained.')
# Adjacent prose names the target explicitly.
members['D30'].setdefault('naming_context',[])
add('D31','Algorithm 1',r'''
$L\leftarrow\max\{1,\widehat{\mathtt i}_{\widehat{\mathtt j}}-12\times2^{K_{\alpha/2}}\}-1$, $U\leftarrow\min\{n+1,\widehat{\mathtt i}_{\widehat{\mathtt j}}+12\times2^{K_{\alpha/2}}\}-1$, $\alpha_1\leftarrow\alpha/8$, $\alpha_2=\alpha/24$

Generate $z_{3,0},z_{3,1}\ldots,z_{3,n}\overset{\mathrm{i.i.d.}}\sim N(0,1)$

$i_l\leftarrow\min\{\{U\}\cup\{i\in[L,U-1]:y_{e,i}+\sqrt3\sigma z_{3,i}-(y_{e,i+1}+\sqrt3\sigma z_{3,i+1})\leq2\sqrt3\sigma z_{\alpha_1}\}\}$

$i_r\leftarrow\max\{\{L-1\}\cup\{i\in[L,U-1]:y_{e,i}+\sqrt3\sigma z_{3,i}-(y_{e,i+1}+\sqrt3\sigma z_{3,i+1})\geq-2\sqrt3\sigma z_{\alpha_1}\}\}$

if $i_l=U$ then

if $i_l=n$ and $y_{e,n-2}-y_{e,n-1}-\sqrt3\sigma(z_{3,n-2}-z_{3,n-1})+2\sqrt6\sigma z_{\alpha_2}>0$ then

$t_{hi}\leftarrow1$
\[
t_{lo}\leftarrow\left(\left(-\frac{y_{e,n}-y_{e,n-1}-\sqrt3\sigma(z_{3,n}-z_{3,n-1})+2\sqrt6\sigma z_{\alpha_2}}{n(y_{e,n-2}-y_{e,n-1}-\sqrt3\sigma(z_{3,n-2}-z_{3,n-1})+2\sqrt6\sigma z_{\alpha_2})}+\frac{n-1}n\right)\vee\frac{n-1}n\right)\wedge\frac nn,
\]
else

$t_{lo}=t_{hi}=U/n$

end if

end if

if $i_r=L-1$ then

if $i_r=-1$ and $y_{e,2}-y_{e,1}-\sqrt3\sigma(z_{3,2}-z_{3,1})+2\sqrt6\sigma z_{\alpha_2}>0$ then
\[
t_{hi}\leftarrow\left(\left(\frac{y_{e,0}-y_{e,1}-\sqrt3\sigma(z_{3,0}-z_{3,1})+2\sqrt6\sigma z_{\alpha_2}}{n(y_{e,2}-y_{e,1}-\sqrt3\sigma(z_{3,2}-z_{3,1})+2\sqrt6\sigma z_{\alpha_2})}+\frac1n\right)\vee\frac0n\right)\wedge\frac1n,\quad t_{lo}=0
\]
else

$t_{lo}=t_{hi}=0$

end if

end if

if $(i_l-U)(i_r-L+1)\ne0$ then

$i_{lo}\leftarrow(i_l-1)\vee L$, $i_{hi}\leftarrow(i_r+2)\wedge U$

if $i_{hi}-i_{lo}\geq3$ or $(i_{hi}-n)i_{lo}=0$ then

$t_{lo}=i_{lo}/n$, $t_{hi}=i_{hi}/n$

else if $y_{e,i_{hi}+1}-y_{e,i_{hi}}-\sqrt3\sigma(z_{3,i_{hi}+1}-z_{3,i_{hi}})\leq-2\sqrt6\sigma z_{\alpha_2}$ or $y_{e,i_{lo}-1}-y_{e,i_{lo}}-\sqrt3\sigma(z_{3,i_{lo}-1}-z_{3,i_{lo}})\leq-2\sqrt6\sigma z_{\alpha_2}$ then

$t_{lo}=t_{hi}=(i_{hi}+i_{lo})/2n$

else
\[
t_{hi}\leftarrow\left(\left(\frac{y_{e,i_{hi}-1}-y_{e,i_{hi}}-\sqrt3\sigma(z_{3,i_{hi}-1}-z_{3,i_{hi}})+2\sqrt6\sigma z_{\alpha_2}}{n(y_{e,i_{hi}+1}-y_{e,i_{hi}}-\sqrt3\sigma(z_{3,i_{hi}+1}-z_{3,i_{hi}})+2\sqrt6\sigma z_{\alpha_2})}+\frac{i_{hi}}n\right)\vee\frac{i_{hi}-1}n\right)\wedge\frac{i_{hi}}n
\]
\[
t_{lo}\leftarrow\left(\left(-\frac{y_{e,i_{lo}+1}-y_{e,i_{lo}}-\sqrt3\sigma(z_{3,i_{lo}+1}-z_{3,i_{lo}})+2\sqrt6\sigma z_{\alpha_2}}{n(y_{e,i_{lo}-1}-y_{e,i_{lo}}-\sqrt3\sigma(z_{3,i_{lo}-1}-z_{3,i_{lo}})+2\sqrt6\sigma z_{\alpha_2})}+\frac{i_{lo}}n\right)\vee\frac{i_{lo}}n\right)\wedge\frac{i_{lo}+1}n
\]
end if

end if
''',[20],'Algorithm 1 — Computing t_lo and t_hi when check-j is infinite',{'D29':'The algorithm is invoked in the no-trigger branch and uses its last localized block.','D26':'The slope comparisons use the estimation copy and additional Gaussian variables.','D37':'The initial window width is calibrated by K_(alpha/2).'},kind='source_passage',context='Algorithm 1 Computing $t_{lo}$ and $t_{hi}$ when $\check j=\infty$',symbols=[r'i_l',r'i_r'],shape='Complete source pseudocode for the no-trigger minimizer-interval endpoint computation, including both boundary cases, local slope tests, fallback point intervals and clipped line-intersection formulas.')
add('D32',['confidence interval','minimizer'],r'''
To construct the confidence interval for $Z(f)$, we take a few adjacent blocks to the left and right of $\widehat{\mathtt i}_{\widehat{\mathtt j}}$-th block at level $\widehat{\mathtt j}$. Let
\[
L=\max\{0,\widehat{\mathtt i}_{\widehat{\mathtt j}}-12\times2^{K_{\alpha/2}}+1\}\quad\text{and}\quad U=\min\{\lceil(n+1)2^{\widehat{\mathtt j}-J}\rceil,\widehat{\mathtt i}_{\widehat{\mathtt j}}+12\times2^{K_{\alpha/2}}-2\}.
\]
When $\check j<\infty$, let
\[
t_{lo}=\frac{2^{J-\widehat{\mathtt j}}}n L-\frac1{2n}\quad\text{and}\quad t_{hi}=\frac{2^{J-\widehat{\mathtt j}}}n U-\frac1{2n}.
\]
When $\check j=\infty$, $t_{lo}$ and $t_{hi}$ are calculated by the following Algorithm 1. Note that $\check j=\infty$ means that the procedure is forced to end and the discretization error can be dominant.

The $(1-\alpha)$-level confidence interval for the minimizer $Z(f)$ is given by
\[
\mathrm{CI}_{z,\alpha}=[t_{lo}\wedge t_{hi},t_{hi}]\tag{4.7}
\]
''',[19,20],'Section 4.2.4 — regression minimizer interval, equation (4.7)',{'D29':'The triggering state chooses between the displayed endpoints and the no-trigger refinement.','D31':'Algorithm 1 supplies both endpoints in the no-trigger branch.','D37':'The triggered window uses K_(alpha/2).'},symbols=[r'\mathrm{CI}_{z,\alpha}'],shape='Two-branch discrete-design minimizer confidence interval, with printed lower endpoint min(t_lo,t_hi) and no silently added clipping to [0,1].')
add('D33',['estimator','minimum'],r'''
We now construct the estimator and confidence interval for the minimum $M(f)$. Let $\Delta=\mathbf1\{Y_{\widehat{\mathtt j},\widehat{\mathtt i}_{\widehat{\mathtt j}}+6,s}-Y_{\widehat{\mathtt j},\widehat{\mathtt i}_{\widehat{\mathtt j}}+5,s}\leq2\sqrt6\sigma\sqrt{2^{J-\widehat{\mathtt j}}}\}-\mathbf1\{Y_{\widehat{\mathtt j},\widehat{\mathtt i}_{\widehat{\mathtt j}}-6,s}-Y_{\widehat{\mathtt j},\widehat{\mathtt i}_{\widehat{\mathtt j}}-5,s}\leq2\sqrt6\sigma\sqrt{2^{J-\widehat{\mathtt j}}}\}$ and define
\[
\widetilde{\mathtt i}_{\widehat{\mathtt j}}=\begin{cases}\widehat{\mathtt i}_{\widehat{\mathtt j}}+2\Delta&\text{if }\check j<\infty\\\operatorname*{arg\,min}_{\widehat{\mathtt i}_{\widehat{\mathtt j}}-2\leq i\leq\widehat{\mathtt i}_{\widehat{\mathtt j}}+2}y_{e,i-1}&\text{if }\check j=\infty.\end{cases}\tag{4.8}
\]
The estimator of $M(f)$ is then given by the average of the observations of the copy for estimation and inference in the $\widetilde{\mathtt i}_{\widehat{\mathtt j}}$-th block at level $\widehat{\mathtt j}$,
\[
\widehat M=\frac1{2^{J-\widehat{\mathtt j}}}Y_{\widehat{\mathtt j},\widetilde{\mathtt i}_{\widehat{\mathtt j}},e}.\tag{4.9}
\]
''',[21],'Section 4.2.4 — regression minimum estimator, equations (4.8)-(4.9)',{'D29':'Threshold contrasts determine the shift in the triggered branch, with a separate no-trigger local argmin.','D27':'The minimum estimate averages estimation-copy observations in the selected block.'},symbols=[r'\widehat M',r'\Delta'],shape='Triggered directional shift or no-trigger neighboring point search, followed by a block average; both branches belong to the regression experiment.')
add('D34','intermediate estimator',r'''
To construct the confidence interval for $M(f)$, we specify two levels $j_s$ and $j_l$, with
\[
j_s=\max\{0,\widehat{\mathtt j}-K_{\alpha/4}-1\}\quad\text{and}\quad j_l=\min\{J,\widehat{\mathtt j}+\widetilde K_{\alpha/4}\},
\]
where $\widetilde K_{\alpha/4}$ is defined as in Equation (3.8).

Define
\[
I_{lo}=\max\{1,2^{j_l-j_s}(\widehat{\mathtt i}_{j_s}-5)\},\quad I_{hi}=\min\left\{2^{j_l-j_s}(\widehat{\mathtt i}_{j_s}+4)+1,\left\lceil\frac{n+1}{2^{J-j_l}}\right\rceil\right\}.
\]
Define an intermediate estimator for $M(f)$ by
\[
\widehat{\mathtt f}_1=\min_{I_{lo}\leq i\leq I_{hi}}\frac1{2^{J-j_l}}Y_{j_l,i,e}.
\]
Let
\[
f_{hi}=\widehat{\mathtt f}_1+S_{I_{hi}-I_{lo}+1,\alpha/4}\frac{\sqrt3\sigma}{\sqrt{2^{J-j_l}}}
\]
where $S_{n,\beta}$ is defined in Equation (3.9) in Section 3. This is the upper limit of the confidence interval, now we define the lower limit $f_{lo}$.
''',[21],'Section 4.2.4 — regression minimum interval levels, window and upper endpoint',{'D29':'The stopped level and preceding localized indices determine the coarse and fine windows.','D27':'The intermediate estimator minimizes block averages of the estimation copy.','D18':'The upper endpoint uses the maximum-Gaussian quantile.','D37':'The coarse and fine levels use K and K-tilde calibration constants.'},symbols=[r'\widehat{\mathtt f}_1',r'I_{lo}',r'I_{hi}'],shape='Common setup for both lower-endpoint branches of the regression minimum interval; the ceiling may include a partial boundary block, retained as printed.')
members['D34']['excerpt_selection']='Defining passages for levels, window indices, intermediate estimator and upper endpoint; intervening probability assertions are not part of the construction.'
add('D35','Algorithm 2',r'''
$H\leftarrow S_{I_{hi}-I_{lo}+3,\alpha/8}\sqrt3\sigma$, $k_l\leftarrow I_{lo}-1$, $k_r\leftarrow I_{hi}-2$

if $I_{lo}=1$ then

$v_{r,0}(t)\leftarrow\frac{y_{e,2}-y_{e,1}+2H}{1/n}(t-1/n)+y_{e,1}-H$, $h(0)\leftarrow\min_{t\in[0,1/n]}v_{r,0}(t)$, $k_l\leftarrow I_{lo}$

end if

if $I_{hi}-1=n$ then

$v_{l,n-1}(t)\leftarrow\frac{y_{e,n-1}-y_{e,n-2}-2H}{1/n}(t-\frac{n-1}n)+y_{e,n-1}-H$, $h(n-1)=\min_{t\in[(n-1)/n,1]}v_{l,n-1}(t)$, $k_r\leftarrow I_{hi}-3$

end if

for $i=k_l,\ldots,k_r$ do

Define two linear functions:
\[
v_{l,i}(t)=\frac{y_{e,i}-y_{e,i-1}-2H}{1/n}(t-x_i)+y_{e,i}-H,\quad v_{r,i}=\frac{y_{e,i+2}-y_{e,i+1}+2H}{1/n}(t-x_{i+1})+y_{e,i+1}-H
\]
\[
h(i)=\min_{t\in[x_i,x_{i+1}]}\max\{v_{l,i}(t),v_{r,i}(t)\}
\]
end for

$f_{lo}\leftarrow\min\{h(i):I_{lo}-1\leq i\leq I_{hi}-2\}\wedge f_{hi}$
''',[22],'Algorithm 2 — Computing f_lo at the finest regression level',{'D34':'The algorithm consumes the previously defined window and upper endpoint.','D26':'The piecewise-linear bounds use the estimation-copy observations.','D18':'H is calibrated with a maximum-Gaussian quantile.'},kind='source_passage',context=r'Algorithm 2 Computing $f_{lo}$ when $\widehat{\mathtt j}+\widetilde K_{\alpha/4}>J$',symbols=[r'H\leftarrow',r'h(i)'],shape='Complete source algorithm for the discretization-dominated lower minimum endpoint, with both boundary constructions, interior maxima of two lines and final clipping against f_hi.')
add('D36',['confidence interval','minimum'],r'''
When $\widehat{\mathtt j}+\widetilde K_{\alpha/4}\leq J$, let
\[
f_{lo}=\widehat{\mathtt f}_1-(z_{\alpha/4}+1)\frac{\sqrt3\sigma}{\sqrt{2^{J-j_l}}}.
\]
When $\widehat{\mathtt j}+\widetilde K_{\alpha/4}>J$, we compute $f_{lo}$ by Algorithm 2,

The $(1-\alpha)$-level confidence interval for the minimum $M(f)$ is given by
\[
\mathrm{CI}_{m,\alpha}=[f_{lo},f_{hi}].\tag{4.11}
\]
''',[21,22],'Section 4.2.4 — regression minimum interval, equation (4.11)',{'D34':'Both branches use the common window, intermediate minimum and upper endpoint.','D35':'Algorithm 2 computes the lower endpoint when fine refinement exceeds the design horizon.'},symbols=[r'\mathrm{CI}_{m,\alpha}'],shape='Regression minimum interval with Gaussian correction before the finest level and geometric Algorithm 2 correction otherwise; no white-noise interval construction is imported.')
members['D36']['excerpt_selection']='Both original lower-endpoint branch instructions followed by the final interval; geometric explanation (4.10) and separately archived Algorithm 2 are omitted between them.'
(ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
(ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
print('Saved',len(interfaces),'source-backed interfaces.')
