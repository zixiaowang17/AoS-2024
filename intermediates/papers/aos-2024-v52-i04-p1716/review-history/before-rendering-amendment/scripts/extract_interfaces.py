"""Reproduce manually reviewed original main-text definitions and conditions.

Each source passage remains separate from its interpretation and naming context.
"""
import json
from pathlib import Path
from save_inventory import PID, ROOT
interfaces=[];members={}
def add(n,term,s,pages,kind,deps,symbols,description,context=None,context_page=None,heading=None):
    lid=f'D{n}';heading=heading or f'Section {2 if min(pages)<=5 else 3 if min(pages)<=8 else 4} — {term}'
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=[])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context,(lid,term)
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original source naming context for '+lid)])];kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='hypothesis' if kind in ['assumption','condition'] else 'definition',type_shape=description,semantic_boundary=description,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))
add(1,'Hilbert space',r'''Throughout the paper, we let $\mathcal H$ be the Hilbert space defined as a set of measurable functions $f(\cdot)$ on a bounded set $\mathbb C$ such that $\int_{\mathbb C}f^2(u)du<\infty$. The inner product in $\mathcal H$ is defined as $\langle f_1,f_2\rangle=\int_{\mathbb C}f_1(u)f_2(u)du$. For $f\in\mathcal H$, we define the $L_2$-norm $\|f\|:=\|f\|_2=\langle f,f\rangle^{1/2}=[\int_{\mathbb C}|f(u)|^2du]^{1/2}$ and more generally the $L_p$-norm $\|f\|_p=[\int_{\mathbb C}|f(u)|^pdu]^{1/p}$, $p\geq1$.''',[4],'definition',[],[r'\mathcal H',r'\|f\|',r'\|\delta_i\|'],'The source real function space, inner product and integral norms. Identification modulo almost-everywhere equality and finiteness for p>2 are not specified in this passage.',heading='Section 1 — Hilbert space and norms')
add(2,'continuous linear operators',r'''Let $\mathcal L(\mathcal H)$ be the space of continuous linear operators from $\mathcal H$ to $\mathcal H$ equipped with the operation norm defined by $\|L\|_O=\sup_{f\in\mathcal H}\{\|L(f)\|:\|f\|\leq1\}$. For each $L\in\mathcal L(\mathcal H)$, its adjoint $L'$ is defined via $\langle Lf_1,f_2\rangle=\langle f_1,L'f_2\rangle$ for any $f_1,f_2\in\mathcal H$.''',[4],'definition',[1],[r'\mathcal L(\mathcal H)',r'\|L\|_O'],'Bounded real-linear maps on the source Hilbert space, their operator norm and adjoint; the printed phrase operation norm is retained.',heading='Section 1 — Continuous linear operators')
add(3,'model',r'''Suppose that we collect a sequence of functional observations $X_t=(X_{1t},\cdots,X_{Nt})^\top$, $t=1,\cdots,T$, where $X_{it}=(X_{it}(u):u\in\mathbb C)$. For the $i$-th subject, $X_{it}$, $t=1,\cdots,T$, are generated from the following model with a possible break in the mean function:
\[
X_{it}=\mu_i+\delta_i I(t>\tau_i)+\epsilon_{it},
\]
(2.1)
where $\mu_i=(\mu_i(u):u\in\mathbb C)$ is the pre-break mean function, $\delta_i=(\delta_i(u):u\in\mathbb C)$ is the jump function, $\tau_i$ is the break point, $I(\cdot)$ is the indicator function and $\epsilon_{it}=(\epsilon_{it}(u):u\in\mathbb C)$ is stationary over the temporal dimension. The unknown functional components $\mu_i$ and $\delta_i$ as well as the break points $\tau_i$ are allowed to vary over $i$, reflecting heterogeneity of functional time series over subjects.''',[4],'source_passage',[1],[r'X_{it}',r'\delta_i',r'\tau_i'],'Subject-specific one-break mean functions with temporally stationary error, all in the standing function-space setting. Cross-subject independence is not part of this model passage.')
add(4,'functional linear process',r'''(i) Let
\[
\epsilon_{it}=\sum_{j=0}^{\infty}A_{ij}\eta_{i,t-j},
\]
(2.3)
where $\eta_{it}=(\eta_{it}(u):u\in\mathbb C)$ are i.i.d. random elements in $\mathcal H$ with mean zero and positive definite covariance function $\Omega_i(u,v)$, $u,v\in\mathbb C$, and $A_{ij}$ are continuous linear operators with the operator norm satisfying
\[
\sum_{j=0}^{\infty}j\left(\max_{1\leq i\leq N}\|A_{ij}\|_O\right)<C_A,
\]
(2.4)
where $C_A$ is a positive constant which does not depend on $N$.''',[5],'assumption',[1,2],[r'\eta_{it}',r'A_{ij}',r'C_A'],'Assumption 1(i) specifies the source linear process and uniform weighted operator summability. The iid convention is temporal for each subject, since cross-subject dependence is allowed separately.',context=r'''From Assumption 1(i), the functional linear process $\epsilon_{it}$ defined in (2.3) with coefficient operators satisfying (2.4) is stationary and short-range dependent over time $t$, but its distribution is allowed to vary over $i$.''',heading='Assumption 1(i)')
add(5,'positive definite integral operator',r'''(ii) Let
\[
\widetilde\eta_{Nt}=\frac{1}{\sqrt N}\sum_{i=1}^N A_i\eta_{is},\qquad A_i=\sum_{j=0}^{\infty}A_{ij}.
\]
There exists a positive definite integral operator $\widetilde\Omega$ with the kernel satisfying
\[
\widetilde\Omega(u,v)=\lim_{N\to\infty}E[\widetilde\eta_{Nt}(u)\widetilde\eta_{Nt}(v)].
\]
(2.5)
Furthermore, for any $i$, $E[\exp\{c_\eta\|\eta_{it}\|^2\}]<\infty$ with $c_\eta$ being a positive and bounded constant, and for any sequence of continuous linear operators $B_i$,
\[
E\left[\left\|\frac{1}{\sqrt N}\sum_{i=1}^N B_i\eta_{it}\right\|_O^{2+\iota}\right]=O\left(\max_{1\leq i\leq N}\|B_i\|_O^{2+\iota}\right),\quad0\leq\iota\leq1.
\]
(2.6)''',[5],'assumption',[4,2,1],[r'\widetilde\Omega',r'\widetilde\eta_{Nt}',r'\eta_{it}'],'Assumption 1(ii), including the limiting covariance kernel, exponential moment and operator-weighted cross-sectional moment restriction. Printed eta_is and the O norm on a random element are preserved as unresolved source notation.',heading='Assumption 1(ii)')
add(6,'eigenvalues',r'''As $\widetilde\Omega$ is positive definite, we may conduct an eigenanalysis and find pairs of non-negative eigenvalues and eigenvectors $(\lambda_k,\psi_k)$ (with eigenvalues arranged in an non-increasing order), $k=1,2,\cdots$, such that
\[
\widetilde\Omega(\psi_k)(u)=\lambda_k\psi_k(u).
\]
(2.7)''',[5,6],'definition',[5],[r'\lambda_k',r'\lambda_i',r'\widetilde\Omega'],'The source eigenpairs and their ordering for the limiting operator. Spectral existence, trace summability and normalization conventions are not proved by this definition.')
add(7,'hypothesis testing problem',r'''Our primary interest lies in the following hypothesis testing problem:
\[
H_0:\delta_i=0,\ i=1,\cdots,N,\qquad\text{versus}\qquad H_A:\delta_i\ne0\text{ for some }i.
\]
(2.2)''',[4],'condition',[3],[r'H_0',r'H_A'],'The null of no subject-level jump and the alternative of at least one nonzero functional jump.')
add(8,'model formulation',r'''Letting $\nu_{it}=\mu_i+\delta_i I(t>\tau_i)$, we may re-write model (2.1) as
\[
X_{it}=\nu_{it}+\epsilon_{it},\quad t=1,\cdots,T,\ i=1,\cdots,N.
\]
(3.1)
Define
\[
\widetilde X_t=\frac1N\sum_{i=1}^N X_{it},\quad\widetilde\nu_t=\frac1N\sum_{i=1}^N\nu_{it}\quad\text{and}\quad\widetilde\epsilon_t=\frac1N\sum_{i=1}^N\epsilon_{it},
\]
where we suppress their dependence on $N$. From the model formulation (3.1), we have
\[
\widetilde X_t=\widetilde\nu_t+\widetilde\epsilon_t,\quad t=1,\cdots,T.
\]
(3.2)''',[6],'definition',[3],[r'\widetilde X_t',r'\widetilde\nu_t'],'The mean path and cross-subject averages used to define the aggregated functional CUSUM and alternative region.')
add(9,'functional CUSUM statistic',r'''Define the functional CUSUM statistic as
\[
\widetilde Z_{NT}(x;u)=\sqrt{N/T}\left(\widetilde S_{NT}(x;u)-\frac{\lfloor Tx\rfloor}{T}\widetilde S_{NT}(1;u)\right)\quad\text{with}\quad\widetilde S_{NT}(x;u)=\sum_{s=1}^{\lfloor Tx\rfloor}\widetilde X_s(u),
\]
(3.3)
where $0\leq x\leq1$, $u\in\mathbb C$ and $\lfloor\cdot\rfloor$ denotes the floor function, and subsequently construct the test statistic via
\[
Z_{NT}=\sup_{0\leq x\leq1}\int_{\mathbb C}\widetilde Z_{NT}^2(x;u)du=\max_{1\leq t\leq T}\int_{\mathbb C}\widetilde Z_{NT}^2(t/T;u)du.
\]
(3.4)''',[6],'definition',[8,1],[r'\widetilde Z_{NT}',r'Z_{NT}'],'Aggregated centered partial sums normalized by sqrt(N/T), followed by the supremum integrated square. Floor-centering is preserved.')
add(10,'subject-specific functional CUSUM statistic',r'''Define the subject-specific functional CUSUM statistic:
\[
Z_{iT}(x;u)=\frac1{\sqrt T}\left[S_{iT}(x;u)-\frac{\lfloor Tx\rfloor}{T}S_{iT}(1;u)\right]\quad\text{with}\quad S_{iT}(x;u)=\sum_{s=1}^{\lfloor Tx\rfloor}X_{is}(u),
\]
(3.5)''',[7],'definition',[3,1],[r'Z_{iT}',r'S_{iT}'],'Subject-level CUSUM, with the same standing x and u domains and floor convention as (3.3).')
add(11,'high-criticism threshold',r'''Throughout this paper we set the threshold as $\xi_{NT}=c_\xi\ln(N\vee T)\ln\ln(N\vee T)$ with $c_\xi$ being a user-specified positive constant.''',[7],'definition',[],[r'\xi_{NT}'],'The prescribed max-based logarithmic threshold. The simulation-only NT alternative is retained separately as auxiliary context.',context=r'''where $\xi_{NT}$ denotes a high-criticism threshold and $a\vee b=\max\{a,b\}$.''')
add(12,'PE component',r'''and the PE component:
\[
Z_{NT}^\diamond=\sqrt{N\vee T}\sum_{i=1}^N I\left(\sup_{0\leq x\leq1}\int_{\mathbb C}Z_{iT}^2(x;u)du>\xi_{NT}\right),
\]
(3.6)''',[7],'definition',[10,11],[r'Z_{NT}^\diamond'],'A diverging factor times the count of subjects whose squared CUSUM exceeds the threshold strictly.')
add(13,'power enhanced CUSUM (PE-CUSUM) test statistic',r'''Combining the CUSUM test statistic $Z_{NT}$ defined in (3.4) and the PE component $Z_{NT}^\diamond$ defined in (3.6), we propose the following power enhanced CUSUM (PE-CUSUM) test statistic:
\[
\widehat Z_{NT}=Z_{NT}+Z_{NT}^\diamond.
\]
(3.7)''',[8],'definition',[9,12],[r'\widehat Z_{NT}'],'The sum of the aggregated CUSUM test and its nonnegative power-enhancement component.')
add(14,'alternative',r'''Let $H_A^\diamond$ be the alternative $H_A$ defined in (2.2) with $\delta_i$ satisfying
\[
\max_{1\leq i\leq N}\frac{T\omega_{Ti}^2\|\delta_i\|^2}{\xi_{NT}}\to\infty,\quad\omega_{Ti}=(\tau_i/T)\wedge(1-\tau_i/T),
\]
(3.8)
and $\widetilde H_A^\diamond$ the alternative $H_A$ with $\delta_i$ satisfying (3.8) or $\widetilde\nu_t$ defined in (3.2) satisfying
\[
\sup_{0\leq x\leq1}\int_{\mathbb C}\nu_{NT}^2(x,u)du\to\infty\quad\text{with}\quad\nu_{NT}(x,u)=\frac1{\sqrt T}\left[\sum_{s=1}^{\lfloor Tx\rfloor}\widetilde\nu_s(u)-x\sum_{s=1}^T\widetilde\nu_s(u)\right].
\]
(3.9)''',[8],'condition',[7,8,11,1],[r'H_A^\diamond',r'\widetilde H_A^\diamond'],'Two explicitly distinct nested alternative regions, with a maximum signal condition versus its union with a deterministic mean-path condition. The omega definition alone is retained as auxiliary context for Theorem 2.')
add(15,'index set',r'''Hence, we may split the index set $\{1,2,\cdots,N\}$ into
\[
\mathcal C_\bullet=\{1\leq i\leq N:\delta_i\ne0\}\quad\text{and}\quad\mathcal C_\circ=\{1\leq i\leq N:\delta_i=0\},
\]
the index set with structural breaks in mean functions and that without breaks.''',[9],'definition',[3],[r'\mathcal C_\bullet',r'\mathcal C_\circ'],'The true partition into subjects with a nonzero jump and subjects without a jump.')
add(16,'estimates',r'''It is natural to estimate $\mathcal C_\bullet$ and $\mathcal C_\circ$ by
\[
\widehat{\mathcal C}_\bullet=\left\{1\leq i\leq N:\sup_{0\leq x\leq1}\int_{\mathbb C}Z_{iT}^2(x;u)du\geq\xi_{NT}\right\}
\]
and
\[
\widehat{\mathcal C}_\circ=\left\{1\leq i\leq N:\sup_{0\leq x\leq1}\int_{\mathbb C}Z_{iT}^2(x;u)du<\xi_{NT}\right\},
\]
respectively, where $Z_{iT}(x;u)$ and $\xi_{NT}$ are defined in Section 3.''',[9],'definition',[10,11],[r'\widehat{\mathcal C}_\bullet',r'\widehat{\mathcal C}_\circ'],'The data-defined partition uses >= for the detected set and < for its complement, unlike the strict PE count. Its definition does not require knowledge of the true partition.',context=r'''The following theorem shows that $\widehat{\mathcal C}_\bullet$ and $\widehat{\mathcal C}_\circ$ are consistent estimates and provides a uniform approximation rate for $\widehat\tau_i$ over $i\in\mathcal C_\bullet$.''',context_page=10)
add(17,'break points',r'''Subsequently, we estimate the (heterogeneous) break points $\tau_i$ by
\[
\widehat\tau_i=\arg\max_{1\leq t\leq T}\int_{\mathbb C}Z_{iT}^2(t/T;u)du,\quad i\in\widehat{\mathcal C}_\bullet.
\]
(4.1)''',[9],'definition',[10,16],[r'\widehat\tau_i'],'Per-detected-subject maximizer of the integrated squared CUSUM. The source does not specify a tie rule or extension to missed true subjects.')
add(18,'partition',r'''Assume that there exists a partition of $\mathcal C_\bullet$, denoted by $\mathcal C(b_1),\cdots,\mathcal C(b_{K_0})$, such that
\[
\tau_i=b_k\ \forall i\in\mathcal C(b_k),\quad\mathcal C(b_{k_1})\cap\mathcal C(b_{k_2})=\varnothing\text{ for }k_1\ne k_2,\quad\cup_{k=1}^{K_0}\mathcal C(b_k)=\mathcal C_\bullet,
\]
(4.6)
where $b_1<b_2<\cdots<b_{K_0}$ are $K_0$ distinct break points. Neither the group membership nor the number $K_0$ is known.''',[10],'assumption',[15,3],[r'\mathcal C(b_k)',r'K_0',r'b_k'],'The latent partition groups true broken subjects by a common break location; distinct locations are ordered. Nonempty parts and admissible integer locations are conventional, not additional source formulas.',heading='Section 4 — Latent structure (4.6)')
add(19,'estimated clusters',r'''With the estimated break points $\widehat\tau_i$ defined in (4.1), $i\in\widehat{\mathcal C}_\bullet$, we first sort them from minimum to maximum and denote the ordered points as $\widehat\tau^{(1)},\cdots,\widehat\tau^{(n)}$, $n=|\widehat{\mathcal C}_\bullet|$, where $|A|$ denotes the cardinality of set $A$. Then calculate the jumps:
\[
\Delta_i(\widehat\tau)=\widehat\tau^{(i+1)}-\widehat\tau^{(i)},\quad i=1,\cdots,n-1.
\]
If the number of distinct break points is assumed to be $K$, define $\overline\tau_j=\widehat\tau^{(i+1)}$ with $\Delta_i(\widehat\tau)$ being the $j$-th largest jump, $1\leq j\leq K-1$. Then we sort $\overline\tau_1,\cdots,\overline\tau_{K-1}$ from minimum to maximum, denote them as $\overline\tau_K^{(1)},\cdots,\overline\tau_K^{(K-1)}$, and obtain the estimated clusters as
\[
\widehat{\mathcal C}(k|K)=\{i\in\widehat{\mathcal C}_\bullet:\overline\tau_K^{(k-1)}\leq\widehat\tau_i<\overline\tau_K^{(k)}\},\quad k=1,\cdots,K,
\]
(4.7)
where, without loss of generality, $\overline\tau_K^{(0)}=1$ and $\overline\tau_K^{(K)}=T$.''',[10,11],'definition',[17,16],[r'\widehat{\mathcal C}(k|K)',r'\Delta_i(\widehat\tau)'],'Largest-gap clustering of the estimated break locations, with half-open intervals. Ties, feasibility of K and endpoint exclusions remain source issues.')
add(21,'penalised objective function',r'''Given the cluster number $K$, we compute
\[
\widehat\tau_{k|K}=\frac1{|\widehat{\mathcal C}(k|K)|}\sum_{i\in\widehat{\mathcal C}(k|K)}\widehat\tau_i,\qquad\widehat\nu_{it,k|K}=\widehat\mu_{i,k|K}+\widehat\delta_{i,k|K}I(t>\widehat\tau_{k|K})
\]
(4.8)
with
\[
\widehat\mu_{i,k|K}=\frac1{\widehat\tau_{k|K}}\sum_{t=1}^{\widehat\tau_{k|K}}X_{it}\quad\text{and}\quad\widehat\delta_{i,k|K}=\frac1{T-\widehat\tau_{k|K}}\sum_{t=\widehat\tau_{k|K}+1}^T X_{it}-\frac1{\widehat\tau_{k|K}}\sum_{t=1}^{\widehat\tau_{k|K}}X_{it}.
\]
Construct the penalised objective function:
\[
IC(K)=\ln(V(K))+K\rho_{NT},
\]
(4.9)
where $\rho_{NT}$ is a user-specified tuning parameter satisfying some restrictions, see Assumption 2(iii) below, and
\[
V(K)=\frac1{|\widehat{\mathcal C}_\bullet|}\sum_{k=1}^K\sum_{i\in\widehat{\mathcal C}(k|K)}\frac1T\sum_{t=1}^T\|X_{it}-\widehat\nu_{it,k|K}\|^2.
\]
The true cluster number $K_0$ is determined by
\[
\widehat K=\arg\min_{1\leq K\leq\overline K}IC(K),
\]
(4.10)
where $\overline K$ is a pre-specified upper bound of the cluster number. Replacing $K$ by $\widehat K$ in (4.7), we obtain
\[
\widehat{\mathcal C}(b_k)=\widehat{\mathcal C}(k|\widehat K),\quad k=1,\cdots,\widehat K.
\]''',[11],'definition',[19,17,3,16,1,24],[r'IC(K)',r'\widehat K',r'\widehat{\mathcal C}(b_k)'],'Cluster-average break location, fitted means, penalized residual criterion, selected group count and relabeled estimated groups. Noninteger average break locations remain in summation limits as printed. The definition explicitly refers to Assumption 2(iii) for its tuning sequence; this is a construction dependency, not an import of Theorem 3.')
add(22,'cluster-specific break points',r'''(i) The cluster-specific break points satisfy that $b_k=c_kT$ with $0<c_1<\cdots<c_{K_0}<1$, and the latent cluster size satisfies that $|\mathcal C(b_k)|=d_k|\mathcal C_\bullet|$ with $d_k>0$ and $\sum_{k=1}^{K_0}d_k=1$.''',[11],'assumption',[18,15],[r'b_k=c_kT',r'|\mathcal C(b_k)|'],'Separated proportional break locations and proportional latent-group sizes. This part is cited alone in Theorem 4.',heading='Assumption 2(i)')
add(23,'mild restrictions',r'''(ii) Let $\|\mu_i\|$ and $\|\delta_i\|$ be bounded uniformly over $i$ and $\min_{i\in\mathcal C_\bullet}\|\delta_i\|$ be bounded away from zero.''',[11],'assumption',[1,3,15],[r'\|\mu_i\|',r'\|\delta_i\|'],'Uniform upper bounds on mean and jump norms, and a positive lower bound on true jump norms. Only Theorem 3 explicitly assumes this part.',context=r'''Assumption 2(ii) imposes some mild restrictions on sizes of $\|\mu_i\|$ and $\|\delta_i\|$.''',context_page=12,heading='Assumption 2(ii)')
add(24,'tuning parameter',r'''(iii) Let $\rho_{NT}$ satisfy $\rho_{NT}\to0$ and $T\rho_{NT}/[\ln(N\vee T)]^{1+\zeta}\to\infty$ for any $\zeta>0$.''',[11],'assumption',[],[r'\rho_{NT}'],'The vanishing but sufficiently large penalty sequence. The quantifier is for any positive zeta, as printed.',context=r'''Finally, Assumption 2(iii) is a crucial condition on the tuning parameter in the penalty term, ensuring that the information criterion can consistently select $K_0$.''',context_page=12,heading='Assumption 2(iii)')
add(25,'CUSUM quantities',r'''As $X_{it}$, $i\in\mathcal C(b_k)$, $t=1,\cdots,T$, have a common break point, it is sensible to estimate $b_k$ more efficiently by pooling the CUSUM quantities over the subjects in $\widehat{\mathcal C}(b_k)$, i.e.,
\[
\widehat b_k=\arg\max_{1\leq t\leq T}\sum_{i\in\widehat{\mathcal C}(b_k)}\int_{\mathbb C}Z_{iT}^2(t/T;u)du,
\]
(4.13)''',[12],'definition',[21,10],[r'\widehat b_k'],'Pooled squared-CUSUM maximizer over an estimated group. It uses the selected groups, not an oracle replacement by true groups; tie and exceptional-event conventions are unspecified.')
def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
    write('source-passages.json',dict(paper_id=PID,source_passages=list(members.values())))
    write('interface-extraction.json',dict(paper_id=PID,interfaces=interfaces))
    print(f'Saved {len(members)} original source passages; final dependency review remains separate.')
if __name__=='__main__':main()
