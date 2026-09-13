"""Attach source-reviewed theorem-to-interface paths and finalize this paper."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT = {'2.3': {'D13': 'The opening Assumption H includes the linear-independence clause H(i).', 'D14': 'The same reference includes the strict order-dimension condition H(ii).', 'D15': 'The same reference includes H(iii), with its fixed compact location set and eventual support disjointness.', 'D16': 'The same reference includes the uniform initial-condition bound H(iv).', 'D17': 'Every entry of Sigma_theta uses the whole-space fractional principal operator.', 'D12': 'Both normalization displays use the rate matrix rho_delta or its componentwise rates.', 'D10': 'The statement asserts convergence of the observed information I_delta and uses it in the first normalization.', 'D11': 'Both CLTs concern the original augmented MLE hat theta_delta.', 'D7': 'The matrix entries and Gaussian covariance use the original point spread function K.', 'D2': 'The entries use formal adjoints A_i-star and a_theta; the second CLT uses the operator orders n_i.'}, '3.1': {'D18': 'The formula involves the general negative self-adjoint A and its Hilbert-space domain from the Section 3 setup.', 'D19': 'The first sentence explicitly identifies the stationary process X in (3.1).', 'D20': 'H_X and its norm are the RKHS of the Gaussian law, in the source covariance/RKHS convention.'}, '3.2': {'D18': 'The kernels are in D(A), the Gram matrix G_A uses A, and the pairings use the general Hilbert space.', 'D19': 'The statement explicitly uses X in (3.1).', 'D20': 'The target is the RKHS and its norm for the finite observed Gaussian process.', 'D21': 'The components defining X_K are the generalized pairings defined immediately before this theorem.'}, '4.1': {'D22': 'The opening Assumption L requires the stationary SPDE law P_theta.', 'D23': 'The same reference includes the iterated-Laplacian kernel requirement L(i).', 'D24': 'The suprema range over the one-dimensional parameter classes Theta_i in L(ii), with their assigned differential orders.', 'D25': 'The same reference includes the strict separation and support conditions in L(iii).', 'D8': 'The last sentence restricts the infimum to estimators of the local observation vector X_delta.'}, '4.3': {'D22': 'Theorem 4.3 inherits the stationary-law assumption and both regimes of Theorem 4.1 through its explicit opening reference.', 'D23': 'Its final clause applies L(i) to each of K, Delta K and (nabla dot b)K, preserving all three instantiations of the original kernel requirement.', 'D24': 'The inherited local suprema and rates use the same Theta_i and orders from L(ii); b also specifies the added transport channel.', 'D25': 'The final clause applies L(iii) to each of the three kernel choices, in addition to its own linear-independence condition.', 'D8': 'The estimator may use the original X_delta channel.', 'D9': 'The estimator may additionally use the Delta and divergence-in-b channels, defined by the same formal-adjoint measurement convention.'}}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Verified registered arXiv:2211.02496v2 PDF, 42 pages; main text ends above Appendix A on page 24. Appendix bodies excluded.',
        normalization_policy='Preserve all five full Theorem statements, including both regimes in Theorem 4.1 and the original inheritance wording in Theorem 4.3. Keep original assumption clauses and source errors unchanged.',
        semantic_ranking_policy='Trace statement dependencies, distinguishing the general self-adjoint RKHS setup from the spatial SPDE. Apply each Assumption L clause to all three kernels in Theorem 4.3; exclude proof-only martingale and Gaussian lower-bound constructions.',
        build_order_policy='Derive the graph from original local definitions, retain source conditions and unresolved meanings, and do not infer library availability.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                evidence=list(c['evidence'])
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=evidence))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
            sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])
            for lid in path:evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
            for a,b in zip(path,path[1:]):sentences.append(edges[a][b])
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=' '.join(sentences),evidence=evidence)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
            linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors),(m['local_id'],'missing source highlight')
            assert all(s in linked for s in selectors),(m['local_id'],'unmatched selector')
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Structural validation passed; independent full source audit remains pending.')
    finalized=json.loads((ROOT/'ranked-interfaces.json').read_text())
    passages=dict(paper_id=PID,members=[m for x in finalized['interfaces'] for m in x['members']])
    (ROOT/'source-passages.json').write_text(json.dumps(passages,indent=2,ensure_ascii=False)+'\n')

if __name__ == "__main__":
    main()
