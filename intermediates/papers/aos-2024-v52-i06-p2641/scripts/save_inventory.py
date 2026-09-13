"""Reproduce all five main-text Theorems from the registered arXiv v3 PDF."""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = next(p for p in ROOT.parents if (p / 'scripts/resolve_paper_pdf.py').is_file())
PID = 'aos-2024-v52-i06-p2641'
SHA = '75c32f603a25c35f73c4d498d58a074623bae8b97104a17fd2c99e293659d987'
URL = 'https://arxiv.org/pdf/2006.02611v3'
NUMBERS = ['3.1', '3.2', '3.3', '3.4', '3.5']
PAGES = [[11], [13], [13, 14], [22], [23]]
STATEMENTS = [r'''Suppose Assumption 1 holds. Let $h_0\le T/4$ and $P_k$, $\Theta_{k,0}$, $\Theta^*_{k,0}$ and $\lambda_k$ be as in (2.2), (3.1), (3.3) and (3.5) respectively. Let $R^{(0)}=\max_{1\le k\le K}R_k^{(0)}$ with the $R_k^{(0)}$ in (3.7), $R^{(TOPUP)}=\max_{1\le k\le K}R_k^{(TOPUP)}$ with the $R_k^{(TOPUP)}$ in (3.9), $R^{(ideal)}=\max_{1\le k\le K}R_k^{(ideal)}$ with the $R_k^{(ideal)}$ in (3.10), and $R^{(add)}=\max_{1\le k\le K}R_k^{(add)}$ with the $R_k^{(add)}$ in (3.11). Let $\widehat P_k^{(m)}=\widehat U_k^{(m)}\widehat U_k^{(m)\top}$ with the $m$-step estimator $\widehat U_k^{(m)}$ in the iTOPUP algorithm. Then, the following statements hold for a certain numerical constant $C_1^{(TOPUP)}$ and a constant $C_{1,K}^{(iter)}$ depending on $K$ only: When
\[
C_1^{(TOPUP)}R^{(0)}\le(1-\rho)/4\quad\text{and}\quad C_{1,K}^{(iter)}(R^{(ideal)}+R^{(add)})\le\rho
\]
(3.12)
with a constant $0<\rho<1$, it holds simultaneously for all $1\le k\le K$ and $m\ge0$ that
\[
\|\widehat P_k^{(m)}-P_k\|_{\mathrm S}\le2C_1^{(TOPUP)}\left((1-\rho^m)(1-\rho)^{-1}R^{(ideal)}+(\rho^m/2)R^{(TOPUP)}\right)
\]
(3.13)
in an event with probability at least $1-\sum_{k=1}^Ke^{-d_k}$. In particular, after at most $J=\lfloor\log(\max_k d_{-k}/r_{-k})/\log(1/\rho)\rfloor$ iterations,
\[
\overline{\mathbb E}\left[\max_{1\le k\le K}\|\widehat P_k^{(J)}-P_k\|_{\mathrm S}\right]\le\frac{3C_1^{(TOPUP)}}{1-\rho}R^{(ideal)}+\sum_{k=1}^Ke^{-d_k}.
\]
(3.14)''', r'''Suppose Assumption 1 holds. Let $P_k$, $\Theta^*_{k,0}$ and $\lambda_k^*$ be as in (2.2), (3.3) and (3.6) respectively. Let $h_0\le T/4$, and
\[
R^{*(0)}=\max_{1\le k\le K}R_k^{*(0)};\qquad R^{*(ideal)}=\max_{1\le k\le K}R_k^{*(ideal)},\qquad R^{*(add)}=\max_{1\le k\le K}R_k^{*(add)}.
\]
with $R_k^{*(0)}$ in (3.16), $R_k^{*(ideal)}$ in (3.17) and $R_k^{*(add)}$ in (3.18). Let $\widehat P_k^{(m)}=\widehat U_k^{(m)}\widehat U_k^{(m)\top}$ with the $m$-step estimator $\widehat U_k^{(m)}$ in iTIPUP algorithm. Then, the following statements hold for a certain numerical constant $C_1^{(TIPUP)}$ and a constant $C_{1,K}^{(iter)}$ depending on $K$ only: When
\[
C_1^{(TIPUP)}R^{*(0)}\le\min_{1\le k\le K}\frac{(1-\rho)\lambda_k^{*2}}{8\|\Theta^*_{k,0}\|_{\mathrm S}}\quad\text{and}\quad C_{1,K}^{(iter)}(R^{*(ideal)}+R^{*(add)})\le\rho
\]
(3.19)
with a constant $0<\rho<1$, it holds simultaneously for all $1\le k\le K$ and $m\ge0$ that
\[
\|\widehat P_k^{(m)}-P_k\|_{\mathrm S}\le2C_1^{(TIPUP)}\left((1-\rho^m)(1-\rho)^{-1}R^{*(ideal)}+(\rho^m/2)R^{*(0)}\right)
\]
(3.20)
in an event with probability at least $1-\sum_{k=1}^Ke^{-d_k}$. In particular, after at most $J=\lfloor\log(\max_k d_{-k}/r_{-k})/\log(1/\rho)\rfloor$ iterations,
\[
\overline{\mathbb E}\left[\max_{1\le k\le K}\|\widehat P_k^{(J)}-P_k\|_{\mathrm S}\right]\le\frac{3C_1^{(TIPUP)}}{1-\rho}R^{*(ideal)}+\sum_{k=1}^Ke^{-d_k}.
\]
(3.21)''', r'''Assumption 1 holds. Let $R^{(0)}$, $R^{(ideal)}$ and $R^{(add)}$ be as in Theorem 3.1 and $R^{*(0)}$ be as in Theorem 3.2. Let $\widehat P_k^{(m)}=\widehat U_k^{(m)}\widehat U_k^{(m)\top}$ with $\widehat U_k^{(m)}$ being the $m$-step estimator in the TIPUP-iTOPUP algorithm. Then, the following statement holds for a certain numerical constant $C_1^{(TOPUP)}$ and a constant $C_{1,K}^{(iter)}$ depending on $K$ only: When
\[
C_1^{(TOPUP)}R^{*(0)}\le(1-\rho)/4\quad\text{and}\quad C_{1,K}^{(iter)}(R^{(ideal)}+R^{(add)})\le\rho
\]
(3.22)
with a constant $0<\rho<1$, it holds in an event with probability at least $1-\sum_{k=1}^Ke^{-d_k}$ that simultaneously for all $1\le k\le K$ and $m\ge0$
\[
\|\widehat P_k^{(m)}-P_k\|_{\mathrm S}\le2C_1^{(TOPUP)}\left((1-\rho^m)(1-\rho)^{-1}R^{(ideal)}+(\rho^m/2)R^{*(0)}\right).
\]''', r'''Suppose that Hypothesis I holds for some $0<\delta<1/2$ and $d^{1/K}\asymp d_k\ge T$ and $r_k$ is fixed for all $1\le k\le K$. If, for some $\vartheta>0$,
\[
\liminf_{T\to\infty}\frac{\sigma^2d^{1/2-\vartheta}}{T^{1/2}\lambda^2}>0,
\]
(3.36)
then for any randomized polynomial-time estimators $\widehat U_k=\widehat U_k(\mathcal X_1,\ldots,\mathcal X_T)$, $1\le k\le K$,
\[
\liminf_{T\to\infty}\sup_{\mathcal X_1,\ldots,\mathcal X_T\in\mathscr P(T,d_1,\ldots,d_K,\lambda)}\mathbb P\left(\min_{1\le k\le K}\|\widehat P_k-P_k\|_{\mathrm S}^2>\frac13\right)>\frac14,
\]
(3.37)
where $\widehat P_k=\widehat U_k\widehat U_k^\top$ and $P_k=U_kU_k^\top$.''', r'''Suppose $\lambda>0$ and $d_k\to\infty$ as $T\to\infty$ for all $1\le k\le K$. Then there exists a universal constant $c>0$ such that for $T$ sufficiently large,
\[
\inf_{\widehat U_k}\sup_{\mathcal X_1,\ldots,\mathcal X_T\in\mathscr P(T,d_1,\ldots,d_K,\lambda)}\mathbb E\|\widehat P_k-P_k\|_{\mathrm S}\ge c\min\left(1,(\sigma^2+\sigma\lambda)\sqrt{d_k}\big/(\lambda^2\sqrt{Tr_{-k}})\right)
\]
(3.38)
for all $1\le k\le K$, where $\widehat P_k=\widehat U_k\widehat U_k^\top$ and $P_k=U_kU_k^\top$.''']

def inventory():
    claims = [dict(claim_id=PID+'/T'+n, paper_id=PID, claim_kind='theorem', label='Theorem '+n, source_order=i, statement_original=s, evidence=[dict(page=p, location='Theorem '+n+' — '+('complete original statement' if len(pages)==1 else 'original statement '+('start' if j==0 else 'continuation and conclusion'))) for j,p in enumerate(pages)]) for i,(n,pages,s) in enumerate(zip(NUMBERS,PAGES,STATEMENTS),1)]
    paper = dict(paper_id=PID, title='Tensor factor model estimation by iterative projection', authors=['Yuefeng Han','Rong Chen','Dan Yang','Cun-Hui Zhang'], version='arXiv:2006.02611v3, marked 18 Jul 2024', pdf_pages=58, pdf_sha256=SHA, source_url=URL, main_text_last_pdf_page=24, main_text_boundary=dict(location='Summary and acknowledgements end on PDF page 24 before REFERENCES at y650.489; evidence clipped at y644. Page 24 is shared with references, not an appendix. Supplementary simulation material starts on PDF page 28; all supplementary bodies are excluded.', shared_page_with_appendix=False), intake_review=dict(status='complete', theorem_ids=[c['claim_id'] for c in claims], zero_theorems_confirmed=False, method='Independently enumerate actual small-cap THEOREM headings in pages 1–24, clipping page 24 before references. Visually compare all five statements, including Theorem 3.3 across pages 13–14. Exclude Propositions, Corollaries, Lemma 4.1, remarks, references to theorems, and supplementary material.'))
    return dict(schema_version='statistical-theorem-inventory-v1', scope=dict(paper_count=1, theorem_scope='main_text_only', source_policy='Verified registered local arXiv v3 PDF pinned by SHA-256; main text only, excluding supplementary bodies.', normalization_policy='Preserve all five complete original statements, numbering, hypotheses, formulas and quantifiers; normalize wrapping and mathematical typesetting only. Preserve conditional expectation in Theorems 3.1–3.2, floor iteration counts, starred versus unstarred rates, joint events over all iterations and modes, the minimum and squared norm in Theorem 3.4, and the unsquared norm in Theorem 3.5.'), papers=[paper], claims=claims)

def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved five complete main-text Theorems; independent inventory review remains separate.')

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output-dir',type=Path); args=parser.parse_args()
    if args.output_dir: ROOT=args.output_dir.resolve()
    main()
