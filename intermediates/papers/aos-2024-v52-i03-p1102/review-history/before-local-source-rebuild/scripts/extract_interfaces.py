"""Extract main-text MARS prerequisites without consulting appendix mathematics."""
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
add('D1','ReLU function',r'''Here $\cdot_+:=\max\{\cdot,0\}$ indicates the ReLU function.''',[1],'Section 1 — positive part',symbols=[r'\cdot_+'],shape='Positive-part function used by every hinge factor, with zero included. The arguments and knots in individual hinge factors are local binders.')
add('D2','interaction term',r'''
Indeed, the term (1) can be interpreted as an interaction term of order $|\alpha|$ between the variables in the set $S(\alpha)$. Here and in the rest of the paper, we use the notation
\[
S(\alpha):=\{j\in[d]:\alpha_j=1\},\qquad\text{where }[d]:=\{1,\ldots,d\},
\]
and
\[
|\alpha|:=|S(\alpha)|=\sum_{j=1}^d\mathbf1\{\alpha_j=1\}.
\]
''',[2],'Section 1 — interaction index and order',symbols=[r'S(\alpha)',r'|\alpha|'],shape='Support and number of active coordinates of a binary interaction index alpha. The surrounding MARS basis context fixes alpha in {0,1}^d; this is not a norm of a general real vector.')
add('D3','infinite linear combinations',r'''
In the MARS context, infinite linear combinations of the basis functions (1) with $|\alpha|\le s$ are
\[
f_{a_0,\{\nu_\alpha\}}(x_1,\ldots,x_d):=a_0+\sum_{\substack{\alpha\in\{0,1\}^d\setminus\{\mathbf0\}\\|\alpha|\le s}}\int_{[0,1)^{|\alpha|}}\prod_{j\in S(\alpha)}(x_j-t_j)_+\,d\nu_\alpha(t^{(\alpha)}),\tag{3}
\]
where $\mathbf0:=(0,\ldots,0)$, $a_0\in\mathbb R$, $\nu_\alpha$ is a finite (Borel) signed measure on $[0,1)^{|\alpha|}$, and $t^{(\alpha)}$ indicates the vector $(t_j,j\in S(\alpha))$ for each binary vector $\alpha\in\{0,1\}^d\setminus\{\mathbf0\}$ with $|\alpha|\le s$. We will denote the collection of all such functions $f_{a_0,\{\nu_\alpha\}}$ by $\mathcal F_{\infty-\mathrm{mars}}^{d,s}$ (the subscript $\infty$ highlights the fact that $\mathcal F_{\infty-\mathrm{mars}}^{d,s}$ contains infinite linear combinations of the functions (1)).
''',[3],'Section 1 — signed-measure MARS class (3)',{'D1':'Each integrand is a product of positive-part hinge functions.','D2':'The binary support S(alpha) determines the active coordinates and the interaction cutoff |alpha|<=s.'},symbols=[r'\mathcal F_{\infty-\mathrm{mars}}^{d,s}',r'f_{a_0,\{\nu_\alpha\}}'],shape='Functions on the unit cube represented by an intercept and finite signed Borel measures on half-open knot cubes, over nonempty interactions of order at most s. The representation uses signed measures, not only probabilities or nonnegative mixtures.')
add('D4','variation',r'''Recall that, for a signed measure $\nu$ on $\Omega$ and a measurable subset $E\subseteq\Omega$, the variation of $\nu$ on $E$ is denoted by $|\nu|(E)$ and is defined as the supremum of $\sum_{A\in\pi}|\nu(A)|$ over all partitions $\pi$ of $E$ into a countable number of disjoint measurable subsets.''',[3],'Section 1 — variation of a signed measure',symbols=[r'|\nu|(E)'],shape='Total variation measure evaluated on a measurable set, defined using countable measurable partitions. This is distinct from the later function total variation and Hardy–Krause variation.')
add('D5','complexity measure',r'''
Using the variation of the involved signed measures, we define our complexity measure for functions $f=f_{a_0,\{\nu_\alpha\}}\in\mathcal F_{\infty-\mathrm{mars}}^{d,s}$ by
\[
V_{\mathrm{mars}}(f_{a_0,\{\nu_\alpha\}})=\sum_{\substack{\alpha\in\{0,1\}^d\setminus\{\mathbf0\}\\|\alpha|\le s}}|\nu_\alpha|\bigl([0,1)^{|\alpha|}\setminus\{\mathbf0\}\bigr).\tag{6}
\]
We are excluding $\mathbf0=(0,\ldots,0)$ in the variation of $\nu_\alpha$ because we want to only penalize those basis functions that include at least one nonlinear term and leave unpenalized basis functions that are products of linear functions (note that $(x_j-t_j)_+=x_j$ is linear when $t_j=0$ because $x_j\in[0,1]$).
''',[3],'Section 1 — MARS complexity (6)',{'D3':'The complexity is defined from the signed measures of the original function representation.','D4':'It sums their variation measures on the knot cubes with only the all-zero vector removed.'},symbols=[r'V_{\mathrm{mars}}',r'[0,1)^{|\alpha|}\setminus\{\mathbf0\}'],shape='Complexity seminorm excluding the all-zero atom in each interaction measure. Intercepts and products of linear coordinates are unpenalized. The uniqueness proof is in an appendix, but the entire defining formula is in the main text.')
add('D6','estimator',r'''
Our estimator is thus given by
\[
\widehat f_{n,V}^{d,s}\in\operatorname*{arg\,min}_f\left\{\sum_{i=1}^n\bigl(y_i-f(x^{(i)})\bigr)^2:f\in\mathcal F_{\infty-\mathrm{mars}}^{d,s}\text{ and }V_{\mathrm{mars}}(f)\le V\right\}\tag{7}
\]
for a tuning parameter $V>0$.
''',[4],'Section 1 — constrained MARS least-squares estimator (7)',{'D3':'The feasible functions lie in the signed-measure MARS class.','D5':'The constraint bounds the MARS complexity while leaving its nullspace unpenalized.'},symbols=[r'\widehat f_{n,V}^{d,s}'],shape='Any solution of constrained least squares on the original infinite-dimensional MARS class. The definition is an argmin membership, not a uniqueness claim or a penalized-objective formula. Fixed/random sampling assumptions are imposed separately by the corresponding risk section.')
add('D7','finite-dimensional lasso problem',r'''
Also, let $(\widehat a_0,\widehat\gamma_{n,V}^{d,s})\in\mathbb R\times\mathbb R^{|J|}$ be a solution to the following finite-dimensional lasso problem
\[
(\widehat a_0,\widehat\gamma_{n,V}^{d,s})\in\operatorname*{arg\,min}_{a_0\in\mathbb R,\gamma\in\mathbb R^{|J|}}\left\{\|y-a_0\mathbf1-M\gamma\|_2^2:\sum_{\substack{(\alpha,l)\in J\\l\ne\mathbf0}}|\gamma_{\alpha,l}|\le V\right\},\tag{13}
\]
where $\mathbf1:=(1,\ldots,1)$ and $y=(y_i,i\in[n])$ is the vector of observations.
''',[7],'Proposition 2.2 — finite-dimensional optimization formula (13)',symbols=[r'\widehat\gamma_{n,V}^{d,s}',r'l\ne\mathbf0'],shape='Constrained coefficient optimization formula with index set J and design matrix M. The original proposition uses observed-data knots, while Section 2 explicitly reuses this formula with different J,M for the approximate problem. The formula is kept separate from either instantiation; do not force observed knots into the approximate estimator.')
add('D8','approximate method',r'''
In the approximate method, we instead restrict our attention to discrete signed measures $\nu_\alpha$ supported on the lattices generated by
\[
\widetilde{\mathcal U}_k=\left\{0,\frac1{N_k},\frac2{N_k},\ldots,1\right\}
\]
for some pre-selected positive integers $N_1,\ldots,N_d$, and we only take into consideration the basis functions corresponding to those signed measures.
''',[8],'Section 2 — fixed knot grids for the approximate method',{'D3':'The restriction concerns the signed measures in the MARS representation.'},symbols=[r'\widetilde{\mathcal U}_k',r'N_1,\ldots,N_d'],shape='Equispaced candidate grids fixed before fitting. The grid includes 1, but the signed-measure representation and the subsequent coefficient index set omit upper-endpoint knots, whose hinge contribution is zero.')
add('D9','approximate (finite-dimensional optimization) problem',r'''
We then consider the finite-dimensional optimization problem to which the problem (7) reduces when we additionally impose such restrictions on signed measures $\nu_\alpha$. We call this problem the approximate (finite-dimensional optimization) problem. The approximate problem has the same form as (13) but with different $M$ and $J$. Here
\[
J=\left\{(\alpha,l):\alpha\in\{0,1\}^d\setminus\{\mathbf0\},|\alpha|\le s,\text{ and }l\in\prod_{k\in S(\alpha)}[0:(N_k-1)]\right\},
\]
and $M$ is the $n\times|J|$ matrix with columns indexed by $(\alpha,l)\in J$ such that
\[
M_{i,(\alpha,l)}=\prod_{k\in S(\alpha)}\left(x_k^{(i)}-\frac{l_k}{N_k}\right)_+\qquad\text{for }i\in[n]\text{ and }(\alpha,l)\in J.
\]
''',[8],'Section 2 — approximate optimization matrix and index set',{'D3':'The source restricts the signed-measure feasible class of problem (7) to the approximate grids.','D5':'The same MARS complexity constraint is retained under that restriction; no value of the exact estimator is required.','D7':'The coefficient objective and constraint have the same form as (13), instantiated with the J,M displayed here.','D8':'The matrix columns use the predetermined grids with knots l_k/N_k.','D2':'The column index set uses active-coordinate supports and the interaction cutoff.','D1':'The columns are products of positive-part hinge functions.'},symbols=[r'M_{i,(\alpha,l)}',r'[0:(N_k-1)]'],shape='Approximate design matrix and coefficient index set. The preselected grid resolutions N_k differ from the observed-grid counts n_k of Proposition 2.2 and from the lattice design counts reused in Section 3.1.')
add('D10','function',r'''
Then, the function $f$ on $[0,1]^d$ defined by
\[
f(x_1,\ldots,x_d)=\widehat a_0+\sum_{(\alpha,l)\in J}(\widehat\gamma_{n,V}^{d,s})_{\alpha,l}\cdot\prod_{k\in S(\alpha)}(x_k-u_{l_k}^{(k)})_+\tag{14}
\]
''',[7],'Proposition 2.2 — function reconstruction formula (14)',{'D7':'The coefficients and intercept are a selected optimizer of the finite-dimensional objective.','D2':'Each product uses the coordinates in the support S(alpha).','D1':'The reconstruction multiplies positive-part hinge functions.'},symbols=[r'(\widehat\gamma_{n,V}^{d,s})_{\alpha,l}'],shape='Function reconstruction from coefficient/intercept and knot values. Proposition 2.2 uses observed knots; page 9 explicitly instructs using the same formula for the approximate problem, where u_{l_k}^{(k)} is instantiated by l_k/N_k. The observed-knot construction is not inherited as an approximate-estimator restriction.')
add('D11','approximate version',r'''Once we find a solution to the approximate problem, we can construct an estimator of the true underlying function $f^*$ through the equation (14) as before. We denote this estimator by $\widetilde f_{n,V}^{d,s}$ and call it an approximate version of $\widehat f_{n,V}^{d,s}$.''',[9],'Section 2 — approximate MARS estimator',{'D9':'The selected optimizer comes from the approximate problem with its fixed-grid J,M.','D10':'The source explicitly constructs the fitted function through the reconstruction formula (14), using those approximate knots.'},symbols=[r'\widetilde f_{n,V}^{d,s}'],shape='Fixed-grid approximation defined by solving the approximate constrained problem and reconstructing its function. The label hat-f in the source comparison does not make this an unrestricted optimizer of (7); the approximation uses the restricted feasible class.')

add('D12','lattice',r'''
Here we assume that $x^{(1)},\ldots,x^{(n)}$ form a lattice
\[
\{x^{(1)},\ldots,x^{(n)}\}=\prod_{k=1}^d\left\{u_{i_k}^{(k)}:i_k\in[0:(n_k-1)]\right\}\tag{15}
\]
where for every $k\in[d]$, we have $n_k\ge2$, $0=u_0^{(k)}<u_1^{(k)}<\cdots<u_{n_k-1}^{(k)}\le1$, and
\[
u_{i_k}^{(k)}-u_{i_k-1}^{(k)}\ge\frac\rho{n_k}\qquad\text{for all }i_k\in[n_k-1]
\]
for some constant $\rho>0$.
''',[9],'Section 3.1 — fixed lattice design (15)',kind='assumption',symbols=[r'u_{i_k}^{(k)}-u_{i_k-1}^{(k)}',r'\frac\rho{n_k}'],shape='Cartesian product design with a zero left endpoint, at least two distinct coordinate values and a uniform lower spacing bound. It need not be equally spaced or reach 1 at its upper endpoint. These n_k counts differ from the earlier computational-grid counts that include an extra terminal point.')
add('D13',['regression model','sub-Gaussian errors'],r'''
We also assume that $y_1,\ldots,y_n$ are generated according to the regression model
\[
y_i=f^*(x^{(i)})+\xi_i\tag{16}
\]
where $f^*:[0,1]^d\to\mathbb R$ is an unknown regression function and $\xi_i$ are independent sub-Gaussian errors with mean zero and with a sub-Gaussian parameter $\sigma$, i.e.,
\[
\mathbb E[e^{\lambda\xi_i}]\le e^{\frac{\sigma^2\lambda^2}2}
\]
for all $\lambda\in\mathbb R$.
''',[9],'Section 3.1 — fixed-design regression and error law (16)',kind='assumption',symbols=[r'\mathbb E[e^{\lambda\xi_i}]',r'y_i=f^*(x^{(i)})+\xi_i'],shape='Fixed-design regression with independent mean-zero errors and a common sub-Gaussian mgf bound. Identical error distributions are not required. Lattice geometry is a separate condition, not built into this model formula.')
add('D14','risk',r'''
We measure the accuracy of an estimator $\widehat f_n$ of $f^*$ via the squared empirical $L^2$ norm
\[
\|\widehat f_n-f^*\|_n^2:=\frac1n\sum_{i=1}^n\bigl(\widehat f_n(x^{(i)})-f^*(x^{(i)})\bigr)^2\tag{17}
\]
and define its risk as
\[
\mathcal R_F(\widehat f_n,f^*)=\mathbb E\|\widehat f_n-f^*\|_n^2
\]
where the expectation is taken over $y_1,\ldots,y_n$.
''',[9],'Section 3.1 — fixed-design squared empirical loss and risk',{'D13':'The expectation over responses uses the fixed-design regression model (16).'},symbols=[r'\mathcal R_F',r'\|\widehat f_n-f^*\|_n^2'],shape='Expected squared empirical prediction error, averaging at the fixed design points. This is neither population L2 error nor the random-design rate-in-probability quantity.')
add('D15','collection of all the functions',r'''
which is defined as the collection of all the functions of the form
\[
(x_1,\ldots,x_m)\mapsto\int(x_1-t_1)_+\cdots(x_m-t_m)_+\,d\nu(t),
\]
where $m\in[d]$ and $\nu$ is a signed measure on $[0,1]^m$ with variation $|\nu|([0,1]^m)\le1$.
''',[10],'Section 3.1 — function class D_m',{'D1':'The class consists of signed integrals of products of positive-part hinges.','D4':'Its measure has total variation at most one on the entire closed cube.'},symbols=[r'|\nu|([0,1]^m)\le1',r'\mathcal D_m'],shape='The class D_m used by both entropy Theorems. It has no added intercept and bounds all measure mass on the closed cube, including zero. It is not the original MARS feasible class with its unpenalized multilinear nullspace. The source does not provide a separate natural-language name, so its literal collection description is retained.')
add('D16','probability density function',r'''Here we assume that $x^{(1)},\ldots,x^{(n)}$ are realizations of i.i.d. random variables $X^{(1)},\ldots,X^{(n)}$ with a probability density function $p_0$ on $[0,1]^d$ that is bounded by some constant $B\ge1$, i.e., $\|p_0\|_\infty\le B$.''',[11],'Section 3.2 — random design with bounded density',kind='assumption',symbols=[r'\|p_0\|_\infty\le B'],shape='Iid design points with a density bounded above on the unit cube. No lower density bound is imposed here; the minimax lower-bound paragraph adds one separately.')
add('D17',['regression model','i.i.d. errors'],r'''
Also, we assume that $(X^{(1)},y_1),\ldots,(X^{(n)},y_n)$ are generated according to the regression model
\[
y_i=f^*(X^{(i)})+\xi_i\tag{20}
\]
where $\xi_i$ are i.i.d. errors independent of $X^{(1)},\ldots,X^{(n)}$ with mean zero and with finite $L^{5,1}$ norm; that is,
\[
\|\xi_i\|_{5,1}:=\int_0^\infty\bigl(\mathbb P(|\xi_i|>t)\bigr)^{\frac15}\,dt<\infty.\tag{21}
\]
''',[11],'Section 3.2 — random-design regression and L^{5,1} errors (20)–(21)',{'D16':'The covariates are the iid bounded-density design variables of this section.'},kind='assumption',symbols=[r'\|\xi_i\|_{5,1}',r'y_i=f^*(X^{(i)})+\xi_i'],shape='Random-design regression with iid mean-zero errors independent of the covariates and a finite Lorentz L^{5,1} tail integral. This is stronger than a finite fifth moment and is not replaced by the fixed-design sub-Gaussian condition.')
add('D18','accuracy',r'''
In this setting, we measure the accuracy of an estimator $\widehat f_n$ of $f^*$ by
\[
\|\widehat f_n-f^*\|_{p_0,2}^2:=\int\bigl(\widehat f_n(x)-f^*(x)\bigr)^2p_0(x)\,dx.\tag{22}
\]
''',[11],'Section 3.2 — squared population L2 error (22)',{'D16':'The weighting density p0 is the random-design density on the unit cube.'},symbols=[r'\|\widehat f_n-f^*\|_{p_0,2}^2'],shape='Squared L2 prediction error under the design density, a random quantity for a fitted estimator. Theorems 3.5 and 3.8 bound it in probability; Theorem 3.9 instead concerns its expected minimax risk.')
add('D19','minimax risk',r'''
Specifically, we bound the minimax risk defined as
\[
\mathfrak M_{n,V}^{d,s}=\inf_{\widehat f_n}\sup_{\substack{f^*\in\mathcal F_{\infty-\mathrm{mars}}^{d,s}\\V_{\mathrm{mars}}(f^*)\le V}}\mathbb E_{f^*}\|\widehat f_n-f^*\|_{p_0,2}^2,
\]
where the expectation is taken over $(X^{(1)},y_1),\ldots,(X^{(n)},y_n)$ of (20) and $\inf_{\widehat f_n}$ denotes the infimum over all estimators $\widehat f_n$ of $f^*$ based on $(X^{(1)},y_1),\ldots,(X^{(n)},y_n)$.
''',[12],'Section 3.2 — minimax expected population risk',{'D3':'The supremum ranges over the signed-measure MARS class.','D5':'The class in the supremum has complexity at most V.','D17':'The expectation is over the complete random-design regression experiment (20).','D18':'The loss is squared population L2 error under p0.'},symbols=[r'\mathfrak M_{n,V}^{d,s}'],shape='Minimax expected loss over all data-based estimators and all MARS regression functions satisfying the complexity bound. It does not restrict the infimum to either the exact or approximate MARS estimator.')
add('D20',['Gaussian errors','probability density function'],r'''Here we further restrict that $\xi_i$ in the model (20) are independent Gaussian errors with mean zero and variance $\sigma^2$ and that the probability density function $p_0$ of $X^{(i)}$ is bounded below by some positive constant $b$, i.e., $\|p_0\|_\infty\ge b$.''',[12,13],'Section 3.2 — additional model restrictions before Theorem 3.9',{'D17':'This paragraph further restricts the noise in regression model (20).','D16':'The lower-density prose refers to the same design density, already bounded above by B.'},kind='assumption',symbols=[r'\sigma^2',r'\|p_0\|_\infty\ge b'],phrases=['Gaussian errors'],shape='Additional Gaussian-noise and lower-density assumptions for the minimax lower bound only. The prose states a positive lower density bound, but the printed sup-norm inequality does not express that property; both are retained as a source inconsistency.')
add('D21','bracketing number',r'''where $N_{[\,]}(\epsilon,\mathcal D_m,\|\cdot\|_2)$ is the $\epsilon$-bracketing number of $\mathcal D_m$ under the $L^2$ norm.''',[12],'Theorem 3.6 — bracketing-number notation',{'D15':'The brackets cover the signed-hinge integral class D_m under Lebesgue L2 distance.'},kind='source_passage',symbols=[r'N_{[\,]}(\epsilon,\mathcal D_m,\|\cdot\|_2)'],shape='Named bracketing-number functional from the statement. Its standard order-bracket meaning is ambient; the main text does not separately define endpoint measurability, almost-everywhere order or the open/closed width convention.')
add('D22','metric entropy',r'''The key step of our proof of Theorem 3.1 is to find an upper bound of the metric entropy of $\mathcal D_m$ (under the $L^2$ norm),''',[10],'Section 3.1 — metric-entropy terminology preceding Theorem 3.2',{'D15':'The entropy concerns the original signed-hinge integral class D_m.'},kind='source_passage',phrases=['metric entropy'],symbols=[r'N(\epsilon,\mathcal D_m,\|\cdot\|_2)'],shape='Metric entropy, represented by log N(epsilon,D_m,L2) in Theorem 3.2. The main text names the quantity but does not give a separate covering-number definition or center/radius convention. The mention of the proof of Theorem 3.1 is motivation and creates no statement dependency for that regression theorem.')

if __name__=='__main__':
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,status='extracted',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} original source passages and their local dependencies.')
