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

add('D1','discounted infinite-horizon MDP',r'''
Consider a discounted infinite-horizon MDP represented by a tuple $\mathcal M=\{\mathcal S,\mathcal A,P,\gamma,r\}$. The key components of $\mathcal M$ are: (i) $\mathcal S=\{1,2,\ldots,S\}$: a finite state space of size $S$; (ii) $\mathcal A=\{1,2,\ldots,A\}$: an action space of size $A$; (iii) $P:\mathcal S\times\mathcal A\to\Delta(\mathcal S)$: the transition probability kernel of the MDP (i.e., $P(\cdot\mid s,a)$ denotes the transition probability from state $s$ when action $a$ is executed); (iv) $\gamma\in[0,1)$: the discount factor, so that $\frac{1}{1-\gamma}$ represents the effective horizon; (v) $r:\mathcal S\times\mathcal A\to[0,1]$: the deterministic reward function (namely, $r(s,a)$ is the immediate reward received when the current state-action pair is $(s,a)$). Without loss of generality, the immediate rewards are normalized so that they are contained within the interval $[0,1]$. Throughout this section, we introduce the convenient notation
\[
P_{s,a}:=P(\cdot\mid s,a)\in\mathbb R^{1\times S}.\tag{9}
\]
''',[7],'Section 2.1 — discounted infinite-horizon MDP',kind='source_passage',phrases=['discounted infinite-horizon MDP'],shape='Finite state/action discounted MDP with deterministic bounded rewards and gamma in [0,1).')
add('D2','stationary policy',r'''
A stationary policy $\pi:\mathcal S\to\Delta(\mathcal A)$ is a possibly randomized action selection rule; that is, $\pi(a\mid s)$ represents the probability of choosing $a$ in state $s$. When $\pi$ is a deterministic policy, we abuse the notation by letting $\pi(s)$ represent the action chosen by the policy $\pi$ in state $s$. A sample trajectory induced by the MDP under policy $\pi$ can be written as $\{(s_t,a_t)\}_{t\geq0}$, with $s_t$ (resp., $a_t$) denoting the state (resp., action) of the trajectory at time $t$.
''',[7],'Section 2.1 — stationary policy',{'D1':'The policy selects actions and induces trajectories in the discounted MDP.'},phrases=['stationary policy'],symbols=[r'\pi(a\mid s)'],shape='Stationary randomized policy with deterministic-policy notation as a special case; do not substitute a time-dependent finite-horizon policy.')
add('D3',['value function','Q-function'],r'''
To proceed, we shall also introduce the value function $V^\pi$ and Q-value function $Q^\pi$ associated with policy $\pi$. Specifically, the value function $V^\pi:\mathcal S\to\mathbb R$ of policy $\pi$ is defined as the expected discounted cumulative reward as follows:
\[
\forall s\in\mathcal S:\quad V^\pi(s):=\mathbb E\left[\sum_{t=0}^{\infty}\gamma^t r(s_t,a_t)\mid s_0=s;\pi\right],\tag{10}
\]
where the expectation is taken over the sample trajectory $\{(s_t,a_t)\}_{t\geq0}$ generated in a way that $a_t\sim\pi(\cdot\mid s_t)$ and $s_{t+1}\sim P(\cdot\mid s_t,a_t)$ for all $t\geq0$. Given that all immediate rewards lie within $[0,1]$, it is easily verified that $0\leq V^\pi(s)\leq\frac{1}{1-\gamma}$ for any policy $\pi$. The Q-function (or action-state function) of policy can be defined analogously as follows:
\[
\forall(s,a)\in\mathcal S\times\mathcal A:\quad Q^\pi(s,a):=\mathbb E\left[\sum_{t=0}^{\infty}\gamma^t r(s_t,a_t)\mid s_0=s,a_0=a;\pi\right],\tag{11}
\]
which differs from (10) in that it is also conditioned on $a_0=a$.

Let $\rho\in\Delta(\mathcal S)$ be a given state distribution. If the initial state is randomly drawn from $\rho$, then we can define the following weighted value function of policy $\pi$:
\[
V^\pi(\rho):=\mathbb E_{s\sim\rho}[V^\pi(s)].\tag{12}
\]
''',[7],'Section 2.1 — value function and Q-function, equations (10)-(12)',{'D1':'The discounted sum uses gamma, rewards and the transition kernel.','D2':'The trajectory law follows the stationary policy.'},phrases=['value function','Q-function'],symbols=[r'V^\pi(\rho)'],shape='Original passage defining discounted state value, action-state value and averaging over the test initial law rho; the two functions are not asserted equivalent.')
add('D4','discounted occupancy distributions',r'''
We also introduce the discounted occupancy distributions associated with $\pi$ as follows:
\[
\forall s\in\mathcal S:\quad d^\pi(s;\rho):=(1-\gamma)\sum_{t=0}^{\infty}\gamma^t\mathbb P(s_t=s\mid s_0\sim\rho;\pi),\tag{13}
\]
\[
\forall(s,a)\in\mathcal S\times\mathcal A:\quad d^\pi(s,a;\rho):=(1-\gamma)\sum_{t=0}^{\infty}\gamma^t\mathbb P(s_t=s,a_t=a\mid s_0\sim\rho;\pi),\tag{14}
\]
where we consider the randomness over a sample trajectory that starts from an initial state $s_0\sim\rho$ and that follows policy $\pi$ (i.e., $a_t\sim\pi(\cdot\mid s_t)$ and $s_{t+1}\sim P(\cdot\mid s_t,a_t)$ for all $t\geq0$).
''',[8],'Section 2.1 — discounted occupancy distributions, equations (13)-(14)',{'D1':'The occupancy weights include gamma and the MDP transition kernel.','D2':'Probabilities concern trajectories following pi from rho.'},phrases=['discounted occupancy distributions'],symbols=[r'd^\pi(s,a;\rho)'],shape='Normalized discounted state and state-action occupancy from the specified initial law.')
add('D5','optimal value and optimal Q-function',r'''
It is known that there exists at least one deterministic policy—denoted by $\pi^\star$—that simultaneously maximizes $V^\pi(s)$ and $Q^\pi(s,a)$ for all state-action pairs $(s,a)\in\mathcal S\times\mathcal A$ (Bertsekas (2017)). We use the following shorthand notation to represent respectively the resulting optimal value and optimal Q-function:
\[
\forall(s,a)\in\mathcal S\times\mathcal A:\quad V^\star(s):=V^{\pi^\star}(s)\ \text{and}\ Q^\star(s,a):=Q^{\pi^\star}(s,a).\tag{15}
\]
Correspondingly, the discounted occupancy distributions associated with $\pi^\star$ is denoted by
\[
\begin{aligned}
\forall(s,a)\in\mathcal S\times\mathcal A:\quad d^\star(s)&:=d^{\pi^\star}(s;\rho),\ d^\star(s,a)\\
&:=d^{\pi^\star}(s,a;\rho)=d^\star(s)\mathbb 1(a=\pi^\star(s)),
\end{aligned}\tag{16}
\]
where the last equality is valid since $\pi^\star$ is assumed to be deterministic.
''',[8],'Section 2.1 — optimal policy, values and occupancies, equations (15)-(16)',{'D2':'The selected optimal policy is deterministic and stationary.','D3':'Optimality maximizes the state and action-state values.','D4':'The d-star notation specializes the discounted occupancy to that fixed optimal policy.'},phrases=['optimal value and optimal Q-function'],symbols=[r'V^\star(s)',r'd^\star(s,a)'],shape='Source passage fixing one deterministic optimal policy, its values and its occupancy. Preserve dependence of concentrability on that chosen optimal policy.')
add('D6','independent sampling model',r'''
Let us work with an independent sampling model as studied in Rashidinejad et al. (2022). To be precise, imagine that we observe a batch data set $\mathcal D=\{(s_i,a_i,s_i')\}_{1\leq i\leq N}$ containing $N$ sample transitions. These samples are independently generated based on a distribution $d^{\mathrm b}\in\Delta(\mathcal S\times\mathcal A)$ and the transition kernel $P$ of the MDP, namely
\[
(s_i,a_i)\overset{\mathrm{ind.}}{\sim}d^{\mathrm b}\quad\text{and}\quad s_i'\overset{\mathrm{ind.}}{\sim}P(\cdot\mid s_i,a_i),\quad1\leq i\leq N.\tag{17}
\]
In addition, it is assumed that the learner is aware of the reward function.
''',[8],'Section 2.1 — Offline/batch data, equation (17)',{'D1':'Each independent record has a state-action pair and a next state generated by the discounted MDP kernel.'},kind='condition',phrases=['independent sampling model'],symbols=[r'd^{\mathrm b}'],shape='Independent transition samples with arbitrary state-action design distribution and known reward function. Do not require d-b to be a policy occupancy.')
add('D7','Single-policy concentrability for infinite-horizon MDPs',r'''
The single-policy concentrability coefficient of a batch data set $\mathcal D$ is defined as
\[
C^\star:=\max_{(s,a)\in\mathcal S\times\mathcal A}\frac{d^\star(s,a)}{d^{\mathrm b}(s,a)}.\tag{18}
\]
Clearly, one necessarily has $C^\star\geq1$.
''',[8],'Definition 1 (Single-policy concentrability for infinite-horizon MDPs)',{'D5':'The numerator is the chosen optimal-policy discounted occupancy.','D6':'The denominator is the independent sampling distribution d-b.'},context='Single-policy concentrability for infinite-horizon MDPs',phrases=['Definition 1'],symbols=[r'C^\star'],shape='Unclipped maximum density ratio for a single optimal discounted policy; keep the 0/0=0 ambient convention.')
add('D8','Single-policy clipped concentrability for infinite-horizon MDPs',r'''
The single-policy clipped concentrability coefficient of a batch data set $\mathcal D$ is defined as
\[
C^\star_{\mathrm{clipped}}:=\max_{(s,a)\in\mathcal S\times\mathcal A}\frac{\min\{d^\star(s,a),\frac1S\}}{d^{\mathrm b}(s,a)}.\tag{19}
\]
''',[9],'Definition 2 (Single-policy clipped concentrability for infinite-horizon MDPs)',{'D5':'The numerator clips the chosen optimal-policy discounted occupancy at 1/S.','D6':'The denominator is the independent sampling distribution.'},context='Single-policy clipped concentrability for infinite-horizon MDPs',phrases=['Definition 2'],symbols=[r'C^\star_{\mathrm{clipped}}'],shape='Clipping acts on the numerator occupancy, not on the density ratio. This coefficient need not be at least one.')
add('D9','empirical MDP',r'''
Recall that we are given $N$ independent sample transitions $\{(s_i,a_i,s_i')\}_{i=1}^N$ in the data set $\mathcal D$. For any given state-action pairs $(s,a)$, we denote by
\[
N(s,a):=\sum_{i=1}^N\mathbb 1((s_i,a_i)=(s,a))\tag{24}
\]
the number of samples transitions from $(s,a)$. We then construct an empirical transition matrix $\widehat P$ such that: for each $(s,a,s')\in\mathcal S\times\mathcal A\times\mathcal S$,
\[
\widehat P(s'\mid s,a)=\begin{cases}
\displaystyle\frac1{N(s,a)}\sum_{i=1}^N\mathbb 1\{(s_i,a_i,s_i')=(s,a,s')\}&\text{if }N(s,a)>0,\\
\displaystyle\frac1S&\text{else.}
\end{cases}\tag{25}
\]
''',[10],'Section 2.2 — The empirical MDP, equations (24)-(25)',{'D1':'The empirical transition matrix has one row per state-action pair.','D6':'The count and frequencies use the independent offline transition data.'},context='The empirical MDP.',phrases=['empirical transition matrix'],symbols=[r'N(s,a)',r'\widehat P'],shape='Count-based empirical transition kernel, with a uniform next-state law for every unobserved state-action pair.')
add('D10','pessimistic Bellman operator',r'''
Our algorithm is developed based on finding the fixed point of some variant of the classical Bellman operator. Let us first introduce this key operator and elucidate how the pessimism principle is enforced. Recall that the Bellman operator $\mathcal T(\cdot):\mathbb R^{SA}\to\mathbb R^{SA}$ w.r.t. the transition kernel $P$ is defined such that for any vector $Q\in\mathbb R^{SA}$,
\[
\mathcal T(Q)(s,a):=r(s,a)+\gamma P_{s,a}V\quad\text{for all }(s,a)\in\mathcal S\times\mathcal A,\tag{26}
\]
where $V=[V(s)]_{s\in\mathcal S}$ with $V(s):=\max_a Q(s,a)$. We propose to penalize the original Bellman operator w.r.t. the empirical kernel $\widehat P$ as follows:
\[
\widehat{\mathcal T}_{\mathrm{pe}}(Q)(s,a):=\max\{r(s,a)+\gamma\widehat P_{s,a}V-b(s,a;V),0\}\quad\text{for all }(s,a)\in\mathcal S\times\mathcal A,\tag{27}
\]
where $b(s,a;V)$ denotes the penalty term employed to enforce pessimism amid uncertainty.
''',[10],'Section 2.2 — The pessimistic Bellman operator, equations (26)-(27)',{'D1':'The Bellman formula uses r, gamma and P.','D9':'The pessimistic operator replaces P by the empirical kernel.','D11':'The specified Bernstein-style penalty supplies b in the theorem-referenced algorithm.'},context='The pessimistic Bellman operator.',symbols=[r'\widehat{\mathcal T}_{\mathrm{pe}}'],phrases=['Bellman operator'],shape='Max-with-zero empirical Bellman update on an arbitrary action-value vector, using its rowwise action maximum and the specified penalty.')
add('D11','Bernstein-style penalty',r'''
In this paper, we focus on the following Bernstein-style penalty to exploit the power of variance statistics:
\[
b(s,a;V):=\min\left\{\max\left\{\sqrt{\frac{c_{\mathrm b}\log\frac{N}{(1-\gamma)\delta}}{N(s,a)}\operatorname{Var}_{\widehat P_{s,a}}(V)},\frac{2c_{\mathrm b}\log\frac{N}{(1-\gamma)\delta}}{(1-\gamma)N(s,a)}\right\},\frac1{1-\gamma}\right\}+\frac5N\tag{28}
\]
for every $(s,a)\in\mathcal S\times\mathcal A$, where $c_{\mathrm b}>0$ is some numerical constant (e.g., $c_{\mathrm b}=144$), and $\delta\in(0,1)$ is some given quantity ($1-\delta$ is the target success probability). Here, for any vector $V\in\mathbb R^S$, we recall that $\operatorname{Var}_{\widehat P_{s,a}}(V)$ is the variance of $V$ w.r.t. the distribution $\widehat P_{s,a}$ (see (8)).
''',[10],'Section 2.2 — Bernstein-style penalty, equation (28)',{'D1':'The cap and linear term use the discount factor.','D9':'The penalty uses empirical row variance and the state-action count.'},phrases=['Bernstein-style penalty'],symbols=[r'b(s,a;V)'],shape='Nested min/max Bernstein penalty plus 5/N, with empirical rather than true transition variance. The vector V is an input; do not create a circular dependency on the value-iteration output.')

def add_algorithm(lid,title,steps,pages,heading,deps,shape):
    body='\n'.join('    '*depth+'- **'+str(n)+'.** '+text.replace('\n','\n'+'    '*depth+'  ') for n,depth,text in steps)
    add(lid,title,body,pages,heading,deps,context=title,phrases=[heading.split(' — ')[0]],shape=shape)
    members[lid]['algorithm_steps_original']=[dict(line=n,depth=depth,text_original=text) for n,depth,text in steps]

add_algorithm('D12','Offline value iteration with LCB (VI-LCB) for infinite-horizon MDPs',[
(1,0,r'input: data set $\mathcal D$; reward function $r$; target success probability $1-\delta$; max iteration number $\tau_{\max}$.'),
(2,0,r'initialization: $\widehat Q_0=0$, $\widehat V_0=0$.'),
(3,0,r'construct the empirical transition kernel $\widehat P$ according to (25).'),
(4,0,r'for $\tau=1,2,\ldots,\tau_{\max}$ do'),
(5,1,r'for $s\in\mathcal S,a\in\mathcal A$ do'),
(6,2,r'compute the penalty term $b(s,a;\widehat V_{\tau-1})$ according to (28).'),
(7,2,r'set $\widehat Q_\tau(s,a)=\max\{r(s,a)+\gamma\widehat P_{s,a}\widehat V_{\tau-1}-b(s,a;\widehat V_{\tau-1}),0\}$.'),
(8,1,r'for $s\in\mathcal S$ do'),
(9,2,r'set $\widehat V_\tau(s)=\max_a\widehat Q_\tau(s,a)$.'),
(10,0,r'output: $\widehat\pi$ s.t. $\widehat\pi(s)\in\arg\max_a\widehat Q_{\tau_{\max}}(s,a)$ for any $s\in\mathcal S$.')
],[11],'Algorithm 1 — Offline value iteration with LCB (VI-LCB) for infinite-horizon MDPs',{
'D9':'Step 3 constructs the empirical transition kernel according to (25).',
'D11':'Step 6 computes the penalty according to (28).',
'D10':'Step 7 applies the pessimistic Bellman update (27).',
'D2':'The output is a stationary deterministic greedy action-selection policy.'},
'Complete ten-line discounted algorithm, with zero initialization, sample reuse, nested updates, iteration horizon and greedy output.')

add('D13','finite-horizon Markov decision process',r'''
Consider the setting of a finite-horizon Markov decision process, as denoted by $\mathcal M=\{\mathcal S,\mathcal A,H,P,r\}$. It consists of the following key components: (i) $\mathcal S=\{1,\ldots,S\}$: a state space of size $S$; (ii) $\mathcal A=\{1,\ldots,A\}$: an action space of size $A$; (iii) $H$: the horizon length; (iv) $P=\{P_h\}_{1\leq h\leq H}$, with $P_h:\mathcal S\times\mathcal A\to\Delta(\mathcal S)$ denoting the probability transition kernel at step $h$ (namely, $P_h(\cdot\mid s,a)$ stands for the transition probability of the MDP at step $h$ when the current state-action pair is $(s,a)$); (v) $r=\{r_h\}_{1\leq h\leq H}$, with $r_h:\mathcal S\times\mathcal A\to[0,1]$ denoting the reward function at step $h$ (namely $r_h(s,a)$ indicates the immediate reward gained at step $h$ when the current state-action pair is $(s,a)$). It is assumed without loss of generality that the immediate rewards fall within the interval $[0,1]$ and are deterministic. Conveniently, we introduce the following $S$-dimensional row vector:
\[
P_{h,s,a}:=P_h(\cdot\mid s,a),\quad\forall(s,a,h)\in\mathcal S\times\mathcal A\times[H].\tag{37}
\]
''',[14,15],'Section 3.1 — finite-horizon Markov decision process',kind='source_passage',phrases=['finite-horizon Markov decision process'],symbols=[r'P_{h,s,a}'],shape='Finite-state, finite-action H-step MDP with time-dependent kernels and deterministic bounded rewards. No discount factor is introduced.')
add('D14','policy',r'''
A (possibly randomized) policy $\pi=\{\pi_h\}_{1\leq h\leq H}$ with $\pi_h:\mathcal S\to\Delta(\mathcal A)$ is an action selection rule, such that $\pi_h(a\mid s)$ specifies the probability of choosing action $a$ when in state $s$ and step $h$. When $\pi$ is a deterministic policy, we overload the notation and let $\pi_h(s)$ represent the action selected by $\pi$ in state $s$ at step $h$. We can generate a sample trajectory $\{(s_h,a_h)\}_{1\leq h\leq H}$ by implementing policy $\pi$ in the MDP $\mathcal M$, where $s_h$ and $a_h$ denote the state and the action in step $h$, respectively.
''',[15],'Section 3.1 — finite-horizon policy',{'D13':'The action rules are indexed by steps 1 through H of the finite-horizon MDP.'},symbols=[r'\pi_h(a\mid s)'],phrases=['policy'],shape='Time-dependent Markov randomized policy, with deterministic notation and trajectory convention.')
add('D15',['value function','Q-function'],r'''
We then introduce the value function $V^\pi=\{V_h^\pi\}_{1\leq h\leq H}$ and the Q-function $Q^\pi=\{Q_h^\pi\}_{1\leq h\leq H}$ associated with policy $\pi$; specifically, the value function $V_h:\mathcal S\to\mathbb R$ of policy $\pi$ at step $h$ is defined to be the expected cumulative reward from step $h$ on as a result of policy $\pi$, namely
\[
\forall s\in\mathcal S:\quad V_h^\pi(s):=\mathbb E\left[\sum_{t=h}^H r_t(s_t,a_t)\mid s_h=s;\pi\right],\tag{38}
\]
where the expectation is taken over the randomness of the sample trajectory $\{(s_t,a_t)\}_{t=h}^H$ when policy $\pi$ is implemented (i.e., $a_t\sim\pi_t(\cdot\mid s_t)$ and $s_{t+1}\sim P_t(\cdot\mid s_t,a_t)$ for all $t\geq h$). Correspondingly, the Q-function of policy $\pi$ at step $h$ is defined to be
\[
\forall(s,a)\in\mathcal S\times\mathcal A:\quad Q_h^\pi(s,a):=\mathbb E\left[\sum_{t=h}^H r_t(s_t,a_t)\mid s_h=s,a_h=a;\pi\right]\tag{39}
\]
when conditioned on the state-action $(s,a)$ at step $h$. If the initial state is drawn from a distribution $\rho\in\Delta(\mathcal S)$, we find it convenient to define the weighted value function of $\pi$:
\[
V_1^\pi(\rho):=\mathbb E_{s\sim\rho}[V_1^\pi(s)].\tag{40}
\]
''',[15],'Section 3.1 — value function and Q-function, equations (38)-(40)',{'D13':'The reward sum runs from h to H without discounting.','D14':'The trajectory follows the time-indexed policy and transition kernels.'},phrases=['value function','Q-function'],symbols=[r'V_1^\pi(\rho)'],shape='Step-indexed undiscounted state/action values and test-distribution average at step one. Keep these separate from discounted values.')
add('D16','occupancy distributions',r'''
We also introduce the following occupancy distributions associated with policy $\pi$ at step $h$:
\[
d_h^\pi(s;\rho):=\mathbb P(s_h=s\mid s_1\sim\rho;\pi),\tag{41a}
\]
\[
d_h^\pi(s,a;\rho):=\mathbb P(s_h=s,a_h=a\mid s_1\sim\rho;\pi)=d_h^\pi(s;\rho)\pi(a\mid s),\tag{41b}
\]
which are conditioned on the initial state distribution $s_1\sim\rho$ and on the event that all actions are selected according to $\pi$. In particular, it is self-evident that
\[
d_1^\pi(s;\rho)=\rho(s)\quad\text{for any policy }\pi\text{ and any state }s\in\mathcal S.\tag{42}
\]
''',[15],'Section 3.1 — occupancy distributions, equations (41)-(42)',{'D13':'State and action laws are evaluated at a given finite-horizon step.','D14':'The trajectory follows the time-indexed policy.'},phrases=['occupancy distributions'],symbols=[r'd_h^\pi(s,a;\rho)'],note='The final factor in (41b) is printed as pi(a|s), without h. The original notation is preserved.',shape='Time-indexed state and state-action probabilities, rather than a discounted mixture over time.')
add('D17','optimal deterministic policy',r'''
It is well known that there exists at least one deterministic policy that simultaneously maximizes the value function and the Q-function for all $(s,a,h)\in\mathcal S\times\mathcal A\times[H]$ (Bertsekas (2017)). In light of this, we shall denote by $\pi^\star=\{\pi_h^\star\}_{1\leq h\leq H}$ an optimal deterministic policy throughout this paper; this allows us to employ $\pi_h^\star(s)$ to indicate the corresponding optimal action chosen in state $s$ at step $h$. The resulting optimal value function and optimal Q-function are denoted respectively by $V^\star:=\{V_h^\star\}_{1\leq h\leq H}$ and $Q^\star:=\{Q_h^\star\}_{1\leq h\leq H}$:
\[
\forall(s,a,h)\in\mathcal S\times\mathcal A\times[H]:\quad V_h^\star:=V_h^{\pi^\star}\quad\text{and}\quad Q_h^\star:=Q_h^{\pi^\star}.
\]
Further, we adopt the following notation for convenience: for any $(s,a,h)\in\mathcal S\times\mathcal A\times[H]$,
\[
d_h^\star(s):=d_h^{\pi^\star}(s;\rho)\quad\text{and}\quad d_h^\star(s,a):=d_h^{\pi^\star}(s,a;\rho)=d_h^\star(s)\mathbb 1\{a=\pi^\star(s)\},\tag{43}
\]
where the last identity holds given that $\pi^\star$ is assumed to be deterministic.
''',[15],'Section 3.1 — optimal deterministic policy and its values/occupancies',{'D14':'One time-indexed deterministic policy is chosen as optimal.','D15':'Optimality simultaneously maximizes state and action-state values at every step.','D16':'The d-h-star quantities specialize the stepwise occupancy to the chosen optimal policy.'},phrases=['optimal deterministic policy'],symbols=[r'V_h^\star',r'd_h^\star(s,a)'],note='The final indicator in (43) prints pi-star(s) without h, despite the preceding time-indexed policy definition; no subscript is inserted.',shape='A single deterministic optimal policy sequence, its values and its occupancy; preserve the printed omission of h in the indicator.')
add('D18','batch data set',r'''
Suppose we have access to a batch data set (or historical data set) $\mathcal D$, which comprises a collection of $K$ i.i.d. sample trajectories generated by a behavior policy $\pi^{\mathrm b}=\{\pi_h^{\mathrm b}\}_{1\leq h\leq H}$. The $k$th sample trajectory $(1\leq k\leq K)$ consists of a data sequence
\[
(s_1^k,a_1^k,s_2^k,a_2^k,\ldots,s_H^k,a_H^k,s_{H+1}^k),\tag{44}
\]
which is generated by the MDP $\mathcal M$ under the behavior policy $\pi^{\mathrm b}$ in the following manner:
\[
s_1^k\sim\rho^{\mathrm b},\quad a_h^k\sim\pi_h^{\mathrm b}(\cdot\mid s_h^k)\quad\text{and}\quad s_{h+1}^k\sim P_h(\cdot\mid s_h^k,a_h^k),\quad1\leq h\leq H.\tag{45}
\]
Here and throughout, $\rho^{\mathrm b}$ stands for some predetermined initial state distribution associated with the batch data set. In addition to the above data set (cf. (44) for all $1\leq k\leq K$), the learner also has access to the reward function. For notational simplicity, we introduce the following shorthand notation for the occupancy distribution w.r.t. the behavior policy $\pi^{\mathrm b}$:
\[
\forall(s,a,h)\in\mathcal S\times\mathcal A\times[H]:\quad d_h^{\mathrm b}(s):=d_h^{\pi^{\mathrm b}}(s;\rho^{\mathrm b})\text{and}d_h^{\mathrm b}(s,a):=d_h^{\pi^{\mathrm b}}(s,a;\rho^{\mathrm b}).\tag{46}
\]
In particular, it is easily seen that $d_1^{\mathrm b}(s)=\rho^{\mathrm b}(s)$ for all $s\in\mathcal S$. Note that the initial state distribution $\rho^{\mathrm b}$ of the batch data set might not coincide with the test distribution $\rho$.
''',[16],'Section 3.1 — Offline/batch data, equations (44)-(46)',{'D13':'Each trajectory follows the finite-horizon transition kernel.','D14':'The behavior policy is a time-indexed Markov policy.','D16':'The behavior occupancies specialize the time-indexed occupancy to pi-b and rho-b.'},kind='condition',phrases=['batch data set'],symbols=[r'\rho^{\mathrm b}',r'd_h^{\mathrm b}(s,a)'],shape='K iid length-H trajectories, with temporal dependence within each, known rewards, behavior policy and possibly different training/test initial laws.')
add('D19','Single-policy concentrability for finite-horizon MDPs',r'''
The single-policy concentrability coefficient of a batch data set $\mathcal D$ is defined as
\[
C^\star:=\max_{(s,a,h)\in\mathcal S\times\mathcal A\times[H]}\frac{d_h^\star(s,a)}{d_h^{\mathrm b}(s,a)},\tag{47}
\]
which clearly satisfies $C^\star\geq1$.
''',[16],'Definition 3 (Single-policy concentrability for finite-horizon MDPs)',{'D17':'The numerator is the chosen optimal-policy occupancy at each step.','D18':'The denominator is the behavior occupancy from the actual trajectory law.'},context='Single-policy concentrability for finite-horizon MDPs',phrases=['Definition 3'],symbols=[r'C^\star'],shape='Maximum unclipped density ratio over states, actions and times; not a ratio of time-aggregated discounted occupancies.')
add('D20','Single-policy clipped concentrability for finite-horizon MDPs',r'''
The single-policy clipped concentrability coefficient of a batch data set $\mathcal D$ is defined as
\[
C^\star_{\mathrm{clipped}}:=\max_{(s,a,h)\in\mathcal S\times\mathcal A\times[H]}\frac{\min\{d_h^\star(s,a),\frac1S\}}{d_h^{\mathrm b}(s,a)}.\tag{48}
\]
''',[16],'Definition 4 (Single-policy clipped concentrability for finite-horizon MDPs)',{'D17':'The numerator is the chosen optimal-policy occupancy, clipped at 1/S at each step.','D18':'The denominator is the behavior-policy stepwise occupancy.'},context='Single-policy clipped concentrability for finite-horizon MDPs',phrases=['Definition 4'],symbols=[r'C^\star_{\mathrm{clipped}}'],shape='Timewise numerator-clipped concentrability; retain the original stepwise behavior law and test initial law.')
add('D21','Empirical MDP',r'''
Suppose for the moment that we have a data set $\mathcal D_0$ containing $N$ sample transitions $\{(s_i,a_i,h_i,s_i')\}_{i=1}^N$, where $(s_i,a_i,h_i,s_i')$ denotes the transition from state $s_i$ at step $h_i$ to state $s_i'$ in the next step when action $a_i$ is taken. We now describe a pessimistic variant of the model-based approach on the basis of $\mathcal D_0$.

Empirical MDP. For each $(s,a,h)\in\mathcal S\times\mathcal A\times[H]$, we denote by
\[
\begin{aligned}
N_h(s,a)&:=\sum_{i=1}^N\mathbb 1\{(s_i,a_i,h_i)=(s,a,h)\}\quad\text{and}\\
N_h(s)&:=\sum_{i=1}^N\mathbb 1\{(s_i,h_i)=(s,h)\}
\end{aligned}\tag{50}
\]
the total number of sample transitions at step $h$ that transition from $(s,a)$ and from $s$, respectively. We can then compute the empirical estimate $\widehat P=\{\widehat P_h\}_{1\leq h\leq H}$ of $P$ as follows:
\[
\widehat P_h(s'\mid s,a)=\begin{cases}
\displaystyle\frac1{N_h(s,a)}\sum_{i=1}^N\mathbb 1\{(s_i,a_i,h_i,s_i')=(s,a,h,s')\}&\text{if }N_h(s,a)>0,\\
\displaystyle\frac1S&\text{else,}
\end{cases}\tag{51}
\]
for each $(s,a,h,s')\in\mathcal S\times\mathcal A\times[H]\times\mathcal S$.
''',[17],'Section 3.2 — Empirical MDP, equations (50)-(51)',{'D13':'The empirical kernels use the finite state, action and time index sets.'},phrases=['Empirical MDP'],symbols=[r'N_h(s,a)',r'\widehat P_h'],shape='Empirical stepwise transition kernels from an input transition collection D0, uniform on unobserved pairs. D0 is not asserted iid; Algorithm 3 supplies it by subsampling.')
add('D22','Bernstein-style penalty',r'''
As before, we adopt Bernstein-style penalty in order to better capture the variance structure over time; that is, for any $(s,a,h)\in\mathcal S\times\mathcal A\times[H]$,
\[
b_h(s,a)=\min\left\{\sqrt{\frac{c_{\mathrm b}\log\frac{NH}{\delta}}{N_h(s,a)}\operatorname{Var}_{\widehat P_{h,s,a}}(\widehat V_{h+1})}+c_{\mathrm b}H\frac{\log\frac{NH}{\delta}}{N_h(s,a)},H\right\}\tag{55}
\]
for some universal constant $c_{\mathrm b}>0$ (e.g., $c_{\mathrm b}=16$). Here, $\operatorname{Var}_{\widehat P_{h,s,a}}(\widehat V_{h+1})$ corresponds to the variance of $\widehat V_{h+1}$ w.r.t. the distribution $\widehat P_{h,s,a}$ (see the definition (8)). Note that we choose $\widehat P$ as opposed to $P$ (i.e., $\operatorname{Var}_{P_{h,s,a}}(\widehat V_{h+1})$) in the variance term, mainly because we have no access to the true transition kernel $P$.
''',[17,18],'Section 3.2 — The Bernstein-style penalty terms, equation (55)',{'D13':'The penalty is capped at the horizon H.','D21':'The statistical terms use the empirical time-specific row and its observation count.'},phrases=['Bernstein-style penalty'],symbols=[r'b_h(s,a)'],shape='Finite-horizon empirical-variance penalty: sum of square-root and linear terms capped at H, without discounted penalty max or 5/N. The next value vector is supplied by the backward iteration.')
add_algorithm('D23','Offline value iteration with LCB (VI-LCB) for finite-horizon MDPs',[
(1,0,r'input: data set $\mathcal D_0$; reward function $r$; target success probability $1-\delta$.'),
(2,0,r'initialization: $\widehat V_{H+1}=0$.'),
(3,0,r'for $h=H,\ldots,1$ do'),
(4,1,r'compute the empirical transition kernel $\widehat P_h$ according to (51).'),
(5,1,r'for $s\in\mathcal S,a\in\mathcal A$ do'),
(6,2,r'compute the penalty term $b_h(s,a)$ according to (55).'),
(7,2,r'set $\widehat Q_h(s,a)=\max\{r_h(s,a)+\widehat P_{h,s,a}\widehat V_{h+1}-b_h(s,a),0\}$.'),
(8,1,r'for $s\in\mathcal S$ do'),
(9,2,r'set $\widehat V_h(s)=\max_a\widehat Q_h(s,a)$ and $\widehat\pi_h(s)\in\arg\max_a\widehat Q_h(s,a)$.'),
(10,0,r'output: $\widehat\pi=\{\widehat\pi_h\}_{1\leq h\leq H}$.')
],[18],'Algorithm 2 — Offline value iteration with LCB (VI-LCB) for finite-horizon MDPs',{
'D21':'Step 4 builds each empirical kernel according to (51).',
'D22':'Step 6 evaluates the penalty from (55) using the already computed next-step value estimate.',
'D14':'The output is a deterministic time-indexed greedy policy.',
'D13':'The backward recursion runs from H to 1 with terminal value zero and rewards r_h.'},
'Full ten-line backward value iteration, including terminal initialization, state-action updates and within-step greedy-policy extraction.')
add_algorithm('D24','Subsampled VI-LCB for episodic finite-horizon MDPs',[
(1,0,r'input: a data set $\mathcal D$; reward function $r$.'),
(2,0,r'''subsampling: run the following procedure to generate the subsampled data set $\mathcal D^{\mathrm{trim}}$.

(1) Data splitting. Split $\mathcal D$ into two halves: $\mathcal D^{\mathrm{main}}$ (which contains the first $K/2$ trajectories), and $\mathcal D^{\mathrm{aux}}$ (which contains the remaining $K/2$ trajectories); we let $N_h^{\mathrm{main}}(s)$ (resp., $N_h^{\mathrm{aux}}(s)$) denote the number of sample transitions in $\mathcal D^{\mathrm{main}}$ (resp., $\mathcal D^{\mathrm{aux}}$) that transition from state $s$ at step $h$.

(2) Lower bounding $\{N_h^{\mathrm{main}}(s)\}$ using $\mathcal D^{\mathrm{aux}}$. For each $s\in\mathcal S$ and $1\leq h\leq H$, compute
\[
N_h^{\mathrm{trim}}(s):=\max\left\{N_h^{\mathrm{aux}}(s)-10\sqrt{N_h^{\mathrm{aux}}(s)\log\frac{HS}{\delta}},0\right\};\tag{56}
\]

(3) Random subsampling. Let $\mathcal D^{\mathrm{main}'}$ be the set of all sample transitions (i.e., the quadruples taking the form $(s,a,h,s')$) from $\mathcal D^{\mathrm{main}}$. Subsample $\mathcal D^{\mathrm{main}'}$ to obtain $\mathcal D^{\mathrm{trim}}$, such that for each $(s,h)\in\mathcal S\times[H]$, $\mathcal D^{\mathrm{trim}}$ contains $\min\{N_h^{\mathrm{trim}}(s),N_h^{\mathrm{main}}(s)\}$ sample transitions randomly drawn from $\mathcal D^{\mathrm{main}'}$.'''),
(3,0,r'run VI-LCB: set $\mathcal D_0=\mathcal D^{\mathrm{trim}}$; run Algorithm 2 to compute a policy $\widehat\pi$.')
],[19],'Algorithm 3 — Subsampled VI-LCB for episodic finite-horizon MDPs',{
'D18':'The input consists of K independent trajectories, split into two halves.',
'D21':'The retained data are step-labelled transitions in the format D0, with empirical stepwise counts.',
'D23':'The last step runs Algorithm 2 on the trimmed transition collection.'},
'Full three-step wrapper including all three subsampling substeps and equation (56). Keep K trajectories distinct from N transitions; preserve unresolved rounding of K/2 and trimming counts.')

def main():
    for name,data in [('source-passages.json',dict(paper_id=PID,members=list(members.values()))),('interface-draft.json',interfaces)]:
        (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source interfaces.')
if __name__=='__main__':main()
