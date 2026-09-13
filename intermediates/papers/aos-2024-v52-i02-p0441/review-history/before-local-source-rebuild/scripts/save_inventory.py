"""Save both printed main-text Theorems, independently of interface extraction."""
import hashlib,json,re,subprocess,sys,shutil
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,page,body):claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=page,location='Theorem '+n)]))
claim('4.2',11,r'''
Let $n$ i.i.d pairs $(\boldsymbol x_i,y_i)$ be drawn from the data model (2.1) and let $\widehat{\boldsymbol\theta}^{\varepsilon}$ be the robust ERM fit (4.3) to this data using the class of random features models $\mathcal F_{\mathrm{RF}}(\boldsymbol W)$, given by (2.2) with the shifted ReLU activation. Consider the asymptotic regime, described in Assumption 1. With function $S(\cdot;\psi_1)$ given by (4.4), define
\[
\sigma^2=\tau^2+1-\psi_1\left(1+\left(1-\frac2\pi\right)S\left(\frac2\pi-1;\psi_1\right)\right).
\]
(a) For $\varepsilon>0$, the following convex-concave minimax scalar optimization has a unique solution $(\alpha_\star,\tau_{g\star},\beta_\star,\gamma_\star,\tau_{q\star})$:
\[
\max_{0\leq\beta,\gamma,\tau_q}\min_{0\leq\alpha,\tau_g}\mathcal R(\alpha,\tau_g,\beta,\gamma,\tau_q),\tag{4.5}
\]
where
\[
\begin{aligned}
\mathcal R(\alpha,\tau_g,\beta,\gamma,\tau_q)&:=\frac{\tau_q}{2\alpha}(\tau^2+1-\sigma^2)-\frac{\alpha\tau_q}2+\frac{\beta\tau_g}2\psi_2+\frac{\beta}{2(\tau_g+\beta)}(\sigma^2+\alpha^2)\\
&\quad+\boldsymbol 1_{\left\{\frac{\gamma(\tau_g+\beta)}{\varepsilon\beta\sqrt{\alpha^2+\sigma^2}}>\sqrt{\frac2\pi}\right\}}\frac{\beta^2(\alpha^2+\sigma^2)}{2\tau_g(\tau_g+\beta)}\left(\operatorname{erf}\left(\frac{\nu^*}{\sqrt2}\right)-\frac{\gamma(\tau_g+\beta)}{\varepsilon\beta\sqrt{\alpha^2+\sigma^2}}\nu^*\right)\\
&\quad-\frac\alpha{\tau_q}\sup_{0\leq\lambda<1}\left[\frac{\lambda\psi_1}2\left\{\frac{\tau_q^2}{\alpha^2}+\beta^2+\left(\frac{\tau_q^2}{\alpha^2}\left(1-\frac2\pi\lambda\right)+\frac2\pi(1-\lambda)\beta^2\right)S\left(\frac2\pi\lambda-1;\psi_1\right)\right\}-\frac\lambda{2(1-\lambda)}\gamma^2\right].
\end{aligned}
\]
Here, $\nu^*$ is the unique solution to
\[
\frac{\gamma(\tau_g+\beta)}{\varepsilon\beta\sqrt{\alpha^2+\sigma^2}}-\frac\beta{\tau_g}\nu-\nu\cdot\operatorname{erf}\left(\frac\nu{\sqrt2}\right)-\sqrt{\frac2\pi}e^{-\nu^2/2}=0.
\]
(b) The adversarial risk of the robust ERM $\widehat{\boldsymbol\theta}^{\varepsilon}$ converges in probability
\[
\mathrm{AR}(\widehat{\boldsymbol\theta}^{\varepsilon})\xrightarrow{\mathcal P}\left[1+\left(\frac{\varepsilon_{\mathrm{test}}\beta_\star\nu_\star}{\varepsilon\tau_{g\star}}\right)^2+2\sqrt{\frac2\pi}\frac{\varepsilon_{\mathrm{test}}\beta_\star\nu_\star}{\varepsilon\tau_{g\star}}\right](\alpha_\star^2+\sigma^2).\tag{4.6}
\]
Here, the probabilistic statement is with respect to the randomness in both the training data $\{(\boldsymbol x_i,y_i)\}_{i=1}^n$ and the random features $\boldsymbol W$.
''')
claim('6.9',20,r'''
Consider the quantities $\Phi_A$ and $\Phi_B$ defined as
\[
\Phi_A:=\min_{\boldsymbol\theta}\frac1n\sum_{i=1}^n\left(|y_i-\boldsymbol\theta^\top\sigma(\boldsymbol W\boldsymbol x_i)|+\varepsilon\|\boldsymbol J\boldsymbol\theta\|_{\ell_2}\right)^2+\lambda\|\boldsymbol\theta\|_{\ell_2}^2+\lambda_w\left\|\frac12\boldsymbol W^\top\boldsymbol\theta-\boldsymbol\beta\right\|_{\ell_2}^2+\lambda_s\frac{\log(d)}d(\boldsymbol 1^\top\boldsymbol\theta)^2,
\]
\[
\Phi_B:=\min_{\boldsymbol\theta}\frac1n\sum_{i=1}^n\left(y_i-\boldsymbol\theta^\top\boldsymbol f_i+\varepsilon\|\boldsymbol J\boldsymbol\theta\|_{\ell_2}\right)^2+\lambda\|\boldsymbol\theta\|_{\ell_2}^2+\lambda_w\left\|\frac12\boldsymbol W^\top\boldsymbol\theta-\boldsymbol\beta\right\|_{\ell_2}^2+\lambda_s\frac{\log(d)}d(\boldsymbol 1^\top\boldsymbol\theta)^2,
\]
where $\lambda,\lambda_s,\lambda_w>0$, and $(\boldsymbol x_i,y_i)$ is generated i.i.d. according to (2.1). We further assume that the event $\mathcal E_{\boldsymbol W}$ holds. Then, we have
\[
\Phi_A\xrightarrow{\mathcal P}c\text{ if and only if }\Phi_B\xrightarrow{\mathcal P}c,\tag{6.22}
\]
where $\xrightarrow{\mathcal P}$ denotes convergence in probability.
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=25,main_text_boundary=dict(location='Main discussion and supplementary-material notice end on page 22. References continue through page 25. The separate-title supplementary material begins on PDF page 26 and its appendix sections start on page 27; all supplementary pages 26-86 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
for c in claims:
 for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
  depth=0
  for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
   depth+=1 if b=='{' else -1
   assert depth>=0,c['claim_id']
  assert depth==0,c['claim_id']
p=ROOT/'theorem-inventory.json';p.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(p)],check=True)
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.now(timezone.utc).isoformat(),theorem_count=2,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),notes=[
 'Pinned arXiv:2201.05149v2, stamped 1 February 2024. Searched all 25 main-text pages; actual Theorem environments occur only on pages 11 and 20.',
 'Theorem 4.2 includes its full scalar objective, indicator threshold, nested supremum, unique-root equation, both subparts and the final probability-scope sentence. The following page begins upright discussion outside the theorem.',
 'Theorem 4.2 uses superscript epsilon on theta-hat; it defines nu with a superscript star in part (a), but writes nu with a subscript star in (4.6). These printed positions are retained.',
 'Theorem 6.9 is included even though it appears in the proof-outline section. Both Phi objectives and the iff convergence assertion are preserved. Proposition 6.10 immediately below it is excluded.',
 'Phi_A has an absolute residual; Phi_B in the theorem lacks the absolute-value bars. The discrepancy with the nearby noisy-linear objective in Proposition 6.10 is not repaired.',
 'The source outline lists the first appendix at page 27, but the separate supplementary title page is already page 26. Its introductory content is not used in the census; only a title crop is retained for the boundary.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,10,11,12,20,22,25]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
for name in ['supplement-title','risk-limit','scalar-objective','comparison-objectives']:shutil.copy2(work/(name+'.png'),ROOT/'evidence'/(name+'.png'))
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve the random-features and data models, risk/ERM definitions, Stieltjes formula, J matrix, Gaussian surrogate features and event E_W from the main text. Keep inline scalar optimization quantities separate from reusable prerequisites.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated both Theorems.')
