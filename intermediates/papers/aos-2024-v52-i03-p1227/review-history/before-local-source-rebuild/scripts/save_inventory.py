"""Save the independently enumerated main-text Theorems from the local v6 PDF."""
import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
PID = ROOT.name
prov = json.loads((ROOT / 'evidence/source-provenance.json').read_text())
claims = []

def claim(n, pages, text):
    claims.append(dict(claim_id=f'{PID}/T{n}', paper_id=PID, claim_kind='theorem',
        label=f'Theorem {n}', source_order=n, statement_original=text.strip(),
        evidence=[dict(page=p, location=f'Theorem {n}' + (' (continued)' if i else '')) for i,p in enumerate(pages)]))

claim(1, [9], r'''
Fix $\alpha\in(0,1)$ and $\nu\in(0,\alpha)$. Suppose that the simultaneous confidence regions $\{C_{\gamma\cdot\Gamma'}\}_{\Gamma'\subseteq\Gamma}$ are monotone (Ass. 1). Consider the set of targets
\[
\widehat\Gamma^+_\nu=\bigcup_{P'\in B_\nu(y)}\Gamma_\nu(P')=\bigcup_{P'\in B_\nu(y)}\bigcup_{y'\in A_\nu(P')}\widehat\Gamma(y').\tag{2}
\]
Then, it holds that
\[
P\left\{\theta_\gamma\in C^{(\alpha-\nu)}_{\gamma\cdot\widehat\Gamma^+_\nu},\forall\gamma\in\widehat\Gamma\right\}\ge1-\alpha.
\]
''')
claim(2, [10], r'''
Fix $\alpha\in(0,1)$ and $\nu\in(0,\alpha)$. Suppose that the confidence intervals are monotone (Ass. 1), i.e., $q^\alpha_{\Gamma_1}\le q^\alpha_{\Gamma_2}$ for all $\Gamma_1\subseteq\Gamma_2$, and centered (Ass. 2). Let $A_\nu(P)=\{y:\theta_\gamma\in C_\gamma(q^\nu_\Gamma),\forall\gamma\in\Gamma\}$, and let $\widehat\Gamma^+_\nu$ denote the set of targets from Theorem 1 (Eq. (2)). Let
\[
\hat q=\min\left\{q^{(\alpha-\nu)}_{\widehat\Gamma^+_\nu},q^\alpha_\Gamma\right\}.
\]
Then, it holds that
\[
P\left\{\theta_\gamma\in C_\gamma(\hat q),\forall\gamma\in\widehat\Gamma\right\}\ge1-\alpha.
\]
''')
claim(3, [11,12], r'''
Fix $\alpha\in(0,1)$ and $\nu\in(0,\alpha)$.

- For the problem of inference on the winner (Eq. (3)), let the set of plausible indices be
\[
\widehat\Gamma^+_\nu=\{\gamma\in[m]:y_\gamma\ge y_{\hat\gamma}-4q^\nu([m])\}.
\]
Then,
\[
P_\mu\left\{\mu_{\hat\gamma}\in\left(y_{\hat\gamma}\pm\min\left\{q^{(\alpha-\nu)}(\widehat\Gamma^+_\nu),q^\alpha([m])\right\}\right)\right\}\ge1-\alpha.
\]

- For the file-drawer problem (Eq. (4)), let the set of plausible indices be
\[
\widehat\Gamma^+_\nu=\{\gamma\in[m]:y_\gamma\ge T-2q^\nu([m])\}.
\]
Then,
\[
P_\mu\left\{\mu_\gamma\in\left(y_\gamma\pm\min\left\{q^{(\alpha-\nu)}(\widehat\Gamma^+_\nu),q^\alpha([m])\right\}\right),\forall\gamma\in\widehat\Gamma\right\}\ge1-\alpha.
\]
''')
claim(4, [13], r'''
Fix $\alpha\in(0,1)$ and $\nu\in(0,\alpha)$. Assume that $C^{\alpha_1}_\gamma\supseteq C^{\alpha_2}_\gamma$ for all $\alpha_1,\alpha_2\in(0,1)$ such that $\alpha_1\le\alpha_2$.

- For the problem of inference on the winner (Eq. (5)), let the set of plausible indices be
\[
\widehat\Gamma^+_\nu=\left\{\gamma\in[m]:y_\gamma\ge y_{\hat\gamma}-4w^{\nu/m}_n\right\}.
\]
Then,
\[
P\left\{\theta_{\hat\gamma}\in C^{(\alpha-\nu)/|\widehat\Gamma^+_\nu|}_{\hat\gamma}\right\}\ge1-\alpha.
\]

- For the file-drawer problem (Eq. (6)), let the set of plausible indices be
\[
\widehat\Gamma^+_\nu=\left\{\gamma\in[m]:y_\gamma\ge T-2w^{\nu/m}_n\right\}.
\]
Then,
\[
P\left\{\theta_\gamma\in C^{(\alpha-\nu)/|\widehat\Gamma^+_\nu|}_\gamma,\forall\gamma\in\widehat\Gamma\right\}\ge1-\alpha.
\]
''')
claim(5, [16], r'''
Algorithm 1 returns exactly the set of plausible models, i.e.
\[
\widehat{\mathcal M}^+_\nu=\left\{\widehat M(y'):\|X^\top y-X^\top y'\|_\infty\le2q^\nu(\{X_j\}_{j=1}^d)\right\}.
\]
''')
claim(6, [17], r'''
Fix $\alpha\in(0,1)$ and $\nu\in(0,\alpha)$. Assume that $|\ell(f,z)|\le1$ for all $z$ and $f\in\mathcal F$. Consider the data-dependent hypothesis class:
\[
\widehat{\mathcal F}^+_\nu=\left\{f\in\mathcal F:R_n(f,\mathcal D)\le R_n(\hat f,\mathcal D)+4\operatorname{Gap}_n(\mathcal F)+4\sqrt{\frac2n\log\left(\frac1\nu\right)}\right\}.
\]
Then,
\[
P\left\{R(\hat f,P)\le R_n(\hat f,\mathcal D)+\operatorname{Gap}_n(\widehat{\mathcal F}^+_\nu)+\sqrt{\frac2n\log\left(\frac1{\alpha-\nu}\right)}\right\}\ge1-\alpha.
\]
''')

if __name__ == '__main__':
    pdf = fitz.open(prov['cached_pdf'])
    assert len(pdf) == 36
    assert hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest() == prov['pdf_sha256']
    assert 'arXiv:2212.09009v6' in pdf[0].get_text()
    headings=[]; ordinary=[]
    for i in range(27):
        assert (ROOT/'evidence'/f'page-{i+1:02}.txt').read_bytes().decode('utf8') == pdf[i].get_text()
        for b in pdf[i].get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                m=re.match(r'^Theorem (\d+)\.',text)
                if m:
                    (headings if 'BX' in line['spans'][0]['font'] else ordinary).append((i+1,int(m[1])))
    assert headings == [(9,1),(10,2),(11,3),(13,4),(16,5),(17,6)]
    assert ordinary == [(16,5)]
    assert 'Deferred proofs' in pdf[27].get_text(clip=fitz.Rect(70,100,550,126))
    assert '[36]' in pdf[26].get_text()
    for c in claims:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$', c['statement_original'], re.S):
            depth=0
            for b in re.findall(r'(?<!\\)[{}]', ''.join(chunks)):
                depth += 1 if b == '{' else -1
                assert depth >= 0, c['claim_id']
            assert depth == 0, c['claim_id']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=27, main_text_boundary=dict(location='Substantive main text ends with acknowledgements on PDF page 25; references continue through page 27. Appendix A, Deferred proofs, begins on page 28 at y=106.64. All appendices are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Existing local arXiv:2212.09009v6 PDF, pages 1–27 before Appendix A; no external retrieval.'),papers=[paper],claims=claims)
    dest=ROOT/'theorem-inventory.json';dest.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(dest)],check=True)
    notes=[
        'All six bold Theorem headings independently enumerated across pages 1–27. The ordinary-font Theorem 5 reference on page 16 is excluded. Lemmas and Corollary 1 are not inventoried.',
        'All six full statements visually reviewed on PDF pages 9–13 and 16–17; Theorem 3 includes both bullet items across pages 11 and 12.',
        'Theorem 1 preserves the nested union and alpha-minus-nu coverage. Theorem 2 preserves its specific acceptance region, Assumptions 1–2, and the minimum with the full-family alpha correction.',
        'Theorem 3 retains factors 4 and 2 and both minima; Theorem 4 retains marginal confidence-region monotonicity, w at level nu/m, and the random-cardinality Bonferroni correction without adding a minimum.',
        'Theorem 5 is the exact model-enumeration identity as printed, not the separate inferential coverage consequence in Corollary 1.',
        'Theorem 6 preserves absolute boundedness by 1, calligraphic dataset D and hypothesis class F, both factors 4, and square-root 2/n logarithm constants. Gap_n is an upper-bound functional, not automatically Rademacher complexity.',
        'Appendix boundary header visually checked without reading its mathematics; substantive main text ends on page 25 and references end on page 27.',
        'The local PDF title and two authors match the corpus; arXiv v6 date is 2 May 2024 although the title-page date reads 05.03.24. Exact published-version equivalence is not asserted.',
        'Interface extraction, prerequisite closure and final independent census audit remain pending.'
    ]
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (ROOT/'inventory-review.json').write_text(json.dumps(dict(paper_id=PID,status='complete',source_checked=True,inventory_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),reviewed_at=now,method='Independent bold-font heading enumeration and visual comparison of all six complete statements.',theorem_ids=[c['claim_id'] for c in claims],notes=notes),indent=2)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=now,next_action='Extract and review main-text prerequisites of Theorems 1–6. Keep general, parametric, bounded-data, LASSO and risk settings distinct; preserve unresolved appendix subroutines and source assumptions.'),indent=2)+'\n')
    print('Saved and validated six source-checked main-text Theorems.')
