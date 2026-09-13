"""Main-text statement dependencies for the four resource lower bounds."""
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
PID=ROOT.name
SOURCE=(ROOT/'evidence/main-only.tex').read_text()
MACROS=(ROOT/'evidence/macros.tex').read_text()
PRELIMS=(ROOT/'evidence/prelims.tex').read_text()
TPCA=(ROOT/'evidence/tensorPCA.tex').read_text()
ATPCA=(ROOT/'evidence/ATPCA.tex').read_text()
NGCA=(ROOT/'evidence/NGCA.tex').read_text()
CCA=(ROOT/'evidence/CCA.tex').read_text()
REFS={'fig: memory-bounded-algorithm':'1','fourier_gauss_appendix':'I.2',
      'eq: symmetric_tpca_setup':'6','eq: symmetric_atpca_setup':'9','eq: ngca-model':'14',
      'eq: ngca-likelihood':'15','eq:k-CCA-correlation':'29','eq:kCCA-likelihood':'30','eq:kCCA-coordprior':'31'}

def passage(start,end,source=SOURCE):
    a=source.index(start)
    return source[a:source.index(end,a)].strip()

def env(kind,label,source=SOURCE):
    hits=[m[1] for m in re.finditer(r'\\begin\{'+kind+r'\}(.*?)\\end\{'+kind+r'\}',source,re.S) if r'\label{'+label+'}' in m[1]]
    assert len(hits)==1
    return hits[0].split(r'\label{'+label+'}',1)[1].strip()

def convert(raw):
    raw=re.sub(r'(?<!\\)%[^\n]*','',raw)
    raw=raw.replace(r'\citet{montanari2014statistical}','Montanari and Richard [63]')
    raw=re.sub(r'\\eqref\{([^}]+)\}',lambda m:'('+REFS[m[1]]+')',raw)
    raw=re.sub(r'\\ref\{([^}]+)\}',lambda m:REFS[m[1]],raw)
    assert r'\cite' not in raw
    sub=re.search(r'\\begin\{subequations\}\s*\\label\{([^}]+)\}',raw)
    subnumber=REFS[sub[1]] if sub else None
    raw=re.sub(r'\\begin\{subequations\}\s*\\label\{[^}]+\}|\\end\{subequations\}','',raw)
    count=0
    def display(m):
        nonlocal count
        kind,body=m[1],m[2]
        label=re.search(r'\\label\{([^}]+)\}',body)
        tag=''
        if not kind.endswith('*'):
            if label:tag=REFS[label[1]]
            elif subnumber:tag=subnumber+chr(ord('a')+count);count+=1
            else:raise ValueError('Unmapped numbered display')
        body=re.sub(r'\\label\{[^}]+\}','',body).strip()
        if r'\\' in body:body=r'\begin{aligned}'+body+r'\end{aligned}'
        else:body=body.replace('&','')
        return r'\['+body+(r'\tag{'+tag+'}' if tag else '')+r'\]'
    raw=re.sub(r'\\begin\{(align\*?|equation\*?)\}(.*?)\\end\{\1\}',display,raw,flags=re.S)
    raw=re.sub(r'\\label\{[^}]+\}','',raw)
    out=subprocess.run(['pandoc','-f','latex','-t','markdown','--wrap=none'],input=MACROS+'\n\\begin{document}\n'+raw+'\n\\end{document}',text=True,capture_output=True,check=True).stdout.strip()
    out=out.replace(r'\bm',r'\boldsymbol')
    out=re.sub(r'\$\$(.*?)\$\$',lambda m:'\n\\[\n'+m[1]+'\n\\]\n',out,flags=re.S)
    out=out.replace(r'\[63\]','[63]')
    assert '[^' not in out and 'reference-type' not in out
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

add('D1','memory bounded estimation algorithm',env('definition','def:memory-bounded-algorithm',PRELIMS),[12],
    'Definition 1 (Memory bounded estimation algorithm with resource profile (N, T, s))',
    phrases=['memory bounded estimation algorithm'],symbols=[r'f_{t,i}',r'g: \{0,1\}^\state \rightarrow \estimatespace'],
    shape='N sequential samples revisited for T passes, an initially zero s-bit state, arbitrary time/sample-indexed update functions and a final estimator function. The printed definition is deterministic.')
add('D2','Symmetric Tensor PCA',passage('In the symmetric order-',r'\subsection{Statistical-Computational Gap',TPCA),[19],
    'Section 4.1 — Symmetric Tensor PCA, equation (6)',kind='source_passage',context='Symmetric Tensor PCA',symbols=[r'\bm V^{\otimes k}',r'\dmu{\bm V}'],
    note='The source writes X_{1:m} while describing N samples. This notation is retained; m is not treated as an additional sample-size parameter.',
    shape='N iid Gaussian-noise order-k tensors with mean lambda times V tensor-power k divided by sqrt(d^k), estimating a vector V of norm sqrt(d).')
add('D3','Asymmetric Tensor PCA',passage('In the asymmetric order-',r'\subsection{Statistical-Computational Gap',ATPCA),[25],
    'Section 5.1 — Asymmetric Tensor PCA, equation (9)',kind='source_passage',context='Asymmetric Tensor PCA',symbols=[r'\bm V_1 \otimes \bm V_2 \dotsb \otimes \bm V_k',r'\paramspace'],
    shape='N iid Gaussian-noise order-k tensors whose mean is lambda divided by sqrt(d^k) times a rank-one product of k vectors of norm sqrt(d); the target is the full tensor, not an individual factor.')
add('D4','Non-Gaussian Component Analysis',passage('In the Non-Gaussian Component Analysis',r'The likelihood ratio',NGCA),[29],
    'Section 6.1 — Non-Gaussian Component Analysis, equations (14a) and (14b)',kind='source_passage',symbols=[r'\bm x_i',r'\nongauss'],phrases=['Non-Gaussian Component Analysis'],
    shape='Iid observations with a non-Gaussian scalar component along V/sqrt(d) and independent standard Gaussian noise projected onto its orthogonal complement; V has norm sqrt(d).')
add('D5','Degree of Non-Gaussianity',passage('The statistical and computational difficulty',r'\subsubsection{Assumptions on the Non-Gaussian Component}',NGCA),[29],
    'Section 6.1.1 — Degree of Non-Gaussianity',{'D4':'The order-k problem is the NGCA observation model with the stated moment restrictions on its scalar component.'},role='predicate',context='Degree of Non-Gaussianity',symbols=[r'\lambda > 0'],phrases=['NGCA'],
    shape='The first k-1 scalar moments match the standard Gaussian and the absolute kth-moment difference is lambda>0, with k at least two. This original problem definition supplies the meaning of k and lambda in Theorem 3.')
add('D6','non-Gaussian distributions',passage('The computational lower bounds we prove holds',r'Before stating these assumptions',NGCA),[30],
    'Section 6.1.2 — non-Gaussian distributions with a density',role='hypothesis',kind='condition',phrases=['non-Gaussian distributions'],symbols=[r'\refmu = \gauss{0}{1}'],
    shape='The scalar non-Gaussian distribution has a density with respect to the univariate standard Gaussian; this is the section-wide domain restriction for the numbered assumptions.')
add('D7','Hermite polynomials',passage(r'We will make extensive use of the Hermite polynomials',r'\paragraph{Miscellaneous:}',PRELIMS),[12],
    'Section 2.1 — Hermite polynomials',kind='source_passage',phrases=['Hermite polynomials'],
    note='The main text specifies orthonormality for the Gaussian measure and refers to Appendix I.2 for the construction. That appendix was not inspected; no extra sign or leading-coefficient convention is supplied.',
    shape='The named univariate and multivariate orthonormal Hermite families for the corresponding standard Gaussian measures, as characterized in main-text notation.')
add('D8','Hermite coefficient',passage('Before stating these assumptions',r'We now state our assumptions below.',NGCA),[30],
    'Section 6.1.2 — Hermite coefficient',{'D6':'The equivalent likelihood-ratio formula uses the density of nu with respect to the scalar standard Gaussian.','D7':'The coefficient is the expectation under nu of the orthonormal Hermite polynomial H_i.'},kind='source_passage',phrases=['Hermite coefficient'],symbols=[r'\hat{\nongauss}_i'],
    shape='Coefficients nu-hat_i=E_nu H_i for nonnegative integer i, with H_0=1, the Gaussian-density formula and the printed Plancheral identity retained.')
add('D9','Moment Matching Assumption',env('assumption','ass: moment-matching',NGCA),[30],
    'Assumption 1 (Moment Matching Assumption)',{'D8':'The zeros in the first formula refer to the Hermite coefficients defined immediately above.'},kind='assumption',role='hypothesis',phrases=['Moment Matching Assumption','Assumption 1'],
    shape='For k>=2, Hermite coefficients 1 through k-1 vanish; retain the source’s equivalent raw-moment identities as well.')
add('D10','Bounded Signal Strength Assumption',env('assumption','ass: bounded-snr',NGCA),[30],
    'Assumption 2 (Bounded Signal Strength Assumption)',{'D8':'The square-sum bound is over all positive-order Hermite coefficients of the likelihood ratio.'},kind='assumption',role='hypothesis',phrases=['Bounded Signal Strength Assumption','Assumption 2'],
    shape='Sum over positive-order squared Hermite coefficients is at most K^2 lambda^2, with lambda and K nonnegative; retain the source’s extra Z~N(0,1) clause.')
add('D11','Locally Bounded Likelihood Ratio Assumption',env('assumption','ass: locally-bounded-LLR',NGCA),[30],
    'Assumption 3 (Locally Bounded Likelihood Ratio Assumption)',{'D6':'The likelihood ratio is the density of nu relative to the univariate standard Gaussian.'},kind='assumption',role='hypothesis',phrases=['Locally Bounded Likelihood Ratio Assumption','Assumption 3'],
    shape='Pointwise density-ratio deviation bounded by K lambda (1+abs(z))^kappa only at z where that bound is at most one, with nonnegative parameters.')
add('D12','Canonical Correlation Analysis',passage('In the order-',r'Note that we have not explicitly specified',CCA),[38],
    'Section 7.1 — Canonical Correlation Analysis, equation (29)',kind='source_passage',phrases=['Canonical Correlation Analysis'],symbols=[r'\bm V',r'\mview{\bm x_i}{1}'],
    shape='Iid k-view observations whose cross moment is lambda times a rank-one tensor V/sqrt(d^k), with unit factor vectors and tensor norm sqrt(d^k). The general model does not otherwise fix the sampling measure.')
add('D13','likelihood ratio',passage('Note that we have not explicitly specified',r'Finally, our computational lower bound',CCA),[39],
    'Section 7.1 — likelihood ratio, equations (30a) and (30b)',{'D12':'The density uses the k views and the cross-moment parameter tensor from the k-CCA model.'},symbols=[r'\lambda_k'],phrases=['likelihood ratio'],
    note='Equation (30b) prints (2/pi)^(k/2)=(E|Z|)^(k/2). The equality is inconsistent for a standard Gaussian; both expressions are preserved rather than silently changing the second exponent.',
    shape='The specific density 1+(lambda/lambda_k) times the sign of the normalized tensor inner product, relative to the standard Gaussian in dimension kd; retain both printed normalizer expressions and the range 0<=lambda<=lambda_k.')
add('D14','cross-moment tensor',passage('Finally, our computational lower bound',r'\subsection{Statistical-Computational Gap',CCA),[39],
    'Section 7.1 — cross-moment tensor restricted by equation (31)',{'D12':'The additional promise restricts the k-CCA parameter to a product of standard basis vectors scaled by sqrt(d^k).'},role='predicate',kind='condition',
    context='The goal is to estimate the cross-moment tensor V.',symbols=[r'\bm V = \sqrt{d^k} \cdot \bm e_{i_1}\otimes \bm e_{i_2} \dotsb \otimes \bm e_{i_k}'],
    shape='Additional parameter promise V=sqrt(d^k) times a tensor product of standard basis vectors, with each index in [d]. Distinct coordinate indices are not imposed.')
# The naming sentence for D14 occurs on the preceding page, separately from (31).
members['D14']['naming_context']=[dict(context_id='D14/name',text=convert('The goal is to estimate the cross-moment tensor $\\bm V$.'),evidence=[dict(page=38,location='Section 7.1 — closing sentence of the general model description')])]

def main():
    for name,data in [('source-passages.json',dict(paper_id=PID,members=list(members.values()))),
                      ('evidence/source-passages-tex.json',archive),('interface-draft.json',interfaces)]:
        (ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    ambient=[('Section 2.1 — Important sets',passage(r'\paragraph{Important sets:}',r'\paragraph{Linear Algebra:}',PRELIMS),[11]),
             ('Section 2.1 — Linear Algebra',passage(r'\paragraph{Linear Algebra:}',r'\paragraph{Asymptotic notation:}',PRELIMS),[11]),
             ('Section 2.1 — Asymptotic notation',passage(r'\paragraph{Asymptotic notation:}',r'\paragraph{Important distributions:}',PRELIMS),[11]),
             ('Section 2.1 — Important distributions',passage(r'\paragraph{Important distributions:}',r'\paragraph{Hermite polynomials:}',PRELIMS),[12]),
             ('Section 2.1 — Miscellaneous',passage(r'\paragraph{Miscellaneous:}',r'\subsection{Statistical Inference Problems}',PRELIMS),[12]),
             ('Section 2.2 — model and estimator',passage('A general statistical inference problem',r'An estimator $\hat{\bm V}:',PRELIMS),[12])]
    (ROOT/'ambient-conventions.json').write_text(json.dumps(dict(paper_id=PID,passages=[dict(name=n,statement_original=convert(raw),original_tex=raw,evidence=[dict(page=p,location=n) for p in pages]) for n,raw,pages in ambient]),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} interfaces with original source passages.')

if __name__=='__main__':main()
