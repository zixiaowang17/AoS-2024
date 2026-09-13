"""Save main-text notation, auxiliary formulas and unresolved source conventions."""
import json
from extract_interfaces import ROOT,PID,SOURCE,passage,convert,members

def main():
    aux=[]
    def add(key,raw,page,heading,uses,note):
        aux.append(dict(local_id=key,source_heading=heading,source_kind='source_passage',
            statement_original=convert(raw),original_tex=raw,evidence=[dict(page=page,location=heading)],
            used_by_local_ids=uses,resolution_note=note))
    add('A1',passage('For any $a,b\\in\\mathbb{R}$',r'\section{Problem formulation}'),6,
        'Section 1.4 — Notation',list(members),
        'Ambient notation rather than an additional ranked interface. The PDF prints smallest where the matching TeX says smallset; the mathematical strict inequalities are retained.')
    aux[-1]['statement_original']=aux[-1]['statement_original'].replace('smallset','smallest')
    add('A2',passage('The performance of the policy $\\pi$','One can expect that as long as distributions'),3,
        'Section 1.1 — original cumulative regret, equation (1)',['D4'],
        'Original reward-variable expression referred to by (2); its printed reward arguments are retained. No new theorem dependency is introduced beyond the regret entry.')
    add('A3',passage('As an important observation','As a consequence, at each time'),9,
        'Section 3.1 — conditional bin reward, equation (6)',[],
        'Explanatory conditional mean for positive-mass bins. It is not an additional prerequisite of the algorithms or theorem statements; do not infer a proof dependency.')
    notes=[
      dict(local_ids=['D6','D5'],evidence=[dict(page=7,location='Final paragraph of Section 2.1'),dict(page=14,location='After Theorem 2')],text='The lower-bound admissible-history passage omits the source dataset; Section 2.1 explicitly includes the full source dataset. Both are saved. The omission is unresolved, not silently repaired.'),
      dict(local_ids=['D12'],evidence=[dict(page=8,location='Definition 1 and following paragraph')],text='The transfer exponent is defined as the smallest exponent, including infinity. Attainment and the meaning of r^infinity at r=1 are not specified. The following assertion that infinity always works is not used to replace the original definition.'),
      dict(local_ids=['D15','D16','D17'],evidence=[dict(page=9,location='Equation (5)'),dict(page=10,location='Bin selection, visit count and tree')],text='Bins are closed, and the containing bin is chosen by center closest to the origin. The count formula includes s=t despite prose saying prior to t. The perfect-tree description uses depths 0<=i<l. These printed conventions are preserved.'),
      dict(local_ids=['D19'],evidence=[dict(page=10,location='Equation (8)')],text='The empirical-mean summand prints Y with no i subscript, although the record is indexed by i. No correction is inserted into the original statement.'),
      dict(local_ids=['D23','D31','D22','D22a'],evidence=[dict(page=11,location='Algorithm 1'),dict(page=12,location='Procedure 1'),dict(page=17,location='Algorithm 2')],text='The algorithms remove B from the partition using setminus B as printed, and use tilded active-set and count outputs where Procedure 1 prints untilded versions. The correspondence is recorded without rewriting either source.'),
      dict(local_ids=['D22a','D29','D30'],evidence=[dict(page=12,location='Procedure 1 step 2'),dict(page=17,location='Algorithm 2 and following adaptive substitutions'),dict(page=18,location='Equation (18)')],text='Algorithm 2 and Section 4.2 substitute U-hat and associated tau-hat. The original Procedure 1 initializer still references (10). The adaptive local member preserves that body and separately records the substitutions; it does not inherit the true gamma/kappa confidence formula.'),
      dict(local_ids=['D26'],evidence=[dict(page=16,location='Assumption 4')],text='One common arm must satisfy self-similarity under Q_X and P_(X|pi=k). A conditional law for a zero-probability arm is not defined here; the general exploration coefficient can be zero. No positivity condition is added to the source.'),
      dict(local_ids=['D28'],evidence=[dict(page=18,location='Procedure 2 steps 13 and 20')],text='The grid prints k_i=[2^l3] and i=[d], rather than membership signs. The smoothness formula prints ordinary log(b), while its correction uses log_2. The b=0 case is not given a separate convention. Preserve these source expressions.'),
      dict(local_ids=['D28','D31'],evidence=[dict(page=17,location='Algorithm 2 step 2'),dict(page=18,location='Procedure 2 input and sample counts')],text='Procedure 2 lists tuning constants C1,C2 but Algorithm 2 does not pass them explicitly. No finite-sample clipping of T to the available source or target budget is specified. These implementation details remain unresolved.'),
      dict(local_ids=['D29'],evidence=[dict(page=17,location='Equation (17)'),dict(page=18,location='Conventions following (17)')],text='The zero-pull branch uses ordinary log(n|B|^(d+2 beta-hat)), not log-plus; the square-root domain is not repaired. The source explicitly specifies 1/0=infinity.'),
      dict(local_ids=['A1','D28'],evidence=[dict(page=6,location='Section 1.4'),dict(page=18,location='Procedure 2')],text='The source describes floor/ceiling using strictly smaller/larger integers. The familiar non-strict convention is not substituted.'),
    ]
    data=dict(paper_id=PID,scope='Main text only; no appendix or external proof inspected.',
        auxiliary_passages=aux,
        standard_ambient_resolution=[
          'Probability laws, measurable random variables, conditional distributions and expectations, integrals, supports, indicators, Euclidean and sup norms, finite sums, minima/maxima, suprema/infima and asymptotic comparison retain the source ambient mathematical meanings. No mathlib availability is asserted.',
          'Section 1.4 defines the covariate cube, closed sup-norm balls, log-plus and constants independent of nP and nQ. Section 2.2 fixes K as constant; no K>=2 assumption is added.',
          'Definition 3 names the generic Holder class H(beta,C_beta). Resolve its individual-function Holder bound by the inequality in Assumption 1 on page 7, without importing the assumption that every arm has that property into the definition for an arbitrary f.',
          'Algorithm inputs and local variables are bound by their saved full procedures: arm sets, finite partitions, source subsets, counts, empirical means, confidence radii, tuning constants and smoothness/transfer bounds. Theorems 1-4 retain their own alpha*beta<=d and parameter quantifiers.',
          'The common conditional reward law, source iid covariate-arm sampling and target history are recorded as distinct local passages. Within-vector arm independence is not asserted.',
          'The lower-bound admissible-policy convention is shared by Theorems 2 and 4. Theorem 4 does not require running either upper-bound algorithm.',
        ],unresolved_source_conventions=notes,
        transcription_notes=[
          'Procedure 2 equation (16) was checked against the PDF, including the grouping of numerator and denominator and their indicator factors. Its TeX is valid and retained verbatim in the raw archive.',
          'The PDF, rather than the ordering of algorithm environments in TeX, supplies the evidence pages: Assumption 4 and the self-similar class are on 16, Algorithm 2 on 17, Procedure 2 on 18, equation (17) spans its formula on 17 and conventions on 18.',
        ])
    (ROOT/'ambient-conventions.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print('Saved three unranked source passages and eleven explicit source-convention notes.')
if __name__=='__main__':main()
