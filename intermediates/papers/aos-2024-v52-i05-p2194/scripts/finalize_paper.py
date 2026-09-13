"""Assemble source relationships while retaining design and theorem-subpart scope."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={
'3.1':[2,3,4,5,6,7,8,9,10,11,12,24,26],
'3.2':[2,3,4,5,6,7,8,10,12,13,14,15,24,27],
'4.1':[2,3,4,5,6,7,8,10,16,17,18,19,20,22,23,25,28],
'5.1':[2,3,4,5,6,7,8,9,10,12,13,14,15,26,27,29,30],
'5.2':[2,3,4,5,6,7,10,16,17,18,19,20,22,23,28,29,30],
'5.3':[7,9,10,11,12,13,14,15,26,27,30,31,32,34],
'5.4':[7,10,16,17,18,19,20,22,23,28,30,33,34],
'6.1':[10,13,14,15,29,35],
'6.2':[10,13,14,15,29,36],
'6.3':[1,3,10,12,37]}
DIRECT={n:['D'+str(i) for i in ids] for n,ids in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'The empirical population distribution sums the N units of the finite population in Section 2.'},
'D3':{'D2':'Equation (1) normalizes a weighted estimator of F_y,N and takes its generalized inverse; x uses the analogous construction.'},
'D4':{'D2':'The ratio correction uses the known finite-population auxiliary quantile Q_x,N.','D3':'The ratio is formed from the two weighted sample quantiles Qhat_y and Qhat_x.'},
'D5':{'D2':'The difference correction uses the known Q_x,N.','D3':'It corrects Qhat_y by Q_x,N minus the weighted sample quantile Qhat_x.'},
'D6':{'D2':'The regression correction uses the known finite-population auxiliary quantile.','D3':'It adjusts Qhat_y using Qhat_x and the uncentered weighted slope defined in (2).'},
'D7':{'D1':'P* integrates the subset sampling probabilities P(s,omega) over the superpopulation measure.'},
'D9':{'D1':'The relative-entropy sum ranges over fixed-size samples in S.','D7':'Equation (3) uses the random design P(s,omega), with convergence almost surely under the superpopulation law.'},
'D11':{'D1':'Assumption 2 constrains the inclusion probabilities of the fixed-size sample design.'},
'D13':{'D1':'RHC partitions the finite population using SRSWOR draws before one PPS draw from each group.'},
'D16':{'D1':'The two-stage stratum design selects a subset s of the population with inclusion probability pi_i=m_h r_h/(M_h N_hj).'},
'D17':{'D16':'Assumption 6 uses the stratum, cluster and sample counts of the two-stage design.'},
'D18':{'D16':'Assumption 7 is indexed by the stratum/cluster/unit observations of Section 4.'},
'D19':{'D16':'Assumption 8 requires the marginal CDFs of the stratum-specific superpopulation model to have common supports and positive continuous derivatives.'},
'D20':{'D16':'Assumption 9 controls growing-H cluster counts and cluster-size variation for that design.'},
'D21':{'D16':'The mixture CDF weights are N_h/N, using the stratum-specific distributions and counts.'},
'D22':{'D16':'The moment sums in Assumption 10 range over all stratum/cluster/unit indices.','D21':'Its covariance limits use Gamma_h, defined from indicators at mixture quantiles Q_y,H and Q_x,H.'},
'D23':{'D21':'Assumption 11 imposes convergence of the mixture CDFs and uniform convergence of their derivatives.'},
'D24':{'D3':'Table 1 first row corresponds to the weighted sample quantile.','D4':'Its second row subtracts the auxiliary indicator scaled by the ratio of superpopulation quantiles.','D5':'Its third row corresponds to the difference estimator, using the ratio E_P Y/E_P X.','D6':'Its fourth row corresponds to the regression estimator; the printed second-moment typography is retained.'},
'D25':{'D3':'Both Table 3 regimes include the sample-quantile row.','D4':'Both include the ratio-estimator row with mixture quantile ratio.','D5':'Both include a difference-estimator row, using stratum expectations for fixed H and Theta_2/Theta_1 for growing H.','D6':'Both include a regression-estimator row, using stratum moments or Theta_3/Theta_4.','D21':'All rows evaluate indicators and densities at the mixture quantiles from Section 4.'},
'D26':{'D1':'Kernel (5) depends on inclusion probabilities and their centering correction.','D24':'Theorem 3.1 explicitly supplies its zeta_i from Table 1.'},
'D27':{'D13':'Kernel (7) uses the RHC group-size factor gamma and its limit c.','D24':'Theorem 3.2 explicitly supplies its zeta_i from Table 1.'},
'D28':{'D16':'Kernel (8) sums stratum contributions with N_h(N_h-n_h)/n_h.','D25':'Theorem 4.1 explicitly supplies zeta-prime from Table 3, selecting the appropriate H regime.'},
'D29':{'D2':'Both smooth parameters are functions of the finite-population quantile Q_y,N.'},
'D30':{'D29':'The variance functionals use the weight J and gradient of the smooth finite-quantile function f.'},
'D31':{'D1':'Kernel estimator (12) uses inverse inclusion probabilities and the sampled units.','D24':'Its zeta-hat is obtained by estimated substitutions in Table 1; the substitutions are only referenced to the supplement.'},
'D32':{'D13':'Kernel estimator (13) uses the RHC group total A_i and within-group weights.','D27':'It uses gamma and the Table-1 zeta underlying kernel (7); the exact estimated substitutions are unresolved.'},
'D33':{'D16':'Equations (15)–(16) use the sampled clusters, sampled units and stratum size weights.','D25':'The estimated zeta-prime is formed from Table 3, with exact substitutions referenced to supplement Table 6.'},
'D34':{'D3':'The estimated gradient is evaluated at the unadjusted weighted sample quantiles Qhat_y as printed.','D29':'The variance estimators use the same smooth J and f as the finite-population parameters.','D30':'They estimate sigma_1² and sigma_2² from (10), with the supplied estimated covariance kernel.'},
'D35':{'D9':'The fixed design may be HEpiPS, defined in Section 3 as high entropy and piPS.','D26':'The comparison family explicitly refers to Table 2, which supplies the SRSWOR and HEpiPS cases of kernel (5).','D27':'The comparison family explicitly refers to kernel (7) for the RHC case.'},
'D36':{'D9':'The third design-indexed kernel is for an HEpiPS design.','D26':'The first and third kernels come from the SRSWOR and HEpiPS specializations in Table 2.','D27':'The second design-indexed kernel is the RHC covariance (7).'},
'D37':{'D1':'The mean/median/GREG comparison is under SRSWOR.','D3':'Its sample median is Qhat_y(0.5), the unadjusted weighted sample quantile (under SRSWOR weights).'}}
def direct_reason(n,lid):
    label='Theorem '+n
    if lid=='D1':return label+' explicitly works under SRSWOR, the fixed-size subset sampling law in Section 2.'
    if lid=='D2':return label+' uses Q_y,N as its finite-population quantile target, explicitly or through the cited convergence conclusion.'
    if lid in ['D3','D4','D5','D6']:
        name={'D3':'sample quantile Qhat_y','D4':'ratio estimator Qhat_y,RA','D5':'difference estimator Qhat_y,DI','D6':'regression estimator Qhat_y,REG'}[lid]
        return label+' selects the '+name+' from (1)–(2), '+('in the conclusion imported from Theorem 3.1, with the current design weights.' if n in ['3.2','4.1'] else 'in the normal limits (9) imported with cluster weights.' if n=='5.2' else 'at p=0.5 for the sample-median comparison.' if n=='6.3' else 'as one of the four choices for G in the stated process or functional.')
    if lid=='D7':return label+' states its stochastic conclusion under the joint law P*, explicitly or through (9)/(14); Section 3 defines it by integrating the sampling design over P. '+('Section 4 uses the distinct stratum model A9.' if n in ['4.1','5.2','5.4'] else 'Single-stage branches use the iid superpopulation model A3.')
    if lid=='D8':return label+' uses the D[alpha,beta] process-convergence conclusion '+('as a hypothesis in part (i).' if n=='5.1' else 'with the supremum metric and left-continuous/right-limit path convention from Section 2.')
    if lid=='D9':return label+' explicitly specifies a high entropy sampling design'+(' in part (i); its RHC branch is separate.' if n in ['5.1','5.3'] else '.')+' Equation (3) defines the KL limit to a rejective design.'
    if lid=='D10':return label+' invokes Assumption 1'+(' through Theorem 3.2 assumptions in part (ii) only; part (i) assumes a convergence conclusion.' if n=='5.1' else ', including both relevant branches.' if n in ['4.1','5.2','5.3','5.4'] else '.')+(' Here lambda is further restricted to (0,E_P X_i/b).' if n in ['6.1','6.2'] else '')
    if lid=='D11':return label+' requires Assumption 2'+(' in its high-entropy part (i), through Theorem 3.1 assumptions and its final explicit reference; not in its RHC part (ii).' if n=='5.3' else ', the covariance limit and inclusion-probability bounds in Section 3.')
    if lid=='D12':return label+' invokes Assumption 3'+(' through Theorem 3.2 assumptions only in part (ii).' if n=='5.1' else ' through the assumptions of both Theorems 3.1 and 3.2 in their respective branches.' if n=='5.3' else ', requiring positive continuous derivatives of the superpopulation CDFs on the source open supports.')
    if lid=='D13':return label+' specifies RHC and grouping (6)'+(' through the Theorem 3.2 assumptions in part (ii).' if n in ['5.1','5.3'] else '.' if n=='3.2' else ', with the comparison considering SRSWOR and HEpiPS as well; (6) is explicitly printed.')+' A_i is the sampled group auxiliary total.'
    if lid in ['D14','D15']:
        a='4 (the uniform max/min auxiliary-value ratio)' if lid=='D14' else '5 (joint-support noncollinearity)'
        return label+' invokes Assumption '+a+(' through Theorem 3.2 assumptions in part (ii) only.' if n in ['5.1','5.3'] else ' in its printed opening conditions.')
    if lid=='D16':return label+' specifies stratified multistage cluster sampling with SRSWOR; Section 4 defines its two sampling stages, inclusion probability and stratum-specific model.'
    if lid in ['D17','D18','D19','D20','D22','D23']:
        num={'D17':6,'D18':7,'D19':8,'D20':9,'D22':10,'D23':11}[lid]
        branch='both H regimes' if num==8 else 'the fixed-H branch only' if num in [6,7] else 'the growing-H branch only'
        return label+' invokes Assumption '+str(num)+' in '+branch+(' through the assumptions of Theorem 4.1.' if n=='5.4' else '.')+' The theorem dependency union does not make these alternative regimes simultaneous.'
    if lid=='D24':return label+' explicitly refers to Table 1 for the four zeta_i expressions used in its covariance kernel.'
    if lid=='D25':return 'Theorem 4.1 explicitly refers to Table 3 for zeta-prime, with distinct fixed-H and growing-H rows.'
    if lid=='D26':return label+' uses covariance kernel (5)'+(' in its high-entropy branch.' if n in ['5.1','5.3'] else '.')+(' Part (i) separately assumes its continuity and the process convergence conclusion.' if n=='5.1' else '')
    if lid=='D27':return label+' uses RHC covariance kernel (7)'+(' in part (ii), through the Theorem 3.2 assumptions and resulting limit.' if n=='5.1' else ' in part (ii).' if n=='5.3' else '.')
    if lid=='D28':return label+' uses stratum covariance kernel (8), with the appropriate Table 3 regime'+('; part (ii) additionally assumes continuity.' if n=='5.2' else '.')
    if lid=='D29':return label+' states results for the integral of Q_y,N against J and for f of finitely many quantiles. Section 5 specifies smooth J on [0,1] and smooth f:R^k→R.'
    if lid=='D30':return label+' uses the variance targets sigma_1² and sigma_2² of (10)–(11), '+('in the normal limits (9).' if n in ['5.1','5.2'] else 'as the limits of the variance estimators in (14).')+' The covariance kernel is chosen for each design; the formula alone does not impose all designs.'
    if lid=='D31':return 'Theorem 5.3(i) explicitly specifies Khat by (12), with inverse-inclusion weighting and supplement-referenced zeta-hat substitutions.'
    if lid=='D32':return 'Theorem 5.3(ii) explicitly specifies Khat by (13), with RHC grouping weights and supplement-referenced zeta-hat substitutions.'
    if lid=='D33':return 'Theorem 5.4 explicitly specifies Khat by (16); (15) and its preceding prose define the stratum centering and leave exact substitutions to supplement Table 6.'
    if lid=='D34':return label+' asserts the consistency (14) of the variance estimators defined immediately before Theorem 5.3; the gradient uses Qhat_y, and the current design supplies Khat.'
    if lid=='D35':return 'Theorem 6.1 uses K_1,...,K_4 and Delta_1,...,Delta_4 from (17): four estimator choices under one fixed sampling design, compared through maxima over u=2,...,4.'
    if lid=='D36':return 'Theorem 6.2 uses K_1*,K_2*,K_3* and Delta_1*,Delta_2*,Delta_3* from (20): three designs for one fixed estimator G, compared through maxima over u=2,3.'
    if lid=='D37':return 'Theorem 6.3 compares sample median, sample mean and the cited GREG mean estimator. Section 6.2 specifies superpopulation centering but gives no GREG formula; the external definition stays unresolved.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Every one of ten main-text Theorems retained with all subparts; dependencies cover uses in alternative branches without conjoining their conditions.',build_order_policy='Paper-local dependencies distinguish design alternatives, fixed/growing strata, conclusion references and assumption references. Supplement-only and external definitions remain explicitly unresolved.')
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
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=reason,evidence=ev)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors) and all(s in linked for s in selectors),(m['local_id'],[s for s in selectors if s not in linked])
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Census structurally validated; independent source review remains pending.')
if __name__=='__main__':main()
