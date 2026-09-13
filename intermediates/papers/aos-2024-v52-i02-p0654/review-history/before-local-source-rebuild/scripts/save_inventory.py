"""Independent source-ordered inventory of every main-paper Theorem."""
import datetime,fitz,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text())
claims=[]
def claim(n,title,pages,body):
    claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label='Theorem '+n+' ('+title+')',source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+n+(' — continuation' if i else '')) for i,p in enumerate(pages)]))
claim('2.1','The minimax risk under conventional setup and common design',[6],r'''
Suppose no source samples are available, i.e. $n_s=0$ and the fixed and common design points for the target sample satisfy $\max_{1\leq j\leq m_t+1}(T_j^{[t]}-T_{j-1}^{[t]})\leq C_t/m_t$ for some constant $C_t>0$, where $T_0^{[t]}=0$ and $T_{m_t+1}^{[t]}=1$. Then
\[
\inf_{\widehat f^{[t]}}\sup_{\mathbb P\in\mathcal P}\mathbb E\|\widehat f^{[t]}-f^{[t]}\|_{\mathcal L^2}^2
=\widetilde\Theta\left(L_m^2m_t^{-2\alpha_m}+\frac1{n_t}\right),
\]
where the infimum is taken over all estimators $\widehat f^{[t]}=\widehat f^{[t]}(\mathcal D^{[t]})$ based on the target sample.
''')
claim('2.2','Upper bound under a common design',[8,9],r'''
Suppose
\[
\max_{1\leq j\leq m_t+1}(T_j^{[t]}-T_{j-1}^{[t]})\leq\frac{C_t}{m_t}
\quad\text{and}\quad
\max_{1\leq j\leq m_s+1}(T_j^{[s]}-T_{j-1}^{[s]})\leq\frac{C_s}{m_s}
\]
where $C_t,C_s>0$ are some constants as well as $T_0^{[t]}=T_0^{[s]}=0$ and $T_{m_t+1}^{[t]}=T_{m_t+1}^{[s]}=1$. Consider the conventional learning estimator $\widehat f_{\mathrm{CL}}^{[t]}$ which is the output of the algorithm $\mathcal A_{\mathrm{CL}}(b_t,d_t,M_t)$ with the following specifications:

- Any constant degree $d_t\geq\omega(\alpha_m)$,
- Any bandwidth $b_t=\lceil m_t/2B_t(d_t+1)\rceil^{-1}$ for constant $B_t\geq C_t$,
- The threshold $M_t=\log n_t$.

Plus, let $\widehat f_{\mathrm{TL}}^{[t]}$ be the output of the transfer learning algorithm $\mathcal A_{\mathrm{TL}}(b_s,b_\delta,d_s,d_\delta,M_s,M_\delta)$ with the following specifications:

- Any constant degrees $d_s\geq\omega(\alpha_m)$ and $d_\delta\geq\omega(\alpha_\delta)$.
- Any bandwidths $b_s=\lceil m_s/2(d_s+1)B_s\rceil^{-1}$ and $b_\delta=\lceil m_t/2(d_\delta+1)B_\delta\rceil^{-1}$ for any given constants $B_s\geq C_s$ and $B_\delta\geq C_t$.
- Two thresholds $M_s=\log n_s$ and $M_\delta=\log n_tn_s$.

The estimator $\widehat f^{[t]}$ for the mean function $f^{[t]}$ is now defined as one of them:
\[
\widehat f^{[t]}=\begin{cases}
\widehat f_{\mathrm{CL}}^{[t]}&\text{when }R_C(\widehat f_{\mathrm{CL}}^{[t]})\leq R_C(\widehat f_{\mathrm{TL}}^{[t]}),\\
\widehat f_{\mathrm{TL}}^{[t]}&\text{when }R_C(\widehat f_{\mathrm{CL}}^{[t]})>R_C(\widehat f_{\mathrm{TL}}^{[t]}),
\end{cases}
\]
where the following quantities are additionally defined:
\[
R_C(\widehat f_{\mathrm{CL}}^{[t]}):=L_m^2m_t^{-2\alpha_m}+\frac{\log^2 n_t}{n_t},
\]
\[
R_C(\widehat f_{\mathrm{TL}}^{[t]}):=L_\delta^2m_t^{-2\alpha_\delta}+\frac{\log^2(n_tn_s)}{n_t}
+L_m^2m_s^{-2\alpha_m}+\frac{\log^2(Kn_s)}{Kn_s}.
\]
In this situation, we obtain
\[
\sup_{\mathbb P\in\mathcal P}\mathbb E\|\widehat f^{[t]}-f^{[t]}\|_{\mathcal L^2}^2
\lesssim R_C(\widehat f_{\mathrm{CL}}^{[t]})\wedge R_C(\widehat f_{\mathrm{TL}}^{[t]}).
\]
''')
claim('2.3','Lower bound under a common design',[9],r'''
Under a common design,
\[
\inf_{\widehat f^{[t]}}\sup_{\mathbb P\in\mathcal P}\mathbb E\|\widehat f^{[t]}-f^{[t]}\|_{\mathcal L^2}^2
\gtrsim\left(L_m^2m_t^{-2\alpha_m}+\frac1{n_t}\right)\wedge
\left(L_\delta^2m_t^{-2\alpha_\delta}+\frac1{n_t}+L_m^2m_s^{-2\alpha_m}+\frac1{Kn_s}\right),
\]
where the infimum is taken over all possible estimators $\widehat f^{[t]}=\widehat f^{[t]}(\mathcal D^{[t]},\mathcal D^{[s,1]},\ldots,\mathcal D^{[s,K]})$.
''')
claim('2.4','Adaptive estimation under a common design',[12],r'''
Under the same assumptions as Theorem 2.2, we consider a maximum number of repetitions, $r_{\max}\in\mathbb Z^+$ and let $\widehat g_r^{[t]}$ $(r=1,\ldots,r_{\max})$ denote the output of the $r$-th execution of the algorithm $\mathcal A_{\mathrm{ALC}}$. By averaging these estimates, we obtain the final estimator:
\[
\widehat f^{[t]}=\frac1{r_{\max}}\sum_{r=1}^{r_{\max}}\widehat g_r^{[t]}.\tag{5}
\]
This adaptive estimator $\widehat f^{[t]}$ attains the same upper bound of Theorem 2.2:
\[
\sup_{\mathbb P\in\mathcal P}\mathbb E\|\widehat f^{[t]}-f^{[t]}\|_{\mathcal L^2}^2
\lesssim R_C(\widehat f_{\mathrm{CL}}^{[t]})\wedge R_C(\widehat f_{\mathrm{TL}}^{[t]}).
\]
''')
claim('3.1','The minimax risk under conventional setup and independent design',[12,13],r'''
Suppose the distribution $\eta_t$ for the target design points is dominated by the Lebesgue measure and its density is bounded from below by a constant $C_t>0$ and from above by $\Gamma_t>0$. Then
\[
\inf_{\widehat f^{[t]}}\sup_{\mathbb P\in\mathcal P}\mathbb E\|\widehat f^{[t]}-f^{[t]}\|_{\mathcal L^2}^2
=\widetilde\Theta\left(L_m^{2/(2\alpha_m+1)}(m_tn_t)^{-2\alpha_m/(2\alpha_m+1)}+\frac1{n_t}\right),
\]
where the infimum is taken over all estimators $\widehat f^{[t]}=\widehat f^{[t]}(\mathcal D^{[t]})$ based on the target sample.
''')
claim('3.2','Upper bound under an independent design',[13,14],r'''
Suppose the distributions $\eta_t$ and $\eta_s$ for target and source design points are dominated by the Lebesgue measure, and their densities are bounded from below by a constant $C_t,C_s>0$ and from above by $\Gamma_t,\Gamma_s>0$, respectively. Consider the conventional learning estimator $\widehat f_{\mathrm{CL}}^{[t]}$ which is the output of algorithm $\mathcal A_{\mathrm{CL}}(b_t,d_t,M_t)$ with the following specifications:

- For any constant $B_t\geq\Gamma_t$, bandwidth:
\[
b_t=\left\lceil(L_m^2m_tn_t)^{1/(2\alpha_m+1)}(\log n_t)^{-2/(2\alpha_m+1)}\right\rceil^{-1}
\wedge\lceil2B_tm_t\rceil^{-1},
\]
- Any constant degree $d_t\geq\omega(\alpha_m)$,
- The threshold $M_t=\log n_t$.

Besides, let $\widehat f_{\mathrm{TL}}^{[t]}$ be the output of the transfer learning algorithm $\mathcal A_{\mathrm{TL}}(b_s,b_\delta,d_s,d_\delta,M_s,M_\delta)$ with the following specifications:

- For any constants $B_s\geq\Gamma_s$ and $B_\delta\geq\Gamma_t$, bandwidths:
\[
b_s=\left\lceil(L_m^2Km_sn_s)^{1/(2\alpha_m+1)}\big(\log(Kn_s)\big)^{-2/(2\alpha_m+1)}\right\rceil^{-1}
\wedge\lceil2B_sKm_s\rceil^{-1},
\]
\[
b_\delta=\left\lceil(L_\delta^2m_tn_t)^{1/(2\alpha_\delta+1)}\big(\log(n_tn_s)\big)^{-2/(2\alpha_\delta+1)}\right\rceil^{-1}
\wedge\lceil2B_\delta m_t\rceil^{-1}.
\]
- Any constant degrees $d_s\geq\omega(\alpha_m)$ and $d_\delta\geq\omega(\alpha_\delta)$.
- Two thresholds $M_s=\log n_s$ and $M_\delta=\log n_tn_s$.

The estimator $\widehat f^{[t]}$ of the mean function $f^{[t]}$ is defined as one of them:
\[
\widehat f^{[t]}=\begin{cases}
\widehat f_{\mathrm{CL}}^{[t]}&\text{when }R_I(\widehat f_{\mathrm{CL}}^{[t]})\leq R_I(\widehat f_{\mathrm{TL}}^{[t]}),\\
\widehat f_{\mathrm{TL}}^{[t]}&\text{when }R_I(\widehat f_{\mathrm{CL}}^{[t]})>R_I(\widehat f_{\mathrm{TL}}^{[t]}),
\end{cases}
\]
where the following quantities are further defined:
\[
R_I(\widehat f_{\mathrm{CL}}^{[t]}):=L_m^{2/(2\alpha_m+1)}
\left(\frac{\log^2 n_t}{m_tn_t}\right)^{2\alpha_m/(2\alpha_m+1)}+\frac{\log^2 n_t}{n_t},
\]
\[
R_I(\widehat f_{\mathrm{TL}}^{[t]}):=L_m^{2/(2\alpha_m+1)}
\left(\frac{\log^2(Kn_s)}{Km_sn_s}\right)^{2\alpha_m/(2\alpha_m+1)}
+\frac{\log^2(Kn_s)}{Kn_s}
+L_\delta^{2/(2\alpha_\delta+1)}
\left(\frac{\log^2(n_tn_s)}{m_tn_t}\right)^{2\alpha_\delta/(2\alpha_\delta+1)}
+\frac{\log^2(n_tn_s)}{n_t}.
\]
In this situation, we have
\[
\sup_{\mathbb P\in\mathcal P}\mathbb E\|\widehat f^{[t]}-f^{[t]}\|_{\mathcal L^2}^2
\lesssim R_I(\widehat f_{\mathrm{CL}}^{[t]})\wedge R_I(\widehat f_{\mathrm{TL}}^{[t]}).
\]
''')
claim('3.3','Lower bound under an independent design',[14],r'''
Under an independent design,
\[
\inf_{\widehat f^{[t]}}\sup_{\mathbb P\in\mathcal P}\mathbb E\|\widehat f^{[t]}-f^{[t]}\|_{\mathcal L^2}^2
\gtrsim\left[L_m^{2/(2\alpha_m+1)}(m_tn_t)^{-2\alpha_m/(2\alpha_m+1)}+\frac1{n_t}\right]
\wedge\left[L_\delta^{2/(2\alpha_\delta+1)}(m_tn_t)^{-2\alpha_\delta/(2\alpha_\delta+1)}+\frac1{n_t}
+L_m^{2/(2\alpha_m+1)}(Km_sn_s)^{-2\alpha_m/(2\alpha_m+1)}+\frac1{Kn_s}\right],
\]
where the infimum is taken over all possible estimators $\widehat f^{[t]}=\widehat f^{[t]}(\mathcal D^{[t]},\mathcal D^{[s,1]},\ldots,\mathcal D^{[s,\ell]})$.
''')
claim('3.4','Adaptive estimation under an independent design',[17],r'''
Suppose the assumptions in Theorem 3.2 hold. For any given $r_{\max}\in\mathbb Z^+$, let $\widehat g_r^{[t]}$ $(r=1,\ldots,r_{\max})$ be the output of the $r$-th execution of the algorithm $\mathcal A_{\mathrm{ALI}}$. Take an average of them to obtain our final estimator:
\[
\widehat f^{[t]}=\frac1{r_{\max}}\sum_{r=1}^{r_{\max}}\widehat g_r^{[t]}.\tag{6}
\]
This adaptive estimator $\widehat f^{[t]}$ attains the same upper bound of Theorem 3.2:
\[
\sup_{\mathbb P\in\mathcal P}\mathbb E\|\widehat f^{[t]}-f^{[t]}\|_{\mathcal L^2}^2
\lesssim R_I(\widehat f_{\mathrm{CL}}^{[t]})\wedge R_I(\widehat f_{\mathrm{TL}}^{[t]}).
\]
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=25,main_text_boundary=dict(location='The entire 25-page PDF is the main paper, including Section 6 proofs on pages 21-23, a notice for a separate supplement on page 23, and references and author addresses ending on page 25. No appendix or supplement body is embedded; the separately referenced supplement is excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);labels=[]
assert len(pdf)==25 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
assert '2401.12331v2' in pdf[0].get_text() and '27 Mar 2024' in pdf[0].get_text()
for n in range(25):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(span['text'] for span in line['spans'])
            match=re.fullmatch(r'THEOREM (\d+\.\d+) \((.+)\)\.',text.strip())
            if match:
                assert all(span['font']=='NimbusRomNo9L-Regu' for span in line['spans'])
                labels.append((n+1,match.group(1)))
assert labels==[(6,'2.1'),(8,'2.2'),(9,'2.3'),(12,'2.4'),(12,'3.1'),(13,'3.2'),(14,'3.3'),(17,'3.4')],labels
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
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=8,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),printed_heading_check=labels,notes=[
 'Pinned arXiv:2401.12331v2, stamped 27 March 2024, 25 main-paper pages. Section 6 contains main-paper proofs; the page-23 supplement notice describes a separate document that was not opened. References and author addresses end on page 25.',
 'Independent enumeration joins the small-cap THEOREM spans on all main pages and finds exactly Theorems 2.1-2.4 and 3.1-3.4. Proof headings, Propositions, Lemmas and citations are excluded.',
 'All eight complete original statements were checked visually on pages 6,8,9,12,13,14,17. Theorems 2.2,3.1 and 3.2 retain their page continuations.',
 'Both conventional minimax results quantify estimators based only on the target sample. The transfer lower bounds quantify all available-sample estimators rather than imposing a specific algorithm.',
 'The common-design upper bound preserves every degree, bandwidth, threshold, selection inequality and risk expression. Its source endpoint T_[m_t+1]^[s] is retained rather than changed to the source sample count.',
 'The independent-design upper bound preserves both density bounds, all bandwidth ceilings and minimum caps, threshold choices, selection inequalities, and every factor of K in the risk terms.',
 'Both adaptive results retain the full reference to the corresponding upper-bound assumptions, the algorithm name, the arbitrary positive repetition count and the averaging formula.',
 'The final data argument in Theorem 3.3 uses ell rather than K in the source and is preserved. Interpretation and algorithm specification issues will be recorded separately during extraction.',
 'The census remains incomplete until the parameter class, random-function observation model, smoothness convention, sub-Gaussian condition, sampling designs and all four algorithms have been resolved and independently audited.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,6,8,9,12,13,14,17,23,25]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve main-text parameter class, random-function observation model, smoothness and sub-Gaussian conditions, common/independent design settings and Algorithms 1-4. Preserve source algorithm ambiguities; do not open the separate supplement.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated eight complete main-text Theorems.')
