"""Rebuild original main-text passages and local dependencies for this paper.

The saved data is manually transcribed; source audit is a separate stage.
"""
import json
from pathlib import Path
from save_inventory import PID, claims

ROOT = Path(__file__).resolve().parents[1]
interfaces, members, edges = [], {}, {}


def add(lid, term, body, pages, heading, deps=None, *, kind='definition',
        symbols=(), phrases=(), context=None, context_pages=None, shape):
    evidence = [dict(page=p, location=heading) for p in pages]
    member = dict(paper_id=PID, local_id=lid, local_label=heading,
        source_heading=heading, source_kind=kind, statement_original=body.strip(),
        relation='exact', depends_on=list(deps or {}), evidence=evidence,
        highlight_symbols=list(symbols), highlight_phrases=list(phrases))
    keyword = dict(paper_id=PID, local_id=lid, source_text=term,
                   label=term[0].upper()+term[1:], kind='term')
    if term not in body:
        assert context and term in context, (lid, term)
        member['naming_context'] = [dict(context_id=lid+'/name', text=context,
            evidence=[dict(page=p, location=heading+' — naming context') for p in (context_pages or pages)])]
        keyword['context_id'] = lid+'/name'
    interfaces.append(dict(interface_id=PID+'/'+lid, rank_group='all', name=keyword['label'],
        lean_role='hypothesis' if kind in ('condition', 'assumption') else 'definition',
        type_shape=shape, semantic_boundary=shape, members=[member], source_keywords=[keyword],
        central_claim_uses=[], dependencies=[], theorem_explanations={}))
    members[lid] = member
    edges[lid] = deps or {}


add('D1','signal plus noise model',r'''
To be more specific, we consider the signal plus noise model
\[
\mathbf Y=\mathbf A+\mathbf E,\tag{1}
\]
''',[1],'Introduction — observation equation (1)',kind='source_passage',symbols=[r'\mathbf Y=\mathbf A+\mathbf E'],shape='The common additive matrix observation equation. The Gaussian and sub-Gaussian noise laws are separate source passages; the equation alone does not impose a noise law.')

add('D2','standard normal distribution',r'''
where $\mathbf A$ is the unobserved signal and $\mathbf E$ is a $p\times q$ noise matrix with independent entries following a standard normal distribution. Extension to non-Gaussian noise are dealt with at the end of the manuscript. Without loss of generality the noise variance is set to one. Also, we assume throughout the manuscript that $p\ge q$.
''',[1],'Introduction — Gaussian noise and dimension convention',{'D1':'The noise matrix and unobserved signal belong to observation equation (1).'},kind='condition',symbols=[r'\mathbf E'],phrases=['standard normal distribution'],shape='Independent standard Gaussian noise for Sections 1-5. Theorem 6.3 replaces this law with the Section 6 sub-Gaussian setup; it retains the dimension order directly in its own statement.')

add('D3','singular values',r'''
Given a $p\times q$ matrix $\mathbf A$, we write $\sigma_1(\mathbf A)\ge\sigma_2(\mathbf A)\ldots\ge\sigma_q(\mathbf A)\ge0$ for its ordered sequence of singular values. The rank of a matrix $\mathbf A$ corresponds to its number of positive singular values.
''',[1],'Introduction — ordered singular values',symbols=[r'\sigma_1(\mathbf A)',r'\sigma_q(\mathbf A)'],shape='Descending singular values of a rectangular matrix, including zero values up to q. No rank restriction is imposed by this definition.')

add('D4','Schatten norm',r'''
For any $s\ge1$, the $s$-Schatten norm of $\mathbf A$ is defined as the $l_s$ norm of its sequence of singular values, that is
\[
\|\mathbf A\|_s^s=\sum_{i=1}^q\sigma_i^s(\mathbf A).\tag{2}
\]
''',[1],'Introduction — Schatten norm (2)',{'D3':'The norm is the l_s norm of the ordered singular-value sequence.'},symbols=[r'\|\mathbf A\|_s^s'],shape='Finite s>=1 Schatten norm, distinguished from its s-th power and from entrywise matrix norms. The bound in Theorem 3.3 uses powers 4k-4 and 4k-2; Theorem 6.3 uses the 2k-th power as target.')

add('D5','operator norm',r'''
For $s=\infty$, we define $\|\mathbf A\|_\infty=\sigma_1(\mathbf A)$ as the operator norm of $\mathbf A$.
''',[1],'Introduction — operator norm',{'D3':'The operator norm is the largest singular value.'},symbols=[r'\|\mathbf A\|_\infty'],shape='Largest singular value, not entrywise maximum. It bounds the parameter set in Theorem 4.9 and appears in the sub-Gaussian risk terms.')

add('D6','functional',r'''
More generally, given a function $f:\mathbb R^+\mapsto\mathbb R^+$, we define the functional $f_\sigma(\mathbf A)$ by $f_\sigma(\mathbf A)=\sum_{i=1}^q f(\sigma_i(\mathbf A))$.
''',[1],'Introduction — spectral functional',{'D3':'The functional sums f over the singular values.'},symbols=[r'f_\sigma(\mathbf A)'],shape='Original nonnegative-valued f convention. Theorem 4.9 explicitly broadens f to a continuous real-valued function and repeats the same defining sum; this range distinction is retained.')

add('D7','Hermite polynomial',r'''
Write $\phi(y)=e^{-y^2/2}(2\pi)^{-1/2}$ for the density of the standard normal random variables. For a positive integer $r$, we define the Hermite polynomial of degree $r$ by the equation
\[
\frac{d^r}{dy^r}\phi(y)=(-1)^rH_r(y)\phi(y).\tag{8}
\]
''',[7],'Section 3 — Hermite polynomial (8)',symbols=[r'H_r(y)'],shape='Probabilists Hermite polynomials defined using the standard Gaussian density, regardless of the law of the observed noise. Degree zero is consumed by U_k but not included in this printed positive-integer definition; record H_0 as an ambient convention.')

add('D8','number of occurrences',r'''
Given two sequences $i=(i_1,\ldots,i_k)$ and $j=(j_1,\ldots,j_k)$, we denote $N_{rs}(ij)$ the number of occurrences of the 2-tuple $(r,s)$ in the sequences $(i_t,j_t)$ and $(i_t,j_{t+1})$ with $t=1,\ldots,k$ (recall that, by convention $i_{k+1}=i_1$).
''',[7],'Section 3 — occurrence counts before (9)',symbols=[r'N_{rs}(ij)'],shape='Counts of each matrix-entry pair in the cyclic product. The sentence prints i_(k+1)=i_1, while the earlier cyclic product explicitly defines j_(k+1)=j_1; both original conventions are preserved separately.')

add('D9','estimator',r'''
\[
U_k=\sum_{i_1,\ldots,i_k=1}^p\sum_{j_1,\ldots,j_k=1}^q\prod_{r=1}^p\prod_{s=1}^q H_{N_{rs}(i,j)}(\mathbf Y_{rs})\tag{9}
\]
''',[7],'Section 3 — polynomial estimator (9)',{'D1':'The polynomial is evaluated on the observed matrix Y.','D7':'Each matrix-entry factor is a Hermite polynomial.','D8':'Its degree is the occurrence count of that matrix entry.'},context='Then, the estimator',symbols=[r'U_k='],shape='Same explicit polynomial statistic under both noise laws. Unbiasedness holds in the Gaussian setup; the sub-Gaussian theorem controls its squared error and does not assert unbiasedness.')

add('D10','supremum norm',r'''
For a continuous function $g$ defined on an interval $I$, we denote $|g|_{\infty,I}=\sup_{x\in I}|g(x)|$ its supremum norm.
''',[10],'Section 4.2 — supremum norm',symbols=[r'|g|_{\infty,I}'],shape='Uniform norm on the specified interval. Theorem 4.9 uses double bars for f while this original convention uses single bars; the notation alias is recorded explicitly.')

add('D11','best uniform approximation',r'''
Given a collection $\mathcal F$ of functions, an interval $I$ and a function $g:I\mapsto\mathbb R$, we denote
\[
E_{\mathcal F}[g,I]=\inf_{f\in\mathcal F}|f-g|_{\infty,I},\tag{16}
\]
for the best uniform approximation of $g$ by $\mathcal F$.
''',[11],'Section 4.2.1 — best uniform approximation (16)',{'D10':'The objective uses the original interval supremum norm.'},symbols=[r'E_{\mathcal F}[g,I]'],shape='Infimum uniform approximation error for an arbitrary function class. In Theorem 4.9 instantiate with symmetric polynomials of degree at most 2k-star; no existence of a minimizing polynomial is added.')

add('D12','symmetric polynomials',r'''
In the sequel, $\mathcal P_k^{sym}$ denote the space of the symmetric polynomials of degree less or equal to $k$.
''',[12],'Section 4.3 — symmetric polynomial space',symbols=[r'\mathcal P_k^{sym}'],shape='Univariate even/symmetric polynomials with a degree bound. Theorem 4.9 uses degree at most 2k-star. The main-text discussion that these can be represented as P(x^2) records the intended even symmetry.')

add('D13','probability measure',r'''
Write $\delta_x$ for the Dirac measure at $x$. Given a vector $\sigma=(\sigma_1,\ldots,\sigma_q)$, let $\mu_\sigma=q^{-1}\sum_{i=1}^q\delta_{\sigma_i}$ where $\delta_x$ denote the associated probability measure.
''',[13],'Section 5 — empirical measure of a vector',symbols=[r'\mu_\sigma',r'\delta_x'],shape='Equal-weight empirical measure with exactly q atoms counted with multiplicity, not the unnormalized counting measure. The original concluding delta_x phrase is retained despite its apparent misidentification of the associated measure.')

add('D14','Wasserstein distance',r'''
For two measures $\mu_1$ and $\mu_2$ on $\mathbb R$ with cumulative distribution functions $F_{\mu_1}$ and $F_{\mu_2}$, the Wasserstein distance $W(\mu_1,\mu_2)$ is defined as
\[
W(\mu_1,\mu_2)=\int_{\mathbb R}|F_{\mu_1}(t)-F_{\mu_2}(t)|dt.
\]
''',[13],'Section 5 — Wasserstein distance on the line',symbols=[r'W(\mu_1,\mu_2)'],shape='One-dimensional order-one Wasserstein distance in CDF form. In the theorem it compares bounded empirical probability measures; it is not a higher-order transport cost.')

add('D15','even moments',r'''
Let $K$ be a tuning parameter. Denote the size $K$ vector $\widehat m$ by $\widehat m_k=q^{-1}[M(pq)^{1/4}]^{-2k}U_k$ where $U_k$ defined in (9) is our estimator of the $\|\mathbf A\|_{2k}^{2k}$.
''',[13],'Section 5 — normalized even-moment estimates',{'D9':'Each coordinate rescales the polynomial statistic U_k.','D4':'The source identifies its target as a power of a Schatten norm.'},context='Still, we can adapt their approach by nearly matching the first even moments instead of all the first moments.',symbols=[r'\widehat m_k'],shape='First K even-moment estimates, normalized by q and by the known spectral scale. The subsequent program uses undefined hat U in place of this named vector; preserve the mismatch and the evidence of the intended moment-matching connection.')

add('D16','regular grid',r'''
Fix $\zeta=1/(M^2q)$ and consider a fine regular grid $x=(x_1,\ldots,x_d)$ on $[0,b(pq)^{1/4}]$ with $x_i=(i-1)\zeta$ and $d=\lceil M(pq)^{1/4}/\zeta\rceil$. Define also the $K\times d$ matrix $\mathbf V$ such that $\mathbf V_{ij}=x_j^{2i}$.
''',[13,14],'Section 5 — grid and even-power matrix',symbols=[r'\zeta=1/(M^2q)',r'\mathbf V_{ij}=x_j^{2i}'],shape='Printed grid, its cardinality and even-power design matrix. The upper endpoint uses an undefined b whereas d uses M; the physical scaling conflicts with the normalized-moment vector and subsequent rescaling. No corrected grid is substituted.')

add('D17','linear program',r'''
Let $p^+\in\mathbb R^d$ be the solution to the following linear program, which we will regard as a distribution consisting of point masses at values $x$
\[
\operatorname{minimize}_p|\mathbf Vp-\widehat U|_1\text{ subject to }1^Tp=1\text{ and }p>0.\tag{24}
\]
''',[14],'Section 5 — estimator step 1, linear program (24)',{'D16':'The program uses the grid dimension, grid points and even-power design matrix.','D15':'The procedure introduces normalized even-moment estimates immediately before the grid; the proof of Theorem 5.2 uses hat m in the objective. The displayed program instead writes undefined hat U, so their identification is recorded as an unresolved source notation mismatch.'},symbols=[r'p^+',r'\widehat U'],shape='Printed l1 fitting program on strictly positive unit-mass weights. Strict positivity, existence of a minimizer and the undefined hat U alias remain unresolved. Do not silently replace p>0 by nonnegativity.')

add('D18','two step estimator',r'''
Return the singular values $\widehat\sigma_i$ by taking the rescaled $i$-th $(q+1)$st quantile of the distribution corresponding to $p^+$, that is $\widehat\sigma_i=M(qp)^{1/4}\min\{x_j:\sum_{l\le j}p_l^+\ge\frac{i}{q+1}\}$.
''',[14],'Section 5 — estimator step 2, rescaled quantiles',{'D17':'The quantiles use the fitted weight vector p-plus from the preceding program.','D16':'They use the original grid points and rescale by M(qp)^(1/4).'},context='We consider the following two step estimator of the singular values vector.',symbols=[r'\widehat\sigma_i'],shape='Ascending rescaled quantiles at i/(q+1), as printed. The true singular values are defined in descending order, creating a source ordering mismatch in the coordinate-error display; it is not repaired in the original.')

add('D19','non-Gaussian model',r'''
In this section, we extend our results to a non-Gaussian model $\mathbf Y=\mathbf A+\mathbf E$ where the entries $(\mathbf E_{i,j})$ of $\mathbf E$ are independent, and identically distributed as a sub-Gaussian random variable $E$ satisfying $\mathbb E[E]=0$ and $\operatorname{Var}(E)=1$.
''',[14],'Section 6 — independent sub-Gaussian noise',{'D1':'The additive observation equation is the same, with a replacement noise law.','D20':'The scalar noise law is sub-Gaussian with the norm named in the following sentence.'},kind='condition',symbols=[r'\mathbb E[E]=0',r'\operatorname{Var}(E)=1'],shape='Independent identically distributed centered unit-variance sub-Gaussian entries. E is a scalar noise variable, distinct from the bold noise matrix. Gaussian moments beyond order two and rotational invariance are not assumed.')

add('D20','sub-Gaussian norm',r'''
In the sequel, we write $\|E\|_{\psi_2}$ for its sub-Gaussian norm – see e.g. [39] for a definition.
''',[14],'Section 6 — sub-Gaussian norm reference',kind='source_passage',symbols=[r'\|E\|_{\psi_2}'],shape='The source names the scalar psi_2 norm but delegates its definition to an external reference. Record the external dependency rather than invent a formula or normalization inside the original passage.')


def main():
    for lid,m in members.items():
        assert all(d in members for d in m['depends_on']),lid
        assert any(s in m['statement_original']+' '+m['local_label'] for s in m['highlight_symbols']+m['highlight_phrases']),lid
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,status='extracted_pending_source_audit',interfaces=interfaces,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,status='extracted_pending_source_audit',members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source passages; full source audit remains pending.')

if __name__=='__main__':main()
