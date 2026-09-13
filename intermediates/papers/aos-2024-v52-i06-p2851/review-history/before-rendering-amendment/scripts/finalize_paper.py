"""Derive source-backed statement relationships for all four PCM Theorems."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'4':[1,3,4,5,10,11,12,13,14,17,18,26,27],'5':[2,3,4,5,8,10,11,13,17,18,25],'6':[1,5,10,11,19,20,22,23,24],'7':[2,5,11,19,20,22]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D1':{'D6':'The null equates the full regression to the response-on-Z conditional mean m.','D7':'The full conditional expectation in the null is the regression denoted by g_P in Assumption 4.'},
'D2':{'D8':'The signal tau is the expected square of the regression difference h.'},
'D8':{'D6':'The projection h subtracts the response-on-Z conditional mean m.','D7':'The first term of h is the full response regression g.'},
'D9':{'D4':'The population regression of hatf conditions on its training sample and computation randomness under the explicit Section 1.3 convention.'},
'D10':{'D4':'Algorithm 1 uses two independent data splits and fitted functions under the source sampling convention.','D5':'Its final rejection rule compares T with the standard normal quantile z_(1-alpha).'},
'D11':{'D4':'Algorithm 2 uses four independent splits of n observations, with fitted-function conditioning understood as in Section 1.3.','D5':'Algorithm 2 retains the normal-quantile rejection rule and alpha input.','D10':'Algorithm 2 explicitly performs Algorithm 1 with the two residualization training datasets replaced by D3 and D4.'},
'D12':{'D6':'The response residual epsilon subtracts m_P(Z), the conditional expectation of Y given Z.'},
'D13':{'D9':'The population projection residual xi subtracts m_(P,hatf)(Z).'},
'D14':{'D4':'The variance sigma_P² conditions on the training sample and randomness represented by hatf.','D13':'sigma_P² is the conditional variance of the population projection residual xi_P.'},
'D15':{'D6':'The first MSPE compares the supplied response regression estimate with its target m_P.'},
'D16':{'D9':'The second MSPE compares the fitted projection regression with its population target m_(P,hatf).','D14':'The source normalizes the second MSPE by sigma_P².'},
'D17':{'D3':'Assumption 3 imposes uniform small-order conditions on both MSPEs, their product and the weighted error.','D13':'Part (b) weights the response prediction error by the squared population projection residual xi_(P,i).','D14':'Part (b) divides by the random conditional variance sigma_P².','D15':'Part (a) requires the first, response-regression MSPE to vanish and enter the product bound.','D16':'Part (a) uses the normalized second MSPE in both its individual and product bounds.'},
'D20':{'D10':'The spline procedure uses Algorithm 1 notation and replaces its variance learner by one while specifying all relevant regression methods; Algorithm 2 can then change the training splits.','D19':'The four spline choices use phi, phi^Z and the higher-order psi bases defined immediately before them.'},
'D22':{'D6':'Assumption 4(c) bounds the Holder norm of the response-on-Z conditional mean m_P.','D7':'Assumption 4 defines the full response mean g_P and bounds its Holder norm.','D12':'Assumption 4(a) uses the response residual epsilon_P from (11), namely Y-m_P(Z).','D19':'Assumption 4 uses the unit-cube dimensions d_X,d_Z,d and spline order r fixed in Section 5.','D21':'Part (c) uses the Holder spaces and norms whose precise definitions are referenced in Definition S24.'},
'D23':{'D19':'The coefficient projection uses K_X,K_Z,K_XZ and the source tensor ordering to subtract within-block means.'},
'D24':{'D19':'The coefficient identity uses the joint tensor basis and its X-basis partition of unity.','D20':'The coefficients beta_XZ and beta_Z are the outputs of the ghat and mtilde spline regressions.'},
'D26':{'D10':'The linear-smoother alternative is expressly for the response regression mhat in Algorithm 1.'}}
REASONS={
'4':{
1:'Theorem 4 explicitly defines its null class by equality of the full and Z-only conditional means.',
3:'Theorem 4(b) uses the uniform conditional Lyapunov order o_(P0)(n^(delta/2)), with the Section 1.3 meaning of uniform order.',
4:'Theorem 4(b) conditions its residual moment on hatf; Section 1.3 specifies that this includes its training data and computation randomness.',
5:'The conclusion compares the distribution of T with the standard normal distribution function Phi, uniformly in t.',
10:'Alternatives (ii), (iii) and (iv) compute T by Algorithm 1, each with its own additional condition; they are not simultaneous requirements.',
11:'Alternative (i) computes T by Algorithm 2 with auxiliary training datasets, without requiring the other three alternatives.',
12:'Conditions (b) and (c) use epsilon_P, the response residual Y-m_P(Z) from (11).',
13:'Condition (b) uses xi_P, the population-residualized learned projection from (11).',
14:'Conditions (a) and (b) use the random conditional projection variance sigma_P² from (12).',
17:'The first sentence explicitly assumes Assumption 3 over the null class P0.',
18:'Alternative (iv), and only that alternative here, requires the response learner to satisfy the sufficiently stable conditions referenced on page 18.',
26:'Alternative (iii) requires the response learner mhat in Algorithm 1 to be a linear smoother.',
27:'Alternative (ii) imposes full conditional independence Y independent of X given Z, which is stronger than the common conditional-mean null.'},
'5':{
2:'Theorem 5 defines its separated alternative class by tau_P>=epsilon_n, using the squared regression-difference signal (1).',
3:'Its assumption (d) requires a probability to be o(1) uniformly over the separated class; Assumption 3 also uses uniform probabilistic orders.',
4:'Condition (d) takes conditional correlation given hatf under the training-sample conditioning convention.',
5:'The power conclusion is for the upper-tail normal cutoff z_(1-alpha), for each alpha in (0,1).',
8:'Conditions (b) and (d) use h_P(X,Z), the unweighted difference of conditional regression means; (b) is printed as a one-sided upper bound.',
10:'The second algorithm alternative uses Algorithm 1 together with sufficient stability of mhat.',
11:'The first algorithm alternative uses Algorithm 2, with the two final regressions trained on auxiliary splits.',
13:'Condition (d) requires positive conditional correlation with xi_P, the population projection residual from (11), not its fitted counterpart.',
17:'Theorem 5 begins by assuming Assumption 3 over the alternative class P1.',
18:'The Algorithm 1 alternative requires the sufficiently stable response learner defined by the supplemental reference in Section 4.1.',
25:'Condition (a) explicitly requires positive-scale equivariance of the fitted projection regression method.'},
'6':{
1:'Theorem 6 explicitly restricts Assumption 4 to distributions satisfying the conditional-mean null.',
5:'Its conclusion is uniform convergence of the distribution of T to the standard normal CDF Phi.',
10:'Theorem 6 permits Algorithm 1 when its regressions use the spline choices specified in Section 5.',
11:'Theorem 6 also permits Algorithm 2 with those spline choices and auxiliary training splits.',
19:'Theorem 6 uses phi in the conditional covariance Lambda and the basis dimensions K_XZ and tilde K_Z in its two rate conditions.',
20:'The final premise explicitly requires T to be computed using spline regressions, including the variance-one override and OLS basis choices.',
22:'Its first sentence assumes Assumption 4, and conditions (14) and (16) refer back to its constants c and delta.',
23:'The nondegeneracy condition uses Pi beta_hat, and (14) restricts the Rayleigh minimization to Pi x=x.',
24:'The nondegeneracy condition uses the estimated coefficient contrast beta_hat defined immediately before the theorem.'},
'7':{
2:'Theorem 7 defines the separated class using tau_P>=epsilon_n, with tau the squared regression-difference signal (1).',
5:'Its power conclusion uses the upper-tail normal cutoff z_(1-alpha); the alpha range is supplied by Algorithm 2.',
11:'Theorem 7 specifies Algorithm 2 only. The source expressly excludes this result from the D3=D4 auxiliary-sample reuse relaxation.',
19:'Its tuning assumptions specify K_X,K_Z,tilde K_Z, order r and total dimension d from the original spline setup.',
20:'Theorem 7 expressly requires the spline regression choices, including variance one and the higher-order final-regression basis.',
22:'Its first sentence assumes the full distributional and smoothness conditions of Assumption 4.'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Preserve all four original main-text Theorems and the original regression targets, procedures, assumptions and spline conditions.',build_order_policy='Derive same-paper paths from the original source definitions. Preserve disjunctive algorithm branches and spline overrides; proof reductions do not add generic regression assumptions to the spline statements.')
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
