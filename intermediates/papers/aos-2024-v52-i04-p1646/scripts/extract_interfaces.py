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

add('D1','matrix factor model',r'''
To fix ideas, let $\{X_t,t=1,2,...\}$ be a time series of $p_1\times p_2$ matrices. A matrix factor model with common factors can be written as
\[
(X_t)_{p_1\times p_2}=(R)_{p_1\times k_1}(F_t)_{k_1\times k_2}(C')_{k_2\times p_2}+(E_t)_{p_1\times p_2},\quad k_1,k_2>0,\tag{1.1}
\]
where the subscripts represent the row and column dimensions of each matrix. In (1.1), $R$ is a $p_1\times k_1$ matrix of loadings explaining the variations of $X_t$ across the rows, $C$ is a $p_2\times k_2$ matrix of loadings reflecting the differences across the columns of $X_t$, $F_t$ is a matrix of common factors, and $E_t$ is the idiosyncratic component, and we assume that factor numbers $k_1$ and $k_2$ are positive, demonstrating a collaborative dependence between both the cross-row and the cross-column dimensions. The matrix factor structure in (1.1) is also known as a two-way factor structure, and we use the same convention as in He et al. (2021) that
\[
(X_t)_{p_1\times p_2}=
\begin{cases}
(R)_{p_1\times k_1}(F_t)_{k_1\times p_2}+(E_t)_{p_1\times p_2},&k_1>0,\ k_2=0,\\
(F_t)_{p_1\times k_2}(C')_{k_2\times p_2}+(E_t)_{p_1\times p_2},&k_2>0,\ k_1=0,\\
(E_t)_{p_1\times p_2},&k_1=k_2=0,
\end{cases}\tag{1.2}
\]
to indicate that there may be no column common factors (first case), no row common factors (second case) or no factor structure at all (third case).
''',[2],'Section 1 — matrix factor model and zero-factor conventions (1.1)–(1.2)',kind='source_passage',symbols=[r'(X_t)_{p_1\times p_2}',r'k_1=k_2=0'],shape='Matrix-valued factor model with distinct positive, one-way and zero-factor conventions. The one-way cases are not obtained by silently multiplying empty factor matrices in (1.1). Assumptions B1-B4 are supplementary and unresolved.')
add('D2','projected column (row) covariance matrix',r'''
In order to fully make use of the two-way interactive factor structure, we propose studying the spectrum of a projected column (row) covariance matrix, as suggested by Yu et al. (2021). Heuristically, if $C$ is known and satisfies the orthogonality condition $C'C/p_2=I_{k_2}$, the data matrix can be projected into a lower dimensional space by setting $Y_t=X_tC/p_2$. In view of this, we define
\[
\widehat M_1=\frac1m\sum_{t=1}^m\widetilde Y_t\widetilde Y_t',\tag{2.4}
\]
where $\widetilde Y_t=p_2^{-1}X_t\widetilde C$ and $\widetilde C$ is an initial estimator of $C$. As suggested by Yu et al. (2021), the initial estimator can be set as $\widetilde C=\sqrt{p_2}Q$, where the columns of $Q$ are the leading $k_2$ eigenvectors of $M_r$, where $M_r$ is the column “flattened” sample covariance matrices, i.e.,
\[
M_r:=\frac1{Tp_1}\sum_{t=1}^T X_t'X_t=\frac1{Tp_1}\sum_{t=1}^T\sum_{j=1}^{p_1}X_{j\cdot,t}X_{j\cdot,t}'.
\]
Furthermore, if $k_2$ is not known, we can select the leading $\widetilde k$ eigenvectors of $M_r$ with $\widetilde k$ chosen such that $\widetilde k\ge k_2$ (we refer to Section 5 for details on how we choose $\widetilde k$).
''',[6,7],'Section 2 — projected covariance and initial projection estimator',{'D1':'The projection uses the observation matrices and their column loading matrix.'},symbols=[r'\widehat M_1',r'\widetilde C=\sqrt{p_2}Q'],shape='Uncentered projected second moment with window length m. Preserve the printed full-T initial covariance and row-product order; the source does not specify a causal estimator update or eigenvector tie convention here.')
add('D3','eigenvalue',r'''
We monitor for changepoints in the row factor structure of $X_t$ across an interval $m+1\le t\le m+T_m$, with - tidying up the notation - $m+T_m=T$. The monitoring schemes are based on the eigenvalue
\[
\widehat\lambda_{k_1+1,\tau}=\lambda_{k_1+1}\left(\frac1m\sum_{t=\tau+1}^{m+\tau}\widetilde Y_t\widetilde Y_t^\top\right),
\]
where $\widetilde Y_t=p_2^{-1}X_t\widetilde C$.
''',[7],'Section 3 — rolling-window monitoring eigenvalue',{'D2':'The moving-window eigenvalue uses the projected observations and initial projection estimator.','D1':'The monitored index is one beyond the row-factor count in the matrix model.'},symbols=[r'\widehat\lambda_{k_1+1,\tau}'],shape='The (k1+1)-th eigenvalue in decreasing order, computed on observations tau+1,...,m+tau. Monitoring time tau is relative to the training length m; T=m+Tm.')
add('D4','sequence',r'''
Throughout the paper, we often use the following sequence
\[
l_{p_1,p_2,m}=\left(\frac1{p_2}+\frac1m+\frac{p_1}{\sqrt{mp_2}}\right)\left(\ln^2p_1\ln p_2\ln m\right)^{1+\epsilon}.\tag{1.3}
\]
''',[6],'Section 1 — sequence (1.3)',symbols=[r'l_{p_1,p_2,m}'],shape='Deterministic rate sequence. The square root covers m times p2, and the exponent 1+epsilon applies to the whole logarithmic product. This epsilon is the arbitrarily positive rate slack, not automatically the tuning epsilon in (3.14).')
add('D5','column space',r'''
The column space of $R$ does not change during $1\le t\le m$.
''',[7],'Assumption C1',{'D1':'The fixed column space belongs to the row-factor loading matrix R.'},kind='assumption',phrases=['column space'],shape='No change of the row-factor loading space during training. Theorem 3 does not explicitly list C1, although it appears in the section setup.')
add('D6','monitoring',r'''
It holds that $T_m=T_m(m)$ with $\lim_{m\to\infty}T_m=\infty$, and $T_m=\Omega(m^\varsigma)$ with $\varsigma\ge1$.
''',[9],'Assumption C2',kind='assumption',symbols=[r'T_m=\Omega(m^\varsigma)'],context=r'We allow the monitoring $T_m$ to go on for a long time.',shape='Diverging monitoring horizon with at least the stated polynomial lower growth. Keep ordinary Omega here distinct from the explicitly defined almost-sure Omega convention.')
add('D7','row factor space',r'''
A first source of change could be a scenario in which the number of common factors is constant across regimes, but the row factor space spanned by the columns of $R$ switches from one to another after a point in time $t^*$, i.e.,
\[
X_t=
\begin{cases}
RF_{1,t}C'+E_t&\text{for }1\le t\le m+t^*,\\
\widetilde R F_{2,t}C'+E_t&\text{for }t>m+t^*,
\end{cases}\tag{3.7}
\]
where $R=[R_0|R_1]$, $\widetilde R=[R_0|R_2]$, $R_0$ is a $p_1\times(k_1-c_1)$ matrix of loadings which do not undergo a change, and $R_1$ and $R_2$ are $p_1\times c_1$ matrices of loadings which differ before and after the changepoint $t^*$. We would like to point out that, in (3.7) and henceforth, we assume that $C$ does not change merely for simplicity.
''',[8],'Section 3 — fixed-count factor-space change (3.7)',{'D1':'The alternative changes the row loading space in the matrix factor model while retaining its factor count.'},kind='source_passage',symbols=[r'R=[R_0|R_1]',r'\widetilde R=[R_0|R_2]'],shape='Fixed number of row factors with a changed loading space. The break is at calendar time m+t*, not t* alone. No orthogonality or rank conditions from supplementary B assumptions are invented.')
add('D8','common factors',r'''
As a second possible alternative, we consider the scenario whereby a set of common factors appear after the point in time $t^*$, i.e., the column space of $R$ enlarges:
\[
X_t=
\begin{cases}
RF_{a,t}C'+E_t&\text{for }1\le t\le m+t^*,\\
\widetilde R F_tC'+E_t&\text{for }t>m+t^*,
\end{cases}\tag{3.9}
\]
where $\widetilde R=[R|R_3]$, $R_3$ is a $p_1\times c_3$ matrix, $F_t'=[F_{a,t}'|F_{b,t}']$, and $F_{b,t}$ is a $c_3\times k_2$ matrix of new common factors.
''',[8],'Section 3 — additional common factors (3.9)',{'D1':'This alternative enlarges the row factor space of the matrix model.'},kind='source_passage',symbols=[r'\widetilde R=[R|R_3]',"F_t'=[F_{a,t}'|F_{b,t}']"],shape='Additional row factors after calendar time m+t*. This differs from the fixed-count space-change alternative. The unchanged column loading is the section convention; later extensions are not imported.')
add('D9','continuous transformation',r'''
The dichotomous behaviour in (3.13) is the building block of our monitoring schemes, and it can be further enhanced by considering a continuous transformation $g(\cdot)$ such that $\lim_{x\to0}g(x)=0$ and $\lim_{x\to\infty}g(x)=\infty$. Defining
\[
\psi_\tau=g\left(\frac{p_1^{-\delta}\widehat\lambda_{k_1+1,\tau}}{p_1^{-1}\sum_{j=1}^{p_1}\widehat\lambda_{j,\tau}}\right),\tag{3.15}
\]
where $\widehat\lambda_{k_1+1,\tau}$ is normalised by the trace of $\left(\frac1m\sum_{t=\tau+1}^{m+\tau}\widetilde Y_t\widetilde Y_t^\top\right)$; again, other rescaling schemes are possible.
''',[9],'Section 3 — continuous transformation and normalized sequence (3.15)',{'D3':'The transformation uses the moving-window spectrum and its average eigenvalue.'},symbols=[r'\psi_\tau',r'\lim_{x\to0}g(x)=0'],shape='Original passage defines the transformation and its application to the normalized eigenvalue. The denominator is the trace divided by p1. Delta is the separately archived source tuning rule; no unspecified zero-trace convention or monotonicity assumption is added.')
add('D10','new sequence',r'''
Finally, after computing $\psi_\tau$ at each $1\le\tau\le T_m$, we define the new sequence $\{y_\tau,1\le\tau\le T_m\}$ as
\[
y_\tau=z_\tau+\psi_\tau,\tag{3.16}
\]
where $z_\tau\overset{i.i.d.}{\sim}N(0,1)$ for $1\le\tau\le T_m$.
''',[9],'Section 3 — randomized sequence (3.16)',{'D9':'The randomization adds standard normal noise to the transformed eigenvalue.'},symbols=[r'y_\tau=z_\tau+\psi_\tau'],shape='Gaussian randomization around the data-dependent drift. The null drift vanishes asymptotically; y_tau is not exactly centered iid normal at finite sample. The conditional construction is preserved without silently asserting an unstated sampling protocol.')
add('D11','functional form',r'''
In both cases, we will need the following restriction on the functional form of $g(\cdot)$:
\[
\lim_{\min(p_1,T_m)\to\infty}T_mg\left(p_1^{-\delta}l_{p_1,p_2,m}\right)=0.\tag{3.17}
\]
''',[9,10],'Section 3.1 — transformation rate restriction (3.17)',{'D9':'The restriction concerns the same continuous transformation g used to construct psi_tau.','D4':'Its argument contains the source rate sequence (1.3).'},kind='condition',symbols=[r'T_mg\left(p_1^{-\delta}l_{p_1,p_2,m}\right)'],shape='Uniform monitoring-horizon control of the null drift scale. The printed limit uses min(p1,Tm), unlike the min(m,p1,p2) theorem limits. Delta is resolved by the auxiliary original tuning passage.')
add('D12','probability conditional',r'''
Henceforth, we let $P^*$ denote the probability conditional on $\{X_t,1\le t\le T\}$; we use “$\xrightarrow{P^*}$”, and “$\xrightarrow{D^*}$” to denote convergence in probability and in distribution according to $P^*$, respectively.
''',[10],'Section 3.1 — conditional probability and convergence',{'D1':'The conditioning data are the complete observed matrix time series.'},symbols=[r'P^*',r'\xrightarrow{D^*}'],shape='Conditional inference given the original observations, with almost-all-data-realizations qualification in every theorem. Do not replace conditional probability by the original data law.')
add('D13','partial sums process',r'''
In particular, recall the definition of $y_\tau$ in (3.16), and consider the partial sums process
\[
S_\tau=\sum_{j=1}^\tau y_j.\tag{3.18}
\]
''',[10],'Section 3.1.1 — partial sums (3.18)',{'D10':'The partial sums accumulate the randomized observations.'},symbols=[r'S_\tau=\sum_{j=1}^\tau y_j'],shape='Uncentered partial sum of the randomized sequence; not a Brownian bridge or a demeaned CUSUM.')
add('D14','weighted functionals',r'''
(i) the weighted functionals
\[
T_m^{\eta-1/2}\max_{1\le\tau\le T_m}\frac{|S_\tau|}{\tau^\eta},\tag{3.19}
\]
for $0\le\eta<1/2$;
''',[10],'Section 3.1.1 — weighted functionals (3.19)',{'D13':'The statistic is a weighted maximum of absolute partial sums.'},symbols=[r'T_m^{\eta-1/2}',r'0\le\eta<1/2'],shape='Monitoring-normalized maximum for eta strictly below one half. Eta=one half and trimmed eta-above-one-half regimes are separate source definitions.')
add('D15','standardised partial sums',r'''
(ii) the standardised partial sums
\[
\max_{1\le\tau\le T_m}\frac{|S_\tau|}{\tau^{1/2}};\tag{3.20}
\]
''',[10],'Section 3.1.1 — standardised partial sums (3.20)',{'D13':'The standardization divides each absolute partial sum by the square root of its time index.'},symbols=[r'\max_{1\le\tau\le T_m}\frac{|S_\tau|}{\tau^{1/2}}'],shape='Borderline eta=one-half maximum. The separate alpha_Tm and beta_Tm normalizers are archived as an auxiliary original passage.')
add('D16','Rényi statistics',r'''
(iii) the Rényi statistics (see Horváth et al., 2020)
\[
r_{T_m}^{\eta-1/2}\max_{r_{T_m}\le\tau\le T_m}\frac{|S_\tau|}{\tau^\eta},\tag{3.21}
\]
for $\eta>1/2$, where $r_{T_m}$ is a sequence such that, as $T_m\to\infty$,
\[
r_{T_m}\to\infty\quad\text{and}\quad\frac{r_{T_m}}{T_m}\to0.
\]
''',[10],'Section 3.1.1 — Rényi statistics and trimming (3.21)',{'D13':'The trimmed statistic uses absolute partial sums starting from r_Tm.'},symbols=[r'r_{T_m}^{\eta-1/2}',r'\frac{r_{T_m}}{T_m}\to0'],shape='Eta greater than one half with a diverging but negligible fraction of initial monitoring times omitted. The normalization is r_Tm^(eta-1/2), not Tm^(eta-1/2).')
add('D17','worst-case scenario',r'''
These features (independence and Gaussianity) allow to propose a completely different monitoring scheme based on
\[
Z_{T_m}=\max_{1\le\tau\le T_m}y_\tau.\tag{3.31}
\]
''',[13],'Section 3.1.2 — worst-case maximum (3.31)',{'D10':'The maximum is over individual randomized observations, not over partial sums.'},symbols=[r'Z_{T_m}=\max_{1\le\tau\le T_m}y_\tau'],context='Monitoring schemes based on worst-case scenario',shape='One-sided maximum without absolute values. The surrounding iid-Gaussian description is heuristic under the null; the actual observations contain the data-dependent drift.')
add('D18','norming sequences',r'''
In order to study the asymptotics of $Z_{T_m}$, we define the norming sequences
\[
a_{T_m}=\frac{b_{T_m}}{1+b_{T_m}^2},\qquad b_{T_m}=\sqrt{2\ln T_m}-\frac{\ln\ln T_m+\ln(4\pi)}{2\sqrt{2\ln T_m}},
\]
which are proposed in Gasull et al. (2015).
''',[13],'Section 3.1.2 — maximum-statistic norming sequences',symbols=[r'a_{T_m}=\frac{b_{T_m}}{1+b_{T_m}^2}',r'b_{T_m}=\sqrt{2\ln T_m}'],shape='Centering b and scale a for the raw maximum statistic. They differ from the iterated-log alpha,beta normalization for standardized partial sums. Expressions are interpreted for sufficiently large Tm.')

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edges=edges),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} original source interfaces; full census review pending.')
if __name__=='__main__':main()
