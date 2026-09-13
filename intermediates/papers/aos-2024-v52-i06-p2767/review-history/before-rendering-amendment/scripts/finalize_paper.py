"""Derive source-backed theorem dependencies without importing supplementary bodies."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'4.5':[1,4,5,9,10,11,12],'4.6':[1,4,5,10,11,12,13],'5.2':[5,14],'5.5':[5,14,15],'6.2':[1,5,16,17],'6.3':[5,9,10,18],'6.4':[1,5,15],'6.5':[5,15,19],'7.1':[4,20],'7.2':[4,21],'7.3':[6,22,23]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D4':{'D1':'Definition1.1 measures uniform error using the original normalized total variation distance.'},
'D5':{'D1':'The infimum-supremum defining epsilon-star uses the same normalized TV discrepancy.'},
'D6':{'D4':'The defining prose describes the largest additional sample size admitting an amplification procedure.','D5':'The printed maximum is over sample sizes whose minimax error epsilon-star is at most the target epsilon.'},
'D8':{'D7':'Algorithm1 computes a sufficient statistic and uses its parameter-independent conditional generation kernel.'},
'D9':{'D7':'Definition4.3 names T(x) as the sufficient statistic of the natural exponential family.'},
'D10':{'D9':'Assumption1 concerns the parameter set Theta and the law of T(X) from Definition4.3.'},
'D11':{'D9':'Assumption2 standardizes that family’s statistic using the gradient and Hessian of its log-partition function.'},
'D12':{'D7':'The averaged T_n is explicitly described as a sufficient statistic.','D8':'The last sentence specifies Algorithm1 with the identity map between sample sizes.','D9':'The iid observations and statistic T are from the natural exponential family in Definition4.3.'},
'D13':{'D9':'Every coordinate factor is a one-dimensional exponential family in the original natural-family sense.','D15':'The joint law is the product of the separate coordinate families.'},
'D14':{'D3':'Definition5.1 averages the original asymmetric chi-squared divergence with estimator first and truth second.'},
'D17':{'D7':'The sample mean is the sufficient statistic used in Example4.1.','D8':'That example explicitly instantiates Algorithm1 with an identity transformation.','D16':'The sample and conditional generation law belong to the unknown-mean known-covariance Gaussian family.'},
'D18':{'D9':'Assumption3 imposes its linear-independence condition on the statistic T under the base measure mu of Definition4.3.'},
'D19':{'D2':'The coordinate-pair condition uses the square of the original normalized Hellinger distance.','D15':'Its reference to Theorem6.4 imports the product family and its coordinate parameter spaces.'},
'D23':{'D22':'P_c is a subclass of the same L-Lipschitz probability densities, with an additional pointwise lower bound.'}}
REASONS={
'4.5':{1:'Theorem4.5 explicitly compares the laws of T_n and T_(n+m) in the source TV distance.',4:'Its final sentence asserts existence of a sample amplification procedure of the stated size.',5:'Its first quantity is the minimax amplification error epsilon-star defined in(4).',9:'It explicitly takes an exponential family as defined in Definition4.3.',10:'It explicitly assumes Assumption1 on the natural parameter set and the law of the statistic.',11:'It explicitly imposes Assumption2 with k=3 on the full statistic.',12:'Its T_n and T_(n+m) are the average sufficient statistics defined immediately before the theorem, used with the identity map.'},
'4.6':{1:'Theorem4.6 explicitly uses TV between the average-statistic laws.',4:'Its final clause asserts an(n,n+m,epsilon) amplification procedure.',5:'It bounds the same minimax error epsilon-star.',10:'Its Assumption1 is imposed on each one-dimensional component, not merely on an arbitrary observation density.',11:'Its Assumption2 is imposed componentwise with k=10, distinct from k=3 in4.5.',12:'The statistic T_n is the average statistic and identity-map construction introduced in Section4.3.',13:'It explicitly requires the product exponential family introduced immediately before the theorem.'},
'5.2':{5:'Theorem5.2 bounds the minimax amplification error epsilon-star for a general model class.',14:'Its RHS is the expected chi-squared minimax estimation error at sample size n/2 defined in5.1.'},
'5.5':{5:'Theorem5.5 bounds epsilon-star for the full product model.',14:'The sum uses Definition5.1 separately on each coordinate class P_j at n/2.',15:'The theorem explicitly assumes P is the Cartesian product of its coordinate families.'},
'6.2':{1:'The exact RHS is TV between two centered Gaussian laws with identity covariance scaled by sample size.',5:'The LHS is explicitly the minimax error from(4).',16:'The theorem specifies the unknown-mean Gaussian location family with fixed known Sigma.',17:'The final sentence explicitly asserts optimality of the particular sufficiency-based procedure in Example4.1.'},
'6.3':{5:'Theorem6.3 gives a lower bound on the original epsilon-star.',9:'It explicitly takes a d-dimensional natural exponential family.',10:'It retains Assumption1 on the parameter set and absolutely continuous sufficient-statistic law.',18:'It explicitly assumes the source linear independence condition3; Section6.1 drops moment Assumption2.'},
'6.4':{1:'Its two inline coordinate-pair hypotheses use normalized TV at sample sizes n and n+m.',5:'Its conclusion lower-bounds epsilon-star for the joint model.',15:'It explicitly assumes a product law with a Cartesian product parameter space.'},
'6.5':{5:'Theorem6.5 bounds epsilon-star at the ceiling-rounded additional sample size.',15:'It explicitly requires a product model.',19:'It explicitly assumes Assumption4, the per-coordinate Hellinger-scale pair condition for the given n.'},
'7.1':{4:'Theorem7.1 asks whether an(n,n+1,0.1) amplification procedure exists in the Definition1.1 sense.',20:'The class P_(d,t) is the original discrete model with known mass p0=t defined immediately above.'},
'7.2':{4:'Theorem7.2 states existence of an(n,n+1,0.1) amplification procedure.',21:'Its above low-rank covariance model is the isotropic rank-d projection-covariance Gaussian family in Section7.2.'},
'7.3':{6:'Theorem7.3 uses m-star(P,n), the maximal additional sample count at the source small fixed error.',22:'Its second rate concerns the base L-Lipschitz density class on[0,1].',23:'Its first rate concerns the distinct subclass P_c with density bounded below by c everywhere.'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Preserve all eleven original main-text Theorems and original source definitions, assumptions and distinct model classes.',build_order_policy='Derive same-paper paths from the original statement definitions. Keep proof-only algorithms, decision risks and sufficient moment criteria separate from required assumptions.')
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
