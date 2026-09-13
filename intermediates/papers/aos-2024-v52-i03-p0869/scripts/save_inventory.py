"""Transcribe every actual main-text Theorem in the pinned v2 preprint."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i03-p0869', 'title': 'Dimension-free mixing times of Gibbs samplers for Bayesian hierarchical models', 'version': 'arXiv:2304.06993v2', 'source_url': 'https://arxiv.org/pdf/2304.06993v2', 'pdf_pages': 80, 'pdf_sha256': 'b3974fe0fcf4eb356e80cc84d4f37c2d08f8a3c91ebe97c46ef0c098a1b036e1'};claims=[]
def claim(n,pages,text,title=None):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+(' ('+title+')' if title else ''),source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+n) for p in pages]))
claim('2.4',[7],r'''
Let assumption (A1) holds. Then for every $t\in\mathbb N$ and $M\geq1$ it holds
\[
\lim_{n\to\infty}\sup_{\mu_n\in\mathcal N(\pi_n,M)}\|\mu_nP_n^t-\pi_n\|_{TV}
=\sup_{\widetilde\mu\in\mathcal N(\widetilde\pi,M)}\|\widetilde\mu\widetilde P^t-\widetilde\pi\|_{TV},
\]
in $Q^{(n)}$-probability.
''')
claim('3.1',[9],r'''
Consider model (11) and let the map $\psi\to f(\cdot\mid\psi)$ be one-to-one. Let the map $\psi\to\sqrt{f(y\mid\psi)}$ be continously differentiable for every $y\in\mathcal Y$, with non-singular and continuous Fisher Information $\mathcal I(\psi)$. Let the prior measure be absolutely continuous in a neighborhood of $\psi^*\in\mathcal X$ with a continuous positive density at $\psi^*$. Finally, let $\Psi$ be a compact neighborhood of $\psi^*$ for which there exists a sequence of tests $u_n$ such that
\[
\int_{\mathcal Y^{(n)}}u_n(y_1,\ldots,y_n)\prod_{i=1}^n f(dy_i\mid\psi^*)\to0,
\]
\[
\sup_{\psi\notin\Psi}\int_{\mathcal Y^{(n)}}[1-u_n(y_1,\ldots,y_n)]\prod_{i=1}^n f(dy_i\mid\psi)\to0,\qquad\text{as }n\to\infty.\tag{12}
\]
Then, if $Y_i\overset{\mathrm{iid}}\sim Q_{\psi^*}$ for $i=1,2,\ldots$ with $Q_{\psi^*}$ admitting density $f(y\mid\psi^*)$, it holds
\[
\|\mathcal L(d\widetilde\psi\mid Y^{(n)})-N(\mathcal I^{-1}(\psi^*)\Delta_{n,\psi^*},\mathcal I^{-1}(\psi^*))\|_{TV}\to0,\qquad\text{as }n\to\infty
\]
in $Q_{\psi^*}^{(\infty)}$-probability, where $\widetilde\psi=\sqrt n(\psi-\psi^*)$ and $\Delta_{n,\psi^*}=\left.\frac1{\sqrt n}\sum_{i=1}^n\nabla\log f(Y_i\mid\psi)\right|_{\psi=\psi^*}$.
''','Bernstein-von Mises')
claim('4.2',[12],r'''
Consider model (13) and the Gibbs sampler defined as in (15), with mixing times $t_{mix}^{(J)}(\epsilon,M)$. Then, under assumptions (B1)-(B6), for every $(M,\epsilon)\in[1,\infty)\times(0,1)$ there exists $T(\psi^*,\epsilon,M)<\infty$ such that
\[
Q_{\psi^*}^{(J)}(t_{mix}^{(J)}(\epsilon,M)\leq T(\psi^*,\epsilon,M))\to1,
\]
as $J\to\infty$. It follows that $t_{mix}^{(J)}(\epsilon,M)=\mathcal O_P(1)$ as $J\to\infty$.
''')
claim('6.1',[22],r'''
Consider the same setting of Theorem 4.2 and let $\mu_J\in\mathcal P(\mathbb R^{lJ+D})$ as in (35). Then, for every $\epsilon\in(0,1)$ there exists $T(\psi^*,\epsilon,c)<\infty$ such that
\[
\liminf_{J\to\infty}Q_{\psi^*}^{(J)}(t_{mix}^{(J)}(\epsilon,\mu_J)\leq T(\psi^*,\epsilon,c))\to1\qquad\text{as }J\to\infty.
\]
''')
def main():
    repo=Path(__file__).resolve().parents[5]
    source=Path(subprocess.check_output([sys.executable,str(repo/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=27,main_text_boundary=dict(location='Main text and references end on PDF page 27. Appendix A begins on PDF page 28; only its heading was inspected. All appendix mathematics on pages 28-80 is excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    pdf=fitz.open(source);labels=[];references=[]
    assert len(pdf)==80 and hashlib.sha256(source.read_bytes()).hexdigest()==paper['pdf_sha256']
    first=pdf[0].get_text();assert '2304.06993v2' in first and '30 Oct 2023' in first and 'October 31, 2023' in first
    for n in range(27):
        for block in pdf[n].get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(span['text'] for span in line['spans']).strip();match=re.match(r'Theorem (\d+(?:\.\d+)*)(?=[.\s(])',text)
                if match:
                    if line['spans'][0]['font']=='CMBX10':labels.append((n+1,match.group(1)))
                    else:references.append((n+1,text))
    assert labels==[(7,'2.4'),(9,'3.1'),(12,'4.2'),(22,'6.1')],labels
    assert len(references)==1 and references[0][0]==18
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in claims]==labels
    assert 'Dimension-' in pdf[26].get_text()
    assert pdf[27].get_text(clip=fitz.Rect(0,0,pdf[27].rect.width,95)).startswith('Appendix A')
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
