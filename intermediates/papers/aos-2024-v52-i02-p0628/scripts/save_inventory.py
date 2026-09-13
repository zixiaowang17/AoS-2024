"""Save every main-text Theorem before resolving its statement dependencies."""
import datetime,fitz,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i02-p0628', 'title': 'Testing for practically significant dependencies in high dimensions via bootstrapping maxima of U-statistics', 'version': 'arXiv:2210.17439v2', 'source_url': 'https://arxiv.org/pdf/2210.17439v2', 'pdf_pages': 66, 'pdf_sha256': '6985f30f69767e8e75d30899bfe10303542404a0e3720f8f55ae1367c3aee7cc'}
claims=[]
def claim(n,pages,body):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+n) for p in pages]))
claim('2.2',[8],r'''
If Assumptions (A1), (A2), (A3) are satisfied, $\log d=o(n^\gamma)$ with $0\leq\gamma\leq\frac1{2/\beta+1}$ and
\[
\frac{B_n^2\big(\log(nd)\big)^{4+2/\beta}}n=o(1),\quad n\to\infty,\tag{2.16}
\]
then, for any $\alpha\in(0,1-e^{-1})$,
\[
\limsup_{n\to\infty}\sup_{F\in\mathcal H_0(\Delta)}
\mathbb P\left(\mathcal T_{n,\Delta}>\frac{q_{1-\alpha}}{a_d}+b_d\right)\leq\alpha,\tag{2.17}
\]
with strict inequality, whenever $\limsup_{n\to\infty}|\{i\in\{1,\ldots,d\}:|\theta_i|=\Delta\}|/d<1$. Moreover,
\[
\lim_{n\to\infty}\sup_{F\in\mathcal H_0(\Delta)}
\mathbb P\left(\mathcal T_{n,\Delta}>\frac{q_{1-\alpha}}{a_d}+b_d\right)
=\begin{cases}
\alpha,&\text{if }|\theta_i|=\Delta\text{ for all }1\leq i\leq d,\\
0,&\text{if }\sup_{d\in\mathbb N}\max_{i=1}^d|\theta_i|<\Delta.
\end{cases}
\]
''')
claim('2.4',[9],r'''
If $\log d=o(n^\gamma)$ with $0\leq\gamma\leq\frac1{2/\beta+1}$, then there exists a constant $c>0$, only depending on $\gamma$ and $\beta$, such that
\[
\lim_{n\to\infty}\inf_{F\in\mathcal H_1(c)}
\mathbb P\left(\mathcal T_{n,\Delta}>\frac{q_{1-\alpha}}{a_d}+b_d\right)=1.
\]
''')
claim('2.5',[10],r'''
Let Assumptions (A1') and (A2) be satisfied, assume that $\log d=o(n^\gamma)$ with $0\leq\gamma\leq\frac1{2/\beta+1}$ and that
\[
\frac{B_n^2(\log(nd))^{5+2/\beta}}n+
\frac{B_n^3(\log(nd))^{1+2/\beta}}{\sqrt n}=o(1),\quad n\to\infty.\tag{2.24}
\]
(1) For any $\alpha\in(0,1)$ it follows that
\[
\limsup_{n\to\infty}\sup_{F\in\mathcal H_{0,\mathrm{boot}}(\Delta)}
\mathbb P\left(\mathcal T_{n,\Delta}>q_{1-\alpha}^*\right)\leq\alpha,\tag{2.25}
\]
where
\[
\mathcal H_{0,\mathrm{boot}}(\Delta):=\{F\in\mathcal F\mid\theta_F\in V_0;\ F\text{ satisfies Assumptions (A1'), (A2)}\}\tag{2.26}
\]
and $V_0$ is defined in (2.14).

(2) For a sufficiently large constant $c$, which only depends on $\gamma$ and $\beta$, it follows that
\[
\lim_{n\to\infty}\inf_{F\in\mathcal H_1(c(\log(nd))^{1/\beta})}
\mathbb P\left(\mathcal T_{n,\Delta}>q_{1-\alpha}^*\right)=1,\tag{2.27}
\]
where the set $\mathcal H_1(c)$ is defined in (2.18). Moreover, if the kernel $h$ in (2.3) is bounded, then the set $\mathcal H_1(c(\log(nd))^{1/\beta})$ in (2.27) can be replaced by $\mathcal H_1(c)$.
''')
claim('2.8',[12],r'''
Let the assumptions of Theorem 2.5 be satisfied.

(1) For any $\alpha\in(0,1)$ it follows that
\[
\limsup_{n\to\infty}\sup_{F\in\mathcal H_{0,\mathrm{boot}}(\Delta)}
\mathbb P\left(\mathcal T_{n,\Delta}^{\mathrm{abs}}>q_{1-\alpha}^{*,\mathrm{abs}}\right)\leq\alpha,
\]
where $\mathcal H_{0,\mathrm{boot}}(\Delta)$ is defined in defined in (2.26).

(2) For a sufficiently large constant $c$, which only depends on $\gamma$ and $\beta$, it follows that
\[
\lim_{n\to\infty}\inf_{F\in\mathcal H_1(c(\log(nd))^{1/\beta})}
\mathbb P\left(\mathcal T_{n,\Delta}^{\mathrm{abs}}>q_{1-\alpha}^{*,\mathrm{abs}}\right)=1,\tag{2.33}
\]
where the set $\mathcal H_1(c)$ is defined in (2.18). Moreover, if the kernel $h$ in (2.3) is bounded, then the set $\mathcal H_1(c(\log(nd))^{1/\beta})$ in (2.33) can be replaced by $\mathcal H_1(c)$.
''')
claim('3.5',[18],r'''
Assume that the dependence measure $d_{ij}$ in (2.4) is given by $d_{ij}=\operatorname{Cov}_F(X_{1i},X_{1j})$ and $d_{ii}=1$ $(i,j=1,\ldots,p)$; so we have $d=p(p-1)/2$. Further let $c_0,\alpha,\beta$ denote positive constants such that $c_0<1-\Delta$ and $\alpha+\beta<1$. If $\log(p)/n\to0$ and $\log(p)n/p^2\to0$, as $n\to\infty$, then we have for sufficiently large $n$ and $p$
\[
\inf_{T_\alpha\in\mathcal T_\alpha}\sup_{F\in\mathcal H_1(c_0)}
\mathbb P(T_\alpha\text{ does not reject }H_0)\geq1-\alpha-\beta.\tag{3.3}
\]
''')
def main():
    repo=Path(__file__).resolve().parents[5]
    source=Path(subprocess.check_output([sys.executable,str(repo/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=25,main_text_boundary=dict(location='Main Sections 1-4 and acknowledgements end on PDF page 25. Appendix A: Online supplement: proofs begins on a separate page 26. Only its heading region was used to establish the boundary; supplement bodies on pages 26-66 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    pdf=fitz.open(source);labels=[]
    assert len(pdf)==66 and hashlib.sha256(source.read_bytes()).hexdigest()==paper['pdf_sha256']
    for n in range(25):
        for block in pdf[n].get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(span['text'] for span in line['spans'])
                match=re.fullmatch(r'THEOREM (\d+\.\d+)\.',text.strip())
                if match:
                    assert all(span['font']=='NimbusRomNo9L-Regu' for span in line['spans'])
                    labels.append((n+1,match.group(1)))
    assert labels==[(8,'2.2'),(9,'2.4'),(10,'2.5'),(12,'2.8'),(18,'3.5')],labels
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
