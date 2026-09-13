"""Regenerate the complete manually transcribed main-text theorem inventory."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1460'
SHA='7d26b0fb80a5a46f7044f5223d98da7b1a1a6eec64c520380562f10cd66a628d'
claims=[]
def claim(number,pages,text,title=None):
    claims.append(dict(claim_id=f'{PID}/T{number}',paper_id=PID,claim_kind='theorem',label=f'Theorem {number}'+(f' ({title})' if title else ''),source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location=f'Theorem {number}, '+('complete original statement' if len(pages)==1 else ('opening of original statement' if p==pages[0] else 'continuation of original statement'))) for p in pages]))
claim('3.1',[7],r'''
Assume $\mu_\Lambda,\mu_\Theta$ have finite non-singular second moments $\boldsymbol Q_\Lambda,\boldsymbol Q_\Theta$ with $\boldsymbol Q_\Theta=q_\Theta\boldsymbol I_r$ (with no loss of generality per Remark 3.1). If $n,d\to\infty$ with $d/n\to\infty$, then under the model of Eq. (4):

1. $L^{\sin}(\widehat{\boldsymbol\Lambda}_s,\boldsymbol\Lambda)\overset P\to0$.

2. If we further assume that for some $\varepsilon>0$ we have $\mathbb E_{\Lambda_0\sim\mu_\Lambda}[\|\boldsymbol\Lambda_0\|^{4+\varepsilon}]<\infty$, then there exists an estimator $\widehat{\boldsymbol L}:\boldsymbol A\mapsto\widehat{\boldsymbol L}(\boldsymbol A)\in\mathbb R^{n\times n}$, such that $\mathbb E[\|\widehat{\boldsymbol L}(\boldsymbol A)-\boldsymbol\Lambda\boldsymbol\Lambda^{\mathsf T}\|_F^2]/n^2\to0$ as $n,d\to\infty$.

3. Let $\boldsymbol\Lambda_0\sim\mu_\Lambda$. If we further assume that there does not exist $\boldsymbol\Omega\in\mathcal O(r)$, such that $\boldsymbol\Omega\ne\boldsymbol I_r$ and $\boldsymbol\Omega\boldsymbol\Lambda_0\overset d=\boldsymbol\Lambda_0$, then there exists $\widehat{\boldsymbol\Lambda}:\boldsymbol A\mapsto\widehat{\boldsymbol\Lambda}(\boldsymbol A)\in\mathbb R^{n\times r}$, such that $\mathbb E[\|\widehat{\boldsymbol\Lambda}(\boldsymbol A)-\boldsymbol\Lambda\|_F^2]/n\to0$ as $n,d\to\infty$.
''')
claim('3.2',[8],r'''
Consider the strong signal model of Eq. (4), assuming, without loss of generality, the setting of Remark 3.1. We let $n,d\to\infty$ simultaneously with $d/n\to\infty$, then for any estimator $\widehat{\boldsymbol\Theta}:\boldsymbol A\mapsto\widehat{\boldsymbol\Theta}(\boldsymbol A)\in\mathbb R^{d\times r}$, we have
\[
\liminf_{n,d\to\infty}\frac1d\mathbb E\left[\|\widehat{\boldsymbol\Theta}(\boldsymbol A)-\boldsymbol\Theta\|_F^2\right]\ge rq_\Theta-\mathbb E\left[\left\|\mathbb E[\boldsymbol\Theta_0\mid\boldsymbol Q_\Lambda^{1/2}\boldsymbol\Theta_0+\boldsymbol G]\right\|^2\right],\tag{7}
\]
where $\boldsymbol G\sim\mathsf N(0,\boldsymbol I_r)$, $\boldsymbol\Theta_0\sim\mu_\Theta$ are mutually independent. Notice that the right hand side of Eq. (7) is independent of $(n,d)$.

If we further assume $\mathbb E[\|\boldsymbol\Theta_0\|^4]<\infty$, then for any $\widehat{\boldsymbol M}:\boldsymbol A\mapsto\widehat{\boldsymbol M}(\boldsymbol A)\in\mathbb R^{d\times d}$, we have
\[
\liminf_{n,d\to\infty}\frac1{d^2}\mathbb E\left[\|\widehat{\boldsymbol M}(\boldsymbol A)-\boldsymbol\Theta\boldsymbol\Theta^{\mathsf T}\|_F^2\right]\ge rq_\Theta^2-\left\|\mathbb E\left[\mathbb E[\boldsymbol\Theta_0\mid\boldsymbol Q_\Lambda^{1/2}\boldsymbol\Theta_0+\boldsymbol G]\mathbb E[\boldsymbol\Theta_0\mid\boldsymbol Q_\Lambda^{1/2}\boldsymbol\Theta_0+\boldsymbol G]^{\mathsf T}\right]\right\|_F^2.\tag{8}
\]
''')
claim('3.3',[8],r'''
Under the conditions of Theorem 3.1, claim 3, there exist estimators $\widehat{\boldsymbol\Theta}:\boldsymbol A\mapsto\widehat{\boldsymbol\Theta}(\boldsymbol A)$ and $\widehat{\boldsymbol M}:\boldsymbol A\mapsto\widehat{\boldsymbol M}(\boldsymbol A)$, such that
\[
\lim_{n,d\to\infty}\frac1d\mathbb E\left[\|\widehat{\boldsymbol\Theta}(\boldsymbol A)-\boldsymbol\Theta\|_F^2\right]=rq_\Theta-\mathbb E\left[\left\|\mathbb E[\boldsymbol\Theta_0\mid\boldsymbol Q_\Lambda^{1/2}\boldsymbol\Theta_0+\boldsymbol G]\right\|^2\right],
\]
\[
\lim_{n,d\to\infty}\frac1{d^2}\mathbb E\left[\|\widehat{\boldsymbol M}(\boldsymbol A)-\boldsymbol\Theta\boldsymbol\Theta^{\mathsf T}\|_F^2\right]=rq_\Theta^2-\left\|\mathbb E\left[\mathbb E[\boldsymbol\Theta_0\mid\boldsymbol Q_\Lambda^{1/2}\boldsymbol\Theta_0+\boldsymbol G]\mathbb E[\boldsymbol\Theta_0\mid\boldsymbol Q_\Lambda^{1/2}\boldsymbol\Theta_0+\boldsymbol G]^{\mathsf T}\right]\right\|_F^2.
\]
''')
claim('4.1',[9],r'''
There exists a deterministic countable set $\mathcal D\subseteq\mathbb R_{\ge0}$ such that
\[
q_\Theta\in\mathbb R_{\ge0}\quad\Rightarrow\quad\lim_{n\to\infty}\mathrm I_n^{\mathrm{symm}}(\mu_\Lambda;q_\Theta)=\frac14q_\Theta^2\|\mathbb E_{\Lambda_0\sim\mu_\Lambda}[\boldsymbol\Lambda_0\boldsymbol\Lambda_0^{\mathsf T}]\|_F^2-\sup_{\boldsymbol Q\in S_r^+}\mathcal F(q_\Theta^2,\boldsymbol Q),
\]
\[
q_\Theta\in\mathbb R_{\ge0}\setminus\mathcal D\quad\Rightarrow\quad\lim_{n\to\infty}\operatorname{MMSE}_n^{\mathrm{symm}}(\mu_\Lambda;q_\Theta)=\|\mathbb E_{\Lambda_0\sim\mu_\Lambda}[\boldsymbol\Lambda_0\boldsymbol\Lambda_0^{\mathsf T}]\|_F^2-\|\boldsymbol Q^*(s)\|_F^2.
\]
''','[LM19], Corollary 42, Proposition 43')
claim('4.2',[9,10],r'''
Consider the weak signal model of Eq. (9), assuming, without loss of generality, the setting of Remark 3.1. Let $n,d\to\infty$ simultaneously with $d/n\to\infty$. Then for any estimator $\widehat{\boldsymbol\Theta}:\boldsymbol A\mapsto\widehat{\boldsymbol\Theta}(\boldsymbol A)\in\mathbb R^{d\times r}$, we have
\[
\liminf_{n,d\to\infty}\frac1d\mathbb E[\|\widehat{\boldsymbol\Theta}(\boldsymbol A)-\boldsymbol\Theta\|_F^2]\ge rq_\Theta-\|\mathbb E_{\Theta_0\sim\mu_\Theta}[\boldsymbol\Theta_0]\|^2.
\]
If we further assume $\mu_\Theta$ has bounded fourth moment, then for any $\widehat{\boldsymbol M}:\boldsymbol A\mapsto\widehat{\boldsymbol M}(\boldsymbol A)\in\mathbb R^{d\times d}$, we have
\[
\liminf_{n,d\to\infty}\frac1{d^2}\mathbb E[\|\widehat{\boldsymbol M}(\boldsymbol A)-\boldsymbol\Theta\boldsymbol\Theta^{\mathsf T}\|_F^2]\ge rq_\Theta^2-\|\mathbb E_{\Theta_0\sim\mu_\Theta}[\boldsymbol\Theta_0]\|^4.
\]
Notice that the above lower bounds are achieved by the null estimators $\widehat{\boldsymbol\Theta}(\boldsymbol A)=\mathbb E[\boldsymbol\Theta]\in\mathbb R^{d\times r}$ and $\widehat{\boldsymbol M}(\boldsymbol A)=\mathbb E[\boldsymbol\Theta\boldsymbol\Theta^{\mathsf T}]\in\mathbb R^{d\times d}$.
''')
claim('4.3',[10],r'''
Define the mutual information per coordinate in asymmetric model of Eqs. (9), via
\[
\mathrm I_n^{\mathrm{asym}}(\mu_\Lambda,\mu_\Theta):=\frac1n\mathbb E\log\frac{d\mathbb P_{\boldsymbol\Lambda,\boldsymbol A}}{d(\mathbb P_{\boldsymbol\Lambda}\times\mathbb P_{\boldsymbol A})}(\boldsymbol\Lambda,\boldsymbol A).\tag{16}
\]
Further recall the definition of mutual information in the symmetric model (10) given by Eq. (12). Within the setting of Assumption 4.1, we let $n,d\to\infty$ simultaneously with $d/n\to\infty$. In addition, we require without loss of generality $\boldsymbol Q_\Theta=q_\Theta\boldsymbol I_r$, cf. Remark 3.1. Then the following limits exist and are equal
\[
\lim_{n,d\to\infty}\mathrm I_n^{\mathrm{asym}}(\mu_\Lambda,\mu_\Theta)=\lim_{n\to\infty}\mathrm I_n^{\mathrm{symm}}(\mu_\Lambda;q_\Theta).
\]
''')
claim('4.4',[11],r'''
Under the conditions of Theorem 4.3, for all but countably many values of $q_\Theta>0$, we have
\[
\liminf_{n,d\to\infty}\operatorname{MMSE}_n^{\mathrm{asym}}(\mu_\Lambda,\mu_\Theta)\ge\lim_{n\to\infty}\operatorname{MMSE}_n^{\mathrm{symm}}(\mu_\Lambda;q_\Theta).\tag{18}
\]
Further, consider a modified model in which the statistician observes $(\boldsymbol A,\boldsymbol Y'(\varepsilon))$, where $\boldsymbol A$ is given by Eq. (9), and
\[
\boldsymbol Y'(\varepsilon):=\frac{\sqrt\varepsilon}{n}\boldsymbol\Lambda\boldsymbol\Lambda^{\mathsf T}+\boldsymbol W',\qquad\boldsymbol W'\sim\operatorname{GOE}(n).
\]
Here, we assume $\boldsymbol W'$ is independent of everything else. Denote by $\operatorname{MMSE}_n^{\mathrm{asym}}(\mu_\Lambda,\mu_\Theta;\varepsilon)$ the corresponding matrix mean square error. Then, for all but countably many values of $q_\Theta>0$, we have
\[
\lim_{\varepsilon\to0+}\limsup_{n,d\to\infty}\operatorname{MMSE}_n^{\mathrm{asym}}(\mu_\Lambda,\mu_\Theta;\varepsilon)\le\lim_{n\to\infty}\operatorname{MMSE}_n^{\mathrm{symm}}(\mu_\Lambda;q_\Theta).\tag{19}
\]
''')
claim('4.5',[12],r'''
Under the conditions of Theorem 4.3, we further assume at least one of the following conditions holds:

(a) $dn^{-3}(\log n)^{-6}\to\infty$.

(b) $d(\log d)^{8/5}/n^{6/5}\to0$ and $\mu_\Lambda$ has bounded support.

(c) For the case $r=1$, define $Y=\sqrt\gamma\Lambda_0+G$ with $G\sim\mathsf N(0,1)$ independent of $\Lambda_0\sim\mu_\Lambda$, and define $\mathsf I(\gamma)=\mathbb E\log\frac{dp_{Y\mid\Lambda_0}}{dp_Y}(Y,\Lambda_0)$. Let
\[
\Psi(\gamma,s)=\frac{s^2}4+\frac{\gamma^2}{4s}-\frac\gamma2+\mathsf I(\gamma).
\]
Assume that the global maximum of $\gamma\mapsto\Psi(\gamma,q_\Theta)$ over $(0,\infty)$ is also the first stationary point of the same function.

Then, we have
\[
\lim_{n,d\to\infty}\operatorname{MMSE}_n^{\mathrm{asym}}(\mu_\Lambda,\mu_\Theta)=\lim_{n\to\infty}\operatorname{MMSE}_n^{\mathrm{symm}}(\mu_\Lambda;q_\Theta).\tag{20}
\]
(For condition (b), the conclusion is guaranteed to hold for all but countably many values of $q_\Theta>0$.)
''')
claim('5.1',[14,15],r'''
Consider the Gaussian mixture model with $k$ components of equal weights, in the high-dimensional asymptotics $d,n\to\infty$, $d/n\to\infty$. Under the above assumptions on the centers $\boldsymbol\Theta$, the following results hold:

(a) If $q_\Theta<q_\Theta^{\mathrm{info}}(k)$, then for any estimator $\widehat{\boldsymbol\Lambda}:\mathbb R^{n\times d}\to\{\boldsymbol e_j:j\in[k]\}^n$ that is a measurable function of the input $\boldsymbol A$, we have
\[
\mathop{\mathrm{p\text{-}lim}}_{n,d\to\infty}\operatorname{Overlap}_n=\frac1k.
\]

(b) Assume either $dn^{-3}(\log n)^{-6}\to\infty$ or $dn^{-6/5}(\log d)^{8/5}\to0$. If $q_\Theta>q_\Theta^{\mathrm{info}}(k)$, then there exists an estimator $\widehat{\boldsymbol\Lambda}:\mathbb R^{n\times d}\to\{\boldsymbol e_j:j\in[k]\}^n$ that is a measurable function of the input $\boldsymbol A$, such that
\[
\liminf_{n,d\to\infty}\mathbb E[\operatorname{Overlap}_n]>\frac1k.
\]
''')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='Fundamental Limits of Low-Rank Matrix Estimation with Diverging Aspect Ratios',authors=['Andrea Montanari','Yuchen Wu'],version='arXiv:2211.00488v1, 1 November 2022',source_url='https://arxiv.org/pdf/2211.00488v1',pdf_pages=74,pdf_sha256=SHA,main_text_last_pdf_page=28,main_text_boundary=dict(location='Main text and references end on PDF page 28 after reference [ZSF22]. Appendix A begins on the separate PDF page 29.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    data=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Verified registered arXiv v1 PDF, main-text pages 1-28; appendix bodies excluded.'),papers=[paper],claims=claims)
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
