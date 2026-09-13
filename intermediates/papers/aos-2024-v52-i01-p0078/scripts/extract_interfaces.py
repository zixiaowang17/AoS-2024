"""Main-text source extraction for StarTrek. All dependency choices are reviewed input."""
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
PID=ROOT.name
SOURCE=(ROOT/'evidence/main-only.tex').read_text()
MACROS=re.sub(r'(?<!\\)%[^\n]*','',(ROOT/'evidence/macros.tex').read_text())
REFS={'eq:problem_setup':'2.1','eq:T_E':'2.2','eq:BHq_alpha':'2.3','algo:skipdown':'1','algo:startrek':'2',
      'eq:ccb_max':'3.1','eq:ccb_sparse_unitvar':'3.2','eq:mul_linear_model':'4.1','eq:dlasso':'4.2',
      'eq:optimization':'4.3','eq:dlasso_normal':'4.4','eq:scaled_lasso':'4.5','eq:dlasso_chat':'4.6',
      'eq:dlasso_quantile_valid':'4.7','eq:strong_Y_set':'4.8','eq:ggm_tdTheta':'5.1','eq:ggm_chat':'5.2',
      'eq:dep_term_set':'5.3','eq:cond1':'5.4','eq:cond2':'5.5','eq:ggm_gen':'6.1',
      'asp:dlasso':'4.1','asp:tradeoff_fdp':'5.1','asmp:zeta12':'6.1','asp:tradeoff_fdp_gen':'6.2',
      'sec:method':'2','sec:startrek':'2.1','sec:bipartite_selection':'4','sec:hub_selection':'5'}
CITES={'javanmard2014confidence':'39','javanmard2014hypothesis':'40','sun2012scaled':'77',
       'friedman2008sparse':'28','cai2011constrained':'10','chernozhukov2013gaussian':'17'}

def passage(start,end,source=SOURCE):
    a=source.index(start)
    return source[a:source.index(end,a)].strip()

def env(kind,contains):
    found=[m[1] for m in re.finditer(r'\\begin\{'+kind+r'\}(.*?)\\end\{'+kind+r'\}',SOURCE,re.S) if contains in m[1]]
    assert len(found)==1,(kind,contains,len(found))
    return found[0].strip()

def convert(raw):
    text=raw.replace(r'\independent',r'\mathrel{\perp\!\!\!\perp}')
    text=re.sub(r'\\eqref\{([^}]+)\}',lambda m:'('+REFS[m[1]]+')',text)
    text=re.sub(r'\\ref\{([^}]+)\}',lambda m:REFS[m[1]],text)
    text=re.sub(r'\\cite\{([^}]+)\}',lambda m:'['+', '.join(sorted([CITES[x] for x in m[1].split(',')],key=int))+']',text)
    def display(m):
        kind,body=m[1],m[2]
        labels=re.findall(r'\\label\{([^}]+)\}',body)
        numbered=r'\nonumber' not in body
        body=re.sub(r'\\label\{[^}]+\}|\\nonumber','',body).strip()
        tag=''
        if numbered and labels:
            assert len(labels)==1,labels
            tag=r'\tag{'+REFS[labels[0]]+'}'
        if '&' in body or r'\\' in body:
            body=r'\begin{aligned}'+body+r'\end{aligned}'
        return r'\['+body+tag+r'\]'
    text=re.sub(r'\\begin\{(equation|align|eqnarray)\}(.*?)\\end\{\1\}',display,text,flags=re.S)
    text=re.sub(r'\\label\{[^}]+\}','',text)
    text=re.sub(r'\\vspace\{[^}]+\}','',text)
    result=subprocess.run(['pandoc','-f','latex','-t','markdown','--wrap=none'],text=True,
        input=MACROS+'\n\\begin{document}\n'+text+'\n\\end{document}',capture_output=True,check=True).stdout.strip()
    result=result.replace(r'\bm{',r'\boldsymbol{').replace(r'\mathds{1}',r'\mathbb{1}')
    result=re.sub(r'\\\[([0-9, ]+)\\\]',r'[\1]',result)
    assert '\\ref{' not in result and 'reference-type' not in result
    return result

def symbol(raw):
    x=convert('$'+raw+'$')
    assert x.startswith('$') and x.endswith('$'),x
    return x[1:-1]

interfaces=[]; members={}; edges={}; archive=[]
def add(lid,keyword,raw,pages,heading,deps=None,*,kind='definition',role='definition',symbols=(),phrases=(),context=None,group=None,note=None,shape):
    body=convert(raw)
    term_list=keyword if isinstance(keyword,list) else [keyword]
    names=[x[0].upper()+x[1:] for x in term_list]
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,
           statement_original=body,relation='exact',depends_on=list(deps or {}),
           evidence=[dict(page=p,location=heading) for p in pages],
           highlight_symbols=[symbol(x) for x in symbols],highlight_phrases=list(phrases))
    if note:m['variant_note']=note
    keywords=[]
    for term,name in zip(term_list,names):
        k=dict(paper_id=PID,local_id=lid,source_text=term,label=name,kind='term')
        if context:
            m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=m['evidence'])]
            k['context_id']=lid+'/name'
            assert term in context,(lid,term,context)
        else:assert term in body,(lid,term,body)
        keywords.append(k)
    gid=group or lid
    existing=next((x for x in interfaces if x['interface_id']==PID+'/'+gid),None)
    if existing:
        assert existing['name']==' · '.join(names)
        existing['members'].append(m);existing['source_keywords']+=keywords
    else:
        interfaces.append(dict(interface_id=PID+'/'+gid,rank_group='all',name=' · '.join(names),lean_role=role,
            type_shape=shape,semantic_boundary=shape+' The original source passage governs the conventions and quantifiers; no library verdict is attached.',
            members=[m],source_keywords=keywords,central_claim_uses=[],dependencies=[],theorem_explanations={}))
    members[lid]=m;edges[lid]=deps or {}
    archive.append(dict(local_id=lid,original_tex=raw,evidence=m['evidence']))

add('D1','selection problem',passage('Before introducing our method',r'Let $\psi_j'),[5],
    'Section 2 — graph selection problem, equation (2.1)',kind='source_passage',symbols=[r'k_{\tau}',r'\bTheta'],
    shape='Weighted graph or bipartite graph with a chosen tested node set; the null is degree below k_tau and the alternative is degree at least k_tau.')
add('D2','false discovery proportion',passage(r'Let $\psi_j',r'We illustrate the above general setup'),[5],
    'Section 2 — false discovery proportion and FDR',{'D1':'The null-node set consists of nodes whose degrees are below the threshold k_tau.'},
    symbols=[r'{\rm FDP}',r'{\rm FDR}'],phrases=['false discovery proportion'],
    shape='FDP is the number of rejected true nulls divided by max(1,total rejections); FDR is its expectation, with q in (0,1).')
add('D3','maximum test statistic',passage(r'Denote this generic estimator by',r'and its quantile is defined'),[6],
    'Section 2.1 — maximum test statistic, equation (2.2)',{'D1':'The estimator is indexed by pairs of graph nodes, with an edge subset E as the index set of the maximum.'},
    symbols=[r'T_{E}',r'\tTheta'],shape='Given a generic weight-matrix estimator, take max over E of sqrt(n) times the absolute estimated entry; this initial statistic is uncentered.')
add('D4a','quantile',passage('and its quantile is defined',', a generic method called'),[6],
    'Section 2.1 — upper-tail quantile',{'D3':'The quantile c(alpha,E) is defined from the law of the maximum statistic T_E.'},
    group='D4',symbols=[r'{c} (\alpha,E)'],
    shape='Quantile passages retain their separate probability laws, conditioning and inputs; the common source keyword does not identify different calibration procedures.')
algo=env('algorithm',r'\label{algo:startrek}')
algo=passage(r'\STATE \textbf{Input:}',r'\end{algorithmic}',algo)
algo=algo.replace(r'\STATE','\n\n').replace(r'\FOR {$j \in [d]$}',r'\textbf{for} $j\in[d]$ \textbf{do}').replace(r'\ENDFOR',r'\textbf{end for}')
add('D5','StarTrek Filter',algo,[6],'Algorithm 2 — StarTrek Filter',
    {'D1':'The procedure tests all nodes against the degree threshold k_tau.','D2':'The nominal level q and its domain (0,1) use the false-discovery convention stated in Section 2.','D3':'Its ordered absolute entries use the same sqrt(n) maximum-statistic scale.','D4a':'Each node score uses the inverse of the estimated upper-tail quantile function.'},
    context='StarTrek Filter',kind='source_passage',symbols=[r'\alpha_j',r'j_{\max}'],
    note='The source writes an inverse estimated-quantile function without defining an inverse/tie convention. It prints a square-graph loop excluding the diagonal, while Section 4 supplies a rectangular response-by-predictor input. Those conventions are preserved and not silently repaired.',
    shape='Sort each node’s absolute estimated edge weights, maximize inverse-calibration scores over the first k_tau order statistics, then apply the printed BHq order-statistic threshold and selection rule.')
add('D6','centered Gaussian random vectors',passage(r'Let $U,V\in',r'Recall that the maximal difference'),[7],
    'Section 3 — centered Gaussian random vectors',kind='source_passage',symbols=[r'\bSigma^U',r'\bSigma^V'],
    shape='Two centered d-dimensional Gaussian vectors with covariance matrices Sigma-U and Sigma-V; the model context of both comparison Theorems.')
add('D7','maximal difference',passage('Recall that the maximal difference','and the elementwise'),[7],
    'Section 3 — maximal covariance difference',{'D6':'Delta-infinity is the elementwise maximum norm of the difference of the two Gaussian covariance matrices.'},
    symbols=[r'\maxdiff'],shape='Maximum absolute entry difference between the two Gaussian covariance matrices.')
add('D8','elementwise ℓ₀ norm difference',passage('and the elementwise',r'The Gaussian maxima',SOURCE[SOURCE.index('Recall that the maximal difference'):]),[7],
    'Section 3 — elementwise covariance difference',{'D6':'Delta-zero counts covariance entries where Sigma-U and Sigma-V differ.'},
    context='elementwise ℓ₀ norm difference',symbols=[r'\zerodiff'],
    shape='Number of differing entries in the two d-by-d covariance matrices, counted over all ordered index pairs as in the source.')
add('D9','multitask regression',passage('Consider the multitask regression problem',r'Let $s ='),[9],
    'Section 4 — multitask regression model, equation (4.1)',kind='source_passage',symbols=[r'\bY_i',r'\Db'],
    shape='Independent sample pairs with a shared predictor vector, rectangular coefficient matrix and independent centered Gaussian response noise with diagonal covariance; conditional response-noise independence is explicitly assumed.')
add('D10','sparsity level',passage(r'Let $s =',r'As mentioned in Section'),[9],
    'Section 4 — sparsity level',{'D9':'The sparsity s is the maximum row support size of the multitask coefficient matrix.','D1':'The surrounding selection description uses the graph and threshold k_tau from the common testing setup.'},
    symbols=[r's = \max_{j\in [d_1]}\norm{\bTheta_{j}}_0'],
    note='This paragraph says columns after defining row sparsity and selecting among response nodes [d1]. The original wording is retained; the formal row/column convention is not silently changed.',
    shape='Maximum row sparsity of the rectangular multitask coefficient matrix, in the source’s stated notation.')
add('D11','debiased Lasso estimator',passage(r'For each response variable $\bY^{(j)}, j \in [d_1]$, we compute',r'In addition, we also need to compute'),[9],
    'Section 4 — debiased Lasso estimator, equations (4.2) and (4.3)',{'D9':'The estimator uses the shared design matrix and one response column from the multitask model.'},
    symbols=[r'\tdTheta_j',r'\Mb'],
    note='Both argmin constructions are preserved as written. The source does not specify a minimizer tie rule; the matrix M is the stated constrained quadratic-program construction.',
    shape='Lasso estimate plus the M X-transpose residual correction, with M formed rowwise by the constrained covariance quadratic programs and empirical covariance X-transpose X/n.')
add('D12','scaled Lasso',passage(r'As the noise variance $\sigma_j$',r'Regarding our testing problem'),[10],
    'Section 4 — scaled Lasso, equation (4.5)',{'D9':'The joint optimization uses the shared design and a selected response column to estimate that response noise scale.'},
    symbols=[r'\hat\sigma_j'],shape='Joint minimization over coefficients and a positive scale of residual loss divided by scale, scale/2 and an L1 penalty.')
add('D4b','quantile',passage('Regarding our testing problem',r'Indeed, under proper scaling conditions'),[10],
    'Section 4 — Gaussian quantile approximation, equation (4.6)',
    {'D11':'The Gaussian calibration covariance uses M and the empirical covariance constructed for the debiased Lasso.','D12':'The covariance scale is the response-specific scaled-Lasso estimate.'},
    group='D4',symbols=[r'T^{\cN}_{E}',r'\hat{c} (\alpha,E)'],
    shape='Conditional Gaussian calibration of the multitask maximum, with covariance formed from the estimated response scale, M and empirical predictor covariance.')
ass4=env('assumption',r'\label{asp:dlasso}')
ass4=ass4[ass4.index('The following assumptions'):]
add('D13','Debiased Lasso with random designs',ass4,[10], 'Assumption 4.1 — Debiased Lasso with random designs',
    {'D9':'The population second-moment matrix and whitened random design refer to the multitask predictors.','D10':'The sample-size requirement uses the maximum row sparsity s.','D11':'The tuning mu and lambda are those of the constrained M program and the Lasso construction.'},
    kind='assumption',role='hypothesis',context='Debiased Lasso with random designs',phrases=['Assumption 4.1'],
    note='The passage invokes constants nu0, a, c and a noise scale sigma without supplying all their numerical choices in the main text; the cited-source reference is preserved.',
    shape='Population covariance bounds, independent zero-mean subgaussian whitened rows, and the printed sample-size and tuning conditions for the debiased Lasso.')
add('D14a','signal strength',passage(r'Recall that $\cH_0 =',r'\rev{As mentioned at the beginning'),[10],
    'Section 4 — non-hub responses and signal strength, equation (4.8)',
    {'D9':'The null and strong-signal sets use rows of the multitask coefficient matrix.','D1':'Their null criterion compares row support size with the degree threshold k_tau.'},
    group='D14',symbols=[r'\cH_0',r'\rho'],
    shape='Separate source-local null counts and proportions of strong non-null nodes; the multitask threshold uses log(d2) and denominator d1, while the graphical-model threshold uses log(d) and denominator d.')
add('D15','Gaussian graphical models',passage('This section focuses on the hub node selection',r'we consider the following one-step estimator')+'}',[11],
    'Section 5 — Gaussian graphical models and initial estimator',kind='source_passage',symbols=[r'\bTheta = \bSigma^{-1}',r'\hat{\bTheta}'],
    note='The main text gives graphical Lasso and CLIME as examples of the initial estimator. No additional rate assumption or appendix definition is supplied by this extraction.',
    shape='Independent centered Gaussian observations with covariance Sigma, precision weight matrix Sigma-inverse and a supplied initial precision-matrix estimator.')
one=passage(r'we consider the following one-step estimator',r'Our StarTrek filter selects nodes')
# This passage ends by closing the source editorial revision wrapper opened before it.
one=re.sub(r'\}\s*$','',one)
add('D16','one-step estimator',one,[11], 'Section 5 — one-step estimator, equation (5.1)',
    {'D15':'The correction uses the initial precision estimator and empirical covariance from the Gaussian graphical model.'},
    symbols=[r'\dTheta_{jk}',r'\tdTheta_{jk}'],
    note='The correction denominator and the subsequent diagonal standardization are preserved exactly; row/column conventions and the base estimator are not replaced by a preferred implementation.',
    shape='The printed one-step precision correction followed by division by the square root of its two corrected diagonal entries.')
add('D4c','Gaussian multiplier bootstrap',passage('The quantiles are approximated using',r'\cite{chernozhukov2013gaussian} shows'),[11],
    'Section 5 — Gaussian multiplier bootstrap quantiles, equation (5.2)',
    {'D15':'The multiplier statistic is built from the initial precision estimate and Gaussian observations; it does not require the debiased estimator as a mathematical input.'},
    group='D4c',symbols=[r'T^{\cB}_{E}',r'\hat{c} (\alpha,E)'],
    shape='Conditional upper-tail quantile of the printed precision-model Gaussian multiplier statistic, retaining its normalization by the initial diagonal precision estimates.')
h0=passage('Similarly, the set of non-hub nodes', 'Now we consider the following set')
strength=passage('And similarly as in Section', 'In the following, we list our assumptions needed')
add('D14b','signal strength',h0+'\n\n'+strength,[12,13], 'Section 5 — non-hub nodes and signal strength',
    {'D1':'The source null set compares the support count of a weight-matrix row with k_tau; rho counts sufficiently strong rows outside that set.'},
    group='D14',symbols=[r'\cH_0',r'\rho'],
    note='The source writes the full row norm in H0 here, whereas Section 2.1 excludes the diagonal. Both passages are preserved, and no diagonal correction is inferred. Section 6 explicitly reuses this d0 and rho convention without importing Gaussian data assumptions.',
    shape='The graphical-model null count and fraction of non-null rows whose supported entries exceed c sqrt(log(d)/n), used again by Section 6.')
dep=passage('Now we consider the following set',r'\begin{figure}')
dep+= '\n\n'+passage('Remark that in the above definition','If there exists a large number')
add('D17','dependence level',dep,[12], 'Section 5 — dependence set, equation (5.3)',
    {'D14b':'The first two indices must be distinct non-hub nodes in the graphical-model null set.','D1':'The zero and nonzero weight entries specify the cross-connection pattern of the graph.'},
    context='In general, the sparsity/density of the graph is closed related to the dependence level of multiple testing problem on graphical models.',
    symbols=['S ='],
    note='The source permits k1=j2 and k2=j1. It imposes k1!=k2 but does not require four distinct vertices.',
    shape='Ordered quadruples of two null nodes and two auxiliary indices satisfying the exact zero and crossed-nonzero weight pattern in (5.3).')
add('D18','number of connected components',passage('In addition to $|S|$', 'And similarly as in Section'),[13],
    'Section 5 — number of connected components',{'D1':'The quantity p counts connected components of the graph being tested.'},
    phrases=['number of connected components'],shape='The number p of graph connected components; distinct from the locally bound Gaussian block-partition count in Theorem 3.3.')
add('D19',['Signal strength and scaling condition','Dependency and connectivity condition'],env('assumption',r'\label{asp:tradeoff_fdp}'),[13],
    'Assumption 5.1',{'D14b':'Both scaling conditions use the graphical-model signal fraction rho and null count d0.','D17':'Condition (5.5) includes the cardinality of the ordered dependence set S.','D18':'The denominator in (5.5) includes the graph component count p.'},
    kind='assumption',role='hypothesis',phrases=['Assumption 5.1'],
    note='The class U(M,s,r0) is named here but has no definition in the inspected main text. Its meaning remains unresolved; no appendix definition is imported.',
    shape='The source parameter-class membership plus its two asymptotic restrictions, including the exact powers of log d, rho and n, and the factor p in the dependence term.')
generic=passage(r'Recall that in Section \ref{sec:startrek}',r'In specific, similar to the assumptions')
add('D20','generic estimator',passage(r'Recall that in Section \ref{sec:startrek}', 'We can then estimate the quantile'),[14],
    'Section 6 — generic estimator and linear representation',{'D1':'The generic weight matrix has a nonzero entry exactly when the corresponding edge is present.'},
    kind='source_passage',symbols=[r'\tilde \bTheta',r'\bY_i(e)'],
    shape='Generic graph weight estimator with an edgewise asymptotic representation as an average of independent mean-zero influence variables plus o_P(n^-1/2).')
add('D4d','Gaussian multiplier bootstrap',passage('We can then estimate the quantile',r'In specific, similar to the assumptions'),[14],
    'Section 6 — generic Gaussian multiplier quantiles, equation (6.1)',{'D20':'This passage centers the maximum by the true weight matrix and calibrates its estimator error using a generic multiplier statistic.'},
    group='D4c',symbols=[r'T^{\cB}_{E}',r'\hat{c} (\alpha,E)'],
    note='This passage uses a centered T_E, unlike the uncentered statistic (2.2). The source does not give a specific formula for the generic T_E^B; Assumption 6.1 supplies approximation requirements.',
    shape='Generic multiplier calibration for centered estimation-error maxima, retaining the distinction between the actual multiplier statistic and its influence-variable approximation.')
add('D21','general assumptions',env('assumption',r'\label{asmp:zeta12}'),[14], 'Assumption 6.1',
    {'D20':'The ideal maxima are built from the mean-zero influence variables in the generic estimator representation.','D4d':'The second probability bound controls the generic multiplier statistic relative to its ideal multiplier maximum.'},
    kind='assumption',role='hypothesis',context=convert(passage('In specific, similar to the assumptions',r'\begin{assumption}')),phrases=['Assumption 6.1'],symbols=[r'\zeta_1',r'\zeta_2'],
    shape='Uniform-in-edge-set probability approximation bounds for data and conditional multiplier maxima, plus variance and psi1 moment restrictions on influence variables and independent normal multipliers.')
add('D22','dependency set',passage(r'Similar to \eqref{eq:dep_term_set}', 'We also impose the cardinality'),[14],
    'Section 6 — dependency set',{'D20':'Nonzero covariance of the two influence variables determines membership in the general dependency set.','D14b':'The first two indices must be distinct null nodes, using the graphical-model null convention retained in Section 6.'},
    symbols=['S='],note='This general set is defined by influence covariance and two zero weights; it does not reproduce the additional weight-pattern and k1!=k2 conditions of (5.3).',
    shape='Ordered quadruples with two distinct null nodes, two zero tested weights and nonzero covariance between their influence variables; separate from the Gaussian precision-pattern set.')
add('D23','scaling condition',env('assumption',r'\label{asp:tradeoff_fdp_gen}'),[14], 'Assumption 6.2',
    {'D14b':'The source explicitly reuses the null count d0 and signal fraction rho from Section 5.','D21':'The approximation parameters zeta1 and zeta2 come from Assumption 6.1.','D22':'The cardinality term uses the general influence-covariance dependency set S.'},
    kind='assumption',role='hypothesis',phrases=['Assumption 6.2'],
    note='The class U(M,s,r0) remains undefined in the inspected main text. This scaling condition has no graph-component divisor p, unlike Assumption 5.1.',
    shape='Parameter-class membership and the complete asymptotic scaling restriction, including zeta2*d^4 and the general dependence term without p.')

def main():
    for x in interfaces:
        if len(x['members'])>1:
            for m in x['members']:
                m['relation']='distinct'
                m['variant_note']=m.get('variant_note','')+' This source occurrence retains its own inputs and dependency path; sharing a keyword does not equate the conditions.'
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,local_edge_explanations=edges),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'evidence/source-passages-tex.json').write_text(json.dumps(archive,indent=2,ensure_ascii=False)+'\n')
    notation=passage(r'Let $\phi(x),\Phi(x)$',r'\section{Methodology}')
    (ROOT/'ambient-conventions.json').write_text(json.dumps(dict(paper_id=PID,source_heading='Section 1.3 — Notations',statement_original=convert(notation),evidence=[dict(page=4,location='Section 1.3 begins'),dict(page=5,location='Section 1.3, norms and asymptotic conventions')]),indent=2,ensure_ascii=False)+'\n')
    print('Saved',len(members),'source members in',len(interfaces),'interface groups; connections remain to be finalized.')

if __name__=='__main__':main()
