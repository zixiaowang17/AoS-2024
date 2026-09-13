# -*- coding: utf-8 -*-
"""Finalize the source-pinned two-Theorem census; do not certify it by rebuilding."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
'1':{
'D3':'The theorem inherits the iid stationary transition-pair observation model (3), explicitly confirmed in the Discussion; its probability statement is over that data.',
'D12':'Part (a) explicitly assumes kernel boundedness (13); part (b) assumes it in addition to its extra condition.',
'D13':'Only the fast-rate branch explicitly adds the uniform eigenfunction bound (14).',
'D15':'R in both critical inequalities and in (18) is the standing radius constrained by (15).',
'D16':'Part (b) substitutes the Bellman residual noise sigma(theta-star) into the critical inequality and condition (18).',
'D17':'Both parts explicitly use CI and its solutions, with different zeta values; (18) specifically uses the smallest fast-rate solution.',
'D18':'Both conclusions reference (17), whose full error bound and tail probability are stated immediately before the theorem.'},
'2':{
'D1':'Both parts assert the existence of a family of discounted Markov reward processes.',
'D3':'The minimax experiment uses n iid stationary transition pairs, as specified in Section 3.4 and the full specification in Section 4.2.1.',
'D19':'The kappa in (33a)-(33b) is fixed at 2 by the standing lower-family condition (29a), which also supplies the spectral trace bound.',
'D21':'Both parts require a (bar-R,bar-sigma)-valid family, explicitly defined by (29a)-(29b).',
'D22':'Delta_n in both bounds is the lower critical radius (30), using the prescribed sequence clarified on page 22.',
'D23':'The additional eigengap condition in part (b) uses d_n, the statistical dimension defined just before (31).',
'D24':'Adjacent main-text prose explicitly says Theorem 2 also requires regular-kernel condition (31).',
'D25':'Both conclusions assert the named LB predicate, whose infimum, supremum and probability event are defined before the theorem.',
'D26':'Part (a) explicitly selects Regime A (32a).',
'D27':'Part (b) explicitly selects Regime B (32b); its reversed printed pair order remains a recorded source convention.',
'D28':'The section titled Full specification of the minimax lower bound clarifies the stationary experiment and L2 norm in this theorem, separating mu(P) from construction Lebesgue measure.',
'D29':'The same full specification supplies family M_A in (41a) for Regime A, with fixed RKHS/reward and exact eigenvalues; it is not the finite proof packing.',
'D30':'The full specification supplies family M_B in (41b) for Regime B, retaining its value-norm cap and j>=2 eigenvalue envelope.'}}
EDGES={
'D2':{'D1':'The true discounted value is defined from the reward, discount and Markov transition kernel of the MRP.'},
'D3':{'D1':'The observation model uses the transition kernel and a stationary distribution of that MRP.'},
'D5':{'D1':'The Bellman operator in (6) uses r, gamma and conditional transitions.','D4':'The fixed point is projected by the metric projection Pi from (5).'},
'D7':{'D3':'The operator expectations use the stationary marginal and stationary transition-pair law.','D6':'Both operators are formed from the RKHS evaluation representers Phi_X.'},
'D8':{'D5':'The population kernel LSTD target is the projected fixed point (6).','D6':'The approximating class is the RKHS H, whose kernel and norm are defined in Section 2.2.'},
'D9':{'D3':'The two sums are over the iid observed transition pairs.','D6':'Their tensor factors are the evaluation representers Phi_x.'},
'D10':{'D9':'The estimator equation uses the empirical covariance and cross-covariance operators.','D6':'The equation is solved on the RKHS, with its identity operator.','D1':'Its right side uses the given reward r and discount gamma.'},
'D11':{'D6':'The decomposition is of the RKHS kernel K.','D3':'The eigenfunctions are orthonormal under the stationary measure mu chosen in the observation model.'},
'D12':{'D6':'Condition (13) bounds the diagonal of the reproducing kernel K.'},
'D13':{'D11':'Condition (14) bounds the sup norms of the Mercer eigenfunctions phi_j.'},
'D14':{'D1':'The effective horizon is computed from the MRP discount gamma.'},
'D15':{'D8':'The radius controls the projected population target theta-star.','D6':'Its first term is the RKHS norm of theta-star minus r.','D12':'Its second term uses the kernel diagonal bound b from (13).'},
'D16':{'D8':'The Bellman residual is evaluated at the population projected target theta-star.','D3':'The expectation is over one stationary transition pair (X,X-prime).','D1':'The residual uses the MRP reward r and discount gamma.'},
'D17':{'D11':'The upper critical complexity is the sum of truncated instance kernel eigenvalues.','D15':'Its slope uses the upper-theorem radius R constrained by (15).','D14':'Its slope uses the effective horizon H(gamma).'},
'D18':{'D10':'The error in (17) uses the regularized kernel LSTD estimate theta-hat.','D8':'The comparison target in (17) is the population projected theta-star.','D15':'Its magnitude uses the source radius R.','D12':'The probability exponent uses the kernel bound b.','D3':'The event probability is with respect to the iid stationary transition-pair dataset.'},
'D19':{'D11':'Condition (29a) concerns the lower-family kernel eigenpairs, with instance versus prescribed spectra clarified in Section 4.2.1.','D13':'Its introductory sentence explicitly invokes the eigenfunction bound (14) with kappa=2.'},
'D20':{'D8':'The radius cap uses theta-star; lower-family realizability equates that target with the true value in its stated scope.','D6':'The first cap uses the RKHS norm of theta-star minus r.','D16':'The second cap bounds the Bellman residual sigma(theta-star) from (16).'},
'D21':{'D1':'The valid objects are families of MRPs.','D19':'Validity explicitly requires conditions (29a).','D20':'Validity also explicitly requires the two bounds (29b).'},
'D23':{'D22':'The threshold in the maximum-index definition is the lower critical radius delta_n squared.'},
'D24':{'D22':'The regularity inequality uses the lower critical radius and its prescribed parameters.','D23':'It lower bounds a multiple of the statistical dimension d_n.'},
'D25':{'D3':'The instance probability in LB is the iid transition-pair data law.','D21':'The supremum ranges over the given valid family of MRPs.','D22':'The error-event threshold uses the lower critical radius delta_n.'},
'D26':{'D14':'Regime A explicitly describes scaling with the effective horizon 1/(1-gamma).'},
'D27':{'D14':'Regime B also describes its radius/noise scaling relative to the effective horizon.'},
'D28':{'D1':'The full specification fixes reward and discount and varies the MRP transition kernel.','D3':'It identifies the stationary starting distribution of the observed transition pairs.','D6':'The RKHS and evaluation representers are fixed within each regime-specific family.','D7':'It explicitly defines the instance covariance operator under mu(P), using the earlier population operator convention.'},
'D29':{'D1':'M_A contains MRPs with the fixed reward r_A and discount gamma.','D2':'Its realizability restriction concerns the true value function, denoted theta-star in this lower-bound section.','D6':'It requires the true value to lie in H_A.','D20':'Condition (i) explicitly invokes inequalities (29b).','D28':'Its instance eigenpairs and stationary norms use the immediately preceding full-specification convention.'},
'D30':{'D1':'M_B contains MRPs with fixed r_B and gamma.','D2':'The value-norm bound and realizability concern the true value in this lower-bound family.','D6':'The true value must lie in H_B.','D20':'Condition (ii) explicitly invokes (29b).','D28':'Its mu(P)-norm and instance eigenpair constraints use the full-specification convention.'}}

def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Both complete main-text Theorems; preserve their original rate and regime branches and all referenced bounds.',build_order_policy='Source-backed same-paper paths; distinguish projected and true targets, upper and lower critical radii, and prescribed and instance spectra.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGES.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            local=[m for m in x['members'] if m['local_id'] in DIRECT[n]]
            if local:
                reason=' '.join(DIRECT[n][m['local_id']] for m in local)
                ev=copy.deepcopy(c['evidence'])
                for m in local:ev.extend(e for e in m['evidence'] if e not in ev)
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+x['interface_id'].split('/')[-1],paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=reason,evidence=ev))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for rel in x['related_theorems']:
            cid=rel['claim_id'];n=cid.split('/T')[-1];path=rel['via_local_ids']
            ex=' '.join([DIRECT[n][path[0]]]+[EDGES[a][b] for a,b in zip(path,path[1:])])
            ev=copy.deepcopy(claims[cid]['evidence'])
            for lid in path:ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=ex,evidence=ev)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
            linked=own+' '+' '.join(claims[t['claim_id']]['statement_original'] for t in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors) and all(s in linked for s in selectors),m['local_id']
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    check=json.loads((ROOT/'ranked-interfaces.json').read_text())
    assert [{k:v for k,v in c.items() if k!='depends_on'} for c in check['claims']]==inv['claims']
    print('Census structurally validated; full independent source review remains pending.')
if __name__=='__main__':main()
