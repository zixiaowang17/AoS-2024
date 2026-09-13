"""Save every complete original main-paper Theorem before interface extraction."""
import datetime,fitz,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i02-p0679', 'title': 'Finding the optimal dynamic treatment regimes using smooth Fisher consistent surrogate loss', 'version': 'arXiv:2111.02826v4', 'source_url': 'https://arxiv.org/pdf/2111.02826v4', 'pdf_pages': 50, 'pdf_sha256': '2b00e8abb4878ad695f61c97a5316989a63b5853482e811c95e473a899c186d7'}
claims=[]
def claim(n,pages,body,title=None):
    label='Theorem '+str(n)+((' ('+title+')') if title else '')
    claims.append(dict(claim_id=PID+'/T'+str(n),paper_id=PID,claim_kind='theorem',label=label,source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+str(n)+(' — continuation' if i else '')) for i,p in enumerate(pages)]))
claim(1,[12],r'''
Suppose $\psi$ is closed, strictly concave, and bounded above. In addition, $\psi$ has continuous second order partial derivatives and $\psi_{12}$ has continuous partial derivatives on $\operatorname{int}(\operatorname{dom}(\psi))$. Then $\psi$ can not be Fisher consistent for two stage DTR.
''')
claim(2,[15],r'''
Suppose $\psi(x,y)=\min(x,y,1)$. Further, suppose Assumptions I-IV hold and $Y_1$ and $Y_2$ are bounded below by some positive constant.

- First stage: If (13) holds for some $h_1\in\mathcal H_1$, then $\widetilde d_1(h_1)=d_1^*(h_1)$. If (13) does not hold, then $\widetilde d_1(H_1)=\{1,-1\}$.
- Second stage: If $h_2\equiv(h_1,a_1,y_1,o_2)\in\mathcal H_2$ is such that $a_1$ and $h_1$ satisfy $a_1=\widetilde d_1(h_1)$, then $\widetilde d_2(h_2)=d_2^*(h_2)$. For all other $h_2$, $\widetilde d_2(h_2)=\{-1,1\}$.
''',r'$\widetilde d_1$ and $\widetilde d_2$ for hinge loss')
claim(3,[18],r'''
Suppose $Y_1,Y_2>0$ and Assumptions I-IV hold. Let $\psi(x,y)=\phi(x)\phi(y)$ with $\phi$ satisfying Condition 2 with some $C_\phi>0$. Then
\[
V^*-V(f_1,f_2)\leq\frac{\big(V_\psi^*-V_\psi(f_1,f_2)\big)}{(C_\phi/2)^2}.\tag{15}
\]
''')
claim(4,[23,24],r'''
Suppose $\mathbb P$ satisfies Assumptions I-IV, Assumption A and Assumption B with small noise coefficient $\alpha$. Let $0<a_n\to\infty$ be any sequence of positive reals. Further suppose there exist a small number $\delta_n\in(0,1)$ and maps $\widetilde h_{n,1}:\mathcal H_1\mapsto\mathbb R$ and $\widetilde h_{n,2}:\mathcal H_2\times\{0,1\}\mapsto\mathbb R$ so that
\[
\|\widetilde h_{n,1}-(\eta_1-1/2)\|_\infty+\|\widetilde h_{n,2}-(\eta_2-1/2)\|_\infty\leq\delta_n
\]
where $\eta_1$ and $\eta_2$ are defined in (9) and (10). Then for any $\phi$ of type A, the following holds for any $\alpha'\in(0,\alpha)$ satisfying $\alpha-\alpha'<1$:
\[
V_\psi^*-V_\psi(a_n\widetilde h_{n,1},a_n\widetilde h_{n,2})
\lesssim\begin{cases}
a_n^{1-\kappa}+\min(\delta_n^{2+\alpha}a_n,\delta_n^{1+\alpha})&\text{if }\kappa<2+\alpha,\\
\dfrac{a_n^{-\frac{1+\alpha}{1+(\alpha-\alpha')/(\kappa-1)}}}{\alpha-\alpha'}+\min(\delta_n^{2+\alpha}a_n,\delta_n^{1+\alpha})+\dfrac{\delta_n^{\alpha'+2-\kappa}}{(\alpha-\alpha')a_n^{\kappa-1}}&\text{if }\kappa\geq2+\alpha.
\end{cases}
\]
Suppose $\phi$ is of type B. Then
\[
V_\psi^*-V_\psi(a_n\widetilde h_{n,1},a_n\widetilde h_{n,2})\lesssim\frac{(\log a_n)^{1+\alpha}}{a_n^{1+\alpha}}+\min(a_n\delta_n^{2+\alpha},\delta_n^{1+\alpha})+a_n\delta_n\exp(-\kappa a_n\delta_n/2).
\]
''')
claim(5,[26],r'''
Suppose $\mathcal U_n$ is such that there exists $A_n>0$ and $\rho_n\in\mathbb R$ so that (21) holds with $\liminf_n\rho_n>0$, $\rho_n\log A_n=o(n)$, and $\liminf_n\rho_n\log A_n>0$. Further suppose there exist $(\widetilde f_{n,1},\widetilde f_{n,2})\in\mathcal U_n$ so that
\[
\|\widetilde f_{n,1}/a_n-(\eta_1-1/2)\|_\infty+\|\widetilde f_{n,2}/a_n-(\eta_2-1/2)\|_\infty\leq\left(\frac{\rho_n\log A_n}{n}\right)^{1/(2+\alpha)}\tag{22}
\]
for some $a_n=n^a$ where $a>1$. We also assume that $\mathbb P$ satisfies Assumptions I-IV, Assumption A, and Assumption B with coefficient $\alpha>0$. Then there exist $C>0$ and $N_0\geq1$ such that for all $n\geq N_0$ and all $x>0$,
\[
V_\psi^*-V_\psi(\widehat f_{n,1},\widehat f_{n,2})\leq C\max\left\{(1+x)^2(\log n)^2\left(\frac{\rho_n\log A_n}{n}\right)^{\frac{1+\alpha}{2+\alpha}},\mathit{Opt}_n\right\}
\]
with probability at least $1-\exp(-x)$.
''')
claim(6,[26],r'''
Suppose the function-class $\mathcal U_n$ is such that (23) holds with $\rho_n\in(0,1)$, $A_n>1$, where it also holds that $A_n^{2\rho_n}/n\to0$. Further suppose the approximation error
\[
V_\psi^*-\sup_{(f_1,f_2)\in\mathcal U_n}V_\psi(f_1,f_2)=O((\log n)^k/n)
\]
for some $k\in\mathbb N$, the optimization error $\mathit{Opt}_n<1/2$, and Assumptions I-IV, A, and C hold. Then there exist $C>0$ and $N_0>0$ such that for all $n\geq N_0$ and for any $x>0$,
\[
V_\psi^*-V_\psi(\widehat f_{n,1},\widehat f_{n,2})\leq C\max\left\{(1+x)^{2/(1+\rho_n)}A_n^{2\rho_n/(1+\rho_n)}n^{-1/(1+\rho_n)},\mathit{Opt}_n\right\}
\]
with probability at least $1-\exp(-x)$.
''')
claim(7,[27],r'''
Suppose $\mathcal U_n$ is a function-class such that there exist $A_n>0$ and $\rho_n>0$ so that
\[
N_{[\ ]}(\epsilon,\mathcal U_n,L_2(\mathbb P_n))\lesssim\left(\frac{A_n}{\epsilon}\right)^{\rho_n},\tag{24}
\]
and $\liminf_n(\rho_n\log A_n)>0$. Further, suppose the approximation error
\[
V_\psi^*-\sup_{(f_1,f_2)\in\mathcal U_n}V_\psi(f_1,f_2)=O((\log n)^k/n)\tag{25}
\]
for some $k\in\mathbb N$. Then under Assumptions I-IV, A, and C, there exist $C>0$ and $N_0>0$ such that for all $n>N_0$ and any $x>0$,
\[
V_\psi^*-V_\psi(\widehat f_{n,1},\widehat f_{n,2})\leq C\max\left\{\frac{(1+x)^2(\log n)^2(\rho_n\log A_n)^2+(\log n)^k}{n},\mathit{Opt}_n\right\}
\]
with $\mathbb P$-probability at least $1-\exp(-x)$.
''')
def main():
    repo=Path(__file__).resolve().parents[5]
    source=Path(subprocess.check_output([sys.executable,str(repo/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=50,main_text_boundary=dict(location='All 50 PDF pages belong to the main paper. Discussion and acknowledgments end on page 42; page 43 contains a notice linking to a separate supplement, followed by references. Main-paper figure floats continue through Figure 5 on page 50. No appendix or supplement body is embedded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    pdf=fitz.open(source);labels=[]
    assert len(pdf)==50 and hashlib.sha256(source.read_bytes()).hexdigest()==paper['pdf_sha256']
    assert '2111.02826v4' in pdf[0].get_text() and '1 Oct 2023' in pdf[0].get_text()
    for n in range(50):
        for block in pdf[n].get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                spans=line['spans'];text=''.join(span['text'] for span in spans).strip()
                if spans and spans[0]['font']=='CMBX10' and text.startswith('Theorem '):
                    match=re.match(r'Theorem (\d+)(?:\.| \()',text)
                    assert match,(n+1,text)
                    labels.append((n+1,match.group(1)))
    assert labels==[(12,'1'),(15,'2'),(18,'3'),(23,'4'),(26,'5'),(26,'6'),(27,'7')],labels
    assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in claims]==labels
    assert 'Due to the size of the Supplement' in pdf[42].get_text()
    assert 'References' in pdf[42].get_text() and 'Fig 5:' in pdf[49].get_text()
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
