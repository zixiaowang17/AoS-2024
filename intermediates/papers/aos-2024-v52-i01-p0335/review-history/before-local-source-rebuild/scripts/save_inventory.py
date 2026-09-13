"""Preserve all fourteen printed main-text Theorems before extracting dependencies."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text())
claims=[]
def claim(number,pages,body,title=None):
    claims.append(dict(claim_id=PID+'/T'+number,paper_id=PID,claim_kind='theorem',label='Theorem '+number+((' ('+title+')') if title else ''),source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+number+(' (continued)' if i else '')) for i,p in enumerate(pages)]))

claim('2.1',[8],r'''
Suppose that the parameter spaces $\{\Theta_{n,m}\}_{m\in\mathcal M_n}$ are disjoint. Then the variational posterior distribution in (2.7) satisfies
\[
\widehat Q_n=\sum_{m\in\mathcal M_n}\widehat\gamma_{n,m}\widehat Q_{n,m},\tag{2.10}
\]
where
\[
\widehat Q_{n,m}\in\operatorname*{argmin}_{Q\in\mathcal Q_{n,m}}\mathcal E_n(Q,\Pi_{n,m},\mathrm p_n)\tag{2.11}
\]
and
\[
\widehat\gamma_{n,m}:=\frac1{\widehat Z_{\gamma,n}}\alpha_{n,m}\exp\left(-\mathcal E_n(\widehat Q_{n,m},\Pi_{n,m},\mathrm p_n)\right)\tag{2.12}
\]
with $\widehat Z_{\gamma,n}:=\sum_{m'\in\mathcal M_n}\alpha_{n,m'}\exp\left(-\mathcal E_n(\widehat Q_{n,m'},\Pi_{n,m'},\mathrm p_n)\right)$ being the normalizing constant.
''')
claim('3.1',[12],r'''
Under Assumption A, we have
\[
\sup_{\boldsymbol\lambda^\star\in\Lambda_n^\star}\sup_{m\in\mathcal M_n}\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\widehat Q_{n,m}\left(\mathcal d_n(\mathrm T(\boldsymbol\theta),\boldsymbol\lambda^\star)\geq A_n(\eta_{n,m}+\zeta_{n,m})\right)\right]=o(1)\tag{3.4}
\]
for any diverging sequence $(A_n)_{n\in\mathbb N}\to\infty$.
''')
claim('3.3',[13],r'''
For any $\boldsymbol\lambda^\star\in\Lambda_n^\star$,
\[
\begin{aligned}
\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\operatorname{KL}\left(\widehat Q_n,\Pi_n(\cdot\mid\mathbf Y^{(n)})\right)\right]
&\leq\inf_{Q\in\mathcal Q_n}\left\{\operatorname{KL}(Q,\Pi_n)+Q\left[\operatorname{KL}\left(\mathrm P_{\boldsymbol\lambda^\star}^{(n)},\mathrm P_{\mathrm T(\boldsymbol\theta)}^{(n)}\right)\right]\right\}\\
&\leq\inf_{m\in\mathcal M_n}\inf_{Q_m\in\mathcal Q_{n,m}}\left\{-\log(\alpha_{n,m})+\operatorname{KL}(Q_m,\Pi_{n,m})+Q_m\left[\operatorname{KL}\left(\mathrm P_{\boldsymbol\lambda^\star}^{(n)},\mathrm P_{\mathrm T(\boldsymbol\theta)}^{(n)}\right)\right]\right\}.
\end{aligned}\tag{3.10}
\]
Further suppose that Assumption A2 and Assumption B3 hold. Then (3.1) holds with $\varepsilon_n=\varepsilon_n(\mathcal M_n)$.
''','Variational approximation gap')
claim('3.4',[13],r'''
Under Assumptions A and B, we have
\[
\sup_{\boldsymbol\lambda^\star\in\Lambda_n^\star}\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\widehat Q_n\left(\mathcal d_n(\mathrm T(\boldsymbol\theta),\boldsymbol\lambda^\star)\geq A_n\varepsilon_n\right)\right]=o(1)\tag{3.11}
\]
for any diverging sequence $(A_n)_{n\in\mathbb N}\to\infty$.
''','Adaptive contraction rate')
claim('3.5',[14],r'''
Assume that $n\varepsilon_n^2\to\infty$. Then under Assumptions A2 and B, there exists an absolute constant $H_1>0$ such that
\[
\sup_{\boldsymbol\lambda^\star\in\Lambda_n^\star}\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\widehat Q_n\left(\mathcal M_n^{\mathrm{over}}(H_1)\right)\right]=o(1).\tag{3.14}
\]
''','Selection, no severe overestimation')
claim('3.6',[15],r'''
Under Assumptions A and B, we have
\[
\sup_{\boldsymbol\lambda^\star\in\Lambda_n^\star}\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\widehat Q_n\left(\mathcal M_n^{\mathrm{under}}(\underline A_n\varepsilon_n;\boldsymbol\lambda^\star)\right)\right]=o(1)\tag{3.16}
\]
for any diverging sequence $(\underline A_n)_{n\in\mathbb N}$ such that $\underline A_n\to\infty$.
''','Selection, no underestimation')
claim('4.1',[17],r'''
Let $\mathcal F^\star\subset\mathcal F^d$. For each $n\in\mathbb N$, let $\mathcal M_n\subset\mathbb N_{\geq2}\times\mathbb N$ be a set of some network architectures such that $\log|\mathcal M_n|\lesssim\log n$ and $\max_{(K,M)\in\mathcal M_n}(K\vee M)\lesssim n$. Assume that $1\leq B_n\lesssim n^{\iota_0}$ for some absolute constant $\iota_0>0$. Then
\[
\sup_{f^\star\in\mathcal F^\star}\mathrm P_{f^\star}^{(n)}\left[\widehat Q_n\left(\|\operatorname{net}(\boldsymbol\theta)-f^\star\|_{n,2}\geq A_n\varepsilon_n(\mathcal F^\star)\right)\right]=o(1)\tag{4.6}
\]
for any diverging sequence $(A_n)_{n\in\mathbb N}\to\infty$, where
\[
\varepsilon_n(\mathcal F^\star):=\varepsilon_n(\mathcal F^\star;\mathcal M_n):=\inf_{(K,M)\in\mathcal M_n}\left\{\sup_{f^*\in\mathcal F^\star}\inf_{\boldsymbol\theta\in\Theta_{(K,M)}^{\leq B_n}}\|\operatorname{net}(\boldsymbol\theta)-f^*\|_\infty+KM\sqrt{\frac{\log n}{n}}\right\}.\tag{4.7}
\]
''','Oracle contraction rate, regression function')
claim('5.1',[20],r'''
Under Assumption D, we have
\[
\sup_{\boldsymbol\lambda^\star\in\Lambda_n^\star}\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\widehat Q_n\left(\mathcal d_n(\mathrm T(\boldsymbol\theta),\boldsymbol\lambda^\star)\geq A_n\varepsilon_n\right)\right]=o(1)\tag{5.7}
\]
for any diverging sequence $(A_n)_{n\in\mathbb N}\to\infty$, where $\varepsilon_n$ is defined in (5.3), and hence
\[
\sup_{\boldsymbol\lambda^\star\in\Lambda_n^\star}\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\widehat Q_n\left(\left\{(m,S)\in\mathcal M_n\times\mathcal S_n:\inf_{\boldsymbol\theta\in\Theta_{n,m,S}}\mathcal d_n(\mathrm T(\boldsymbol\theta),\boldsymbol\lambda^\star)\geq A_n\varepsilon_n\right\}\right)\right]=o(1).\tag{5.8}
\]
On the other hand, under Assumptions D2 and D3, there exists an absolute constant $H_1>0$ such that
\[
\sup_{\boldsymbol\lambda^\star\in\Lambda_n^\star}\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\widehat Q_n\left(\left\{(m,S)\in\mathcal M_n\times\mathcal S_n:\zeta_{n,m,S}\geq H_1\varepsilon_n\right\}\right)\right]=o(1).\tag{5.9}
\]
''','Adaptive contraction rate and model selection consistency, combinatorial model spaces')
claim('5.2',[21,22],r'''
Assume that $s_nr_n\log d_n=o(n)$, $s_n\geq r_n$ and $\log d_n\gtrsim\log n$. Then if $\mathcal M_n=[m_{\max,n}]$ with $r_n\leq m_{\max,n}\leq n$,
\[
\sup_{\boldsymbol\Sigma^\star\in\Lambda_n^\star}\mathrm P_{\boldsymbol\Sigma^\star}^{(n)}\left[\widehat Q_n\left(\|\mathrm T(\mathbf L)-\boldsymbol\Sigma^\star\|_{\mathrm{op}}\geq A_n\sqrt{\frac{s_nr_n\log d_n}{n}}\right)\right]=o(1)\tag{5.11}
\]
for any diverging sequence $(A_n)_{n\in\mathbb N}\to\infty$.
''','Covariance matrix')
claim('5.3',[22],r'''
Suppose that the same assumptions as in Theorem 5.2 hold. Furthermore assume that $\eta_n^*\geq\underline A_n\sqrt{s_nr_n\log d_n/n}$ for some diverging sequence $(\underline A_n)_{n\in\mathbb N}\to\infty$. Then there exist absolute constants $H_1>1$ and $H_2>1$ such that
\[
\inf_{\boldsymbol\Sigma^\star\in\Lambda_n^\star(\eta_n^*)}\mathrm P_{\boldsymbol\Sigma^\star}^{(n)}\left[\widehat Q_n\left(\{m\in\mathcal M_n:r_n\leq m\leq H_1r_n\}\right)\right]\to1,\tag{5.13}
\]
\[
\inf_{\boldsymbol\Sigma^\star\in\Lambda_n^\star(\eta_n^*)}\mathrm P_{\boldsymbol\Sigma^\star}^{(n)}\left[\widehat Q_n\left(s_n\leq|\operatorname{supp}(\mathbf L)|\leq H_2s_n\right)\right]\to1.\tag{5.14}
\]
''','Factor dimensionality and sparsity')
claim('6.1',[23],r'''
Under Assumptions A2, B1 and B3, we have
\[
\sup_{\boldsymbol\lambda^\star\in\Lambda_n^\star}\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\widehat Q_n\left(\mathcal M_n^{\mathrm{ivB,over}}(A_n)\right)\right]=o(1).\tag{6.3}
\]
for any diverging sequence $(A_n)_{n\in\mathbb N}\to\infty$.
''','ivB regularization')
claim('6.2',[23],r'''
Under Assumptions A, B1 and B3, we have
\[
\sup_{\boldsymbol\lambda^\star\in\Lambda_n^\star}\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\widehat Q_n\left(\mathcal d_n(\mathrm T(\boldsymbol\theta),\boldsymbol\lambda^\star)\geq(A_n\varepsilon_n)\vee\zeta_n^\ddagger\right)\right]=o(1)\tag{6.5}
\]
for any diverging sequence $(A_n)_{n\in\mathbb N}\to\infty$, where $\zeta_n^\ddagger$ is defined in (6.4).
''','Adaptive contraction rate through ivB regularization')
claim('7.1',[26],r'''
Suppose that Assumption E1 holds. Then for any $\boldsymbol\lambda^\star\in\Lambda_n$,
\[
\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\operatorname{KL}\left(\widehat Q_n^\natural,\Pi_n^\natural(\cdot\mid\mathbf Y^{(n)})\right)\right]\leq\inf_{m\in\mathcal M_n}\inf_{Q_m\in\mathcal Q_{n,m}}\left\{-\log(\alpha_{n,m})+\operatorname{KL}(Q_m,\Pi_{n,m})+\frac{\mathfrak c_2}{\rho}Q_m\left[n\mathcal d_n^2(\mathrm T(\boldsymbol\theta),\boldsymbol\lambda^\star)\right]\right\}.\tag{7.9}
\]
Further suppose that Assumptions E2 and E3 holds additionally. Then (7.5) holds with $\varepsilon_n=\varepsilon_n(\mathcal M_n)$.
''','Variational approximation gap to quasi-posterior')
claim('7.2',[26],r'''
Under Assumption E, we have
\[
\sup_{\boldsymbol\lambda^\star\in\Lambda_n^\star}\mathrm P_{\boldsymbol\lambda^\star}^{(n)}\left[\widehat Q_n^\natural\left(\mathcal d_n(\mathrm T(\boldsymbol\theta),\boldsymbol\lambda^\star)\geq A_n\varepsilon_n\right)\right]=o(1)\tag{7.10}
\]
for any diverging sequence $(A_n)_{n\in\mathbb N}\to\infty$.
''','Adaptive contraction rate of variational quasi-posterior')

paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=29,
    main_text_boundary=dict(location='Main results end with Section 7.2 on PDF page 26. Acknowledgments, funding and a supplementary-material pointer precede the references on page 27; references end on page 29. PDF page 30 begins the separately titled supplement and its table of contents. Appendix bodies are excluded.',shared_page_with_appendix=False),
    intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inventory=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
for c in claims:
    for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
        depth=0
        for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
            depth+=1 if brace=='{' else -1
            assert depth>=0,c['claim_id']
        assert depth==0,c['claim_id']
path=ROOT/'theorem-inventory.json';path.write_text(json.dumps(inventory,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.now(timezone.utc).isoformat(),theorem_count=len(claims),inventory_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),notes=[
    'Pinned arXiv:2109.03204v4, stamped 11 March 2024. Source identity with the journal publication is not assumed.',
    'All main-document pages 1-29 were searched for Theorem environments. All 14 full statements were visually checked, including the final sentence of Theorem 5.2 on page 22.',
    'Theorem 2.1 retains the disjoint-space assumption, mixture formula, individual argmins, weights and normalizing constant.',
    'Theorem 3.3 retains the two unconditional variational bounds and its separate A2/B3 consequence. Theorem 7.1 retains E1 for its bound and adds E2/E3 only for its final consequence.',
    'Theorem 3.5 requires n epsilon_n^2 tending to infinity and assumes A2 and B; Theorem 6.1 assumes only A2, B1 and B3. No missing A1 or B2 is supplied.',
    'Theorem 4.1 preserves the order sup_f inf_theta inside its oracle expression, all architecture restrictions and the polynomial magnitude bound. It does not itself impose a Holder smoothness class.',
    'Theorem 5.1 retains all three conclusions and its weaker D2/D3 hypotheses for the overestimation assertion.',
    'Theorem 5.3 retains both probability-to-one conclusions, H1/H2 strictly larger than one, the signal lower bound, and the source reference importing Theorem 5.2 assumptions.',
    'Underlined A_n in Theorems 3.6 and 5.3 is preserved. The maximum with zeta_n double-dagger in Theorem 6.2 is preserved.',
    'Theorem 7.1 quantifies over Lambda_n without a star, unlike Theorem 7.2. Its coefficient is c_2/rho, and quasi-posterior natural superscripts are preserved.',
    'Equations (3.1), (5.3), (6.4) and (7.5), as well as Assumptions A/B/D/E and imported model conventions, remain references to resolve during the interface stage. No reference is expanded into the original theorem statement.',
    'Corollaries, lemmas, examples, remarks, proof headings, citations and all supplemental Theorems are excluded from the inventory.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve main-text definitions and Assumptions A/B/D/E, preserve distinct application-specific priors and variational families, and derive the local theorem dependency graph.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated the complete fourteen-Theorem inventory.')
