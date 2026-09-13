"""Reproduce the six complete main-text Theorems in the registered v9 source."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2613'
SHA='849a1093c30a5bbbf5a48b96910096a35d30ae37c622b8fe2e5ddf3cacee9318'
URL='https://arxiv.org/pdf/2103.06476v9'
NUMBERS=['2.2','2.4','2.8','3.1','3.2','3.3']
PAGES=[8,10,13,18,19,21]
TITLES=['Gaussian mixture asymptotic confidence sequence','An abstract AsympCS for well-approximated processes',r'Asymptotic $(1-\alpha)$-coverage for Gaussian mixture AsympCSs','Confidence sequences for the ATE in randomized experiments','Confidence sequence for the ATE in observational studies','AsympCSs for the running average treatment effect']
STATEMENTS=[r'''Suppose $(Y_t)_{t=1}^\infty\sim\mathbb P$ is an infinite sequence of i.i.d. observations from a distribution $\mathbb P$ with mean $\mu$ and finite variance. Let $\widehat\mu_t:=\frac1t\sum_{i=1}^tY_i$ be the sample mean, and $\widehat\sigma_t^2:=\frac1t\sum_{i=1}^tY_i^2-(\widehat\mu_t)^2$ the sample variance based on the first $t$ observations. Then, for any prespecified constant $\rho>0$,
\[
\overline C_t^{\mathcal G}\equiv(\widehat\mu_t\pm\overline{\mathfrak B}_t^{\mathcal G}):=\left(\widehat\mu_t\pm\widehat\sigma_t\sqrt{\frac{2(t\rho^2+1)}{t^2\rho^2}\log\left(\frac{\sqrt{t\rho^2+1}}\alpha\right)}\right)
\]
(8)
forms a $(1-\alpha)$-AsympCS for $\mu$.''',r'''Let $\mathcal T$ be a totally ordered infinite set containing a minimal element $t_0\in\mathcal T$ and let $(\widehat\theta_t)_{t\in\mathcal T}$ be a real-valued process. Under Conditions G-1–G-4,
\[
[\widehat\theta_t-L_t,\widehat\theta_t+U_t]
\]
forms a $(1-\alpha)$-AsympCS for $\theta_t$ meaning there exists (on a potentially enriched probability space) some nonasymptotic $(1-\alpha)$-CS $[\widehat\theta_t-L_t^*,\widehat\theta_t+U_t^*]_{t\in\mathcal T}$ for $(\theta_t)_{t\in\mathcal T}$, i.e.
\[
\mathbb P\left(\forall t\in\mathcal T,\ \theta_t\in[\widehat\theta_t-L_t^*,\widehat\theta_t+U_t^*]\right)\ge1-\alpha
\]
such that
\[
L_t^*/L_t\xrightarrow{\mathrm{a.s.}}1\quad\text{and}\quad U_t^*/U_t\xrightarrow{\mathrm{a.s.}}1.
\]''',r'''Given the same setup as Proposition 2.5 and Conditions L-1, L-2, and L-3-$\eta$, the AsympCSs $(\widetilde C_t(m))_{t=m}^\infty$ given in (18) have sharp asymptotic $(1-\alpha)$-coverage for $\widetilde\mu_t:=\frac1t\sum_{i=1}^t\mu_i$ as $m\to\infty$, meaning
\[
\lim_{m\to\infty}\mathbb P\left(\forall t\ge m,\ \widetilde\mu_t\in\widetilde C_t(m)\right)=1-\alpha.
\]''',r'''Let $\widehat\psi_t^\times$ be the cross-fit AIPW estimator as in (25). Suppose $\|\widehat\mu_t^a(X)-\overline\mu^a(X)\|_{L_2(\mathbb P)}=o(1)$ for each $a\in\{0,1\}$ where $\overline\mu^a$ is some function (but need not be $\mu^a$), and hence $\|\widehat f_t-\overline f\|_{L_2(\mathbb P)}=o(1)$ for some influence function $\overline f$. Suppose that propensity scores are bounded away from 0 and 1, i.e. $\pi(X)\in[\delta,1-\delta]$ almost surely for some $\delta>0$, and suppose that $\mathbb E|\overline f(Z)|^{2+\varepsilon}<\infty$ for some $\varepsilon>0$. Then for any constant $\rho>0$,
\[
\widehat\psi_t^\times\pm\sqrt{\widehat{\operatorname{var}}_t(\widehat f)}\cdot\sqrt{\frac{2(t\rho^2+1)}{t^2\rho^2}\log\left(\frac{\sqrt{t\rho^2+1}}\alpha\right)}
\]
forms a $(1-\alpha)$-AsympCS for $\psi$.''',r'''Consider the same setup as Theorem 3.1 but with $\pi(x)$ no longer known. Suppose that regression functions and propensity scores are consistently estimated in $L_2(\mathbb P)$ at a product rate of $o(\sqrt{\log t/t})$, meaning that
\[
\|\widehat\pi_t-\pi\|_{L_2(\mathbb P)}\sum_{a=0}^1\|\widehat\mu_t^a-\mu^a\|_{L_2(\mathbb P)}=o\left(\sqrt{\log t/t}\right).
\]
Moreover, suppose that $\|\widehat f_t-f\|_{L_2(\mathbb P)}=o(1)$ where $f$ is the efficient influence function (24) and that $\mathbb E|f(Z)|^{2+\varepsilon}<\infty$ for some $\varepsilon>0$. Then for any constant $\rho>0$,
\[
\widehat\psi_t^\times\pm\sqrt{\widehat{\operatorname{var}}_t(\widehat f)}\cdot\sqrt{\frac{2(t\rho^2+1)}{t^2\rho^2}\log\left(\frac{\sqrt{t\rho^2+1}}\alpha\right)}
\]
forms a $(1-\alpha)$-AsympCS for $\psi$.''',r'''Suppose $Z_1,Z_2,\ldots$ are independent triples $Z_t:=(X_t,A_t,Y_t)$ and that Conditions $\widetilde{\mathrm{ATE}}$-1 and $\widetilde{\mathrm{ATE}}$-2 hold. Finally, suppose that the conditions of Corollary 2.6 hold, but with $(Y_t)_{t=1}^\infty$ replaced by the influence functions $(\overline f(Z_t))_{t=1}^\infty$. Then,
\[
\widehat\psi_t^\times\pm\sqrt{\frac{2(t\rho^2\widehat{\operatorname{var}}_t(\overline f)+1)}{t^2\rho^2}\log\left(\frac{\sqrt{t\rho^2\widehat{\operatorname{var}}_t(\overline f)+1}}\alpha\right)}
\]
(29)
forms a $(1-\alpha)$-AsympCS for the running average treatment effect $\widetilde\psi_t:=\frac1t\sum_{i=1}^t\psi_i$.''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+' ('+title+')',source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement')]) for i,(n,p,title,s) in enumerate(zip(NUMBERS,PAGES,TITLES,STATEMENTS),1)]
    paper=dict(paper_id=PID,title='Time-uniform central limit theory and asymptotic confidence sequences',authors=['Ian Waudby-Smith','David Arbour','Ritwik Sinha','Edward H. Kennedy','Aaditya Ramdas'],version='arXiv:2103.06476v9, marked 14 Mar 2024',pdf_pages=69,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=28,main_text_boundary=dict(location='Conclusion and acknowledgements end on PDFpage28 before References at y638.557; evidence clipped at y632. Page28 is shared with references, not an appendix. Appendix proofs start onpage33 and all appendix bodies are excluded. The PDF outline has displaced main-section page numbers, so actual page text controls the boundary.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Independently enumerate actual bold SFBX1000 Theorem headings on main-text pages1–28, clipping28 before references; visually inspect all six statements. Exactly Theorems2.2,2.4,2.8,3.1,3.2,3.3. Proposition2.5 and Corollary2.6 are not Theorems despite stale appendix outline labels.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Verified registered local arXiv v9 source, pinned bySHA256. Main text only; exclude appendix bodies and do not replace the source by its published version.',normalization_policy='Preserve all six full original statements, printed numbering, hypotheses and formulas; normalize wrapping and mathematical typesetting only. Preserve barred Gaussian-mixture C/B, changing-variance tilde C, fitted f versus limit bar-f variance expressions, exact coverage equality, and explicit condition/estimator references. Source discrepancies remain separate notes.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved six complete main-text Theorem statements; independent review remains separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
