"""Derive source-backed statement relationships for both general minimax Theorems."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'1':[11,12],'2':[11,12]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D4':{'D2':'N1 is asserted for P-almost everyxi in the operator-law space.','D3':'N1 integrates w against the conditional noise kernelnu(dw|xi).'},
'D5':{'D2':'N2 uses the same P-almost-everywhere operator-law quantifier.','D3':'N2 bounds the conditional quadratic form undernu(dw|xi).'},
'D6':{'D4':'Membership inP(Sigma_w) requires the first conditionN1.','D5':'Membership inP(Sigma_w) also requires the covariance-bound conditionN2.'},
'D7':{'D1':'After composing the law of(xi,w), the source generatesy by observation model1.','D2':'The first marginal ofP timesnu is the operator-index lawP.','D3':'The conditional law ofw givenxi isnu, so the product notation denotes a kernel composition.'},
'D9':{'D8':'The ellipseTheta bounds the norm induced byK_c inverse.'},
'D10':{'D1':'Admissible estimators observe only the pair(T_xi,y) in model1.'},
'D11':{'D6':'The risk supremum ranges over allnu inP(Sigma_w), the class defined byN1/N2.','D7':'Risk is averaged under the original kernel-composed joint lawP timesnu.','D8':'The loss is the squaredK_e norm of estimation error.','D9':'The unknown parameter ranges overTheta(varrho,K_c).','D10':'The infimum ranges over all measurable functions of the observed operator and response.'},
'D12':{'D2':'The expectation inPhi is overxi and hence over the distribution of the random operatorT_xi.','D8':'Phi uses the positive square roots ofK_e and inverse square roots ofK_c from the source norm geometry.'}}
REASONS={'1':{11:'Theorem1 bounds the original minimax riskM defined in3.',12:'Its upper bound is exactly the trace functionalPhi defined in5, with the same six arguments.'},'2':{11:'Theorem2 bounds the same minimax riskM at radiusvarrho.',12:'Its first bound evaluatesPhi at radiusvarrho/2 and its second compares this to one quarterPhi at the original radius.'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Preserve both original main-text Theorems and original operator, conditional-noise, matrix-norm and minimax definitions.',build_order_policy='Derive same-paper paths from the original statement definitions. Keep operator-law expectation outside deterministic supremum choices. Gaussian and conditional-linear proof restrictions do not narrow the original model or estimator class.')
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
