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
add('D1','conditional expectation',r'''
Let $(y_1,\boldsymbol x_1^\top),\ldots,(y_n,\boldsymbol x_n^\top)$ be a random sample from a joint distribution $P_{(y,\boldsymbol x)}=P_{y\mid\boldsymbol x}P_{\boldsymbol x}$ supported on $\mathcal Y\times\mathcal X$. Here $\boldsymbol x=(x_1,\ldots,x_p)^\top$ is a vector of $p$ predictor variables supported on $\mathcal X\subseteq\mathbb R^p$ and $y$ is a real-valued outcome variable with range $\mathcal Y\subseteq\mathbb R$. Our objective is to compute an estimate of the conditional expectation, $\mu(\boldsymbol x)=\mathbb E[y\mid\boldsymbol x]$, a target which is optimal for predicting $y$ from some function of $\boldsymbol x$ in mean squared error.
''',[2],'Section 1.1 — random sample and conditional expectation',symbols=[r'\mu(\boldsymbol x)',r'P_{\boldsymbol x}'],phrases=['conditional expectation'],shape='Conditional mean function of a real response given a Euclidean covariate, together with the paper sample and support convention. The source says random sample; the usual i.i.d. reading is recorded separately.')
add('D2','sum-of-squares error',r'''
A decision tree is a hierarchically organized data structure constructed in a top down, greedy manner through recursive binary splitting. According to CART methodology (Breiman et al., 1984), a parent node $t$ (i.e., a region in $\mathcal X$) in the tree is divided into two child nodes, $t_L$ and $t_R$, by maximizing the decrease in sum-of-squares error (SSE)
\[
\widehat\Delta(b,\boldsymbol a,t)=\frac1n\sum_{\boldsymbol x_i\in t}(y_i-\overline y_t)^2-\frac1n\sum_{\boldsymbol x_i\in t}(y_i-\overline y_{t_L}\mathbf1(\boldsymbol a^\top\boldsymbol x_i\leq b)-\overline y_{t_R}\mathbf1(\boldsymbol a^\top\boldsymbol x_i>b))^2,\tag{1}
\]
with respect to $(b,\boldsymbol a)$, with $\mathbf1(\cdot)$ denoting the indicator function and $\overline y_t$ denoting the sample average of the $y_i$ data whose corresponding $\boldsymbol x_i$ data lies in the node $t$.
''',[2,3],'Section 1.1 — split criterion, equation (1)',{'D1':'The split criterion uses the response/covariate sample introduced in Section 1.1.'},symbols=[r'\widehat\Delta(b,\boldsymbol a,t)'],phrases=['sum-of-squares error'],shape='Sample-normalized reduction in within-node squared error for a hyperplane split, using the means on its two children. An empty-child convention is not supplied.')
add('D3','candidate directions',r'''
As mentioned earlier, it is challenging to find the direction $\widehat{\boldsymbol a}$ that optimizes $\widehat\Delta(b,\boldsymbol a,t)$. Many of the aforementioned computational papers address the problem by restricting the search space to a more tractable subset of candidate directions $\mathcal A_t$ with sparsity
\[
\sup\{\|\boldsymbol a\|_{\ell_0}:\boldsymbol a\in\mathcal A_t\}\leq d,
\]
for some positive integer $d$, where $\|\boldsymbol a\|_{\ell_0}$ counts the number of nonzero coordinates of $\boldsymbol a$. Because such search strategies are sometimes unlikely to find the global maximum, we theoretically measure their success by specifying a sub-optimality (slackness) parameter $\kappa\in(0,1]$ and considering the probability $P_{\mathcal A_t}(\kappa)$ that the maximum of $\widehat\Delta(b,\boldsymbol a,t)$ over $\boldsymbol a\in\mathcal A_t\subseteq\mathbb R^p$ is within a factor $\kappa$ of the maximum of $\widehat\Delta(b,\boldsymbol a,t)$ on the unrestricted parameter space, $\boldsymbol a\in\mathbb R^p$. That is, to theoretically quantify the sub-optimality of the chosen hyperplane, we measure
\[
P_{\mathcal A_t}(\kappa)=\mathbb P_{\mathcal A_t}\left(\max_{(b,\boldsymbol a)\in\mathbb R\times\mathcal A_t}\widehat\Delta(b,\boldsymbol a,t)\geq\kappa\max_{(b,\boldsymbol a)\in\mathbb R^{1+p}}\widehat\Delta(b,\boldsymbol a,t)\right),
\]
where $\mathbb P_{\mathcal A_t}$ denotes the probability with respect to the randomness in the search spaces $\mathcal A_t$, conditional on the data. The maximum of $\widehat\Delta(b,\boldsymbol a,t)$ over $(b,\boldsymbol a)$ is achieved because the number of distinct values of $\widehat\Delta(b,\boldsymbol a,t)$ is finite (at most the number of ways of dividing $n$ observations into two groups, or, $2^n-1$).
''',[7],'Section 2.2 — candidate directions and splitting probabilities',{'D2':'The success event compares the candidate-restricted and unrestricted maxima of split criterion (1).'},symbols=[r'P_{\mathcal A_t}(\kappa)',r'\mathcal A_t'],phrases=['candidate directions'],shape='Possibly random node-specific direction sets with sparsity bound d, and their conditional probability of achieving a kappa fraction of the unrestricted squared-error improvement. Does not impose Assumption 1.')
add('D4','maximal decision tree',r'''
The solution of (1) yields estimates $(\widehat b,\widehat{\boldsymbol a})$, and the refinement of $t$ produces child nodes $t_L=\{\boldsymbol x\in t:\widehat{\boldsymbol a}^\top\boldsymbol x\leq\widehat b\}$ and $t_R=\{\boldsymbol x\in t:\widehat{\boldsymbol a}^\top\boldsymbol x>\widehat b\}$. These child nodes become new parent nodes at the next level of the tree and can be further refined in the same manner until a desired depth is reached. To obtain a maximal decision tree $T_K$ of depth $K$, the procedure is iterated $K$ times or until either (i) the node contains a single data point $(y_i,\boldsymbol x_i^\top)$ or (ii) all input values $\boldsymbol x_i$ and/or all response values $y_i$ within the node are the same. The maximal decision tree with maximum depth is denoted by $T_{max}$.
''',[3],'Section 1.1 — recursive construction and stopping rule',{'D2':'Child nodes are formed from an optimizer of split criterion (1).','D3':'The theorem-wide convention on page 10 specifies that T_K is built using the node search spaces A_t of Section 2.2.'},symbols=[r'T_K',r'T_{max}'],phrases=['maximal decision tree'],shape='Recursive oblique hyperplane tree with depth cap K and the stated singleton/equal-input/equal-response stopping conditions, with the later computational framework restricting each split search. Tie and empty-child selection are not specified.')
members['D4']['application_context']=[dict(text=r'For the following statements, the output of a depth $K$ tree $T_K$ constructed with oblique CART methodology using the search spaces $\{\mathcal A_t:t\in[T]\}$ is denoted $\widehat\mu(T_K)$.',evidence=[dict(page=10,location='Section 2.4 — tree convention preceding Lemma 2')])]
add('D5','tree output',r'''
In a conventional regression problem, where the goal is to estimate the conditional mean response $\mu(\boldsymbol x)$, the canonical tree output for $\boldsymbol x\in t$ is $\overline y_t$, i.e., if $T$ is a decision tree, then
\[
\widehat\mu(T)(\boldsymbol x)=\overline y_t=\frac1{n(t)}\sum_{\boldsymbol x_i\in t}y_i,\tag{2}
\]
where $n(t)$ denotes the number of observations in the node $t$.
''',[3],'Section 1.1 — tree output, equation (2)',{'D1':'The node averages are computed from the observed response/covariate pairs.'},symbols=[r'\widehat\mu(T)',r'\overline y_t'],phrases=['tree output'],shape='Piecewise constant prediction from terminal-node sample means for a supplied tree. The definition does not require that the supplied tree was produced by a specific optimizer.')
add('D6','total variation',r'''
We define the total variation of a ridge function $\boldsymbol x\mapsto h(\boldsymbol a^\top\boldsymbol x)$ with $\boldsymbol a\in\mathbb R^p$ and $h:\mathbb R\to\mathbb R$ in the node $t$ as
\[
V(h,\boldsymbol a,t)=\sup_{\mathcal P}\sum_{\ell=0}^{|\mathcal P|-1}|h(z_{\ell+1})-h(z_\ell)|,
\]
where the supremum is over all partitions $\mathcal P=\{z_0,z_1,\ldots,z_{|\mathcal P|}\}$ of the interval $I(\boldsymbol a,t)=[\min_{\boldsymbol x\in t}\boldsymbol a^\top\boldsymbol x,\max_{\boldsymbol x\in t}\boldsymbol a^\top\boldsymbol x]\subset\mathbb R$ (we allow for the possibility that one or both of the endpoints is infinite). If the function $h$ is smooth, then $V(h,\boldsymbol a,t)$ admits the familiar integral representation $\int_{I(\boldsymbol a,t)}|h'(z)|dz$. We can then define the $\mathcal L_1$ norm of an additive function $h(\boldsymbol x)=\sum_{k=1}^Mh_k(\boldsymbol x)$ as
\[
\|h\|_{\mathcal L_1}=\sum_{k=1}^MV(h_k,\boldsymbol a_k,t).
\]
''',[6],'Section 2.1 — ridge variation and finite additive norm',symbols=[r'V(h,\boldsymbol a,t)',r'I(\boldsymbol a,t)'],phrases=['total variation'],shape='Variation on the scalar projection interval and the printed finite-expansion sum. Retains the source additive-function formula, its unbound directions, the suppressed node argument, and its partition indexing. These are recorded ambiguities, not repaired definitions.')
add('D7','ridge functions',r'''
To theoretically showcase these qualities and make comparisons with other procedures (such as neural networks and projection pursuit regression), we will consider modeling $\mu$ with finite linear combinations of ridge functions, i.e., the library
\[
\mathcal G=\left\{g(\boldsymbol x)=\sum_{k=1}^Mg_k(\boldsymbol a_k^\top\boldsymbol x),\ \boldsymbol a_k\in\mathbb R^p,\ g_k:\mathbb R\mapsto\mathbb R,\ k=1,\ldots,M,\ M\geq1,\ \|g\|_{\mathcal L_1}<\infty\right\},
\]
where $\|\cdot\|_{\mathcal L_1}$ is a total variation norm that is defined in Section 2.1.
''',[5],'Section 1.2 — finite ridge library',{'D6':'The finite library requires a finite total-variation sum for its ridge expansion, supplied by the finite additive-norm passage in Section 2.1. The source reuses this notation for the later relaxed norm; that ambiguity is documented separately.'},symbols=[r'\mathcal G',r'g_k(\boldsymbol a_k^\top\boldsymbol x)'],phrases=['ridge functions'],shape='Finite ridge-expansion library with finite total variation. Its finite-expansion norm is resolved to the preceding construction in Section 2.1; the later closure and relaxed norm are kept separate. Mentioning the regression target as motivation does not constrain the library by the data model.')
add('D8','total variation norm',r'''
Central to our results is the $\mathcal L_1$ total variation norm of $f\in\mathcal F=\operatorname{cl}(\mathcal G)$ in the node $t$, the closure being taken in $\mathcal L_2(P_{\boldsymbol x})$. This quantity captures the local capacity of a function in $\mathcal F$. It is defined as
\[
\|f\|_{\mathcal L_1(t)}:=\lim_{\varepsilon\downarrow0}\inf_{g\in\mathcal G}\left\{\sum_{k=1}^MV(g_k,\boldsymbol a_k,t):g(\boldsymbol x)=\sum_{k=1}^Mg_k(\boldsymbol a_k^\top\boldsymbol x),\ \|f-g\|\leq\varepsilon\right\}.
\]
For simplicity, we write $\|f\|_{\mathcal L_1}$ for $\|f\|_{\mathcal L_1(\mathcal X)}$. This norm may be thought of as an $\ell_1$ norm on the coefficients in a representation of the function $f$ by elements of a normalized dictionary of ridge functions.
''',[6],'Section 2.1 — library closure and local total variation norm',{'D7':'F is the L2 closure of the finite ridge library G, and the infimum ranges over that same library.','D6':'The infimum sums the ridge variations V(g_k,a_k,t) on the node projection interval.','D1':'The closure and approximation distance use the covariate marginal P_x fixed by the sampling model.'},symbols=[r'\mathcal F',r'\|f\|_{\mathcal L_1(t)}',r'\|f\|_{\mathcal L_1}'],phrases=['total variation norm'],shape='L2(P_x) closure of the finite ridge library, with relaxed local ridge-variation functional and its global shorthand. Closure membership and finite relaxed variation are not silently equated.')
add('D9','pruned subtree',r'''
We say that $T$ is a pruned subtree of $T'$ , written as $T\preceq T'$, if $T$ can be obtained from $T'$ by iteratively merging any number of its internal nodes. A pruned subtree of $T_{max}$ is defined as any binary subtree of $T_{max}$ having the same root node as $T_{max}$. Recall that the number of terminal nodes in a tree $T$ is denoted $|T|$. As shown in Breiman et al. (1984, Section 10.2), the smallest minimizing subtree for the penalty coefficient $\lambda=\lambda_n\geq0$,
\[
T_{opt}\in\operatorname*{argmin}_{T\preceq T_{max}}\left\{\|\boldsymbol y-\widehat{\boldsymbol\mu}(T)\|_n^2+\lambda|T|\right\},\tag{8}
\]
exists and is unique (smallest in the sense that if $T_{opt}$ optimizes the penalized risk of (8), then $T_{opt}\preceq T$ for every pruned subtree $T$ of $T_{max}$).
''',[11],'Section 2.5 — penalized pruning, equation (8)',{'D4':'The admissible pruned trees are rooted binary subtrees of the maximal tree T_max from the recursive construction.','D5':'The empirical loss in (8) uses terminal-node fitted values from tree output (2).'},symbols=[r'T_{opt}',r'\lambda_n'],phrases=['pruned subtree'],shape='Smallest penalized least-squares subtree of the fully grown tree, with penalty per terminal node. Preserve the printed smallest-subtree explanation, which does not restrict its comparison to minimizers.')
add('D10','Exponential tails of the conditional response variable',r'''
The conditional distribution of $y$ given $\boldsymbol x$ has exponentially decaying tails. That is, there exist positive constants $c_1,c_2,\gamma$, and $M$, such that for all $\boldsymbol x\in\mathcal X$,
\[
\mathbb P(|y|>B+M\mid\boldsymbol x)\leq c_1\exp(-c_2B^\gamma),\qquad B\geq0.
\]
''',[11],'Assumption 2 (Exponential tails of the conditional response variable)',{'D1':'The conditional distribution and covariate support are those of the observation model.'},kind='assumption',context='Assumption 2 (Exponential tails of the conditional response variable)',symbols=[r'c_1\exp(-c_2B^\gamma)'],phrases=['Assumption 2'],shape='Uniform conditional response-tail bound with positive constants c1,c2,gamma,M and all nonnegative thresholds B, on every covariate in X.')
add('D11','Aggregated ℓq variation',r'''
The regression function $\mu$ belongs to $\mathcal F$ and there exist positive numbers $V$ and $q>2$ such that, for any $K\geq1$,
\[
\mathbb E\left[\sum_{t\in T_K}\|\mu\|_{\mathcal L_1(t)}^q\right]\leq V^q.\tag{12}
\]
''',[14],'Assumption 3 (Aggregated ℓq variation)',{'D1':'Mu is the conditional expectation of the response given the covariate.','D8':'The assumption requires mu in F and bounds the qth powers of its relaxed local variation.','D4':'The sum is over terminal nodes of the data-adaptive depth-K tree.'},kind='assumption',context='Assumption 3 (Aggregated ℓq variation)',symbols=[r'\|\mu\|_{\mathcal L_1(t)}^q'],phrases=['Assumption 3'],shape='A single q greater than two and positive V bound the expected sum of local variation powers for every tree depth. The expectation includes data and split-search randomness.')
add('D12','Node size moment bound',r'''
Let $q>2$ be the positive number from Assumption 3. There exist positive numbers $A$ and $\nu\geq1+2/(q-2)$ such that, for any $K\geq1$,
\[
\left(\mathbb E\left[\left(\max_{t\in T_K}n(t)\right)^\nu\right]\right)^{1/\nu}\leq\frac{An}{2^K}.
\]
''',[15],'Assumption 4 (Node size moment bound)',{'D11':'The moment exponent threshold uses the same q fixed in Assumption 3.','D4':'The maximum is over terminal nodes of the depth-K tree, with n(t) their observed counts.'},kind='assumption',context='Assumption 4 (Node size moment bound)',symbols=[r'\max_{t\in T_K}n(t)'],phrases=['Assumption 4'],shape='Uniform-in-depth Lnu bound on the largest terminal-node sample count, with nu at least 1+2/(q-2). The literal all-K quantifier has a compatibility issue with finite-sample stopping, recorded separately.')
add('D13','random forest',r'''
A random forest is a randomized ensemble of trees. While traditional random forests use axis-aligned trees, it is also possible to work with oblique trees.
The randomization mechanism in a random forest affects the way each tree is constructed, and consists of two parts. The first part generates a subsample without replacement of size $N<n$ from the original training data, on which the tree is trained, and the second part generates a random collection of candidate splitting directions at each node, from which the optimal one is chosen (see the discussion under the purely random heading in Section 2 for generating $\mathcal A_t$).
Let $\Theta$ denote the random variable whose law governs the aforementioned randomization mechanism and let $T_K(\Theta)$ be the associated maximal tree of depth $K$. Let $\boldsymbol\Theta=(\Theta_1,\ldots,\Theta_B)^\top$ denote $B$ independent copies of $\Theta$, corresponding to $B$ trees $T_K(\Theta_b)$, for $b=1,\ldots,B$. The output of the random forest at a point $\boldsymbol x$ is obtained by averaging the predictions of all $B$ trees in the forest, viz.,
\[
\widehat\mu(\boldsymbol\Theta)(\boldsymbol x)=\frac1B\sum_{b=1}^B\widehat\mu(T_K(\Theta_b))(\boldsymbol x).
\]
''',[16],'Section 4 — oblique random forest construction',{'D4':'Each subsample is fitted with a maximal depth-K oblique tree.','D5':'The forest averages the terminal-node mean predictions of its B trees.','D3':'The second component of Theta randomizes the candidate splitting directions, over which the best split is selected.'},symbols=[r'\widehat\mu(\boldsymbol\Theta)',r'T_K(\Theta_b)'],phrases=['random forest'],shape='Average of B randomized oblique trees, each trained on a size-N subsample without replacement with randomized node candidate directions. Independent randomization copies share the original data.')
members['D13']['application_context']=[dict(text=r'It should be noted that the expectation in the second term of the bound in Theorem 5 is over the subsampled data (instead of over the entire data set as in Theorem 1).',evidence=[dict(page=17,location='After Theorem 5 — expectation convention')])]
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
    print('Saved',len(interfaces),'source-backed interfaces.')


if __name__ == '__main__':
    main()
