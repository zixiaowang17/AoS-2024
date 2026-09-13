"""Preserve all ten original main-text Theorems of the diffusion similarity paper."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,page,text,title=None):
    label='Theorem '+n+(' ('+title+')' if title else '')
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label=label,source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=page,location=label)]))
claim('3.1',9,r'''
Let $\Psi_{T,y,h}^{b_0}(X)$ be given as above for a continuous kernel $K$ of bounded variation with support $[-1,1]$ and $\|K\|_{[-1,1]}\le1$. Define
\[
\widehat\sigma_T(y,h)^2:=\frac1T\int_0^T K_{y,h}(X_s)^2\,ds\quad\text{and}\quad\widehat\sigma_{T,\max}^2:=\frac1T\int_0^T\mathbb1_{[-A,A]}(X_s)^2\,ds.
\]
Then under $\mathbb P_{b_0}$ the family (indexed in $T$)
\[
\sup_{(y,h)\in\mathcal T}\left(\left|\Psi_{T,y,h}^{b_0}(X)\right|-\Upsilon\bigl(\widehat\sigma_T(y,h)^2/\widehat\sigma_{T,\max}^2\bigr)\right)
\]
is asymptotically tight, where $0/0:=0$ in the argument of $\Upsilon(\cdot)$ and
\[
\Upsilon(r):=(2\log(1/r))^{\frac12}\mathbb1_{\{r>0\}}.
\]
''')
claim('4.1',12,r'''
Let $T_T^\eta$ be given as in (4.3) with a non-negative continuous kernel function $K$ of bounded variation supported in $[-1,1]$ with $\|K\|_{[-1,1]}\le1$. Furthermore, assume that $b_0\in\Sigma(C/2-\eta,A,\gamma+\eta/\sigma^2,\sigma)$. Then we have for any $r\in\mathbb R$,
\[
\limsup_{T\to\infty}\sup_{b\in H_0(b_0,\eta)}\mathbb P_b\bigl(T_T^\eta(X)\ge r\bigr)\le\mathbb P\left(U_1\vee U_2+4\sqrt{A\eta/\sigma^2}\ge r\right),
\]
where $U_1\vee U_2$ denotes the (pointwise) maximum of $U_1$ and $U_2$ given by
\[
U_1:=\sup_{(y,h)\in\mathcal T}\left(\left|\frac{\int_{-A}^A K_{y,h}(z)\sqrt{q_{b_0+\eta}(z)}\,dW_z}{\|K_{y,h}\sqrt{q_{b_0+\eta}}\|_{L^2}}\right|-\Upsilon\left(\frac{\|K_{y,h}\sqrt{q_{b_0+\eta}}\|_{L^2}^2}{\|\mathbb1_{[-A,A]}\sqrt{q_{b_0+\eta}}\|_{L^2}^2}\right)\right),
\]
\[
U_2:=\sup_{(y,h)\in\mathcal T}\left(\left|\frac{\int_{-A}^A K_{y,h}(z)\sqrt{q_{b_0-\eta}(z)}\,dW_z}{\|K_{y,h}\sqrt{q_{b_0-\eta}}\|_{L^2}}\right|-\Upsilon\left(\frac{\|K_{y,h}\sqrt{q_{b_0-\eta}}\|_{L^2}^2}{\|\mathbb1_{[-A,A]}\sqrt{q_{b_0-\eta}}\|_{L^2}^2}\right)\right).
\]
''')
claim('5.1',15,r'''
Let $\eta\ge0$ and $\psi_T$ be a test that is uniformly over $H_0(b_0,\eta)$ of level $\alpha$, i.e. $\sup_{b\in H_0(b_0,\eta)}\mathbb E_b[\psi_T]\le\alpha$, for some drift function $b_0\in\Sigma(C/2-\eta,A,\gamma+\eta/\sigma^2,\sigma)$. Then for arbitrary numbers $\epsilon_T>0$ with $\lim_{T\to\infty}\epsilon_T=0$ and $\lim_{T\to\infty}\epsilon_T\sqrt{\log T}=\infty$,
\[
\limsup_{T\to\infty}\inf_{\substack{b\in H_1(b_0,\eta)\cap\{b-b_0\in\mathcal H(\beta,L)\}:\\\Delta_J(b)\ge(1-\epsilon_T)c_*\delta_T}}\mathbb E_b[\psi_T]\le\alpha
\]
for any fixed compact interval $J\subset(-A,A)$.
''')
claim('5.2',16,r'''
Let $\beta,L>0$, $\eta>0$, $b_0\in\Sigma(C/2-\eta,A,\gamma+\eta/\sigma^2,\sigma)$ and let $K$ be a non-negative kernel of bounded variation supported in $[-1,1]$ with $\|K\|_{[-1,1]}=1$. Then for arbitrary numbers $\epsilon_T>0$ with $\lim_{T\to\infty}\epsilon_T=0$ and $\lim_{T\to\infty}\epsilon_T\sqrt{\log T}=\infty$ there exists a constant $c=c(\beta,L,K)$ such that for the test $\phi_T^\eta$ given in (4.7),
\[
\lim_{T\to\infty}\inf_{\substack{b\in H_1(b_0,\eta)\cap\{b-b_0\in\mathcal H(\beta,L)\}:\\\Delta_J(b)\ge(1+\epsilon_T)c\delta_T}}\mathbb P_b\bigl(\phi_T^\eta(X)=1\bigr)=1
\]
for any fixed compact interval $J\subset(-A,A)$. In the case $\beta\in(0,1]$ we can choose $K=K_\beta$ and the result is true for $c=c_*$.
''')
claim('5.3',16,r'''
Let $\beta,L>0$ and $b_0$, $K$ and $\epsilon_T$ be specified as in Theorem 5.2. Then for a compact subset $[\beta_1,\beta_2]\times[L_1,L_2]\subset(0,\infty)^2$ the test $\phi_T^\eta$ is rate-adaptive in both parameters $\beta$ and $L$ in the sense
\[
\lim_{T\to\infty}\inf_{(b,L)\in[\beta_1,\beta_2]\times[L_1,L_2]}\inf_{\substack{b\in H_1(b_0,\eta)\cap\{b-b_0\in\mathcal H(\beta,L)\}:\\\Delta_J(b)\ge(1+\epsilon_T)c(\beta,L,K)\delta_T}}\mathbb P_b\bigl(\phi_T^\eta(X)=1\bigr)=1.
\]
For $\beta\le1$ we have sharp adaptivity in the parameter $L\in[L_1,L_2]\subset(0,\infty)$ in the sense
\[
\lim_{T\to\infty}\inf_{L\in[L_1,L_2]}\inf_{\substack{b\in H_1(b_0,\eta)\cap\{b-b_0\in\mathcal H(\beta,L)\}:\\\Delta_J(b)\ge(1+\epsilon_T)c_*\delta_T}}\mathbb P_b\bigl(\phi_T^\eta(X)=1\bigr)=1.
\]
''',title='Adaptivity')
claim('5.4',17,r'''
Let $\beta,L>0$ and $b_0$ and $\epsilon_T$ be specified as in Theorem 5.2. Then the test $\phi_T^{b_0}$ given in (3.6) with the kernel $K=K_\beta$ satisfies for any compact interval $J\subset(-A,A)$
\[
\lim_{T\to\infty}\inf_{\substack{b\in H_{\ne}\cap\{b-b_0\in\mathcal H(\beta,L)\}:\\\Delta_J(b)\ge(1-\epsilon_T)c_*\delta_T}}\mathbb P_b\bigl(\phi_T^{b_0}=1\bigr)=1.
\]
''')
claim('6.1',19,r'''The mapping $\widetilde T_T^\eta:D_{A,T}\longrightarrow\mathbb R$ is continuous with respect to the topology of uniform convergence.''')
claim('6.3',20,r'''
Conditional on the event $\{X^{H,b},X^b\in D_{A,T}\}$, the test statistic $\widetilde T_T^\eta(X^{H,b})$ converges to $\widetilde T_T^\eta(X^b)$ in probability uniformly over drift functions $b\in\Sigma(C,A,\gamma,\sigma)\cap\mathcal H(1,L)$ for any $L>0$, i.e. for every $\epsilon>0$,
\[
\sup_{b\in\Sigma(C,A,\gamma,\sigma)\cap\mathcal H(1,L)}\mathbb P\left(\left|\widetilde T_T^\eta(X^{H,b})-\widetilde T_T^\eta(X^b)\right|>\epsilon\,\middle|\,X^{H,b},X^b\in D_{A,T}\right)\xrightarrow{H\to\frac12}0
\]
for $T$ sufficiently large. Moreover, we have for the conditioning event
\[
\begin{aligned}
&\liminf_{T\to\infty}\liminf_{H\to\frac12}\inf_{b\in\Sigma(C,A,\gamma,\sigma)\cap\mathcal H(1,L)}\mathbb P\bigl(X^{H,b},X^b\in D_{A,T}\bigr)\\
&\quad=\liminf_{H\to\frac12}\liminf_{T\to\infty}\inf_{b\in\Sigma(C,A,\gamma,\sigma)\cap\mathcal H(1,L)}\mathbb P\bigl(X^{H,b},X^b\in D_{A,T}\bigr)=1.
\end{aligned}
\]
''')
claim('6.5',21,r'''
Let $x_0\in[-A,A]$ and $b_0\in\Sigma(C/2-\eta,A,\gamma+\eta/\sigma^2,\sigma)$. Then for every $\epsilon>0$ there exists a sequence $\delta(T):=\delta(T,\epsilon)>0$ such that
\[
\limsup_{T\to\infty}\sup_{H:\,|H-\frac12|<\delta(T)}\sup_{\psi_T^H}\inf_{\substack{b\in H_1(b_0,\eta)\cap\{b-b_0\in\mathcal H(\beta,L)\}:\\\Delta_J(b)\ge(1-\epsilon_T)c_*\delta_T}}\mathbb E\left[\psi_T^H(X^{H,b})\right]\le\alpha+\epsilon,
\]
where $\sup_{\psi_T^H}$ is taken over tests $\psi_T^H$ with $\sup_{b\in H_0(b_0,\eta)}\mathbb E\left[\psi_T^H(X^{H,b})\right]\le\alpha$.
''')
claim('7.1',23,r'''
Let $K$ be given as in Theorem 4.1 and define the random variable $Z_b(y,h):=\int_{-A}^A K_{y,h}(z)\sqrt{q_b(z)}\,dW_z$ with a two-sided Brownian motion $W$ on $[-A,A]$, $\sigma_b(y,h):=\|K_{y,h}\sqrt{q_b}\|_{L^2}$, $\sigma_{b,\max}:=\|\mathbb1_{[-A,A]}\sqrt{q_b}\|_{L^2}$, and based on those
\[
S_b:=\sup_{(y,h)\in\mathcal T}\left(\frac{|Z_b(y,h)|}{\sigma_b(y,h)}-\Upsilon\left(\frac{\sigma_b(y,h)^2}{\sigma_{b,\max}^2}\right)\right).
\]
Then the following uniform weak convergence holds true:
\[
\sup_{b\in\Sigma(C,A,\gamma,\sigma)}d_{BL}^b\bigl(T_T^b(X),S_b\bigr)\xrightarrow{T\to\infty}0.
\]
''')

if __name__=='__main__':
    pdf=fitz.open(prov['cached_pdf']);assert len(pdf)==153
    assert hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==prov['pdf_sha256']
    first=' '.join(pdf[0].get_text().split());assert prov['title'].upper() in first
    for name in prov['authors']:assert name in first
    assert '2203.13776v3' in first and '16 Apr 2024' in first
    labels=[];mentions=[]
    for n in range(31):
        page=pdf[n];assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans']).strip();m=re.match(r'^Theorem\s+(\d+\.\d+)',text)
                if m:(labels if line['spans'][0]['font']=='CMCSC10' else mentions).append((n+1,m[1]))
    assert labels==[(9,'3.1'),(12,'4.1'),(15,'5.1'),(16,'5.2'),(16,'5.3'),(17,'5.4'),(19,'6.1'),(20,'6.3'),(21,'6.5'),(23,'7.1')]
    assert mentions==[(6,'1.16'),(9,'3.1'),(10,'3.1')]
    assert '[54]' in pdf[30].get_text()
    assert 'SUPPLEMENT TO' in pdf[31].get_text(clip=fitz.Rect(0,120,pdf[31].rect.width,170))
    for c in claims:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
            depth=0
            for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if b=='{' else -1
                assert depth>=0,c['claim_id']
            assert depth==0,c['claim_id']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=31,main_text_boundary=dict(location='References end on page 31. A separately titled supplement begins on page 32 with its title at y=127.30317687988281. Page 32 and all subsequent supplementary/appendix mathematics are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    path=ROOT/'theorem-inventory.json';path.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    for n in [9,12,15,16,17,19,20,21,23]:shutil.copyfile(Path(prov['working_pdf']).parent/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    notes=[
     'Pinned 153-page source is arXiv:2203.13776v3 dated 16 April 2024. Main text and references end on page 31; the separately titled supplement starts on page 32 and is excluded.',
     'Independent CMCSC10 heading enumeration finds ten main-text Theorems. Three ordinary-font mentions, including an external Theorem 1.16 citation, are excluded. All ten complete theorem bodies fit on their listed pages.',
     'Theorem 3.1 preserves both empirical variance definitions, the squared indicator, asymptotic tightness, the 0/0 convention in the correction argument and the original correction function.',
     'Theorem 4.1 preserves the uniform limsup over the composite null, the additive 4 sqrt(A eta/sigma^2) term and both full Gaussian supremum definitions. U1 and U2 use the same W as printed, without an independence assumption.',
     'Theorem 5.1 retains arbitrary uniform-level tests and the below-boundary (1-epsilon_T)c_*delta_T separation. Theorem 5.2 retains the above-boundary condition, kernel assumptions and sharp-constant beta<=1 case.',
     'Theorem 5.3 prints (b,L), not (beta,L), in the outer infimum over the smoothness rectangle. This mismatch is retained literally rather than repaired. Both rate and sharp-adaptivity statements are complete.',
     'Theorem 5.4 prints a (1-epsilon_T)c_*delta_T threshold in its power-one conclusion. This differs from the plus sign in Theorem 5.2 and apparently conflicts with the matching lower-bound interpretation; the original minus sign is preserved.',
     'Theorem 6.1 is the complete short continuity statement. Theorem 6.3 includes both conditional uniform convergence and both orders of the iterated limits for the conditioning event.',
     'Theorem 6.5 preserves the order of limsup, H supremum, test supremum and alternative infimum, the alpha+epsilon bound and the defining uniform-level restriction on the tests. Its delta(T) Hurst neighborhood differs from the separation sequence delta_T.',
     'Theorem 7.1 includes all Gaussian variable/variance/S_b definitions and the uniform weak-convergence conclusion. The following regular-font paragraph on page 24 explains the bounded-Lipschitz metric and points to Appendix F.1; it is context, not part of the theorem body.',
     'Scalar statistics T_T and path domain D_{A,T} use plain italic capitals; the index set and Holder class use script T,H. Hypothesis H is plain italic, probability/expectation are blackboard bold, and c_* has a subscript star.',
     'Only the independent theorem inventory is complete. Resolve drift classes, stationary versus fixed-start diffusion laws, similarity hypotheses, kernels, all statistics and quantiles, weighted separation, optimal-recovery kernels, pathwise extension/domain, the fractional coupling and metric references from main text before completing the census.'
    ]
    (ROOT/'inventory-review.json').write_text(json.dumps(dict(paper_id=PID,status='complete',source_checked=True,inventory_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='Independent small-caps heading enumeration on main-text pages 1–31 followed by visual review of every complete theorem body.',theorem_ids=[c['claim_id'] for c in claims],notes=notes),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),next_action='Extract all main-text prerequisites of the ten saved Theorems. Resolve Sections 2–5 first (drift/diffusion model, hypotheses, kernels/statistics/quantiles, Holder classes, weighted distance and optimal-recovery constant), then the pathwise domain/extension and fractional coupling of Section6 and bounded-Lipschitz metric for7.1. Keep appendix-only K_H in (I.8), any appendix-only h_min(T), and metric details in F.1 explicitly unresolved if the main text does not define them. Preserve all printed sign/index/variable mismatches.'),indent=2)+'\n')
    print('Saved and independently validated all ten original Theorems.')
