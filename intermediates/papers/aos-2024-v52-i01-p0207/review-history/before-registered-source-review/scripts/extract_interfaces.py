"""Extract the bandit paper's original source passages and algorithm control structure."""
import json
from pathlib import Path
import re
import subprocess
ROOT=Path(__file__).resolve().parents[1];PID=ROOT.name
SOURCE=(ROOT/'evidence/main-only.tex').read_text()
MACROS=(ROOT/'evidence/macros.tex').read_text()
REFS={'eq:regret':'1','eq:def-regret':'2','eq:tran-exp':'3','eq:explore-coef':'4','def:bin':'5',
'eq:cond-mean-reward-func':'6','eq:n-k-B-Pdata':'7','eq:Y-bar-k-B-Pdata':'8','eq:UCB':'9','eq:tau-star':'10',
'eq:upper-bound-oracle':'11','eq:lower-bound-oracle':'12','eq:minimax-rate':'13','eq:minimax-rate-conventional':'14',
'eq:def-poly-proj':'15','def:local-estimator':'16','eq:UCB-adapt':'17','eq:tau-star-adaptive':'18','eq:upper-bound-adaptive':'19',
'assumption:smooth':'1','assumption:margin':'2','assumption:bounded-density':'3','assumption:self-similar':'4',
'def:transfer':'1','def:explore-coef':'2','def:self-similar':'3','alg:UCB-TL':'1','alg:EA-TL':'1','alg:UCB-TL-adaptive':'2','alg:smoothness':'2',
'sec:intro':'1','sec:Problem-formulation':'2','sec:Main-Results':'3','subsection:algorithm':'3.1','sec:Adaptivity':'4','subsec:The-self-similarity-assumption':'4.1','subsec:Adaptive-Algorithm':'4.2','sec:Discussion':'5',
'fig:alg':'1','thm:upper-bound':'1','thm:lower-bound':'2','thm:upper-bound-adaptive':'3','thm:lower-bound-adaptive':'4'}

def passage(start,end,source=SOURCE):
 a=source.index(start);return source[a:source.index(end,a)].strip()
def env(kind,label):
 hits=[m[1] for m in re.finditer(r'\\begin\{'+kind+r'\}(.*?)\\end\{'+kind+r'\}',SOURCE,re.S) if r'\label{'+label+'}' in m[1]]
 assert len(hits)==1,(kind,label)
 body=re.sub(r'^\s*\[[^]]*\]','',hits[0]);return re.sub(r'\\label\{[^}]+\}','',body).strip()
def convert(raw):
 raw=re.sub(r'\\eqref\{([^}]+)\}',lambda m:'('+REFS[m[1]]+')',raw)
 raw=re.sub(r'\\ref\{([^}]+)\}',lambda m:REFS[m[1]],raw)
 assert not re.search(r'\\cite',raw),'Select and resolve citation-bearing passages separately.'
 def display(m):
  kind,body=m[1],m[2];labs=re.findall(r'\\label\{([^}]+)\}',body)
  assert len(labs)<=1,labs
  body=re.sub(r'\\label\{[^}]+\}|\\nonumber','',body).strip()
  if r'\\' in body and r'\begin{cases}' not in body:body=r'\begin{aligned}'+body+r'\end{aligned}'
  elif r'\begin{cases}' not in body:body=body.replace('&','')
  return r'\['+body+(r'\tag{'+REFS[labs[0]]+'}' if labs else '')+r'\]'
 raw=re.sub(r'\\begin\{(align\*?|equation\*?)\}(.*?)\\end\{\1\}',display,raw,flags=re.S)
 raw=re.sub(r'\\label\{[^}]+\}','',raw)
 out=subprocess.run(['pandoc','-f','latex','-t','markdown','--wrap=none'],input=MACROS+'\n\\begin{document}\n'+raw+'\n\\end{document}',text=True,capture_output=True,check=True).stdout.strip()
 out=out.replace(r'\mathds{1}',r'\mathbb{1}')
 out=re.sub(r'\$\$(.*?)\$\$',lambda m:'\n\\[\n'+m[1]+'\n\\]\n',out,flags=re.S)
 assert 'reference-type' not in out and r'\ref{' not in out
 return out

def unbrace(s):
 s=s.strip()
 if not s.startswith('{'):return s
 depth=0
 for i,c in enumerate(s):
  if i and s[i-1]=='\\':continue
  if c=='{':depth+=1
  elif c=='}':
   depth-=1
   if depth==0:
    assert not s[i+1:].strip(),s
    return s[1:i]
 raise ValueError('unclosed argument '+s[:80])

def algorithm(label):
 raw=env('algorithm',label)
 caption=re.search(r'\\caption\{([^}]+)\}',raw)[1]
 body=re.search(r'\\begin\{algorithmic\}(?:\[\d+\])?(.*?)\\end\{algorithmic\}',raw,re.S)[1]
 tokens=list(re.finditer(r'\\(State|Comment|For|While|If|Else|Loop|EndFor|EndWhile|EndIf|EndLoop)\b',body))
 steps=[];depth=0
 for i,t in enumerate(tokens):
  kind=t[1];piece=body[t.end():tokens[i+1].start() if i+1<len(tokens) else len(body)].strip()
  if kind.startswith('End'):
   assert not piece,(kind,piece);depth-=1;continue
  if kind=='Else':depth-=1
  if kind=='Comment':
   assert steps
   steps[-1]['comment_original']=convert(unbrace(piece));continue
  if kind=='State':
   converted_piece=unbrace(piece)
   if label=='alg:smoothness' and r'\widehat{\eta}_{k}(x;B)' in converted_piece:
    # Keep the PDF equation number, removed with labels by the environment extractor.
    converted_piece=converted_piece.replace(r'\end{align}',r'\tag{16}\end{align}')
   text=convert(converted_piece)
  elif kind in ['For','While','If']:
   text=kind.lower()+' '+convert(unbrace(piece))+(' then' if kind=='If' else ' do')
  else:
   assert not piece,(kind,piece);text=kind.lower()
  steps.append(dict(line=len(steps)+1,depth=depth,control=kind,text_original=text,source_tex=piece))
  if kind in ['For','While','If','Else','Loop']:depth+=1
 assert depth==0,depth
 lines=[]
 for s in steps:
  indent='    '*s['depth'];text=s['text_original']
  if s.get('comment_original'):text+=' ▷ '+s['comment_original']
  lines.append(indent+'- **'+str(s['line'])+'.** '+text.replace('\n','\n'+indent+'  '))
 return caption,'\n'.join(lines),steps,raw

def symbol(s):
 t=convert('$'+s+'$');assert t.startswith('$') and t.endswith('$');return t[1:-1]
interfaces=[];members={};edges={};archive=[]
def add(lid,term,raw,pages,heading,deps=None,*,context=None,kind='definition',role='definition',symbols=(),phrases=(),note=None,shape,rendered=None,group=None,relation='exact'):
 body=convert(raw) if rendered is None else rendered
 m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind=kind,statement_original=body,
 relation=relation,depends_on=list(deps or {}),evidence=[dict(page=p,location=heading) for p in pages],
 highlight_symbols=[symbol(s) for s in symbols],highlight_phrases=list(phrases))
 if note:m['variant_note']=note
 key=dict(paper_id=PID,local_id=lid,source_text=term,label=term[0].upper()+term[1:],kind='term')
 if context:
  m['naming_context']=[dict(context_id=lid+'/name',text=context,evidence=m['evidence'])];key['context_id']=lid+'/name'
 assert term in (context or body),(lid,term,body[:300])
 gid=group or lid;existing=next((x for x in interfaces if x['interface_id']==PID+'/'+gid),None)
 if existing:
  assert existing['name']==key['label'];existing['members'].append(m);existing['source_keywords'].append(key)
 else:interfaces.append(dict(interface_id=PID+'/'+gid,rank_group='all',name=key['label'],lean_role=role,type_shape=shape,semantic_boundary=shape,members=[m],source_keywords=[key],central_claim_uses=[],dependencies=[],theorem_explanations={}))
 members[lid]=m;edges[lid]=deps or {};archive.append(dict(local_id=lid,original_tex=raw,evidence=m['evidence']))

add('D1','reward function',passage('Let $Q$ be a probability distribution', 'In the context of transfer learning'),[6],
 'Section 2.1 — target bandit and reward functions',kind='source_passage',phrases=['reward function'],symbols=[r'f_{k}^{Q}'],shape='Independent target-bandit vectors with bounded arm rewards and conditional-mean functions; policy maps are selected using the permitted history.')
add('D2','batch dataset',passage('In the context of transfer learning','As mentioned in the introduction'),[6,7],
 'Section 2.1 — pre-collected source bandit dataset',{'D1':'The source bandit uses the same covariate space and K-arm bounded-reward format.'},kind='source_passage',phrases=['batch dataset'],symbols=[r'\mathcal{D}^{P}'],shape='Pre-collected source observations, source conditional reward functions, and n=max(nQ,nP).')
add('D3','covariate shift model',passage('As mentioned in the introduction','Recall that $\\pi^{\\star}$'),[7],
 'Section 2.1 — covariate shift model',{'D1':'Q supplies target conditional rewards.','D2':'P supplies source conditional rewards and its marginal law.'},kind='condition',role='hypothesis',phrases=['covariate shift model'],symbols=[r'f_{k}(x)'],shape='Common conditional reward distributions and common reward functions; preserve the printed P_X!=Q_X assertion.')
add('D4','regret',passage('Recall that $\\pi^{\\star}$','Finally, we would like to emphasize'),[7],
 'Section 2.1 — oracle policy and expected regret, equation (2)',{'D3':'The regret uses the common reward functions f_k.','D5':'The evaluated policy uses the admissible observed-data history.'},phrases=['regret'],symbols=[r'R_{n_Q}(\pi)',r'\pi^{\star}(x)'],shape='Expected target cumulative reward gap to a pointwise maximizing oracle; retain the full original expression and arbitrary oracle tie-breaking.')
add('D5','policy',passage('Finally, we would like to emphasize',r'\subsection{Assumptions}'),[7],
 'Section 2.1 — history available to a target policy',{'D1':'The policy sees past observed target rewards and the current target covariate.','D2':'It also sees the complete pre-collected source dataset.'},kind='condition',role='hypothesis',phrases=['policy'],shape='Target decisions may depend on prior target observations, current covariates and all source data.')
add('D6','admissible policies',passage('Here, the infimum is taken','We now discuss several important implications.'),[14],
 'Section 3.2 — admissible policies for the lower bound',{'D5':'The general policy-history convention in Section 2.1 supplies the earlier source-data allowance; this later displayed history omits that dataset.'},kind='condition',role='hypothesis',phrases=['admissible policies'],note='This passage lists target observations and the current covariate only. Section 2.1 explicitly also allows the full source dataset. Both passages are preserved rather than editing this history.',shape='Nonanticipating policy class for the lower-bound infimum, with the source-history omission explicitly recorded.')
members['D6']['invocation_context_original']=[dict(text=convert(passage('Similar to Theorem','Recognizing that the self-similar function space')),evidence=[dict(page=19,location='Paragraph following Theorem 4')])]
add('D7','Smoothness',env('assumption','assumption:smooth'),[7],
 'Assumption 1 (Smoothness)',{'D3':'The assumption restricts every common reward function.'},context='Smoothness',kind='assumption',role='hypothesis',phrases=['Assumption 1'],symbols=[r'C_{\beta}'],shape='Every arm reward is beta-Holder in sup norm for 0<beta<=1 and a common C_beta>0.')
add('D8','second pointwise maximum',passage('Next, it is natural to expect that the gap','Equipped with these notations'),[7,8],
 'Section 2.2 — pointwise maximum and second pointwise maximum',{'D3':'The order statistics are formed from all common reward functions.'},phrases=['second pointwise maximum'],symbols=[r'f_{(2)}(x)'],shape='Largest reward and largest strictly smaller reward; if all rewards coincide the second value equals the maximum. This is not the second order statistic with multiplicity.')
add('D9','Margin',env('assumption','assumption:margin'),[8],
 'Assumption 2 (Margin)',{'D8':'The positive reward-gap event uses f_(1) minus f_(2).','D1':'Its probability is under the target covariate law Q_X.'},context='Margin',kind='assumption',role='hypothesis',phrases=['Assumption 2'],shape='Target probability of a strictly positive reward gap at most delta is bounded by C_alpha*delta^alpha for every delta in (0,1].')
add('D10','Bounded density',env('assumption','assumption:bounded-density'),[8],
 'Assumption 3 (Bounded density)',{'D1':'The ball-mass condition is imposed on the target covariate marginal.'},context='Bounded density',kind='assumption',role='hypothesis',phrases=['Assumption 3'],symbols=[r'\underline{q}',r'\overline{q}'],shape='Two-sided target mass bounds on closed sup-norm balls centered in the target support, for every radius in (0,1].')
add('D11','covariate-arm pairs',passage('In addition, the covariate-arm pairs','We make a note that this i.i.d.'),[9],
 'Section 2.2 — iid source covariate-arm sampling',{'D2':'The condition concerns the pre-collected source observations.'},kind='condition',role='hypothesis',phrases=['covariate-arm pairs'],symbols=[r'\mu(\cdot \, | \, x)'],shape='Source covariate-arm pairs are iid from P_X and a fixed conditional behavior policy mu; preserve this additional model assumption.')
add('D12','transfer exponent',env('definition','def:transfer'),[8],
 'Definition 1 (Transfer exponent)',{'D1':'Q_X supplies the target support and ball masses.','D2':'P_X supplies the source ball masses.'},phrases=['transfer exponent'],symbols=[r'\gamma'],shape='Smallest nonnegative extended exponent satisfying the source-to-target ball mass bound with some positive constant c_gamma; retain smallest and the infinity case as printed.')
add('D13','exploration coefficient',env('definition','def:explore-coef'),[9],
 'Definition 2 (exploration coefficient)',{'D11':'The infimum uses the source behavior distribution mu.','D1':'It ranges over arms and covariates in the target support.'},phrases=['exploration coefficient'],symbols=[r'\kappa'],shape='Infimum of K*mu(k|x) over all arms and the entire target support, taking values in [0,1].')
add('D14','nonparametric contextual K-armed bandits',passage('Finally, we assume the number of arms',r'\section{Minimax Rate of Convergence}'),[9],
 'Section 2.2 — general parameter space Pi',{'D3':'The parameter space is in the preceding covariate-shift model.','D7':'It includes Assumption 1.','D9':'It includes Assumption 2.','D10':'It includes Assumption 3.','D11':'The preceding iid source-sampling convention remains in force.','D12':'It includes Definition 1 and its transfer parameters.','D13':'It includes Definition 2 and its exploration parameter.'},kind='definition',context=convert(passage('Denote by $\\Pi(K,\\beta,C_{\\beta}',r'\section{Minimax Rate of Convergence}')).replace('$K$','K'),phrases=['nonparametric contextual'],symbols=[r'\Pi(K,\beta,\alpha,\gamma, \kappa )'],shape='The full general parameter class and its shorthand, including all constants omitted in the shorthand and fixed K. No hidden constants are set equal to one.')

add('D15','bins',passage('Here, for any non-negative integer', 'As an important observation'),[9],
 'Section 3.1 — dyadic bins, equation (5)',phrases=['bins'],symbols=[r'\mathcal{B}_{l}'],shape='Closed dyadic cubes on [0,1]^d and side length |B|=2^(-l); retain closed endpoints and the separate boundary selection convention.')
add('D16','bin in the partition',passage('First, for any $x\\in\\mathcal{X}$','Before delving into the details'),[10],
 'Section 3.1 — selecting bins and counting target visits',{'D15':'The selected bin belongs to the current dyadic partition.','D1':'Visit counts refer to target covariates.'},phrases=['bin'],symbols=[r'B_{t}(x)',r'N_{t}(B)'],shape='Select a containing bin by center closest to origin; N_t sums s<=t even though the preceding prose says prior to t. The local policy correspondence is preserved as source context.')
add('D17','perfect tree',passage('To this end, denote by', 'Next, given a subset'),[10],
 'Section 3.1 — perfect tree and child bins',{'D15':'Tree nodes are bins in the dyadic collections.'},phrases=['perfect tree'],symbols=[r'\mathsf{child}(B)'],shape='Tree of dyadic bins and child(B) relation; retain the source depth indexing and leaf-partition description.')
add('D18','number of samples',passage('Next, given a subset','Let $\\overline{Y}_{k}^{P}(B;\\mathcal{D})$'),[10],
 'Section 3.1 — source sample count, equation (7)',{'D2':'The count uses a subset of the pre-collected source data.','D15':'It restricts covariates to a bin.'},phrases=['number of samples'],symbols=[r'n_{k}^{P}(B;\mathcal{D})'],shape='Count of source records in a bin with the specified arm.')
add('D19','empirical mean',passage('Let $\\overline{Y}_{k}^{P}(B;\\mathcal{D})$', 'In addition, for any non-negative integer'),[10],
 'Section 3.1 — source empirical mean, equation (8)',{'D18':'The denominator is the source bin-arm count, with the zero-count branch explicitly defined.'},phrases=['empirical mean'],symbols=[r'\overline{Y}_{k}^{P}(B;\mathcal{D})'],note='The source summand prints Y rather than Y_i. The indexed record and the unindexed summand are both preserved.',shape='Source bin-arm empirical reward mean, equal to zero when the count is zero; retain the printed unindexed Y in the sum.')
add('D20','confidence bound',passage('In addition, for any non-negative integer','With these notations in place'),[10],
 'Section 3.1 — confidence bound, equation (9)',{'D18':'The statistical radius uses the source bin-arm sample count.','D15':'The radius and bias term use bin side length.','D7':'The bias scale uses the given smoothness parameters beta and C_beta.','D12':'The zero-pull branch uses the transfer exponent gamma.','D13':'The zero-pull branch also uses the exploration coefficient kappa.'},phrases=['confidence bound'],symbols=[r'U_{k}'],shape='Two-branch confidence radius with log-plus=max(log,1), bias floor and 1/0=infinity; this is the known-parameter radius.')
add('D21','upper bound on the number of pulls',passage('In order to achieve such an adaptive partition','Note that the confidence bound'),[10],
 'Section 3.1 — upper bound on pulls, equation (10)',{'D20':'The minimum is the first nonnegative pull count for which the known-parameter confidence radius is at most its bias floor.'},phrases=['upper bound on the number of pulls'],symbols=[r'\tau^\star_k(B;\mathcal{D})'],shape='Minimum nonnegative integer pull count satisfying the printed threshold criterion; retain the set-minimum convention.')
cap,body,steps,raw=algorithm('alg:EA-TL')
add('D22',cap,raw,[12],'Procedure 1 — '+cap,{'D18':'Step 2 initializes source bin-arm counts.','D19':'Step 2 initializes source empirical means.','D21':'In its known-parameter use, Step 2 initializes the pull limits by (10).','D1':'Selected target arms produce the observed rewards used in the mean updates.'},context=cap,rendered=body,phrases=['Procedure 1'],symbols=[r'\widetilde{\pi}_{t}'],shape='Original 25-line successive-elimination procedure, with its control hierarchy and source comments retained. U is an input; this member records its known-parameter instantiation.')
members['D22']['algorithm_steps_original']=steps
cap,body,steps,raw=algorithm('alg:UCB-TL')
add('D23',cap,raw,[11],'Algorithm 1 — '+cap,{'D22':'Each leaf runs Procedure 1 with the known-parameter confidence function.','D20':'The zero-pull elimination and calls to Procedure 1 use U from (9).','D21':'Splitting tests compare every active arm count with its limit (10).','D16':'The algorithm selects the bin containing the current covariate, with the earlier boundary convention.','D17':'Splitting replaces a bin by its children.','D19':'Source empirical means supply the zero-pull arm elimination.'},context=cap,rendered=body,phrases=['Algorithm 1'],shape='Full 24-line known-parameter transfer algorithm, preserving initialization, adaptive partition, elimination and returned policy.')
members['D23']['algorithm_steps_original']=steps
add('D24','piecewise-constant functions',passage('For any function $f(\\cdot)$','Recall that $\\mathcal{B}_{l}$'),[15],
 'Section 4.1 — piecewise-constant projection, equation (15)',{'D15':'The projection is defined over a bin in the covariate space.'},phrases=['piecewise-constant functions'],symbols=[r'\Gamma_{B}'],shape='Bin average under lambda when its mass is positive, and zero otherwise. No support-only supremum is substituted in the later self-similarity condition.')
add('D25','self-similar',env('definition','def:self-similar'),[15],
 'Definition 3 (Self-similarity)',{'D24':'The lower bias bound uses the bin-average projection Gamma_B.','D15':'The two suprema range over every dyadic bin at each integer level and every point of that bin.'},phrases=['self-similar'],symbols=[r'b2^{-\beta l}'],shape='For an individual Holder function, a global lower bias bound at every integer l>=l0. The Holder-class notation is resolved separately from the all-arms smoothness assumption.')
add('D26','Self-similarity',env('assumption','assumption:self-similar'),[16],
 'Assumption 4 (Self-similarity)',{'D25':'One common arm must satisfy Definition 3 under both measures with the same parameters.','D3':'The selected f_k is a common reward function.','D11':'One measure is the source covariate law conditional on selection of that arm.','D1':'The other measure is the target covariate law Q_X.'},context='Self-similarity',kind='assumption',role='hypothesis',phrases=['Assumption 4'],shape='Existence of one arm whose reward is self-similar under both Q_X and P_(X|pi=k), not all arms or different arms for the two laws.')
add('D27','self-similar function space',passage('We denote by $\\Pi(K,\\beta,C_{\\beta}',r'\subsection{Adaptive algorithm}'),[16],
 'Section 4.1 — self-similar parameter space Pi',{'D14':'The self-similar class retains the general bandit conditions and transfer definitions.','D26':'It additionally imposes Assumption 4 with l0 and b.'},context=convert(passage('Recognizing that the self-similar function space','Theorem \\ref{thm:lower-bound-adaptive}')),phrases=['nonparametric contextual'],symbols=[r'\Pi(K,\beta,\alpha,\gamma, \kappa,l_{0},b)'],shape='Self-similar subfamily with full constants and its shorthand; the extra assumption is retained distinctly from the general parameter class.')
members['D27']['naming_context'][0]['evidence']=[dict(page=19,location='Paragraph following Theorem 4')]
cap,body,steps,raw=algorithm('alg:smoothness')
add('D28',cap,raw,[18],'Procedure 2 — '+cap,{'D1':'The target branch collects bounded rewards while choosing arms uniformly.','D2':'The source branch uses the first T records and returns the unused-source start index.','D15':'The estimator uses two dyadic resolutions and a finer dyadic grid.','D16':'The containing-bin convention supplies a choice when a point lies on closed bin boundaries.'},context=cap,rendered=body,phrases=['Procedure 2'],symbols=[r'\widehat{\beta}'],shape='Full 21-line smoothness-estimation procedure including both sample-source branches, bandwidths, grid, estimate (16), logarithm, clipping and returned split indices. Its inputs are the bounds on smoothness and transfer, not the true unknown parameters.')
members['D28']['algorithm_steps_original']=steps
members['D28']['transcription_note']='Equation (16), including both indicator factors and the grouping of the numerator and denominator, agrees with the inspected PDF on page 18. The original TeX and the printed equation number are retained.'
uhat=passage('Given a subset $\\mathcal{D}$ of the source data', 'The associated non-negative upper bound on play rounds')
add('D29','confidence bound',uhat,[17,18],
 'Section 4.2 — adaptive confidence bound, equation (17)',{'D18':'The radius uses the source bin-arm count in the supplied data subset.','D15':'The radius uses bin side length.','D28':'Its bias exponent is the smoothness estimate returned by Procedure 2.'},context='To construct an adaptive procedure in Algorithm 2, we substitute it with the confidence bound',symbols=[r'\widehat{U}_{k}'],note='The zero-pull branch prints log, not log-plus; its square-root domain is not silently repaired.',shape='Adaptive radius with beta-hat and C-beta upper bound. The positive-pull branch has log-plus, whereas the zero-pull branch has ordinary log.')
add('D30','upper bound on play rounds',passage('The associated non-negative upper bound on play rounds','It is noteworthy that the source sample size'),[18],
 'Section 4.2 — adaptive upper bound on play rounds, equation (18)',{'D29':'The first threshold crossing uses the adaptive confidence radius and its estimated-smoothness bias floor.'},phrases=['upper bound on play rounds'],symbols=[r'\widehat{\tau}^\star_k(B;\mathcal{D})'],shape='Adaptive stopping threshold using U-hat, beta-hat and the upper bound on C_beta.')
# The original Procedure 1 body remains untouched; the adaptive source explicitly supplies U-hat and tau-hat.
cap,body,steps,raw=algorithm('alg:EA-TL')
context_raw=passage('With the smoothness estimate $\\widehat{\\beta}$ in hand','Given a subset $\\mathcal{D}$ of the source data')
context_text=convert(context_raw)
add('D22a',cap,raw,[12,17,18],'Procedure 1 — adaptive invocation in Algorithm 2',{'D18':'The source counts use the retained decision-making subset.','D19':'The source empirical means use that same subset.','D30':'The adaptive invocation uses the replacement pull limits (18), specified by Algorithm 2.','D29':'Algorithm 2 passes U-hat rather than the original U.','D1':'The procedure updates means with newly observed target rewards.'},context=cap,rendered=body,group='D22',relation='specialization',phrases=['Procedure 1'],symbols=[r'\widetilde{\pi}_{t}'],note='The body is the original Procedure 1, including its reference to (10). Algorithm 2 and Section 4.2 specify substitution of the confidence bound (17) and associated threshold (18); the source leaves the original initializer reference unchanged.',shape='Source-backed adaptive invocation of the same elimination procedure; keep the original body and record the specified substitutions separately.')
members['D22a']['algorithm_steps_original']=steps
members['D22a']['invocation_context_original']=[dict(text=context_text,evidence=[dict(page=17,location='Section 4.2 — adaptive substitutions')]),dict(text=convert(passage('The associated non-negative upper bound on play rounds','It is noteworthy that the source sample size')),evidence=[dict(page=18,location='Equation (18)')])]
cap,body,steps,raw=algorithm('alg:UCB-TL-adaptive')
add('D31',cap,raw,[17],'Algorithm 2 — '+cap,{'D28':'The first stage calls Procedure 2 and retains its target actions as the policy prefix.','D22a':'The second stage calls Procedure 1 with the adaptive bound and remaining source data.','D29':'Zero-pull elimination and the procedure calls use U-hat.','D30':'Splitting uses the adaptive pull thresholds.','D16':'The current target observation selects its containing bin.','D17':'Splits replace a bin by its dyadic children.','D19':'Elimination uses empirical source means from the retained subset.'},context=cap,rendered=body,phrases=['Algorithm 2'],shape='Complete 26-line adaptive algorithm, retaining the initial exploration policy, source-data split and adaptive elimination stage.')
members['D31']['algorithm_steps_original']=steps

def main():
 for name,data in [('source-passages.json',dict(paper_id=PID,members=list(members.values()))),('interface-draft.json',interfaces),('evidence/source-passages-tex.json',archive)]:
  (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 print(f'Saved {len(interfaces)} interfaces and {len(members)} source members.')
if __name__=='__main__':main()
