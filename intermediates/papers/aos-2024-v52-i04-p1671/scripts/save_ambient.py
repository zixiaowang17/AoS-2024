"""Preserve source context and unresolved meanings without rewriting theorem statements."""
import json
from pathlib import Path
from save_inventory import PID
ROOT=Path(__file__).resolve().parents[1]
passages=[]
def add(lid,text,pages,heading,kind='definition'):
    passages.append(dict(paper_id=PID,local_id=lid,source_kind=kind,source_heading=heading,
        statement_original=text.strip(),evidence=[dict(page=p,location=heading) for p in pages]))
add('A1',r'''
For every vector $\boldsymbol v=(v_1,...,v_p)^{\mathrm T}$, define $|\boldsymbol v|_2=\sqrt{\sum_{l=1}^p v_l^2}$, $|\boldsymbol v|_1=\sum_{l=1}^p|v_l|$, and $|\boldsymbol v|_\infty=\max_{1\le l\le p}|v_l|$. Moreover, we use $\operatorname{supp}(\boldsymbol v)=\{l|v_l\ne0,1\le l\le p\}$ to denote the support of the vector $\boldsymbol v$, and define $\boldsymbol v_{-l}=(v_1,\ldots,v_{l-1},v_{l+1},\ldots,v_p)^{\mathrm T}$. For each matrix $\boldsymbol A\in\mathbb R^{p_1\times p_2}$, $\|\boldsymbol A\|=\sup_{|\boldsymbol v|_2=1}|\boldsymbol A\boldsymbol v|_2$, $\|\boldsymbol A\|_\infty=\max_{1\le l_1\le p_1,1\le l_2\le p_2}|A_{l_1,l_2}|$ and $\|\boldsymbol A\|_{L_\infty}=\sup_{|\boldsymbol v|_\infty=1}|\boldsymbol A\boldsymbol v|_\infty$. Furthermore, let $\Lambda_{\max}(\boldsymbol A)$ and $\Lambda_{\min}(\boldsymbol A)$ denote the largest and smallest eigenvalues of $\boldsymbol A$, respectively. We use $\mathbb I(\cdot)$ to denote the indicator function, and $\operatorname{sgn}(\cdot)$ to denote the sign function. For two sequences $\{a_n\}$, $\{b_n\}$, we say $a_n\asymp b_n$ if $a_n=O(b_n)$ and $a_n=\Theta(b_n)$ hold simultaneously. For simplicity, we let $\mathbb S^{p-1}$ and $\mathbb B^p$ denote the unit sphere and the unit ball in $\mathbb R^p$ centered on $\boldsymbol0$. For a sequence of vectors $\{\boldsymbol v_i\}_{i=1}^n\subseteq\mathbb R^p$, we define $\operatorname{med}(\cdot)$ as the coordinate-wise median. Finally, the generic constants were assumed to be independent of $m$, $n$, and $p$. We define $[p]$ to be the set $\{1,\ldots,p\}$.
''',[6],'Section 1.2 — notation')
add('A2',r'''
Formally, for each row $\boldsymbol Q_l^r$, we compute the number of positives, negatives, and nulls as follows:
\[
N_l^+=\sum_{j=1}^m\mathbb I(Q_{l,j}=1),\qquad
N_l^-=\sum_{j=1}^m\mathbb I(Q_{l,j}=-1),\qquad
N_l^0=\sum_{j=1}^m\mathbb I(Q_{l,j}=0).\tag{1}
\]
''',[7],'Section 2.1 — vote counts (1)')
add('A3',r'''
Let $\boldsymbol\theta^*=(\theta_1^*,\ldots,\theta_p^*)^{\mathrm T}$ be the true population parameter of interest. We denote $S$ as the support of $\boldsymbol\theta^*$ and $s=|S|$. We assume that the vector is sparse in the sense that many entries $\theta_l^*$ are zero. There are $N$ i.i.d. observations $\boldsymbol X_i$ that satisfy $\mathbb E[\boldsymbol X_i]=\boldsymbol\theta^*$ and are stored in $m$ machines $\mathcal H_j$ (where $1\le j\le m$), each holds $n_j$ (where $1\le j\le m$) samples. We assume that $n_j$'s have the same order as $n$, namely $n_1\asymp...\asymp n_m\asymp n$. We define $\mathbb X=\{\boldsymbol X_1,\ldots,\boldsymbol X_N\}$ as the full dataset. Our task is to identify $\operatorname{sgn}(\boldsymbol\theta^*)$ under DGDP.
''',[13],'Section 3.1 — mean-model setup','source_passage')
add('A4',r'''
Let $(\boldsymbol X_i,Y_i)$ (where $i=1,\ldots,N$) be the i.i.d. observations from the model
\[
Y=\boldsymbol X^{\mathrm T}\boldsymbol\theta^*+z,\tag{13}
\]
where $\boldsymbol\theta^*=(\theta_1^*,\ldots,\theta_p^*)^{\mathrm T}$ is the true sparse regression parameter, and $z$ is the noise independent of the covariate $\boldsymbol X$. The full dataset is denoted by $\mathbb X=\{(\boldsymbol X_1,Y_1),\ldots,(\boldsymbol X_N,Y_N)\}$, and it is assumed that $\mathbb X$ is divided into $m$ local machines $\mathcal H_j$ $(1\le j\le m)$, each holds $n_j$ samples. Similarly, we attempt to recover the sign vector $\operatorname{sgn}(\boldsymbol\theta^*)=(\operatorname{sgn}(\theta_1^*),\ldots,\operatorname{sgn}(\theta_p^*))^{\mathrm T}$.
''',[16],'Section 4.1 — regression model (13)','source_passage')
add('A5',r'''
Given an algorithm $\mathcal A:\mathcal X^N\to\Theta$, the global sensitivity of $\mathcal A$ is defined as
\[
\operatorname{GS}_{\mathcal A}=\sup\{|\mathcal A(\mathbb X)-\mathcal A(\mathbb X')|:\mathbb X,\mathbb X'\in\mathcal X^N,H(\mathbb X,\mathbb X')=1\},
\]
where $H(\cdot,\cdot)$ denotes the Hamming distance.
''',[8],'Definition 2 (Global Sensitivity)')
add('A6',r'''
For the global sensitivity for DGDP in the distributed setting, we let $H(\mathbb X,\mathbb X')=1$ denote that all elements are the same except for one local machine.
''',[8],'Section 2.2 — whole-machine adjacency convention')
add('A7',r'''
In assumption (b), we assume (19) holds with a probability tending to 1. Here, randomness comes from the selection of $\lambda_j$'s. Note that each $\lambda_j$ is chosen according to (15) which depends on the data. Assumption (c) implies that, for $l\in S^c$, the $l$-th row of the precision machine $\boldsymbol\Sigma^{-1}$ is dominated by the diagonal entry $\omega_{l,l}$.
''',[18],'Commentary after Theorem 4 — probability and diagonal condition','source_passage')
add('A8',r'''
In this paper, we focus on the high-dimensional scenario where the dimension $p$ tends to infinity. Therefore, Theorem 2 implies consistency under this assumption.
''',[12],'Commentary after Theorem 2 — asymptotic scenario','source_passage')
issues=[
'The registered source is arXiv:2209.04419v2 dated 4 June 2024, with 41 pages. The main paper and references end on page 28; Section 7 Appendix begins on page 29. No appendix body or separate source version was reviewed.',
'All four main-text Theorems are retained, including Theorem 4(c) and its conclusion on page 18. Lemmas 1–4 quote external theorem numbers but are not Theorem environments. Appendix Propositions 1 and 2 are neither read nor inventoried.',
'Theorem 1 asserts a privacy property for arbitrary sign matrices; Theorem 2 controls agreement with the realized non-private majority vector. Theorems 3 and 4 assert population sign consistency in distinct models. These targets must not be merged.',
'Distributed group adjacency replaces the entire dataset of a fixed local machine. It is not record-level adjacency, arbitrary groups of a given size, or privacy from the trusted server. The trusted-curator setup is stated in Section 2 and discussed again on page 22.',
'The introductory equal-size description uses n=N/m, whereas the two model-specific theorems allow unequal n_j of comparable order. Their sample mean and loss denominators are n_j, not a substituted common n. The distributed partition gives N=sum_j n_j.',
'Section 1.2 prints a_n asymp b_n as simultaneous O(b_n) and Theta(b_n). This redundant/nonstandard presentation is retained, rather than replaced by another asymptotic convention. Generic constants are independent of m,n,p as printed.',
'Theorem 2 uses s-bar=|S-bar| for the majority-vector support, whereas Theorems 3 and 4 use s=|supp(theta*)|. Selection count s-tilde is a third quantity. Do not replace any one of them with another.',
'Majority Vote requires more than half of all votes for a nonzero sign; ties and any remaining case return zero. The vote counts (1) are auxiliary definitions shared by the majority, stability and utility passages.',
'The stability prose describes a minimal flip count, but (4) is a signed vote-margin formula. For example three positive votes give score 3, although flipping two entries suffices to change the majority. Preserve the formula and prose separately from this issue; do not repair the definition.',
'The opening of Section 2.3 repeats N_l^+ twice in its list, where (1) has positive, negative and null counts. The duplicate is retained in the original passage.',
'The peeling score f^S has a negative minimum for the zero-majority branch. The utility f_l(.,0) in (5) has the positive minimum. Theorem 2 calls its f_l quantity a stability function, but its formula refers to (5), not f^S in (4).',
'Algorithm 1 selects without replacement by fresh noisy maximization. Its displayed sampling line does not explicitly say independent or specify tie breaking. An eventual implementation needs these conventions; they are not inserted into the original algorithm.',
'Algorithm 2 calls Peeling with epsilon/2 and delta/2, then draws signs using epsilon-prime=epsilon/(4 sqrt(2 s-tilde log(2/delta))) and a further divisor 4 in every utility exponent. These distinct factors and logarithms are preserved.',
'Algorithm 2 returns a support and a set of nonzero signs, while later algorithms and theorems use a full indexed sign vector. Zero extension and coordinate association are implicit; plain unordered sets alone do not encode the vector. The graph preserves the algorithm and flags this output convention.',
'The prose on page 11 says the algorithm always outputs a non-empty set of signs, but its printed output may be empty if all selected draws are zero. This claim is not added to the theorem statements or algorithm definition.',
'The algorithm formulas require positive epsilon, a suitable delta strictly between zero and one, and an integer selection count at most p. Their theorem statements do not enumerate these domains; s-tilde=0 also makes the displayed scales degenerate. Domain conventions remain explicit interpretation issues.',
'Theorem 3 prints the distribution family as blackboard P(theta*,C), whereas (10) defines calligraphic P(theta*,C). The association is source-context based; the original theorem typography remains unchanged.',
'Theorem 3 contains an otherwise unused gamma_1>0 before its conclusion. The symbol is retained and its role remains unspecified within the main text.',
'Theorem 3 imposes only a lower bound on lambda_N in (11), and (12) does not compare the signal with the chosen lambda_N. Arbitrarily large thresholds are not ruled out by the printed hypotheses. An intended upper bound or calibrated choice is unresolved; no hidden condition is added.',
'The mean distribution family bounds third absolute centered moments coordinatewise. It does not impose coordinate independence, bounded observations, or an explicit positive lower bound on coordinate variances.',
'Theorem 4 uses equality in (18), unlike the inequality in Theorem 3(11). Its signal condition includes the random maximum over lambda_j and holds with probability tending to one, as confirmed by commentary on page 18.',
'The local Lasso argmin in (14) is written as an estimator without a selection rule for nonunique minimizers. The rule (15) takes a minimum over penalties; the nearby assertion that its feasible set is nonempty does not by itself establish attainment. Both are retained as definition-scope issues.',
'Algorithm 4 consumes s-tilde in (16), although it is omitted from its printed input line. Its lambda_N is externally supplied by (18); treating the forward reference as a dependency on the whole theorem would create a false recursive definition.',
'Theorem 4 calls Sigma=E[XX^T] the covariance matrix, without an explicit centering assumption in (13), (17) or the theorem. Equation (17) likewise does not explicitly require zero-mean noise. Do not replace Sigma by a centered covariance or silently impose means zero.',
'Theorem 4 introduces columns omega_1,...,omega_p but prints omega_-l in (20). Section 1.2 defines deletion for a generic vector; the intended deletion of the diagonal coordinate from column/row l is suggested by the commentary, but the missing parent-column index remains a notation issue.',
'Delta_0 in (20) has no explicit value, range or quantifier elsewhere in the admitted main text. Its intended positive gap is not silently inferred from the formula.',
'The minimum over a possibly empty population support and maximum over an empty complement are not assigned conventions in the source. Sign recovery of the zero vector or full-support cases need these conventions if included.',
'Global sensitivity and the exponential-mechanism/composition lemmas motivate the privacy proof. The numbered algorithms give their sampling probabilities explicitly. Proof tools are not automatically theorem-statement dependencies; Definition 2 is retained as auxiliary source context.',
'Theorem 2 explicitly takes probability only over the mechanism given signs. Model-specific limiting probabilities combine data and mechanism randomness under the usual algorithm construction; randomness and conditional versus joint law are not conflated.',
'Source hypotheses about rates concern sequences as N grows; p,m,n,n_j and the selection count may vary. The source does not fully quantify dependence of epsilon and delta or uniformity in changing privacy parameters. No stronger uniform theorem is claimed.',
]
resolution={
'shared':'Finite real vectors/matrices, ternary signs, positive sample counts and a fixed partition into machines are ambient. Source notation A1 resolves support, norms, vector deletion, eigenvalues, indicator, asymptotic order and [p]. A2 resolves vote counts for D2–D6. Measurable kernels/events, probability and expectation, limits, exponential/logarithm, square root, minima and maxima are ambient primitives; unspecified domains and empty-set conventions are flagged.',
'1':'Algorithm 2 is D9; the asserted privacy predicate is D1. Its source-defined inputs and body resolve through D2,D8,D6 and their dependencies. Epsilon and delta are algorithm parameters. The theorem does not acquire moment or regression assumptions from later applications, and proof-only composition/sensitivity lemmas are not dependency edges.',
'2':'D2 supplies Q_l^r; D3 the target majority vector and its scalar entries; D4 its support size s-bar; D6 the evaluated sign utility; D9 the random output. The margin (6), gamma>2 and selection-count inequality are local hypotheses. The probability bound is over algorithm randomness, and the p-to-infinity convention is A8.',
'3':'D12 supplies the third-centered-moment class despite the theorem typography mismatch. D11 defines the estimator and local means, with D10 quantization and recursive DPVote dependencies. A3 supplies s=|S| and the mean setup. All rate conditions, S, lambda_N and C1,C2,gamma0 are bound in the original statement. Gamma1 and the missing restriction on arbitrarily large lambda_N remain unresolved. No privacy conclusion from Theorem 1 is appended.',
'4':'D16 supplies the sampling class. Theorem part (c) locally defines Sigma and its inverse columns; A1 and A7 support interpretation of its deletion and diagonal notation. D14 supplies data-dependent lambda_j and D15 the output estimator, recursively using D13 and D9. S and the displayed rate/margin conditions remain local binders; positive definiteness and (20) are theorem hypotheses, not relabeled definitions. Delta0, centering, minimizer selection and the missing index in omega_-l remain explicit issues.'
}
def main():
    unresolved=[
        dict(reference='Appendix Propositions 1 and 2 and proofs',status='excluded_not_imported',reason='Main-text-only census; proof dependencies do not extend scope.'),
        dict(reference='Theorem 3 threshold scope and gamma_1',status='unresolved_in_main_text',reason=issues[17]+' '+issues[18]),
        dict(reference='Theorem 4 Delta_0 and omega_-l',status='unresolved_in_main_text',reason=issues[24]+' '+issues[25]),
        dict(reference='Algorithm output, minimizer selection and parameter domains',status='implicit_or_unresolved',reason='See source issues; source formulas are preserved without an invented repair.')]
    out=dict(paper_id=PID,unranked_auxiliary_passages=passages,source_issues=issues,statement_resolution=resolution,unresolved_source_references=unresolved)
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
