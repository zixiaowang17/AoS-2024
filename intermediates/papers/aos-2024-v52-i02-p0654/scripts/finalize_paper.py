"""Derive all eight theorem connections without importing proof-only requirements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '2.1':{'D1':'The estimators observe only D^[t] and their loss compares with the target mean f^[t].','D8':'The statement assumes fixed common target design points and an upper bound on consecutive spacings.','D17':'The supremum over P is specialized explicitly to n_s=0, the conventional target-only experiment.'},
 '2.2':{'D1':'The loss is squared functional L2 error for the target mean f^[t].','D7':'The supremum over P uses the full transfer model defined in Section 2.','D8':'The opening hypotheses bound spacings in the common target and source designs.','D3':'The explicit degree requirements use omega(alpha_m) and omega(alpha_delta), the strict-integer derivative-order convention.','D11':'The first candidate is the output of A_CL with the displayed common-design parameters.','D12':'The second candidate is the output of A_TL with the displayed source and residual parameters.'},
 '2.3':{'D1':'The target observation sample D^[t] and target mean f^[t] appear in the estimator domain and risk.','D2':'The infimum covers estimators based on all K source samples as well as the target sample.','D7':'The worst-case risk is over the full transfer model P.','D8':'The statement explicitly works under a common design; it does not restate or inherit an upper spacing bound.'},
 '2.4':{'D1':'The averaged estimator is evaluated against the target mean f^[t].','D7':'The supremum and reference to Theorem 2.2 retain the full transfer model P.','D8':'The reference to the assumptions of Theorem 2.2 retains the common design and its spacing bounds.','D3':'The inherited base-estimator specifications include the omega(alpha) degree conditions.','D14':'Each averaged g_r is an execution of A_ALC, Algorithm 3 with weighted test-loss selection.'},
 '3.1':{'D1':'The estimators use target data D^[t] only and estimate its mean f^[t].','D9':'The statement uses the target design law eta_t from Section 3 and adds its positive lower and upper density bounds.','D17':'Section 3.1 explicitly sets n_s=0 before this conventional minimax theorem, fixing the target-only meaning of P.'},
 '3.2':{'D1':'The loss compares the chosen estimator with the target mean f^[t].','D7':'The supremum is over P with the Section 3 replacement of the sampling design.','D9':'The statement assumes independent-design laws eta_t,eta_s and explicitly adds lower and upper density bounds.','D3':'Its constant polynomial degrees use omega(alpha_m) and omega(alpha_delta).','D11':'The first candidate is A_CL with the exact displayed independent-design bandwidth and threshold.','D12':'The second candidate is A_TL with the two displayed independent-design bandwidths and thresholds.'},
 '3.3':{'D1':'The target mean and target observation sample occur in the risk and estimator domain.','D2':'The estimator domain includes source samples; the final source index is printed ell rather than K and is retained.','D7':'The worst-case risk ranges over the full statistical model P retained by Section 3.','D9':'The theorem explicitly assumes an independent design. The density bounds of Theorem 3.2 are not imported into this lower-bound statement.'},
 '3.4':{'D1':'The repetition average estimates the target mean f^[t].','D7':'The supremum and inherited assumptions use the full transfer model P.','D9':'The reference to Theorem 3.2 retains independent designs and their two-sided density bounds.','D3':'The inherited base-estimator degree requirements use omega(alpha); Algorithm 4 also prints these explicitly.','D16':'Each g_r is an execution of A_ALI, the candidate-bandwidth and empirical-loss procedure in Algorithm 4.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned arXiv:2401.12331v2, all 25 main-paper pages. The separate supplementary document is excluded. Preserve eight printed Theorems in source order.',
     normalization_policy='Preserve original statements and algorithm steps, including source inconsistencies. Record conditional no-source and sampling-design specializations separately.',
     semantic_ranking_policy='Direct statement dependencies and recursive same-paper reach; distinguish target-only minimax experiments from the full transfer model and from named estimators.',
     build_order_policy='Keep the common and independent design hypotheses separate. A generic algorithm branches on its supplied design; its two branches do not impose both designs on any theorem.')
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


if __name__ == "__main__":
    main()
