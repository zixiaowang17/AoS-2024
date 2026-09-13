"""Preserve original Gaussian-approximation definitions and source conditions."""
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
add(1,'norm',r'''For a random variable $Y$, write $Y\in L^p$, $p>0$, if $\|Y\|_p:=\mathbb E(|Y|^p)^{1/p}<\infty$. For $L^2$ norm write $\|\cdot\|=\|\cdot\|_2$.''',[4],[],[r'\|Y\|_p',r'\|\cdot\|=\|\cdot\|_2'],'Lp random-variable norm; the un-subscripted norm in Conditions2.3–2.4 is L2, and its square is the second moment.','Section 1.2 — Moment norms')
add(2,'causal representation',r'''To characterize the non-stationary process $(X_t)$, we view $X_t$ as outputs from a physical system with the following causal representation:
\[
X_t=g_t(\mathcal F_t),\quad\text{with }\mathcal F_t=(\ldots,\varepsilon_{t-1},\varepsilon_t),
\]
(1.2)
where $(\varepsilon_i)_{i\in\mathbb Z}$ are i. i. d. inputs of this system and $g_t:\mathbb R^\infty\to\mathbb R$ are measurable functions.''',[2],[],[r'X_t=g_t(\mathcal F_t)',r'\mathcal F_t'],'Time-dependent measurable causal maps of a two-sided iid innovation sequence. Maps may vary with t; no stationarity or smooth temporal variation is imposed. Mean zero is the separate Section2.2 convention archived in ambient context.','Section 1 — Nonstationary causal representation (1.2)')
add(3,'partial sums',r'''$S_i:=\sum_{j=1}^iX_j$''',[2],[],[r'S_i'],'Uncentered sum notation; Xi are mean zero in the approximation results. In T4.1 the inherited approximation is applied to noise Zi, so S_i there is the noise sum, not the noncentered observations.','Section 1 — Partial sums',context='blocks of partial sums',context_page=3)
add(4,'common, possibly enriched probability space',r'''Note that in principle such Gaussian approximations for random variables $(X_i)_{i=1}^n$ require a common, possibly enriched probability space $(\Phi_c,\mathcal A_c,\mathbb P_c)$ on which the approximating Gaussian processes and random variables $(X_i^c)_{1\le i\le n}=_{\mathcal D}(X_i)_{1\le i\le n}$ can be defined. In order for better readability, we omit this technicality and simply state our results in terms of the original random variables $X_i$’s.''',[4,5],[],[r'(X_i^c)_{1\le i\le n}=_{\mathcal D}(X_i)_{1\le i\le n}'],'Existence of a coupling with an equal-joint-law copy on an enriched space. Not an independent Gaussian on the original probability space or an asserted almost-sure approximation.','Section 2 — Gaussian coupling convention',kind='source_passage')
add(5,'uniform functional dependence',r'''With this system, given $k\ge0$, a time lag, we measure the dependence from how much the outputs $X_i$ of this system will change if we replace the input information at time $i-k$ with an i.i.d. copy $\varepsilon'_{i-k}$. For $p\ge1$, define the uniform functional dependence
\[
\delta_p(k):=\sup_i(\mathbb E|X_i-X_{i,\{i-k\}}|^p)^{1/p},\quad\text{where }X_{i,\{i-k\}}=g_i(\ldots,\varepsilon_{i-k-1},\varepsilon'_{i-k},\varepsilon_{i-k+1},\ldots,\varepsilon_i)
\]
(2.3)
is a coupled version of $X_i$.''',[5],[1,2],[r'\delta_p(k)',r'X_{i,\{i-k\}}'],'Replace one innovation by an independent copy and take the Lp difference uniformly over time. Not a mixing coefficient or replacement of the whole past.','Section 2.2 — Functional dependence (2.3)')
add(6,'dependence condition',r'''we will express our dependence condition in terms of
\[
\Theta_{i,p}=\sum_{k=i}^\infty\delta_p(k),\quad i\ge0.
\]
(2.4)''',[6],[5],[r'\Theta_{i,p}'],'Tail sum of uniform functional-dependence coefficients, not a single-lag coefficient.','Section 2.2 — Cumulative dependence (2.4)')
add(7,'uniform dependency-adjusted norm',r'''Consider (1.2). Suppose that $\Theta_{0,p}<\infty$ for some $p>2$. Assume there exists $A>1$ and constant $C>0$, such that the uniform dependency-adjusted norm
\[
\mu_{p,A}:=\sup_{i\ge0}(i+1)^A\Theta_{i,p}\le C<\infty.
\]
(2.5)''',[6],[2,6],[r'\mu_{p,A}',r'(i+1)^A\Theta_{i,p}'],'Uniform polynomial decay of dependence tails. Theorem-specific A cutoffs are separate. The p>4 branch of T3.1 also uses this norm at moment order4.','Condition 2.1',kind='condition')
add(8,'truncated uniform integrability condition',r'''For the same $p$ as in Condition 2.1, the series $(|X_i|^p)$ satisfies the truncated uniform integrability condition:
For any fixed $a>0$, $\sup_i\mathbb E(|X_i|^p\mathbb I_{\{|X_i|^p\ge an\}})\to0$ as $n\to\infty$.''',[6],[1],[r'\sup_i\mathbb E(|X_i|^p\mathbb I_{\{|X_i|^p\ge an\}})'],'Printed supremum over i with truncation an for every fixed a>0. Keep the p parameter shared with Condition2.1 without adding decay as a dependency of integrability itself. The source’s claim that this is weaker than classical UI is recorded separately.','Condition 2.2',kind='condition')
add(9,'non-singularity condition',r'''For all sequences $(m_n)\in\mathbb N$ with $m_n\to\infty$ and $m_n<n$, the process $(X_i)$ satisfies that $\lim_{n\to\infty}\min_{1\le i\le n-m_n}\|X_i+\ldots+X_{i+m_n}\|^2=\infty$.''',[6],[1],[r'\|X_i+\ldots+X_{i+m_n}\|^2'],'Uniform divergence of every increasing-block second moment, with m_n+1 terms as printed. No linear-in-length lower bound is asserted.','Condition 2.3',kind='condition',context='This non-singularity condition is a very natural one.',context_page=6)
add(10,'truncated partial sum process',r'''\[
S_i^\oplus:=\sum_{j=1}^i(X_j^\oplus-\mathbb E(X_j^\oplus)),\quad\text{where }X_i^\oplus=T_{n^{1/p}}(X_i),\quad i=1,\ldots,n,
\]
(2.6)
with $T_b(w)=\max\{\min\{w,b\},-b\}$.''',[6],[],[r'S_i^\oplus',r'X_i^\oplus',r'T_b(w)'],'Winsorization at n^(1/p) followed by explicit centering in the partial sums. Covariance matching in T2.2 uses winsorized variables; its approximation still targets the original partial sums.','Section 2.3 — Truncation (2.6)',context='we begin by presenting a Gaussian approximation for the truncated partial sum process',context_page=6)
add(11,'non-singularity condition',r'''The series $(X_i)$ satisfies the following condition: There exists a constant $c>0$ and $l_0\in\mathbb N$, such that for all $l\ge l_0$, $\min_{1\le j\le n-l+1}\|X_j+\ldots+X_{j+l-1}\|^2/l\ge c$.''',[7],[1],[r'\|X_j+\ldots+X_{j+l-1}\|^2/l\ge c'],'Uniform linear lower bound on block second moments, stronger than Condition2.3. The printed range leaves l≤n implicit; empty minima are not assigned invented values.','Condition 2.4',kind='condition',context='Finally, if one were to assume non-singularity condition as written below',context_page=7)
add(12,'decay rate condition',r'''\[
A>A_0:=\max\left\{\frac{p^2-p-2+(p-2)\sqrt{p^2+10p+1}}{4p},1\right\}.
\]
(2.7)''',[7],[],[r'A_0',r'\sqrt{p^2+10p+1}'],'A0 cutoff for T2.2 and T2.4, inherited on noise by T4.1. Distinct from A0-prime and the weaker A>1 in T3.1–T3.2.','Theorem 2.2 — Decay cutoff (2.7)',kind='theorem_excerpt',context='we are also able to improve the decay rate condition',context_page=7)
add(13,'decay rate condition',r'''\[
A>A'_0:=\max\left\{\frac{p^2-4+(p-2)\sqrt{p^2+20p+4}}{8p},1\right\}.
\]
(2.10)''',[7],[],[r"A'_0",r'\sqrt{p^2+20p+4}'],'Improved cutoff paired with the stronger Condition2.4 in T2.3 and T2.5; not interchangeable with A0.','Theorem 2.3 — Decay cutoff (2.10)',kind='theorem_excerpt',context='we are also able to improve the decay rate condition',context_page=7)
add(14,'Quadratic large deviation bounds',r'''Let $Q_n=\sum_{1\le s\le t\le n}a_{s,t}X_sX_t$, with $a_{s,t}=0$ if $|s-t|>D_n$ for some $D_n\le n$, and $\sup|a_{s,t}|\le1$. Denote
\[
R_k=\sum_{j=1}^k(V_j-\mathbb E(V_j)),\quad\text{where }V_k=\sum_{t=(k-1)D_n+1}^{(kD_n)\wedge n}\sum_{1\le s\le t}a_{s,t}X_sX_t,\quad\text{for }1\le k\le\lceil n/D_n\rceil.
\]
(3.3)''',[11],[],[r'Q_n',r'R_k',r'V_k'],'Banded upper-triangular quadratic form, partitioned by its terminal index and centered blockwise. D_n is a positive integer bandwidth for these sums, though the statement only explicitly prints D_n≤n. R_k is distinct from the earlier residual block sum R_j.','Theorem 3.1 — Banded quadratic partial sums',kind='theorem_excerpt',context='Quadratic large deviation bounds have a long history that started with the seminal work by Hanson and Wright [47] and Wright [100].',context_page=11)
add(15,'block length',r'''In particular, with $m\asymp n^{\zeta_1}$, where $\zeta_1=\min\{1,2-4/p\}/(1+2A)$, (3.9) implies''',[13],[],[r'\zeta_1=\min\{1,2-4/p\}/(1+2A)'],'The numeric exponent used in T3.2; its definition comes from balancing BRV bias and stochastic error. T3.2 does not assume that an empirical BRV estimator is supplied.','Section 3.2 — Block exponent',context=r'Usually the block length $m$ is taken so as $m\to\infty$ with $m/n\to0$.',context_page=11)
add(16,'signal-plus-noise model',r'''Consider
\[
X_i=\mu(t_i)+Z_i,\quad i=1,\ldots,n,
\]
(4.6)
where $\mu(\cdot)\in C^3[0,1]$.''',[15],[],[r'X_i=\mu(t_i)+Z_i'],'Observed signal-plus-noise data. The Gaussian approximation assumptions apply to centered noise Zi, not observations Xi with a varying mean.','Section 4.2 — Trend model (4.6)',context='a time-varying signal-plus-noise model',context_page=15)
add(17,'grid',r'''Let $0=t_0<t_1<t_2<\ldots<t_{n-1}<t_n<t_{n+1}=1$ be an $n$-length grid on $[0,1]$.
Here we let $t_i=F^{-1}(i/n)$, where $F(t)=\int_0^tf(u)\,du$ for some density $f\in C^3[0,1]$.''',[15],[],[r't_i=F^{-1}(i/n)',r'F(t)=\int_0^tf(u)\,du'],'Deterministic quantile design from a smooth density. The printed strict endpoint grid conflicts with t_n=F^-1(1)=1; retain both passages and flag the endpoint convention.','Section 4.2 — Design grid')
add(18,'smooth symmetric kernel',r'''Assume that $K$ is a smooth symmetric kernel with bounded support $[-\omega,\omega]$, satisfying:
\[
\int_{\mathbb R}\Psi_K(u;\delta)\,du=O(\delta)\text{ as }\delta\to0,\quad\text{where }\Psi_K(u;\delta)=\sup\{|K(y)-K(u)|:|y-u|\le\delta\}.
\]
(4.9)''',[15],[],[r'\Psi_K(u;\delta)',r'[-\omega,\omega]'],'Smooth symmetric compactly supported kernel with integrated modulus condition. Normalization and denominator nondegeneracy are customary but not separately stated in this passage.','Section 4.2 — Kernel assumption (4.9)',kind='assumption')
add(19,'local linear estimate',r'''Define
\[
S_j(t)=\sum_{i=1}^n(t-t_i)^jK((t-t_i)/h_n).
\]
(4.7)
Theorem 4.1 below provides a Gaussian approximation for the local linear estimate
\[
\widehat\mu_{h_n}(t):=\sum_{i=1}^nw_{h_n}(t,i)X_i,\quad\text{where }w_{h_n}(t,i)=K\left(\frac{t-t_i}{h_n}\right)\frac{S_2(t)-(t-t_i)S_1(t)}{S_2(t)S_0(t)-S_1^2(t)}.
\]
(4.8)''',[15],[16,17,18],[r'\widehat\mu_{h_n}(t)',r'w_{h_n}(t,i)',r'S_j(t)'],'Local linear smoother using deterministic design and kernel moments. S_j(t) denotes weighted design moments, distinct from stochastic partial sums S_i. Same weights are applied to the Gaussian noise in T4.1.','Section 4.2 — Local linear estimator (4.7)–(4.8)')
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
