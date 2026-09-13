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
add('D1','high-dimensional linear model',r'''
In this work, we analyze sequential early stopping for an iterative boosting algorithm applied to data $Y=(Y_i)_{i\leq n}$ from a high-dimensional linear model
\[
Y_i=f^*(X_i)+\varepsilon_i=\sum_{j=1}^p\beta_j^*X_i^{(j)}+\varepsilon_i,\qquad i=1,\ldots,n,\tag{1.1}
\]
where $f^*(x)=\sum_{j=1}^p\beta_j^*x^{(j)}$, $x\in\mathbb R^p$, is a linear function of the columns of the design matrix, $\varepsilon:=(\varepsilon_i)_{i\leq n}$ is the vector of centered noise terms in our observations and the parameter size $p$ is potentially much larger than the sample size $n$.
''',[1],'Section 1 — linear observation model, equation (1.1)',kind='source_passage',phrases=['high-dimensional linear model'],symbols=[r'f^*(x)',r'\beta_j^*'],shape='Linear regression function and response decomposition with centered noise; independence, design rank and model-sequence conditions are recorded separately.')
add('D2','minimal assumptions',r'''
In order to state results for sequential early stopping of OMP in model (1.1), as minimal assumptions, we require that the rows $(X_i)_{i\leq n}$ of the design matrix $X=(X_i^{(j)})_{i\leq n,j\leq p}$ are independently and identically distributed such that $X$ has full rank $n$ almost surely. We also require that the noise terms $(\varepsilon_i)_{i\leq n}$ are independently and identically distributed and assume that, conditional on the design, a joint subgaussian parameter for the noise terms exists.
''',[3],'Section 1.1 — sampling and rank requirements',{'D1':'The rows and noise terms are the covariates and residuals of (1.1).'},kind='condition',phrases=['minimal assumptions','full rank'],shape='I.i.d. design rows with full row rank n almost surely and i.i.d. noise terms, with a common conditional subgaussian parameter. Does not silently strengthen the separately stated marginal independence into conditional independence of the complete noise vector.')
add('D3','centered subgaussians',r'''
Conditional on the design, the noise terms are centered subgaussians with a joint parameter $\overline\sigma^2>0$, i.e., for all $i\leq n$ and $u\in\mathbb R$,
\[
\mathbb E(e^{u\varepsilon_i}\mid X_i)\leq e^{u^2\overline\sigma^2/2}\qquad\text{almost surely}.
\]
Complementary to $\overline\sigma^2$, we set $\underline\sigma^2:=\operatorname{Var}(\varepsilon_1)$.
''',[3],'(A1) (SubGE)',{'D1':'The epsilon_i are the additive residuals in the observation model.'},kind='assumption',phrases=['(SubGE)','centered subgaussians'],symbols=[r'\overline\sigma^2',r'\underline\sigma^2'],shape='Uniform scalar conditional MGF bound with common positive variance proxy, and separate actual noise variance. The display conditions on X_i although the prose says the design.')
add('D4','orthogonal projection',r'''
By $\widehat\Pi_J:\mathbb R^n\to\mathbb R^n$, we denote the orthogonal projection with respect to $\langle\cdot,\cdot\rangle_n$ onto the span of the columns $\{X^{(j)}:j\in J\}$ of the design matrix.
''',[3],'Section 1.1 — empirical projection',{'D1':'The columns are those of the model design matrix X.'},phrases=['orthogonal projection'],symbols=[r'\widehat\Pi_J'],shape='Empirical-inner-product orthogonal projector onto the selected design columns. This geometric definition is valid without the erroneous transpose or inverse formula later printed in (1.26).')
add('D5','Orthogonal matching pursuit',r'''
1: $\widehat F^{(0)}\leftarrow0,\ \widehat J_0\leftarrow\varnothing$

2: for $m=0,1,2,\ldots$ do

3: $\widehat j_{m+1}\leftarrow\operatorname*{argmax}_{j\leq p}\left|\left\langle Y-\widehat F^{(m)},\frac{X^{(j)}}{\|X^{(j)}\|_n}\right\rangle_n\right|$

4: $\widehat J_{m+1}\leftarrow\widehat J_m\cup\{\widehat j_{m+1}\}$

5: $\widehat F^{(m+1)}\leftarrow\widehat\Pi_{\widehat J_{m+1}}Y$

6: end for
''',[4],'Algorithm 1 Orthogonal matching pursuit (OMP)',{'D1':'OMP uses the observed response vector and the design columns.','D4':'Every update is the empirical orthogonal projection onto the selected-column span.'},context='Algorithm 1 Orthogonal matching pursuit (OMP)',symbols=[r'\widehat F^{(0)}',r'\widehat F^{(m+1)}',r'\widehat J_m'],phrases=['Orthogonal matching pursuit'],shape='Iterative normalized-residual-correlation variable selection followed by refitting on the selected span. The printed argmax includes all j<=p and leaves ties and zero column norms unspecified.')
add('D6','squared empirical residual norm',r'''
\[
r_m^2:=\|Y-\widehat F^{(m)}\|_n^2,\qquad m\geq0,\tag{1.2}
\]
where, at iteration $m$, $\widehat F^{(m)}$ is the OMP-estimator of $f^*$ and $r_m^2$ is the squared empirical residual norm.
''',[2],'Equation (1.2) — residual norm definition',{'D5':'The residual subtracts the mth OMP fitted vector from the responses.'},phrases=['squared empirical residual norm'],symbols=[r'r_m^2'],shape='Empirical squared residual of each OMP iterate. Only the residual-definition fragment of (1.2) is used here; its introductory fixed-threshold stopping time is superseded by (1.8).')
add('D7','sequential early stopping time',r'''
where $C_\tau\geq0$ is a non-negative constant. Since the empirical noise level $\|\varepsilon\|_n^2$ is unknown, it has to be replaced by an estimator $\widehat\sigma^2$ and we redefine
\[
\tau:=\inf\{m\geq0:r_m^2\leq\kappa_m\}\quad\text{with}\quad\kappa_m:=\widehat\sigma^2+\frac{C_\tau m\log p}n,\qquad m\geq0.\tag{1.8}
\]
''',[4],'Section 1.1 — estimated-noise stopping rule, equation (1.8)',{'D6':'The rule stops when the squared residual norm r_m^2 reaches its iteration-dependent threshold.'},context=r'Our analysis in Section 2 shows that in order to derive such an adaptation result for the sequential early stopping time $\tau$ in Equation (1.2), ideally, the critical value $\kappa$ should be chosen depending on the iteration as',phrases=[],symbols=[r'\kappa_m',r'\widehat\sigma^2'],shape='First nonnegative integer iteration with residual below an estimated empirical-noise level plus a linear-in-iteration penalty. The noise estimate is an input whose accuracy is specified separately by each theorem.')
add('D8','ideal oracle iteration',r'''
\[
m^o=m^o(f^*):=\operatorname*{argmin}_{m\geq0}\|\widehat F^{(m)}-f^*\|_n^2.\tag{1.6}
\]
''',[4],'Section 1.1 — ideal oracle iteration, equation (1.6)',{'D5':'The oracle minimizes the empirical error along the OMP path.','D1':'The target is the true linear signal f* in model (1.1).'},context='the ideal oracle iteration',symbols=[r'm^o'],shape='Classical empirical-risk minimizing OMP iteration, distinct from the balanced oracle used in the proof. No tie-breaking rule is supplied.')
add('D9','sparsity of the coefficients',r'''
We assume one of the two following assumptions holds.

(i) $\beta^*$ is $s$-sparse for some $s\in\mathbb N_0$, i.e., $\|\beta^*\|_0\leq s$, where $\|\beta^*\|_0$ is the cardinality of the support $S:=\{j\leq p:|\beta_j^*|\neq0\}$. Additionally, we require that
\[
s\|\beta^*\|_1^2=s\left(\sum_{j=1}^p|\beta_j^*|\right)^2=o\left(\frac n{\log p}\right),\qquad\|f^*\|_{L^2}^2\leq C_{f^*}\quad\text{and}\quad\min_{j\in S}|\beta_j^*|\geq\underline\beta,
\]
where $C_{f^*},\underline\beta>0$ are numerical constants.

(ii) $\beta^*$ is $\gamma$-sparse for some $\gamma\in[1,\infty)$, i.e., $\|\beta^*\|_2\leq C_{\ell^2}$ and
\[
\sum_{j\in J}|\beta_j^*|\leq C_\gamma\left(\sum_{j\in J}|\beta_j^*|^2\right)^{\frac{\gamma-1}{2\gamma-1}}\quad\text{for all }J\subset\{1,\ldots,p\},
\]
where $C_{\ell^2},C_\gamma>0$ are numerical constants.
''',[5,6],'(A2) (Sparse)',{'D1':'The sparsity alternatives constrain beta* and its linear signal f* from (1.1).','D17':'The little-o condition in the s-sparse branch is along the paper-wide model sequence.'},kind='assumption',context=r'We quantify the sparsity of the coefficients $\beta^*$ of $f^*$:',phrases=['(Sparse)'],symbols=[r'\underline\beta',r'\|\beta^*\|_2'],shape='Disjunction of exact-support sparsity with growth, signal-size and beta-min conditions, or the uniform subset coefficient-decay condition with bounded ell2 norm. The same chosen branch must govern all rate and iteration definitions.')
members['D9']['naming_context'][0]['evidence']=[dict(page=5,location='Immediately before (A2) (Sparse)')]
add('D10','design variables',r'''
The design variables are centered subgaussians in $\mathbb R^p$ with unit variance, i.e., there exists some $\rho>0$ such that for all $x\in\mathbb R^p$ with $\|x\|=1$,
\[
\mathbb Ee^{u\langle x,X_1\rangle}\leq e^{u^2\rho^2/2},\quad u\in\mathbb R\quad\text{and}\quad\operatorname{Var}(X_1^{(j)})=1\quad\text{for all }j\leq p.
\]
''',[6],'(A3) (SubGD)',{'D1':'The random vector X_1 is one covariate observation in (1.1).'},kind='assumption',phrases=['(SubGD)'],symbols=[r'\rho',r'\operatorname{Var}(X_1^{(j)})=1'],shape='Uniform subgaussian MGF bound over unit Euclidean directions and unit marginal coordinate variances. Coordinates need not be independent.')
add('D11','covariance matrix',r'''
The complete covariance matrix $\Gamma:=\operatorname{Cov}(X_1)$ of one design observation is bounded from below, i.e., there exists some $c_\lambda>0$ such that the smallest eigenvalue of $\Gamma$ satisfies
\[
\lambda_{min}(\Gamma)\geq c_\lambda>0.\tag{1.12}
\]
Further, we assume that there exists $C_{Cov}>0$ such that the partial population covariance matrices $\Gamma_J:=(\Gamma_{jk})_{j,k\in J}$, for $J\subset\{1,\ldots,p\}$, satisfy
\[
\sup_{|J|\leq M_n,k\notin J}\|\Gamma_J^{-1}v_k\|_1<C_{Cov}\tag{1.13}
\]
with $M_n:=\sqrt{n/((\overline\sigma^2+\rho^4)\log p)}$, where $v_k:=(\operatorname{Cov}(X_1^{(k)},X_1^{(j)}))_{j\in J}\in\mathbb R^{|J|}$ is the vector of covariances between the $k$-th covariate and the covariates from the set $J$.
''',[6],'(A4) (CovB)',{'D1':'Gamma and v_k are covariances of the model covariates.','D3':'The cutoff M_n contains the noise proxy bar-sigma squared from (SubGE).','D10':'The same cutoff uses the design MGF parameter rho from (SubGD).'},kind='assumption',phrases=['(CovB)'],symbols=[r'\lambda_{min}(\Gamma)',r'\|\Gamma_J^{-1}v_k\|_1',r'M_n'],shape='Positive lower eigenvalue bound and a uniform ell1 bound on subset regression coefficients up to M_n. Retain the strict inequality in (1.13), despite the later weak-inequality restatement.')
add('D12','orthogonal projection',r'''
Assuming that all of the covariates are square-integrable, for $J\subset\{1,\ldots,p\}$, let $\Pi_J:L^2(P_{X_1})\to L^2(P_{X_1})$ denote the orthogonal projection with respect to $\langle\cdot,\cdot\rangle_{L^2}$ onto the span of the covariates $\{X_1^{(j)}:j\in J\}$. Setting $\Pi_m:=\Pi_{\widehat J_m}$, the population risk decomposes into
\[
\|\widehat F^{(m)}-f^*\|_{L^2}^2=\|(I-\Pi_m)f^*\|_{L^2}^2+\|\widehat F^{(m)}-\Pi_mf^*\|_{L^2}^2=B_m^2+S_m,\tag{1.9}
\]
where $B_m^2:\ a=\|(I-\Pi_m)f^*\|_{L^2}^2$ is the squared population bias and $S_m:=\|\widehat F^{(m)}-\Pi_mf^*\|_{L^2}^2$ is the population stochastic error.
''',[5],'Section 1.2 — population projection and bias, equation (1.9)',{'D1':'The projection is in L2 of the covariate distribution, and the residual uses f*.','D5':'The iteration-indexed population projector uses the random selected set J-hat_m from OMP.'},phrases=['orthogonal projection'],symbols=[r'\Pi_J',r'\Pi_m',r'B_m^2'],shape='Population projection on a given coordinate subset and its OMP-indexed version; the geometric definition and bias are distinct from empirical fitted-value projection. Preserve the printed malformed assignment B_m^2 : a =.')
add('D13','rates',r'''
\[
\mathcal R(s,\gamma):=\begin{cases}
\displaystyle\frac{\overline\sigma^2s\log p}n,&\beta^*\text{ }s\text{-sparse},\\[3pt]
\displaystyle\left(\frac{(\overline\sigma^2+\rho^4)\log p}n\right)^{1-\frac1{2\gamma}},&\beta^*\text{ }\gamma\text{-sparse}.
\end{cases}\tag{1.20}
\]
''',[8],'Section 1.2 — rates, equation (1.20)',{'D9':'The two rate branches use the corresponding (Sparse) alternative and its parameter s or gamma.','D3':'Both branches contain the common conditional noise proxy bar-sigma squared.','D10':'The gamma-sparse branch additionally contains the design proxy rho to the fourth power.'},context='with the rates',symbols=[r'\mathcal R(s,\gamma)'],shape='Branch-indexed target rate. The display is not a single bivariate formula applicable to an arbitrary independent pair (s,gamma).')
add('D14','No stopping too early',r'''
The sequential procedure stops too early if the squared population bias $B_m^2=\|(I-\Pi_m)f^*\|_{L^2}^2$ has not reached the optimal rate of convergence yet, i.e., $\tau<\widetilde m_{s,\gamma,G}$, where
\[
\widetilde m_{s,\gamma,G}:=\begin{cases}
\inf\{m\geq0:S\subset\widehat J_m\},&\beta^*\text{ }s\text{-sparse},\\[3pt]
\displaystyle\inf\left\{m\geq0:\|(I-\Pi_m)f^*\|_{L^2}^2\leq G\left(\frac{(\overline\sigma^2+\rho^4)\log p}n\right)^{1-\frac1{2\gamma}}\right\},&\beta^*\text{ }\gamma\text{-sparse}
\end{cases}\tag{3.2}
\]
for any constant $G>0$.
''',[15],'Section 3.1 No stopping too early — iteration (3.2)',{'D9':'The s-sparse branch uses the support S and the gamma-sparse branch uses gamma from (Sparse).','D5':'Support coverage uses the selected coordinate sets J-hat_m.','D12':'The other branch tests the population projection residual (I-Pi_m)f*.','D3':'The threshold uses the noise proxy bar-sigma squared.','D10':'The threshold also uses the design proxy rho.'},context='3.1. No stopping too early',symbols=[r'\widetilde m_{s,\gamma,G}',r'B_m^2'],shape='First support-coverage iteration in the s-sparse case, or first population-bias threshold crossing in the gamma-sparse case, with G>0. The comparison to tau explains its role; its value is determined by the full OMP path.')
add('D15','high-dimensional Akaike-information criterion',r'''
Motivated by Blanchard et al. [3], we propose a two-step procedure combining early stopping with an additional model selection step based on the high-dimensional Akaike-information criterion
\[
\widehat m_{AIC}:=\operatorname*{argmin}_{m\geq0}\operatorname{AIC}(m)\quad\text{with}\quad\operatorname{AIC}(m):=r_m^2+\frac{C_{AIC}m\log p}n,\qquad m\geq0.\tag{5.5}
\]
This criterion slightly differs from the one introduced in Ing [12], which is necessary for our setting, see Remark 5.2.
''',[21,22],'Section 5.2 — additive Akaike criterion, equation (5.5)',{'D6':'AIC adds an iteration penalty to the squared OMP residual r_m^2.'},phrases=['high-dimensional Akaike-information criterion'],symbols=[r'\operatorname{AIC}(m)',r'C_{AIC}'],shape='Additive residual-plus-iteration-penalty criterion and its unrestricted minimizer. The original HDAIC multiplicative criterion is a different procedure and is not substituted here.')
add('D16','two-step procedure',r'''
In combination, we select the iteration
\[
\tau_{two\text{-}step}:=\operatorname*{argmin}_{m\leq\tau}\operatorname{AIC}(m)\quad\text{with}\quad\tau\text{ from Equation (1.8).}\tag{5.6}
\]
Since this only requires $\tau$ additional comparisons of $\operatorname{AIC}(m)$ for $m\leq\tau$, the two-step procedure has the same computational complexity as the estimator $\widehat F^{(\tau)}$.
''',[22],'Section 5.2 — two-step selection, equation (5.6)',{'D7':'The search is restricted to iterations up to the sequential stopping time (1.8).','D15':'The selected iteration minimizes the additive AIC from (5.5) on that prefix.'},phrases=['two-step procedure'],symbols=[r'\tau_{two\text{-}step}'],shape='Choose an AIC-minimizing iteration on the computed OMP prefix through tau. Nonnegative integer indexing is inherited from the algorithm; no tie convention is supplied.')
add('D17','sequence of models',r'''
For the asymptotic analysis, we assume that the observations stem from a sequence of models of the form (1.1), where $p=p(n)\to\infty$ and $\log(p(n))/n\to0$ for $n\to\infty$. We allow the quantities $X=X^{(n)}$, $\beta^*=(\beta^*)^{(n)}$ and $\varepsilon=\varepsilon^{(n)}$ to vary in $n$. For notational convenience, we keep this dependence implicit.
''',[3],'Section 1.1 — model-sequence convention',{'D1':'The sequence consists of linear observation models of the form (1.1).'},kind='condition',phrases=['sequence of models'],symbols=[r'p=p(n)\to\infty',r'\log(p(n))/n\to0'],shape='High-dimensional triangular model sequence with p diverging subexponentially in n. Design, coefficients and errors may change with sample size.')
(ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
(ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
print('Saved',len(interfaces),'source-backed interfaces.')
