"""Preserve original EILLS model, objectives, conditions and theorem-local quantities."""
import json
from save_inventory import ROOT,PID,STATEMENTS
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
add(1,'important variables',r'''The distribution of $\mathbf x$ and $y$, $\mu$, satisfies
\[
\mu\in\mathcal U_{\boldsymbol\beta^*,\sigma^2}=\left\{\mu:\mathbb E_\mu[y\mid\mathbf x_{S^*}]=(\boldsymbol\beta_{S^*}^*)^\top\mathbf x_{S^*},\ \operatorname{Var}_\mu[y\mid\mathbf x_{S^*}]\le\sigma^2,\quad\mu\text{-a.s. }\mathbf x,\quad\forall j\in[p],\ \mathbb E_\mu[x_j^2]\le\sigma^2\right\}.
\]
(2.1)
Here, $S^*\subseteq[p]$ denotes the set of important variables that contribute to explain the “truth”, $\boldsymbol\beta^*$ is the parameter of interest whose support set $\operatorname{supp}(\boldsymbol\beta^*)$ is $S^*$, and $\sigma^2$ is any given positive number.''',[6],[],[r'\mathcal U_{\boldsymbol\beta^*,\sigma^2}',r'S^*'],'Common conditional mean on the unknown true support, conditional variance bound and marginal second moments. No full-covariate exogeneity or SCM assumption is imposed.','Section 2.1 — Distribution class (2.1)')
add(2,'residuals',r'''We also define $\varepsilon^{(e)}=y^{(e)}-\mathbb E[y^{(e)}\mid\mathbf x_{S^*}^{(e)}]=y^{(e)}-(\boldsymbol\beta^*)^\top\mathbf x^{(e)}$ and $\varepsilon_i^{(e)}=y_i^{(e)}-(\boldsymbol\beta^*)^\top\mathbf x_i^{(e)}$.''',[8],[1],[r'\varepsilon^{(e)}',r'\varepsilon_i^{(e)}'],'True residual, distinct from candidate-model fitted residual. Orthogonal to true-support covariates but possibly correlated with others.','Section 2.2 — True residual',context='but the collected covariates are easily correlated with residuals of $y$ on $\\mathbf x_{S^*}$',context_page=6)
add(3,'population covariance matrix',r'''Let $\widehat{\mathbf\Sigma}^{(e)}$ and $\mathbf\Sigma^{(e)}$ denote the empirical covariance matrix and population covariance matrix for environment $e\in\mathcal E$, respectively, that is, $\widehat{\mathbf\Sigma}^{(e)}=\widehat{\mathbb E}[\mathbf x^{(e)}(\mathbf x^{(e)})^\top]$ and $\mathbf\Sigma^{(e)}=\mathbb E[\mathbf x^{(e)}(\mathbf x^{(e)})^\top]$.''',[8],[],[r'\mathbf\Sigma^{(e)}'],'Source calls raw second moments covariances; the centered-covariate convention is stated on page 12.','Section 2.2 — Environment covariance matrices')
add(4,'population $L^2$ risk',r'''\[R^{(e)}(\boldsymbol\beta)=\mathbb E[|y^{(e)}-\boldsymbol\beta^\top\mathbf x^{(e)}|^2].\]
(2.5)''',[8],[],[r'R^{(e)}(\boldsymbol\beta)'],'Population squared prediction risk for one environment. Empirical risk is separately retained as D27; no data dependence is imported into a population objective.','Section 2.2 — Population risk (2.5)',context=r'''Define the empirical $L^2$ risk $\widehat R^{(e)}$ and population $L^2$ risk $R^{(e)}$ as''',context_page=8)
add(5,'population-level best linear predictor',r'''When $\mathbf\Sigma^{(e)}$ is positive definite, for any $S\subseteq[p]$ we can define the $\boldsymbol\beta^{(e,S)}$, the population-level best linear predictor constrained on $S$ for environment $e\in\mathcal E$ as
\[
\boldsymbol\beta^{(e,S)}=\underset{\boldsymbol\beta\in\mathbb R^p,\operatorname{supp}(\boldsymbol\beta)\subseteq S}{\operatorname{argmin}}R^{(e)}(\boldsymbol\beta).
\]
(2.6)
It is worth noticing that though $\boldsymbol\beta^{(e,S)}\in\mathbb R^p$, the support set of $\boldsymbol\beta^{(e,S)}$ is a subset of $S$.''',[8],[3,4],[r'\boldsymbol\beta^{(e,S)}'],'Full p-vector supported within S, not required to have support exactly S. Positive-definite environment covariance gives uniqueness.','Section 2.2 — Restricted least-squares predictor (2.6)')
add(6,'pre-determined weights',r'''where $\omega=(\omega^{(e)})_{e\in\mathcal E}\in\mathbb R^{|\mathcal E|}$ are pre-determined weights associated with environments $\mathcal E$ satisfying $\sum_{e\in\mathcal E}\omega^{(e)}=1$ and $\omega^{(e)}>0$ for any $e\in\mathcal E$. Some typical choices of $\omega$ can be $\omega^{(e)}=1/|\mathcal E|$ or $\omega^{(e)}=n^{(e)}/(\sum_{e'\in\mathcal E}n^{(e')})$.''',[10],[],[r'\omega^{(e)}'],'General method allows positive normalized fixed weights. Section 4 theorems specialize to equal weights and equal n.','Section 3.1 — Environment weights')
add(7,'focused linear invariance regularizer',r'''Based on the above derivations, we propose to minimize a focused linear invariance regularizer, whose population-level form $J(\boldsymbol\beta;\omega)$ can be written as
\[
J(\boldsymbol\beta;\omega)=\sum_{j=1}^p\mathbb1\{\beta_j\ne0\}\sum_{e\in\mathcal E}\frac{\omega^{(e)}}4|\nabla_jR^{(e)}(\boldsymbol\beta)|^2.
\]
(3.2)''',[9],[4,6],[r'J(\boldsymbol\beta;\omega)',r'\mathbb1\{\beta_j\ne0\}'],'Penalize population risk gradients only in active coordinates, with the original one-quarter factor. The support gate makes this generally nonconvex and discontinuous.','Section 3.1 — Population focused regularizer (3.2)')
add(8,'observations',r'''For each $e\in\mathcal E$, suppose we have $n^{(e)}$ observations $\{(\mathbf x_i^{(e)},y_i^{(e)})\}_{i=1}^{n^{(e)}}\subseteq\mathbb R^p\times\mathbb R$ drawn i.i.d. from some distribution $\mu^{(e)}$. Let $\mathbb E[f(\mathbf x^{(e)},y^{(e)})]=\int f(x,y)\mu^{(e)}(dx,dy)$ and $\widehat{\mathbb E}[f(\mathbf x^{(e)},y^{(e)})]=\frac1{n^{(e)}}\sum_{i=1}^{n^{(e)}}f(\mathbf x_i^{(e)},y_i^{(e)})$ for a measurable function $f$.''',[7,8],[],[r'\widehat{\mathbb E}',r'n^{(e)}'],'Expectation and within-environment empirical average; the theorem regime additionally fixes n^(e)=n and cross-environment independence.','Section 2.2 — Empirical expectation')
add(9,'empirical-level focused linear invariance regularizer',r'''Given data $\{D^{(e)}\}_{e\in\mathcal E}=\{\{(\mathbf x_i^{(e)},y_i^{(e)})\}_{i=1}^{n^{(e)}}\}_{e\in\mathcal E}$ from heterogeneous environments, the empirical-level focused linear invariance regularizer with weights $\omega$ can be written as
\[
\widehat J(\boldsymbol\beta;\omega)=\sum_{j=1}^p\mathbb1\{\beta_j\ne0\}\sum_{e\in\mathcal E}\omega^{(e)}\left|\widehat{\mathbb E}[x_j^{(e)}(y^{(e)}-\boldsymbol\beta^\top\mathbf x^{(e)})]\right|^2.
\]
(3.5)''',[10],[6,8],[r'\widehat J(\boldsymbol\beta;\omega)',r'\mathbb1\{\beta_j\ne0\}'],'Square the empirical residual-covariate moment within each environment, then average across environments; not the empirical average of squared products or square of a pooled moment.','Section 3.2 — Empirical focused regularizer (3.5)')
add(10,'pooled empirical $L^2$ loss',r'''Recall that $\widehat R^{(e)}(\boldsymbol\beta)$ defined in (2.5) is the empirical $L^2$ loss in environment in $e\in\mathcal E$. We also define the following pooled empirical $L^2$ loss over all the environments: for $\boldsymbol\beta\in\mathbb R^p$,
\[
\widehat R(\boldsymbol\beta;\omega)=\sum_{e\in\mathcal E}\omega^{(e)}\widehat R^{(e)}(\boldsymbol\beta)=\sum_{e\in\mathcal E}\frac{\omega^{(e)}}{n^{(e)}}\sum_{i=1}^{n^{(e)}}\{y_i^{(e)}-\boldsymbol\beta^\top\mathbf x_i^{(e)}\}^2.
\]
(3.6)''',[10],[6,8,27],[r'\widehat R(\boldsymbol\beta;\omega)'],'Weighted average of within-environment sample losses; balanced theory uses total sample n times |E|.','Section 3.2 — Pooled empirical loss (3.6)')
add(11,'environment invariant linear least squares',r'''The environment invariant linear least squares (EILLS) estimator $\widehat{\boldsymbol\beta}_Q$ is defined by minimizing the following objective function:
\[
\widehat Q(\boldsymbol\beta;\gamma,\omega)=\widehat R(\boldsymbol\beta;\omega)+\gamma\widehat J(\boldsymbol\beta;\omega),
\]
(3.7)
which is a linear combination of the pooled empirical $L^2$ loss $\widehat R(\boldsymbol\beta;\omega)$ and focused linear invariance regularizer $\widehat J(\boldsymbol\beta;\omega)$ with weights $(1,\gamma)$ for some given hyper-parameter $\gamma\in\mathbb R^+$.''',[11],[9,10],[r'\widehat{\boldsymbol\beta}_Q',r'\widehat Q(\boldsymbol\beta;\gamma,\omega)'],'Global empirical minimizer of the focused objective, not an arbitrary stationary point or the population optimizer.','Section 3.2 — EILLS estimator (3.7)')
add(12,'population analogs',r'''We also define the population analogs of the EILLS objective function as follows:
\[
Q(\boldsymbol\beta;\gamma,\omega)=R(\boldsymbol\beta;\omega)+\gamma J(\boldsymbol\beta;\omega)\quad\text{with}\quad R(\boldsymbol\beta;\omega)=\sum_{e\in\mathcal E}\omega^{(e)}\mathbb E[|y^{(e)}-\mathbf x^\top\mathbf x^{(e)}|^2].
\]
(3.8)''',[11],[4,6,7],[r'Q(\boldsymbol\beta;\gamma,\omega)'],'Printed population formula has x^T x^(e), not beta^T x^(e). Preserve this source typo; (2.5), the empirical analog and theorem context indicate the intended pooled squared prediction risk. The normalized interpretation is separate from the quotation.','Section 3.2 — Population EILLS objective (3.8)')
add(13,'regularized EILLS estimator',r'''They can be eliminated further by introducing an $\ell_0$ penalty. This leads us to considering the $\ell_0$ regularized EILLS estimator $\widehat{\boldsymbol\beta}_L$ that minimizes the following objective:
\[
\widehat L(\boldsymbol\beta;\lambda,\gamma,\omega)=\widehat Q(\boldsymbol\beta;\gamma,\omega)+\lambda\|\boldsymbol\beta\|_0=\widehat R(\boldsymbol\beta;\omega)+\gamma\widehat J(\boldsymbol\beta;\omega)+\lambda\|\boldsymbol\beta\|_0
\]
(3.9)
with given hyper-parameter $\lambda$. This helps reduce variables that are uncorrelated to residuals and $y$.''',[11],[11],[r'\widehat{\boldsymbol\beta}_L',r'\lambda\|\boldsymbol\beta\|_0'],'Global minimizer with support-cardinality penalty, distinct from the unpenalized EILLS estimator. Main-text results do not analyze Gumbel approximations or generic local solvers.','Section 3.2 — Penalized EILLS estimator (3.9)')
add(14,'pooled covariance matrix',r'''Define the pooled covariance matrix $\mathbf\Sigma=\frac1{|\mathcal E|}\sum_{e\in\mathcal E}\mathbf\Sigma^{(e)}$.''',[11],[3],[r'\mathbf\Sigma=\frac1{|\mathcal E|}'],'Uniform population second-moment average. Condition 4.3 standardizes every environment by this pooled matrix, not its own covariance.','Section 4 — Pooled covariance')
add(15,'smallest eigenvalue',r'''There exists some universal constants $\kappa_L\in(0,1]$ and $\kappa_U\in[1,\infty)$ such that
\[
\forall e\in\mathcal E,\quad\kappa_L\mathbf I_p\preceq\mathbf\Sigma^{(e)}\preceq\kappa_U\mathbf I_p.
\]
(4.1)''',[11],[3],[r'\kappa_L\mathbf I_p\preceq\mathbf\Sigma^{(e)}\preceq\kappa_U\mathbf I_p'],'Uniform full-population eigenvalue bounds across environments. Not a restricted eigenvalue condition on only sparse vectors or a sample covariance bound.','Condition 4.2',kind='condition',context=r'''The lower bound on the smallest eigenvalue, $\kappa_L$, is to establish non-asymptotic error bounds on $\ell_2$ norm $\|\widehat{\boldsymbol\beta}-\boldsymbol\beta^*\|_2$.''',context_page=12)
add(16,'joint sub-Gaussian condition',r'''There exists some universal constant $\sigma_x\in[1,\infty)$ such that
\[
\forall e\in\mathcal E,\mathbf v\in\mathbb R^p,\quad\mathbb E\left[\exp\{\mathbf v^\top\mathbf\Sigma^{-1/2}\mathbf x^{(e)}\}\right]\le\exp\left(\frac{\sigma_x^2}2\cdot\|\mathbf v\|_2^2\right).
\]
(4.2)''',[11],[14],[r'\mathbf\Sigma^{-1/2}\mathbf x^{(e)}'],'Uniform sub-Gaussian vector condition with pooled covariance normalization and every vector v. Not just coordinatewise tails.','Condition 4.3',kind='condition',context='One can also substitute the joint sub-Gaussian condition of the covariate with the marginal sub-Weibull condition',context_page=12)
add(17,'sub-Gaussian condition of the noise',r'''There exists some universal constant $\sigma_\varepsilon\in\mathbb R^+$ such that,
\[
\forall e\in\mathcal E,\lambda\in\mathbb R,\quad\mathbb E[e^{\lambda\varepsilon^{(e)}}]\le e^{\frac12\lambda^2\sigma_\varepsilon^2}.
\]
(4.3)''',[11],[2],[r'\mathbb E[e^{\lambda\varepsilon^{(e)}}]'],'Marginal sub-Gaussian true residual uniformly over environments; not conditional sub-Gaussianity given every covariate and not independence from all covariates.','Condition 4.4',kind='condition',context=r'''For example, one can replace the sub-Gaussian condition of the noise $\varepsilon^{(e)}$ with the sub-Weibull condition (Vladimirova et al., 2020).''',context_page=12)
add(18,'Pooled Linear Spurious Variables',r'''We let $G$ be the index set of all pooled linear spurious variables in environments $\mathcal E$ concerning the uniform weights $\omega^{(e)}\equiv1/|\mathcal E|$, that is, $G=\{j\in[p]:\sum_{e\in\mathcal E}\mathbb E[x_j^{(e)}\varepsilon^{(e)}]\ne0\}$. We say $x_j$ is a pooled linear spurious variable if $j\in G$.''',[12],[2],[r'G=\{j\in[p]',r'\mathbb E[x_j^{(e)}\varepsilon^{(e)}]'],'Pooled correlation can cancel across environments. G excludes covariates with zero pooled residual correlation even if some individual correlations are nonzero. G^c means complement within [p].','Definition 4.1 — Pooled Linear Spurious Variables',context='Pooled Linear Spurious Variables.',context_page=12)
add(19,'Identification',r'''For any $S\subseteq[p]$ satisfying $S\cap G\ne\varnothing$, there exists some $e,e'\in\mathcal E$ such that $\boldsymbol\beta^{(e,S)}\ne\boldsymbol\beta^{(e',S)}$, where $\boldsymbol\beta^{(e,S)}$ is defined in (2.6).''',[13],[5,18],[r'S\cap G\ne\varnothing',r'\boldsymbol\beta^{(e,S)}'],'Every set intersecting pooled spurious variables has differing restricted least-squares coefficients in some pair of environments, possibly depending on S. Not only supersets of S*.','Condition 4.5 — Identification',kind='condition',context='Condition 4.5 (Identification).',context_page=13)
add(20,'bias mean',r'''$b_S=\|\frac1{|\mathcal E|}\sum_{e\in\mathcal E}\mathbb E[\varepsilon^{(e)}\mathbf x_S^{(e)}]\|_2^2$''',[13],[2],[r'b_S'],'Squared norm of the pooled residual-covariate mean; distinct from the average of squared environment biases. Interpretation as coefficient bias in Remark4.2 is restricted to S containing S*.','Theorem 4.2 — Bias mean',kind='theorem_excerpt',context='Here we refer to $b_S$ as bias mean',context_page=13)
add(21,'variance of bias',r'''$\bar d_S=\sum_{e\in\mathcal E}\frac1{|\mathcal E|}\|\boldsymbol\beta^{(e,S)}-\bar{\boldsymbol\beta}^{(S)}\|_2^2$ with $\bar{\boldsymbol\beta}^{(S)}=\frac1{|\mathcal E|}\sum_{e'\in\mathcal E}\boldsymbol\beta^{(e',S)}$''',[13],[5],[r'\bar d_S',r'\bar{\boldsymbol\beta}^{(S)}'],'Average squared dispersion of full-p restricted predictors around their environment mean. Definition applies to arbitrary S; its bias interpretation is separately qualified.','Theorem 4.2 — Environment coefficient dispersion',kind='theorem_excerpt',context=r'''Thus, the quantity $\bar d_S$ can be interpreted as the variance of bias since it measures the variations of the biases $\Delta^{(e)}$ among different environments.''',context_page=13)
add(22,'Critical Threshold',r'''\[
\gamma^*=(\kappa_L)^{-3}\sup_{S:S\cap G\ne\varnothing}(b_S/\bar d_S).
\]
(4.5)''',[13],[15,18,20,21],[r'\gamma^*',r'\sup_{S:S\cap G\ne\varnothing}'],'Supremum of the bias-to-dispersion ratio over every support meeting G. Identification makes denominators positive in the nonempty-G regime; empty-family conventions are not specified.','Theorem 4.2 — Critical threshold (4.5)',kind='theorem_excerpt',context='Interpretation of the Critical Threshold',context_page=13)
add(23,'signal of true important variables',r'''Define
\[
s_+=\min_{j\in S^*}|\beta_j^*|^2\qquad\text{and}\qquad s_-=\min_{S\subseteq[p],S\cap G\ne\varnothing}\bar d_S.
\]
(4.7)''',[14],[1,18,21],[r's_+',r's_-'],'Paired screening strengths: squared beta-min and minimum coefficient dispersion over supports meeting G. The two signals are distinct, not interchangeable mathematical variants.','Theorem 4.3 — Screening signals (4.7)',kind='theorem_excerpt',context=r'''Here, the quantities $s_+$ and $s_-$ defined in (4.7) can be interpreted as the signal of true important variables and the signal of heterogeneity, respectively.''',context_page=15)
add(24,'sample size',r'''In the high-dimensional regime, we further define $s^*=|S^*|$, $\beta_{\min}=\min_{j\in S^*}|\beta_j^*|$. We need a condition asserting that the sample size $n$ should be large enough for the given hyper-parameter $\gamma$.
Suppose that $\log(|\mathcal E|)\le C\log p$ and that
(1) $n\ge c_1(\gamma/\kappa_L)\{(s^*+\beta_{\min}^{-2})\log p+(\kappa_L\beta_{\min})^{-1}\sqrt{(s^*+\log p)s^*\log p}\}$
(2) $n\cdot|\mathcal E|\ge c_2(\gamma/\kappa_L)^2(s^*\log p)\{1+1/(\kappa_L\beta_{\min}^2)\}$,
Here $c_1$–$c_2$ are positive universal constants that depend only on $(C,\sigma_x,\kappa_U,\sigma_\varepsilon)$.''',[15,16],[1,15],[r'\beta_{\min}',r'\log(|\mathcal E|)\le C\log p'],'Condition4.6 with the immediately preceding definitions of sparsity and minimum nonzero coefficient. Separate per-environment and total-sample inequalities; constants do not depend on n,p or |E|.','Condition 4.6 — High-dimensional sample size',kind='condition')
add(25,'additional conditions',r'''There exists some universal constants $c_1$–$c_2$ that only depends on $(\kappa_U,\sigma_x,\sigma_\varepsilon)$ such that for any $t>0$, if $n\ge c_1(\gamma/\kappa_L)(p+\log(|\mathcal E|)+t)\{s_+^{-0.5}+s_+^{-1}+(\gamma\kappa_Ls_-)^{-0.5}\}$, and $n\cdot|\mathcal E|\ge c_2(\gamma/\kappa_L)^2(p+t)\{s_+^{-1}+(\gamma\kappa_Ls_-)^{-1}+1\}$''',[14],[15,23],[r'(\gamma\kappa_Ls_-)^{-0.5}',r's_+^{-1}'],'The two additional screening sample bounds from T4.3 are imported only into T4.4’s moreover branch; not into its first bound or the high-dimensional theorem.','Theorem 4.3 — Additional sample conditions',kind='theorem_excerpt',context='Moreover, when the additional conditions in Theorem 4.3 hold, then',context_page=15)
add(26,'balanced data with equal weights',r'''For each $e\in\mathcal E$, $(\mathbf x_1^{(e)},y_1^{(e)}),\ldots,(\mathbf x_n^{(e)},y_n^{(e)})$ are i.i.d. copies of $(\mathbf x^{(e)},y^{(e)})\sim\mu^{(e)}$, where $\mu^{(e)}$ belongs to $\mathcal U_{\boldsymbol\beta^*,\sigma^2}$ for some $\sigma^2$. The data from different environments are also independent. We set $\omega^{(e)}\equiv1/|\mathcal E|$.''',[11],[1],[r'\mathcal U_{\boldsymbol\beta^*,\sigma^2}',r'\omega^{(e)}\equiv1/|\mathcal E|'],'Independent iid samples within each environment and across environments, equal n and uniform weights. Unequal-size/weight theory is deferred to Appendix A and excluded.','Condition 4.1',kind='condition',context=r'''To simplify the presentation, we consider the case of balanced data with equal weights, that is, $n^{(e)}\equiv n$ and $\omega^{(e)}\equiv1/|\mathcal E|$, and defer the results of varying $(n^{(e)},\omega^{(e)})$ to Appendix A.''',context_page=11)
add(27,'empirical $L^2$ risk',r'''\[\widehat R^{(e)}(\boldsymbol\beta)=\widehat{\mathbb E}[|y^{(e)}-\boldsymbol\beta^\top\mathbf x^{(e)}|^2].\]
(2.5)''',[8],[8],[r'\widehat R^{(e)}(\boldsymbol\beta)'],'Within-environment empirical squared prediction risk, distinct from its population counterpart D4.','Section 2.2 — Empirical risk (2.5)',context=r'''Define the empirical $L^2$ risk $\widehat R^{(e)}$ and population $L^2$ risk $R^{(e)}$ as''',context_page=8)
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
