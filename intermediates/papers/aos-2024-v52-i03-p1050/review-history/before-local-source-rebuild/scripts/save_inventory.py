"""Preserve every complete main-text Theorem in the pinned change-acceleration paper."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,pages,text):claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n,source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+n+(' — continuation' if j else '')) for j,p in enumerate(pages)]))
claim('3.1',[8],r'''
Assume the change-point model is Markovian as defined in (1), and consider the procedure $(\mathcal X_c^*,T_c^*)$ defined in (9), that solves the auxiliary optimization problem (6) for some $c>0$. Then there exists a function $b_c:\mathbb R^\kappa\to\mathbb R_+$ such that
\[
T_c^*=\inf\{t\ge0:\Gamma_t\ge b_c(\mathbb S_t)\}.
\]
In the special case of the memoryless model (i.e., $\kappa=0$), the function $b_c$ is a constant.
''')
claim('5.1',[12,13],r'''
Suppose that the response model satisfies condition (14) and that the change-point model satisfies condition (16). Let $\Xi_1$ and $\Xi_2$ be blocks of length $\ell_1$ and $\ell_2$, respectively. Then, for any $\epsilon>0$, $b_2\ge b_1>1$, and $d>1$, we have
\[
\mathsf E[\widetilde T]\le\mathcal U(b_1,b_2,d)(1+\epsilon)+\frac{(1+\epsilon)^2}{1-\eta(b_1,d)}\mathcal R,
\]
where $\eta(b_1,d)\equiv(b_1+d)/(d(1+b_1))$,
\[
\begin{aligned}
\mathcal U(b_1,b_2,d)\equiv{}&\left(\lambda(\Xi_1)+\frac{\log(b_2)}{\mathsf D(\Xi_2)}\right)+\frac{\eta(b_1,d)}{1-\eta(b_1,d)}\left(\widetilde\lambda(\Xi_1)+\frac{\log(b_2)}{\mathsf D(\Xi_2)}\right)\\
&+\frac1{1-\eta(b_1,d)}\left[\log(b_1)\left(\frac1{\mathsf D(\Xi_1)}-\frac1{\mathsf D(\Xi_2)}\right)+\frac{\log(d)}{1+b_1}\left(\frac1{\mathsf D(\Xi_2)}+\frac1{J(\Xi_2)}\right)\right],
\end{aligned}
\]
and
\[
\begin{aligned}
\mathcal R\equiv{}&M\left(\Xi_1,\frac{\epsilon\mathsf D(\Xi_1)}{1+\epsilon}\right)+M\left(\Xi_2,\frac{\epsilon\mathsf D(\Xi_2)}{1+\epsilon}\right)+3\ell_1+2\ell_2\\
&+\left(\frac{V^I(\Xi_1)}{(\mathsf D(\Xi_1))^2}+\frac{V^I(\Xi_2)}{(\mathsf D(\Xi_2))^2}+\frac{V^J(\Xi_2)}{(J(\Xi_2))^2}\right)+\frac{|\log(\zeta(\Xi_1))|}{\mathsf D(\Xi_1)}.
\end{aligned}
\]
Further, if the treatment assignment rule is modified as in Subsection 4.2, the upper bound holds with $\lambda(\Xi_1)$ replaced by $\lambda(z_0,\Xi_1)$, which is defined as follows:
\[
\begin{aligned}
&(1-\pi_0)+(1-\pi_0)\sum_{t=1}^{t_0}\prod_{s=1}^t\left(1-\pi_s\left(z_0(1:s)\right)\right)\\
&\quad+(1-\pi_0)\sum_{t=t_0+1}^\infty\prod_{s=1}^{t_0}\left(1-\pi_s\left(z_0(1:s)\right)\right)\prod_{s=t_0+1}^t\left(1-\pi_s\left(z_0,\Xi_1(1:s-t_0)\right)\right).
\end{aligned}\tag{21}
\]
''')
claim('6.1',[17],r'''
Suppose that the response model satisfies condition (14) and that the change-point model satisfies conditions (27) and (28). If condition (29) also holds, then
\[
\inf_{(\mathcal X,T)\in\mathcal C_\alpha}\mathsf E[T]\ge\left(\lambda^*+\frac{|\log(\alpha)|}{\mathsf D^*}\right)(1+o(1)).
\]
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=26,main_text_boundary=dict(location='Final references [47]–[48] occupy the top of page 26. Appendix A starts at y=137.4128; only the area above y=137.4 is included. All appendix mathematics on pages 26–53 is excluded.',shared_page_with_appendix=True),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);assert len(pdf)==53 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
first=pdf[0].get_text();assert '1710.00915v5' in first and '21 Jun 2024' in first
labels=[];mentions=[]
for n in range(26):
    page=pdf[n];clip=fitz.Rect(0,0,page.rect.width,137.4) if n==25 else page.rect
    assert (ROOT/'evidence'/f'page-{n+1:02}.txt').read_bytes().decode('utf8')==page.get_text(clip=clip)
    for b in page.get_text('dict',clip=clip)['blocks']:
        for ln in b.get('lines',[]):
            text=''.join(s['text'] for s in ln['spans']).strip();m=re.match(r'^(THEOREM|Theorem)\s+(\d+\.\d+)',text)
            if m:(labels if m[1]=='THEOREM' else mentions).append((n+1,m[2]))
assert labels==[(8,'3.1'),(12,'5.1'),(17,'6.1')],labels
assert mentions==[(16,'5.1')],mentions
assert '[48]' in pdf[25].get_text(clip=fitz.Rect(0,0,pdf[25].rect.width,137.4))
assert 'APPENDIX A:' in pdf[25].get_text(clip=fitz.Rect(0,137.4,pdf[25].rect.width,152))
for c in claims:
    for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
        depth=0
        for b in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
            depth+=1 if b=='{' else -1
            assert depth>=0,c['claim_id']
        assert depth==0,c['claim_id']
path=ROOT/'theorem-inventory.json';path.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(path)],check=True)
for n in [8,12,13,17]:shutil.copyfile(Path(prov['working_pdf']).parent/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=3,inventory_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),printed_heading_check=labels,notes=[
 'The inspected 53-page PDF is arXiv:1710.00915v5 dated 21 June 2024. Its title and both author names match the corpus entry.',
 'Final references share page 26 with Appendix A. Only the area above y=137.4 is used; the actual heading starts at y=137.4128. Appendix content is excluded.',
 'There are three main-text THEOREM headings. One ordinary-case Theorem mention at the beginning of a line on page 16 is a citation, not a fourth theorem. All other result kinds are excluded.',
 'Theorem 3.1 retains its auxiliary-optimization and Markovian hypotheses, the state-dependent posterior-odds boundary and the memoryless special case.',
 'Theorem 5.1 spans pages 12–13. The complete remainder formula and the modified-assignment extension (21) are included, not only the leading expectation inequality.',
 'Font inspection distinguishes sans-serif D and E from italic I,J,V, script X,U,R and script C. The Markov sufficient statistic is blackboard-bold S (MSBM10), unlike the plain S used for stage endpoints later. This distinction is retained in Theorem 3.1.',
 'Theorem 6.1 retains all four numbered condition references and the infimum over the false-alarm-constrained class. The asymptotic parameter convention will be resolved from Section 6, without rewriting this original statement.',
 'Only the independent theorem inventory is complete. Resolve the response/change-point models, Markov sufficient state, stopping/control construction, proposed cyclic procedure, conditions (14),(16),(27)–(29), information numbers and all bound terms before completing the paper census.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,status='in_progress',stage='inventory_validated',updated_at=review['reviewed_at'],next_action='Resolve the three Theorems from main-text definitions: response and change-point models, posterior odds and Bellman procedure, two-stage cyclic assignment and modification, information/variance/transition quantities, admissible class, and conditions (14),(16),(27)–(29). All Theorem 5.1 terms and its page-13 extension are already inventoried. Exclude appendix content below y=137.4 on page 26 and thereafter.'),indent=2)+'\n')
print('Saved and independently validated three complete main-text Theorems.')
