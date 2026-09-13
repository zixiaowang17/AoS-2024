"""Preserve both original main-text Theorems in arXiv:2305.11672v2."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i03-p1178', 'title': 'Nonparametric classification with missing data', 'authors': ['Torben Sell', 'Thomas B. Berrett', 'Timothy I. Cannings'], 'version': 'arXiv:2305.11672v2', 'source_url': 'https://arxiv.org/pdf/2305.11672v2', 'pdf_pages': 73, 'pdf_sha256': '02ed1c44949085eadd0343d487709cdbf5883670a7158cc33ef146f1ba453096'};claims=[]
def claim(n,page,text):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=page,location='Theorem '+n)]))
claim('1',9,r'''
Fix $d,n\in\mathbb N$, $\mathcal O\subseteq\{0,1\}^d$, $o_1,\ldots,o_n\in\mathcal O$, $\Omega_\star\in\mathcal I(\{0,1\}^d)\setminus\{\{\mathbf0_d\},\emptyset\}$, $c_{\mathrm E}\in[0,1/4]$, $\boldsymbol\gamma\in[0,\infty)^d$, $C_{\mathrm L}>1$, $\boldsymbol\beta\in(0,1]^d$, $C_{\mathrm S}\ge1$, $\alpha\in[0,\infty)$ and $C_{\mathrm M}\ge1$. Suppose that $\min_{\omega\in\Omega_\star}\gamma_\omega>\max_{\omega\in\Omega_\star}\beta_\omega/d_\omega$, $\max_{\omega\in\Omega_\star}\alpha\beta_\omega\le\min_{\omega\in\Omega_\star}d_\omega$, $c_{\mathrm E}\le(16|\Omega_\star|)^{-1}$, $C_{\mathrm L}\ge(8d)^{(1+d)(1+\|\boldsymbol\gamma\|_\infty)}$ and $C_{\mathrm M}\ge\max_{\omega\in\Omega_\star}\big(1+6\cdot4^{d/\beta_\omega}\big)$. Let
\[
R:=\max_{\omega\in\Omega_\star\cap\mathcal N}\left\{n_\omega^{-\frac{\beta_\omega\gamma_\omega(1+\alpha)}{\gamma_\omega(2\beta_\omega+d_\omega)+\alpha\beta_\omega}}\right\}.\tag{12}
\]
Then, there exist constants $0<c<C$ (neither of which depend on $n$ nor $o_1,\ldots,o_n$) such that
\[
\begin{aligned}
c\cdot\big(R+\mathbb1_{\{\Omega_\star\cap\mathcal N^c\ne\emptyset\}}\big)
&\le\inf_{\widehat C\in\mathcal C_n}\sup_{Q\in\mathcal Q'_{\mathrm{Miss}}}\mathbb E_Q\left\{\mathcal E_{P_Q}(\widehat C)\mid O_1=o_1,\ldots,O_n=o_n\right\}\\
&\le C\cdot\log_+^{\frac{1+\alpha}2}\left(\min_{\omega\in\Omega_\star\cap\mathcal N}n_\omega\right)\cdot R+\mathbb1_{\{\Omega_\star\cap\mathcal N^c\ne\emptyset\}}.
\end{aligned}\tag{13}
\]
''')
claim('2',12,r'''
Fix $d,n\in\mathbb N$, $\mathcal O\subseteq\{0,1\}^d$, $o_1,\ldots,o_n\in\mathcal O$, $\Omega_\star\in\mathcal I(\{0,1\}^d)\setminus\{\{\mathbf0_d\},\emptyset\}$, $c_{\mathrm E}\in(0,1/4]$, $\boldsymbol\gamma\in[0,\infty)^d$, $C_{\mathrm L}\ge1$, $\boldsymbol\beta\in(0,1]^d$, $C_{\mathrm S}\ge1$, $\alpha\in[0,\infty)$ and $C_{\mathrm M}\ge1$. Suppose that $\Omega_\star\subseteq\mathcal N$ and we have $\min_{\omega\in\Omega_\star}\gamma_\omega>\max_{\omega\in\Omega_\star}\beta_\omega/d_\omega$. Suppose that $n_\omega\ge\log^{\frac{4(\gamma_\omega(2\beta_\omega+d_\omega)+\alpha\beta_\omega)}{\beta_\omega\gamma_\omega}}\big(2|\mathcal N|\min_{\omega'\in\Omega_\star}n_{\omega'}\big)$, for $\omega\in U(\Omega_\star)\cap\mathcal N$, then there exists a constant $C_{\mathrm U}\ge1$ (not depending on $n$ nor $o_1,\ldots,o_n$) such that
\[
\sup_{Q\in\mathcal Q^+_{\mathrm{Miss}}}\mathbb E_Q\left\{\mathcal E_{P_Q}(\widehat C_{\mathrm{HAM}})\mid O_1=o_1,\ldots,O_n=o_n\right\}
\le C_{\mathrm U}\cdot\log_+^{\frac{1+\alpha}2}\left(\min_{\omega\in\Omega_\star}n_\omega\right)\cdot\max_{\omega\in\Omega_\star}\left\{n_\omega^{-\frac{\beta_\omega\gamma_\omega(1+\alpha)}{\gamma_\omega(2\beta_\omega+d_\omega)+\alpha\beta_\omega}}\right\}.\tag{14}
\]
''')

def main():
    repo=Path(__file__).resolve().parents[5]
    source=Path(subprocess.check_output([sys.executable,str(repo/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==prov['pdf_sha256']
    pdf=fitz.open(source);assert len(pdf)==73
    assert hashlib.sha256(source.read_bytes()).hexdigest()==prov['pdf_sha256']
    first=' '.join(pdf[0].get_text().split());assert prov['title'].upper() in first
    for name in prov['authors']:assert name.upper() in first
    assert 'Submitted to the Annals of Statistics' in first
    labels=[];mentions=[]
    for n in range(1,23):
        page=pdf[n-1]
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans']).strip()
                m=re.match(r'^THEOREM\s+(\d+)\.',text)
                if m:labels.append((n,m[1]))
                m=re.match(r'^Theorem\s+(\d+)',text)
                if m:mentions.append((n,m[1]))
    assert labels==[(9,'1'),(12,'2')]
    assert mentions==[(2,'1'),(9,'1'),(12,'1')]
    assert 'Funding.' in pdf[21].get_text()
    assert 'S1. Additional results and proofs of the claims in Section 2' in pdf[22].get_text(clip=fitz.Rect(90,55,515,83))
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in claims]==labels
    for c in claims:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,c['claim_id']
            assert depth==0,c['claim_id']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=22,main_text_boundary=dict(location='Main text ends with funding on PDF page 22. Supplementary Section S1 begins on PDF page 23 at y=67.57; all Sections S1–S5 and following references are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Pinned arXiv:2305.11672v2, main text PDF 1–22 only; supplementary sections excluded.'),papers=[paper],claims=claims)
    path=ROOT/'theorem-inventory.json';path.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)

if __name__ == "__main__":
    main()
