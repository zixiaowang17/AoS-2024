"""Reproduce all three complete main-text Theorems from the registered arXiv v3 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2714'
SHA='d9415db3f063bab2fad33909ef2e4c13027032c29660f9b505a4a6340b3479ea'
URL='https://arxiv.org/pdf/2301.03038v3'
NUMBERS=['2.1','4.1','4.5']
PAGES=[11,22,25]
STATEMENTS=[r'''Let $h=\delta_n^{-1}(\theta-\theta_*)$, and define $M_n=\sqrt{c_0\log\delta_n^{-1}}$, with $c_0>0$. Then, under Assumptions 1–4, if $\theta_*$ is an inner point of $\Theta$, it holds
\[
\|\Pi_n(\cdot)-P_{\mathrm{SKS}}^n(\cdot)\|_{\mathrm{TV}}=O_{P_0^n}(M_n^{c_3}\delta_n^2),\tag{8}
\]
where $c_3>0$, and $P_{\mathrm{SKS}}^n(\cdot)$ is the cdf of the SKS density $p_{\mathrm{SKS}}^n(h)$ in (1) with parameters
\[
\xi=\Delta_{\theta_*}^n+\delta_n(V_{\theta_*}^n)^{-1}\log\pi^{(1)},\qquad\Omega^{-1}=[v_{st}^n-\delta_na_{\theta_*,stl}^{(3),n}\xi_l],
\]
\[
\alpha_\eta(h-\xi)=(\delta_n/12\eta)a_{\theta_*,stl}^{(3),n}\{(h-\xi)_s(h-\xi)_t(h-\xi)_l+3(h-\xi)_s\xi_t\xi_l\}.
\]
The function $F(\cdot)$ entering the definition of $p_{\mathrm{SKS}}^n(h)$ in (1) is any univariate cdf which satisfies $F(-x)=1-F(x)$ and $F(x)=1/2+\eta x+O(x^2)$, for some $\eta\in\mathbb R$, when $x\to0$.''',r'''Let $\widehat h=\sqrt n(\theta-\widehat\theta)$, and define $M_n=\sqrt{c_0\log n}$, with $c_0>0$. If Assumptions 1, 7–8, and 9–10 are met, then the posterior for $\widehat h$ satisfies
\[
\|\Pi_n(\cdot)-\widehat P_{\mathrm{SKS}}^n(\cdot)\|_{\mathrm{TV}}=O_{P_0^n}\left(M_n^{c_8}/n\right),\tag{23}
\]
for some $c_8>0$, where $\widehat P_{\mathrm{SKS}}^n(S)=\int_S\widehat p_{\mathrm{SKS}}^n(\widehat h)\,\mathrm d\widehat h$ for $S\subset\mathbb R^d$ with $\widehat p_{\mathrm{SKS}}^n(\widehat h)$ defined as in (22). In addition, let $G:\mathbb R^d\to\mathbb R$ be a function satisfying $|G(\widehat h)|\lesssim\|\widehat h\|^r$. If the prior is such that $\int\|\widehat h\|^r\pi(\widehat\theta+\widehat h/\sqrt n)\,\mathrm d\widehat h<\infty$ then
\[
\int G(\widehat h)|\pi_n(\widehat h)-\widehat p_{\mathrm{SKS}}^n(\widehat h)|\,\mathrm d\widehat h=O_{P_0^n}(M_n^{c_8+r}/n).\tag{24}
\]''',r'''Let $\Pi_{n,C}(S)=\int_S\pi_{n,C}(\widehat h_C)\,\mathrm d\widehat h_C$ for $S\subset\mathbb R^{d_C}$. Then, under the assumptions of Theorem 4.1, we have that
\[
\|\Pi_{n,C}(\cdot)-\widehat P_{\mathrm{SKS},C}^n(\cdot)\|_{\mathrm{TV}}=O_{P_0^n}\left(M_n^{c_9}/n\right),\tag{32}
\]
for $c_9>0$, where $\widehat P_{\mathrm{SKS},C}^n(S)=\int_S\widehat p_{\mathrm{SKS},C}^n(\widehat h_C)\,\mathrm d\widehat h_C$ with $\widehat p_{\mathrm{SKS},C}^n(\widehat h_C)$ defined as in (31).''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement')]) for i,(n,p,s) in enumerate(zip(NUMBERS,PAGES,STATEMENTS),1)]
    paper=dict(paper_id=PID,title='Skewed Bernstein–von Mises theorem and skew-modal approximations',authors=['Daniele Durante','Francesco Pozza','Botond Szabo'],version='arXiv:2301.03038v3, marked 8 Apr 2024',pdf_pages=54,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=29,main_text_boundary=dict(location='Discussion continues onto PDF page29 and ends before REFERENCES at y248.679. Evidence on29 is clipped at y242. Supplementary Proofs of Lemmas, Theorems and Corollaries begin on32 according to the outline; all supplementary bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Independently enumerate actual small-cap THEOREM headings on pages1–29, clipping29 before references, and visually compare all three complete statements. Exclude remarks, lemmas, corollaries, prose mentions and supplementary results.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Verified registered local arXiv v3 PDF pinned by SHA256. Main text includes the final discussion on29; supplementary bodies are excluded.',normalization_policy='Preserve all three original theorem statements, hypotheses, formulas and both parts of Theorem4.1. Normalize line wrapping and mathematical typesetting only. Preserve subscript theta_*, Einstein-index notation, eta in R including its unresolved zero case, signed G times the absolute density difference, and the printed numbering4.5.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved three complete main-text Theorems; independent inventory review remains separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
