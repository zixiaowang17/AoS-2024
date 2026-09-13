"""Derive source-backed theorem dependencies without importing supplementary bodies."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'2.1':[4,8,9,10,11,12,13,15],'4.1':[4,11,16,17,18,19,21,22,23],'4.5':[11,16,17,18,19,22,23,24,28,29]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'The KL projection minimizes divergence from the true experiment P0^n over the model family P_Theta.'},
'D3':{'D1':'The log-likelihood is log p_theta^n evaluated on the observed data from that dominated experiment.'},
'D4':{'D3':'The prior and posterior are those for the stated model likelihood; the ordinary Bayes relationship is recorded as ambient interpretation.'},
'D5':{'D2':'The original derivative notation is evaluated at the KL projection theta_*, with later evaluation points explicitly changed to the MAP.','D3':'These arrays are successive derivatives of the source log-likelihood ell(theta).'},
'D6':{'D5':'Observed information J is defined as the negative second log-likelihood derivative array.'},
'D7':{'D2':'The displayed prior-derivative notation is initially evaluated at theta_*, with evaluation at generic local points in Assumption10.','D4':'These are derivatives of the logarithm of the source prior density pi.'},
'D8':{'D2':'The local coordinate h is centered at the KL projection theta_*.'},
'D10':{'D9':'The skewing weight is F of an odd polynomial, using the original symmetric-CDF and local-expansion convention.'},
'D11':{'D2':'Assumption1 requires the original KL projection parameter to be unique.'},
'D12':{'D1':'Assumption2 expands the ratio of model densities p_theta^n under stochastic order governed by the true law P0^n.','D2':'The ratio is centered at the projection theta_*.','D8':'The perturbation is theta_*+delta_n h at the generic norming rate.','D14':'Its uniform remainder uses K_n and M_n, whose definitions are separated from the expansion hypothesis.'},
'D13':{'D2':'The prior expansion is centered at theta_*.','D4':'Its ratio uses the original prior density pi.','D8':'The prior argument is theta_*+delta_n h under the generic local rescaling.','D14':'Its supremum uses the same K_n and logarithmic radius M_n without importing Assumption2 regularity.'},
'D14':{'D8':'The logarithmic radius and theta-space ball use the generic norming delta_n and its center theta_*.'},
'D15':{'D2':'The contraction region is centered at theta_*.','D4':'The inner tail probability is taken under the original posterior Pi_n.','D8':'Both the radius and probability threshold are expressed using the generic rate delta_n.','D14':'Its radius uses M_n defined immediately before the assumptions.'},
'D16':{'D2':'The prior smoothness and positive finite density condition are at the KL projection theta_*.','D4':'The differentiated function is the logarithm of the original prior density.'},
'D17':{'D2':'The likelihood separation is outside neighborhoods of theta_*.','D3':'It bounds the original normalized log-likelihood difference ell(theta)-ell(theta_*).'},
'D18':{'D3':'The MAP maximizes the sum containing the log-likelihood ell(theta).','D4':'The other term in its objective is the log prior density pi(theta).'},
'D19':{'D18':'The root-n local coordinate is centered at the MAP theta-hat.'},
'D20':{'D6':'The covariance is the inverse of observed likelihood information J divided by n.','D18':'That observed information is evaluated at the MAP theta-hat.'},
'D21':{'D5':'Its cubic skewing factor contains the third log-likelihood derivative.','D9':'The factor uses the source CDF F and its expansion slope eta.','D18':'The derivatives are evaluated at the MAP.','D19':'It is a density for the root-n MAP-centered coordinate hat h.','D20':'The Gaussian factor uses the original covariance Omega-hat.'},
'D22':{'D2':'The proximity event measures distance from theta_*.','D18':'The estimator in that event is the original MAP, not a generic efficient estimator.'},
'D23':{'D5':'The joint event controls spectral norms of third and fourth likelihood derivatives divided by n.','D7':'The same event controls the log-prior Hessian.','D18':'All local suprema are on a fixed-radius ball centered at the MAP.','D20':'Its separate eigenvalue event bounds the inverse Gaussian covariance defined before Eq22.'},
'D24':{'D19':'The retained and complementary coordinates split the MAP-centered variable hat h.'},
'D25':{'D20':'The blocks, conditional mean matrix and Schur complement come from Omega-hat.','D24':'The block partition is indexed by C and its complement.'},
'D26':{'D5':'Every coefficient contracts the third likelihood derivative array.','D18':'That derivative is evaluated at the MAP.','D24':'The free indexes are in C and contracted complementary indexes are in C complement.','D25':'The contractions use the conditional Gaussian matrix Lambda_C and covariance barOmega.'},
'D27':{'D9':'Its normalization divides by eta, the original CDF expansion slope.','D24':'Its arguments are the selected coordinates hat h_C with indexes in C.','D26':'Its linear and cubic terms use the original coefficients nu_1 and nu_3 from Eq29.'},
'D28':{'D9':'The skewing factor applies the source symmetric CDF F.','D24':'The density has dimension d_C and argument hat h_C.','D25':'Its Gaussian factor uses the selected block Omega-hat_CC.','D27':'Its skewing argument is the separately constructed marginal polynomial alpha_(eta,C).'},
'D29':{'D4':'It integrates the true posterior density pi_n.','D19':'That posterior is expressed in the MAP-centered coordinate hat h.','D24':'The integration removes the complementary block and retains coordinates C.'}}
REASONS={
'2.1':{4:'Theorem 2.1 compares the rescaled posterior Pi_n with the SKS probability measure.',8:'Its h and delta_n use the original generic norming sequence tending to zero and centering at theta_*.',9:'The theorem explicitly repeats the conditions on F and its expansion slope eta.',10:'It explicitly takes the approximating density from Eq. (1), with the parameters then specified in the theorem.',11:'It explicitly assumes Assumption 1, uniqueness of the KL projection.',12:'It explicitly assumes Assumption 2; its displayed parameters use that assumption’s abstract Delta, V and third-order array.',13:'It explicitly assumes Assumption 3 and uses its abstract log-prior expansion vector in xi.',15:'It explicitly assumes Assumption 4, the stated posterior contraction condition.'},
'4.1':{4:'Theorem 4.1 concerns the posterior Pi_n/pi_n and uses the original prior pi in its additional moment condition.',11:'It explicitly retains Assumption 1 on the projection parameter.',16:'It explicitly assumes Assumption 7, local smoothness and positive finite prior density.',17:'It explicitly assumes Assumption 8, uniform likelihood separation outside root-n neighborhoods.',18:'Its centering estimate theta-hat is the MAP defined at the start of Section 4.1.',19:'The theorem uses the root-n MAP-centered coordinate hat h from that section.',21:'Its approximating density is explicitly defined by Eq. (22), including the original covariance and cubic skewing factor.',22:'It explicitly assumes Assumption 9, the MAP proximity event.',23:'It explicitly assumes Assumption 10, the covariance and local derivative events.'},
'4.5':{11:'Theorem 4.5 imports the base assumptions of Theorem 4.1, including Assumption 1.',16:'That inheritance retains Assumption 7 on the prior.',17:'That inheritance retains Assumption 8 on likelihood separation.',18:'The inherited centering estimate is the MAP theta-hat.',19:'The marginal theorem uses blocks of the inherited root-n MAP-centered variable hat h.',22:'It inherits Assumption 9 on MAP proximity.',23:'It inherits Assumption 10 on covariance and local derivatives.',24:'Its d_C, selected coordinates and complement use the set C defined in Section 4.2.',28:'Its approximating density is explicitly Eq. (31), which is separately constructed for the marginal.',29:'Its target Pi_(n,C) is obtained from the true marginal posterior density defined immediately before the theorem.'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Preserve all three original main-text Theorems, numbered assumptions and literal source definitions. Separate general SKS, MAP-based joint and separately constructed marginal approximations.',build_order_policy='Derive same-paper paths from source definitions and explicit assumption references. Do not import sufficient conditions backwards or treat exact marginalization as the definition of Eq31.')
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
