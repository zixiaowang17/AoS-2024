# -*- coding: utf-8 -*-
"""Reproduce this paper's original definitions and source conditions."""
import json
from save_inventory import PID, ROOT, STATEMENTS
interfaces=[];members={}
def add(n,term,s,pages,deps,symbols,description,heading,kind='definition',context=None,context_page=None):
    lid=f'D{n}'
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=[])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original naming context')])]
        kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='definition',type_shape=description,semantic_boundary=description,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))
add(1,'normalized sample matrices',r'''With the normalized vector $\hat x_t(i):=x_t(i)/\sqrt N$ for all $t\in[[k]]$ and $i\in[[N]]$, we can define the following normalized sample matrices,
\[
X:=(\hat x(1),\ldots,\hat x(N)),\qquad X_t:=(\hat x_t(1),\ldots,\hat x_t(N)),\qquad t\in[[k]].
\]
(3)''',[3],[],[r'X_t:=(\hat x_t(1),\ldots,\hat x_t(N))',r'\hat x_t(i):=x_t(i)/\sqrt N'],'Block data scaled by square root N. The structural observation model and raw data matrices are retained as auxiliary context. Distribution assumptions are separate and are not embedded in this construction.','Section 1.1 — Normalized sample matrices (3)')
add(2,'sample means',r'''For brevity, we denote by
\[
\hat Y:=(y(1)-\bar y,\ldots,y(N)-\bar y),\qquad\hat Y_i:=(y_t(1)-\bar y_t,\ldots,y_t(N)-\bar y_t),\qquad t\in[[k]],
\]
where $\bar y=\frac1N\sum_{i=1}^Ny(i)$ and $\bar y_t=\frac1N\sum_{i=1}^Ny_t(i)$ are the sample means.''',[2],[],[r'\hat Y_i',r'\bar y_t'],'Sample means and the displayed centered observations. Retain the source i/t mismatch in the centered block symbol. Original raw observations are in auxiliary context.','Section 1.1 — Sample means and centered observations')
add(3,'Sample block correlation matrix (with unknown mean)',r'''For any $k\in\mathbb N$, when the population mean $\mu$ is unknown, the sample block correlation matrix $\hat B:=\hat B(Y_1,\ldots,Y_k)$ is defined as follows,
\[
\hat B:=\operatorname{diag}((\hat Y_t\hat Y_t')^{-1/2})_{t=1}^k\cdot\hat Y\hat Y'\cdot\operatorname{diag}((\hat Y_t\hat Y_t')^{-1/2})_{t=1}^k.
\]''',[2],[2],[r'\hat B:=',r'(\hat Y_t\hat Y_t\')^{-1/2}'.replace('\\\'',"'")],'Unknown-mean block correlation matrix defined from centered observations. Inverses and square roots use the usual positive-definite domain, which the original definition does not spell out separately.','Definition 1.1 (Sample block correlation matrix (with unknown mean))',context='Definition 1.1 (Sample block correlation matrix (with unknown mean)).')
add(4,'random projections',r'''\[
H:=Y'\cdot\operatorname{diag}((Y_tY_t')^{-1})_{t=1}^k\cdot Y=\sum_{t=1}^kY_t'(Y_tY_t')^{-1}Y_t=\sum_{t=1}^kX_t'(X_tX_t')^{-1}X_t=:\sum_{t=1}^kP_t.
\]
(4)
Notice that $H$ is a sum of $k$ random projections, and it does not depend on the unknown $\Sigma_{tt}$'s (or $T_t$'s).''',[3],[1],[r'X_t\'(X_tX_t\')^{-1}X_t'.replace('\\\'',"'"),r'P_t'],'N by N sum of block row-space projections. H and B share nonzero eigenvalues, not necessarily all eigenvalues or traces for functions nonzero at zero. The observation model explains the Y-to-X equality.','Section 1.1 — Random projections (4)')
add(5,'empirical spectral distribution',r'''The empirical spectral distribution (ESD) of $H$ is defined as
\[
\mu_N:=\frac1N\sum_{i=1}^N\delta_{\lambda_i(H)}.
\]
(5)''',[3],[4],[r'\mu_N'],'Empirical measure of all N eigenvalues, including zeros, in the source descending eigenvalue convention.','Section 1.1 — Empirical spectral distribution (5)')
add(6,'Green function',r'''The limiting behaviour of the ESD can often be studied via the Green function of $H$, $G(z):=(H-z)^{-1}$, and its normalized trace, also known as the Stieltjes transform of $H$
\[
m_N(z)=\frac1N\operatorname{Tr}G(z)=\int\frac1{\lambda-z}\mu_N(dz),\qquad z\in\mathbb C^+:=\{w\in\mathbb C:\Im w>0\}.
\]
(6)''',[3],[4,5,7],[r'G(z):=(H-z)^{-1}',r'm_N(z)'],'Resolvent with H-z sign convention and N-normalized trace. Preserve the printed measure differential mu_N(dz), although lambda is the integration symbol.','Section 1.1 — Green function (6)')
add(7,'normalized trace',r'''Hereafter we use $\operatorname{Tr}A$ to denote the trace of a matrix $A$ and use $\operatorname{tr}A:=N^{-1}\operatorname{Tr}A$ to denote the normalized (by $N$) trace for any square matrix $A$, no matter the dimension of $A$ is $N\times N$ or not.''',[4],[],[r'\operatorname{tr}A:=N^{-1}\operatorname{Tr}A'],'All lower-case traces divide by the sample size N, including traces of p_t by p_t block covariance inverses. Upper-case Tr is unnormalized.','Section 1.1 — Trace convention',context=r'and its normalized trace, also known as the Stieltjes transform of $H$',context_page=3)
add(8,'linear spectral statistics',r'''For a test function $f:\mathbb R\to\mathbb R$, the linear spectral statistics (LSS) of $H$ is defined as
\[
\sum_{i=1}^Nf(\lambda_i(H))=\operatorname{Tr}f(H)=N\int f(\lambda)\mu_N(d\lambda).
\]
(7)
Similarly, we can define LSS for any square matrix.''',[4],[5,7],[r'\operatorname{Tr}f(H)',r'\mu_N(d\lambda)'],'The original H-specific formula and its explicitly stated extension to other square matrices. The graph retains H-specific dependencies; the unknown-mean theorem uses its separately archived generic extension, rather than treating H-hat as H.','Definition 1.4 (Linear spectral statistics)')
add(9,'Stieltjes transform',r'''Given a generic probability measure $\mu$ on $\mathbb R$, its Stieltjes transform, $m_\mu$, is defined by $m_\mu(z):=\int_{\mathbb R}(x-z)^{-1}d\mu(x)$, $z\in\mathbb C^+$. We denote by $F_\mu$ the negative reciprocal Stieltjes transform of $\mu$, i.e. $F_\mu(z):=-(m_\mu(z))^{-1}$, $z\in\mathbb C^+$.''',[4],[],[r'm_\mu(z)',r'F_\mu(z)'],'Analytic transform on the upper half-plane with x-z sign, and its negative reciprocal. This is a generic construction for original, tilde and Marchenko-Pastur measures.','Section 1.2 — Stieltjes transform')
add(10,'subordination functions',r'''Given $k$ probability measures $\mu_1,\ldots,\mu_k$ on $\mathbb R$, there exist unique analytic functions, $\omega_1,\ldots,\omega_k:\mathbb C^+\to\mathbb C^+$, such that,

i) for all $z\in\mathbb C^+$, $\Im\omega_1,\Im\omega_2,\ldots,\Im\omega_k\geq\Im z$, and
\[
\lim_{\eta\to\infty}\frac{\omega_t(i\eta)}{i\eta}=1,\qquad t\in[[k]],
\]
(9)
ii) for all $z\in\mathbb C^+$,
\[
F_{\mu_1}(\omega_1(z))=F_{\mu_2}(\omega_2(z))=\cdots=F_{\mu_k}(\omega_k(z)),
\]
(10)
and for all $t\in[[k]]$,
\[
\omega_1(z)+\omega_2(z)+\cdots+\omega_k(z)-z=(k-1)F_{\mu_t}(\omega_t(z)).
\]
(11)''',[4],[9],[r'\omega_1,\ldots,\omega_k',r'\omega_t(i\eta)'],'Generic subordination characterization from Proposition 1.5, with all normalizations and equations. Retained as a source passage rather than falsely labeled Definition or Theorem. The tilde instance in Theorem 1.18 uses Bernoulli parameters p_t/(N-1).','Proposition 1.5',kind='source_passage',context=r'''The functions $\omega_t$'s in Proposition 1.5 are called subordination functions and $m_\boxplus:=-1/F_\boxplus$ is said to be subordinated to $m_{\mu_t}$.''',context_page=5)
add(11,'free additive convolution',r'''It follows from (9) that the analytic function $F_\boxplus:\mathbb C^+\to\mathbb C^+$ defined by
\[
F_\boxplus(z):=F_{\mu_t}(\omega_t(z)),\qquad t\in[[k]],
\]
(12)
satisfies the analogues of (8). Hence, from [1], we know that $F_\boxplus$ is the negative reciprocal Stieltjes transform of a probability measure $\mu_\boxplus$, called the free additive convolution of $\mu_t$'s, usually denoted by $\mu_\boxplus=\mu_1\boxplus\cdots\boxplus\mu_k$. The functions $\omega_t$'s in Proposition 1.5 are called subordination functions and $m_\boxplus:=-1/F_\boxplus$ is said to be subordinated to $m_{\mu_t}$. Apparently, we can also rewrite (12) as
\[
m_\boxplus(z)=m_{\mu_t}(\omega_t(z)),\qquad t\in[[k]].
\]
(13)''',[5],[9,10],[r'\mu_\boxplus',r'F_\boxplus(z)'],'Generic free additive convolution via subordination. Input Bernoulli measures, limiting Bernoulli measures and tilde measures remain separate instances. Equation (8) normalization is retained in auxiliary context.','Section 1.2 — Free additive convolution (12)–(13)')
add(12,'Bernoulli distributions',r'''In (4), observe that $P_t$ is a projection matrix, whose ESD is trivially $\mu_t\equiv\mu_t^N=y_t\delta_1+(1-y_t)\delta_0$ (almost surely), with $y_t:=p_t/N$.''',[4],[4],[r'\mu_t\equiv\mu_t^N',r'y_t:=p_t/N'],'Finite-N ESD of each projection. Theorem 1.9 separately binds the limiting Bernoulli laws; Theorem 1.18 binds different p_t/(N-1) laws, which are not this finite-N member.','Section 1.2 — Bernoulli distributions',context=r'''Heuristically, if we view $P_t$'s as certain random variables in a non-commutative probability space, and regard the ESD $\mu_t$ as the distribution of $P_t$, the random matrix $H$ can be regarded as a sum of $k$ random variables $P_t$ with Bernoulli distributions.''')
add(13,'Assumption on matrix entrices',r'''Assume that $X=(X_{ab})$ in (3) has i.i.d. columns. For its entries, we further impose the following assumptions,

• Under $H_0$, $X_{ab}$'s ($a\in[[p]]$, $b\in[[N]]$) are independent.

• $\mathbb E[X_{ab}]=0$, $\mathbb E[|X_{ab}|^2]=1/N$ for all $a\in[[p]]$ and $b\in[[N]]$.

• For each $\ell\in\mathbb N$, there exists a constant $C_\ell$ such that $\mathbb E[|\sqrt NX_{ab}|^\ell]<C_\ell$ for all $N,a,b$.''',[5],[1],[r'\mathbb E[|\sqrt NX_{ab}|^\ell]',r'X=(X_{ab})'],'All-order uniform entry moments, iid columns, independent entries under H0 and variance 1/N. Entries need not have identical distributions. Preserve the typo in the printed heading; the weaker replacement is a separate assumption.','Assumption 1.6 (Assumption on matrix entrices)',kind='assumption',context='Assumption 1.6 (Assumption on matrix entrices).')
add(14,'Assumption on dimensional parameters',r'''For the dimensional parameters, we impose the following assumptions,

• $\sum_{t=1}^ky_t=:y\to\hat y\in(0,\infty)$ as $N\to\infty$.

• $y_t\to\hat y_t\in[0,1)$, $t=1,\ldots,k$ as $N\to\infty$.

• there exists some small constant $c>0$, such that $y-\max_ty_t\geq c$, for sufficiently large $N$.''',[5],[],[r'y-\max_ty_t\geq c',r'y_t\to\hat y_t'],'Asymptotic dimensional conditions with y_t=p_t/N, allowing growing k and unequal block sizes. Ratios, pmax and N-dependent notation are retained as ambient source conventions; no moment premise is embedded here.','Assumption 1.7 (Assumption on dimensional parameters)',kind='assumption',context='Assumption 1.7 (Assumption on dimensional parameters).')
add(15,'Assumption on matrix entries',r'''Keeping the first two assumptions in Assumption 1.6, and replacing the third assumption with

• $X_{ab}$'s follow continuous distributions, and there exists a constant $\delta>0$ such that $\mathbb E[|\sqrt NX_{ab}|^{4+\delta}]<C$ for all $N,a,b$.''',[9,10],[1],[r'\mathbb E[|\sqrt NX_{ab}|^{4+\delta}]'],'Replacement of the all-order moment bullet by continuity and a uniform 4+delta moment. The first two bullets are reproduced in auxiliary context; no edge to the entire stronger Assumption 1.6 is permitted. The standing iid-column convention remains recorded.','Assumption 1.19 (Assumption on matrix entries)',kind='assumption',context='Assumption 1.19 (Assumption on matrix entries).',context_page=9)
add(16,'contours',r'''For sufficiently small $\epsilon_1>\epsilon_2>0$, and sufficiently large $M_2>M_1>0$, let
\[
\begin{aligned}
C_1\equiv C_1(\epsilon_1,\epsilon_2)&:=\{z:|z|=\epsilon_1,\Im z\geq0,\Re z\geq-\epsilon_2\},\\
C_2\equiv C_2(\epsilon_1,\epsilon_2,M_1)&:=\{z:\Im z=\sqrt{\epsilon_1^2-\epsilon_2^2},-M_1\leq\Re z\leq-\epsilon_2\},\\
C_3\equiv C_3(\epsilon_1,\epsilon_2,M_1,M_2)&:=\{z:\sqrt{\epsilon_1^2-\epsilon_2^2}\leq\Im z\leq M_2,\Re z=-M_1\},\\
C_4\equiv C_4(M_1,M_2)&:=\{z:\Im z=M_2,-M_1\leq\Re z\leq M_1\},\\
C_5\equiv C_5(\epsilon_1,\epsilon_2,M_1,M_2)&:=\{z:\sqrt{\epsilon_1^2-\epsilon_2^2}\leq\Im z\leq M_2,\Re z=M_1\},\\
C_6\equiv C_6(\epsilon_1,\epsilon_2,M_1)&:=\{z:0\leq\Im z\leq\sqrt{\epsilon_1^2-\epsilon_2^2},\Re z=M_1\}.
\end{aligned}
\]
(17)
In summary, the contour for the case of $\hat y\in(0,1)$ is $\gamma^0:=\mathcal C^0\cup\overline{\mathcal C^0}$, where $\mathcal C^0\equiv\mathcal C^0(\epsilon_1,\epsilon_2,M_1,M_2):=\bigcup_{a=1}^6C_a$.

For the other case, we choose the contour $\gamma$ with upper half shown in Fig. 2 and its complex conjugate. Let $C_7=\{z:0\leq\Im z\leq\epsilon_2,\Re z=-M_1\}$. The contour now becomes $\gamma:=\mathcal C\cup\overline{\mathcal C}$, where $\mathcal C\equiv\mathcal C(\epsilon_1,\epsilon_2,M_1,M_2):=\bigcup_{a=3}^7C_a$. With the above configuration, we first define the contour used for the CLT. For sufficiently small $\epsilon_{1i}>\epsilon_{2i}>0$, $i=1,2$ and sufficiently large $M_{2i}>M_{1i}>0$, $i=1,2$, let
\[
\begin{aligned}
\gamma_1^0&:=\gamma(\epsilon_{11},\epsilon_{21},M_{11},M_{21}),&\gamma_2^0&:=\gamma(\epsilon_{12},\epsilon_{22},M_{12},M_{22})\\
\gamma_1&:=\gamma(\epsilon_{11},\epsilon_{21},M_{11},M_{21}),&\gamma_2&:=\gamma(\epsilon_{12},\epsilon_{22},M_{12},M_{22})
\end{aligned}
\]
(18)
be counterclockwise contours. Notice that by choosing sufficiently well separated parameters $\epsilon_{1i}$, $\epsilon_{2i}$, $M_{1i}$ and $M_{2i}$, $i=1,2$, the contours $\gamma_1^0$ ($\gamma_1$) and $\gamma_2^0$ ($\gamma_2$) are nonintersecting. In addition, by choosing $\epsilon_{1i}$, $\epsilon_{2i}$, $M_{1i}$ and $M_{2i}$, $i=1,2$ appropriately, we can always have that $\{m_\boxplus(z):z\in\gamma_1^0\}$ and $\{m_\boxplus(z):z\in\gamma_2^0\}$ are well separated and the same holds if $(\gamma_1^0,\gamma_2^0)$ is replaced by $(\gamma_1,\gamma_2)$ (c.f., Section J in Appendix). Notice that all the contours enclose the set $\operatorname{supp}(\mu_\boxplus)\setminus0$ (c.f., Lemma 4.1).''',[6,7],[11,12],[r'\gamma_1^0',r'\gamma_2^0',r'\gamma_1',r'\gamma_2'],'Both original contour constructions, their orientation, separation and support restrictions. Preserve the missing superscripts on the RHS of (18) and the C7 endpoint inconsistency. No appendix construction was inspected.','Section 1.3 — Contours (17)–(18)')
add(17,'working domains',r'''Recall the definition in (18). Let $\bar\gamma_1^0$ and $\bar\gamma_2^0$ be the parts of $\gamma_1^0$ and $\gamma_2^0$ with $|\Im z|\geq N^{-K}$ for some large (but fixed) $K$, and $\bar\gamma_1$ and $\bar\gamma_2$ are defined analogously.''',[18],[16],[r'\bar\gamma_1^0',r'|\Im z|\geq N^{-K}'],'Contours cut off near the real axis with fixed large K. The bars denote this truncation, not complex conjugation.','Section 4 — Working domains',context='Then we set up our working domains.')
add(18,'expectation operator',r'''Let $\chi(x)$ be a smooth cutoff which equals $0$ when $x>2N^K$ and $1$ when $x<N^K$ for some sufficiently large constant $K>0$ and $|\chi^{(n)}(x)|=O(1)$ for all $n\geq1$. We define for any random variable $\xi$ in the sequel
\[
\mathbb E^\chi(\xi):=\mathbb E(\xi\cdot\Xi)
\]
(22)
where
\[
\Xi:=\prod_{t=1}^k\chi(\operatorname{tr}(X_tX_t')^{-1})\chi(\operatorname{tr}(X_tX_t'))
\]
(23)
is used to control $\|(X_tX_t')^{-1}\|$ and $\|X_tX_t'\|$ crudely but deterministically.''',[17],[1,7],[r'\mathbb E^\chi(\xi)',r'\Xi:='],'Weighted expectation under a smooth product cutoff; not conditional expectation and not normalized by E Xi. Retain all cutoff thresholds and derivative qualifications.','Section 3 — Truncated expectation (22)–(23)',context='Therefore, to facilitate the estimations in our paper, we define the following “truncated” expectation operator.')
add(19,'Marchenko-Pastur law',r'''\[
\mu_{\mathrm{mp},\hat y}:=\frac{\sqrt{([(1+\sqrt{\hat y})^2-x][x-(1-\sqrt{\hat y})^2])_+}}{2x}\,dx+(1-\hat y)_+\delta_0.
\]
(16)''',[6],[],[r'\mu_{\mathrm{mp},\hat y}'],'Original displayed law inside Theorem 1.9, including its printed 2x denominator without pi. Theorem 1.17 uses the corresponding finite-y law; this source ambiguity is recorded, not repaired into a standard probability density. This member extracts the measure definition from the displayed convergence; it imposes no condition on a random matrix.','Theorem 1.9 — Marchenko-Pastur law (16)',kind='theorem_excerpt',context='Cases 2 corresponds to the classical Poisson convergence, and indeed Marchenko-Pastur law is called Free Poisson law in Free Probability Theory.')
add(20,'Sample block correlation matrix (with mean 0)',r'''For any $k\in\mathbb N$, with the population mean $\mu=0$, the sample block correlation matrix $B:=B(Y_1,\ldots,Y_k)$ is defined as follows,
\[
B:=\operatorname{diag}((Y_tY_t')^{-1/2})_{t=1}^k\cdot YY'\cdot\operatorname{diag}((Y_tY_t')^{-1/2})_{t=1}^k.
\]
(2)''',[3],[],[r'B:=',r'\mu=0'],'Known zero-mean matrix. Raw data matrices and the general known-mean subtraction convention are retained as auxiliary context. Theorem 1.20 explicitly retains its Schott/Wilks specializations; Theorem 1.18 substitutes the distinct B-hat construction.','Definition 1.2 (Sample block correlation matrix (with mean 0))',context='Definition 1.2 (Sample block correlation matrix (with mean 0)).')

# Keep the author's generic extension separate from the H-specific instance.
generic=dict(paper_id=PID,local_id='D8g',local_label='Section 1.1 — Extension after Definition 1.4',source_heading='Section 1.1 — Extension after Definition 1.4',source_kind='source_passage',statement_original='Similarly, we can define LSS for any square matrix.',relation='distinct',depends_on=['D7'],evidence=[dict(page=4,location='Sentence immediately after equation (7)')],highlight_symbols=[],highlight_phrases=['LSS'],variant_note='Generic spectral-statistic convention used for H-hat and the Corollary substitutions, kept separate from the H-specific ESD formula.')
members['D8g']=generic
next(x for x in interfaces if x['interface_id']==PID+'/D8')['members'].append(generic)

# Known source wording has no symbol for the prose distinction between assumptions.
for n in [13,14,15]:
    members[f'D{n}']['highlight_phrases']=['Assumption '+{13:'1.6',14:'1.7',15:'1.19'}[n]]
def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    for name,data in [('source-passages.json',dict(paper_id=PID,status='extracted',scope='Original main-text source passages; full source review is a separate gate.',source_passages=list(members.values()))),('interface-extraction.json',dict(paper_id=PID,status='extracted',interfaces=interfaces))]:
        (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(members)} source entries; final validation is separate.')
if __name__=='__main__':main()
