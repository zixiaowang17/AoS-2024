"""Derive source-backed theorem dependencies without importing supplementary bodies."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'2.1':[3,4],'2.2':[5,6],'4.1':[3,7],'5.1':[3,8,9,10,11,12,13],'5.2':[8,9,10,11,12,14]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'The transformed density pi_S is evaluated at x=SP(z), using the radius-indexed stereographic map.'},
'D3':{'D1':'Algorithm 1 maps x to SP inverse, makes its tangent proposal on the unit sphere, and returns SP of the normalized proposal.'},
'D5':{'D1':'Algorithm 2 evolves on the unit sphere and returns x=SP(z).','D2':'Its bounce hazard and tangent reflection use the gradient of log pi_S, whose original formula is Eq. (4).'},
'D13':{'D3':'Definition 5.1 takes expectation under the stationary SPS proposal law and uses the acceptance ratio printed in Algorithm 1.'},
'D14':{'D1':'Algorithm 4 maps the current point by SP inverse and maps both spherical proposals back by SP before splicing coordinates.'}}
REASONS={
'2.1':{3:'Theorem 2.1 names SPS, the transition defined by the full proposal and acceptance steps of Algorithm 1.',4:'Its conclusion uses the preceding discrete-time definition of uniform ergodicity, with a common N for all starting states.'},
'2.2':{5:'Theorem 2.2 names SBPS, defined by the great-circle flow, bounce and constant-refresh steps of Algorithm 2.',6:'Its conclusion uses the preceding continuous-time semigroup definition of uniform ergodicity, with a common time T for all starting states.'},
'4.1':{3:'Theorem 4.1 evaluates the stationary acceptance probability under the ordinary SPS proposal with scale h; Section 4.2 explicitly studies SPS robustness.',7:'Its target pi_(mu,Sigma), means mu_i and eigenvalues lambda_i are those of the diagonal-covariance Gaussian class defined immediately above the theorem.'},
'5.1':{3:'Theorem 5.1 explicitly assumes the SPS chain is in its stationary phase, using the original Algorithm 1.',8:'Its reference to Section 5.1 includes the product target pi(x)=product_i f(x_i) in Eq. (12).',9:'That reference includes the normalized second moment and finite sixth moment in Eq. (13).',10:'That reference includes the Lipschitz score, derivative boundary limit and all three integrability bounds in Eq. (14).',11:'Section 5.1 additionally specifies that f has full support in R, after Remark 5.1.',12:'The theorem explicitly reparameterizes h by ell according to Eq. (15) with lambda=1.',13:'Its ESJD is the exact joint expectation in Definition 5.1, displayed immediately before the theorem.'},
'5.2':{8:'Theorem 5.2 explicitly imports the Section 5.1 product target pi(x)=product_i f(x_i).',9:'The imported Section 5.1 assumptions include Eq. (13): second moment one and finite sixth moment.',10:'Those assumptions include Eq. (14), the Lipschitz score and the stated derivative boundary limit.',11:'The same section specifies full support for f in R after Remark 5.1.',12:'The speed s(ell) uses the continuing section convention defining ell through Eq. (15); R=sqrt(d) selects lambda=1. The printed theorem does not repeat that equation reference.',14:'The theorem explicitly concerns the RSPS chain, whose two-proposal coordinate splice is printed in Algorithm 4, rather than the original SPS chain.'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Preserve all five original main-text Theorems and source terminology. Keep SPS, SBPS and RSPS distinct, and preserve exact ESJD separately from its approximation.',build_order_policy='Derive same-paper paths from original definitions, explicit assumptions and recorded section conventions. Exclude proof-only supplementary references and conjectured extensions.')
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
