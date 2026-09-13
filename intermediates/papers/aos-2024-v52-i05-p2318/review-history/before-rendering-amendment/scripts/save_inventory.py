"""Reproduce all seven complete main-text Theorems from the registered graphon PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2318'
SHA='7bcc38eb8b952de996d7b08259295d5e2a91f94a7081aab2c7dedec225a52275'
URL='https://arxiv.org/pdf/2308.15728v4'
NUMBERS=['1','2','3','4','5','6','7']
STATEMENTS=[r'''Suppose $2\le k\le\sqrt n$. For any $D\ge1$, there exists a universal constant $c>0$ such that
\[
\inf_{\widehat M\in\mathbb R[A]_{\le D}^{n\times n}}\sup_{M\in\mathcal M_k}\mathbb E(\ell(\widehat M,M))\ge\frac{ck}{nD^4}.
\]
(6)
Here the notation $\widehat M\in\mathbb R[A]_{\le D}^{n\times n}$ means that for all $(i,j)\in[n]\times[n]$, $\widehat M_{ij}$ is a polynomial of $A$ with degree no more than $D$.''',r'''For any $0<r<1$ and $D\ge1$, if
\[
\frac{(p-q)^2}{q(1-p)}\le\frac{r}{(D(D+1))^2}\left(\frac{k^2}{n}\wedge1\right),
\]
(14)
then we have
\[
\inf_{\widehat M\in\mathbb R[A]_{\le D}^{n\times n}}\mathbb E_{A,M\sim\mathbb P_{\mathrm{SBM}(p,q)}}(\ell(\widehat M,M))\ge\frac{(p-q)^2}{k}-(p-q)^2\left(\frac1{k^2}+\frac{r(2-r)}{(1-r)^2n}\right).
\]
(15)
Here the notation $\widehat M\in\mathbb R[A]_{\le D}^{n\times n}$ means that for all $(i,j)\in[n]\times[n]$, we have $\widehat M_{ij}\in\mathbb R[A]_{\le D}$.''',r'''Take $r=2k$, $t_1=t_2=C'\log n$ and the stepsize of GD to be
\[
\eta=\frac1{C''\left(\left(\frac{n(p-q)}k+C''\sqrt n\right)^{2t_1}k\vee(C''n)^{t_1+1}\right)}
\]
for some large $C',C''>0$ in Algorithm 1. Then there exist $c,C,\bar C>0$ depending only on $C',C''$ such that when $n\ge Ck\log^3n$, we have with $\mathbb P_{\mathrm{SBM}(p,q)}$-probability at least $1-n^{-\bar C}$, the $\widehat M$ in Algorithm 1 satisfies $\ell(\widehat M,M)\le\frac{c(k+\log n)\log^2n}{n}$.''',r'''Suppose $\gamma>0.5$. For any $D\ge1$, there exists $c>0$ only depending on $L$ and $\gamma$ such that
\[
\inf_{\widehat M\in\mathbb R[A]_{\le D}^{n\times n}}\sup_{f\in\mathcal F_\gamma(L)}\sup_{\mathbb P_\xi}\mathbb E\left(\ell(\widehat M,M_f)\right)\ge cn^{-\frac{2\gamma+1}{2\gamma+2}}/D^4.
\]''',r'''For any $D\ge1$, suppose
\[
\frac{(p-q)^2}{q(1-p)}\le\frac1{2(D(D+1))^2}\left(\frac{k^2}{n}\wedge1\right),
\]
then
\[
\inf_{\widehat Z\in\mathbb R[A]_{\le D}^{n\times n}}\mathbb E_{A,M\sim\mathbb P_{\mathrm{SBM}(p,q)}}(\ell(\widehat Z,Z_M))\ge\frac1k-\frac1{k^2}-\frac3n.
\]
(24)
In particular, when $k\le\sqrt n$ and
\[
\frac{n(p-q)^2}{k^2q(1-p)}\le\frac1{2(D(D+1))^2},
\]
(25)
the lower bound (24) holds.''',r'''Suppose $2\le k\le\sqrt n$ and $\rho\ge\frac{ck^2}{n}$ for some small $0<c<1$. Then for any $D\ge1$, there exists a universal constant $c'>0$ such that
\[
\inf_{\widehat M\in\mathbb R[A]_{\le D}^{n\times n}}\sup_{M\in\mathcal M_{k,\rho}}\mathbb E(\ell(M,\widehat M))\ge\frac{c'\rho k}{nD^4}.
\]''',r'''For any $0<r<1$ and $D\ge1$, if
\[
\lambda^2\le\frac{r}{(D(D+1))^2}\min\left(1,\frac{k_1^2\wedge k_2^2}{n_1\vee n_2}\right)
\]
(28)
holds, then
\[
\inf_{\widehat M\in\mathbb R[Y]_{\le D}^{n_1\times n_2}}\mathbb E_{Y,M\sim\mathbb P_{\mathrm{BC}(\lambda)}}(\ell(\widehat M,M))\ge\frac{\lambda^2}{k_1\wedge k_2}-\left(\frac{\lambda^2}{k_1^2\wedge k_2^2}+\frac{r(2-r)\lambda^2}{(1-r)^2(n_1\vee n_2)}\right).
\]
(29)''']
def inventory():
    pages=[[4],[10],[12,13],[14],[16],[17],[18]]
    cs=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement'+(' across pages 12–13' if n=='3' else '')) for p in pp]) for i,(n,s,pp) in enumerate(zip(NUMBERS,STATEMENTS,pages),1)]
    paper=dict(paper_id=PID,title='Computational lower bounds for graphon estimation via low-degree polynomials',authors=['Yuetian Luo','Chao Gao'],version='arXiv:2308.15728v4; 12 Aug 2024',pdf_pages=58,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=27,main_text_boundary=dict(location='Main-text Section 7 proof ends on PDF page 27 before References at y=251.06. Page-27 evidence clipped at y=244. References and all appendix bodies excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in cs],zero_theorems_confirmed=False,method='Enumerate every bold Theorem environment across all main-text pages; seven labels 1–7. T3 heading splits into two spans and its statement continues on PDF page13. Exclude Corollaries, Propositions, Definitions, Remarks and proof citations.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered local hash-verified arXiv v4; appendix bodies excluded.',normalization_policy='Preserve original wording, quantifiers, formulas and all subparts. Normalize line wrapping and mathematical typesetting. Visual PDF fixes the text-layer misreading of primed constants as numeric subscripts in T3 and T6.'),papers=[paper],claims=cs)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved all seven complete main-text Theorems; independent source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
