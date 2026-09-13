"""Reproduce all five original main-text Theorems from the registered arXiv v2 PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i06-p2692'
SHA='7244d5d4a662bc47b902b98a29ba176ffc566951f35346982a8009c0514c4934'
URL='https://arxiv.org/pdf/2205.12112v2'
NUMBERS=['2.1','2.2','4.1','5.1','5.2']
PAGES=[7,9,14,19,20]
STATEMENTS=[r'''If $\pi(x)$ is positive and continuous in $\mathbb R^d$, then SPS is uniformly ergodic if and only if
\[
\sup_{x\in\mathbb R^d}\pi(x)(R^2+\|x\|^2)^d<\infty.\tag{5}
\]''',r'''If $\pi(x)$ is positive in $\mathbb R^d$ with continuous first derivative in all components, then SBPS is uniformly ergodic if
\[
\limsup_{\{x:\|x\|\to\infty\}}\sum_{i=1}^d\left(\frac{\partial\log\pi(x)}{\partial x_i}x_i\right)+2d<\frac12.
\]''',r'''Assume there exist constants $C<\infty$ and $c>0$ such that $c\le\lambda_i\le C$ and $|\mu_i|\le C$ for all $i=1,\ldots,d$. Furthermore, assume $R=d^{1/2}$ and
\[
\left|\sum_{i=1}^d\mu_i^2-\sum_{i=1}^d(1-\lambda_i)\right|=O(d^\alpha),\tag{10}
\]
where $\alpha\le1$. Then, under stationarity that $X\sim\pi$, the expected acceptance probability converges to $1$ as $d\to\infty$
\[
\mathbb E_{X\sim\pi_{\mu,\Sigma}}\mathbb E_{\widehat X\mid X}\left[1\wedge\frac{\pi_{\mu,\Sigma}(\widehat X)(R^2+\|\widehat X\|^2)^d}{\pi_{\mu,\Sigma}(X)(R^2+\|X\|^2)^d}\right]\to1,
\]
for all $h$ such that
\[
h=o\left(\frac{d^{-1}}{\sqrt{\max\{\frac1d\sum_i|1-\lambda_i|,\frac1d\sum_i\mu_i^2\}}}\wedge d^{-(\frac12\vee\alpha)}\right).\tag{11}
\]''',r'''Under the assumptions on the target in Section 5.1, suppose $f$ is not the standard Gaussian density, the SPS chain is in the stationary phase, and the radius parameter is chosen as $R=\sqrt d$ and re-parameterize $h$ by $\ell$ according to Eq. (15) with $\lambda=1$. Then, as $d\to\infty$, we have $\mathrm{ESJD}\to2\ell^2\cdot\Phi\left(-\frac\ell2\sqrt{\mathbb E_f\left[((\log f)')^2\right]-1}\right)$.''',r'''Under the assumptions on $\pi$ in Section 5.1, suppose $f$ is not the standard Gaussian density and the RSPS chain $\{X^d(t)\}$ starts from the stationarity, i.e. $X^d(0)\sim\pi$, and the radius parameter is chosen as $R=\sqrt d$. Writing $X^d(t)=(X_1^d(t),\ldots,X_d^d(t))$, we let $U^d(t):=X_1^d(\lfloor dt\rfloor)$ be the sequence of the first coordinates of $\{X^d(t)\}$ sped-up by a factor of $d$. Then, as $d\to\infty$, we have $U^d\Rightarrow U$, where $\Rightarrow$ denotes weak convergence in Skorokhod topology, and $U$ satisfies the following Langevin SDE
\[
\mathrm dU(t)=(s(\ell))^{1/2}\mathrm dB(t)+s(\ell)\frac{f'(U(t))}{2f(U(t))}\mathrm dt,
\]
where $s(\ell):=2\ell^2\Phi\left(-\ell\frac{\sqrt{\mathbb E_f[((\log f)')^2]-1}}2\right)$ is the speed measure for the diffusion process, and $\Phi(\cdot)$ being the standard Gaussian cumulative density function.''']
def inventory():
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,statement_original=s,evidence=[dict(page=p,location='Theorem '+n+' — complete original statement')]) for i,(n,p,s) in enumerate(zip(NUMBERS,PAGES,STATEMENTS),1)]
    paper=dict(paper_id=PID,title='Stereographic Markov chain Monte Carlo',authors=['Jun Yang','Krzysztof Łatuszyński','Gareth O. Roberts'],version='arXiv:2205.12112v2, marked 21 Feb 2024',pdf_pages=80,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=24,main_text_boundary=dict(location='Main text ends with Discussion and Acknowledgement on PDF page24. The PDF outline places Proofs of Main Results on25 and Additional Simulations on62; these supplementary bodies are excluded. No supplementary body is read.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Independently enumerate actual small-cap THEOREM headings across PDF pages1–24, excluding mixed-case prose mentions, propositions, corollaries, lemmas and supplementary bodies; visually compare all five complete statements.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Verified registered local arXiv v2 PDF pinned by SHA256; read main text only, excluding supplementary bodies.',normalization_policy='Preserve complete original theorem bodies, printed numbering, hypotheses and formulas. Normalize line wrapping and mathematical typesetting only. Keep the if-and-only-if in T2.1, sufficient condition in T2.2, both restrictions in T4.1, SPS in T5.1 and RSPS in T5.2. Preserve the original phrase cumulative density function.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip());assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n');print('Saved five complete main-text Theorems; independent inventory review remains separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
