"""Transcribe statement prerequisites from the inspected pinned preprint, without supplements."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
interfaces=[];members={};edges={}
def add(lid,term,body,pages,heading,deps=None,*,kind='definition',symbols=(),phrases=(),context=None,note=None,shape):
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,
        statement_original=body.strip(),relation='exact',depends_on=list(deps or {}),
        evidence=[dict(page=p,location=heading) for p in pages],highlight_symbols=list(symbols),highlight_phrases=list(phrases))
    if note:m['variant_note']=note
    terms=term if isinstance(term,list) else [term];keywords=[]
    for t in terms:
        key=dict(paper_id=PID,local_id=lid,source_text=t,label=t[0].upper()+t[1:],kind='term')
        if t not in body:
            assert context and t in context,(lid,t)
            m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=m['evidence'])];key['context_id']=lid+'/name'
        keywords.append(key)
    interfaces.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=' · '.join(k['label'] for k in keywords),
        lean_role='hypothesis' if kind in ('condition','assumption') else 'definition',type_shape=shape,semantic_boundary=shape,
        members=[m],source_keywords=keywords,central_claim_uses=[],dependencies=[],theorem_explanations={}))
    members[lid]=m;edges[lid]=deps or {}
add('D1','filtration',r'''
Let $(\Omega,\mathcal A)$ be a measurable space and $\mathcal P$ some set of probability distributions on $(\Omega,\mathcal A)$. Note that $(\Omega,\mathcal A,\mathcal P)$ is to be understood in an abstract sense and it is not supposed to be completely known in advance. We assume that the data follows some unknown distribution $\mathbb P\in\mathcal P$. The hypotheses $(H_i)_{i\in\mathbb N}$ can be formally considered as subsets of $\mathcal P$ and by testing $H_i$, we want to examine whether $\mathbb P\in H_i$. Unless otherwise stated, equalities and inequalities involving random variables should be understood to hold almost surely for all $\mathbb P\in\mathcal P$. We further assume that a filtration $\mathbb F=(\mathcal F_i)_{i\in\mathbb N}$ (increasing sequence of $\sigma$-fields) is given, where $\mathcal F_i\subseteq\mathcal A$ defines the information that the test decision for $H_i$ is allowed to depend on.
''',[2,3],'Section 2 — experiment, hypotheses and information filtration',kind='source_passage',phrases=['filtration'],symbols=[r'\mathbb F=(\mathcal F_i)_{i\in\mathbb N}',r'\mathbb P\in\mathcal P'],shape='A fixed abstract experiment with a model of possible probability laws, hypotheses as subsets of that model, and increasing available information. Random equalities use the paper’s almost-sure-for-every-law convention. The text does not provide a separate random-hypothesis formalism or a common-null-set convention across uncountably many subsets.')
add('D2','Online multiple testing procedure',r'''
An online multiple testing procedure (hereinafter referred to as online procedure for short) for $\mathcal H=(H_i)_{i\in\mathbb N}$ is a sequence of test decisions $\boldsymbol d=(d_i)_{i\in\mathbb N}$, where each $d_i$ is a random variable with values in $\{0,1\}$ that is measurable with respect to $\mathcal F_i$. If $d_i=1$, we conclude that $H_i$ is rejected and if $d_i=0$, that $H_i$ is accepted.
''',[3],'Definition 2.1 (Online multiple testing procedure)',{'D1':'The hypotheses and their available sigma-fields are those of the abstract experiment.'},context='Definition 2.1 (Online multiple testing procedure).',phrases=['online multiple testing procedure'],symbols=[r'\boldsymbol d=(d_i)_{i\in\mathbb N}',r'\mathcal F_i'],shape='Binary decisions adapted to the current available information. This definition alone imposes no error-rate bound, no independent p-values and no requirement that the decision already be measurable at the preceding time.')
add('D3','familywise error rate',r'''
We denote by $I_0^{\mathbb P}:=\{i\in\mathbb N:\mathbb P\in H_i\}$ and $I_1^{\mathbb P}:=\mathbb N\setminus I_0^{\mathbb P}$ the index sets of true and false null hypotheses, if $\mathbb P$ was the true distribution, respectively. Furthermore, for all $i\in\mathbb N$, we define $v_{\mathbb P}(i):=\sum_{j\leq i,j\in I_0^{\mathbb P}}d_j$ as the number of falsely rejected hypotheses up to step $i\in\mathbb N$ and set $v_{\mathbb P}:=\lim_{i\to\infty}v_{\mathbb P}(i)$. With this, we define the familywise error rate (FWER) at time $i\in\mathbb N$ and over all hypotheses as
\[
\operatorname{FWER}_{\mathbb P}(i):=\mathbb P(v_{\mathbb P}(i)>0)\quad\text{and}\quad\operatorname{FWER}_{\mathbb P}:=\mathbb P(v_{\mathbb P}>0)\qquad(\mathbb P\in\mathcal P).\tag{1}
\]
We aim for strong control of the FWER at each time $i\in\mathbb N$, which means that for some pre-specified $\alpha\in(0,1)$, we have $\operatorname{FWER}_{\mathbb P}(i)\leq\alpha$ for all $i\in\mathbb N$ and $\mathbb P\in\mathcal P$. Note that this is equivalent to requiring $\operatorname{FWER}_{\mathbb P}\leq\alpha$ for all $\mathbb P\in\mathcal P$,
''',[3],'Section 2 — FWER and strong control, equation (1)',{'D1':'The true-null set depends on the law in the model and the fixed hypothesis subsets.'},phrases=['familywise error rate','strong control'],symbols=[r'I_0^{\mathbb P}',r'\operatorname{FWER}_{\mathbb P}'],shape='Probability of at least one rejection of a true null over the entire infinite sequence, uniformly bounded over model laws. The increasing false-rejection count may be infinite. Adaptedness is a separate procedure property; the event must still be measurable for the probability to be defined.')
add('D4','intersection hypothesis',r'''
For a potentially infinite index set $I\subseteq\mathbb N$, we denote the corresponding intersection hypothesis and intersection test by $H_I=\bigcap_{i\in I}H_i$ and $\phi_I$, respectively. Each $\phi_I$ is a random variable with values in $\{0,1\}$ such that $H_I$ is rejected by $\phi_I$, if $\phi_I=1$, and accepted, if $\phi_I=0$.
''',[3],'Section 3 — intersection hypotheses and binary tests',{'D1':'Each intersection is a subset of the same model of possible laws.'},phrases=['intersection hypothesis','intersection test'],symbols=[r'H_I=\bigcap_{i\in I}H_i',r'\phi_I'],shape='Intersection hypotheses for every subset of the positive integers, including infinite subsets, and their binary measurable tests. The source separately fixes the empty-index test to zero. This bare definition does not require online measurability or a level bound.')
members['D4']['application_context']=[dict(text=r'where we always set $\phi_\varnothing=0$.',evidence=[dict(page=3,location='Section 3 — empty-intersection test convention')])]
add('D5','online intersection test',r'''
We say that $\phi_I$, $I\subseteq\mathbb N$, is an online intersection test, if $\phi_I$ is measurable with respect to $\mathcal F_{\sup(I)}$, where $\mathcal F_\infty=\mathcal A$.
''',[3],'Section 3 — online measurability of intersection tests',{'D4':'The property concerns the binary test of the indexed intersection.','D1':'The endpoint sigma-field is the filtration field at sup I, with the total field used for infinite I.'},phrases=['online intersection test'],symbols=[r'\mathcal F_{\sup(I)}',r'\mathcal F_\infty=\mathcal A'],shape='Finite intersections can use information through their last index; infinite intersections can use the total sigma-field. This is adaptedness of a single intersection test, not the separate across-intersection predictability condition. The empty test is fixed separately, avoiding an unspecified F_sup(empty).')
add('D6','α-level intersection test',r'''
Furthermore, $\phi_I$ is an α-level intersection test, if $\mathbb P(\phi_I=1)\leq\alpha$ for all $\mathbb P\in H_I$.
''',[3],'Section 3 — level of an intersection test',{'D4':'The rejection probability is bounded only under laws in the relevant intersection null.'},phrases=['α-level intersection test'],symbols=[r'\mathbb P(\phi_I=1)\leq\alpha'],shape='A marginal level-alpha guarantee over the intersection-null model. It is not conditional validity given the past and is not itself a familywise guarantee for an arbitrary collection of separate individual tests.')
add('D7','Predictable family of online intersection tests',r'''
A family of online intersection tests $\boldsymbol\phi=(\phi_I)_{I\subseteq\mathbb N}$ is called predictable, if for all $i\in\mathbb N$ and $I\subseteq\{1,\ldots,i\}$ holds that:
\[
\phi_I=1\text{ implies }\phi_K=1\text{ for all }K=I\cup J\text{ with }J\subseteq\{j\in\mathbb N:j>i\}.
\]
''',[3],'Definition 3.1 (Predictable family of online intersection tests)',{'D5':'The family consists of online intersection tests; predictability adds stability under adjoining future indices.'},context='Definition 3.1 (Predictable family of online intersection tests).',phrases=['Definition 3.1'],symbols=[r'K=I\cup J',r'\phi_I=1\text{ implies }\phi_K=1'],shape='Rejection of a finite intersection persists when future indices are adjoined, including infinitely many future indices. It need not persist when omitted past indices are inserted. This named property differs from ordinary stochastic-process predictability or past-measurability of a significance threshold.')
interfaces[-1]['lean_role']='predicate'
add('D8','closed procedure',r'''
the closed procedure $\boldsymbol d^\phi=(d_i^\phi)_{i\in\mathbb N}$ based on $\boldsymbol\phi$ defined by
\[
d_i^\phi=\min\{\phi_I:I\subseteq\mathbb N\text{ with }i\in I\}
\]
''',[3],'Theorem 3.2 — inline definition of the closed procedure',{'D4':'An individual decision requires rejection by every intersection test containing its index.'},kind='theorem_excerpt',phrases=['closed procedure'],symbols=[r'd_i^\phi=\min\{\phi_I'],shape='A binary minimum over all subsets containing the current index. There are uncountably many such subsets, so measurability of this minimum is not automatic from separate measurability of every test. The later predictable case reduces to finitely many intersections; the arbitrary-family assertion retains its unstated measurability convention.')
add('D9','consonant',r'''
A family of intersection tests $\boldsymbol\phi=(\phi_I)_{I\subseteq\mathbb N}$ is consonant [9], if for all $I\subseteq\mathbb N$:
\[
\phi_I=1\text{ implies }\exists i\in I:\phi_J=1\quad\forall J\subseteq I\text{ with }i\in J.\tag{2}
\]
''',[4],'Section 3.1 — consonance, equation (2)',{'D4':'The condition compares tests for one intersection and all its sub-intersections containing a witnessing index.'},phrases=['consonant'],symbols=[r'\exists i\in I:',r'\forall J\subseteq I'],shape='A rejected intersection has an index that survives all sub-intersection tests within it. The witness may depend on the intersection and outcome. This does not impose arbitrary superset rejection; the latter would be a stronger monotonicity property.')
interfaces[-1]['lean_role']='predicate'
add('D10','p-values',r'''
Most existing online multiple testing procedures are defined based on p-values $(p_i)_{i\in\mathbb N}$ for the individual hypotheses $(H_i)_{i\in\mathbb N}$ [8, 17, 36]. Each p-value $p_i$ can be considered as a random variable with values in $[0,1]$ that is measurable with respect to $\mathcal F_i$. It is assumed that all p-values are valid, which means $\mathbb P(p_i\leq x)\leq x$ for all $\mathbb P\in H_i$ and $x\in[0,1]$.
''',[7],'Section 4 — adapted valid p-values',{'D1':'Each p-value concerns its hypothesis subset and is available in the corresponding information field.'},phrases=['p-values'],symbols=[r'\mathbb P(p_i\leq x)\leq x',r'p_i'],shape='Adapted p-values with marginal superuniformity under their individual nulls. The general theorem does not assume independence or conditional superuniformity; an alpha-level property for the constructed intersection tests is a separate hypothesis.')
add('D11','online α-adjustment',r'''
Using p-values, a null hypothesis $H_i$ is rejected if $p_i\leq\alpha_i$, where $\alpha_i\in[0,1)$ is the individual significance level for $H_i$. We call a sequence $(\alpha_i)_{i\in\mathbb N}$ α-adjustment and the multiple testing procedure $\boldsymbol d=(d_i)_{i\in\mathbb N}$ with $d_i=\mathbb 1\{p_i\leq\alpha_i\}$ α-adjustment procedure. An α-adjustment defines an online procedure, if $\alpha_i$ is measurable with respect to $\mathcal F_i$. In this case, we refer to it as online α-adjustment.
''',[7],'Section 4 — online significance-level adjustment',{'D10':'Decisions compare the current valid p-value with its threshold.','D2':'An online procedure means a decision measurable with respect to the current information field.'},phrases=['online α-adjustment'],symbols=[r'\alpha_i\in[0,1)',r'd_i=\mathbb 1\{p_i\leq\alpha_i\}'],shape='Current-information-measurable thresholds in [0,1), with equality causing rejection. The source allows dependence on the current p-value; measurability does not by itself guarantee any error rate. A preceding-time threshold restriction is only an example later in the paragraph.')
add('D12','online sub α-adjustment',r'''
One can also use α-adjustments to test intersection hypotheses $H_I$, $I\subseteq\mathbb N$. In this case, we only require an individual significance level $\alpha_i^I$ for each $H_i$ with $i\in I$. We define $\boldsymbol\alpha_I=(\alpha_i^I)_{i\in I}$ as online sub α-adjustment, if $\alpha_i^I$ is measurable regarding $\mathcal F_i$ for all $i\in I$. With this, each $\boldsymbol\alpha_I$ defines an online intersection test $\phi_I$ by
\[
\phi_I=\mathbb 1\{\exists i\in I:p_i\leq\alpha_i^I\}.\tag{3}
\]
''',[7],'Section 4 — sub-adjustments and intersection tests, equation (3)',{'D11':'Each subfamily uses the same individual-threshold range and current-information measurability convention as an online alpha-adjustment.','D4':'The constructed binary decision tests the intersection indexed by I.'},phrases=['online sub α-adjustment'],symbols=[r'\phi_I=\mathbb 1\{\exists i\in I:p_i\leq\alpha_i^I\}',r'\boldsymbol\alpha_I'],shape='Thresholds indexed by members of a possibly infinite intersection and the countable union of their rejection events. The empty-index union gives zero. Separate measurability of thresholds supplies an online intersection test, while level-alpha control is an explicit additional hypothesis in Theorem 4.2.')
add('D13','Predictable family of online sub α-adjustments',r'''
A family of online sub α-adjustments $(\boldsymbol\alpha_I)_{I\subseteq\mathbb N}$ is called predictable, if for all $I\subseteq\{1,\ldots,i\}$ and $K=I\cup J$ with $J\subseteq\{k\in\mathbb N:k>i\}$ it holds that $\alpha_j^I=\alpha_j^K$ for all $j\in I$.
''',[7],'Definition 4.1 (Predictable family of online sub α-adjustments)',{'D12':'The condition compares the threshold families used to construct each intersection test.'},context='Definition 4.1 (Predictable family of online sub α-adjustments).',phrases=['Definition 4.1'],symbols=[r'\alpha_j^I=\alpha_j^K',r'K=I\cup J'],shape='Adjoining future indices leaves the thresholds of existing members unchanged. This equality condition is stronger than mere rejection persistence from Definition 3.1. It is not replaced by threshold inequalities or by measurability with respect to the past. The universal time index i is implicit in the source sentence.')
interfaces[-1]['lean_role']='predicate'
(ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=members,local_dependency_reasons=edges),indent=2,ensure_ascii=False)+'\n')
(ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
print(f'Saved {len(interfaces)} source interfaces.')
