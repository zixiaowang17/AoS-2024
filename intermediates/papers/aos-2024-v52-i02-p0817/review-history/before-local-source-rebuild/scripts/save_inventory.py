"""Save every main-text Theorem in the pinned online-closure preprint."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
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
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=16,main_text_boundary=dict(location='Main discussion ends on PDF page 16. The Appendix heading begins on page 17; pages 17-21 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);labels=[]
assert len(pdf)==21 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
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
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=4,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),printed_heading_check=labels,notes=[
 'Pinned arXiv:2211.11400v3. The margin is stamped 21 December 2023 and the title page is dated 22 December 2023; both dates are preserved in provenance. Main text ends on page 16, before the Appendix on page 17.',
 'Independent bold-heading enumeration over pages 1-16 finds exactly Theorems 3.2,3.5,3.9,4.2. Plain-text references, proof headings, Lemmas, Propositions and Corollaries are excluded.',
 'All four statements were visually checked on pages 3,4,6,8. Theorem 3.2 retains its arbitrary-family FWER assertion separately from the additional predictable-online assertion.',
 'Theorem 3.5 retains the maximum over every subset I and the exact equality of decision sequences; the standing empty-set convention still needs to be attached as source context.',
 'Theorem 3.9 retains the recursive index set and both decision procedures. Theorem 4.2 retains its threshold-based recursion and all three equivalent procedures, including the instantiated threshold alpha_i^{I_i}.',
 'Only the theorem inventory is complete. Resolve the experiment/filtration, online decisions, strong FWER, online level tests, predictability, closure, consonance, online sub-alpha adjustments and equation (3). Preserve any measurability issue with an uncountable family separately; no appendix proof is read.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,3,4,6,8,16]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
shutil.copy2(work/'appendix-heading-only.png',ROOT/'evidence/appendix-heading-only.png')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve the experiment/filtration, Definitions 2.1 and 3.1, FWER, level intersection tests, closure, consonance (2), online alpha/sub-alpha adjustments, Definition 4.1 and equation (3). Check the arbitrary-family measurability and empty-set conventions. Exclude pages 17-21; then finalize and independently audit.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated four complete main-text Theorems.')
