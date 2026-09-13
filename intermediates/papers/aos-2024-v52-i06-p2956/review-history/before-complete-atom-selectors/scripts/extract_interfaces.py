"""Save original crossed-model source passages; do not synthesize equivalent definitions."""
import hashlib,json
from save_inventory import ROOT,PID,STATEMENTS
REVIEW_ROOT=ROOT
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
add(1,'two-way crossed random effect with interaction model',r'''Let the total number of rows, columns, and observations per cell be $g$, $h$, and $m$, respectively, so the sample size $n=ghm$. (We explain in the next paragraph why we treat the balanced case with the same number of observations in in each cell.) The two-way crossed random effect with interaction model is
\[
y_{ijk}=\xi_0+\boldsymbol x_{ijk}^T\boldsymbol\xi_s+\alpha_i+\beta_j+\gamma_{ij}+e_{ijk},\tag{1}
\]
for $i=1,\ldots,g$, $j=1,\ldots,h$, $k=1,\ldots,m$, where $\xi_0$ is the intercept, $\boldsymbol\xi_s$ is the $p_0$-dimensional vector of slope parameters, $\alpha_i$ is the random effect due to the $i$th row, $\beta_j$ is the random effect due to the $j$th column, $\gamma_{ij}$ is the interaction random effect of row $i$ and column $j$, and $e_{ijk}$ is the error term. The variables $\alpha_i$, $\beta_j$, $\gamma_{ij}$, and $e_{ijk}$ are assumed mutually independent with zero means and variances $\sigma_\alpha^2$, $\sigma_\beta^2$, $\sigma_\gamma^2$, and $\sigma_e^2$, respectively; we do not assume normality.''',[2],[],[r'\gamma_{ij}',r'n=ghm'],'Balanced crossed rows, columns and cells with four mutually independent zero-mean random-effect families. Gaussian truth is not assumed.','Section 1 — Crossed model (1)',kind='source_passage')
add(2,'covariate',r'''A general covariate $x_{ijk}$ can vary with all subscripts (a within cell covariate), with both $i$ and $j$ (an interaction covariate), or with $i$ (a row covariate) or $j$ (a column covariate) alone. We write $\bar x=n^{-1}\sum_{i=1}^g\sum_{j=1}^h\sum_{k=1}^mx_{ijk}$, $\bar x_{ij}=m^{-1}\sum_{k=1}^mx_{ijk}$, $\bar x_{i.}=(hm)^{-1}\sum_{j=1}^h\sum_{k=1}^mx_{ijk}$, and $\bar x_{.j}=(gm)^{-1}\sum_{i=1}^g\sum_{k=1}^mx_{ijk}$, using the convention that we retain a dot as a placeholder subscript when required (as in $\bar x_{i.}$ and $\bar x_{.j}$) but not when there is no ambiguity (as in $\bar x_{ij}$ and $\bar x$). Then we can decompose a within cell covariate $x_{ijk}$ as $\bar x+(\bar x_{i.}-\bar x)+(\bar x_{.j}-\bar x)+(\bar x_{ij}-\bar x_{i.}-\bar x_{.j}+\bar x)+(x_{ijk}-\bar x_{ij})$, the sum of an overall mean, row, column, interaction, and within cell term. Similarly, we can decompose a covariate at any level into components in each of the higher levels of the hierarchy. This is important to accommodate the fact that the estimated coefficients of the covariates at each level have different rates of convergence; it also exactly orthogonalizes the covariates. Finally, allowing the different terms in the decomposition to have possibly different coefficients in the model increases the flexibility of the model. Following [17], we arrange the covariate vector $\boldsymbol x_{ijk}$ in four subvectors: a $p_a$-vector of row covariates $\boldsymbol x_i^{(a)}$, a $p_b$-vector of column covariates $\boldsymbol x_j^{(b)}$, a $p_{ab}$-vector of interaction covariates $\boldsymbol x_{ij}^{(ab)}$, and a $p_w$-vector of within cell covariates $\boldsymbol x_{ijk}^{(w)}$, where $p=p_a+p_b+p_{ab}+p_w\ge p_0$. Not all of these vectors need be present in the model, but it is helpful to work with the most complete model.''',[3],[1],[r'\boldsymbol x_i^{(a)}',r'\boldsymbol x_{ijk}^{(w)}'],'Original means, hierarchical decomposition and four covariate blocks. Different level coefficients are permitted.','Section 2 — Covariates and decomposition')
add(3,'parameter vector',r'''The two-way crossed classification with interaction model (1) can be generalized to
\[
y_{ijk}=\xi_0+\boldsymbol x_i^{(a)T}\boldsymbol\xi_1+\boldsymbol x_j^{(b)T}\boldsymbol\xi_2+\boldsymbol x_{ij}^{(ab)T}\boldsymbol\xi_3+\boldsymbol x_{ijk}^{(w)T}\boldsymbol\xi_4+\alpha_i+\beta_j+\gamma_{ij}+e_{ijk},\tag{4}
\]
for $i=1,\ldots,g$, $j=1,\ldots,h$, $k=1,\ldots,m$, where $\xi_0$ is the intercept, $\boldsymbol\xi_1$ is the $p_a$-vector of row slopes, $\boldsymbol\xi_2$ is the $p_b$-vector of column slopes, $\boldsymbol\xi_3$ is the $p_{ab}$-vector of interaction slopes, and $\boldsymbol\xi_4$ is the $p_w$-vector of within-cell slopes. We denote a general parameter vector for the model (4) by $\omega=[\xi_0,\boldsymbol\xi_1^T,\sigma_\alpha^2,\boldsymbol\xi_2^T,\sigma_\beta^2,\boldsymbol\xi_3^T,\sigma_\gamma^2,\boldsymbol\xi_4^T,\sigma_e^2]^T$ and the true parameter vector by $\dot\omega=[\dot\xi_0,\dot{\boldsymbol\xi}_1^T,\dot\sigma_\alpha^2,\dot{\boldsymbol\xi}_2^T,\dot\sigma_\beta^2,\dot{\boldsymbol\xi}_3^T,\dot\sigma_\gamma^2,\dot{\boldsymbol\xi}_4^T,\dot\sigma_e^2]^T$. All expectations are taken under the true model with the covariates treated as fixed (i.e. we condition on any random covariates).''',[4],[1,2],[r'\dot\omega',r'\boldsymbol\xi_4'],'Original enlarged balanced model and interleaved parameter order, with true fixed-design expectation.','Section 2 — Model (4) and parameter vector',kind='source_passage')
add(4,'matrix form',r'''To express model (4) in matrix form like (2), let $\boldsymbol\xi=[\xi_0,\boldsymbol\xi_1^T,\boldsymbol\xi_2^T,\boldsymbol\xi_3^T,\boldsymbol\xi_4^T]^T$, $\boldsymbol X^{(a)}=[\boldsymbol x_1^{(a)},\ldots,\boldsymbol x_g^{(a)}]^T$, $\boldsymbol X^{(b)}=[\boldsymbol x_1^{(b)},\ldots,\boldsymbol x_h^{(b)}]^T$, $\boldsymbol X^{(ab)}=[\boldsymbol x_{11}^{(ab)},\ldots,\boldsymbol x_{gh}^{(ab)}]^T$ and $\boldsymbol X^{(w)}=[\boldsymbol x_{111}^{(w)},\ldots,\boldsymbol x_{ghm}^{(w)}]^T$. Then the matrix form of (4) is
\[
\boldsymbol y=\boldsymbol X\boldsymbol\xi+\boldsymbol Z_1\alpha+\boldsymbol Z_2\beta+\boldsymbol Z_3\gamma+\boldsymbol Z_0\boldsymbol e,\tag{5}
\]
where $\boldsymbol X=[\boldsymbol1_n,\boldsymbol X^{(a)}\otimes\boldsymbol1_h\otimes\boldsymbol1_m,\boldsymbol1_g\otimes\boldsymbol X^{(b)}\otimes\boldsymbol1_m,\boldsymbol X^{(ab)}\otimes\boldsymbol1_m,\boldsymbol X^{(w)}]$.''',[4],[2,3,20],[r'\boldsymbol X^{(ab)}\otimes\boldsymbol1_m'],'Original fixed-effect design with Kronecker repetitions matching the stacked balanced observations.','Section 2 — Matrix model (5)')
add(5,'true value',r'''To simplify notation, we let $\eta=g/h$ and $\tau=\sigma_\alpha^2+\eta\sigma_\beta^2$ with true value $\dot\tau=\dot\sigma_\alpha^2+\eta\dot\sigma_\beta^2$.''',[4],[1,3],[r'\eta=g/h',r'\dot\tau'],'Original row-column ratio and combined variance; finite ratios and limiting eta=0/infinity must remain distinct.','Section 2 — Ratio and combined variance')
add(6,'variables that are centered',r'''We define the means of $y_{ijk}$ (and later $e_{ijk}$) analogously to the means of $x_{ijk}$. For variables that are centered, we use the additional subscript $(c)$. We use superscripts $(a)$, $(b)$, $(ab)$, and $(w)$ to indicate that a variable is a row, column, interaction, or within-cell variable, respectively. For example, $\boldsymbol x_{i(c)}^{(a)}=\boldsymbol x_i^{(a)}-\bar{\boldsymbol x}^{(a)}$, $\bar{\boldsymbol x}_{i.(c)}^{(ab)}=\bar{\boldsymbol x}_{i.}^{(ab)}-\bar{\boldsymbol x}^{(ab)}$, $\bar{\boldsymbol x}_{i.(c)}^{(w)}=\bar{\boldsymbol x}_{i.}^{(w)}-\bar{\boldsymbol x}^{(w)}$, and similarly for terms such as $\boldsymbol x_{j(c)}^{(b)}$, $\bar{\boldsymbol x}_{.j(c)}^{(ab)}$, $\bar{\boldsymbol x}_{.j(c)}^{(w)}$, $\bar{\boldsymbol x}_{ij(c)}^{(ab)}$, $\bar{\boldsymbol x}_{ij(c)}^{(w)}$, and $\boldsymbol x_{ijk(c)}^{(w)}$.''',[4],[2],[r'\boldsymbol x_{i(c)}^{(a)}',r'\boldsymbol x_{ijk(c)}^{(w)}'],'Original centering conventions and examples. The precise cell/within residualization is only referred to as similar here; do not replace it using an unread appendix.','Section 2 — Centering conventions')
add(7,'sums of squares',r'''We also define sums of squares for certain variables. Let $\boldsymbol X_{i(c)}^{(a)}=[\boldsymbol x_{i(c)}^{(a)T},\bar{\boldsymbol x}_{i.(c)}^{(ab)T},\bar{\boldsymbol x}_{i.(c)}^{(w)T}]^T$, $\boldsymbol X_{j(c)}^{(b)}=[\boldsymbol x_{j(c)}^{(b)T},\bar{\boldsymbol x}_{.j(c)}^{(ab)T},\bar{\boldsymbol x}_{.j(c)}^{(w)T}]^T$ and $\boldsymbol X_{ij(c)}^{(ab)}=[\boldsymbol x_{ij(c)}^{(ab)T},\bar{\boldsymbol x}_{ij(c)}^{(w)T}]^T$. Then we write
\[
\sum_{i=1}^g\boldsymbol X_{i(c)}^{(a)}\boldsymbol X_{i(c)}^{(a)T}=
\begin{bmatrix}
SA_{\boldsymbol x^{(a)}}&SA_{\boldsymbol x^{(a)},(ab)}&SA_{\boldsymbol x^{(a)},(w)}\\
SA_{\boldsymbol x^{(ab)},(a)}&SA_{\boldsymbol x^{(ab)}}&SA_{\boldsymbol x^{(ab)},(w)}\\
SA_{\boldsymbol x^{(w)},(a)}&SA_{\boldsymbol x^{(w)},(ab)}&SA_{\boldsymbol x^{(w)}}
\end{bmatrix},
\]
\[
\sum_{j=1}^h\boldsymbol X_{j(c)}^{(b)}\boldsymbol X_{j(c)}^{(b)T}=
\begin{bmatrix}
SB_{\boldsymbol x^{(b)}}&SB_{\boldsymbol x^{(b)},(ab)}&SB_{\boldsymbol x^{(b)},(w)}\\
SB_{\boldsymbol x^{(ab)},(b)}&SB_{\boldsymbol x^{(ab)}}&SB_{\boldsymbol x^{(ab)},(w)}\\
SB_{\boldsymbol x^{(w)},(b)}&SB_{\boldsymbol x^{(w)},(ab)}&SB_{\boldsymbol x^{(w)}}
\end{bmatrix},
\]
\[
\sum_{i=1}^g\sum_{j=1}^h\boldsymbol X_{ij(c)}^{(ab)}\boldsymbol X_{ij(c)}^{(ab)T}=
\begin{bmatrix}SAB_{\boldsymbol x^{(ab)}}&SAB_{\boldsymbol x^{(ab)},(w)}\\SAB_{\boldsymbol x^{(w)},(ab)}&SAB_{\boldsymbol x^{(w)}}\end{bmatrix},
\]
and $\sum_{i=1}^g\sum_{j=1}^h\sum_{k=1}^m\boldsymbol x_{ijk(c)}^{(w)}\boldsymbol x_{ijk(c)}^{(w)T}=SW_{\boldsymbol x^{(w)}}$.''',[4],[6],[r'\boldsymbol X_{i(c)}^{(a)}',r'SW_{\boldsymbol x^{(w)}}'],'Original enlarged Gram blocks. Capital X stacks multiple covariate types and is not interchangeable with the lowercase row block.','Section 2 — Sums of squares')
add(8,'block matrices',r'''We define the block matrices $\hat{\boldsymbol D}_1=g^{-1}SA_{\boldsymbol x^{(a)}}$, $\hat{\boldsymbol D}_2=h^{-1}SB_{\boldsymbol x^{(b)}}$, $\hat{\boldsymbol D}_3=(gh)^{-1}SAB_{\boldsymbol x^{(ab)}}$ and $\hat{\boldsymbol D}_4=n^{-1}SW_{\boldsymbol x^{(w)}}$, and their respective limits $\boldsymbol D_1=\lim_{g\to\infty}\hat{\boldsymbol D}_1$, $\boldsymbol D_2=\lim_{h\to\infty}\hat{\boldsymbol D}_2$, $\boldsymbol D_3=\lim_{g,h\to\infty}\hat{\boldsymbol D}_3$ and $\boldsymbol D_4=\lim_{g,h,m\to\infty}\hat{\boldsymbol D}_4$. For a comprehensive list of all notation, refer to Appendix A.''',[4],[1,7],[r'\hat{\boldsymbol D}_1',r'\boldsymbol D_4'],'Original selected normalized Gram blocks and their four asymptotic limits. The appendix reference is preserved but its body is excluded.','Section 2 — Normalized block matrices')
add(9,'log-likelihood',r'''The log-likelihood for the parameters in model (5) is
\[
l(\omega;\boldsymbol y)=-\frac n2\log2\pi-\frac12\log|\boldsymbol V|-\frac12(\boldsymbol y-\boldsymbol X\boldsymbol\xi)^T\boldsymbol V^{-1}(\boldsymbol y-\boldsymbol X\boldsymbol\xi),\tag{6}
\]
where $|\boldsymbol V|$ is the determinant of $\boldsymbol V$.''',[4,5],[3,4,10],[r'l(\omega;\boldsymbol y)',r'\log|\boldsymbol V|'],'Original working Gaussian objective; it is used under a non-Gaussian true model as well.','Section 2 — Log-likelihood (6)')
add(10,'inverse',r'''To write down the inverse of $\boldsymbol V$, we define $\boldsymbol J_a^0=\boldsymbol I_a$ and $\boldsymbol J_a^1=\boldsymbol J_a$, so the dispersion matrix (3) is written as
\[
\boldsymbol V=\sigma_\alpha^2(\boldsymbol J_g^0\otimes\boldsymbol J_h^1\otimes\boldsymbol J_m^1)+\sigma_\beta^2(\boldsymbol J_g^1\otimes\boldsymbol J_h^0\otimes\boldsymbol J_m^1)+\sigma_\gamma^2(\boldsymbol J_g^0\otimes\boldsymbol J_h^0\otimes\boldsymbol J_m^1)+\sigma_e^2(\boldsymbol J_g^0\otimes\boldsymbol J_h^0\otimes\boldsymbol J_m^0).\tag{7}
\]
Following [26], we obtain the explicit expression
\[
\boldsymbol V^{-1}=\frac1{\lambda_0}(\boldsymbol I_g\otimes\boldsymbol I_h\otimes\boldsymbol C_m)+\frac1{\lambda_1}(\boldsymbol C_g\otimes\boldsymbol C_h\otimes\bar{\boldsymbol J}_m)+\frac1{\lambda_2}(\boldsymbol C_g\otimes\bar{\boldsymbol J}_h\otimes\bar{\boldsymbol J}_m)+\frac1{\lambda_3}(\bar{\boldsymbol J}_g\otimes\boldsymbol C_h\otimes\bar{\boldsymbol J}_m)+\frac1{\lambda_4}(\bar{\boldsymbol J}_g\otimes\bar{\boldsymbol J}_h\otimes\bar{\boldsymbol J}_m),
\]
where $\lambda_0=\sigma_e^2$, $\lambda_1=\sigma_e^2+m\sigma_\gamma^2$, $\lambda_2=\sigma_e^2+m\sigma_\gamma^2+hm\sigma_\alpha^2$, $\lambda_3=\sigma_e^2+m\sigma_\gamma^2+gm\sigma_\beta^2$, $\lambda_4=\sigma_e^2+m\sigma_\gamma^2+hm\sigma_\alpha^2+gm\sigma_\beta^2$, $\bar{\boldsymbol J}_a=\frac1a\boldsymbol J_a$ and $\boldsymbol C_a=\boldsymbol I_a-\bar{\boldsymbol J}_a$. The details are given in Appendix B.''',[5],[1,20],[r'\boldsymbol V^{-1}',r'\boldsymbol C_a'],'Original spectral decomposition of the balanced covariance inverse, available in the main text. Appendix derivation is excluded.','Section 2 — Dispersion inverse')
add(11,'estimating function',r'''To find the maximum likelihood estimator $\hat\omega$ of $\omega$, we differentiate (6) with respect to $\omega$ to obtain the estimating function $\psi(\omega)$ and then solve the estimating equation $\boldsymbol0_{[(p+5):1]}=\psi(\omega)$, where $\boldsymbol0_{[p:q]}$ is a $p\times q$ matrix of zeros. The derivation of the estimating function $\psi(\omega)$ is given in Supplementary Section S.2. Henceforth, to be concise and maintain clarity, the argument $\omega$ will be excluded from expressions when doing so does not affect the intended meaning or introduce ambiguity.''',[5],[3,9],[r'\psi(\omega)',r'\hat\omega'],'Original score defined by differentiating the working likelihood in the specified parameter order. Root existence does not imply a unique global maximizer.','Section 2 — Likelihood estimating function')
add(12,'Euclidean (Frobenius) norm',r'''Throughout the paper, we let $|\boldsymbol a|=(\boldsymbol a^T\boldsymbol a)^{1/2}$ and $\|\boldsymbol A\|=\{\operatorname{trace}(\boldsymbol A\boldsymbol A^T)\}^{1/2}$ denote the Euclidean (Frobenius) norm of the vector $\boldsymbol a$ and the matrix $\boldsymbol A$, respectively.''',[6],[],[r'|\boldsymbol a|',r'\|\boldsymbol A\|'],'Original vector and matrix norm conventions.','Section 2 — Norms')
add(13,'Condition A',r'''1. The model (4) holds with true parameter $\dot\omega$ inside the parameter space $\Omega$.
2. The number of factor A levels (rows) $g\to\infty$, the number of factor B levels (columns) $h\to\infty$ and the number of observations within each cell $m\to\infty$.
3. The random variables $\alpha_i$, $\beta_j$, $\gamma_{ij}$ and $e_{ijk}$ are independent and identically distributed and mutually independent. Moreover, there is a $\delta>0$, such that $\mathbb E|\alpha_1|^{4+\delta}<\infty$, $\mathbb E|\beta_1|^{4+\delta}<\infty$, $\mathbb E|\gamma_{11}|^{4+\delta}<\infty$ and $\mathbb E|e_{111}|^{4+\delta}<\infty$.
4. The limits $\lim_{g\to\infty}g^{-1}\sum_{i=1}^g\boldsymbol x_i^{(a)}=\bar{\boldsymbol x}^{(a)}$ and $\lim_{h\to\infty}\sum_{j=1}^h\boldsymbol x_j^{(b)}=\bar{\boldsymbol x}^{(b)}$ exist. Also, the limits of the matrices $\lim_{g\to\infty}g^{-1}\sum_{i=1}^g\boldsymbol X_{i(c)}^{(a)}\boldsymbol X_{i(c)}^{(a)T}$, $\lim_{h\to\infty}h^{-1}\sum_{j=1}^h\boldsymbol X_{j(c)}^{(b)}\boldsymbol X_{j(c)}^{(b)T}$, $\lim_{g,h\to\infty}(gh)^{-1}\sum_{i=1}^g\sum_{j=1}^h\boldsymbol X_{ij(c)}^{(ab)}\boldsymbol X_{ij(c)}^{(ab)T}$ and $\lim_{g,h,m\to\infty}n^{-1}\sum_{i=1}^g\sum_{j=1}^h\sum_{k=1}^m\boldsymbol x_{ijk(c)}^{(w)}\boldsymbol x_{ijk(c)}^{(w)T}$ exist and are positive definite. Additionally, there is a $\delta>0$, such that $\lim_{g\to\infty}g^{-1}\sum_{i=1}^g|\boldsymbol x_{i(c)}^{(a)}|^{2+\delta}<\infty$, $\lim_{h\to\infty}h^{-1}\sum_{j=1}^h|\boldsymbol x_{j(c)}^{(b)}|^{2+\delta}<\infty$, $\lim_{g,h\to\infty}(gh)^{-1}\sum_{i=1}^g\sum_{j=1}^h|\boldsymbol x_{ij(c)}^{(ab)}|^{2+\delta}<\infty$ and $\lim_{g,h,m\to\infty}n^{-1}\sum_{i=1}^g\sum_{j=1}^h\sum_{k=1}^m|\boldsymbol x_{ijk(c)}^{(w)}|^{2+\delta}<\infty$.''',[6,7],[1,2,3,6,7,12],[r'\Omega',r'4+\delta'],'All four original conditions, including increasing rows/columns/replication and enlarged Gram limits. Preserve the missing h inverse in the printed column-mean limit.','Condition A',kind='condition',context='Condition A',context_page=6,phrases=['Condition A'])
add(14,'diagonal matrix',STATEMENTS[0][STATEMENTS[0].index('where $\\boldsymbol K'):STATEMENTS[0].index(' Moreover,')],[7],[1,2], [r'\boldsymbol K'],'Original four-rate normalization in theorem parameter order; not a single root-n rate.','Theorem 1 — Rate matrix',kind='theorem_excerpt',context='Each of these rates requires a different normalization on the corresponding estimators; we achieve this using a diagonal matrix which is readily interpretable.',context_page=3)
# Keep the exact contiguous theorem fragments, including their internal definitions.
add(15,'influence functions',STATEMENTS[0][STATEMENTS[0].index('and $\\phi='):STATEMENTS[0].index('It follows that')],[7],[1,2,3,5,6],[r'\phi_{\xi_0}',r'\phi_{\boldsymbol\xi_4}'],'Original nine-component leading score vector in the asymptotic representation; retains cross-row/column contributions and variance centering.','Theorem 1 — Influence components (10)',kind='theorem_excerpt',context='We derive asymptotic representations for both the maximum likelihood and REML estimators in terms of their influence functions that are useful in their own right and for the development of the central limit theorem.',context_page=3)
add(16,'asymptotic variance matrix',STATEMENTS[0][STATEMENTS[0].index('where\n'):STATEMENTS[0].index(' The result for')],[8],[1,2,3,5,8],[r'\boldsymbol F_{1(a),(b)}',r'\boldsymbol F_3'],'Original full asymptotic covariance with skewness terms and ratio-dependent cross-block. The printed zero-block dimension remains unchanged.','Theorem 1 — Asymptotic covariance',kind='theorem_excerpt',context='The asymptotic variance matrix we obtain is elegantly structured with a block diagonal configuration, which is both concise and interpretable, and simplifies making asymptotic inferences for the unknown parameters.',context_page=3)
add(17,'derivative function',r'''where $\boldsymbol B=\lim_{g,h,m\to\infty}-\boldsymbol K^{-1/2}\mathbb E\nabla\psi(\dot\omega)\boldsymbol K^{-1/2}$
\[
\boldsymbol B=
\begin{bmatrix}
\boldsymbol B_{1(a),(a)}&\boldsymbol B_{1(a),(b)}&\boldsymbol0_{[(p_a+2):(p_{ab}+1)]}&\boldsymbol0_{[(p_a+2):(p_w+1)]}\\
\boldsymbol B_{1(b),(a)}&\boldsymbol B_{1(b),(b)}&\boldsymbol0_{[(p_b+1):(p_{ab}+1)]}&\boldsymbol0_{[(p_b+1):(p_w+1)]}\\
\boldsymbol0_{[(p_{ab}+1):(p_a+2)]}&\boldsymbol0_{[(p_{ab}+1):(p_b+1)]}&\boldsymbol B_2&\boldsymbol0_{[(p_{ab}+1):(p_w+1)]}\\
\boldsymbol0_{[(p_w+1):(p_a+2)]}&\boldsymbol0_{[(p_w+1):(p_b+1)]}&\boldsymbol0_{[(p_w+1):(p_{ab}+1)]}&\boldsymbol B_3
\end{bmatrix},\tag{13}
\]
with
\[
\boldsymbol B_{1(a),(a)}=1/\dot\tau\begin{bmatrix}
1&\bar{\boldsymbol x}^{(a)T}&0\\
\bar{\boldsymbol x}^{(a)}&\dot\tau\boldsymbol D_1/\dot\sigma_\alpha^2+\bar{\boldsymbol x}^{(a)}\bar{\boldsymbol x}^{(a)T}&\boldsymbol0_{[p_a:1]}\\
0&\boldsymbol0_{[1:p_a]}&\dot\tau/(2\dot\sigma_\alpha^4)
\end{bmatrix},\qquad
\boldsymbol B_{1(a),(b)}=\boldsymbol B_{1(b),(a)}^T=1/\dot\tau\begin{bmatrix}
\eta^{1/2}\bar{\boldsymbol x}^{(b)T}&0\\
\eta^{1/2}\bar{\boldsymbol x}^{(a)}\bar{\boldsymbol x}^{(b)T}&\boldsymbol0_{[p_a:1]}\\
\boldsymbol0_{[1:p_b]}&0
\end{bmatrix},
\]
\[
\boldsymbol B_{1(b),(b)}=\begin{bmatrix}
\boldsymbol D_2/\dot\sigma_\beta^2+\eta\bar{\boldsymbol x}^{(b)}\bar{\boldsymbol x}^{(b)T}/\dot\tau&\boldsymbol0_{[p_b:1]}\\
\boldsymbol0_{[1:p_b]}&1/(2\dot\sigma_\beta^4)
\end{bmatrix},\quad
\boldsymbol B_2=\begin{bmatrix}\boldsymbol D_3/\dot\sigma_\gamma^2&\boldsymbol0_{[p_{ab}:1]}\\\boldsymbol0_{[1:p_{ab}]}&1/(2\dot\sigma_\gamma^4)\end{bmatrix}
\]
and $\boldsymbol B_3=\begin{bmatrix}\boldsymbol D_4/\dot\sigma_e^2&\boldsymbol0_{[p_w:1]}\\\boldsymbol0_{[1:p_w]}&1(2\dot\sigma_e^4)\end{bmatrix}$.''',[14,19],[3,5,8,11,14],[r'\boldsymbol B_{1(a),(a)}',r'\boldsymbol B_3'],'Original normalized expected score derivative and explicit blocks in main-text Lemma 4. Preserve missing slash in final B3 entry; do not impose information equality under nonnormality.','Section 6.1 and Lemma 4 — Matrix (13)',kind='source_passage',context='6.4. Lemmas for the derivative function.',context_page=19)
add(18,'REML criterion function',r'''For REML estimation, group the regression parameters as $\boldsymbol\xi=[\xi_0,\boldsymbol\xi_1^T,\boldsymbol\xi_2^T,\boldsymbol\xi_3^T,\boldsymbol\xi_4^T]^T$ and the variance components as $\theta=[\sigma_\alpha^2,\sigma_\beta^2,\sigma_\gamma^2,\sigma_e^2]^T$. The REML criterion function is obtained by replacing the regression parameters $\boldsymbol\xi$ in the log-likelihood (6) by their maximum likelihood estimators for each $\theta$ and then modifying the resulting profile log-likelihood for $\theta$ to reduce the bias of the estimators. For each $\theta$, the estimating equations for $\boldsymbol\xi$ presented in (8) are solved by $\hat{\boldsymbol\xi}(\theta)=\{\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol X\}^{-1}\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol y$, and the REML criterion function is
\[
l_R(\theta;\boldsymbol y)=l(\hat{\boldsymbol\xi}(\theta),\theta;\boldsymbol y)-\frac12\log|\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol X|.
\]
The REML estimator $\hat\theta_R$ of $\dot\theta$ maximizes the REML criterion function $l_R(\theta;\boldsymbol y)$. We define $\hat{\boldsymbol\xi}_R=\hat{\boldsymbol\xi}(\hat\theta_R)$ to be the REML estimator of $\boldsymbol\xi$ and write the REML estimator of $\dot\omega$ as $\hat\omega_R=[\hat\xi_{R0},\hat{\boldsymbol\xi}_{R1}^T,\hat\sigma_{R\alpha}^2,\hat{\boldsymbol\xi}_{R2}^T,\hat\sigma_{R\beta}^2,\hat{\boldsymbol\xi}_{R3}^T,\hat\sigma_{R\gamma}^2,\hat{\boldsymbol\xi}_{R4}^T,\hat\sigma_{Re}^2]^T$.''',[9],[3,4,9,11,20],[r'l_R(\theta;\boldsymbol y)',r'\hat\omega_R'],'Original profiled working REML and parameter reassembly, distinct from the adjusted full-parameter score.','Section 3 — REML criterion and estimator')
add(19,'adjusted log-likelihood',r'''Since $\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol X$ is not a function of $\boldsymbol\xi$, the REML estimator also maximizes the adjusted log-likelihood
\[
l_A(\boldsymbol\xi,\theta;\boldsymbol y)=l(\omega;\boldsymbol y)-\frac12\log|\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol X|.
\]
According to [23], the REML estimator can be identified in a single step (rather than in two steps) by optimizing $l_A(\boldsymbol\xi,\theta;\boldsymbol y)$ directly. This means that the estimating function is represented by $\psi_A(\omega)$ using the derivatives $l_{A\xi_0}=l_{\xi_0}$, $l_{A\boldsymbol\xi_1}=l_{\boldsymbol\xi_1}$, $l_{A\boldsymbol\xi_2}=l_{\boldsymbol\xi_2}$, $l_{A\boldsymbol\xi_3}=l_{\boldsymbol\xi_3}$, $l_{A\boldsymbol\xi_4}=l_{\boldsymbol\xi_4}$ and
\[
\begin{aligned}
l_{A\sigma_\alpha^2}(\omega)&=l_{\sigma_\alpha^2}(\omega)-\frac12\operatorname{trace}\{(\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol X)^{-1}\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol Z_1\boldsymbol Z_1^T\boldsymbol V^{-1}\boldsymbol X\},\\
l_{A\sigma_\beta^2}(\omega)&=l_{\sigma_\beta^2}(\omega)-\frac12\operatorname{trace}\{(\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol X)^{-1}\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol Z_2\boldsymbol Z_2^T\boldsymbol V^{-1}\boldsymbol X\},\\
l_{A\sigma_\gamma^2}(\omega)&=l_{\sigma_\gamma^2}(\omega)-\frac12\operatorname{trace}\{(\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol X)^{-1}\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol Z_3\boldsymbol Z_3^T\boldsymbol V^{-1}\boldsymbol X\},\\
l_{A\sigma_e^2}(\omega)&=l_{\sigma_e^2}(\omega)-\frac12\operatorname{trace}\{(\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol X)^{-1}\boldsymbol X^T\boldsymbol V^{-1}\boldsymbol Z_0\boldsymbol Z_0^T\boldsymbol V^{-1}\boldsymbol X\}.
\end{aligned}
\]''',[9],[3,4,9,11,18,20],[r'\psi_A(\omega)',r'l_A(\boldsymbol\xi,\theta;\boldsymbol y)'],'Original adjusted likelihood and all four variance-score corrections. Preserve the printed minus signs; their derivative consistency is a separate source issue.','Section 3 — Adjusted likelihood and REML score')
add(20,'dispersion (variance-covariance) matrix',r'''where $\boldsymbol Z_0=\boldsymbol I_g\otimes\boldsymbol I_h\otimes\boldsymbol I_m$, $\boldsymbol Z_1=\boldsymbol I_g\otimes\boldsymbol1_h\otimes\boldsymbol1_m$, $\boldsymbol Z_2=\boldsymbol1_g\otimes\boldsymbol I_h\otimes\boldsymbol1_m$ and $\boldsymbol Z_3=\boldsymbol I_g\otimes\boldsymbol I_h\otimes\boldsymbol1_m$, with $\boldsymbol1_a$ the $a$-vector of ones, $\boldsymbol I_a$ a $a\times a$ identity matrix, and $\otimes$ representing the Kronecker product. The dispersion (variance-covariance) matrix of $\boldsymbol y$, denoted by $\boldsymbol V$, is given by
\[
\boldsymbol V=\boldsymbol Z_1\boldsymbol Z_1^T\sigma_\alpha^2+\boldsymbol Z_2\boldsymbol Z_2^T\sigma_\beta^2+\boldsymbol Z_3\boldsymbol Z_3^T\sigma_\gamma^2+\boldsymbol Z_0\boldsymbol Z_0^T\sigma_e^2,\tag{3}
\]
where $\boldsymbol Z_0\boldsymbol Z_0^T=\boldsymbol I_g\otimes\boldsymbol I_h\otimes\boldsymbol I_m$, $\boldsymbol Z_1\boldsymbol Z_1^T=\boldsymbol I_g\otimes\boldsymbol J_h\otimes\boldsymbol J_m$, $\boldsymbol Z_2\boldsymbol Z_2^T=\boldsymbol J_g\otimes\boldsymbol I_h\otimes\boldsymbol J_m$ and $\boldsymbol Z_3\boldsymbol Z_3^T=\boldsymbol I_g\otimes\boldsymbol I_h\otimes\boldsymbol J_m$, with $\boldsymbol J_a=\boldsymbol1_a\boldsymbol1_a^T$, a $a\times a$ matrix of ones.''',[2],[1],[r'\boldsymbol Z_1',r'\boldsymbol V'],'Original incidence and variance-component matrices for the balanced observation order.','Section 1 — Incidence and dispersion matrices')
def main():
    r=json.loads((REVIEW_ROOT/'inventory-review.json').read_text());assert r['status']=='complete' and r['source_checked']
    assert hashlib.sha256((ROOT/'theorem-inventory.json').read_bytes()).hexdigest()==r['inventory_sha256']
    assert len(interfaces)==len(members)==20
    for x in interfaces:
        m=x['members'][0];assert set(m['depends_on'])<=set(members)
        assert any(v in m['statement_original']+' '+m['local_label'] for v in m['highlight_symbols']+m['highlight_phrases'])
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
    print('Saved 20 source passages; independent full review is pending.')
if __name__=='__main__':main()
