"""Save original ambient passages and unresolved source meanings separately."""
import json
from pathlib import Path
from save_inventory import PID
ROOT=Path(__file__).resolve().parents[1]
aux=[]

def add(lid,text,pages,location):
    aux.append(dict(local_id=lid,statement_original=text.strip(),evidence=[dict(page=p,location=location) for p in pages]))

add('A1',r'''
In this work, $c,c_1,c'$ denote numerical positive constants that may vary from line to line. We write that two quantities $u$ and $v$ satisfy $u\lesssim v$ if there exists a numerical constant $c$ such that $u\le cv$. We recall that norm of the form $\|\mathbf A\|_s$ for $(s\in[1,\infty])$ correspond to the $s$-Schatten norms. In contrast, for $s\in[1,\infty]$, we write $|\mathbf A|_s$ and $|u|_s$ for entry-wise $l_s$ norms of the matrix $\mathbf A$ and the vector $u$.
''',[5],'Section 1.4 — constants, comparison notation and entrywise norms')
add('A2',r'''
Recall that, when $k$ is an integer, we have the following identity
\[
\|\mathbf A\|_{2k}^{2k}=\operatorname{tr}[(\mathbf A^T\mathbf A)^k]=\sum_{i_1,\ldots,i_k=1}^p\sum_{j_1,\ldots,j_k=1}^q\prod_{t=1}^k\mathbf A_{i_tj_t}\mathbf A_{i_tj_{t+1}},
\]
with the convention $j_{k+1}=j_1$.
''',[7],'Section 3 — cyclic trace identity and j-index convention')
add('A3',r'''
It is well known (see e.g. [7]) that, for $Z\sim\mathcal N(x,1)$, $\mathbb E[H_r(Z)]=x^r$.
''',[7],'Section 3 — Gaussian Hermite expectation identity')
add('A4',r'''
As in the previous section, we shall assume henceforth that the singular values of $\mathbf A$ are bounded by $M(pq)^{1/4}$ for some known $M>1$.
''',[13],'Section 5 — known spectral bound')
add('A5',r'''
It was previously observed (e.g. in [21]) that the $l_1$ distance between two ordered vectors is proportional to the Wasserstein distance between the two corresponding measure.
\[
\sum_{i=1}^q|\sigma_i-\sigma_i'|=qW(\mu_\sigma;\mu_{\sigma'}).\tag{23}
\]
''',[13],'Section 5 — ordered-vector Wasserstein identity (23)')
add('A6',r'''
As a consequence, this distribution $\mu_0$ is a feasible point of the linear program and its objective value is less or equal to $|\overline m-\widehat m|_1+2\zeta\sum_{k=1}^K k$.
''',[42],'Proof of Theorem 5.2 — notation used for the linear-program target')
add('A7',r'''
any symmetric polynomial of degree at most $2K$ can be represented as $P(x^2)$ where $P\in\mathcal P_K$
''',[35],'Proof of Lemma 4.5 — original phrase specifying even symmetry')
add('A8',r'''
Since only the two first moments of $E$ match those of the standard normal distribution, the estimator $U_k$ is therefore biased for all $k>1$.
''',[15],'Section 6 — original bias discussion, not a new hypothesis')

resolution={
'shared':'Matrices are real p-by-q and p>=q. D1 is the common observation equation. D2 specifies Gaussian noise only for Theorems 3.3,4.9,5.2; D19 replaces it for Theorem 6.3. A1 distinguishes Schatten from entrywise norms and defines numerical constants and lesssim. Variance, expectation under the chosen observation law, real-valued measurable estimators, finite sums/products, trace, Dirac mass, CDF, logarithms, floors, ceilings and the positive-part operation are ambient. The census does not silently add low rank, Gaussianity in Section 6, a corrected optimization problem or a proof certification.',
'3.3':'U_k is D9, with the Hermite convention D7 and occurrence counts D8. A2 supplies the cyclic j_(k+1)=j_1 convention, while the occurrence sentence prints i_(k+1)=i_1. H_0=1 is the usual zero-degree extension consumed when an entry has zero occurrences, but the printed definition only states r>0; record the convention separately, not inside the quotation. D4/D3 give the two Schatten-power terms. The theorem has k>=2 and all five variance-bound terms. The signal is arbitrary: the preceding diagonalization is a Gaussian invariance argument, not a diagonal-matrix hypothesis.',
'4.9':'D2 fixes the Gaussian experiment; D5 bounds the local parameter set. The theorem binds I_0, k-star and a continuous real-valued f, broadening the original nonnegative-valued convention D6 while repeating its defining sum. D11 is instantiated with D12, with uniform norm D10. Symmetric means even in this univariate setting, as the main-text phrase A7 confirms. Positive part applies after subtracting the q^(1/2) uniform-norm term. The printed extra bracket after I_0 is retained. The infimum is understood over estimators from Y, although the source does not separately spell out measurability or integrability here.',
'5.2':'D18 references the printed two-step estimator, which depends on D17/D16 and the introduced moment vector D15; D15 uses the same U_k and Gaussian law. The proof passage A6 confirms the use of hat m in the objective but does not repair the undefined hat U in (24). D13 creates the empirical measures and D14 supplies W. A4 makes M known. A5 requires both vectors to have a common ordering for coordinate matching; the printed quantiles ascend while the original true singular values descend. K=floor(c log q), the repeated M in the constant clause, undefined b and hat U, strict positivity, grid scaling, existence/selection of a minimizer and the missing expectation in (25) are all unresolved source issues, not quietly rewritten assumptions.',
'6.3':'D19 is the iid centered unit-variance sub-Gaussian law, with scalar norm D20; the external psi_2 normalization is not supplied by the source itself. The polynomial U_k is still D9/D7/D8, which is a statistic independent of the law used to analyze it. No edge to D2 is introduced. D4 gives the target and D5 the two operator-norm powers. This is a mean squared error bound, not a variance or unbiasedness statement. The case k=1 is included as printed; the zero power at A=0 needs the ordinary exponent-zero convention. A8 records the author bias claim separately; sub-Gaussian laws can match additional Gaussian moments, so it is not treated as a universal new hypothesis.'}
issues=[
'The registered PDF is arXiv:2111.13551v1, dated 26 November 2021, with 67 pages. The precise version URL and hash are pinned; the manifest filename and unversioned export URL are aliases of those verified bytes.',
'There are four main-text results explicitly labeled Theorem. Numbered proof Sections 8 and 9 remain main text, through Lemma 9.15 on page 65; Appendix A begins at y=400.551 and its body is excluded. The earlier prose saying proofs are postponed to the appendix does not change this printed section boundary.',
'The introduction assumes independent standard Gaussian entries. Section 6 replaces that law with iid centered unit-variance sub-Gaussian entries. The shared estimator formula is not a reason to propagate Gaussian assumptions to Theorem 6.3.',
'The bold noise matrix E and the plain scalar noise variable E are distinct. Matrix Schatten norms use double bars, while entrywise vector/matrix l_s norms use single bars.',
'The source defines singular values in descending order and includes all q values, including zeros. No low-rank restriction is imposed in any retained theorem.',
'The Section 3 prose prints the 2k-Schatten norm as a sum raised to 2k rather than 1/(2k). The actual original definition (2) and theorem formulas are retained; this preceding prose error is not used to redefine the norm.',
'The cyclic trace product explicitly uses j_(k+1)=j_1. The following occurrence-count paragraph instead recalls i_(k+1)=i_1 despite containing j_(t+1). Both source passages are preserved; the original count clause is not silently corrected.',
'The Hermite definition is stated for positive degree r, but U_k uses degree zero whenever an entry does not occur. The usual H_0=1 extension is an ambient resolution, not an invented original definition.',
'The distributional diagonalization before Theorem 3.3 is justified by Gaussian invariance. It is not a restriction that A itself must be diagonal and cannot be reused for the sub-Gaussian theorem.',
'Theorem 3.3 bounds variance for k>=2, while Theorem 6.3 bounds mean squared error for k>=1. The latter statistic can have nonzero bias; these two losses are not interchangeable.',
'The spectral-functional definition initially assumes nonnegative-valued f. Theorem 4.9 explicitly allows continuous real-valued f and recalls the same sum; preserve the changed range.',
'Theorem 4.9 uses double bars for the supremum norm although the local definition uses single bars. Its approximation notation also switches the comma separator in (16) to a semicolon; these are recorded notation aliases.',
'Theorem 4.9 has an extra printed closing bracket immediately after E[f;I_0]. The transcription preserves it; the intended positive part is outside the subtractive expression.',
'Theorem 5.2 repeats suitable numerical constant M>1 after using c in K=floor(c log q). The proof instead selects a small constant c1. The original theorem is not repaired.',
'Theorem 5.2 displays a Wasserstein bound without expectation, followed by an expected coordinate-error bound. The proof explicitly bounds expected Wasserstein distance but later drops expectation again. No expectation is inserted into the original theorem.',
'Theorem 5.2 gives no lower restriction on q to make log(q) and positive K meaningful; q=1 is not silently removed or replaced by a truncated logarithm.',
'The empirical-measure paragraph writes where delta_x denote the associated probability measure after defining mu_sigma. Both symbols are preserved; the normalized empirical sum and each Dirac mass remain distinguishable.',
'The grid upper endpoint contains undefined b, while its cardinality uses M. The printed endpoint, spacing, floor/ceiling convention and cardinality are retained without setting b=M.',
'The moment vector hat m is normalized to the spectral scale, but the grid is written on the physical spectral interval and the quantile step rescales by that scale again. The main proof works with normalized moments. This scaling conflict is recorded, not repaired.',
'The program (24) fits undefined hat U although the preceding paragraph defines hat m. Its main-text proof uses hat m. The graph records this contextual link as an unresolved alias, not an equality certified from the printed algorithm.',
'The program requires strictly positive p rather than nonnegative p. The open simplex may not attain a minimum, and the proof uses a rounded measure that can have zero weights. No existence, tie-breaking or measurability rule for the selected optimizer is supplied.',
'The quantile estimator is nondecreasing in i, while the original singular values are nonincreasing. The expected coordinatewise comparison in Theorem 5.2 requires compatible ordering; reversing one sequence is not inserted into its original statement.',
'The sub-Gaussian norm is named but its definition and normalization are delegated to [39]. Keep it as an unresolved external convention instead of inventing an Orlicz formula.',
'The Section 6 prose says U_k is biased for all k>1 because only the first two moments match. Particular non-Gaussian laws can match further Gaussian moments. The theorem only needs its original squared-error bound; no universal bias claim is inferred from this prose.',
'For k=1 the operator-norm term in Theorem 6.3 has exponent zero, including at A=0. The ordinary zero-exponent convention is needed; it is not a new nonzero-signal assumption.',
'The proof-only prior constructions, Gaussian mixture distances, moment-comparison inequalities and combinatorial graph partitions are not definitions consumed by the retained theorem statements. Proof correctness and effective executable behavior of the inconsistent estimator are not certified by this source census.'
]
excluded=[dict(reference='Appendix A: Technical inequalities',location='Below y=400.551 on PDF page 65',status='excluded_not_opened',reason='Appendix bodies are outside the requested main-text-only scope.'),dict(reference='[39] sub-Gaussian norm definition',location='Section 6, PDF page 14',status='external_not_expanded',reason='The source names the norm but does not provide its normalization; no external definition is fabricated.'),dict(reference='[21] Algorithm 1 and related moment matching results',location='Section 5, PDF page 13',status='external_not_expanded',reason='The paper gives its own estimator; external content cannot silently repair its printed aliases, ordering or scaling.'),dict(reference='Lemmas A.1-A.3 and other external inequalities',location='Main-text proof references',status='excluded_not_opened',reason='Proof ingredients do not expand the theorem inventory or replace source-local definitions.')]

def main():
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(dict(paper_id=PID,scope='main_text_only',auxiliary_source_passages=aux,statement_resolution=resolution,source_issues=issues,excluded_references=excluded),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(aux)} auxiliary passages and {len(issues)} source notes.')

if __name__=='__main__':main()
