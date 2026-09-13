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
WORK=Path('[local path omitted]')/PID
PDF=Path('[local-workspace]/minimax/reference/aos2024/pdf/23-AOS2342.pdf')
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
    assert digest(PDF)==SHA
    doc=fitz.open(PDF);assert len(doc)==28
    assert doc.metadata['title']=='Settling the sample complexity of model-based offline reinforcement learning'
    heads=[]
    for i,page in enumerate(doc):
        text=page.get_text()
        for m in re.finditer(r'(?m)^THEOREM (\d+)\.',text):heads.append(dict(number=m[1],page=i+1))
        (ROOT/'evidence'/f'page-{i+1:02}.txt').write_text(text)
    assert heads==[dict(number=n,page=p) for n,p,_ in STATEMENTS]
    assert all('THEOREM ' not in doc[i].get_text() for i in range(25,28))
    for p in [1,12,13,19,20,25,26,28]:shutil.copy2(WORK/f'page-{p:02}.png',ROOT/'evidence'/f'page-{p:02}.png')
    claims=[dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=i,
        statement_original=body,evidence=[dict(page=p,location='Theorem '+n+', published page '+str(232+p))])
        for i,(n,p,body) in enumerate(STATEMENTS,1)]
    paper=dict(paper_id=PID,title=doc.metadata['title'],version='Published version: The Annals of Statistics 52(1), 2024, pp. 233-260; DOI 10.1214/23-AOS2342',
        source_url=URL,pdf_pages=28,pdf_sha256=SHA,main_text_last_pdf_page=25,
        main_text_boundary=dict(location='Section 6 Discussion concludes on PDF page 25 (published page 257), followed by acknowledgments and a notice linking a separate supplement. References begin on the same page and continue through PDF page 28. The published PDF contains no appendix body; the linked supplement was not opened.',shared_page_with_appendix=False),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    write('theorem-inventory.json',dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims))
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)
    write('evidence/enumeration.json',dict(headings=heads,method='Enumerate printed uppercase THEOREM paragraph starts across the 28-page published PDF. Inspect full statements on PDF pages 12, 13, 19 and 20. Confirm the discussion/supplement-notice/reference boundary on page 25 and references-only pages thereafter.',source_pdf_metadata=doc.metadata,appendix_body_present=False,separate_supplement_opened=False))
    manifest=Path('[local-workspace]/minimax/reference/aos2024/manifest.json')
    source=next(x for x in json.loads(manifest.read_text())['papers'] if x['id']=='23-AOS2342')
    assert source['download']['sha256']==SHA
    write('evidence/source-provenance.json',dict(source_manifest_path=str(manifest),source_record=source,pdf_path=str(PDF),verified_sha256=SHA,verified_pdf_pages=28,published_metadata=doc.metadata))
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',
        reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=4,inventory_sha256=digest(ROOT/'theorem-inventory.json'),notes=[
          'Every complete statement was transcribed from the published PDF; no title was invented for the four untitled numbered Theorems.',
          'Theorem 1 preserves its iteration-count condition, probability at least 1-2 delta, sufficient penalty constant, logarithmic sample-size threshold, and final alternative replacing clipped concentrability with ordinary concentrability.',
          'Theorem 2 preserves gamma>=2/3, S>=2, clipped concentrability>=8 gamma/S, the accuracy bound 1/[42(1-gamma)], two MDPs, strict loss >epsilon and probability lower bound 1/8.',
          'Theorem 3 preserves probability exceeding 1-12 delta, the Algorithm 3 policy, the (55) penalty, trajectory count K rather than transition count N, and the alternative ordinary concentrability coefficient.',
          'Theorem 4 preserves H>=12, clipped concentrability>=8/S, epsilon<=c3 H, the collection of MDPs, non-strict loss >=epsilon, probability lower bound 1/4, and N=KH.',
          'Theorem 2 and Theorem 4 print all estimator in the singular; this wording is retained. No additional positivity or state-count assumptions are inserted into their original bodies.',
          'The main-text result statements are distinct from explanatory Remarks and Lemmas. Their proofs are deferred to a separate supplement, which was not opened.']))
    write('checkpoint.json',dict(paper_id=PID,stage='interface_extraction',inventory_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=SHA,
        remaining_work='Extract separate discounted and episodic MDP models, value functions, occupancy and concentrability definitions, data-sampling models, Bernstein penalties and Algorithms 1-3. Preserve theorem-local assumptions and ordinary/clipped alternatives, then finalize and source-check the census.'))
    print('Saved and independently validated all four original main-text Theorems.')
if __name__=='__main__':main()
