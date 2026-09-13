"""Attach source-reviewed theorem-to-interface paths and finalize this paper."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT = {'1': {'D2': 'Theorem 1 uses the iid baseline experiment of Section 3.', 'D3': 'The target psi is psi(P), with the stated fixed-K asymptotic convention.', 'D7': 'The conclusion concerns the batching statistic W_B.', 'D11': 'The leading distribution is Student t_(K-1).', 'D16': 'The opening hypothesis is the uniform scalar Edgeworth expansion with polynomial parity.'}, '2': {'D2': 'The statement explicitly recalls the iid observations from P.', 'D12': 'The opening sentence defines the smooth-function statistical functional.', 'D13': 'Equation (4) is the stated vector Cramer condition.', 'D14': 'The moment and covariance clause supplies the finite r+2 moments and nonsingular covariance.', 'D15': 'The statement requires r+1 derivatives and a nonzero gradient near the mean.', 'D7': 'The final replacement clause includes batching W_B.', 'D8': 'The same clause includes sectioning W_S.', 'D9': 'The same clause includes sectioning-batching W_SB.', 'D10': 'The two displayed conclusions are first stated for sectioned jackknife W_SJ.', 'D11': 'Both conclusions use the Student law with K-1 degrees of freedom.'}, '3': {'D17': 'The functions f and g and their stationary scalar objective come from the Section 5 setup.', 'D18': 'The theorem title and Section 5.1 setup specify gaps of n^delta between retained batches and substitution of their empirical laws.', 'D19': 'The mixing-rate hypothesis uses alpha(n) from Definition 1; its printed sigma alias remains unresolved.', 'D20': 'Harris recurrence is explicitly required and defined in Definition 2.', 'D7': 'The final replacement clause includes W_B with the gapped data substitution.', 'D8': 'The final replacement clause includes W_S with the gapped data substitution.', 'D9': 'The final replacement clause includes W_SB with the gapped data substitution.', 'D10': 'The expansion is stated first for W_SJ with the gapped data substitution.', 'D11': 'The leading law is t_(K-1).'}, '4': {'D17': 'The centered g and stationary expectation are from the scalar transformed setup.', 'D18': 'This is the second gap-based construction in Section 5.1, using the same retained-batch empirical substitution.', 'D19': 'The mixing-rate condition uses Definition 1.', 'D20': 'The statement explicitly requires Harris recurrence.', 'D21': 'The theorem defines the split process, residual kernel and centered cycle quantities consumed in conditions (i)-(iv).', 'D7': 'The final replacement clause includes gapped batching W_B.', 'D8': 'It includes gapped sectioning W_S.', 'D9': 'It includes gapped sectioning-batching W_SB.', 'D10': 'The displayed conclusions are for gapped sectioned jackknife W_SJ.', 'D11': 'The leading and symmetric reference probabilities are Student probabilities.'}, '5': {'D22': 'The positive expected duration and Q_i observations use the defined regenerative return times and cycle rewards.', 'D23': 'The theorem assumes the cycle-pair distribution and uses the ratio functional and empirical substitution defined immediately above it.', 'D7': 'The replacement clause includes W_B evaluated on cycle pairs.', 'D8': 'It includes W_S evaluated on cycle pairs.', 'D9': 'It includes W_SB evaluated on cycle pairs.', 'D10': 'The displayed conclusions use W_SJ evaluated on cycle pairs.', 'D11': 'The expansion is about the Student distribution.'}, '6': {'D2': 'The inherited Theorem 2 conditions include the iid original-data experiment.', 'D12': 'The inherited functional is a smooth function of a vector mean.', 'D13': 'Theorem 2 with r=2 retains the vector Cramer condition.', 'D14': 'The inherited moment order is four with nonsingular covariance.', 'D15': 'The inherited smoothness order is three, with nonzero gradient.', 'D24': 'The statement explicitly names expansion (6), whose n^(-1) coefficient is c.', 'D28': 'The conclusion refers to the original Algorithm 1, including its remaining Taylor, boundary and output steps.', 'D7': 'The statement explicitly allows W_B as its selected statistic.', 'D8': 'It explicitly allows W_S.', 'D9': 'It explicitly allows W_SB.', 'D10': 'It explicitly allows W_SJ.'}, '7': {'D2': 'The statement explicitly assumes the iid Section 3 experiment.', 'D3': 'Psi retains its target-value meaning, but the theorem explicitly replaces the baseline limit by fixed n and K tending to infinity.', 'D7': 'Its first coverage limit concerns W_B.', 'D8': 'Its second coverage limit concerns W_S.', 'D10': 'Its last coverage limit concerns W_SJ; no W_SB limit is stated.', 'D29': 'The differentiability and variance assumptions explicitly use the influence function IF named in Section 3.'}}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Verified registered arXiv:2111.06859v1 PDF, 46 pages; main text and references end above Appendix A on page 22. Appendix bodies excluded.',
        normalization_policy='Preserve all seven full Theorem statements and original Algorithm 1. Keep all page continuations, named conditions, data substitutions, different asymptotic regimes and printed source errors unchanged.',
        semantic_ranking_policy='Trace paper-local dependencies under the correct sampling construction. Gapped and regenerative methods do not inherit iid raw data. Theorem 6 inherits Theorem 2 at r=2; Theorem 7 changes the limit and has no SB conclusion. Missing appendix-only formulas remain unresolved.',
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
