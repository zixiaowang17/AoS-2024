"""Attach source-reviewed theorem-to-interface paths and finalize this paper."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT = {'1': {'D1': 'The reduced distributions P_g^{V_n} and Q_g^{V_n} are the image '
             'laws of the measurable statistic V_n.',
       'D2': 'The full and reduced KL expressions use the mixtures Pi_j^g '
             'indexed by G.',
       'D3': 'The assumption equates the full-data KL infimum and reduced-data '
             'minimum, which also gives the optimal value.',
       'D8': 'The last sentence identifies the group-indexed null P_g and '
             'alternative Q_g.',
       'D10': 'The maximization ranges over all e-statistics for that null.',
       'D11': 'The conclusion asserts GROW, namely the maximization of the '
              'worst-case log-growth objective (8).'},
 '2': {'D1': 'The reduced laws Q^{M_n}, P^{M_n} are the image measures for '
             'M_n.',
       'D2': 'The infimum ranges over the pair of full-data mixtures Pi_1^g '
             'Q_g and Pi_0^g P_g.',
       'D3': 'The conclusion is an equality of a KL infimum and the reduced KL '
             'divergence.',
       'D7': 'The opening sentence requires M_n to be maximally invariant '
             'under the group action.',
       'D8': 'P_g and Q_g are the two group-indexed hypotheses throughout the '
             'theorem.',
       'D9': 'The hypothesis explicitly requires G to be amenable.',
       'D13': 'The reference to all of Assumption 1 includes its topological '
              'Part 1.',
       'D14': 'The same reference includes the free, continuous and proper '
              'action in Part 2.',
       'D16': 'The same reference includes invariant dominated models, the '
              'multiplier and common support in Part 3.'},
 '4': {'D3': 'The hypothesis requires, for every alternative Q_g, some null '
             'P_h at finite KL divergence.',
       'D8': 'The final equivalence is explicitly for hypothesis testing '
             'problem (4).',
       'D10': 'The oracle supremum and both optimality criteria range over the '
              'same e-statistics.',
       'D11': 'The conclusion refers to maximizers of (8), the GROW criterion.',
       'D12': 'The conclusion refers to maximizers of (10), the relative GROW '
              'criterion.',
       'D16': 'The opening clause assumes Part 3 of Assumption 1 only; no '
              'other part is included.'}}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Verified registered arXiv:2208.07610v2 PDF, 31 pages; main text and references on pages 1-23, appendices excluded.',
        normalization_policy='Preserve all three complete original Theorems 1, 2 and 4, including every hypothesis and optimization quantifier. Preserve original definitions and separate source notes.',
        semantic_ranking_policy='Resolve group-model, probability-mixture and optimality definitions locally. Theorem 4 uses only Part 3 of Assumption 1; amenability and topological/action conditions belong to Theorem 2. Do not add proof-only Haar or martingale constructions.',
        build_order_policy='Derive all edges and reach from the original local dependency graph; keep the independent theorem inventory unchanged.')
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
