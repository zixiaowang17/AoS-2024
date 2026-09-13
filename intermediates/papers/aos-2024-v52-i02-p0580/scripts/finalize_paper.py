"""Derive all four theorem connections from the source-local definitions."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{
  'D1':'The theorem explicitly assumes the Bayesian two-groups model (1) with a uniform null. It retains the exact equality involving pi_0.',
  'D2':'The first expectation evaluates lfdr at the last rejected p-value; lfdr is the null posterior ratio (2).',
  'D3':'Only the final sentence additionally assumes the alternative density f_1 is non-increasing. The preceding last-rejection identity does not require that condition.',
  'D4':'The final conclusion controls max-lfdr as defined in (3), including its zero value for no rejection.',
  'D5':'The theorem explicitly selects procedure (4), including its last minimizing index R_ell and the corresponding p-value threshold.'
 },
 '4':{
  'D1':'The theorem explicitly assumes model (1) with the uniform null.',
  'D3':'The opening hypothesis requires a non-increasing alternative density f_1.',
  'D4':'The conclusion bounds max-lfdr, the expected maximum defined in (3).',
  'D8':'The displayed objective uses pi-hat_0^lambda, the plus-one null-proportion estimate (12) introduced immediately before the theorem.',
  'D9':'The theorem defines the constrained SL index and rejection set in (13) and controls that specific modified rule.'
 },
 '5':{
  'D1':'The theorem explicitly assumes model (1), with pi_0 in (0,1), a uniform null and common mixture density f.',
  'D3':'The opening hypothesis requires f_1 to be non-increasing; local smoothness and the negative derivative of f are additional inline conditions.',
  'D2':'The second distributional limit and its variance conclusion evaluate lfdr(tau_(ell-hat)), the density-ratio posterior (2).',
  'D5':'The empirical threshold tau_(ell-hat) is the order statistic selected by the SL rule (4) at the random tuning level. The population crossing t_ell is bound inline and resolved in A3.',
  'D11':'The theorem explicitly names Chernoff’s distribution (22), whose variable Z is the location of the Brownian-parabola maximum, not the maximum value.'
 },
 '6':{
  'D1':'The theorem explicitly assumes model (1), with pi_0 in (0,1) and a uniform null.',
  'D3':'The opening hypothesis requires a non-increasing alternative density f_1.',
  'D2':'The unique-crossing condition uses lfdr(tau*)=pi_0/f(tau*)=alpha from definition (2).',
  'D5':'The procedure in the regret is ordinary SL at level alpha/pi-hat_0. The estimator is arbitrary under the stated condition; it is not necessarily the specific estimate (12) or constrained rule (13).',
  'D7':'Tau* is the oracle threshold (7) at the cost-derived alpha from (6), here required to be a unique interior crossing.',
  'D10':'Regret_m is the expected excess weighted loss relative to the oracle, defined in (16). It averages both the data and null indicators.',
  'D11':'The limiting constant uses Var(Z), where the theorem expressly identifies Z with Chernoff’s distribution (22).'
 }
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned arXiv:2207.07299v2, main pages 1-25 only. Appendix A begins separately on page 26, inspected only through its heading crop. Preserve Theorems 1,4,5,6 in source order.',
     normalization_policy='Preserve original statements, last-minimizer convention, conditional monotonicity, exact error exponents and distinct finite-sample versus general-estimator assumptions. Record discrepancies separately.',
     semantic_ranking_policy='Direct statement dependencies and deduplicated recursive same-paper reach. Proof-only Grenander and least-concave-majorant constructions do not count as requirements.',
     build_order_policy='Keep deterministic decision rules, mixture model, posterior criterion, loss, oracle and regret separate. The modified rule uses its specific estimator; the asymptotic regret theorem permits a general estimator.')
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


if __name__ == '__main__':
    main()
