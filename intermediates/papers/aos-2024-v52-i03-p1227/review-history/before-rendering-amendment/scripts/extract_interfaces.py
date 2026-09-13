"""Rebuild original main-text passages and local dependencies for locally simultaneous inference.

The saved data is manually transcribed; source audit is a separate stage.
"""
import json
from pathlib import Path
from save_inventory import PID

ROOT = Path(__file__).resolve().parents[1]
interfaces, members, edges = [], {}, {}


def add(lid, term, body, pages, heading, deps=None, *, kind='definition',
        symbols=(), phrases=(), context=None, context_pages=None, shape):
    evidence = [dict(page=p, location=heading) for p in pages]
    member = dict(paper_id=PID, local_id=lid, local_label=heading,
        source_heading=heading, source_kind=kind, statement_original=body.strip(),
        relation='exact', depends_on=list(deps or {}), evidence=evidence,
        highlight_symbols=list(symbols), highlight_phrases=list(phrases))
    keyword = dict(paper_id=PID, local_id=lid, source_text=term,
                   label=term[0].upper()+term[1:], kind='term')
    if term not in body:
        assert context and term in context, (lid, term)
        member['naming_context'] = [dict(context_id=lid+'/name', text=context,
            evidence=[dict(page=p, location=heading+' — naming context') for p in (context_pages or pages)])]
        keyword['context_id'] = lid+'/name'
    interfaces.append(dict(interface_id=PID+'/'+lid, rank_group='all', name=keyword['label'],
        lean_role='hypothesis' if kind in ('condition', 'assumption') else 'definition',
        type_shape=shape, semantic_boundary=shape, members=[member], source_keywords=[keyword],
        central_claim_uses=[], dependencies=[], theorem_explanations={}))
    members[lid] = member
    edges[lid] = deps or {}


add('D1', 'target estimands', r'''
We consider a possibly nonparametric family of distributions $\mathcal P$. For every distribution $P\in\mathcal P$, we have a family of possible target estimands indexed by $\gamma\in\Gamma$, $\{\theta_\gamma(P)\}_{\gamma\in\Gamma}$.
''', [7], 'Section 2.1 — distributions and target estimands', symbols=[r'\theta_\gamma(P)'], shape='A possibly nonparametric statistical model with an indexed family of targets. The target index set need not be finite. Theta without P suppresses its dependence on the underlying law.')
add('D2', 'data-dependent set of inferential targets', r'''
Selective inference studies the problem of doing inference on $\{\theta_\gamma:\gamma\in\widehat\Gamma(y)\}$ given data $y\sim P$, where $\widehat\Gamma(y)$ determines a data-dependent set of inferential targets. We will adopt the convention that $\widehat\Gamma\equiv\widehat\Gamma(y)$ when the argument $y$ is clear from the context. When there is a single selected target, we will denote it by $\hat\gamma\equiv\hat\gamma(y)$; in that case $\widehat\Gamma=\{\hat\gamma\}$.
''', [7], 'Section 2.1 — selected targets', {'D1':'The selection indexes the original family of estimands under P.'}, symbols=[r'\widehat\Gamma(y)'], shape='A set-valued selection rule applied to the same data as inference. Single-selection and set-selection notation remain distinguishable; measurability for possibly infinite target families is not elaborated in the source.')
add('D3', 'simultaneous confidence regions', r'''
To implement this idea, we assume that we can construct simultaneous confidence regions $C_{\gamma\cdot\Gamma'}$ for any desired subset $\Gamma'\subseteq\Gamma$, at any target error level $\alpha$. Formally, we have access to a family of confidence regions $\{C_{\gamma\cdot\Gamma'}\}_{\Gamma'\subseteq\Gamma}$ such that
\[
P\{\theta_\gamma\in C_{\gamma\cdot\Gamma'},\forall\gamma\in\Gamma'\}\ge1-\alpha,
\]
for all $\Gamma'\subseteq\Gamma$.
''', [8], 'Section 2.1 — simultaneous validity for fixed subsets', {'D1':'The confidence regions cover the indexed estimands under the model law.'}, kind='condition', symbols=[r"C_{\gamma\cdot\Gamma'}"], shape='Simultaneous coverage for each fixed admissible subset at every requested error level. This is not already a guarantee for arbitrary data-selected subsets. Alpha is suppressed in C by the source convention.')
add('D4', 'monotone', r'''
We say that the confidence regions $\{C_{\gamma\cdot\Gamma'}\}_{\Gamma'\subseteq\Gamma}$ are monotone if for all $\Gamma_1\subseteq\Gamma_2\subseteq\Gamma$ and $\gamma\in\Gamma_1$,
\[
C_{\gamma\cdot\Gamma_1}\subseteq C_{\gamma\cdot\Gamma_2}.
\]
''', [8], 'Assumption 1', {'D3':'The set-inclusion condition is imposed on the family of simultaneous confidence regions.'}, kind='assumption', symbols=[r'C_{\gamma\cdot\Gamma_1}\subseteq C_{\gamma\cdot\Gamma_2}'], shape='Pathwise monotonicity under inclusion of target sets at a fixed error level. This is distinct from nesting under error-level changes.')
add('D5', 'acceptance region', r'''
For every $P\in\mathcal P$, suppose that we can construct a set $A_\nu(P)$ that satisfies
\[
P\{y\in A_\nu(P)\}\ge1-\nu,
\]
for any pre-specified $\nu\in(0,1)$. In other words, $A_\nu(P)$ is the acceptance region of a valid test for the null hypothesis $H_P:y\sim P$ at level $1-\nu$.
''', [8], 'Section 2.2 — acceptance region', {'D1':'There is an acceptance set for every model distribution P.'}, kind='condition', symbols=[r'A_\nu(P)'], shape='The acceptance probability is at least 1-nu under each P. The prose calls the test level 1-nu; that wording is preserved alongside the actual probability inequality, without correcting it to nu.')
add('D6', 'plausible targets', r'''
We define the set of plausible targets under distribution $P$ to be:
\[
\Gamma_\nu(P):=\bigcup_{y'\in A_\nu(P)}\widehat\Gamma(y').
\]
Note that, unlike the realized selection $\widehat\Gamma(y)$, $\Gamma_\nu(P)$ is a fixed set of targets.
''', [8], 'Section 2.2 — plausible targets under a fixed distribution', {'D5':'The union ranges over the acceptance region for P.','D2':'Each possible observation contributes its selected target set.'}, symbols=[r'\Gamma_\nu(P)'], shape='Fixed distribution-indexed union over accepted observations; it is not the observed random augmentation.')
add('D7', 'confidence region for the true distribution', r'''
Finally, we define the inversion of $A_\nu(P)$, which gives a confidence region for the true distribution $P$:
\[
B_\nu(y)=\{P\in\mathcal P:y\in A_\nu(P)\}.
\]
''', [8], 'Section 2.2 — inverted acceptance region', {'D5':'Inversion retains the same family of acceptance sets.'}, symbols=[r'B_\nu(y)'], shape='Random set of plausible distributions obtained by inverting acceptance regions. It is not a parameter confidence interval unless a parametric specialization is made.')
add('D8', 'set of targets', r'''
Consider the set of targets
\[
\widehat\Gamma^+_\nu=\bigcup_{P'\in B_\nu(y)}\Gamma_\nu(P')=\bigcup_{P'\in B_\nu(y)}\bigcup_{y'\in A_\nu(P')}\widehat\Gamma(y').\tag{2}
\]
''', [9], 'Theorem 1 — augmented target set (2)', {'D7':'The outer union ranges over the inverted confidence region.','D6':'The inner target set is the fixed-distribution plausible target set.','D5':'The expanded union explicitly uses the acceptance regions.','D2':'The expanded expression uses the selection rule on alternative data.'}, kind='theorem_excerpt', symbols=[r'\widehat\Gamma^+_\nu'], shape='Original target-set construction explicitly reused by Theorem 2. Theorem 1 binds this set inline; storing it here does not create a second theorem or a proof dependency.')
add('D9', 'centered confidence intervals', r'''
We say that $\{C^\alpha_{\gamma\cdot\Gamma'}\}_{\gamma'\subseteq\Gamma}$ are centered confidence intervals if
\[
C^\alpha_{\gamma\cdot\Gamma'}=(\hat\theta_\gamma\pm q^\alpha_{\Gamma'}\cdot\hat\sigma_\gamma),
\]
for some estimator $\hat\theta_\gamma$ and standard error $\hat\sigma_\gamma$, where $q^\alpha_{\Gamma'}$ is chosen such that $P\{\theta_\gamma\in C^\alpha_{\gamma\cdot\Gamma'},\forall\gamma\in\Gamma'\}\ge1-\alpha$.
''', [10], 'Assumption 2', {'D3':'The common correction calibrates simultaneous coverage on the chosen subset.'}, kind='assumption', symbols=[r"q^\alpha_{\Gamma'}\cdot\hat\sigma_\gamma"], shape='Centered intervals with common subset correction and coordinate-specific center/standard error. The printed lowercase gamma-prime family index is retained. Positivity and zero-standard-error conventions are not explicitly supplied.')
add('D10', 'intervals valid simultaneously', r'''
We denote $C_\gamma(q):=(\hat\theta_\gamma\pm q\hat\sigma_\gamma)$; then, $C_{\gamma\cdot\Gamma'}=C_\gamma(q^\alpha_{\Gamma'})$ are intervals valid simultaneously over $\Gamma'$ at level $1-\alpha$. Without loss of generality we assume that $q^\alpha_{\Gamma'}$ is nonincreasing in $\alpha$.
''', [10], 'Section 2.2 — correction-indexed interval and error-level nesting', {'D9':'The center, standard error and calibrated correction come from Assumption 2.'}, symbols=[r'C_\gamma(q)', r"q^\alpha_{\Gamma'}"], shape='The interval map used in Theorem 2 and its stated monotonicity in alpha. This is not an assumed Gaussian quantile.')
add('D11', 'location family', r'''
We begin with the case where $\mathcal P$ is a parametric family; in particular, we take $\mathcal P=\{P_\mu\}_\mu$ to be a location family with location parameter $\mu\in\mathbb R^m$. In other words, $y=(y_1,\ldots,y_m)\sim P_\mu$ can be written as $y=\mu+Z$, where $Z=(Z_1,\ldots,Z_m)\sim P_0$. For simplicity of exposition we assume that the errors $Z_i$ have the same marginal symmetric zero-mean distribution $P_0^{(1)}$ (e.g., $P_0^{(1)}=N(0,\sigma^2)$), however generalizing beyond this setting is straightforward. We do not assume that the errors $Z_i$ are necessarily independent, i.e. that $P_0$ is a product distribution.
''', [11], 'Section 3.1 — location model for promising effects', kind='source_passage', symbols=[r'y=\mu+Z', r'P_0^{(1)}'], shape='Common symmetric zero-mean marginal errors with unrestricted joint dependence. Normality is an example, not a theorem assumption; dimension is m.')
add('D12', 'inference on the winner', r'''
Given data $y=(y_1,\ldots,y_m)\in\mathbb R^m$, the problem of inference on the winner asks for a confidence interval for the mean of the largest entry of $y$. Formally, if we let $\theta_\gamma=Ey_\gamma$ for all $\gamma\in[m]$, the goal is to do inference on $\theta_{\hat\gamma}$, where
\[
\hat\gamma=\operatorname*{argmax}_{\gamma\in[m]}y_\gamma.\tag{3}
\]
''', [11], 'Section 3 — winner selection (3)', symbols=[r'\hat\gamma=\operatorname*{argmax}'], shape='Single largest observed coordinate; tie breaking is not specified. Under the location model the target is mu_hat-gamma.')
add('D13', 'file-drawer problem', r'''
The file-drawer problem asks for a confidence region that simultaneously covers the means of all observations that exceed a critical threshold $T$. Formally, the region is required to cover $\{\theta_\gamma:\gamma\in\widehat\Gamma\}$, where
\[
\widehat\Gamma=\{\gamma\in[m]:y_\gamma\ge T\}.\tag{4}
\]
''', [11], 'Section 3 — threshold selection (4)', symbols=[r'y_\gamma\ge T'], shape='All coordinates at or above a fixed critical threshold, including equality. It is simultaneous over the selected coordinates, not a conditional guarantee for one coordinate.')
add('D14', 'quantile of the maximum absolute error', r'''
For an index set $\mathcal I\subseteq[m]$, we define
\[
q^\alpha(\mathcal I)=\inf\left\{q:P_0\left\{\max_{i\in\mathcal I}|Z_i|\le q\right\}\ge1-\alpha\right\}.
\]
In words, $q^\alpha(\mathcal I)$ is the $1-\alpha$ quantile of the maximum absolute error over indices in $\mathcal I$.
''', [11], 'Section 3.1 — subset maximum-error quantile', {'D11':'The quantile is taken under the joint zero-location error law P0.'}, symbols=[r'q^\alpha(\mathcal I)'], shape='Unstandardized maximum absolute error over a subset, retaining joint dependence. Not the standardized maximal z-statistic of Example 5. Empty-subset conventions are not supplied.')
add('D15', 'i.i.d. samples', r'''
For each of the $m$ candidates, we assume that we have $n$ i.i.d. observations that are bounded in $[0,1]$. More formally, we observe $n$ i.i.d. samples $y^{(1)},\ldots,y^{(n)}$ drawn from a distribution $P$ with $\operatorname{supp}(P)\subseteq[0,1]^m$. As before, we denote the $m$-dimensional vector of means by $\theta=Ey^{(1)}$.
''', [12], 'Section 3.2 — bounded vector observations', kind='source_passage', symbols=[r'\operatorname{supp}(P)\subseteq[0,1]^m', r'\theta=Ey^{(1)}'], shape='IID vector observations across sample index, with arbitrary dependence among coordinates. This is not the location-family model of Section 3.1.')
add('D16', 'inference on the winner', r'''
In the problem of inference on the winner, we would like to do inference on $\theta_{\hat\gamma}$, where
\[
\hat\gamma=\operatorname*{argmax}_{\gamma\in[m]}y_\gamma:=\operatorname*{argmax}_{\gamma\in[m]}\frac1n\sum_{j=1}^ny^{(j)}_\gamma.\tag{5}
\]
''', [12], 'Section 3.2 — winner of empirical means (5)', {'D15':'The coordinates being averaged are the bounded iid sample observations.'}, symbols=[r'\frac1n\sum_{j=1}^ny^{(j)}_\gamma'], shape='Winner of the coordinatewise empirical means; y_gamma now denotes an average, not one location-family observation. Ties remain unspecified.')
add('D17', 'file-drawer problem', r'''
In the file-drawer problem, we would like to do inference on $\{\theta_\gamma:\gamma\in\widehat\Gamma\}$, where
\[
\widehat\Gamma=\{\gamma\in[m]:y_\gamma\ge T\}:=\left\{\gamma\in[m]:\frac1n\sum_{j=1}^ny^{(j)}_\gamma\ge T\right\}.\tag{6}
\]
''', [12], 'Section 3.2 — thresholded empirical means (6)', {'D15':'The selection uses averages of the bounded vector observations.'}, symbols=[r'\frac1n\sum_{j=1}^ny^{(j)}_\gamma\ge T'], shape='All empirical means at or above the fixed threshold; an empty selected set is possible.')
add('D18', 'valid bound on the deviation', r'''
Let $w_n^\alpha$ be any valid bound on the deviation of the empirical average of $n$ i.i.d. random variables $X_1,\ldots,X_n\in[0,1]$ from their mean. Formally, $w_n^\alpha$ satisfies
\[
P\left\{EX_1\in\left(\frac1n\sum_{i=1}^nX_i\pm w_n^\alpha\right)\right\}\ge1-\alpha.
\]
''', [12], 'Section 3.2 — marginal mean deviation bound', symbols=[r'w_n^\alpha'], kind='condition', shape='Any valid deviation width for iid bounded scalar variables. The Hoeffding expression is only an example; Theorem 4 uses this bound at nu/m without requiring the final intervals to have the same form.')
add('D19', 'confidence region', r'''
Furthermore, for every $\gamma\in[m]$, we let $C_\gamma^\alpha$ be a confidence region for $\theta_\gamma$ valid at level $1-\alpha$.
''', [12], 'Section 3.2 — marginal confidence region', {'D15':'The target is the coordinate mean of the bounded vector distribution.'}, kind='condition', symbols=[r'C_\gamma^\alpha'], shape='Arbitrary marginally valid regions. Theorem 4 separately requires nesting as alpha decreases; the betting intervals mentioned for experiments are not mandatory.')
add('D20', 'fixed design matrix', r'''
To set up the problem, suppose that we have a fixed design matrix $X\in\mathbb R^{n\times d}$ and a corresponding vector of outcomes $y\in\mathbb R^n$, where $y\sim P_\mu$. We assume $P_\mu$ is a location family, that is, $y\sim P_\mu\Leftrightarrow y\overset d=\mu+Z$, where $Z\sim P_0$ has mean zero.
''', [13], 'Section 4 — fixed-design location model', kind='source_passage', symbols=[r'X\in\mathbb R^{n\times d}', r'Z\sim P_0'], shape='Fixed design and mean-zero n-dimensional error law. No common marginal symmetry or independence from the Section 3.1 model is imported. X_j denotes a design column in the later formulas.')
add('D21', 'contrasts', r'''
To state the result, for a set of contrasts $\mathcal V$, we define
\[
q^\alpha(\mathcal V)=\inf\left\{q:P_0\left\{\sup_{v\in\mathcal V}|v^\top Z|\le q\right\}\ge1-\alpha\right\},
\]
where $Z\sim P_0$.
''', [13,14], 'Section 4 — contrast quantile', {'D20':'The contrasts act on the n-dimensional error vector in the fixed-design model.'}, symbols=[r'q^\alpha(\mathcal V)', r'|v^\top Z|'], shape='Quantile of a supremum of absolute linear contrasts, used with design columns for the local model radius. It is not the index-subset quantile of Section 3.1 despite sharing q notation.')
add('D22', 'LASSO', r'''
Recall that the LASSO solves the following penalized regression problem:
\[
\hat\beta(y)=\operatorname*{argmin}_\beta\frac12\|y-X\beta\|_2^2+\lambda\|\beta\|_1,
\]
and selects $\widehat M=\{i\in[d]:\hat\beta(y)_i\ne0\}$. We will write $\hat\beta(y)\equiv\hat\beta$ when the argument is clear from the context.
''', [14], 'Section 4.1 — LASSO solution and selected support', {'D20':'The loss uses the fixed design and response vector.'}, symbols=[r'\hat\beta(y)', r'\lambda\|\beta\|_1'], shape='The original half-squared-error plus l1 penalty and nonzero-coordinate support. The main text does not supply a tie-breaking/uniqueness rule for nonunique LASSO solutions or explicitly restrict lambda in this display.')
add('D23', 'plausible models', r'''
More precisely, denoting $\mathcal B^\infty_\nu=\{y':\|X^\top y-X^\top y'\|_\infty\le2q^\nu(\{X_j\}_{j=1}^d)\}$ the relevant neighboring outcome vectors, the set of plausible models is $\widehat{\mathcal M}^+_\nu=\{\widehat M(y'):y'\in\mathcal B^\infty_\nu\}$. To simplify notation we will denote by $s_\nu=2q^\nu(\{X_j\}_{j=1}^d)$ the radius of $\mathcal B^\infty_\nu$.
''', [14], 'Section 4.1 — neighboring outcomes and plausible models', {'D22':'Each neighboring outcome is mapped to its selected LASSO support.','D21':'The radius is twice the contrast quantile over design columns.'}, symbols=[r'\mathcal B^\infty_\nu', r's_\nu=2q^\nu(\{X_j\}_{j=1}^d)'], shape='Closed neighborhood in the transformed statistic X^T y, with all models realizable there. In outcome space it may be an unbounded polyhedron, despite the source calling it a box.')
add('D24', 'polyhedron', r'''
Denoting by $\hat s=\operatorname{sign}(\hat\beta_{\widehat M})$ the signs of the selected variables in the LASSO solution, Lee et al. show that
\[
\{\widehat M=M,\hat s=s\}=\left\{\begin{pmatrix}A_0^+(M,s)\\A_0^-(M,s)\\A_1(M,s)\end{pmatrix}y<\begin{pmatrix}b_0^+(M,s)\\b_0^-(M,s)\\b_1(M,s)\end{pmatrix}\right\},
\]
for any fixed model-sign pair $(M,s)$, where
\[
\begin{aligned}
A_0^+(M,s)&=\frac1\lambda X_{M^c}^\top(I-\Pi_M),&b_0^+(M,s)&=\mathbf1-X_{M^c}^\top(X_M^\top)^+s;\\
A_0^-(M,s)&=-\frac1\lambda X_{M^c}^\top(I-\Pi_M),&b_0^-(M,s)&=\mathbf1+X_{M^c}^\top(X_M^\top)^+s;\\
A_1(M,s)&=-\operatorname{diag}(s)(X_M^\top X_M)^{-1}X_M^\top,&b_1(M,s)&=-\lambda\operatorname{diag}(s)(X_M^\top X_M)^{-1}s.
\end{aligned}
\]
Here, $\Pi_M:=X_M(X_M^\top X_M)^{-1}X_M^\top$. We will denote the polyhedron above by $P(M,s)$.
''', [15], 'Section 4.1 — model-sign polyhedron', {'D22':'The event is the selected support and signs of the original LASSO solution.'}, symbols=[r'P(M,s)', r'\Pi_M', r'A_0^+(M,s)'], shape='Complete main-text polyhedral representation with strict inequalities, original inverses and pseudoinverse. Rank, uniqueness, positivity of lambda and boundary conventions are not added; full rank is needed to interpret the displayed inverses.')
add('D25', 'model-sign pairs', r'''
We use $\mathcal B(M,s)$ to denote the set of model-sign pairs whose corresponding polyhedra neighbor, i.e. share a face with, $P(M,s)$.
''', [15], 'Section 4.1 — neighboring model-sign regions', {'D24':'Adjacency is defined by sharing a face of the model-sign polyhedra.'}, symbols=[r'\mathcal B(M,s)'], shape='The prose definition is adjacency of model-sign regions. ExactScreening subsequently restricts relevance to the local neighborhood; that distinction and open-polyhedron boundary convention are retained as unresolved source details.')
add('D26', 'Exact screening rules', r'''
The core idea of exact screening rules is to find the minimal representation of $P(M,s)\cap\mathcal B^\infty_\nu$. That is, the goal is to prune all redundant constraints coming from $P(M,s)$; the inequalities that remain are “active” and indicate that the variables corresponding to those constraints can enter or leave the model in one of the neighboring polyhedra. In Algorithm 3 in the Appendix we use a standard solution to finding a minimal polyhedral representation, which relies on solving one linear program for each constraint whose redundancy is being checked.
''', [15,16], 'Section 4.1 — exact screening, main-text description', {'D24':'Redundancy is tested for constraints of the model-sign polyhedron.','D23':'The intersection is restricted to the local outcome neighborhood.','D25':'Active faces indicate neighboring model-sign pairs.'}, context='Exact screening rules.', context_pages=[15], kind='source_passage', symbols=[r'P(M,s)\cap\mathcal B^\infty_\nu'], shape='Main-text specification of the exact-screening task. Algorithm 3 pseudocode is in the excluded appendix, so the subroutine is not reconstructed or claimed independently implemented.')
add('D27', 'locally linear', r'''
For all $y'\inP(M,s)$, the LASSO optimality conditions imply that the LASSO solution is locally linear, namely
\[
\hat\beta(y')=\beta_{(M,s)}(y'):=(X_M^\top X_M)^{-1}(X_M^\top y'-\lambda s).
\]
Note that, while $\beta_{(M,s)}(y')$ is equal to the LASSO solution for $y'\inP(M,s)$, it can be computed for $y'\notinP(M,s)$.
''', [16], 'Section 4.1 — local affine solution formula', {'D24':'The equality with the LASSO solution is restricted to the given model-sign region.','D22':'The original LASSO penalty and design determine the formula.'}, symbols=[r"\beta_{(M,s)}(y')"], shape='Restricted-coordinate affine formula, called locally linear by the source. The equality uses full beta notation despite the |M|-dimensional right side; no zero-extension or rank convention is silently inserted.')
add('D28', 'Safe exclusion', r'''
Fix a model-sign pair $(M,s)$. Let
\[
\mathcal I^-_{\mathrm{safe}}(M,s):=\left\{j\in M^c:|X_j^\top(y-X_M\beta_{(M,s)}(y))|<\lambda-s_\nu\big(1+\|X_j^\top X_M(X_M^\top X_M)^{-1}\|_1\big)\right\}.
\]
''', [16], 'Lemma 2 (Safe exclusion) — screening set', {'D27':'The residual is formed from the affine solution formula.','D23':'The margin uses the local-neighborhood radius s_nu.'}, context='Lemma 2 (Safe exclusion).', symbols=[r'\mathcal I^-_{\mathrm{safe}}(M,s)'], shape='Original excluded-variable screening set with strict less-than and row-vector l1 norm. The subsequent lemma conclusion is not a new inventoried theorem; the appendix implementation remains excluded.')
add('D29', 'Safe inclusion', r'''
Fix a model-sign pair $(M,s)$. Let
\[
\mathcal I^+_{\mathrm{safe}}(M,s)=\left\{j\in M:|\beta_{j\cdot(M,s)}(y)|>s_\nu\|e_{j\cdot(M,s)}^\top(X_M^\top X_M)^{-1}\|_1\right\}.
\]
''', [16], 'Lemma 3 (Safe inclusion) — screening set', {'D27':'The coefficient is a component of the local affine solution.','D23':'The inequality uses the neighborhood radius s_nu.'}, context='Lemma 3 (Safe inclusion).', symbols=[r'\mathcal I^+_{\mathrm{safe}}(M,s)'], shape='Original retained-variable screening set with strict greater-than and a row l1 norm. The canonical basis subscript carries the model-sign pair as printed; no unprinted equality case rule is added.')
add('D30', 'Locally simultaneous inference for the LASSO', r'''
input: design matrix $X$, outcome vector $y$, penalty $\lambda$, error level $\alpha$, parameter $\nu\in(0,\alpha)$

output: set of plausible models $\widehat{\mathcal M}^+_\nu$

Compute width of $\mathcal B^\infty_\nu$: $s_\nu=2q^\nu(\{X_j\}_{j=1}^d)$

Compute LASSO solution: $\hat\beta=\operatorname*{argmin}_\beta\frac12\|y-X\beta\|_2^2+\lambda\|\beta\|_1$

Let $\widehat M=\operatorname{supp}(\hat\beta)$, $\hat s=\operatorname{sign}(\hat\beta_{\widehat M})$

Initialize $\mathcal P_{\mathrm{todo}}\leftarrow\{(\widehat M,\hat s)\}$, $\mathcal P^+_\nu\leftarrow\emptyset$

while $\mathcal P_{\mathrm{todo}}\ne\emptyset$ do

Take any pair $(M,s)\in\mathcal P_{\mathrm{todo}}$

Update $(M,s)$ as visited: $\mathcal P_{\mathrm{todo}}\leftarrow\mathcal P_{\mathrm{todo}}\setminus\{(M,s)\}$, $\mathcal P^+_\nu\leftarrow\mathcal P^+_\nu\cup\{(M,s)\}$

$\mathcal I_{\mathrm{safe}}(M,s)\leftarrow\operatorname{SafeScreening}(X,y,(M,s))$ (Alg. 2)

$\mathcal B(M,s)\leftarrow\operatorname{ExactScreening}(X,y,(M,s),\mathcal I_{\mathrm{safe}}(M,s))$ (Alg. 3)

$\mathcal P_{\mathrm{todo}}\leftarrow\mathcal P_{\mathrm{todo}}\cup(\mathcal B(M,s)\setminus\mathcal P^+_\nu)$

end

Return $\widehat{\mathcal M}^+_\nu=\{M:\exists s\text{ s.t. }(M,s)\in\mathcal P^+_\nu\}$
''', [16], 'Algorithm 1 — Locally simultaneous inference for the LASSO', {'D22':'The starting model and signs are computed from the original LASSO problem.','D23':'The search radius and target model set use the local outcome neighborhood.','D25':'The queue traverses neighboring model-sign pairs.','D26':'ExactScreening is described by the minimal-representation task in the main text.','D28':'The main text links safe screening to the safe-exclusion criterion.','D29':'The main text also links safe screening to the safe-inclusion criterion.'}, context='Algorithm 1 Locally simultaneous inference for the LASSO', symbols=[r'\operatorname{SafeScreening}', r'\operatorname{ExactScreening}', r'\mathcal P_{\mathrm{todo}}'], shape='Entire main-text Algorithm 1, including both appendix subroutine calls. The subroutines are intentionally unresolved beyond their main-text descriptions; this census neither imports appendix algorithms nor asserts that the traversal has been executed.')
add('D31', 'empirical risk minimizer', r'''
To set the problem up formally, suppose we have a dataset $\mathcal D=\{z_i\}_{i=1}^n\sim P^n$, which should typically be thought of as consisting of feature–outcome pairs. We are interested in the empirical risk minimizer on this dataset within a hypothesis class $\mathcal F$:
\[
\hat f=\operatorname*{argmin}_{f\in\mathcal F}R_n(f,\mathcal D):=\operatorname*{argmin}_{f\in\mathcal F}\frac1n\sum_{i=1}^n\ell(f,z_i),
\]
where $\ell(f,z)$ measures the loss incurred by predicting on point $z$ using hypothesis $f$ (for example, if $z=(x,y)$ is a feature–outcome pair, we could have $\ell(z,f)=1\{y\ne f(x)\}$).
''', [17], 'Section 5 — iid data, empirical risk and minimizer', symbols=[r'\mathcal D=\{z_i\}_{i=1}^n\sim P^n', r'\hat f', r'R_n(f,\mathcal D)'], shape='IID sample and empirical loss minimization over a fixed hypothesis class. The source example reverses the loss arguments; that typo is retained. Theorem 6 allows signed losses with absolute value at most one, not only binary or nonnegative loss.')
add('D32', 'population risk', r'''
For a fixed hypothesis $f\in\mathcal F$, we define its population risk as:
\[
R(f,P)=E_{z\sim P}\ell(f,z).
\]
''', [17], 'Section 5 — population risk', {'D31':'The expectation uses the same loss, hypothesis class and data-generating law as the empirical risk.'}, symbols=[r'R(f,P)'], shape='Expectation for a fixed hypothesis; at the fitted hypothesis it is a random quantity depending on training data, with a fresh P-distributed evaluation point.')
add('D33', 'generalization gap', r'''
In the following we let $\operatorname{Gap}_n(\mathcal F)$ denote any valid upper bound on $E\sup_{f\in\mathcal F}|R(f,P)-R_n(f,\mathcal D)|$. Such a bound typically follows from a complexity argument.
''', [17], 'Section 5 — expected generalization-gap bound', {'D31':'The empirical risks and outer expectation use the iid dataset.','D32':'The discrepancy compares empirical with population risk.'}, context=r'Therefore, it suffices to bound the so-called generalization gap, $\sup_{f\in\mathcal F}|R(f,P)-R_n(f,\mathcal D)|$, to get a valid upper bound on $R(\hat f,P)$.', symbols=[r'\operatorname{Gap}_n(\mathcal F)'], shape='Any upper-bound functional for the expected uniform generalization gap. Twice Rademacher complexity is an example, not its definition. The bound is later applied to a random subclass; monotonicity and how to evaluate it there are not explicitly stated in this definition.')


def main():
    for lid, member in members.items():
        assert all(d in members for d in member['depends_on']), lid
        own=member['statement_original']+' '+member['local_label']
        assert any(s in own for s in member['highlight_symbols']+member['highlight_phrases']), lid
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,
        status='extracted_pending_source_audit',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source passages; full census audit remains pending.')


if __name__=='__main__':
    main()

