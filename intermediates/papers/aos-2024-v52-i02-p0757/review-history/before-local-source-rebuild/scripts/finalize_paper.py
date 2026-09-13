"""Derive all five theorem connections without importing proof-only requirements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '4.1':{'D1':'The theorem concerns measurable random objects and a Borel law on the metric space.','D2':'Part (a) compares the original and pushforward distance profiles, and part (c) compares profiles along the curve.','D3':'Part (d) explicitly assumes strong negative type (9) for the underlying metric space.','D4':'All four parts concern transport ranks from (12), with R a scalar despite the printed extra argument in part (c).','D5':'Part (b) asserts membership of the transport mode in the median set from (13).','D6':'Parts (b) and (c) explicitly invoke a transport mode as in (14).'},
 '5.1':{'D10':'The theorem explicitly assumes Assumption 1.','D11':'The theorem explicitly assumes Assumption 2.','D7':'The empirical process uses the full-sample empirical profiles from (15).','D12':'The limiting covariance uses the closed-ball indicators y_omega,t introduced immediately before the theorem.'},
 '5.2':{'D10':'The theorem explicitly assumes Assumption 1.','D11':'The theorem explicitly assumes Assumption 2.','D8':'The estimated rank in the uniform root-n bound is the signed quantile estimator (16).','D4':'The target R_omega is the population transport rank (12).'},
 '5.3':{'D10':'The theorem explicitly assumes Assumption 1.','D11':'The theorem explicitly assumes Assumption 2.','D14':'The theorem explicitly assumes Assumption 3, retaining its printed pointwise-median separation formula.','D5':'The population median set is explicitly required to be nonempty.','D9':'The empirical set in the conclusion is the sample argmax (17).','D13':'The set convergence is measured in the Hausdorff metric (19).'},
 '6.1':{'D10':'The theorem explicitly assumes Assumption 1.','D18':'The theorem explicitly assumes Assumption 4, including the weight convergence (25).','D19':'The theorem explicitly assumes Assumption 5.','D20':'The theorem explicitly assumes Assumption 6.','D15':'The null H0 is explicitly referenced as (20).','D17':'The statistic is the weighted profile statistic (24).','D23':'The random-series law and its covariance eigenvalues are defined inline in the theorem.'},
 '6.2':{'D10':'The theorem explicitly assumes Assumption 1.','D18':'The theorem explicitly assumes Assumption 4.','D19':'The theorem explicitly assumes Assumption 5.','D20':'The theorem explicitly assumes Assumption 6.','D22':'The result is for the sequence H_nm defined in (29).','D28':'The power beta_nm is expressly referenced as (30), including the oracle null critical value.'},
 '6.3':{'D10':'All clauses explicitly assume Assumption 1.','D18':'All clauses explicitly assume Assumption 4.','D19':'All clauses explicitly assume Assumption 5.','D20':'All clauses explicitly assume Assumption 6; the last clause additionally imposes the two displayed root-total-size balance restrictions.','D15':'The first two clauses explicitly impose H0 (20).','D24':'The null critical value q_alpha uses the generalized inverse of Gamma_L defined in Section 6.1.', 'D25':'The empirical CDF and estimated quantile are those of (27)-(28), with K permutations.','D23':'Gamma_L denotes the null random-series distribution from Theorem 6.1; its relevant CDF continuity is imposed explicitly.','D26':'The final clause uses the mixture-reference CDF and its quantile introduced immediately before the theorem.','D27':'The final conclusion concerns permutation power from (31), retaining the sequence H_nm through that definition.'}
}
inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
data['schema_version']='statistical-ranked-interfaces-v4'
data['scope'].update(paper_count=1,
 source_policy='Pinned arXiv:2202.06117v4 dated 27 February 2024; main text ends above the Supplementary Material heading on shared PDF page 33. All seven main-text Theorems are included; supplement material is excluded.',
 normalization_policy='Preserve original statements, definitions and assumptions. Keep population and empirical profiles, transport ranks, and the separate two-sample branch distinct; source ambiguities are recorded separately.',
 semantic_ranking_policy='Direct statement references and recursive paper-local definition prerequisites. No proof-only dependencies or automatic import of all hypotheses of a theorem defining a referenced object.',
 build_order_policy='Keep Assumptions 2 and 5 separate; preserve leave-one-out versus full-sample profiles, both power functions and all three quantile laws.')
data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
for c in data['claims']:
    n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
    for x in data['interfaces']:
        lid=x['members'][0]['local_id']
        if lid in DIRECT[n]:
            x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']))
derived=canonical_dependencies(data)
for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
derive_metrics(data)
for x in data['interfaces']:
    for r in x['related_theorems']:
        cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
        sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])
        for lid in path:
            evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
            for ctx in members[lid].get('application_context',[]):
                evidence.extend(e for e in ctx['evidence'] if e not in evidence)
        for a,b in zip(path,path[1:]):sentences.append(edges[a][b])
        x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=' '.join(sentences),evidence=evidence)
    for m in x['members']:
        own=m['statement_original']+' '+m['local_label']
        linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors),(m['local_id'],'missing source highlight')
        assert all(s in linked for s in selectors),(m['local_id'],'unmatched selector')
attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
(ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
print('Finalized and independently validated; final source audit remains.')
