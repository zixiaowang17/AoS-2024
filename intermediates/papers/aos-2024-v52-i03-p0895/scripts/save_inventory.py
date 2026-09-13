"""Preserve the three complete main-text Theorems, stopping before Appendix A on a shared page."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i03-p0895', 'title': 'Reconciling model-X and doubly robust approaches to conditional independence testing', 'version': 'arXiv:2211.14698v2', 'source_url': 'https://arxiv.org/pdf/2211.14698v2', 'pdf_pages': 75, 'pdf_sha256': '3ff5392125e3a9af824c39e4d0f70fe16b83fbceaaf981a33896a6fed16741b2', 'main_text_end_y': 288.68743896484375};claims=[]
def claim(n,pages,text):
    claims.append(dict(claim_id=PID+'/T'+str(n),paper_id=PID,claim_kind='theorem',label='Theorem '+str(n),source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+str(n)) for p in pages]))
claim(1,[8,9],r'''
Suppose the sequences of true and learned laws $\mathcal L_n$ and $\widehat{\mathcal L}_n$ satisfy the following two nondegeneracy properties:
\[
\mathbb P_{\mathcal L_n}[(\widehat S_n^{\widehat{\mathrm{dCRT}}})^2\geq\epsilon]\to1\text{ for some }\epsilon>0;\tag{NDG1}
\]
\[
0<\operatorname{Var}_{\widehat{\mathcal L}_n}[X_i\mid Z_i],\ (Y_i-\widehat\mu_{n,y}(Z_i))^2,\ (Y_i-\mu_{n,y}(Z_i))^2<\infty\text{ almost surely}.\tag{NDG2}
\]
If the conditional Lyapunov condition
\[
\frac1{n^{1+\delta/2}}\sum_{i=1}^n|Y_i-\widehat\mu_{n,y}(Z_i)|^{2+\delta}\mathbb E_{\widehat{\mathcal L}_n}[|\widetilde X_i-\widehat\mu_{n,x}(Z_i)|^{2+\delta}\mid X,Z]\xrightarrow{p}0\tag{Lyap-1}
\]
is satisfied for some $\delta>0$, then
\[
\frac1{\widehat S_n^{\widehat{\mathrm{dCRT}}}}T_n^{\widehat{\mathrm{dCRT}}}(\widetilde X,X,Y,Z)\mid X,Y,Z\xrightarrow{d,p}N(0,1)\tag{14}
\]
and therefore
\[
C_n^{\widehat{\mathrm{dCRT}}}(X,Y,Z)\equiv\mathbb Q_{1-\alpha}\left[\frac1{\widehat S_n^{\widehat{\mathrm{dCRT}}}}T_n^{\widehat{\mathrm{dCRT}}}(\widetilde X,X,Y,Z)\mid X,Y,Z\right]\xrightarrow{p}z_{1-\alpha}.\tag{15}
\]
''')
claim(2,[12,13],r'''
Suppose $\mathcal L_n\in\mathscr L_n^0$ is a sequence of laws satisfying the assumptions (SP1') and (SP2), the nondegeneracy condition (NDG2), the variance consistency property (23) and the Lyapunov condition
\[
\frac1{n^{1+\delta/2}}\sum_{i=1}^n\mathbb E_{\mathcal L_n}[|Y_i-\mu_{n,y}(Z_i)|^{2+\delta}\mid Z_i]\mathbb E_{\widehat{\mathcal L}_n}[|\widetilde X_i-\widehat\mu_{n,x}(Z_i)|^{2+\delta}\mid X,Z]\xrightarrow{p}0.\tag{Lyap-2}
\]
Then, the $\widehat{\mathrm{dCRT}}$ and GCM variance estimates are asymptotically equivalent:
\[
\frac{(\widehat S_n^{\widehat{\mathrm{dCRT}}})^2}{(\widehat S_n^{\mathrm{GCM}})^2}\xrightarrow{p}1,\tag{25}
\]
as are the $\widehat{\mathrm{dCRT}}$ and GCM tests themselves:
\[
\lim_{n\to\infty}\mathbb P_{\mathcal L_n}[\phi_n^{\widehat{\mathrm{dCRT}}}(X,Y,Z)=\phi_n^{\mathrm{GCM}}(X,Y,Z)]=1.\tag{26}
\]
''')
claim(3,[16],r'''
Consider the conditional independence testing problem (32), with a collection of null distributions $\mathscr R\subseteq\mathscr L^0$ satisfying some regularity conditions, a linear subspace $\mathcal H_g\subseteq L^2(\mathcal L_{x,z}(\boldsymbol Z))$ specifying possible values for the nonparametric component $g$ in the GPLM alternative model (29), and some subset $\mathcal S\subseteq\mathcal H_g$. If the following four assumptions hold:
\[
\text{assumptions (SP1) and (SP2) hold for all }\mathcal L\in\mathscr R,\tag{35}
\]
\[
\ddot\psi=K>0\text{ and }\mathbb E_{\mathcal L_{x,z}}[\boldsymbol X^2]<\infty\quad\text{OR}\quad\operatorname{supp}(\boldsymbol X,\boldsymbol Z)\text{ is compact and }\mathcal H_g\subseteq C(\mathbb R^p),\tag{36}
\]
\[
\mathbb E_{\mathcal L_{x,z}}[\boldsymbol X\mid\cdot]\in\mathcal H_g,\tag{37}
\]
\[
\forall g_0\in\mathcal S,h_g\in\mathcal H_g,\ \mathcal L_{\theta_n(0,h_g)}\in\mathscr R\text{ for large enough }n,\tag{38}
\]
then $\phi_n^{\mathrm{GCM}}$ is LAUMP($\mathcal S$) against $\mathcal L_{\theta_n(h)}$ for $h\in(0,\infty)\times\mathcal H_g$, with
\[
\lim_{n\to\infty}\mathbb E_{\mathcal L_{\theta_n(h)}}[\phi_n^{\mathrm{GCM}}(X,Y,Z)]=1-\Phi(z_{1-\alpha}-h_\beta\cdot s(\theta_0)).\tag{39}
\]
''')
def main():
    repo=Path(__file__).resolve().parents[5]
    source=Path(subprocess.check_output([sys.executable,str(repo/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=34,main_text_boundary=dict(location='References finish in the upper part of PDF page 34. Appendix A begins at y=288.68743896484375 on that page; only main text above this boundary is included. Appendix mathematics on pages 34-75 is excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    pdf=fitz.open(source);labels=[];references=[];boundary=prov['main_text_end_y']
    assert len(pdf)==75 and hashlib.sha256(source.read_bytes()).hexdigest()==paper['pdf_sha256']
    first=pdf[0].get_text();assert '2211.14698v2' in first and '8 Feb 2023' in first and 'February 10, 2023' in first
    for n in range(34):
        page=pdf[n];clip=fitz.Rect(0,0,page.rect.width,boundary) if n==33 else None
        for block in page.get_text('dict',clip=clip)['blocks']:
            for line in block.get('lines',[]):
                text=''.join(span['text'] for span in line['spans']).strip();match=re.match(r'Theorem (\d+)(?=[.\s(])',text)
                if match:
                    if line['spans'][0]['font']=='CMBX12':labels.append((n+1,match.group(1)))
                    else:references.append((n+1,text))
    assert labels==[(8,'1'),(12,'2'),(16,'3')],labels
    assert len(references)==2 and all(p==18 for p,t in references)
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in claims]==labels
    assert 'Zhong' in pdf[33].get_text(clip=fitz.Rect(0,0,pdf[33].rect.width,boundary)) and 'Theorem' not in pdf[33].get_text(clip=fitz.Rect(0,0,pdf[33].rect.width,boundary))
    assert all(e['page']<34 for c in claims for e in c['evidence'])
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
