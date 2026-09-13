"""Source-checked transcription from the pinned 23-page author manuscript."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import fitz

ROOT=Path(__file__).resolve().parents[1]
PID=ROOT.name
REPO=ROOT.parents[3]

SKILL=Path('skills/statistical-paper-census/scripts')
SHA='7ec9d3f7bef00582b4790863c99d76c3d61f56d92373dfb64620a1793a5e7f7c'
STATEMENTS=[
 ('1',[9],r'''Suppose $\mathbf{x}$ and $\mathbf{y}$ are continuous, and Assumption 1 holds. Under $H_0$ in (1), as $\max(p,q)\to\infty$ and $n\to\infty$,
\[
\Delta_h\{C(d,2)\}^{-1}\{C(n,2)\}^{1/2}\sum_{k=1}^{p}\sum_{l=1}^{q}\widehat{U}^{(kl)}_h\,/\,S\xrightarrow{D}N(0,1),
\]
where $\xrightarrow{D}$ stands for "convergence in distribution".'''),
 ('2',[9],r'''Under the conditions in Theorem 1, $\widehat{S}^{2}/S^{2}\xrightarrow{P}E(\widehat{S}^{2}/S^{2})=1$, where $\xrightarrow{P}$ denotes "convergence in probability". Accordingly, $\widehat{T}_h\xrightarrow{D}N(0,1)$.'''),
 ('3',[9,10],r'''Under the conditions in Theorem 1, we have
\[
\begin{aligned}
&\sup_{x\in\mathbb{R}}|P(\widehat{T}_h\leq x)-\Phi(x)|\\
&\leq C\left[\frac{E\{V(\mathbf{z}_1,\mathbf{z}_2)V(\mathbf{z}_2,\mathbf{z}_3)V(\mathbf{z}_3,\mathbf{z}_4)V(\mathbf{z}_4,\mathbf{z}_1)\}+n^{-1}E\{V(\mathbf{z}_1,\mathbf{z}_2)^4\}}{E^2\{V(\mathbf{z}_1,\mathbf{z}_2)^2\}}\right]^{1/5},
\end{aligned}
\]
where $C$ is a universal constant which is completely independent of $n$, $p$ and $q$, and $\Phi(\cdot)$ is the standard normal distribution function.'''),
 ('4',[11],r'''Suppose $\{\widehat{U}^{(kl)}_h:1\leq k\leq p,1\leq l\leq q\}$ have a common kernel $h$ that satisfies conditions (8)-(10). As $\max(p,q)\to\infty$ and $n\to\infty$,
\[
\Delta_h\{C(d,2)\}^{-1}\{C(n,2)\}^{1/2}\sum_{k=1}^{p}\sum_{l=1}^{q}\{\widehat{U}^{(kl)}_h-\theta^{(kl)}_h\}/S\xrightarrow{D}N(0,1).
\]'''),
 ('5',[12,13],r'''Assume $(X_k,Y_l)\in\mathbb{R}^2$ is bivariate Gaussian with Pearson correlation $\rho_{kl}$, for $1\leq k\leq p$ and $1\leq l\leq p$. Then

(1) $E\{\widehat{U}^{(kl)}_h\}=M_h(\rho_{kl})$, where
\[
\begin{aligned}
M_{h^{(D)}}(\rho_{kl})
&=(4\pi^2)^{-1}[(\arcsin\rho_{kl})^2-\{\arcsin(\rho_{kl}/2)\}^2]\\
&\quad+\pi^{-2}\left[\int_0^{\arcsin\frac{\rho_{kl}}{2}}\arcsin\left(\frac{\sin x}{2\cos 2x+1}\right)\,dx\right.\\
&\qquad\left.+\int_0^{\arcsin\frac{\rho_{kl}}{2}}\arcsin\left\{\left(\frac{2\cos 2x-1}{6\cos 2x+3}\right)^{1/2}\sin x\right\}\,dx\right]\\
&\quad-(2\pi^2)^{-1}\left\{\int_0^{\arcsin\rho_{kl}}\arcsin\left(\frac{\sin x}{3}\right)\,dx\right.\\
&\qquad\left.+\int_0^{\arcsin\frac{\rho_{kl}}{2}}\arcsin\left(\frac{2\cos 2x+3}{2\cos 2x+1}\sin x\right)\,dx\right\},
\end{aligned}
\]
\[
\begin{aligned}
M_{h^{(R)}}(\rho_{kl})
&=(2\pi^2)^{-1}\left\{\int_0^{\arcsin\frac{\rho_{kl}}{2}}\arcsin\left(\frac{2\cos 2x+3}{2\cos 2x+1}\sin x\right)\,dx\right.\\
&\qquad\left.-\int_0^{\arcsin\frac{\rho_{kl}}{2}}\arcsin\left(\frac{\sin x}{2\cos 2x+1}\right)\,dx\right\},
\end{aligned}
\]
\[
\begin{aligned}
M_{h^{(\tau^*)}}(\rho_{kl})
&=3\pi^{-2}[(\arcsin\rho_{kl})^2-\{\arcsin(\rho_{kl}/2)\}^2]\\
&\quad+12\pi^{-2}\int_0^{\arcsin\frac{\rho_{kl}}{2}}\arcsin\left\{\left(\frac{2\cos 2x-1}{6\cos 2x+3}\right)^{1/2}\sin x\right\}\,dx\\
&\quad-6\pi^{-2}\left\{\int_0^{\arcsin\rho_{kl}}\arcsin\left(\frac{\sin x}{3}\right)\,dx\right.\\
&\qquad\left.-\int_0^{\arcsin\frac{\rho_{kl}}{2}}\arcsin\left(\frac{2\cos 2x+3}{2\cos 2x+1}\sin x\right)\,dx\right\};
\end{aligned}
\]

(2) $M_h(\rho_{kl})=M_h(-\rho_{kl})$ and $M_h(\rho_{kl})/\rho_{kl}^2$ is nondecreasing in $|\rho_{kl}|$;

(3)
\[
\begin{aligned}
\inf_{\rho_{kl}\ne0}\frac{M_{h^{(D)}}(\rho_{kl})}{\rho_{kl}^2}&=(12\pi^2)^{-1},\quad \sup_{\rho_{kl}\ne0}\frac{M_{h^{(D)}}(\rho_{kl})}{\rho_{kl}^2}=1/30,\\
\inf_{\rho_{kl}\ne0}\frac{M_{h^{(R)}}(\rho_{kl})}{\rho_{kl}^2}&=(12\pi^2)^{-1},\quad \sup_{\rho_{kl}\ne0}\frac{M_{h^{(R)}}(\rho_{kl})}{\rho_{kl}^2}=1/90,\\
\inf_{\rho_{kl}\ne0}\frac{M_{h^{(\tau^*)}}(\rho_{kl})}{\rho_{kl}^2}&=3\pi^{-2},\quad \sup_{\rho_{kl}\ne0}\frac{M_{h^{(\tau^*)}}(\rho_{kl})}{\rho_{kl}^2}=2/3.
\end{aligned}
\]''')]

def write(name,value):(ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    PDF=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(PDF)==SHA
    doc=fitz.open(PDF)
    assert len(doc)==23
    headings=[]
    for i,page in enumerate(doc):
        text=page.get_text()
        for match in re.finditer(r'(?im)^Theorem\s+(\d+)\.',text):
            headings.append(dict(number=match[1],page=i+1))
    assert headings==[dict(number=n,page=p[0]) for n,p,_ in STATEMENTS]
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,
        source_order=i,statement_original=body,evidence=[dict(page=p,location='Theorem '+n+(' — continued' if j else '')) for j,p in enumerate(pages)])
        for i,(n,pages,body) in enumerate(STATEMENTS,1)]
    paper=dict(paper_id=PID,title='Rank-based indices for testing independence between two high-dimensional vectors',
        version='PMC11064990 author manuscript; PDF created 2023-11-29',
        source_url='https://pmc.ncbi.nlm.nih.gov/articles/PMC11064990/pdf/',pdf_pages=23,pdf_sha256=SHA,
        main_text_last_pdf_page=23,
        main_text_boundary=dict(location='Discussion and acknowledgments on page 21, funding through page 22, a supplement availability notice on page 22, then references through the end of page 23. No appendix body is embedded in this PDF; the separate supplement is excluded.',shared_page_with_appendix=False),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    write('theorem-inventory.json',dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims))
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)

if __name__=='__main__':main()
