"""Preserve all eight main-text Theorems in the pinned v4 PDF."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,pages,text,title=None):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+(' ('+title+')' if title else ''),source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+n+(' — continuation after the intervening Algorithm 2 page' if n=='4.3' and p==27 else '')) for p in pages]))
claim('3.1',[16],r'''
Assume Assumptions 1–5 hold and $L=o(m^{\frac23(\alpha-1)}/(p\log m)^{\frac{2\alpha+1}3})$. By specifying $h=h^*:=(1/n)^{\frac1{2\alpha+1}}$, for any $\boldsymbol\vartheta\in\mathbb R^p\setminus\{\boldsymbol0\}$, we have, as $n\to\infty$,
\[
\frac{n^{\frac\alpha{2\alpha+1}}\boldsymbol\vartheta^\top(\widehat{\boldsymbol\beta}_{\texttt{(Avg-SMSE)}}-\boldsymbol\beta^*)-\boldsymbol\vartheta^\top V^{-1}U}{\sqrt{\boldsymbol\vartheta^\top V^{-1}V_sV^{-1}\boldsymbol\vartheta}}\xrightarrow{d}\mathcal N(0,1),\tag{9}
\]
where $V$ and $V_s$ are defined in Assumption 4, and $U$ is defined below,
\[
U:=\pi_U\mathbb E\left(\sum_{k=1}^\alpha\frac{2(-1)^{k+1}}{k!(\alpha-k)!}F^{(k)}(0\mid\boldsymbol Z)\rho^{(\alpha-k)}(0\mid\boldsymbol Z)\boldsymbol Z\right),\tag{10}
\]
with constant $\pi_U$ defined in Assumption 1.
''')
claim('3.3',[19],r'''
Assume Assumptions 1–5 hold, and there exists a constant $0<c_2<1$ such that $p=O(m^{c_2})$. Further, assume the initial estimator satisfies $\|\widehat{\boldsymbol\beta}^{(0)}-\boldsymbol\beta^*\|_2=O_{\mathbb P}((p/m)^{\frac13})$. By choosing $h_t=\max\{(p/n)^{\frac1{2\alpha+1}},(p/m)^{\frac{2^t}{3\alpha}}\}$ at iteration $t=1,2,\ldots,T$, we have
\[
\|\widehat{\boldsymbol\beta}^{(t)}-\boldsymbol\beta^*\|_2=O_{\mathbb P}\big((p/n)^{\frac\alpha{2\alpha+1}}+(p/m)^{\frac{2^t}3}+(p/m)^{\frac{2^{t-1}}3}(p/n)^{\frac{\alpha-1}{2\alpha+1}}\sqrt{\log n}\big).\tag{12}
\]
''')
claim('3.4',[20],r'''
Assume the assumptions in Theorem 3.3 hold. Further, assume that the local size $m>n^{c_3}$ for some constant $0<c_3<1$ and $p=o(n^{\frac{2(\alpha-1)}{4\alpha+1}}(\log n)^{-\frac{2\alpha+1}{4\alpha+1}})$. When $T$ satisfies (13), let $h_{T+1}=(\lambda_h/n)^{\frac1{2\alpha+1}}$ for some constant $\lambda_h>0$, and then for any $\boldsymbol\vartheta\in\mathbb R^p\setminus\{\boldsymbol0\}$, we have
\[
\frac{n^{\frac\alpha{2\alpha+1}}\boldsymbol\vartheta^\top(\widehat{\boldsymbol\beta}^{(T+1)}-\boldsymbol\beta^*)-\lambda_h^{\frac\alpha{2\alpha+1}}\boldsymbol\vartheta^\top V^{-1}U}{\lambda_h^{-\frac1{2(2\alpha+1)}}\sqrt{\boldsymbol\vartheta^\top V^{-1}V_sV^{-1}\boldsymbol\vartheta}}\xrightarrow{d}\mathcal N(0,1),\tag{14}
\]
where $V$ and $V_s$ are defined in Assumption 4 and $U$ is defined in (10).
''')
claim('4.1',[24],r'''
Suppose Assumptions 1 and 5–9 hold and the sample size of the smallest local batch $\min_\ell m_\ell\gtrsim pn^{3/(2\alpha+1)}\log n$. By taking $h=n^{-1/(2\alpha+1)}$, we have that, for any $\boldsymbol\vartheta\in\mathbb R^p\setminus\{\boldsymbol0\}$,
\[
\frac{n^{\frac\alpha{2\alpha+1}}\boldsymbol\vartheta^\top(\widehat{\boldsymbol\beta}_{\texttt{(wAvg-SMSE)}}-\boldsymbol\beta^*)-\sum_{\ell=1}^L\boldsymbol\vartheta^\top W_\ell V_\ell^{-1}U_\ell}{\sqrt{\sum_{\ell=1}^L\frac n{m_\ell}\boldsymbol\vartheta^\top W_\ell V_\ell^{-1}V_{s,\ell}V_\ell^{-1}W_\ell^\top\boldsymbol\vartheta}}\xrightarrow{d}\mathcal N(0,1).\tag{19}
\]
''',title='wAvg-SMSE')
claim('4.2',[24],r'''
Suppose Assumptions 1 and 5–9 hold and $\|\widehat{\boldsymbol\beta}^{(0)}-\boldsymbol\beta^*\|_2=O_{\mathbb P}(\delta_0)$. Further, assume that the local size $m>n^{c_3}$ for some constant $0<c_3<1$ and $p=o(n^{\frac{2(\alpha-1)}{4\alpha+1}}(\log n)^{-\frac{2\alpha+1}{4\alpha+1}})$. By taking $h_t=\max\{(p/n)^{\frac1{2\alpha+1}},\delta_0^{2^t/\alpha}\}$ at iteration $t=1,2,\ldots,T$ and $h_{T+1}=n^{-1/(2\alpha+1)}$, we have
\[
\frac{n^{\frac\alpha{2\alpha+1}}\boldsymbol\vartheta^\top(\widehat{\boldsymbol\beta}^{(T+1)}_{\texttt{(wmSMSE)}}-\boldsymbol\beta^*)-\boldsymbol\vartheta^\top\overline V_W^{-1}\overline U_W}{\sqrt{\boldsymbol\vartheta^\top\overline V_W^{-1}\sum_{\ell=1}^L\frac n{m_\ell}W_\ell V_{s,\ell}W_\ell^\top\overline V_W^{-\top}\boldsymbol\vartheta}}\xrightarrow{d}\mathcal N(0,1),\tag{20}
\]
for any $\boldsymbol\vartheta\in\mathbb R^p\setminus\{\boldsymbol0\}$ and sufficiently large $T$, where $\overline U_W:=\sum_{\ell=1}^LW_\ell U_\ell$, $\overline V_W:=\sum_{\ell=1}^LW_\ell V_\ell$.
''',title='wmSMSE')
claim('4.3',[25,27],r'''
Assume the assumptions in Theorem 3.3 hold. Further, assume that $\varepsilon\leq\varepsilon_0$ for some constant $\varepsilon_0<1$. By choosing $h_0=(\frac{p\log L}m)^{\frac1{2\alpha+1}}$ and $h_t=\max\{\delta_{m,0}^{2^t/\alpha},(\frac pn)^{\frac1{2\alpha+1}}\}$ for $t=1,2,\ldots,T$, we have that
\[
\|\widehat{\boldsymbol\beta}^{(t)}_1-\boldsymbol\beta^*_1\|_2=O_{\mathbb P}\left(\left(\frac p{(1-\varepsilon)n}\right)^{\frac\alpha{2\alpha+1}}+\delta_{m,0}^{2^t}+\delta_{m,0}^{2^{t-1}}\left(\frac p{(1-\varepsilon)n}\right)^{\frac{\alpha-1}{2\alpha+1}}\sqrt{\log n}+\varepsilon\delta_{m,0}^2\right),\tag{22}
\]
where $\delta_{m,0}=(\frac{p\log L}{\omega m})^{\frac\alpha{2\alpha+1}}$.
''')
claim('5.1',[28,29],r'''
Assume Assumptions 1–4 hold, and the covariates are uniformly bounded, that is, there exists $\overline B$ such that $\|\boldsymbol z_i\|_\infty\leq\overline B$, with finite second moment, that is, $\sup_{\|\boldsymbol v\|_2=1}\mathbb E[(\boldsymbol v^\top\boldsymbol Z)^2]<+\infty$. Further, assume that the dimension $p=O(n^\nu)$ for some $\nu>0$, the local sample size $m=O(n^c)$ for some $0<c<1$, the sparsity $s=o(m^{1/4})$ and the initial value $\widehat{\boldsymbol\beta}^{(0)}$ satisfies $\|\widehat{\boldsymbol\beta}^{(0)}-\boldsymbol\beta^*\|_2=O_{\mathbb P}(\delta_{m,0})$ and $\|\widehat{\boldsymbol\beta}^{(0)}-\boldsymbol\beta^*\|_1=O_{\mathbb P}(\sqrt s\delta_{m,0})$ for some $\delta_{m,0}=o(1)$. Moreover, assume that $\sqrt s\delta_{m,0}=O(h_1^{3/2})$ and $\frac{s^2\log m}{mh_1^3}=o(1)$. By specifying
\[
\lambda_n^{(1)}=C_0\left(s\delta_{m,0}^2+h_1^\alpha+\sqrt{\frac{\log p}{nh_1}}+\sqrt{\frac{s\log p}{mh_1^3}}\delta_{m,0}\right),
\]
with a sufficiently large constant $C_0$, it holds that
\[
\|\widehat{\boldsymbol\beta}^{(1)}-\boldsymbol\beta^*\|_2=O_{\mathbb P}(\sqrt s\lambda_n^{(1)})=O_{\mathbb P}\left[s^{3/2}\delta_{m,0}^2+\sqrt sh_1^\alpha+\sqrt{\frac{s\log p}{nh_1}}+\sqrt{\frac{s^2\log p}{mh_1^3}}\delta_{m,0}\right],\tag{27}
\]
and $\|\widehat{\boldsymbol\beta}^{(1)}-\boldsymbol\beta^*\|_1\leq2\sqrt s\|\widehat{\boldsymbol\beta}^{(1)}-\boldsymbol\beta^*\|_2$ with probability tending to one.
''')
claim('5.2',[29,30],r'''
Assume the assumptions in Theorem 5.1 hold. With proper bandwidth $h_t$, parameter $\lambda_n^{(t)}$ and kernel function $H(\cdot)$, we can obtain that for $1\leq t\leq T$,
\[
\|\widehat{\boldsymbol\beta}^{(t)}-\boldsymbol\beta^*\|_2=O_{\mathbb P}\left(\sqrt s\left(\frac{\log p}n\right)^{\frac\alpha{2\alpha+1}}+(r_m)^t\delta_{m,0}\right),\tag{28}
\]
and $\|\widehat{\boldsymbol\beta}^{(t)}-\boldsymbol\beta^*\|_1=O_{\mathbb P}(\sqrt s\|\widehat{\boldsymbol\beta}^{(t)}-\boldsymbol\beta^*\|_2)$, where $r_m$ is an infinitesimal quantity.
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=40,main_text_boundary=dict(location='Main text and references end on PDF page 40. Appendix A starts on PDF page 41; appendix mathematics on pages 41–102 is excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);labels=[];references=[]
assert len(pdf)==102 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
first=pdf[0].get_text();assert '2210.08393v4' in first and '15 Aug 2024' in first
assert all(name in first for name in prov['authors'])
for n in range(40):
    page=pdf[n]
    assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text()
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(span['text'] for span in line['spans']).strip();match=re.match(r'Theorem (\d+\.\d+)(?=[.\s(])',text)
            if match:
                if line['spans'][0]['font']=='CMBX10':labels.append((n+1,match.group(1)))
                else:references.append((n+1,text))
assert labels==[(16,'3.1'),(19,'3.3'),(20,'3.4'),(24,'4.1'),(24,'4.2'),(25,'4.3'),(28,'5.1'),(29,'5.2')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in claims]==labels
assert len(references)==2 and [p for p,t in references]==[16,30]
assert 'Zhou' in pdf[39].get_text() and 'Theoretical Results of the High-dimensional' in pdf[40].get_text(clip=fitz.Rect(0,0,pdf[40].rect.width,99))
for c in claims:
    for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
        depth=0
        for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
            depth+=1 if brace=='{' else -1
            assert depth>=0,c['claim_id']
        assert depth==0,c['claim_id']
p=ROOT/'theorem-inventory.json';p.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(p)],check=True)
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=8,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),printed_heading_check=labels,notes=[
 'The pinned cached file is arXiv:2210.08393v4, 102 pages, stamped 15 August 2024. It is not the journal-layout version.',
 'Main text and references end on page 40. Appendix A starts on page 41, whose heading alone was inspected. No appendix theorem or mathematical detail was imported.',
 'Font-aware independent enumeration finds eight Theorems. Proposition 3.2 is not a Theorem; ordinary-font references on pages 16 and 30 are excluded.',
 'Theorem 4.3 begins on page 25, is interrupted by Algorithm 2 occupying page 26, and concludes with equation (22) and delta_m,0 on page 27.',
 'Visual crops distinguish exponents 2^(t-1) from 2^t minus 1 in equations (12) and (22); the former is printed.',
 'Theorem 4.2 uses barred U_W and V_W; the variance ends in inverse transpose V_W. Theorem 3.4 has a negative bandwidth power in its denominator.',
 'Theorem 5.1 uses barred B, plain C_0, log m in its small-o hypothesis but log p in lambda and its error bound; delta_m,0 multiplies the square root rather than lying inside it.',
 'Theorem 5.2 is an abbreviated main-text statement. Its proper tuning choices and the formal definition of r_m are explicitly deferred to Appendix A, so those details remain unresolved within scope.',
 'The complete original statements are preserved; inherited assumptions and estimator definitions still require interface extraction and a separate source audit before this paper can count as complete.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve the eight Theorems against main-text Assumptions 1–9, the homogeneous and heterogeneous sampling settings, SMSE algorithms, equation (13), coefficient-shift selection, and the sparse Dantzig update. Keep appendix-only tuning and r_m unresolved. Then finalize and independently source-audit.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated eight complete main-text Theorems.')
