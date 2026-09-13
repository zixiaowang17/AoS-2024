"""Main-text AdaDetect source passages and reviewed local dependencies."""
import json
from pathlib import Path
import re
import subprocess
from save_inventory import REFS as INVENTORY_REFS

ROOT=Path(__file__).resolve().parents[1]
PID=ROOT.name
SOURCE=re.sub(r'(?<!\\)%[^\n]*','',(ROOT/'evidence/main-only.tex').read_text())
MACROS=(ROOT/'evidence/macros.tex').read_text()+r'\renewcommand{\rev}[1]{#1}'
REFS=dict(INVENTORY_REFS,**{'sec:setting':'1.1','equFDRFDP':'2','equTDRTDP':'3','equkchapeau':'4',
 'scorefunction':'7','equscores':'9','equ:f':'15','equ:f1bar':'16','sec:adaptiveteststat':'2.4',
 'rem:invariance':'2.1','equoraclescore':'19','NPexactRgamma':'25','defghat':'26'})
CITES={'BH1995':'Benjamini and Hochberg (1995)','BY2001':'Benjamini and Yekutieli (2001)',
 'weinstein2017power':'Weinstein et al. (2017)','yang2021bonus':'Yang et al. (2021)',
 'mary2021semisupervised':'Mary and Roquain (2022)','bates2021testing':'Bates et al. (2021)',
 'SC2007':'Sun and Cai (2007)','lei2018adapt':'Lei and Fithian (2018)',
 'weinstein2021permutation':'Weinstein (2021)','rosset2022optimal':'Rosset et al. (2022)',
 'BLS2010':'Blanchard et al. (2010)','cannon2002learning':'Cannon et al. (2002)',
 'scott2005neyman':'Scott and Nowak (2005)','vapnik1998statistical':'Vapnik (1998)'}

def passage(start,end,source=SOURCE):
    a=source.index(start);return source[a:source.index(end,a)].strip()

def env(kind,label):
    hits=[m[1] for m in re.finditer(r'\\begin\{'+kind+r'\}(.*?)\\end\{'+kind+r'\}',SOURCE,re.S) if r'\label{'+label+'}' in m[1]]
    assert len(hits)==1,(kind,label)
    return re.sub(r'\\label\{[^}]+\}','',hits[0]).strip()

def mathenv(label):
    hits=[m.group() for m in re.finditer(r'\\begin\{(align|equation)\}(.*?)\\end\{\1\}',SOURCE,re.S) if r'\label{'+label+'}' in m[2]]
    assert len(hits)==1,label
    return hits[0]

def mathrow(label):
    raw=mathenv(label);body=re.sub(r'\\begin\{[^}]+\}|\\end\{[^}]+\}','',raw)
    rows=[r for r in re.split(r'\\\\',body) if r'\label{'+label+'}' in r]
    assert len(rows)==1
    return r'\begin{equation}'+rows[0]+r'\end{equation}'

def unwrap_box(raw):
    if not raw.startswith(r'\mbox{'):return raw
    depth=1;i=len(r'\mbox{')
    while depth:
        if raw[i]=='{':depth+=1
        elif raw[i]=='}':depth-=1
        i+=1
    return raw[len(r'\mbox{'):i-1]+raw[i:]

def convert(raw):
    raw=unwrap_box(raw)
    raw=re.sub(r'\\eqref\{([^}]+)\}',lambda m:'('+REFS[m[1]]+')',raw)
    raw=re.sub(r'\\ref\{([^}]+)\}',lambda m:REFS[m[1]],raw)
    raw=re.sub(r'\\cite(?:p|alp)?(?:\[([^]]*)\])?(?:\[([^]]*)\])?\{([^}]+)\}',lambda m:((m[1]+' ') if m[1] else '')+'; '.join(CITES[k.strip()] for k in m[3].split(',')),raw)
    def display(m):
        kind,body=m[1],m[2]
        rows=re.split(r'\\\\',body)
        labels=re.findall(r'\\label\{([^}]+)\}',body)
        if len(labels)>1:
            return '\n\n'.join(display((None,'equation',r)) for r in rows)
        body=re.sub(r'\\label\{[^}]+\}|\\nonumber','',body).strip()
        if r'\\' in body:body=r'\begin{aligned}'+body+r'\end{aligned}'
        else:body=body.replace('&','')
        return r'\['+body+(r'\tag{'+REFS[labels[0]]+'}' if labels else '')+r'\]'
    raw=re.sub(r'\\begin\{(align|equation)\}(.*?)\\end\{\1\}',display,raw,flags=re.S)
    raw=re.sub(r'\\label\{[^}]+\}','',raw)
    out=subprocess.run(['pandoc','-f','latex','-t','markdown','--wrap=none'],input=MACROS+'\n\\begin{document}\n'+raw+'\n\\end{document}',text=True,capture_output=True,check=True).stdout.strip()
    out=out.replace(r'\mathds{1}',r'\mathbb{1}')
    out=re.sub(r'\$\$(.*?)\$\$',lambda m:'\n\\[\n'+m[1]+'\n\\]\n',out,flags=re.S)
    assert 'reference-type' not in out and r'\ref{' not in out
    return out

def symbol(raw):
    x=convert('$'+raw+'$')
    assert x.startswith('$') and x.endswith('$')
    return x[1:-1]

interfaces=[];members={};edges={};archive=[]
def add(lid,term,raw,pages,heading,deps=None,*,role='definition',kind='definition',symbols=(),phrases=(),context=None,group=None,relation='exact',note=None,shape):
    body=convert(raw)
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,
           statement_original=body,relation=relation,depends_on=list(deps or {}),
           evidence=[dict(page=p,location=heading) for p in pages],
           highlight_symbols=[symbol(x) for x in symbols],highlight_phrases=list(phrases))
    if note:m['variant_note']=note
    keyword=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
    if context:
        m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=m['evidence'])]
        keyword['context_id']=lid+'/name'
        assert term in context
    else:assert term in body,(lid,term,body)
    gid=group or lid
    existing=next((x for x in interfaces if x['interface_id']==PID+'/'+gid),None)
    if existing:
        assert existing['name']==keyword['label']
        existing['members'].append(m);existing['source_keywords'].append(keyword)
    else:
        interfaces.append(dict(interface_id=PID+'/'+gid,rank_group='all',name=keyword['label'],lean_role=role,
            type_shape=shape,semantic_boundary=shape+' Original source domains and conventions are preserved; this is not a library audit.',
            members=[m],source_keywords=[keyword],central_claim_uses=[],dependencies=[],theorem_explanations={}))
    members[lid]=m;edges[lid]=deps or {}
    archive.append(dict(local_id=lid,original_tex=raw,evidence=m['evidence']))

add('D1','null training sample',passage('As in Section',r'Throughout the paper, we consider the semi-supervised setting'),[5],
    'Section 2.1 — null training sample, test sample and model',kind='source_passage',phrases=['null training sample'],symbols=[r'\cH_0',r'\cH_1'],
    shape='Joint law P of null training sample Y and test sample X; H0 and H1 compare marginal laws with P0, with the printed counts and proportions.')
add('D2','false discovery rate',passage('Given a procedure $R$, the false discovery rate','Similarly, the true discovery rate'),[5],
    'Section 2.2 — false discovery rate and false discovery proportion, equation (2)',{'D1':'False discoveries are rejections in H0, with expectation under the joint law P.'},phrases=['false discovery rate'],symbols=[r'\FDR(P,R)',r'\FDP(P,R)'],
    shape='Expected false discovery proportion with denominator max(1,number of rejections).')
add('D3','BH algorithm',passage('Suppose a set of $p$-values','When the null $p$-values'),[6],
    'Section 2.3 — BH algorithm, equation (4)',phrases=['BH algorithm'],symbols=[r'\hat{k}'],
    shape='Step-up rejection set at alpha*khat/m, using the largest integer 0..m with at least khat p-values below that threshold.')
add('D4','second null sample',passage('It starts by splitting the null sample','It proceeds with the following steps.'),[6],
    'Section 2.4 — split of the null sample',{'D1':'The split partitions the null training observations while retaining all test observations.'},phrases=['second null sample'],symbols=[r'\ell=n - k'],
    shape='First k null observations are training data, remaining ell=n-k are calibration data, and calibration plus test form the mixed sample.')
add('D5','data-driven score function',passage('Compute a data-driven score function',r'\item Transform the raw data'),[6],
    'Section 2.4 — data-driven score function, equations (7) and (8)',{'D4':'The score takes separate training and mixed arguments; only the latter is permutation invariant.'},phrases=['data-driven score function'],
    shape='Real score invariant under all permutations of its mixed-sample argument, for every query and possible dataset.')
add('D6','univariate scores',passage('Transform the raw data into univariate scores',r'\item For each test point'),[7],
    'Section 2.4 — univariate scores, equation (9)',{'D5':'S_i evaluates the fitted data-driven score at observation Z_i.'},phrases=['univariate scores'],symbols=[r'S_i'],
    shape='Adaptive real scores for all mixed-sample observations, with large values intended to indicate novelties.')
add('D7','empirical p-value',passage('For each test point',r'\item Apply the BH algorithm'),[7],
    'Section 2.4 — empirical p-values, equation (10)',{'D4':'The count compares each test score with the ell calibration scores.'},context=convert(passage('For each test point',r'\begin{equation}')).replace('$p$','p'),phrases=['empirical'],symbols=[r'p_j'],
    shape='p_j=(1+count of calibration scores strictly larger than the test score)/(ell+1). Arbitrary input scores are permitted; they need not have been fitted by (9).')
add('D8','AdaDetect',passage('In this paper, we propose a method called AdaDetect.',r'By simple algebra, the last two steps'),[6,7],
    'Section 2.4 — AdaDetect procedure',{'D4':'AdaDetect splits the null sample.','D5':'It fits a score satisfying mixed-sample permutation invariance.','D6':'It evaluates the fitted score on the mixed sample.','D7':'It forms empirical p-values from the comparisons.','D3':'The final step applies BH at the target level.'},phrases=['AdaDetect'],
    shape='Full four-step split, invariant score, empirical p-value and BH procedure; preserve the source strict score comparison.')
add('D9','Exchangeability',env('assumption','as:exchangeable0'),[8],
    'Assumption 1 — exchangeability of the raw measurements',{'D1':'The exchangeable family comprises training and null test observations, conditional on alternative test observations.'},kind='assumption',role='hypothesis',context='Exchangeability',phrases=['Assumption 1'],
    shape='Conditional exchangeability of raw null observations, including the footnote requiring existence of the conditional distribution.')
add('D10','exchangeability of the scores',env('assumption','as:newexch'),[9],
    'Assumption 2 — exchangeability of the scores',{'D1':'H0 and H1 identify null and alternative test-score indices.','D4':'The null-score family also includes all calibration scores.'},kind='assumption',role='hypothesis',context='For our results, a necessary assumption is exchangeability of the scores under the null:',phrases=['Assumption 2'],
    shape='Conditional exchangeability of calibration and null test scores given alternative scores. This is a condition on arbitrary scores, not on their construction.')
add('D11','no ties',env('assumption','as:noties'),[9],
    'Assumption 3 — no ties',{'D4':'The no-ties condition ranges over the entire mixed-sample score family.'},kind='assumption',role='hypothesis',phrases=['no ties','Assumption 3'],
    shape='Almost surely all calibration and test scores are distinct.')
add('D12','PRDS',passage('Following \\cite{BY2001}',r'\begin{theorem}\label{thm:PRDS_multidim}'),[9],
    'Section 3.2 — PRDS',{'D1':'Positive regression dependence is imposed on null indices H0.'},role='predicate',phrases=['PRDS'],
    shape='For each null index and increasing measurable set, its conditional probability given that p-value equals u is nondecreasing in u; include the increasing-set footnote.')
di=passage('For each $i\\in \\cH_0$, let',r'\begin{theorem}\label{thm:AdaptBONuS}')
di=di.replace(mathenv('def:Di'),r'''\[
\left\{\begin{array}{l}
p'_j=0,\ j\in\cH_1,\ p'_i=1/(\ell+1);\\
p'_j,\ j\in\cH_0\backslash\{i\}\ \text{are i.i.d. conditionally on }U\text{ with a common c.d.f. }F^U;\\
U=(U_1,\dots,U_{\ell+1})\text{ has i.i.d. }U(0,1)\text{ components,}
\end{array}\right.\tag{13}
\]''')
add('D13','least favorable distribution',di,[10],
    'Section 3.4 — distribution D_i, equation (13)',{'D1':'The law distinguishes alternatives, the selected null i, and other null indices.','D4':'Its grid and uniform vector have size ell+1.'},context=convert(passage('In a nutshell, the distribution $\\mathcal{D}_{i}$', 'It can be seen as an adaptation')),symbols=[r'\mathcal{D}_{i}',r'F^U'],
    shape='Full common-uniform construction, conditional iid null coordinates with the printed discrete cdf, fixed alternatives zero and selected null 1/(ell+1); order statistics descend.')
members['D13']['naming_context'][0]['evidence']=[dict(page=11,location='Paragraph following Theorem 3.6')]
add('D14','mutually independent',env('assumption','as:indep'),[12],
    'Assumption 4 — mutual independence',{'D1':'The condition applies to all training and test observations.'},kind='assumption',role='hypothesis',phrases=['mutually independent','Assumption 4'],
    shape='Mutual independence of every observation Y_1..Y_n and X_1..X_m.')
add('D15','positive density',env('assumption','equ-marg'),[12],
    'Assumption 5 — positive densities',{'D1':'The null and alternative marginals have densities relative to the same measure nu.'},kind='assumption',role='hypothesis',phrases=['positive density','Assumption 5'],
    shape='Each Pi for i in {0} union H1 has a positive density fi with respect to nu.')
dens=passage('Let \n\\begin{align}\nf&=',r'Compared to $f$, the mixture')
add('D16','average density',dens,[12],
    'Section 4.1 — average densities and gamma, equations (15)-(17)',{'D14':'The accompanying average-density interpretation is stated under Assumption 4.','D15':'The mixture uses common-reference null and alternative densities.','D1':'Weights pi0, pi1 and m1 are the fixed marginal-type proportions and counts.','D4':'The mixed sample has ell calibration observations, yielding gamma=m1/(ell+m).'},phrases=['average density'],symbols=[r'f_\gamma',r'\gamma'],
    shape='Average alternative, test and mixed-sample densities with gamma=m1/(ell+m). These averages do not assert iid mixture sampling.')
add('D17','density ratio',passage('Lastly, we define the density ratio',r'\subsection{Optimal score function}'),[12],
    'Section 4.1 — density ratio, equation (18)',{'D16':'The ratio is pi1 times average alternative density divided by average test density.'},phrases=['density ratio'],symbols=[r'\lrt(x)'],
    shape='r(x)=pi1*f1bar(x)/f(x); retain the printed almost-everywhere range, including its limitation when a mixture proportion vanishes.')
add('D18','marginal FDR',passage(r'\rev{Recall that AdaDetect is equivalent',r'\begin{theorem}\label{th:SCextended}'),[13],
    'Section 4.2 — marginal FDR (mFDR)',{'D1':'The passage compares expectations of rejection counts under the joint law.','D4':'The printed numerator uses calibration indices {k+1,...,n}.'},kind='source_passage',phrases=['marginal FDR'],
    note='The printed ratio intersects R(t) with calibration indices, although Section 2.2 defines rejection sets using test indices. This indexing ambiguity and the displayed approximations are preserved.',
    shape='The complete main-text mFDR passage with its ratio of expected counts; indexing and empty-denominator conventions remain unresolved.')
add('D19','oracle AdaDetect procedure',env('definition','def:oraclebonus'),[13],
    'Definition 4.2 — oracle AdaDetect procedure',{'D8':'The oracle retains the AdaDetect calibration and BH rule.','D17':'Its score is the population ratio r.'},phrases=['oracle AdaDetect procedure'],
    shape='AdaDetect with the deterministic oracle density-ratio score.')
add('D20','score function',passage('Since AdaDetect is invariant under any strictly monotone',r'Since $\lrt$ (or $g^*$)'),[13],
    'Section 4.2 — oracle score function, equation (19)',{'D17':'The score g-star is Psi composed with r.'},phrases=['score function'],symbols=[r'g^*'],
    shape='g-star=Psi composed with r for increasing continuous Psi:(0,1)->R; preserve the prose about strictly monotone transformations separately from the displayed increasing condition.')
risks=mathenv('NPexactRgamma')+'\n'+passage('where $\\gamma$, $f_0$, and $\\bar{f}_1$',r'We consider a function class')
add('D21','0-1 loss',risks,[18],
    'Section 5.1 — empirical and population risks, equation (25)',{'D16':'Population risks use f0, average alternative f1bar, and mixed density f-gamma.','D4':'Empirical null and mixed risks use the separate training and mixed samples.'},context=convert(passage('For the convenience of theoretical analysis', 'Define\n')).replace('$0$-$1$','0-1'),symbols=[r'R_0(g)',r'R_1(g)',r'\hat{R}_\gamma(g)'],
    shape='All risks in (25), retaining g>=0 for null error and g<0 for alternative/mixed error, and the mixture-risk identity.')
members['D21']['naming_context'][0]['evidence']=[dict(page=p,location='Section 5.1 — opening sentence') for p in [17,18]]
add('D22','Vapnik-Chervonenkis (VC) dimension',passage('We consider a function class',r'and the following constrained ERM score function'),[18],
    'Section 5.1 — finite Vapnik-Chervonenkis (VC) dimension',role='hypothesis',kind='condition',phrases=['Vapnik-Chervonenkis (VC) dimension'],symbols=[r'V(\cG)'],
    note='The source cites VC dimension without defining the induced set class for real-valued scores. No external or appendix convention is supplied.',
    shape='Finite VC dimension V(G) of the score class in the stated source convention.')
add('D23','constrained ERM score function',mathenv('defghat'),[18],
    'Section 5.1 — constrained ERM score function, equation (26)',{'D21':'The empirical minimizer optimizes mixed error subject to null error at most beta+epsilon0.','D22':'Optimization is over the class G whose VC dimension enters the theorem.'},context=convert(passage('We consider a function class',r'\begin{align}')),symbols=[r'\hat{g}'],
    shape='A selected empirical constrained minimizer. Existence, measurability and permutation-invariant tie selection are not specified by the argmin formula alone.')
add('D24','population version',passage('for some $\\epsilon_0 > 0$, as well as its population version',r'\begin{theorem}\label{powerhighdim}'),[18],
    'Section 5.1 — population version, equation (27)',{'D21':'The population optimizer minimizes R-gamma subject to R0<=beta.','D22':'Its candidates lie in the same class G.'},phrases=['population version'],symbols=[r'g^\sharp_\cG'],
    shape='A selected population constrained minimizer in G; Theorem 5.1 separately requires equality in its null-risk constraint.')
tail='Now we move to general score functions. Let $g^*$ be any measurable function $\\R^d\\to \\R$ in the form of \\eqref{equoraclescore} and\n'+mathrow('equGbar')
add('D25','General score functions',tail,[19],
    'Section 5.2 — oracle score tail, equation (33)',{'D20':'The deterministic score has oracle form (19).','D1':'The tail probability is under the null law P0.'},context='General score functions',symbols=[r'\ol{G}_0(s)'],
    shape='Null upper-tail function P0(g-star(X)>=s); continuity and strict decrease are additional theorem hypotheses.')
add('D26','local fluctuation',mathrow('funcdelta')+'\n'+passage('Here, $\\zeta_r(\\cdot)$ measures',r'Furthermore, consider any data-driven'),[19],
    'Section 5.2 — local fluctuation, equation (34)',{'D25':'Relative fluctuation uses the null tail two eta below its inverse at u.'},phrases=['local fluctuation'],symbols=[r'\zeta_{r}(\eta)'],
    shape='Maximum relative null-tail change over u in [alpha*(r vee 1)/m,alpha], for a 2*eta score shift, with all printed domains.')
add('D27','maximal discrepancy',passage('Furthermore, consider any data-driven score function',r'\begin{theorem}\label{th:BHestimated}'),[19,20],
    'Section 5.2 — maximal discrepancy, equation (35)',{'D5':'The estimated score must satisfy permutation condition (8).','D20':'Its comparison score is the fixed oracle g-star.','D4':'The maximum runs over every mixed-sample observation.'},phrases=['maximal discrepancy'],symbols=[r'\hat{\eta}'],
    shape='Maximum absolute estimated/oracle score difference on the mixed sample, with the following conventions for naming the two AdaDetect procedures.')

def main():
    for name,data in [('source-passages.json',dict(paper_id=PID,members=list(members.values()))),('evidence/source-passages-tex.json',archive),('interface-draft.json',interfaces)]:
        (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} interfaces and {len(members)} source members.')

if __name__=='__main__':main()
