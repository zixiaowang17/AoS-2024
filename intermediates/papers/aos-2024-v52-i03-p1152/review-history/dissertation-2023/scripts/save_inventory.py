"""Preserve the four Theorems in the corresponding 2023 author-manuscript chapter."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,page,text):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=page,location='Chapter 3 — Theorem '+n)]))
claim('3.5.1',112,r'''
Suppose Assumptions 3.5.1-3.5.3 hold and that the true parameter $\theta_0\in\mathbb R^p$ satisfies the spectral moment condition (3.2). If $b/n+n/b^2\to0$ as $n\to\infty$, then
\[
\ell_n(\theta_0)\xrightarrow{d}\chi_p^2.
\]
''')
claim('3.6.1',115,r'''
With Assumptions 3.5.1-3.5.3, suppose the following regularity conditions in a neighborhood of $\theta_0$ satisfying (3.2): (i) partial derivatives $\partial G_\theta(\cdot)/\partial\theta$, $\partial^2G_\theta(\cdot)/\partial\theta\partial\theta^\intercal$, $\partial\mathcal M_\theta/\partial\theta$ and $\partial^2\mathcal M_\theta/\partial\theta\partial\theta^\intercal$ exist; (ii) each component $\partial g_{i,\theta_0}(\cdot)/\partial\theta_j$ of $\partial G_{\theta_0}(\cdot)/\partial\theta$ is Riemann integrable for $i,j=1,\ldots,p$; (iii) $\|\partial\mathcal M_\theta/\partial\theta\|$, $\left\|\partial^2\mathcal M_\theta/\partial\theta\partial\theta^\intercal\right\|$ are bounded, and $\|\partial G_\theta(\cdot)/\partial\theta\|$, $\left\|\partial^2G_\theta(\cdot)/\partial\theta\partial\theta^\intercal\right\|$ are bounded by a Riemann integrable function $H(\cdot):[-\pi,\pi]\mapsto\mathbb R^+$; and (iv) $D_{\theta_0}\equiv\int_{-\pi}^\pi[\partial G_{\theta_0}(\lambda)/\partial\theta]f(\lambda)d\lambda-\partial\mathcal M_{\theta_0}/\partial\theta$ is non-singular.

Then, as $n\to\infty$, there exists a solution sequence $\{\widehat\theta_n\}$ such that $\widehat\theta_n\xrightarrow{p}\theta_0$ and, furthermore, $\sqrt n(\widehat\theta_n-\theta_0)\xrightarrow{d}\mathcal N(0_p,\Sigma_{\theta_0})$, where $\Sigma_{\theta_0}\equiv(D_{\theta_0}^\intercal V_{\theta_0}^{-1}D_{\theta_0})^{-1}$.
''')
claim('3.6.2',118,r'''
Under assumptions of Theorem 3.6.1, if $b/n+n/b^2\to0$ as $n\to\infty$, then
\[
\sup_{x\in\mathbb R}\left|\mathbb P_*(\ell_n^*(\widehat\theta_n)\le x)-\mathbb P(\ell_n(\theta_0)\le x)\right|\xrightarrow{p}0.
\]
''')
claim('3.8.1',129,r'''
Suppose Assumptions for Theorem 3.6.2 hold. If, additionally, the function $h(\cdot):\mathbb R^p\mapsto\mathbb R^s$ is continuously differentiable in a neighborhood of the true parameter $\theta_0$ (defining $\vartheta_0=h(\theta_0)$), then, as $b/n+n/b^2\to\infty$,
\[
\ell_n(\vartheta_0)\xrightarrow{d}\chi_u^2\qquad\text{and}\qquad\sup_{x\in\mathbb R}\left|\mathbb P_*(\ell_n^*(\widehat\vartheta_n)\le x)-\mathbb P(\ell_n(\vartheta_0)\le x)\right|\xrightarrow{p}0,
\]
where $u$ denotes the rank of the $s\times p$ matrix $\partial h(\theta)/\partial\theta|_{\theta=\theta_0}$.
''')

if __name__=='__main__':
    pdf=fitz.open(prov['cached_pdf']);assert len(pdf)==295
    assert hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==prov['pdf_sha256']
    chapter=' '.join(pdf[98].get_text().split());assert prov['source_title'].upper() in chapter
    for name in prov['authors']:assert name in chapter
    assert 'Modified from a manuscript under review by The Annals of Statistics' in chapter
    assert '2023' in pdf[0].get_text() and 'Haihan Yu' in pdf[0].get_text()
    labels=[];mentions=[]
    for n in range(99,137):
        page=pdf[n-1];assert (ROOT/'evidence'/f'page-{n:03}.txt').read_bytes().decode('utf8')==page.get_text()
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans']).strip();m=re.match(r'^Theorem\s+(\d+(?:\.\d+)+)',text)
                if m:
                    heading=any(s['font']=='NimbusRomNo9L-Medi' and 'Theorem' in s['text'] for s in line['spans'])
                    (labels if heading else mentions).append((n,m[1]))
    assert labels==[(112,'3.5.1'),(115,'3.6.1'),(118,'3.6.2'),(129,'3.8.1')]
    assert mentions==[(112,'3.5.1'),(118,'3.5.1'),(129,'3.8.1'),(129,'2.1'),(129,'3.8.1')]
    assert 'Zhu, K. (2016)' in pdf[135].get_text()
    assert 'Appendix A: Additional numerical results' in pdf[136].get_text(clip=fitz.Rect(0,105,pdf[136].rect.width,126))
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in claims]==labels
    for c in claims:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
            depth=0
            for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if brace=='{' else -1
                assert depth>=0,c['claim_id']
            assert depth==0,c['claim_id']
    paper={k:prov[k] for k in ['paper_id','title','source_title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_first_pdf_page=99,main_text_last_pdf_page=136,main_text_boundary=dict(location='Only dissertation Chapter 3 main text and references, PDF pages99–136 (printed89–126), are in scope. Its Appendix A starts on PDF137 at y=110.645195; all chapter appendix material and every other dissertation chapter are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Corresponding author-manuscript version in the 2023 institutional dissertation, Chapter3 only. Preserve original manuscript numbering and title separately from the final journal title; final-version equivalence is not asserted.'),papers=[paper],claims=claims)
    path=ROOT/'theorem-inventory.json';path.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    for n in [112,115,118,129]:shutil.copyfile(Path(prov['working_pdf']).parent/f'page-{n:03}.png',ROOT/'evidence'/f'page-{n:03}.png')
    notes=[
     'The source is the 2023 dissertation Chapter3 author manuscript, titled A composite empirical likelihood method for time series in frequency domain inference. It lists the same three authors and explicitly identifies itself as modified from an Annals submission; provenance retains the published-title comparison.',
     'The institutional PDF has295 pages. Only Chapter3 main text and references on PDF99–136 (printed89–126) are used. The following chapter appendix begins at PDF137; other chapters and every appendix are excluded.',
     'Independent bold-font heading enumeration identifies four actual Theorems and five ordinary-font references, including an external Theorem2.1 citation. Each full statement fits on one page.',
     'Theorem3.5.1 retains all three assumption references, spectral moment condition(3.2), b/n+n/b^2 tending to zero, and the chi-square limit with p degrees of freedom.',
     'Theorem3.6.1 retains all four regularity conditions, including the second derivatives, Riemann-integrable derivative components and envelope, nonsingular D_theta0, existence of a consistent solution sequence, and the full asymptotic covariance formula.',
     'Theorem3.6.2 retains the referenced M-estimation assumptions, block-size condition and supremum over real x of the bootstrap-versus-sampling CDF difference, converging in probability.',
     'Theorem3.8.1 literally prints b/n+n/b^2 tending to infinity while importing Theorem3.6.2 assumptions that include the same expression tending to zero. The printed infinity is preserved as a source conflict; it is not corrected in the original statement.',
     'Theorem3.8.1 preserves both smooth-function conclusions and the definition of u as the rank of the s-by-p Jacobian. The source does not explicitly require a constant rank in a neighborhood in this theorem.',
     'Script M denotes the spectral moment function, script N the normal law, and plain D,V,Sigma are matrices. Bootstrap probability P_* has a subscript star while the bootstrap log-ratio ell_n^* has a superscript star; PDF font positions were checked.',
     'This inventory describes the pinned manuscript version, not a verified reconciliation against the final journal article. Complete source extraction, dependencies and independent final census review remain.'
    ]
    (ROOT/'inventory-review.json').write_text(json.dumps(dict(paper_id=PID,status='complete',source_checked=True,inventory_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='Independent bold-heading enumeration restricted to PDF99–136, followed by visual review of all four full original statements.',theorem_ids=[c['claim_id'] for c in claims],notes=notes),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),next_action='Extract main-text prerequisites of all four original Theorems from Chapter3 only, PDF99–136: Assumptions3.5.1–3.5.3, spectral moments and estimating functions, process/spectral density and cumulants, periodograms and data blocks, SEL objective/log-ratio, spectral M-estimator and regularity conditions, SEL bootstrap probability/statistic, and smooth-function profile statistics. Preserve script M, subscript P_* and printed infinite block-size limit in3.8.1. Keep manuscript-version correspondence and final-journal uncertainty explicit. No appendix or other chapter mathematics.'),indent=2)+'\n')
    print('Saved and independently validated all four original manuscript Theorems.')
