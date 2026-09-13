"""Build the nine-Theorem census from source-specific local dependency decisions."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'2.1':[1,2],'2.2':[3,4,5,7,8],'2.3':[3,4,5,7,8],'3.1':[3,5,8,9,10,11,13],'3.2':[3,5,10,11,13,14],'3.3':[3,5,9,10,11],'3.4':[5,10,11,12,15,16],'3.5':[5,10,11,12,15,16,17],'5.1':[1,2]}
DIRECT={n:['D'+str(i) for i in ids] for n,ids in DIRECT_NUMS.items()}
EDGE_TEXT={
 'D2':{'D1':'Its singular decompositions and leading-vector matrices are defined for the two matrices Y and Y-hat in (1).'},
 'D4':{'D3':'The columns X_i, signal centers and noise vectors are those of the mixture model (6).'},
 'D5':{'D3':'The minimum cluster size counts the mixture assignment labels z_i*.'},
 'D6':{'D4':'X_{-i} is formed by deleting column i from the mixture data matrix X.'},
 'D7':{'D4':'The full empirical SVD is that of the matrix X=P+E.','D6':'The second SVD and U-hat_{-i,1:r} use the leave-one-out matrix X_{-i}.'},
 'D8':{'D4':'Lambda_j and kappa are the singular values and rank of the signal matrix P.'},
 'D9':{'D4':'Algorithm 1 decomposes the observed data matrix X and clusters projections of its columns.'},
 'D10':{'D3':'The loss compares a label vector with the true assignment z* in the mixture model.'},
 'D11':{'D3':'Delta is the minimum Euclidean distance between the mixture centers theta_a*.'},
 'D13':{'D12':'Vector SG_d requires the scalar SG condition for u^T X in every unit direction.'},
 'D14':{'D4':'Algorithm 2 uses the SVD of X from Algorithm 1 step 1, retained in A3, then its own selected-rank clustering step.'},
 'D15':{'D3':'Equation (28) explicitly specializes the mixture model (6) to two opposite centers with iid noise entries.'},
 'D16':{'D4':'The projection in (29) uses X_i and the leading empirical singular vector of X, with SVD convention A3.','D15':'Equation (29) is the two-cluster estimator for the model (28).'},
 'D17':{'D11':'The imported Lemma 3.4 assumptions require the center separation Delta to be constant.','D15':'Its density f belongs to the noise distribution F in model (28).'}}
def direct_reason(n,lid):
    if lid=='D1':return 'The formula uses the appended column y_n from the arbitrary-matrix pair (1), with no mixture-model restriction.'
    if lid=='D2':return 'The formula uses sigma_r, sigma_i, u_i and the projection matrices formed from U_r and U-hat_r in the ordered SVD setup of Section 2.1.'
    if lid=='D3':return ('The projection term uses the noise epsilon_i from mixture model (6), and k counts its centers; no noise distribution is imposed in this deterministic theorem.' if n in ['2.2','2.3'] else 'The epsilon_i hypotheses and target assignment z* refer to the mixture model (6); the noise distribution and independence are imposed separately in this theorem.')
    if lid=='D4':return 'The denominator uses the norm of the noise matrix E from the decomposition X=P+E in (7).'
    if lid=='D5':return ('Theorem 3.5 imports beta*n>40 from Theorem 3.4; beta is the normalized minimum cluster size on page 6.' if n=='3.5' else 'The cluster-size hypothesis explicitly uses beta, defined on page 6 by the minimum number of observations assigned to a cluster.')
    if lid=='D7':return 'The left side and noise projection use the empirical full-data and leave-one-out singular-vector matrices defined on page 7, instantiated at '+('r=kappa.' if n=='2.2' else 'the r selected in (11).')
    if lid=='D8':return ('The estimator is run at r=kappa and (22) uses lambda_kappa, the rank and smallest nonzero singular value of the signal P.' if n=='3.1' else 'The spectral-gap ratio uses the population signal singular values lambda_j, and '+('its rank kappa.' if n=='2.2' else 'the selected indices r and r+1.'))
    if lid=='D9':return 'The theorem explicitly specifies Algorithm 1 for z-hat, with '+('r=kappa.' if n=='3.1' else 'r=k.')
    if lid=='D10':return ('Theorem 3.5 names the minimax rate (31), whose expectation uses ell from page 9; the exact rate is retained in A6.' if n=='3.5' else 'The risk is the expectation of ell applied to the stated clustering estimate and z*, using the original page-9 loss definition with its separately recorded indicator-sign discrepancy.')
    if lid=='D11':return ('Theorem 3.5 imports the separation ratio from Theorem 3.4 and the fixed-Delta assumption and rate (31) from Lemma 3.4; Delta is the minimum center distance.' if n=='3.5' else 'The rate and separation condition use Delta, the minimum distance between centers defined on page 9.')
    if lid=='D12':return ('Theorem 3.5 imports the scalar noise restriction xi~SG(sigma^2) from Theorem 3.4, retained in A5.' if n=='3.5' else 'The noise variable xi is explicitly required to satisfy the scalar SG(sigma^2) condition from Notation; its actual variance is separately bar-sigma squared.')
    if lid=='D13':return 'The hypothesis epsilon_i~SG_p(sigma^2) uses the directional vector condition in Notation; the theorem additionally states independence and zero mean.'
    if lid=='D14':return 'Theorem 3.2 explicitly uses the estimator z-tilde from Algorithm 2 and constrains its input threshold T through rho_2.'
    if lid=='D15':return 'The theorem opens with model (28), the two-cluster symmetric specialization with iid scalar noise entries from F.'
    if lid=='D16':return 'The statement concerns check-z, the exact two-means estimator on the leading empirical singular projection defined in (29).'
    if lid=='D17':return 'Theorem 3.5 explicitly imports Lemma 3.4 assumptions: a positive continuously differentiable mean-zero density with finite Fisher information and fixed Delta; its referenced rate (31) uses that information.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All nine main-text Theorems, including the main-text proof-section Theorem 5.1; original source terms and conditions remain separate.',build_order_policy='Same-paper source dependencies. Imported construction subparts and unnamed formulas are retained as auxiliary passages and expanded only within their stated scope.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGE_TEXT.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=DIRECT[n]
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                ev=copy.deepcopy(c['evidence'])+copy.deepcopy(members[lid]['evidence'])
                if n=='3.5':ev.append(dict(page=16,location='Theorem 3.4 hypotheses and local ratio psi_3 imported by Theorem 3.5'))
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
            if n=='3.5':ev.append(dict(page=16,location='Imported Theorem 3.4 assumptions and original psi_3 formula'))
            if 'D14' in path or 'D16' in path:ev.append(dict(page=8,location='Algorithm 1 Step 1 only, preserved in A3'))
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
