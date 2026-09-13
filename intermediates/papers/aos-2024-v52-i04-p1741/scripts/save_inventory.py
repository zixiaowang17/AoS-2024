"""Reproduce seven complete original Theorems transcribed from the registered PDF.

Running this script preserves a reviewed extraction; it does not conduct a new
mathematical source review. Appendix and supplementary results are excluded.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1741'
SHA='4610424fb82ecdd4bb95f29d0e675272d01dc3a33fae493aa47959a85c9a7a2c'
URL='https://projecteuclid.org/journals/annals-of-statistics/volume-52/issue-4/Efficient-functional-Lasso-kernel-smoothing-for-high-dimensional-additive-regression/10.1214/24-AOS2415.pdf'
STATEMENTS=[r'''Suppose that $R<\infty$ and that there exists $q_0>0$ such that any tuple $\eta=(\eta_1,\ldots,\eta_d)$ with $\int_0^1\eta_j(x_j)\widehat p_j(x_j)dx_j=0$ satisfies
\[
\left\|\sum_{j=1}^d\eta_j\right\|_{\widehat p}^2\leq q_0^2\sum_{j=1}^d\|\eta_j\|_{\widehat p}^2.
\]
(2.16)
Then, for all $r\geq1$, it holds that
\[
L_n^{\mathrm{pen}}(\widehat{\mathbf f}^{(r)})-L_n^{\mathrm{pen}}(\widehat{\mathbf f})\leq\frac{2R^2(1+q_0)^2}{r}\cdot\max\left\{\frac1{2R^2(1+q_0)^2}-1,L_n^{\mathrm{pen}}(\widehat{\mathbf f}^{(0)})-L_n^{\mathrm{pen}}(\widehat{\mathbf f}),2\right\}.
\]''',
r'''Assume that (A1)–(A6) hold and that $\phi>0$ for all $d$. Let the bandwidth size $h$ in the assumption (A5) be chosen so that
\[
\frac{|S|}{\phi\wedge1}\cdot\sqrt{\frac{\log(d\vee n)}{n}}\ll h\ll\frac{\phi^2\wedge1}{|S|^2},
\]
(2.20)
and the penalty parameter $\lambda$ satisfy $\lambda\geq2C_1(\sqrt{\log(d\vee n)/(nh)}+h^{3/2})$. Then, it holds that
\[
\sum_{j=1}^d\|\widehat f_j-f_j\|_p\lesssim|S|\left(\frac\lambda\phi+h^2+\sqrt{\frac{\log(|S|\vee n)}{n}}\right).
\]''',
r'''Assume that (A1)–(A7) hold and that $\phi$ is bounded away from zero. Also, let the bandwidth size $h$ satisfy (2.20), and the penalty constant $\lambda$ fulfill (2.21). Then, it holds that
\[
\max_{1\leq j\leq d}\|\widehat f_j^{\mathrm{de}}-f_j\|_p\lesssim\left(\sqrt{\frac{\log(d\vee n)}{nh}}+h^{3/2}\right)(1+s_1).
\]''',
r'''Assume that the conditions of Theorem 3 hold. Let $h$ and $\lambda$ satisfy (2.20) and (2.21), respectively. In addition, suppose that
\[
h\ll\min\left\{\frac{n^{-1/5}}{|S|^{2/5}(1+s_1)^{2/5}},\frac1{|S|^2(1+s_1)^2},\frac1{\sqrt{\log(d\vee n)}}\cdot\frac1{|S|(1+s_1)}\right\}.
\]
(3.11)
Then, for each $1\leq j\leq d$ and for each fixed $x_j\in(0,1)$, it holds that
\[
\sqrt{nh_j}\bigl(\widehat f_j^{\mathrm{de}}(x_j)-f_j(x_j)\bigr)=\sqrt{nh_j}(I_j+\widehat\Theta_j)(\widehat{\mathbf m}^{A})(x_j)+o_p(1).
\]''',
r'''Assume that the conditions of Theorem 3 hold. Let $h$ and $\lambda$ satisfy (2.20) and (2.21), respectively. In addition, suppose that $(1+s_1^2)nh^3\to0$ as $n\to\infty$. Then, it holds that
\[
\max_{1\leq j\leq d}\sup_{x_j\in[0,1]}\sqrt{nh_j}\left|\widehat f_j^{\mathrm{de}}(x_j)-f_j(x_j)-(I_j+\widehat\Theta_j)(\widehat{\mathbf m}^{A})(x_j)\right|=o_p(1).
\]''',
r'''Assume that (A1), (A2), (A4), (A5) and (A7) hold. Then, we have $\max_{1\leq j\leq d}\|\widehat\Theta_j-\Theta_j\|_{1,\max}\lesssim\gamma s_1$. Furthermore, under the additional assumption that $\max_{1\leq j,k\leq d}\sup_{u_j\in[0,1]}\int_0^1\Theta_{jk}''(u_j,x_k)^2dx_k\lesssim1$ and with the additional constraint that $\max_{1\leq j,k\leq d}\sup_{u_j\in[0,1]}\int_0^1\Xi_{jk}''(u_j,x_k)^2dx_k\lesssim1$ in the optimization at (3.7), it holds that
\[
\max_{1\leq j,k\leq d}\|\widehat\Theta_{jk}-\Theta_{jk}\|_\infty\lesssim(\gamma s_1)^{3/4},\qquad\max_{1\leq j\leq d}\sum_{k=1}^d\|\widehat\Theta_{jk}-\Theta_{jk}\|_\infty\lesssim s_q(\gamma s_1)^{3(1-q)/4}
\]
for all $q\in[0,1]$, where $s_q:=\max_{1\leq j\leq d}\sum_{k=1}^d\|\Theta_{jk}\|_\infty^q$.''',
r'''Assume that there exist $q\in(0,1]$, $\alpha\in(0,1)$ and $\beta>0$ such that, after some permutation of the indices $1,\ldots,d$, it holds that
\[
\|(p_{jk}-p_jp_k)/p_j\|_\infty\leq c_q(\alpha,\beta)\cdot\alpha^{|j-k|}
\]
(4.1)
for all $1\leq j\ne k\leq d$. Then, $s_q\vee s_q^*\leq\beta$.''']
PAGES=[8,11,16,16,17,18,18]
def inventory():
    claims=[dict(claim_id=f'{PID}/T{i}',paper_id=PID,claim_kind='theorem',label=f'Theorem {i}',source_order=i,statement_original=s,evidence=[dict(page=p,location=f'Theorem {i}; complete statement ending before the following commentary.')]) for i,(s,p) in enumerate(zip(STATEMENTS,PAGES),1)]
    paper=dict(paper_id=PID,title='Efficient functional Lasso kernel smoothing for high-dimensional additive regression',authors=['Eun Ryung Lee','Seyoung Park','Enno Mammen','Byeong U. Park'],version='Published version, The Annals of Statistics 52(4), 2024, pp. 1741-1773',pdf_pages=33,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=25,
        main_text_boundary=dict(location='Conclusion continues from PDF page 24 onto page 25 and ends with "The latter seems to be also a promising avenue for future research." Appendix heading starts at y=205.598 points on page 25. Retained page-25 evidence is clipped above y=204.59; appendix and subsequent material are excluded.',shared_page_with_appendix=True),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Independent enumeration of actual small-cap Theorem headings on main-text pages 1–25, with page 25 clipped before the appendix; visual comparison of all seven complete statements. Propositions, unnumbered consequences and theorem citations are excluded.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Verified registered published PDF; retain main text only, including the conclusion above the appendix heading on page 25.',normalization_policy='Preserve original theorem wording, formulas, branches and quantifiers; normalize PDF line wrapping and mathematical typography only.',semantic_ranking_policy='All main-text Theorems, without selection by importance.',build_order_policy='Source-backed paper-local dependencies after independent inventory validation.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
