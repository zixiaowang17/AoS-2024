"""Finalize signed-tree and color-coding statement dependencies without proof-only APIs."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'1':[2,5,8,9],'2':[2,10,11,14]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'The alternative graph-pair law P is the uniform latent-permutation correlated Bernoulli model; Q is the independent graph-pair null with the same marginals.'},
'D4':{'D2':'The centered matrices subtract their common Bernoulli marginal expectations under either observation law.'},
'D5':{'D3':'The tree family contains one isomorphism class of each unrooted tree with exactly K edges.'},
'D6':{'D3':'W_H sums distinct edge-set subgraphs of the complete graph that are isomorphic to H, using the source graph-copy convention.'},
'D8':{'D3':'Each summand carries aut(H), the original number of graph automorphisms.','D4':'The weighted counts are evaluated on Abar and Bbar, the entrywise centered matrices, not on uncentered counts minus their means.','D5':'The outer sum ranges over every unlabeled unrooted tree with K edges.','D6':'The two factors W_H are sums of edge-weight products over copies of the same tree class in the two graphs.','D7':'Each term uses beta=(rho/[q(1−q)])^K*(n−K−1)!/n!, retaining its possible sign.'},
'D9':{'D5':'Otter’s alpha is defined by the exponential growth of the full family T of unrooted unlabeled K-edge trees.'},
'D10':{'D9':'Condition(7) explicitly compares rho² to Otter’s alpha and keeps the strict inequality, in addition to its sparsity and tree-size bounds.'},
'D11':{'D2':'The threshold uses expectation under the alternative graph-pair law P.','D5':'Its explicit value includes the cardinality of the full K-edge tree family T.','D8':'Tau is C times the alternative expectation of the exact signed-tree statistic f_T, not a data estimate or the randomized statistic itself.'},
'D13':{'D3':'The colorful count ranges over edge-set copies S isomorphic to H and multiplies their weighted edges.','D12':'It retains only copies whose vertex set has all distinct colors, using chi_mu from the independent uniform vertex coloring.'},
'D14':{'D3':'The approximate outer sum retains the original automorphism weight aut(H).','D4':'Its colorful weighted counts use the two centered adjacency matrices Abar and Bbar.','D5':'The approximation sums over the same complete set T of unlabeled K-edge trees.','D7':'The normalized approximation multiplies Y_T by beta/r² using the original signed scaling beta.','D12':'It uses two independent coloring arrays with t=ceil(1/r), where r=(K+1)!/(K+1)^(K+1).','D13':'For each tree class it multiplies the two separate sample means of the colorful weighted counts X_H.'}}
def direct_reason(n,lid):
    reasons={
'1':{'D2':'Theorem1 displays testing errors under Q and P, the independent and latent-permutation correlated graph-pair laws defined in Section1.1.','D5':'Its explicit threshold C*rho^(2K)*|T| uses the complete family T of unlabeled trees with K edges, not rooted trees or a selected subfamily.','D8':'Theorem1 tests the exact f_T(A,B) in(3), whose signed-tree summands multiply automorphism-weighted counts in centered edge matrices.','D9':'The hypothesis rho²>alpha explicitly uses Otter’s constant, defined by lim_K |T|^(1/K)=1/alpha in(6).'},
'2':{'D2':'Theorem2 displays the same Q/P error probabilities for a randomized statistic. P and Q originate as graph-pair laws; independent colorings extend those laws implicitly as specified in Section4.','D10':'Theorem2 explicitly assumes(7), the sparsity, strict Otter-threshold and diverging tree-size conditions printed within Theorem1.','D11':'Theorem2 refers to(8) and retains its tau, defined as C*E_P[f_T]=C*rho^(2K)*|T| for any fixed0<C<1.','D14':'Theorem2 uses tilde-f_T, the main-text color-coding approximation(31)–(32), and asserts an n^(2+o(1)) computation. Its formula uses beta/r² times a product of two independent coloring averages.'}}
    return reasons[n][lid]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Both complete main-text Theorems retained. Preserve exact source definitions and internal references without importing the computational-hardness discussion.',build_order_policy='Separate graph observation laws, signed weighted subgraph counts, the exact statistic and randomized color-coding construction. Theorem2 inherits only the referenced condition and threshold; approximation/runtime proof propositions do not become assumptions.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGE_TEXT.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=DIRECT[n]
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                ev=copy.deepcopy(c['evidence'])+copy.deepcopy(members[lid]['evidence'])
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=direct_reason(n,lid),evidence=ev))
    edges=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=edges[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for rel in x['related_theorems']:
            cid=rel['claim_id'];n=cid.split('/T')[-1];path=rel['via_local_ids']
            reason=' '.join([direct_reason(n,path[0])]+[EDGE_TEXT[a][b] for a,b in zip(path,path[1:])])
            ev=copy.deepcopy(claims[cid]['evidence'])
            for lid in path:ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=reason,evidence=ev)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors) and all(s in linked for s in selectors),(m['local_id'],[s for s in selectors if s not in linked])
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Census structurally validated; independent source review remains pending.')
if __name__=='__main__':main()
