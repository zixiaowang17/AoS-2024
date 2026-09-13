"""Transcribe statement prerequisites from the inspected published PDF, without supplements."""
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
        lean_role='hypothesis' if kind=='condition' else 'definition',type_shape=shape,semantic_boundary=shape,
        members=[m],source_keywords=keywords,central_claim_uses=[],dependencies=[],theorem_explanations={}))
    members[lid]=m;edges[lid]=deps or {}

add('D1','linear model',r'''
Suppose that the true linear model with $K_0$ groups of non-zero coefficients takes the form:
\[
Y=\sum_{j=1}^p\beta_j^*X_j+\sum_{k=1}^q\alpha_k^*Z_k+\varepsilon,\quad\beta_j^*\in\{0,\gamma_1^*,\gamma_2^*,\ldots,\gamma_{K_0}^*\},\ \forall j\in[p],\tag{1.1}
\]
where $\varepsilon\sim\mathcal N(0,\sigma^2)$, and where the coefficients $\{\beta_j^*\}_{j=1}^p$ belong to a set including 0 and $K_0$ unknown different nonzero values $\{\gamma_k^*\}_{k=1}^{K_0}$. Note that the group membership of each nonzero $\beta_j$ is not observed in data collection. Write $\alpha^*=(\alpha_1^*,\ldots,\alpha_q^*)^\top\in\mathbb R^q$, $\beta^*=(\beta_1^*,\ldots,\beta_p^*)^\top\in\mathbb R^p$ and $\gamma^*=(\gamma_1^*,\ldots,\gamma_{K_0}^*)^\top\in\mathbb R^{K_0}$. Our main goal in this paper is to estimate $\gamma^*$, $\beta^*$ and $\alpha^*$ simultaneously based on an independent and identically distributed (i.i.d.) sample $\{(\mathbf x_i,\mathbf z_i,y_i)\}_{i=1}^n$ of size $n$. In the case of high dimension, $\beta$ is often assumed sparse so that we perform feature selection and grouping simultaneously to ensure statistical consistency.
''',[2],'Section 1 — linear model, equation (1.1)',kind='source_passage',phrases=['linear model'],symbols=[r'\sigma^2'],shape='Gaussian-error regression with grouped beta coefficients and unrestricted nuisance alpha, using n iid observations. Preserve the error-law statement without inventing additional design assumptions.')
add('D2','parameter space',r'''
Define the parameter space $\Theta(K,s):=\{\theta=(\beta^\top,\alpha^\top)^\top\in\mathbb R^{p+q}\mid\gamma\in\mathbb R^K,\beta_j\in\{0,\gamma_1,\ldots,\gamma_K\},\forall j\in[p],\|\beta\|_0\leq s\}$.
''',[5],'Section 2.3 — parameter space Theta(K,s)',phrases=['parameter space'],symbols=[r'\Theta(K,s)'],shape='Grouped/sparse coefficient vectors with at most K nonzero values and at most s nonzero beta coordinates; alpha is unrestricted. The gamma witness is implicit in the printed set-builder syntax.')
add('D3',['index operator','grouping operator'],r'''
Denote the index operator for the elements of $\beta$ with value $r$ by $\mathcal G(\beta;r)=\{j\in[p]\mid\beta_j=r\}$ and the grouping operator by $\mathbb G(\beta)=\{\mathcal G(\beta;r)\mid r\neq0,\mathcal G(\beta;r)\neq\varnothing\}$. Let $|\mathcal G(\beta;r)|$ and $|\mathbb G(\beta)|$ be the cardinality of $\mathcal G(\beta;r)$ and $\mathbb G(\beta)$, respectively.
''',[5],'Section 2.3 — index operator and grouping operator',phrases=['index operator','grouping operator'],symbols=[r'\mathbb G(\beta)',r'\mathcal G(\beta;r)'],shape='Coordinate classes by exact coefficient equality; the grouping operator excludes the zero-valued and empty classes, while the index operator also permits r=0.')
add('D4','Distance between groupings',r'''
Let $\mathcal F(\beta,\beta'):=\{f\text{ is injective}:\mathbb G(\beta)\to\mathbb G(\beta')\}$. Then for any $\beta,\beta'$ such that $|\mathbb G(\beta)|\leq|\mathbb G(\beta')|$, define
\[
d(\beta,\beta'):=\min_{f\in\mathcal F(\beta,\beta')}\left|\bigcup_{\mathcal G_2\in\mathbb G(\beta')}\left\{\mathcal G_2\setminus\bigcup_{\mathcal G_1\in\mathbb G(\beta)}\{\mathcal G_1\cap f(\mathcal G_1)\}\right\}\right|.\tag{2.2}
\]
''',[5],'Definition 2.1 (Distance between groupings)',{'D3':'The injections and inconsistent-coordinate sets are formed from the nonzero coefficient groups.'},context='Distance between groupings',phrases=['Definition 2.1'],symbols=[r'\mathcal F'],shape='Minimum unmatched-coordinate count over injective nonzero-group matchings, defined when the first grouping has no more groups than the second. Do not symmetrize or add zero groups.')
add('D5','Grouping sensitivity',r'''
\[
c_{\min}\equiv c_{\min}(\theta^*,\mathbf X,\mathbf Z)=\min_{\substack{\theta\in\Theta(|\mathbb G(\beta^*)|,\|\beta^*\|_0)\\\mathbb G(\beta)\neq\mathbb G(\beta^*)}}\frac{\|\mathbf X(\beta-\beta^*)+\mathbf Z(\alpha-\alpha^*)\|_2^2}{n\max(d(\beta,\beta^*),1)},\tag{2.3}
\]
where $\theta^*=(\beta^{*\top},\alpha^{*\top})^\top\in\mathbb R^{p+q}$.
''',[5],'Definition 2.2 (Grouping sensitivity)',{'D2':'Competing vectors have the true group-count and support-size upper bounds.','D3':'Only competitors with a different nonzero grouping are admitted.','D4':'The denominator is the grouping discrepancy, floored at one.'},context='Grouping sensitivity',phrases=['Definition 2.2'],symbols=[r'c_{\min}'],shape='Design-dependent minimal prediction separation per grouping error. X and Z are fixed matrix arguments; the scalar Gaussian noise distribution is not a prerequisite of this definition.')
add('D6','L0-Fusion',r'''
Suppose we have $n$ independent observations $(\mathbf x_i,\mathbf z_i,y_i)_{i\in[n]}$ from model (1.1). Our paper revolves around the following combinatorial optimization problem to achieve feature selection and homogeneity fusion simultaneously:
\[
\begin{aligned}
\min_{\alpha\in\mathbb R^q,\beta\in\mathbb R^p,\gamma\in\mathbb R^K}\ &\sum_{i=1}^n(y_i-\mathbf x_i^\top\beta-\mathbf z_i^\top\alpha)^2,\\
\text{subject to:}\quad&\beta_j\in\{0,\gamma_1,\gamma_2,\ldots,\gamma_K\},\forall j\in[p],\\
&\|\beta\|_0:=\sum_{j=1}^p I(\beta_j\neq0)\leq s.
\end{aligned}\tag{2.1}
\]
The first constraint requires the non-zero group number to be bounded by $K$, and the second constraint requires the sparsity of $\beta$ to be bounded by $s$. Given that the problem above restricts the $\ell_0$-norm of $\beta$ and also fuses the components of $\beta$, we refer to it as the $L_0$-Fusion problem.
''',[3,4],'Section 2.2 — L0-Fusion, equation (2.1)',{'D1':'The response and covariates are sampled from the regression model.','D2':'The constraints define the grouped/sparse coefficient class.'},context='L0-Fusion',symbols=[r'\|\beta\|_0'],shape='Global least-squares minimization with upper bounds on group count and beta support size, not a prescribed mixed-integer implementation or preliminary screening algorithm.')
members['D6']['naming_context'][0]['text']='L0-Fusion'
members['D6']['naming_context'][0]['typesetting_note']='Source term is L_0-Fusion, with 0 as a subscript; only this typesetting is normalized in the name.'
members['D6']['invocation_context_original']=[dict(text=r'Denote the solution of the $L_0$-Fusion problem (2.1) by $\widehat\theta^{\mathrm g}=(\widehat\beta^{\mathrm g\top},\widehat\alpha^{\mathrm g\top})^\top$.',evidence=[dict(page=6,location='Paragraph preceding Theorem 2.4')])]
add('D7','groupwise collapsed matrix',r'''
Given a grouping status $\mathbb G(\beta)$, define
\[
\mathbf X_{\mathbb G(\beta)}:=\left(\sum_{k\in\mathcal G(\beta;\gamma_1)}\mathbf X_k,\ldots,\sum_{k\in\mathcal G(\beta;\gamma_{|\mathbb G(\beta)|})}\mathbf X_k\right),
\]
which is a groupwise collapsed matrix by summing up columns of $\mathbf X$ according to the groups in $\mathbb G(\beta)$.
''',[5],'Section 2.3.2 — groupwise collapsed matrix',{'D3':'Each column sums the original design columns in one nonzero coefficient group.'},phrases=['groupwise collapsed matrix'],symbols=[r'\mathbf X_{\mathbb G(\beta)}'],shape='Design with one column per nonzero group, summing original columns. The zero group contributes no column.')
add('D8','Oracle least squares estimator',r'''
Given the true coefficient $\beta^*$, the oracle least squares estimator $\widehat\theta^{\mathrm{ol}}=(\widehat\beta^{\mathrm{ol}\top},\widehat\alpha^{\mathrm{ol}\top})^\top$ is defined as
\[
\widehat\theta^{\mathrm{ol}}:=\arg\min_{\theta:\mathbb G(\beta)=\mathbb G(\beta^*)}\|\mathbf Y-\mathbf X\beta-\mathbf Z\alpha\|_2^2.
\]
More specifically, in $\widehat\beta^{\mathrm{ol}}=(\widehat\beta_1^{\mathrm{ol}},\ldots,\widehat\beta_p^{\mathrm{ol}})^\top$, $\widehat\beta_j^{\mathrm{ol}}$ is $\widehat\gamma_k$ if $j\in\mathcal G(\beta^*;\gamma_k^*);k=1,\ldots,K_0$, and $\widehat\beta_j^{\mathrm{ol}}$ is 0 if $j\in\mathcal G(\beta^*;0)$, where
\[
(\widehat\gamma^\top,\widehat\alpha^\top)=(\widehat\gamma_1,\ldots,\widehat\gamma_{K_0},\widehat\alpha^\top)=\arg\min_{(\gamma^\top,\alpha^\top)^\top\in\mathbb R^{K_0+q}}\|\mathbf Y-\mathbf X_{\mathbb G(\beta^*)}\gamma-\mathbf Z\alpha\|_2^2.
\]
''',[6],'Definition 2.3 (Oracle least squares estimator)',{'D3':'The oracle fixes the true nonzero group membership and sets zero-group coefficients to zero.','D7':'Its displayed least-squares representation uses the collapsed true-group design.'},context='Oracle least squares estimator',phrases=['Definition 2.3'],symbols=[r'\widehat\theta^{\mathrm{ol}}'],shape='Original group-constrained oracle and its stated unrestricted collapsed-design least-squares representation; preserve any nonuniqueness or mismatch rather than adding rank assumptions.')
add('D9','0-1 grouping risk',r'''
For any estimator $\widehat\theta=(\widehat\beta^\top,\widehat\alpha^\top)^\top$ of $\theta^*$, define the 0-1 grouping risk $\mathcal L_g(\widehat\theta;\theta^*):=\mathbb P(\mathbb G(\widehat\beta)\neq\mathbb G(\beta^*))$.
''',[6],'Section 2.3.2 — 0-1 grouping risk',{'D3':'The error event compares the estimated and true nonzero groupings.'},phrases=['0-1 grouping risk'],symbols=[r'\mathcal L_g(\widehat\theta;\theta^*)'],shape='Probability of incorrect nonzero-group recovery for any estimator. It does not require running L0-Fusion.')
add('D10','subspace',r'''
For $\ell>0$, consider the following subspace of $\Theta(K_0,s_0)$:
\[
\Theta_c(K_0,s_0,\ell):=\{\theta:\theta\in\Theta(K_0,s_0),c_{\min}(\theta,\mathbf X,\mathbf Z)\geq\ell\}.
\]
''',[7],'Section 2.3.3 — subspace with grouping sensitivity at least ell',{'D2':'The class lies in the grouped/sparse coefficient space.','D5':'Every member has grouping sensitivity at least ell for the supplied designs.'},phrases=['subspace'],symbols=[r'\Theta_c(K_0,s_0,\ell)'],shape='Parameter subclass with a lower bound on grouping sensitivity; preserve the author term subspace without asserting linear closure.')
add('D11',['well separated signal strengths','balanced group sizes'],r'''
For notational convenience, define the following subspace $\widetilde\Theta(K_0,s_0)$ of $\Theta(K_0,s_0)$ with well separated signal strengths across groups and balanced group sizes:
\[
\widetilde\Theta(K_0,s_0):=\{\theta^*\in\Theta(K_0,s_0):|\beta_j^*-\beta_{j'}^*|\geq1,\forall\beta_j^*\neq\beta_{j'}^*;\ |\mathcal G(\beta^*,\gamma_k^*)|\leq2|\mathcal G(\beta^*,\gamma_{k'}^*)|,\forall k,k'\in[K_0]\}.
\]
''',[7],'Section 2.3.3 — separated coefficients and balanced group sizes',{'D2':'The subclass retains the original grouped/sparse constraints.','D3':'The balancing condition compares the sizes of nonzero groups.'},phrases=['well separated signal strengths'],symbols=[r'\widetilde\Theta(K_0,s_0)'],shape='All unequal coefficient values separated by at least one and nonzero group sizes within factor two; the coefficient-separation condition also covers comparison with zero.')
add('D12','convex objective function',r'''
Suppose we are interested in a convex objective function $g(\theta)$ satisfying that:

(i) $g(\theta)\geq C_2>-\infty$ for some universal constant $C_2$;

(ii) $g(\theta)$ has Lipschitz continuous gradient, i.e., $\|\nabla g(\theta)-\nabla g(\widetilde\theta)\|_2\leq l\|\theta-\widetilde\theta\|_2$ for some positive $l$ and any $\theta,\widetilde\theta\in\Theta(K,s)$, which is defined in the beginning of Section 2.3.

Consider the following generalized $L_0$-Fusion problem:
\[
\min_{\theta\in\Theta(K,s)}g(\theta).\tag{3.3}
\]
''',[9],'Section 3.2 — convex objective conditions (i)-(ii) and problem (3.3)',{'D2':'The Lipschitz condition and constrained problem use Theta(K,s).'},kind='condition',phrases=['convex objective function'],symbols=[r'g(\theta)',r'l'],shape='General convex lower-bounded objective with Lipschitz gradient on the stated constrained domain; no Gaussian regression model or squared-loss specialization is assumed.')
add('D13','projection',r'''
For convenience, for any constant vector $\mathbf c=(c_1,\ldots,c_{p+q})^\top$, define
\[
\mathcal H_{K,s}(\mathbf c):=\arg\min_{\theta\in\Theta(K,s)}\|\theta-\mathbf c\|_2^2.
\]
''',[10],'Section 3.2 — projection onto Theta(K,s)',{'D2':'The nearest-point set is taken over the grouped/sparse parameter space.'},context=r'Algorithm 2 is essentially a projected gradient descent algorithm: In each iteration, we perform a gradient descent step followed by projection onto $\mathcal H_{K,s}$.',phrases=['constant vector'],symbols=[r'\mathcal H_{K,s}'],shape='Set-valued Euclidean projection onto the nonconvex grouped/sparse set. The name comes from the source explanation immediately following Algorithm 2.')
add('D14','Warm Start',r'''
Input: Loss function $g(\theta)$, number of groups $K$, sparsity constraint $s$, step size parameter $L$ and convergence tolerance $\varepsilon$.

1. Initialize with $\theta_1\in\mathbb R^{p+q}$.
2. For $m\geq1$, $\theta_{m+1}\in\mathcal H_{K,s}(\theta_m-\frac1L\nabla g(\theta_m))$.
3. Repeat Step 2 until $g(\theta_m)-g(\theta_{m+1})\leq\varepsilon$.

Output: $\theta_{m+1}$.
''',[10],'Algorithm 2 — Warm Start',{'D12':'The input objective has the convexity, lower bound and gradient regularity stated before the generalized problem.','D13':'Every update chooses an element of the projection of the gradient step.'},context='Warm Start',phrases=['Algorithm 2'],symbols=[r'\theta_{m+1}'],shape='Complete three-step projected-gradient warm-start algorithm with arbitrary initial vector and printed stopping tolerance; retain the infinite-sequence convention separately for Theorem 3.2.')

def main():
 for name,data in [('source-passages.json',dict(paper_id=PID,members=list(members.values()))),('interface-draft.json',interfaces)]:
  (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 print(f'Saved {len(interfaces)} source interfaces.')
if __name__=='__main__':main()
