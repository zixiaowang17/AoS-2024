"""Retain source passages and statement dependencies; build the paper census."""
import copy,json,subprocess,sys
from pathlib import Path
from save_inventory import ROOT,PID
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
MOMENT=r'''\[
\kappa_p:=\sup_{v\in\mathbb R^d,\,\langle v,\Sigma v\rangle=1}\mathbb E[|\langle X,v\rangle|^p]^{\frac1p}.
\]'''
ASSUMPTION=r'''$X_1,\ldots,X_n$ are i.i.d. copies of a random element $X$ of $\mathbb R^d$ satisfying $\mathbb E[\|X\|^p]<+\infty$ for some $p\geq4$. We assume $\mathbb E[X]=0$, that the covariance $\Sigma$ of $X$ is non-null, and set
'''+MOMENT+r'''
Finally, we let $Y_1,\ldots,Y_n$ denote other random elements of $\mathbb R^d$ that satisfy the following condition:
\[
\#\{i\in[n]:Y_i\ne X_i\}\leq\eta n
\]
for some $\eta\in[0,1)$.'''
def evidence(page,location):return [dict(page=page,location=location)]
def entries():
    specs=[
      ('D1','covariance matrix',r'''In this paper, we are interested in estimating the covariance matrix $\Sigma=\mathbb E[XX^\top]$ of a random vector $X\in\mathbb R^d$ with zero mean from independent and identically distributed (i.i.d.) copies $X_1,\ldots,X_n$ of $X$.''',1,'Section 1 — Covariance matrix','definition',[],[r'\Sigma=\mathbb E[XX^\top]'],None,'Covariance of the zero-mean population vector. This is not the sample covariance or the covariance of the contaminated observations.'),
      ('D2','i.i.d. sample with contamination',ASSUMPTION,3,'Assumption 1.2 (i.i.d. sample with contamination)','assumption',['D1','D3'],[r'\mathbb E[\|X\|^p]<+\infty',r'\#\{i\in[n]:Y_i\ne X_i\}\leq\eta n'],'Assumption 1.2 (i.i.d. sample with contamination).','Original complete assumption: iid clean observations, finite p-th norm moment for p>=4, zero mean, nonzero covariance, standardized moment constant and bounded replacements. Y need not be iid or independent of X.'),
      ('D3','moment condition',MOMENT,3,'Assumption 1.2 — Moment constant','definition',['D1'],[r'\kappa_p',r'\kappa_4',r'\langle v,\Sigma v\rangle=1'],r'''The sole requirement is that the one-dimensional marginals satisfy a moment condition, $\kappa_p^2$ is referred to as the $L^p-L^2$ hypercontractivity constant by [Abdalla and Zhivotovskiy, 2022] and elsewhere in the literature.''','The displayed definition is kappa_p, whereas the adjacent text calls its square the hypercontractivity constant. Kappa_4 in the theorem is this moment definition at exponent four. The direction is normalized by population variance, not Euclidean length.'),
      ('D4','stable rank',r'''The stable rank of a non-zero matrix $M\in\mathbb R^{d\times d}_{\geq0}$ is given by:
\[
r(M)=\frac{\operatorname{tr}(M)}{\|M\|}.
\]''',8,'Section 2.1 — Stable rank','definition',[],[r'r(M)',r'r(\Sigma)'],None,'Trace divided by operator norm for a nonzero symmetric positive semidefinite matrix. In the theorem M=Sigma; this is neither algebraic rank nor the squared Frobenius-to-operator ratio sometimes given the same name.')]
    out=[]
    for lid,term,s,page,heading,kind,deps,symbols,context,boundary in specs:
        m=dict(paper_id=PID,local_id=lid,local_label=heading,source_kind=kind,source_heading=heading,relation='exact',statement_original=s,depends_on=deps,evidence=evidence(page,heading),highlight_symbols=symbols,highlight_phrases=['Assumption 1.2'] if lid=='D2' else [])
        kw=dict(paper_id=PID,local_id=lid,kind='term',source_text=term,label=term[0].upper()+term[1:])
        if context:
            m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=evidence(page,'Original source naming context'))];kw['context_id']=lid+'/name'
        out.append(dict(interface_id=PID+'/'+lid,rank_group='all',name=kw['label'],lean_role='definition',type_shape=boundary,semantic_boundary=boundary,members=[m],source_keywords=[kw],central_claim_uses=[],dependencies=[],theorem_explanations={}))
    return out
DIRECT={
 'D1':'The target Sigma and its operator norm are the covariance of the clean zero-mean population vector, as defined in Section 1.',
 'D2':'Theorem 1.3 explicitly requires Assumption 1.2 and evaluates the estimator on its contaminated observations Y_1,...,Y_n; its eta<1/2 restriction strengthens the assumption eta<1.',
 'D3':'The cutoff uses kappa_4^4, the sampling-error terms use kappa_4^2, and the contamination term uses kappa_p^2. All are instances or powers of the moment constant defined in Assumption 1.2.',
 'D4':'The sample-size condition and error rate use r(Sigma), obtained by applying the Section 2.1 stable-rank formula to the nonzero covariance matrix.'}
def ambient():
    aux=[
      dict(local_id='A1',statement_original=r'''In what follows, $\mathbb R^{d\times d}_{\geq0}$ is the set of $d\times d$ symmetric positive semidefinite matrices, and $\|\cdot\|_{\mathrm{op}}$ is the operator norm.''',evidence=evidence(3,'Section 1.2 — Notation preceding Theorem 1.3'),scope_note='The theorem estimator is explicitly PSD-valued; these standard matrix notions remain ambient.'),
      dict(local_id='A2',statement_original=r'''The cardinality of a finite set $A$ is denoted by $\#A$. For real numbers $x,y$, $x_+:=\max\{x,0\}$, and $x\wedge y:=\min\{x,y\}$ and $x\vee y:=\max\{x,y\}$. For $n\in\mathbb N$, $[n]:=\{i\in\mathbb N:1\leq i\leq n\}$ is the set of numbers from $1$ to $n$.''',evidence=evidence(8,'Section 2.1 — Finite-set and real-number notation'),scope_note='Resolves the replacement-count condition; no integer rounding is inserted into its original bound.'),
      dict(local_id='A3',statement_original=r'''We use the standard euclidean norm $\|\cdot\|$ and inner product $\langle\cdot,\cdot\cdot\rangle$ over $\mathbb R^d$. The unit sphere this space is denoted by $\mathbb S^{d-1}:=\{u\in\mathbb R^d:\|u\|=1\}$. Letting $\mathbb R^{d\times d}$ denote the space of $d\times d$ matrices, we also use $\|\cdot\|$ to denote the operator norm over this space, and $\operatorname{tr}(\cdot)$ denotes the trace. $\mathbb R^{d\times d}_{\geq0}$ is the subset consisting of symmetric positive semidefinite matrices.''',evidence=evidence(8,'Section 2.1 — Norms and matrix notation'),scope_note='The source overloads the vector and matrix norm. Its stable rank uses the operator norm; the moment definition uses the Euclidean inner product. The extra dot and missing preposition in the original prose are retained.'),
      dict(local_id='A4',statement_original=r'''Assumption 1.2 also includes the possibility of sample contamination. That is, all estimators we consider will be computed on a random sample, denoted as $Y_1,\ldots,Y_n$, which may differ from the original sample $X_1,\ldots,X_n$ by at most $\eta n$ indices.''',evidence=evidence(3,'Paragraph interpreting Assumption 1.2'),scope_note='Replacements apply to the observed sample; independence applies to the clean X observations only.')]
    issues=[
      dict(issue_id='slash-cutoff',description='The theorem prints eta<=1/C kappa_4^4 without denominator parentheses. Preserve that typography. The proof on page 26 explicitly says eta*kappa_4^4 must be small, supporting the reciprocal-of-product interpretation; this interpretation is separate from the quotation.',evidence=evidence(4,'Theorem 1.3 cutoff')+evidence(26,'Opening paragraph of its proof')),
      dict(issue_id='non-null-covariance',description='Non-null means nonzero covariance, not positive definite. Singular nonzero covariance is not excluded. The moment supremum restricts to directions with v-transpose Sigma v=1, and the stable-rank denominator is nonzero.',evidence=evidence(3,'Assumption 1.2')+evidence(8,'Stable rank')),
      dict(issue_id='moment-constant-square',description='The formula defines kappa_p as a p-th root of a standardized moment; the following prose calls kappa_p squared the hypercontractivity constant. These are not interchangeable numbers.',evidence=evidence(3,'Moment definition and adjacent prose')),
      dict(issue_id='existential-estimator',description='Theorem 1.3 binds a measurable PSD-valued estimator depending on alpha, eta and n. The trimmed estimates and their selection rule implement the proof; they are not additional statement dependencies or assumptions about an estimator supplied to the theorem.',evidence=evidence(4,'Theorem 1.3')+evidence(26,'Proof of Theorem 1.3')),
      dict(issue_id='sample-size-wording',description='The theorem states n>=C(r(Sigma)+log(2/alpha)) and says only that a constant C>0 exists. The proof later uses a sufficient threshold involving D*kappa_p^p. This census preserves the theorem exactly and does not add a moment-dependent factor or certify that the proof establishes the printed threshold.',evidence=evidence(4,'Printed sample-size threshold')+evidence(26,'Temporary k-star construction')),
      dict(issue_id='result-2-2-label',description='Several main-text citations say Theorem 2.2, but the actual heading is Proposition 2.2. It is excluded by the printed-label inventory rule, and its PAC-Bayesian definitions are proof-only for Theorem 1.3.',evidence=evidence(6,'Citation to Theorem 2.2')+evidence(10,'Proposition 2.2 heading')),
      dict(issue_id='appendix-variant',description='The paragraph after Theorem 1.3 mentions an Appendix D weak-moment variant. It is not a main-text Theorem environment, and the appendix body is excluded.',evidence=evidence(4,'Appendix D reference after the theorem'))]
    return dict(paper_id=PID,status='extracted',unranked_auxiliary_passages=aux,source_issues=issues,ambient_prerequisites=['Finite-dimensional real vectors and matrices; measurable estimators and random elements; expectation, probability, operator norm, trace, cardinality and natural logarithm retain their stated mathematical meanings.','The p in the theorem comes from Assumption 1.2 and satisfies p>=4. Kappa_4 denotes the same standardized-moment definition with exponent four.','The confidence parameter, contamination level, sample size and estimator are bound by the theorem. The probability is over the clean sample and any allowed replacement mechanism, without imposing independence on the replacements.'],statement_local_bindings={'T1.3':'C>0 is existential before the fixed confidence, n and eta. The estimator is then existential and measurable with PSD-valued output. X and Sigma, p, kappa_p, and the contaminated Y sample come from Assumption 1.2. The two square-root error terms and eta exponent are preserved separately. The covariance and stable rank have no positive-definiteness requirement.'},source_claim_references=[])
def write(n,d):(ROOT/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def main():
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);xs=entries()
    write('source-passages.json',dict(paper_id=PID,members=[m for x in xs for m in x['members']]))
    write('interface-extraction.json',dict(paper_id=PID,interfaces=xs))
    write('ambient-prerequisites.json',ambient())
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All printed main-text Theorems, with source-keyword names and distinct local source entries.',build_order_policy='Source-backed local definition prerequisites; no proof-only estimator construction or concentration machinery.')
    data['interfaces']=xs;c=data['claims'][0];c['depends_on']=list(DIRECT)
    for x in xs:
        lid=x['members'][0]['local_id'];ev=c['evidence']+x['members'][0]['evidence']
        x['central_claim_uses']=[dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[lid],evidence=ev)]
    derived=canonical_dependencies(data)
    for x in xs:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in xs:
        lid=x['members'][0]['local_id'];rel=x['related_theorems'][0]
        assert rel['relation']=='direct' and rel['via_local_ids']==[lid]
        x['theorem_explanations'][c['claim_id']]=dict(paper_id=PID,via_local_ids=[lid],text=DIRECT[lid],evidence=c['evidence']+x['members'][0]['evidence'])
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    write('unfinalized-census.json',data)
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
if __name__=='__main__':main()
