"""Preserve original change-point models, estimators and functional-dependence source passages."""
import json,hashlib
from save_inventory import ROOT,PID,STATEMENTS
REVIEW_ROOT=ROOT
interfaces=[];members={}
def add(n,term,s,pages,deps,symbols,boundary,heading,kind='definition',context=None,context_page=None,phrases=None):
    lid=f'D{n}'
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=s,relation='exact',depends_on=[f'D{i}' for i in deps],evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=symbols,highlight_phrases=phrases or [])
    kw=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if term not in s:
        assert context and term in context,(lid,term)
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=[dict(page=context_page or pages[0],location='Original naming context')])];kw['context_id']=lid+'/name'
    members[lid]=m
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='definition',type_shape=boundary,semantic_boundary=boundary,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))
add(1,'Model for the data',r'''Suppose we are given noisy data of the form
\[
X_t=\mu_t+Z_t,\qquad t=1,\ldots,n,\tag{1}
\]
where $\mu_t$ are means or signals and $(Z_t)_{t\in\mathbb Z}$ is a stationary process with mean $0$, auto-covariance function $\gamma(k)=\operatorname{Cov}(Z_{t+k},Z_t)$, and finite long-run variance
\[
0<\sigma_\infty^2:=\sum_{k=-\infty}^{\infty}\gamma(k)<\infty.\tag{2}
\]''',[3],[2],[r'X_t=\mu_t+Z_t'],'Original deterministic signal plus stationary centered noise model, with positive finite long-run variance. Signals need not be piecewise constant after the change.','Section 2.1 — Model (1)–(2)',kind='source_passage',context='Model for the data and the problems considered.')
add(2,'long-run variance',r'''auto-covariance function $\gamma(k)=\operatorname{Cov}(Z_{t+k},Z_t)$, and finite long-run variance
\[
0<\sigma_\infty^2:=\sum_{k=-\infty}^{\infty}\gamma(k)<\infty.\tag{2}
\]''',[3],[],[r'\sigma_\infty^2',r'\gamma(k)=\operatorname{Cov}(Z_{t+k},Z_t)'],'Original two-sided covariance-sum variance of the stationary centered noise. It is explicitly positive; do not replace it by marginal variance or assume independent observations.','Section 2.1 — Long-run variance (2)',kind='condition')
add(3,'null hypothesis',r'''Consider the following null hypothesis
\[
H_0:\mu_1=\cdots=\mu_n,\tag{3}
\]
where the signal is constant (i. e., all means $\mu_j$ are equal, but not necessarily zero)''',[3],[1],[r'H_0:\mu_1=\cdots=\mu_n'],'Original constant-mean null with unrestricted common level.','Section 2.1 — Null hypothesis (3)',kind='condition')
add(4,'alternative hypothesis',r'''the alternative hypothesis
\[
H_1:\exists\tau\in\{2,\ldots,n\},d>0:\mu_1=\cdots=\mu_{\tau-1},\quad\mu_\tau,\ldots,\mu_n\ge\mu_1+d,\tag{4}
\]
where the signal is constant for the first $\tau-1$ observations and the means from the $\tau$th observation onward may then vary arbitrarily as long as they are larger by at least $d$.''',[3],[1],[r'\mu_\tau,\ldots,\mu_n\ge\mu_1+d',r'\tau\in\{2,\ldots,n\}'],'Original one-sided irregular-signal alternative. Tau indexes the first changed observation; d is a lower gap bound, not necessarily an attained minimum.','Section 2.1 — Alternative hypothesis (4)',kind='condition')
add(5,'consistent estimator',r'''and $\hat\sigma_\infty^2$ is a consistent estimator for the long-run variance $\sigma_\infty^2$, defined in (2).''',[4],[2],[r'\hat\sigma_\infty^2'],'Original generic variance-estimator requirement for the test, also explicitly required by Theorem 3.3. It does not force the optional canonical estimator (8).','Section 2.2 — Variance estimator requirement',kind='condition')
add(6,'Testing procedure',r'''We use the following quantity:
\[
\hat T:=\min_{j=1,2,\ldots,n}\sum_{i=1}^j(X_i-\bar X_n)/(\sqrt n\hat\sigma_\infty),\qquad\text{where }\bar X_n:=\frac1n\sum_{i=1}^nX_i,\tag{5}
\]''',[4],[1,5],[r'\hat T:=\min',r'\bar X_n:=\frac1n\sum_{i=1}^nX_i'],'Original lower-tail minimum CUSUM statistic, using the full-sample mean and a consistent long-run standard deviation estimate. It is not the maximum absolute CUSUM.','Section 2.2 — Testing procedure (5)',context='Testing procedure.')
add(7,'sample means',r'''To reduce the noise from the data and to focus our attention on the signal, we will, here and in the following sections, split the data set into $m:=\lfloor n/k\rfloor$ blocks of size $k$ where $k\to\infty$ and $k/n\to0$. Then we calculate the blocks’ sample means as follows:
\[
R_j:=\frac1k\sum_{i=(j-1)k+1}^{jk}X_i,\qquad j=1,2,\ldots,m.\tag{6}
\]''',[4],[1],[r'R_j:=\frac1k',r'm:=\lfloor n/k\rfloor'],'Original nonoverlapping block means and block-size regime. A final incomplete block is not included in R_1 through R_m.','Section 2.3.1 — Block means (6)')
add(8,'index',r'''From the $R_j$ we then obtain
\[
\hat L:=\operatorname*{argmin}_{i=1,\ldots,m}R_i,\qquad\hat\ell:=k\hat L,\tag{7}
\]
where $\hat L$ indicates an index of a block likely to have all observations in it prior to the change point and $\hat\ell$ points to the last observation in the $\hat L$th block.''',[4],[7],[r'\hat L:=\operatorname*{argmin}',r'\hat\ell:=k\hat L'],'Original minimum-block index and selected prefix endpoint. Tie-breaking is not specified; the later fixed-J alternative is kept separate.','Section 2.3.1 — Preliminary index (7)')
add(9,'preliminary estimate',r'''\[
\hat\mu_0:=\frac1{\hat\ell}\sum_{i=1}^{\hat\ell}X_i,
\]''',[4],[1,8],[r'\hat\mu_0:=\frac1{\hat\ell}'],'Original selected-prefix sample mean, using ell_hat from (7). The initial centering mean is distinct from the later improved muhat_1.','Section 2.3.2 — Preliminary mean in (8)',context='is a preliminary estimate for',context_page=5)
add(10,'overlapping block averages',r'''\[
R_{s/k}:=\frac1k\sum_{i=s-k+1}^sX_i,
\]
where the definition of the overlapping block averages $R_{s/k}$ extends the one for the non-overlapping blocks in (6)''',[4,5],[1,7],[r'R_{s/k}:=\frac1k'],'Original sliding average indexed by s/k, which need not be an integer; its window ends at s.','Section 2.3.2 — Overlapping averages in (8)')
add(11,'Estimate for long-run variance',r'''To estimate the long-run variance, we suggest
\[
\hat\sigma^2:=\frac k{\hat\ell-k+1}\sum_{s=k}^{\hat\ell}(R_{s/k}-\hat\mu_0)^2,\tag{8}
\]''',[4],[2,8,9,10],[r'\hat\sigma^2:=\frac k{\hat\ell-k+1}'],'Original data-selected overlapping-block variance estimator, the specific estimator studied by Theorem 3.2. It is an optional choice in (5) and (9), not automatically required there.','Section 2.3.2 — Variance estimate (8)',context='Estimate for long-run variance.')
add(12,'standard normal distribution',r'''The quantity $z_\alpha$, $\alpha\in(0,1)$, denotes the $\alpha$th-quantile of the standard normal distribution, and $m:=\lfloor n/k\rfloor$, as before.''',[5],[],[r'z_\alpha',r'\alpha\in(0,1)'],'Original normal-quantile convention for blockwise decisions. The choice 1-1/m tends to one; it is not the Brownian-bridge cutoff for the global test.','Section 2.3.3 — Normal quantile')
add(13,'test statistics',r'''\[
\hat D_j:=\sqrt k(R_j-\hat\mu_0)/\hat\sigma_\infty
\]''',[5],[5,7,9],[r'\hat D_j:=\sqrt k'],'Original standardized blockwise statistic using the preliminary mean and any consistent variance estimator.','Section 2.3.3 — Blockwise statistic (9)',context='We then compute ‘test statistics’')
add(14,'test decisions',r'''\[
\hat I_j=\begin{cases}1&\text{if }\hat D_j\ge z_{1-1/m},\\0&\text{otherwise.}\end{cases}\tag{9}
\]''',[5],[7,12,13],[r'\hat I_j=\begin{cases}',r'z_{1-1/m}'],'Original binary decision with an inclusive >= threshold. Requires m>=2 for a finite interior normal quantile.','Section 2.3.3 — Blockwise decision (9)',context='and ‘test decisions’')
add(15,'fitting a step function',r'''\[
\hat\eta:=\operatorname*{argmin}_{t=1,\ldots,m-1}\sum_{j=1}^m(\hat I_j-\mathbf1_{[t+1,m]}(j))^2=\operatorname*{argmin}_{t=1,\ldots,m-1}\left[\sum_{j=1}^t\hat I_j+\sum_{j=t+1}^m(1-\hat I_j)\right].\tag{10}
\]''',[5],[7,14],[r'\hat\eta:=\operatorname*{argmin}',r'\mathbf1_{[t+1,m]}(j)'],'Original binary step-fit estimate of the coarse change block. Its argmin tie convention is unspecified.','Section 2.3.3 — Step fit (10)',context='obtained by fitting a step function',context_page=6)
add(16,'preliminary estimates',r'''\[
\hat\mu_1:=\frac1{k\hat\eta}\sum_{i=1}^{k\hat\eta}X_i,
\]''',[5],[1,7,15],[r'\hat\mu_1:=\frac1{k\hat\eta}'],'Original improved prefix mean using eta_hat, not the initial minimum-block L_hat.','Section 2.3.3 — Improved mean in (11)',context='Finally, we obtain the preliminary estimates')
add(17,'preliminary estimates',r'''\[
\hat d:=\min_{i=k(\hat\eta+1)+1,\ldots,n-k+1}\frac1k\sum_{j=i}^{i+k-1}(X_j-\hat\mu_1).\tag{11}
\]''',[5],[1,7,15,16],[r'\hat d:=\min_{i=k(\hat\eta+1)+1,\ldots,n-k+1}'],'Original sliding-block gap estimate. The source later says it estimates d_star, not necessarily the pointwise lower bound d. No empty-minimum fallback is stated.','Section 2.3.3 — Gap estimate (11)',context='Finally, we obtain the preliminary estimates')
add(18,'Locating Algorithm',r'''In this section we define the novel estimate for the time $\tau$ where the change occurs; cf. (4). Consider
\[
\hat\tau:=\operatorname*{argmin}_{j=2,\ldots,n}\sum_{t=1}^{j-1}(X_t-\hat\mu_1-\rho\hat d),\tag{12}
\]
where $\rho\in(0,1)$ is a tuning parameter.''',[6],[1,16,17],[r'\hat\tau:=\operatorname*{argmin}',r'\rho\in(0,1)'],'Original refined location estimator. The criterion stops at j-1 while j denotes the first changed observation. Rho=1/2 is an optional rule of thumb, not the full theorem domain.','Section 2.3.4 — Locating Algorithm: Step 2 (12)',context='Locating Algorithm: Step 2.')
add(19,'causal stationary process',r'''In this framework, we view the causal stationary process $(Z_t)_{t\in\mathbb Z}$ as outputs from a physical system as follows
\[
Z_t=G(\ldots,\varepsilon_{t-1},\varepsilon_t),\tag{13}
\]
where $(\varepsilon_t)_{t\in\mathbb Z}$, i. i. d., is the input information of this system and $G$ is an $\mathbb R$-valued measurable function that can be thought of as a filter or, intuitively, “mechanism” of this system.''',[6],[],[r'Z_t=G(\ldots,\varepsilon_{t-1},\varepsilon_t)'],'Original causal measurable-function representation driven by IID innovations; the observed noise process itself need not be independent.','Section 3.1 — Causal process (13)',kind='source_passage')
add(20,'functional dependence measure',r'''Then with this system, we measure the dependence from how much the outputs of this system will change if we replace the input information at time $t=0$ with an i. i. d. copy $\varepsilon'_0$. Assume $\mathbb E|Z_i|^\theta<\infty$, $\theta\ge1$. For a single observation at time $i$, we define the functional dependence measure as follows:
\[
\delta_{i,\theta}=(\mathbb E|Z_i-Z_{i,\{0\}}|^\theta)^{1/\theta},\qquad\text{where }Z_{i,\{0\}}=G(\ldots,\varepsilon_{-1},\varepsilon'_0,\varepsilon_1,\ldots,\varepsilon_i).\tag{14}
\]''',[7],[19],[r'\delta_{i,\theta}',r'Z_{i,\{0\}}'],'Original single-innovation coupling at time zero with its Ltheta norm. This is not pairwise covariance or a replacement of the entire past.','Section 3.1 — Functional dependence (14)')
add(21,'cumulative dependence measure',r'''To measure the temporal dependence for the whole time series, we define the cumulative dependence measure of $(Z_i)_{i\ge n}$ on $\varepsilon_0$:
\[
\Theta_{n,\theta}=\sum_{i\ge n}\delta_{i,\theta},\qquad n\ge0.\tag{15}
\]''',[7],[20],[r'\Theta_{n,\theta}',r'\Theta_{0,2}'],'Original future-tail sum of functional dependence measures, with n=0 permitted.','Section 3.1 — Cumulative dependence (15)')
add(22,'Condition 3.1',r'''$(Z_i)_{i\in\mathbb Z}$ satisfies that the $\theta$-th moment $H_\theta:=(\mathbb E|Z_i|^\theta)^{1/\theta}<\infty$, where $\theta>2$. Assume that any one of the following holds
• $\theta>4$ and $\Theta_{n,\theta}=O(n^{-\gamma_\theta}(\log n)^{-A})$, as $n\to\infty$, for $A>2(1/\theta+1+\gamma_\theta)/3$, where
\[
\gamma_\theta=(\theta^2-4+(\theta-2)\sqrt{\theta^2+20\theta+4})/(8\theta);
\]
• $2<\theta\le4$ and $\Theta_{n,\theta}=O(n^{-1}(\log n)^{-A})$, as $n\to\infty$, with $A>3/2$.''',[7],[19,21],[r'H_\theta',r'\gamma_\theta='],'Complete original moment/dependence condition, including both theta regimes and exact logarithmic thresholds. Gamma_theta is an exponent, not the autocovariance gamma(k).','Condition 3.1',kind='condition',context='Condition 3.1.',phrases=['Condition 3.1'])
add(23,'short-range dependence',r'''Assume that the short-range dependence condition holds:
\[
\Theta_{0,2}=\sum_{i\ge0}\delta_{i,2}<\infty.\tag{16}
\]''',[7],[21],[r'\Theta_{0,2}=\sum_{i\ge0}\delta_{i,2}<\infty'],'Original summability condition in Theorem 3.1, weaker than the separate higher-moment Condition 3.1 used for the locating theory.','Theorem 3.1 — Short-range dependence (16)',kind='theorem_excerpt')
add(24,'index of the last block',r'''Denote by $\eta:=\lfloor\tau/k\rfloor$ the index of the last block for which the signal is still constant; i. e., $\eta k+1\le\tau\le(\eta+1)k$, where $\tau$ is the index of the change; cf. the alternative hypothesis (4) considered.''',[5],[4,7],[r'\eta:=\lfloor\tau/k\rfloor'],'Original floor definition and its printed accompanying interval. The two conflict when tau is an exact multiple of k; retain the source wording and record that boundary issue.','Section 2.3.3 — True block index')
add(25,'quantities',r'''In the statement of the proof we write $a_n\ll b_n$ or $b_n\gg a_n$ to mean that $a_n=o(b_n)$, as $n\to\infty$. The quantities $d=d_n$ and $\tau=\tau_n$ are the ones from (4), which we allow to depend on $n$ without making this explicit in the notation, and $k$ is the user-chosen block size; cf. Section 2.3.1. Further, $m:=\lfloor n/k\rfloor$ and $\eta:=\lfloor\tau/k\rfloor$, as before.''',[8],[4,7,24],[r'a_n\ll b_n',r'a_n=o(b_n)'],'Original sequence-order and n-dependence convention. These are contextual bindings, not new model hypotheses; meanings of d,tau,k,m,eta are resolved separately.','Section 3.3 — Rate and sequence conventions',kind='source_passage')
add(26,'minimum gap',r'''We provide this bound in terms of the minimum gap to the signal averaged over sliding blocks. More precisely, defining
\[
d_*:=\min_{i=k(\eta+1)+1,\ldots,n-k+1}\frac1k\sum_{j=i}^{i+k-1}(\mu_j-\mu_1),\tag{20}
\]''',[8],[4,7,24],[r'd_*:=\min_{i=k(\eta+1)+1,\ldots,n-k+1}'],'Original minimum sliding-block signal gap after the true block index. It is not the same object as the pointwise lower bound d or its noisy estimate d_hat.','Section 3.3 — Minimum averaged gap (20)')
# Source-inspected rendering amendment; see the explicit saved review plan.
members['D6']['highlight_symbols'] = ['\\hat T:=\\min_{j=1,2,\\ldots,n}', '\\bar X_n:=\\frac1n\\sum_{i=1}^nX_i']
members['D8']['highlight_symbols'] = ['\\hat L:=\\operatorname*{argmin}_{i=1,\\ldots,m}', '\\hat\\ell:=k\\hat L']
members['D14']['highlight_symbols'] = ['\\hat I_j=\\begin{cases}1&\\text{if }\\hat D_j\\ge z_{1-1/m},\\\\0&\\text{otherwise.}\\end{cases}', 'z_{1-1/m}']
members['D15']['highlight_symbols'] = ['\\hat\\eta:=\\operatorname*{argmin}_{t=1,\\ldots,m-1}', '(\\hat I_j-\\mathbf1_{[t+1,m]}(j))^2']
members['D18']['highlight_symbols'] = ['\\hat\\tau:=\\operatorname*{argmin}_{j=2,\\ldots,n}', '\\rho\\in(0,1)']

def main():
    r=json.loads((REVIEW_ROOT/'inventory-review.json').read_text());assert r['status']=='complete' and r['source_checked']
    assert hashlib.sha256((ROOT/'theorem-inventory.json').read_bytes()).hexdigest()==r['inventory_sha256']
    assert len(interfaces)==len(members)==26
    for x in interfaces:
        m=x['members'][0];assert set(m['depends_on'])<=set(members)
        assert any(v in m['statement_original']+' '+m['local_label'] for v in m['highlight_symbols']+m['highlight_phrases'])
        for ctx in m.get('naming_context',[]):assert not any(ord(ch)<32 and ch!='\n' for ch in ctx['text'])
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces),indent=2,ensure_ascii=False)+'\n')
    print('Saved 26 original source entries; full review remains pending.')
if __name__=='__main__':main()
