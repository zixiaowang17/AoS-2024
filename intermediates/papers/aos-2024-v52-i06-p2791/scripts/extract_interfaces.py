"""Preserve original convex regression classes, designs, losses and entropy notation."""
import json,hashlib
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
add(1,'nonparametric regression',r'''We work in the standard nonparametric regression setting for estimating an unknown convex function $f_0:\Omega\to\mathbb R$ defined on a known full-dimensional compact convex domain $\Omega\subseteq\mathbb R^d$ ($d\ge1$) from observations $(X_1,Y_1),\ldots,(X_n,Y_n)$ generated via the model:
\[
Y_i=f_0(X_i)+\xi_i,\qquad\text{for }i=1,\ldots,n,\tag{1}
\]
where $\xi_1,\ldots,\xi_n$ are i.i.d. errors having the $N(0,\sigma^2)$ distribution, and design points $X_1,\ldots,X_n\in\Omega$ that may be fixed or random.''',[1],[],[r'Y_i=f_0(X_i)+\xi_i'],'Original convex regression model with Gaussian errors; independence of errors from random design is the usual model convention but not explicitly included in this sentence.','Introduction — Regression model (1)',kind='source_passage')
add(2,'convex functions',r'''$\mathcal C(\Omega)$: class of all convex functions on $\Omega$.''',[2],[],[r'\mathcal C(\Omega)'],'Original unrestricted class of real-valued convex functions on the domain. Convexity of each function differs from convexity of a class of functions in4.1.','Introduction — Convex function class')
add(3,'uniformly Lipschitz',r'''$\mathcal C_L^B(\Omega)$: class of all convex functions on $\Omega$ which are uniformly Lipschitz with Lipschitz constant $L$ and uniformly bounded by $B$.''',[2],[2],[r'\mathcal C_L^B(\Omega)',r'\mathcal C_L^L(\Omega)'],'Original simultaneous Lipschitz and absolute uniform bound;3.4 specializes B=L. Positive L,B are fixed in n by adjacent prose.','Introduction — Bounded Lipschitz convex class')
add(4,'Lipschitz constant',r'''$\mathcal C_L(\Omega)$: class of all convex functions on $\Omega$ that are uniformly Lipschitz with Lipschitz constant $L$. There is no uniform boundedness assumption on functions in this class.''',[2],[2],[r'\mathcal C_L(\Omega)'],'Original Lipschitz-only class, invariant under addition of constants. Do not add a uniform bound.','Introduction — Lipschitz convex class')
add(5,'uniformly bounded',r'''$\mathcal C^B(\Omega)$: class of all convex functions on $\Omega$ that are uniformly bounded by $B$. There is no Lipschitz assumption on functions in this class.''',[2],[2],[r'\mathcal C^B(\Omega)',r'\mathcal C^\Gamma(\Omega)'],'Original absolute uniformly bounded convex class. Gamma is the instantiated bound in4.5; no Lipschitz condition is added.','Introduction — Bounded convex class')
add(6,'Least Squares Estimator (LSE)',r'''The Least Squares Estimator (LSE) over a class $\mathcal F$ of functions on $\Omega$ is defined as any minimizer of the least squares criterion over $\mathcal F$:
\[
\hat f_n(\mathcal F)\in\operatorname*{argmin}_{f\in\mathcal F}\sum_{i=1}^n(Y_i-f(X_i))^2.\tag{2}
\]''',[2],[],[r'\hat f_n(\mathcal F)',r'\hat f_n(\mathcal C(\Omega))'],'Original generic least-squares argmin over a supplied class and sample. It is a selection, not a claim of unique functions off design points. Existence and measurability are not automatic for arbitrary classes.','Introduction — Least squares estimator (2)')
add(7,'convex body',r'''For our results, we assume throughout the paper that the convex body $\Omega$ (which is the domain of the unknown function $f_0$) is translated and scaled so that
\[
r_d\mathfrak B_d\subseteq\Omega\subseteq\mathfrak B_d\tag{3}
\]
where $\mathfrak B_d$ is the unit ball in $\mathbb R^d$ and $r_d$ is a positive constant depending on $d$ alone.''',[2],[],[r'r_d\mathfrak B_d\subseteq\Omega\subseteq\mathfrak B_d'],'Original normalized-domain assumption, with dimensional inradius. Theorem4.5 expressly asks only for containment in the unit ball;4.1 uses its own arbitrary design body.','Introduction — Domain condition (3)',kind='condition')
add(8,'random design',r'''We focus first on the random design setting where the design points $X_1,\ldots,X_n$ are assumed to be independent having the uniform distribution $\mathbb P$ on $\Omega$ (see Subsection 5.3 for a discussion of more general design assumptions in random design)''',[3],[],[r'\mathbb P'],'Original iid uniform random-design law. The stronger Section5.3 generalization is a separate discussion, not the original hypothesis of3.1.','Introduction — Random design',kind='assumption',phrases=['uniform distribution'])
add(9,'loss function',r'''and work with the loss function
\[
\ell_{\mathbb P}^2(f,g):=\int_\Omega(f-g)^2d\mathbb P.\tag{4}
\]''',[3],[8],[r'\ell_{\mathbb P}^2(f,g)'],'Original squared population L2 loss under the uniform law; its square root is the corresponding metric. Not the random empirical loss used in conditional proof arguments.','Introduction — Population loss (4)')
add(10,'expectation',r'''where $\mathbb E_{f_0}$ denotes expectation with respect to the joint distribution of all the observations $(X_1,Y_1),\ldots,(X_n,Y_n)$ when $f_0$ is the true regression function (see (1)), and the infimum is over all estimators $\breve f_n$.''',[3],[1],[r'\mathbb E_{f_0}'],'Original true-regression-function subscript on risk expectations. Under fixed design only the errors are random; the notation remains the same. Final infimum clause belongs to preceding minimax definition, archived separately.','Introduction — Risk expectation convention',kind='source_passage')
add(11,'empirical distribution',r'''\[
\ell_{\mathbb P_n}^2(f,g):=\int(f-g)^2d\mathbb P_n=\frac1n\sum_{i=1}^n(f(X_i)-g(X_i))^2\tag{8}
\]
with $\mathbb P_n$ being the (non-random) empirical distribution of $X_1,\ldots,X_n$.''',[6],[],[r'\ell_{\mathbb P_n}^2(f,g)',r'\ell_{\mathbb P_n}(f,g)'],'Original empirical quadratic loss at supplied fixed design points; the formula itself does not impose a regular grid. It is a pseudometric on full functions and a metric on evaluation vectors.','Section 1.1 — Empirical loss (8)')
add(12,'affine functions',r'''where $\mathcal A(\Omega)$ denotes the class of all affine functions on $\Omega$, and $\mathfrak L$ is a fixed positive constant.''',[6],[],[r'\mathcal A(\Omega)'],'Original affine comparison class, not a bounded/Lipschitz-restricted subclass. The fraktur L in this sentence belongs to Eq9.','Section 1.1 — Affine comparison class')
add(13,'function class',r'''In this setting, we are able to prove uniform rates of convergence for $\hat f_n(\mathcal C(\Omega))$ over a function class that is larger than the function classes considered so far. This function class is given by:
\[
\mathcal F^{\mathfrak L}(\Omega):=\left\{f_0\text{ convex on }\Omega:\inf_{g\in\mathcal A(\Omega)}\ell_{\mathbb P_n}(f_0,g)\le\mathfrak L\right\}\tag{9}
\]''',[6],[2,11,12],[r'\mathcal F^{\mathfrak L}(\Omega)'],'Original distance-to-affine class with unsquared empirical distance <=fraktur L. This is neither a Lipschitz constant nor a uniform bound; class depends on design through the empirical loss.','Section 1.1 — Function class (9)')
add(14,'polytope',r'''For fixed design, we are mostly only able to prove results when $\Omega$ is a polytope (see Subsection 5.2 for some remarks on fixed-design results for non-polytopal $\Omega$). Specifically, we assume that
\[
\Omega:=\{x\in\mathbb R^d:a_i\le v_i^Tx\le b_i\text{ for }i=1,\ldots,F\}\tag{14}
\]
for $F\ge1$, unit vectors $v_1,\ldots,v_F$ and real numbers $a_1,\ldots,a_F,b_1,\ldots,b_F$. The number $F$ is assumed to be bounded from above by a constant depending on $d$ alone. As in the rest of the paper, we also assume (3).''',[9],[7],[r'a_i\le v_i^Tx\le b_i'],'Original fixed-design slab representation and dimensional slab-count bound. F counts defining slabs, not necessarily the exact number of facets. The additional branch of3.1 instead states a facet condition directly.','Section 2.2 — Polytopal domain (14)',kind='condition')
add(15,'regular rectangular grid',r'''Specifically, for $\delta>0$, let
\[
\mathcal S:=\{(k_1\delta,\ldots,k_d\delta):k_i\in\mathbb Z,1\le i\le d\}\tag{15}
\]
denote the regular $d$-dimensional $\delta$-grid in $\mathbb R^d$. We assume that $X_1,\ldots,X_n$ are an enumeration of the points in $\mathcal S\cap\Omega$ with $n$ denoting the cardinality of $\mathcal S\cap\Omega$. By the usual volumetric argument and assumption (3) , there exists a small enough constant $\kappa_d>0$ such that whenever $0<\delta\le\kappa_d$, we have
\[
2\le c_d\delta^{-d}\le n\le C_d\delta^{-d}\tag{16}
\]
for dimensional constants $c_d$ and $C_d$. We have included a proof of the above claim in Lemma C.2. Throughout, we assume $\delta\le\kappa_d$ so that the above inequality holds.''',[9],[7],[r'\mathcal S',r'\delta\le\kappa_d'],'Original lattice and small-resolution design convention. n is the cardinality of its domain intersection, not a freely independent parameter. The response clause in naming context invokes1 only for statistical applications; deterministic entropy4.11 does not require responses or Gaussian noise.','Section 2.2 — Fixed grid (15)–(16)',kind='condition',context='The design points $X_1,\ldots,X_n$ are assumed to form a fixed regular rectangular grid in $\Omega$ and $Y_1,\ldots,Y_n$ are generated according to (1).')
add(16,'piecewise affine convex functions',r'''For $k\ge1$ and $h\ge1$, let $\mathcal C_{k,h}(\Omega)$ denote all functions $f\in\mathcal C(\Omega)$ for which there exist $k$ convex subsets $\Omega_1,\ldots,\Omega_k$ satisfying the following properties:
1. $f$ is affine on each $\Omega_i$,
2. each $\Omega_i$ can be written as an intersection of at most $h$ slabs (i.e., as in (14) with $F=h$), and
3. $\Omega_1\cap\mathcal S,\ldots,\Omega_k\cap\mathcal S$ are disjoint with $\cup_{i=1}^k(\Omega_i\cap\mathcal S)=\Omega\cap\mathcal S$ (recall that $\mathcal S$ is the regular rectangular grid (15)).''',[12],[2,15],[r'\mathcal C_{k,h}(\Omega)'],'Original grid-partition piecewise-affine class. Slab format is invoked locally, with h instead of F; do not impose the normalized-domain inradius on each cell. Grid intersections, not full regions, must be disjoint and cover.','Section 3.2 — Piecewise affine class',context='Theorem 3.6 (stated later in this section) which provides a lower bound on the risk of $\hat f_n(\mathcal C(\Omega))$ for certain piecewise affine convex functions.',context_page=11)
add(17,'simplex',r'''Recall that a $d$-simplex $\Delta$ in $\mathbb R^d$ is the convex hull of $d+1$ affinely independent points. It is well-known that $d$-simplices can be represented as the intersection of $d+1$ halfspaces.''',[10],[],[],'Original full-dimensional simplex terminology. Disjoint interiors in4.5 do not require a partition of the entire domain.','Section 3.1 — Simplex definition',phrases=['affinely independent points'])
add(18,'piecewise affine approximation',r'''Suppose $\Omega$ is a convex body satisfying (3). Let $f_0(x):=\|x\|^2$. There exists a positive constant $C_d$ (depending on $d$ alone) such that the following is true. For every $k\ge1$, there exist $m\le C_dk$ $d$-simplices $\Delta_1,\ldots,\Delta_m\subseteq\Omega$ and a convex function $\tilde f_k$ on $\Omega$ such that
1. $(1-C_dk^{-1/d})\Omega\subseteq\cup_{i=1}^m\Delta_i\subseteq\Omega$,
2. $\Delta_i\cap\Delta_j$ is contained in a facet of $\Delta_i$ and a facet of $\Delta_j$ for each $i\ne j$,
3. $\tilde f_k$ is affine on each $\Delta_i$, $i=1,\ldots,m$,
4. $\sup_{x\in\Omega}|f_0(x)-\tilde f_k(x)|\le C_dk^{-2/d}$,
5. $\tilde f_k\in\mathcal C_{C_d}^{C_d}(\Omega)$,
If, in addition, $\Omega$ is a polytope whose number of facets is bounded by a constant depending on $d$ alone, then the first condition above can be strengthened to $\Omega=\cup_{i=1}^m\Delta_i$.''',[10,11],[3,7,17],[r'\tilde f_k',r'\mathcal C_{C_d}^{C_d}(\Omega)'],'Complete Lemma3.2 statement supplies the function explicitly required by3.6. Store as source passage, not an inventoried theorem or invented definition. It gives existence, not a uniquely specified construction; no appendix construction imported.','Lemma 3.2 — Referenced approximation function',kind='source_passage',context='This function $\tilde f$ will be a piecewise affine approximation to the quadratic $f_0(x):=\|x\|^2$.',context_page=10)
add(19,'metric entropy',r'''Recall that the $\epsilon$-metric entropy of a function class $\mathcal F$ with respect to a metric $\ell$ is defined as the logarithm of the smallest number $N(\epsilon,\mathcal F,\ell)$ of closed balls of radius $\epsilon$ whose union contains $\mathcal F$.''',[3],[],[r'N(\epsilon,\mathcal F,\ell)'],'Original covering entropy convention with closed balls. Centers and pseudometric quotient conventions are not separately stated. This is not bracketing entropy.','Introduction — Metric entropy')
add(20,'bracketing entropy',r'''The left hand side above denotes bracketing entropy with respect to $L_p$ metric on $\Delta_1\cup\cdots\cup\Delta_k$.''',[17],[],[],'Original explanation of N-brackets in43 with Lp on the union of simplices, distinct from the uniform-probability-metric instance defined on4. Lebesgue Lp and bracket ordering are ambient here; original specialization is archived separately.','Theorem 4.5 — Bracketing entropy convention',kind='source_passage',phrases=['bracketing entropy'])
add(21,'bounded convex functions',r'''For a fixed $1\le p<\infty$ and $t>0$, let
\[
B_p^\Gamma(\tilde f,t,\Omega)=\left\{f\in\mathcal C^\Gamma(\Omega):\int_\Omega|f(x)-\tilde f(x)|^pdx\le t^p\right\}.\tag{42}
\]''',[17],[5],[r'B_p^\Gamma(\tilde f,t,\Omega)'],'Original local Lp ball of Gamma-bounded convex functions around a supplied convex center. The norm constraint is on the full domain, whereas43 brackets restrictions to the union of simplices.','Theorem 4.5 — Local function class (42)',kind='theorem_excerpt',context='It provides an upper bound on the bracketing entropy of bounded convex functions with an additional $L_p$ norm constraint.',context_page=17)
add(22,'discrete metric',r'''Even though we only need the entropy bound for $p=2$, we state the next result for the discrete $L_p$ metric $(f,g)\mapsto\ell_{\mathcal S}(f-g,\Omega,p)$ for every $1\le p<\infty$ where
\[
\ell_{\mathcal S}(f,\Omega,p)=\left(\frac1n\sum_{s\in\Omega\cap\mathcal S}|f(s)|^p\right)^{1/p}.\tag{51}
\]
The $\epsilon$-covering number of a space $\mathcal F$ of functions on $\Omega$ under the metric $(f,g)\mapsto\ell_{\mathcal S}(f-g,\Omega,p)$ will be denoted by $N(\epsilon,\mathcal F,\ell_{\mathcal S}(\cdot,\Omega,p))$.''',[19],[15,19],[r'\ell_{\mathcal S}(f,\Omega,p)',r'1\le p<\infty'],'Original discrete Lp norm and induced covering-number notation. For the entropy theorem, S is supplied by the separate grid conditionD15. Empirical counting is normalized by n; do not replace it by Lebesgue integration.','Section 4.4 — Discrete metric (51)',context='Theorem 4.11 is the first entropy result for convex functions that deals with the discrete metric $\ell_{\mathcal S}(\cdot,\Omega,p)$ (all previous results hold for continuous $L_p$ metrics).',context_page=20)
add(23,'concave function',r'''\[
H_f(t,\mathcal F):=\mathbb E\sup_{g\in\mathcal F:\ell_{\mathbb P_n}(f,g)\le t}\frac1n\sum_{i=1}^n\xi_i(g(X_i)-f(X_i))-\frac{t^2}2.
\]''',[13],[11],[r'H_f(t,\mathcal F)'],'Original deterministic-design expected local Gaussian supremum minus t squared over2; bind f,F,design and Gaussian noise as in4.1. Random-design conditional counterpart32 is archived separately, not substituted.','Theorem 4.1 — Local objective',kind='theorem_excerpt',context='Then $H_f(\cdot,\mathcal F)$ is a concave function on $[0,\infty)$, $t_f(\mathcal F)$ is unique and the following pair of inequalities hold for positive constants $c$ and $C$:',context_page=13)
add(24,'maximizer',r'''\[
t_f(\mathcal F):=\operatorname*{argmax}_{t\ge0}H_f(t,\mathcal F)
\]''',[13],[23],[r't_f(\mathcal F)'],'Original argmax of the local objective on nonnegative radii. Uniqueness is asserted by4.1; it is not uniqueness of the regression function itself.','Theorem 4.1 — Maximizing radius',kind='theorem_excerpt',context='The challenge is to show that the maximizer of $H_{\tilde f_k}(t,\mathcal F)$ is at least $n^{-1/d}(\log n)^{-2(d+1)/d}$ for each function class $\mathcal F$ in the statement of Theorem 3.1.',context_page=14)
# Source-inspected rendering amendment; see the explicit saved review plan.
members['D3']['highlight_symbols'] = ['\\mathcal C_L^B(\\Omega)', '\\sup_{f\\in\\mathcal C_L^L(\\Omega)}']
members['D11']['highlight_symbols'] = ['\\ell_{\\mathbb P_n}^2(f,g)', '\\sup_{g\\in\\mathcal F:\\ell_{\\mathbb P_n}(f,g)\\le t}']

def main():
    review=json.loads((REVIEW_ROOT/'inventory-review.json').read_text());assert review['status']=='complete' and review['source_checked']
    assert hashlib.sha256((ROOT/'theorem-inventory.json').read_bytes()).hexdigest()==review['inventory_sha256']
    assert len(interfaces)==len(members)==24
    for x in interfaces:
        m=x['members'][0];assert set(m['depends_on'])<=set(members)
        assert any(v in m['statement_original']+' '+m['local_label'] for v in m['highlight_symbols']+m['highlight_phrases'])
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
    print('Saved24 original source entries; full census review remains pending.')
if __name__=='__main__':main()
