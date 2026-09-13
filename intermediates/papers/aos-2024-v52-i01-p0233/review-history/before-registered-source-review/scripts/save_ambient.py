"""Preserve notation and source ambiguities without adding theorem assumptions."""
import json
from extract_interfaces import ROOT,PID
NOTATION=r'''
Throughout this paper, we adopt the convention that $0/0=0$. We use $\Delta(\mathcal S)$ to indicate the probability simplex over the set $\mathcal S$, and denote by $[H]$ the set $\{1,\ldots,H\}$ for any positive integer $H$. We use $\mathbb 1(\cdot)$ to represent the indicator function. For any vector $x=[x(s,a)]_{(s,a)\in\mathcal S\times\mathcal A}\in\mathbb R^{SA}$, we overload the notation by letting $x^2=[x(s,a)^2]_{(s,a)\in\mathcal S\times\mathcal A}$. For two vectors $a=[a_i]_{1\leq i\leq n}$ and $b=[b_i]_{1\leq i\leq n}$, $a\circ b=[a_ib_i]_{1\leq i\leq n}$ denotes their Hadamard product, and $a\geq b$ (resp., $a\leq b$) means $a_i\geq b_i$ (resp., $a_i\leq b_i$) for all $i$. Following the convention in RL, the norm $\|\cdot\|_1$ of a matrix $P=[P_{ij}]$ is defined to be $\|P\|_1:=\max_i\sum_j|P_{ij}|$. For any probability vector $q\in\mathbb R^{1\times S}$ (which is a row vector) and any vector $V\in\mathbb R^S$, define
\[
\operatorname{Var}_q(V):=q(V\circ V)-(qV)^2\in\mathbb R\tag{8}
\]
with $qV=\sum_iq_iV_i$, which corresponds to the variance of $V$ w.r.t. the distribution $q$. The standard notation $O(\cdot)$ is adopted to represent the orderwise scaling of a function.
'''
def main():
    data=dict(paper_id=PID,scope='Published main text only; separate supplement excluded.',
        auxiliary_passages=[dict(local_id='A1',source_kind='source_passage',source_heading='Section 1.4 — Notation',
            statement_original=NOTATION.strip(),evidence=[dict(page=6,location='Section 1.4'),dict(page=7,location='Section 1.4 continuation, equation (8)')],
            used_by_local_ids=['D7','D8','D19','D20','D11','D22'],
            resolution_note='The global 0/0 convention governs the density ratios and zero-count expressions. Equation (8) resolves the empirical row variance in both penalty formulas; this is a local auxiliary, not an asserted mathlib declaration.')],
        standard_ambient_resolution=[
          'The finite state and action sets, positive integral horizon and finite sums use the source index-set conventions. Probability simplices, expectations and conditional trajectory laws are resolved in the source models and policy definitions.',
          'The discounted theorem pair uses gamma-discounted values, normalized discounted occupancy and N independent transitions. The finite-horizon pair uses stepwise values and occupancies and K independent trajectories of length H; within-trajectory observations are not independent.',
          'V-star(rho) and V_1-star(rho) use the respective weighted-value definitions with the selected deterministic optimal policy substituted. The initial test distribution rho need not equal the behavior initial distribution rho-b in the episodic setting.',
          'The source fixes a single deterministic optimal policy in each setting. Concentrability pertains to that policy; no supremum over all policies or all possible optimal choices is introduced.',
          'C-star and C-star-clipped are distinct coefficients. Theorem 1 explicitly permits either Definition 2 or Definition 1; Theorem 3 explicitly permits either Definition 4 or Definition 3. These alternatives are recorded as direct uses without equating the coefficients.',
          'Algorithm estimates Q-hat and V-hat are local iteration variables, not true value functions. Their zero/terminal initial values and greedy updates are in the full algorithm bodies. The variance penalties accept the already available current or next value vector; no circular dependency on a completed policy evaluation is added.',
          'Theorem 2 binds the two MDPs, P0/P1, the initial distribution and estimated policy in its own statement. Theorem 4 similarly binds its MDP family, index set Theta and P-theta. Their construction proofs are not prerequisites of their statements.',
          'The error-probability events retain >epsilon in Theorem 2 and >=epsilon in Theorem 4. The upper-bound guarantees retain at least 1-2 delta versus exceeding 1-12 delta and their distinct sample/trajectory counts.',
          'The generic input D0 in Section 3.2 is a collection of time-labelled transitions. Algorithm 3 supplies it from trimmed trajectories; it is not independently equated with the iid transition model of Section 2.1.',
        ],
        unresolved_source_conventions=[
          dict(local_ids=['D16','D17'],evidence=[dict(page=15,location='Equations (41b) and (43)')],text='The stepwise occupancy formula (41b) prints pi(a|s) without h; the optimal occupancy formula (43) likewise prints pi-star(s). The surrounding definitions specify time-indexed policies. The original formulas are preserved without adding subscripts.'),
          dict(local_ids=['D24'],evidence=[dict(page=19,location='Algorithm 3, subsampling steps (1)-(3), equation (56)')],text='The procedure uses first and remaining K/2 trajectories without specifying odd-K rounding. The trimming bound in (56) can be nonintegral, but the random sample count is its minimum with an integer count; no rounding rule is stated. Neither an even-K assumption nor a floor is inserted.'),
          dict(local_ids=['D24'],evidence=[dict(page=18,location='Section 3.3 first subsampling bullet'),dict(page=19,location='Algorithm 3 step 2(1)')],text='The prose describes a random split into two halves; Algorithm 3 specifies the first and remaining halves. The full algorithm is retained as printed. Its input trajectories are iid, but no permutation operation is silently added.'),
          dict(local_ids=['D11','D22','D24'],evidence=[dict(page=10,location='Equation (28)'),dict(page=17,location='Equation (55)'),dict(page=19,location='Equation (56) and Algorithm 3 input')],text='The paper explicitly sets 0/0=0. Positive-over-zero expressions in the capped penalties do not receive a separate convention here. Algorithm 3 uses delta in trimming and in the called Algorithm 2, while listing only data and rewards as inputs; delta remains the theorem-specified tuning quantity.'),
          dict(local_ids=['D21','D22','D24'],evidence=[dict(page=17,location='Section 3.2 D0 and (55)'),dict(page=19,location='Algorithm 3 final step'),dict(page=20,location='Theorem 4 equation (61)')],text='Section 3.2 uses N for the size of the supplied transition collection D0, while the overall sample-complexity discussion uses N=KH before trimming. The source expressions and both contexts are retained rather than silently replacing N in (55) with KH.'),
          dict(local_ids=['D8','D20'],evidence=[dict(page=13,location='Theorem 2'),dict(page=20,location='Theorem 4')],text='The lower-bound statements print upper bounds on epsilon without an explicit positive lower bound; Theorem 4 also does not restate an S>=2 condition. No additional conditions are inserted into their original statements. Their ambient finite-MDP and target-accuracy context remains separate.'),
        ],
        excluded_proof_dependencies=['Supplement Sections A, B.2, B.3, C, C.2, D.1, E.2 and E.3 were referenced in main text but not opened. Lemmas, numerical examples and proof techniques do not create additional theorem records or statement requirements.'])
    (ROOT/'ambient-conventions.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print('Saved source notation, variance formula and six source-convention notes.')
if __name__=='__main__':main()
