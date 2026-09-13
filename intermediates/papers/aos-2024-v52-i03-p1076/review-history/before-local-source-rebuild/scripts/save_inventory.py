"""Transcribe all ten main-text Theorems in the pinned spectral two-sample paper."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,title,pages,text):
    label='Theorem '+n+(' ('+title+')' if title else '')
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label=label,source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location=label+(' — continuation' if i else '')) for i,p in enumerate(pages)]))
claim('3.1','Separation boundary of MMD test',[7],r'''
Suppose $(A_0)$ holds. Let $N\ge2$, $M\ge2$, $M\le N\le DM$, for some constant $D>1$, $k\in\{1,2\}$, and
\[
\sup_{(P,Q)\in\mathcal P}\|\mathcal T^{-\theta}u\|_{L^2(R)}<\infty.\tag{3.3}
\]
Then for any $\alpha>0$, $\delta>0$, $P_{H_0}\{\widehat D_{\mathrm{MMD}}^2\ge\gamma_k\}\le\alpha$,
\[
\inf_{(P,Q)\in\mathcal P}P_{H_1}\{\widehat D_{\mathrm{MMD}}^2\ge\gamma_k\}\ge1-k\delta,\quad k=1,2,
\]
where $\gamma_1=\frac{2\sqrt6\kappa}{\sqrt\alpha}\left(\frac1N+\frac1M\right)$, $\gamma_2=q_{1-\alpha}$,
\[
\Delta_{N,M}:=\Delta=c_k(\alpha,\delta)(N+M)^{-\frac{2\theta}{2\theta+1}},
\]
$c_1(\alpha,\delta)\asymp\max\{\alpha^{-1/2},\delta^{-1}\}$ and $c_2(\alpha,\delta)\asymp\delta^{-1}\log\frac1\alpha$, with $q_{1-\alpha}$ being the $(1-\alpha)$-quantile of the permutation function of $\widehat D_{\mathrm{MMD}}^2$ based on $(N+M)!$ permutations of the samples $(\mathbb X_N,\mathbb Y_M)$.

Furthermore, suppose $\Delta_{N,M}(N+M)^{\frac{2\theta}{2\theta+1}}\to0$ as $N,M\to\infty$ and one of the following holds: (i) $\theta\ge\frac12$, (ii) $\sup_i\|\phi_i\|_\infty<\infty$, $\theta>0$. Then for any decay rate of $(\lambda_i)_i$,
\[
\liminf_{N,M\to\infty}\inf_{(P,Q)\in\mathcal P}P_{H_1}\{\widehat D_{\mathrm{MMD}}^2\ge\gamma_k\}<1.
\]
''')
claim('3.2','Minimax separation boundary',[8],r'''
Suppose $\lambda_i\asymp L(i)$, where $L(\cdot)$ is a strictly decreasing function on $(0,\infty)$, and $M\le N\le DM$. Then, for any $0\le\delta\le1-\alpha$, there exists $c(\alpha,\delta)$ such that if
\[
(N+M)\Delta_{N,M}\le c(\alpha,\delta)\sqrt{\min\left\{L^{-1}\left(\Delta_{N,M}^{1/2\theta}\right),L^{-1}(\Delta_{N,M})\right\}}
\]
then
\[
R_{\Delta_{N,M}}^*:=\inf_{\phi\in\Phi_{N,M,\alpha}}R_{\Delta_{N,M}}(\phi)>\delta,
\]
where $R_{\Delta_{N,M}}(\phi):=\sup_{(P,Q)\in\mathcal P}\mathbb E_{P^N\times Q^M}[1-\phi]$.

Furthermore if $\sup_k\|\phi_k\|_\infty<\infty$, then the above condition on $\Delta_{N,M}$ can be replaced by
\[
(N+M)\Delta_{N,M}\le c(\alpha,\delta)\sqrt{\min\left\{L^{-1}\left(\Delta_{N,M}^{1/2\theta}\right),\Delta_{N,M}^{-2}\right\}}.
\]
''')
claim('4.1','',[12],r'''
Let $(\widehat\lambda_i,\widehat\alpha_i)_i$ be the eigensystem of $\frac1s\widetilde{\boldsymbol H}_s^{1/2}K_s\widetilde{\boldsymbol H}_s^{1/2}$ where $K_s:=[K(Z_i,Z_j)]_{i,j\in[s]}$, $\boldsymbol H_s=\boldsymbol I_s-\frac1s\mathbf1_s\mathbf1_s^\top$, and $\widetilde{\boldsymbol H}_s=\frac{s}{s-1}\boldsymbol H_s$. Define $G:=\sum_i\left(\frac{g_\lambda(\widehat\lambda_i)-g_\lambda(0)}{\widehat\lambda_i}\right)\widehat\alpha_i\widehat\alpha_i^\top$. Then
\[
\widehat\eta_\lambda=\frac1{n(n-1)}\left(\text{①}-\text{②}\right)+\frac1{m(m-1)}\left(\text{③}-\text{④}\right)-\frac2{nm}\text{⑤},
\]
where $\text{①}=\mathbf1_n^\top A_1\mathbf1_n$, $\text{②}=\operatorname{Tr}(A_1)$, $\text{③}=\mathbf1_n^\top A_2\mathbf1_n$, $\text{④}=\operatorname{Tr}(A_2)$, and
\[
\text{⑤}=\mathbf1_m^\top\left(g_\lambda(0)K_{mn}+\frac1sK_{ms}\widetilde{\boldsymbol H}_s^{1/2}G\widetilde{\boldsymbol H}_s^{1/2}K_{ns}^\top\right)\mathbf1_n,
\]
with $A_1:=g_\lambda(0)K_n+\frac1sK_{ns}\widetilde{\boldsymbol H}_s^{1/2}G\widetilde{\boldsymbol H}_s^{1/2}K_{ns}^\top$ and $A_2:=g_\lambda(0)K_m+\frac1sK_{ms}\widetilde{\boldsymbol H}_s^{1/2}G\widetilde{\boldsymbol H}_s^{1/2}K_{ms}^\top$. Here $K_n:=[K(X_i,X_j)]_{i,j\in[n]}$, $K_m:=[K(Y_i,Y_j)]_{i,j\in[m]}$, $[K(X_i,Z_j)]_{i\in[n],j\in[s]}=:K_{ns}$, $K_{ms}:=[K(Y_i,Z_j)]_{i\in[m],j\in[s]}$, and $K_{mn}:=[K(Y_i,X_j)]_{i\in[m],j\in[n]}$.
''')
claim('4.2','Critical region–Oracle',[13],r'''
Let $n\ge2$ and $m\ge2$. Suppose $(A_0)$–$(A_2)$ hold. Then for any $\alpha>0$ and $\frac{140\kappa}{s}\log\frac{48\kappa s}{\alpha}\le\lambda\le\|\Sigma_{PQ}\|_{\mathcal L^\infty(\mathscr H)}$,
\[
P_{H_0}\{\widehat\eta_\lambda\ge\gamma\}\le\alpha,
\]
where $\gamma=\frac{6\sqrt2(C_1+C_2)\mathcal N_2(\lambda)}{\sqrt\alpha}\left(\frac1n+\frac1m\right)$. Furthermore if $C:=\sup_i\|\phi_i\|_\infty<\infty$, the above bound holds for $136C^2\mathcal N_1(\lambda)\log\frac{24\mathcal N_1(\lambda)}{\delta}\le s$ and $\lambda\le\|\Sigma_{PQ}\|_{\mathcal L^\infty(\mathscr H)}$.
''')
claim('4.3','Separation boundary–Oracle',[14,15],r'''
Suppose $(A_0)$–$(A_4)$ and $(B)$ hold. Let $s=d_1N=d_2M$, $\sup_{(P,Q)\in\mathcal P}\|\mathcal T^{-\theta}u\|_{L^2(R)}<\infty$, $\|\Sigma_{PQ}\|_{\mathcal L^\infty(\mathscr H)}\ge\lambda=d_\theta\Delta_{N,M}^{\frac1{2\widetilde\theta}}$, for some constants $0<d_1,d_2<1$ and $d_\theta>0$, where $d_\theta$ is a constant that depends on $\theta$. For any $0<\delta\le1$, if $N+M\ge\frac{32\kappa d_1}{\delta}$ and $\Delta_{N,M}$ satisfies
\[
\frac{\Delta_{N,M}^{\frac{2\widetilde\theta+1}{2\widetilde\theta}}}{\mathcal N_2\left(d_\theta\Delta_{N,M}^{\frac1{2\widetilde\theta}}\right)}\gtrsim\frac{d_\theta^{-1}\delta^{-2}}{(N+M)^2},\qquad
\frac{\Delta_{N,M}}{\mathcal N_2\left(d_\theta\Delta_{N,M}^{\frac1{2\widetilde\theta}}\right)}\gtrsim\frac{\alpha^{-1/2}+\delta^{-1}}{N+M},
\]
and
\[
\Delta_{N,M}\ge c_\theta\left(\frac{N+M}{\log(N+M)}\right)^{-2\widetilde\theta},
\]
then
\[
\inf_{(P,Q)\in\mathcal P}P_{H_1}\{\widehat\eta_\lambda\ge\gamma\}\ge1-2\delta,\tag{4.7}
\]
where $\gamma=\frac{6\sqrt2(C_1+C_2)\mathcal N_2(\lambda)}{\sqrt\alpha}\left(\frac1n+\frac1m\right)$, $c_\theta>0$ is a constant that depends on $\theta$, and $\widetilde\theta=\min(\theta,\xi)$.

Furthermore, suppose $N+M\ge\max\{32\delta^{-1},e^{d_1/272C^2}\}$ and $C:=\sup_i\|\phi_i\|_\infty<\infty$. Then (4.7) holds when the above conditions on $\Delta_{N,M}$ are replaced by
\[
\frac{\Delta_{N,M}}{\mathcal N_1\left(d_\theta\Delta_{N,M}^{\frac1{2\widetilde\theta}}\right)}\gtrsim\frac{\delta^{-2}}{(N+M)^2},\qquad
\frac{\Delta_{N,M}}{\mathcal N_2\left(d_\theta\Delta_{N,M}^{\frac1{2\widetilde\theta}}\right)}\gtrsim\frac{\alpha^{-1/2}+\delta^{-1}}{N+M},
\]
and
\[
\mathcal N_1\left(d_\theta\Delta_{N,M}^{\frac1{2\widetilde\theta}}\right)\lesssim\left(\frac{N+M}{\log(N+M)}\right).
\]
''')
claim('4.6','Critical region–permutation',[17],r'''
For any $0<\alpha\le1$ and $0<w+\widetilde w<1$, if $B\ge\frac1{2\widetilde w^2\alpha^2}\log\frac2{\alpha(1-w-\widetilde w)}$, then
\[
P_{H_0}\{\widehat\eta_\lambda\ge\widehat q_{1-w\alpha}^{B,\lambda}\}\le\alpha.
\]
''')
claim('4.7','Separation boundary–permutation',[18],r'''
Suppose $(A_0)$–$(A_4)$ and $(B)$ hold. Let $s=d_1N=d_2M$, $\sup_{(P,Q)\in\mathcal P}\|\mathcal T^{-\theta}u\|_{L^2(R)}<\infty$, $\|\Sigma_{PQ}\|_{\mathcal L^\infty(\mathscr H)}\ge\lambda=d_\theta\Delta_{N,M}^{\frac1{2\widetilde\theta}}$, for some constants $0<d_1,d_2<1$ and $d_\theta>0$, where $d_\theta$ is a constant that depends on $\theta$. For any $0<\delta\le1$, if $(N+M)\ge\max\left\{d_3\delta^{-1/2}\log\frac1{(w-\widetilde w)\alpha},32\kappa d_1\delta^{-1}\right\}$ for some $d_3>0$, $B\ge\frac1{2\widetilde w^2\alpha^2}\log\frac2\delta$ for any $0<\widetilde w<w<1$ and $\Delta_{N,M}$ satisfies
\[
\frac{\Delta_{N,M}^{\frac{2\widetilde\theta+1}{2\widetilde\theta}}}{\mathcal N_2\left(d_\theta\Delta_{N,M}^{\frac1{2\widetilde\theta}}\right)}\gtrsim\frac{d_\theta^{-1}(\delta^{-1}\log(1/\widetilde\alpha))^2}{(N+M)^2},\qquad
\frac{\Delta_{N,M}}{\mathcal N_2\left(d_\theta\Delta_{N,M}^{\frac1{2\widetilde\theta}}\right)}\gtrsim\frac{\delta^{-1}\log(1/\widetilde\alpha)}{N+M},
\]
\[
\Delta_{N,M}\ge c_\theta\left(\frac{N+M}{\log(N+M)}\right)^{-2\widetilde\theta},
\]
then
\[
\inf_{(P,Q)\in\mathcal P}P_{H_1}\left\{\widehat\eta_\lambda\ge\widehat q_{1-w\alpha}^{B,\lambda}\right\}\ge1-5\delta,\tag{4.8}
\]
where $c_\theta>0$ is a constant that depends on $\theta$, $\widetilde\alpha=(w-\widetilde w)\alpha$ and $\widetilde\theta=\min(\theta,\xi)$.

Furthermore, suppose $C:=\sup_i\|\phi_i\|_\infty<\infty$ and $N+M\ge\max\left\{\frac{d_3}{\sqrt\delta}\log\frac1{(w-\widetilde w)\alpha},\frac{32}\delta,e^{\frac{d_1}{272C}}\right\}$. Then (4.8) holds when the above conditions on $\Delta_{N,M}$ are replaced by
\[
\frac{\Delta_{N,M}}{\mathcal N_1\left(d_\theta\Delta_{N,M}^{\frac1{2\widetilde\theta}}\right)}\gtrsim\frac{(\delta^{-1}\log(1/\widetilde\alpha))^2}{(N+M)^2},\qquad
\frac{\Delta_{N,M}}{\mathcal N_2\left(d_\theta\Delta_{N,M}^{\frac1{2\widetilde\theta}}\right)}\gtrsim\frac{\delta^{-1}\log(1/\widetilde\alpha)}{N+M},
\]
and
\[
\frac1{\mathcal N_1\left(d_\theta\Delta_{N,M}^{\frac1{2\widetilde\theta}}\right)}\gtrsim\left(\frac{N+M}{\log(N+M)}\right)^{-1}.
\]
''')
claim('4.10','Critical region–adaptation',[20],r'''
For any $0<\alpha\le1$ and $0<w+\widetilde w<1$, if $B\ge\frac{|\Lambda|^2}{2\widetilde w^2\alpha^2}\log\frac{2|\Lambda|}{\alpha(1-w-\widetilde w)}$, then
\[
P_{H_0}\left\{\bigcup_{\lambda\in\Lambda}\widehat\eta_\lambda\ge\widehat q_{1-\frac{w\alpha}{|\Lambda|}}^{B,\lambda}\right\}\le\alpha.
\]
''')

# The printed branch bodies coincide apart from the kernel-family multiplier.
# Emit both complete original bodies, retaining their distinct preambles below.
def adaptation_cases(kernel=False):
    body=r'''
(i) $\lambda_i\lesssim i^{-\beta}$, $1<\beta<\beta_u<\infty$, $\lambda_L=r_1\frac{\log(N+M)}{N+M}$, $\lambda_U=r_2\left(\frac{\log(N+M)}{N+M}\right)^{\frac2{4\widetilde\xi+1}}$, for some constants $r_1,r_2>0$, where $\widetilde\xi=\max(\xi,\frac14)$, $\|\Sigma_{PQ}\|_{\mathcal L^\infty(\mathscr H)}\ge\lambda_U$, and
\[
\Delta_{N,M}=c(\alpha,\delta,\theta)\max\left\{\left(\frac{\log\log(N+M)}{N+M}\right)^{\frac{4\widetilde\theta\beta}{4\widetilde\theta\beta+1}},\left(\frac{\log(N+M)}{N+M}\right)^{2\widetilde\theta}\right\},
\]
with $c(\alpha,\delta,\theta)\gtrsim\max\left\{\delta^{-2}(\log1/\alpha)^2,d_1^{2\widetilde\theta}\right\}$, for some constant $d_1>0$. Furthermore, if $\sup_i\|\phi_i\|_\infty<\infty$, then the above conditions on $\lambda_L$ and $\lambda_U$ can be replaced by $\lambda_L=r_3\left(\frac{\log(N+M)}{N+M}\right)^{\beta_u}$, $\lambda_U=r_4\left(\frac{\log(N+M)}{N+M}\right)^{\frac2{4\widetilde\xi+1}}$, for some constants $r_3,r_4>0$ and
\[
\Delta_{N,M}=c(\alpha,\delta,\theta,\beta)\max\left\{\left(\frac{\log\log(N+M)}{N+M}\right)^{\frac{4\widetilde\theta\beta}{4\widetilde\theta\beta+1}},\left(\frac{\log(N+M)}{N+M}\right)^{2\widetilde\theta\beta}\right\},
\]
where $c(\alpha,\delta,\theta,\beta)\gtrsim\max\left\{\delta^{-2}(\log1/\alpha)^2,d_2^{2\widetilde\theta\beta}\right\}$ for some constant $d_2>0$.

(ii) $\lambda_i\lesssim e^{-\tau i}$, $\tau>0$, $\lambda_L=r_5\frac{\log(N+M)}{N+M}$, $\lambda_U=r_6\left(\frac{\log(N+M)}{N+M}\right)^{1/2\xi}$ for some $r_5,r_6>0$, $\lambda_U\le\|\Sigma_{PQ}\|_{\mathcal L^\infty(\mathscr H)}$, and
\[
\Delta_{N,M}=c(\alpha,\delta,\theta)\max\left\{\frac{\sqrt{\log(N+M)}\log\log(N+M)}{N+M},\left(\frac{\log(N+M)}{N+M}\right)^{2\widetilde\theta}\right\},
\]
where $c(\alpha,\delta,\theta)\gtrsim\max\left\{\sqrt{\frac1{2\widetilde\theta}},1\right\}\max\left\{\delta^{-2}(\log1/\alpha)^2,d_4^{2\widetilde\theta}\right\}$, for some constant $d_4>0$. Furthermore if $\sup_i\|\phi_i\|_\infty<\infty$, then the above conditions on $\lambda_L$ and $\lambda_U$ can be replaced by $\lambda_L=r_7\left(\frac{\log(N+M)}{N+M}\right)^{\frac1{2\theta_l}}$, $\lambda_U=r_8\left(\frac{\log(N+M)}{N+M}\right)^{\frac1{2\xi}}$, for some $r_7,r_8>0$ and
\[
\Delta_{N,M}=c(\alpha,\delta,\theta)\frac{\sqrt{\log(N+M)}\log\log(N+M)}{N+M},
\]
where $c(\alpha,\delta,\theta)\gtrsim\max\left\{\sqrt{\frac1{2\widetilde\theta}},\frac1{2\widetilde\theta},1\right\}\delta^{-2}(\log1/\alpha)^2.
'''
    if kernel:
        body=body.replace(r'\frac{\log\log(N+M)}',r'\frac{\mathcal A\log\log(N+M)}')
        body=body.replace(r'\frac{\sqrt{\log(N+M)}',r'\frac{\mathcal A\sqrt{\log(N+M)}')
        # The last displayed branch prints A outside the fraction, after c.
        body=body.replace(r'\Delta_{N,M}=c(\alpha,\delta,\theta)\frac{\mathcal A\sqrt',r'\Delta_{N,M}=c(\alpha,\delta,\theta)\mathcal A\frac{\sqrt')
    return body
claim('4.11','Separation boundary–adaptation',[20,21],r'''
Suppose $(A_0)$–$(A_4)$ and $(B)$ hold. Let $\widetilde\theta=\min(\theta,\xi)$, $s=e_1N=e_2M$ for $0<e_1,e_2<1$, and $\sup_{\theta>0}\sup_{(P,Q)\in\mathcal P}\|\mathcal T^{-\theta}u\|_{L^2(R)}<\infty$. Then for any $\delta>0$, $B\ge\frac{|\Lambda|^2}{2\widetilde w^2\alpha^2}\log\frac2\delta$, $0<\widetilde w<w<1$, $0<\alpha\le e^{-1}$, $\theta_l>0$, there exists $k$ such for all $N+M\ge k$, we have
\[
\inf_{\theta>\theta_l}\inf_{(P,Q)\in\mathcal P}P_{H_1}\left\{\bigcup_{\lambda\in\Lambda}\widehat\eta_\lambda\ge\widehat q_{1-\frac{w\alpha}{|\Lambda|}}^{B,\lambda}\right\}\ge1-5\delta,
\]
provided one of the following cases hold:
'''+adaptation_cases())
claim('4.12','Separation boundary–adaptation over kernel',[22,23],r'''
Suppose $(A_0)$–$(A_4)$ and $(B)$ hold. Let $\mathcal A:=\log|\mathcal K|$, $\widetilde\theta=\min(\theta,\xi)$, $s=e_1N=e_2M$ for $0<e_1,e_2<1$, and
\[
\sup_{K\in\mathcal K}\sup_{\theta>0}\sup_{(P,Q)\in\widetilde{\mathcal P}}\|\mathcal T^{-\theta}u\|_{L^2(R)}<\infty.
\]
Then for any $\delta>0$, $0<\alpha\le e^{-1}$, $B\ge\frac{|\Lambda|^2|\mathcal K|^2}{2\widetilde w^2\alpha^2}\log\frac2\delta$, $0<\widetilde w<w<1$, $0<\alpha\le e^{-1}$, $\theta_l>0$, there exists $k$ such for all $N+M\ge k$, we have
\[
\inf_{K\in\mathcal K}\inf_{\theta>\theta_l}\inf_{(P,Q)\in\widetilde{\mathcal P}}P_{H_1}\left\{\bigcup_{(\lambda,K)\in\Lambda\times\mathcal K}\widehat\eta_{\lambda,K}\ge\widehat q_{1-\frac{w\alpha}{|\Lambda||\mathcal K|}}^{B,\lambda,K}\right\}\ge1-5\delta,
\]
provided one of the following cases hold: For any $K\in\mathcal K$ and $(P,Q)\in\widetilde{\mathcal P}$,
'''+adaptation_cases(kernel=True))

def save():
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=55,main_text_boundary=dict(location=f'Numbered Section 7 (Proofs) is main text on pages 32–52. References continue through page 55 above Appendix A, Technical results, whose heading begins at y={prov["main_text_end_y"]}. Only the region above that boundary is admitted on page 55; all appendix mathematics is excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    pdf=fitz.open(prov['cached_pdf']);assert len(pdf)==75 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
    first=pdf[0].get_text();assert '2212.09201v3' in first and '1 May 2024' in first
    labels=[];mentions=[]
    for n in range(55):
        page=pdf[n];clip=fitz.Rect(0,0,page.rect.width,prov['main_text_end_y']) if n==54 else page.rect
        assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text(clip=clip)
        for b in page.get_text('dict',clip=clip)['blocks']:
            for ln in b.get('lines',[]):
                text=''.join(s['text'] for s in ln['spans']).strip();m=re.match(r'^Theorem\s+(\d+\.\d+)',text)
                if m:(labels if ln['spans'][0]['font']=='CMBX10' else mentions).append((n+1,m[1]))
    assert labels==[(7,'3.1'),(8,'3.2'),(12,'4.1'),(13,'4.2'),(14,'4.3'),(17,'4.6'),(18,'4.7'),(20,'4.10'),(20,'4.11'),(22,'4.12')],labels
    assert mentions==[(22,'4.11')],mentions
    assert 'Technical results' in pdf[54].get_text(clip=fitz.Rect(0,prov['main_text_end_y'],pdf[54].rect.width,prov['main_text_end_y']+20))
    assert 'Proofs' in pdf[31].get_text(clip=fitz.Rect(0,230,pdf[31].rect.width,260))
    for c in claims:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
            depth=0
            for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if b=='{' else -1
                assert depth>=0,c['claim_id']
            assert depth==0,c['claim_id']
    path=ROOT/'theorem-inventory.json';path.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    for n in [7,8,12,13,14,15,17,18,20,21,22,23]:shutil.copyfile(Path(prov['working_pdf']).parent/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    notes=[
     'Pinned 75-page source is arXiv:2212.09201v3 dated 1 May 2024. The author line includes Bharath K. Sriperumbudur, matching the corpus author without its middle initial.',
     'Numbered Section 7 is main text, not an appendix. Appendix A starts below the references on page 55 at the exact archived y coordinate; all appendix mathematics is excluded.',
     'Independent font-aware enumeration finds ten Theorems, excluding one regular-font mention on page 22 and all proof headings. Theorems 4.3, 4.11 and 4.12 span two pages; every continuation is included.',
     'Theorem 3.1 retains both thresholds, their constant scalings, the power bound and the separate asymptotic non-optimality conclusion under two alternative regularity conditions.',
     'Theorem 3.2 retains the risk infimum, the two distinct inverse-decay conditions and the optional bounded-eigenfunction branch. Its printed exponent 1/2theta is retained without adding grouping not present in the PDF.',
     'Theorem 4.1 retains all five circled scalar labels and matrix definitions. The third term is printed with 1_n on both sides of A_2, although A_2 is m by m; this apparent dimension mismatch is not corrected.',
     'Theorem 4.1 sums a divided difference over eigenvalues without explicitly excluding zero eigenvalues or specifying its value there. Centering creates a singular matrix, so this convention must remain a source issue.',
     'Theorem 4.2 uses delta inside the optional eigenfunction-bound logarithm, even though delta is not bound in that statement. Alpha is not substituted for it.',
     'Theorem 4.3 prints e^{d_1/272C^2}, with an inline slash in the exponent, whereas Theorem 4.7 prints e^{d_1/(272C)} as a stacked fraction. Their different constants and typography are retained.',
     'Theorems 4.6 and 4.10 constrain only the sum w+tilde-w in their displayed hypothesis; separate positivity conditions are not silently added. Their rejection events use greater-than-or-equal signs, even at potentially tied permutation quantiles.',
     'The four branches of each adaptation result are preserved. The exponential branch has sqrt(log(N+M)) times log log(N+M), with the latter outside the radical.',
     'Theorem 4.12 uses script A=log|K|, includes the additional kernel infimum and quantile multiplicity, and repeats the alpha<=e^{-1} condition in its preamble. The source repetition and multiplier are retained.',
     'All source statement names and symbols are preserved: script T and N, script RKHS H, bold-italic centering/identity matrices, bold all-ones vectors, and blackboard-bold sample collections X_N,Y_M. Conditions are named A_0 through A_4 as printed.',
     'Only the independent inventory is complete. Resolve the alternative classes, eigenfunction versions, sample splitting, covariance/regularizer/statistic constructions, all assumptions, permutation quantiles, grid endpoints and uniform kernel-family conditions before completing the full paper census.'
    ]
    review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=10,inventory_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),printed_heading_check=labels,notes=notes)
    (ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=review['reviewed_at'],next_action='Resolve all ten Theorems from their main-text definitions. Start with A0, the centered kernel operator, alternative class, separation distance, minimax testing class and MMD statistic. Then sample splitting, covariance operators, regularizers A1–A4, spectral statistic, effective dimensions, B, permutation quantiles and adaptive grids/kernel families. Retain all source issues and exclude Appendix A from its heading on page 55.'),indent=2)+'\n')
    print('Saved and independently validated ten complete main-text Theorems.')
if __name__=='__main__':save()
