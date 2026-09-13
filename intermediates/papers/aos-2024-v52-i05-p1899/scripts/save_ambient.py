# -*- coding: utf-8 -*-
"""Save original scope context, local bindings and unresolved source conventions.

Reproduction does not perform independent source review.
"""
import json
from save_inventory import ROOT,PID
A=[]
def passage(n,s,pages,note):A.append(dict(local_id=f'A{n}',statement_original=s,evidence=[dict(page=p,location=f'Main-text scope passage A{n}') for p in pages],scope_note=note))
passage(1,r'''Finally, we collect some notations that are used throughout the paper. We denote the set of natural numbers by $\mathbb N$, i.e., $\mathbb N:=\{1,2,\ldots\}$, and for any $n\in\mathbb N$ we set $[n]:=\{1,\ldots,n\}$. We denote by $\mathbb R$ the set of real numbers and for any $a,b\in\mathbb R$ we set $a\vee b\equiv\max\{a,b\}$ and $a\wedge b\equiv\min\{a,b\}$. $|A|$ represents the cardinality of a finite set $A$. For a square matrix $M$, we denote by $\det(M)$ its determinant and by $\operatorname{tr}(M)$ its trace. For any $p\in\mathbb N$, we denote by $N_p(\mu,\Sigma)$ the $p$-variate Gaussian distribution with mean vector $\mu$ and covariance matrix $\Sigma$, and omit the subscript when $p=1$. For a probability measure $P$, we denote by $\mathbb E_P$, $\operatorname{Var}_P$ and $\operatorname{Corr}_P$ the corresponding expectation, variance and correlation, respectively. Finally, for any sequences of positive numbers $(x_n)$ and $(y_n)$, we write $x_n\sim y_n$ for $\lim_n(x_n/y_n)=1$ and $x_n\lesssim y_n$ for $\limsup_n(x_n/y_n)\leq1$.''',[2,3],'Source asymptotic comparison is first-order sharp, not a bound up to an arbitrary constant. Natural numbers begin at 1.')
passage(2,r'''Based on Theorems 3.1 and 3.2, in what follows we assume that

• when $\emptyset\notin\Psi$, $\{A_e,B_e\}_{e\in\mathcal K}$ are selected, as functions of $\gamma,\delta\in(0,1)$, so that
\[
\chi^*\in\mathcal C_\Psi(\gamma,\delta)\quad\forall\gamma,\delta\in(0,1),
\]
\[
\log A_e\sim|\log\delta|,\quad\log B_e\sim|\log\gamma|\quad\forall e\in\mathcal K\quad\text{as }\gamma,\delta\to0,
\]
(8)
• when $\emptyset\in\Psi$, $\{A_e,B_e,C_e,D_e\}_{e\in\mathcal K}$ are selected, as functions of $\alpha,\beta,\gamma,\delta\in(0,1)$, so that
\[
\chi^*_{\mathrm{det}}\in\mathcal D_\Psi(\alpha,\beta),\quad\chi^*_{\mathrm{fwer}}\in\mathcal E_\Psi(\gamma,\delta),\quad\chi^*\in\mathcal C_\Psi(\alpha,\beta,\gamma,\delta)\quad\forall\alpha,\beta,\gamma,\delta\in(0,1),
\]
\[
\log A_e\sim|\log\delta|,\quad\log B_e\sim|\log\gamma|,\quad\log C_e\sim|\log\beta|,\quad\log D_e\sim|\log\alpha|\quad\forall e\in\mathcal K\quad\text{as }\alpha,\beta,\gamma,\delta\to0.
\]
(9)''',[9],'Standing threshold calibration for subsequent performance results. The four-tolerance asymptotic statement and later mixed fixed/vanishing regimes require careful scope recording; no stronger uniformity is silently added.')
passage(3,r'''We further assume that
\[
A_e=A,\quad B_e=B,\quad C_e=C,\quad D_e=D\qquad\text{for every }e\in\mathcal K.
\]
(10)
The latter is not needed for any of the results in Section 4, but simplifies the implementation of the proposed tests in Section 5.1, and is also used in Theorem 6.1.''',[9],'Common thresholds are essential to the explicit stopping-rule forms, not an additional hypothesis needed by the Section 4 bounds.')
passage(4,r'''To state the main results of this section we assume that, for every
\[
e\in\mathcal K,\quad P\in\mathcal G_{\Psi,e},\quad Q\in\mathcal H_{\Psi,e}\cup\mathcal H_0,\quad e\subseteq s\subseteq[K],
\]
there are positive numbers, $\mathcal I(P^s,Q^s)$ and $\mathcal I(Q^s,P^s)$, such that as $n\to\infty$
\[
P\left(\max_{1\leq m\leq n}Z_m(P^s,Q^s)\geq n\rho\right)\to0\qquad\text{for all }\rho>\mathcal I(P^s,Q^s),
\]
\[
Q\left(\max_{1\leq m\leq n}Z_m(Q^s,P^s)\geq n\rho\right)\to0\qquad\text{for all }\rho>\mathcal I(Q^s,P^s),
\]
(11)
\[
\sum_{n=1}^\infty P(Z_n(P^s,Q^s)<n\rho)<\infty\qquad\text{for all }\rho<\mathcal I(P^s,Q^s),
\]
\[
\sum_{n=1}^\infty Q(Z_n(Q^s,P^s)<n\rho)<\infty\qquad\text{for all }\rho<\mathcal I(Q^s,P^s).
\]
(12)''',[9,10],'Two distinct distributional conditions: upper maximal-tail convergence and summable lower tails, in both likelihood directions. Theorems 4.1 and 4.2 explicitly select (12); Sections 4.4, 5 and 6 retain both as standing assumptions. Their definitions should be split for final interface extraction.')
passage(5,r'''Our standing assumption in the remainder of this section is that conditions (11)-(12) hold.''',[12],'Section 4.4 scope for Theorems 4.3–4.6; this prose is not inserted into their original bodies.')
passage(6,r'''In this section we apply the results of Sections 2-4 to the problem of detecting and isolating anomalous sources. That is, throughout this section the units are the data sources themselves, i.e., $\mathcal K=\{\{k\}:k\in[K]\}$ and, as a result, the hypotheses refer to the marginal distributions of the data sources. Moreover, we assume that the distributional assumptions (11)-(12) are satisfied, thus, all asymptotic optimality results in Section 4 hold when the subsystems are large enough.''',[14],'Section 5 has singleton units and both distributional assumptions, while independence applies only to Subsection 5.1.')
passage(7,r'''\[
P=P^1\otimes\cdots\otimes P^K\quad\text{for every }P\in\mathcal P_\Psi,
\]
(21)''',[14],'Independence of the full source sequences under every plausible global distribution, not merely contemporaneous pairwise independence.')
passage(8,r'''Throughout this subsection we assume that the data sources are independent, i.e., (21) holds, and that arbitrary lower and upper bounds, $l$ and $u$, are given on the number of signals, i.e., $\Psi=\Psi_{l,u}$.''',[15],'Subsection 5.1 scope for Theorems 5.1–5.4. Theorem 5.1 does not repeat the bounded-cardinality prior or the independence assumption in its original body.')
passage(9,r'''In the rest of this subsection we set either $s'_k=\{k\}$ for every $k\in[K]$ or $s'_k=[K]$ for every $k\in[K]$, and focus on the form of the stopping rules.''',[15],'Additional source convention preceding Theorem 5.2; each later theorem retains its explicitly stated subsystem choices.')
passage(10,r'''In this subsection we do not assume that the independence assumption (21) holds, and we do not make any assumption regarding the form of the prior information, $\Psi$. We only assume that $\emptyset\in\Psi$, so that the detection problem is relevant, and focus on the joint detection and isolation problem, restricting our attention to the test $\chi^*$, introduced in Subsection 3.2.3.''',[17],'Subsection 5.2 removes the global independence and bounded-cardinality restrictions; Theorems 5.5 and 5.6 impose source-specific independence only in sufficient conditions for ARE=1.')
passage(11,r'''For this reason, we focus on the case that the subsystems are selected as small as possible, i.e., $s_k=s'_k=\{k\}$ for every $k\in[K]$, so that the implementation of $\chi^*$ requires only the ordering of the local statistics, introduced in (5). For this version of $\chi^*$, we upper bound the asymptotic relative efficiency,
\[
\operatorname{ARE}_P[\chi^*]:=\limsup\frac{\mathbb E_P[T^*]}{\inf\{\mathbb E_P[T]:(T,D)\in\mathcal C_\Psi(\alpha,\beta,\gamma,\delta)\}},
\]
(22)
as $\alpha,\beta,\gamma,\delta$ go to $0$ at various relative rates, for different $P\in\mathcal P_\Psi$ and $\Psi$, and establish sufficient conditions for its asymptotic optimality.''',[17,18],'ARE is expected sample size divided by the optimal expected sample size, hence lower is better and optimal value is 1. Theorem-specific asymptotic paths take precedence over the introductory all-four-vanish wording. Theorem 5.5 repeats only s-prime, 5.6 only s; the source prose supplies the broader local-subsystem context.')
passage(12,r'''To be specific, throughout this section the units are pairs of data sources, i.e.,
\[
\mathcal K=\{\{i,j\}:1\leq i<j\leq K\},
\]
and the components of $X^e$ are independent (resp. dependent) under $P$ when $P^e$ belongs to $\mathcal H^e$ (resp. $\mathcal G^e$) for every $e\in\mathcal K$ and $P\in\mathcal P_\Psi$. We also assume that conditions (11) and (12) are satisfied and, as a result, all asymptotic optimality results in Section 4 hold when the detection and isolation subsystems are equal to $[K]$.''',[19,20],'Section 6 pairwise dependence testing scope. Do not import the Gaussian specialization from Subsection 6.2 into these general Theorems.')
passage(13,r'''For this result, as well as some others in this section, we also assume that, under any $P\in\mathcal P_\Psi$,
\[
s_1,s_2\subseteq[K]\text{ are disjoint and independent}\quad\Longleftrightarrow\quad\{i,j\}\notin\mathcal A(P)\quad\forall i\in s_1,j\in s_2.
\]
(23)''',[20],'A separate property imposed only where expressly assumed or used as an example. Preserve the source quantifier wording and do not conflate pairwise independence with independence of groups in arbitrary distributions.')
passage(14,r'''Moreover, we focus on the joint detection and isolation problem, thus, we assume that $\emptyset\in\Psi$, and restrict our attention to the test $\chi^*$, introduced in Subsection 3.2.3. We also note that, for every $P\in\mathcal P_\Psi$, there is a disjoint partition of $[K]$, $v_0,v_1,\ldots,v_{L(P)}$, such that
\[
P=P^{v_0}\otimes P^{v_1}\otimes\cdots\otimes P^{v_{L(P)}},
\]
where $v_0$ is the subset of $[K]$ that consists of the independent sources under $P$. This decomposition is used in the statement of the main results of this section.''',[20],'Partition convention for Theorems 6.2–6.5, with Theorem 6.6 explicitly returning to the familywise test. The source does not separately specify a uniqueness/minimality rule for the dependent blocks.')
passage(15,r'''For each unit $e\in\mathcal K$ we select two subsets of $[K]$, $s_e,s'_e\subseteq[K]$, that both include $e$, i.e., $e\subseteq s_e\cap s'_e$, to which we refer as the subsystems of unit $e$. Then, at each time $n\in\mathbb N$, we compute the values of the following GLR-type statistics,''',[7],'Binds both subsystem choices for D16-D17; their displayed statistics are preserved separately.')
passage(16,r'''where $P_0$ and $P'_0$ are arbitrary distributions from $\mathcal H_0^{s_e}$ and $\mathcal H_0^{s'_e}$, respectively.''',[7],'Reference-law choices accompanying the two GLR displays. Nonemptiness is not added to the source.')
passage(17,r'''We say that a test $(T,D)\in\mathcal C_\Psi$ commits under some $P\in\mathcal P_\Psi$

• a false alarm when there is no signal but at least one unit is identified as such, i.e., when $\mathcal A(P)=\emptyset$ and the event $D\ne\emptyset$ occurs,

• a missed detection when there is at least one signal but no unit is identified as such, i.e., when $\mathcal A(P)\ne\emptyset$ and the event $D=\emptyset$ occurs,

• a false positive when there is at least one true signal and at least one mistakenly identified signal, i.e., when $\mathcal A(P)\ne\emptyset$ and the event $D\setminus\mathcal A(P)\ne\emptyset$ occurs,

• a false negative when at least one unit is identified as a signal and there is also at least one missed signal, i.e., when the events $D\ne\emptyset$ and $\mathcal A(P)\setminus D\ne\emptyset$ both occur.''',[5],'Original four error descriptions; the conditions involving nonempty A(P) and nonempty D distinguish this formulation from ordinary familywise events.')
passage(18,r'''If it is assumed that there are exactly $m$ signals, i.e., $\Psi=\Psi_{m,m}$, where $m\in(0,|\mathcal K|)$, then
\[
\mathcal C_\Psi(\gamma,\delta)=\{(T,D)\in\mathcal C_\Psi:P(D\ne\mathcal A(P))\leq\gamma\wedge\delta\quad\forall P\in\mathcal P_\Psi\},
\]
since, in this case, whenever a false positive occurs so does a false negative, and vice versa.''',[5],'Remark 2.3 explains the shared error target for fixed cardinality. It is auxiliary context, not an additional inventoried Theorem.')
passage(19,r'''When $\emptyset\notin\Psi$, $\mathcal E_\Psi(\gamma,\delta)$ coincides with $\mathcal C_\Psi(\gamma,\delta)$.''',[6],'Equivalence of error classes when signals cannot be empty; this does not itself define the later familywise procedure for that prior.')
passage(20,r'''A main goal of this work is to propose tests, for each of the above formulations, that achieve the optimal expected sample size under every possible distribution to a first-order asymptotic approximation as the corresponding error probabilities go to $0$.''',[6],'Meaning of asymptotic optimality when the theorem states it in words. The class is selected by the named test and theorem, including familywise optimality in 5.4 and 6.6.')
passage(21,r'''When $e=\{k\}$ for some $k\in[K]$, we replace $e$ in $\Lambda_{e,\mathrm{det}}(n)$, $\Lambda_{e,\mathrm{iso}}(n)$, $\Lambda_e(n)$ by $k$, and write $\Lambda_{k,\mathrm{det}}(n)$, $\Lambda_{k,\mathrm{iso}}(n)$, $\Lambda_k(n)$, instead.''',[7],'Remark 3.1 singleton-index convention; the theorem notation also uses singleton-indexed hypothesis families.')
passage(22,r'''When the detection and isolation subsystems of unit $e\in\mathcal K$ are selected as small as possible, i.e., $s_e=s'_e=e$, then its isolation and detection statistics coincide and reduce to''',[7],'Original sentence leading to (5), whose formula is D19. Preserve this asserted reduction separately from the definition of the local ratio; do not infer a new prior-family richness assumption.')
passage(23,r'''In the latter case, we replace the superscript in $\mathcal H^e$ and $\mathcal G^e$ by $k$ when $e=\{k\}$ for some $k\in[K]$.''',[3],'Remark 2.1 explicitly supplies the singleton local-hypothesis alias following its singleton-unit example; global H_Psi,k/G_Psi,k indexing remains implicit in the later statements.')
EXTRA_ISSUES=[
('unit-count-versus-source-count','The powerset claim for Psi_0,K uses K streams although the general unit family can have more than K elements. The passage is retained verbatim; later singleton applications have |mathcal K|=K.',[4]),
('reference-law-existence','The two GLRs choose reference laws from projected H0 even when the prior excludes the empty configuration. The source calls H0 the global-null family but does not independently guarantee its nonemptiness for every allowed plausible-law family.',[4,7]),
('paired-threshold-calibration','The shared notation in (9) simultaneously lists the familywise test with A=C,B=D and four log-equivalences tied to potentially different tolerances. Treat separately calibrated procedures as the source context, not as a newly proved simultaneous equality for all rates.',[8,9]),
('stopping-time-ties','The joint decision uses strict T0<T_joint and T_joint<T0 branches. No tie or both-infinite convention is explicitly assigned; sufficiently separated positive thresholds may preclude some finite ties, but no convention is inserted.',[8]),
('finite-stopping-domain','The test definition states stopping and decision measurability but does not explicitly require almost-sure finite stopping. Expectations, decisions at infinity and infima of empty stopping sets retain their unstated-domain qualifications.',[5,7,8]),
('ordered-statistic-ties','Ordered likelihood ratios and indices are introduced without a tie-breaking convention. Do not claim unique indexed decisions from the ordering alone.',[7,15]),
('empty-information-extrema','Signal/nonsignal maxima and minima and family infima may have empty indexing sets under endpoint priors. The main text does not state every empty-set convention; preserve the displayed branches instead of adding a positive-signal-count assumption.',[10,11,12,18,22]),
('same-signal-alternatives','The fixed-cardinality expression in Theorem 4.3 uses P_Psi minus {P}, not only laws with a different A(P). Distinct global laws can share a signal configuration in the general model; the original denominator remains unchanged.',[12]),
('familywise-nonempty-prior-rule','Theorem 5.1 names T-star_fwer also in a setting allowing l>0, whereas Subsection 3.2.4 introduces that procedure under emptyset in Psi. Equality of the two error classes for nonempty priors is stated on page 6 but does not specify an extra stopping rule. Keep the branch context explicit.',[6,8,15]),
('local-hypothesis-index-alias','Remark 2.1 explicitly defines the local H^k,G^k singleton alias, saved in A23. Theorems 5.5-5.6 additionally write H_Psi,k and G_Psi,k for singleton global families; that natural index abbreviation is not separately defined by Remark 3.1, which addresses likelihood statistics.',[7,18]),
('ell-versus-l','Theorem 5.2(i) prints ell=u<K after introducing l. Preserve the printed ell and record its apparent alias rather than silently replacing it.',[15]),
('small-stream-endpoints','Some explicit rules use the second ordered statistic or the u+1 statistic. The text does not separately state every lower bound on K or admissible u needed for each index. Preserve the original case splits and record unresolved endpoint domains.',[16,17]),
('partition-choice','The partition v0,v1,...,v_L(P) is stated to exist, but no uniqueness or minimality convention is explicitly given for dependent blocks. Do not silently identify these with a newly defined canonical graph partition.',[20]),
('group-condition-overlap','Condition (23) quantifies over source subsets and places disjointness on its left side only. If the sets overlap, singleton pairs {i,i} do not belong to the pair-unit family, so the literal right side needs care. Preserve the printed equivalence rather than imposing a new disjoint-domain restriction.',[20]),
('theorem-local-stopping-names','T1,...,T6 are separately defined within Theorems 5.2, 5.3 and 5.4. They do not name common procedures across those statements; the familywise T0 also incorporates its own paired threshold.',[15,16,17]),
('scope-is-not-conjunction','A related-theorem edge records use somewhere in the statement or its standing context. It does not conjoin alternative branches: in particular (23) is optional in examples in 6.2, 6.4 and 6.5, while it is explicitly assumed in 6.1 and 6.6.',[20,21,22])]
BINDINGS={
'T3.1':'gamma,delta and candidate thresholds are bound here; m is bound only in (ii). (7) supplies a_e,b_e; no asymptotic distribution condition is imposed.',
'T3.2':'alpha,beta,gamma,delta and candidate thresholds are bound here. Theorem 3.1 is referenced only for numerical A_e,B_e choices. No distributional (11)/(12) is imported.',
'T4.1':'P and the gamma/delta limit are bound here. Unit extrema range over A(P) and its complement in mathcal K; only (12) is expressly required, with selection (8) standing.',
'T4.2':'P is bound and then split into global-null and non-null branches. Each of the five displayed bounds has its own tolerance limit; (9) is standing and only (12) is expressly required.',
'T4.3':'P and subsystem choices are bound; fixed m occurs in a final specialization. Both (11) and (12) are standing, with (8). Full-data s is omitted by Section 4.2 convention.',
'T4.4':'P is a global-null law; detection subsystems satisfy (17). Three error classes and three tolerance paths remain distinct. Fixed gamma/delta are expressly allowed only in the middle conclusion.',
'T4.5':'P is non-null and detection subsystems satisfy (18). The first two conclusions do not require (15); the final familywise conclusion adds (15) and a dominant-gamma path.',
'T4.6':'P is non-null. Conditions (15),(16),(18) are explicit; the two conclusions refer to different error classes and tolerance paths.',
'T5.1':'l,u come from Psi_l,u in the subsection. Singleton/full subsystem choices are conditional on l=0 as printed; T ranges over the two named rules. D_iso has an expressly empty boundary case.',
'T5.2':'l>=1 and s-prime_k=[K] are explicit; T1,...,T6 and their branching are local binders. The subsection supplies independence, Psi_l,u and common A,B.',
'T5.3':'l=0 and s_k=[K] are explicit. Its T_joint formula additionally assumes s-prime_k=[K]; T1,...,T5 are new local binders and products retain their stated indices.',
'T5.4':'l=0 and singleton detection are explicit. Each u branch pairs with its own isolation choice. T0,...,T4 are defined here; optimality is in the familywise class.',
'T5.5':'The model and (11)-(12) persist, but global independence and a fixed form of Psi are dropped in 5.2. A11 preserves the introductory local-subsystem scope; the theorem repeats only the isolation choice. The Psi_0,u and independent-hardest-source restrictions apply only to the respective equality claims.',
'T5.6':'The model and (11)-(12) persist; the theorem repeats only local detection while A11 records the preceding low-complexity context. The one-signal or Psi_1,1 conditions apply only to the relevant equality branch; gamma/delta may stay fixed in (ii).',
'T6.1':'Pair units and (11)-(12) are standing, (23) and Psi_dis explicit, common C,D from (10). B is a bound candidate set in the maximum, not threshold B.',
'T6.2':'Pair-model standing context applies. The containing-block case and the local-subsystem bound are distinct; the last two sufficient-condition bullets are alternatives. Only the first bullet assumes (23).',
'T6.3':'The four block-containment alternatives bind i,j,l,l-prime under the given P. The printed e minus v0 in v_l is preserved. No (23) is a standing prerequisite of this theorem.',
'T6.4':'Part (i) binds the signal e whose subsystem contains the dependent-block union. Part (ii) uses local subsystems; (23) appears only in its final sufficient-condition example.',
'T6.5':'P is global-null and gamma/delta can stay fixed. Psi_1,1 inclusion and an independent hardest pair are additional equality conditions; (23) is an example, not a premise of the bound.',
'T6.6':'P may be null or non-null. This theorem explicitly returns to the familywise procedure despite the preceding focus on joint ARE. Psi_dis, local subsystems, (23) and the independent hardest nonsignal pair are retained.'}

def main():
    d=dict(paper_id=PID,status='partial',unranked_auxiliary_passages=A,scope='Inspected original main-text scope context; full interface extraction and independent graph review are pending.',pending_source_issues=[
      dict(issue_id='disjoint-prior-self-pairs',description='Page 4 defines Psi_dis by if e,e-prime in A then e intersection e-prime is empty, without printing e != e-prime. Preserve the original formula and record its self-pair problem; do not silently repair.',evidence=[dict(page=4,location='Definition of Psi_dis')]),
      dict(issue_id='global-null-family',description='Page 4 writes H0 equivalent to P_emptyset, while Psi is a family of signal subsets and its null-only family would ordinarily be {emptyset}. Preserve the source notation and its intended context separately.',evidence=[dict(page=4,location='Definition of global null distributions')]),
      dict(issue_id='joint-class-domain',description='Page 6 writes the joint class as D_Psi intersect C_(Psi minus emptyset). The latter notation is ambiguous between an error restriction on non-null distributions and a test class whose decisions exclude the empty set. Preserve the source definitions and flag the tension with the proposed empty-output rule.',evidence=[dict(page=5,location='Tests and pure isolation class'),dict(page=6,location='Joint detection and isolation class')]),
      dict(issue_id='subset-membership',description='Theorem 6.3(i) prints e minus v0 in v_l, although the left side is a set. Inventory preserves the membership symbol rather than replacing it by subset.',evidence=[dict(page=21,location='Third subsystem-containment branch')]),
      dict(issue_id='standing-threshold-path',description='Equation (9) gives log-threshold equivalences as all four tolerances vanish; several Theorems allow gamma and delta fixed. The source does not separately state uniform coordinatewise calibration along all these paths.',evidence=[dict(page=9,location='Equation (9)'),dict(page=12,location='Theorem 4.4')]),
      dict(issue_id='local-statistic-reduction',description='Page 7 identifies local GLR statistics with projected constrained-global statistics when s_e=s-prime_e=e. For arbitrary prior restrictions this equality may require a richness/projection condition on the plausible families; preserve the assertion as A22 and retain the projected and unrestricted families as distinct source definitions.',evidence=[dict(page=7,location='Equation (5) and preceding paragraph')]),
      dict(issue_id='threshold-reference',description='Theorem 3.2(iii) references Theorem 3.1 for threshold choices, even though 3.1 assumes emptyset not in Psi. Resolve numerical thresholds without importing that contradictory precondition.',evidence=[dict(page=8,location='Theorem 3.1'),dict(page=9,location='Theorem 3.2(iii)')]),
      dict(issue_id='global-isolation-family',description='H_Psi,e excludes the global null, whereas G_Psi,e contains distributions with a signal in e. Nonemptiness for all units is not explicitly supplied by every prior. Maxima over empty hypothesis families and endpoint signal/non-signal sets require source-scope recording.',evidence=[dict(page=6,location='Beginning of Section 3'),dict(page=7,location='GLR statistics')])])
    d['status']='extracted'
    d['scope']='Original main-text scope, statement bindings and unresolved source conventions; independent source review remains a separate gate.'
    d['source_issues']=d.pop('pending_source_issues')
    d['source_issues'].extend(dict(issue_id=k,description=t,evidence=[dict(page=p,location='Original main-text convention or statement') for p in pages]) for k,t,pages in EXTRA_ISSUES)
    d['statement_local_bindings']=BINDINGS
    d['ambient_prerequisites']=[
        'Probability spaces, sigma-fields, stopping times, measurable decisions, Radon-Nikodym derivatives, marginal laws and full-sequence independence retain their source domains.',
        'Finite set operations, cardinality, order statistics, finite products, extrema and set differences use the printed conventions; unresolved empty-domain cases are recorded as source issues.',
        'Natural numbers begin at 1. Expectations and positive-number logarithms use their source domains. The source defines lesssim as limsup ratio at most 1, and sim as ratio tending to 1, in A1.',
        'The dominant-rate symbol >> in theorem statements is read as a ratio tending to infinity; this interpretation is analysis, not an added original definition.',
        's_e and s-prime_e contain unit e and lie within [K], as preserved in A15. Reference laws P0 and P0-prime are bound by A16.',
        'No temporal iid, Gaussian, universal group-independence or library-availability assumption is inserted into the general results.'
    ]
    d['source_claim_references']=[
        dict(from_claim_id=PID+'/T3.2',to_claim_ids=[PID+'/T3.1'],reference_kind='numerical_threshold_choice',scope='Only A_e,B_e choices; do not import the nonempty-prior hypothesis.'),
        dict(from_claim_id=PID+'/T4.5',to_claim_ids=[PID+'/T4.3'],reference_kind='numbered_condition',local_ids=['D31'],scope='Only condition (15) in the final familywise branch.'),
        dict(from_claim_id=PID+'/T4.6',to_claim_ids=[PID+'/T4.3',PID+'/T4.5'],reference_kind='numbered_conditions',local_ids=['D31','D32','D34'],scope='Only (15),(16),(18); not the full earlier theorem hypotheses or conclusions.')
    ]
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(A)} scope passages, {len(d["source_issues"])} source issues and all twenty statement bindings.')
if __name__=='__main__':main()
