"""Save every main-text Theorem in the pinned online-closure preprint."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov={'paper_id': 'aos-2024-v52-i02-p0817', 'title': 'The online closure principle', 'version': 'arXiv:2211.11400v3', 'source_url': 'https://arxiv.org/pdf/2211.11400v3', 'pdf_pages': 21, 'pdf_sha256': '48a80ff70f762df42f933aa06b58278e6d061eaba9fb26c2f26eb77af5d1b316'};claims=[]
def claim(n,pages,text,title=None):claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+(' ('+title+')' if title else ''),source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+n) for p in pages]))
claim('3.2',[3],r'''
Let $\boldsymbol\phi=(\phi_I)_{I\subseteq\mathbb N}$ be an arbitrary family of $\alpha$-level intersection tests. Then, the closed procedure $\boldsymbol d^\phi=(d_i^\phi)_{i\in\mathbb N}$ based on $\boldsymbol\phi$ defined by
\[
d_i^\phi=\min\{\phi_I:I\subseteq\mathbb N\text{ with }i\in I\}
\]
controls the FWER at level $\alpha$ in the strong sense. In addition, if each $\phi_I$ is an online intersection test and the family of online intersection tests $\boldsymbol\phi$ is predictable, then $\boldsymbol d^\phi$ is an online procedure. We refer to such procedures as online closed procedures.
''','Online closure principle')
claim('3.5',[4],r'''
Let $\boldsymbol d=(d_i)_{i\in\mathbb N}$ be an online procedure with strong FWER control. Then $\boldsymbol\phi=(\phi_I)_{I\subseteq\mathbb N}$, where $\phi_I=\max\{d_i:i\in I\}$, is a predictable family of online $\alpha$-level intersection tests and $\boldsymbol d^\phi=\boldsymbol d$. Thus, for any online procedure $\boldsymbol d$ with FWER control there exists an online closed procedure $\boldsymbol d^\phi$ that leads to the same decisions.
''')
claim('3.9',[6],r'''
Assume $\boldsymbol\phi=(\phi_I)_{I\subseteq\mathbb N}$ is a predictable family of online $\alpha$-level intersection tests with the consonance property. Let us recursively define $I_1=\{1\}$ and $I_i=\{j\in\mathbb N:j<i,\phi_{I_j}=0\}\cup\{i\}$ for all $i\geq2$. Then the following procedures lead to the same decisions:

1. The online closed procedure $\boldsymbol d^\phi$.
2. The short-cut $\boldsymbol d^{\phi,s}=(d_i^{\phi,s})_{i\in\mathbb N}$, where $d_i^{\phi,s}=\phi_{I_i}$ for all $i\in\mathbb N$.
''')
claim('4.2',[8],r'''
Assume $(\boldsymbol\alpha_I)_{I\subseteq\mathbb N}$, where $\boldsymbol\alpha_I=(\alpha_i^I)_{i\in I}$, is a predictable family of online sub $\alpha$-adjustments such that $\boldsymbol\phi=(\phi_I)_{I\subseteq\mathbb N}$ defined by (3) is a family of $\alpha$-level intersection tests with the consonance property. Let us recursively define $I_1=\{1\}$ and $I_i=\{j\in\mathbb N:j<i,p_j>\alpha_j^{I_j}\}\cup\{i\}$ for all $i\geq2$. Then the following three procedures lead to the same decisions:

1. The online closed procedure $\boldsymbol d^\phi$.
2. The short-cut $\boldsymbol d^{\phi,s}=(d_i^{\phi,s})_{i\in\mathbb N}$, where $d_i^{\phi,s}=\phi_{I_i}$ for all $i\in\mathbb N$.
3. The online $\alpha$-adjustment procedure $\boldsymbol d=(d_i)_{i\in\mathbb N}$, where $d_i=\mathbb 1\{p_i\leq\alpha_i^{I_i}\}$ for all $i\in\mathbb N$.
''')
def main():
    repo=Path(__file__).resolve().parents[5]
    source=Path(subprocess.check_output([sys.executable,str(repo/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==prov['pdf_sha256']
    paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
    paper.update(main_text_last_pdf_page=16,main_text_boundary=dict(location='Main discussion ends on PDF page 16. The Appendix heading begins on page 17; pages 17-21 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
    pdf=fitz.open(source);labels=[]
    assert len(pdf)==21 and hashlib.sha256(source.read_bytes()).hexdigest()==paper['pdf_sha256']
    assert '2211.11400v3' in pdf[0].get_text() and '21 Dec 2023' in pdf[0].get_text() and 'December 22, 2023' in pdf[0].get_text()
    for n in range(16):
        for block in pdf[n].get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(span['text'] for span in line['spans']).strip();match=re.match(r'Theorem (\d+(?:\.\d+)*)(?=[.\s(])',text)
                if match and line['spans'][0]['font']=='NimbusRomNo9L-Medi':labels.append((n+1,match.group(1)))
    assert labels==[(3,'3.2'),(4,'3.5'),(6,'3.9'),(8,'4.2')],labels
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
