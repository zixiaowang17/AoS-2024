"""Preserve local conventions and unresolved source details outside ranked interfaces."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
aux=[]
def passage(heading,body,page,users,note):
    aux.append(dict(local_id='A'+str(len(aux)+1),source_heading=heading,source_kind='source_passage',statement_original=body.strip(),evidence=[dict(page=page,location=heading)],used_by_local_ids=users,resolution_note=note))

passage('Section 1 — convergence notation',r'''
All convergences are for $n$ to infinity, if not mentioned otherwise. Weak convergence of random variables and probability distributions is denoted by '$\rightsquigarrow$'.
''',3,[],'Applies to both theorems. Convergence in probability, expectations, conditional expectations, normal laws, product probability laws and independence are standard ambient notions; no source definition is invented.')
passage('Section 2 — fixed order and growing dimension',r'''
Throughout this section, fix $m\in\mathbb N$, and let $n$ be sufficiently large such that $d=d(n)\geq m$. Our test statistic for testing $H_m$ in (1.4) will be based on combining test statistics for each individual $H_k$ with $k\in\{2,\ldots,m\}$.
''',3,['D4','D9','D10'],'The construction uses a fixed finite order m and sufficiently large sample sizes. Theorem 3.1 supplies different dimension-rate conditions for its two assertions; the generic array theorem does not use m.')
passage('Section 2 — marginal evaluation convention',r'''
Here, for a c.d.f. $G$ on $[0,1]^d$, $G_A$ is defined as
\[
G_A((u_j)_{j\in A})=G(u^A),\qquad (u_j)_{j\in A}\in[0,1]^{|A|},
\]
where $u^A\in[0,1]^d$ has $p$th component $u^A_p=u_p\mathbf1_{\{p\in A\}}+\mathbf1_{\{p\notin A\}}$. Occasionally, we also use the notation $u^A$ for vectors $u\in[0,1]^d$, which should note yield any confusion. Finally, we also write $G_A(u)=G(u^A)$ for $u\in[0,1]^d$, despite the fact that $G_A$ is a function on $[0,1]^{|A|}$.
''',4,['D3','D7'],'Coordinates outside A are set to one. Preserve the source wording should note; no mathematical meaning is changed by that typographical error.')
passage('Section 2 — empirical copula',r'''
The basic underlying ingredient is the empirical copula, defined as
\[
\widehat C_n(u)=\frac1n\sum_{i=1}^n\mathbf1_{\{\widehat U_i\leq u\}},\qquad u=(u_1,\ldots,u_d)^\top\in[0,1]^d,
\]
''',3,['D5','D6'],'Source context for the pseudo-observations and copula-process construction. The selected centered product process is explicitly defined using pseudo-observations; no additional dependency through this empirical cdf is invented.')
passage('Theorem 6.5 — conditional variance convergence',r'''
\[
\sum_{r=1}^d\mathbb E\left[X_{n,r}^2\mid\mathcal F_{n,r-1}\right]\xrightarrow[n\to+\infty]{\mathbb P}\eta^2,\tag{6.25}
\]
''',20,['D11'],'The unnamed condition is bound inside Theorem 6.5 and retained in its complete statement. No new author keyword is fabricated for it. The limit is the same eta-squared used in the mixed normal conclusion.')
passage('Section 1 — pairwise independence hypothesis',r'''
$H_2:X_1,\ldots,X_d$ are pairwise independent,

or, equivalently, that all bivariate margins of $C$ are equal to the bivariate independence copula, i.e.,
\[
H_2:C_A=\Pi_2\text{ for all }A\in I_d(2),\tag{1.3}
\]
''',2,['D4','D8'],'Supplies the k=2 endpoint for the family extended in equation (1.4). It is not substituted for the stronger H_5 or H_(4m-3) hypotheses in Theorem 3.1.')

unresolved=[]
def issue(ids,page,location,text):
    unresolved.append(dict(local_ids=ids,evidence=[dict(page=page,location=location)],text=text))
issue(['D4'],2,'Equation (1.4) and following sentence','The equation describes k-wise independence, but the prose says k-wise dependent and prints H2 subset H3 subset ... subset Hd. Those are source discrepancies; the original remains unchanged. Correspondence explanations refer to the displayed copula equality.')
issue(['D4'],6,'Theorem 3.1','H_k is introduced for k<=d. The theorem invokes H5 and H_(4m-3); fixed m and d_n tending to infinity eventually allow those dimensions. No all-n extension or alternate meaning for k>d is added.')
issue(['D8'],4,'Equation (2.2)','The source uses A subset {2,...,d} while admitting k=d and elsewhere summing over {1,...,d}. The inconsistent index set is retained; no hidden corrected definition is supplied.')
issue(['D10'],6,'Final sentence of Theorem 3.1','The source says delta_n(m) may be replaced by bar-delta_n(m), rather than explicitly saying every delta_n(k). The original statement and its possible ambiguity are preserved; the replacement is not expanded.')
issue(['D11','D12','D13'],20,'Theorem 6.5, equations (6.24)-(6.26)','Equation (6.24) visibly uses an unsquared signed martingale difference in its truncated conditional expectation. Equations (6.25) and (6.26) use powers two and four. No standard squared Lindeberg condition is substituted, and no claim is made that the printed theorem has been proved correct.')
issue(['D11'],20,'Theorem 6.5 opening and conclusion','The array is indexed for r>=1 but its differences use S_n,0, and the conclusion identifies S_n,d with the sum of differences. The source does not separately state S_n,0=0. No extra initial-value assumption is inserted.')
issue(['D11'],20,'Theorem 6.5 filtration inclusion','The cross-row inclusion F_n,r subset F_(n+1),r is printed for every r<=d_n, without a separately stated monotonicity condition on d_n. This domain convention is preserved without adding monotonicity.')
issue(['D6'],4,'Finite-grid cdf U_n','The formula min{floor((n+1)t)/n,1} is used at coordinates in [0,1]. It is not silently extended to a cdf on all real t by adding an unprinted lower clamp.')

data=dict(paper_id=ROOT.name,scope='Pinned arXiv v1 main document, PDF pages 1-30; supplementary appendices excluded.',auxiliary_passages=aux,
 standard_ambient_resolution=[
  'Theorem 3.1 uses n iid observations and continuous univariate margins. A generic observation X and sample-indexed X_i have distinct meanings despite overlapping scalar notation.',
  'I_d(k) is the family of all k-coordinate subsets. Pi_d is the product copula; C_A and Pi_A are marginals with the evaluation convention in A3.',
  'Pseudo-observations retain max-ranks and the n+1 denominator. Their deterministic construction and the centered product process do not by themselves require mutual independence.',
  'U_n is the finite-grid cdf used for centering. The original uncentered product with u_p in each factor and its bar-S statistic appear earlier on page 4 but are not the statistic S^M in equation (2.1). Their formulas are preserved in main-text evidence; no relation to an unselected alternative is counted.',
  'T_n(k) aggregates all subset statistics. The scaling sequences retain an exact finite-sample null variance bar-delta and the explicit asymptotic variance constant in delta, together with nu_n centering.',
  'Theorem 3.1 has a scalar first assertion under H5 with only d_n tending to infinity, and a separate joint assertion under H_(4m-3) with the stated upper growth rate. m is fixed; the theorem does not prove a growing-m extension.',
  'Theorem 6.5 introduces its own generic martingale array, filtrations and differences. The conditional-variance hypothesis, almost-sure finiteness, eta, Z, normal N and its independence are retained as local binders or standard ambient requirements in the complete statement.',
  'The Lindeberg and Lyapunov source excerpts are condition records from Theorem 6.5, not numbered Definitions. The fourth-moment sufficient condition is not made a simultaneous assumption of the first implication.',
  'Products of standard normal laws in Theorem 3.1 and the independent scale mixture in Theorem 6.5 are distinct conclusions. They do not impose each other\'s sampling conditions.'
 ],unresolved_source_conventions=unresolved,excluded_proof_dependencies=[
  'Theorem 6.5 is fully included because it is printed as a Theorem in the main document. Its use in proving Proposition 6.4 or Theorem 3.1 does not create statement-dependency edges into Theorem 3.1.',
  'Centered summand reductions, the martingale specifically constructed in the subsequent proof, higher-order moment calculations and combinatorial lemmas are proof machinery, not additional conditions of either theorem statement.',
  'Corollary 3.2 supplies a further combined statistic and test rule, but no Theorem here states that rule. It is not inventoried or attached as a prerequisite.',
  'The supplementary material starts on PDF page 31. Its appendix proofs, calculations and joint-convergence extension are not extracted.'
 ])
def main():
    (ROOT/'ambient-conventions.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print('Saved six auxiliary passages and eight explicit source-convention issues.')

if __name__ == '__main__':
    main()
