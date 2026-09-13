"""Derive same-paper dependencies without importing another estimator's assumptions."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{'D3':'The equality identifies the true first-time conditional mean mu_a using working nu_a-star and rho_a-star; either of the two later-stage functions must equal its true counterpart.','D5':'Assumption 1 is explicitly required for the conditional identification.'},
 '2':{'D3':'The model-correctness alternatives compare first- and second-time working functions to their true conditional functions.','D9':'The sparsities s_gamma_a and s_delta_a and propensity correctness conditions refer to the logistic working projections.','D10':'The sparsity s_alpha_a and nu_a-star refer to the second-time linear projection.','D12':'The S-DRL first-time model and s_beta_a use the projection of YDR in (2.9).','D13':'The printed s2-prime definition contains the indicator mu_a,NR-star != mu_a, despite the S-DRL theorem heading. This literal source reference is retained and flagged.','D5':'The theorem explicitly includes Assumption 1 among Assumptions 1-4.','D23':'Assumption 2 supplies the normalized sub-Gaussian residual hypothesis.','D24':'Assumption 3 supplies the covariate tail and Gram-matrix conditions.','D25':'Assumption 4 bounds the working propensities under misspecification.','D19':'The estimator theta-hat is explicitly defined by Algorithm 1.','D22':'The displayed rate is scaled by sigma defined in (3.1).','D2':'The estimation error is centered at the true dynamic treatment effect theta.'},
 '3':{'D3':'Correct specification equates all four working nuisance functions with their true counterparts.','D9':'The product-sparsity conditions use both population logistic coefficient supports.','D10':'The second-time outcome sparsity is the support size of alpha_a-star.','D12':'The first-time outcome sparsity is the support size of the DR projection beta_a-star.','D5':'Assumption 1 is explicitly required.','D23':'Assumption 2 is explicitly required through Assumptions 1-3.','D24':'Assumption 3 is explicitly required through Assumptions 1-3.','D19':'Both theta-hat and the variance estimate in (2.8) are outputs of Algorithm 1.','D22':'The first normalization explicitly uses sigma squared in (3.1).','D2':'Both normalized errors are centered at the true DTE.'},
 '4':{'D3':'The correctness alternatives compare the working nuisance functions to the true conditional functions.','D9':'The rate uses the logistic projection support sizes s_gamma_a and s_delta_a.','D10':'The second-time outcome support size is s_alpha_a.','D13':'Both the first-time correctness condition and s_beta_a use the nested model, as expressly specified before the theorem in Section 3.2.','D5':'Assumption 1 is included among the required Assumptions 1-4.','D23NR':'Theorem 4 explicitly applies Assumption 2 with the nested first-time model and coefficient replacing the DR projection.','D24':'Assumption 3 is included among the required assumptions.','D25':'Assumption 4 is included for the working propensity bounds.','D20':'The rate concerns theta-hat_DTL from Algorithm 2 and (2.13).','D22NR':'The rate scale sigma uses (3.1) under the theorem\'s explicit nested-model substitution.','D2':'The target theta is the true DTE.'},
 '5':{'D3':'All four nuisance models, with the nested first-time model, must be correctly specified.','D9':'The three product-rate conditions use both propensity coefficient support sizes.','D10':'The product terms use the second-time slope support size s_alpha_a.','D13':'The first-time target and sparsity belong to the nested working model.','D5':'Assumption 1 is explicitly required.','D23NR':'Assumption 2 is applied with the explicit replacement by mu_a,NR-star and beta_a,NR-star.','D24':'Assumption 3 is explicitly required.','D20':'The estimator and fitted variance in (2.13) are the outputs of Algorithm 2.','D22NR':'The population normalization refers to (3.1), with the stated nested-model replacement.','D2':'The normal limits are for errors about the true DTE.'},
 '6':{'D3':'The paired correctness alternatives and extra squared first-time misspecification bound refer to arbitrary working functions in Section 3.3.','D5':'Assumption 1 is explicitly required.','D25':'Assumption 4 imposes overlap on the arbitrary working propensity functions.','D30':'Assumption 5 supplies the four rates a_N,b_N,c_N,d_N and the required moment/estimated-overlap conditions.','D26':'The consistency conclusion concerns the general cross-fitted estimator theta-hat_gen in (2.17).','D27':'The scale sigma in the rate and additional misspecification bound is the general score second moment (3.6).','D2':'Theta in the estimation error is the true DTE.'},
 '7':{'D3':'All arbitrary working nuisance functions of Section 3.3 must equal their true counterparts.','D5':'Assumption 1 is explicitly required.','D30':'Assumption 5 defines the four nuisance estimation rates entering the two product conditions.','D26':'Theta-hat_gen and sigma-hat_gen are the general cross-fitted estimator and empirical variance (2.17).','D27':'The population scale is explicitly sigma squared in (3.6).','D2':'Both normal limits concern errors around the true DTE.'},
 '8':{'D31':'Beta-star, beta-hat, the imputed responses and the M-observation regression experiment are defined immediately before the theorem in (4.1).','D6':'The covariate and residual tail bounds use the psi2-Orlicz norm defined in Section 1.3.'},
 '9':{'D3':'The three rate branches compare rho_a-star and nu_a-star to their true conditional functions.','D5':'Assumption 1 is explicitly required.','D23':'Assumption 2 is explicitly required through Assumptions 1-4.','D24':'Assumption 3 is explicitly required through Assumptions 1-4.','D25':'Assumption 4 is explicitly required through Assumptions 1-4.','D9':'The sparsity s_delta_a refers to the second-time propensity projection.','D10':'Alpha_a-star and its support size determine the outcome-projection contribution to each branch.','D12':'The target beta_a-star and mu_a-star are the first-time DR projection (2.9).','D16':'The pre-theorem paragraph identifies beta-hat_a with the averaged DR fit (2.7); its two component fits use (2.10)-(2.11).','D22':'The tuning parameters and rates are scaled by sigma from (3.1).'},
 '10':{'D5':'Assumption 1 is explicitly required.','D23':'Theorem 10 prints Assumptions 1-3 without the nested-model replacement instruction used in Theorems 4-5. The literal Assumption 2 reference is retained; the possible intended substitution is recorded as unresolved.','D24':'Assumption 3 is explicitly required.','D10':'The sparsity s_alpha_a and the copied rate r_n from Theorem 9(c) refer to the second-time linear projection.','D13':'The target beta_a,NR-star and mu_a,NR-star are the nested working model (2.14).','D17':'The estimated slope and conditional mean use the nested imputed Lasso (2.15), identified in the preceding paragraph.','D22':'The statement uses the scale sigma, with no explicit redefinition of (3.1) in this theorem; the source ambiguity is recorded.'},
 '11':{'D34':'The multi-stage representation explicitly assumes Assumption 6.','D33':'The conditional mean and working functions indexed by stages r are defined in (5.1)-(5.2), including the terminal and stage-zero conventions.','D32':'W_T and the barred histories in the conditional expectation are the Section 5 multi-stage observations.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT = ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,source_policy='Pinned arXiv:2110.04924v4, main pages 1-25. All eleven printed main-text Theorems retained; embedded supplementary pages 26-85 excluded.',normalization_policy='Preserve original wording, equations and source discrepancies. Separate interpretation, symbol resolution and source issues from statement_original.',semantic_ranking_policy='Count direct theorem demand separately from recursive same-paper reach. A definition does not acquire the hypotheses of its consistency theorem.',build_order_policy='Derive an acyclic graph of local source dependencies. Keep parametric, nested, general DR, generic imputed-regression and multi-stage scopes separate; explicit model substitutions get distinct local application records.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for c in data['claims']:
     n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
     for x in data['interfaces']:
      lid=x['members'][0]['local_id']
      if lid in DIRECT[n]:x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
     for r in x['related_theorems']:
      cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1];sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])
      for lid in path:
       evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
       for ctx in members[lid].get('application_context',[]):evidence.extend(e for e in ctx['evidence'] if e not in evidence)
      for a,b in zip(path,path[1:]):sentences.append(edges[a][b])
      x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=' '.join(sentences),evidence=evidence)
     for m in x['members']:
      own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems']);selectors=m['highlight_symbols']+m['highlight_phrases']
      assert any(s in own for s in selectors),(m['local_id'],'missing source highlight')
      assert all(s in linked for s in selectors),(m['local_id'],'unmatched selector')
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Finalized and independently validated; final source audit remains.')


if __name__ == '__main__':
    main()
