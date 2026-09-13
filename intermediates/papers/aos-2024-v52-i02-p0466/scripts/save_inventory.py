"""Preserve all three main-text Theorems, including the page-spanning Theorem 4."""
import hashlib,json,re,subprocess,sys,shutil
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i02-p0466', 'title': 'Convergence rates of oblique regression trees for flexible function libraries', 'version': 'arXiv:2210.14429v2', 'source_url': 'https://arxiv.org/pdf/2210.14429v2', 'pdf_pages': 36, 'pdf_sha256': 'f181fed44b89ff76e53bfdaccff54d908541d44d53ad60170c0f432d9a05fc85'}
claims=[]
def claim(n,pages,body,title=None):claims.append(dict(claim_id=PID+'/T'+str(n),paper_id=PID,claim_kind='theorem',label='Theorem '+str(n)+((' ('+title+')') if title else ''),source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+str(n)+(' — continuation' if j else '')) for j,p in enumerate(pages)]))
claim(1,[12],r'''
Let Assumption 2 hold. Then, for any $K\geq1$,
\[
\mathbb E[\|\mu-\widehat\mu(T_K)\|^2]\leq2\inf_{f\in\mathcal F}\left\{\|\mu-f\|^2+\frac{\|f\|_{\mathcal L_1}^2\mathbb E[\max_{t\in[T_K]}P_{\mathcal A_t}^{-1}(\kappa)]}{\kappa K}+C\frac{2^Kd\log(np/d)\log^{4/\gamma}(n)}n\right\},\tag{10}
\]
where $C=C(c_1,c_2,\gamma,M)$ is a positive constant. Furthermore, if the penalty coefficient satisfies $\lambda_n\gtrsim(d/n)\log(np/d)\log^{4/\gamma}(n)$, then
\[
\mathbb E[\|\mu-\widehat\mu(T_{opt})\|^2]\leq2\inf_{K\geq1,\,f\in\mathcal F}\left\{\|\mu-f\|^2+\frac{\|f\|_{\mathcal L_1}^2\mathbb E[\max_{t\in[T_K]}P_{\mathcal A_t}^{-1}(\kappa)]}{\kappa K}+C\frac{2^Kd\log(np/d)\log^{4/\gamma}(n)}n\right\}.\tag{11}
\]
''','Oracle inequality for oblique trees')
claim(4,[15,16],r'''
Let $d=p$, $\kappa=1$, and $P_{\mathcal A_t}(\kappa)=1$, and let Assumptions 2, 3, and 4 hold. Then, for any $K\geq1$,
\[
\mathbb E[\|\mu-\widehat\mu(T_K)\|^2]\leq\frac{2AV^2}{4^{(K-1)/q}}+C\frac{2^{K+1}p\log^{4/\gamma+1}(n)}n,\tag{14}
\]
where $C=C(c_1,c_2,\gamma,M)$ is a positive constant. Furthermore, if the penalty coefficient satisfies $\lambda_n\gtrsim(p/n)\log^{4/\gamma+1}(n)$, then
\[
\mathbb E[\|\mu-\widehat\mu(T_{opt})\|^2]\leq2(2+q)\left(\frac{AV^2}q\right)^{q/(2+q)}\left(\frac{Cp\log^{4/\gamma+1}(n)}n\right)^{2/(2+q)}.\tag{15}
\]
''')
claim(5,[17],r'''
Suppose Assumptions 2 holds. Let $\widehat\mu(\boldsymbol\Theta)$ be the output of the oblique random forest constructed with oblique trees of depth $K$. Then,
\[
\mathbb E[\|\mu-\widehat\mu(\boldsymbol\Theta)\|^2]\leq2\inf_{f\in\mathcal F}\left\{\|\mu-f\|^2+\frac{\|f\|_{\mathcal L_1}^2\mathbb E[\max_{t\in[T_K]}P_{\mathcal A_t}^{-1}(\kappa)]}{\kappa K}+C\frac{2^Kd\log(Np/d)\log^{4/\gamma}(N)}N\right\},
\]
where $C$ is some positive constant and $N$ is the subsample size.
''','Oracle inequality for oblique forests')
def main():
    repo = Path(__file__).resolve().parents[5]
    source = Path(subprocess.check_output([sys.executable, str(repo/'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest() == prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=18,main_text_boundary=dict(location='Section 5.2 (Classification) ends on PDF page 18 above the heading A Proofs at y=422.38 points. The main-text clip ends at y=421. All content below that heading and pages 19-36 is excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    for c in claims:
     for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
      depth=0
      for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
       depth+=1 if b=='{' else -1
       assert depth>=0,c['claim_id']
      assert depth==0,c['claim_id']
    p=ROOT/'theorem-inventory.json';p.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(p)],check=True)

if __name__ == '__main__':
    main()
