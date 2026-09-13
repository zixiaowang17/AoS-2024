"""Attach source-reviewed theorem-to-interface paths and finalize this paper."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '3.2':{'D3':'The optimization dimension and membership conclusion explicitly refer to the central class fraktur M.','D4':'The objective and GMDD matrix explicitly use kappa(Y,tilde Y).','D5':'The statement names the GMDD matrix and negative GMDD values, using the original dependence functional.'},
 '3.7':{'D9':'The opening clause explicitly assumes (A1), including its first d+1 gap and penalty restriction.','D8':'The solution f-star_{j,mu_j} is the penalized population minimizer of the successive direction extraction method.','D6':'The displayed scaling uses the ordered lambda-star_j and original direction f-star_j from Theorem 3.2.','D7':'The statement also explicitly identifies the optimal direction with the constrained successive search (7).'},
 '3.8':{'D3':'Every component of the minimizing vector is asserted to belong to the central class.','D10':'The displayed minimization and equivalence claim use the Frobenius-penalty objective L_F.','D6':'The final clause uses the ordered lambda-star values and refers to objective (6) in Theorem 3.2.'},
 '4.2':{'D9':'The opening hypothesis explicitly includes (A1).','D16':'The opening hypothesis explicitly includes (A2).','D20':'The opening hypothesis includes (A4), whose V also appears in the sample restriction and rate.','D8':'The left-hand side uses the population objective L1 and its penalized population minimizer.','D14':'The fitted first direction is the empirical minimizer hat f_{1,mu_1} in (11).','D11':'The approximation infimum explicitly ranges over F_n.'},
 '4.4':{'D9':'The opening hypothesis explicitly includes (A1).','D16':'The opening hypothesis explicitly includes (A2).','D20':'The opening hypothesis explicitly includes (A4); its V enters both rate displays.','D8':'The risk display uses L1 and its penalized population optimum.','D14':'Both bounds concern the first empirical minimizer hat f_{1,mu_1}.','D11':'The approximation infimum explicitly ranges over F_n.','D22':'The second display bounds the original sign-invariant squared distance rho^2.'},
 '4.6':{'D9':'The first clause inherits (A1) through its reference to the assumptions of Theorem 4.4.','D16':'The first clause inherits (A2) through the assumptions of Theorem 4.4.','D20':'The first clause inherits (A4) through Theorem 4.4, and its V enters A(n,V,delta).','D8':'The first loss display fixes the previous penalized population directions f-star_[j-1] and compares with f-star_{j,mu_j}.','D25':'The fitted jth direction is the sequential empirical minimizer from (11).','D11':'The displayed approximation term ranges over F_n.','D22':'The probability bound and final expectation both use rho^2 up to sign.','D15':'The statement names R_j and explicitly sums these to the total excess risk R.','D24':'The final expected-error clause explicitly invokes the assumptions of Corollary 4.5, including its ReLU architecture, (A3) and sample-size condition.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Verified registered published PDF, 26 pages, DOI 10.1214/24-AOS2390; external supplementary material excluded.',
        normalization_policy='Preserve six complete original Theorem statements, including all italic consequences in Theorem 4.6. Keep original definitions, assumptions and notation distinct.',
        semantic_ranking_policy='Count direct statement dependencies and same-paper recursive definition paths. Corollary 4.5 conditions apply only to the last clause of Theorem 4.6; first-step estimators do not depend on later-step covariance kernels.',
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
