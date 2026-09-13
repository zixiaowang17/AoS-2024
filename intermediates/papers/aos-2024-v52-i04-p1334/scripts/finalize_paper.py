"""Attach source-reviewed theorem-to-interface paths and finalize this paper."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT = {'3.3': {'D2': 'The variance is under the standard Gaussian observation law imposed in the Introduction.', 'D4': 'The bound uses the 4k-4 and 4k-2 powers of the corresponding Schatten norms.', 'D9': 'The random variable U_k is the polynomial estimator (9).'}, '4.9': {'D2': 'The minimax expectation is under the Gaussian observation law, before the replacement law in Section 6.', 'D5': 'The supremum is restricted by the operator norm of A.', 'D6': 'The statement recalls the defining sum f_sigma(A), while explicitly broadening the original nonnegative range of f to all real values.', 'D10': 'The subtractive term uses the uniform norm of f on I_0, written with double bars in this theorem.', 'D11': 'The first term is the best uniform approximation error on I_0.', 'D12': 'Its approximation class is the symmetric-polynomial space with degree bound 2k-star.'}, '5.2': {'D2': 'The observation law is still the Gaussian model; Section 6 introduces the different noise law afterward.', 'D3': 'The hypothesis bounds the largest true singular value and the last display compares individual true singular values.', 'D13': 'The Wasserstein inequality compares the empirical measures of the estimated and true singular values.', 'D14': 'W is the CDF-based Wasserstein distance introduced in Section 5.', 'D18': 'The estimator defined above is the two-step grid, moment-fitting and rescaled-quantile procedure.'}, '6.3': {'D19': 'The expectation uses the centered unit-variance iid sub-Gaussian noise from the Section 6 setup.', 'D20': 'The bound depends explicitly on the scalar noise psi_2 norm.', 'D9': 'U_k remains the same Hermite polynomial statistic (9), now without a Gaussian unbiasedness assumption.', 'D4': 'The target is the 2k-th power of the 2k-Schatten norm.', 'D5': 'The two signal-dependent terms use powers of the operator norm.'}}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Verified registered arXiv:2111.13551v1 PDF, 67 pages; main text ends above Appendix A on page 65. Appendix bodies excluded.',
        normalization_policy='Preserve all four original Theorem statements, the source errors in Theorems 4.9 and 5.2, and the original two-step estimator without silent repairs.',
        semantic_ranking_policy='Trace paper-local statement dependencies. Keep the Gaussian observation law out of the sub-Gaussian theorem, retain the polynomial statistic under both noise laws and record unresolved aliases in the moment-fitting procedure. Proof-only lower-bound priors and combinatorial lemmas are not statement dependencies.',
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
            if 'D17' in path and 'D15' in path:
                evidence.append(dict(page=42,location='Proof of Theorem 5.2 uses hat m for the linear-program objective; original hat U alias remains unresolved.'))
            if 'D12' in path:
                sentences.append('The main-text proof of Lemma 4.5 specifies the even symmetry through the representation P(x^2).')
                evidence.append(dict(page=35,location='Proof of Lemma 4.5, meaning of symmetric polynomial.'))
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
