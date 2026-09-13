"""Reproduce all complete original main-text Theorems from the registered PDF."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1646'
SHA='051b72df6278997ad32edd271531e68b529cb1b1bc3f4e958806d9e7a91325bc'
claims=[]
def claim(n,pages,text):
    claims.append(dict(claim_id=PID+'/T'+str(n),paper_id=PID,claim_kind='theorem',label='Theorem '+str(n),source_order=n,
        statement_original=text.strip(),evidence=[dict(page=p,location='Theorem '+str(n)+'; complete original statement' if i==0 else 'Theorem '+str(n)+'; continuation and ending') for i,p in enumerate(pages)]))
claim(1,[11],r'''
We assume that Assumptions B1-B4 and C1-C2 hold, and that $g(\cdot)$ satisfies (3.17). Then, under the null, as $\min(m,p_1,p_2)\to\infty$, it holds that

(i)
\[
T_m^{\eta-1/2}\max_{1\le\tau\le T_m}\frac{|S_\tau|}{\tau^\eta}\xrightarrow{D^*}\sup_{0\le u\le1}\frac{|W(u)|}{u^\eta},\tag{3.22}
\]
for all $0\le\eta<1/2$;

(ii)
\[
P^*\left(\alpha_{T_m}\max_{1\le\tau\le T_m}\frac{|S_\tau|}{\tau^{1/2}}\le v+\beta_{T_m}\right)=\exp(-\exp(-v)),\tag{3.23}
\]
for all $-\infty<v<\infty$; and

(iii)
\[
r_{T_m}^{\eta-1/2}\max_{r_{T_m}\le\tau\le T_m}\frac{|S_\tau|}{\tau^\eta}\xrightarrow{D^*}\sup_{1\le u<\infty}\frac{|W(u)|}{u^\eta},\tag{3.24}
\]
for all $\eta>1/2$. All the results hold for almost all realisations of $\{X_t,1\le t\le T\}$.
''')
claim(2,[12,13],r'''
We assume that Assumptions B1-B4 and C1-C2 hold, and that $g(\cdot)$ satisfies (3.17). Then, under (3.7) and (3.9), as $\min(m,p_1,p_2)\to\infty$

(i) if
\[
\left(\frac{t^*}{T_m}\right)^{1-\eta}\frac{T_m^{1/2}}{\sqrt{\ln\ln T_m}}g\left(p_1^{1-\delta}\right)\to\infty,\tag{3.25}
\]
it holds that
\[
T_m^{\eta-1/2}\max_{1\le\tau\le T_m}\frac{|S_\tau|}{\tau^\eta}\xrightarrow{P^*}\infty,\tag{3.26}
\]
for all $0\le\eta<1/2$;

(ii) if
\[
\left(\frac{t^*}{T_m}\right)^{1/2}\frac{T_m^{1/2}}{(\ln\ln T_m)}g\left(p_1^{1-\delta}\right)\to\infty,\tag{3.27}
\]
under (3.7) it holds that
\[
P^*\left(\alpha_{T_m}\max_{1\le\tau\le T_m}\frac{|S_\tau|}{\tau^{1/2}}>v+\beta_{T_m}\right)=1,\tag{3.28}
\]
for all $-\infty<v<\infty$;

(iii) if
\[
\left(\frac{r_{T_m}}{T_m}\right)^{\eta-1/2}\left(\frac{t^*}{T_m}\right)^{1-\eta}\frac{T_m^{1/2}}{\sqrt{\ln\ln T_m}}g\left(p_1^{1-\delta}\right)\to\infty,\tag{3.29}
\]
under (3.7) it holds that
\[
(r_{T_m})^{\eta-1/2}\max_{r_{T_m}\le\tau\le T_m}\frac{|S_\tau|}{\tau^\eta}\xrightarrow{P^*}\infty,\tag{3.30}
\]
for all $\eta>1/2$. All the results hold for almost all realisations of $\{X_t,1\le t\le T\}$.
''')
claim(3,[13,14],r'''
We assume that Assumptions B1-B4 and C2 hold, and that $g(\cdot)$ satisfies (3.17). Then, under the null, as $\min(p_1,p_2,m)\to\infty$, it holds that
\[
\lim_{\min(p_1,p_2,m)\to\infty}P^*\left(\frac{Z_{T_m}-b_{T_m}}{a_{T_m}}\le v\right)=\exp(-\exp(-v)),\tag{3.32}
\]
for almost all realisations of $\{X_t,1\le t\le T\}$ and all $-\infty<v<\infty$. Under the alternatives (3.7) and (3.9), if it holds that
\[
\frac{g\left(p_1^{1-\delta}\right)}{\sqrt{\ln T_m}}\to\infty,\tag{3.33}
\]
as $\min(p_1,m)\to\infty$, then it follows that
\[
\lim_{\min(p_1,p_2,m)\to\infty}P^*\left(\frac{Z_{T_m}-b_{T_m}}{a_{T_m}}\le v\right)=0,\tag{3.34}
\]
for almost all realisations of $\{X_t,1\le t\le T\}$ and all $-\infty<v<\infty$.
''')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='Online Change-point Detection for Matrix-valued Time Series with Latent Two-way Factor Structure',
        authors=['Yong He','Xin-Bing Kong','Lorenzo Trapani','Long Yu'],version='arXiv:2112.13479v1, 27 December 2021',
        source_url='https://arxiv.org/pdf/2112.13479v1',pdf_pages=45,pdf_sha256=SHA,
        main_text_last_pdf_page=31,main_text_boundary=dict(location='References end on PDF page 31 with Yu et al. (2021), Journal of Econometrics, in press.., before Appendix A Further assumptions at y=322.86700439453125. Admitted evidence on this shared page stops at y=321.86700439453125.',shared_page_with_appendix=True),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(dict(schema_version='statistical-theorem-inventory-v1',
        scope=dict(theorem_scope='main_text_only',source_policy='Verified local arXiv v1 PDF; pages 1-30 and references above Appendix A on page 31 only. B1-B4 supplementary assumptions remain unresolved.'),
        papers=[paper],claims=claims),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
