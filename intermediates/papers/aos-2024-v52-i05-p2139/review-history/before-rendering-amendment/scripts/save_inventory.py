"""Reproduce all seven original main-text Theorems of the registered arXiv v3 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2139'
SHA='e76bf0281de05dc5366deaa7a98f870d843e92ad9b9cd69565a0e75006e818d2'
URL='https://arxiv.org/pdf/2301.10600v3'
NUMBERS=['3.3','3.5','4.1','4.2','4.3','4.11','4.12']
STATEMENTS=[r'''Fix $\alpha>0$ and for each $n\in\mathbb N$, let $Q^{(n)}$ be $\alpha$-sequentially-interactive (1.6) from $(\mathcal X^n,\mathcal F^n)$ to $(\mathcal Z^{(n)},\mathcal G^{(n)})$ and assume that all the $\sigma$-fields $\mathcal F$, $\mathcal G_i$, $i=1,\ldots,n$, are countably generated. Suppose the model $\mathcal P=(P_\theta)_{\theta\in\Theta}$ on sample space $(\mathcal X,\mathcal F)$ is DQM at $\theta\in\Theta\subseteq\mathbb R^p$ with score $s_\theta$ and define
\[
\Sigma_{n,\theta}(z_{1:n-1}):=\frac1n\sum_{i=1}^n I_\theta(Q_{z_{1:i-1}}\mathcal P),\qquad z_{1:n-1}=(z_1,\ldots,z_{n-1})\in\mathcal Z^{(n-1)}.
\]
Then $z_{1:i-1}\mapsto I_\theta(Q_{z_{1:i-1}}\mathcal P)$ is measurable and there exists a measurable function $z_{1:i}\mapsto t_{i,\theta}(z_i\mid z_{1:i-1})$ such that for all $z_{1:i-1}\in\mathcal Z^{(i-1)}$, $z\mapsto t_{i,\theta}(z\mid z_{1:i-1})$ is a score in the model $Q_{z_{1:i-1}}\mathcal P$ at $\theta$.
If $\Sigma_{n,\theta}\overset{Q^{(n)}P_\theta^n}{\rightsquigarrow}\Sigma_\theta$ for some random symmetric $p\times p$ matrix $\Sigma_\theta$ and $I_\theta(\mathcal P)\ne0$, then the sequence $\mathcal E_n=(\mathcal Z^{(n)},\mathcal G^{(n)},\{Q^{(n)}P_\theta^n:\theta\in\Theta\})$, $n\in\mathbb N$, is LAMN at $\theta$ with $\delta_n=J_p/\sqrt n$, $\Sigma_{n,\theta}$ as defined above and
\[
\Delta_{n,\theta}(z_{1:n})=\frac1{\sqrt n}\sum_{i=1}^n t_{i,\theta}(z_i\mid z_{1:i-1}).
\]''',r'''Fix $\alpha>0$ and for each $n\in\mathbb N$, let $Q^{(n)}$ be $\alpha$-sequentially-interactive (1.6) from $(\mathcal X^n,\mathcal F^n)$ to $(\mathcal Z^{(n)},\mathcal G^{(n)})$ and assume that all the $\sigma$-fields $\mathcal F$, $\mathcal G_i$, $i=1,\ldots,n$ are countably generated. Suppose the model $\mathcal P=(P_\theta)_{\theta\in\Theta}$ on sample space $(\mathcal X,\mathcal F)$ is DQM at $\theta\in\Theta\subseteq\mathbb R^p$ and let $\Sigma_{n,\theta}$ be defined as in Theorem 3.3. Consider the joint distribution of the sanitized data $R_{n,\theta}:=Q^{(n)}P_\theta^n$ and suppose that for every $n\in\mathbb N$, $R_{n,\theta}(\Sigma_{n,\theta}\text{ is positive definite})=1$ and every weak accumulation point $\Sigma_\theta$ of $(\Sigma_{n,\theta})_{n\in\mathbb N}$ under $R_{n,\theta}$ is almost surely positive definite. Let $\widehat\theta_n:\mathcal Z^{(n)}\to\mathbb R^p$ be an estimator sequence and $D_\theta$ a random $p$-vector, such that
\[
\sqrt n\left(\widehat\theta_n-[\theta+h/\sqrt n]\right)\overset{R_{n,\theta+h/\sqrt n}}{\rightsquigarrow}D_\theta,\qquad\forall h\in\mathbb R^p.
\]
(3.1)
Then the limiting distribution $D_\theta$ admits the representation
\[
P(D_\theta\in A)=\int_{\mathbb R^{p\times p}}[\mathcal N(0,\sigma^{-1})\star L_\theta(\sigma)](A)P_{\Sigma_\theta}(d\sigma),\qquad\forall A\in\mathcal B(\mathbb R^p),
\]
where $P_{\Sigma_\theta}$ is the distribution of any weak accumulation point $\Sigma_\theta$, $\{L_\theta(\sigma):\sigma\in\mathbb R^{p\times p}\}$ is a family of probability distributions on $\mathbb R^p$ possibly depending on $P_{\Sigma_\theta}$ and $\star$ denotes convolution.''',r'''Fix $\theta_0\in\Theta\subseteq\mathbb R^p$. Let $\theta\mapsto\log p_\theta(x)$ be upper-semicontinuous on $\Theta$ for $P_{\theta_0}$ almost all $x\in\mathcal X$ and suppose that for every sufficiently small ball $U\subseteq\Theta$ the function $x\mapsto\sup_{\theta\in U}\log p_\theta(x)$ is measurable and satisfies
\[
\mathbb E_{\theta_0}\left[\sup_{\theta\in U}\log p_\theta\right]<\infty.
\]
If $\theta\mapsto\mathbb E_{\theta_0}[\log p_\theta]$ has a unique maximizer at $\theta_0$, then any estimator $\widehat\theta_n$ that maximizes the log-likelihood $\theta\mapsto\sum_{i=1}^n\log p_\theta(x_i)$ satisfies
\[
P_{\theta_0}^n(\|\widehat\theta_n-\theta_0\|_2>\varepsilon\wedge\widehat\theta_n\in K)\xrightarrow[n\to\infty]{}0,
\]
for every $\varepsilon>0$ and every compact set $K\subseteq\Theta$.''',r'''If $\mathcal P$ is DQM at every $\theta\in\Theta\subseteq\mathbb R^p$ (in particular, $\Theta$ is open) and the channel $Q\in\mathcal Q_\alpha(\mathcal X)$ is such that the model $Q\mathcal P$ is identifiable, then any non-interactive $\alpha$-private MLE satisfies
\[
(QP_{\theta_0})^n(\|\widehat\theta_n-\theta_0\|_2>\varepsilon\wedge\widehat\theta_n\in K)\xrightarrow[n\to\infty]{}0,
\]
for every $\theta_0\in\Theta$, every $\varepsilon>0$ and every compact set $K\subseteq\Theta$.''',r'''Suppose that there exists a measurable function $g:\mathcal X\to G$ with range $G\subseteq\mathbb R^p$, such that the function $f:\Theta\to G$, $f(\theta):=\mathbb E_\theta[g]$ has a continuous inverse $f^{-1}:G\to\Theta$. Generate $Z_i:=\Pi_{\tau_n}[g(X_i)]+\frac{2\tau_n}{\alpha}W_i$, for independent random $p$-vectors $W_i$ with iid standard Laplace components $W_{ij}\sim\operatorname{Lap}(1)$. Then the estimator
\[
\widehat\theta_n=f^{-1}\left(\frac1n\sum_{i=1}^n Z_i\right)
\]
is non-interactive $\alpha$-private. If $\tau_n\to\infty$ and $\tau_n^2/n\to0$ as $n\to\infty$, then it is also consistent.''',r'''Suppose that Conditions (C1), (C2) and (C3) are satisfied with $p=1$ and let $(T_m)_{m\in\mathbb N}$ be a consistent quantizer with associated sequence $(k_m)_{m\in\mathbb N}$ as in Definition 3. Moreover, fix some $Q_0\in\mathcal Q_\alpha(\mathcal X\to\mathcal Z_0)$, $n_1\in\mathbb N$, let $\widetilde\theta_{n_1}:\mathcal Z_0^{n_1}\to\Theta$ be an estimator and write $\widehat T_{n_1}(x):=T_{n_1}(x,\widetilde\theta_{n_1})$ and $\widehat k_{n_1}:=k_{n_1}(\widetilde\theta_{n_1})$. Furthermore, for $\mathcal M_\alpha(k,k)\subseteq\mathbb R^{k\times k}$ as in Lemma 4.5, let $\widehat Q_{n_1}\in\mathcal M_\alpha(\widehat k_{n_1},\widehat k_{n_1})$ be a measurable maximizer (in the sense of Lemma 4.6) of
\[
\max_{Q\in\mathcal M_\alpha(\widehat k_{n_1},\widehat k_{n_1})}I_{\widetilde\theta_{n_1}}(Q\widehat T_{n_1}\mathcal P).
\]
Then $I_{\theta_{n_1}}(\widehat Q_{n_1}\widehat T_{n_1}\mathcal P)$ is measurable as a function of the first group data $z_{1:n_1}\in\mathcal Z_0^{n_1}$ and
\[
0\leq\sup_{Q\in\mathcal Q_\alpha(\mathcal X)}I_\theta(Q\mathcal P)-I_{\theta_{n_1}}(\widehat Q_{n_1}\widehat T_{n_1}\mathcal P)\leq2\varphi(\theta,\widetilde\theta_{n_1})+\varphi(\theta,\theta_{n_1})+C_\alpha(1\vee I_{\widetilde\theta_{n_1}}(\mathcal P))\Delta_{n_1},
\]
for any $\theta,\theta_{n_1}\in\Theta$, where $\varphi$ is as in Lemma 4.10, $C_\alpha>0$ depends only on $\alpha$ and $\Delta_{n_1}:=\Delta_{n_1}(\widetilde\theta_{n_1})$ is as in Definition 3. Moreover, the upper bound converges to zero in $[Q_0P_\theta]^{n_1}$-probability, as $n_1\to\infty$, provided that $\theta_{n_1}\to\theta$ and $[Q_0P_\theta]^{n_1}(|\widetilde\theta_{n_1}-\theta|>\varepsilon)\to0$ as $n_1\to\infty$, for every $\varepsilon>0$.''',r'''Suppose that Conditions (C1), (C2) and (C3) are satisfied with $\Theta\subseteq\mathbb R$. Moreover, suppose that $p_\theta(x)$ is three times continuously differentiable with respect to $\theta$ for every $x\in\mathcal X$ and such that $\theta\mapsto\|\dot p_\theta\|_1$, $\theta\mapsto\|\ddot p_\theta\|_1$ and $\theta\mapsto\|\dddot p_\theta\|_1$ are continuous and finite and $\theta\mapsto\dddot p_\theta$ is continuous as a function from $\Theta\to L_1(\mu)$. If $I_{\alpha,\theta_0}^*:=\sup_{Q\in\mathcal Q_\alpha(\mathcal X)}I_{\theta_0}(Q\mathcal P)>0$ for some $\theta_0\in\Theta$, $n_1=n_1(n)\to\infty$, $n_1/n\to0$ and the two-step MLE $\widehat\theta_{n_2}$ converges to $\theta_0$ in $Q^{(n)}P_{\theta_0}^n$-probability, then it is also regular and efficient at $\theta_0$, that is,
\[
\sqrt n\left(\widehat\theta_{n_2}-[\theta_0+h/\sqrt n]\right)\overset{Q^{(n)}P_{\theta_0+h/\sqrt n}^n}{\rightsquigarrow}\mathcal N\left(0,[I_{\alpha,\theta_0}^*]^{-1}\right),\qquad\forall h\in\mathbb R,
\]
where $Q^{(n)}$ is the two-step $\alpha$-sequentially interactive mechanism generating $Z_1,\ldots,Z_n$ as described above.''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+'; complete original statement')]) for i,(n,s,p) in enumerate(zip(NUMBERS,STATEMENTS,[11,12,14,15,15,21,22]),1)]
    paper=dict(paper_id=PID,title='Efficiency in local differential privacy',authors=['Lukas Steinberger'],version='arXiv:2301.10600v3; 7 Mar 2024',pdf_pages=52,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=29,main_text_boundary=dict(location='Section 5.4 Gaussian scale model and Funding end on PDF page 29. Page-29 evidence is clipped at y=550, above Appendix A Technical lemmas and proofs of Section 3 at y=564.3. No appendix body is used.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerate actual small-cap THEOREM environments on pages 1-28 and the main-text prefix of page 29. Visually compare all seven complete statements. Theorem 4.1 is a cited classical result printed as a Theorem and is retained. Lemmas, Propositions, Definitions and proof headings are excluded.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v3 PDF; no replacement source and no appendix body.',normalization_policy='Preserve complete original theorem wording, hypotheses, constructions, quantifiers and conclusions. Keep the printed nonnegative cross-parameter difference in Theorem 4.11. Normalize PDF line wrapping and mathematical typesetting only.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved all seven original Theorems; independent source validation is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
