"""Source-local extraction. Dependency maps are reviewed mathematical input, not keyword inference."""
import copy
import json
import re
import sys
from pathlib import Path
from transcribe_inventory import ROOT, SOURCE, PAPER_ID, convert

SKILL = Path('skills/statistical-paper-census/scripts')
sys.path.insert(0, str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics

REFS = {'eq:unprojectedmodel':'2.1', 'eq:projectedmodel':'2.2', 'eq:likelihood':'2.3', 'eq:losslessPi':'2.4',
        'eq:R':'2.5','eq:Tk':'2.6','eq:sk':'2.8','eq:tildesk':'2.11',
        'eq:dk':'2.12','eq:tdk':'2.13','eq:Mk':'2.15','eq:tMk':'2.16',
        'eq:Vk':'2.17','eq:tVk':'2.18','eq:momentoptunprojected':'2.19',
        'eq:momentoptprojected':'2.20','eq:GPwhitenoise':'3.1',
        'eq:Fourierbasis':'3.2','eq:fourierbasis':'3.3','eq:MRAG':'3.4',
        'eq:bandlimitedspherical':'4.1','eq:Bl':'4.2','eq:C3basis':'4.3',
        'eq:zorthogonality':'4.4','eq:indices':'4.5','eq:bandlimitedS2':'4.6',
        'eq:cryoEMbandlimited':'4.7','eq:uls':'4.8','eq:Bls':'4.9',
        'eq:projectedobservations':'4.10','eq:cryoEMmodel':'4.11',
        'eq:projcryoEMbandlimited':'4.12','eq:projbandlimited':'4.13','eq:indicesproj':'4.14',
        'sec:sr':'D.2','eq:u-theta':'D.11','sec:rc-harmonic':'D.1',
        'eq:hatv-trans':'D.31','sec:unprojCEM':'D.3','sec:projCEM':'D.4',
        'eq:cryoEMPi':'D.57','thm:seriesexpansion':'2.2','sec:func-est-so2':'3',
        'sec:func-est-so3':'4','thm:landscape':'2.13', 'thm:FI':'2.7','thm:benignlandscape':'2.11'}

def passage(start, end, source=SOURCE):
    a = source.index(start)
    return source[a:source.index(end, a)].strip()

def env(kind, contains):
    found = [m[1] for m in re.finditer(r'\\begin\{' + kind + r'\}(.*?)\\end\{' + kind + r'\}', SOURCE, re.S)
             if contains in m[1]]
    assert len(found) == 1, (kind, contains, len(found))
    return found[0].strip()

def equation(label):
    found = [m[0] for m in re.finditer(r'\\begin\{equation\}.*?\\end\{equation\}', SOURCE, re.S)
             if r'\label{' + label + '}' in m[0]]
    assert len(found) == 1, label
    return found[0]

def display_row(begin, label):
    raw = passage(begin, r'\label{' + label + '}')
    raw = raw.replace('&', '').rstrip(',')
    return r'\[' + raw + r'\tag{' + REFS[label] + r'}\]'

def ev(pages, location):
    return [dict(page=p, location=location) for p in pages]

interfaces = []
members = {}
edges = {}
raw_archive = []

def add(lid, keyword, raw, pages, heading, deps=None, *, kind='definition',
        role='definition', symbols=(), phrases=(), context=None, group=None, note=None, shape):
    body = convert(raw, refs=REFS, equation_numbers=REFS)
    name = keyword[0].upper() + keyword[1:]
    m = dict(paper_id=PAPER_ID, local_id=lid, local_label=heading, source_kind=kind,
             source_heading=heading, statement_original=body, relation='exact',
             depends_on=list(deps or {}), evidence=ev(pages, heading),
             highlight_symbols=list(symbols), highlight_phrases=list(phrases))
    kw = dict(paper_id=PAPER_ID, local_id=lid, source_text=keyword, label=name, kind='term')
    if context:
        text = convert(context, refs=REFS, equation_numbers=REFS)
        m['naming_context'] = [dict(context_id=lid+'/name', text=text, evidence=ev(pages, heading))]
        kw['context_id'] = lid+'/name'
        assert keyword in text, (lid, keyword, text)
    else:
        assert keyword in body, (lid, keyword, body)
    if note:
        m['variant_note'] = note
    gid = group or lid
    match = next((x for x in interfaces if x['interface_id'] == PAPER_ID+'/'+gid), None)
    if match:
        assert match['name'] == name
        match['members'].append(m)
        match['source_keywords'].append(kw)
    else:
        interfaces.append(dict(interface_id=PAPER_ID+'/'+gid, rank_group='all', name=name,
            lean_role=role, type_shape=shape, semantic_boundary=shape+' Preserve the separate source passages and their conditions; no library-availability claim.',
            members=[m], source_keywords=[kw], central_claim_uses=[], dependencies=[], theorem_explanations={}))
    members[lid] = m
    edges[lid] = deps or {}
    raw_archive.append(dict(local_id=lid, original_tex=raw, naming_tex=context, evidence=m['evidence']))

add('D1','Haar probability measure',passage(r'Let $\theta_* \in \R^d$ be an unknown',r' In the \emph{unprojected'),[5],
    'Section 2.1 — Haar probability measure', symbols=[r'\Lambda'],
    shape='Haar probability measure on the fixed compact orthogonal subgroup, normalized to mass one and invariant under left and right translation.')
add('D2','unprojected orbit recovery model',passage(r'In the \emph{unprojected orbit recovery model}',r'The signal $\theta_*$ is identifiable'),[5],
    'Section 2.1 — unprojected orbit recovery model, equation (2.1)',{'D1':r'The rotations $g_i$ in (2.1) are independently drawn from the Haar probability measure $\Lambda$.'},
    kind='source_passage',symbols=[r'g_i \cdot \theta_*'],phrases=['unprojected orbit recovery model'],
    shape='Independent Haar rotations of a fixed real signal plus independent isotropic Gaussian noise in the original dimension.')
add('D3','projected orbit recovery model',passage(r'In the \emph{projected orbit recovery model}',r'Our goal is again'),[5],
    'Section 2.1 — projected orbit recovery model, equation (2.2)',{'D1':r'The projected samples retain Haar-distributed rotations $g_i\sim\Lambda$.'},
    kind='source_passage',symbols=[r'\Pi(g_i \cdot \theta_*)'],phrases=['projected orbit recovery model'],
    shape='A known linear map Pi, not necessarily an orthogonal projection, is applied after Haar rotation; Gaussian noise is in the projected dimension.')
add('D4','orbit',passage(r'The signal $\theta_*$ is identifiable',r'Our goal is to estimate $\orbit_{\theta_*}$'),[5],
    'Section 2.1 — orbit',symbols=[r'\mathcal{O}_{\theta_*}'],
    shape='The orbit of a vector under the fixed compact orthogonal subgroup is the set of all its group rotations.')
add('D5','equivalence notation',passage('We use the equivalence notation','We will restrict attention to projected models'),[6],
    'Section 2.1 — equivalence notation',{'D1':r'Projected-orbit equivalence requires equality in law under Haar-uniform $g\sim\Lambda$.','D4':r'The relation compares projected sets $\Pi(\mathcal{O}_{\theta})$ as well as their induced laws.'},
    role='predicate',symbols=[r'\Pi(\mathcal{O}_\theta)'],
    shape='Equality of projected orbit sets together with equality of the projected Haar-induced probability laws; set equality alone is insufficient.')
add('D6','generic',env('definition',r'\label{def:generic}'),[7], 'Definition 2.3',role='predicate',phrases=['generic'],
    shape='A subset of real d-space is generic when its complement lies in the zero set of a nonzero analytic map to a finite-dimensional real space.')
add('D7','finite number of orbits',passage('We will restrict attention to projected models', 'An equivalent algebraic characterization'),[6],
    'Section 2.1 — condition (2.4)',{'D4':r'Condition (2.4) counts distinct signal orbits.','D5':r'The counted orbits must satisfy the projected equivalence relation $\Pi(\mathcal{O}_{\theta})\equiv\Pi(\mathcal{O}_{\theta_*})$.','D6':r'The finiteness condition is required for generic true signals.'},
    kind='condition',role='predicate',phrases=['finite number of orbits'],
    shape='For generic true signals, only finitely many distinct orbits have the same projected orbit set and Haar-induced law.')
density=passage('In both models, we denote the negative sample log-likelihood', 'The maximum likelihood estimator')
population=passage('We denote the negative \\emph{population} log-likelihood function', 'This population')
add('D8','log-likelihood function',density+'\n\n'+population,[5,6], 'Section 2.1 — likelihood, equations (2.3) and (2.5)',
    {'D2':r'The unprojected likelihood uses the Gaussian mixture density with $\Pi=\mathrm{Id}$ and projected dimension equal to $d$.','D3':r'The density (2.3) integrates the projected Gaussian observation model, and (2.5) takes expectation under its true law.'},
    symbols=[r'R(\theta)',r'p_\theta(y)'],
    shape='Population negative log-likelihood is minus the true-model expectation of the log Gaussian mixture density, with identity projection covering the unprojected case.')
add('D9','Invariant polynomials',passage(r'Let $\cR^\G$ be the (real) algebra',r'Examples of polynomials in $\cR_{\leq k}^\G$'),[6],
    'Section 2.2 — invariant polynomials',symbols=[r'\mathcal{R}_{\leq k}^\mathsf{G}',r'\mathcal{R}^\mathsf{G}'],context='Invariant polynomials and the high-noise expansion',
    shape='Real invariant polynomial algebra and the subalgebra generated by invariants of total degree at most k; elements of this subalgebra can have degree greater than k.')
add('D10','symmetric moment tensors',passage(r'symmetric moment tensors',r'Conversely, any $\G$-invariant polynomial',SOURCE[SOURCE.index('Examples of polynomials in'):]),[6],
    'Section 2.2 — symmetric moment tensors, equation (2.6)',{'D1':r'The integral defining $T_k(\theta)$ is taken against the Haar probability measure $\Lambda$.'},
    symbols=[r'T_k(\theta)'],shape='Order-k tensor obtained by Haar averaging the kth tensor power of the rotated signal, with the source tensor-space Euclidean norm convention.')
add('D11','projected moment tensors',passage('For the projected model with projection',r'We then define'),[6],
    'Section 2.2 — projected moment tensors',{'D1':r'The projected moment integral uses $\Lambda$.','D3':r'The tensor integrates powers of the projected mixture centers $\Pi g\theta$ from (2.2).'},
    symbols=[r'{\widetilde{T}}_k(\theta)'],shape='Haar average of kth tensor powers of the projected rotated signal, taking values in the projected tensor space.')
add('D12','subalgebra',passage(r'We then define',r'Since each entry of $\tT_k$'),[6],
    'Section 2.2 — subalgebra generated by projected moments',{'D9':r'The projected-moment subalgebra is defined inside $\mathcal{R}^{\mathsf{G}}$.','D11':r'Its generators are the entries of projected tensors of orders one through k.'},
    symbols=[r'\mathcal{\widetilde{R}}_{\leq k}^\mathsf{G}'],
    shape='Subalgebra generated by projected moment tensor entries up to order k; not identified with the unprojected degree-generated algebra.')
leading=passage('Our arguments will only require the forms',r'\subsection{Fisher information')
for lid,label,dep,heading in [('D13a','eq:sk','D10','Theorem 2.2(a) — equation (2.8)'),('D13b','eq:tildesk','D11','Theorem 2.2(b) — equation (2.11)')]:
    add(lid,'"leading" terms',equation(label),[7],heading,{dep:r'The leading term is the squared Euclidean tensor discrepancy between the order-k moment at the candidate and true signal, divided by $2(k!)$.'},
        group='D13',context=leading,kind='theorem_excerpt',symbols=[r's_k(\theta)' if lid.endswith('a') else r'\tilde{s}_k(\theta)'],
        shape='Separate unprojected and projected leading terms, each 1/(2 k!) times the squared moment-tensor discrepancy; projection is retained in its own member.')
add('D15','Fisher information matrix',passage('Consider the Fisher information matrix','In this section, we characterize'),[7],
    'Section 2.3 — Fisher information matrix',{'D8':r'The Fisher information is the Hessian of the population negative log-likelihood evaluated at the true parameter.'},symbols=[r'I(\theta_*)'],
    shape='The real symmetric matrix given by the Hessian of the population negative log-likelihood at the true signal.')
add('D16','transcendence degree',env('definition','Polynomials $p_1'),[7], 'Definition 2.4',
    {'D9':r'Definition 2.4 defines transcendence degree for subsets of the invariant polynomial algebra.'},
    phrases=['transcendence degree','algebraically independent'],
    shape='Algebraic independence means absence of any nonzero polynomial relation; transcendence degree is the maximum cardinality of an independent subset, with maximal such subsets called bases.')
prop=env('proposition',r'\label{prop:Kdef}')
kctx=passage('More informally, the order of moments needed', 'We defer proofs of Propositions')
for lid,raw,deps in [
 ('D17a',passage('There is a smallest integer',r'\item $\Pi$',prop),{'D9':'The order K is the first degree threshold whose generated invariant subalgebra has full transcendence degree.','D16':'Proposition 2.6(a) compares the two transcendence degrees.'}),
 ('D17b',passage(r'$\Pi$ satisfies',r'\end{enumerate}',prop),{'D12':'The order in Proposition 2.6(b) is defined using projected-moment subalgebras.','D16':'Its defining equality compares transcendence degrees.','D7':'Proposition 2.6(b) explicitly conditions finite projected order on (2.4).'})]:
    raw=passage('For any compact subgroup',r'\begin{enumerate}',prop)+'\n'+raw
    add(lid,'order of moments',raw,[8], 'Proposition 2.6('+('a' if lid.endswith('a') else 'b')+') — moment order',deps,
        group='D17',context=kctx,kind='source_passage',role='local_object',symbols=['K' if lid.endswith('a') else r'{\widetilde{K}}'],
        shape='Separate smallest finite orders K and projected K-tilde at which transcendence degree reaches the full invariant algebra; projected existence requires (2.4).')
add('D18','maximum orbit dimension',r'\[d_0=\max_{\theta \in \R^d} \dim(\orbit_\theta)\]',[8],
    'Section 2.3 — maximum orbit dimension in equation (2.12)',{'D4':'The value d0 is the maximum manifold dimension among signal orbits.'},
    context=passage('Here, the maximum orbit dimension',r'\end{proposition}'),symbols=['d_0'],
    shape='Maximum of orbit submanifold dimensions over real signals, denoted d0; a geometric dimension, not an increment of transcendence degree.')
for lid,label,alg,k in [('D19a','eq:dk','D9','D17a'),('D19b','eq:tdk','D12','D17b')]:
    add(lid,'total dimension',equation(label),[8], 'Section 2.3 — equation ('+REFS[label]+')',
        {alg:'The dimension increments subtract consecutive transcendence degrees of the corresponding subalgebras.',k:'The sequence stops at the corresponding smallest full-transcendence moment order.','D18':'The zeroth component is the maximum orbit dimension.','D16':'Each positive-index component is a difference of transcendence degrees.'},
        group='D19',context=passage('to decompose the total dimension of', 'The following result expresses'),
        symbols=['d_k' if lid.endswith('a') else r'\tilde{d}_k'],
        shape='Separate unprojected and projected dimension decompositions: zeroth component is orbit dimension, later components are increments of transcendence degree.')
add('D20','globally benign',env('definition','twice-continuously differentiable'),[10], 'Definition 2.10',
    role='predicate',phrases=['globally benign'],
    shape='For a C2 function on a smooth manifold, every critical point is a global minimizer or has a strictly negative Hessian direction in a local chart.')
vctx=passage('To ease notation, let us collect',r'\begin{align}')
for lid,begin,label,dep in [('D21a',r'M_k(\theta)&=', 'eq:Mk','D10'),('D21b',r'\tM_k(\theta)&=','eq:tMk','D11')]:
    add(lid,'vectorized moment tensors',display_row(begin,label),[10], 'Section 2.4 — equation ('+REFS[label]+')',
        {dep:'The vector concatenates all entries of the corresponding moment tensors from order one through k.'},group='D21',context=vctx,
        symbols=[r'M_k(\theta)' if lid.endswith('a') else r'{\widetilde{M}}_k(\theta)'],
        shape='Separate concatenations of all unprojected or projected tensor entries through order k, in their stated Euclidean dimensions.')
mctx=passage(r'Fixing the true signal $\theta_*',r'\begin{align}')
for lid,begin,label,dep in [('D22a',r'\cV_k(\theta_*)&=','eq:Vk','D21a'),('D22b',r'\tcV_k(\theta_*)&=','eq:tVk','D21b')]:
    add(lid,'moment varieties',display_row(begin,label),[10], 'Section 2.4 — equation ('+REFS[label]+')',
        {dep:'The moment variety is the fiber where the concatenated moment vector equals its value at the true signal; order zero is the entire real parameter space.'},
        group='D22',context=mctx,symbols=[r'\mathcal{V}_k(\theta_*)' if lid.endswith('a') else r'\mathcal{\widetilde{V}}_k(\theta_*)'],
        shape='Separate unprojected and projected moment fibers at the true signal, with the explicitly specified order-zero whole-space convention.')
add('D23','non-degenerate up to orbit',env('definition',r'\label{def:nondegenerate}'),[11], 'Definition 2.12',
    {'D22a':'Definition 2.12 restricts the objective and its Hessian to the preceding moment variety.','D13a':'The restricted objective is the order-K leading moment-discrepancy term.','D18':'The allowed Hessian nullity is the maximum orbit dimension d0.','D4':'The critical point must have a locally smooth orbit of dimension d0.'},
    role='predicate',phrases=['non-degenerate up to orbit'],note='Theorem 2.13(b) explicitly prescribes the projected replacements of the moment tensors, varieties and leading terms. No separate projected Definition is invented. K in this local condition indexes the moment problem; the predicate itself does not require the minimal-order equality in Proposition 2.6.',
    shape='At a critical point of the constrained moment objective, its orbit is locally smooth of dimension d0 and the constrained Hessian rank is manifold dimension minus d0.')
add('D24','Continuous multi-reference alignment',passage('To describe the model, let',r'Theorem \ref{thm:MRA} below'),[12],
    'Section 3 — continuous multi-reference alignment',{'D2':'After the real Fourier representation, the source identifies the coefficient observations with the unprojected model (2.1).'},
    kind='source_passage',context='Continuous multi-reference alignment',symbols=[r'd=2L+1',r'\theta^{(0)}'],
    shape='Bandlimited real Fourier model of a periodic function with random circle rotation and independent Gaussian coefficient noise; the exact block-diagonal representation fixes G and d=2L+1.')
add('D25','complex Fourier coefficients',passage('Denote the Fourier coefficients of the true function',r'\begin{theorem}\label{thm:MRA-mom}'),[13],
    'Section 3 — complex Fourier coefficients and Fourier bispectrum',{'D24':'The complex coefficients are formed from the real cosine and sine coordinates of the bandlimited circle model.'},
    symbols=[r'u^{(l)}(\theta)',"r_{l,l',l''}"],phrases=['Fourier bispectrum'],
    shape='Complex circle coefficients with magnitude and phase, plus the explicitly defined triple magnitude products and phase differences; no identification with spherical coefficients.')
add('D26','Spherical registration',passage(r'Let $\sS^2 \subset \R^3$', 'The following result describes the decomposition'),[14],
    'Section 4.1 — spherical registration',kind='source_passage',context='Spherical registration',symbols=[r'd=(L+1)^2'],
    note='The main text names real spherical harmonics and records the finite representation; their explicit forms and rotation matrices are referred to Appendix D.2, which is excluded.',
    shape='Real spherical-harmonic model up to degree L, with surface-area white noise and uniform SO(3) rotations; dimension is (L+1)^2.')
add('D27','complex spherical harmonic coefficients',passage('We write as shorthand',r'We denote'),[14,15],
    'Section 4.1 — complex spherical harmonic coefficients',{'D26':'The complex vectors are unitary transforms of the real coefficients of the spherical registration model.'},
    symbols=[r'u^{(l)}(\theta)'],note='The unitary-transform convention is referenced as (D.11); its appendix formula is not inspected or reconstructed.',
    shape='A vector of 2l+1 complex spherical coefficients at each degree l, related to the real model coefficients by the source-referenced unitary transform.')
add('D28','bispectrum',equation('eq:Bl')+'\n'+passage(r'where $\langle l,m;', 'These quantities express'),[15],
    'Section 4.1 — equation (4.2)',{'D27':'The function B contracts products of the complex spherical coefficients.','D32':'The contraction weights are the Clebsch-Gordan coefficients named below (4.2).'},
    context=passage('The functions\n$B_{l,l',r'\begin{theorem} \label{thm:S2registration-mom}'),
    symbols=["B_{l,l',l''}"],note='Clebsch-Gordan coefficients are named in the main text; their convention is referred to Appendix D.1 and remains unresolved in this main-text-only scan.',
    shape='The source spherical bispectrum contraction sums over m, m-prime, m-double-prime with m-double-prime=m+m-prime and the printed conjugation convention.')
add('D29','Unprojected cryo-EM',passage(r'Consider now a function $f:\R^3', 'This is an unprojected model')+'\n\n'+passage('We parametrize the Fourier domain', 'The following result describes the decomposition',SOURCE[SOURCE.index('We parametrize the Fourier domain'):]),[15,16],
    'Section 4.2 — unprojected cryo-EM',kind='source_passage',context='Unprojected cryo-EM',symbols=[r'\mathcal{I}',r'\hat{j}_{lsm}'],
    note='The main text specifies radial orthogonality, index bounds, and both real and complex representations. Explicit harmonic/real-basis conventions and the unitary transform (D.31) are deferred to appendices and were not inspected.',
    shape='Bandlimited real functions on R3 under uniform SO(3) rotation and white noise, parameterized by radial functions times complex spherical harmonics; d=sum_l (2l+1)S_l.')
add('D30','complex coefficients',passage('Turning to the forms of $s_k(\\theta)$ that define', 'When the original function'),[16,17],
    'Section 4.2 — coefficients and contraction, equations (4.8) and (4.9)',
    {'D29':'The vectors u^(ls) are the complex components of the real cryo-EM basis expansion transformed by V-hat*.','D32':'Equation (4.9) uses the same Clebsch-Gordan coefficients named below (4.2), with radial indices on the complex vectors.'},
    context='complex coefficients',symbols=[r'u^{(ls)}(\theta)'],
    shape='Frequency-pair complex coefficient vectors and their three-frequency Clebsch-Gordan contraction with the exact radial indices and conjugation specified in (4.9).')
add('D31','Projected cryo-EM',passage('We now extend the model of the preceding section', 'Our model setup is similar')+'\n\n'+passage('We again model the Fourier transform', 'The following result verifies'),[17,18],
    'Section 4.3 — projected cryo-EM',{'D29':'The projected model uses the same bandlimited 3D real and complex signal basis and index set (4.5), before integrating along the third coordinate.'},
    kind='source_passage',context='Projected cryo-EM',symbols=[r'\Pi \cdot f',r'\tilde{d}'],
    note='The main text gives the tomographic integral and projected dimension S(2L+1). It further requires radial functions making the projected basis orthonormal. The explicit map (D.57) and basis construction in Appendix D.4 remain uninspected; the unrestricted radial-basis family is not assumed sufficient.',
    shape='Tomographic integral along x3 with Gaussian white noise on R2, retaining the original bandlimited domain and the projected basis/index conventions, including its extra orthonormality requirement.')
add('D32','Clebsch-Gordan',passage(r'where $\langle l,m;', 'The functions\n$B_{l,l'),[15],
    'Section 4.1 — Clebsch-Gordan coefficient convention',kind='source_passage',role='local_object',
    phrases=['Clebsch-Gordan'],note='The main text names this coefficient and refers its definition to Appendix D.1. This record preserves the reference; it does not supply an uninspected definition.',
    shape='Real Clebsch-Gordan coefficients in the paper-specific spherical harmonic convention; the exact convention remains an unresolved appendix reference.')
add('D33','generic signals',passage('We restrict attention to generic signals', 'Different behavior may be observed'),[9],
    'Remark 2.9 — generic signal condition',
    {'D6':'Remark 2.9 specifies the generic set used in the three general likelihood theorems.',
     'D9':'In the unprojected case, the gradient span is formed from the degree-K invariant subalgebra.',
     'D12':'The projected case uses gradients from the projected-moment subalgebra.',
     'D16':'The required span dimension is specified by transcendence degree.',
     'D17a':'The unprojected gradient family is truncated at the order K of Proposition 2.6(a).',
     'D17b':'The projected gradient family is truncated at the order in Proposition 2.6(b).'},
    kind='condition',role='hypothesis',phrases=['generic signals'],
    note='The projected clause prints a full projected algebra with no degree subscript. Section 2.2 explicitly defines only its degree-indexed generated subalgebras. This notation is retained without silently replacing it by the unprojected algebra.',
    shape='The specific generic-gradient-span condition stated for Theorems 2.7, 2.11 and 2.13, with separate unprojected and projected algebra conventions.')

def main():
    for interface in interfaces:
        if len(interface['members']) > 1:
            for member in interface['members']:
                member['relation']='distinct'
                member['variant_note']='This '+('projected' if member['local_id'].endswith('b') else 'unprojected')+' occurrence retains its own source formula and dependency path; grouping the source keywords does not identify the two constructions.'
    # First persist the inspected source passages independently of graph completion.
    (ROOT/'source-passages.json').write_text(json.dumps({'paper_id':PAPER_ID,'members':list(members.values())},indent=2,ensure_ascii=False)+'\n')
    (ROOT/'evidence'/'source-passages-tex.json').write_text(json.dumps(raw_archive,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps({'paper_id':PAPER_ID,'interfaces':interfaces,'local_edge_explanations':edges},indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(members)} source passages in {len(interfaces)} interface groups; theorem connections still require finalization.')

if __name__ == '__main__':
    main()
