"""Pin and independently validate every main-text Theorem in the published PDF."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
REPO=ROOT.parents[3]

SKILL=Path('skills/statistical-paper-census/scripts')
SHA='b8117f2ba646465337f222538705d6960cb994d64c152b25a6b1799e80472363'
URL='https://projecteuclid.org/journals/annals-of-statistics/volume-52/issue-1/Settling-the-sample-complexity-of-model-based-offline-reinforcement-learning/10.1214/23-AOS2342.pdf'
STATEMENTS=[
('1',12,r'''Suppose $\gamma\in[\frac12,1)$, and consider any $0<\delta<1$ and $\varepsilon\in(0,\frac{1}{1-\gamma}]$. Suppose the total number of iterations exceeds $\tau_{\max}\geq\frac{1}{1-\gamma}\log\frac{N}{1-\gamma}$. With probability at least $1-2\delta$, the policy $\widehat\pi$ returned by Algorithm 1 obeys
\[
V^\star(\rho)-V^{\widehat\pi}(\rho)\leq\varepsilon,\tag{34}
\]
provided that $c_{\mathrm b}$ (cf. the Bernstein-style penalty term in (28)) is some sufficiently large numerical constant and the total sample size exceeds
\[
N\geq\frac{c_1SC^\star_{\mathrm{clipped}}\log\frac{NS}{(1-\gamma)\delta}}{(1-\gamma)^3\varepsilon^2}\tag{35}
\]
for some large enough numerical constant $c_1>0$, where $C^\star_{\mathrm{clipped}}$ is introduced in Definition 2. Also, the above result continues to hold if $C^\star_{\mathrm{clipped}}$ is replaced with $C^\star$ (see Definition 1).'''),
('2',13,r'''For any $(\gamma,S,C^\star_{\mathrm{clipped}},\varepsilon)$ obeying $\gamma\in[\frac23,1)$, $S\geq2$, $C^\star_{\mathrm{clipped}}\geq\frac{8\gamma}{S}$ and $\varepsilon\leq\frac{1}{42(1-\gamma)}$, one can construct two MDPs $\mathcal M_0,\mathcal M_1$, an initial state distribution $\rho$ and a batch data set with $N$ independent samples and single-policy clipped concentrability coefficient $C^\star_{\mathrm{clipped}}$ such that
\[
\inf_{\widehat\pi}\max\bigl\{\mathbb P_0\bigl(V^\star(\rho)-V^{\widehat\pi}(\rho)>\varepsilon\bigr),\mathbb P_1\bigl(V^\star(\rho)-V^{\widehat\pi}(\rho)>\varepsilon\bigr)\bigr\}\geq\frac18,
\]
provided that
\[
N\leq\frac{c_2SC^\star_{\mathrm{clipped}}}{(1-\gamma)^3\varepsilon^2}
\]
for some numerical constant $c_2>0$. Here, the infimum is over all estimator $\widehat\pi$, and $\mathbb P_0$ (resp., $\mathbb P_1$) denotes the probability when the MDP is $\mathcal M_0$ (resp., $\mathcal M_1$).'''),
('3',19,r'''Consider any $\varepsilon\in(0,H]$ and any $0<\delta<1$. With probability exceeding $1-12\delta$, the policy $\widehat\pi$ returned by Algorithm 3 obeys
\[
V^\star_1(\rho)-V^{\widehat\pi}_1(\rho)\leq\varepsilon\tag{58}
\]
as long as the penalty terms are chosen according to the Bernstein-style quantity (55) for some large enough numerical constant $c_{\mathrm b}>0$, and the number of sample trajectories exceeds
\[
K\geq\frac{c_{\mathrm k}H^3SC^\star_{\mathrm{clipped}}\log\frac{KH}{\delta}}{\varepsilon^2}\tag{59}
\]
for some sufficiently large numerical constant $c_{\mathrm k}>0$, where $C^\star_{\mathrm{clipped}}$ is introduced in Definition 4. Additionally, the above result continues to hold if $C^\star_{\mathrm{clipped}}$ is replaced with $C^\star$ (introduced in Definition 3).'''),
('4',20,r'''For any $(H,S,C^\star_{\mathrm{clipped}},\varepsilon)$ obeying $H\geq12$, $C^\star_{\mathrm{clipped}}\geq8/S$ and $\varepsilon\leq c_3H$, one can construct a collection of MDPs $\{\mathcal M_\theta\mid\theta\in\Theta\}$, an initial state distribution $\rho$ and a batch data set with $K$ independent sample trajectories each of length $H$, such that
\[
\inf_{\widehat\pi}\max_{\theta\in\Theta}\mathbb P_\theta\bigl\{V^\star_1(\rho)-V^{\widehat\pi}_1(\rho)\geq\varepsilon\bigr\}\geq\frac14,
\tag{60}
\]
provided that the total sample size
\[
N=KH\leq\frac{c_4C^\star_{\mathrm{clipped}}SH^4}{\varepsilon^2}.
\tag{61}
\]
Here, $c_3,c_4>0$ are some small enough numerical constants, the infimum is over all estimator $\widehat\pi$, and $\mathbb P_\theta$ denotes the probability when the MDP is $\mathcal M_\theta$.''')]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
    PDF=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(PDF)==SHA
    doc=fitz.open(PDF);assert len(doc)==28
    assert doc.metadata['title']=='Settling the sample complexity of model-based offline reinforcement learning'
    heads=[]
    for i,page in enumerate(doc):
        text=page.get_text()
        for m in re.finditer(r'(?m)^THEOREM (\d+)\.',text):heads.append(dict(number=m[1],page=i+1))
    assert heads==[dict(number=n,page=p) for n,p,_ in STATEMENTS]
    assert all('THEOREM ' not in doc[i].get_text() for i in range(25,28))
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,
        statement_original=body,evidence=[dict(page=p,location='Theorem '+n+', published page '+str(232+p))])
        for i,(n,p,body) in enumerate(STATEMENTS,1)]
    paper=dict(paper_id=PID,title=doc.metadata['title'],version='Published version: The Annals of Statistics 52(1), 2024, pp. 233-260; DOI 10.1214/23-AOS2342',
        source_url=URL,pdf_pages=28,pdf_sha256=SHA,main_text_last_pdf_page=25,
        main_text_boundary=dict(location='Section 6 Discussion concludes on PDF page 25 (published page 257), followed by acknowledgments and a notice linking a separate supplement. References begin on the same page and continue through PDF page 28. The published PDF contains no appendix body; the linked supplement was not opened.',shared_page_with_appendix=False),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    write('theorem-inventory.json',dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims))
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)

if __name__=='__main__':main()
