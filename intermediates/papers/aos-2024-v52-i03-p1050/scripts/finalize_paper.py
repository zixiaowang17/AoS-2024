"""Derive all three theorem dependency sets from their statements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '3.1':{'D5':'The theorem explicitly assumes the Markovian change-point representation (1), including its sufficient state mathbb-S_t.','D14':'The selected policy and stopping time are the specific optimal procedure (9).','D10':'That procedure is required to solve the auxiliary integrated-cost optimization (6) for c>0.','D9':'The claimed boundary compares the posterior odds Gamma_t with a deterministic function of the sufficient state.','D6':'The final sentence gives the memoryless, zero-dimensional special case.'},
 '5.1':{'D3':'The theorem explicitly invokes the response model.','D4':'It also explicitly invokes the general treatment-controlled change-point model.','D21':'The response model must satisfy the complete log-likelihood second-moment condition (14).','D23':'The change model must satisfy uniform transition stability (16), which also defines M(Xi,epsilon) in the remainder.','D15':'Xi_1 and Xi_2 are cyclic treatment blocks of the displayed lengths ell_1 and ell_2.','D18':'The expectation in the bound concerns the cyclic stopping rule tilde-T from Section 4.1.','D19':'The continuation on page 13 explicitly covers the modified initial assignment from Subsection 4.2.','D24':'The leading and remainder terms use adjusted information D(Xi_1) and D(Xi_2) from (17).','D22':'The displayed terms also use J(Xi_2) and the block-averaged V^I,V^J quantities.','D25':'The leading term uses the expected change time lambda(Xi_1) from (18).','D26':'The additional-cycle contribution uses the worst-history bound tilde-lambda(Xi_1) from (19).','D27':'The remainder contains the logarithm of the two-block hazard bound zeta(Xi_1) from (20).'},
 '6.1':{'D3':'The theorem explicitly invokes the response model.','D4':'The theorem explicitly invokes the treatment-history change-point model.','D21':'The response condition is the full centered log-likelihood variance assumption (14).','D29':'The change model must satisfy the uniform upper hazard bound (27).','D30':'Condition (28) supplies the optimal expected change time lambda-star and the existence of a controlled residual-time continuation.','D31':'Condition (29) supplies the positive information bound D-star and all of its window and uniformity requirements.','D8':'The infimum in the conclusion ranges over the false-alarm-constrained class C_alpha.','D28':'Section 6.1 defines the alpha-to-zero family and the liminf-ratio meaning of the displayed asymptotic lower bound.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned 53-page arXiv:1710.00915v5. Main text and references through page 26 above y=137.4; Appendix A and all subsequent appendix mathematics excluded.',
     normalization_policy='Preserve all three complete Theorems, including the two-page Theorem 5.1 extension, blackboard-bold Markov state versus plain stage endpoints, sans-serif information/probability symbols and every printed hypothesis.',
     semantic_ranking_policy='Count only statement prerequisites and recursive definitions. Keep Markov control, the non-asymptotic cyclic procedure and the universal lower bound distinct; reuse omega without importing the surrounding block-stability condition.',
     build_order_policy='Derive edges from paper-local source definitions. Retain the appendix-only predictive-density reference unresolved. Do not add finite-memory examples, optimized designs or proof assumptions to the theorem graph.')
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
    finalized=json.loads((ROOT/'ranked-interfaces.json').read_text())
    passages=dict(paper_id=PID,members=[m for x in finalized['interfaces'] for m in x['members']])
    (ROOT/'source-passages.json').write_text(json.dumps(passages,indent=2,ensure_ascii=False)+'\n')
    print('Finalized and independently validated; final source audit remains.')


if __name__ == "__main__":
    main()
