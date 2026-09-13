"""Reproduce both complete original main-text Theorems from registered arXiv v4.

Printed fold indices and hats are preserved. This script restores the manual
extraction; it does not perform a fresh mathematical review or certify proofs.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1796'
SHA='45ff9682a415f4d28e0ed8ed4017b0b71f5b6972296a3e6115c0d52b696fdf49'
URL='https://arxiv.org/pdf/2306.16406v4'
STATEMENTS=[r'''With nuisance estimators $\widehat{\boldsymbol\ell}_v$, $\widehat{\boldsymbol\lambda}_v$, $\widehat{\boldsymbol\theta}_v$ and $\widehat{\boldsymbol\pi}_v$ in Algorithms 1 and $1^\dagger$, define
\[
\Delta_v:=\frac{\sum_{a\in\mathcal S'_1}\pi_*^a}{\sum_{a\in\mathcal S'_1}\widehat\pi_v^a}\sum_{k=1}^K\mathbb E_{P_*}\left[h_v^{k-1}(\bar Z_{k-1})-\widehat\ell_v^k(\bar Z_k)\mid A=0\right]
\]
(18)
for every fold $v\in[V]$ and $\Delta:=n^{-1}\sum_{v=1}^V|I_v|\Delta_v$. The following finite-sample expansion of $\widehat r$ holds:
\[
\begin{aligned}
\widehat r-\Delta-r_*={}&\sum_{v\in[V]}\frac{|I_v|}{n\sum_{a\in\mathcal S'_1}\widehat\pi_v^a}(P^{n,v}-P_*)\left\{\left(\sum_{a\in\mathcal S'_1}\widehat\pi_v^a\right)\widetilde{\mathcal T}(\widehat{\boldsymbol\ell}_v,\widehat{\boldsymbol\lambda}_v,\widehat{\boldsymbol\pi}_v)-\left(\sum_{a\in\mathcal S'_1}\pi_*^a\right)\widetilde{\mathcal T}(\boldsymbol\ell_*,\boldsymbol\lambda_*,\boldsymbol\pi_*)\right\}\\
&+\sum_{v\in[V]}\frac{|I_v|\sum_{a\in\mathcal S'_1}\widehat\pi_v^a}{n}\sum_{k=2}^K B_{k,v}+\sum_{v\in[V]}\frac{|I_v|\sum_{a\in\mathcal S'_1}\pi_*^a}{n\sum_{a\in\mathcal S'_1}\pi_v^a}(P^{n,v}-P_*)D_{\mathrm{GSC}}(\boldsymbol\ell_*,\boldsymbol\lambda_*,\boldsymbol\pi_*,r_*).
\end{aligned}
\]
(19)
Moreover, if for all $n,k,v$,

1. $\Pr(\|\widehat\lambda_v^{k-1}-\lambda_*^{k-1}\|_{L^2(P_*)}>a_{n,k,v})\leq c_{n,k,v}$ and $\Pr(\|\widehat\ell_v^{k-1}-h_v^{k-1}\|_{L^2(P_*)}>b_{n,k,v})\leq d_{n,k,v}$ for some positive numbers $a_{n,k,v}$, $b_{n,k,v}$, $c_{n,k,v}$ and $d_{n,k,v}$,
2. $\widehat\lambda_v^{k-1}$ are bounded for all $k$ and $v$, and
3. $\mathbb E_{P_*}|D_{\mathrm{GSC}}(\boldsymbol\ell_*,\boldsymbol\lambda_*,\boldsymbol\pi_*,r_*)(O)|^3<\infty$,

then for any $\varepsilon>0$, there exist quantities $\mathcal C_1,\mathcal C_2>0$ that may only depend on $\varepsilon$, $P_*$ and the bound on $\widehat\lambda_v^{k-1}$ only such that, for any $t>\mathcal C_1\sum_{v\in[V]}\sum_{k=2}^K(a_{n,k,v}b_{n,k,v}+a_{n,k,v}+b_{n,k,v}+n^{-1})$, the following finite-sample confidence guarantee holds:
\[
\begin{aligned}
\Pr(|\widehat r-\Delta-r_*|>t)\leq{}&2\Phi\left(-\sqrt n\frac{t-\mathcal C_1\sum_{v\in[V]}\sum_{k=2}^K(a_{n,k,v}b_{n,k,v}+n^{-1/2}(a_{n,k,v}+b_{n,k,v})+n^{-1})}{\sigma_{*,\mathrm{GSC}}}\right)\\
&+\frac{\mathcal C_2}{\sqrt n}+\sum_{v\in[V]}\sum_{k=2}^K(c_{n,k,v}+d_{n,k,v})+\varepsilon
\end{aligned}
\]
(20)
where $\sigma_{*,\mathrm{GSC}}$ is defined in (10) and $\Phi$ denotes the cumulative distribution function of the standard normal distribution.

1. Efficiency: Under Condition ST.1, with $\widehat r$ in Line 9 of Alg. 1, and $D_{\mathrm{GSC}}$ in (8),
\[
\widehat r-\Delta=r_*+\frac1n\sum_{i=1}^n D_{\mathrm{GSC}}(\boldsymbol\ell_*,\boldsymbol\lambda_*,\boldsymbol\pi_*,r_*)(O_i)+o_p(n^{-1/2}).
\]
(21)
For $\widehat r$ in Line 9 of Alg. $1^\dagger$, with $D_{\mathrm{SC}}$ in (9), this specializes to
\[
\widehat r-\Delta=r_*+\frac1n\sum_{i=1}^n D_{\mathrm{SC}}(\boldsymbol\ell_*,\boldsymbol\theta_*,\boldsymbol\pi_*,r_*)(O_i)+o_p(n^{-1/2}).
\]
(22)
2. Multiply robust consistency: Under Condition ST.2, $\widehat r-\Delta\xrightarrow{p}r_*$ as $n\to\infty$.

Additionally under Condition DS.0, $\Delta=0$ and thus $\widehat r$ is RAL and efficient under Condition ST.1 and is consistent for $r_*$ under Condition ST.2.''',
r'''Suppose that there exists a function $\mathcal E_\infty\in L^2(P_*)$ such that $\max_{v\in[V]}\|\widehat{\mathcal E}^{-v}-\mathcal E_\infty\|_{L^2(P_*)}=o_p(1)$. Under Condition DS.1, the sequence of estimators $\widehat r_{\mathrm{Xcon}}$ in Line 5 of Algorithm 1 is RAL: with $r_*$ from (1) and $D_{\mathrm{Xcon}}$ from (23),
\[
\widehat r_{\mathrm{Xcon}}=r_*+\frac1n\sum_{i=1}^n\left\{D_{\mathrm{Xcon}}(\rho_*,\mathcal E_\infty,r_*)(O_i)+\frac{\mathbb E_{P_*}[\mathcal E_\infty(X)]-r_*}{\rho_*}(1-A_i-\rho_*)\right\}+\mathcal B,
\]
(25)
where
\[
\begin{aligned}
\mathcal B:={}&\sum_{v\in[V]}\frac{|I_v|}{n}\left\{\frac{\widehat\rho^v-\rho_*}{\widehat\rho^v}P_*(\widehat{\mathcal E}^{-v}-\mathcal E_\infty)\right.\\
&\left.\qquad+(P^{n,v}-P_*)\left\{D_{\mathrm{Xcon}}(\widehat\rho^{-v},\widehat{\mathcal E}^{-v},\widehat r_{\mathrm{Xcon}}^v)-D_{\mathrm{Xcon}}(\rho_*,\mathcal E_\infty,r_*)\right\}\right\}=o_p(n^{-1/2}).
\end{aligned}
\]
Moreover, if $\mathcal E_*$ is estimated consistently, namely $\mathcal E_\infty=\mathcal E_*$, then $\widehat r_{\mathrm{Xcon}}$ is efficient:
\[
\widehat r_{\mathrm{Xcon}}=r_*+\frac1n\sum_{i=1}^nD_{\mathrm{Xcon}}(\rho_*,\mathcal E_*,r_*)(O_i)+o_p(n^{-1/2}).
\]
(26)''']
def inventory():
    claims=[dict(claim_id=PID+f'/T{i}',paper_id=PID,claim_kind='theorem',label=label,source_order=i,statement_original=s,evidence=[dict(page=p,location=f'Theorem {i}; full statement including continued formulas and conclusions') for p in pages]) for i,(s,label,pages) in enumerate(zip(STATEMENTS,['Theorem 1',r'Theorem 2 (Efficiency and fully robust asymptotic linearity of $\widehat r_{\mathrm{Xcon}}$)'],[[17,18],[26,27]]),1)]
    claims[0]['source_footnotes']=[dict(label='6',statement_original=r"The denominator $\sum_{a\in\mathcal S'_1}\widehat\pi_v^a$ is nonzero with probability tending to one exponentially.",evidence=[dict(page=17,location='Footnote 6 attached to the definition of Delta_v in Theorem 1')])]
    paper=dict(paper_id=PID,title='Efficient and Multiply Robust Risk Estimation under General Forms of Dataset Shift',authors=['Hongxiang Qiu','Eric Tchetgen Tchetgen','Edgar Dobriban'],version='arXiv:2306.16406v4; arXiv stamp 8 Jun 2024',pdf_pages=96,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=33,main_text_boundary=dict(location='Discussion and acknowledgements end on PDF page 33 before References at y=621.718. Retained page-33 evidence is clipped at y=620.7. Bibliography and the Supplemental Material (beginning on PDF page 43, identified by the table of contents) are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Independent enumeration of actual bold Theorem headings across main-text pages 1–33 and visual comparison of both complete multi-page statements. Lemmas, Propositions, Corollaries and supplement references are excluded.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v4; no published-version substitution. Supplemental bodies excluded.',normalization_policy='Original wording, formulas, hats, fold indices and all branches preserved; PDF wrapping normalized into LaTeX. The theorem footnote is retained in source_footnotes without inserting it into the body.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
