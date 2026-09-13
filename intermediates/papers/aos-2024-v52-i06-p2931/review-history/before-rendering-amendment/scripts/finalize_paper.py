"""Derive source-backed statement relationships for all six decentralized-learning Theorems."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'1':[2,7,8,10,11,17,18,19,20,21],'2':[4,7,8,10,11,13,14,17,18,19,21,22,23],'3':[4,10,11,16,17,18,19,22,24,25,26,27,28],'4':[4,10,11,16,17,18,19,22,24,25,27,28,30,31,32,33],'5':[5,7,10,11,17,19,22,24,26,27,36,38],'6':[4,10,11,17,18,19,22,24,25,27,28,32,39]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D3':{'D1':'The federated risk averages the original client population risks.','D2':'The averaging coefficients are the positive normalized balanced weights.'},
'D4':{'D3':'The target minimizes the original weighted federated risk F.','D5':'The minimization domain is the original closed convex parameter space Phi.'},
'D6':{'D5':'The metric projection is onto the original closed convex parameter space.'},
'D10':{'D9':'Assumption 2.1 constrains the spectrum of the original client connection matrix.'},
'D12':{'D1':'Each gradient column differentiates its client-specific loss at the client iterate and local observation.','D2':'The gradient matrix uses K times the preassigned client weights.'},
'D13':{'D6':'The update projects the resulting state matrix columnwise onto Phi.','D9':'At each synchronization time the update right-multiplies by the client connection matrix.','D11':'The theorem-level DFL trajectories use the original eta_t step-size family.','D12':'The recurrence uses the estimate matrix and K-scaled weighted gradient matrix from (6).'},
'D14':{'D13':'The spatial mean averages the actual DFL client iterates at a fixed time.'},
'D15':{'D13':'The temporal mean averages the actual trajectory of one DFL client.'},
'D16':{'D14':'The joint PR mean averages spatial means over time.','D15':'Equivalently, the source obtains the joint PR mean by averaging client temporal means.'},
'D17':{'D1':'Gradient noise is the stochastic client gradient minus its population-risk gradient.','D5':'The noise-moment bound is uniform over the original parameter space.'},
'D18':{'D1':'Assumption 3.2 is imposed on every original client population risk.','D5':'The convexity/smoothness inequality ranges over pairs in Phi.','D7':'The quadratic remainder uses the original Euclidean norm convention.'},
'D19':{'D1':'The heterogeneity bound compares each original client risk gradient.','D2':'The squared gradient differences are averaged with the original weights.','D3':'The comparison gradient is that of the aggregate federated risk.','D4':'The second bound is evaluated at the K-dependent federated minimizer.','D7':'Both bounds use the original Euclidean norm.'},
'D20':{'D4':'The MSE bound defining B_MSE is centered at the federated target.','D8':'The matrix bound defining B_CE uses the source I-J right-centering notation.','D10':'Lemma 1 expressly assumes network condition 2.1.','D11':'Lemma 1 expressly assumes step-size condition 2.2.','D13':'The lemma bounds actual DFL estimates.','D14':'Its MSE term concerns the spatially averaged iterate.','D17':'The lemma expressly selects v=1 in noise-moment Assumption 3.1.','D18':'The lemma expressly assumes population smoothness/convexity 3.2.','D19':'The lemma expressly assumes heterogeneity condition 3.3.','D21':'The second bound defines a uniform constant for the original consensus error.'},
'D21':{'D7':'Consensus error uses squared Euclidean norms of client disagreements.','D13':'The client values in the disagreement are the actual DFL iterates.','D14':'Each client is compared with the unweighted spatial average.'},
'D22':{'D1':'The curvature inequality is imposed on every client population risk.','D3':'The zero-mu branch imposes generalized self-concordance on the aggregate risk.','D4':'The zero-mu Hessian lower bound is evaluated at the original target.','D5':'The assumption distinguishes unbounded and bounded parameter-space regimes.','D7':'The inequalities use the original Euclidean norm and PSD order.'},
'D23':{'D5':'The zero-mu formula uses the diameter R_d of Phi.','D18':'Both formulas use the smoothness constant L from Assumption 3.2.','D22':'The formulas use mu, mu_star and B_G from the original curvature alternatives.'},
'D24':{'D1':'The averaged smoothness inequality compares stochastic gradients of each original client loss.','D5':'The two parameter values belong to Phi.','D7':'The expectation bounds a squared Euclidean gradient difference.'},
'D25':{'D2':'Aggregated noise uses square-root K times the original client weights.','D4':'Client covariance and the higher moment are evaluated at theta_K*.','D7':'The covariance lower bound uses PSD order and the noise bound uses the Euclidean norm.','D17':'The covariance and aggregated noise are built from the original gradient-noise variables.'},
'D26':{'D3':'Assumption 4.3 differentiates the aggregate population risk twice.','D4':'Its Hessian comparison is centered at theta_K*.','D5':'The Hessian comparison ranges over Phi.','D7':'It uses the spectral matrix norm and Euclidean parameter norm.'},
'D27':{'D3':'The Hessian is that of the aggregate federated risk.','D4':'It is evaluated at the K-dependent target.'},
'D28':{'D25':'The covariance uses the aggregated noise expressly defined in Assumption 4.2.'},
'D29':{'D1':'The covariance estimate uses gradients of the original client loss.','D13':'The gradients are evaluated at the original local DFL iterates, with the printed time-index convention.'},
'D30':{'D2':'The aggregation uses K times the squared original weights.','D28':'The target is the aggregate gradient-noise covariance S.','D29':'The summands are the centered local estimates from (22).'},
'D31':{'D1':'The estimate takes Hessians of the original client loss.','D2':'Local Hessian estimates are combined with the original weights.','D15':'Each sampled Hessian is evaluated at a local temporal average.','D27':'The target is the population Hessian H at the federated minimizer.'},
'D32':{'D1':'Assumption 4.4 requires twice differentiable individual losses and compares their Hessians.','D4':'Both stochastic-Hessian bounds are centered at theta_K*.','D5':'The parameter comparison ranges over Phi.','D7':'Both stochastic-Hessian bounds use squared spectral norm.'},
'D33':{'D16':'The confidence region is centered at the joint PR average.','D30':'The sandwich uses the aggregate centered covariance estimate.','D31':'Both inverse factors are the smooth plug-in Hessian estimate.'},
'D34':{'D11':'The normalization branches use the same step-size exponent alpha.'},
'D36':{'D11':'The initial segment has different formulas for the two step-size exponent regimes.'},
'D37':{'D1':'The regression responses are original client stochastic gradients.','D2':'Z aggregates client cross-products with the original weights and factor K.','D13':'Both regressors and gradients use the original DFL trajectories.','D16':'Regressors are centered by the joint PR average through time T-1.','D27':'The regression targets the original population Hessian.','D34':'The two B normalizations are defined through the original C(T,alpha).','D36':'The sums and gradient centering use the original r1/r3 time segments.'},
'D38':{'D35':'The source applies spectral clipping (30) to V before inversion.','D37':'The numerator Z and the matrix V come from the centered decentralized regression.'},
'D39':{'D1':'The correction uses gradients of the original client losses.','D2':'The gradient correction retains the original client weights.','D13':'Each gradient is evaluated at its own previous local DFL iterate.','D16':'The initial estimator is the joint PR average with alpha=1.','D31':'The inverse correction matrix is explicitly the smooth Hessian estimate (24).'}}
BASE={
10:'The theorem requires the original network contraction Assumption 2.1',
11:'The theorem requires the original step-size Assumption 2.2',
17:'The theorem requires the gradient-noise moment Assumption 3.1',
18:'The theorem requires population convexity/smoothness Assumption 3.2',
19:'The theorem requires the heterogeneity and target-gradient Assumption 3.3',
22:'The theorem requires the complete alternative curvature Assumption 3.4',
24:'The theorem explicitly requires stochastic-gradient Assumption 4.1',
25:'The theorem explicitly requires nondegenerate aggregated-noise Assumption 4.2',
26:'The theorem explicitly requires population-Hessian Assumption 4.3',
32:'The theorem explicitly requires stochastic-Hessian Assumption 4.4'}
REASONS={}
for n,nums in DIRECT_NUMS.items():
    REASONS[n]={}
    for i in nums:
        if i in BASE:
            via=' through the reference to Lemma 1.' if n=='1' else (' through the reference to Theorem 2.' if n in ['3','4','6'] and i in [10,11,17,18,19,22] else '.')
            REASONS[n][i]=BASE[i]+via
            if i==17:REASONS[n][i]+=' The selected moment level is v='+('2' if n=='5' else '1')+'.'
            if i==11:REASONS[n][i]+=(' Here alpha=1 is explicit.' if n=='6' else ' The original exponent range is preserved with the theorem-specific restriction.')
REASONS['1'].update({2:'Theorem 1 explicitly uses b2 from the bound K*w_k<=b2.',7:'Its left-hand side is the squared Frobenius norm of the centered estimate matrix.',8:'Its matrix expression uses the original I-J right-centering notation; the source dimension convention is noted separately.',20:'The theorem explicitly binds B_MSE and B_CE by reference to Lemma 1 and uses them in the unbounded-domain Q formula.',21:'The quantity bounded is the original DFL consensus error; its displayed matrix form represents the client disagreement.'})
REASONS['2'].update({4:'The theorem defines Delta_t by subtracting the federated minimizer theta_K* and uses that target in its initial-error and convergence statements.',7:'Its MSE and consensus terms use the original Euclidean and Frobenius norms.',8:'The consensus contribution uses the original I-J matrix notation.',13:'The initial-error term contains the shared initial estimate theta_hat_0 from the DFL initialization.',14:'Delta_t and the almost-sure conclusion concern the spatially averaged DFL iterate.',21:'Part (i) contains the original consensus error, while part (ii) binds c0 through its rate.',23:'Parts (i)–(ii) explicitly use mu_Rd from (17), including its occurrence in the extra D/gamma conditions.'})
REASONS['3'].update({4:'The theorem centers at theta_K* and explicitly bounds its norm uniformly in K.',16:'The normal approximation concerns the joint spatial-temporal PR average.',27:'The normalizing Hessian H is explicitly defined in the theorem.',28:'The normalizing covariance S is explicitly defined from the aggregated noise.'})
REASONS['4'].update({4:'The premises bound the target and client gradients at that target uniformly in K.',16:'The coverage statement is centered at the joint PR average.',27:'The covariance limit contains the inverse population Hessian H.',28:'The covariance limit contains the aggregate noise covariance S.',30:'The final definition of Sigma_hat explicitly uses S_hat from (23).',31:'The condition K*a(T)->infinity and the final sandwich definition use the trailing-window Hessian estimator (24).',33:'The theorem defines the sandwich estimate Sigma_hat and states its chi-square coverage property.'})
REASONS['5'].update({5:'Theorem 5 explicitly requires Phi to be bounded with finite diameter R_d in both exponent regimes.',7:'The conclusion is convergence of the expected Frobenius norm of the Hessian estimation error.',27:'The target H is the population Hessian at theta_K*.',36:'The theorem explicitly binds zeta by (31), and the estimator uses the original time-segment allocation.',38:'The convergence concerns the thresholded regression Hessian, denoted H_tilde_reg, not the plug-in Hessian (24).'})
REASONS['6'].update({4:'The theorem centers at theta_K* and assumes its uniform norm bound.',27:'The expansion and CLT use the original population Hessian H.',28:'The expansion and CLT use the original aggregate noise covariance S.',39:'The theorem explicitly identifies the alpha=1 one-step estimator by (33); the printed uppercase F_k in the expansion is retained as a source issue.'})
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Preserve all six original main-text Theorems and original federated risks, network and gradient assumptions, averaging schemes and statistical estimators.',build_order_policy='Derive same-paper paths from original source definitions. Keep fixed/growing client regimes, v=1/v=2 noise moments, curvature alternatives, and smooth/regression Hessian estimates distinct. Record ambiguous referenced conditional assumptions and source conventions separately instead of adding unstated hypotheses.')
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
