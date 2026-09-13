"""Save the two complete main-text Theorems from the pinned December 2023 preprint."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i02-p0793', 'title': 'Minimax rates for heterogeneous causal effect estimation', 'version': 'arXiv:2203.00837v4', 'source_url': 'https://arxiv.org/pdf/2203.00837v4', 'pdf_pages': 48, 'pdf_sha256': '289bc44c78f84f2e70d98a343140bd354318b7788d63408c6921b08092f0249f'};claims=[]
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
def main():
    repo=Path(__file__).resolve().parents[5]
    source=Path(subprocess.check_output([sys.executable,str(repo/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=29,main_text_boundary=dict(location='Main text and references end on PDF page 29. The Appendices heading begins on page 30; pages 30-48 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    pdf=fitz.open(source);labels=[]
    assert len(pdf)==48 and hashlib.sha256(source.read_bytes()).hexdigest()==paper['pdf_sha256']
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

if __name__ == "__main__":
    main()
