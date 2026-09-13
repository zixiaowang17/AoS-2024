"""Save all four complete main-text Theorems, excluding the attached supplement."""
import datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i03-p0948', 'title': 'On blockwise and reference panel-based estimators for genetic data prediction in high dimensions', 'version': 'arXiv:2203.12003v1', 'source_url': 'https://arxiv.org/pdf/2203.12003v1', 'pdf_pages': 60, 'pdf_sha256': 'a6bfe1bcf5a885bcc6c101ba8d90c51ab03c402f47efc0791609f9a9262cfcd8', 'authors': ['Bingxin Zhao', 'Shurong Zheng', 'Hongtu Zhu']};claims=[]
def claim(n,pages,text):claims.append(dict(claim_id=PID+'/T'+str(n),paper_id=PID,claim_kind='theorem',label='Theorem '+str(n),source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+str(n)) for p in pages]))
claim(1,[8,9],r'''
Under Condition 1, as $\min(n,p_1,\ldots,p_K)\to\infty$, the limits of
\[
p^{-1}\operatorname{tr}\{(\widehat{\boldsymbol\Sigma}-\widehat{\boldsymbol\Sigma}_B)(\widehat{\boldsymbol\Sigma}_B+\lambda\boldsymbol I_p)^{-1}\boldsymbol\Sigma\}\qquad\text{and}\qquad p^{-1}\operatorname{tr}\{(\widehat{\boldsymbol\Sigma}-\widehat{\boldsymbol\Sigma}_B)(\widehat{\boldsymbol\Sigma}_B+\lambda\boldsymbol I_p)^{-2}\boldsymbol\Sigma\}\tag{2}
\]
are zeros and the limit of
\[
p^{-1}\operatorname{tr}\{(\widehat{\boldsymbol\Sigma}-\widehat{\boldsymbol\Sigma}_B)(\widehat{\boldsymbol\Sigma}_B+\lambda\boldsymbol I_p)^{-1}\boldsymbol\Sigma(\widehat{\boldsymbol\Sigma}-\widehat{\boldsymbol\Sigma}_B)(\widehat{\boldsymbol\Sigma}_B+\lambda\boldsymbol I_p)^{-1}\}\tag{3}
\]
is $\omega^{-1}\sum_{l,h=1,\ldots,K;\ l\ne h}\omega_l\omega_h\cdot\{1-\lambda m_l(-\lambda)\}\{1-\lambda m_h(-\lambda)\}+o_p(1)$, where
\[
m_l(z)=\int\frac1{t\{1-\omega_l-\omega_lzm_l(z)\}-z}\,dH_l(t),\tag{4}
\]
in which $H_l(t)$ is the LSD of $\boldsymbol\Sigma_{B_l}$ and $m_l(z)$ is the Stieltjes transform of $M_l(x)$ for $l=1,\ldots,K$.
''')
claim(2,[9,10],r'''
Under polygenic model (1) and Conditions 1 - 4, as $\min(n,n_z,p_l)\to\infty$, the limit of $A_B^2(\lambda)$ is
\[
\frac{[1-\lambda\boldsymbol R_1(\lambda)]^2\cdot h_\beta^4}{[1+\lambda^2\boldsymbol R_2(\lambda)-2\lambda\boldsymbol R_1(\lambda)+\boldsymbol R_3(\lambda)]\cdot h_\beta^2+[\boldsymbol R_1(\lambda)-\lambda\boldsymbol R_2(\lambda)]\cdot\omega(1-h_\beta^2)}+o_p(1),
\]
where
\[
\boldsymbol R_1(\lambda)=p^{-1}\sum_{l=1}^K\operatorname{tr}\{(a_l\boldsymbol\Sigma_l+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l\},
\]
\[
\boldsymbol R_2(\lambda)=p^{-1}\sum_{l=1}^K\operatorname{tr}\{(a_l\boldsymbol\Sigma_l+\lambda\boldsymbol I_{p_l})^{-2}(\boldsymbol I_{p_l}-\dot a_l\boldsymbol\Sigma_l)\boldsymbol\Sigma_l\},\qquad\text{and}
\]
\[
\boldsymbol R_3(\lambda)=\omega^{-1}\sum_{l,h=1,\ldots,K;\ l\ne h}\omega_l\omega_h\{1-\lambda m_l(-\lambda)\}\{1-\lambda m_h(-\lambda)\}.
\]
Here $a_l$ is the unique positive solution of
\[
1-a_l=\omega_l\cdot\left\{1-\lambda\int_0^\infty(a_lt+\lambda)^{-1}\,dH_l(t)\right\}=\omega_l\cdot\left\{1-\mathrm E_{H_l(t)}\left(\frac\lambda{a_lt+\lambda}\right)\right\}
\]
and $\dot a_l$ is the first order derivative of $a_l$ and given by
\[
\dot a_l=\frac{\omega_l\cdot\mathrm E_{H_l(t)}\left\{\frac{a_lt}{(a_lt+\lambda)^2}\right\}}{-1-\omega_l\lambda\cdot\mathrm E_{H_l(t)}\left\{\frac t{(a_lt+\lambda)^2}\right\}}.
\]
When $\lambda=\lambda^*\equiv\omega\cdot(1-h_\beta^2)/h_\beta^2$, $A_B^2(\lambda)$ is maximized and the optimal prediction accuracy is given by
\[
A_B^2(\lambda^*)=h_\beta^2\cdot\frac{\{1-\lambda^*\boldsymbol R_1(\lambda^*)\}^2}{1-\lambda^*\boldsymbol R_1(\lambda^*)+\boldsymbol R_3(\lambda^*)}+o_p(1).\tag{5}
\]
''')
# These repeated full source expressions are expanded into each original statement.
square_trace=r'\operatorname{tr}\{(\boldsymbol K_l+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l(\boldsymbol K_l+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l\}'
cubic_trace=r'\operatorname{tr}\{(\boldsymbol K_l+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l(\boldsymbol K_l+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l^2\}'
trace=r'\operatorname{tr}\{(\boldsymbol K_l+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l\}'
q3=r'p^{-1}\sum_{l=1}^K\left[1-\frac{n^{-1}'+square_trace+r'}{[1+n^{-1}'+trace+r']^2}\right]^{-1}'+square_trace
q2=r'p^{-1}\sum_{l=1}^K\frac{[1+n^{-1}'+trace+r']^2\cdot '+cubic_trace+r'}{[1+n^{-1}'+trace+r']^2-n^{-1}'+square_trace+r'}'
claim(3,[12],r'''
Under Condition 1, as $\min(n_w,p_l)\to\infty$, the limit of $p^{-1}\sum_{l=1}^K\operatorname{tr}\{(\widehat{\boldsymbol\Sigma}_{BW_l}+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l(\widehat{\boldsymbol\Sigma}_{BW_l}+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l\}$ is approximated by
\[
'''+q3+r''',
\]
where $\boldsymbol K_l=[1+n^{-1}\mathrm E\operatorname{tr}\{(\widehat{\boldsymbol\Sigma}_{BW_l}+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l\}]^{-1}\boldsymbol\Sigma_l=\lambda v_{w_l}(-\lambda)\boldsymbol\Sigma_l$. In addition, the limit of $p^{-1}\sum_{l=1}^K\operatorname{tr}\{(\widehat{\boldsymbol\Sigma}_{BW_l}+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l(\widehat{\boldsymbol\Sigma}_{BW_l}+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l^2\}$ is approximated by
\[
'''+q2+r'''.
\]
''')
claim(4,[12,13],r'''
Under polygenic model (1) and Conditions 1, 2, 3, and 5, as $\min(n,n_w,n_z,p_l)\to\infty$, we have
\[
A_{BW}^2(\lambda)=\frac{\boldsymbol Q_1^2(\lambda)\cdot h_\beta^4}{\boldsymbol Q_2(\lambda)\cdot h_\beta^2+\boldsymbol Q_3(\lambda)\cdot\omega}+o_p(1),
\]
where $\boldsymbol Q_1(\lambda)$, $\boldsymbol Q_2(\lambda)$, and $\boldsymbol Q_3(\lambda)$ are, respectively, given by
\[
p^{-1}\sum_{l=1}^K\operatorname{tr}\{(a_{w_l}\boldsymbol\Sigma_l+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l^2\},
\]
\[
'''+q2+r''',
\]
and
\[
'''+q3+r'''.
\]
Here $a_{w_l}$ is the unique positive solution of $1-a_{w_l}=\omega_{w_l}\cdot\{1-\lambda\int_0^\infty(a_{w_l}t+\lambda)^{-1}\,dH_l(t)\}$. In addition, we have
\[
A_{BZ}^2(\lambda)=\frac{\{1-\lambda\boldsymbol Q_4(\lambda)\}^2\cdot h_\beta^4}{\{\boldsymbol Q_5(\lambda)-\lambda\boldsymbol Q_6(\lambda)\}\cdot h_\beta^2+\{\boldsymbol Q_4(\lambda)-\lambda\boldsymbol Q_7(\lambda)\}\cdot\omega}+o_p(1),
\]
where
\[
\boldsymbol Q_4(\lambda)=p^{-1}\sum_{l=1}^K\operatorname{tr}\{(a_{z_l}\boldsymbol\Sigma_l+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l\},\qquad\boldsymbol Q_5(\lambda)=p^{-1}\sum_{l=1}^K\operatorname{tr}\{(a_{z_l}\boldsymbol\Sigma_l+\lambda\boldsymbol I_{p_l})^{-1}\boldsymbol\Sigma_l^2\},
\]
\[
\boldsymbol Q_6(\lambda)=p^{-1}\sum_{l=1}^K\operatorname{tr}\{(a_{z_l}\boldsymbol\Sigma_l+\lambda\boldsymbol I_{p_l})^{-2}(\boldsymbol I_{p_l}-\dot a_{z_l}\boldsymbol\Sigma_l)\boldsymbol\Sigma_l^2\},\qquad\text{and}
\]
\[
\boldsymbol Q_7(\lambda)=p^{-1}\sum_{l=1}^K\operatorname{tr}\{(a_{z_l}\boldsymbol\Sigma_l+\lambda\boldsymbol I_{p_l})^{-2}(\boldsymbol I_{p_l}-\dot a_{z_l}\boldsymbol\Sigma_l)\boldsymbol\Sigma_l\}.
\]
Moreover, $a_{z_l}$ is the unique positive solution of $1-a_{z_l}=\omega_{z_l}\cdot\{1-\lambda\int_0^\infty(a_{z_l}t+\lambda)^{-1}\,dH_l(t)\}$ and $\dot a_{z_l}$ is the first order derivative of $a_{z_l}$, given by
\[
\dot a_{z_l}=\frac{\omega_{z_l}\cdot\mathrm E_{H_l(t)}\left\{\frac{a_{z_l}t}{(a_{z_l}t+\lambda)^2}\right\}}{-1-\omega_{z_l}\cdot\lambda\mathrm E_{H_l(t)}\left\{\frac t{(a_{z_l}t+\lambda)^2}\right\}}.
\]
''')
def main():
    repo=Path(__file__).resolve().parents[5]
    source=Path(subprocess.check_output([sys.executable,str(repo/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=27,main_text_boundary=dict(location='Main text and references end on PDF page 27. Attached Supplementary Material starts on page 28; pages 28–60 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    pdf=fitz.open(source);labels=[];mentions=[]
    assert len(pdf)==60 and hashlib.sha256(source.read_bytes()).hexdigest()==paper['pdf_sha256']
    first=pdf[0].get_text();assert '2203.12003v1' in first and '22 Mar 2022' in first and 'June 13, 2025' in first
    for author in prov['authors']:assert author in first
    for n in range(27):
        page=pdf[n]
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(span['text'] for span in line['spans']).strip();match=re.match(r'Theorem (\d+)(?=[.\s(])',text)
                if match:
                    if line['spans'][0]['font']=='URWPalladioL-Bold':labels.append((n+1,match.group(1)))
                    else:mentions.append((n+1,text))
    assert labels==[(8,'1'),(9,'2'),(12,'3'),(12,'4')],labels
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in claims]==labels
    assert [p for p,t in mentions]==[10,12,13]
    assert 'Zhou' in pdf[26].get_text() and 'Supplementary Material for' in pdf[27].get_text(clip=fitz.Rect(0,0,pdf[27].rect.width,155))
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
