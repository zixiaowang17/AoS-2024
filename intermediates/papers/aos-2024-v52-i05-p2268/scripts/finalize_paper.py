"""Resolve EILLS theorem requirements with distinct population and empirical objectives."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'4.2':[12,14,15,18,19,20,21,22,26],'4.3':[11,15,16,17,18,19,22,23,25,26],'4.4':[1,11,15,16,17,18,19,22,25,26],'4.5':[13,15,16,17,19,22,24,26]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'The true residual subtracts the common conditional mean on the true support S* from the model (2.1).'},
'D5':{'D3':'The restricted predictor (2.6) is defined when the environment population covariance is positive definite.','D4':'Its objective is the environment population squared prediction risk R^(e) from (2.5).'},
'D7':{'D4':'The population focused regularizer in (3.2) penalizes coordinate gradients of R^(e).','D6':'Its environment contributions use the fixed positive normalized weights omega^(e).'},
'D9':{'D6':'The empirical moment penalties are averaged using omega^(e).','D8':'Each moment is a within-environment empirical average before it is squared.'},
'D10':{'D27':'The pooled loss in (3.6) uses the within-environment empirical risk Rhat^(e) from (2.5).','D6':'The per-environment losses are weighted by omega^(e).','D8':'The expanded formula divides each within-environment sum by n^(e).'},
'D11':{'D9':'The EILLS objective (3.7) includes gamma times the empirical focused regularizer Jhat.','D10':'Its data-fitting component is the pooled empirical squared loss Rhat.'},
'D12':{'D4':'The intended population data-fitting component is the weighted population risk R^(e) in (2.5); equation (3.8) prints an x-versus-beta typo, retained separately.','D6':'The population objective retains the environment weights omega.','D7':'The population EILLS objective adds gamma times the population focused gradient regularizer J.'},
'D13':{'D11':'The l0-regularized criterion (3.9) adds lambda times support cardinality to the unpenalized EILLS objective (3.7).'},
'D14':{'D3':'The pooled covariance is the equal-weight average of the environment covariance matrices.'},
'D15':{'D3':'Condition4.2 bounds each full environment population covariance between kappa_L I and kappa_U I.'},
'D16':{'D14':'Condition4.3 whitens every environment covariate by the common pooled Sigma, not by Sigma^(e).'},
'D17':{'D2':'Condition4.4 applies to the true model residual epsilon^(e), not an arbitrary fitted residual.'},
'D18':{'D2':'G is defined by the pooled correlations of covariates with the true residual epsilon^(e).'},
'D19':{'D5':'Identification compares the restricted population least-squares predictors beta^(e,S) across environments.','D18':'The quantifier ranges over every support S intersecting the pooled spurious-variable set G.'},
'D20':{'D2':'The bias mean b_S is the squared norm of the pooled correlation with the true residual.'},
'D21':{'D5':'The dispersion dbar_S is the mean squared deviation of beta^(e,S) from its mean across environments.'},
'D22':{'D15':'The critical threshold contains the lower eigenvalue constant kappa_L to power minus three.','D18':'Its supremum ranges over supports meeting G.','D20':'The numerator of the critical ratio is b_S.','D21':'The denominator of the critical ratio is dbar_S.'},
'D23':{'D1':'The screening signal s_+ is the squared smallest coefficient on the true support S*.','D18':'The heterogeneity signal minimizes over supports intersecting G.','D21':'The minimized heterogeneity quantity is the environment coefficient dispersion dbar_S.'},
'D24':{'D1':'The high-dimensional condition defines s*=|S*| and beta_min from the true model coefficients.','D15':'Both sample-size bounds use the uniform lower covariance constant kappa_L.'},
'D25':{'D15':'The screening sample bounds use kappa_L in the gamma-to-curvature ratio and the heterogeneity factor.','D23':'Both screening bounds involve the two signals s_+ and s_- defined in (4.7).'},
'D26':{'D1':'Condition4.1 requires every environment law to belong to the common distribution class U_(beta*,sigma²).'}}
EDGE_TEXT['D27']={'D8':'The empirical risk in (2.5) uses the within-environment empirical expectation.'}
def direct_reason(n,lid):
    label='Theorem '+n
    if lid=='D1':return 'Theorem4.4 uses the true-support size |S*| and min_j∈S* |beta*_j| directly in (4.10), with beta* and its support defined in (2.1).'
    if lid=='D11':return label+' concerns the global empirical EILLS minimizer beta-hat_Q of (3.7), using the support-gated moment penalty and pooled sample loss.'
    if lid=='D12':return 'Theorem4.2 compares values of the population EILLS objective Q from (3.8). Its quoted data-fit formula contains the original x-versus-beta typo; the source’s (2.5) supplies the intended squared prediction risk.'
    if lid=='D13':return 'Theorem4.5 concerns the global l0-regularized minimizer beta-hat_L of (3.9); its additional lambda penalty is absent from the estimator in T4.3–T4.4.'
    if lid=='D14':return 'Theorem4.2 uses the pooled Sigma^(1/2) in its lower bound; Sigma is the uniform average defined at the start of Section4.'
    if lid=='D15':return label+' assumes Condition4.2: every environment population covariance has eigenvalues between the fixed kappa_L and kappa_U.'
    if lid=='D16':return label+' assumes Condition4.3, a joint sub-Gaussian bound for every linear functional of the covariates normalized by pooled Sigma.'
    if lid=='D17':return label+' assumes Condition4.4, the marginal sub-Gaussian bound on the true residual; no independence from all covariates is added.'
    if lid=='D18':return label+(' uses G in the critical supremum over supports.' if n=='4.2' else ' uses G^c in the screening event.' if n=='4.3' else ' uses |G^c| in its improved error bound, whose extra conditions come from T4.3.')+' G is the set of nonzero pooled residual-covariate correlations from Definition4.1.'
    if lid=='D19':return label+' assumes Condition4.5: for every support meeting G there is an environment pair with different restricted least-squares coefficients. The pair may depend on the support.'
    if lid=='D20':return 'Theorem4.2 explicitly defines b_S as the squared norm of the average residual-covariate moment; it is not the average of squared moments.'
    if lid=='D21':return 'Theorem4.2 explicitly defines dbar_S and the environment-average restricted coefficient, and uses dbar_supp(beta) in its objective lower bound.'
    if lid=='D22':return label+(' defines gamma* through the supremum of b_S/dbar_S and allows gamma≥epsilon^-1 gamma*.' if n=='4.2' else ' requires gamma≥max(3gamma*,1), referring to gamma* defined in T4.2. This imports its definition, not a new strong-convexity assumption or full theorem conclusion.')
    if lid=='D23':return 'Theorem4.3 defines the two screening signals s_+=min_j∈S* |beta*_j|² and s_-=min_S:S∩G≠empty dbar_S in (4.7).'
    if lid=='D24':return 'Theorem4.5 assumes Condition4.6, including the bound log|E|≤C log p and both per-environment and total-sample inequalities. Its sparsity s* and beta_min are defined in the immediately preceding main-text sentence.'
    if lid=='D25':return label+(' imposes both of the screening sample-size inequalities.' if n=='4.3' else ' imports the additional T4.3 sample-size bounds only for the moreover branch (4.11). The first bound (4.10) does not require successful screening.')
    if lid=='D26':return label+' assumes Condition4.1: iid samples within each environment, independence across environments, the common true conditional-mean model, equal sample counts n and uniform weights.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All four main-text Theorems retained with complete formulas and separate conditional error bounds.',build_order_policy='Preserve population versus empirical objectives, balanced sampling, pooled versus individual environment covariance, focused support gates, definition-only threshold references, and additional screening conditions only in the improved-bound branch.')
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
