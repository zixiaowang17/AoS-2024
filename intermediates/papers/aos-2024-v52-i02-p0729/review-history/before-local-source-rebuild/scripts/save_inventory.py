"""Save every complete original main-paper Theorem before interface extraction."""
import datetime,fitz,hashlib,json,re,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
prov=json.loads((ROOT/'evidence/source-provenance.json').read_text())
claims=[]
def claim(n,pages,body,title=None):
    label='Theorem '+str(n)+((' ('+title+')') if title else '')
    claims.append(dict(claim_id=PID+'/T'+str(n),paper_id=PID,claim_kind='theorem',label=label,source_order=len(claims)+1,statement_original=body.strip(),evidence=[dict(page=p,location='Theorem '+str(n)+(' — continuation' if i else '')) for i,p in enumerate(pages)]))
claim(1,[7],r'''
Assume that each column of the ground truth $\mathbf X$ (cf. (2.1a)) is independently generated from $\mathcal N(\mathbf0,\mathbf S^\star)$, and that the sampling set $\Omega$ follows the random sampling model in Section 1.1. Suppose that $p<1-\delta$ for some arbitrary constant $0<\delta<1$ or $p=1$, and $\kappa,\mu,r,\kappa_\omega\asymp1$. Assume that Assumption 1 holds and $d\gtrsim\log^5n$,
\[
\frac{\omega_{\max}^2}{p\sigma_r^{\star2}}\sqrt{\frac dn}\lesssim\frac1{\log^{7/2}(n+d)},\qquad\frac{\omega_{\max}}{\sigma_r^\star}\sqrt{\frac d{np}}\lesssim\frac1{\log^3(n+d)},\tag{3.5a}
\]
\[
ndp^2\gtrsim\log^9(n+d),\qquad np\gtrsim\log^7(n+d).\tag{3.5b}
\]
Suppose, in addition, that the number of iterations exceeds
\[
t_0\gtrsim\log\left[\left(\frac{\log^2(n+d)}{\sqrt{nd}\,p}+\frac{\omega_{\max}^2}{p\sigma_r^{\star2}}\sqrt{\frac dn}\log(n+d)+\frac{\log(n+d)}{\sqrt{np}}+\frac{\omega_{\max}}{\sigma_r^\star}\sqrt{\frac{d\log(n+d)}{np}}\right)^{-1}\right].\tag{3.6}
\]
Let $\mathbf R$ be the $r\times r$ rotation matrix $\mathbf R=\operatorname{sgn}(\mathbf U^\top\mathbf U^\star)$. Then the estimate $\mathbf U$ returned by Algorithm 2 obeys: for all $1\leq l\leq d$,
\[
\sup_{C\in\mathscr C^r}\left|\mathbb P\big([\mathbf U\mathbf R-\mathbf U^\star]_{l,\cdot}\in C\big)-\mathcal N(\mathbf0,\mathbf\Sigma_{U,l}^\star)\{C\}\right|=o(1),
\]
where $\mathscr C^r$ represents the set of all convex sets in $\mathbb R^r$, and
\[
\mathbf\Sigma_{U,l}^\star:=\left(\frac{1-p}{np}\|\mathbf U_{l,\cdot}^\star\mathbf\Sigma^\star\|_2^2+\frac{\omega_l^{\star2}}{np}\right)(\mathbf\Sigma^\star)^{-2}+\frac{2(1-p)}{np}\mathbf U_{l,\cdot}^{\star\top}\mathbf U_{l,\cdot}^\star
+(\mathbf\Sigma^\star)^{-2}\mathbf U^{\star\top}\operatorname{diag}\big([d_{l,i}^\star]_{1\leq i\leq d}\big)\mathbf U^\star(\mathbf\Sigma^\star)^{-2}\tag{3.7}
\]
with
\[
d_{l,i}^\star:=\frac1{np^2}\big[\omega_l^{\star2}+(1-p)\|\mathbf U_{l,\cdot}^\star\mathbf\Sigma^\star\|_2^2\big]\big[\omega_i^{\star2}+(1-p)\|\mathbf U_{i,\cdot}^\star\mathbf\Sigma^\star\|_2^2\big]+\frac{2(1-p)^2}{np^2}S_{l,i}^{\star2}.
\]
''')
claim(2,[9],r'''
Suppose that the conditions of Theorem 1 hold. Then there exists a $r\times r$ rotation matrix $\mathbf R=\operatorname{sgn}(\mathbf U^\top\mathbf U^\star)$ such that the confidence regions $\mathrm{CR}_{U,l}^{1-\alpha}$ $(1\leq l\leq d)$ computed in Algorithm 3 obey
\[
\sup_{1\leq l\leq d}\left|\mathbb P\big(\mathbf U_{l,\cdot}^\star\mathbf R^\top\in\mathrm{CR}_{U,l}^{1-\alpha}\big)-(1-\alpha)\right|=o(1).
\]
''')
claim(3,[11],r'''
Suppose that $p<1-\delta$ for some arbitrary constant $0<\delta<1$ or $p=1$, and $\kappa,\mu,r,\kappa_\omega\asymp1$. Consider any $1\leq i,j\leq d$. Assume that $\mathbf U^\star$ is $\mu$-incoherent and satisfies the following condition:
\[
\|\mathbf U_{i,\cdot}^\star\|_2+\|\mathbf U_{j,\cdot}^\star\|_2
\gtrsim\left[\frac{\omega_{\max}}{\sigma_r^\star}\sqrt{\frac{d\log^5(n+d)}{np}}+\frac{\omega_{\max}^2}{p\sigma_r^{\star2}}\sqrt{\frac{d\log^5(n+d)}n}+\sqrt{\frac{\log^7(n+d)}{ndp^2}}\right]\sqrt{\frac1d}.\tag{3.12}
\]
In addition, suppose that Assumption 1 holds, and
\[
d\gtrsim\log^5n,\qquad np\gtrsim\log^7(n+d),\qquad ndp^2\gtrsim\log^7(n+d),
\]
\[
\frac{\omega_{\max}}{\sigma_r^\star}\sqrt{\frac d{np}}\lesssim\frac1{\log^3(n+d)},\qquad\frac{\omega_{\max}^2}{p\sigma_r^{\star2}}\sqrt{\frac dn}\lesssim\frac1{\log^{7/2}(n+d)}.
\]
Assume that the number of iterations satisfies (3.6). Then the matrix $\mathbf S$ computed by Algorithm 2 obeys
\[
\sup_{t\in\mathbb R}\left|\mathbb P\left(\frac{S_{i,j}-S_{i,j}^\star}{\sqrt{v_{i,j}^\star}}\leq t\right)-\Phi(t)\right|=o(1),
\]
where $\Phi(\cdot)$ denotes the CDF of the standard Gaussian distribution.
''')
claim(4,[12],r'''
Suppose that the conditions in Theorem 3 hold. Assume that $ndp^2\gtrsim\log^8(n+d)$. Then the confidence interval computed in Algorithm 4 obeys
\[
\mathbb P\big(S_{i,j}^\star\in\mathrm{CI}_{i,j}^{1-\alpha}\big)=1-\alpha+o(1).
\]
''')
claim(5,[21,22],r'''
Suppose that Assumptions 2–3 hold. Assume that
\[
n_1\gtrsim\kappa^{\natural4}\mu^\natural r+\mu^{\natural2}r\log^2n,\qquad n_2\gtrsim r\log^4n,\qquad\text{and}\qquad\zeta_{\mathrm{op}}\ll\frac{\sigma_r^{\natural2}}{\kappa^{\natural2}},\tag{6.11}
\]
and that the algorithm is run for $t_0\geq\log(\frac{\sigma_1^{\star2}}{\zeta_{\mathrm{op}}})$ iterations. With probability exceeding $1-O(n^{-10})$, there exist two matrices $\mathbf Z$ and $\mathbf\Psi$ such that the estimates returned by HeteroPCA obey
\[
\mathbf U\mathbf R_U-\mathbf U^\natural=\mathbf Z+\mathbf\Psi,\tag{6.12}
\]
where
\[
\mathbf Z:=\mathbf E\mathbf V^\natural(\mathbf\Sigma^\natural)^{-1}+\mathcal P_{\mathrm{off\text{-}diag}}(\mathbf E\mathbf E^\top)\mathbf U^\natural(\mathbf\Sigma^\natural)^{-2},\tag{6.13a}
\]
\[
\|\mathbf\Psi\|_{2,\infty}\lesssim\kappa^{\natural2}\frac{\mu^\natural r}{n_1}\frac{\zeta_{\mathrm{op}}}{\sigma_r^{\natural2}}+\kappa^{\natural2}\frac{\zeta_{\mathrm{op}}^2}{\sigma_r^{\natural4}}\sqrt{\frac{\mu^\natural r}{n_1}}.\tag{6.13b}
\]
In fact, for each $m\in[n_1]$, we further have
\[
\|\mathbf Z_{m,\cdot}\|_2\lesssim\frac{\zeta_{\mathrm{op},m}}{\sigma_r^{\natural2}}\sqrt{\frac{\mu^\natural r}{n_1}}+\|\mathbf U_{m,\cdot}^\natural\|_2\left(\kappa^{\natural2}\sqrt{\frac{\mu^\natural r}{n_1}}\frac{\zeta_{\mathrm{op}}}{\sigma_r^{\natural2}}+\kappa^{\natural2}\frac{\zeta_{\mathrm{op}}^2}{\sigma_r^{\natural4}}\right),\tag{6.13c}
\]
\[
\|\mathbf\Psi_{m,\cdot}\|_2\lesssim\kappa^{\natural2}\frac{\zeta_{\mathrm{op}}\zeta_{\mathrm{op},m}}{\sigma_r^{\natural4}}\sqrt{\frac{\mu^\natural r}{n_1}}+\|\mathbf U_{m,\cdot}^\natural\|_2\left(\kappa^{\natural2}\sqrt{\frac{\mu^\natural r}{n_1}}\frac{\zeta_{\mathrm{op}}}{\sigma_r^{\natural2}}+\kappa^{\natural2}\frac{\zeta_{\mathrm{op}}^2}{\sigma_r^{\natural4}}\right).\tag{6.13d}
\]
''')
paper={k:prov[k] for k in ['paper_id','title','version','source_url','pdf_pages','pdf_sha256']}
paper.update(main_text_last_pdf_page=28,main_text_boundary=dict(location=prov['main_text_boundary'],shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
inv=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims)
pdf=fitz.open(prov['cached_pdf']);labels=[]
assert len(pdf)==28 and hashlib.sha256(Path(prov['cached_pdf']).read_bytes()).hexdigest()==paper['pdf_sha256']
assert '10.1214/24-AOS2366' in pdf[0].get_text() and '729–756' in pdf[0].get_text()
for n in range(28):
    for block in pdf[n].get_text('dict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(span['text'] for span in line['spans']).strip()
            match=re.match(r'THEOREM (\d+)\.',text)
            if match:labels.append((n+1,match.group(1)))
assert labels==[(7,'1'),(9,'2'),(11,'3'),(12,'4'),(21,'5')],labels
assert [(c['evidence'][0]['page'],c['claim_id'].split('/T')[-1]) for c in claims]==labels
assert 'SUPPLEMENTARY MATERIAL' in pdf[24].get_text() and 'REFERENCES' in pdf[24].get_text()
for c in claims:
    for chunks in re.findall(r'\\\[(.*?)\\\]|(?<!\\)\$(.*?)(?<!\\)\$',c['statement_original'],re.S):
        depth=0
        for brace in re.findall(r'(?<!\\)[{}]',''.join(chunks)):
            depth+=1 if brace=='{' else -1
            assert depth>=0,c['claim_id']
        assert depth==0,c['claim_id']
p=ROOT/'theorem-inventory.json';p.write_text(json.dumps(inv,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(p)],check=True)
review=dict(paper_id=PID,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=5,inventory_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),printed_heading_check=labels,notes=[
 'Published journal PDF, Annals of Statistics 52(2), pp.729-756, 28 pages. The supplement notice on PDF page 25 links to a separate unopened document. All 28 pages belong to the main paper, including references; no appendix body is embedded.',
 'Independent main-paper heading enumeration finds exactly Theorems 1-5. Cited Theorems 11,13,14 belong to the separate supplement and are excluded. Other result types and references are not inventoried as Theorems.',
 'Complete statements were visually checked on PDF pages 7,9,11,12,21,22. Theorem 5 continues on page 22 and retains all four parts of equation (6.13).',
 'Theorem 1 retains Gaussian columns, the sampling model, the alternative p=1, comparability assumptions, both noise restrictions, the log^9 sampling restriction, exact iteration condition, rotation and the full covariance formula including d-star. Its first iteration denominator is sqrt(nd) times p, not sqrt(ndp).',
 'Theorem 2 asserts a supremum of marginal rowwise coverage errors, not simultaneous joint coverage of every row. Its random rotation and explicit reference to Algorithm 3 remain in the original statement.',
 'Theorem 3 retains its row-norm lower bound and log^7 sampling restriction; it does not inherit the stronger log^9 restriction from Theorem 1 merely because the later discussion compares them. Theorem 4 adds log^8 and refers to Algorithm 4.',
 'Theorem 5 retains the separate general-subspace model notation with natural superscripts, but its iteration lower bound prints sigma_1 with a star superscript. That mismatch is preserved for later source resolution rather than silently changed.',
 'Only the inventory is complete. Resolve Assumptions 1-3, Algorithms 2-5, both models, variance formulas, incoherence, rotations, iteration conventions and applicable main-text footnotes before completing the paper census.'
])
(ROOT/'inventory-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
work=Path(prov['working_pdf']).parent
for n in [1,7,9,11,12,21,22,24,25,28]:shutil.copy2(work/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
shutil.copy2(work/'iteration-crop.png',ROOT/'evidence/iteration-crop.png')
(ROOT/'checkpoint.json').write_text(json.dumps(dict(paper_id=PID,stage='inventory_validated',status='in_progress',next_action='Resolve the PCA and general-subspace models, Assumptions 1-3, Algorithms 2-5, covariance formulas, incoherence and rotation definitions, stopping rules and main-text footnotes. Preserve the starred/natural iteration mismatch and inspect the starred population entry printed inside Algorithm 4. Then finalize and independently audit the census.',updated_at=review['reviewed_at']),indent=2)+'\n')
print('Saved and independently validated five complete main-text Theorems.')
