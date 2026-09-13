"""Attach source-reviewed theorem-to-interface paths and finalize this paper."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT = {'2': {'D4': 'The two lower rates explicitly depend on the volatility-block mesh delta.', 'D5': 'Theorem 2 explicitly states both lower bounds in the original Section 2 experiment E^n and parameter domain D.', 'D6': 'The phrase lower rate of convergence refers to the measurable-estimator minimax criterion, with the stated change of target for eta.'}, '3': {'D4': 'The claimed rate includes delta^(1/2) from the piecewise-constant observation regime.', 'D5': 'The uniform tightness is under the Section 2 laws P_H,eta over its original compact D.', 'D12': 'The normalized error uses the estimator hat H_n defined immediately above, with positive threshold nu_0 and selected scale J_n*; kappa_0 is bound inside the theorem.'}, '4': {'D7': 'Theorem 4 is in Section 3 and uses the general continuous-volatility model and its H<3/4 parameter domain.', 'D8': 'Its lower-rate assertions use the Section 3 minimax criterion for H and eta.'}, '11': {'D7': 'The uniform probability statement uses the general-model law and parameter set of Section 3.', 'D13': 'The displayed iteration condition ranges between the parameter extrema H_- and H_+.', 'D24': 'Both sequences are the recursively defined estimators at integer iteration m_opt, including their initialization and sequential updates.'}}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Verified registered arXiv:2210.01214v2 PDF, 61 pages; main text through the reference endpoint above Appendix A on page 56. Appendix bodies excluded.',
        normalization_policy='Preserve all four full Theorem statements. Keep the piecewise-constant experiment and general model separate, with untouched estimator formulas and separately recorded source inconsistencies.',
        semantic_ranking_policy='Trace original estimator definitions and statistical experiments. Include main-text kappa and Gaussian-integral definitions required to state the estimator; exclude auxiliary proof arguments and latent targets not needed to evaluate it.',
        build_order_policy='Derive the graph from original local definitions, retain source conditions and unresolved meanings, and do not infer library availability.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                evidence=list(c['evidence'])
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=evidence))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
            sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])
            for lid in path:evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
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
    print('Structural validation passed; independent full source audit remains pending.')
    finalized=json.loads((ROOT/'ranked-interfaces.json').read_text())
    passages=dict(paper_id=PID,members=[m for x in finalized['interfaces'] for m in x['members']])
    (ROOT/'source-passages.json').write_text(json.dumps(passages,indent=2,ensure_ascii=False)+'\n')

if __name__ == "__main__":
    main()
