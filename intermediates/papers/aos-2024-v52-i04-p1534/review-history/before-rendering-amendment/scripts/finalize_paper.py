"""Attach source-reviewed theorem-to-interface paths and finalize this paper."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
'1':{'D1':'Part (ii) assumes the candidate EIF has finite Bochner L2 norm.','D4':'The opening assumes pathwise differentiability at P.','D6':'The opening assumes the local parameter space dot-H_P is an RKHS.','D8':'Both implications concern existence or identity of the original EIF phi_P.','D9':'The candidate phi-tilde_P is the feature-map construction (5).'},
'2':{'D1':'The opening requires phi_0 in the Bochner L2 space under P0.','D4':'The opening assumes pathwise differentiability at the true law.','D8':'The linear term and Gaussian covariance use the original EIF phi_0.','D11':'The estimator in the regularity and weak-convergence conclusions is the cross-fitted bar-nu_n.','D12':'The opening separately requires the remainder R_n^j and drift D_n^j to be negligible on both folds.','D13':'The theorem explicitly concludes that bar-nu_n is regular under the local-submodel definition.'},
'3':{'D1':'Theorem 2 conditions include Bochner L2 integrability, and this theorem additionally requires a positive norm.','D4':'The referenced conditions of Theorem 2 include pathwise differentiability.','D8':'The inherited conditions and the nondegeneracy assumption concern the original EIF.','D12':'Both fold-specific negligible remainder and drift conditions are inherited from Theorem 2.','D14':'The theorem requires Omega_n and Omega_0 in O and operator-norm convergence.','D15':'Both coverage conclusions concern the quadratic-form confidence set C_n(zeta-hat_n).'},
'4':{'D1':'The inherited true-law integrability and added fitted-EIF convergence are measured in L2(P0;H).','D4':'The conditions of Theorem 2 include pathwise differentiability at P0.','D8':'The added maximum-over-folds condition compares fitted EIFs with phi_0.','D12':'Theorem 2 conditions include negligible drift and remainder on both folds.','D14':'The standardization operators and their norm convergence are stated explicitly.','D16':'The zeta-hat_n whose consistency is asserted is the conditional split-bootstrap quantile defined immediately before the theorem.'},
'5':{'D4':'The opening requires pathwise differentiability but does not require an original EIF.','D17':'The incorporated expansion (25) uses the regularized influence function phi_0^beta_n.','D18':'The rate conclusion concerns the cross-fitted regularized estimator with an untransformed plug-in.','D19':'The added hypothesis and incorporated expansion (25) use the fold-specific spectral bias B_n^(j,beta_n).','D20':'The opening bounds both regularized remainder and drift terms at norm(beta_n)/sqrt(n).'},
'6':{'D2':'The theorem explicitly selects a quadratic mean differentiable submodel with score s for the local alternatives.','D4':'The opening assumes pathwise differentiability, and the nonzero direction condition uses dot-nu_0(s).','D17':'The asymptotic linear representation and Gaussian limit use the regularized influence function phi_0^beta.','D21':'The estimator targets nu^beta(P0), and the local shift is its transformed derivative dot-nu_0^beta(s).','D22':'The assumed asymptotically linear estimator tilde-nu_n^beta is the transformed-parameter estimator from Section 5.2.','D24':'The rejection event uses the preimage confidence set explicitly defined by equation (30).'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Verified registered arXiv:2303.16711v3 PDF, 83 pages; main text and references through page 30 above Appendices only.',
        normalization_policy='Preserve six complete original Theorems 1-6, including Theorem 5 continuation. Save referenced equations (4) and (25) separately; retain source notation and closed-range issues without rewriting statements.',
        semantic_ranking_policy='Resolve dominated submodels, pathwise derivatives and EIFs, cross-fitting and errors, original and transformed-parameter estimators, confidence sets and quantiles. Conditions of Theorem 2 do not import its regularity conclusion. Regularized results do not require an original EIF, and Theorem 6 does not import Theorem 5 rate conditions or a mandatory bootstrap threshold.',
        build_order_policy='Derive all edges and reach from the original local dependency graph; keep the independent theorem inventory unchanged.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                evidence=list(c['evidence'])+([dict(page=6,location='Referenced expansion (4)')] if n=='2' else [dict(page=16,location='Referenced expansion (25)')] if n=='5' else [])
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=evidence))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
            sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])+([dict(page=6,location='Referenced expansion (4)')] if n=='2' else [dict(page=16,location='Referenced expansion (25)')] if n=='5' else [])
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
