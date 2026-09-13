"""Reproduce all seven complete main-text Theorems from the registered local PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2738'
SHA='e26292d82886e424c8df8739282efad1311f561b890479fe266e078cccaf4ca4'
URL='https://arxiv.org/pdf/2302.05851v1'
NUMBERS=['2.7','2.9','2.12','3.2','3.5','3.8','3.9']
PAGES=[[9],[11],[12],[14,15],[16],[18],[19]]
STATEMENTS=[r'''Consider the two-way interaction model in the equation (2.2), where all the univariate components are $\beta_1$ smooth and all the bivariate components are $\beta_2$ smooth. Choose $N_1L_1=\lfloor n^{1/2(2\beta_1+1)}\rfloor$, $N_2L_2=\lfloor n^{1/2(\beta_2+1)}\rfloor$ Then we have:
\[
\inf_{\phi_2\in\mathcal F^1_{NN},\phi_2\in\mathcal F^2_{NN}}\mathbb E\left[\|f_0(X)-\phi_1(X)-\phi_2(X)\|^2\right]\le C_3\left(d(N_1L_1)^{-4\beta_1}+\binom d2(N_2L_2)^{-2\beta_2}\right),
\]
where $\mathcal F^1_{NN}$ and $\mathcal F^2_{NN}$ are same as defined in (2.4) and (2.5). All the constants $(C_1,C_2,C_3)$ are independent of $(d,N_1,L_1,N_2,L_2)$.''',r'''Under Assumption 2.1 - 2.3 and 2.6, the ERM estimator $\widehat f$ of $f_0$ defined in equation (2.3) satisfies:
\[
\mathbb E\left[\left(\widehat f(X)-f_0(X)\right)^2\mid\mathbf S_n\right]=O_p\left(\rho_n^2+\frac{V_n}{n}\log^{3/2}n\right),
\]
where
\[
\rho_n^2=\text{approximation error}\le C_1\left(dN_1^{-4\beta_1}+\binom d2N_2^{-2\beta_2}\right)
\]
\[
V_n=\text{complexity}\le C_2\left(dN_1^2\log^2N_1\log(dN_1)+\binom d2N_2^2\log^2N_2\log(dN_2)\right).
\]''',r'''Consider the two-way interaction model as defined in equation (2.2) where each component functions $\{f_i\}_{i=1}^d$ and $\{f_{ij}\}_{1\le i<j\le d}$ belongs to $\Sigma(\beta,L)$ (see Assumption 2.3) and denote this collection of mean functions as $\mathcal F$. Then the minimax rate of estimation under Assumptions 2.1-2.3 is:
\[
\mathfrak M(n,d,\mathcal F)=\inf_{\widehat f}\sup_{\substack{f\in\mathcal F\\X\sim P_X}}\mathbb E_f\left[\left(\widehat f(X)-f(X)\right)^2\right]\ge c\left(dn^{-\frac{2\beta_1}{2\beta_1+1}}+\binom d2n^{-\frac{2\beta_2}{2\beta_2+2}}\right).
\]
for some constant $C$ independent of $(n,d)$.''',r'''Under Assumption 2.1-2.3 and 3.1 along with (3.6), the estimator obtained in (3.5) satisfes
\[
\|\widehat f-f_0\|_n^2=O_p\left(s_1\left(\rho_{n,1}^2+\lambda_{n,1}+\frac{\lambda_{n,1}^2}{2}\right)+s_2\left(\rho_{n,2}^2+\lambda_{n,2}+\frac{\lambda_{n,2}^2}{2}\right)\right)
\]
where $\rho_{n,1}$ (resp. $\rho_{n,2}$) is the approximation error of the univariate (resp. bivariate) components of the mean function by neural networks, bounded by (3.8), provided that
\[
\lambda_{n,1}=C_3\sqrt{\frac{V_{n,1}\log n}{n}+\frac{2\log d}{n}},\qquad\lambda_{n,2}=C_4\sqrt{\frac{V_{n,2}\log n}{n}+\frac{3\log d}{n}},\tag{3.7}
\]
with $V_{n,1}=N_1^2\log^3N_1$ and $V_{n,2}=N_2^2\log^3N_2$.''',r'''Consider the function $\widehat\phi$ defined by (3.5). Then, under the same assumptions as that of Theorem 3.2 along with Assumption 3.4, we have:
\[
\|\widehat f-f_0\|_n^2=O_p\left(s_1(\rho_{n,1}^2+\lambda_{n,1}^2)+s_2(\rho_{n,2}^2+\lambda_{n,2}^2)\right).\tag{3.16}
\]''',r'''Assume that the restricted strong convexity assumption (Assumption 3.4) holds with high probability on $\{X_1,\ldots,X_n\}$. Then, under Assumption 3.7, the estimator $\widehat f^{\mathrm{final}}$ satisfies, upto log-factors,
\[
\|\widehat f^{\mathrm{final}}-f_0\|_2^2=O_p\left(s_1\lambda_{n,1}^2+s_2\lambda_{n,2}^2\right).
\]
where $\lambda_{n,1}$ and $\lambda_{n,2}$ are same as in Theorem 3.5.''',r'''Suppose that we have $n$ observations from model (3.1). Then under Assumptions 2.2, 2.1 we have:
\[
\inf_{\widehat f}\sup_{\substack{f\in\mathcal F_{\mathrm{sp}}\\X\sim P_X}}\|\widehat f-f\|_2^2\gtrsim\left(s_1\left(n^{-\frac{2\beta_1}{2\beta_1+1}}\vee\frac{\log(d/s_1)}n\right)+s_2\left(n^{-\frac{2\beta_2}{2\beta_2+2}}\vee\frac{\log(d^2/s_2)}n\right)\right)
\]''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+(' (Main theorem)' if n=='2.9' else ''),source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — original statement'+(' continued' if j else '')) for j,p in enumerate(ps)]) for i,(n,ps,s) in enumerate(zip(NUMBERS,PAGES,STATEMENTS),1)]
    paper=dict(paper_id=PID,title='Deep neural networks for nonparametric interaction models with diverging dimension',authors=['Sohom Bhattacharya','Jianqing Fan','Debarghya Mukherjee'],version='arXiv:2302.05851v1, marked 12 Feb 2023',pdf_pages=46,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=23,main_text_boundary=dict(location='Section 5 main-text proof concludes on PDF page23, followed by Funding. References start at y650.386; evidence on23 is clipped at y645. Appendix A begins on26 according to the outline; appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerate actual small-cap THEOREM headings on pages1–23, clipping23 before references; visually compare all seven full statements, including the continuation of Theorem3.2 onto15. Exclude cited results, proof headings, lemmas, corollaries, remarks and appendices.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Verified registered local arXiv v1 PDF pinned by SHA256. Main-text Section5 is included; appendices excluded.',normalization_policy='Preserve original wording, formulas, all theorem clauses and printed titles. Normalize line wrapping and mathematical typesetting only. Retain the duplicated phi_2 infimum subscript in2.7, slash-form exponents, c/C mismatch in2.12, satisfes typo in3.2, phi-hat/f-hat change in3.5, upto log-factors qualification in3.8, and absent sampling expectation in3.9.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved seven complete main-text Theorems; independent inventory review remains separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
