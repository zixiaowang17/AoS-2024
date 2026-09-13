"""Preserve all four main-text Theorems from the pinned v2 PDF."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,pages,body):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+n+(' — continuation' if i else '')) for i,p in enumerate(pages)]))
claim('1',[8],r'''
Suppose $p_1,\ldots,p_m$ follow the Bayesian two-groups model (1), with uniform null density $f_0=\mathbf1_{[0,1]}$. For the procedure defined in (4) with $\ell\leq1$, we have
\[
\mathbb E\left[\operatorname{lfdr}\big(p_{(R_\ell)}\big)\cdot\mathbf1\{R_\ell>0\}\right]=\mathbb P\left\{H_{(R_\ell)}=0,R_\ell>0\right\}=\pi_0\ell.\tag{11}
\]
Furthermore, if the alternative density $f_1$ is non-increasing, then we have
\[
\operatorname{max\text{-}lfdr}(\mathcal R_\ell)=\pi_0\ell.
\]
''')
claim('4',[10],r'''
Suppose $p_1,\ldots,p_m$ follow the Bayesian two-groups model (1), with $f_0=\mathbf1_{[0,1]}$ and $f_1$ non-increasing. Fix $\lambda\in(0,1)$, and define a modified version of our SL procedure that only examines order statistics below $\lambda$:
\[
R_\ell^\lambda:=\operatorname*{argmin}_{k\geq0:\ p_{(k)}\leq\lambda}\ \widehat\pi_0^\lambda p_{(k)}-\frac{\ell k}{m},\tag{13}
\]
and $\mathcal R_\ell^\lambda=\{i:\ p_i\leq p_{(R_\ell^\lambda)}\}$. Then we have
\[
\operatorname{max\text{-}lfdr}\left(\mathcal R_\ell^\lambda\right)\leq\ell.
\]
''')
claim('5',[15,16],r'''
Suppose $p_1,\ldots,p_m$ follow the Bayesian two-groups model (1), with $\pi_0\in(0,1)$, $f_0=\mathbf1_{[0,1]}$, and $f_1$ non-increasing. For $\ell\in(0,\pi_0^{-1})$, assume additionally that

(i) there is a unique value $t_\ell\in(0,1)$ for which $f(t_\ell)=\ell^{-1}$,

(ii) $f$ is continuously differentiable in a neighborhood of $t_\ell$ with $f'(t_\ell)<0$, and

(iii) $\widehat\ell$ is any random variable with $m^{1/3}(\widehat\ell-\ell)\overset{p}{\longrightarrow}0$ as $m\to\infty$.

Then we have, as $m\to\infty$,
\[
m^{1/3}(\tau_{\widehat\ell}-t_\ell)\overset{d}{\longrightarrow}\left(\frac{\ell}{4}\cdot f'(t_\ell)^2\right)^{-1/3}Z,\quad\text{and}\tag{23}
\]
\[
m^{1/3}\cdot\frac{\operatorname{lfdr}(\tau_{\widehat\ell})-\pi_0\ell}{\pi_0\ell}\overset{d}{\longrightarrow}\left(4\ell^2\cdot|f'(t_\ell)|\right)^{1/3}Z.\tag{24}
\]
where $Z$ follows Chernoff’s distribution defined in (22). Further, suppose that
\[
\mathbb P\{m^{-1/3}|\widehat\ell-\ell|>\varepsilon\}=o\left(m^{-2/3}\right),\quad\text{for all }\varepsilon>0.\tag{25}
\]
Then we also have $\mathbb E\left[\tau_{\widehat\ell}\right]\to t_\ell$. In addition,
\[
m^{2/3}\operatorname{Var}\left(\tau_{\widehat\ell}\right)\to\left(\frac{\ell}{4}\cdot f'(t_\ell)^2\right)^{-2/3}\operatorname{Var}(Z),\quad\text{and}\tag{26}
\]
\[
m^{2/3}\operatorname{Var}\left(\frac{\operatorname{lfdr}(\tau_{\widehat\ell})-\pi_0\ell}{\pi_0\ell}\right)\to\left(4\ell^2\cdot|f'(t_\ell)|\right)^{2/3}\operatorname{Var}(Z),\tag{27}
\]
where $\operatorname{Var}(Z)\approx0.26$.
''')
claim('6',[17],r'''
Suppose $p_1,\ldots,p_m$ follow the Bayesian two-groups model (1), with $\pi_0\in(0,1)$, $f_0=\mathbf1_{[0,1]}$, and $f_1$ non-increasing. Assume additionally that

(i) there is a unique value $\tau^*\in(0,1)$ for which $\operatorname{lfdr}(\tau^*)=\frac{\pi_0}{f(\tau^*)}=\alpha$,

(ii) $f$ is continuously differentiable in a neighborhood of $\tau^*$ with $f'(\tau^*)<0$, and

(iii) $\widehat\pi_0$ is any estimator of $\pi_0$ with $\mathbb P\left\{m^{1/3}(\widehat\pi_0-\pi_0)>\varepsilon\right\}=o\left(m^{-2/3}\right)$ for all $\varepsilon>0$.

Then we have, as $m\to\infty$,
\[
m^{2/3}\operatorname{Regret}_m(\mathcal R_{\alpha/\widehat\pi_0})\to\left(\frac{\alpha^2}{2\pi_0^2}\cdot|f'(\tau^*)|\right)^{-1/3}\operatorname{Var}(Z),\tag{28}
\]
where $Z$ follows Chernoff’s distribution defined in (22), and $\operatorname{Var}(Z)\approx0.26$.
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=25,main_text_boundary=dict(location='Main Sections 1-5 and their figures end on PDF page 25. Appendix A Proofs begins on a separate page 26, established by a heading-only crop. Appendix bodies on pages 26-41 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);labels=[]
assert len(pdf)==41 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
for n in range(25):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                if span['font']=='CMBX10':
                    m=re.fullmatch(r'Theorem (\d+)\.',span['text'].strip())
                    if m:labels.append((n+1,m.group(1)))
expected=[(8,'1'),(10,'4'),(15,'5'),(17,'6')]
assert labels==expected,labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in claims]==labels
for c in claims:
    for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
        depth=0
        for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
            depth+=1 if brace=='{' else -1
            assert depth>=0,c['claim_id']
        assert depth==0,c['claim_id']
p=ROOT/'theorem-inventory.json';p.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(p)],check=True)
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=4,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),printed_heading_check=labels,notes=[
 'Pinned arXiv:2207.07299v2. The arXiv stamp is 21 September 2023, while the title-page date is 22 September 2023; both are recorded. The source has 41 pages. Main text ends with Figure 8 on page 25; the saved heading crop from page 26 marks Appendix A Proofs.',
 'Independent font-sensitive enumeration of all 25 main pages finds precisely Theorems 1,4,5,6. Lemma 2, Remark 3 and Proposition 7 are not Theorem environments. No missing Theorems 2 or 3 are inferred from the shared numbering.',
 'Original bodies were visually inspected on pages 8,10,15,16,17. Theorem 5 spans pages 15-16 and includes three assumptions, two distributional limits, the additional tail condition, mean convergence and two variance limits.',
 'Theorem 1 separates exact last-rejection error control under the uniform null from the additional monotonicity assumption needed for the max-lfdr conclusion. It retains the nonempty-rejection indicator and ell<=1.',
 'Theorem 4 retains the constrained argmin, the estimator pi-hat_0^lambda, the index k>=0 and p_(k)<=lambda, the rejection set and its inequality. No unstated cutoff or positive-tuning clause is inserted into the original body.',
 'Theorem 5 condition (25) prints m^(-1/3) multiplying the absolute tuning error, unlike the m^(1/3) convergence requirement in (iii). Both are preserved without changing the exponent.',
 'Theorem 6 condition (iii) is a one-sided probability bound on pi-hat_0-pi_0, with no absolute value. Its regret constant is the printed power -1/3 of alpha^2 |f-prime(tau*)|/(2 pi_0^2). Neither is silently repaired.',
 'The census remains incomplete until source definitions, ambient conventions and all paper-local dependencies have been extracted and the final artifact independently audited.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,8,10,15,16,17,25]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve the two-groups model, local and maximum lfdr, SL procedure and threshold, null-proportion estimator, population/oracle risk and empirical regret, and Chernoff distribution from main pages 1-25 only.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated four complete main-text Theorems.')
