"""Resolve both missing-data classification Theorems against their original prerequisites."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{'D1':'The restrictions and rate explicitly use pattern dimensions d_omega.','D3':'The conditional risk is for the marginal P_Q of the joint law Q.','D5':'The expectation conditions on all training masks O_i=o_i from the iid observed experiment.','D6':'The minimax infimum explicitly ranges over all measurable classifiers C_n.','D9':'The displayed loss is the excess test error script E_{P_Q}.','D15':'The initial parameter domain requires Omega_star to be an antichain in script I.','D19':'The inequalities, rate and tail-vector bound use the coordinate vector gamma and pattern exponent gamma_omega.','D21':'The inequalities and rate use patternwise smoothness beta_omega.','D24':'The supremum is over the prime distribution class Q-prime-Miss defined in (11).','D25':'The rate and logarithm use the fixed-mask available-case counts n_omega.','D26':'R and the logarithm range over Omega_star intersect script N, and the extra term tests its complement.','D27':'The upper bound uses the lower-truncated logarithm log-plus.'},
 '2':{'D1':'The sample-size exponent and risk rate explicitly use d_omega.','D3':'The test error is under P_Q, the marginal of the joint missing-data law.','D5':'The expected risk is conditional on the whole sequence of training masks.','D9':'The quantity bounded is excess test error script E_{P_Q}.','D15':'The initial parameter domain requires Omega_star to be an antichain.','D16':'The sample-size restriction applies to U(Omega_star), the complement of the active set and its lower closure.','D19':'The tail restriction, sample-size exponent and risk rate use gamma_omega.','D21':'Those expressions also use beta_omega.','D25':'Both the imbalance restriction and the conclusion use n_omega.','D26':'The theorem requires Omega_star to be contained in script N and uses its cardinality in the logarithmic condition.','D27':'The risk bound uses log-plus; the sample-size condition uses the ordinary log.','D28':'The risk concerns the specific HAM classifier defined by every line of Algorithm 1.','D30':'The supremum is over Q-plus-Miss, using the strengthened conditional-feature tail condition.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned arXiv:2305.11672v2, 73 pages. Only main-text PDF 1–22 is admitted. Supplementary Sections S1–S5 begin on page 23 and are excluded.',
     normalization_policy='Preserve both complete original Theorems, all original class definitions and all 21 lines of Algorithm 1. Preserve the distinction between bold coordinate vectors and scalar pattern exponents.',
     semantic_ranking_policy='Count statement prerequisites and local definition dependencies. The minimax theorem does not inherit the HAM algorithm or the stronger plus tail condition; the HAM theorem does not inherit Theorem 1 lower-bound-only parameter restrictions.',
     build_order_policy='Derive edges from original definitions. Conditional and unconditional feature measures, prime and plus distribution classes, and available patterns versus allowed masks remain distinct. Record source ambiguities without inserting corrected formulas.')
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
