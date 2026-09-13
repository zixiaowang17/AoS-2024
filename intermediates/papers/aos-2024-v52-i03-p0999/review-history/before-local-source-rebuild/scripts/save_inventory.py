"""Save all four complete main-text Theorems in the pinned change-point paper."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,pages,text):
    claims.append(dict(claim_id=PID+'/T'+str(n),paper_id=PID,claim_kind='theorem',label='Theorem '+str(n),source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+str(n)) for p in pages]))
claim(3,[12,13],r'''
Given data $\{(y_t,X_t)\}_{t=1}^n$, suppose that Assumptions 1, 2, 3 and 4b hold. Let $\{\widetilde\eta_k\}_{k=1}^{\widehat K}$ be the change point estimators defined in (17), with

- the intervals $\{(s_k,e_k)\}_{k=1}^{\widehat K}$ defined in (18);
- the preliminary estimators $\{\widehat\eta_k\}_{k=1}^{\widehat K}$ from $\mathrm{DPDU}(\{(y_t,X_t)\}_{t=1}^n,\lambda,\zeta)$ detailed in Algorithm 1;
- the DPDU tuning parameters $\lambda=C_\lambda\sqrt{\log(pn)}$ and $\zeta=C_\zeta\{s\log(pn)\}^{2/\gamma-1}$, with $C_\lambda,C_\zeta>0$ being absolute constants; and
- the Lasso estimators $\{\widehat\beta_k\}_{k=1}^{\widehat K}$ defined in (14) with the intervals constructed based on $\{\widehat\eta_k\}_{k=1}^{\widehat K}$.

a. (Non-vanishing regime) For $k\in\{1,\ldots,K\}$, if $\kappa_k\to\varrho_k$, as $n\to\infty$, with $\varrho_k>0$ being an absolute constant, then the following results hold.

a.1. The estimation error satisfies that $|\widetilde\eta_k-\eta_k|=O_p(1)$, as $n\to\infty$.

a.2. When $n\to\infty$,
\[
\widetilde\eta_k-\eta_k\xrightarrow{\mathcal D}\operatorname*{arg\,min}_{r\in\mathbb Z}P_k(r),
\]
where, for $r\in\mathbb Z$, $P_k(r)$ is a two-sided random walk defined as
\[
P_k(r)=\begin{cases}\sum_{t=r}^{-1}\{-2\varrho_k\epsilon_t\xi_t(k)+\varrho_k^2\xi_t^2(k)\},&r<0,\\0,&r=0,\\\sum_{t=1}^{r}\{2\varrho_k\epsilon_t\xi_t(k)+\varrho_k^2\xi_t^2(k)\},&r>0,\end{cases}
\]
where we assume additionally $\{(\epsilon_t,v_k^\top X_t)\}_{t\in\mathbb Z}\xrightarrow{\mathcal D}\{(\epsilon_t,\xi_t(k))\}_{t\in\mathbb Z}$, for $k\in\{1,\ldots,K\}$, and $v_k$ is the normalised jump vector defined in Assumption 1.

b. (Vanishing regime) For $k\in\{1,\ldots,K\}$, if $\kappa_k\to0$, as $n\to\infty$, then the following results hold.

b.1. The estimation error satisfies that $|\widetilde\eta_k-\eta_k|=O_p(\kappa_k^{-2})$, as $n\to\infty$.

b.2. When $n\to\infty$,
\[
\kappa_k^2(\widetilde\eta_k-\eta_k)\xrightarrow{\mathcal D}\operatorname*{arg\,min}_{r\in\mathbb R}\left\{\frac{\varpi_k}{\sigma_\infty(k)}|r|+\mathbb W(r)\right\},
\]
where $\varpi_k$ is the limiting drift coefficient defined in Assumption 2c, and $\mathbb W(r)$ is a two-sided standard Brownian motion defined as
\[
\mathbb W(r)=\begin{cases}\mathbb B_1(-r),&r<0,\\0,&r=0,\\\mathbb B_2(r),&r>0,\end{cases}
\]
with $\mathbb B_1(r)$ and $\mathbb B_2(r)$ being two independent standard Brownian motions.
''')
claim(4,[17],r'''
Let $\{Z_t\}_{t\in\mathbb Z}$ be an $\mathbb R$-valued, mean-zero, possibly nonstationary process of the form (10). Let the cumulative functional dependence measure $\Delta_{m,2}^Z$ be defined in (11). Assume that there exist absolute constants $\gamma_1(Z),\gamma_2(Z),c,C_{\mathrm{FDM}}>0$ such that
\[
\sup_{m\ge0}\exp(cm^{\gamma_1(Z)})\Delta_{m,2}^Z\le C_{\mathrm{FDM}}\tag{28}
\]
and $\sup_{t\in\mathbb Z}\mathbb P(|Z_t|>x)\le\exp(1-x^{\gamma_2(Z)})$, for any $x>0$. Let $\gamma(Z)=\{1/\gamma_1(Z)+1/\gamma_2(Z)\}^{-1}<1$. There exist absolute constants $c_1,c_2>0$ such that for any $x\ge1$ and integer $m\ge3$,
\[
\mathbb P\left\{m^{-1/2}\left|\sum_{t=1}^m Z_t\right|\ge x\right\}\le m\exp\{-c_1x^{\gamma(Z)}m^{\gamma(Z)/2}\}+2\exp\{-c_2x^2\}.\tag{29}
\]
''')
claim(8,[18],r'''
Under all the assumptions and with all the notation in Theorem 3, let $\{\widehat\sigma_\infty^2(k)\}_{k=1}^{\widehat K}$ be the output of Algorithm 2 with $\{\widehat\eta_k\}_{k=1}^{\widehat K}$ output by DPDU in Algorithm 1, $\{\widehat\beta_k\}_{k=1}^{\widehat K}$ constructed from (14) based on the intervals with endpoints $\{\widehat\eta_k\}_{k=1}^{\widehat K}$, $\{\widehat\kappa_k\}_{k=1}^{\widehat K}$ defined in (30), $\{(s_k,e_k)\}_{k=1}^{\widehat K}$ defined in (18) and $R\in\mathbb N$ satisfying $(e_k-s_k)\gg R\gg\sqrt{e_k-s_k}$, as $n$ diverges. We have that
\[
\max_{k=1}^K|\widehat\sigma_\infty^2(k)-\sigma_\infty^2(k)|\xrightarrow{P.}0,\qquad n\to\infty.
\]
''')
claim(10,[21],r'''
Under all the assumptions in Theorem 8, for any $k\in\{1,\ldots,K\}$, let $\widehat u^{(1)}$ be defined in (32) with $M=\infty$ and $\widehat\kappa_k^2$ be the $k$th jump size estimator defined in (30). It holds that
\[
\frac{\kappa_k^2}{\widehat\kappa_k^2}\widehat u^{(1)}\mathbb{1}\{\widehat\kappa_k\ne0\}\xrightarrow{\mathcal D}\operatorname*{arg\,min}_{r\in\mathbb R}\{\varpi_k|r|+\sigma_\infty(k)\mathbb W(r)\},\qquad n\to\infty.
\]
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=33,main_text_boundary=dict(location='Discussion and references end on PDF page 33. Page 34 starts Appendices; only that heading is inspected. All appendix content is excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);assert len(pdf)==112 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
first=pdf[0].get_text();assert '2207.12453v3' in first and '1 Oct 2023' in first and 'October 3, 2023' in first
labels=[];mentions=[]
for n in range(33):
    page=pdf[n];assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text()
    for b in page.get_text('dict')['blocks']:
        for line in b.get('lines',[]):
            text=''.join(s['text'] for s in line['spans']).strip();m=re.match(r'Theorem (\d+)(?=[.\s(])',text)
            if m:
                if line['spans'][0]['font']=='CMBX10':labels.append((n+1,int(m.group(1))))
                else:mentions.append((n+1,text))
assert labels==[(12,3),(17,4),(18,8),(21,10)],labels
assert [p for p,s in mentions]==[13,16,17,18]
assert 'Zhang' in pdf[32].get_text() and 'Appendices' in pdf[33].get_text(clip=fitz.Rect(0,0,pdf[33].rect.width,89))
for c in claims:
    for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
        depth=0
        for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
            depth+=1 if b=='{' else -1
            assert depth>=0,c['claim_id']
        assert depth==0,c['claim_id']
path=ROOT/'theorem-inventory.json';path.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
for n in [12,13,17,18,21]:shutil.copyfile(Path(prov['working_pdf']).parent/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=4,inventory_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),printed_heading_check=labels,notes=[
 'The pinned 112-page preprint is arXiv:2207.12453v3, with margin date 1 October 2023 and title-page date 3 October 2023. The source begins Change point, whereas journal metadata uses Change-point.',
 'Fresh font-aware enumeration across pages 1–33 finds four bold Theorem headings and excludes four regular-font theorem mentions. All appendix mathematics from page 34 is excluded.',
 'Theorem 3 spans pages 12–13 and retains all four estimator/tuning bullets, both regimes, both localization rates, the complete signed two-sided random walk, the extra process convergence assumption, and the independent two-sided Brownian construction.',
 'The Brownian W and B symbols are blackboard bold, whereas the random walk P is ordinary italic. Distributional convergence uses calligraphic D; the convergence-in-probability arrow in Theorem 8 is printed P. with a period.',
 'Theorem 4 retains the potentially nonstationary process, the supremum in its second-moment dependence condition, the uniform tail condition, gamma(Z)<1, and both deviation terms with their exact exponents.',
 'Theorem 8 retains all inherited assumptions and the full list of algorithmic inputs. Its block-count condition is (e_k-s_k)>>R>>sqrt(e_k-s_k), with R an integer.',
 'Theorem 10 calls kappa-hat_k squared the jump size estimator although equation (30) defines its unsquared form. It retains M=infinity and the ratio times the nonzero-jump indicator exactly as printed.',
 'Only the independent theorem inventory is complete. Resolve Assumptions 1–4b, functional dependence (10)–(11), Algorithms 1–2, Lasso and refinement equations (14),(17),(18), drift/variance, jump estimator (30) and simulated minimizer (32) before final census validation.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Extract and resolve all four Theorems against the main-text regression/change-point model, Assumptions 1–4b, dependence measures, DPDU and variance algorithms, Lasso and refinement constructions, drift/long-run variance, and simulated minimizer (32). Preserve inherited assumptions, regime restrictions and source ambiguities. Then finalize and independently source-audit.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated four complete main-text Theorems.')
