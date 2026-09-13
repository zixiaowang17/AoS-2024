"""Preserve original main-text source entries for the four-Theorem census."""
import json
from save_inventory import ROOT,PID
interfaces=[];members={}
def add(n,term,s,pages,deps,symbols,boundary,heading,kind='definition',context=None,context_page=None,phrases=None):
    lid=f'D{n}'
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=phrases or [])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context,(lid,term)
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original naming context')])];kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='definition',type_shape=boundary,semantic_boundary=boundary,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))
add(1,'basic setup',r'''Recall the basic setup outlined earlier: we have available i.i.d. copies $(X_1,Y_1,T_1),\ldots,(X_n,Y_n,T_n)$ of the triple $(X,Y,T)\in\mathbb R^p\times\mathbb R\times\{0,1\}$ representing pretreatment covariates, the outcome and a binary treatment indicator. The first component of $X$ will typically be $1$ representing an intercept term. We collect these data into $\mathbf X\in\mathbb R^{n\times p}$, $\mathbf Y\in\mathbb R^n$ and $\mathbf T\in\{0,1\}^n$.''',[2,3],[],[r'(X_1,Y_1,T_1)',r'\mathbf X\in\mathbb R^{n\times p}'],'Iid observational triples and their matrix/vector organization. The word typically about the intercept is not strengthened here; Assumption 4 separately requires it.','Section 1.1 — Basic setup',kind='source_passage')
add(2,'average treatment effect',r'''We work in the potential outcomes framework [Neyman, 1923, Rubin, 1974] and define the average treatment effect as $\tau:=\mathbb E\{Y(1)-Y(0)\}$ where $Y(0)$ and $Y(1)$ are the potential outcomes such that $Y=Y(T)$.''',[1],[1],[r'\tau:=\mathbb E\{Y(1)-Y(0)\}',r'Y=Y(T)'],'Population expectation target and consistency. The definition does not itself assert identification by observed data.','Section 1 — Average treatment effect')
add(3,'unconfoundedness',r'''Conditioning on the observed covariate vector $X$, $Y(1)$ and $Y(0)$ are independent from the treatment assignment $T$, that is $\{Y(1),Y(0)\}\perp\!\!\!\perp T\mid X$.''',[3],[1],[], 'Conditional independence of the joint potential-outcome pair from treatment; it is not independence of the two outcomes from each other.','Assumption 1',kind='assumption',context=r'''Throughout the paper we assume unconfoundedness as required for identification of the average treatment effect $\tau$.''',phrases=['Assumption 1'])
add(4,'outcome regression functions',r'''We write
\[
r_t(x)=\mathbb E\{Y(t)\mid X=x\},\qquad t=0,1
\]
for the outcome regression functions.''',[3],[1],[r'r_t(x)'],'Conditional potential-outcome means; no linearity or sparsity is assumed. The following population contrast identity is preserved separately as auxiliary context.','Section 1.1 — Outcome regression functions')
add(5,'standard logistic function',r'''Here $\psi(u):=\{1+\exp(-u)\}^{-1}$ denotes the standard logistic function.''',[3],[],[r'\psi(u):=\{1+\exp(-u)\}^{-1}'],'Scalar logistic link; the propensity restriction is a separate assumption.','Section 1.1 — Logistic function')
add(6,'propensity score',r'''We have
\[
\mathbb P(T=1\mid X=x)=\pi(x)=\psi(x^\top\gamma)
\]
(1)
and for some $c_\pi>0$, $c_\pi<\pi(X)<1-c_\pi$ almost surely.''',[3],[1,5],[r'\pi(x)=\psi(x^\top\gamma)',r'c_\pi<\pi(X)<1-c_\pi'],'Logistic conditional treatment probability with strict almost-sure overlap. This does not impose a pointwise bound at every possible x.','Assumption 2',kind='assumption',context=r'''Throughout the manuscript (with the exception of Section 5.1), we will additionally assume a logistic regression model for the propensity score and that we have overlap, that is the propensity scores are bounded away from 0 and 1.''')
add(7,'sparsity',r'''We have in mind the high-dimensional setting where $p$ is large and potentially $p\gg n$, but writing $s:=|\{j:\gamma_j\ne0\}|$, we have $s\ll p$. However, we aim to avoid such sparsity conditions or making any additional structural or smoothness assumptions on $r_0$ and $r_1$.''',[3],[6],[r's:=|\{j:\gamma_j\ne0\}|'],'Count of nonzero coefficients of the propensity model. The motivating much-less-than statements are not converted into quantitative theorem assumptions.','Section 1.1 — Sparsity')
add(8,'oracular counterpart',r'''Thus AIPW chooses $\boldsymbol\mu$ through estimating the function $\mu_{\mathrm{ORA}}:\mathbb R^p\to\mathbb R$ given by
\[
\mu_{\mathrm{ORA}}(x):=\{1-\pi(x)\}r_1(x)+\pi(x)r_0(x).
\]
(4)''',[4],[4,6],[r'\mu_{\mathrm{ORA}}(x)',r'\boldsymbol\mu_{\mathrm{ORA}}'],'Original oracle correction function. The author calls its evaluated vector the oracular counterpart; the exact notation identifies the function and vector in details. No synthesized definition or AIPW theorem is added.','Section 1.1 — Oracle correction (4)',context=r'''One complication in constructing a confidence interval is that without making any further assumptions about how close $\widehat{\boldsymbol\mu}$ is to its oracular counterpart $\boldsymbol\mu_{\mathrm{ORA}}$, we cannot argue that the $\widehat\tau_{\mathrm{DIPW},j}$ are independent, and thus $\widehat\tau_{\mathrm{AVE}}$ can have a complicated non-Gaussian distribution.''',context_page=13)
add(9,'independent auxiliary datasets',r'''In this section, we describe a simple version of our debiased IPW estimator which relies on independent auxiliary datasets $\mathcal D_A:=(\mathbf X_A,\mathbf Y_A,\mathbf T_A)\in\mathbb R^{n_A\times p}\times\mathbb R^{n_A}\times\{0,1\}^{n_A}$ and $\mathcal D_B:=(\mathbf X_B,\mathbf Y_B,\mathbf T_B)\in\mathbb R^{n_B\times p}\times\mathbb R^{n_B}\times\{0,1\}^{n_B}$ that are independent of the main dataset $(\mathbf X,\mathbf Y,\mathbf T)$ and consist of i.i.d. copies of the triple $(X,Y,T)$.''',[5],[1],[r'\mathcal D_A',r'\mathcal D_B'],'Independent auxiliary datasets, also independent of the main sample. Section 3.1 additionally fixes n_A=n, but not n_B=n.','Section 2 — Auxiliary datasets',kind='source_passage')
add(10,'estimate of the propensity score',r'''Using dataset $\mathcal D_B$ we first construct an estimate of the propensity score of the form $\hat\pi(x)=\psi(x^\top\hat\gamma)$, where $\hat\gamma$ is an estimate of $\gamma$. Our default option, which we use in all our numerical experiments, is $\ell_1$-penalised logistic regression (see (27)).''',[5],[5,6,9],[r'\hat\pi(x)=\psi(x^\top\hat\gamma)',r'\hat\gamma'],'Estimated logistic propensity trained on auxiliary B. Penalized logistic regression is an optional default, not a compulsory theorem construction.','Section 2 — Estimated propensity score')
add(12,'initial estimate',r'''Instead, we propose to construct an estimate $\tilde\mu$ of the function $\mu_{\mathrm{ORA}}$ using dataset $\mathcal D_B$;''',[7],[8,9],[r'\tilde\mu',r'\tilde\mu(\mathbf X)'],'Initial fitted function from auxiliary B. The following optional fitting recipes are retained separately; neither requires outcome regressions to be accurately estimable. The optimization itself is preserved in D13.','Section 2 — Initial correction estimate',kind='source_passage',context=r'''Importantly, this unbiasedness property makes essentially no requirements on the quality of the initial estimate $\tilde\mu$.''',context_page=4)
add(13,'convex quadratic program',r'''We thus arrive at the following convex quadratic program for determining $\boldsymbol\mu=\widehat{\boldsymbol\mu}$
\[
\widehat{\boldsymbol\mu}=\operatorname{argmin}_{\boldsymbol\mu\in\mathbb R^n}\frac1n\|\tilde\mu(\mathbf X)-\boldsymbol\mu\|_2^2
\]
\[
\text{subject to}\quad\left\|\frac1{n_A}\mathbf X_A^\top\{\widetilde{\mathbf Y}_A-\tilde\mu(\mathbf X_A)\}-\frac1n\mathbf X^\top\{\boldsymbol\mu-\tilde\mu(\mathbf X)\}\right\|_\infty\leq\eta.
\]
(14)
When no feasible $\widehat{\boldsymbol\mu}$ exists, we simply set $\widehat{\boldsymbol\mu}=\mathbf0$; as explained earlier however, $\widetilde{\mathbf Y}$ is a feasible solution with high probability.''',[7],[9,10,12],[r'\widehat{\boldsymbol\mu}',r'\widehat{\boldsymbol\mu}=\mathbf0'],'Full constrained least-squares correction with zero fallback on infeasibility. The constraint uses auxiliary A while the initial fit uses auxiliary B.','Section 2 — Convex quadratic program (14)')
add(14,'debiased inverse probability weighting estimator',r'''With this we can define the basic version of our debiased inverse probability weighting estimator $\widehat\tau_{\mathrm{DIPW}}$:
\[
\widehat\tau_{\mathrm{DIPW}}:=\frac1n\sum_{i=1}^n\left(\frac{T_i(Y_i-\hat\mu_i)}{\hat\pi_i}-\frac{(1-T_i)(Y_i-\hat\mu_i)}{1-\hat\pi_i}\right).
\]
(15)''',[7],[1,10,13],[r'\widehat\tau_{\mathrm{DIPW}}'],'Basic DIPW estimator using the correction (14). It is distinct from the practical multi-split estimator described later.','Section 2 — DIPW estimator (15)')
add(15,'sub-Gaussian random variables',r'''The potential outcomes $Y(0),Y(1)$ are sub-Gaussian random variables, so there exists $\sigma_Y>0$ such that $\mathbb E\big(\exp[\alpha\{Y(t)-\mathbb EY(t)\}]\big)\leq\exp(\alpha^2\sigma_Y^2/2)$ for all $\alpha\in\mathbb R$ and $t=0,1$. Furthermore we assume there exists a constant $m_Y>0$ such that $\max_{t=0,1}|\mathbb EY(t)|\leq m_Y$.''',[8],[1],[r'\sigma_Y',r'\max_{t=0,1}|\mathbb EY(t)|\leq m_Y'],'Marginal sub-Gaussian potential outcomes with a common proxy and bounded marginal means; not conditional sub-Gaussianity given covariates.','Assumption 3',kind='assumption',phrases=['Assumption 3'])
add(16,'high-dimensional confounders',r'''The first component of $X$ is $1$, representing an intercept term. Denoting by $Z\in\mathbb R^{p-1}$ the remaining components of $X$, we assume $Z$ is sub-Gaussian with $\mathbb EZ=0$, so there exists $\sigma_Z>0$ such that for each $u\in\mathbb R^{p-1}$ with $\|u\|_2=1$, and for all $\alpha\in\mathbb R$, $\mathbb E\{\exp(\alpha u^\top Z)\}\leq\exp(\alpha^2\sigma_Z^2/2)$.''',[8],[1],[r'\mathbb EZ=0',r'\mathbb E\{\exp(\alpha u^\top Z)\}'],'Intercept plus centered jointly sub-Gaussian remaining covariates, uniformly over all unit directions. No minimum eigenvalue condition is added.','Assumption 4',kind='assumption',context=r'''For all of the results to follow, in addition to the unconfoundedness, overlap and propensity score model assumptions (Assumptions 1 and 2), it will be convenient to make the following assumptions about the distribution of the high-dimensional confounders $X$ and the potential outcomes $Y(0),Y(1)$.''',phrases=['Assumption 4'])
add(17,'Assumption 5',r'''There exists a sequence $(a_n)_{n=1}^\infty$ with $\lim_{n\to\infty}a_n=0$ such that $\log(p)/n=a_n$. Furthermore $p\geq2$ and $s\geq1$.''',[9],[7],[r'\log(p)/n=a_n',r'p\geq2',r's\geq1'],'Sequence-level dimension growth and lower bounds, including exclusion of zero sparsity. Retain the source label because no special mathematical name is supplied.','Assumption 5',kind='assumption',context='Assumption 5.',phrases=['Assumption 5'])
add(18,'conditional average treatment effect',r'''\[
\bar\tau:=\frac1n\sum_{i=1}^n\mathbb E\{Y_i(1)-Y_i(0)\mid X_i\}.
\]
(16)''',[9],[1],[r'\bar\tau'],'Average of conditional potential-outcome contrasts at observed covariates. It is a random target before conditioning on the covariate matrix, distinct from population tau.','Section 3.1 — Conditional target (16)',context=r'''In this section we consider constructing confidence intervals around the conditional average treatment effect $\bar\tau$ (16) evaluated across the entire dataset.''',context_page=13)
add(19,'errors',r'''Let us write
\[
\varepsilon(t):=Y(t)-r_t(X)\quad\text{and}\quad\varepsilon_i(t)=Y_i(t)-r_t(X_i),\qquad t=0,1.
\]''',[9],[4],[r'\varepsilon(t)',r'\varepsilon_i(t)'],'Potential-outcome residuals relative to their conditional regression means; no independence from X or homoscedasticity is imposed.','Section 3.1 — Residual notation',context=r'''We also make the mild assumption that the variances of the errors $\varepsilon(0),\varepsilon(1)$ are bounded away from zero.''',context_page=13)
add(21,'event',r'''Define the event $\Omega(c_\gamma,c_{\tilde\mu},c_{\hat\pi})$ depending on constants $c_\gamma,c_{\tilde\mu}>0$ and $c_{\hat\pi}\in(0,1/2]$ to be such that

(i) $\|\hat\gamma-\gamma\|_1\leq c_\gamma s\sqrt{\log(p)/n}$ and $\|\hat\gamma-\gamma\|_2\leq c_\gamma\sqrt{s\log(p)/n}$;

(ii) $c_{\hat\pi}\leq\hat\pi_i\leq1-c_{\hat\pi}$ and $c_{\hat\pi}\leq\hat\pi_{Ai}\leq1-c_{\hat\pi}$ for all $i=1,\ldots,n$;

(iii) $|\mathbb E\{\tilde\mu(X)\mid\mathcal D_B\}|<c_{\tilde\mu}$ and for all $\alpha\in\mathbb R$, $\mathbb E\big(\exp[\alpha\{\tilde\mu(X)-\mathbb E(\tilde\mu(X)\mid\mathcal D_B)\}]\mid\mathcal D_B\big)\leq\exp(\alpha^2c_{\tilde\mu}^2/2)$.

Here $\hat\pi_{Ai}$ is the equivalent of $\hat\pi_i$ but related to the dataset $\mathcal D_A$.''',[9],[7,9,10,12],[r'\Omega(c_\gamma,c_{\tilde\mu},c_{\hat\pi})',r'\Omega^c(c_\gamma,c_{\tilde\mu},c_{\hat\pi})'],'All three event conditions, including estimated-score bounds on two datasets and conditional moments of the initial fit. Complement probability remains in the results; sufficient conditions for it to be small are not additional theorem assumptions.','Section 3.1 — Event conditions')
add(22,'variance term',r'''\[
\sigma_\mu^2:=\frac1n\sum_{i=1}^n\frac{(\hat\mu_i-\mu_{\mathrm{ORA},i})^2}{\pi_i(1-\pi_i)}
\]''',[10],[6,8,13],[r'\sigma_\mu^2',r'\sigma_\mu'],'Additional squared correction error weighted by true propensity variance. Its zero case is not excluded in Theorems 2-3.','Section 3.1 — Additional variance quantity',context=r'''Importantly, the variance term $\sigma_\mu^2$ that we incur in addition to the $\bar\sigma^2$ attainable by AIPW when all nuisance functions are known, is well-controlled.''',context_page=11)
add(23,'semiparametric efficient variance bound',r'''\[
\sigma^2:=\operatorname{Var}\left(r_1(X)-r_0(X)-\tau+\frac{T\varepsilon(1)}{\pi(X)}-\frac{(1-T)\varepsilon(0)}{1-\pi(X)}\right),
\]
(19)''',[11],[2,4,6,19],[r'\sigma^2'],'Variance of the centered population influence expression, not the conditional sample-average residual variance bar-sigma squared.','Section 3.1 — Population variance (19)',context=r'''Note that $\sigma^2$ is the semiparametric efficient variance bound based on a dataset of size $n$ achieved for example by AIPW when $r_0,r_1$ and $\pi$ are all estimable at sufficiently fast rates.''',context_page=12)
add(24,'cross-fit estimator',r'''In this section we consider a single dataset of size $n$, which we assume for simplicity to be a multiple of $3$. We split the observation indices into three parts, $I_1:=\{1,\ldots,n/3\}$, $I_2:=\{n/3+1,\ldots,2n/3\}$ and $I_3:=\{2n/3+1,\ldots,n\}$ to give corresponding datasets $\mathcal D_j:=(X_i,Y_i,T_i)_{i\in I_j}$, $j=1,2,3$. Consider forming three corresponding estimates $\widehat\tau_{\mathrm{DIPW},1},\widehat\tau_{\mathrm{DIPW},2},\widehat\tau_{\mathrm{DIPW},3}$ where $\widehat\tau_{\mathrm{DIPW},j}$ is constructed as described in Section 2 but using $\mathcal D_j$ as the main dataset, and taking auxiliary datasets $\mathcal D_A$ and $\mathcal D_B$ as $\mathcal D_{j+1}$ and $\mathcal D_{j+2}$ respectively, with the additions $j+1$ and $j+2$ understood to be modulo $3$. Here we study properties of the aggregate estimator
\[
\widehat\tau_{\mathrm{AVE}}:=\frac13(\widehat\tau_{\mathrm{DIPW},1}+\widehat\tau_{\mathrm{DIPW},2}+\widehat\tau_{\mathrm{DIPW},3});
\]
(22)
because of the way auxiliary data and the main data are interchanged in $\widehat\tau_{\mathrm{DIPW},j}$ as $j$ varies, the above is sometimes known as a cross-fit estimator.''',[12],[9,14],[r'\widehat\tau_{\mathrm{AVE}}',r'I_1:=\{1,\ldots,n/3\}'],'Three-fold cyclic construction on a single dataset divisible by three. The three estimates share data through different roles and are not assumed independent.','Section 3.2 — Cross-fit estimator (22)')
add(25,'debiasing quantities',r'''For $j=1,2,3$, let $\widehat{\boldsymbol\mu}_j\in\mathbb R^{n/3}$ be the corresponding debiasing quantities constructed as in (14) using estimates $\tilde\mu_1,\tilde\mu_2,\tilde\mu_3$ of $\mu_{\mathrm{ORA}}$, and let $\Omega_j(c_\gamma,c_{\tilde\mu},c_{\hat\pi})$ be defined as in the previous section, but in each case taking the main dataset as $\mathcal D_j$ and auxiliary datasets as above. Let $\widehat{\boldsymbol\mu}$ be the concatenation $\widehat{\boldsymbol\mu}:=(\widehat{\boldsymbol\mu}_1,\widehat{\boldsymbol\mu}_2,\widehat{\boldsymbol\mu}_3)\in\mathbb R^n$. We also retain the definition of $\boldsymbol\mu_{\mathrm{ORA}}\in\mathbb R^n$ from Section 2.''',[12],[8,13,21,24],[r'\widehat{\boldsymbol\mu}_j',r'\Omega_j(c_\gamma,c_{\tilde\mu},c_{\hat\pi})',r'\widehat{\boldsymbol\mu}:='],'Original paragraph defining the fold corrections, fold events and concatenation. These are distinct objects within one source passage; shared indexing does not make them equivalent.','Section 3.2 — Fold-specific quantities',kind='source_passage')
add(26,'confidence interval',r'''\[
\hat\sigma_j^2:=\frac3n\sum_{i\in I_j}\left(\frac{T_i(Y_i-\hat\mu_i)}{\hat\pi_i}-\frac{(1-T_i)(Y_i-\hat\mu_i)}{1-\hat\pi_i}-\widehat\tau_{\mathrm{DIPW},j}\right)^2.
\]
(23)
With this, a valid confidence interval for $\bar\tau$ can be derived via applying a union bound. Specifically, we define $\tilde\sigma:=(\hat\sigma_1+\hat\sigma_2+\hat\sigma_3)/\sqrt3$, and construct a confidence interval via
\[
\widetilde C_\alpha:=\left[\widehat\tau_{\mathrm{AVE}}-\frac{\tilde\sigma}{\sqrt n}z_\alpha,\widehat\tau_{\mathrm{AVE}}+\frac{\tilde\sigma}{\sqrt n}z_\alpha\right].
\]
(24)''',[13],[1,10,18,24,25],[r'\widetilde C_\alpha',r'\widetilde C_{\alpha/3}',r'\hat\sigma_j^2'],'Source confidence-interval construction and empirical variance ingredients. The aggregate uses the sum of standard deviations divided by sqrt(3), not a pooled square root. Theorem 4 evaluates alpha/3. The main-text normal critical-value convention is not explicitly defined.','Section 3.2.1 — Confidence interval (23)-(24)')
add(27,'sparsity assumption',r'''There exists a sequence $(b_n)_{n=1}^\infty$ with $\lim_{n\to\infty}b_n=0$ such that $s=b_n\sqrt n/\log p$.''',[13],[7],[r's=b_n\sqrt n/\log p',r'b_n'],'Sequence-level sparsity for Theorem 4; not silently imported into Theorem 5 through its construction reference.','Assumption 6',kind='assumption',context=r'''To this end, we require an explicit sparsity assumption on the propensity score model; note that we avoided making such an assumption in Theorem 2 for example.''',phrases=['Assumption 6'])
add(28,'variances of the errors',r'''There exists constant $\sigma_\varepsilon>0$ such that $\min_{t=0,1}\operatorname{Var}(\varepsilon(t))\geq\sigma_\varepsilon^2$.''',[13],[19],[r'\min_{t=0,1}\operatorname{Var}(\varepsilon(t))\geq\sigma_\varepsilon^2'],'Positive lower bound for marginal residual variances, not a covariate-wise conditional variance bound.','Assumption 7',kind='assumption',context=r'''We also make the mild assumption that the variances of the errors $\varepsilon(0),\varepsilon(1)$ are bounded away from zero.''',phrases=['Assumption 7'])
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
