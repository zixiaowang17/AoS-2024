"""Preserve original ridge-bandit definitions, assumptions and algorithms."""
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
add(1,'sequential estimation problem',r'''In this paper, we study a sequential estimation problem as follows. At each time $t=1,2,\cdots,T$, the learner chooses an action $a_t$ in a generic action set $\mathcal A$, based on the observed history $\mathcal H_{t-1}=\{(a_s,r_s)\}_{s\le t-1}$. Upon choosing $a_t$, the learner obtains a noisy observation of $f_{\theta^*}(a_t)$, denoted as $r_t=f_{\theta^\star}(a_t)+z_t$, where $\{f_\theta:\mathcal A\to\mathbb R\}_{\theta\in\Theta}$ is a given function class, and the noise $z_t$ follows a standard normal distribution. Here $\theta^\star\in\Theta\subseteq\mathbb R^d$ is an unknown parameter fixed across time, and the learner's target is to estimate the parameter $\theta^\star$ in the high dimensional regime where $d$ could be comparable to $T$. Here the learner needs to both design the sequential experiment (i.e. actions $a_1,\cdots,a_T$) adapted to the history $\{\mathcal H_{t-1}\}_{t=1}^T$, and output a final estimator $\widehat\theta_T=\widehat\theta_T(\mathcal H_T)$ which is close to $\theta^\star$.''',[3],[],[r'\mathcal H_{t-1}=\{(a_s,r_s)\}_{s\le t-1}',r'r_t=f_{\theta^\star}(a_t)+z_t'],'Sequential noisy observation experiment with a fixed unknown parameter and history-adapted actions. Standard normal observation noise is printed; fresh independent query noise is used by the algorithms. Theorem5 replaces reward observations by an oracle transcript and Theorem11 restricts adaptation. These are explicit model variants, not additional simultaneous observation channels.','Section 1 — Sequential observation experiment',kind='source_passage')
add(2,'ridge functions',r'''The mean reward is given by $f_{\theta^\star}(a)=f(\langle\theta^\star,a\rangle)$, where $f:[-1,1]\to[-1,1]$ is a known link function.''',[3],[],[r'f_{\theta^\star}(a)=f(\langle\theta^\star,a\rangle)',r'f:[-1,1]\to[-1,1]'],'Single-index ridge mean function. The source’s default link is known; Theorem10 explicitly overrides this information assumption while retaining the same mean/noise experiment. Unit-sphere parameters and unit-ball actions are original adjacent context, not part of the abstract ridge-function formula; Theorems12/13 change those domains explicitly.','Section 1 — Ridge mean reward',context=r'Throughout this paper, we are interested in both the estimation and regret minimization problems for the class of ridge functions [LS75]. More specifically, we assume that:')
members['D2']['naming_context'].append(dict(context_id='D2/geometry',text=r'''1. The parameter set $\Theta=\mathbb S^{d-1}=\{\theta\in\mathbb R^d:\|\theta\|_2=1\}$ is the unit sphere in $\mathbb R^d$;
2. The action set $\mathcal A=\mathbb B^d=\{a\in\mathbb R^d:\|a\|_2\le1\}$ is the unit ball in $\mathbb R^d$;''',evidence=[dict(page=3,location='Default geometry immediately before ridge mean definition')]))
add(3,'Sample Complexity for Estimation',r'''For a given link function $f$, dimensionality $d$, and $\varepsilon\in(0,1/2]$, the sample complexity of estimating $\theta^\star$ within accuracy $\varepsilon$ is defined as
\[
T^\star(f,d,\varepsilon)=\min\left\{T:\inf_{\widehat\theta_T\in\mathbb S^{d-1}}\sup_{\theta^\star\in\mathbb S^{d-1}}\mathbb E_{\theta^\star}[1-\langle\widehat\theta_T,\theta^\star\rangle]\le\varepsilon\right\},
\]
(1)
where the infimum is taken over all possible actions $a^T$ adapted to $\{\mathcal H_{t-1}\}_{t=1}^T$ and all possible estimators $\widehat\theta_T=\widehat\theta_T(\mathcal H_T)$.''',[3,4],[1,2],[r'T^\star(f,d,\varepsilon)',r'1-\langle\widehat\theta_T,\theta^\star\rangle'],'Minimax expected signed-correlation loss with a unit-sphere estimator and parameter, jointly optimizing experiment and estimator. This is not a high-probability success criterion or sign-invariant loss. Even-link sign identifiability and the later use of accuracy1-epsilon outside the printed domain remain explicit source issues.','Definition 1 — Sample Complexity for Estimation',context='Definition 1 (Sample Complexity for Estimation).')
add(4,'regret',r'''\[
\mathfrak R_T(\Theta,\mathcal A)=\mathbb E_{\theta^\star}\left[T\cdot\max_{a^\star\in\mathcal A}f_{\theta^\star}(a)-\sum_{t=1}^T f_{\theta^\star}(a_t)\right].
\]''',[3],[1],[r'\mathfrak R_T(\Theta,\mathcal A)',r'\sum_{t=1}^T f_{\theta^\star}(a_t)'],'Expected cumulative mean-reward shortfall for a fixed parameter and policy. The general display prints free a under a max over a-star; retain this variable mismatch. Definition2 supplies the correctly bound ridge specialization. Theorem13 changes the parameter space for the minimax version, not the comparator/reward mechanism.','Section 1 — Expected cumulative regret',context=r'In addition to estimating parameter $\theta^\star$, another common target of the learner is to maximize the expected cumulative reward $\mathbb E[\sum_{t=1}^T r_t]$, or equivalently, to minimize the regret defined as')
add(5,'Minimax Regret',r'''For a given link function $f$, dimensionality $d$, and time horizon $T$, the minimax regret is defined as
\[
\mathfrak R_T^\star(f,d)=\inf_{a^T}\sup_{\theta^\star\in\mathbb S^{d-1}}\mathbb E_{\theta^\star}\left[T\cdot\max_{a^\star\in\mathcal A}f(\langle\theta^\star,a^\star\rangle)-\sum_{t=1}^T f(\langle\theta^\star,a_t\rangle)\right],
\]
(2)
where the infimum is taken over all possible actions $a^T$ adapted to $\{\mathcal H_{t-1}\}_{t=1}^T$.''',[4],[1,2,4],[r'\mathfrak R_T^\star(f,d)',r'\sup_{\theta^\star\in\mathbb S^{d-1}}'],'Minimax cumulative regret over sphere parameters and adaptive policies, with unit-ball actions by the standing model. Theorem6’s achieved regret is an upper bound on this infimum; its notation should not be read as equality with every algorithm’s regret. Theorem13 has a separate unit-ball variant D24.','Definition 2 — Minimax Regret',context='Definition 2 (Minimax Regret).')
add(6,'Burn-in Cost',r'''For a given link function $f$ and dimensionality $d$, the burn-in cost is defined as
\[
T^\star_{\mathrm{burn\text{-}in}}(f,d)=T^\star(f,d,1/2),
\]
where $T^\star$ is the sample complexity defined in Definition 1.''',[6],[3],[r'T^\star_{\mathrm{burn\text{-}in}}(f,d)',r'T^\star(f,d,1/2)'],'Constant-accuracy specialization of the expected signed-correlation minimax sample complexity. Preserve the exact1/2 target; high-probability algorithmic guarantees are related upper bounds, not this definition itself.','Definition 3 — Burn-in Cost',context='Definition 3 (Burn-in Cost).')
add(7,'Learning trajectory',r'''For a given link function $f$, dimensionality $d$, and $\varepsilon\in(0,1/2]$, the burn-in cost for achieving $\varepsilon$ inner product is defined as
\[
T^\star_{\mathrm{burn\text{-}in}}(f,d,\varepsilon)=T^\star(f,d,1-\varepsilon),
\]
where $T^\star$ is the sample complexity defined in Definition 1. We will call the function $\varepsilon\mapsto T^\star_{\mathrm{burn\text{-}in}}(f,d,\varepsilon)$ as the minimax learning trajectory during the burn-in period.''',[8],[3],[r'T^\star(f,d,1-\varepsilon)',r'\varepsilon\mapsto T^\star_{\mathrm{burn\text{-}in}}(f,d,\varepsilon)'],'Expected-correlation sample complexity indexed by the target inner product. Definition1 states accuracy at most1/2, whereas this formula calls it at1-epsilon; preserve the implicit-domain-extension discrepancy. It differs from the pathwise Bayes statement of Theorem8.','Definition 4 — Learning trajectory',context='Definition 4 (Learning trajectory).')
add(8,'Regularity conditions for the burn-in period',r'''We assume that the link function $f$ satisfies the following conditions:
1. Normalized scale: $f(0)=0$, $f(1)=1$, and $|f|\le1$;
2. Monotonicity: either (i) $f$ is increasing on $[-1,1]$; or (ii) $f$ is even and increasing on $[0,1]$.''',[6],[],[r'f(0)=0',r'f(1)=1','Monotonicity: either (i)'],'Complete Assumption1, including scale and its alternative monotonicity branches. Increasing is not silently strengthened to strictly increasing or differentiable. Even links make theta and minus theta observationally indistinguishable under the signed loss; preserve this issue rather than changing the loss or excluding the branch.','Assumption 1 — Regularity conditions for the burn-in period',kind='assumption',context='Assumption 1 (Regularity conditions for the burn-in period).')
add(9,'Regularity conditions for the learning phase',r'''The link function $f$ is differentiable and locally linear on some interval $[1-\gamma,1]$ around 1:
\[
c_f\le\min_{x\in[1-\gamma,1]}f'(x)\le\max_{x\in[1-\gamma,1]}f'(x)\le C_f,
\]
(7)
where $f'$ is the derivative of $f$.''',[11],[],[r'[1-\gamma,1]',r'c_f\le\min_{x\in[1-\gamma,1]}f\prime(x)'],'Local derivative bounds near1, not a global lower slope bound. Positivity and range conventions for c_f,C_f,gamma are used by the theorems but not fully quantified in the printed assumption; retain the source and record the intended positive local scale separately. No Assumption1 is included automatically.','Assumption 2 — Regularity conditions for the learning phase',kind='assumption',context='Assumption 2 (Regularity conditions for the learning phase).')
members['D9']['highlight_symbols']=[r'[1-\gamma,1]',r"c_f\le\min_{x\in[1-\gamma,1]}f'(x)"]
add(10,'Lower bound regularity condition',r'''The function $f$ is $L$-Lipschitz on $[-1,1]$, i.e. $|f(x)-f(y)|\le L|x-y|$.''',[12],[],[r'|f(x)-f(y)|\le L|x-y|'],'Global finite-L Lipschitz condition on the entire link domain. Theorems4/5 state Lipschitzness without fixing a numerical L; Theorem7 names Assumption3 and allows its lower-bound constant to depend on L. This does not imply a positive lower derivative near zero.','Assumption 3 — Lower bound regularity condition',kind='assumption',context='Assumption 3 (Lower bound regularity condition).')
add(11,'least squares estimate',r'''In the Eluder-UCB algorithm specialized to ridge bandits, at each time $t$ the learner computes the least squares estimate of $\theta^\star$ based on the past history:
\[
\widehat\theta_t^{\mathrm{LS}}:=\operatorname*{arg\,min}_{\theta\in\mathbb S^{d-1}}\sum_{s<t}(r_s-f(\langle\theta,a_s\rangle))^2.
\]''',[9],[1,2],[r'\widehat\theta_t^{\mathrm{LS}}',r'\sum_{s<t}'],'Sphere-constrained least-squares fit to past observations for Eluder-UCB. It is distinct from Algorithm4’s cap-constrained final least-squares fit. Nonuniqueness and measurable selection remain conventional; Theorem4 separately quantifies an adverse action tie-breaking rule.','Section 1.3.1 — Eluder-UCB least squares')
add(12,'confidence set',r'''\[
\mathbb C_t=\left\{\theta\in\mathbb S^{d-1}:\sum_{s<t}\left(f(\langle a_s,\theta\rangle)-f(\langle a_s,\widehat\theta_t^{\mathrm{LS}}\rangle)\right)^2\le\mathrm{Est}_t\right\},
\]
(4)
where $\mathrm{Est}_t\asymp d$ is an upper bound on the estimation error and known to the learner.''',[9],[2,11],[r'\mathbb C_t',r'\mathrm{Est}_t\asymp d'],'Prediction-discrepancy confidence set centered on the least-squares fit, with a known estimation-error budget hiding polylogarithms. No specific budget formula or universal tie-breaking convention is invented.','Section 1.3.1 — Eluder-UCB confidence set (4)',context=r'Then using standard theory of least squares, one can show that the true parameter $\theta^\star$ belongs to the following confidence set $\mathbb C_t$ with high probability:')
add(13,'Eluder-UCB algorithm',r'''the Eluder-UCB algorithm chooses the action
\[
a_t\in\operatorname*{arg\,max}_{a\in\mathcal A}\max_{\theta\in\mathbb C_t}f(\langle a,\theta\rangle).
\]
(El-UCB)
If there are ties, they can be broken in an arbitrary manner.''',[9,10],[1,2,12],[r'\operatorname*{arg\,max}_{a\in\mathcal A}',r'\mathbb C_t'],'Optimistic action maximization over the source confidence set. Theorem4 asserts existence of a tie-breaking rule causing its lower bound, not that every possible tie-breaking rule has that performance.','Section 1.3.1 — Eluder-UCB action rule')
add(14,'Online regression oracle',r'''Online regression oracle: the oracle outputs $\widehat\theta_t$ at the beginning of time $t$ which satisfies
\[
\sum_{s\le t}\left(f(\langle\theta^\star,a_s\rangle)-f(\langle\widehat\theta_s,a_s\rangle)\right)^2\le\mathrm{Est}^{\mathrm{On}}_t
\]
(5)
with high probability, where $\mathrm{Est}^{\mathrm{On}}_t\asymp d$ is a known quantity.''',[10],[2],[r'\widehat\theta_s',r'\mathrm{Est}^{\mathrm{On}}_t'],'Online prediction guarantee using the sequence of outputs at the start of each round, not a single final fit. Theorem5 selects an improper oracle of this kind. The notation f(inner product) for outputs outside the sphere requires a domain convention not specified in the main text.','Section 1.3.2 — Online regression oracle (5)')
add(15,'Offline regression oracle',r'''Offline regression oracle: the oracle outputs $\widehat\theta_t$ at the end of time $t$ which satisfies
\[
\sum_{s\le t}\left(f(\langle\theta^\star,a_s\rangle)-f(\langle\widehat\theta_t,a_s\rangle)\right)^2\le\mathrm{Est}^{\mathrm{Off}}_t
\]
(6)
with high probability, where $\mathrm{Est}^{\mathrm{Off}}_t\asymp d$ is a known quantity.''',[10],[2],[r'\widehat\theta_t',r'\mathrm{Est}^{\mathrm{Off}}_t'],'Offline guarantee comparing every past action against one current output at the end of the round. Theorem5 selects a proper sphere-valued oracle of this kind; this is distinct from the online improper alternative.','Section 1.3.2 — Offline regression oracle (6)')
add(16,'oracle model',r'''Under the oracle model, instead of observing $(a_1,r_1,a_2,r_2,\cdots)$, the learner only observes $(a_1,\widehat\theta_1,a_2,\widehat\theta_2,\cdots)$, where the learner has no control over $\{\widehat\theta_t\}$ except for the error bound (5) or (6).''',[10],[1,14,15],[r'(a_1,\widehat\theta_1,a_2,\widehat\theta_2,\cdots)'],'Alternative transcript model receiving regression-oracle outputs instead of raw rewards. Equations5 and6 resolve two alternatives, not a requirement to satisfy both simultaneously. Theorem5 quantifies existence of adverse oracle choices, then every learner using that oracle model.','Section 1.3.2 — Oracle transcript model',kind='source_passage')
members['D16']['naming_context']=[dict(context_id='D16/propriety',text=r'The exact statement is summarized in the next theorem, where we call an oracle “proper” if we require that $\widehat\theta_t\in\mathbb S^{d-1}$ for every $t$, and “improper” otherwise.',evidence=[dict(page=10,location='Proper versus improper oracle convention immediately before Theorem5')])]
add(17,'Iterative direction search algorithm',r'''1 Input: link function $f$, dimensionality $d$, a noisy oracle $\mathcal O:a\in\mathbb B^d\mapsto\mathcal N(f(\langle\theta^\star,a\rangle),1)$, error probability $\delta$, target inner product $x_0\in(0,1)$.
2 Output: an action $a_0$ such that $\langle\theta^\star,a_0\rangle\ge x_0$ with probability at least $1-\delta$.
3 Let numerical constants $(\kappa_1,\kappa_2,c_0,d_0)$ be given in Theorem 9.
4 Let $m\leftarrow\lceil x_0^2d\rceil$, $V\leftarrow\{0_d\}$, $L\leftarrow2m\log(2m/\delta)/c_0$.
// Find initial few directions
5 for epoch $i=1,\cdots,d_0$ do
6     while True do
7         Sample $v\sim\operatorname{Unif}(V^\perp\cap\mathbb S^{d-1})$;
8         if InitialActionHypTest $(v;f,d,\mathcal O,\delta/L,\kappa_1/4)=$ True then
9             $v_i\leftarrow v$;
10            $V\leftarrow\operatorname{span}(V\cup\{v_i\})$;
11            break;
// Find subsequent directions
12 for epoch $i=d_0+1,\cdots,m$ do
13    $v_{\mathrm{pre}}\leftarrow\frac1{\sqrt{i-1}}\sum_{j=1}^{i-1}v_j$;
14    $x_{\mathrm{pre}}\leftarrow\sqrt{(i-1)/d}$;
15    while True do
16        Sample $v\sim\operatorname{Unif}(V^\perp\cap\mathbb S^{d-1})$;
17        if GoodActionHypTest $(v;f,d,\mathcal O,\delta/L,\kappa_1/4,\kappa_2,v_{\mathrm{pre}},x_{\mathrm{pre}})=$ True then
18            $v_i\leftarrow v$;
19            $V\leftarrow\operatorname{span}(V\cup\{v_i\})$;
20            break;
// Final action
21 Output $a_0\leftarrow\frac1{\sqrt m}\sum_{i=1}^m v_i$.''',[21],[1,2,18,19,20],['InitialActionHypTest','GoodActionHypTest',r'L\leftarrow2m\log(2m/\delta)/c_0'],'Complete main-text Algorithm1, including the two certification calls, their scaled accuracy argument kappa1/4, candidate sampling and final normalized sum. Its Theorem9 reference imports the numerical parameter block only, not the theorem’s conclusion. The source’s first d0 epochs are not truncated when m<d0; record the range issue. Main-text code assumes monotone f; its even-link modifications are deferred to an excluded appendix.','Algorithm 1 — Iterative direction search algorithm',kind='source_passage',context='Algorithm 1: Iterative direction search algorithm')
add(18,'InitialActionHypTest',r'''1 Input: link function $f$, dimensionality $d$, a noisy oracle $\mathcal O:a\in\mathbb B^d\mapsto\mathcal N(f(\langle\theta^\star,a\rangle),1)$, error probability $\delta$, accuracy parameter $\kappa_1$, test direction $v$.
2 Output: with probablity $\ge1-\delta$, True if $\langle\theta^\star,v\rangle\in[(1+\kappa_1)/\sqrt d,(1+2\kappa_1)/\sqrt d]$, False if $\langle\theta^\star,v\rangle\notin[1/\sqrt d,(1+3\kappa_1)/\sqrt d]$.
3 Define
\[
\varepsilon:=\frac12\min_{z\in[1,1+2\kappa_1]}\left|f\left(\frac{z+\kappa_1}{\sqrt d}\right)-f\left(\frac z{\sqrt d}\right)\right|.
\]
(18)
4 Query the test action $2\log(2/\delta)/\varepsilon^2$ times and compute the sample average $\overline r$;
5 if $\exists x\in[(1+\kappa_1)/\sqrt d,(1+2\kappa_1)/\sqrt d]$ such that $|\overline r-f(x)|\le\varepsilon$ then
6     Return True;
7 else
8     Return False;''',[23],[1,2],[r'\min_{z\in[1,1+2\kappa_1]}',r'|\overline r-f(x)|\le\varepsilon'],'Complete initial-direction certification pseudocode. It uses a projection test and a finite-difference accuracy scale, not a derivative oracle. Zero finite differences and integer query counts are not silently repaired. The gap between accepted and rejected target intervals is deliberate.','Algorithm 2 — InitialActionHypTest',kind='source_passage',context='Algorithm 2: InitialActionHypTest')
add(19,'GoodActionHypTest',r'''1 Input: link function $f$, dimensionality $d$, a noisy oracle $\mathcal O:a\in\mathbb B^d\mapsto\mathcal N(f(\langle\theta^\star,a\rangle),1)$, error probability $\delta$, accuracy parameters $(\kappa_1,\kappa_2)$, test direction $v$, previous action $v_{\mathrm{pre}}$, previous inner product $x_{\mathrm{pre}}$.
2 Output: with probablity $\ge1-\delta$, True if $\langle\theta^\star,v\rangle\in[(1+\kappa_1)/\sqrt d,(1+2\kappa_1)/\sqrt d]$, False if $\langle\theta^\star,v\rangle\notin[1/\sqrt d,(1+3\kappa_1)/\sqrt d]$.
3 Define $\kappa_2^\perp:=\sqrt{1-(1-\kappa_2)^2}$, $\kappa_3:=\kappa_1\kappa_2^\perp$, $\kappa_4:=(\kappa_1^{-1}+2)\kappa_2^\perp$, and
\[
\varepsilon:=\frac12\max_{\kappa_4/\sqrt d\le y\le(1-\kappa_2)x_{\mathrm{pre}}}\min_{z\in[(1-4\kappa_1)y,(1+4\kappa_1)y]}\left|f\left(z+\frac{\kappa_3}{\sqrt d}\right)-f(z)\right|.
\]
(19)
4 Let $y^\star$ be the maximizer of (19), and define $\lambda:=y^\star/[(1-\kappa_2)x_{\mathrm{pre}}]\in[0,1]$.
5 Query both actions $a_-=\lambda(1-\kappa_2)v_{\mathrm{pre}}-\kappa_2^\perp v$ and $a_+=\lambda(1-\kappa_2)v_{\mathrm{pre}}+\kappa_2^\perp v$ for $2\log(4/\delta)/\varepsilon^2$ times, and compute the sample averages $\overline r_-$ and $\overline r_+$.
6 if $\exists z\in[y^\star,(1+3\kappa_1)y^\star]$ and $x\in[(1+\kappa_1)\kappa_2^\perp/\sqrt d,(1+2\kappa_1)\kappa_2^\perp/\sqrt d]$ such that
\[
|\overline r_--f(z-x)|\le\varepsilon\quad\text{and}\quad|\overline r_+-f(z+x)|\le\varepsilon.
\]
(20)
then
7     Return True;
8 else
9     Return False;''',[24],[1,2],[r'\kappa_2^\perp',r'\min_{z\in[(1-4\kappa_1)y,(1+4\kappa_1)y]}',r'|\overline r_--f(z-x)|\le\varepsilon'],'Complete recursive certification pseudocode, using a pair of translated actions and a joint projection test. Preserve the factor4 in the inner interval, the kappa constants, two sample means and the common z,x feasibility condition. Algorithm1 calls it with kappa1/4. Its parameter x_pre describes prior progress, not the unknown exact inner product.','Algorithm 3 — GoodActionHypTest',kind='source_passage',context='Algorithm 3: GoodActionHypTest')
add(20,'numerical constants',STATEMENTS[8].split('If $f$ is monotone')[0].strip(),[22],[2],[r'd_0=',r'c_0=c',r'\varepsilon_i=\begin{cases}',r'm=\lceil x_0^2d\rceil'],'Exact parameter block from Theorem9, including delta and kappa ranges, d0,c0, both epsilon_i cases, c1,c2,m. It is reused by Algorithm1 and Theorem10. c(.) is referenced to Lemma6 in an excluded appendix and remains unresolved. Extracting this block separately prevents an Algorithm1/Theorem9 conclusion cycle. It does not add the theorem’s performance guarantee as a premise.','Theorem 9 — Numerical parameters and finite differences',kind='theorem_excerpt')
add(21,'Regression-based explore-then-commit algorithm',r'''1 Input: link function $f$, dimensionality $d$, time horizon $T$, action $a_0$ with $\langle a_0,\theta^\star\rangle\ge1-\gamma$.
2 Output: final estimator $\widehat\theta_T$, or a sequence of actions $(a_1,\cdots,a_T)$.
3 Set
\[
m\leftarrow\begin{cases}T&\text{for estimation},\\\min\{T,d\sqrt T/c_f\}&\text{for regret minimization}.\end{cases}
\]
(21)
4 for $t=1,2,\cdots,m$ do
5     Play action $a_t=(1-\gamma/8)a_0+(-1)^{\lceil t/d\rceil}\cdot\frac\gamma8 e_{((t-1)\bmod d)+1}$;
6     Receive reward $r_t\sim\mathcal N(f(\langle\theta^\star,a_t\rangle),1)$.
7 Compute the constrained least squares estimator:
\[
\widehat\theta^{\mathrm{LS}}=\operatorname*{arg\,min}_{\theta\in\mathbb S^{d-1}:\langle\theta,a_0\rangle\ge1-\gamma}\sum_{t=1}^m(f(\langle\theta,a_t\rangle)-r_t)^2.
\]
(22)
8 for $t=m+1,\cdots,T$ do
9     Commit to the action $a_t=\widehat\theta^{\mathrm{LS}}$.
10 Return $\widehat\theta_T=\widehat\theta^{\mathrm{LS}}$ or $(a_1,\cdots,a_T)$.''',[26],[1,2,9],[r'm\leftarrow\begin{cases}',r'(-1)^{\lceil t/d\rceil}',r'\langle\theta,a_0\rangle\ge1-\gamma'],'Complete Algorithm4 with its two budget branches, alternating coordinate design, cap-constrained least squares and commit phase. Theorem6 provides a stronger initialization1-3gamma/4 than the printed algorithm input1-gamma. c_f,gamma refer to Assumption2’s local parameters. Integer budgets, complete coordinate cycles and measurable minimizer conventions are not specified in the source.','Algorithm 4 — Regression-based explore-then-commit algorithm',kind='source_passage',context='Algorithm 4: Regression-based explore-then-commit algorithm')
add(22,'nonadaptive sampling',r'''Here under nonadaptive sampling, the actions $a_1,\cdots,a_T\in\mathbb B^d$ are chosen in advance without knowing the history.''',[27],[1],[r'a_1,\cdots,a_T\in\mathbb B^d','chosen in advance without knowing the history'],'Policy restriction to actions selected before observing rewards. Randomized designs remain possible, but adaptation to the reward history is excluded. Theorem11 separately specifies a uniform sphere prior and an expected signed-correlation target.','Section 4.1 — Nonadaptive sampling',kind='source_passage')
add(23,'finite subset',r'''In this section we consider the case where the action space $\mathcal A$ is not continuous and is a finite subset of $\mathbb B^d$, with $|\mathcal A|=K$.''',[27],[],[r'\mathcal A',r'|\mathcal A|=K'],'Finite unit-ball action domain. Theorem12 asserts existence of a hard set for every subexponential K, not a lower bound for every finite action set. Parameter and output domains remain sphere-valued in that theorem.','Section 4.2 — Finitely many actions',kind='source_passage')
add(24,'Unit sphere vs unit ball',r'''In this section, we relax the assumption $\theta^\star\in\mathbb S^{d-1}$ and investigate the statistical complexity of ridge bandits when $\theta^\star\in\mathbb B^d$. The following theorem shows that it is equivalent to think of the unit ball as a union of spheres with different radii.''',[28],[1,2,4],[r'\theta^\star\in\mathbb B^d'],'Theorem13’s explicit parameter-domain change. Its minimax regret takes the worst parameter over the ball while retaining the sequential ridge observation and cumulative regret definitions. It does not inherit the sphere supremum in Definition2 literally; the modified supremum is stated by Theorem13 and this main-text passage.','Section 4.3 — Unit sphere vs unit ball',kind='source_passage',context='4.3 Unit sphere vs unit ball')
add(25,'Monotonicity',r'''Monotonicity: either (i) $f$ is increasing on $[-1,1]$; or (ii) $f$ is even and increasing on $[0,1]$.''',[6],[],['Monotonicity: either (i)'],'Only item2 of Assumption1, explicitly referenced by Theorem13. Keep it separate from normalized scale: Theorem13 does not explicitly import item1. Full Assumption1 is separately preserved as D8 for the other theorems.','Assumption 1, item 2 — Monotonicity',kind='assumption')
# Source-inspected rendering amendment; see the explicit saved review plan.
members['D8']['highlight_symbols'] = ['f(0)=0', 'f(1)=1']
members['D8']['highlight_phrases'] = ['Monotonicity: either (i)']
members['D25']['highlight_symbols'] = []
members['D25']['highlight_phrases'] = ['Monotonicity: either (i)']
members['D13']['highlight_symbols'] = ['\\operatorname*{arg\\,max}_{a\\in\\mathcal A}', '\\max_{\\theta\\in\\mathbb C_t}']
members['D14']['highlight_symbols'] = ['\\widehat\\theta_t', '\\mathrm{Est}^{\\mathrm{On}}_t']
members['D17']['highlight_symbols'] = ['L\\leftarrow2m\\log(2m/\\delta)/c_0']
members['D17']['highlight_phrases'] = ['InitialActionHypTest', 'GoodActionHypTest']
members['D20']['highlight_symbols'] = ['d_0=', 'c_0=c', '\\varepsilon_i', 'm=\\lceil x_0^2d\\rceil']
members['D21']['highlight_symbols'] = ['m\\leftarrow\\begin{cases}T&\\text{for estimation},\\\\\\min\\{T,d\\sqrt T/c_f\\}&\\text{for regret minimization}.\\end{cases}', '(-1)^{\\lceil t/d\\rceil}', '\\operatorname*{arg\\,min}_{\\theta\\in\\mathbb S^{d-1}:\\langle\\theta,a_0\\rangle\\ge1-\\gamma}']
members['D22']['highlight_symbols'] = ['a_1,\\cdots,a_T\\in\\mathbb B^d']
members['D22']['highlight_phrases'] = ['chosen in advance without knowing the history']

def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
