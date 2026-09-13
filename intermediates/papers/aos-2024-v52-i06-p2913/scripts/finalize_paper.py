"""Derive source-backed statement relationships for all three irregular-signal Theorems."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'3.1':[3,4,6,23],'3.2':[2,4,7,11,22,24,25],'3.3':[2,4,5,7,18,22,25,26]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D1':{'D2':'Model (1) explicitly requires the positive finite two-sided long-run variance in (2).'},
'D3':{'D1':'The constant-signal null is imposed on the means in model (1).'},
'D4':{'D1':'The one-sided irregular alternative is imposed on the means in model (1).'},
'D5':{'D2':'Consistency is for the long-run variance defined by the covariance sum in (2).'},
'D6':{'D1':'The minimum CUSUM statistic uses the observed signal-plus-noise data and their sample mean.','D5':'The denominator in (5) uses a consistent long-run standard deviation estimate; the specific estimator (8) is optional.'},
'D7':{'D1':'The nonoverlapping block means average the observations from model (1).'},
'D8':{'D7':'The preliminary index minimizes the block averages in (6), and its endpoint is the index multiplied by block size.'},
'D9':{'D1':'The preliminary mean averages observations from model (1).','D8':'The averaging prefix ends at the selected endpoint ell_hat in (7).'},
'D10':{'D1':'The sliding average uses observations from model (1).','D7':'The source extends the original block averages and retains their block size k.'},
'D11':{'D2':'Estimator (8) targets the original long-run variance.','D8':'Its sliding-window endpoints and normalization use the selected prefix endpoint ell_hat.','D9':'Each window is centered by the preliminary prefix mean muhat_0.','D10':'The sum uses overlapping averages R_(s/k), including noninteger s/k.'},
'D13':{'D5':'The user may choose any consistent variance estimator in standardized statistic (9).','D7':'Each statistic standardizes an original block average and uses the square root of its block size.','D9':'The block average is centered by the preliminary prefix mean muhat_0.'},
'D14':{'D7':'The cutoff level is 1-1/m, where m is the number of blocks.','D12':'The threshold is the original standard-normal quantile z_(1-1/m).','D13':'The decision compares standardized block statistic Dhat_j to that threshold with an inclusive inequality.'},
'D15':{'D7':'The candidate coarse change points and sums are indexed by the original block count m.','D14':'The binary step fit minimizes squared errors for the decisions Ihat_j from (9).'},
'D16':{'D1':'The improved prefix mean averages the original observations.','D7':'The data prefix length is block size k times the estimated block index.','D15':'The estimated coarse block index eta_hat determines the prefix endpoint in (11).'},
'D17':{'D1':'The estimated gap uses the observed data from model (1).','D7':'The sliding averages have the original block size k.','D15':'The lower endpoint of the search window uses eta_hat from the binary step fit.','D16':'The noisy windows are centered by the improved prefix mean muhat_1.'},
'D18':{'D1':'The final cumulative criterion sums the original observed data through j-1.','D16':'The criterion subtracts the improved prefix mean muhat_1.','D17':'The criterion also subtracts rho times the estimated sliding-block gap dhat.'},
'D20':{'D19':'The coupled output replaces only the time-zero IID innovation in the original causal filter representation.'},
'D21':{'D20':'The cumulative dependence coefficient sums the original single-innovation Ltheta coupling coefficients.'},
'D22':{'D19':'Condition 3.1 concerns the causal stationary noise process from (13).','D21':'Its alternative decay regimes constrain the cumulative functional dependence coefficient Theta_(n,theta).'},
'D23':{'D21':'Theorem 3.1 requires the n=0, theta=2 instance of cumulative functional dependence to be finite.'},
'D24':{'D4':'Tau is the first changed observation in alternative (4).','D7':'The source defines eta using tau divided by the original block size k.'},
'D25':{'D4':'The n-dependent d and tau are expressly those from alternative (4).','D7':'The rate context expressly retains the user-chosen block size k and count m.','D24':'The rate context repeats the original eta=floor(tau/k) convention.'},
'D26':{'D4':'The population averaged gap uses the post-change signal means relative to mu_1 in alternative (4).','D7':'The signal windows have the original block size k.','D24':'The first allowed signal window begins at k*(eta+1)+1 with the true block index eta.'}}
REASONS={
'3.1':{3:'Part (i) of Theorem 3.1 is under the constant-mean null H0 in (3).',4:'Part (ii) is under H1 in (4), and its signal condition uses that alternative\'s d and first-change index tau; this is a separate branch from part (i).',6:'Both conclusions concern the minimum CUSUM statistic T_hat in (5), including its arbitrary consistent variance estimate.',23:'The common premise is explicitly the short-range summability condition (16), not the stronger locating Condition 3.1.'},
'3.2':{2:'The target in the variance expansion is the positive finite long-run variance sigma_infinity² in (2).',4:'The n-dependent signal gap d and first-change index tau in the premises are bound by the immediately preceding reference to alternative (4).',7:'The theorem imposes lower and upper rates on the original block length k.',11:'The quantity sigmahat² in the conclusion is expressly the particular overlapping-block estimator defined in (8).',22:'Theorem 3.2 explicitly assumes Condition 3.1 with the same theta appearing in its signal, block and error rates.',24:'The random error rate uses eta, the true block index floor(tau/k) defined in the main text.',25:'The preceding paragraph defines the little-o meaning of the double inequalities and permits d and tau to depend on n.'},
'3.3':{2:'The theorem explicitly identifies sigma_infinity² as the long-run variance targeted by the chosen estimate.',4:'The premises use the alternative\'s gap d and first-change index tau, including the strict comparison d>K*d_star.',5:'The theorem expressly permits the variance estimator used in (9) provided it is consistent; it does not force the specific formula (8).',7:'The block size k appears in both rate inequalities and n-tau>=2k.',18:'The conclusion concerns tau_hat from (12), and the premise K>rho refers to that estimator\'s tuning parameter.',22:'Theorem 3.3 expressly assumes the complete Condition 3.1, with the same theta throughout.',25:'The double inequalities retain the original little-o meaning and n-dependent signal conventions.',26:'The premise d>K*d_star and the localization rate both use the population averaged gap defined immediately before the theorem in (20).'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Preserve all three original main-text Theorems and the original irregular-signal hypotheses, dependence conditions and estimation algorithms.',build_order_policy='Derive same-paper paths from original source definitions. Preserve separate null and alternative branches, arbitrary versus specific variance estimates, true versus estimated block indices, and pointwise versus averaged signal gaps. Proof machinery and optional defaults are not extra premises.')
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
