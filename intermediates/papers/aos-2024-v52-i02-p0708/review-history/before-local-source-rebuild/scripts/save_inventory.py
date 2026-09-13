"""Save every complete original main-paper Theorem before interface extraction."""
import datetime,fitz,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text())
claims=[]
def claim(n,pages,body,title=None):
    label='Theorem '+str(n)+((' ('+title+')') if title else '')
    claims.append(dict(claim_id=PID+'/T'+str(n),paper_id=PID,claim_kind='theorem',label=label,source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+str(n)+(' — continuation' if i else '')) for i,p in enumerate(pages)]))
claim(1,[9,10],r"""
Let Condition 1 hold and $(\alpha,\beta)\in\mathcal I\in\mathcal M(\gamma;C_1)$ for some fixed constant $C_1\in(0,0.5)$. Let $1\leq\ell_1<\cdots<\ell_s\leq p$ be any $s$ given indices for some fixed integer $s\geq1$. As $p\to\infty$, the following three assertions hold.

(a) If $\gamma\gg p^{-1/4}$, then
\[
(p-1)^{1/2}\operatorname{diag}(b_{\ell_1}^{-1/2},\ldots,b_{\ell_s}^{-1/2})(\widehat\theta_{\ell_1}-\theta_{\ell_1},\ldots,\widehat\theta_{\ell_s}-\theta_{\ell_s})^\top\to\mathcal N(\mathbf0,\mathbf I_s)
\]
in distribution.

(b) If $p^{-1/4}\gg\gamma\gg p^{-1/3}\log^{1/6}p$, then
\[
N^{1/2}\operatorname{diag}(\widetilde b_{\ell_1}^{-1/2},\ldots,\widetilde b_{\ell_s}^{-1/2})(\widehat\theta_{\ell_1}-\theta_{\ell_1},\ldots,\widehat\theta_{\ell_s}-\theta_{\ell_s})^\top\to\mathcal N(\mathbf0,\mathbf I_s)
\]
in distribution.

(c) If $\gamma\asymp p^{-1/4}$, then
\[
N^{1/2}\operatorname{diag}[\{(p-2)b_{\ell_1}+\widetilde b_{\ell_1}\}^{-1/2},\ldots,\{(p-2)b_{\ell_s}+\widetilde b_{\ell_s}\}^{-1/2}]
\times(\widehat\theta_{\ell_1}-\theta_{\ell_1},\ldots,\widehat\theta_{\ell_s}-\theta_{\ell_s})^\top\to\mathcal N(\mathbf0,\mathbf I_s)
\]
in distribution.
""")
claim(2,[12],r"""
Let the conditions of Theorem 1 hold, and $\delta\in(0,c]$ for some positive constant $c<0.5$. As $p\to\infty$, if $1\gg\gamma\gg p^{-1/3}\log^{1/6}p$, the following two assertions hold.

(a) Let $1\leq\ell_1<\cdots<\ell_s\leq p$ be any $s$ given indices for some fixed integer $s\geq1$. Then
\[
N^{1/2}\operatorname{diag}(\nu_{\ell_1}^{\dagger,-1/2},\ldots,\nu_{\ell_s}^{\dagger,-1/2})(\widehat\theta_{\ell_1}^\dagger-\theta_{\ell_1},\ldots,\widehat\theta_{\ell_s}^\dagger-\theta_{\ell_s})^\top\to\mathcal N(\mathbf0,\mathbf I_s)
\]
in distribution.

(b) $\max_{\ell\in[p]}|\nu_\ell^\dagger\nu_\ell^{-1}-1|=O(\delta)$, where $\nu_\ell$ is specified in (4.1).
""")
claim(3,[13],r"""
Let Condition 1 hold and $(\alpha,\beta)\in\mathcal M(\gamma;C_1)$ for some fixed constant $C_1\in(0,0.5)$. As $p\to\infty$, if $0<\delta\ll(p\log p)^{-1}$ and $1\gg\gamma\gg p^{-1/3}\log^{1/2}p$, then
\[
\sup_{\mathbf u\in\mathbb R^p}\left|\mathbb P\{N^{1/2}(\mathbf V^\dagger)^{-1/2}(\widehat{\boldsymbol\theta}-\boldsymbol\theta)\leq\mathbf u\}-\mathbb P(\boldsymbol\xi\leq\mathbf u)\right|\to0,
\]
where $\mathbf V^\dagger=\operatorname{diag}(\nu_1^\dagger,\ldots,\nu_p^\dagger)$, and $\boldsymbol\xi\sim\mathcal N(\mathbf0,\mathbf I_p)$.
""")
claim(4,[18],r"""
Let $(\alpha,\beta)\in\mathcal M(\gamma,C_1)$ for some fixed constant $C_1\in(0,0.5)$. Write $\chi_p=\exp(-|\xi^+|\vee\max_{\ell\in S}|\check\theta_\ell^+|)$. If $0\leq\omega_2\leq\omega_1<1/2$, then
\[
|\widehat\xi-\xi|=\widetilde O_p\left(\frac{\log^{1/2}p}{\gamma p^{1/2-\omega_1}}\right)+\widetilde O_p\left(\frac{s\log^{1/2}p}{\gamma p^{3/2-\omega_1-\omega_2}}\right)
+\widetilde O_p\left(\frac{\log^{1/2}p}{\gamma^3p^{1-2\omega_1}}\right)+O\left(\frac{s\log p}{p}\right)=\max_{\ell\in[p]}|\widehat{\check\theta}_\ell-\check\theta_\ell|
\]
provided that $\gamma\gg\chi_p^{-8}(sp^{-3/2+\omega_1+\omega_2}\log^{1/2}p+p^{-1/3+2\omega_1/3}\log^{1/6}p)$.
""")
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=19,main_text_boundary=dict(location='Main text ends on PDF page 19 immediately before the APPENDIX heading at y=313.6376953125. Page 19 was clipped above that heading; all later appendix and embedded supplement content is excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);labels=[]
assert len(pdf)==76 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
assert '2112.10151v2' in pdf[0].get_text() and '2 Apr 2024' in pdf[0].get_text()
for n in range(19):
    clip=fitz.Rect(0,0,pdf[n].rect.width,prov['main_text_shared_page_cutoff_y']) if n==18 else pdf[n].rect
    for block in pdf[n].get_text('dict',clip=clip)['blocks']:
        for line in block.get('lines',[]):
            spans=line['spans'];text=''.join(span['text'] for span in spans).strip()
            match=re.match(r'THEOREM (\d+)\.',text)
            if match:labels.append((n+1,match.group(1)))
assert labels==[(9,'1'),(12,'2'),(13,'3'),(18,'4')],labels
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
 'Pinned arXiv:2112.10151v2, stamped 2 April 2024, 76 PDF pages. The main text ends above the Appendix heading on page 19; the remainder of that page and all subsequent content were excluded.',
 'Independent main-text heading enumeration finds exactly Theorems 1-4; Proposition, Remark, proof and citation occurrences are excluded. Complete statements were inspected visually on pages 9,10,12,13,18.',
 'Theorem 1 retains all three privacy regimes, fixed s, and its page-10 continuation. The unexplained printed membership chain (alpha,beta) in script I in M is retained rather than repaired.',
 'Theorem 2 retains both parts, its reference to the conditions of Theorem 1, the upper bound on delta, population centering theta (not theta-hat), and its deterministic O(delta) variance ratio bound.',
 'Theorem 3 retains the stronger logarithmic privacy restriction, the smaller delta requirement, the supremum over p-dimensional rectangles, original estimator theta-hat and diagonal population variance V-dagger. No estimated variance or bootstrap centering is substituted.',
 'Theorem 4 retains sparse parameters, all four error terms and their exact powers, the printed chain of equality between two estimation errors, and the unparenthesized minus/max expression defining chi_p. These source ambiguities will be recorded separately.',
 'Only the theorem inventory is complete. The paper census remains in progress pending main-text definitions, assumptions, dependencies and a separate source audit.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,9,10,12,13,18]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve the beta-model, jittering class and noise, Condition 1, moment estimator and variance definitions, bootstrap construction, sparse parametrization and stochastic-order convention from main text only. Then finalize and independently audit the census.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated four complete main-text Theorems.')
