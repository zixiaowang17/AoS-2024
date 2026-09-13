"""Build the source-pinned census with explicit theorem-reference scope."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'2':[3,6,7,8,9,13,14,15,16,17,18,19,21,22], '3':[2,3,4,6,7,8,9,13,14,15,16,17,19,21,22,23], '4':[3,6,8,15,16,17,18,24,25,26,27,28], '5':[2,3,4,6,7,8,12,15,16,17,19,23,24,25]}
DIRECT={n:['D'+str(i) for i in ids] for n,ids in DIRECT_NUMS.items()}
REASONS={2:'The target tau is the population average treatment effect defined in Section 1.',3:'The theorem requires Assumption 1, the joint potential-outcome unconfoundedness condition.',4:'The original local rho-cubed formula (20), retained as A10, uses the outcome regression contrast r_1(X)-r_0(X).',6:'Assumption 2 supplies the logistic propensity model and strict almost-sure overlap; its pi also occurs in the source formulas for the referenced variances.',7:'The bias bound uses s, the count of nonzero propensity coefficients.',8:'The correction-error norm explicitly compares a fitted vector with the evaluated oracle function mu_ORA from (4) and (13).',9:'The inherited Section 2/3.1 setup uses independent auxiliary datasets A and B with n_A=n.',12:'Theorem 5 uses the initial fitted function in its foldwise vector tilde-mu(X), explicitly defined on page 14 and retained as A12.',13:'The correction is constructed via the full convex program (14), including its fallback if infeasible; Theorem 3 inherits this setup from Theorem 2.',14:'The estimator is the basic DIPW formula (15); Theorem 3 inherits the same estimator from Theorem 2.',15:'The theorem explicitly requires Assumption 3 on marginal potential-outcome tails and means.',16:'The theorem explicitly requires Assumption 4 on the intercept and centered sub-Gaussian remaining covariates.',17:'The theorem explicitly requires Assumption 5 on log(p)/n and the lower bounds p>=2 and s>=1.',18:'The target bar-tau is the observed-covariate conditional average in (16), not population tau.',21:'The remainder probability uses Omega-complement, with all three conditions in the event definition; Theorem 3 inherits this bound through Theorem 2(i).',22:'Sigma_mu is the weighted correction-error variance term defined on page 10; it appears in the decomposition and normal-approximation bounds.',23:'Sigma in the population decomposition is the square root of the variance (19).',24:'Tau_AVE is the three-fold cyclic average (22), with the estimator construction described in Section 3.2.',25:'The fold events Omega_j are the Section 3.2 versions defined with cyclic data roles; the same source passage specifies the optimized fold vectors and concatenation used in Theorem 4.',26:'Theorem 4 explicitly references interval (24) and covers bar-tau with C-tilde at level alpha/3, using the empirical variance construction (23).',27:'Theorem 4 requires Assumption 6, whose b_n appears in its coverage error.',28:'Theorem 4 requires Assumption 7, the marginal residual-variance lower bound.'}
EDGE_TEXT={
 'D2':{'D1':'The potential-outcome target is defined in the observed-triple setting with Y=Y(T).'},
 'D3':{'D1':'Unconfoundedness concerns the observed covariate and treatment variables and their potential outcomes.'},
 'D4':{'D1':'The regression functions condition each potential outcome on X.'},
 'D6':{'D1':'The propensity is the conditional treatment probability in the observational model.','D5':'Equation (1) uses the standard logistic link psi.'},
 'D7':{'D6':'The sparsity counts nonzero coordinates of the model coefficient gamma.'},
 'D8':{'D4':'Equation (4) combines r_1 and r_0.','D6':'The two weights in (4) use the true propensity pi.'},
 'D9':{'D1':'Auxiliary datasets are iid copies of the observational triples and independent of the main data.'},
 'D10':{'D5':'The fitted propensity uses the same scalar logistic link.','D6':'Gamma-hat estimates the coefficient of the propensity model.','D9':'The coefficient estimate is trained using dataset B.'},
 'D12':{'D8':'The initial function is described as an estimate of mu_ORA.','D9':'The initial fit is constructed using auxiliary B.'},
 'D13':{'D9':'The constraint uses auxiliary A and the main covariate matrix.','D10':'The transformed auxiliary outcome in the constraint is formula (8), retained as A3-A4, with estimated propensity weights.','D12':'The objective and both sides of the constraint use the initial fitted function tilde-mu.'},
 'D14':{'D1':'The average in (15) uses observed Y_i and T_i.','D10':'Its denominators use fitted propensities.','D13':'The subtracted corrections are the solution of (14), including the zero fallback.'},
 'D15':{'D1':'Assumption 3 controls the two potential outcomes in the observational setup.'},
 'D16':{'D1':'Assumption 4 decomposes the observed covariate vector into an intercept and remaining coordinates.'},
 'D17':{'D7':'The lower bound s>=1 refers to the propensity sparsity count.'},
 'D18':{'D1':'Equation (16) averages conditional potential-outcome contrasts over the observed covariates.'},
 'D19':{'D4':'The residuals subtract the conditional regression means r_t(X).'},
 'D21':{'D7':'Part (i) scales coefficient errors by s.','D9':'Part (ii) includes auxiliary A observations and part (iii) conditions on auxiliary B.','D10':'Parts (i)-(ii) involve fitted coefficients and propensity scores.','D12':'Part (iii) bounds conditional moments of the initial fitted function.'},
 'D22':{'D6':'The weight uses true pi_i(1-pi_i).','D8':'The comparison vector evaluates mu_ORA.','D13':'The fitted correction is the optimized vector from (14).'},
 'D23':{'D2':'The influence expression is centered by population tau.','D4':'It includes the contrast r_1(X)-r_0(X).','D6':'Its treatment residuals are divided by true propensity probabilities.','D19':'The two residuals are epsilon(1) and epsilon(0).'},
 'D24':{'D9':'Each fold estimator uses the other two folds in the auxiliary A/B roles.','D14':'The averaged quantities are the three basic DIPW estimates.'},
 'D25':{'D8':'The initial functions and concatenation refer to the evaluated oracle vector.','D13':'Each optimized fold correction is constructed as in (14).','D21':'Each fold event is the same Omega definition instantiated with its cyclic data roles.','D24':'The fold datasets and cyclic roles are those of the cross-fit construction.'},
 'D26':{'D1':'The empirical variance uses observed outcomes and treatment indicators.','D10':'It uses the corresponding fitted propensity denominators.','D18':'The original interval targets bar-tau.','D24':'Its center is tau_AVE and each empirical variance centers by its fold estimate.','D25':'The foldwise corrected observations use components of the concatenated mu-hat.'},
 'D27':{'D7':'The rate condition explicitly restricts propensity sparsity s.'},
 'D28':{'D19':'The marginal variances are those of the residuals epsilon(t).'}}
def direct_reason(n,lid):
    if lid=='D19':return ('Theorem 2 uses the local formulas bar-sigma squared and bar-rho cubed, preserved as A8-A9; expanding them requires the residual definition epsilon_i(t).' if n=='2' else 'The local population rho-cubed formula (20), preserved as A10, uses the two residuals epsilon(t).')
    return REASONS[int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All four main-text Theorems, retaining the source scopes of setup, subpart and construction references.',build_order_policy='Same-paper source dependencies; original unnamed local formulas are saved as auxiliary prerequisites and expanded explicitly into the local graph.')
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
            # Local formula expansions and construction references have source evidence too.
            if 'D19' in path:ev.extend([dict(page=10 if n=='2' else 11,location='Original local moment formula expanded in this connection')])
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=reason,evidence=ev)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors) and all(s in linked for s in selectors),(m['local_id'],[s for s in selectors if s not in linked])
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Census structurally validated; full independent source review remains pending.')
if __name__=='__main__':main()
