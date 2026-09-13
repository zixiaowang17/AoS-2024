"""Preserve all eleven printed main-text Theorems before interface extraction."""
import hashlib,json,re,subprocess,sys,shutil
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i02-p0415', 'title': 'High-dimensional inference for dynamic treatment effects', 'version': 'arXiv:2110.04924v4', 'source_url': 'https://arxiv.org/pdf/2110.04924v4', 'pdf_pages': 85, 'pdf_sha256': 'ea5850b94eb3e9fbb8c8a5444fe0db7a64ba55ddb37f21e9c87b7722a5483123'}
claims=[]
def claim(n,pages,body,title=None):
 claims.append(dict(claim_id=PID+'/T'+str(n),paper_id=PID,claim_kind='theorem',label='Theorem '+str(n)+((' ('+title+')') if title else ''),source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+str(n)+(' — continuation' if j else '')) for j,p in enumerate(pages)]))
claim(1,[3],r'''
Suppose that either $\nu_a^*(\cdot)=\nu_a(\cdot)$ or $\rho_a^*(\cdot)=\rho_a(\cdot)$ holds. Let Assumption 1 holds. Then, for any $\mathbf s_1\in\mathbb R^{d_1}$,
\[
\mu_a(\mathbf s_1)=E\left[\nu_a^*(\mathbf S)+\mathbb 1_{\{A_2=a_2\}}\frac{Y-\nu_a^*(\mathbf S)}{\rho_a^*(\mathbf S)}\mid\mathbf S_1=\mathbf s_1,A_1=a_1\right].\tag{1.4}
\]
''',r'A DR representation of $\mu_a(\cdot)$')
claim(2,[10],r'''
Suppose that at least one of $\mu_a^*(\cdot)$ and $\pi_a^*(\cdot)$ is correctly specified, and at least one of the models $\nu_a^*(\cdot)$ and $\rho_a^*(\cdot)$ is correctly specified. Let Assumptions 1-4 hold. Assume that $\max\{s_{\alpha_a},s_{\beta_a},s_{\gamma_a},s_{\delta_a}\}\log(d)=o(N)$, and either (a) $\|\mathbf S_1\|_\infty\leq C$ almost surely, with a constant $C>0$, or (b) $s_{\delta_a}\log^2(d)=O(N)$. Then the sequential DR Lasso (S-DRL) estimator, $\widehat\theta$, as defined in Algorithm 1, satisfies
\[
\widehat\theta-\theta=O_p\left(\sigma\frac{s_1\log(d)}N+\sigma\sqrt{\frac{s_2\log(d)}N}+\frac1{\sqrt N}\sigma\right),
\]
as $N,d\to\infty$, with $s_1:=\max\{\sqrt{s_{\alpha_a}s_{\delta_a}},\sqrt{s_{\beta_a}s_{\gamma_a}}\}$ and $s'_2:=\max\{s_{\alpha_a}\mathbb 1_{\{\pi_a^*\ne\pi_a\ \mathrm{or}\ \rho_a^*\ne\rho_a\}},s_{\beta_a}\mathbb 1_{\{\pi_a^*\ne\pi_a\}},s_{\gamma_a}\mathbb 1_{\{\mu_{a,NR}^*\ne\mu_a\}},s_{\delta_a}\mathbb 1_{\{\nu_a^*\ne\nu_a\}}\}$.
''','Consistency of the S-DRL')
claim(3,[11],r'''
Suppose that all the nuisance models $\mu_a^*(\cdot)$, $\nu_a^*(\cdot)$, $\pi_a^*(\cdot)$, and $\rho_a^*(\cdot)$ are correctly specified. Let Assumptions 1-3 hold. Assume that $\max\{s_{\alpha_a},s_{\beta_a},s_{\gamma_a},s_{\delta_a}\}\log(d)=o(N)$, and either (a) $\|\mathbf S_1\|_\infty\leq C$ almost surely, with some constant $C>0$, or (b) $s_{\delta_a}\log^2(d)=O(N)$. Additionally, assume the following product-rate condition:
\[
\max\{s_{\gamma_a}s_{\beta_a},s_{\delta_a}s_{\alpha_a}\}\log^2(d)=o(N).\tag{3.2}
\]
Then, with $\sigma^2$ in (3.1) and $\widehat\sigma^2$ in (2.8), the S-DRL estimator satisfies $\sigma^{-1}\sqrt N(\widehat\theta-\theta)\rightsquigarrow N(0,1)$ and $\widehat\sigma^{-1}\sqrt N(\widehat\theta-\theta)\rightsquigarrow N(0,1)$ as $N,d\to\infty$.
''','Asymptotic normality of the S-DRL')
claim(4,[11,12],r'''
Suppose that at least one of $\mu_{a,NR}^*(\cdot)$ and $\pi_a^*(\cdot)$ is correctly specified, and at least one of the models $\nu_a^*(\cdot)$ and $\rho_a^*(\cdot)$ is correctly specified. Let Assumptions 1-4 hold with $\mu_a^*(\cdot)$ and $\boldsymbol\beta_a^*$ replaced by $\mu_{a,NR}^*(\cdot)$ and $\boldsymbol\beta_{a,NR}^*$. Assume that $\max\{s_{\alpha_a},s_{\beta_a},s_{\gamma_a},s_{\delta_a}\}\log(d)=o(N)$. Then the DTL estimator satisfies, as $N,d\to\infty$,
\[
\widehat\theta_{DTL}-\theta=O_p\left(\sigma\frac{s'_1\log(d)}N+\sigma\sqrt{\frac{s'_2\log(d)}N}+\frac1{\sqrt N}\sigma\right),\tag{3.3}
\]
with $s'_1:=\max\{\sqrt{s_{\alpha_a}s_{\gamma_a}},\sqrt{s_{\alpha_a}s_{\delta_a}},\sqrt{s_{\beta_a}s_{\gamma_a}}\}$ and $s'_2:=\max\{s_{\alpha_a}\mathbb 1_{\{\pi_a^*\ne\pi_a\ \mathrm{or}\ \rho_a^*\ne\rho_a\}},s_{\beta_a}\mathbb 1_{\{\pi_a^*\ne\pi_a\}},s_{\gamma_a}\mathbb 1_{\{\mu_{a,NR}^*\ne\mu_a\}},s_{\delta_a}\mathbb 1_{\{\nu_a^*\ne\nu_a\}}\}$.
''','Consistency of the DTL')
claim(5,[12],r'''
Suppose that all the nuisance models $\mu_{a,NR}^*(\cdot)$, $\nu_a^*(\cdot)$, $\pi_a^*(\cdot)$, and $\rho_a^*(\cdot)$ are correctly specified. Let Assumptions 1-3 hold with $\mu_a^*(\cdot)$ and $\boldsymbol\beta_a^*$ replaced by $\mu_{a,NR}^*(\cdot)$ and $\boldsymbol\beta_{a,NR}^*$. Assume that $\max\{s_{\alpha_a},s_{\beta_a},s_{\gamma_a},s_{\delta_a}\}\log(d)=o(N)$. Additionally, assume the following product-rate condition:
\[
\max\{s_{\gamma_a}s_{\beta_a},s_{\delta_a}s_{\alpha_a},s_{\gamma_a}s_{\alpha_a}\}\log^2(d)=o(N).\tag{3.4}
\]
Then, with $\sigma^2$ in (3.1) and $\widehat\sigma^2_{DTL}$ in (2.13), the DTL estimator satisfies $\sigma^{-1}\sqrt N(\widehat\theta_{DTL}-\theta)\rightsquigarrow N(0,1)$ and $\widehat\sigma^{-1}_{DTL}\sqrt N(\widehat\theta_{DTL}-\theta)\rightsquigarrow N(0,1)$ as $N,d\to\infty$.
''','Asymptotic normality of the DTL')
claim(6,[13],r'''
(Consistency of the general DR estimator) Suppose that at least one of $\mu_a^*(\cdot)$ and $\pi_a^*(\cdot)$ is correctly specified, and at least one of $\nu_a^*(\cdot)$ and $\rho_a^*(\cdot)$ is correctly specified. Let Assumptions 1, 4, and 5 hold. Additionally, let $E[\mathbb 1_{\{A_1=a_1\}}(\mu_a(\mathbf S_1)-\mu_a^*(\mathbf S_1))^2]\leq C_\mu\sigma^2$, for some $C_\mu>0$. Then the general DR estimator, $\widehat\theta_{gen}$, satisfies $\widehat\theta_{gen}-\theta=O_p(q_N)$ as $N,d\to\infty$, where $q_N=b_Nc_N+a_Nd_N+b_N\mathbb 1_{\{\pi_a^*\ne\pi_a\}}+a_N\mathbb 1_{\{\rho_a^*\ne\rho_a\}}+c_N\sigma\mathbb 1_{\{\mu_a^*\ne\mu_a\}}+d_N\sigma\mathbb 1_{\{\nu_a^*\ne\nu_a\}}+\sigma/\sqrt N$.
''')
claim(7,[14],r'''
(Asymptotic normality of the general DR estimator) Suppose that all the nuisance models $\mu_a^*(\cdot)$, $\nu_a^*(\cdot)$, $\pi_a^*(\cdot)$, and $\rho_a^*(\cdot)$ are correctly specified. Whenever Assumptions 1, 5 hold and the rates of estimation satisfy the following product conditions
\[
b_Nc_N=o(\sigma N^{-1/2}),\qquad a_Nd_N=o(\sigma N^{-1/2}),\tag{3.7}
\]
then the estimator $\widehat\theta_{gen}$ satisfies $\sigma^{-1}\sqrt N(\widehat\theta_{gen}-\theta)\rightsquigarrow N(0,1)$ and $\widehat\sigma^{-1}_{gen}\sqrt N(\widehat\theta_{gen}-\theta)\rightsquigarrow N(0,1)$ as $N\to\infty$ (and potentially $d\to\infty$), where $\sigma^2$ and $\widehat\sigma^2_{gen}$ are defined in (3.6) and (2.17), respectively.
''')
claim(8,[15],r'''
Let $s=\|\boldsymbol\beta^*\|_0$ and $\varepsilon_i:=Y_i^*-\mathbf X_i^\top\boldsymbol\beta^*$. Suppose that $\|\mathbf a^\top\mathbf X\|_{\psi_2}\leq\sigma_X\|\mathbf a\|_2$ for $\mathbf a\in\mathbb R^d$, $\lambda_{\min}(E[\mathbf X\mathbf X^\top])>\lambda_X$, and $\|\varepsilon\|_{\psi_2}\leq\sigma$ with $\sigma_X,\lambda_X>0$ and $\sigma=\sigma_M>0$ potentially dependent on $M$. For some $\delta_M>0$, define the event $\mathcal E_1:=\{M^{-1}\sum_{i=1}^M[\widehat Y_i-Y_i^*]^2<\delta_M^2\}$. For any $t>0$, let $\lambda_M:=16\sigma\sigma_X(\sqrt{\log(d)/M}+t)$. Then on the event $\mathcal E_1$, when $M>\max\{\log(d),100\kappa_2^2s\log(d)\}$, we have
\[
\|\widehat{\boldsymbol\beta}-\boldsymbol\beta^*\|_2\leq\max\left(\frac{5\kappa_2\delta_M^2}{4\sigma\sigma_X}+4\kappa_1^{-1/2}\delta_M,8\kappa_1^{-1}\sqrt s\lambda_M\right),
\]
with probability at least $1-2\exp(-\frac{4Mt^2}{1+2t+\sqrt{2t}})-c_1\exp(-c_2M)$, where $\kappa_1,\kappa_2,c_1,c_2>0$ are constants independent of $M$ and $d$. Moreover, if $\delta_M=o(\sigma)$, $P(\mathcal E_1)=1-o(1)$, and $M\gg s\log(d)$, then with $\lambda_M\asymp\sigma\sqrt{\log(d)/M}$, as $M,d\to\infty$,
\[
\|\widehat{\boldsymbol\beta}-\boldsymbol\beta^*\|_2=O_p\left(\sigma\sqrt{\frac{s\log(d)}M}+\delta_M\right).\tag{4.2}
\]
''','General imputed Lasso estimators')
claim(9,[16],r'''
Let Assumptions 1-4 hold. Assume that $\max\{s_{\alpha_a}\log(d),s_{\beta_a}\log(d_1),s_{\delta_a}\log(d)\}=o(N)$, and either (a) $\|\mathbf S_1\|_\infty\leq C$ almost surely, with some constant $C>0$, or (b) $s_{\delta_a}\log(d_1)\log(d)=O(N)$. Choose some $\lambda_\alpha\asymp\sigma\sqrt{\log(d)/N}$, $\lambda_\beta\asymp\sigma\sqrt{\log(d_1)/N}$, and $\lambda_\delta\asymp\sqrt{\log(d)/N}$. Then for any constant $r\geq1$, as $N,d\to\infty$, we have
\[
\|\widehat{\boldsymbol\beta}_a-\boldsymbol\beta_a^*\|_2+\{E[\widehat\mu_a(\mathbf S_1)-\mu_a^*(\mathbf S_1)]^r\}^{1/r}=O_p(r_n),
\]
with $r_n$ being determined as follows (a) whenever $\rho_a^*(\cdot)=\rho_a(\cdot)$ and $\nu_a^*(\cdot)=\nu_a(\cdot)$, $r_n=\sigma\sqrt{\frac{s_{\beta_a}\log(d_1)}N}+\frac{\sigma\sqrt{s_{\delta_a}s_{\alpha_a}}\log(d)}N$, (b) whenever $\rho_a^*(\cdot)=\rho_a(\cdot)$, $r_n=\sigma\sqrt{\frac{s_{\beta_a}\log(d_1)}N}+\sigma\sqrt{\frac{s_{\delta_a}\log(d)}N}$, (c) or whenever $\nu_a^*(\cdot)=\nu_a(\cdot)$, $r_n=\sigma\sqrt{\frac{s_{\beta_a}\log(d_1)}N}+\sigma\sqrt{\frac{s_{\alpha_a}\log(d)}N}$.
''')
claim(10,[16],r'''
Let Assumptions 1-3 hold. Assume that $\max\{s_{\alpha_a}\log(d),s_{\beta_a}\log(d_1)\}=o(N)$. Choose some $\lambda_\alpha\asymp\sigma\sqrt{\log(d)/N}$ and $\lambda_\beta\asymp\sigma\sqrt{\log(d_1)/N}$. Then for any constant $r\geq1$, as $N,d\to\infty$, we have with $r_n$ as in Theorem 9(c),
\[
\|\widehat{\boldsymbol\beta}_{a,NR}-\boldsymbol\beta_{a,NR}^*\|_2+\{E[\widehat\mu_{a,NR}(\mathbf S_1)-\mu_{a,NR}^*(\mathbf S_1)]^r\}^{1/r}=O_p(r_n).\tag{4.3}
\]
''')
claim(11,[18],r'''
Let Assumption 6 hold. For $t\leq T-1$ and $t+1\leq r\leq T$, suppose that either $\pi_r^*(\cdot,\bar a_r)$ or $\mu_r^*(\cdot,\bar a_T)$ is correctly specified, i.e., either $\pi_r^*(\cdot,\bar a_r)=\pi_r(\cdot,\bar a_r)$ or $\mu_r^*(\cdot,\bar a_T)=\mu_r(\cdot,\bar a_T)$. Then $\mu_t(\bar{\mathbf s}_t,\bar a_T)=E[\psi^*(W_T,\bar a_T)\mid\bar{\mathbf S}_t=\bar{\mathbf s}_t,\bar A_t=\bar a_t]$, where
\[
\psi^*(W_T,\bar a_T):=\sum_{r=t+1}^T\frac{\prod_{l=t+1}^r\mathbb 1_{\{A_l=a_l\}}}{\prod_{l=t+1}^r\pi_l^*(\bar{\mathbf S}_l,\bar a_l)}(\mu_{r+1}^*(\bar{\mathbf S}_{r+1},\bar a_T)-\mu_r^*(\bar{\mathbf S}_r,\bar a_T))+\mu_{t+1}^*(\bar{\mathbf S}_{t+1},\bar a_T).
\]
''')
def main():
    repo = Path(__file__).resolve().parents[5]
    source = Path(subprocess.check_output([sys.executable, str(repo / 'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == prov['pdf_sha256'], 'Registered PDF version changed; review before rebuilding.'
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=25,main_text_boundary=dict(location='Main article discussion, acknowledgments and supplement notice end on page 23; references occupy pages 24-25. The embedded Supplementary Materials begins on page 26. Pages 26-85 are excluded from the census.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
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
    print('Regenerated eleven saved theorem transcriptions; source review is a separate step.')

if __name__ == '__main__':
    main()
