"""Assemble dependencies without conflating coefficient-CLT conclusions and assumptions."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'2.1':[4,6,7,8],'2.2':[4,6,7,8,9,10,11,12,13],'2.3':[1,4,6,7,8,9,15,16,17,19],'2.4':[1,4,6,7,8,9,15,16,18,19]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'The pooled covariance and separate sample means use the two common-covariance populations specified at the start of Section 2.'},
'D3':{'D1':'The population correlation R is obtained by separating the positive marginal variances of the common covariance Sigma.'},
'D4':{'D3':'Equation (3) models the inverse of the population correlation matrix, not the inverse of the sample covariance.'},
'D5':{'D2':'Rhat is the diagonal normalization of the pooled sample covariance S.'},
'D6':{'D4':'The loss (4) fits the coefficients of the specified symmetric basis matrices A_k.','D5':'Its sample B and b are trace products built from Rhat.'},
'D8':{'D1':'The standardized-coordinate representation uses the two means and common positive-definite covariance Sigma.'},
'D9':{'D4':'Theorem 2.2 bounds normalized trace products R A_i R A_j for the specified linear inverse-correlation bases.'},
'D10':{'D4':'The population B entries are traces of R and the specified A_k.','D7':'Their rank-one correction is multiplied by the finite-sample ratio y_(n−2).'},
'D11':{'D3':'D0 and g are entrywise expressions involving R and its square root.','D8':'The beta_w parameter is kappa−3, using the standardized-coordinate fourth moment from Theorem 2.1.'},
'D12':{'D4':'D1 is the basis combination sum eta_k A_k.','D10':'The contrast coefficient vector eta equals pi times the inverse of the population B defined in Theorem 2.2.'},
'D13':{'D7':'Nu uses y_(n−2), while sigma² also uses its limit y and the printed (1−y) denominator.','D11':'The complete centering and variance use D0, g and beta_w from the same theorem.','D12':'Their contrast dependence is through the matrix D1=sum eta_k A_k.'},
'D14':{'D2':'Precision estimation uses the inverse square roots of diag(S).','D4':'The fitted inverse correlation is a linear combination of the specified bases A_k.','D6':'The coefficient asymptotics inherited by the testing theorems concern the raw estimator B^-1 b; corrected and penalized versions are separately flagged as a source-scope ambiguity.'},
'D15':{'D2':'T_n is the quadratic form of the difference between the two sample means.','D14':'Its weight is the fitted precision matrix Omega-hat from (6).'},
'D16':{'D3':'The null centering and variance use population correlation R, its inverse and the elementwise cubic matrix A0.'},
'D17':{'D14':'Rtilde normalizes the diagonal of Rhat_L, the inverse of the fitted basis combination in (6).','D16':'Substitution of Rtilde into mu0 and sigma0² gives the two estimated null normalizers.'},
'D18':{'D1':'Delta_n is the Mahalanobis quadratic form of the two-population mean difference, and H1 replaces the null.','D7':'Its associated shrinkage c=(1+y)^-1 uses the limiting dimension-to-sample ratio.'},
'D19':{'D3':'The Discussion requires bounded spectral norm of the population correlation matrix R for T2.3–T2.4.'}}
def direct_reason(n,lid):
    label='Theorem '+n
    if lid=='D1':return label+' uses '+('the null H0:mu1=mu2.' if n=='2.3' else 'the alternative H1:mu1≠mu2, replacing the null in the cited theorem.')+' Both populations retain the same finite positive-definite covariance.'
    if lid=='D4':return label+' uses the true coefficient vector theta from the exact inverse-correlation representation (3) in the known symmetric A_k. The Discussion keeps the active K finite and assumes the true bases are included.'
    if lid=='D6':return label+' concerns '+('theta-hat=B^-1 b from (4), the unpenalized trace-loss minimizer.' if n in ['2.1','2.2'] else 'a test built from coefficients whose assumptions are inherited from Theorems 2.1–2.2; their established estimator is the unpenalized B^-1 b.')+' The bias-corrected and penalized reuse of theta-hat is recorded separately.'
    if lid=='D7':return label+' uses the preceding ratio y_(n−2)=p/(n−2) and finite limit y'+('; its scale additionally prints (1−y)^-2 without explicitly excluding y=1.' if n=='2.2' else '; c-hat uses the finite ratio.' if n=='2.3' else '; c uses the limit.' if n=='2.4' else ' in the almost-sure shrinkage factor.')
    if lid=='D8':return label+(' states' if n=='2.1' else ' inherits')+' the representation x^(m)=Sigma^(1/2)w+mu_m with iid coordinates of w having mean zero, variance one and fourth moment kappa.'
    if lid=='D9':return label+(' imposes' if n=='2.2' else ' inherits from Theorem 2.2')+' bounded p^-1 tr(R A_i R A_j), for the fixed basis indices i,j.'
    if lid=='D10':return 'Theorem 2.2 explicitly defines a population B using trace products and the y_(n−2) correction. This is not the sample B of (4).'
    if lid=='D11':return 'Theorem 2.2 explicitly defines D0, the fourth-moment kernel g and beta_w=kappa−3 for its centering and variance formulas.'
    if lid=='D12':return 'Theorem 2.2 explicitly defines D1=sum eta_k A_k, with eta=pi B^-1 using its population B and arbitrary contrast pi.'
    if lid=='D13':return 'Theorem 2.2 standardizes its coefficient contrast by the full centering nu and scale sigma, whose formulas span pages 5–6; all terms and trace powers are retained.'
    if lid=='D15':return label+' normalizes n T_n, where (7) defines T_n without n using the fitted precision and difference of sample means.'
    if lid=='D16':return label+(' defines' if n=='2.3' else ' uses the definitions from Theorem 2.3 of')+' the population null centering mu0 and variance sigma0², including the elementwise cubic matrix A0. They are distinct from the coefficient-CLT nu and sigma².'
    if lid=='D17':return 'Theorem 2.3 uses c-hat, mu0-hat and sigma0-hat; the last sentence prescribes substitution of the fitted, re-normalized correlation Rtilde into the population normalizers.'
    if lid=='D18':return 'Theorem 2.4 defines delta_n as the population Mahalanobis squared mean difference and c=(1+y)^-1. Its explicit H1 replaces H0 rather than conjoining the two.'
    if lid=='D19':return label+' is explicitly named in the Discussion as requiring bounded spectral norm of R. The condition is retained as a separate original source passage because the printed theorem does not spell it out.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All four main-text Theorems retained, including the complete two-page coefficient-CLT formulas.',build_order_policy='Distinguish sample/population B, unpenalized versus corrected or penalized coefficients, coefficient-CLT conclusions versus inherited assumptions, and population versus estimated test normalizers.')
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
