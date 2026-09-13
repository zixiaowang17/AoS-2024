"""Derive source-specific coverage, coupling and causal theorem dependencies."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'2.2':[1],'2.4':[1,2,3,4,5],'2.8':[1,6,7,8,9,10,11],'3.1':[1,14,15,16,17,20,21,22,23,24,28],'3.2':[1,14,15,16,17,18,20,21,22,28],'3.3':[1,13,21,24,25,26,27]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D3':{'D2':'G2 explicitly bounds the coupled approximating process Z_t from equation9 in G1.'},
'D4':{'D2':'G3 compares the strong-approximation error rate r_t from G1 to the boundary scale.','D3':'The rate must be negligible relative to the minimum of both hatted boundaries in equation10.'},
'D5':{'D3':'G4 approximates each side of the hatted simultaneous boundary from G2 by its corresponding unadorned width.'},
'D7':{'D6':'L1 defines cumulative variance V_t by summing the source conditional variances sigma_i².'},
'D8':{'D6':'L2 centers Y_t at the conditional mean mu_t and conditions on the past observations.','D7':'Both truncation threshold and summability denominator use the cumulative variance V_t to exponentkappa.'},
'D9':{'D6':'L3eta compares the variance estimate with the running average conditional variance, at the stated cumulative-variance-based polynomial rate.'},
'D11':{'D12':'Boundary18 plugs in the starting-time-dependent rho_m defined immediately above it, rather than an arbitrary fixed tuning value.'},
'D13':{'D6':'Corollary2.6 explicitly defines unconditional individual means and variances under independence, with the running mean and average variance of Section2.4.','D7':'Corollary2.6 explicitly imports ConditionL1 and uses its cumulative variance V_i in both moment sums and the mean-growth condition.'},
'D18':{'D16':'The uncentered EIF formula24 contains the two conditional regression functions mu^1,mu^0 and mu^a.','D17':'The EIF weights the outcome residual by a/pi(x)-(1-a)/(1-pi(x)).'},
'D20':{'D18':'The fitted influence function substitutes estimated or known nuisances into the original uncentered EIF formula24.','D19':'The nuisance fit is constructed solely from the training split, whose current size is T prime.'},
'D21':{'D19':'The cross-fit estimate sums the two permanently assigned folds using their counts T andT prime, with denominator t=T+T prime.','D20':'Each fold is evaluated with the influence function fitted only on the opposite fold, using the current fit for every observation in that fold.'},
'D22':{'D19':'The variance definition uses the evaluation-fold and training-fold sample variances with equal one-half weights.','D20':'Its pseudo-outcomes are the opposite-fold fitted influence-function values used in the source formula.'},
'D23':{'D16':'The randomized specialization allows regression fits to converge to limits bar-mu^a different from the true conditional mean functions.','D17':'It replaces fitted propensities with the true probability pi(x), known by design.','D20':'Its nuisance-convergence notation refers to either growing training-fold fitted function.','D21':'The specialization explicitly starts from the cross-fit estimator25.','D24':'Its L2 convergence statement refers to the limiting influence function bar-f defined in27.'},
'D24':{'D16':'The limit influence formula uses regression limits bar-mu^a, which can differ from the true conditional means.','D17':'The limit formula27 retains the true propensity pi(x) in both residual weights, without itself assuming it is known.'},
'D25':{'D15':'The equality identifying each expected time-indexed potential-outcome contrast is stated under the earlier causal identification assumptions.'},
'D26':{'D16':'ATE1 imposes L2 convergence of regression estimators to bar-mu^a uniformly over all covariate observation indices i.'},
'D27':{'D16':'ATE2 averages products containing the two treatment-specific regression estimation errors.','D17':'The other factor in each product is the propensity estimation error at X_i.'},
'D28':{'D17':'Theorem3.1’s overlap clause bounds the true treatment probability pi(X) away from both endpoints.'}}
REASONS={
'2.2':{1:'Theorem2.2’s explicit interval is asserted to form an AsympCS, using Definition2.1’s relative-width approximation to a nonasymptotic CS. Its iid finite-variance model and empirical moments are bound within the theorem.'},
'2.4':{1:'Theorem2.4 concludes an AsympCS and explicitly spells out the common-center nonasymptotic interval and almost-sure width ratios from Definition2.1.',2:'Theorem2.4 explicitly assumes G1, the coupling and strong-approximation rate for the estimator error.',3:'Theorem2.4 explicitly assumes G2, a simultaneous boundary for the coupled approximating process.',4:'Theorem2.4 explicitly assumes G3, negligibility of the coupling error compared with both boundary widths.',5:'Theorem2.4 explicitly assumes G4, almost-sure relative approximation of both hatted boundaries.'},
'2.8':{1:'Theorem2.8 calls the intervals18 AsympCSs; their approximation meaning remains Definition2.1, distinct from the extra limiting coverage conclusion.',6:'Theorem2.8 imports Proposition2.5’s conditional moment setup and targets the running average of its conditional means.',7:'Theorem2.8 explicitly assumes L1, divergence of cumulative conditional variance.',8:'Theorem2.8 explicitly assumes L2, the conditional Lindeberg-type tail summability requirement.',9:'Theorem2.8 explicitly requires L3eta, the polynomial-rate variance-estimation condition, rather than merely the weaker L3 ratio condition.',10:'Theorem2.8 asserts sharp asymptotic coverage in the sense of Definition2.7 and prints the stronger ordinary-limit equality1-alpha.',11:'Theorem2.8 explicitly refers to the later-started intervals Ctilde_t(m) given by equation18.'},
'3.1':{1:'Theorem3.1’s interval is asserted to be an AsympCS for the ATE under Definition2.1.',14:'Theorem3.1 targets psi, the expected potential-outcome contrast defined at the start of Section3.',15:'The standing Section3 causal identification assumptions identify that psi with the observed-data functional used by the AIPW estimator.',16:'Theorem3.1 explicitly compares fitted regression functions to possibly misspecified limits bar-mu^a and mentions the true mu^a.',17:'Theorem3.1 explicitly bounds pi(X), the treatment propensity defined in Section3.2.',20:'Theorem3.1’s L2 convergence and variance formula contain the fitted influence function hat-f_t, constructed by opposite-fold nuisance substitution.',21:'Theorem3.1 explicitly takes the cross-fit AIPW estimator from equation25.',22:'Theorem3.1’s width uses varhat_t(hat-f), the cross-fit variance estimate in26.',23:'Theorem3.1 is in the randomized-experiment setting described immediately beforehand, using true propensities and allowing misspecified regression limits.',24:'Theorem3.1 assumes convergence to bar-f and a2+epsilon moment for that limiting influence function, whose formula is27.',28:'Theorem3.1 explicitly assumes the true-propensity overlap clause preserved here.'},
'3.2':{1:'Theorem3.2’s interval is asserted to be an AsympCS for psi under Definition2.1.',14:'Theorem3.2 retains the ATE targetpsi through its common setup with Theorem3.1.',15:'The common Section3 causal identification assumptions continue to identify the observed-data ATE in the observational setting.',16:'Theorem3.2 requires the regression estimates to converge to the true mu^a and includes their errors in its product rate.',17:'Theorem3.2 explicitly changes pi(x) from known to estimated while retaining the same propensity probability object.',18:'Theorem3.2 explicitly cites efficient influence function24, requires hat-f_t→f in L2 and a2+epsilon moment forf.',20:'Theorem3.2 uses fitted influence functions with consistently estimated regression and propensity nuisances, evaluated out of fold.',21:'Its common setup retains the cross-fit AIPW estimator25 as the interval center.',22:'Theorem3.2’s width explicitly uses the fitted cross-fit variance varhat_t(hat-f) defined in26.',28:'The common-setup reference to Theorem3.1 retains its bound on the true propensity; it does not independently impose a bound on estimated propensities.'},
'3.3':{1:'Theorem3.3’s interval is an AsympCS for a moving parameter sequence, a case explicitly allowed by Definition2.1.',13:'Theorem3.3 explicitly imports every Corollary2.6 assumption with Y_t replaced by bar-f(Z_t), including all moment and variation-in-means conditions.',21:'Theorem3.3 centers its interval at the cross-fit estimator psi-hat-times; page22 explicitly says the single-fold estimator cannot replace it for moving targets.',24:'Theorem3.3 substitutes the limiting influence-function sequence bar-f(Z_t) into Corollary2.6 and prints bar-f as the variance argument. That latter source object remains unresolved in auxiliaryA9, without equating it to fitted variance26.',25:'Theorem3.3 explicitly targets the running mean of the time-indexed expected treatment effectspsi_i defined in Section3.4.',26:'Theorem3.3 explicitly assumes tilde-ATE1, uniform L2 convergence of the regression estimators over all observation indices.',27:'Theorem3.3 explicitly assumes tilde-ATE2, the average product of nuisance errors at rateo(sqrt(logt/t)).'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Retain all six actual main-text Theorems. Separate AsympCS approximation from later-start coverage, four coupling conditions, conditional/independent moment requirements and randomized/observational/moving-effect models.',build_order_policy='Derive same-paper paths from original source formulas and explicit condition references. Respect overrides in T3.2, full Corollary2.6 substitution in T3.3, and unresolved bar-f variance notation. No proof-only or implication-only dependencies; no appendix bodies.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGE_TEXT.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=DIRECT[n];assert set(REASONS[n])==set(DIRECT_NUMS[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=direct_reason(n,lid),evidence=copy.deepcopy(c['evidence'])+copy.deepcopy(members[lid]['evidence'])))
    edges=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=edges[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for rel in x['related_theorems']:
            cid=rel['claim_id'];n=cid.split('/T')[-1];path=rel['via_local_ids']
            reason=' '.join([direct_reason(n,path[0])]+[EDGE_TEXT[a][b] for a,b in zip(path,path[1:])]);ev=copy.deepcopy(claims[cid]['evidence'])
            for lid in path:ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=reason,evidence=ev)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems']);selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors) and all(s in linked for s in selectors),(m['local_id'],[s for s in selectors if s not in linked])
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Census structurally validated; independent source review remains pending.')
if __name__=='__main__':main()
