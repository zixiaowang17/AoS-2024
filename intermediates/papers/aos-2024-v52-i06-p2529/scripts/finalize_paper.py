"""Finalize source-specific assumption imports and Gaussian-object references."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'5':[1,2,3,4,5,10,11],'8':[2,3,4,8,19,20,27],'10':[5,7,10,13,14,17,20,22,23,24,26,27]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'Equation3 fixes each marginal tail of the regularly varying X* to have unit exponent-measure mass, with a* the reciprocal marginal tail scale.'},
'D3':{'D1':'The conditional Pareto/spectral limit in(5) is the polar form of the index1 regular variation in(2).'},
'D4':{'D1':'The global coefficient tau is the exponent-measure mass above maximum norm1, equivalently the a*-scaled tail limit.'},
'D8':{'D1':'The subset coefficient is an exponent-measure mass and an a*-scaled tail limit of X*.','D3':'Its alternative expression uses the spectral expectation E ell_I(Theta).','D4':'Equation14 multiplies that expectation by the full-set coefficient tau.','D6':'The set and exceedance event in(13) use ell_I, the coordinate maximum over I.'},
'D9':{'D3':'The law of Theta^I is constructed from the probability spectral law of Theta.','D6':'The tilt and normalization use ell_I(Theta), with rescaling by ell_I before projecting onto I.'},
'D11':{'D5':'The generalized moment estimator is indexed by nonnegative l1-unit convex-combination weights v.','D10':'Its angular summands use the coordinate scaling/power transformation and the perturbation domain A_delta prime.'},
'D12':{'D7':'The subset specialization Phat_{n,u,I}=Phat_{n,u}(1_I) uses the coordinate indicator vector.','D11':'The exceedance proportion is explicitly the p=0 generalized empirical moment, using the printed0^0=1 convention.'},
'D13':{'D3':'The target c is a normalized expectation over the common independent Pareto radial variable Y and probability spectral vector Theta.','D5':'The target is defined on the original nonnegative l1-unit weight domain; its later masked arguments are recorded separately.','D10':'The formula and domain of c use coordinate powers, scaling and A_delta prime.'},
'D14':{'D1':'Corollary6 explicitly imports Theorem5’s index1 regular-variation assumption; its exact sample and sequence clauses are preserved in A1.','D2':'The imported Theorem5 assumptions include unit marginal normalization(3).','D3':'Theorem5’s imported assumptions identify the spectral component Theta, distinct from the X* printed in the bias factor.','D4':'The printed bias comparison contains the global coefficient tau.','D5':'Uniformity is printed over partial B1 star rather than the previously defined plus simplex; preserve this unresolved source-domain discrepancy.','D10':'Uniformity of condition27 is over the same perturbation domain A_delta prime.','D11':'The finite-sample bias term contains the expectation of the generalized empirical moment Mhat.','D13':'The asymptotic bias comparison multiplies the target c, whose spectral normalization differs from the printed X* factor in(27).'},
'D17':{'D5':'The random-threshold estimator retains the convex-combination weight domain inherited from Section3.1.','D6':'Both its angular normalization and exceedance event use the subset maximum ell_I.','D7':'The numerator uses masked v_I without renormalizing the remaining weights.','D16':'Coordinate ratios are taken relative to the positive marginal kth upper order statistics X_{k:n}.','D19':'Coordinate powers are the estimated marginal tail indices alphahat, defined by Hill equation(33).'},
'D19':{'D6':'The singleton maximum ell_{i} selects the ith coordinate in the logarithm and threshold event.','D16':'Hill equation(33) uses X_{k:n} and its strict-exceedance proportion Ptilde, preserved independently as A3; no angular-moment numerator is required.'},
'D20':{'D1':'The second-order expansion concerns the index1 regularly varying normalized coordinate X_i* and its scaling a*.','D2':'Its leading term s^{-1} uses the unit marginal tail normalization(3).'},
'D22':{'D3':'Covariance25 uses the same Pareto Y and spectral Theta in both factors, with a joint exceedance indicator.','D4':'The covariance is multiplied by the global coefficient tau.','D5':'The Gaussian process is indexed by the original convex-combination weight simplex.','D10':'Its two covariance arguments use the perturbation domains and coordinate powers beta and gamma.'},
'D23':{'D5':'The ratio process and its Gaussian limit are indexed by the original simplex of weights.','D7':'The specialized covariance uses indicator vectors1_I and the I-coordinate projection of the tilted spectral vector.','D8':'The specialized Gaussian covariance has the factor1/tau_I.','D9':'Remark7.1 expresses the covariance through the tilted angular law Theta^I projected onto I.','D10':'The defining ratio process uses A_delta prime, with the specialized covariance at s=1_I,beta=1.','D11':'The original process defining the ratio Gaussian limit uses Mhat in its numerator.','D12':'The ratio process divides by the deterministic-threshold exceedance proportion Phat.','D13':'The defining ratio process is centered at the spectral target c; its assumptions are kept separately in D14.'},
'D24':{'D3':'The joint Hill Gaussian covariance contains the spectral minimum E[Theta_i wedge Theta_j].','D4':'The first covariance expression contains the full-set coefficient tau.','D8':'The equivalent expression uses the pair extremal coefficient tau_ij, a specialization of tau_I.','D27':'The covariance scales by the coordinate-specific true tail indices alpha_i alpha_j from the non-standard model.'},
'D26':{'D5':'The original joint-limit statement and cross covariances are indexed by the source convex-combination weights.','D7':'Equation34 and the i in J specialization use the coordinate mask Theta_J and indicator vector1_J.','D22':'Remark9 couples the Hill limit with the G process; p=0 gives the G^0 restriction used in Theorem10.','D23':'Remark9 also couples Gtilde with G through Remark7.2, whose required original cross covariance is preserved as A4.','D24':'The H_i variables are the jointly Gaussian Hill limits of Theorem8, with the original marginal covariance retained.'},
'D27':{'D1':'The non-standard model is defined by the coordinate-specific power transformation yielding the index1 regularly varying X* in(2).'}}
def direct_reason(n,lid):
    reasons={
'5':{'D1':'Theorem5 explicitly assumes a nonnegative regularly varying X* with index1; no unknown-margin standardization is required.','D2':'Theorem5 explicitly requires Eq3, the unit marginal tail normalization and reciprocal scale a*.','D3':'Theorem5 identifies spectral component Theta and uses the common independent Pareto Y and Theta in covariance25.','D4':'Theorem5’s covariance has the explicit factor tau, the full maximum-norm extremal coefficient.','D5':'The process and l-infinity convergence space in Theorem5 explicitly use partial B1 plus, the nonnegative l1-unit weight simplex.','D10':'Theorem5 quantifies delta≥0 and indexes s,beta by A_delta prime, the source’s coordinate perturbation domain.','D11':'Theorem5 defines G_n in(24) from Mhat and its exact expectation; Mhat is the generalized moment estimator in Section3.1.'},
'8':{'D2':'Theorem8 explicitly assumes Eq3 for its normalized X* margins, preserving the unit tail masses.','D3':'Theorem8’s joint Hill covariance contains E[Theta_i wedge Theta_j], using the source probability spectral vector.','D4':'The first Hill covariance expression has the global extremal coefficient tau as its numerator factor.','D8':'The equivalent Hill covariance expression contains tau_ij, the extremal coefficient for the pair {i,j}.','D19':'Theorem8’s reciprocal vector alphahat^{-1} consists of the marginal Hill estimators defined in(33), with denominator and order-statistic conventions preserved.','D20':'Theorem8 explicitly imports second-order condition(30), then adds sqrt(k_n) A_i*(n/k_n)→0 for every margin.','D27':'Theorem8 assumes a non-standard regularly varying X and gives its X* transformation. The source model uses coordinate alpha_i, whereas the theorem prints unindexed alpha in that mapping; both are preserved.'},
'10':{'D5':'Theorem10 indexes v by the nonnegative l1-unit simplex in both its derivative domain and weak convergence space.','D7':'Theorem10 uses v_I and1_I throughout its estimator, centering and Gaussian limit, plus singleton1_{i}; these are masks, not renormalized weights.','D10':'Theorem10 explicitly requires delta>0 and continuous partial derivatives on partial B1 plus times A_delta prime, whose original domain discrepancy is recorded.','D13':'Theorem10 explicitly uses c, its s_i and beta_i partial derivatives, and the target value c(v_I,1_I,1,p).','D14':'Theorem10 explicitly assumes the hypotheses of Corollary6, including its original uniform bias formula(27), finite K and imported Theorem5 assumptions.','D17':'Theorem10’s centered empirical ratio is Mtilde_{n,k,I}(v_I,p)/Ptilde_{n,k,I}, the random-threshold estimator defined in Section3.2.','D20':'Theorem10 explicitly assumes the hypotheses of Theorem8, which include second-order condition(30) and its all-coordinate bias rates; the full imported assumption excerpt is A2.','D22':'Theorem10 uses G^0(1_{i}), defined immediately beforehand as G(.,s,.,0), the p=0 restriction of the Gaussian process in Theorem5.','D23':'Theorem10’s first limit term is Gtilde(v_I,1_I,1,p), whose required same-subset covariance is given in main-text Remark7.1.','D24':'Theorem10 includes alpha_i Htilde_i in each beta-derivative correction, using the jointly Gaussian reciprocal-Hill limit defined in Theorem8.','D26':'Theorem10’s sum combines Gtilde,G^0 and Htilde with the joint law established in Remark9 and Remark7.2; separate independent Gaussian copies would give the wrong limit.','D27':'Theorem10 explicitly assumes the non-standard regularly varying X model and the hypotheses of Theorem8; Section2 defines its coordinate-specific tail indices and standardization.'}}
    return reasons[n][lid]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All three complete main-text Theorems retained. Preserve normalized and non-standard regular variation, expectation centering, separate bias assumptions and the jointly coupled Gaussian limits.',build_order_policy='Derive same-paper dependencies from source definitions and explicit assumption imports. Preserve Corollary6 as an assumption source without counting it as a Theorem; resolve the Hill denominator independently; exclude appendix proofs and preserve source notation issues.')
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
