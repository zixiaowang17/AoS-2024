"""Preserve all four main-text Theorems from the pinned July 2023 v2 source."""
import datetime,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text());claims=[]
def claim(n,title,pages,body):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+' ('+title+')',source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+n+(' — continuation' if i else '')) for i,p in enumerate(pages)]))
claim('1','GA with cross-sectional independence',[10,11],r'''
Suppose that Assumptions 1–3 are satisfied. Then, under the null hypothesis, for $\Delta_0=(bn)^{-1/3}\log^{2/3}(n)$,
\[
\Delta_1=\left(\frac{n^{4/q}\log^7(pn)}p\right)^{1/6},\quad
\Delta_2=\left(\frac{n^{4/q}\log^3(pn)}{p^{1-2/q}}\right)^{1/3},
\]
we have
\[
\sup_{u\in\mathbb R}\left|\mathbb P(\mathcal Q_n\leq u)-\mathbb P\left(\max_{bn+1\leq i\leq n-bn}Z_i\leq u\right)\right|\lesssim\Delta_0+\Delta_1+\Delta_2,\tag{14}
\]
where the constant in $\lesssim$ is independent of $n,p,b$. If in addition, $\log(n)=o\{(bn)^{1/2}\}$ and
\[
n^4p^{2-q}\log^{3q}(pn)\to0,\tag{15}
\]
then we have
\[
\sup_{u\in\mathbb R}\left|\mathbb P(\mathcal Q_n\leq u)-\mathbb P\left(\max_{bn+1\leq i\leq n-bn}Z_i\leq u\right)\right|\to0.\tag{16}
\]
''')
claim('2','Temporal consistency',[15],r'''
Let $q\geq8$. Under Assumptions 1–4, if (15) hold, $b\ll\kappa_n$, $\delta_p^2\geq3\omega$, $\omega\gg(p\log(n))^{1/2}(bn)^{-1}$ and $\max_{1\leq k\leq K}|\Lambda^{-1}\gamma_k|_q/|\Lambda^{-1}\gamma_k|_2=O(1/K^{1/q})$, then we have the following results:

(i) (Number of breaks). $\mathbb P(\widehat K=K)\to1$.

(ii) (Time stamps of breaks). Let $\Gamma_k=p/(bn|\Lambda^{-1}\gamma_k|_2^2)$. Then, we have $\max_{1\leq k\leq K}|\widehat\tau_k-\tau_{k^*}|\cdot|\Lambda^{-1}\gamma_k|_2^2/(1+\Gamma_k)=O_{\mathbb P}\{\log^2(n)\}$, where $k^*=\operatorname*{arg\,min}_i|\widehat\tau_k-\tau_i|$. If in addition, $\delta_p^2/p\gtrsim1/(bn)$, we have
\[
\max_{1\leq k\leq K}|\widehat\tau_k-\tau_{k^*}|\cdot|\Lambda^{-1}\gamma_k|_2^2=O_{\mathbb P}\{\log^2(n)\}.
\]

(iii) (Break sizes). $\max_{1\leq k\leq K}\left||\Lambda^{-1}(\widehat\gamma_k-\gamma_{k^*})|_2^2-\bar c\right|=O_{\mathbb P}\{(p\log(n))^{1/2}(bn)^{-1}\}$, which also implies that $|\widehat\delta_p-\delta_p|=O_{\mathbb P}\{(p\log(n))^{1/4}(bn)^{-1/2}\}$.
''')
claim('3','GA for Two-Way MOSUM',[21],r'''
Suppose that Assumptions 1–3 and 5 are satisfied. Then, under the null hypothesis, for $\Delta_0^\diamond=(bn)^{-1/3}\log^{2/3}(nS)$,
\[
\Delta_1^\diamond=\left(\frac{(nS)^{4/q}\log^7(pn)}{|\mathcal L_{\min}|}\right)^{1/6},\quad
\Delta_2^\diamond=\left(\frac{(nS)^{4/q}p^{2/q}\log^3(pn)}{|\mathcal L_{\min}|}\right)^{1/3},
\]
we have
\[
\sup_{u\in\mathbb R}\left|\mathbb P(\mathcal Q_n^\diamond\leq u)-\mathbb P\left(\max_{\varphi\in\mathcal N}Z_\varphi^\diamond\leq u\right)\right|\lesssim\Delta_0^\diamond+\Delta_1^\diamond+\Delta_2^\diamond,\tag{35}
\]
where $\mathcal N$ is defined in (33), and the constant in $\lesssim$ is independent of $n,p,b$. If in addition, $\log(nS)=o\{(bn)^{1/2}\}$ and
\[
(nS)^4p^2|\mathcal L_{\min}|^{-q}\log^{3q}(pn)\to0,\tag{36}
\]
then we have
\[
\sup_{u\in\mathbb R}\left|\mathbb P(\mathcal Q_n^\diamond\leq u)-\mathbb P\left(\max_{\varphi\in\mathcal N}Z_\varphi^\diamond\leq u\right)\right|\to0.\tag{37}
\]
''')
claim('4','GA with weak cross-sectional dependence',[30],r'''
Suppose that Assumptions 8–12 hold. Then, under the null hypothesis, for $\widetilde\Delta_0=(bn)^{-1/3}\log^{2/3}(nS)$, $\widetilde\Delta_1=c_{p,n}^{-(q-4)/(3q)}$, $\widetilde\Delta_2=c_{p,n}^{-1/(8v)}\log(pn)$, where
\[
c_{p,n}=p^{-\frac2{q-4}}B_{\min}^{\frac q{q-4}}(nS)^{-\left(\frac4{q-4}+\frac{2v}{q\xi}\right)}\big(\log(pn)\big)^{-\left(\frac{(2+q)v}{2q\xi}+\frac{3q}{q-4}\right)},\tag{57}
\]
we have
\[
\sup_{u\in\mathbb R}\left|\mathbb P(\widetilde{\mathcal Q}_n\leq u)-\mathbb P\left(\max_{\varphi\in\mathcal N}\widetilde Z_\varphi\leq u\right)\right|\lesssim\widetilde\Delta_0+\widetilde\Delta_1+\widetilde\Delta_2,
\]
where $\mathcal N$ is defined in (33), and the constant in $\lesssim$ is independent of $n,p,b$ and $S$. If in addition, $\log(nS)=o\{(bn)^{1/2}\}$ and $\log^{8v}(pn)=o(c_{p,n})$, then
\[
\sup_{u\in\mathbb R}\left|\mathbb P(\widetilde{\mathcal Q}_n\leq u)-\mathbb P\left(\max_{\varphi\in\mathcal N}\widetilde Z_\varphi\leq u\right)\right|\to0.
\]
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=37,main_text_boundary=dict(location='Main Sections 1-5 and references end on PDF page 37. Appendix A Simulation and Application begins on a separate page 38, established with a heading-only crop. Appendix bodies on pages 38-111 are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);labels=[]
assert len(pdf)==111 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
for n in range(37):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            for span in line['spans']:
                if span['font']=='CMBX10':
                    match=re.fullmatch(r'Theorem (\d+)',span['text'].strip())
                    if match:labels.append((n+1,match.group(1)))
assert labels==[(10,'1'),(15,'2'),(21,'3'),(30,'4')],labels
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
 'Pinned arXiv:2208.13074v2, stamped 4 July 2023, 111 pages. Main text and references end on page 37. Only the heading crop from page 38 was inspected to establish Appendix A; appendix bodies were excluded.',
 'Independent font-sensitive enumeration of all 37 main pages finds exactly Theorems 1-4. Corollaries and Propositions are excluded from the inventory, and prose references are distinguished from CMBX10 theorem labels.',
 'The complete original bodies were visually checked on pages 10,11,15,21,30. Theorem 1 continues onto page 11; all other theorem statements fit on their cited page.',
 'Theorem 1 retains all three approximation errors, the constant-dependence clause, and both additional rate conditions for convergence. Condition (15) is preserved for its later reference in Theorem 2.',
 'Theorem 2 retains Assumptions 1-4, q>=8, condition (15), all signal and threshold requirements, and each of its three conclusions. The nearest-break matching k*, the Gamma_k denominator and the optional stronger rate are unchanged.',
 'Theorem 3 retains its distinct minimum-neighborhood normalization, the p^(2/q) factor in Delta_2, both additional convergence conditions, and its constant clause excluding n,p,b but not explicitly S.',
 'Theorem 4 retains its new Assumptions 8-12, all powers in c_(p,n), its separate convergence conditions, and the constant clause explicitly independent of S. No assumption of cross-sectional independence is imported.',
 'The census remains incomplete until all main-text definitions, inherited conditions, Gaussian covariance formulas and estimator constructions have been resolved and independently audited.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,10,11,15,21,30,37]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve main-text model (1), linear and nonlinear error processes, Assumptions 1-5 and 8-12, MOSUM statistics, break estimators and Gaussian reference covariance formulas. Exclude appendix bodies.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated four complete main-text Theorems.')
