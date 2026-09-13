"""Reproduce the nine complete main-text Theorems of the registered v2 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2004'
SHA='da7501754279852947b00ef181c4a65367e96957aa65be6fccb91a99d48e228b'
URL='https://arxiv.org/pdf/2205.14855v2'
NUMBERS=['2.1','2.2','2.3','3.1','3.2','3.3','3.4','3.5','5.1']
PAGES=[[4,5],[7],[7],[11],[14],[14],[16],[17],[20]]
STATEMENTS=[r'''If
\[
\rho:=\frac{\sigma_r-\sigma_{r+1}}{\|(I-U_rU_r^T)y_n\|}>2,
\]
(3)
we have
\[
\|\hat U_r\hat U_r^T-U_rU_r^T\|_{\mathrm F}\leq\frac{4\sqrt2}{\rho}\sqrt{\sum_{i=1}^r\left(\frac{u_i^Ty_n}{\sigma_i}\right)^2}.
\]
(4)''',r'''Assume $\beta n/k^2\geq10$. Assume
\[
\rho_0:=\frac{\lambda_\kappa}{\|E\|}>16.
\]
(9)
For any $i\in[n]$, we have
\[
\|\hat U_{1:\kappa}\hat U_{1:\kappa}^T-\hat U_{-i,1:\kappa}\hat U_{-i,1:\kappa}^T\|_{\mathrm F}\leq\frac{128}{\rho_0}\left(\sqrt{\frac{k\kappa}{\beta n}}+\frac{\|\hat U_{-i,1:\kappa}\hat U_{-i,1:\kappa}^T\epsilon_i\|}{\lambda_\kappa}\right).
\]
(10)''',r'''Assume $\beta n/k^2\geq10$. Assume there exists some $r\in[k]$ such that
\[
\tilde\rho_0:=\frac{\lambda_r-\lambda_{r+1}}{\max\left\{\|E\|,\sqrt{\frac{k^2}{\beta n}}\lambda_{r+1}\right\}}>16.
\]
(11)
For any $i\in[n]$, we have
\[
\|\hat U_{1:r}\hat U_{1:r}^T-\hat U_{-i,1:r}\hat U_{-i,1:r}^T\|_{\mathrm F}\leq\frac{128}{\tilde\rho_0}\left(\frac{\sqrt{kr}}{\sqrt{\beta n}}+\frac{\|\hat U_{-i,1:r}\hat U_{-i,1:r}^T\epsilon_i\|}{\lambda_r}\right).
\]
(12)''',r'''Consider the spectral clustering $\hat z$ of Algorithm 1 with $r=\kappa$. Assume $\epsilon_i\sim\mathrm{SG}_p(\sigma^2)$ independently with zero mean for each $i\in[n]$. Assume $\beta n/k^2\geq10$. There exist constants $C,C'>0$ such that under the assumption that
\[
\psi_1:=\frac{\Delta}{\beta^{-0.5}k\left(1+\sqrt{\frac pn}\right)\sigma}>C
\]
(21)
and
\[
\rho_1:=\frac{\lambda_\kappa}{(\sqrt n+\sqrt p)\sigma}>C,
\]
(22)
we have
\[
\mathbb E\ell(\hat z,z^*)\leq\exp\left(-\left(1-C'(\psi_1^{-1}+\rho_1^{-2})\right)\frac{\Delta^2}{8\sigma^2}\right)+\exp\left(-\frac n2\right).
\]''',r'''Consider the estimator $\tilde z$ from Algorithm 2. Assume $\epsilon_i\sim\mathrm{SG}_p(\sigma^2)$ independently with zero mean for each $i\in[n]$. Assume $\beta n/k^4\geq400$. There exist constants $C,C',C_1,C_2>0$ such that under the assumption that
\[
\psi_2:=\frac{\Delta}{\beta^{-0.5}k^2\left(1+\sqrt{\frac pn}\right)\sigma}>C
\]
and $\rho_2:=T/(\sigma(\sqrt n+\sqrt p))$ satisfies $C_1\leq\rho_2\leq\psi_2/C_2$, we have
\[
\mathbb E\ell(\tilde z,z^*)\leq\exp\left(-\left(1-C'(\rho_2\psi_2^{-1}+\rho_2^{-1})\right)\frac{\Delta^2}{8\sigma^2}\right)+\exp\left(-\frac n2\right).
\]
If $\psi_2,\rho_2\to\infty$ and $\rho_2/\psi_2=o(1)$ are further assumed, we have
\[
\mathbb E\ell(\tilde z,z^*)\leq\exp\left(-(1-o(1))\frac{\Delta^2}{8\sigma^2}\right)+\exp\left(-\frac n2\right).
\]''',r'''Consider the spectral clustering $\hat z$ of Algorithm 1 with $r=k$. Assume $\epsilon_i\overset{\mathrm{iid}}\sim\mathcal N(0,\sigma^2I_p)$ for each $i\in[n]$. Assume $\beta n/k^4\geq100$ and
\[
\frac{\Delta}{k^{3.5}\beta^{-0.5}\left(1+\frac pn\right)\sigma}\to\infty.
\]
(26)
We have
\[
\mathbb E\ell(\hat z,z^*)\leq\exp\left(-\left(1-C\left(\frac{\Delta}{k^{3.5}\beta^{-0.5}\left(1+\frac pn\right)\sigma}\right)^{-0.25}\right)\frac{\Delta^2}{8\sigma^2}\right)+2e^{-0.08n},
\]
(27)
where $C>0$ is some constant.''',r'''Consider the model (28). For any $\xi\sim F$, assume $\mathbb E\xi=0,\operatorname{Var}(\xi)=\bar\sigma^2$, and $\xi\sim\mathrm{SG}(\sigma^2)$ where $\sigma\leq C\bar\sigma$ for some constant $C>0$. Assume $\beta n>40$. Then there exist constants $C',C'',C^{\prime\prime\prime}>0$ such that if $\psi_3\geq C'$, we have
\[
\mathbb E\ell(\check z,z^*)\leq\exp\left(-\frac{(1-C''\psi_3^{-1})^2\Delta^2}{8\bar\sigma^2}\right)+\exp(-C''\sqrt p)+\exp\left(-\frac n2\right),
\]
and
\[
\mathbb E\ell(\check z,z^*)\geq\exp\left(-\frac{(1+C^{\prime\prime\prime}\psi_3^{-1})^2\Delta^2}{8\bar\sigma^2}\right)-\exp(-C^{\prime\prime\prime}\sqrt p)-\exp\left(-\frac n2\right).
\]''',r'''Consider the model (28). Assume all the assumptions needed in Theorem 3.4 and Lemma 3.4 hold. Then the spectral clustering $\check z$ is in general suboptimal, i.e., it fails to achieve the minimax rate (31). It is optimal if and only if the noise distribution $F$ is $\mathcal N(0,\bar\sigma^2)$.''',r'''If $\sigma_r^2-\sigma_{r+1}^2-\|(I-U_rU_r^T)y_n\|^2>0$, we have
\[
\|\hat U_r\hat U_r^T-U_rU_r^T\|_{\mathrm F}\leq\frac{2\sqrt2\sigma_r\|(I-U_rU_r^T)y_n\|}{\sigma_r^2-\sigma_{r+1}^2-\|(I-U_rU_r^T)y_n\|^2}\sqrt{\sum_{i=1}^r\left(\frac{u_i^Ty_n}{\sigma_i}\right)^2}.
\]''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+'; complete original statement'+(' including page-5 continuation' if len(pages)>1 else '')) for p in pages]) for i,(n,s,pages) in enumerate(zip(NUMBERS,STATEMENTS,PAGES),1)]
    paper=dict(paper_id=PID,title='Leave-one-out singular subspace perturbation analysis for spectral clustering',authors=['Anderson Y. Zhang','Harrison Y. Zhou'],version='arXiv:2205.14855v2; 14 Jan 2024',pdf_pages=50,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=28,main_text_boundary=dict(location='Main-text Sections 1-6 end on PDF page 28 followed by Acknowledgements. Evidence on page 28 is clipped at y=414, before Supplementary Material at y=419.9 and References at y=529.9. Appendix A starts on page 31. No appendix body is used.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerate actual small-cap Theorem environments on pages 1-27 and the main-text prefix of page 28. Include Theorem 5.1 in the main-text proof section; exclude Lemmas, Propositions, Corollaries, proof headings, citations and appendix results. Visually compare all nine complete statements.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v2 PDF; main text only.',normalization_policy='Preserve original wording and all mathematical hypotheses, conclusions and subparts. Normalize PDF line wrapping and mathematical typesetting only.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved nine complete original Theorems; independent source validation is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
