"""Source-backed graph interfaces; only statement dependencies, never proof use."""
import json
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]
PID=ROOT.name
SOURCE=(ROOT/'evidence/main-only.tex').read_text()
MACROS=(ROOT/'evidence/macros.tex').read_text()

def passage(start,end,source=SOURCE):
    a=source.index(start)
    return source[a:source.index(end,a)].strip()

def definition(label):
    matches=[m[1] for m in re.finditer(r'\\begin\{mydef\}(.*?)\\end\{mydef\}',SOURCE,re.S) if r'\label{'+label+'}' in m[1]]
    assert len(matches)==1
    # Discard the separately archived heading, not any statement text.
    return matches[0].split(r'\label{'+label+'}',1)[1].strip()

def convert(raw):
    raw=raw.replace(r'\citet[pp.~1442--3]{zhang2008causal}','Zhang (2008a, pp. 1442–3)')
    for key,text in {'richardson2002':'Richardson and Spirtes (2002)','zhang2008causal':'Zhang (2008a)'}.items():
        raw=raw.replace(r'\citet{'+key+'}',text)
    raw=raw.replace(r'\ref{sec:introduction}','1')
    assert r'\cite' not in raw and r'\ref{' not in raw
    raw=re.sub(r'\\label\{[^}]+\}','',raw)
    out=subprocess.run(['pandoc','-f','latex','-t','markdown','--wrap=none'],input=MACROS+'\n\\begin{document}\n'+raw+'\n\\end{document}',text=True,capture_output=True,check=True).stdout.strip()
    assert 'reference-type' not in out
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

add('D1','directed partial mixed graphs',passage('Throughout this paper we only consider',r'A \textbf{directed mixed graph}'),[3],
    'Section 2 — directed partial mixed graphs',role='structure',phrases=['directed partial mixed graphs'],
    shape='Loop-free graph with at most one edge between distinct vertices and the four stated edge types, retaining its edge-type decomposition.')
add('D2','directed mixed graph',passage(r'A \textbf{directed mixed graph}',r'The \textbf{skeleton}'),[3,4],
    'Section 2 — directed mixed graph',{'D1':'A directed mixed graph is the stated partial mixed graph with partially directed and non-directed edges excluded.'},role='predicate',phrases=['directed mixed graph'],
    shape='Restriction of a partial mixed graph to directed and bidirected edges.')
add('D3','directed cycle',passage(r'A directed partial mixed graph $\G$ has a \emph{directed cycle}',r'A \textbf{directed acyclic graph'),[4],
    'Section 2 — directed cycle',{'D1':'The cycle predicate is stated on a directed partial mixed graph.'},role='predicate',phrases=['directed cycle'],
    shape='Distinct vertices that are ancestors of each other; reflexive ancestry and directed paths follow the archived Section 2 conventions.')
add('D4','directed acyclic graph (DAG)',passage(r'A \textbf{directed acyclic graph',r'A directed partial mixed graph $\G$ has an \emph{almost directed cycle}'),[4],
    'Section 2 — directed acyclic graph (DAG)',{'D2':'The underlying directed graph is the directed mixed graph without bidirected edges, as defined in Section 2.','D3':'The DAG condition excludes directed cycles.'},role='predicate',phrases=['directed acyclic graph'],
    shape='A directed graph without directed cycles; the directed-graph restriction is archived in the ambient source conventions.')
add('D5','directed maximal ancestral graph (DMAG)',passage(r'A directed partial mixed graph $\G$ has an \emph{almost directed cycle}',r'Every DAG is a DMAG.'),[4],
    'Section 2 — directed maximal ancestral graph (DMAG)',{'D2':'An ancestral graph is a directed mixed graph.','D3':'An ancestral graph excludes directed cycles as well as the explicitly defined almost directed cycles.'},role='predicate',phrases=['directed maximal ancestral graph'],
    shape='Directed ancestral graph with no inducing path between non-adjacent vertices; inducing paths, colliders and reflexive ancestry retain the Section 2 definitions.')
add('D6','edge marks',passage(r'We denote a directed edge',r'A \textbf{walk}'),[4],
    'Section 2 — edge marks',{'D1':'The endpoint marks encode the four allowed edge types.'},phrases=['edge marks','non-circle marks'],
    shape='Heads, tails and circles at edge endpoints; non-circle marks are exactly heads and tails, with the stated wildcard notation.')
add('D7','time series structure',definition('def:time_structure'),[5],
    'Definition 3.1 (Time series structure)',role='predicate',phrases=['time series structure'],symbols=[r'\Tindex'],
    shape='Vertices factor into a finite nonempty variable-index set and a contiguous integer time interval, possibly unbounded at either end.')
add('D8','time ordered',definition('def:time_order'),[5],
    'Definition 3.2 (Time order)',{'D1':'Time order is defined for a directed partial mixed graph.','D7':'The inequality compares the time coordinates supplied by the time series structure.'},role='predicate',phrases=['time ordered'],
    shape='Every directed edge goes from an earlier or equal time to a later or equal time.')
add('D9','repeating edges',definition('def:repeating_edges'),[6],
    'Definition 3.3 (Repeating edges)',{'D1':'The definition quantifies over all four allowed edge types.','D7':'Translations of endpoints must remain in the time-structured vertex set.'},role='predicate',phrases=['repeating edges'],
    shape='Every edge repeats with its type under every common time shift that keeps both endpoints in the graph.')
add('D10','time series DAG',definition('def:tsDAG'),[6],
    'Definition 3.4 (Time series DAG)',{'D4':'A ts-DAG is required to be a DAG.','D7':'Its time series structure has time index set Z.','D8':'It is time ordered.','D9':'It has repeating edges.'},role='predicate',phrases=['time series DAG','ts-DAG'],
    shape='DAG on a finite variable-index set times all integers, with time order and repeating edges; no finite longest-edge condition is added.')
add('D11','Regular sampling',passage('Throughout the paper we restrict the set',r'The time window length'),[8],
    'Section 3.4 — Regular sampling and Regular subsampling',role='predicate',phrases=['Regular sampling','Regular subsampling'],
    shape='The two explicitly permitted observed-time sets: every time in a finite window, or every n-th time for an integer n at least two. The two alternatives are retained separately in the source list.')
add('D12','marginalization / projection',passage('In most real-world scenarios',r'Below, we generalize'),[7],
    'Section 3.4 — marginalization / projection',{'D4':'The cited projection takes a DAG and an observed vertex subset.','D5':'Its output is a DMAG on the observed subset.'},kind='source_passage',phrases=['marginalization / projection'],symbols=[r'\M_{\Ovar}(\D)'],
    note='This passage states the input, output and preservation properties, but cites the construction externally. The main text does not supply the full MAG latent-projection or m-separation rule.',
    shape='Cited MAG latent projection to observed vertices, preserving their ancestral relationships and converting observable d-separations to m-separations; construction remains an external source prerequisite.')
add('D13','ts-DMAG',definition('def:ts_dmag_implied'),[8],
    'Definition 3.6 (Time series DMAG)',{'D10':'The graph being marginalized is a ts-DAG.','D11':'The observed time set is regularly sampled or regularly subsampled.','D12':'The output is obtained by the cited MAG latent projection with all other vertices latent.'},phrases=['ts-DMAG'],symbols=[r'\M_{\Ovar}(\D)'],
    shape='Project a ts-DAG to a variable-index subset times one of the two permitted finite observed-time sets; every vertex outside that set is latent.')
add('D13p','ts-DMAG',passage('Due to this equivalence we from here on restrict',r'\subsection{Properties of ts-DMAGs}'),[10],
    'Section 4.2 — regularly sampled ts-DMAG notation',{'D13':'The abbreviation M^p(D) denotes the time series DMAG M_O(D).','D11':'From this point the observed time set is the regular-sampling window of length p.'},
    role='local_object',group='D13',relation='specialization',symbols=[r'\Mtaumax(\D)'],context='Properties of ts-DMAGs',
    shape='M^p(D) is the regular-sampling abbreviation of M_O(D); the observed variable subset remains part of the context.')
add('D14','stationarification',definition('def:stationarification'),[11],
    'Definition 4.6 (Stationarification)',{'D1':'Stationarification retains the four edge-type distinctions of a directed partial mixed graph.','D7':'The universal time shifts are restricted to those keeping both endpoints in the time-structured vertex set.'},phrases=['stationarification'],symbols=[r'\stat(\G)'],
    shape='Keep the vertex set and retain exactly the edges whose type occurs at every admissible common time shift; apply also to graphs with circle marks.')
add('D15','stationarified ts-DMAG',passage(r'We thus refer to $\stat(\Mtaumax(\D))$',r'\begin{myexample}'),[12],
    'Section 4.4 — stationarified ts-DMAG',{'D13p':'The input M^p(D) is the regularly sampled ts-DMAG.','D14':'The object M^p_st(D) is defined to be its stationarification.'},phrases=['stationarified ts-DMAG'],symbols=[r'\Mtaumaxstat(\D)'],
    shape='The abbreviation M^p_st(D)=stat(M^p(D)); it need not itself be a ts-DMAG.')
add('D16','canonical ts-DAG',definition('def:canonical_ts-DAG'),[14],
    'Definition 4.13 (Canonical ts-DAG)',{'D2':'The input is a directed mixed graph, not necessarily ancestral or maximal.','D3':'The input is required to be acyclic.','D7':'Its finite time-indexed vertices specify I and the reference window.','D14':'The explicit construction uses only edges of stat(G).'},symbols=[r'\Dc(\G)',r'\mathbf{J}'],phrases=['canonical ts-DAG'],
    shape='The full two-part construction of vertices (I union J) times Z and three classes of directed edges, using stationarified edges and latent indices (i,j,tau); preserve the printed endpoint time shifts.')
add('D17','background knowledge',definition('def:background_knowledge'),[18],
    'Definition 5.1 (Background knowledge, cf. Mooij and Claassen (2020))',{'D5':'A background knowledge is a Boolean function on all DMAGs.'},phrases=['background knowledge'],symbols=[r'\BR(\M)'],
    shape='Boolean function on DMAGs; consistency is value one and inconsistency value zero.')
add('D18','Markov equivalent',passage('Markov equivalent DMAGs by definition',r'They might, however'),[18],
    'Section 5.1 — Markov equivalent DMAGs',{'D5':'Markov equivalence here compares DMAGs through equality of their m-separations.'},role='predicate',phrases=['Markov equivalent'],
    note='The main text characterizes equivalence by the same m-separations but does not reproduce the m-separation path criterion.',
    shape='DMAGs with the same m-separations; the separation criterion is a cited external prerequisite.')
add('D19','DPAG',definition('def:pags_background_knowledge'),[18,19],
    'Definition 5.2 (DPAGs refined by background knowledge)',{'D5':'The graph M and all elements of its equivalence class are DMAGs.','D17':'The restricted class retains exactly DMAGs consistent with the chosen Boolean background knowledge.','D18':'The candidates are drawn from the Markov equivalence class of M.','D1':'A DPAG is a directed partial mixed graph with M’s skeleton.','D6':'Maximal informativeness requires shared non-circle marks and witnesses with opposite head/tail marks at every remaining circle.'},phrases=['DPAG'],symbols=[r'\PAG(\M, \BR)'],
    shape='Preserve all four parts defining DPAG, maximal informativeness relative to a class, P(M,A), and the conventional empty-background case. No existence claim for arbitrary inconsistent background knowledge is added.')
raw=definition('def:time_shift_persistent')
orientation=passage(r'\item[3.]',r'\end{enumerate}',raw).replace(r'\item[3.]','',1).strip()
ancestry=passage(r'\item[4.]',r'\item[5.]',raw).replace(r'\item[4.]','',1).strip()
add('D20','repeating orientations',r'A partial mixed graph $\G = (\V, \E) $ with time series structure has$\ldots$'+'\n\n'+orientation,[10],
    'Definition 4.2, part 3 (Repeating orientations)',{'D1':'The condition compares the allowed edge types.','D7':'The two endpoint pairs differ by a common time shift.'},role='predicate',phrases=['repeating orientations'],
    shape='An existing shifted adjacency must have the same orientation; this does not require shifted adjacencies to exist.')
add('D21','repeating ancestral relationships',r'A DMAG $\M = (\V, \E) $ with time series structure has'+'\n\n'+ancestry,[10],
    'Definition 4.2, part 4 (Repeating ancestral relationships)',{'D5':'The ancestral relation is taken in a DMAG.','D7':'The ancestry implication is repeated under shifts for which both vertices remain in the time-structured vertex set.'},role='predicate',phrases=['repeating ancestral relationships'],
    shape='Ancestry persists under every admissible common time shift; reflexive ancestry follows Section 2.')
add('D22','Specific background knowledges',definition('def:specific_background_knowledges'),[19],
    'Definition 5.4 (Specific background knowledges)',{'D17':'All four cases are Boolean background knowledges in the sense of Definition 5.1.','D13p':'A_D tests whether the graph is M^p(D) for some ts-DAG.','D15':'A_D^stat instead tests whether the graph is M^p_st(D) for some ts-DAG.','D8':'Both A_ta and A_to require time order.','D20':'A_to additionally requires repeating orientations.','D21':'A_ta additionally requires repeating ancestral relationships.'},role='predicate',
    context='Definition 5.4 (Specific background knowledges)',symbols=[r'\BRtsDAG',r'\BRtsDAGstat',r'\BRtora',r'\BRtoro'],
    shape='Four distinct Boolean restrictions: underlying ts-DAG, underlying ts-DAG for stationarifications, time order with repeating ancestry, and time order with repeating orientations.')

def main():
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'evidence/source-passages-tex.json').write_text(json.dumps(archive,indent=2,ensure_ascii=False)+'\n')
    (ROOT/'interface-draft.json').write_text(json.dumps(interfaces,indent=2,ensure_ascii=False)+'\n')
    # Basic source conventions are retained without turning each abbreviation into an API.
    ambient=[
        ('graph and adjacency',passage(r'A \textbf{graph}',r'Throughout this paper'),[3]),
        ('directed graph and skeleton',passage(r'and a \textbf{directed graph}',r'Given directed partial mixed graphs'),[3,4]),
        ('subgraph and induced subgraph',passage('Given directed partial mixed graphs',r'We denote a directed edge'),[4]),
        ('walks, paths, colliders and ancestry',passage(r'A \textbf{walk}',r'A directed partial mixed graph $\G$ has a \emph{directed cycle}'),[4]),
        ('time coordinates and lags',passage(r'We say that a vertex $(i, t)',r'Second, below eq.'),[5])]
    (ROOT/'ambient-conventions.json').write_text(json.dumps(dict(paper_id=PID,passages=[dict(name=n,statement_original=convert(raw),original_tex=raw,evidence=[dict(page=p,location='Section 2 or Definition 3.1 surrounding notation') for p in pages]) for n,raw,pages in ambient]),indent=2,ensure_ascii=False)+'\n')
    print(f'Saved {len(interfaces)} source-backed interfaces and {len(members)} local members.')

if __name__=='__main__':main()
