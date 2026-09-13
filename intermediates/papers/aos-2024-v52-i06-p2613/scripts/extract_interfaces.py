"""Preserve original confidence-sequence, coupling and causal-estimation source passages."""
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
add(1,'asymptotic confidence sequence',r'''Let $\mathcal T$ be a totally ordered infinite set (denoting time) that has a minimum value $t_0\in\mathcal T$. We say that the intervals $(\widehat\theta_t-L_t,\widehat\theta_t+U_t)_{t\in\mathcal T}$ centered at the estimators $(\widehat\theta_t)_{t\in\mathcal T}$ with non-zero bounds $L_t,U_t>0,\forall t\in\mathcal T$ form a $(1-\alpha)$-asymptotic confidence sequence (AsympCS) for a sequence of real parameters $(\theta_t)_{t\in\mathcal T}$ if there exists a (typically unknown) nonasymptotic $(1-\alpha)$-CS $(\widehat\theta_t-L_t^*,\widehat\theta_t+U_t^*)_{t\in\mathcal T}$ for $(\theta_t)_{t\in\mathcal T}$ — i.e. satisfying
\[
\mathbb P\left(\forall t\in\mathcal T,\ \theta_t\in[\widehat\theta_t-L_t^*,\widehat\theta_t+U_t^*]\right)\ge1-\alpha,
\]
and such that $L_t,U_t$ become arbitrarily precise almost-sure approximations to $L_t^*$ and $U_t^*$:
\[
L_t^*/L_t\xrightarrow{\mathrm{a.s.}}1\quad\text{and}\quad U_t^*/U_t\xrightarrow{\mathrm{a.s.}}1.
\]''',[6],[],[r'L_t^*/L_t',r'U_t^*/U_t'],'Definition2.1 requires positive widths, a common centered nonasymptotic CS with simultaneous coverage, and almost-sure relative-width convergence. It does not assert the displayed approximate intervals already have finite-sample coverage. The source alternates parenthesis interval notation and square brackets in its probability event; preserve this.','Definition 2.1 — Asymptotic confidence sequences')
add(2,'Strong approximation',r'''On a potentially enriched probability space, there exists a process $(Z_t)_{t\in\mathcal T}$ starting at $Z_{t_0}\equiv0$ that strongly approximates $(\widehat\theta_t-\theta_t)_{t\in\mathcal T}$ up to a rate of $(r_t)_{t\in\mathcal T}$, i.e.
\[
(\widehat\theta_t-\theta_t)-Z_t=O(r_t)\quad\text{almost surely}.
\]
(9)''',[9],[],[r'Z_{t_0}\equiv0',r'(\widehat\theta_t-\theta_t)-Z_t=O(r_t)'],'Coupling on a potentially enlarged probability space, with approximation rate r_t almost surely. The approximating process need not be Gaussian in abstract Theorem2.4. Common ordered-time setup is auxiliary context.','Condition G-1 — Strong approximation',kind='condition',context='Condition G-1 (Strong approximation).')
add(3,'Boundary for the approximating process',r'''There exist $\widehat L_t>0$ and $\widehat U_t>0$ for each $t\in\mathcal T$ so that $[-\widehat L_t,\widehat U_t]_{t\in\mathcal T}$ forms a $(1-\alpha)$-boundary for the process $(Z_t)_{t\in\mathcal T}$ given in (9):
\[
\mathbb P\left(\forall t\in\mathcal T,\ Z_t\in[-\widehat L_t,\widehat U_t]\right)\ge1-\alpha.
\]
(10)''',[9],[2],[r'[-\widehat L_t,\widehat U_t]',r'\forall t\in\mathcal T'],'One simultaneous event controls the whole approximating path. These hatted boundaries differ from both the eventual nonasymptotic starred widths and their observable unadorned approximations.','Condition G-2 — Boundary for the approximating process',kind='condition',context='Condition G-2 (Boundary for the approximating process).')
add(4,'Strong approximation rate',r'''The approximation rate $(r_t)_{t\in\mathcal T}$ in (9) is faster than both $(\widehat L_t)_{t\in\mathcal T}$ and $(\widehat U_t)_{t\in\mathcal T}$ in (10), i.e.
\[
r_t=o(\widehat L_t\wedge\widehat U_t)\quad\text{almost surely}.
\]''',[9],[2,3],[r'r_t=o(\widehat L_t\wedge\widehat U_t)'],'The coupling error is smaller than both one-sided approximating boundaries, almost surely. This condition is separate from the existence of either the coupling or the boundary.','Condition G-3 — Strong approximation rate',kind='condition',context='Condition G-3 (Strong approximation rate).')
add(5,'Almost-sure approximate boundary',r'''The $(1-\alpha)$-boundary $[-\widehat L_t,\widehat U_t]_{t\in\mathcal T}$ for $(Z_t)_{t\in\mathcal T}$ is almost-surely approximated by the sequences $[-L_t,U_t]_{t\in\mathcal T}$, i.e.
\[
L_t/\widehat L_t\xrightarrow{\mathrm{a.s.}}1\quad\text{and}\quad U_t/\widehat U_t\xrightarrow{\mathrm{a.s.}}1.
\]''',[9],[3],[r'L_t/\widehat L_t',r'U_t/\widehat U_t'],'Almost-sure relative approximation of each side of the hatted process boundary. Theorem2.4 constructs starred valid widths; these are not simply identified with the hatted widths.','Condition G-4 — Almost-sure approximate boundary',kind='condition',context='Condition G-4 (Almost-sure approximate boundary).')
add(6,'conditional means and variances',r'''Suppose $(Y_t)_{t=1}^\infty$ is a sequence of random variables with conditional means and variances given by $\mu_t:=\mathbb E(Y_t\mid Y_1^{t-1})$ and $\sigma_t^2:=\operatorname{var}(Y_t\mid Y_1^{t-1})$, respectively where we use the shorthand $Y_1^{t-1}$ for $\{Y_1,\ldots,Y_{t-1}\}$. First, we require that the average conditional variance $\widetilde\sigma_t^2:=\frac1t\sum_{i=1}^t\sigma_i^2$ either does not vanish, or does so superlinearly; equivalently, we require that the cumulative conditional variance diverges almost surely.''',[10],[],[r'\mu_t:=\mathbb E(Y_t\mid Y_1^{t-1})',r'\widetilde\sigma_t^2:=\frac1t\sum_{i=1}^t\sigma_i^2'],'Conditional means/variances and their running average. The prose says superlinearly, but the immediately following formal L-1 requires t times average variance to diverge; retain the wording discrepancy. Independence in Corollary2.6 specializes these to unconditional quantities.','Section 2.4 — Conditional moments and average variance',kind='source_passage')
add(7,'Cumulative variance diverges almost surely',r'''For each $t\ge1$, let $\sigma_t^2:=\operatorname{var}(Y_t\mid Y_1^{t-1})$ be the conditional variance of $Y_t$. Then,
\[
V_t:=\sum_{i=1}^t\sigma_i^2\to\infty\quad\text{almost surely}.
\]
(11)''',[10],[6],[r'V_t:=\sum_{i=1}^t\sigma_i^2\to\infty'],'Divergence of cumulative variance, not necessarily convergence or a positive lower bound for the average variance. The independent-data condition in Corollary2.6 references this with unconditional variances.','Condition L-1 — Cumulative variance diverges almost surely',kind='condition',context='Condition L-1 (Cumulative variance diverges almost surely).')
add(8,'Lindeberg-type uniform integrability',r'''For $t\ge1$, let $\sigma_t^2:=\operatorname{var}(Y_t\mid Y_1^{t-1})$ be the conditional variance of $Y_t$. Then there exists some $0<\kappa<1$ such that
\[
\sum_{t=1}^\infty\frac{\mathbb E\left[(Y_t-\mu_t)^2\mathbf1\left((Y_t-\mu_t)^2>V_t^\kappa\right)\mid Y_1^{t-1}\right]}{V_t^\kappa}<\infty\quad\text{almost surely}.
\]
(12)''',[10],[6,7],[r'0<\kappa<1',r'(Y_t-\mu_t)^2>V_t^\kappa'],'Conditional tail summability with threshold and denominator V_t^kappa, and a single exponent in(0,1). It is an explicit condition of Theorem2.8, not imported into other theorems merely because their proofs use an invariance principle.','Condition L-2 — Lindeberg-type uniform integrability',kind='condition',context='Condition L-2 (Lindeberg-type uniform integrability).')
add(9,'Polynomial rate variance estimation',r'''There exists some $0<\eta<1$ such that
\[
\widehat\sigma_t^2-\widetilde\sigma_t^2=o\left(\frac{(t\widetilde\sigma_t^2)^\eta}{t}\right)\quad\text{almost surely}.
\]
(17)''',[13],[6],[r'\widehat\sigma_t^2-\widetilde\sigma_t^2',r'\frac{(t\widetilde\sigma_t^2)^\eta}{t}'],'Polynomial-rate error relative to cumulative variance, stronger than simple ratio consistency. The estimator’s definition is retained as auxiliary context from L-3; no implication-only edge to the weaker L-3 condition is inserted.','Condition L-3-η — Polynomial rate variance estimation',kind='condition',context='Condition L-3-$\eta$ (Polynomial rate variance estimation).')
add(10,'Asymptotic time-uniform coverage',r'''For each $m\in\mathbb N$, let $(C_t(m))_{t=m}^\infty$ be a sequence of sets, and let $\alpha\in(0,1)$ be the desired miscoverage level. We say that $(C_t(m))_{t=m}^\infty$ has asymptotic time-uniform $(1-\alpha)$-coverage for $(\mu_t)_{t=1}^\infty$ if
\[
\liminf_{m\to\infty}\mathbb P(\forall t\ge m,\ \mu_t\in C_t(m))\ge1-\alpha,
\]
(16)
and we say that this coverage is sharp if the above inequality holds with equality.''',[13],[],[r'\liminf_{m\to\infty}',r'\forall t\ge m'],'Coverage of a family indexed by later starting times m. This definition differs from relative-width approximation in Definition2.1. Sharp means equality of the displayed liminf; Theorem2.8 additionally states an ordinary limit equality.','Definition 2.7 — Asymptotic time-uniform coverage',context='Definition 2.7 (Asymptotic time-uniform coverage).')
add(12,'tuning',r'''we will now choose $\rho_m$ based on the first peeking time $m$ as
\[
\rho_m:=\rho(\widehat\sigma_m^2m\log(m\vee e))\equiv\sqrt{\frac{-2\log\alpha+\log(-2\log\alpha)+1}{\widehat\sigma_m^2m\log(m\vee e)}}.
\]''',[13],[],[r'\rho_m',r'\widehat\sigma_m^2m\log(m\vee e)'],'Starting-time-dependent tuning, based on the estimated variance at m and m log(m∨e). No arbitrary fixed-rho substitution yields Theorem2.8’s stated sharp coverage. A positive denominator is needed; the source does not specify how to handle initial zero estimates.','Section 2.5 — Tuning at the first peeking time',context='after appropriate tuning, our AsympCSs have asymptotic $(1-\alpha)$ coverage uniformly for all $t\ge m$ as $m\to\infty$',context_page=12)
add(11,'Gaussian mixture AsympCS',r'''Then, let $(\widetilde C_t(m))_{t=m}^\infty$ be the Gaussian mixture AsympCS with $\rho_m$ plugged into the expression of the boundary for all $t\ge m$:
\[
\widetilde C_t(m):=\left(\widehat\mu_t\pm\sqrt{\frac{2(t\widehat\sigma_t^2\rho_m^2+1)}{t^2\rho_m^2}\log\left(\frac{\sqrt{t\widehat\sigma_t^2\rho_m^2+1}}\alpha\right)}\right).
\]
(18)''',[13],[12],[r'\widetilde C_t(m)',r't\widehat\sigma_t^2\rho_m^2+1'],'Original later-started interval formula18. The variance appears inside the Gaussian-mixture expression and rho_m is fixed from the first peeking time. Sample mean and variance-estimator meanings are auxiliary context; this formula does not itself impose L1/L2/L3eta.','Section 2.5 — Later-started Gaussian mixture boundary (18)')
add(13,'Lyapunov-type condition',r'''Suppose $(Y_t)_{t=1}^\infty$ is a sequence of independent random variables with individual means and variances given by $\mu_t:=\mathbb E(Y_t)$ and $\sigma_t^2:=\operatorname{var}(Y_t)$, respectively. Suppose that in addition to Condition L-1 and the Lyapunov-type condition $\sum_{i=1}^\infty[\mathbb E|Y_i-\mu_i|^{2+\delta}/\sqrt{V_i}^{2+\delta}]<\infty$, we have the following regularity conditions:
\[
\sum_{i=1}^\infty\frac{\mathbb E|Y_i^2-\mathbb EY_i^2|^{1+\beta}}{V_i^{1+\beta}}<\infty,\qquad\widetilde\mu_t^2=o(V_t)\ \mathrm{a.s.},\quad\text{and}\quad\frac1t\sum_{i=1}^t(\mu_i-\widetilde\mu_t)^2=o(\widetilde\sigma_t^2)
\]
(14)
for some $\beta\in(0,1)$. In other words, the higher moments of $(Y_t)_{t=1}^\infty$, the running mean $\widetilde\mu_t$, and the cumulative “variation in means” $\sum_{i=1}^t(\mu_i-\widetilde\mu_t)^2$ all cannot diverge too quickly relative to $(V_t)_{t=1}^\infty$.''',[12],[6,7],[r'\mathbb E|Y_i-\mu_i|^{2+\delta}',r'\mathbb E|Y_i^2-\mathbb EY_i^2|^{1+\beta}',r'\widetilde\mu_t^2=o(V_t)',r'\frac1t\sum_{i=1}^t(\mu_i-\widetilde\mu_t)^2'],'All original Corollary2.6 hypotheses imported by Theorem3.3 with Y_t replaced by bar-f(Z_t). Preserve cumulative variance, centered Lyapunov sum, centered squared-observation sum, running-mean condition and relative variation in means. The preceding main text specifies delta>0; preserve that context separately. Do not replace the whole condition by an informal bounded-moments shortcut.','Corollary 2.6 — Assumptions imported by Theorem 3.3',kind='assumption')
add(14,'average treatment effect',r'''Our target estimand is the average treatment effect (ATE) $\psi$ defined as
\[
\psi:=\mathbb E(Y^1-Y^0),
\]
where $Y^a$ is the counterfactual outcome for a randomly selected subject had they received treatment $a\in\{0,1\}$. The ATE $\psi$ can be interpreted as the average population outcome if everyone were treated $\mathbb E(Y^1)$ versus if no one were treated $\mathbb E(Y^0)$.''',[16],[],[r'\psi:=\mathbb E(Y^1-Y^0)',r'Y^a'],'Potential-outcome ATE, separate from the identifying observed-data functional and its assumptions. Baseline iid triplets for Section3 are retained in auxiliary context.','Section 3 — Average treatment effect')
add(15,'causal identification assumptions',r'''Under standard causal identification assumptions — typically referred to as consistency, positivity, and exchangeability (see e.g. Kennedy [24, §2.2]) —''',[16],[],[], 'The source names consistency, positivity and exchangeability as standing assumptions. It does not formally expand their potential-outcome predicates in the inspected main text; preserve the named requirement and unresolved detail, not an invented original assumption statement. They identify both the fixed ATE and each time-indexed effect.','Section 3 — Causal identification assumptions',kind='assumption',phrases=['consistency, positivity, and exchangeability'])
add(16,'conditional mean function',r'''Since $\mu^a$ is simply a conditional mean function, we can use virtually any regression techniques to estimate it.''',[18],[],[r'\mu^a'],'Original main-text description of the treatment-specific regression function. Its role is established by the identified functional and EIF24; the main text does not separately print a full equation mu^a(x)=E(Y|X=x,A=a), so that interpretation remains explanatory context rather than a rewritten definition.','Section 3.2 — Regression-function source terminology',kind='source_passage')
add(17,'propensity score',r'''Consider a sequential randomized experiment so that a subject with covariates $x$ has a known propensity score
\[
\pi(x):=\mathbb P(A=1\mid X=x).
\]''',[18],[],[r'\pi(x):=\mathbb P(A=1\mid X=x)'],'Conditional treatment probability. The quoted passage introduces it in a known-propensity randomized setting; Theorem3.2 explicitly changes it to unknown. Referencing the probability object does not assume it is known in every theorem.','Section 3.2 — Propensity score')
add(18,'efficient influence function',r'''where $\widehat f_{T'}$ is given by the so-called efficient influence function (a brief review of semiparametric efficient estimators can be found in Appendix B.8),
\[
f(z)\equiv f(x,a,y):=\{\mu^1(x)-\mu^0(x)\}+\left(\frac a{\pi(x)}-\frac{1-a}{1-\pi(x)}\right)\{y-\mu^a(x)\},
\]
(24)''',[17],[16,17],[r'f(x,a,y)',r'\frac a{\pi(x)}-\frac{1-a}{1-\pi(x)}'],'Original uncentered ATE influence formula24, whose expectation is psi; it is not the centered mean-zero f-psi. The source explicitly calls it uncentered later onpage22. No appendix semiparametric exposition is imported.','Section 3.1.1 — Efficient influence function (24)')
add(19,'sample splitting',r'''We will denote $\mathcal D_\infty^{\mathrm{trn}}$ and $\mathcal D_\infty^{\mathrm{eval}}$ as the “training” and “evaluation” sets, respectively. At time $t$, we assign $Z_t$ to either group with equal probability:
\[
Z_t\in\begin{cases}\mathcal D_\infty^{\mathrm{trn}}&\text{with probability }1/2,\\\mathcal D_\infty^{\mathrm{eval}}&\text{otherwise.}\end{cases}
\]
Note that at time $t+1$, $Z_t$ is not re-randomized into either split — once $Z_t$ is randomly assigned to one of $\mathcal D_\infty^{\mathrm{trn}}$ or $\mathcal D_\infty^{\mathrm{eval}}$, they remain in that split for the remainder of the study. In this way, we can write $\mathcal D_\infty^{\mathrm{trn}}=(Z_1^{\mathrm{trn}},Z_2^{\mathrm{trn}},\ldots)$ and $\mathcal D_\infty^{\mathrm{eval}}=(Z_1^{\mathrm{eval}},Z_2^{\mathrm{eval}},\ldots)$ and think of these as independent, sequential observations from a common distribution $\mathbb P$. To keep track of how many subjects have been randomized to $\mathcal D_\infty^{\mathrm{eval}}$ at time $t$, define
\[
T:=|\mathcal D_\infty^{\mathrm{eval}}|\quad\text{and}\quad T':=|\mathcal D_\infty^{\mathrm{trn}}|=t-T,
\]
where we have left the dependence on $t$ implicit.''',[16],[],[r'\mathcal D_\infty^{\mathrm{trn}}',r'T:=|\mathcal D_\infty^{\mathrm{eval}}|'],'Permanent random training/evaluation assignment and time-dependent fold counts. The source uses infinity subscripts for streams while using their counts at time t; preserve the explicit convention. Theorem3.3 keeps the split mechanism but replaces the common-law iid setting with independent non-identical data.','Section 3.1 — Sequential sample splitting',context='3.1 Sequential sample splitting and cross fitting')
add(20,'estimators',r'''with $\eta\equiv(\mu^1,\mu^0,\pi)$ replaced by $\widehat\eta_{T'}\equiv(\widehat\mu_{T'}^1,\widehat\mu_{T'}^0,\overline\pi_{T'})$ — where $\overline\pi_{T'}$ may be an estimator $\widehat\pi_{T'}$ of the propensity score $\pi$, or the propensity score itself, depending on whether one is considering an observational study or randomized experiment — so that $\widehat\eta_{T'}$ is built solely from $\mathcal D_\infty^{\mathrm{trn}}$.''',[17],[18,19],[r'\widehat\eta_{T\prime}',r'\overline\pi_{T\prime}'],'Fitted influence function obtained by substituting training-only nuisance estimates into24, with either estimated or true propensity. The evaluation-fold version swaps roles of the two splits. The full original context explicitly determines which observations can train each function.','Section 3.1.1 — Fitted influence function by nuisance substitution',context='The sequential sample-split estimators',context_page=16)
members['D20']['highlight_symbols']=[r"\widehat\eta_{T'}",r"\overline\pi_{T'}"]
add(21,'cross-fit estimator',r'''An easy fix is to cross-fit: swap the two samples, using the evaluation set $\mathcal D_\infty^{\mathrm{eval}}$ for training and the training set $\mathcal D_\infty^{\mathrm{trn}}$ for evaluation to recover the full sample size of $t=T+T'$ [45, 69, 7]. That is, construct $\widehat f_T$ solely from $\mathcal D_\infty^{\mathrm{eval}}$ and define the cross-fit estimator $\widehat\psi_t^\times$ as
\[
\widehat\psi_t^\times:=\frac{\sum_{i=1}^T\widehat f_{T'}(Z_i^{\mathrm{eval}})+\sum_{i=1}^{T'}\widehat f_T(Z_i^{\mathrm{trn}})}t,
\]
(25)''',[17],[19,20],[r'\widehat\psi_t^\times',r"\widehat f_{T'}(Z_i^{\mathrm{eval}})",r'\widehat f_T(Z_i^{\mathrm{trn}})'],'Cross-fit estimator uses both folds, each evaluated by a function trained solely on the opposite fold. Each numerator sum uses the current fitted function, not a different online fit per i. This distinction is essential to the source dependency and non-iid statement.','Section 3.1.2 — Sequential cross-fit estimator (25)')
add(22,'cross-fit variance estimate',r'''and the associated cross-fit variance estimate
\[
\widehat{\operatorname{var}}_t(\widehat f):=\frac{\widehat{\operatorname{var}}_T(\widehat f_{T'})+\widehat{\operatorname{var}}_{T'}(\widehat f_T)}2,
\]
(26)
where $\widehat{\operatorname{var}}_T(\widehat f_{T'})$ is the $\mathcal D_\infty^{\mathrm{eval}}$-sample variance of the pseudo-outcomes, $(\widehat f_{T'}(Z_i^{\mathrm{eval}}))_{i=1}^T$ and similarly for $\widehat{\operatorname{var}}_{T'}$ (we deliberately omit the subscript on $\widehat f$ in the left-hand side of (26)).''',[17],[19,20],[r'\widehat{\operatorname{var}}_t(\widehat f)',r'\widehat{\operatorname{var}}_{T\prime}'],'Average of the two fold sample variances with equal1/2 weights, not a pooled variance or T/t-weighted average. Theorem3.3 prints bar-f as the argument instead of fitted f; retain that source discrepancy and the unresolved feasible/pooled-versus-fold interpretation separately.','Section 3.1.2 — Cross-fit variance estimate (26)')
members['D22']['highlight_symbols']=[r'\widehat{\operatorname{var}}_t(\widehat f)',r"\widehat{\operatorname{var}}_{T'}(\widehat f_T)"]
add(23,'randomized experiment',r'''Consider the cross-fit AIPW estimator $\widehat\psi_t^\times$ as given in (25) but with estimated propensity scores — $\widehat\pi_{T'}(x)$ and $\widehat\pi_T(x)$ — replaced by their true values $\pi(x)$, and with $\widehat\mu_{T'}^a$ and $\widehat\mu_T^a$ being possibly misspecified estimators for $\mu^a$. We will assume that $\widehat\mu_t^a$ converges to some function $\overline\mu^a$, which need not coincide with $\mu^a$. In what follows, when we use $\widehat\mu_t^a$ or $\widehat f_t$ in writing $\|\widehat\mu_t^a-\overline\mu^a\|_{L_2(\mathbb P)}$ or $\|\widehat f_t-\overline f\|_{L_2(\mathbb P)}$, we are referring to large-sample properties of the estimator (and hence $\widehat f_t$ could be replaced by $\widehat f_{T'}$ or $\widehat f_T$ without loss of generality).''',[18],[16,17,20,21],[r'\pi(x)',r'\overline\mu^a'],'Randomized-experiment specialization: true propensity is used and regression limits may be misspecified. Nuisance convergence refers to either growing training fold. Theorem3.2 changes the known-propensity premise and requires consistent nuisance functions; this full randomized-only premise is not imported into it.','Section 3.2 — Known propensity and possibly misspecified regression',kind='source_passage',context='Consider a sequential randomized experiment so that a subject with covariates $x$ has a known propensity score')
add(24,'influence function',r'''Notice that since $\widehat\mu_t^a$ is consistent for a function $\overline\mu^a$, we have that $\widehat f_t$ is converging to some influence function $\overline f$ of the form
\[
\overline f(z)\equiv\overline f(x,a,y):=\{\overline\mu^1(x)-\overline\mu^0(x)\}+\left(\frac a{\pi(x)}-\frac{1-a}{1-\pi(x)}\right)\{y-\overline\mu^a(x)\}.
\]
(27)''',[18],[16,17],[r'\overline f(x,a,y)',r'\overline\mu^1(x)-\overline\mu^0(x)'],'Limit influence function with the true propensity and potentially misspecified regression limits. Its formula does not itself assume the propensity is known. Theorem3.1 imposes its moment condition, and Theorem3.3 substitutes bar-f(Z_t) into Corollary2.6 conditions. Theorem3.2 uses the efficient f instead.','Section 3.2 — Limiting influence function (27)')
add(25,'individual treatment effects',r'''Consider a strict generalization where distributions — and hence individual treatment effects in particular — may change over time. In other words,
\[
\psi_t:=\mathbb E\{Y_t^1-Y_t^0\}\overset{(\star)}\equiv\mathbb E\{\mathbb E(Y_t\mid X_t,A_t=1)-\mathbb E(Y_t\mid X_t,A_t=0)\},
\]
where the equality $(\star)$ holds under the familiar causal identification assumptions discussed earlier. Despite the non-stationary and non-i.i.d. structure, it is nevertheless possible to derive AsympCSs for the running average of individual treatment effects $\widetilde\psi_t:=\frac1t\sum_{i=1}^t\psi_i$ — or simply, the running average treatment effect — using the Lyapunov-type bounds of Corollary 2.6.''',[20],[15],[r'\psi_t:=\mathbb E\{Y_t^1-Y_t^0\}',r'\widetilde\psi_t:=\frac1t\sum_{i=1}^t\psi_i'],'Time-indexed population treatment effects and their running mean. The source calls them individual effects but still takes expectations, so do not reinterpret them as realized unit-level differences. The Corollary2.6 mention is motivation; its actual assumption import is a direct T3.3 dependency.','Section 3.4 — Time-varying treatment effects',kind='source_passage')
add(26,'Regression estimator',r'''We assume that regression estimators $\widehat\mu_t^a(X_i)$ converge in $L_2(\mathbb P)$ to any function $\overline\mu^a(X_i)$ uniformly for $i\in\{1,2,\ldots\}$ i.e.
\[
\sup_{1\le i<\infty}\|\widehat\mu_t^a(X_i)-\overline\mu^a(X_i)\|_{L_2(\mathbb P)}=o(1)
\]
for each $a\in\{0,1\}$.''',[20],[16],[r'\sup_{1\le i<\infty}',r'\widehat\mu_t^a(X_i)-\overline\mu^a(X_i)'],'Uniformity over all observation indices i, not merely each fixed i. The limit regression need not be true under this condition alone. Almost-sure little-o convention is separately archived.','Condition ATẼ-1 — Regression estimator is uniformly well-behaved in L₂(P)',kind='condition',context='Condition $\widetilde{\mathrm{ATE}}$-1 (Regression estimator is uniformly well-behaved in $L_2(\mathbb P)$).')
add(27,'Convergence of average nuisance errors',r'''Let $\widehat\mu_t^a$ be an estimator of the regression function $\mu^a$, $a\in\{0,1\}$ and $\widehat\pi_t$ an estimator of the propensity score $\pi$. We assume that the average bias shrinks at a $\sqrt{\log t/t}$ rate, i.e.
\[
\frac1t\sum_{i=1}^t\left\{\|\widehat\pi_t(X_i)-\pi(X_i)\|_{L_2(\mathbb P)}\sum_{a=0}^1\|\widehat\mu_t^a(X_i)-\mu^a(X_i)\|_{L_2(\mathbb P)}\right\}=o\left(\sqrt{\frac{\log t}t}\right).
\]
(28)''',[21],[16,17],[r'\frac1t\sum_{i=1}^t',r'\widehat\pi_t(X_i)-\pi(X_i)'],'Average product of nuisance L2 errors at the current training time t over observations i≤t. Do not replace it with the product of average errors, with pointwise convergence, or with the fixed-distribution T3.2 rate. Under known propensity the propensity error is zero.','Condition ATẼ-2 — Convergence of average nuisance errors',kind='condition',context='Condition $\widetilde{\mathrm{ATE}}$-2 (Convergence of average nuisance errors).')
add(28,'propensity scores',r'''Suppose that propensity scores are bounded away from 0 and 1, i.e. $\pi(X)\in[\delta,1-\delta]$ almost surely for some $\delta>0$''',[18],[17],[r'\pi(X)\in[\delta,1-\delta]'],'Original true-propensity overlap condition in T3.1, retained under the common-setup reference in T3.2. The theorem does not separately assert the same bound for estimated propensities; no truncation assumption is inserted. Theorem3.3 does not explicitly cite T3.1, so any stronger global overlap import remains unresolved rather than silently added.','Theorem 3.1 — Propensity overlap condition',kind='theorem_excerpt')
# The paper uses a tilde over ATE in both numbered condition labels.
for n in [26,27]:
    m=members['D'+str(n)]
    m['source_heading']=m['local_label']=m['local_label'].replace('ATẼ',r'$\widetilde{\mathrm{ATE}}$')
    m['highlight_phrases']=[r'$\widetilde{\mathrm{ATE}}$-'+str(n-25)]
# Name fitted nuisance construction with the paper's explicit Figure3 terminology.
x=next(x for x in interfaces if x['members'][0]['local_id']=='D20');m=members['D20']
m['naming_context']=[dict(context_id='D20/name',text=r"Nuisance function estimators $(\widehat\mu_{T'}^1,\widehat\mu_{T'}^0,\widehat\pi_{T'})$ are constructed using $\mathcal D_\infty^{\mathrm{trn}}$ which then yield $\widehat f_{T'}$.",evidence=[dict(page=17,location='Figure3 caption')])]
x['source_keywords']=[dict(paper_id=PID,local_id='D20',source_text='Nuisance function estimators',label='Nuisance function estimators',kind='term',context_id='D20/name')];x['name']='Nuisance function estimators'
# Keep formula definitions separate from introductory estimation commentary.
for n,term in [(18,'efficient influence function'),(24,'influence function')]:
    m=members['D'+str(n)];intro,formula=m['statement_original'].split(r'\[',1)
    m['statement_original']=r'\['+formula
    m['naming_context']=[dict(context_id=m['local_id']+'/name',text=intro.strip(),evidence=m['evidence'])]
    x=next(x for x in interfaces if x['members'][0]['local_id']==m['local_id'])
    x['source_keywords'][0]['context_id']=m['local_id']+'/name'
members['D23']['depends_on'].append('D24')
def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
