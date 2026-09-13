"""Preserve all nine main-text Theorems in the pinned 2024 transport paper."""
import datetime, hashlib, json, re, shutil, subprocess, sys
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
PID = ROOT.name
prov = json.loads((ROOT/'evidence/source-provenance.json').read_text())
claims = []
def claim(n, pages, text, title=None):
    label = 'Theorem '+str(n)+((' ('+title+')') if title else '')
    claims.append(dict(claim_id=PID+'/T'+str(n), paper_id=PID, claim_kind='theorem', label=label, source_order=len(claims)+1, statement_original=text.strip(), evidence=[dict(page=p, location=label) for p in pages]))

claim(1, [9], r'''
Let $P\in\mathcal P_{\mathrm{ac}}(\Omega)$ and $Q\in\mathcal P(\Omega)$.

(i) There exists an optimal transport map $T_0$ between $P$ and $Q$ which takes the form $T_0=\nabla\varphi_0$ for a convex function $\varphi_0:\mathbb R^d\to\mathbb R$ which solves the semi-dual problem (12). Furthermore, $T_0$ is uniquely determined $P$-almost everywhere.

(ii) If we further have $Q\in\mathcal P_{\mathrm{ac}}(\Omega)$, then $\nabla\varphi_0^*$ is the ($Q$-almost everywhere uniquely determined) gradient of a convex function such that $\nabla\varphi_0^*{}_{\#}Q=P$, and solves the Monge problem for transporting $Q$ onto $P$. Furthermore, for Lebesgue-almost every $x,y\in\Omega$
\[
\nabla\varphi_0^*\circ\nabla\varphi_0(x)=x,\qquad\nabla\varphi_0\circ\nabla\varphi_0^*(y)=y.
\]
''', 'Brenier’s Theorem')
claim(3, [10], r'''
Assume $\Omega$ satisfies condition (S1). Assume further that there exists $\gamma>0$ such that $\gamma^{-1}\le p,q\le\gamma$ over $\Omega$. Then, the Brenier potential $\varphi_0$ is unique up to an additive constant, and satisfies the following.

(i) (Interior Regularity) Suppose there exists $\alpha>1$, $\alpha\notin\mathbb N$, such that $p,q\in\mathcal C^{\alpha-1}(\Omega^\circ)$. Then $\varphi_0\in\mathcal C^{\alpha+1}(\Omega^\circ)$. Moreover, for any open subdomain $\Omega'$ such that $\overline{\Omega'}\subseteq\Omega^\circ$, there exists a constant $C>0$ depending on $\gamma,\alpha,\Omega,\Omega',\|\varphi_0\|_{L^\infty(\Omega)},\|p\|_{\mathcal C^{\alpha-1}(\Omega^\circ)},\|q\|_{\mathcal C^{\alpha-1}(\Omega^\circ)}$ such that $\|\varphi_0\|_{\mathcal C^{\alpha+1}(\Omega')}\le C$.

(ii) (Global Regularity) Assume $\Omega$ admits a $\mathcal C^2$ boundary and is uniformly convex. Assume further that there exists $\alpha>1$, $\alpha\notin\mathbb N$, such that $p,q\in\mathcal C^{\alpha-1}(\Omega)$. Then, $\varphi_0\in\mathcal C^{\alpha+1}(\Omega)$.
''', 'Caffarelli’s Regularity Theory')
claim(5, [11], r'''
Let $P,Q\in\mathcal P(\mathbb T^d)$ be absolutely continuous with respect to the Lebesgue measure, with respective densities $p,q$ satisfying $\gamma^{-1}\le p,q\le\gamma$ for some $\gamma>0$. Assume further that $p,q\in\mathcal C^{\alpha-1}(\mathbb T^d)$ for some $\alpha>1$. Then, there exists a constant $C>0$ depending only on $\alpha,\gamma,\|p\|_{\mathcal C^{\alpha-1}(\mathbb T^d)}$ and $\|q\|_{\mathcal C^{\alpha-1}(\mathbb T^d)}$ such that, $\|\varphi_0\|_{\mathcal C^{\alpha+1}([0,1]^d)}\le C$.
''')
claim(6, [12], r'''
Let $P,Q\in\mathcal P_{\mathrm{ac}}(\Omega)$, and assume condition $A1(\lambda)$ holds for some $\lambda>0$. For any $\widehat Q\in\mathcal P(\Omega)$, let $\widehat T=\nabla\widehat\varphi$ be the unique optimal transport map from $P$ to $\widehat Q$. Then,
\[
\frac1\lambda\|\widehat T-T_0\|_{L^2(P)}^2\le W_2^2(P,\widehat Q)-W_2^2(P,Q)-\int\psi_0\,d(\widehat Q-Q)\le\lambda W_2^2(\widehat Q,Q).\tag{16}
\]
''')
claim(10, [16], r'''
Let $\alpha>1$ and $M,\gamma>0$. Let $P,Q\in\mathcal P_{\mathrm{ac}}([0,1]^d)$, and assume the density $q$ satisfies $q\in\mathcal C^{\alpha-1}([0,1]^d;M,\gamma)$. Let $2^{J_n}\asymp n^{1/(d+2(\alpha-1))}$. Then, the following assertions hold.

(i) (Optimal Transport Maps) Assume $\varphi_0$ satisfies condition $A1(\lambda)$ for some $\lambda>0$. Then, there exists a constant $C>0$ depending on $M,\lambda,\gamma,\alpha$ such that,
\[
\mathbb E\|\widehat T_n-T_0\|_{L^2(P)}^2\le CR_{T,n}(\alpha),\qquad\text{where }R_{T,n}(\alpha):=\begin{cases}1/n,&d=1,\\(\log n)^2/n,&d=2,\\n^{-\frac{2\alpha}{2(\alpha-1)+d}},&d\ge3.\end{cases}
\]

(ii) (Wasserstein Distances) Assume that for some $\lambda>0$, $\varphi_0^*\in\mathcal C^{\alpha+1}([0,1]^d;\lambda)$, and $\gamma^{-1}\le p\le\gamma$ over $[0,1]^d$. Then, there exists a constant $C>0$ depending on $M,\lambda,\gamma,\alpha$ such that,
\[
\left|\mathbb EW_2^2(P,\widehat Q_n)-W_2^2(P,Q)\right|\le CR_{T,n}(\alpha),
\]
\[
\mathbb E\left|W_2^2(P,\widehat Q_n)-W_2^2(P,Q)\right|^2\le\left[CR_{T,n}(\alpha)+\sqrt{\frac{\operatorname{Var}_Q[\psi_0(Y)]}{n}}\right]^2.
\]
''', 'One-Sample Wavelet Estimators')
claim(18, [21,22], r'''
Let the distributions $P,Q\in\mathcal P_{\mathrm{ac}}(\mathbb T^d)$ admit densities $p,q\in\mathcal C^{\alpha-1}(\mathbb T^d;M,\gamma)$ for some $\alpha>1$ and $M,\gamma>0$. Assume further that $K$ is a kernel satisfying condition $K1(2\alpha,\kappa)$ for some $\kappa>0$. Let $h_n\asymp n^{-1/(d+2(\alpha-1))}$. Then, there exists a constant $C>0$ depending only on $K,M,\gamma,\alpha$ such that the following statements hold.

(i) (Optimal Transport Maps) We have,
\[
\mathbb E\|\widehat T_{nm}^{(\mathrm{ker})}-T_0\|_{L^2(P)}^2\le CR_{K,n\wedge m}(\alpha),\qquad\text{where }R_{K,n}(\alpha):=\begin{cases}n^{-\frac{2\alpha}{2(\alpha-1)+d}},&d\ge3,\\\log n/n,&d=2,\\1/n,&d=1.\end{cases}
\]

(ii) (Wasserstein Distances) Assume further that $\alpha\notin\mathbb N$. Then,
\[
\left|\mathbb EW_2^2(\widehat P_n^{(\mathrm{ker})},\widehat Q_m^{(\mathrm{ker})})-W_2^2(P,Q)\right|\le CR_{K,n\wedge m}(\alpha),
\]
\[
\mathbb E\left|W_2^2(\widehat P_n^{(\mathrm{ker})},\widehat Q_m^{(\mathrm{ker})})-W_2^2(P,Q)\right|^2\le\left[CR_{K,n\wedge m}(\alpha)+\sqrt{\frac{\operatorname{Var}_P[\phi_0(X)]}{n}+\frac{\operatorname{Var}_Q[\psi_0(Y)]}{m}}\right]^2.
\]
''', 'Kernel Estimators')
claim(20, [24], r'''
Let $\Omega$ be a domain satisfying condition (C1). Assume the distributions $P,Q\in\mathcal P_{\mathrm{ac}}(\Omega)$ admit densities $p,q\in\mathcal C_N^{\alpha-1}(\Omega;M,\gamma)$ for some $\alpha>1$, $\alpha\notin\mathbb N$, and $M,\gamma>0$. Let $L_n^{1/d}\asymp n^{1/(d+2(\alpha-1))}$. Then, there exists a constant $C>0$ depending only on $\Omega,M,\gamma,\alpha,\tau$ such that the following statements hold.

(i) (One-Sample) Assume $\varphi_0\in\mathcal C^2(\Omega;M)$. Then,
\[
\mathbb E\|\overline T_m-T_0\|_{L^2(P)}^2\le CR_{K,m}(\alpha).
\]

(ii) (Two-Sample) Assume that condition (C2) holds. Then,
\[
\mathbb E\|\widehat T_{nm}-T_0\|_{L^2(P)}^2\le CR_{K,n\wedge m}(\alpha),
\]
''')
claim(22, [26], r'''
Assume that $P,Q\in\mathcal P_{\mathrm{ac}}(\Omega)$ admit positive and bounded densities $p,q$ over $\Omega$. Then, the following assertions hold.

(i) (Density Estimation over the Torus) Let $\Omega=\mathbb T^d$ and assume $p,q\in\mathcal C^{\alpha-1}(\Omega)$ for some $\alpha>1$ satisfying $2(\alpha+1)>d$. Then, equations (38)–(39) hold when
\[
(\widehat P_n,\widehat Q_m)=(\widehat P_n^{(\mathrm{ker})},\widehat Q_m^{(\mathrm{ker})}).
\]

(ii) (Density Estimation over the Hypercube) Let $\Omega=[0,1]^d$, and assume $p,q\in\mathcal C^{\alpha-1}(\Omega)$ for some $\alpha>1$ satisfying $2(\alpha+1)>d$. Assume additionally that $\varphi_0\in\mathcal C^{\alpha+1}(\Omega)$. Then, equation (38) holds when
\[
(\widehat P_n,\widehat Q_m)=(\widehat P_n^{(\mathrm{bc})},\widehat Q_m^{(\mathrm{bc})}).
\]
Furthermore, equation (39) holds under the additional condition $\varphi_0^*\in\mathcal C^{\alpha+1}(\Omega)$.

(iii) (Empirical Measures) Let $\Omega$ be either $\mathbb T^d$ or $[0,1]^d$. Assume $d\le3$, and $\varphi_0\in\mathcal C^2(\Omega)$. Then equations (38)–(39) hold when
\[
(\widehat P_n,\widehat Q_m)=(P_n,Q_m).
\]
''', 'Central Limit Theorems')
claim(24, [28], r'''
Given $M,\gamma>0$ and $\alpha>1$, let $P,Q\in\mathcal P_{\mathrm{ac}}(\mathbb T^d)$ admit densities $p,q\in\mathcal C^{\alpha-1}(\mathbb T^d;M,\gamma)$. Let $(\phi_0,\psi_0)$ denote a pair of Kantorovich potentials between $P$ and $Q$, unique up to translation by a constant. Then, there exist $\overline M,\overline\gamma,\overline u>0$, depending only on $M,\gamma,\alpha$, such that $P_{t,h_1}$ and $Q_{t,h_2}$ admit densities in $\mathcal C^{\alpha-1}(\mathbb T^d;\overline M,\overline\gamma)$, for all $t>0$ and $h_1,h_2\in\mathbb R$ satisfying $t(|h_1|\vee|h_2|)\le\overline u$. Furthermore,

(i) (One Sample) For any estimator sequence $(U_n)_{n\ge1}$, we have
\[
\sup_{\substack{\mathcal I\subseteq\mathbb R\\|\mathcal I|<\infty}}\liminf_{n\to\infty}\sup_{h\in\mathcal I}n\mathbb E_{n,h}\left|U_n-\Phi_Q(P_{n^{-1/2},h})\right|^2\ge\operatorname{Var}_P[\phi_0(X)].
\]
where $\mathbb E_{n,h}$ denotes the expectation taken over the probability measure $P_{n^{-1/2},h}^{\otimes n}$.

(ii) (Two Sample) For any estimator sequence $(U_{nm})_{n,m\ge1}$, we have
\[
\sup_{\substack{\mathcal I\subseteq\mathbb R^2\\|\mathcal I|<\infty}}\liminf_{n,m\to\infty}\sup_{(h_1,h_2)\in\mathcal I}\frac{nm}{n+m}\mathbb E_{n,m,h_1,h_2}\left|U_{nm}-W_2^2(P_{n^{-1/2},h_1},Q_{m^{-1/2},h_2})\right|^2
\ge(1-\rho)\operatorname{Var}_P[\phi_0(X)]+\rho\operatorname{Var}_Q[\psi_0(Y)],
\]
where the limit inferior is taken as $n/(n+m)\to\rho\in[0,1]$, and $\mathbb E_{n,m,h_1,h_2}$ denotes the expectation taken over the probability measure $P_{n^{-1/2},h_1}^{\otimes n}\otimes Q_{m^{-1/2},h_2}^{\otimes m}$.
''', r'Asymptotic Minimax Lower Bound over $\mathbb T^d$')

paper = {k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=29, main_text_boundary=dict(location='Discussion ends on PDF page 29 before y=637.536865234375, where Appendix A: Smoothness Classes and Density Estimation begins. All content at and below this boundary is excluded except the boundary heading itself.', shared_page_with_appendix=True), intake_review=dict(status='complete', theorem_ids=[c['claim_id'] for c in claims], zero_theorems_confirmed=False))
inv = dict(schema_version='statistical-theorem-inventory-v1', scope=dict(theorem_scope='main_text_only'), papers=[paper], claims=claims)
pdf=fitz.open(prov['cached_pdf'])
assert len(pdf)==99 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
assert '2107.12364v3' in pdf[0].get_text() and '16 Jun 2024' in pdf[0].get_text()
headings=[]
for i in range(29):
    page=pdf[i]
    clip=fitz.Rect(0,0,page.rect.width,prov['main_text_end_y']) if i==28 else page.rect
    source=page.get_text(clip=clip)
    assert (ROOT/'evidence'/f'page-{i+1:02}.txt').read_bytes().decode('utf8')==source
    for m in re.finditer(r'^THEOREM (\d+)(?=[.\s(])',source,re.M):headings.append((i+1,int(m.group(1))))
assert headings==[(9,1),(10,3),(11,5),(12,6),(16,10),(21,18),(24,20),(26,22),(28,24)],headings
assert [(c['evidence'][0]['page'],int(c['claim_id'].split('/T')[-1])) for c in claims]==headings
assert 'APPENDIX A: SMOOTHNESS CLASSES AND DENSITY ESTIMATION' in pdf[28].get_text(clip=fitz.Rect(0,prov['main_text_end_y'],pdf[28].rect.width,651))
for c in claims:
    for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
        depth=0
        for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
            depth+=1 if b=='{' else -1
            assert depth>=0,c['claim_id']
        assert depth==0,c['claim_id']
path=ROOT/'theorem-inventory.json'
path.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
for n in [9,10,11,12,16,21,22,24,26,28]:
    shutil.copyfile(Path(prov['working_pdf']).parent/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=9,inventory_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),printed_heading_check=headings,notes=[
    'Independent main-text enumeration finds nine actual Theorem environments, including background Theorems 1, 3 and 5. Lemmas, Propositions, Corollaries and theorem mentions are excluded.',
    'Theorem 18 spans pages 21–22. All other Theorems are contained on their listed page. Theorem 20 ends with the printed comma; the following discussion and footnote are not part of its statement.',
    'Original PDF differentiates curly-phi Brenier potential (LaTeX varphi) from straight-phi Kantorovich potential (LaTeX phi). Neither is substituted for the other.',
    'Theorem 3 retains the closure over the interior subdomain and its noninteger smoothness qualifications. Theorem 5 retains the norm assertion without adding a potential normalization or a noninteger qualification absent from the source.',
    'Theorem 1 retains the source assertion of Lebesgue-almost-everywhere inverse identities and its finite-valued global convex potential without correcting or weakening the source.',
    'Theorem 10 has squared-logarithmic rate in dimension two; Theorem 18 has a single logarithm. Theorem 18 places both variance terms within one square root.',
    'Theorem 20 distinguishes the barred one-sample map from the hatted two-sample map and uses the one-dth power of L_n in the tuning condition.',
    'Theorem 22 retains references to (38)–(39) and the extra conjugate-potential condition for the two-sample hypercube assertion. The referenced limits and preceding tuning conventions must be separately archived during interface resolution.',
    'Theorem 24 has three barred constants M, gamma and u. Its supremum ranges over finite subsets, not intervals. The one- and two-sample local product experiments and sample-size ratio are preserved.',
    'The main-text preamble identifies the differentiable paths in Theorem 24 but refers their construction to Appendix L equations (115–116). These equations are outside scope and must remain explicitly unresolved.',
    'This validates the independent theorem inventory only. Main-text definitions, standing conditions, estimators, dependency relationships and source-backed selectors still require extraction before the paper census is complete.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve all nine Theorems against main-text transport definitions, smoothness classes, S1/A1/K1/C1/C2 conditions, wavelet/kernel/Laplacian estimators, sampling and limits (38)–(39), and differentiable-path notation. Preserve appendix-only definitions as unresolved. Extract source keywords, highlights and paper-local relationships, finalize and independently source-audit.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated nine complete main-text Theorems.')
