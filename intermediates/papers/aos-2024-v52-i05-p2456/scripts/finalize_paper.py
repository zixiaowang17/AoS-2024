"""Finalize separate abstract-CLT, statistical null and bootstrap statement graphs."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'4.1':[3,4,6],'4.3':[3,8,10,14,15,17,19],'4.4':[3,19,20,21,22]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'The RKHS H_K is associated with the real symmetric covariance kernel K defined in Section3.'},
'D3':{'D2':'H_K* consists of bounded linear functionals on H_K, with norm defined by the supremum over its unit ball B_K.'},
'D4':{'D3':'AssumptionA concerns an arbitrary sequence S_n in H_K*, evaluated on H_K and tested for vanishing squared coordinate tails in an orthonormal basis.'},
'D5':{'D2':'T_sigma acts on H_K using the kernel section K_x, and its eigenvectors are orthonormal in the H_K inner product.','D4':'Its covariance form sigma and trace summability are supplied by AssumptionA, under which the source introduces the spectral notation mu_j,phi_j.'},
'D6':{'D3':'S_infinity is defined as a random bounded functional in H_K*.','D5':'The Gaussian series uses sqrt(mu_j) and the H_K-orthonormal eigenvectors of T_sigma, with iid standard-normal coefficients.'},
'D8':{'D7':'The CMR null requires the given measurable moment function to have conditional expectation zero at some theta_0 under the observed joint law.'},
'D9':{'D7':'The score differentiates epsilon(Z,theta), and the conditional score takes its expectation given X in the joint observation model.'},
'D10':{'D9':'The population projection subtracts G(a,theta_0)Gamma^−1 g, where both G and Gamma are moments of the conditional score.'},
'D11':{'D1':'The projected kernel formula combines the original covariance kernel K with two cross terms and a double-expectation correction.','D9':'Its auxiliary Upsilon kernel is built from conditional scores at both arguments.','D10':'Upsilon uses the same population score Gram inverse Gamma^−1 as Pi; Kperp is the covariance kernel pertaining to that population projection.'},
'D12':{'D9':'The empirical projection uses the fitted conditional scores g(X_i,theta-hat) in G_n and Gamma_n.','D10':'The source explicitly defines Pi-hat as the sample analog of the population projection(13), replacing the population moments by sample moments.'},
'D13':{'D1':'The raw Gram matrix has entries K(X_i,X_j)/n, retaining its exact factor1/n.','D9':'The fitted projection matrix is formed from the n-by-p design whose rows are fitted conditional scores.'},
'D14':{'D2':'Rhat_n is indexed by a in H_K.','D12':'Equation(15) uses the fitted projected weights Pi-hat a(X_i).','D23':'Each projected weight multiplies the fitted residual epsilon(Z_i,theta-hat), with overall scale1/sqrt(n).'},
'D15':{'D13':'Algorithm1 computes n*Qhat as the fitted-residual quadratic form in the projected Gram matrix.','D14':'Equation(14) identifies the same statistic with sup over the H_K unit ball of Rhat_n(a)^2.','D23':'The quadratic-form vector is the fitted residual vector from Algorithm1 step1.'},
'D16':{'D7':'The weighting measure uses the conditional second moment E[epsilon(Z,theta_0)^2|X] under the data law.','D11':'Its kappa-perp integral is the diagonal integral of the population projected kernel Kperp against mu.'},
'D17':{'D11':'The integral operator and its expansion are defined for Kperp, with eigenvalues lambda_j and functions varphi_j.','D16':'The operator acts on L2(mu); both orthonormality and almost-everywhere expansion are relative to the residual-second-moment-weighted measure, under integrability(16).'},
'D18':{'D1':'Kappa_s integrates the original kernel diagonal K(x,x), not Kperp, against the score moment measure.','D9':'The source measure uses E[s*s-prime|X], and dot-s and dot-g differentiate the score and conditional score.'},
'D19':{'D1':'B(i) explicitly requires a separable covariate support, continuous K and finite mean kernel diagonal.','D7':'B(iii) imposes twice continuous differentiability and a uniform second-moment bound on the model residual function; B(iv) specifies the parameter domain and fitted-estimator rate.','D9':'B(iii) imposes score and derivative moment bounds and positive definiteness of E[g*g-prime] near theta_0.','D13':'B(ii) names lambda_max(mathbb K)=O_P(n^−1) for the raw Gram matrix defined in Algorithm1.','D16':'B(ii) requires finite kappa-perp for the projected-kernel diagonal under the residual-weighted measure.','D18':'B(ii) requires finite kappa_s, and B(iii) uses Theta_0 and dot-s defined immediately before the assumption.'},
'D20':{'D2':'The bootstrap process has the same H_K index functions as Rhat_n.','D12':'The bootstrap formula holds the fitted projection Pi-hat fixed while resampling multipliers.','D23':'Its summands multiply the fixed fitted residuals by independent bounded iid centered unit-variance V_i.'},
'D22':{'D2':'The limit functional is evaluated on a in H_K, while the printed inner product is that of the projected-kernel RKHS.','D10':'The defining series explicitly contains Pi a, the population score-orthogonal projection(13).','D17':'The series uses lambda_j and L2(mu)-orthonormal varphi_j from the Kperp spectral representation, with the printed coefficient lambda_j rather than sqrt(lambda_j).'},
'D23':{'D7':'The fitted residual is the original moment function evaluated on the observed Z_i at the supplied theta-hat.'}}
def direct_reason(n,lid):
    reasons={
'4.1':{'D3':'Theorem4.1 asserts S_n weakly converges in the separable bounded-functional space H_K*, with the operator-norm and Hoffmann-Jorgensen convention specified in Section4.1.','D4':'Theorem4.1 explicitly assumes all of AssumptionA: coordinate Gaussian limits, summable covariance trace and the double-limit tail condition for the arbitrary sequence S_n.','D6':'Its target S_infinity is the preceding Gaussian random element, whose expansion uses sqrt(mu_j) with the H_K-orthonormal covariance eigenbasis.'},
'4.3':{'D3':'Theorem4.3 explicitly places Rhat_n weak convergence in H_K*, the bounded-functional dual with its operator norm.','D8':'Theorem4.3 explicitly assumes H0, meaning the original conditional moment restriction(1) holds almost surely at some theta_0.','D10':'Its inline R_infinity(a) formula explicitly applies the population projection Pi to a before taking the Kperp-RKHS inner product.','D14':'Theorem4.3 asserts convergence of Rhat_n from(15), the feasible projected process with fitted residuals.','D15':'Its second conclusion concerns n*Qhat_K^perp, the fitted-residual quadratic statistic of Algorithm1 and the squared dual norm in(14).','D17':'The inline limit and chi-square mixture explicitly use lambda_j and varphi_j, the Kperp integral-operator eigenelements normalized in L2(mu), with U_j iid standard normals by the page11 convention.','D19':'Theorem4.3 explicitly invokes AssumptionB as introduced on pages11–12, comprising parts(i)–(iv); the local-power addition(v) has not yet been introduced.'},
'4.4':{'D3':'Both norms in Theorem4.4 are the operator norm on H_K*, previously defined by the supremum over the H_K unit ball.','D19':'Theorem4.4 prints AssumptionB, meaning the preceding parts(i)–(iv). It does not explicitly print H0 or the later local-power part(v).','D20':'Theorem4.4 uses Rhat_n-star, the Section4.3 multiplier process with fitted residuals and projection held fixed, and bounded iid centered unit-variance weights independent of the original data.','D21':'The qualifier convergence-in-distribution a.s. refers to Section4.3’s named almost-sure bootstrap consistency, not almost-sure convergence of the statistic itself; the formal criterion is cited externally.','D22':'Theorem4.4 reuses R_infinity from the inline formula in Theorem4.3. This is a definition reference to its projected-kernel Gaussian series, not an import of Theorem4.3’s H0 premise.'}}
    return reasons[n][lid]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All three main-text Theorems retained. Original assumptions and source definitions are indexed without proof-only dependencies.',build_order_policy='Separate the abstract dual-space theorem from the CMR and bootstrap applications. Preserve population/sample projections, both spectral normalizations, and AssumptionB(i)–(iv) without its later local-power addition.')
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
