"""Restore original main-text definitions; source review is recorded separately."""
import json
from save_inventory import PID, ROOT
interfaces=[]
members={}
def add(n,term,s,pages,deps,symbols,description,heading,kind='definition',context=None,context_page=None):
    lid=f'D{n}'
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=[])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original naming context')])]
        kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='definition',type_shape=description,semantic_boundary=description,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))

add(1,'nonparametric regression model',r'''Consider a nonparametric regression model
\[
Y=f_0(X)+\varepsilon,
\]
(2.1)
where $X\in[0,1]^d$ is the $d$-dimensional covariate vector, and $\varepsilon$ is the noise variable satisfying
\[
\mathbb E[\varepsilon\mid X=x]=0\quad\text{and}\quad\mathbb E[|\varepsilon|^p\mid X=x]\leq v_p<\infty\text{ for all }x\in[0,1]^d.
\]
(2.2)''',[7],[],[r'Y=f_0(X)+\varepsilon'],'Additive regression on the unit cube with the stated conditional noise convention; iid sampling is retained separately as an auxiliary source passage. No Gaussian or uniform-design restriction is imposed here.','Section 2 — Nonparametric regression model (2.1)–(2.2)',kind='source_passage')
add(2,'Boundedness',r'''The random covariate vector $X\in\mathbb R^d$ follows some distribution $\mathbb P_X$ over the unit cube $[0,1]^d$. The regression function $f_0:[0,1]^d\to\mathbb R$ is uniformly bounded, i.e., $\|f_0\|_\infty:=\sup_{x\in[0,1]^d}|f_0(x)|\leq M$ for some $M\geq1$.''',[9],[],[r'\|f_0\|_\infty',r'\mathbb P_X'],'General supported design and bounded regression function; the lower-bound section later specializes to uniform design and M=1.','Condition 1 (Boundedness)',kind='condition',context='Condition 1 (Boundedness).')
add(3,'Moment conditions',r'''The noise variable $\varepsilon$ has zero mean and uniformly bounded (conditional) $p$-th moments for some $p\geq1$, that is,
\[
\mathbb E[\varepsilon\mid X=x]=0\quad\text{and}\quad\mathbb E[|\varepsilon|^p\mid X=x]\leq v_p<\infty\text{ for all }x\in[0,1]^d.
\]
(3.1)''',[9],[],[r'\mathbb E[|\varepsilon|^p\mid X=x]',r'p\geq1'],'Conditional mean zero and uniform absolute-moment bound. Theorem 3.3 explicitly strengthens the order to p>=2. Moment symbols in later bounds retain their standing meaning without changing the original condition.','Condition 2 (Moment conditions)',kind='condition',context='Condition 2 (Moment conditions).')
add(4,'Symmetric noise',r'''For each $x\in[0,1]^d$, the conditional distribution of $\varepsilon\mid X=x$ is symmetric around $0$. Moreover, there exists some constant $v_1>0$ such that
\[
\mathbb E[|\varepsilon|\mid X=x]\leq v_1\text{ for all }x\in[0,1]^d.
\]
(3.4)''',[10],[],[r'\varepsilon\mid X=x',r'v_1'],'Conditional symmetry and a finite first absolute moment; no second-moment condition is inserted into this source assumption.','Condition 3 (Symmetric noise)',kind='condition',context='Condition 3 (Symmetric noise).')
add(5,'smooth functions',r'''Let $\beta=r+s$ for some nonnegative integer $r$ and $0<s\leq1$, and $C>0$. A $d$-variate function $f$ is called $(\beta,C)$-smooth if for every sequence $\{\alpha_j\}_{j=1}^d$ of nonnegative integers such that $\sum_{j=1}^d\alpha_j=r$, the partial derivative $(\partial f)/(\partial x_1^{\alpha_1}\cdots\partial x_d^{\alpha_d})$ exists and satisfies for any $x,z\in\mathbb R^d$ that
\[
\left|\frac{\partial^rf}{\partial x_1^{\alpha_1}\cdots\partial x_d^{\alpha_d}}(x)-\frac{\partial^rf}{\partial x_1^{\alpha_1}\cdots\partial x_d^{\alpha_d}}(z)\right|\leq C\|x-z\|_2^s.
\]
(2.5)''',[7,8],[],[r'\beta=r+s',r'C\|x-z\|_2^s'],'Source Holder-type derivative condition on R^d, including r=0 and s=1. The prose numerator uses partial f while the display uses partial^r f; preserve both. No additional supremum bound on derivatives is invented.',r'Definition 2.1 ($(\beta,C)$-smooth function)',context=r'''We first revisit the class of $(\beta,C)$-smooth functions as follows.''',context_page=7)
add(6,'hierarchical composition model',r'''Given positive integers $d,l\in\mathbb N^+$ and a subset of $[1,\infty)\times\mathbb N^+$, denoted by $\mathcal P$, satisfying $\sup_{(\beta,t)\in\mathcal P}\max\{\beta,t\}<\infty$, the hierarchical composition model $\mathcal H(d,l,\mathcal P)$ is defined recursively as follows. For $l=1$,
\[
\begin{aligned}
\mathcal H(d,1,\mathcal P)=\{h:\mathbb R^d\to\mathbb R:{}&h(x)=g(x_{\pi(1)},\ldots,x_{\pi(t)}),\text{ where }\pi:[t]\to[d]\text{ and}\\
&g:\mathbb R^t\to\mathbb R\text{ is }(\beta,C)\text{-smooth for some }(\beta,t)\in\mathcal P,C>0\};
\end{aligned}
\]
and for $l>1$,
\[
\begin{aligned}
\mathcal H(d,l,\mathcal P)=\{h:\mathbb R^d\to\mathbb R:{}&h(x)=g(f_1(x),\ldots,f_t(x)),\text{ where }f_i\in\mathcal H(d,l-1,\mathcal P)\text{ and}\\
&g:\mathbb R^t\to\mathbb R\text{ is }(\beta,C)\text{-smooth for some }(\beta,t)\in\mathcal P,C>0\}.
\end{aligned}
\]''',[8],[5],[r'\mathcal H(d,l,\mathcal P)',r'\pi:[t]\to[d]'],'Recursive class with bounded smoothness/arity index set and arbitrary coordinate map, not necessarily an injection. Recursion at l-1 is internal to this definition, not a cyclic dependency edge. The source quantifies C inside the class formula.','Definition 2.2 (Hierarchical composition model)')
add(7,'dimension-adjusted smoothness',r'''\[
\gamma^*=\frac{\beta^*}{d^*}\quad\text{with}\quad(\beta^*,d^*)=\operatorname{argmin}_{(\beta,t)\in\mathcal P}\frac\beta t
\]
(2.6)
characterizes the dimension-adjusted smoothness of the least smooth (after dimension adjustment) component in the compositions.''',[8],[6],[r'\gamma^*',r'(\beta^*,d^*)'],'Least component smoothness-to-dimension ratio. The source writes argmin as a selected pair; attainment, nonemptiness and tie conventions are not added. Distinct from the minimax-risk definition in Definition 4.1.','Section 2 — Dimension-adjusted smoothness (2.6)')
add(8,'Huber loss',r'''Given some parameter $\tau\in(0,\infty]$, the Huber loss $\ell_\tau(\cdot)$ is defined as
\[
\ell_\tau(x)=\begin{cases}\frac12x^2&|x|\leq\tau\\\tau|x|-\frac12\tau^2&|x|>\tau\end{cases}.
\]
(2.7)
Note that the Huber loss is continuously differentiable with score function $\ell'_\tau(x)=\min\{\max(-\tau,x),\tau\}$. In particular, the Huber loss with $\tau=\infty$ coincides with the squared loss.''',[9],[],[r'\ell_\tau(x)',r'\tau=\infty'],'Piecewise quadratic-linear loss with tau=infinity allowed. The half factor differs from the normalization of the separate squared loss (2.3), even though the minimizers coincide.','Definition 2.3 (Huber Loss)')
add(9,'deep ReLU network',r'''A multilayer feedforward neural network with network architecture $(L,N)$ and the ReLU activation function can be written as
\[
f(x)=\mathcal L_{L+1}\circ\sigma\circ\mathcal L_L\circ\sigma\circ\mathcal L_{L-1}\circ\sigma\circ\cdots\circ\mathcal L_2\circ\sigma\circ\mathcal L_1(x),
\]
(2.10)
where $\mathcal L_i(x)=W_ix+b_i$ is a linear transformation with $W_i\in\mathbb R^{d_i\times d_{i-1}}$, $b_i\in\mathbb R^{d_i}$ and $(d_0,d_1,\cdots,d_L,d_{L+1})=(d,N,\cdots,N,1)$, and $\sigma:\mathbb R^{d_i}\to\mathbb R^{d_i}$ applies the ReLU function $\sigma(x)=\max\{0,x\}$ to each entry of an $\mathbb R^{d_i}$-valued vector. We refer to this type of networks as deep ReLU network with width $N$ and depth $L$, and $\{(W_i,b_i)\}_{i=1}^{L+1}$ are the network weights or parameters. Now we are ready to define the following two classes of network functions:
\[
\mathcal F_n(d,L,N)=\{f:\mathbb R^d\to\mathbb R\text{ is of the form (2.10) with width }N\text{ and depth }L\}
\]''',[9],[],[r'\sigma(x)=\max\{0,x\}',r'\mathcal F_n(d,L,N)',r'\mathcal L_i(x)=W_ix+b_i'],'Untruncated fully connected ReLU network, with L hidden ReLU stages and L+1 affine maps, common hidden width N and scalar output. The source calls its affine layer a linear transformation. No weight bound is imposed.','Section 2 — Deep ReLU network (2.10)')
add(10,'truncated ReLU neural networks',r'''\[
\mathcal F_n(d,L,N,M)=T_M\mathcal F_n(d,L,N)=\{f=T_Mg:g\in\mathcal F_n(d,L,N)\},
\]
where $T_M$ is the truncation operator at level $M>0$, defined as $T_Mu=\operatorname{sgn}(u)(|u|\wedge M)$.''',[9],[9],[r'\mathcal F_n(d,L,N,M)',r'T_Mu'],'Output truncation of the network class, distinct from a global bound on weights. Earlier upper bounds use M>=1; lower bounds use M=1. The approximation Theorems 4.5 and 4.6 only assert a deep network and do not gain a global output-range restriction.','Section 2 — Truncated ReLU neural networks',context=r'''where $\mathcal F_n(d,L,N,M)$ denotes the space of truncated ReLU neural networks with width $N$ (number of neurons per hidden layer), depth $L$ (number of layers), input dimension $d$ and a truncation parameter $M$.''')
add(11,'empirical Huber loss',r'''Given a robustification parameter $\tau=\tau_n>0$, consider the empirical Huber loss
\[
\widehat{\mathcal R}_\tau(f)=\frac1n\sum_{i=1}^n\ell_\tau(Y_i-f(X_i)).
\]
(2.8)''',[9],[1,8],[r'\widehat{\mathcal R}_\tau(f)'],'Empirical loss for the iid regression sample and chosen Huber parameter. Theorems explicitly also use its tau=infinity specialization.','Section 2 — Empirical Huber loss (2.8)')
add(12,'population risk',r'''For any $\tau\in(0,\infty]$, define the population risk under the Huber loss
\[
\mathcal R_\tau(f)=\mathbb E_{X,Y}\{\ell_\tau(Y-f(X))\}.
\]
(3.2)''',[10],[1,8],[r'\mathcal R_\tau(f)'],'Expected Huber loss under the regression law, distinguished from the empirical average and the ordinary squared-loss risk.','Section 3 — Population risk (3.2)')
add(13,'norm',r'''Our goal is to derive the rate of convergence for $\widehat f_n$ (2.9) under the $\|\cdot\|_2=\|\cdot\|_{L_2(\mathbb P_X)}$-norm, defined as $\|f\|_2=\sqrt{\mathbb E_{X\sim\mathbb P_X}|f(X)|^2}$.''',[10],[],[r'\|f\|_2',r'L_2(\mathbb P_X)'],'Population L2 norm of a scalar function, not the empirical norm or its square. The design law is a parameter; the lower bounds separately choose the uniform law. Euclidean vector norms elsewhere are ambient, not this function norm.','Section 3 — Population norm')
add(14,'measurable functions',r'''Denote by $\Theta$ the set of all measurable functions $f:[0,1]^d\to\mathbb R$ satisfying $\|f\|_\infty\leq M$ for the same $M\geq1$ as in Condition 1.''',[10],[2],[r'\Theta',r'\|f\|_\infty\leq M'],'Bounded measurable comparison class for population minimization, using the same radius as Condition 1. It is not restricted to neural networks.','Section 3.1 — Measurable functions')
add(15,'global minimizer',r'''Let $f_{0,\tau}$ be the global minimizer of the population Huber risk, i.e.,
\[
f_{0,\tau}\in\operatorname{argmin}_{f\in\Theta}\mathcal R_\tau(f).
\]
(3.7)''',[11],[12,14],[r'f_{0,\tau}',r'\operatorname{argmin}_{f\in\Theta}'],'A selected population Huber minimizer over bounded measurable functions, not the original regression function when noise is asymmetric. Existence, uniqueness and representative conventions are source-level qualifications.','Section 3.1 — Global minimizer (3.7)')
# Reuse verbatim portions of the saved transcription for definitions inside Theorems.
from save_inventory import STATEMENTS,NUMBERS
THEOREMS=dict(zip(NUMBERS,STATEMENTS))
def excerpt(num,start,end):
    s=THEOREMS[num];i=s.index(start);j=s.index(end,i)
    return s[i:j].strip()
add(16,'approximate empirical risk minimizers',excerpt('3.3',r'Let $\mathcal S_{n,\tau}(\delta)$','Then, there exists'),[11],[10,11],[r'\mathcal S_{n,\tau}(\delta)',r'+\delta^2'],'Upper-bound approximate minimizer set with a squared objective tolerance. Theorem 3.7 writes S(delta) without n,tau subscripts; preserve that notation and document the local correspondence.','Theorem 3.3 — Approximate empirical risk minimizers',kind='theorem_excerpt')
add(17,'intrinsic dimension-adjusted smoothness',r'''We say a class $\mathcal F$ of functions $\{f:\mathbb R^d\to\mathbb R\}$ has an intrinsic dimension-adjusted smoothness upper bounded by $\alpha$ if the minimax $L_2$ risk over this function class is lower bounded by $n^{-\frac{2\alpha}{2\alpha+1}}$ up to a constant, that is,
\[
\liminf_{n\to\infty}\inf_{\widehat f_n}\sup_{f_0\in\mathcal F}n^{\frac{2\alpha}{2\alpha+1}}\mathbb E[\|\widehat f_n-f_0\|_2^2]>0,
\]
where the infimum is taken over all estimators constructed from the i.i.d. sample $\{(X_i,Y_i)\}_{i=1}^n$ satisfying $Y_i=f_0(X_i)+\varepsilon_i$ with $\varepsilon_i\sim N(0,1)$ and $X_i\sim\operatorname{Uniform}([0,1]^d)$.''',[17],[1,13],[r'\liminf_{n\to\infty}',r'n^{\frac{2\alpha}{2\alpha+1}}'],'A property defined through a Gaussian-experiment minimax risk lower bound; not a derivative regularity assumption. Its infimum ranges over all estimators, unlike the existence event over approximate neural network estimators in Theorems 4.1 and 4.2.','Definition 4.1 (Intrinsic dimension-adjusted smoothness)')
add(18,'data generating processes',excerpt('4.1','Define the family',r'Let $\mathcal S^{\mathrm{HN}}'),[18],[1],[r'\mathcal U(d,p,\mathcal F)',r'\mathbb E[|\varepsilon|^p\mid X]\leq1'],'Lower-bound experiment family specialized to uniform design and moment bound one. The generic argument F is replaced by F0 in the theorem suprema. No derivative smoothness is imposed by this family itself.','Theorem 4.1 — Data generating processes (4.2)',kind='theorem_excerpt')
add(19,'approximate Huber ReLU-DNN estimates',excerpt('4.1',r'Let $\mathcal S^{\mathrm{HN}}','Then, there exists'),[18],[10,11,15],[r'\mathcal S^{\mathrm{HN}}_{n,\tau}(\delta)',r'n^{-100}'],'Lower-bound set with two alternative eligibility branches, one involving comparison to the population Huber minimizer. It is distinct from S_n,tau(delta), and the lower theorem asserts existence of a bad member rather than that every member is bad.','Theorem 4.1 — Approximate Huber ReLU-DNN estimates (4.3)',kind='theorem_excerpt')
add(20,'sub-hypercubes',excerpt('4.5','For any given','Then, there exist'),[23],[],[r'Q_\alpha(\Delta)',r'\mathbf1_{\{\alpha_i<K\}}\Delta'],'Source coordinate regions with one-sided gaps except at the last coordinate index. Theorem 4.6 uses Q_alpha(Delta1) and their union. Dimension, grid size and tolerance are bound here; no global output restriction on the fitted networks is implied.','Theorem 4.5 — Sub-hypercubes (4.8)',kind='theorem_excerpt',context=r'''The next theorem claims that a ReLU neural network with depth $\bar L$ and width $\bar N$ can fit any piecewise constant function in $(\bar N\bar L)^2$ sub-hypercubes.''')
add(21,'depth and width',excerpt('3.5','Consider the neural network class','Moreover, let'),[14],[6,10],[r'\bar L=c_3\lceil L\log L\rceil',r'\bar N=c_4\lceil N\log N\rceil'],'Logarithmically enlarged architecture used by Theorems 3.5–3.7. The source identifies c3,c4 via the composition-class approximation proposition; its constant dependence is preserved as auxiliary context, not as an extra theorem conclusion.','Theorem 3.5 — Depth and width (3.15)',kind='theorem_excerpt')

# Source-inspected rendering amendment; see the explicit saved review plan.
members['D13']['highlight_symbols'] = ['\\|f\\|_2', '\\|\\cdot\\|_{L_2(\\mathbb P_X)}']
members['D16']['highlight_symbols'] = ['\\mathcal S_{n,\\tau}(\\delta)', '\\delta^2']

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    for name,data in [('source-passages.json',dict(paper_id=PID,status='extracted',scope='Original main-text source passages; full source review is a separate gate.',source_passages=list(members.values()))),('interface-extraction.json',dict(paper_id=PID,status='extracted',interfaces=interfaces))]:
        (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(members)} source entries; final validation is separate.')
if __name__=='__main__':main()
