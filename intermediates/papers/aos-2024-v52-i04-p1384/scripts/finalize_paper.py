"""Attach source-reviewed theorem-to-interface paths and finalize this paper."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT = {'2.1': {'D4': 'The opening reference to Assumption 1 requires its unique minimum and positive Hessian.',
         'D5': 'The opening reference to Assumption 2 supplies a3, a4, q and both scale restrictions.',
         'D6': 'The opening reference to Assumption 3 supplies the lower growth bound and c0.',
         'D9': 'The pair hat m, hat S is explicitly the canonical pair furnished by Lemma 2.1.',
         'D11': 'The hypothesis gives the entire centered growth condition (2.7) for g.',
         'D12': 'All three conclusions use Var_hat-pi(g).'},
 '2.2': {'D4': 'Assumption 1 is explicitly required.',
         'D5': 'Assumption 2 is explicitly required and supplies a3, a4, q.',
         'D6': 'Assumption 3 is explicitly required and supplies c0.',
         'D9': 'The definition of Q and both approximation integrals use the section-wide canonical Gaussian '
               'hat pi.',
         'D11': 'The hypothesis requires g to satisfy (2.7).',
         'D12': 'The remainder bound contains Var_hat-pi(g).',
         'D13': 'The theorem explicitly defines Q in (2.11) and uses its integral as the leading '
                'correction.'},
 '3.1': {'D16': 'The setting immediately before the theorem imposes a well-specified logistic model, iid '
                'Gaussian design, bounded theta0 and bounded prior precision. The claimed event is under '
                'this sampling law.',
         'D7': 'The first conclusion identifies a solution to the original optimality equations (1.9).',
         'D8': 'That solution is required to lie in the region R_V.',
         'D9': 'The subsequent bounds use the Gaussian hat pi of this canonical pair on the stated event.',
         'D11': 'The hypothesis requires (2.7) with the explicit specialization c0=1/8.',
         'D12': 'The integral bounds involve Var_hat-pi(g).',
         'D17': 'The theorem explicitly refers to Q as defined in (3.7) and (3.6).',
         'D18': 'The two suprema use B(R^d) and the symmetric Borel class, printed B_{s,hat m} here but '
                'introduced as S_{hat m} on page 8.'},
 '4.1': {'D4': 'The explicit inheritance of the conditions of Theorem 2.1 includes Assumption 1.',
         'D5': 'The inherited conditions include Assumption 2, with its two scale constraints and '
               'parameters.',
         'D6': 'The inherited conditions include Assumption 3.',
         'D9': 'The inherited Lemma 2.1 pair is the canonical Gaussian approximation used for T.',
         'D11': 'The opening sentence explicitly requires g to satisfy (2.7).',
         'D19': 'The theorem names T from (4.2) and rho and V0 from (4.3); f and Delta_f are bound in the '
                'statement itself.',
         'D21': 'The third branch requires orthogonality to all third order Hermite polynomials under the '
                'standard Gaussian.',
         'D22': 'The corrected difference uses the polynomial p3 defined immediately before the theorem.'}}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Verified registered arXiv:2301.02168v2 PDF, 49 pages; main text ends after Acknowledgments on page 22. Appendix notation prelude and all appendix bodies excluded.',
        normalization_policy='Preserve four complete original Theorem statements and source passages. Keep notation inconsistencies in quotations with separate source notes.',
        semantic_ranking_policy='Trace only statement dependencies. Keep the canonical stationarity solution distinct from global KL minimization. The logistic sampling law is local to Theorem 3.1; do not propagate it to general results.',
        build_order_policy='Derive prerequisite edges from original local definitions; preserve theorem completeness and source-specific conditions.')
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
