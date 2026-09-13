"""Reproduce all eleven original main-text Theorems from the registered PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2767'
SHA='cdd4ca38815c06e49f1af375f06ec2da68b5b7db6c043b718bd3fc87e46ee8e4'
URL='https://arxiv.org/pdf/2201.04315v2'
NUMBERS=['4.5','4.6','5.2','5.5','6.2','6.3','6.4','6.5','7.1','7.2','7.3']
PAGES=[[13],[14],[15],[15],[18],[18,19],[19],[20],[21],[22],[22]]
STATEMENTS=[r'''If the exponential family $\mathcal P$ satisfies Assumptions 1 and 2 with $k=3$, then for $\theta\in\Theta$, it holds that
\[
\varepsilon^\star(\mathcal P,n,m)\le\|\mathcal L(T_n)-\mathcal L(T_{n+m})\|_{\mathrm{TV}}\le\frac C{\sqrt n}+\frac{m\sqrt d}n,
\]
where $C<\infty$ is an absolute constant depending only on $d$ and the moment upper bound in Assumption 2. In particular, for sufficiently large $n$, a sample amplification of size $\Omega(n/\sqrt d)$ is achievable.''',r'''Let $(\mathcal X,\mathcal P=(P_\theta)_{\theta\in\Theta})$ be a product exponential family, where each one-dimensional component satisfies Assumptions 1 and 2 with $k=10$. Then for $\theta\in\Theta$, it holds that
\[
\varepsilon^\star(\mathcal P,n,m)\le\|\mathcal L(T_n)-\mathcal L(T_{n+m})\|_{\mathrm{TV}}\le C\left(\frac d{n^2}+\frac{m\sqrt d}n\right),
\]
where $C<\infty$ is an absolute constant independent of $(n,d)$. In particular, as long as $n=\Omega(\sqrt d/\varepsilon)$, an $(n,n+m,\varepsilon)$ sample amplification of size $m=\Omega(n\varepsilon/\sqrt d)$ is achievable.''',r'''For general $\mathcal P$ and $n,m\ge0$, it holds that
\[
\varepsilon^\star(\mathcal P,n,m)\le\sqrt{\frac{m^2}n\cdot r_{\chi^2}(\mathcal P,n/2)}.
\]''',r'''For $\mathcal P=\prod_{j=1}^d\mathcal P_j$ and $n,m\ge0$, it holds that
\[
\varepsilon^\star(\mathcal P,n,m)\le\sqrt{\frac{m^2}n\sum_{j=1}^dr_{\chi^2}(\mathcal P_j,n/2)}.
\]''',r'''For the Gaussian location model $\mathcal P=\{\mathcal N(\theta,\Sigma)\}_{\theta\in\mathbb R^d}$ with a fixed covariance $\Sigma\in\mathbb R^{d\times d}$, the minimax error of sample amplification in (4) is exactly
\[
\varepsilon^\star(\mathcal P,n,m)=\left\|\mathcal N\left(0,\frac{I_d}n\right)-\mathcal N\left(0,\frac{I_d}{n+m}\right)\right\|_{\mathrm{TV}}.
\]
In particular, the sufficiency-based approach in Example 4.1 is exactly minimax optimal.''',r'''Given a $d$-dimensional exponential family $\mathcal P$ satisfying Assumptions 1 and 3, for every $n,m\in\mathbb N$, the minimax error of sample amplification satisfies
\[
\varepsilon^\star(\mathcal P,n,m)\ge c\cdot\left(\frac{m\sqrt d}n\wedge1\right)-C\cdot\left(\frac{\log n}n\right)^{1/3},
\]
where $c>0$ is an absolute constant independent of $(n,m,d,\mathcal P)$, and constant $C>0$ depends only on the exponential family (and thus on $d$).''',r'''Let $\varepsilon\in(0,1)$ and $P_\theta=\prod_{j=1}^dp_{\theta_j}$ be a product model with $(\theta_1,\ldots,\theta_d)\in\prod_{j=1}^d\Theta_j$. Suppose for each $j\in[d]$, there exist two points $\theta_{j,+},\theta_{j,-}\in\Theta_j$ such that
\[
\|p_{\theta_{j,+}}^{\otimes n}-p_{\theta_{j,-}}^{\otimes n}\|_{\mathrm{TV}}\le\alpha_j-\frac\varepsilon{\sqrt d},\tag{10}
\]
\[
\|p_{\theta_{j,+}}^{\otimes(n+m)}-p_{\theta_{j,-}}^{\otimes(n+m)}\|_{\mathrm{TV}}\ge\alpha_j+\frac\varepsilon{\sqrt d},\tag{11}
\]
with $\alpha_j\in(\underline\alpha,\overline\alpha)$, where $\underline\alpha,\overline\alpha\in(0,1)$ are absolute constants. Then there exists an absolute constant $c=c(\underline\alpha,\overline\alpha)>0$ such that
\[
\varepsilon^\star(\mathcal P,n,m)\ge c\varepsilon.
\]''',r'''Let $\mathcal P$ be a product model satisfying Assumption 4. Then for any $c>0$, there is some $c'>0$ depending only on $c$ (thus independent of $n,d,\varepsilon,\mathcal P$) such that
\[
\varepsilon^\star\left(\mathcal P,n,\left\lceil\frac{c\varepsilon n}{\sqrt d}\right\rceil\right)\ge c'\varepsilon.
\]''',r'''For the class $\mathcal P_{d,t}$ with $t\in[1/(2\sqrt d),1/2]$, an $(n,n+1,0.1)$ sample amplification is possible if and only if
\[
n=\Omega\left(\frac1t\right).
\]''',r'''For the above low-rank covariance estimation model with $p\ge d+1$, an $(n,n+1,0.1)$ sample amplification is possible if and only if $n\ge d$.''',r'''Let $L\ge8$ and $c\in(0,1)$ be fixed. It holds that
\[
m^\star(\mathcal P_c,n)\asymp n^{5/6},\qquad\text{while}\qquad m^\star(\mathcal P,n)\lesssim n^{3/4}.
\]''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — original statement'+(' continued' if j else '')) for j,p in enumerate(ps)]) for i,(n,ps,s) in enumerate(zip(NUMBERS,PAGES,STATEMENTS),1)]
    paper=dict(paper_id=PID,title='On the statistical complexity of sample amplification',authors=['Brian Axelrod','Shivam Garg','Yanjun Han','Vatsal Sharan','Gregory Valiant'],version='arXiv:2201.04315v2, stamped 18 Sep 2024; title-page date 19 Sep 2024',pdf_pages=62,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=22,main_text_boundary=dict(location='Section7.3 concludes on PDF page22, followed by Acknowledgements and Funding ending with a Simons Foundation Investigator Award. Appendix A starts on23 according to the outline; all appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Independently enumerate bold CMBX10 Theorem headings on pages1–22, excluding prose mentions, tables, references, lemmas, examples and corollaries. Visually compare all eleven complete original statements, including6.3 continuation on19.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local arXiv v2 PDF pinned by SHA256. Main text through22; appendices excluded.',normalization_policy='Preserve all eleven original statements, formulas, constants, quantifiers and final clauses. Normalize line wrapping and mathematical typesetting only. Keep the pointwise-looking middle TV terms in4.5/4.6, n,m>=0 in5.2/5.5 despite division by n, constant dependencies in6.3, ceiling in6.5 and asymptotic if-and-only-if wording in7.1.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved eleven original main-text Theorems; independent review remains separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
