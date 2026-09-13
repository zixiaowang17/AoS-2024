"""Rebuild source-backed context, branch resolution and unresolved source ambiguities."""
import json
from pathlib import Path
from save_inventory import PID
ROOT=Path(__file__).resolve().parents[1]
aux=[]
def passage(lid,pages,heading,text,note):
    aux.append(dict(local_id=lid,source_heading=heading,statement_original=text.strip(),evidence=[dict(page=p,location=heading) for p in pages],note=note))
passage('A1',[4],'Prior terminology — OT and HT',r'''
We call priors $\Pi$ verifying (5)–(7)–(8) Oversmoothed heavy-Tailed priors or simply OT–priors while HT($\alpha$) for $\alpha$–Heavy Tailed priors stand for those satisfying (6)–(7)–(8).
''','These are the original names of the specified combinations. The census keeps scales and density conditions separately so that a moment or tail condition is not silently made part of either name.')
passage('A2',[4],'Sobolev-type ball — classical interpretation',r'''
For certain choices of $\varphi_k$, the sets $\mathcal S^\beta(L)$ correspond to balls of classical Hilbert-Sobolev spaces of functions in $L^2[0,1]$ possessing $\beta$ square integrable derivatives.
''','The coefficient-space theorem is primary. The source makes the identification with classical derivative spaces conditional on the choice of basis.')
passage('A3',[5],'Hölder-type ball — classical interpretation',r'''
For wavelet bases with classical Hölder regularity higher than $\beta$, the sets $\mathcal H^\beta(L)$ correspond to $L$-balls of the Hölder-Zygmund spaces $\mathcal C^\beta[0,1]$, see [40, Section 4.3]. For non-integer $\beta$ the latter spaces coincide with the classical Hölder spaces $C^\beta[0,1]$, while for $\beta$ an integer it holds $\mathcal C^{\beta'}\subset C^\beta\subset\mathcal C^\beta$ for all $\beta'>\beta$ where inclusions are all strict.
''','Preserve the distinction between classical Hölder and Hölder-Zygmund at integer smoothness; no extra basis regularity constraint is inserted into the coefficient-ball definition.')
passage('A4',[5],'Besov-type ball — classical interpretation',r'''
Again for appropriate wavelet bases, the sets $\mathcal B^\beta_{rr}(L)$ correspond to $L$-balls of Besov spaces $B^\beta_{rr}[0,1]$ defined via moduli of continuity, see [40, Section 4.3]. For $r=2$, Besov spaces coincide with the Hilbert-Sobolev spaces, while for $r<2$ Besov spaces are useful for modelling spatially inhomogeneous functions, that is functions which are smooth in some areas of the domain and irregular or even discontinuous in other areas, see [32] or [45, Section 9.6]. Here, we restrict to Besov spaces $B^\beta_{rq}$ with $r=q$ for simplicity, see Section 5 for a discussion.
''','The paper identifies spaces, not literal equality of the strict ball (11) and the closed ball (9). Do not merge the two local ball definitions.')
passage('A5',[8],'Remark 2 — smoothness and order of basis',r'''
Theorem 1 and results below hold for any smoothness parameter $\beta>0$, over regularity balls defined by coefficients as before. As usual with estimators defined over bases, if one wishes results over classical Hölder spaces or Besov spaces defined via moduli of continuity, one needs to assume a basis of large enough order/regularity (which means adaptation holds in that case over $\beta\le\beta_{\max}$, where $\beta_{\max}$ can be made as large as desired by choosing the order of the basis large enough).
''','This specifies the limit of interpreting coefficient regularity as classical function regularity, rather than weakening the original coefficient statements.')
passage('A6',[7],'Section 2.1 — single and double indices',r'''
Here for simplicity of notation we consider only single-index bases, but the results in the present Section and the next hold as well for double-indexed wavelet bases, such as ones considered in Section 2.3, with the corresponding appropriately chosen scalings as in (5)–(6).
''','The immediately named sections are 2.1 and 2.2. This observation supports the basis convention there; it does not explicitly resolve the Theorem 6 versus wavelet-prior discrepancy in Theorem 9.')
passage('A7',[11],'White noise sequence — membership in the multiscale subspace',r'''
It is not hard to see that $\mathbb W$ almost surely belongs to $\mathcal M_0$ (and $X^{(n)}$ as well for $f\in L^2$) under the condition that $w_l$ diverges faster than $\sqrt l$, see [22].
''','Theorem 5 gives two different power choices satisfying the stated large-level growth. Their value at level zero conflicts with the preceding w_l>=1 convention; the source is not silently amended.')
passage('A8',[14],'Classification — weighted norm and true law',r'''
Denote by $\|\cdot\|_{G,1}$ the $L^1(G)$ norm on $\mathcal X$ and by $P_0$ the true data generating distribution with regression $f_0$ and marginal $g$ (note that Bayesian modelling of $g$ is not needed for inference on $f$ as it factorises from the likelihood).
''','The source does not explicitly define the capital G measure beyond this norm notation; the marginal law of X is the natural reading. More substantially, Theorem 9 inserts the joint density p_f(x,y) into a norm described on X. This domain mismatch is unresolved. The prose also calls f0 the regression, whereas the binary probability is h0 and f0 is its logit.')
passage('A9',[14],'Classification — preceding choice of function prior',r'''
From a function $f$ sampled from (4)–(6) (or (4)–(5)), setting
\[
h_f(x)=\Lambda(f(x))\tag{26}
\]
induces a prior distribution $\Pi$ on binary regression functions.
''','Theorem 9 instead explicitly refers to the parameters of Theorem 6, whose construction is (3) and whose second scale is (21). Both original passages are retained. Dependency resolution follows the explicit theorem reference and leaves the mismatch as a source issue, rather than adding the two incompatible prior choices simultaneously.')
passage('A10',[4],'Scale choices — general exponents',r'''
The choice of the square in (5) is mostly to fix ideas and results below also hold for $\sigma_k=e^{-a(\log k)^{1+\delta}}$ with any given constants $a,\delta>0$. The fact that $(\sigma_k)$ in (5) decreases faster than any polynomial in $k^{-1}$, but not exponentially fast (as for instance $e^{-k}$), is key for the results ahead. Similarly, for double-index bases we can use $s_l=2^{-l^{1+\delta}}$ for any fixed $\delta>0$ in (5).
''','General-scale discussion is retained without changing statements that explicitly select (5). Theorem 6 separately prints (21) and its delta-dependent rate; it is directly used there and through the explicit reference in Theorem 9.')
NOTES=[
'The inspected source is the registered 59-page arXiv:2308.04916v3 PDF, 29 May 2024. Main text ends after Funding on page 26, before the Supplementary Material heading; the supplement introduction and appendix bodies are excluded.',
'Exactly ten actual main-text Theorem environments occur, numbered 1-10. Theorem 6 and Theorem 7 each retain their two complete bullets in a single claim. The later application and remarks are not additional Theorems.',
'Generic constructions (3) and (4) share one original source passage but retain distinct single-index and wavelet branches. Basis coefficients are ambient objects usable without a prior, so smoothness balls and observation models do not depend on the prior construction.',
'Scale alternatives (5), (6) and (21) retain their original natural-language keyword and source labels. Identical keywords do not establish equivalent scales. Branch resolution specifies which scale, coefficient indexing and rate each theorem selects.',
'Conditions (7) and (8) constrain the innovation density. The logarithmic upper bound on 1/h is a lower bound on density decay, not an upper-tail condition. The constants c1>0 and kappa>=0 remain unchanged.',
'Moment condition (14) and tail condition (19) are different. An x^-2 survival bound need not give a finite second moment. Theorems 1, 2 and 4 require q=2; Theorem 3 allows q>=1; Theorem 5 assumes neither condition; Theorems 6-10 use (19).',
'Theorem 1 explicitly includes priors truncated at k=n, setting later coefficients to zero. That extra assertion is absent from Theorem 2 and is not propagated by analogy.',
'Theorem 3 requires alpha>=beta+1/q in the polynomial-scale branch. Theorem 5 allows any alpha>0 and has no corresponding lower bound by beta. These parameter ranges are not homogenized.',
'Theorem 4 prints sigma_k in its final (6) branch even though its prior is defined by the wavelet construction (4). Preserve the original symbol and record the apparent indexing inconsistency instead of silently changing it to s_l.',
'Sobolev (9) and Hölder (10) balls use non-strict inequalities, while Besov (11) uses a strict inequality. Coefficient definitions are primary; identifying them with classical spaces requires the source basis conditions. Equal spaces at r=2 do not make the printed strict and non-strict balls identical.',
'The weighted space (17) assumes w_l>=1 for l>=0, but Theorem 5 prints weights l^(1+kappa+epsilon) and l^((1+kappa+epsilon)/2), both zero at l=0. This finite-level convention is unresolved; neither the index origin nor the weights are silently repaired.',
'Theorem 5 compares the ordinary posterior after the data-dependent affine map tau with the law of the standard Gaussian coefficient sequence. It uses the separable vanishing-level space M0, not the whole nonseparable bounded sequence space M.',
'The bounded-Lipschitz metric is named but its exact test-function normalization is not supplied. The source claim about metrizing weak convergence is preserved; the theorem applies it on the separable space M0.',
'Theorem 6 requires alpha>1/2 in its polynomial branch and uses the general (21) scale in the other branch. Its two rate formulas differ from the two supremum-norm rates of Theorem 7. Unlike Theorem 7, its printed statement does not contain an explicit for-large-enough-n clause.',
'Theorem 8 refers to Theorem 7 for prior parameters and rates, not merely as a proof citation. Both branches are unpacked, including beta<=alpha in the polynomial branch. The original density-map paragraph first illustrates (4),(5), but its map itself is used with both branches by the theorem.',
'Theorem 9 refers to Theorem 6 for parameters and rates, whereas the preceding classification prior sentence mentions (4),(6) or (4),(5). Preserve both source passages; the theorem reference controls recorded branch parameters, with the basis discrepancy explicitly unresolved.',
'The classification covariate domain is [0,1]^d for d>=1, while the preceding series bases and smoothness balls are defined on [0,1]. The main-text classification paragraph does not supply a multivariate basis or dimension-dependent rate convention; no such construction is invented.',
'Theorem 9 prints the joint density difference p_f-p_f0 in the G,1 norm defined on X alone. The capital G is not separately defined there. Preserve this unresolved source-domain issue instead of substituting the regression difference h_f-h_f0.',
'The posterior power is defined for 0<rho<=1. Theorems 8-10 state rho<1 within this range, so their effective range is 0<rho<1; nonpositive powers are not included. Theorem 8 explicitly states M(rho)>0 while Theorem 9 does not print that inequality.',
'The normalization map for densities and logistic map for binary regression take an input function or prior. Their introductory prior examples do not impose fixed scale dependencies on every application; the theorem selects its branch explicitly.',
'Theorem 10 has only the wavelet scale (5), the tail bound (19), and the Besov regularity restriction. Do not add Theorem 4\'s polynomial branch or moment assumption merely because the discussion compares the results.',
'Usual L1, L2 and supremum norms, expectations, iid Gaussian distributions, coefficient inner products, measure pushforwards and asymptotic constants are ambient. The exact G,1 norm use remains unresolved as described above. Logarithmic rate multipliers are bound within the statements.',
'Proof-only posterior coordinate estimates, testing and sieve constructions, the displayed application to primitive functions, and simulation-specific forward operators are not required to state these ten theorems. External references and appendix proofs are not imported.'
]
RESOLUTION={
'shared':'f is a function in L2[0,1], identified with coefficients in the selected basis. D1 archives the basis, indices and two prior constructions. Those basis conventions are ambient for D8-D10 and D12-D15 and do not require a prior. H is the innovation law with density h; its generic probability-law convention is ambient and its conditions are D5-D7. Standard integrals, norms, conditional laws and expected values use their displayed domain and sampling experiment. Scope constants and log-rate multipliers are locally bound.',
'1':'D13 specifies the experiment, D1 the single-index prior, D2/D3 its alternative scales, D5 density assumptions, D6 with q=2 its moment, and D8 the true coefficient ball. D11 is the ordinary posterior. beta,L,d and the truncation f_k=0 for k>n are locally bound. No extra standalone interface is invented for the convergence limit or truncation.',
'2':'D14 is the inverse model, with singular value sequence kappa_k and degree nu. D1,D2/D3,D5,D6 specify the two prior branches and second moment. D8 is Sobolev regularity and D11 the ordinary posterior. The rate denominator is 2beta+2nu+1. No truncation extension is added.',
'3':'D15 fixes the wavelet experiment; D1 uses (4). D2/D3 are alternatives with the branch-specific moment q and restriction alpha>=beta+1/q; D5,D6 are the density and moment conditions. D9 gives coefficient Hölder regularity and D11 the usual posterior. Supremum norm and positive constants are ambient/local.',
'4':'D12 is the white noise model and D15 its wavelet observation convention, explicitly selected in the Section 2.4 preamble; D1 selects (4), D2/D3 the two printed scale clauses, D5,D6 the density and second moment conditions, D10 the Besov ball and D11 the usual posterior. r in [1,2] and beta>1/r-1/2 are inline constraints. The sigma_k notation in the second branch remains as printed.',
'5':'D15 fixes wavelet observations, D1,D2/D3,D5 the prior; D9 is the truth class. D17 resolves M0 via D16. D18 is the Gaussian noise law; D19 resolves the transformed posterior using D11,D15,D17. D20 is beta_M0. Weight powers, epsilon,alpha,beta,L and n are local; the level-zero weight inconsistency is recorded. D6 and D7 are absent.',
'6':'D1 uses (3). The first branch selects D3 with alpha>1/2,beta<=alpha; the second selects D4 with a,delta>0. Both use D5,D7,D8. Rates (20),(22),d1,d2 and the open L2 ball are locally defined. This is prior mass, not posterior convergence, so no observation model or posterior interface is attached.',
'7':'D1 uses (4), with D3 and rate (23) in the first branch or D2 and rate (24) in the second. D5,D7,D9 apply. The polynomial branch has alpha>1/2,beta<=alpha. Both open sup-norm prior-mass bounds hold for large enough n. There is no sampling model or posterior in this statement.',
'8':'The iid density experiment, positivity of g0, f0=log g0, L1 loss and M(rho) are local or ambient. D22 is the density map; D21 is the tempered posterior. The explicit reference to Theorem 7 supplies D1,D2/D3,D5,D7 and paired rates (23)/(24), while D9 is also explicitly required of f0. Referenced parameter branches are preserved without copying the prior-mass conclusion into this theorem.',
'9':'D23 resolves the data and true probability h0; D24 gives the inverse logit f0. D25,D26 give the prior map and joint density; A8 records the printed norm convention and its domain ambiguity. D8 is the stated Sobolev ball. Theorem 6 explicitly supplies D1,D3/D4,D5,D7 and paired rates (20)/(22), with basis disagreement to A9 recorded. D21 is the tempered posterior. The covariate dimension and one-dimensional coefficient conventions are not silently reconciled.',
'10':'D12 is the experiment and D15 resolves the wavelet observation sequence X^(n); D1 uses only (4) with D2 scale (5), D5 density conditions and D7 tail bound. D10 is the Besov class with locally bound r,beta,L. D21 is the tempered posterior; its range gives 0<rho<1. The log multiplier is local. Neither D3 nor D6 is imported from Theorem 4.'
}
BRANCHES={
'1':[dict(prior='(3)',scale='(5)',moment='(14), q=2',truth='(9), beta,L>0'),dict(prior='(3)',scale='(6)',moment='(14), q=2',restriction='alpha>=beta',truncation='Both branches also hold with f_k=0 for k>n.')],
'2':[dict(prior='(3)',scale='(5)',moment='(14), q=2'),dict(prior='(3)',scale='(6)',moment='(14), q=2',restriction='alpha>=beta')],
'3':[dict(prior='(4)',scale='(5)',moment='(14), q>=1'),dict(prior='(4)',scale='(6), s_l',moment='(14), q>=1',restriction='alpha>=beta+1/q')],
'4':[dict(prior='(4)',scale='(5)',moment='(14), q=2'),dict(prior='(4)',scale='(6), sigma_k as printed',moment='(14), q=2',restriction='alpha>=beta')],
'5':[dict(prior='(4)',scale='(5)',weight='l^(1+kappa+epsilon)',restriction='epsilon>0'),dict(prior='(4)',scale='(6), s_l',weight='l^((1+kappa+epsilon)/2)',restriction='epsilon>0, any alpha>0')],
'6':[dict(prior='(3)',scale='(6)',tail='(19)',restriction='alpha>1/2, 0<beta<=alpha',rate_equation='(20)'),dict(prior='(3)',scale='(21)',tail='(19)',restriction='a,delta,beta>0',rate_equation='(22)')],
'7':[dict(prior='(4)',scale='(6)',tail='(19)',restriction='alpha>1/2, 0<beta<=alpha',rate_equation='(23)'),dict(prior='(4)',scale='(5)',tail='(19)',restriction='beta>0',rate_equation='(24)')],
'8':dict(referenced_theorem=PID+'/T7',use='Prior parameters and matching rate only; preserve both branches.',additional='g0 bounded away from zero, log g0 in H^beta(L), 0<rho<1'),
'9':dict(referenced_theorem=PID+'/T6',use='Prior parameters and matching rate only; preserve both branches.',additional='logit h0 in S^beta(L), 0<rho<1',unresolved='The preceding classification prose selects wavelet priors instead.'),
'10':[dict(prior='(4)',scale='(5)',tail='(19)',restriction='0<rho<1, r in [1,2], beta>1/r-1/2')]
}
def main():
    data=dict(paper_id=PID,scope='Main text only; supplement and appendices excluded.',unranked_auxiliary_passages=aux,source_issues=NOTES,statement_resolution=RESOLUTION,branch_resolution=BRANCHES,unresolved_source_references=[
        dict(reference='Supplementary Material and Appendices A onward',status='excluded_not_opened',reason='The supplement introduction and appendix bodies are beyond the inspected main-text endpoint. Referenced proof and posterior-contraction results are not imported.'),
        dict(reference='Theorem 5 and equation (17)',status='source_ambiguity_preserved',reason='Printed power weights vanish at level zero but the space definition assumes w_l>=1 for all l>=0.'),
        dict(reference='Theorem 9 and Section 3.3',status='source_ambiguity_preserved',reason='Theorem 6 prior-reference versus wavelet-prose discrepancy, joint-density norm domain and multivariate versus one-dimensional basis convention are unresolved in the inspected main text.'),
        dict(reference='[40], [22] and external general posterior theory',status='external_not_imported',reason='Retain the in-paper coefficient definitions and metric names. External definitions or proof hypotheses are not substituted for the printed statements.')])
    (ROOT/'ambient-prerequisites.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
