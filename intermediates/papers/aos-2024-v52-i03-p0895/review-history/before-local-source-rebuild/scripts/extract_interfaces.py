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
add('D1','data points',r'''
using $n$ data points
\[
(X,Y,Z)\equiv\{(X_i,Y_i,Z_i)\}_{i=1,\ldots,n}\overset{\mathrm{i.i.d.}}\sim\mathcal L_n.\tag{2}
\]
''',[2],'Section 1.1 — sampled data (2)',kind='source_passage',phrases=['data points'],symbols=[r'\{(X_i,Y_i,Z_i)\}_{i=1,\ldots,n}'],shape='An iid sample of size n from a possibly n-dependent joint law. Population variables are bold; sample arrays and individual observations use regular math font. The experiment itself does not assume conditional independence.')
members['D1']['application_context']=[dict(text=r'''Given a predictor $\boldsymbol X\in\mathbb R$, response $\boldsymbol Y\in\mathbb R$, and high-dimensional covariate vector $\boldsymbol Z\in\mathbb R^p$ drawn from a joint distribution $(\boldsymbol X,\boldsymbol Y,\boldsymbol Z)\sim\mathcal L_n$ (potentially varying with $n$ to accommodate growing $p$),''',evidence=[dict(page=1,location='Section 1.1 — population variables'),dict(page=2,location='Section 1.1 — continuation of model setup')])]
add('D2','conditional independence',r'''
We denote by
\[
\mathscr L_n^0\equiv\{\mathcal L_n:\mathcal L_n(\boldsymbol X,\boldsymbol Y\mid\boldsymbol Z)=\mathcal L_n(\boldsymbol X\mid\boldsymbol Z)\times\mathcal L_n(\boldsymbol Y\mid\boldsymbol Z)\}\tag{3}
\]
the set of laws satisfying conditional independence, and $\mathscr R_n$ a class of distributions satisfying some regularity assumptions.
''',[5],'Section 1.4 — null-law class (3)',{'D1':'The factorization is a property of the sampled joint law.'},phrases=['conditional independence'],symbols=[r'\mathscr L_n^0',r'\mathcal L_n(\boldsymbol X,\boldsymbol Y\mid\boldsymbol Z)'],shape='The conditional-independence null class, distinct from an additional regularity class. No model-X known-law assumption is imposed on every member.')
add('D3','conditional means',r'''
Let
\[
\mu_{n,x}(\boldsymbol Z)\equiv\mathbb E_{\mathcal L_n}[\boldsymbol X\mid\boldsymbol Z]\quad\text{and}\quad\mu_{n,y}(\boldsymbol Z)\equiv\mathbb E_{\mathcal L_n}[\boldsymbol Y\mid\boldsymbol Z].\tag{5}
\]
''',[6],'Section 1.4 — population conditional means (5)',{'D1':'The expectations are under the true sampled law.'},context=r'''including the assumption that the conditional means $\mu_{n,x}$ and $\mu_{n,y}$ are fit accurately enough (SP1)''',phrases=[],symbols=[r'\mu_{n,x}(\boldsymbol Z)',r'\mu_{n,y}(\boldsymbol Z)'],shape='True conditional means as functions of the covariates, evaluated at observed Z_i in the statistics and error conditions. Their fitted counterparts are data-dependent nuisance functions; no particular regression algorithm is prescribed.')
members['D3']['naming_context'][0]['evidence']=[dict(page=16,location='Discussion of assumption (35) — source terminology')]
add('D4','learned laws',r'''
Learn $\widehat{\mathcal L}_n(\boldsymbol X\mid\boldsymbol Z)$ based on $(X,Z)$ and $\widehat\mu_{n,y}(\boldsymbol Z)$ based on $(Y,Z)$;

Sample $\widetilde X^{(m)}\mid X,Y,Z\sim\prod_{i=1}^n\widehat{\mathcal L}_n(X_i\mid Z_i)$
''',[6],'Algorithm 1 — fitting and resampling steps',{'D1':'The learned conditional law and fitted response mean are computed from the observed sample.'},kind='source_passage',context=r'Suppose the sequences of true and learned laws $\mathcal L_n$ and $\widehat{\mathcal L}_n$ satisfy the following two nondegeneracy properties:',phrases=['Learn'],symbols=[r'\widehat{\mathcal L}_n(\boldsymbol X\mid\boldsymbol Z)',r'\prod_{i=1}^n\widehat{\mathcal L}_n(X_i\mid Z_i)'],shape='In-sample learning of the predictor conditional kernel from (X,Z) and the response mean from (Y,Z), followed by conditionally independent predictor draws across observations. The learned object needed by resampling is a conditional kernel, not a fully specified joint law.')
members['D4']['naming_context'][0]['evidence']=[dict(page=8,location='Theorem 1 — true and learned laws')]
members['D4']['application_context']=[dict(text=r'''where $\widehat\mu_{n,x}(Z_i)\equiv\mathbb E_{\widehat{\mathcal L}_n}[X_i\mid Z_i]$.''',evidence=[dict(page=6,location='After (6) — learned-kernel mean')])]
add('D5','test statistic',r'''
This procedure is based on the test statistic
\[
T_n^{\widehat{\mathrm{dCRT}}}(X,Y,Z)\equiv\frac1{\sqrt n}\sum_{i=1}^n(X_i-\widehat\mu_{n,x}(Z_i))(Y_i-\widehat\mu_{n,y}(Z_i)),\tag{6}
\]
''',[6],'Section 1.4 — fitted residual-product statistic (6)',{'D1':'The residual-product functional is evaluated on the observed sample.'},phrases=['test statistic'],symbols=[r'T_n^{\widehat{\mathrm{dCRT}}}(X,Y,Z)',r'(X_i-\widehat\mu_{n,x}(Z_i))(Y_i-\widehat\mu_{n,y}(Z_i))'],shape='The raw residual-product functional takes two fitted mean functions as inputs. It is shared by GCM and the learned-law dCRT. Its evaluation needs the fitted means, not random draws or an entire conditional distribution; Algorithm 1 separately supplies the learned-kernel realization used for resampling.')
add('D6','resampled test statistics',r'''
\[
T_n^{\widehat{\mathrm{dCRT}}}(\widetilde X^{(m)},X,Y,Z)\equiv\frac1{\sqrt n}\sum_{i=1}^n(\widetilde X_i-\widehat\mu_{n,x}(Z_i))(Y_i-\widehat\mu_{n,y}(Z_i));\tag{7}
\]
The resampled test statistics $T_n^{\widehat{\mathrm{dCRT}}}(\widetilde X^{(m)},X,Y,Z)$ (7) have four arguments instead of three in order to emphasize that the conditional mean $\widehat\mu_{n,x}(\cdot)$ is not refit upon resampling.
''',[6],'Algorithm 1 — resampled statistic (7)',{'D4':'The replacement predictor array is drawn from the fitted conditional product law.','D5':'The residual-product statistic keeps the original fitted functions and replaces only its predictor observations.'},phrases=['resampled test statistics'],symbols=[r'T_n^{\widehat{\mathrm{dCRT}}}(\widetilde X^{(m)},X,Y,Z)'],shape='The predictor is resampled while the original fitted mean functions remain fixed. The source places m on the array argument but not on each component in the sum; this shorthand is retained.')
add('D7','GCM test',r'''
Another CI test is the GCM test (Shah and Peters, 2020), defined as
\[
\phi_n^{\mathrm{GCM}}(X,Y,Z)\equiv\mathbb 1(T_n^{\mathrm{GCM}}(X,Y,Z)>z_{1-\alpha}),\tag{8}
\]
where
\[
T_n^{\mathrm{GCM}}(X,Y,Z)\equiv\frac1{\widehat S_n^{\mathrm{GCM}}}\frac1{\sqrt n}\sum_{i=1}^n(X_i-\widehat\mu_{n,x}(Z_i))(Y_i-\widehat\mu_{n,y}(Z_i))\equiv\frac1{\widehat S_n^{\mathrm{GCM}}}T_n^{\widehat{\mathrm{dCRT}}}(X,Y,Z)\tag{9}
\]
and $(\widehat S_n^{\mathrm{GCM}})^2$ is the empirical variance of the product-of-residual summands:
\[
(\widehat S_n^{\mathrm{GCM}})^2\equiv\widehat{\operatorname{Var}}\{(X_i-\widehat\mu_{n,x}(Z_i))(Y_i-\widehat\mu_{n,y}(Z_i))\}.\tag{10}
\]
''',[7],'Section 1.4 — GCM decision and normalization (8)-(10)',{'D5':'GCM uses the same fitted residual-product numerator, with its own empirical variance.'},phrases=['GCM test'],symbols=[r'\phi_n^{\mathrm{GCM}}',r'\widehat S_n^{\mathrm{GCM}}'],shape='A one-sided standard-normal-threshold test using an empirical residual-product variance. The source leaves the empirical-variance divisor convention implicit. The functional does not require a predictor resampling kernel; zero denominators require a convention not supplied in these displays.')
add('D8','variance of the resampling distribution',r'''
Note that the variance of the resampling distribution of $T_n^{\widehat{\mathrm{dCRT}}}$ is
\[
(\widehat S_n^{\widehat{\mathrm{dCRT}}})^2\equiv\operatorname{Var}_{\widehat{\mathcal L}_n}[T_n^{\widehat{\mathrm{dCRT}}}(\widetilde X,X,Y,Z)\mid X,Y,Z]=\frac1n\sum_{i=1}^n\operatorname{Var}_{\widehat{\mathcal L}_n}[X_i\mid Z_i](Y_i-\widehat\mu_{n,y}(Z_i))^2.\tag{11}
\]
''',[8],'Section 2 — conditional resampling variance (11)',{'D6':'The variance is for the resampled statistic conditional on the original data.','D4':'Its explicit sum uses conditional variances from the learned predictor law.'},phrases=['variance of the resampling distribution'],symbols=[r'\widehat S_n^{\widehat{\mathrm{dCRT}}}',r'\operatorname{Var}_{\widehat{\mathcal L}_n}[X_i\mid Z_i]'],shape='Conditional resampling variance, not empirical residual-product variance. It uses the fitted predictor conditional variance and the observed response residuals.')
add('D9','conditional quantile',r'''
Here, the $\alpha$ conditional quantile $\mathbb Q_\alpha[W\mid\mathcal F]$ of a random variable $W$ given a $\sigma$-algebra $\mathcal F$ is defined via
\[
\mathbb Q_\alpha[W\mid\mathcal F]\equiv\inf\{t:\mathbb P[W\leq t\mid\mathcal F]\geq\alpha\}.\tag{12}
\]
''',[8],'Section 2 — conditional quantile (12)',phrases=['conditional quantile'],symbols=[r'\mathbb Q_\alpha[W\mid\mathcal F]'],shape='The lower conditional quantile defined by an infimum of a conditional CDF threshold. The symbol is blackboard Q and the CDF uses a non-strict inequality; conditional-law versions and measurability remain ambient.')
add('D10','infinite-resamples limit',r'''
It will be convenient to reformulate $\widehat{\mathrm{dCRT}}$ as
\[
\phi_n^{\widehat{\mathrm{dCRT}}}(X,Y,Z)\equiv\mathbb 1(T_n^{\widehat{\mathrm{dCRT}}}(X,Y,Z)>\mathbb Q_{1-\alpha}[T_n^{\widehat{\mathrm{dCRT}}}(\widetilde X,X,Y,Z)\mid X,Y,Z])
\]
\[
=\mathbb 1\left(\frac1{\widehat S_n^{\widehat{\mathrm{dCRT}}}}T_n^{\widehat{\mathrm{dCRT}}}(X,Y,Z)>\mathbb Q_{1-\alpha}\left[\frac1{\widehat S_n^{\widehat{\mathrm{dCRT}}}}T_n^{\widehat{\mathrm{dCRT}}}(\widetilde X,X,Y,Z)\mid X,Y,Z\right]\right)
\]
\[
\equiv\mathbb 1\left(\frac1{\widehat S_n^{\widehat{\mathrm{dCRT}}}}T_n^{\widehat{\mathrm{dCRT}}}(X,Y,Z)>C_n^{\widehat{\mathrm{dCRT}}}(X,Y,Z)\right).
\]
Note that this test is obtained from that in Algorithm 1 by sending $M\to\infty$; we focus our theoretical analysis here and throughout on this infinite-resamples limit of the $\widehat{\mathrm{dCRT}}$.
''',[8],'Section 2 — infinite-resampling decision',{'D5':'The observed decision statistic is the fitted residual-product sum.','D6':'The threshold is computed from the conditional resampled statistic.','D8':'The equivalent standardized expression divides by the conditional resampling standard deviation.','D9':'The decision threshold is a conditional quantile.'},phrases=['infinite-resamples limit'],symbols=[r'\phi_n^{\widehat{\mathrm{dCRT}}}',r'C_n^{\widehat{\mathrm{dCRT}}}(X,Y,Z)'],shape='The infinite-resampling theoretical dCRT with strict rejection above a conditional quantile. Finite Monte Carlo p-values in Algorithm 1 are a distinct implementation; the theorem does not provide an arbitrary fixed-M guarantee.')
add('D11','converges in distribution',r'''
For each $n$, let $W_n$ be a random variable and let $\mathcal F_n$ be a $\sigma$-algebra. Then, we say $W_n$ converges in distribution to a random variable $W$ conditionally on $\mathcal F_n$ if
\[
\mathbb P[W_n\leq t\mid\mathcal F_n]\xrightarrow{p}\mathbb P[W\leq t]\text{ for each }t\in\mathbb R\text{ at which }t\mapsto\mathbb P[W\leq t]\text{ is continuous}.\tag{13}
\]
We denote this relation via $W_n\mid\mathcal F_n\xrightarrow{d,p}W$.
''',[8],'Definition 1',phrases=['converges in distribution','Definition 1'],symbols=[r'W_n\mid\mathcal F_n\xrightarrow{d,p}W'],shape='Conditional CDF convergence in probability at continuity points of a fixed limiting distribution. It is not almost-sure conditional convergence or unconditional weak convergence alone.')
add('D12','nondegeneracy properties',r'''
\[
0<\operatorname{Var}_{\widehat{\mathcal L}_n}[X_i\mid Z_i],\ (Y_i-\widehat\mu_{n,y}(Z_i))^2,\ (Y_i-\mu_{n,y}(Z_i))^2<\infty\text{ almost surely}.\tag{NDG2}
\]
''',[8],'Theorem 1 — condition (NDG2)',{'D4':'The first quantity is a conditional variance of the learned predictor law.','D3':'The last residual uses the true response conditional mean.'},kind='theorem_excerpt',context=r'Suppose the sequences of true and learned laws $\mathcal L_n$ and $\widehat{\mathcal L}_n$ satisfy the following two nondegeneracy properties:',phrases=['(NDG2)'],symbols=[r'(Y_i-\mu_{n,y}(Z_i))^2'],shape='The source’s comma-separated chain requires the learned variance and both squared response residuals to be positive and finite almost surely. NDG1 remains separately bound in Theorem 1; it is not added to Theorem 2 merely because both conditions occur together here.')
add('D13','in-sample mean-squared error quantities',r'''
It controls Type-I error if the following in-sample mean-squared error quantities are small (Shah and Peters, 2020):
\[
E_{n,x}\equiv\left(\frac1n\sum_{i=1}^n(\widehat\mu_{n,x}(Z_i)-\mu_{n,x}(Z_i))^2\right)^{1/2};\quad E'_{n,x}\equiv\left(\frac1n\sum_{i=1}^n(\widehat\mu_{n,x}(Z_i)-\mu_{n,x}(Z_i))^2\operatorname{Var}_{\mathcal L_n}[Y_i\mid Z_i]\right)^{1/2};
\]
\[
E_{n,y}\equiv\left(\frac1n\sum_{i=1}^n(\widehat\mu_{n,y}(Z_i)-\mu_{n,y}(Z_i))^2\right)^{1/2};\quad E'_{n,y}\equiv\left(\frac1n\sum_{i=1}^n(\widehat\mu_{n,y}(Z_i)-\mu_{n,y}(Z_i))^2\operatorname{Var}_{\mathcal L_n}[X_i\mid Z_i]\right)^{1/2}.
\]
''',[7],'Section 1.4 — four regression error quantities',{'D3':'The errors compare fitted nuisance functions with the true conditional means.'},phrases=['in-sample mean-squared error quantities'],symbols=[r'E_{n,x}',r"E'_{n,x}",r'E_{n,y}',r"E'_{n,y}"],shape='Empirical root-mean-square errors at the same observed covariates, including the two opposite-response variance weights. These are not out-of-sample risks. The fitted functions are inputs shared by GCM and dCRT, with no particular learned distribution required for these error functionals.')
add('D14','estimation errors',r'''
\[
E_{n,x}E_{n,y}=o_{\mathcal L_n}(n^{-1/2}),\quad E'_{n,x}=o_{\mathcal L_n}(1),\quad E'_{n,y}=o_{\mathcal L_n}(1),\tag{SP1}
\]
''',[7],'(SP1)',{'D13':'SP1 constrains the product of ordinary errors and each variance-weighted error.'},kind='assumption',context=r'''The GCM test is therefore doubly robust in the sense that it controls Type-I error if the product of the estimation errors for $\mathbb E[\boldsymbol X\mid\boldsymbol Z]$ and $\mathbb E[\boldsymbol Y\mid\boldsymbol Z]$ ($E_{n,x}E_{n,y}$) converges to zero at the $o_{\mathcal L_n}(n^{-1/2})$ rate.''',phrases=['(SP1)'],symbols=[r'E_{n,x}E_{n,y}=o_{\mathcal L_n}(n^{-1/2})'],shape='A product-rate and two weighted-error conditions under the true law. This is rate double robustness, not validity whenever one model happens to be correctly specified without quantitative control of the other fit.')
add('D15','moment assumptions',r'''
and, for some constants $c_1,c_2,\delta>0$,
\[
\inf_n\mathbb E_{\mathcal L_n}[(\boldsymbol X-\mu_{n,x}(\boldsymbol Z))^2(\boldsymbol Y-\mu_{n,y}(\boldsymbol Z))^2]>c_1
\]
\[
\sup_n\mathbb E_{\mathcal L_n}[|(\boldsymbol X-\mu_{n,x}(\boldsymbol Z))(\boldsymbol Y-\mu_{n,y}(\boldsymbol Z))|^{2+\delta}]<c_2.\tag{SP2}
\]
''',[7],'(SP2)',{'D3':'The residual-product moments use both true conditional means.'},kind='assumption',context='and fairly mild moment assumptions (SP2).',phrases=['(SP2)'],symbols=[r'\inf_n\mathbb E_{\mathcal L_n}',r'\sup_n\mathbb E_{\mathcal L_n}'],shape='A uniform-in-n positive lower bound on the residual-product second moment and upper bound on a 2+delta moment. The source’s constants and quantifier scope are retained; they are not automatically uniform over every regularity class.')
members['D15']['naming_context'][0]['evidence']=[dict(page=16,location='Discussion of assumption (35) — moment terminology')]
add('D16','variance consistency property',r'''
\[
\frac1n\sum_{i=1}^n(\operatorname{Var}_{\widehat{\mathcal L}_n}[X_i\mid Z_i]-\operatorname{Var}_{\mathcal L_n}[X_i\mid Z_i])\operatorname{Var}_{\mathcal L_n}[Y_i\mid Z_i]\xrightarrow{p}0.\tag{23}
\]
''',[12],'Section 4.1 — variance consistency (23)',{'D4':'The first variance is from the learned predictor kernel.','D1':'The comparison and response-weight variances are under the true sampled law.'},kind='condition',context='the variance consistency property (23)',phrases=[],symbols=[r'\operatorname{Var}_{\widehat{\mathcal L}_n}[X_i\mid Z_i]-\operatorname{Var}_{\mathcal L_n}[X_i\mid Z_i]'],shape='A signed empirical average of predictor variance-estimation errors weighted by true response variance. It is not pointwise variance consistency or convergence of an average absolute error.')
add('D18','estimation errors',r'''
In preparation to state our equivalence result, we augment the assumption (SP1) as follows:
\[
E_{n,x}E_{n,y}=o_{\mathcal L_n}(n^{-1/2}),\quad E'_{n,x}=o_{\mathcal L_n}(1),\quad E'_{n,y}=o_{\mathcal L_n}(1),\quad\widehat E'_{n,y}=o_{\mathcal L_n}(1),\tag{SP1'}
\]
''',[12],"(SP1')",{'D14':'SP1-prime retains all three original SP1 rate conditions.','D3':'The added error uses the true response mean.','D4':'Its additional weight uses the learned predictor conditional variance.'},kind='assumption',context=r'The GCM test is therefore doubly robust in the sense that it controls Type-I error if the product of the estimation errors for $\mathbb E[\boldsymbol X\mid\boldsymbol Z]$ and $\mathbb E[\boldsymbol Y\mid\boldsymbol Z]$ ($E_{n,x}E_{n,y}$) converges to zero at the $o_{\mathcal L_n}(n^{-1/2})$ rate.',phrases=['assumption',"(SP1')"],symbols=[r"\widehat E'_{n,y}=o_{\mathcal L_n}(1)"],shape='The strengthened regression-rate condition used by Theorem 2, adding the learned-variance-weighted response error. Theorem 3 uses SP1, not this augmentation.')
members['D18']['naming_context'][0]['evidence']=[dict(page=7,location='Section 1.4 — original estimation-error terminology')]
members['D18']['application_context']=[dict(text=r'''where
\[
\widehat E'_{n,y}\equiv\left(\frac1n\sum_{i=1}^n(\widehat\mu_{n,y}(Z_i)-\mu_{n,y}(Z_i))^2\operatorname{Var}_{\widehat{\mathcal L}_n}[X_i\mid Z_i]\right)^{1/2}.\tag{24}
\]''',evidence=[dict(page=12,location='Section 4.1 — additional weighted error (24)')])]
add('D19','asymptotic Type-I error control',r'''
For any regularity class $\mathscr R_n$, we consider testing the null hypothesis $\mathcal L_n\in\mathscr L_n^0\cap\mathscr R_n$. A sequence of tests $\phi_n:(X,Y,Z)\mapsto[0,1]$ of this null hypothesis has asymptotic Type-I error control if
\[
\limsup_{n\to\infty}\sup_{\mathcal L_n\in\mathscr L_n^0\cap\mathscr R_n}\mathbb E_{\mathcal L_n}[\phi_n(X,Y,Z)]\leq\alpha.\tag{4}
\]
''',[5],'Section 1.4 — uniform asymptotic level (4)',{'D2':'The level bound ranges over the intersection of the conditional-independence null and a regularity class.'},phrases=['asymptotic Type-I error control'],symbols=[r'\sup_{\mathcal L_n\in\mathscr L_n^0\cap\mathscr R_n}'],shape='A uniform-over-laws level bound before the limsup in n. Randomized tests take values in [0,1]. Pointwise validity at each fixed law is not silently substituted for this definition.')
add('D20','GPLM alternatives',r'''
We will seek power against semiparametric GPLM alternatives of the form
\[
\mathcal L_\theta(\boldsymbol X,\boldsymbol Y,\boldsymbol Z)\equiv\mathcal L_{\beta,\eta}(\boldsymbol X,\boldsymbol Y,\boldsymbol Z)\equiv\mathcal L_{x,z}(\boldsymbol X,\boldsymbol Z)\times f_\eta(\boldsymbol Y\mid\boldsymbol X,\boldsymbol Z),\qquad\eta=\boldsymbol X\beta+g(\boldsymbol Z).\tag{29}
\]
Here, $\mathcal L_{x,z}$ is a fixed law, $f_\eta$ is a one-parameter exponential family with natural parameter $\eta\in\mathbb R$ and log-partition function $\psi$, $\beta\in\mathbb R$ and
\[
g\in\mathcal H_g\subseteq L^2(\mathcal L_{x,z}(\boldsymbol Z)),\tag{30}
\]
where $\mathcal H_g$ is a linear subspace of the $L^2$ space of functions on $\mathbb R^p$ with the measure $\mathcal L_{x,z}(\boldsymbol Z)$.
''',[15],'Section 5.1 — generalized partially linear alternatives (29)-(30)',kind='source_passage',phrases=['GPLM alternatives'],symbols=[r'\eta=\boldsymbol X\beta+g(\boldsymbol Z)',r'\mathcal H_g\subseteq L^2'],shape='A fixed covariate/predictor law and a canonical one-parameter exponential-family response with additive linear predictor. The nuisance space is linear, not explicitly closed. The source parameter notation L_{beta,eta} is retained even though paths are parameterized by (beta,g). The model need only describe alternatives, not all null laws.')
members['D20']['application_context']=[dict(text=r'''To facilitate the link with semiparametric theory, in this section of the paper we operate in a fixed-dimensional setting. Accordingly, we drop the subscript $n$ from $\mathscr L_n^0$ and $\mathscr R_n$. For each value of $n$, we have $(\boldsymbol X,\boldsymbol Y,\boldsymbol Z)\in\mathbb R^{1+1+p}$ for fixed $p$.''',evidence=[dict(page=15,location='Section 5.1 — fixed-dimensional convention')])]
add('D21','local alternatives',r'''
We focus on power against local alternatives $\mathcal L_{\theta_n(h)}$ near $\theta_0\equiv(0,g_0)$, defined by
\[
\theta_n(h)\equiv\theta_n(h_\beta,h_g)\equiv(h_\beta/\sqrt n,g_0+h_g/\sqrt n),\quad\text{for}\quad h\equiv(h_\beta,h_g)\in(0,\infty)\times\mathcal H_g.\tag{31}
\]
We leave the dependence of $\theta_n(h)$ on $g_0$ implicit.
''',[15],'Section 5.1 — local paths (31)',{'D20':'The paths vary the linear coefficient and nuisance function within the GPLM alternative family.'},phrases=['local alternatives'],symbols=[r'\theta_n(h)',r'g_0+h_g/\sqrt n'],shape='Root-n local paths about (0,g_0) with positive coefficient direction and arbitrary nuisance direction. The theorem also evaluates the same formula at coefficient direction zero for its null-path inclusion condition. The scalar power scale defined in (34) is retained as application context because the author does not supply it a separate natural-language name.')
members['D21']['application_context']=[dict(text=r'''Finally, define
\[
s^2(\theta_0)\equiv\mathbb E_{\mathcal L_{\theta_0}}[\operatorname{Var}_{\mathcal L_{\theta_0}}[\boldsymbol X\mid\boldsymbol Z]\operatorname{Var}_{\mathcal L_{\theta_0}}[\boldsymbol Y\mid\boldsymbol Z]].\tag{34}
\]''',evidence=[dict(page=15,location='Section 5.1 — scalar in the power formula')])]
add('D22','locally asymptotically uniformly most powerful',r'''
For $h\in(0,\infty)\times\mathcal H_g$, we say a test $\phi_n^*$ is the locally asymptotically most powerful level $\alpha$ test of
\[
H_0:\mathcal L\in\mathscr R\subseteq\mathscr L^0\quad\text{versus}\quad H_{1n}:\mathcal L=\mathcal L_{\theta_n(h)}\tag{32}
\]
if $\phi_n^*$ has asymptotic Type-I error control over $\mathscr R$ at level $\alpha$ and for any other test $\phi_n$ satisfying the same property we have
\[
\limsup_{n\to\infty}\mathbb E_{\mathcal L_{\theta_n(h)}}[\phi_n(X,Y,Z)]\leq\liminf_{n\to\infty}\mathbb E_{\mathcal L_{\theta_n(h)}}[\phi_n^*(X,Y,Z)].\tag{33}
\]
If this is true for every $h\in(0,\infty)\times\mathcal H_g$, such a test is locally asymptotically uniformly most powerful at $g_0$, or LAUMP($g_0$). A test is LAUMP($\mathcal S$) against $\mathcal L_{\theta_n(h)}$ for $h\in(0,\infty)\times\mathcal H_g$ if it is LAUMP($g_0$) for each $g_0\in\mathcal S\subseteq\mathcal H_g$.
''',[15],'Definition 2',{'D19':'The comparison class consists of tests satisfying the paper’s asymptotic level definition over the null class.','D21':'Power is compared along the root-n GPLM local alternatives, at each base nuisance function.'},phrases=['locally asymptotically uniformly most powerful','Definition 2'],symbols=[r'\phi_n^*',r'\mathcal S\subseteq\mathcal H_g'],shape='Pointwise-in-direction asymptotic power domination for all level-alpha competitors, then quantification over all directions and base nuisance functions. The word uniformly does not replace the displayed limits by a supremum over directions, and null level control remains the separate uniform-over-laws requirement.')
(ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
(ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
print(f'Saved {len(interfaces)} source interfaces.')
