"""Derive all five theorem connections from their main-text definitions and hypotheses."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '3.3':{'D1':'The exact process X is explicitly the solution of equation (1).','D3':'The opening hypothesis explicitly assumes (A1), the regularity and one-sided Lipschitz condition on N.','D4':'The opening hypothesis explicitly assumes (A2), the polynomial increment and derivative bounds on N.','D14':'Condition (1) requires the one-step map to be Lp consistent of order q2-1/2, as defined in Definition 3.1.','D15':'Condition (2) requires the numerical approximation to have bounded moments, as defined in Definition 3.2.','D8':'The error is evaluated at grid times t_k for k=1,...,N with step h.'},
 '3.5':{'D1':'The comparison process X is explicitly the solution of equation (1).','D3':'The theorem explicitly assumes (A1), the regularity and one-sided Lipschitz condition.','D4':'The theorem explicitly assumes (A2), the polynomial increment and derivative condition.','D12':'The numerical process is expressly the LT approximation defined by equation (10).','D8':'The conclusion bounds the error at each grid time t_k in terms of the common step size h.'},
 '3.7':{'D1':'The comparison process X is explicitly the solution of equation (1).','D3':'The theorem explicitly assumes (A1), the regularity and one-sided Lipschitz condition.','D4':'The theorem explicitly assumes (A2), the polynomial increment and derivative condition.','D11':'The theorem explicitly adds (A6), the asymptotic inverse-flow assumption.','D13':'The numerical process is expressly the S splitting defined by equation (11).','D8':'The error bound is stated for all grid times t_k, with rate R(h,x_0).'},
 '5.1':{'D1':'The observed process X is explicitly the solution of equation (1).','D2':'The estimator components are the drift parameter and identifiable diffusion covariance, and their true values use the Section 2 parameter convention.','D3':'The reference (A1)-(A6) includes (A1), the regularity and one-sided Lipschitz condition on N.','D4':'The reference (A1)-(A6) includes (A2), the polynomial increment and derivative bounds on N.','D5':'The reference (A1)-(A6) includes (A3), existence of an invariant probability for X.','D6':'The reference (A1)-(A6) includes (A4), invertibility of the covariance on the parameter domain.','D7':'The reference (A1)-(A6) includes (A5), identifiability of the full drift in beta.','D11':'The reference (A1)-(A6) includes (A6), asymptotic existence of the inverse nonlinear flow.','D16':'The estimator is explicitly required to minimize either approximate objective (22) or (23).','D8':'The consistency limits h tending to zero and Nh tending to infinity use the sample grid and observed horizon.'},
 '5.2':{'D1':'The observed process X is explicitly the solution of equation (1).','D2':'The true parameter is explicitly required to lie in Theta; the drift and covariance targets use the Section 2 parameterization.','D3':'The reference (A1)-(A6) includes (A1), the regularity and one-sided Lipschitz condition on N.','D4':'The reference (A1)-(A6) includes (A2), the polynomial increment and derivative bounds on N.','D5':'The reference (A1)-(A6) includes (A3), existence of an invariant probability for X.','D6':'The reference (A1)-(A6) includes (A4), invertibility of the covariance on the parameter domain.','D7':'The reference (A1)-(A6) includes (A5), identifiability of the full drift in beta.','D11':'The reference (A1)-(A6) includes (A6), asymptotic existence of the inverse nonlinear flow.','D16':'The estimator is explicitly required to minimize either approximate objective (22) or (23).','D8':'The three asymptotic restrictions h tending to zero, Nh tending to infinity and Nh squared tending to zero refer to the sample grid.','D17':'The diffusion component is the half-vectorized covariance varsigma and is scaled by square root N.','D18':'The theorem requires C(theta_0) to be positive definite and gives its inverse as the limiting Gaussian covariance.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned published journal PDF, The Annals of Statistics 52(2), 842-867 (2024), DOI 10.1214/24-AOS2371. Separate supplementary article and code are excluded.',
     normalization_policy='Preserve all five original Theorems, A1-A6, numerical consistency and moment definitions, forward splitting flows, approximate objectives and covariance information. Keep all original formulas separate from interpretive notes.',
     semantic_ranking_policy='Count direct statement prerequisites and recursive paper-local definition paths only; exclude proof-only expansions and the simulation comparison methods.',
     build_order_policy='Preserve the SDE and drift decomposition before split flows. Keep asymptotic inverse existence distinct from a globally invertible flow and full objectives distinct from the approximate objectives cited in the estimation Theorems.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']))
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
