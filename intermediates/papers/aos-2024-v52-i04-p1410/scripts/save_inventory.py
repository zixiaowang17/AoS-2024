"""Rebuild the manually transcribed main-text theorem inventory for this paper."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1410'
SHA='e9e5fd4e0096e3be7e7b07d083fd73818791feafd69a65676c289c0f63db6223'
claims=[]
def claim(number,page,text,title=None):
    claims.append(dict(claim_id=f'{PID}/T{number}',paper_id=PID,claim_kind='theorem',label=f'Theorem {number}'+(f' ({title})' if title else ''),source_order=len(claims)+1,statement_original=text.strip(),evidence=[dict(page=page,location=f'Theorem {number}, complete original statement')]))
claim('1',7,r'''
Suppose that there exists a statistic $V_n=v_n(X^n)$ such that
\[
\inf_{\boldsymbol\Pi_0,\boldsymbol\Pi_1}\operatorname{KL}(\boldsymbol\Pi_1^g\mathbf Q_g,\boldsymbol\Pi_0^g\mathbf P_g)=\min_{\boldsymbol\Pi_0,\boldsymbol\Pi_1}\operatorname{KL}(\boldsymbol\Pi_1^g\mathbf Q_g^{V_n},\boldsymbol\Pi_0^g\mathbf P_g^{V_n})<\infty,\tag{9}
\]
where $\boldsymbol\Pi_0$ and $\boldsymbol\Pi_1$ are probability distributions on $G$. Let $\boldsymbol\Pi_0^\star$ and $\boldsymbol\Pi_1^\star$ be probability distributions that achieve the minimum on the right hand side. Then
\[
\max_{T_n\text{ e-stat.}}\inf_{g\in G}\mathbf E_g^{\mathbf Q}[\ln T_n]=\operatorname{KL}(\boldsymbol\Pi_1^{\star g}\mathbf Q_g^{V_n},\boldsymbol\Pi_0^{\star g}\mathbf P_g^{V_n}),
\]
and the maximum on the left is achieved by $T_n^*$ as given by
\[
T_n^*:=\frac{\int q_g^{V_n}(v_n(X^n))d\boldsymbol\Pi_1^\star(g)}{\int p_g^{V_n}(v_n(X^n))d\boldsymbol\Pi_0^\star(g)}.
\]
In other words, the e-statistic $T_n^*$ is GROW for testing $\{\mathbf P_g\}_{g\in G}$ against $\{\mathbf Q_g\}_{g\in G}$.
''','GHK Theorem 1 in Section 4.3')
claim('2',10,r'''
Let $M_n=m_n(X^n)$ be a maximally invariant statistic under the action of the group $G$ on $\mathcal X^n$. Assume that $G$ is amenable, that Assumption 1 holds, and that there is $\varepsilon>0$ such that
\[
\mathbf E_1^{\mathbf Q}\left[\left|\ln\frac{q_1(X^n)}{p_1(X^n)}\right|^{1+\varepsilon}\right],\mathbf E^{\mathbf Q^{M_n}}\left[\left|\ln\frac{q^{M_n}(M_n)}{p^{M_n}(M_n)}\right|^{1+\varepsilon}\right]<\infty,\tag{14}
\]
where the subindex 1 refers to the unit element of $G$. Then
\[
\inf_{\boldsymbol\Pi_0,\boldsymbol\Pi_1}\operatorname{KL}(\boldsymbol\Pi_1^g\mathbf Q_g,\boldsymbol\Pi_0^g\mathbf P_g)=\operatorname{KL}(\mathbf Q^{M_n},\mathbf P^{M_n}),
\]
where the infimum is over all pairs $(\boldsymbol\Pi_0,\boldsymbol\Pi_1)$ of probability distributions on $G$.
''')
claim('4',10,r'''
Suppose that Part 3 of Assumption 1 is satisfied and that, for each $g\in G$, there exists $h\in G$ such that $\operatorname{KL}(\mathbf Q_g,\mathbf P_h)$ is finite. Then the map defined by
\[
g\mapsto\sup_{T_n\text{ e-stat.}}\mathbf E_g^{\mathbf Q}[\ln T_n]
\]
is constant. Consequently, any maximizer of (8) also maximizes (10), that is, an e-statistic is GROW if and only if it is relatively GROW for the hypothesis testing problem (4).
''')
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    paper=dict(paper_id=PID,title='E-statistics, group invariance and anytime-valid testing',authors=['Muriel Felipe Pérez-Ortiz','Tyron Lardy','Rianne de Heide','Peter D. Grünwald'],version='arXiv:2208.07610v2, 17 October 2023',source_url='https://arxiv.org/pdf/2208.07610v2',pdf_pages=31,pdf_sha256=SHA,main_text_last_pdf_page=23,main_text_boundary=dict(location='Main text and references end on PDF page 23; Appendix A begins on the separate PDF page 24. Appendix bodies are excluded.',shared_page_with_appendix=False),intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    data=dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only',source_policy='Verified registered arXiv v2 PDF, main text and references on pages 1-23; appendices excluded.'),papers=[paper],claims=claims)
    ROOT.mkdir(parents=True,exist_ok=True);(ROOT/'theorem-inventory.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
