"""Save every main-text Theorem in the pinned dynamic-volatility preprint."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i03-p1027', 'title': 'High-dimensional covariance matrices under dynamic volatility models: Asymptotics and shrinkage estimation', 'version': 'arXiv:2211.10203v2', 'source_url': 'https://arxiv.org/pdf/2211.10203v2', 'pdf_pages': 49, 'pdf_sha256': 'dd4e1b59134c24ecec0c5ab2e4adfa80e1388296f732747ba2c4a4977d67982f'};claims=[]
def claim(n,page,text):claims.append(dict(claim_id=PID+'/T'+str(n),paper_id=PID,claim_kind='theorem',label='Theorem '+str(n),source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=page,location='Theorem '+str(n))]))
claim(1,7,r'''
Under model (1.1) and Assumption 1, if $\eta(a_p,b_p,p)\to0$ as $p\to\infty$, then
\[
L(F^{\mathbf S_n},F^{\mathbf S_n^0})=o_p(1).\tag{2.2}
\]
''')
claim(2,8,r'''
Under model (1.1) and Assumption 1, if $\eta(a_p,b_p,p)>c$ for some constant $c>0$, then there exists $\delta>0$ such that for all $p$ large enough,
\[
E(M_2^p)\ge E(M_2^{0,p})+\delta.\tag{2.3}
\]
''')
claim(3,10,r'''
Under model (1.1) and Assumption 1, if, in addition, $\delta<\min(a_p,b_p)<a_p+b_p<1-\delta$ for some $\delta>0$, and $M_p$ satisfies that $M_p\to\infty$ and $M_p=o(\sqrt p)$, then
\[
L(F^{\widetilde{\mathbf S}_n},F^{\mathbf S_n^0})=o_p(1).\tag{2.7}
\]
''')
claim(4,12,r'''
Under model (1.1) and Assumption 1, if, in addition, $\delta<\min(a_p,b_p)<a_p+b_p<1-\delta$ for some $\delta>0$, $M_p\to\infty$, $M_p=o(\sqrt p)$, the limiting distribution $H$ is supported by $[h_1,h_2]$ for some constants $0<h_1\le h_2<\infty$, and $g$ is a bounded function on $[h_1,h_2]$ with finitely many points of discontinuity, then,
\[
\Theta_n^g(z)-\Theta^g(z)=o_p(1),\qquad\text{for all }z\in\mathbb C^+,
\]
where
\[
\Theta^g(z)=\int_{-\infty}^{+\infty}\left(\tau\left(1-y^{-1}-y^{-1}zm_F(z)\right)-z\right)^{-1}g(\tau)\,dH(\tau).\tag{2.12}
\]
''')
claim(5,13,r'''
Under the assumptions of Theorem 4,
\[
\frac1{\sqrt p}\|\widetilde{\boldsymbol\Sigma}-\widetilde{\boldsymbol\Sigma}^{or}\|_F=o_p(1).
\]
''')
def main():
    repo=Path(__file__).resolve().parents[5]
    source=Path(subprocess.check_output([sys.executable,str(repo/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=36,main_text_boundary=dict(location='Numbered main-text Section 5 ends on page 32. The Supplement Materials notice on pages 32–33 describes the attached supplement; references continue through page 36. The actual supplement starts with its own title on page 37, and pages 37–49 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    pdf=fitz.open(source);assert len(pdf)==49 and hashlib.sha256(source.read_bytes()).hexdigest()==paper['pdf_sha256']
    first=pdf[0].get_text();assert '2211.10203v2' in first and '21 Nov 2022' in first and 'November 18, 2022' in first
    labels=[];mentions=[]
    for n in range(36):
        page=pdf[n]
        for b in page.get_text('dict')['blocks']:
            for line in b.get('lines',[]):
                text=''.join(s['text'] for s in line['spans']).strip();m=re.match(r'Theorem (\d+)(?=[.\s(])',text)
                if m:
                    if line['spans'][0]['font']=='SFBX1200':labels.append((n+1,int(m.group(1))))
                    else:mentions.append((n+1,text))
    assert labels==[(7,1),(8,2),(10,3),(12,4),(13,5)],labels
    assert [p for p,s in mentions]==[7,8,10,13]
    assert 'Zheng' in pdf[35].get_text() and 'Supplement to' in pdf[36].get_text(clip=fitz.Rect(0,0,pdf[36].rect.width,143))
    for c in claims:
        for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
            depth=0
            for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
                depth+=1 if b=='{' else -1
                assert depth>=0,c['claim_id']
            assert depth==0,c['claim_id']
    path=ROOT/'theorem-inventory.json';path.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)

if __name__ == "__main__":
    main()
