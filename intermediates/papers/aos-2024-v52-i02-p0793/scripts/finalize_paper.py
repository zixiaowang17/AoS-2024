"""Derive both theorem connections from their main-text definitions and hypotheses."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{'D1':'The model uses the iid observations and covariate density f defined in Section 2.','D2':'The lower-bound model restricts the propensity pi and control regression mu_0 defined in Section 2.','D3':'The minimax risk concerns the pointwise CATE tau at the interior point x_0 and mean absolute error.','D4':'The alpha-, beta- and gamma-smooth restrictions use the paper’s explicit Hölder convention.'},
 '2':{'D1':'The estimator operates on the observed-data sampling model and covariate distribution from Section 2.','D2':'The theorem explicitly restricts pi and mu_0, and their nuisance-estimation errors refer to these same conditional functions.','D3':'The target is the same pointwise CATE and absolute-error loss; the upper bound does not take a supremum over the entire lower-bound model.','D4':'Both the nuisance functions, their estimation errors and the CATE use the source Hölder smoothness convention.','D7':'Conditions B and C and Condition 1 explicitly concern the trained nuisance estimates pi-hat, mu_0-hat and F-hat.','D8':'The theorem explicitly invokes the estimator from Definition 2, retaining all its printed correction formulas.','D9':'Conditions A and C use the population matrix Q from the locally weighted projection (4).','D10':'The density ratio and both error norms are with respect to the transformed local measure F-star.','D11':'Condition A uses the population correction-basis matrix Omega, identified by the main-text coordinate formula for the F-star projection.','D12':'The theorem explicitly requires the Hölder approximating condition (6) for the correction basis b.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned arXiv:2203.00837v4 dated 23 December 2023. Main text and references end on PDF page 29; all appendices starting on page 30 are excluded.',
     normalization_policy='Preserve both original theorem statements and all estimator formulas. The lower-bound model and upper-bound regularity requirements remain distinct, with ambiguities recorded outside the source statements.',
     semantic_ranking_policy='Direct statement references and recursive paper-local definition prerequisites. Proof constructions and propositions are not imported as theorem dependencies.',
     build_order_policy='Retain the observed-data target, strict Hölder floor, two distinct bases, independent nuisance training, estimator, population projection and transformed-measure approximation requirements.')
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
