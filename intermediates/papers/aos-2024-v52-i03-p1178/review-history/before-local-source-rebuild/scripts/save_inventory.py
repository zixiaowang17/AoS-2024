"""Preserve both original main-text Theorems in arXiv:2305.11672v2."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
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

if __name__=='__main__':
    pdf=fitz.open(prov['cached_pdf']);assert len(pdf)==73
    assert hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==prov['pdf_sha256']
    first=' '.join(pdf[0].get_text().split());assert prov['title'].upper() in first
    for name in prov['authors']:assert name.upper() in first
    assert 'Submitted to the Annals of Statistics' in first
    labels=[];mentions=[]
    for n in range(1,23):
        page=pdf[n-1];assert (ROOT/'evidence'/f'page-{n:02}.txt').read_bytes().decode('utf8')==page.get_text()
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
    for n in [9,12]:shutil.copyfile(Path(prov['working_pdf']).parent/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    notes=[
     'Pinned arXiv v2 dated 2 May 2024; PDF title and all three authors match the corpus article, and the cached hash agrees with the earlier independent acquisition record. Exact final-journal equivalence is not asserted.',
     'The main text occupies PDF 1–22, ending with funding. Section S1 starts on PDF 23; all supplementary mathematics is excluded. Main-text Section 5 proof overview was inspected for Theorem headings, not automatically excluded because it contains proofs.',
     'Independent small-caps THEOREM heading enumeration identifies exactly Theorems 1 and 2 on pages 9 and 12. Three ordinary-font line-leading references are excluded; both full statements fit on single pages.',
     'Theorem 1 retains the full constant restrictions, maximum/minimum parameter inequalities, rate R and both sides of the conditional minimax bound, including the unavailable-pattern indicator. Its c_E range includes zero and C_L is strictly greater than one.',
     'Theorem 2 retains its positive c_E, C_L>=1, availability restriction, tail/smoothness restriction, exact logarithmic sample-size condition on U(Omega_star) intersect N, and the uniform HAM risk bound. The stronger constant and margin restrictions from Theorem 1 are not imported.',
     'Bold beta/gamma vectors and the bold zero vector are verified by PDF font spans; scalar pattern-indexed beta_omega/gamma_omega remain unbolded. O,I,N,C,Q and the excess-risk E use script notation; U is plain.',
     'Theorem 1 uses Q-prime-Miss while Theorem 2 uses Q-plus-Miss. Expectations are conditional on the entire observed missingness pattern sequence. The upper-bound unavailable-pattern indicator lies outside the constant-times-rate term.',
     'The sample-size logarithm in Theorem 2 has no plus subscript; both risk bounds use log-plus to power (1+alpha)/2. The exact rate denominator is gamma_omega(2 beta_omega+d_omega)+alpha beta_omega.',
     'Main-text definitions, all statement prerequisites, source highlights and final independent census audit remain to be completed.'
    ]
    (ROOT/'inventory-review.json').write_text(json.dumps(dict(paper_id=PID,status='complete',source_checked=True,inventory_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='Independent small-caps heading enumeration of PDF 1–22 and visual review of both full original Theorems, including math-font checks.',theorem_ids=[c['claim_id'] for c in claims],notes=notes),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),next_action='Read main-text definitions and Algorithm1; extract all prerequisites of Theorems1–2, preserving Q-prime versus Q-plus classes, missingness conditioning, ANOVA interactions, antichains, tail/smoothness/margin classes and HAM construction. Resolve empty maxima and log-plus conventions from main text. Do not read supplementary SectionsS1–S5.'),indent=2)+'\n')
    print('Saved and independently validated both original main-text Theorems.')
