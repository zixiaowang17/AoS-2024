"""Derive all four theorem connections without importing proof-only requirements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{'D2':'The errors are centered at the node parameters theta of the beta-model (3.1).','D4':'The opening hypothesis restricts (alpha,beta) to M(gamma;C_1), subject to the unresolved printed extra script-I membership.','D5':'The statement explicitly assumes Condition 1, the uniform bound on the dense-model node parameters.','D8':'Each error uses the original triangle-moment estimator theta-hat from (3.8).','D10':'The three normalizations use b_ell, tilde-b_ell or their displayed combination from (3.12)-(3.13).'},
 '2':{'D2':'The bootstrap errors retain the original beta-model parameter theta as their population center.','D4':'The reference to the conditions of Theorem 1 retains M(gamma;C_1); the theorem gives its own vanishing-gamma window.','D5':'Condition 1 is inherited through the explicit reference to the conditions of Theorem 1.','D14':'Part (a) uses the twice-jittered estimator theta-hat-dagger from (4.4), centered at theta.','D16':'Both parts use the population bootstrap variance nu-dagger defined in (4.5).','D11':'Part (b) compares nu-dagger with the original combined population variance nu in (4.1).'},
 '3':{'D2':'The probability statement compares the original fitted parameter vector with the beta-model parameter vector theta.','D4':'The theorem explicitly restricts the original jitter probabilities to M(gamma;C_1).','D5':'The opening sentence expressly assumes Condition 1.','D8':'The vector theta-hat is defined immediately before the theorem as the original estimator from (3.8), evaluated on Z.','D16':'The inline definition of V-dagger is diagonal with the population nu-dagger quantities from (4.5).'},
 '4':{'D4':'The opening condition invokes M(gamma,C_1), resolving to the class defined in Section 3.3 despite the comma in this statement.','D17':'The theorem uses the sparse-model intercept xi, sparse effects, support S and size s, as well as the logarithmic residual parametrization xi-plus and check-theta-plus from Section 6.','D18':'The errors concern the sparse intercept and effect estimates in (6.3).','D19':'The first three error terms use the explicitly defined tilde-O_p convention from the start of page 18.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned arXiv:2112.10151v2; main text is pages 1-18 and the portion of page 19 before the Appendix heading. Preserve all four printed Theorems. No appendix or supplement body was used.',
     normalization_policy='Retain source statements, condition labels, distinct original and bootstrap populations and all sparse-model restrictions. Keyword grouping indexes original component passages without claiming their equivalence.',
     semantic_ranking_policy='Rank direct statement uses and derive recursive same-paper reach; proof expansions, later algorithms and applications do not create dependencies.',
     build_order_policy='Preserve local dependencies within keyword groups. Dense parameter bounds remain separate from the sparse model; population variance and empirical bootstrap estimation remain distinct.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lids=[m['local_id'] for m in x['members'] if m['local_id'] in DIRECT[n]]
            if lids:
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+x['interface_id'].split('/')[-1],paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=' '.join(DIRECT[n][lid] for lid in lids),evidence=c['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
            sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])
            for lid in path:
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                for ctx in members[lid].get('application_context',[]):
                    evidence.extend(e for e in ctx['evidence'] if e not in evidence)
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
    print('Finalized and independently validated; final source audit remains.')


if __name__ == "__main__":
    main()
