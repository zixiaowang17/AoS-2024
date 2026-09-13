"""Derive source-backed theorem dependencies without importing supplementary bodies."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'2.7':[1,2,3,4,6,9],'2.9':[1,2,3,4,7,8,9,10],'2.12':[1,2,3,4,9,11],'3.2':[2,3,4,12,15,16,17,18,19,20],'3.5':[2,3,4,12,15,16,17,18,19,20,21],'3.8':[3,12,15,20,21,22,23,24],'3.9':[2,3,12,15]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D3':{'D1':'Assumption2.2 centers the components and bounds the total mean f0 of model(2.2).'},
'D4':{'D1':'Assumption2.3 imposes its original Holder smoothness on the univariate and bivariate components of that mean.'},
'D6':{'D5':'Equations(2.4)–(2.5) instantiate the generic architecture class with separate component-sum structure and depth-dependent sizes.'},
'D7':{'D5':'Equations(2.7)–(2.8) instantiate the same architecture notation with constant depth and revised widths and weight counts.'},
'D8':{'D3':'The estimator clips its output to B using the total-mean bound in Assumption2.2.','D7':'For Theorem2.9, Section2.2 revises the class symbols in estimator(2.3) to the constant-depth versions(2.7)–(2.8).'},
'D9':{'D4':'The dense growth condition uses beta1 and beta2, the source component smoothness indices clarified in Remark2.5.'},
'D10':{'D1':'The training sample S_n consists of the observed input-response pairs from the two-way model.'},
'D11':{'D1':'The supremum ranges over two-way additive-interaction mean functions.','D4':'Its component class Sigma(beta,L) explicitly refers to Assumption2.3.'},
'D12':{'D4':'The definition of F_sp expressly retains beta1-smooth univariate and beta2-smooth bivariate components under the original smoothness convention.'},
'D13':{'D5':'Equations(3.2)–(3.3) instantiate F_NN for input dimension1 and2, with their own constant depths and sizes.'},
'D14':{'D12':'The approximant sum uses the original active sets, component means and smoothness of sparse model(3.1).','D13':'Its component witnesses are required to lie in the classes F_NN,1 and F_NN,2.'},
'D15':{'D12':'Assumption3.1 uses sparsities s1,s2 and smoothness indices of the sparse model, not the dense dimension count.'},
'D17':{'D12':'Bound(3.6) applies to each original univariate and bivariate mean component in the sparse setting.'},
'D18':{'D13':'Its global minimization ranges over the component network classes(3.2)–(3.3).','D16':'The group penalty sums empirical L2 norms of the component functions.','D17':'The adjacent source convention truncates the component networks at B.'},
'D19':{'D12':'The component approximation errors refer to the sparse mean components and their two smoothness indices.','D13':'Those components are approximated by the separate network classes used in the estimator.'},
'D20':{'D13':'The complexity expressions V_n,1 and V_n,2 use the size parameters of the component network architectures.'},
'D21':{'D12':'RSC separates the active sets S1,S2 from their complements and uses their cardinalities.','D14':'The deviations are measured from the original approximants and sum phi-star in(3.4).','D16':'Both its cone and curvature inequalities use the empirical L2 norm.','D19':'Its cone includes the original component approximation slack rho_n,1 and rho_n,2.','D20':'Both the cone and its squared-penalty slack use the prescribed lambdas from(3.7).'},
'D22':{'D12':'Minimal signal strength is imposed on the active components and uses their sparse cardinalities and smoothness indices.'},
'D23':{'D13':'The refit minimizes unpenalized squared loss over the original component network classes.','D16':'The estimated active sets threshold empirical L2 norms of the initial component fits.','D18':'Step2 fits the initial components on D1 by the penalized procedure(3.5).','D20':'The algorithm inputs and thresholds use the penalty choices specified by(3.7) when invoked by Theorem3.8.'},
'D24':{'D2':'Section3.2 expressly requires the random covariates to have distribution satisfying Assumption2.1.'}}
REASONS={
'2.7':{1:'Theorem2.7 explicitly concerns the two-way model(2.2).',2:'Its expectation uses the design distribution fixed by the standing Assumption2.1 in Section2.',3:'Section2.1 explicitly recalls the zero component marginals from Assumption2.2 before stating this approximation theorem.',4:'The theorem explicitly requires beta1-smooth univariate and beta2-smooth bivariate components, with the convention from Assumption2.3.',6:'It explicitly uses F_NN^1 and F_NN^2 from(2.4)–(2.5), including their original depth dependence.',9:'Section2.1 adopts Assumption2.6 immediately before Theorem2.7; this is recorded as section context, although the theorem body does not repeat it.'},
'2.9':{1:'Theorem2.9 estimates f0 in the stated two-way model.',2:'Its Assumption2.1 supplies the design-density and noise bounds.',3:'Its Assumption2.2 supplies the original centering and total-mean boundedness.',4:'Its Assumption2.3 supplies component smoothness.',7:'The F_NN classes used by the estimator have been explicitly revised in Section2.2 to(2.7)–(2.8).',8:'It explicitly invokes the ERM estimator defined by(2.3), including final clipping.',9:'It explicitly assumes the dense growth condition2.6.',10:'Its conditional expectation is given the training sample S_n defined on10.'},
'2.12':{1:'Theorem2.12 explicitly concerns model(2.2) and its component mean class.',2:'It explicitly assumes2.1 on design and errors.',3:'It explicitly assumes2.2 on identifiability and boundedness.',4:'It explicitly refers to Sigma(beta,L) and Assumption2.3.',9:'The opening paragraph of Section2.3 expressly retains Assumption2.6 and growing d=o(n) for this minimax problem.',11:'Its target M(n,d,F) is the minimax risk defined immediately above the theorem.'},
'3.2':{2:'Theorem3.2 explicitly assumes2.1, despite the fixed-design context of Section3.1.',3:'It explicitly retains Assumption2.2.',4:'It explicitly retains Assumption2.3 on component smoothness.',12:'Its target f0 and sparsities s1,s2 are those of sparse model(3.1).',15:'It explicitly assumes the sparse growth condition3.1.',16:'The conclusion is measured using the source empirical norm ||.||_n.',17:'It explicitly requires component bound(3.6).',18:'It explicitly invokes the penalized estimator(3.5).',19:'Its continuation on15 defines component approximation errors and refers to their bounds(3.8).',20:'The continuation explicitly prescribes both lambdas and both V expressions in(3.7).'},
'3.5':{2:'Theorem3.5 inherits Assumption2.1 through the hypotheses of3.2.',3:'It inherits Assumption2.2 through3.2.',4:'It inherits Assumption2.3 through3.2.',12:'Its f0,s1,s2 refer to the original sparse model.',15:'It inherits Assumption3.1 through3.2.',16:'Its rate is stated in the empirical L2 norm.',17:'It inherits the component bound(3.6) through3.2.',18:'The estimator is explicitly defined by(3.5), despite the phi-hat/f-hat change in notation.',19:'Its rho terms are the component approximation errors defined in3.2.',20:'The inherited penalty choices are exactly(3.7).',21:'It additionally requires Assumption3.4, the full approximate-cone RSC condition.'},
'3.8':{3:'Section3.2 continues the same sparse interaction model and its standing identifiability/boundedness convention2.2; this is section context rather than a repeated theorem hypothesis.',12:'The target f0 and sparsities belong to the original sparse mean class.',15:'Section3 adopted Assumption3.1 before dividing the analysis into its three subsections; its growth scope is recorded separately from the abbreviated theorem body.',20:'The theorem expressly uses lambdas from3.5, which resolves to their definitions in(3.7).',21:'It explicitly assumes that Assumption3.4 holds with high probability on the random design sample.',22:'It explicitly assumes the minimal-signal condition3.7.',23:'The preceding sentence identifies its f-hat-final as the estimator returned by Algorithm1.',24:'Theorem3.8 belongs to Section3.2, whose original setup specifies random covariates under2.1 and population prediction loss.'},
'3.9':{2:'Theorem3.9 explicitly assumes2.1.',3:'It explicitly assumes2.2.',12:'It explicitly takes observations from model(3.1) and a supremum over its class F_sp.',15:'Section3 adopted the sparse growth condition3.1 before its three subsections; retain this standing context separately, without inserting it into3.9 original text or importing RSC.'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Preserve all seven original main-text Theorems, source assumptions and network/model definitions; rank all statement uses.',build_order_policy='Use source-local definition paths, explicit theorem references and recorded section conventions. Separate the two architecture versions, dense/sparse regimes and empirical/population losses.')
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
