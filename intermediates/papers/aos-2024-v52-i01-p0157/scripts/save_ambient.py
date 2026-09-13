"""Archive main-text ambient conventions without inventing source definitions."""
import json
from extract_interfaces import ROOT, PID, passage, convert

def main():
    specs=[
      ('Section 1.1 — measurable observation space', [1], passage('These measurements are assumed', 'Putting two samples together')),
      ('Section 2.1 — unknown null distribution', [5], passage('Throughout the paper, we consider the semi-supervised setting', r'\subsection{Criteria}')),
      ('Section 2.2 — measurable rejection procedure', [5], passage('A novelty detection procedure is a measurable function', 'Given a procedure $R$')),
      ('Section 2.2 — TDR and TDP, equation (3)', [5], passage('Similarly, the true discovery rate', r'\subsection{BH algorithm')),
      ('Section 4.4 — measurable score class', [14], passage('Here, $g$ is a function that belongs', 'Typical choices of the loss function')),
      ('Section 5 — Euclidean observations', [17], passage('Throughout this section we assume', 'We start in Section')),
    ]
    rows=[dict(name=name, statement_original=convert(raw), original_tex=raw,
               evidence=[dict(page=p, location=name) for p in pages]) for name,pages,raw in specs]
    data=dict(paper_id=PID,passages=rows,
      notes=[
       'These ambient passages are retained outside the ranked interface list. TDR/TDP are archived to distinguish the source terminology from the undefined TPR in Theorem 4.1; their equivalence is not asserted.',
       'Probability, expectation, indicators, finite index sets, floors, ceilings, minima, maxima, inverse functions, measurable functions and iid uniform variables are ambient mathematical notions. Their specialized source formulas are retained in the corresponding interfaces.',
       'Super-uniform is used in Theorem 3.3 without a main-text formula. It is recorded as ambient terminology rather than supplied with a fabricated original definition.',
       'Theorem 3.4 binds random variables K_i with range {1,...,m}; the main text does not construct them. No appendix construction is imported.',
       'G in Theorem 3.6, r-prime and c-prime in Theorem 4.1, and epsilon0, Delta, M, the event R and alpha-prime in Theorems 5.1 and 5.4 are bound or defined inside their statements.',
       'Theorem 5.1 inherits the independent positive-density model from the setting of Theorem 4.1. It does not invoke that theorem as a proved premise or use its mFDR-optimality conclusion.',
       'Theorem 3.3 needs the AdaDetect score and p-value construction for its final specialization; the subsequent BH rejection step is not a requirement for its conclusion about the p-values.'],
      unresolved_source_conventions=[
       dict(source='Theorem 4.1 and Section 4.2', issue='TPR is not explicitly defined in the inspected main text, and the mFDR passage uses calibration indices in its numerator while rejection sets use test indices. The printed higher TPR comparison and exact-level threshold existence clause are preserved.'),
       dict(source='Section 4.1, equations (16) and (18)', issue='The average alternative density divides by m1 and the claimed range r in (0,1) implicitly requires nondegenerate mixture proportions. The source does not add those restrictions to Assumption 5; they are not silently inserted.'),
       dict(source='Section 3.2 — PRDS', issue='Conditional probabilities given p_i=u require a version, including at unattained values of these discrete p-values. The main-text definition does not select one. Assumption 1 separately includes its conditional-distribution existence footnote.'),
       dict(source='Section 3.4, equation (13)', issue='The cdf expression uses an indicator to restrict the order-statistic term to 1/(ell+1)<=x<1; outside that interval the subscript may be out of range. Preserve the source expression; do not replace it with an unquoted piecewise definition.'),
       dict(source='Section 5.1, equations (25)-(29)', issue='The main text does not specify optimizer existence, measurable selection or permutation-invariant tie selection for the argmin formulas, nor the induced set-class convention for VC dimension of real-valued scores. Denominators involving ell and M also retain their printed domain limitations.'),
       dict(source='Section 4.2, equation (19)', issue='The prose says strictly monotone transformation, while the displayed condition says increasing continuous Psi. Both are retained; neither strictness nor a change in direction is silently imposed.'),
       dict(source='Section 5.2, equations (33)-(36)', issue='The inverse tail, its range and attainment of the maximum in zeta retain the printed conventions. Theorem 5.4 separately assumes continuity and strict decrease. No generalized-inverse convention or level clipping is inserted.')])
    (ROOT/'ambient-conventions.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print('Saved six original ambient passages and unresolved source conventions.')

if __name__=='__main__':main()
