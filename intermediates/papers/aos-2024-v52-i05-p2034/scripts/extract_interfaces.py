"""Preserve original main-text source entries for the two-Theorem census."""
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
add(1,'linear regression model',r'''Consider the following linear regression model:
\[
y=b_0+\mathbf x^\top\boldsymbol\beta+\varepsilon,
\]
(1)
where $y$ is the response, $\mathbf x$ is a $p$-dimensional random vector with mean $\boldsymbol\mu_X$ and covariance matrix $\Sigma_X$, $\boldsymbol\beta$ is the regression coefficient vector, $b_0$ is the intercept, and $\varepsilon$ is the random error independent from $\mathbf x$ with $\mathbb E(\varepsilon\mid\mathbf x)=0$ and $\operatorname{Var}(\varepsilon\mid\mathbf x)=\sigma^2$.''',[2,3],[],[r'\Sigma_X',r'\boldsymbol\beta',r'\sigma^2'],'Random-design linear model with an intercept, error-design independence, conditional mean zero and constant conditional variance. Do not weaken the stated independence to uncorrelatedness.','Section 2 — Linear regression model (1)',kind='source_passage')
add(2,'hypothesis',r'''Suppose that $\{\mathbf x_i,y_i\}$, $i=1,\ldots,n$, are independent and identically distributed (i.i.d.) random samples from model (1). Of interest is to test the hypothesis
\[
H_0:\boldsymbol\beta=\boldsymbol\beta_0\quad\text{versus}\quad H_1:\boldsymbol\beta\ne\boldsymbol\beta_0,
\]
(2)
where $\boldsymbol\beta_0$ is known.''',[3],[1],[r'H_0',r'\boldsymbol\beta_0'],'Iid sampling and the known-vector null. The later REM proof centers the null at zero; this general hypothesis is not silently changed.','Section 2.1 — Hypotheses (2)',kind='source_passage')
add(3,'score function',r'''This motivates us to define $\mathbf z_i=(\mathbf x_i-\boldsymbol\mu_X)\{y_i-\mu_Y-(\mathbf x_i-\boldsymbol\mu_X)^\top\boldsymbol\beta_0\}$ for the purpose of testing (2). Denote $\boldsymbol\mu=\mathbb E(\mathbf z_i)$, which gives us
\[
\boldsymbol\mu=\mathbb E\{(\mathbf x_i-\boldsymbol\mu_X)[(\mathbf x_i-\boldsymbol\mu_X)^\top(\boldsymbol\beta-\boldsymbol\beta_0)+\varepsilon_i]\}=\Sigma_X(\boldsymbol\beta-\boldsymbol\beta_0).
\]''',[3],[1,2],[r'\mathbf z_i',r'\boldsymbol\mu=\mathbb E(\mathbf z_i)'],'Population-centered score vector and its expectation. Population covariance in Omega is interpreted using this score; it is distinct from sample-centered score vectors.','Section 2.1 — Population score',context=r'''Hence, for nonsingular $\Sigma_X$, testing the hypothesis in (2) is equivalent to a one-sample mean testing problem on the mean of the score function''')
add(4,'score equation vectors',r'''In practice, $\boldsymbol\mu_X$ and $\mu_Y$ are unknown. It is natural to use the sample means $\bar{\mathbf x}$ and $\bar y$ to estimate $\boldsymbol\mu_X$ and $\mu_Y$, respectively. Thus, with a slight abuse of notation, we define
\[
\mathbf z_i=(\mathbf x_i-\bar{\mathbf x})\{y_i-\bar y-(\mathbf x_i-\bar{\mathbf x})^\top\boldsymbol\beta_0\}
\]
for the purpose of hypothesis testing (3).''',[3,4],[1,2],[r'\mathbf z_i',r'\bar{\mathbf x}'],'Sample-centered scores computed from the whole sample. They share sample means and must not be treated as iid population-centered score vectors.','Section 2.1 — Scores using sample means',context=r'''To construct the test statistic $T_n$, we first create the necessary score equation vectors''',context_page=23)
add(5,'statistic',r'''For the one-sample mean testing problem (3), we define a statistic that we will use to construct a test statistic $T_n$ in (5) below
\[
W_n=\frac2{n(n-1)}\sum_{i<j}[\mathbf z_i^\top\mathbf z_j+k_n\boldsymbol\alpha^\top\mathbf z_i\mathbf z_j^\top\boldsymbol\alpha],
\]
(4)
where $\boldsymbol\alpha$ is a $p$-dimensional vector with $\|\boldsymbol\alpha\|=1$, and $k_n$ is a positive number.''',[4],[4],[r'W_n',r'k_n\boldsymbol\alpha^\top\mathbf z_i\mathbf z_j^\top\boldsymbol\alpha'],'Unstudentized score statistic, including the positive-weight power-enhancement term. The source later uses the same formula with population means for derivation; that usage is retained separately.','Section 2.1 — Statistic (4)')
add(6,'sample covariance',r'''$\widehat\Sigma_Z$ is the sample covariance of $\mathbf z$,''',[5],[4],[r'\widehat\Sigma_Z'],'Sample covariance of the sample-centered score vectors. This is distinct from the separately defined estimate of the squared population covariance in (6).','Section 2.1 — Sample covariance')
add(7,'estimators',r'''\[
\widehat{\Sigma_Z^2}=\frac1{n(n-1)}\sum_{i\ne j}\left(\mathbf z_i\mathbf z_j^\top-\frac1{n(n-1)}\sum_{i\ne j}\mathbf z_i\mathbf z_j^\top\right)^2
\]
\[
=\frac1{n(n-1)}\sum_{i\ne j}(\mathbf z_i\mathbf z_j^\top)^2-\left(\frac1{n(n-1)}\sum_{i\ne j}\mathbf z_i\mathbf z_j^\top\right)^2.
\]
(6)''',[5],[4],[r'\widehat{\Sigma_Z^2}'],'Original squared-covariance estimator with ordered off-diagonal pairs and ordinary matrix squares. The hat covers Sigma_Z squared; this is not the square of the sample covariance. No positivity fallback is inserted.','Section 2.1 — Estimator (6)',context=r'''The rationale in the derivation of these estimators is similar to that of the derivation of the test statistic $W_n$.''')
add(8,'test statistic',r'''We further propose our test statistic $T_n$ based on $W_n$ as
\[
T_n=\frac{nW_n}{\sqrt{2\widehat{\operatorname{tr}(\Omega^2)}}},
\]
(5)
where $\widehat{\operatorname{tr}(\Omega^2)}$ is defined as
\[
\widehat{\operatorname{tr}(\Omega^2)}=\operatorname{tr}(\widehat{\Sigma_Z^2})+2k_n\boldsymbol\alpha^\top\widehat{\Sigma_Z^2}\boldsymbol\alpha+k_n^2(\boldsymbol\alpha^\top\widehat\Sigma_Z\boldsymbol\alpha)^2,
\]''',[5],[5,6,7],[r'T_n',r'\widehat{\operatorname{tr}(\Omega^2)}'],'Studentized statistic and complete estimated trace formula. Its denominator is an estimate, whereas the shift in Theorem 1 uses the population trace. The defining formula does not require a population Omega matrix as an input.','Section 2.1 — Test statistic (5)')
add(9,'Assumption A1',r'''$\mathbf x_i=\boldsymbol\mu_X+\Gamma\mathbf x_{0i}$, where $\mathbf x_{0i}$, $i=1,\ldots,n$, are i.i.d. random vectors of length $p$ with elements having mean zero, variance one, and bounded fourth order moments, $\Gamma=\Sigma_X^{1/2}$, $\mathbf x_{0i}=(x_{0i1},\ldots,x_{0ip})^\top$ and $\mathbb E(x_{0i\alpha_1}^{l_{\alpha_1}}\cdots x_{0i\alpha_s}^{l_{\alpha_s}})=\mathbb E(x_{0i\alpha_1}^{l_{\alpha_1}})\cdots\mathbb E(x_{0i\alpha_s}^{l_{\alpha_s}})$ for $1\leq\alpha_1<\ldots<\alpha_s\leq p$ and $\sum_{i=1}^s l_{\alpha_i}\leq4$.''',[5],[1],[r'\Gamma=\Sigma_X^{1/2}',r'\sum_{i=1}^s l_{\alpha_i}\leq4'],'Coordinate moments factor only through total degree four. Full coordinate independence, Gaussian design and higher-moment factorization are not asserted.','Assumption A1',kind='assumption',context='Assumption A1 is similar to the independent component assumption widely used in high-dimensional literature (Bai and Saranadasa (1996)).',context_page=6,phrases=['A1'])
add(10,'Assumption A2',r'''$\varepsilon_i$, $i=1,\ldots,n$, are i.i.d. random variables with mean zero and variance $\sigma^2$, and bounded fourth order moments.''',[5],[1],[r'\sigma^2'],'Iid errors with bounded fourth moments. Error-design independence belongs to the model; Gaussian errors are added only in Theorem 2(i).','Assumption A2',kind='assumption',context='Assumption A2 is a mild assumption on the distribution of the random error.',context_page=6,phrases=['A2'])
add(11,'local alternative',r'''We further assume that the local alternative has the following form:
\[
H_a:\boldsymbol\beta=\boldsymbol\beta_0+n^{-1/2}\delta\mathbf u\quad\text{with }|\delta|\leq C\text{ and }\|\mathbf u\|=1,
\]
(7)
where $C$ is a nonnegative constant independent of $p$, and $\|\cdot\|$ is the Euclidean $L_2$ norm.''',[6],[1,2],[r'H_a',r'|\delta|\leq C'],'Deterministic local coefficient displacement with bounded scalar delta and unit direction. The source explicitly states C independent of p; the separate REM is not substituted.','Section 2.2 — Local alternative (7)',kind='condition')
add(12,'random effects model',r'''To study the optimality of the proposed test, we follow the random effects setting in Arias-Castro, Candès and Plan (2011a), and consider a random effects model (REM) with the following prior $\pi$ on the regression coefficient vector in the alternatives: the regression vector $\boldsymbol\beta$ has $S=p^{1-s}$ nonzero coefficients following i.i.d. sub-Gaussian distributions with mean zero and variance $\gamma^2$, and the support of $\boldsymbol\beta$ is uniformly randomly generated among the size-$S$ subsets of $\{1,2,\ldots,p\}$.''',[8],[1],[r'S=p^{1-s}',r'\gamma^2'], 'Prior on the sparse coefficient vector, with uniform fixed-size support and iid mean-zero sub-Gaussian nonzero coefficients of actual variance gamma squared. Theorem 2 restricts s to [0,1/2]; no precise common proxy bound or rounding rule for S is supplied here.','Section 2.2 — Random effects model',kind='source_passage')
add(13,'rejection region',r'''From Theorem 1, the test with the rejection region $\{T_n>z_a\}$ has asymptotic size $a$, where $z_a$ is the right $a$ quantile of the standard normal distribution.''',[6],[8],[r'T_n>z_a'],'Source test rule using the right-tail normal critical value. The accompanying size statement is preserved as source context; it does not cause Theorem 2 to inherit every assumption of Theorem 1.','Section 2.2 — Rejection region',kind='source_passage')
add(14,'average risk',r'''$\operatorname{Risk}_\pi(T)=P_0(T=1)+\mathbb E_\pi[\mathbb I(T=0)]$, where $P_0(T=1)$ is the type I error and $\mathbb E_\pi[\mathbb I(T=0)]$ is the type II error under the prior $\pi$ on the alternatives.''',[13],[2,12],[r'\operatorname{Risk}_\pi(T)'],'Sum of null rejection error and prior-averaged nonrejection error, used to interpret the all-tests lower bound in Theorem 2(i). T is a generic binary test, not the studentized statistic T_n. The original expectation notation is retained.','Section 2.3.3 — Average risk',context=r'''By the Neyman-Pearson lemma, the likelihood ratio test $T=\{W(\mathbf X,\mathbf y)>1\}$ minimizes the average risk''')
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
