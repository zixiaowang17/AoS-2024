"""Reproduce the four original main-text Theorems from the registered local PDF."""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
REPO = next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID = 'aos-2024-v52-i04-p1671'
SHA = '98f01d3c2ca9245356a1395a25fb45d6a8f77aae94d3612f7b45fa3489778a4d'
claims = []
def claim(n, title, pages, text):
    claims.append(dict(claim_id=PID+'/T'+str(n), paper_id=PID, claim_kind='theorem',
        label='Theorem '+str(n)+' ('+title+')', source_order=n, statement_original=text.strip(),
        evidence=[dict(page=p, location='Theorem '+str(n)+'; original statement' if i==0 else
            'Theorem '+str(n)+'; part (c) and conclusion, before commentary') for i,p in enumerate(pages)]))
claim(1, 'Differential privacy of DPVote', [12], r'''
The proposed DPVote mechanism in Algorithm 2 is $(\epsilon,\delta)$-distributed group differentially private.
''')
claim(2, 'Sign consistency of DPVote', [12], r'''
Given the privacy level $(\epsilon,\delta)$, suppose $\widetilde s\ge\overline s$, and for $1\le l\le p$, the stability function satisfies
\[
f_l(\boldsymbol Q_l^r,\overline Q_l)\ge8(\gamma+1)\sqrt{2\widetilde s\log(2/\delta)}\log p/\epsilon,\tag{6}
\]
where $\gamma>2$. Then, the proposed DPVote algorithm produces $(\widehat S,\widehat{\boldsymbol Q})$ that has the same signs as $\overline{\boldsymbol Q}$with a probability (with respect to the randomness in the algorithm) of no less than $1-O(p^{-\gamma+2})$.
''')
claim(3, 'Sign consistency of DPVote for the mean vector', [15], r'''
Let $\{\boldsymbol X_1,\ldots,\boldsymbol X_N\}$ be $N$ i.i.d. random vectors sampled from $\mathbb P(\boldsymbol\theta^*,C)$ distributed in $m$ machines $\mathcal H_1,\ldots,\mathcal H_m$, with each machine holds $n_j$ $(1\le j\le m)$ samples. Here we assume $n_1\asymp\ldots\asymp n_m\asymp n$. Moreover, assume that there exist sufficiently large constants $C_1,C_2,\gamma_0>0$ such that

(a) The dimension $p$ satisfies $p=O(n^{\gamma_0})$, and the number of machines $m$ satisfies $\sqrt{\widetilde s\log(1/\delta)}\log p/\epsilon=o(m)$. We take
\[
\lambda_N\ge C_1\left(\sqrt{\frac{\log p}{N}}+\frac{\sqrt{\widetilde s\log(1/\delta)}\log p}{m\sqrt n\epsilon}+\frac1n\right);\tag{11}
\]

(b) Define $S=\operatorname{supp}(\boldsymbol\theta^*)$, and assume that
\[
\min_{l\in S}|\theta_l^*|\ge C_2\left(\sqrt{\frac{\log p}{N}}+\frac{\sqrt{\widetilde s\log(1/\delta)}\log p}{m\sqrt n\epsilon}+\frac1n\right).\tag{12}
\]

Then for $\widetilde s\ge s$, $\gamma_1>0$ and $\widehat{\boldsymbol Q}(\mathbb X)$ defined in Algorithm 3, we have
\[
\lim_{N\to\infty}\mathbb P\left(\widehat{\boldsymbol Q}(\mathbb X)=\operatorname{sgn}(\boldsymbol\theta^*)\right)=1.
\]
''')
claim(4, 'Sign consistency of DPVote Lasso', [17,18], r'''
Let $\mathbb X=\{(\boldsymbol X_1,Y_1),\ldots,(\boldsymbol X_N,Y_N)\}$ be $N$ i.i.d. random vectors sampled from $\mathcal P_{X,Y}(\boldsymbol\theta^*,\rho,\eta_1,C_1,\eta_2,C_2)$ distributed in $m$ machines $\mathcal H_1,\ldots,\mathcal H_m$, with each machine holds $n_j$ $(1\le j\le m)$ samples. Here we assume $n_1\asymp\ldots\asymp n_m\asymp n$. Moreover, assume that sufficiently large constants $C_3,C_4,\gamma_0$ exist such that

(a) The dimension, the number of machines and the sparsity level satisfy $p=O(n^{\gamma_0})$, $\sqrt{\widetilde s\log(1/\delta)}\log p/\epsilon=o(m)$, $\widetilde s=o(\sqrt{n/\log p})$, and we take
\[
\lambda_N=C_3\left(\sqrt{\frac{\log p}{N}}+\frac{\sqrt{\widetilde s\log(1/\delta)}\log p}{m\sqrt n\epsilon}+\frac1n\right);\tag{18}
\]

(b) For $S=\operatorname{supp}(\boldsymbol\theta^*)$, the minimal signal satisfies
\[
\min_{l\in S}|\theta_l^*|\ge C_4\left(\sqrt{\frac{\log p}{N}}+\frac{\sqrt{\widetilde s\log(1/\delta)}\log p}{m\sqrt n\epsilon}+\frac1n+\max_{1\le j\le m}\lambda_j\right),\tag{19}
\]
with probability tending to 1.

(c) The covariance matrix $\boldsymbol\Sigma=\mathbb E\boldsymbol X\boldsymbol X^{\mathrm T}$ is positive definite. Let $\boldsymbol\Sigma^{-1}=(\boldsymbol\omega_1,\ldots,\boldsymbol\omega_p)$, assume that
\[
\max_{l\in S^c}\frac{|\boldsymbol\omega_{-l}|_1}{\omega_{l,l}}\le1-\Delta_0.\tag{20}
\]

Then for $\widetilde s\ge s$, the estimator $\widehat{\boldsymbol Q}(\mathbb X)$ defined in Algorithm 4 satisfies
\[
\lim_{N\to\infty}\mathbb P\left(\widehat{\boldsymbol Q}(\mathbb X)=\operatorname{sgn}(\boldsymbol\theta^*)\right)=1.
\]
''')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='Majority Vote for Distributed Differentially Private Sign Selection',
        authors=['Weidong Liu','Jiyuan Tu','Xiaojun Mao','Xi Chen'],version='arXiv:2209.04419v2, 4 June 2024',
        source_url='https://arxiv.org/pdf/2209.04419v2',pdf_pages=41,pdf_sha256=SHA,
        main_text_last_pdf_page=28,main_text_boundary=dict(location='Main paper and references end on PDF page 28 with Zhu, Li and Wang (2021), pages 1004–1018. Section 7 Appendix starts on PDF page 29; appendix bodies excluded.',shared_page_with_appendix=False),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(dict(schema_version='statistical-theorem-inventory-v1',
        scope=dict(theorem_scope='main_text_only',source_policy='Verified local arXiv v2 PDF; pages 1–28 only. No appendix bodies.'),
        papers=[paper],claims=claims),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
