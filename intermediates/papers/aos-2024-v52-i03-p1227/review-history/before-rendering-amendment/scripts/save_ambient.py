"""Save main-text conventions and unresolved meanings without expanding appendices."""
import json
from pathlib import Path
from save_inventory import PID
ROOT=Path(__file__).resolve().parents[1]
aux=[]


def add(lid,text,pages,location):
    aux.append(dict(local_id=lid,statement_original=text.strip(),
        evidence=[dict(page=p,location=location) for p in pages]))


add('A1',r'''The relevant distribution $P$ will usually be clear from the context, in which case we will simplify notation and write $\theta_\gamma\equiv\theta_\gamma(P)$.''',[7],'Section 2.1 — suppressed distribution argument')
add('A2',r'''The subscript $\gamma\cdot\Gamma$ indicates that the confidence region is provided for target $\gamma$ while adjusting for the requirement of simultaneous coverage over $\Gamma$. The superscript $\alpha$ indicates the tolerated error probability. Sometimes the error probability will be irrelevant or clear from the context, in which case we will drop it and write $C_{\gamma\cdot\Gamma}\equiv C^\alpha_{\gamma\cdot\Gamma}$.''',[7],'Section 2.1 — confidence-region indices and error levels')
add('A3',r'''With simultaneously valid confidence regions in hand, as long as the selected targets $\widehat\Gamma$ are guaranteed to fall within the fixed admissible set $\Gamma$, meaning $\widehat\Gamma\subseteq\Gamma$ almost surely, an immediate implication is that
\[
P\{\theta_\gamma\in C_{\gamma\cdot\Gamma},\forall\gamma\in\widehat\Gamma\}\ge P\{\theta_\gamma\in C_{\gamma\cdot\Gamma},\forall\gamma\in\Gamma\}\ge1-\alpha,
\]
''',[8],'Section 2.1 — admissible selected targets')
add('A4',r'''We note that exact knowledge of $P_0$ is not necessary; being able to compute an upper bound on $q^\alpha(\mathcal I)$ suffices.

Note that $\theta_i=Ey_i\equiv\mu_i$ in this setting; that is, the possible estimands $\theta_i$ are coordinates of the location parameter.''',[11],'Section 3.1 — quantile upper bounds and location targets')
add('A5',r'''Let also $e_{j\cdot M}\in\mathbb R^{|M|}$ be the canonical vector with entry $1$ corresponding to feature $j\in M$''',[14],'Section 4 — model-indexed canonical vector')
add('A6',r'''Lemma 2 and Lemma 3 show that the safe screening subroutine (stated explicitly in Algorithm 2 in the Appendix) is valid.''',[16],'Section 4.1 — safe-screening subroutine reference')
add('A7',r'''For example, the classical symmetrization argument proves that $\operatorname{Gap}_n(\mathcal F)=2\mathcal R_n(\mathcal F)$ is a valid upper bound on $E\sup_{f\in\mathcal F}|R(f,P)-R_n(f,\mathcal D)|$, where $\mathcal R_n(\mathcal F)$ denotes the Rademacher complexity of $\{\ell(f,\cdot)\}_{f\in\mathcal F}$.''',[17],'Section 5 — one optional complexity bound')
add('A8',r'''We will focus on methods that use $X^\top y$ as a sufficient statistic, which includes most common selection methods such as the LASSO, forward stepwise, etc.''',[13],'Section 4 — selection based on the transformed response')

resolution={
 'shared':'The six Theorems retain their original statements. For the general theory D1 supplies the statistical model and indexed targets, D2 the selection, and A1-A3 the suppressed distribution/error-level notation and admissible target universe. Basic probability, expectations, sets, unions, infima/suprema, natural index notation [m] and [d], cardinalities, Euclidean and infinity norms, transpose, diagonal matrices and pseudoinverse are ambient. The source interval notation (center plus/minus width) is preserved without choosing endpoint conventions. Measurability of set-valued selections, uncountable simultaneous events and extrema is not developed. Different uses of P, X, y, theta, q, M and F are scoped to their own sections; no shared spelling implies the same model or definition.',
 '1':'D1-D7 resolve all external quantities: target estimands, selected targets, simultaneous regions at every fixed subset, Assumption 1, valid acceptance sets, fixed-P plausible targets and inversion B_nu(y). Gamma-hat-plus is defined completely inline, including both forms of the nested union; D8 archives that construction for the explicit later reuse in Theorem 2. Nu is fixed in (0,alpha), and the final confidence regions use alpha-nu. This is an unconditional probability covering every selected target, not coverage conditional on a particular selection. Lemma 1 and its joint-event regions are used in the proof only and are not extra hypotheses.',
 '2':'D4 is set-inclusion monotonicity; D9 is the centered interval form and D10 its correction-indexed map with nonincreasing calibration in alpha. D8 resolves the explicit reference to Theorem 1 equation (2), retaining its local acceptance/inversion dependencies. The theorem itself specifies the special acceptance set A_nu(P) from full-family intervals and binds hat-q as the minimum of the local alpha-nu and global alpha corrections. This acceptance choice is essential and is not replaced by a generic choice from Theorem 1. No Gaussian model is required.',
 '3':'D11 is the location experiment y=mu+Z with common symmetric zero-mean marginals and unrestricted joint dependence. D12 and D13 separately resolve the two selection rules (3) and (4), while D14 resolves the maximum absolute coordinate-error quantile. A4 identifies theta with mu. The winner and threshold branches use margins 4q^nu([m]) and 2q^nu([m]) respectively; both retain the minimum with the full-family alpha correction. The augmented sets are bound inside each bullet, not imported from another theorem as extra assumptions. Theorem 2 proves the specialized result but is not an independent model restriction.',
 '4':'D15 supplies n iid vectors in [0,1]^m with arbitrary coordinate dependence. D16 and D17 define winner and threshold selection from coordinatewise averages. D18 supplies any valid scalar mean-deviation bound; D19 supplies any valid marginal confidence regions, with the theorem adding nesting in the error level. The margins use w_n at level nu/m with factors 4 and 2. The final confidence level is (alpha-nu) divided by the realized plausible-set cardinality. It is not a minimum with a global correction, and neither Gaussian errors, Hoeffding widths nor betting-based intervals are forced. Empty threshold-selection/plausible-set conventions remain unspecified.',
 '5':'D20 is the fixed-design location setup and D21 the contrast quantile under its error law. D22 defines the LASSO selection map. D30 preserves all of Algorithm 1, including initialization, visited/todo queues, both screening calls and projection from visited model-sign pairs to models. D23 resolves the neighborhood and radius, D24 the original strict model-sign polyhedron, D25 its neighbors, D26 the exact-screening description and D27-D29 the local affine solution and safe criteria. A5 provides the canonical-vector convention; A6 records the unresolved safe subroutine reference. Theorem 5 asserts the exact returned model set, not the projection-parameter coverage of Corollary 1. Algorithms 2 and 3 and detailed handling of degenerate faces are in excluded appendix material. The source statement is retained despite unresolved uniqueness, invertibility and boundary conventions.',
 '6':'D31 defines the iid sample from P^n, hypothesis class, loss, empirical risks and selected empirical minimizer; D32 defines population risk. D33 is any bound on the expected uniform generalization gap, with A7 an optional Rademacher example. The theorem binds the random plausible hypothesis class inline using the full-class bound, two factors 4 and sqrt((2/n)log(1/nu)). Its conclusion uses Gap_n evaluated on that random class and sqrt((2/n)log(1/(alpha-nu))). The absolute loss bound is one, allowing signed losses. No fixed confidence-interval family, location model or LASSO object is a statement prerequisite. Monotonicity/measurability of the chosen bound as a function of a possibly random class is not specified in the main text.'
}
issues=[
 'The registered source is arXiv:2212.09009v6, 36 pages, with arXiv date 2 May 2024 and title-page date 05.03.24. The register labels the same bytes as 2212.09009v6.pdf and stores an unversioned export URL. The original inventory retains its precise versioned URL and description; no source substitution or assertion of final-published equivalence is made.',
 'Main text ends with acknowledgments on page 25; references continue through page 27. Only the Appendix A heading on page 28 was inspected. Appendix bodies, including Algorithms 2 and 3, were not read.',
 'Six actual bold Theorem headings are included; Theorem 3 spans pages 11 and 12. Both bullets of Theorems 3 and 4 remain complete. Lemmas 1-3 and Corollary 1 are not additional theorem records.',
 'Theorems 1 and 2 allow general model families and possibly infinite target universes. The main text does not formalize measurability of unions, selected sets or uncountable simultaneous coverage events; these are not replaced by a finite-target restriction.',
 'Simultaneous coverage for each fixed target subset is different from coverage for a random subset. Assumption 1 supplies pathwise inclusion monotonicity; it is not a probability-monotonicity statement.',
 'Acceptance sets satisfy probability at least 1-nu, while the prose calls the test level 1-nu. Both the wording and mathematical inequality are preserved.',
 'Gamma_nu(P) is fixed once P is fixed, B_nu(y) is a random set of distributions, and Gamma-hat-plus is the random augmented target set. Their unions and different roles are not merged.',
 'Theorem 2 requires the particular acceptance set based on full-family centered intervals and the minimum with the global alpha correction. It is not stated for arbitrary acceptance regions.',
 'Assumption 2 prints a lowercase gamma-prime family index where the surrounding notation uses a subset Gamma-prime. This typographical inconsistency is retained. Nonnegative widths and zero-standard-error conventions are not explicitly given.',
 'Interval notation (center plus/minus width) does not separately specify open or closed endpoints. Exact/discrete quantile statements and boundary coverage should not be silently changed by adopting open endpoints.',
 'The location errors in Theorem 3 share symmetric zero-mean marginals but may be dependent. The fixed-design error law in Section 4 only states mean zero, so the stronger marginal restrictions are not imported into Theorem 5.',
 'Winner selection is written as a single argmax without a tie-breaking convention. Threshold selection includes equality, even though the surrounding prose says exceeds.',
 'The file-drawer branch can have no selected targets. Its plausible set may also be empty; the maximum over an empty index set in q and the division by an empty plausible-set cardinality in Theorem 4 have no explicit convention. Vacuous coverage does not by itself define those formulas.',
 'Theorem 4 requires iid vector observations across sample index, not independent coordinates. Its deviation bound is arbitrary subject to validity, and its final marginal confidence regions may have another construction.',
 'The q^alpha(index-set) of Section 3.1 is the maximum of coordinate errors, whereas q^alpha(contrast-set) in Section 4 is a supremum of linear contrasts. They remain separate source objects.',
 'The LASSO neighborhood constrains X^T(y-y-prime). It is a box in transformed-statistic coordinates but can be an unbounded polyhedron in outcome space. The closed inequality is retained.',
 'The LASSO is written as a selected argmin without a uniqueness/tie-breaking rule, and the main display does not explicitly require positive lambda. Its polyhedral formulas divide by lambda and use Gram inverses, requiring conditions not spelled out at that point.',
 'The model-sign selection event is represented by strict inequalities in the source. Boundaries of these open regions and models that occur only on local-neighborhood boundaries may require additional conventions for the exact enumeration claim. No almost-sure exception is inserted into Theorem 5.',
 'The affine formula beta_(M,s) has |M| coordinates but is equated to the full LASSO beta notation. It is evaluated even outside its own region for screening. Zero-extension and noninvertible Gram conventions are not supplied.',
 'The prose defines B(M,s) as all face-sharing model-sign neighbors, whereas ExactScreening prunes constraints after intersection with the local neighborhood. Lemmas 2 and 3 describe the safe criteria using the former notation. The intended restricted-neighbor interpretation is recorded without silently rewriting the definition.',
 'Algorithm 1 calls SafeScreening and ExactScreening without explicitly passing the radius or penalty. They are contextual quantities; the omitted appendix implementations are not reconstructed from guessed arguments. The return value drops signs and retains each visited support once.',
 'Theorem 5 concerns the returned plausible model set. The PoSI projection coefficients, standard errors, Corollary 1 coverage and the following inferential application do not become dependencies of that exact-set statement.',
 'Theorem 6 assumes absolute loss at most one, not loss in [0,1]. The loss example in the source reverses the argument order. The empirical minimizer existence and measurable selection are not established by the definition alone.',
 'Gap_n is any bound on the expected supremum, not necessarily that supremum or twice Rademacher complexity. Applying it to a random subclass needs a defined bound functional; its monotonicity, possible law-dependence and measurability are not explicitly stated. The source theorem is preserved without supplying an unprinted condition.',
 'Theorems 3-6 are applications proved using the general principle; proof provenance alone does not add the generic confidence-region APIs as prerequisites of every specialized statement. All dependency connections in the census follow their own original definitions.'
]
excluded=[
 dict(reference='Appendix A (Deferred proofs)',location='PDF page 28 heading',status='excluded_not_read',reason='The user scope excludes appendix bodies; only the boundary heading was inspected.'),
 dict(reference='Algorithms 2 and 3 in the Appendix',location='Main-text PDF pages 15-16',status='unresolved_excluded_appendix',reason='Save Algorithm 1 and the main-text descriptions and criteria; do not reconstruct omitted screening pseudocode.'),
 dict(reference='Appendix B examples and simulations',location='Main-text PDF pages 3-6 and 25',status='excluded_not_read',reason='Examples and additional simulations are not definitions required by the six stored Theorems.'),
 dict(reference='Lee et al. [24]',location='Main-text PDF page 15',status='external_not_expanded',reason='The exact main-text polyhedral formulas are preserved; external rank/uniqueness hypotheses are not silently imported.'),
 dict(reference='Berk et al. [6] and confidence-bound examples [4,5,7,34]',location='Main-text PDF pages 7,12-14',status='external_not_expanded',reason='Examples and the separate PoSI coverage result are not substituted for the source theorem dependencies.')
]


def main():
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(dict(paper_id=PID,
        scope='main_text_only',auxiliary_source_passages=aux,statement_resolution=resolution,
        source_issues=issues,excluded_references=excluded),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(aux)} auxiliary passages and {len(issues)} source notes.')


if __name__=='__main__':
    main()
