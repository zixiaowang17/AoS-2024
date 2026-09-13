"""Preserve all eight main-text Theorems in the pinned v4 PDF."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i03-p0922', 'title': 'Distributed estimation and inference for semiparametric binary response models', 'version': 'arXiv:2210.08393v4', 'source_url': 'https://arxiv.org/pdf/2210.08393v4', 'pdf_pages': 102, 'pdf_sha256': '2a9174faf0cf534dc4c4ce87bef4d970c416e09bed9a37067d9c1609d5d682e5', 'authors': ['Xi Chen', 'Wenbo Jing', 'Weidong Liu', 'Yichen Zhang']};claims=[]
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
def main():
    repo=Path(__file__).resolve().parents[5]
    source=Path(subprocess.check_output([sys.executable,str(repo/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=40,main_text_boundary=dict(location='Main text and references end on PDF page 40. Appendix A starts on PDF page 41; appendix mathematics on pages 41–102 is excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    pdf=fitz.open(source);labels=[];references=[]
    assert len(pdf)==102 and hashlib.sha256(source.read_bytes()).hexdigest()==paper['pdf_sha256']
    first=pdf[0].get_text();assert '2210.08393v4' in first and '15 Aug 2024' in first
    assert all(name in first for name in prov['authors'])
    for n in range(40):
        page=pdf[n]
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

if __name__ == "__main__":
    main()
