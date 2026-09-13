"""Build paper-local dependency paths for the four time-series Theorems."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'1':[1,5,10],'2':[1,5,6,7,8,9,11],'3':[1,5,6,12,13,14,16],'4':[1,5,6,7,9,13,14,16,17,18,19,22,23,24,25]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D3':{'D1':'The coupling coefficient is the m moment norm of X minus its single-innovation replacement.','D2':'The replacement is applied to the same measurable causal map, with an independent copy of one innovation retaining its own law.'},
'D4':{'D1':'Definition1 requires uniformly bounded m moment norms.','D2':'Definition1 explicitly requires the generating equation(2), allowing nonidentical innovations and T-dependent maps.','D3':'Its dependence-tail condition sums the uniform coupling distances delta_m(l).'},
'D5':{'D4':'Remark2 explicitly defines short range as Definition1 with beta=0, including its zero-mean and uniform-moment clauses. The printed k-versus-l typo is preserved separately.'},
'D8':{'D6':'Population autocorrelation is sigma_j/sigma_0 using the Section3 lag-invariant autocovariances.'},
'D9':{'D7':'Sample autocorrelation is the ratio of the two raw lag-product sample covariance estimates in(16).'},
'D11':{'D6':'The autocorrelation linearization uses sigma_j and sigma_0 in its centering and the two ratio-derivative coefficients.'},
'D12':{'D6':'Definition3 solves the Yule–Walker system using lag-only covariances of a weakly stationary process.'},
'D13':{'D7':'The sample Yule–Walker system replaces every covariance by the estimator(16), with denominator T.','D12':'The estimated coefficient vector targets the general-process AR coefficients defined by the population Yule–Walker equations.'},
'D14':{'D6':'The Toeplitz matrix Sigma, vector gamma and lag-selector convention use the population lag covariances.'},
'D15':{'D14':'Every column of B is expressed using Sigma, gamma, coordinate vectors and the lag-selector matrices T_i.'},
'D16':{'D6':'The AR centered lag products use the weak-stationary covariance context; the undefined printed sigma_k^(i) is retained and flagged.','D15':'Equation(27) weights centered products by the full AR derivative matrix B, including columns zero and p.'},
'D20':{'D7':'Second-order residuals subtract the sample covariance sigma-hat_j from each valid observed lag product.'},
'D21':{'D17':'The Gaussian multiplier covariance is K((j1−j2)/k_T), with K from Definition2; its Fourier condition supports positive semidefiniteness.'},
'D22':{'D7':'Equation(38) perturbs the original sample covariance.','D20':'The perturbation uses the lag-specific second-order residuals from Algorithm1 step1.','D21':'The same dependent Gaussian multiplier sequence weights the residuals across lags.'},
'D23':{'D22':'The bootstrap correlation divides the perturbed lag-j covariance by the perturbed lag-zero covariance, not by the original sample variance.'},
'D24':{'D22':'The bootstrap AR vector uses the Toeplitz matrix and lag vector formed from perturbed covariances, followed by the explicitly specified Moore–Penrose inverse.'},
'D25':{'D6':'H_sigma is the maximum CDF of the Gaussian vector defined in Theorem2(i), whose covariance is built from centered population lag products; the printed repeated-j issue is preserved.','D11':'H_rho uses the mean-zero Gaussian vector with covariance from the Theorem2(ii) autocorrelation linearization.','D16':'H_a uses the mean-zero Gaussian vector with covariance from the Theorem3 AR linearization(27).'}}
def direct_reason(n,lid):
    label='Theorem '+n
    if lid=='D1':return label+' uses the m moment norm through short-range dependence and explicitly uses the second moment norm in its normalized-sum lower bound'+('s, via the branchwise references to (18),(20),(28).' if n=='4' else '.')
    if lid=='D5':return label+(' imports from Lemma4 the (m,alpha_X)-short-range condition, with m≥8 and alpha_X>2.' if n=='4' else ' explicitly assumes (m,alpha)- or (m,alpha_X)-short-range dependence with m≥8 and decay exponent greater than two, defined by Remark2 as beta=0 in Definition1.')
    if lid=='D6':return label+(' uses the Section3 mean-zero weak-stationary setting for sigma_j=E X_i X_(i−j); that context precedes its statement.' if n=='2' else ' explicitly assumes weak stationarity and uses the population covariance matrix Sigma.' if n=='3' else ' uses the Section3 stationary covariance targets in branches(i)–(ii), and inherits Theorem3 weak stationarity through Lemma4(iii) for the AR branch.')
    if lid=='D7':return label+' compares sigma-hat_j from(16), the raw sample lag-product sum divided by T'+(' to sigma_j in branch(i).' if n=='2' else ' to its bootstrap perturbation in branch(i).')
    if lid=='D8':return label+(' uses rho_j=sigma_j/sigma_0 as its branch(ii) estimation target.' if n=='2' else ' imports autocorrelation condition(20) through Lemma4(ii), retaining the population variance lower bound and the covariance-ratio setting of branch(ii).')
    if lid=='D9':return label+' uses the sample covariance ratio rho-hat_j from(16)'+(' in the autocorrelation Gaussian approximation.' if n=='2' else ' as the centering of the bootstrap autocorrelation error in branch(ii).')
    if lid=='D10':return 'Theorem1 defines Z_(i,k) as the deterministic a_kj-weighted sum of individually centered lag products, with coefficient-row square bounds and separate p1 growth. It does not assume lag-only stationary centering.'
    if lid=='D11':return 'Theorem2(ii) explicitly defines Z_(i,j) as the two-term autocorrelation linearization and uses it both in nondegeneracy condition(20) and the Gaussian covariance.'
    if lid=='D12':return label+(' explicitly identifies a_1,...,a_p by Definition3, the general-process Yule–Walker system.' if n=='3' else ' inherits the Theorem3 assumptions through Lemma4(iii) and uses the same general-process AR coefficient setting for branch(iii), without requiring a linear AR generating model.')
    if lid=='D13':return label+' uses the sample Yule–Walker coefficient vector a-hat from(24)'+(' in its normalized estimation error.' if n=='3' else ' to center the bootstrap coefficient error in branch(iii).')
    if lid=='D14':return label+' explicitly requires the smallest eigenvalue of the population covariance matrix Sigma to exceed a positive constant'+('.' if n=='3' else ' in branch(iii), where order p remains O(1).')
    if lid=='D16':return label+(' explicitly defines Z_(i,j) by(27), using it in condition(28) and the Gaussian target covariance.' if n=='3' else ' explicitly invokes the AR nondegeneracy condition(28) in branch(iii); its Z is the population AR linearization(27), not the correlation Z or an estimated covariance-lemma quantity.')
    if lid=='D17':return 'Theorem4 explicitly mentions K and imports Lemma4’s requirement that it satisfy the full Definition2, including nonnegative integrable Fourier transform.'
    if lid=='D18':return 'Theorem4 defines v_T by Lemma3 with alpha=alpha_X and uses it in all three bandwidth regimes. This is a numerical definition reference, not a whole-Lemma3 assumption import.'
    if lid=='D19':return 'Theorem4 uses Prob* in all three conclusions, defined as probability conditional on X_1,...,X_T; its Op/op errors are assessed under the outer original-data law.'
    if lid=='D22':return 'Theorem4(i) uses sigma-hat-star from Algorithm1 equation(38), a dependent multiplier perturbation of the sample covariance through centered lag-product residuals.'
    if lid=='D23':return 'Theorem4(ii) uses rho-hat-star from Algorithm1(40), the ratio of two bootstrap covariances, not the estimated linearization appearing in Lemma4(ii).'
    if lid=='D24':return 'Theorem4(iii) uses a-hat-star from Algorithm1(39)–(40), with the Moore–Penrose inverse of the perturbed Toeplitz covariance matrix.'
    if lid=='D25':return 'Theorem4 compares the three conditional bootstrap maximum laws to H_sigma,H_rho,H_a, defined immediately before it as the Gaussian maximum CDFs in(19),(21),(29); their vectors and covariances are distinct and may vary with T.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All four main-text Theorems retained with full statements and every subpart.',build_order_policy='Keep nonstationary linear-combination, stationary covariance/correlation, fixed-order AR and conditional bootstrap scopes distinct. Preserve branchwise assumptions and definition-only references.')
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
