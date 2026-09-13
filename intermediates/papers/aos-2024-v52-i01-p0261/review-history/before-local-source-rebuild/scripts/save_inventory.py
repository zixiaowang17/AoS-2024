"""Save the four complete published main-text Theorems before interface extraction."""
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
PDF=Path('[local-workspace]/minimax/reference/aos2024/pdf/23-AOS2346.pdf')
SKILL=Path('skills/statistical-paper-census/scripts')
SHA='5c9496bc2c45f9538e22a05064c3988a3f80f29fd33caced41a34087c4a18f6c'
URL='https://projecteuclid.org/journals/annals-of-statistics/volume-52/issue-1/Rates-of-estimation-for-high-dimensional-multireference-alignment/10.1214/23-AOS2346.pdf'
STATEMENTS=[
('2.1','Minimax risk in high noise',6,r'''Fix any $\beta\in[0,\frac12)$ and any constant $c_0>0$. If $\sigma^2\geq c_0K^{1-2\beta}$, then for a constant $C_0>0$ depending only on $\beta$, $\underline c$, $\overline c$, $c_0$ and for any $N\geq C_0K^{6\beta}\sigma^6\log K$,
\[
\inf_{\widehat\theta}\sup_{\theta^*\in\Theta_\beta}\mathbb E_{\theta^*}[L(\widehat\theta,\theta^*)]\asymp\frac{K^{4\beta}\sigma^6}{N}.
\]'''),
('2.2','Minimax risk in low noise',6,r'''Fix any $\beta\in[0,\frac12)$. There exist constants $C_0,C_1>0$ depending only on $\beta$, $\underline c$, $\overline c$ such that if $\sigma^2\leq\frac{K^{1-2\beta}}{C_1\log K}$ and $N\geq C_0K^{1+2\beta}\sigma^2\log K$, then
\[
\inf_{\widehat\theta}\sup_{\theta^*\in\Theta_\beta}\mathbb E_{\theta^*}[L(\widehat\theta,\theta^*)]\asymp\frac{K\sigma^2}{N}.
\]'''),
('4.1',None,8,r'''Let $\widehat\theta\in\{\widehat\theta^{\mathrm{oracle}},\widehat\theta^{\mathrm{opt}}\}$ be the above method-of-moments estimator, where $\widehat\Phi_{k,l}$ is chosen either using the oracle of Section 4.1 or the optimization procedure of Section 4.2. Suppose $r_k\geq\underline r>0$ for each $k=1,\ldots,K$. There exist universal constants $C,C_0>0$ such that if $N\geq C_0(\frac{\sigma^6}{\underline r^6}\log K+\frac{\sigma^3}{\underline r^3}(\log K)^{3/2})$, then
\[
\mathbb E[L(\widehat\theta,\theta^*)]\leq CK\left(\frac{\sigma^2}{N}+\frac{\sigma^4}{N\underline r^2}\right)+\frac{C\|\theta^*\|^2}{K}\left(\frac{K\sigma^2}{N\underline r^2}+\frac{\sigma^6}{N\underline r^6}\right).\tag{19}
\]'''),
('5.2',None,15,r'''Suppose Assumption 5.1 holds. Then there exist constants $C,C_0,C_1>0$ depending only on $c_{\mathrm{gen}}$ such that if $\sigma^2\leq\frac{K}{C_1\log K}$ and $N\geq C_0K(1+\frac{K\sigma^2}{\|\theta^*\|^2})\log(K+\frac{\|\theta^*\|^2}{\sigma^2})$, then
\[
\mathbb E_{\theta^*}[L(\widehat\theta^{\mathrm{MLE}},\theta^*)]\leq\frac{CK\sigma^2}{N}.
\]''')]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
    assert digest(PDF)==SHA
    doc=fitz.open(PDF);assert len(doc)==24
    assert doc.metadata['title']=='Rates of estimation for high-dimensional multireference alignment'
    heads=[]
    for i,page in enumerate(doc):
        t=page.get_text();(ROOT/'evidence'/f'page-{i+1:02}.txt').write_text(t)
        for m in re.finditer(r'(?m)^THEOREM (\d+\.\d+)(?:\.| \()',t):heads.append(dict(number=m[1],page=i+1))
    assert heads==[dict(number=n,page=p) for n,_,p,_ in STATEMENTS]
    for n in [1,6,8,9,15,16,22,23,24]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    claims=[]
    for order,(number,title,page,body) in enumerate(STATEMENTS,1):
        label='Theorem '+number+(' ('+title+')' if title else '')
        claims.append(dict(claim_id=PID+'/T'+number,paper_id=PID,claim_kind='theorem',label=label,source_order=order,
            statement_original=body,evidence=[dict(page=page,location=label+', published page '+str(260+page))]))
    paper=dict(paper_id=PID,title=doc.metadata['title'],version='Published version: The Annals of Statistics 52(1), 2024, pp. 261-284; DOI 10.1214/23-AOS2346',
        source_url=URL,pdf_pages=24,pdf_sha256=SHA,main_text_last_pdf_page=22,
        main_text_boundary=dict(location='Section 6 concludes on PDF page 22 (published page 282). Acknowledgments, funding and a notice for a separate supplement follow; references begin on the same page and continue through PDF page 24. The published PDF has no embedded appendix. The linked supplementary appendices were not opened.',shared_page_with_appendix=False),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    write('theorem-inventory.json',dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims))
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)
    write('evidence/enumeration.json',dict(headings=heads,method='Enumerate numbered uppercase THEOREM starts over all pages of the published PDF; visually inspect all four complete statements and their endpoints. Section 6 ends on page 22; the supplement is a separate linked file and subsequent pages are references.',source_pdf_metadata=doc.metadata,appendix_body_present=False,separate_supplement_opened=False))
    manifest=Path('[local-workspace]/minimax/reference/aos2024/manifest.json')
    source=next(x for x in json.loads(manifest.read_text())['papers'] if x['id']=='23-AOS2346');assert source['download']['sha256']==SHA
    write('evidence/source-provenance.json',dict(source_manifest_path=str(manifest),source_record=source,pdf_path=str(PDF),verified_sha256=SHA,verified_pdf_pages=24,published_metadata=doc.metadata))
    write('inventory-review.json',dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        theorem_count=4,inventory_sha256=digest(ROOT/'theorem-inventory.json'),notes=[
            'The four stored results are exactly Theorems 2.1, 2.2, 4.1 and 5.2. Their complete bodies were visually checked on PDF pages 6, 8 and 15. Section numbers and printed titles are retained.',
            'Theorem 2.1 retains the high-noise threshold c0 K^(1-2 beta), sample threshold C0 K^(6 beta) sigma^6 log K and rate K^(4 beta) sigma^6/N.',
            'Theorem 2.2 retains the low-noise threshold K^(1-2 beta)/(C1 log K), sample threshold C0 K^(1+2 beta) sigma^2 log K and rate K sigma^2/N. Both minimax theorems keep beta in [0,1/2) and their respective constant-dependence clauses.',
            'Theorem 4.1 includes both oracle and optimization-based method-of-moments estimators, the strictly positive lower bound on every Fourier magnitude, both sample-threshold terms and the complete two-part risk bound in (19). The following simplified bound is a remark outside the theorem.',
            'Theorem 5.2 invokes Assumption 5.1; its constants depend only on c_gen. The sample threshold retains both the signal-norm-dependent prefactor and logarithm. The proof-specific rotation chosen afterward is not part of the theorem statement.',
            'The common minimax expectation/estimator/asymptotic-comparison convention following Theorems 2.1 and 2.2 is separate surrounding prose; it will be archived during definition extraction.',
            'The lower-bound results in Section 6 are labelled Lemma, not Theorem, and are not added to the inventory. No supplementary appendix was opened.']))
    write('checkpoint.json',dict(paper_id=PID,stage='interface_extraction',inventory_status='validated',source_pdf_path=str(PDF),source_pdf_sha256=SHA,
        remaining_work='Extract the circular/Fourier observation model, rotation-invariant loss, decay class, minimax conventions, method-of-moments procedure with distinct oracle/optimization phase choices, likelihood estimator and Assumption 5.1. Preserve theorem-local dependencies rather than proof lemmas, then finalize and source-check.'))
    print('Saved and independently validated four complete original main-text Theorems.')
if __name__=='__main__':main()
