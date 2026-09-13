"""Derive all five theorem connections without importing proof-only requirements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '2.2':{
  'D2':'The strictness condition and the final two cases concern the expectation coordinates theta_i defined in (2.2).',
  'D8':'The rejection event uses the normalized squared statistic T_(n,Delta) defined in (2.9).',
  'D9':'Its critical value is q_(1-alpha)/a_d+b_d, using the explicit Gumbel quantile and normalizing constants following (2.11).',
  'D11':'The theorem expressly assumes (A1), including its B_n,beta,D tail and projection-moment bounds.',
  'D12':'The theorem expressly assumes (A2), which requires positive first-projection variance only for coordinates with |theta_i|>c.',
  'D13':'The theorem expressly assumes the first-projection correlation condition (A3).',
  'D14':'The supremum ranges over H_0(Delta), the distribution class defined in (2.15).',
  'D16':'The boundary and strict-interior cases describe positions in the null parameter region V_0 from (2.14).'
 },
 '2.4':{
  'D8':'The power event uses the same normalized squared statistic T_(n,Delta) from (2.9).',
  'D9':'The critical value again uses q_(1-alpha),a_d,b_d from the Gumbel calibration.',
  'D15':'The infimum is over the separated alternative class H_1(c) defined in (2.18), imposing (A1) but not (A2) or (A3).'
 },
 '2.5':{
  'D2':'The final sentence additionally assumes that the kernel h from (2.3) is bounded to improve the alternative separation rate.',
  'D8':'Both conclusions use the observed normalized statistic T_(n,Delta) defined in (2.9).',
  'D12':'The opening hypothesis expressly assumes restricted non-degeneracy (A2).',
  'D15':'Part (2) evaluates the class H_1 at c(log(nd))^(1/beta), or at c in the bounded-kernel case.',
  'D16':'The theorem explicitly refers to V_0 from (2.14) when defining its bootstrap null class.',
  'D17':'The opening hypothesis assumes the repeated-index kernel condition (A1-prime), which contains (A1).',
  'D21':'The critical value q*_(1-alpha) comes from the normalized bootstrap statistic and conditional distribution in (2.22)-(2.23).',
  'D22':'Part (1) defines and uses H_(0,boot)(Delta) in (2.26), with (A1-prime),(A2) and without (A3).'
 },
 '2.8':{
  'D2':'The final sentence uses boundedness of the kernel h to remove the extra logarithmic factor in the alternative class.',
  'D12':'The reference to the assumptions of Theorem 2.5 inherits (A2), as well as the full growth condition (2.24) archived separately.',
  'D15':'Part (2) uses H_1(c(log(nd))^(1/beta)), with the bounded-kernel refinement to H_1(c).',
  'D17':'The reference to the assumptions of Theorem 2.5 inherits the repeated-index condition (A1-prime).',
  'D22':'Part (1) uses the bootstrap null class H_(0,boot)(Delta) from (2.26).',
  'D23':'The event uses the observed unnormalized absolute statistic T_abs_(n,Delta) from (2.30).',
  'D24':'Its conditional critical quantile q*abs_(1-alpha) comes from the absolute bootstrap statistic (2.31).'
 },
 '3.5':{
  'D4':'The theorem explicitly specializes the pairwise dependence measure d_ij from (2.4) and uses its upper-triangle dimension d=p(p-1)/2.',
  'D5':'The event is failure to reject H_0 from the relevant hypotheses (2.5), and the separation constant satisfies c_0<1-Delta.',
  'D15':'The worst-case nonrejection probability ranges over H_1(c_0), the separated alternative class (2.18), specialized here to the covariance kernel.',
  'D25':'The infimum ranges over all tests in the printed class T_alpha from the preceding paragraph. Its null nonrejection event is preserved and separately flagged as inconsistent.',
  'D26':'The dependence measure is the population covariance with unit diagonal variances. The covariance-kernel correspondence on page 15 fixes this specialization.'
 }
}
inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
data['schema_version']='statistical-ranked-interfaces-v4'
data['scope'].update(paper_count=1,
 source_policy='Pinned arXiv:2210.17439v2; main pages 1-25 only. Appendix A online supplement begins separately on page 26. Preserve all five printed main-text Theorems in source order.',
 normalization_policy='Keep original statements, hypotheses, test statistics, conditional bootstrap construction and minimax quantifiers. Record source inconsistencies separately.',
 semantic_ranking_policy='Direct statement dependencies and deduplicated recursive same-paper reach. Assumption inheritance is distinguished from inheriting the construction of a different test.',
 build_order_policy='Separate the null parameter region from each distribution class, and distinguish Gumbel, normalized bootstrap, absolute bootstrap and arbitrary-test lower-bound constructions.')
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
