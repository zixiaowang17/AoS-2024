"""Build the census while preserving both synchronization models and their estimator fallbacks."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'1':[2,3,4],'2':[6,8,9],'3':[2,3,4],'4':[6,8,9]}
DIRECT={n:['D'+str(i) for i in ids] for n,ids in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'The unknown phase vector has unit-complex coordinates under the source C1 convention.'},
'D3':{'D1':'The estimator normalizes each coordinate to a unit complex number.','D2':'Its leading eigenvector is computed from the masked Hermitian data matrix, with completion retained in A1.'},
'D4':{'D1':'The loss minimizes over one global unit-complex multiplier a.'},
'D6':{'D5':'The unknown block parameters Z*_j are real orthogonal matrices.'},
'D7':{'D5':'The polar factor M V^T belongs to the real orthogonal group.'},
'D8':{'D5':'The block estimator returns orthogonal matrices and uses I_d on singular blocks.','D6':'It uses the top-d eigenvector matrix of the real block data matrix, retained with its completion in A2.','D7':'Nonsingular eigenvector blocks are normalized by the full-rank polar-factor map.'},
'D9':{'D5':'The printed loss minimizes over one orthogonal alignment O; its omitted sum/free j is separately recorded.'}}
def direct_reason(n,lid):
    if lid=='D2':return 'Theorem '+n+' bounds the phase estimator under the masked complex model (1), with p the edge probability and sigma the noise scale; A1 gives the Hermitian data completion.'
    if lid=='D3':return 'Theorem '+n+' concerns zhat from (4), the leading data eigenvector normalized coordinatewise, including the explicit value 1 on zero coordinates.'
    if lid=='D4':return 'Theorem '+n+' uses ell(zhat,z*), the averaged squared coordinate error minimized over one global phase in (5).'
    if lid=='D6':return 'Theorem '+n+' concerns the orthogonal synchronization model (20), with independent upper-triangle Bernoulli masks and standard real matrix-Gaussian noise; A2 retains its block completion.'
    if lid=='D8':return 'Theorem '+n+' bounds Zhat from (13): top-d eigenvectors, block polar normalization and identity on singular blocks. This does not require a first-order approximation as an estimator input.'
    if lid=='D9':return 'Theorem '+n+' uses ell^od(Zhat,Z*), whose original page-11 definition is retained in D9. That display has a free block index and omits the sum suggested by the stacked-matrix context A8; the census does not silently repair it.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All four complete main-text Theorems, retaining asymptotic and finite-sample statements separately for phase and orthogonal synchronization.',build_order_policy='Same-paper model, estimator and loss dependencies with original matrix completions; population approximations and perturbation lemmas are proof-only and do not add edges.')
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
