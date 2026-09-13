"""Preserve all three main-text Theorems, including the page-spanning Theorem 4."""
import hashlib,json,re,subprocess,sys,shutil
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
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
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.now(timezone.utc).isoformat(),theorem_count=3,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),notes=[
 'Pinned arXiv:2210.14429v2, stamped 30 August 2023; cover date is 1 September 2023. Main pages 1-17 and the portion of page 18 above Appendix A were searched.',
 'Only Theorems 1, 4 and 5 are printed in the main text. Numbers 2 and 3 are Corollaries, not omitted Theorems.',
 'Theorem 1 preserves both its depth-K inequality and the penalized-pruning inequality, including the extra infimum over K in the latter.',
 'Theorem 4 begins on page 15 and continues at the top of page 16. Both rates, the constant declaration and the penalty condition are included; the following upright discussion is outside the theorem.',
 'Theorem 5 preserves the source wording Suppose Assumptions 2 holds and uses N, the subsample size, in the complexity term. The expectation over inverse split probabilities remains as printed.',
 'All complete statements were visually checked on pages 12, 15-17. The page-18 main-text clip and separate Appendix A heading crop verify the shared-page boundary. No appendix body is read or used.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,12,15,16,17,18]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
shutil.copy2(work/'appendix-heading-only.png',ROOT/'evidence/appendix-heading-only.png')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve ridge-function library and local variation, empirical tree construction, randomized split probabilities, pruning, tail/partition assumptions and forest subsampling from the main text.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated three Theorems.')
