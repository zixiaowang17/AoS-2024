"""Preserve six formal Theorems and three separately labeled overview statements."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i05-p2167'
SHA='e16df8b32ca2250fd73e8e9d56aaafa49a771467015b5593da33bd35de477222'
URL='https://arxiv.org/pdf/2311.18613v2'
NUMBERS=['4.1-overview','5.8-overview','5.1-overview','3.1','4.1','5.1','5.4','5.7','5.8']
STATEMENTS=[r'''For $\mu$ verifying the assumptions of Model 1 and $\gamma\in[1,\beta+1]$, there exist theoretical classes of functions $\mathcal G$ and $\mathcal D_\gamma$ such that the GAN estimator $\widehat g$ of (1.3) verifies
\[
\mathbb E\left[d_{\mathcal H_1^\gamma}(\widehat g_{\#U},\mu)\right]\le C\log(n)^{C_2}\left(n^{-\frac{\beta+\gamma}{2\beta+d}}\vee n^{-\frac12}\right).
\]''',r'''For $\mu$ verifying the assumptions of Model 3, there exist tractable neural network classes $\mathcal G$ and $\mathcal D$ such that the GAN estimator $\widehat g$ of (1.3) verifies for all $\gamma\in[1,\beta+1]$ simultaneously:
\[
\mathbb E\left[d_{\mathcal H_1^\gamma}(\widehat g_{\#U},\mu)\right]\le C\log(n)^{C_2}\left(n^{-\frac{\beta+\gamma}{2\beta+d}}\vee n^{-\frac12}\right).
\]''',r'''Let $g,g^\star\in\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$ verifying the $K$-manifold and $K$-density regularity conditions. There exists constants $C,C_2>0$ such that if $d_{\mathcal H_1^{\beta+1}}(g_{\#U},g^\star_{\#U})\le C^{-1}$, then for all $\epsilon\in(0,1)$ and $\gamma\in[1,\beta+1]$, we have
\[
d_{\mathcal H_1^\gamma}(g_{\#U},g^\star_{\#U})\le C_2\log(\epsilon^{-1})^4\left(d_{\mathcal H_1^{\beta+1}}(g_{\#U},g^\star_{\#U})^{\frac{\beta+\gamma}{2\beta+1}}+\epsilon\right).
\]''',r'''If $g^\star\in\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$ and $\mathcal G\subset\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$, $\mathcal D\subset\mathcal H_1^\gamma(B^p(0,K),\mathbb R)$, then the GAN estimator (1.3) verifies
\[
\mathbb E\left[d_{\mathcal H_1^\gamma}(\widehat g_{\#U},g^\star_{\#U})\right]-\Delta_{\mathcal G}-\Delta_{\mathcal D}
\le C\min_{\delta\in[0,1]}\left\{\sqrt{\frac{(\delta+1/n)^2\log(n|\mathcal G_{1/n}||\mathcal D_{1/n}|)}n}+\frac1{\sqrt n}\left(1+\delta^{(1-\frac d{2\gamma})}+\log(\delta^{-1})\mathbf1_{\{2\gamma=d\}}\right)\right\}.
\]''',r'''For all $g^\star\in\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$ and $\gamma\in[1,\beta+1]$, the GAN estimator $\widehat g$ of (1.3) with $\mathcal G$ and $\mathcal D$ defined in (4.1) and (4.2), satisfies
\[
\mathbb E\left[d_{\mathcal H_1^\gamma}(\widehat g_{\#U},g^\star_{\#U})\right]\le C\log(n)^{C_2}\left(n^{-\frac{\beta+\gamma}{2\beta+d}}\vee n^{-\frac12}\right).
\]''',r'''Let $g,g^\star\in\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$ that verify the $K$-manifold regularity condition with $g^\star$ that verifies the $K$-density regularity condition of Definition 2.1. There exists constants $C,C_2>0$ such that if $d_{\mathcal H_1^{\beta+1}}(g_{\#U},g^\star_{\#U})\le C^{-1}$, then for all $\epsilon\in(0,1)$ and $\gamma\in[1,\beta+1]$, we have
\[
d_{\mathcal H_1^\gamma}(g_{\#U},g^\star_{\#U})\le C_2\log(\epsilon^{-1})^4\left(d_{\mathcal H_1^{\beta+1}}(g_{\#U},g^\star_{\#U})^{\frac{\beta+\gamma}{2\beta+1}}+\epsilon\right).
\]''',r'''For all $g^\star\in\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$ verifying the $K$-manifold and $K$-density regularity conditions of Definition 2.1, the GAN estimator $\widehat g$ of (1.3), with $\mathcal G$ and $\mathcal D$ defined in (5.1) and (5.3), satisfies
\[
\mathbb E\left[d_{\mathcal H_1^{\widetilde\beta+1}}(\widehat g_{\#U},g^\star_{\#U})\right]-\Delta_{\mathcal G}-\mathbb E[\Delta_{\mathcal D}^{\widehat g}]\le C\min_{\delta\in[0,1]}\left\{\sqrt{\frac{(\delta+1/n)^2\log(n|\mathcal G_{1/n}||(\mathcal D_{\mathcal G})_{1/n}|)}n}+\frac1{\sqrt n}\left(1+\delta^{(1-\frac d{2(\widetilde\beta+1)})}+\log(\delta^{-1})\mathbf1_{\{\beta+1=d/2\}}\right)\right\}.
\]''',r'''For all $g^\star\in\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$ verifying the $K$-manifold and $K$-density regularity conditions of Definition 2.1, the GAN estimator $\widehat g$ of (1.3), with $\mathcal G$ and $\mathcal D$ defined in (5.1) and (5.3), satisfies
\[
\mathbb E\left[d_{\mathcal H_1^{\widetilde\beta+1}}(\widehat g_{\#U},g^\star_{\#U})\right]\le C\log(n)^{C_2}n^{-\frac{2\widetilde\beta+1}{2\widetilde\beta+d}}.
\]''',r'''For all $g^\star\in\mathcal H_K^{\beta+1}(\mathbb T^d,\mathbb R^p)$ verifying the $K$-manifold and $K$-density regularity conditions of Definition 2.1, the GAN estimator $\widehat g$ (1.3), with $\mathcal G$ and $\mathcal D$ defined in (5.1) and (5.3), satisfies, for all $\gamma\in[1,\widetilde\beta+1]$,
\[
\mathbb E\left[d_{\mathcal H_1^\gamma}(\widehat g_{\#U},g^\star_{\#U})\right]\le C\log(n)^{C_2}\left(n^{-\frac{\beta+\gamma}{2\beta+d}}\vee n^{-\frac12}\right).
\]''']
def inventory():
    claims=[]
    for i,(n,s,p) in enumerate(zip(NUMBERS,STATEMENTS,[5,7,7,11,16,20,23,23,24]),1):
        overview=n.endswith('-overview');label='Theorem '+n.split('-')[0]
        claims.append(dict(claim_id=PID+'/T'+n,paper_id=PID,claim_kind='theorem',label=label,source_order=i,statement_original=s,occurrence_kind='overview_statement' if overview else 'formal_theorem',evidence=[dict(page=p,location=label+(' — bold labeled overview statement' if overview else ' — complete formal statement'))]))
    paper=dict(paper_id=PID,title='Wasserstein generative adversarial networks are minimax optimal distribution estimators',authors=['Arthur Stéphanovitch','Eddie Aamari','Clément Levrard'],version='arXiv:2311.18613v2; 12 Mar 2025',pdf_pages=83,pdf_sha256=SHA,source_url=URL,main_text_last_pdf_page=25,main_text_boundary=dict(location='Discussion ends on PDF page 25 before the Supplementary Material heading at y=373.77. Page-25 evidence is clipped at y=370. The separate supplement begins on page 27 and its appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False,method='Enumerate six small-cap formal THEOREM environments and three bold labeled overview statements in source order. Preserve the overview occurrences separately, including differences in assumptions and parameter ranges. Exclude theorem citations, Table 1 entries, proofs, Lemmas, Propositions and Corollaries.'))
    return dict(schema_version='statistical-theorem-inventory-v1',scope=dict(paper_count=1,theorem_scope='main_text_only',source_policy='Registered hash-verified local arXiv v2 dated March 2025; not represented as the final 2024 publication text. No replacement source and no appendix body.',normalization_policy='Preserve all original theorem wording and formulas. Normalize line wrapping and mathematical typesetting only. Retain the overview/formal differences, the printed beta versus tilde-beta indicator and the delta=0 endpoint in the minima.'),papers=[paper],claims=claims)
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(inventory(),indent=2,ensure_ascii=False)+'\n')
    print('Saved nine labeled theorem occurrences (six formal and three overview statements); source review is separate.')
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output-dir',type=Path);args=parser.parse_args()
    if args.output_dir:ROOT=args.output_dir.resolve()
    main()
