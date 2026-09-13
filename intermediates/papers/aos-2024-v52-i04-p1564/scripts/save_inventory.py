"""Rebuild the nine complete original main-text theorem statements."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1564'
SHA='764e61241f4805afe2049048f37e0d748f1cbc048b08c77037438725b7ec10ba'
claims=[]
def claim(n,pages,text,title=None):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+(' ('+title+')' if title else ''),source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+n+', complete original statement'+(' including continuation' if len(pages)>1 else '')) for p in pages]))
claim('1',[10],r'''
In the Gaussian location model of Example 1 consider $\Theta_b=\Theta(a_b,s_n)$ as in (10). For any fixed $b\in\mathbb R$, under the sparse asymptotics (3) the minimax $\mathfrak R$-risk over $\Theta_b$ verifies
\[
\inf_\varphi\sup_{\theta\in\Theta_b}\mathfrak R(\theta,\varphi)=\overline\Phi(b)+o(1).
\]
The result also holds in the limiting cases $b=b_n\to+\infty$ and $b=b_n\to-\infty$.
''')
claim('2',[11],r'''
In the Gaussian location model of Example 1, consider $\Theta_b=\Theta(a_b,s_n)$ as in (10) where $b$ is either fixed in $\mathbb R$ or is a sequence $b=b_n$ tending to $+\infty$. There exists a multiple testing procedure $\varphi$, not depending on $s_n$ or $b$, such that in the sparse asymptotics (3)
\[
\sup_{\theta\in\Theta_b}\mathfrak R(\theta,\varphi)=\overline\Phi(b)+o(1).
\]
In particular this holds for the empirical Bayes $\ell$-value procedure (S-29) taken at any fixed threshold $t\in(0,1)$. In addition, under (12), this also holds for the BH procedure (S-18) taken at a vanishing level $\alpha=\alpha_n=o(1)$ that satisfies $-\log(\alpha_n)=o(\sqrt{\log n})$.
''')
claim('3',[12],r'''
In the setting of Theorem 1, consider a fixed real $b$, a sequence $B=(B_n)_n$ with $B_n^2\le e^{(\log(n/s_n))^{1/4}}$ and $\underline{\lim}_n B_n>1$, and consider $\mathcal S_B(\Theta_b)$ as in Definition 1. Then we have in the sparse asymptotics (3)
\[
\inf_{\varphi\in\mathcal S_B(\Theta_b)}\sup_{\theta\in\Theta_b}\operatorname{FNR}(\theta,\varphi)=\overline\Phi(b)+o(1).\tag{15}
\]
The result continues to hold if $b=b_n\to+\infty$ or $b=b_n\to-\infty$.
''')
claim('4',[15,16],r'''
Consider the sparse sequence model (1)–(3) with Assumption 1. Consider a vector $\boldsymbol a=(a_1,\ldots,a_{s_n})\in\mathbb R_+^{s_n}$, $\Theta(\boldsymbol a,s_n)$ defined by (21) and $\Lambda_n(\boldsymbol a)$ defined by (22). Then

• Under Assumption 1A,
\[
\inf_\varphi\sup_{\theta\in\Theta(\boldsymbol a,s_n)}\mathfrak R(\theta,\varphi)=\Lambda_n(\boldsymbol a)+o(1);
\]

• Under Assumption 1B,
\[
\inf_\varphi\sup_{\theta\in\Theta(\boldsymbol a,s_n)}\mathfrak R(\theta,\varphi)=2\Lambda_n(\boldsymbol a)-1+o(1).
\]
In each case the risk bound is achieved by a thresholding procedure $\varphi_i(X)=\mathbf 1\{|X_i|>a_n^*\}$ with $a_n^*$ as in Assumption 1.
''')
claim('5',[16],r'''
Consider the sparse sequence model (1)–(3) and grant Assumption 1A. Then the BH procedure taken at a level $\alpha=\alpha_n$ obeying (24) satisfies, for all $\theta\in\mathbb R^n$ with $|S_\theta|=s_n$, for $n$ large enough,
\[
\mathfrak R(\theta,\varphi)\le\Lambda_n(\theta)+\alpha_n+\exp\left(-\frac{(1-\Lambda_n(\theta))^2}{32}s_n\right).\tag{25}
\]
It follows that the BH procedure achieves the bound of Theorem 4,
\[
\sup_{\theta\in\Theta(\boldsymbol a,s_n)}\mathfrak R(\theta,\varphi)\le\Lambda_n(\boldsymbol a)+o(1).
\]
In addition, if $\Lambda_n(\boldsymbol a)$ is bounded away from 1 we have the concrete expression $\alpha_n+\exp\left(-(1-\Lambda_n(\boldsymbol a))^2s_n/32\right)$ for the $o(1)$ terms. Finally, if we instead grant Assumption 1B, the same bounds hold with $\Lambda_n(\cdot)$ replaced by $2\Lambda_n(\cdot)-1$.
''')
claim('6',[17],r'''
Consider the settings of Theorem 4. For any sequence $B=(B_n)_n$ with $B_n^2\le\frac13(n/s_n)\overline F_0(a_n^*-\delta_n)$ and $\underline{\lim}_n B_n>1$, let $\mathcal S_B$ denote the set of sparsity preserving procedures over the set $\Theta=\Theta(\boldsymbol a,s_n)$, as in Definition 1. Then the conclusions of Theorem 4 hold with $\mathfrak R(\theta,\varphi)$ replaced by $\operatorname{FNR}(\theta,\varphi)$ if the infimum is taken only over $\varphi\in\mathcal S_B$.
''')
claim('7',[22],r'''
Consider the Gaussian location model of Example 1. If one sets $a_b=\sqrt{2\log(n/s_n)}+b$ for an arbitrary real $b$ or a sequence $b=b_n\to\pm\infty$, then for $\Theta'_b=\Theta'_b(s_n)$ as in (31), the sharp asymptotic minimax risk for classification is
\[
\inf_\varphi\sup_{\theta\in\Theta'_b}E_\theta\mathrm L_{\mathrm C}(\theta,\varphi)/s_n=\overline\Phi(b)+o(1).
\]
For $\varphi=\varphi^{\widehat\ell}$ the empirical Bayes $\ell$-value procedure (S-29) or $\varphi=\varphi^{BH}$ the BH procedure (S-18) at a level $\alpha=\alpha_n=o(1)$ with $-\log\alpha=o((\log n)^{1/2})$ (additionally assuming the polynomial sparsity (12)), the bound is achieved: for any real $b$, or for $b=b_n\to\pm\infty$,
\[
\sup_{\theta\in\Theta'_b}E_\theta\mathrm L_{\mathrm C}(\theta,\varphi)/s_n=\overline\Phi(b)+o(1).
\]
''')
claim('8',[23,24],r'''
Consider the Subbotin location model (Example 2) for some $\zeta>1$ and the parameter set $\Theta(r,\beta)$ defined by (32)–(33). Let $\kappa=\kappa(r,\beta,\zeta)$ be the unique element of $(0,r/2^\zeta)$ such that $(r^{1/\zeta}-\kappa^{1/\zeta})^\zeta-\kappa=\beta$. Then the thresholding procedure $\varphi_i^*=\mathbf 1_{|X_i|\ge t_n^*}$ based upon the threshold
\[
t_n^*=(\zeta\log n)^{1/\zeta}(r^{1/\zeta}-\kappa^{1/\zeta})=(\zeta(\beta+\kappa)\log n)^{1/\zeta}\tag{34}
\]
is asymptotically rate minimax:
\[
\sup_{\theta\in\Theta(r,\beta)}\mathfrak R(\theta,\varphi^*)\asymp\inf_\varphi\sup_{\theta\in\Theta(r,\beta)}\mathfrak R(\theta,\varphi)\asymp n^{-\kappa}/(\log n)^{1-1/\zeta}.
\]
The same result holds for classification upon replacing $\mathfrak R$ by $E_\theta\mathrm L_{\mathrm C}/n^{1-\beta}$.
''')
claim('9',[24],r'''
Consider the setting of Theorem 8 with $\zeta=2$ (Gaussian noise). The following points consider the adaptation problem over the class $\Theta(r,\beta)$ for some $\beta\in(0,1)$ and $\beta<r$. The results hold for the $\mathfrak R$–risk as well as for the normalised classification risk $E_\theta\mathrm L_{\mathrm C}(\theta,\varphi)/n^{1-\beta}$.

(i) Simultaneous adaptation to $(r,\beta)$ is impossible over the full range of parameters.

(ii) Known exact sparsity $s_n$, unknown $r$: the top–$s_n$ procedure provides adaptation to $r$.

(iii) Unknown $\beta$, known $r$: a plug-in procedure provides adaptation to $\beta$.

(iv) Simultaneous adaptation to $(r,\beta)$ is possible in the regime $\kappa(r,\beta,2)<1-\beta$.

Moreover, for point (i) the loss due to adaptation is polynomial in $n$.
''','Adaptation to large signals, summary in Gaussian case')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='Sharp multiple testing boundary for sparse sequences',authors=['Kweku Abraham','Ismaël Castillo','Étienne Roquain'],version='arXiv:2109.13601v2, 30 August 2023',source_url='https://arxiv.org/pdf/2109.13601v2',pdf_pages=86,pdf_sha256=SHA,main_text_last_pdf_page=33,main_text_boundary=dict(location='Main paper and references end on PDF page 33 after reference [48], Sun and Cai (2009). Page 34 begins This supplementary material and Section S-1; supplementary sections are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Verified registered arXiv v2 PDF; main paper pages 1-33 only; supplementary results excluded.'),papers=[paper],claims=claims),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
