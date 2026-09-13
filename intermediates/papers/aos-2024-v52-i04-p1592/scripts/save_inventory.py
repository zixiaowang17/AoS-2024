"""Rebuild all four complete original main-text theorem statements."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1592'
SHA='16810a1dcbde7957e273977a06255d6b5e043016acb7976583b2b1b86dc17ad4'
claims=[]
def claim(n,pages,text):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+n+', complete original statement') for p in pages]))
claim('3.1',[17],r'''
Let Assumptions I1–I3, D1–D4, E(A).1–E(A).4, and $E(B)_3$ hold and let $w(\cdot)$ be a continuously differentiable weight function on $\mathcal A$. Let $\sigma^2(\cdot)$ and $T_n$ be as given in (3.2) and (J.1). Then under $H_0$ (from (M.4)), we have
\[
d\{\mathcal L(T_n),\mathcal L(N(b_{0h},V))\}\to0\tag{3.3}
\]
as $n\to\infty$, where
\[
b_{0h}=h^{-1/2}K^{(2)}(0)\int_{\mathcal A}\frac{\sigma^2(a)w(a)}{\varpi_0(a)}\,da,\qquad
V=2K^{(4)}(0)\int_{\mathcal A}\left[\frac{\sigma^2(a)w(a)}{\varpi_0(a)}\right]^2\,da.\tag{3.4}
\]
''')
claim('3.2',[20],r'''
Let Assumptions I1–I3, D1–D4, E(A)1–E(A)4 hold and let $w(\cdot)$ be a continuously differentiable weight function on $\mathcal A$. Let $\sigma^2(\cdot)$ and $T_n$ be as given in (3.2) and (J.1). Then under the alternative $\theta_0(a)=c_0+\delta_n(n\sqrt h)^{-1/2}g(a)$, where $c_0=\mathbb P\xi(\boldsymbol Z;\pi_0,\mu_0)$, where $g(\cdot)$ is not the constant 0, and where $\int g(a)\varpi(a)w(a)\,da=0$. Moreover, $\delta_n$ is a sequence converging to $\infty$ such that $\lim_{n\to\infty}n^{1/40}/\delta_n=0$. Then we have
\[
P(T_n>z_{n,1-\alpha})\to1
\]
as $n\to\infty$, where we use $z_{n,1-\alpha}$ to denote the upper $\alpha$ quantile of the $N(b_{0h},V)$ distribution in (3.3).
''')
claim('3.3',[20],r'''
Let the assumptions of Theorem 3.1 hold. Let $T_n^*$ be the bootstrap test statistic defined in the paragraph preceding this theorem. Then
\[
d(\mathcal L^*(T_n^*),\mathcal L(N(b_h,V)))\to_p0
\]
as $n\to\infty$.
''')
claim('3.4',[21],r'''
Let the assumptions of Theorem 3.1 hold. Further, assume that $J_4(1,\mathcal F,L_2)<\infty$ for $\mathcal F=\mathcal F_\mu$ and for $\mathcal F=\mathcal F_\pi$. Let $T_n^*$ be the bootstrap test statistic defined in the paragraph preceding this theorem. Then
\[
d(\mathcal L^*(T_n^*),\mathcal L(N(b_h,V)))\to_p0
\]
as $n\to\infty$.
''')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='A nonparametric doubly robust test for a continuous treatment effect',authors=['Charles R. Doss','Guangwei Weng','Lan Wang','Ira Moscovice','Tongtan Chantarat'],version='arXiv:2202.03369v2, 22 May 2023; manuscript dated 23 May 2023',source_url='https://arxiv.org/pdf/2202.03369v2',pdf_pages=93,pdf_sha256=SHA,main_text_last_pdf_page=28,main_text_boundary=dict(location='Main paper ends with Acknowledgements on PDF page 28 before Appendix A, Empirical process lemmas, at y=201.71694946289062 PDF points. Evidence admits that page only above y=200.71694946289062. Appendix bodies and later references are excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Verified registered arXiv v2 PDF; pages 1-27 and the acknowledgements above Appendix A on page 28 only.'),papers=[paper],claims=claims),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
