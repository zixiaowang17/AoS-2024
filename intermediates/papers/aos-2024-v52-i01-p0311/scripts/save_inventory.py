"""Save the source-reviewed main-text inventory before interface extraction."""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
PID = ROOT.name
REPO = ROOT.parents[3]
SHA = '349496d29be69819df89de9cc87ff4f226c0cb48c1e917a0d4c6514c3784a28a'
claims = []
def claim(number, page, body, title=None):
    claims.append(dict(claim_id=PID+'/T'+number, paper_id=PID,
        claim_kind='theorem', label='Theorem '+number+((' ('+title+')') if title else ''),
        source_order=len(claims)+1, statement_original=body.strip(),
        evidence=[dict(page=page, location='Theorem '+number)]))

claim('3.1', 6, r'''
Under the null hypothesis $H_5$, if $d=d_n\to\infty$, we have
\[
\frac{T_n(2)-\nu_n(2)}{\delta_n(2)}\rightsquigarrow\mathcal N(0,1).
\]
Moreover, under the null hypothesis $H_{4m-3}$ and if $d=d_n\to\infty$ such that $d=o\left(n^{\frac1{m-1}}\right)$, we have
\[
\left(\frac{T_n(2)-\nu_n(2)}{\delta_n(2)},\ldots,\frac{T_n(m)-\nu_n(m)}{\delta_n(m)}\right)\rightsquigarrow\mathcal N(0,1)^{\otimes(m-1)}.
\]
Finally, the same results are true if $\delta_n(m)$ is replaced by $\bar\delta_n(m)$.
''')
claim('6.5', 20, r'''
Let $d=d_n\to\infty$. Let $\eta^2$ be an a.s. finite r.v. and let $\{(S_{n,r},\mathcal F_{n,r}):1\leq r\leq d,n\geq1\}$ be a zero-mean, square integrable martingale array with differences $X_{n,r}=S_{n,r}-S_{n,r-1}$. If $\mathcal F_{n,r}\subset\mathcal F_{n+1,r}$ for all $1\leq r\leq d$ and $n\geq1$ and if
\[
\forall\varepsilon>0:\quad\sum_{r=1}^d\mathbb E\left[X_{n,r}\mathbf1_{\{|X_{n,r}|>\varepsilon\}}\mid\mathcal F_{n,r-1}\right]\xrightarrow[n\to+\infty]{\mathbb P}0,\tag{6.24}
\]
\[
\sum_{r=1}^d\mathbb E\left[X_{n,r}^2\mid\mathcal F_{n,r-1}\right]\xrightarrow[n\to+\infty]{\mathbb P}\eta^2,\tag{6.25}
\]
then $S_{n,d}=\sum_{r=1}^dX_{n,r}\rightsquigarrow Z$, where $Z$ is a random variable distributed as $\eta N$ with $N\sim\mathcal N(0,1)$ independent of $\eta$. Moreover, the Lindeberg condition in (6.24) is a consequence of the Lyapunov condition:
\[
\sum_{r=1}^d\mathbb E\left[X_{n,r}^4\mid\mathcal F_{n,r-1}\right]\xrightarrow[n\to+\infty]{\mathbb P}0.\tag{6.26}
\]
.
''', 'Corollary 3.1 in Hall and Heyde, 1980')
def main():
    source = Path(subprocess.check_output([sys.executable, str(REPO / 'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == SHA
    pdf = fitz.open(source)
    assert len(pdf) == 51 and '2204.01803v1' in pdf[0].get_text()
    prov = dict(paper_id=PID, title='Testing for independence in high dimensions based on empirical copulas', version='arXiv:2204.01803v1', source_url='https://arxiv.org/pdf/2204.01803v1', pdf_pages=51, pdf_sha256=SHA)
    paper = {k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=30,
        main_text_boundary=dict(location='Main body ends with Section 6.7 and acknowledgements on PDF page 29, followed by references ending on page 30. Page 31 starts a separate supplementary-material title, abstract and Appendix A heading. Appendix bodies are excluded.',shared_page_with_appendix=False),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inventory=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    path=ROOT/'theorem-inventory.json'
    path.write_text(json.dumps(inventory,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
    review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',
        reviewed_at=datetime.now(timezone.utc).isoformat(),theorem_count=len(claims),inventory_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        notes=[
            'Pinned arXiv:2204.01803v1, stamped 4 April 2022 (manuscript date April 6, 2022); no identity with the later journal version is assumed.',
            'All 30 main-document pages were searched for printed Theorem environments. Theorem 3.1 and Theorem 6.5 are the only two; Theorem 6.5 remains included although attributed to Hall and Heyde and placed in a proofs section.',
            'Theorem 4.1 on page 6 is a citation to Leung and Drton, not a local result. Proof headings, other citations, Corollary 3.2 and all Propositions/Lemmas are excluded.',
            'Theorem 3.1 preserves its unrestricted diverging-d first regime, its separate d=o(n^(1/(m-1))) joint regime under H_(4m-3), product normal law, and the final delta_n(m) replacement exactly as printed.',
            'Theorem 6.5 was visually checked: equation (6.24) contains X_(n,r) to the first power, whereas equations (6.25) and (6.26) contain powers two and four. The possibly erroneous first-power formula is preserved for downstream review.',
            'The theorem retains the cross-row filtration inclusion, a.s.-finite eta^2, the mixed normal limit with independence, and the Lyapunov sufficient-condition clause.',
            'Main/supplement boundary confirmed from PDF outline, last reference page and a crop ending at the Appendix A heading; no appendix body was read.'
        ])
    (ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Extract source definitions and conditions, connect both inventoried theorems, and validate the resulting census.',updated_at=review['reviewed_at']),indent=2)+'\n')
    print('Saved and independently validated two-Theorem inventory.')

if __name__ == '__main__':
    main()
