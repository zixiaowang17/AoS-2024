"""Derive source-backed theorem dependencies without importing supplementary bodies."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'3.1':[1,5,6,7,8],'3.2':[1,5,6,7,8,9],'3.3':[1,5,6,7,8,9,10,12,15,36],'4.1':[4,5,16],'5.1':[1,6,7,8,9,10,18,22,24],'6.1':[2,5,6,25,31],'6.2':[6,25,33]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D1':{'D2':'Model(2.1) assigns each regression coefficient by the four original sign-defined regions R_k.'},
'D4':{'D2':'Criterion(3.1) evaluates the four sign indicators1_k at the candidate hyperplane scores.'},
'D5':{'D3':'The LSE definition minimizes over the normalized compact parameter spaceTheta.','D4':'Its minimizers attain the infimum of empirical criterionM_T in(3.1).'},
'D7':{'D2':'Assumption2 uses true/candidate region intersections and distinct coefficients on adjacent sign-defined regions.','D3':'Its covariance condition quantifies every candidate gamma inGamma1×Gamma2.','D11':'Its local mass condition usesq_i, and its fixed-jump clause uses the ordered adjacent-region setS(i).'},
'D9':{'D11':'Assumption4 uses the signed boundary coordinateq_i and the pairsS(i) to state local mass and regression-jump conditions.'},
'D10':{'D11':'Assumption5 constrains the near-zero boundary scoresq_i,t.','D13':'It requires continuity/bounds for the conditional densities of the boundary score and its contrast markxi, and compact support ofZ_-1,i.'},
'D11':{'D2':'The adjacency setsS(1),S(2) are defined by which of the four sign regions share a splitting hyperplane.'},
'D12':{'D2':'The covarianceSigma_k and design momentB_k restrict their expectations to the true sign regionR_k.'},
'D13':{'D2':'Each contrast markxi is multiplied by the indicator of a union of two source regions, and its sign is determined on a region.','D11':'The jump-mark construction explicitly selects adjacent pairs(k,h) inS(i) and uses their boundary scoreq_i.'},
'D14':{'D11':'The limiting process sums over each boundary and its ordered adjacent-region pairsS(i).','D13':'Its independent marks and density-scaled signed arrivals use the source conditional laws ofxi andq_i, and signs s_i^(k).'},
'D15':{'D5':'The empirical centroid is taken over the original boundary-LSE minimizer setG-hat.','D35':'The mapC is the source centroid integral functional.'},
'D16':{'D3':'The MIQP explicitly requires beta_k inB andgamma_j inGamma_j.','D17':'Its lifted-product constraints use the coefficient boundsL_i,U_i.','D32':'It uses the candidate-region indicatorsI, lifted productsell and their sign constants from the algebraic reformulation.','D34':'Its second constraint line uses the data-dependent boundM_jt and binary hyperplane sign encodingg_jt.'},
'D17':{'D3':'The finite coordinate bounds are chosen over the compact coefficient spaceB.'},
'D18':{'D1':'The source explicitly calls heteroscedastic model(5.1) a refinement of four-regime model(2.1).','D2':'Its conditional regression sum uses the original sign-defined regionsR_k.'},
'D20':{'D2':'Fitted residuals subtract the regression associated with each estimated source region.','D5':'The residuals are formed from the original least-squares estimates.','D18':'The local-linear estimator targets the conditional variance sigma0² from the heteroscedastic refinement.','D19':'It uses the K1,K2 kernels and covariate dimensions introduced in the smoothing passage, with its own bandwidthsb1,b2.'},
'D21':{'D20':'Standardized residuals divide the fitted errors by the local-linear scale estimate before centering.'},
'D22':{'D18':'Assumption6(ii) bounds the target conditional variance sigma0².','D19':'It constrains the joint covariate density, K1/K2 kernels andh bandwidths from the smoothed-law construction.','D20':'It also constrains theb bandwidths used for the local-linear variance estimator.'},
'D23':{'D2':'Bootstrap outcomes use the sign-defined regions evaluated at the original empirical centroid.','D5':'Each resample is fitted by the same LSE construction, producing regression estimates and boundary minimizers.','D15':'The source empirical centroid centers the boundary estimates and defines bootstrap regime membership.','D19':'Step1 samples covariates from the preceding smoothed distribution, calledF-tilde in the step.','D20':'Bootstrap outcomes are scaled with the local-linear conditional standard-deviation estimate.','D21':'Step1 samples standardized errors independently from their centered empirical distributionG-hat.'},
'D24':{'D5':'The target distribution uses the original regression LSE and its true coefficient vector.','D15':'Its boundary component is theT-scaled empirical centroid error.','D23':'The approximating law is the empirical distribution ofB resamples produced by the three-step smoothed bootstrap.'},
'D25':{'D26':'Unified model(6.6) includes the source nonintersecting three-region family(a.1).','D27':'It includes the intersecting three-region family(a.2), whose printed region discrepancy is preserved.','D28':'It includes the one-hyperplane two-region family(b.1).','D29':'It includes the two-hyperplane intersection/complement family(b.2).','D30':'ItsK0=1 case is the global linear family(c).'},
'D31':{'D5':'The finite coefficient and boundary sets are formed from four-regime LSEs obtained by(3.2).'},
'D32':{'D2':'The candidate indicatorI_k,t refers to the original four sign regionsR_k(gamma).','D4':'The lifted quadratic expression is explicitly the original empirical criterionM_T rewritten usingell=I*beta.'},
'D33':{'D2':'The initial fitted cells are the original four sign regions before adjacent cells are merged.','D3':'Each merged-cell regression is minimized over the coefficient spaceB.','D5':'The initial coefficients and cells are those of the four-regime LSE fit.'},
'D34':{'D3':'M_jt maximizes the absolute candidate score overGamma_j.','D32':'The binary sign variables are introduced to link candidate-region indicatorsI_k,t to the hyperplane coefficients.'},
'D36':{'D14':'The limiting centroid is taken over the set of minimizers of the printed marked processD(v).','D35':'It uses the same source centroid functionalC, separate from the empirical minimizer set.'}}
REASONS={
'3.1':{1:'Theorem3.1 targets theta0, the stacked boundary/regression coefficients of the original four-regime model.',5:'It asserts consistency for the LSE theta-hat with any gamma-hat in the minimizer setG-hat.',6:'It explicitly assumes Assumption1, temporal dependence and the martingale-difference error condition.',7:'It explicitly assumes Assumption2, the four identification clauses.',8:'It explicitly assumes Assumption3, moments and local crossing-probability control.'},
'3.2':{1:'Theorem3.2 compares the LSEs with beta0 andgamma0 from the original four-regime model.',5:'Its rates hold for the regression LSE and any boundary minimizer inG-hat.',6:'It explicitly includes Assumption1 inAssumptions1–4.',7:'It explicitly includes Assumption2 inAssumptions1–4.',8:'It explicitly includes Assumption3 inAssumptions1–4.',9:'It explicitly assumes Assumption4, including local boundary mass, jump and intersection/moment conditions.'},
'3.3':{1:'Theorem3.3 concerns the original regression and boundary coefficients in the four-regime model.',5:'Its regression components are the original LSEs beta-hat_k.',6:'It explicitly includes Assumption1 inAssumptions1–5.',7:'It explicitly includes Assumption2 inAssumptions1–5.',8:'It explicitly includes Assumption3 inAssumptions1–5.',9:'It explicitly includes Assumption4 inAssumptions1–5.',10:'It explicitly assumes Assumption5 on near-boundary dependence and conditional densities.',12:'Its Gaussian limit uses covarianceSigma_k defined before the theorem.',15:'Its boundary estimate is specifically the centroid gamma-hat-c, rather than an arbitrary minimizer.',36:'The boundary limit isgamma_D-c, the centroid of the limiting-process minimizer set.'},
'4.1':{4:'Theorem4.1 asserts equality of the original least-squares criterionM_T at the two fits.',5:'Its theta-hat is explicitly a solution ofLSE definition(3.2).',16:'Its theta-tilde is explicitly a solution of the full MIQP(4.6)–(4.7) for small positiveepsilon.'},
'5.1':{1:'Theorem5.1 targets the distribution of estimates of the original four-regime coefficients, under the stated model setup.',6:'It explicitly includes Assumption1 inAssumptions1–6.',7:'It explicitly includes Assumption2 inAssumptions1–6.',8:'It explicitly includes Assumption3 inAssumptions1–6.',9:'It explicitly includes Assumption4 inAssumptions1–6.',10:'It explicitly includes Assumption5 inAssumptions1–6.',18:'Section5 sets the bootstrap theorem under the independent standardized-error refinement(5.1); this is not inferred solely from mean-zero errors.',22:'It explicitly assumes Assumption6 governing densities, conditional variance, kernels and bandwidths.',24:'Its metric comparesL_T,B withL_T, the joint bootstrap empirical law and target law defined immediately above it.'},
'6.1':{2:'Its regime-error conclusion uses unions of fitted four-regime cellsR_i(gamma-hat), whose sign convention is the original one.',5:'Those fitted regions and coefficients come from the four-regime LSE procedure(3.2), even when the true model has fewer regimes.',6:'Theorem6.1 explicitly assumes Assumption1, while its other assumptionsS2–S4 remain external and unresolved.',25:'It explicitly takes the true model from(6.6), withK0<4 and at most two boundaries.',31:'It measures errors by the defined point-to-set distanced, using the finite fitted coefficient and boundary sets.'},
'6.2':{6:'Through its reference to the assumptions ofTheorem6.1, it retains Assumption1 and the separately recorded unresolvedS2–S4.',25:'That same reference retains the true degenerate model(6.6) withK0<4; no unprinted four-regime extension is added.',33:'Its selectedK-hat and reported merged-region coefficients are explicitly the outputs of(6.8), built by the complete preceding recursive merging algorithm.'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Preserve every one of the seven main-text Theorems and original source entries. Separate empirical versus limiting centroids, algebraic optimization from stochastic assumptions, and degenerate true models from four-regime fitted models.',build_order_policy='Derive paper-local dependency paths from original formulas and explicit references. Keep supplementaryS2–S4 unresolved as external prerequisites. Do not import theorem conclusions as assumptions or silently repair source discrepancies.')
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
