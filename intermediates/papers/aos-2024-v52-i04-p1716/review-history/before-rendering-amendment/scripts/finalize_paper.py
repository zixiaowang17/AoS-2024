"""Build the census from the reviewed source graph without modifying the inventory."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
1:{'D4':'Assumption 1 includes the temporal linear-process and operator-summability conditions in part (i).',
   'D5':'Assumption 1 also includes the limiting covariance and moment conditions in part (ii).',
   'D6':'The null limit explicitly uses the eigenvalues defined in (2.7).',
   'D7':'Part (i) is stated under the no-break null H0 defined in (2.2).',
   'D12':'Part (ii), equation (3.11), concerns the PE component Z-diamond_NT itself.',
   'D13':'The distributional limit and final consistency statement use the combined statistic Z-hat_NT.',
   'D14':'Part (ii) distinguishes H-diamond_A from the enlarged alternative H-tilde-diamond_A.'},
2:{'D1':'Conditions (4.2) and (4.4) use the source L2 norm of each jump function.',
   'D3':'The signal conditions use the model jump delta_i and break location tau_i through omega_Ti.',
   'D4':'The theorem explicitly assumes part (i) of Assumption 1 as part of the full assumption.',
   'D5':'The full Assumption 1 also requires part (ii) on moments and the limiting covariance.',
   'D11':'The signal-to-threshold ratio in (4.2) uses the prescribed xi_NT.',
   'D15':'The minimum and maximum range over the true broken-subject set C-bullet, and (4.3) targets both true sets.',
   'D16':'Equation (4.3) asserts equality of both estimated threshold sets with their true counterparts.',
   'D17':'The additional branch bounds the error of the per-subject CUSUM argmax tau-hat_i.'},
3:{'D4':'Theorem 3 explicitly assumes the full Assumption 1, including its linear-process part.',
   'D5':'Its Assumption 1 citation includes the moment and covariance conditions in part (ii).',
   'D18':'The statement explicitly requires the latent structure (4.6).',
   'D21':'The two conclusions concern K-hat and the estimated groups C-hat(b_k) defined by the penalised criterion.',
   'D22':'The full Assumption 2 includes proportional distinct break locations and group sizes in part (i).',
   'D23':'The full Assumption 2 includes the uniform mean/jump norm restrictions in part (ii).',
   'D24':'The full Assumption 2 includes the tuning-sequence restrictions in part (iii).'},
4:{'D1':'The signal condition (4.14) sums squared L2 norms of jump functions.',
   'D3':'Those jump functions delta_i belong to the original subject-level break model.',
   'D4':'Assumption 1(i) defines eta_it and the error process; Theorem 4 additionally imposes independence over subjects i.',
   'D5':'The stated full Assumption 1 includes its second part on moments and limiting covariance.',
   'D15':'The two growth conditions and the joint limit use the number of truly broken subjects |C-bullet|.',
   'D18':'Theorem 4 requires the latent structure (4.6), whose groups and break locations enter (4.14) and (4.15).',
   'D22':'The theorem expressly cites only part (i) of Assumption 2.',
   'D25':'The exact-recovery conclusion concerns the pooled CUSUM maximizer b-hat_k defined in (4.13).'}}
EDGES={
'D2':{'D1':'The operators, adjoint and operation norm are defined on the source Hilbert space.'},
'D3':{'D1':'The standing model observations and mean functions live in the source real function space.'},
'D4':{'D1':'The innovations are random elements of H with mean zero.','D2':'The coefficients are continuous linear operators and their operator norms occur in the summability condition.'},
'D5':{'D4':'The second part uses the innovations eta_it and coefficient operators A_ij defined in part (i).','D2':'It forms operator sums and quantifies over sequences of continuous linear operators B_i.','D1':'Its exponential moment and random-element moment use the source function-space norm, with the printed O subscript noted separately.'},
'D6':{'D5':'The eigenpairs belong to the limiting positive definite integral operator in (2.5).'},
'D7':{'D3':'The null and alternative are expressed through the subject-specific jump functions delta_i.'},
'D8':{'D3':'The averaged observations and mean paths are formed from the model X_it=mu_i+delta_i I(t>tau_i)+epsilon_it.'},
'D9':{'D8':'Its partial sums use the cross-subject averaged observations X-tilde_t.','D1':'Its squared-integral criterion is the source L2 norm over the bounded function domain.'},
'D10':{'D3':'The subject-specific partial sums are formed from the observed X_is in the model.','D1':'The CUSUM is a function on the standing source domain with the inherited L2 structure.'},
'D12':{'D10':'The count tests the integrated square of each subject-specific CUSUM.','D11':'Its strict threshold comparison uses the prescribed xi_NT.'},
'D13':{'D9':'The combined test contains the aggregated CUSUM statistic Z_NT.','D12':'Its second summand is the PE component Z-diamond_NT.'},
'D14':{'D7':'Both regions restrict the original alternative HA.','D8':'The enlarged region uses the averaged deterministic mean path nu-tilde_t.','D11':'The maximum signal condition divides by xi_NT.','D1':'Its signal condition uses the L2 norm of delta_i and its mean-path condition uses a squared integral.'},
'D15':{'D3':'The true partition is determined by whether the model jump delta_i is zero.'},
'D16':{'D10':'The estimated partition thresholds the integrated squared subject CUSUM.','D11':'It compares that quantity with xi_NT, using >= for the detected set.'},
'D17':{'D10':'The individual break estimate maximizes the integrated squared subject CUSUM.','D16':'The source defines it only for members of the estimated broken-subject set.'},
'D18':{'D15':'The latent partition covers the true broken-subject set.','D3':'Each part is defined by equality of the model break locations tau_i to b_k.'},
'D19':{'D17':'Clustering sorts the estimated individual break locations and their adjacent gaps.','D16':'Only subjects in the estimated broken-subject set are sorted and assigned.'},
'D21':{'D19':'The fitted means, residual sum and final group labels use the candidate clusters from (4.7).','D17':'Its within-cluster average break location averages the individual tau-hat_i.','D3':'The fitted pre/post-break means and residuals use the model observations X_it.','D16':'The residual average is normalized by the estimated number of broken subjects.','D1':'The residual criterion uses the squared source L2 norm.','D24':'The criterion definition explicitly says that rho_NT satisfies restrictions and refers to Assumption 2(iii).'},
'D22':{'D18':'The proportional locations and sizes are imposed on the true latent groups and their b_k.','D15':'The group-size formula is proportional to the cardinality of the true broken-subject set.'},
'D23':{'D1':'The restriction is expressed through source L2 norms.','D3':'The bounded functions are the model mean mu_i and jump delta_i.','D15':'The positive lower jump bound ranges over the true broken-subject set.'},
'D25':{'D21':'The pooled estimator uses C-hat(b_k) from the selected penalised clustering construction, not oracle groups.','D10':'Within each estimated group it sums the integrated squared subject CUSUMs.'}}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All four source Theorems; distinguish explicit assumptions, estimator-construction dependencies and ambient notation.',build_order_policy='Topological ordering of source-backed local definition dependencies.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGES.get(lid,{})),lid
    for c in data['claims']:
        n=int(c['claim_id'].split('/T')[-1]);c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            m=x['members'][0];lid=m['local_id']
            if lid in DIRECT[n]:x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']+m['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for rel in x['related_theorems']:
            cid=rel['claim_id'];n=int(cid.split('/T')[-1]);path=rel['via_local_ids']
            text=' '.join([DIRECT[n][path[0]]]+[EDGES[a][b] for a,b in zip(path,path[1:])])
            ev=copy.deepcopy(claims[cid]['evidence'])
            for lid in path:ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=text,evidence=ev)
        m=x['members'][0];own=m['statement_original']+' '+m['local_label']
        linked=own+' '+' '.join(claims[t['claim_id']]['statement_original'] for t in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors) and all(s in linked for s in selectors),m['local_id']
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Census structurally validated; independent source review remains pending.')
if __name__=='__main__':main()
