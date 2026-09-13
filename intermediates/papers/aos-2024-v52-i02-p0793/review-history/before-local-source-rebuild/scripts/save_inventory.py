"""Save the two complete main-text Theorems from the pinned December 2023 preprint."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,pages,text):claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+n) for p in pages]))
claim('1',[5],r'''
For $x_0\in(0,1)^d$, let $\mathcal P$ denote the model where:

1. $f(x)$ is bounded above by a constant,
2. $\pi(x)$ is $\alpha$-smooth,
3. $\mu_0(x)$ is $\beta$-smooth, and
4. $\tau(x)$ is $\gamma$-smooth.

Let $s\equiv(\alpha+\beta)/2$. Then for $n$ larger than a constant depending on $(\alpha,\beta,\gamma,d)$, the minimax rate is lower bounded as
\[
\inf_{\widehat\tau}\sup_{P\in\mathcal P}\mathbb E_P|\widehat\tau(x_0)-\tau_P(x_0)|\gtrsim
\begin{cases}
n^{-1/\left(1+\frac d{2\gamma}+\frac d{4s}\right)}&\text{if }s<\dfrac{d/4}{1+d/2\gamma},\\
n^{-1/\left(2+\frac d\gamma\right)}&\text{otherwise.}
\end{cases}
\]
''')
claim('2',[24],r'''
Assume the regularity conditions:

A. The eigenvalues of $Q$ and $\Omega$ are bounded above and below away from zero.

B. $\widehat\pi(x)-\pi(x)$ is $\alpha$-smooth and $\widehat\mu_0(x)-\mu_0(x)$ is $\beta$-smooth.

C. The quantities $y^2$, $(\widehat\pi^2,\widehat\mu_0^2)$, $\|\widehat\mu_0-\mu_0\|_{F^*}$, and $\|\widehat Q^{-1}-Q^{-1}\|$ are all bounded above, and $\|d\widehat F^*/dF^*\|_\infty$ is bounded above and below away from zero.

Also assume the basis $b$ satisfies Hölder approximating condition (6), and:

1. $\|(d\widehat F^*/dF^*)-1\|_\infty\lesssim\dfrac{n^{-1/\left(1+\frac d{2\gamma}+\frac d{4s}\vee\left(1+\frac d{2\gamma}\right)\right)}}{\|\widehat\pi-\pi\|_{F^*}(\|\widehat\mu_0-\mu_0\|_{F^*}+h^\gamma)}$,
2. $\pi(x)$ is $\alpha$-smooth, and $\epsilon\leq\pi(x)\leq1-\epsilon$ for some $\epsilon>0$,
3. $\mu_0(x)$ is $\beta$-smooth,
4. $\tau(x)$ is $\gamma$-smooth.

Finally let the tuning parameters satisfy
\[
h\sim n^{-(1/\gamma)/\left(1+\frac d{2\gamma}+\frac d{4s}\right)}\quad\text{and}\quad k\sim n^{\left(\frac d{2s}-\frac d\gamma\right)/\left(1+\frac d{2\gamma}+\frac d{4s}\right)}
\]
if $s<\frac{d/4}{1+d/2\gamma}$, or $h\sim n^{-\frac1{2\gamma+d}}$ and $k\sim nh^d$ otherwise. Then the estimator $\widehat\tau$ from Definition 2 has error upper bounded as
\[
\mathbb E_P|\widehat\tau(x_0)-\tau_P(x_0)|\lesssim
\begin{cases}
n^{-1/\left(1+\frac d{2\gamma}+\frac d{4s}\right)}&\text{if }s<\dfrac{d/4}{1+d/2\gamma},\\
n^{-1/\left(2+\frac d\gamma\right)}&\text{otherwise.}
\end{cases}
\]
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=29,main_text_boundary=dict(location='Main text and references end on PDF page 29. The Appendices heading begins on page 30; pages 30-48 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);labels=[]
assert len(pdf)==48 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
assert '2203.00837v4' in pdf[0].get_text() and '23 Dec 2023' in pdf[0].get_text()
for n in range(29):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(span['text'] for span in line['spans']).strip();match=re.match(r'Theorem (\d+)\.',text)
            if match and line['spans'][0]['font']=='SFBX1095':labels.append((n+1,match.group(1)))
assert labels==[(5,'1'),(24,'2')],labels
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
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=2,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),printed_heading_check=labels,notes=[
 'Pinned arXiv:2203.00837v4, stamped 23 December 2023, 48 pages. Main text and references end on page 29. Appendices begin on page 30; no appendix mathematics is used.',
 'Independent bold-heading inspection over pages 1-29 finds exactly Theorems 1 and 2, on pages 5 and 24. Plain-text references starting a line, Proposition statements, Lemmas and Remarks do not create additional Theorems.',
 'Both full statements were visually checked, including the four lower-bound model conditions, its average smoothness definition, strict elbow threshold, both rates, and all upper-bound regularity and numbered conditions.',
 'Theorem 2 preserves its density-ratio sup-norm lower-bound wording, the unparenthesized maximum within its rate exponent, both tuning-parameter regimes and its reference to Definition 2. These source conventions need separate resolution rather than silent corrections.',
 'The upper bound has no supremum over P, unlike the minimax lower bound. Its additional distribution-estimation requirements are not inherited by the lower-bound model.',
 'Only the inventory is complete. The paper census requires the main-text CATE model, Hölder class convention, norms, localized polynomial and correction bases, projection matrices, split-sample estimator, transformed measure and Hölder approximation condition. Appendix proof material remains excluded.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,5,24,29]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve the CATE model, exact Hölder floor convention, norms, Definition 2 and all its localized polynomial/correction bases, split-sample nuisance inputs, Q/Omega/F-star quantities and approximation condition (6). Check the upper-bound rate exponent grouping and density-ratio wording literally, then finalize and independently audit. Exclude pages 30-48.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated two complete main-text Theorems.')
