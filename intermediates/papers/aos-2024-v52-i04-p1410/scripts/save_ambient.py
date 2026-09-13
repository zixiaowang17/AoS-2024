"""Rebuild the paper's source-backed ambient conventions and auxiliary context."""
import json
from pathlib import Path
from save_inventory import PID
ROOT=Path(__file__).resolve().parents[1]
aux=[]
def passage(lid,pages,heading,text,note):
    aux.append(dict(local_id=lid,source_heading=heading,statement_original=text.strip(),evidence=[dict(page=p,location=heading) for p in pages],note=note))
passage('A1',[3],'Section 2.1 — observations and measurable statistics',r'''
We write $X$ for a random variable taking values in the observation space $\mathcal X$, endowed with a measurable structure, and $X^n:=(X_1,\ldots,X_n)$ for $n$ independent copies of $X$ under the distributions that are to be considered. Statistics of the data are denoted as $T=t(X^n)$, where $t$ is implicitly assumed to be a measurable function. We use letters $\mathbf P$ and $\mathbf Q$ to refer to distributions of $X$.
''','The paper overloads P and Q between one-observation and n-observation laws; theorem formulas use the law of the displayed data. The census retains the source notation.')
passage('A2',[3],'Section 2.1 — expectations and conditional laws',r'''
When writing conditional expectations, we write $\mathbf E^{\mathbf P}[f(X)\mid Y]$, and $\mathbf P^{X\mid y}$ for the conditional distribution of $X$ given $Y=y$. We only deal with situations where such conditional distributions exist. If we are considering a set of distributions parameterized in terms of a parameter space $\Theta$, we write $\mathbf E_\theta^{\mathbf P}[f(X)]$ rather than $\mathbf E^{\mathbf P_\theta}[f(X)]$ for the sake of readability.
''','Explains superscript-family/subscript-parameter expectations in every theorem. Conditional distributions are background notation, not added theorem requirements.')
passage('A3',[7],'After Theorem 1 — arbitrary reduced statistic',r'''
The statistic $V_n$ may be any measurable function, taking values in any set $\mathcal V_n$ equipped with a corresponding $\sigma$-algebra, but in all examples in our paper we can take $\mathcal V_n=\mathbb R^m$ for some $m\le n$. By allowing $V_n\ne X^n$, the theorem also covers cases in which the infimum on the left in (9) is not achieved.
''','V_n in Theorem 1 need not be maximally invariant; the full-data infimum need not have a minimizing pair even though the reduced-data minimum does.')
passage('A4',[9],'Assumption 1 — preamble',r'''
Let $G$ be a topological group acting on a topological space $\mathcal X^n$, both equipped with their Borel $\sigma$-algebra. The group $G$, the observation space $\mathcal X^n$, and the probabilistic models under consideration satisfy the following three properties:
''','Shared ambient spaces for the numbered clauses D13, D14 and D16. Theorem 4 invokes Part 3, so the Polish/local compactness and free/proper conditions in Parts 1-2 are not added to that theorem.')
passage('A5',[4],'Section 2.2 — topological group description',r'''
In (2), a topological group is a group equipped with a topology, such that the group operation, seen as a function $G\times G\to G$, is continuous.
''','Original description omits an explicit continuity requirement for inversion. The census preserves it and does not replace it with a stronger quoted definition.')
passage('A6',[4,5],'Section 2.2 — right Haar measure',r'''
Furthermore, since $G$ is assumed to be locally compact, there exists a measure $\rho$ on $G$ that is right invariant (see Bourbaki, 2004, VII,§1,no 2). This means that for any $g\in G$ and any $B\subseteq G$ that is measurable, it holds that $\rho\{Bg\}=\rho\{B\}$. The measure $\rho$ is called the Haar measure, it is unique up to a multiplicative factor, and it is finite if and only if $G$ is compact.
''','Right-Haar convention for the alternate amenability formulation. It is not itself a direct requirement of the inventoried theorem formulas, whose mixtures use probability priors.')
passage('A7',[18],'Section 6.2 — alternate amenability characterization',r'''
For the proof of the main result, we use an equivalent definition of amenability to the one that was already anticipated in Section 2.2. We take the one that suits our purposes best (see Bondar and Milnes, 1981, p. 109, Condition $A_1$). That is, a group $G$ is amenable if there exists an increasing sequence of symmetric compact subsets $C_1\subseteq C_2,\cdots\subset G$ such that, for any compact set $K\subseteq G$,
\[
\frac{\rho\{C_i\}}{\rho\{C_iK\}}\to1,\quad\text{as }i\to\infty.
\]
In this formulation, amenability is the existence of almost invariant symmetric compact subsets of the group $G$. We use these sets to build a sequence of almost invariant probability measures when $G$ is noncompact.
''','The source calls this equivalent to D9. Preserve both exact formulations without silently replacing the pointwise probability definition or adding implicit positivity/nonempty-set qualifiers to this quotation.')
passage('A8',[4],'Section 2.1 — group subset operations',r'''
Given two subsets $H,K$ of a group $G$ we write $HK=\{hk:h\in H,k\in K\}$ for the set of all products between elements of $H$ and elements of $K$. Similarly, for $g\in G$ and $K\subseteq G$, we write $gK=\{gk:k\in K\}$ for the translation of $K$ by $g$, and $K^{-1}=\{k^{-1}:k\in K\}$ for the set of inverses of $K$. We say that $K$ is symmetric if $K=K^{-1}$.
''','Group products, translations and symmetry for amenability and Haar context. These are not Euclidean Minkowski operations.')
passage('A9',[1,2],'Introduction — reduced density convention',r'''
Indeed, because it is an invariant function, the density of $M_n$ depends only on $\delta$. Let us denote $p^{M_n}$ and $q^{M_n}$ the densities of $M_n$ under $\mathcal H_0$ and $\mathcal H_1$, respectively.
''','Resolves omission of g on the reduced laws and densities in Theorem 2. The two hypotheses fix two invariant parameter values; their remaining parameter is the group index.')
NOTES=[
'The registered source is the 31-page arXiv:2208.07610v2 PDF, dated 17 October 2023. The precise versioned URL is saved along with the register filename and export-URL aliases.',
'Exactly Theorems 1, 2 and 4 occur in main text. Number 3 belongs to a Corollary. References end on page 23 and Appendix A begins separately on page 24; no appendix body was read.',
'Theorem 1 requires equality between a full-data KL infimum and an attained reduced-data minimum. It does not assert existence of a full-data minimizing pair, and V_n is any measurable statistic rather than a required invariant.',
'Theorem 1 has two potentially different probability priors on G. The optimum is a ratio of mixtures of reduced densities, not a mixture of likelihood ratios or an assumed Haar-prior Bayes factor.',
'Theorem 2 requires all three parts of Assumption 1 and amenability. Both log likelihood ratios have 1+epsilon moments, one under Q_1 and one under Q^{M_n}; the identity subscript is not a sample index.',
'Theorem 4 invokes only Part 3 of Assumption 1. For every g it requires some h with finite KL(Q_g,P_h); it does not require a single h to work for all g or finiteness for every pair.',
'Theorem 4 proves a constant oracle value and then equivalence of the sets of optimizers for the absolute and relative criteria. These definitions remain separate, and existence of an optimizer is not added to the theorem.',
'The source defines e-statistics as nonnegative real statistics, allowing zero. Logarithmic objectives therefore need the usual extended-value convention at zero; this and expectation well-definedness are not explicitly spelled out in the displayed definition.',
'The KL definition uses the Radon-Nikodym derivative dQ/dP but does not explicitly define the non-absolutely-continuous case. Finite KL requirements and common-support statements are preserved without fabricating a complete source convention.',
'Theorem 1 uses reduced densities without a separately printed dominating-measure specification in that theorem. Density existence and measurability are part of interpreting its formula; no extra Assumption 1 clauses are inserted into it.',
'Assumption 1 Part 1 says Polish followed by a dash and separable, completely metrizable and locally compact. All listed properties are retained; the wording is not taken to make local compactness part of the standard definition of Polish.',
'The main-text description of a topological group specifies continuity of the group operation but does not explicitly mention continuity of inversion. Preserve the description; a formalization must resolve this usual ambient convention.',
'Part 3 requires a common relatively left-invariant dominating measure and a single common support for all densities. It is not silently replaced by the left-invariant measure used in the subsequent proof.',
'The amenability definition on page 5 is a sequence with convergence separately for each measurable B and each g. No supremum over sets or uniform convergence on compact sets is written there; the source quantifiers are preserved.',
'Page 18 gives a second amenability formulation using increasing symmetric compact sets and a right-Haar ratio. The source calls it equivalent; this is retained as auxiliary context, without certifying equivalence or filling in unspecified positivity and empty-set conventions.',
'The componentwise action notation on page 4 switches from input x^n to capital gX^n. This typographical mismatch remains in the original passage.',
'Section 2.1 introduces independent copies and overloads P,Q between one-observation and sample laws. Pi^g is a mixture binding the group index; it is not group exponentiation. Q^{M_n} is instead an image law.',
'The reduced laws do not carry a group subscript because invariance removes that nuisance index within each of the two fixed invariant-parameter hypotheses. This does not identify null and alternative reduced laws with each other.',
'The reparameterization discussion uses free action on the parameter space to identify each orbit with G. The extracted testing problem is the resulting group-indexed model; no reparameterization proof or extra free-action clause is appended to Theorem 4.',
'Anytime-validity, martingales, optional stopping, composite-invariant-parameter extensions and example-specific formulas occur as propositions, corollaries or discussion. They are not additional Theorems and do not become dependencies of these three statements solely because they occur in the same paper.',
'The census checks original statements, source meanings and dependency paths. It does not certify the proofs or the paper\'s external group-theoretic equivalence claims, and it does not audit mathlib availability.'
]
RESOLUTION={
'shared':'G is the group of transformations, with group actions and measurable translates from D4. Data X^n and measurable statistics follow A1; expectation notation follows A2. The fixed null and alternative group-indexed models are D8 with invariance D6. Group algebra, Borel sigma-algebras, ordinary topology, densities and integrals are ambient. Existence of indicated densities and extended logarithmic expectations must be respected without rewriting the original statements.',
'1':'V_n and v_n are local statistic binders, with arbitrary measurable codomain as stated in A3. Image laws and superscript density notation use D1; Pi_0,Pi_1 and their starred minimizers are probability priors on G with mixtures D2. KL is D3. The null/alternative are D8, competitors are D10 and GROW is D11. Neither maximal invariance, amenability nor the full topological Assumption 1 is inserted into this conditional variational theorem.',
'2':'M_n is a maximally invariant statistic D7 with image laws D1; the group-indexed models are D8. Theorem 2 explicitly requires amenability D9 and Assumption 1 Parts 1-3 as D13,D14,D16, with preamble A4. The action requirements resolve to D4,D5,D15. Both moment conditions and epsilon are bound directly in the statement; pg,qg are model densities and p^{M_n},q^{M_n} reduced densities as in A9. Subscript 1 is the group identity. The conclusion uses arbitrary probability mixtures D2 and KL D3.',
'4':'Only the dominated invariant-model clause D16 is explicitly invoked, in the testing problem D8. The quantifiers bind h separately for each g and use KL D3. The supremum ranges over D10 and yields a constant function of g; the equivalence refers to the distinct D11 and D12 optimization criteria. No maximal invariant, Haar integral, amenability, Polish, free or proper action condition is added via a proof dependency.'
}
def main():
    data=dict(paper_id=PID,scope='Main text only; appendices excluded.',unranked_auxiliary_passages=aux,source_issues=NOTES,statement_resolution=RESOLUTION,unresolved_source_references=[
      dict(reference='Appendices A-D',status='excluded_not_opened',reason='Sufficiency, examples, stopping-time details and auxiliary proofs remain outside the requested scope.'),
      dict(reference='GHK Theorem 1 and other cited literature',status='external_not_imported',reason='The original in-paper Theorem 1 is fully transcribed; cited external proofs or alternative statements are not substituted.'),
      dict(reference='Bondar and Milnes (1981), Condition A1',status='external_not_imported',reason='The main-text alternate amenability formulation is saved verbatim, but its cited equivalence proof is not audited.')])
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
