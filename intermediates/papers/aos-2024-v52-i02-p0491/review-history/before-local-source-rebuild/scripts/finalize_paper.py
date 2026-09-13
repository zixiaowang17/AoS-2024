"""Derive the three-theorem same-paper census from the reviewed source inventory."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1.2':{
  'D1':'The empirical risk compares the fitted linear signal with f*, and the noise estimation error uses epsilon from (1.1).',
  'D2':'The minimal requirements preceding (SubGE) apply to the theorem: i.i.d. design rows and noise terms, with full row rank almost surely.',
  'D3':'The theorem explicitly assumes (SubGE), whose overbarred sigma squared enters both the penalty condition and the bound.',
  'D5':'F-hat at tau, at m, and at the oracle iteration denotes Algorithm 1 OMP fits.',
  'D7':'Tau and the noise estimate are explicitly those in stopping rule (1.8).',
  'D8':'The second inequality uses m^o, the ideal empirical-risk oracle in (1.6).',
  'D17':'Probability converging to one is along the model sequence specified in Section 1.1.'},
 '1.8':{
  'D1':'F* and epsilon are the true linear signal and noise in the sampling model (1.1).',
  'D2':'The paper-wide minimal sampling and rank assumptions apply to the population-risk theorem.',
  'D3':'The theorem explicitly assumes (SubGE) and uses its overbarred sigma squared in C_tau.',
  'D5':'The fitted function F-hat at tau is the OMP estimate from Algorithm 1.',
  'D7':'Both the noise-estimation condition and the stopped fit refer explicitly to (1.8).',
  'D9':'The theorem explicitly assumes (Sparse), retaining both alternatives and their respective parameters.',
  'D10':'The theorem explicitly assumes (SubGD); rho to the fourth power occurs in C_tau.',
  'D11':'The theorem explicitly assumes (CovB), the covariance lower bound and subset-coefficient condition.',
  'D13':'R(s,gamma) in the noise-estimation assumption and risk conclusion is the branch-dependent rate (1.20).',
  'D17':'Both high-probability statements use the paper-wide asymptotic model sequence.'},
 '5.1':{
  'D1':'The theorem uses the true signal f* and empirical noise vector epsilon from (1.1).',
  'D2':'The theorem inherits the paper-wide i.i.d. sampling and full-row-rank requirements.',
  'D3':'The theorem explicitly assumes (SubGE), and its proxy enters C_tau and C_AIC.',
  'D5':'The output F-hat at the two-step iteration is an OMP fit from Algorithm 1.',
  'D7':'The noise estimate and first-stage coefficient C_tau are explicitly specified through (1.8).',
  'D9':'The theorem explicitly assumes (Sparse), whose chosen branch also determines its lower-bound iteration and target rate.',
  'D10':'The theorem explicitly assumes (SubGD) and uses its rho parameter in both penalties.',
  'D11':'The theorem explicitly requires (CovB).',
  'D13':'The rate R(s,gamma) occurs in the one-sided noise-estimation condition and the population-risk bound.',
  'D14':'The conclusion explicitly lower-bounds tau_two-step by the iteration tilde-m_(s,gamma,G) from (3.2).',
  'D15':'C_AIC is the additive criterion coefficient from (5.5), set to a sufficiently large multiple of the noise/design proxy.',
  'D16':'The two-step iteration in both conclusions is the AIC minimizer over the prefix through tau, defined in (5.6).',
  'D17':'The asserted common high-probability event is along the model sequence from Section 1.1.'}
}
inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
data['schema_version']='statistical-ranked-interfaces-v4'
data['scope'].update(paper_count=1,source_policy='Pinned arXiv:2210.07850v1; main pages 1-24. All three printed Theorems retained; appendices excluded.',normalization_policy='Preserve complete source theorem bodies, two sparsity alternatives and exact constants/quantifiers. Record source discrepancies separately.',semantic_ranking_policy='Direct statement dependencies and recursive same-paper reach; do not count supporting lemmas, propositions or examples as theorem requirements.',build_order_policy='Acyclic local graph separating geometric projections, OMP iteration, residual, sequential stopping and AIC prefix selection. Preserve the selected sparsity branch in rates and bias thresholds.')
data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
for c in data['claims']:
 n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
 for x in data['interfaces']:
  lid=x['members'][0]['local_id']
  if lid in DIRECT[n]:x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']))
derived=canonical_dependencies(data)
for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
derive_metrics(data)
for x in data['interfaces']:
 for r in x['related_theorems']:
  cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1];sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])
  for lid in path:
   evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
   for ctx in members[lid].get('application_context',[]):evidence.extend(e for e in ctx['evidence'] if e not in evidence)
  for a,b in zip(path,path[1:]):sentences.append(edges[a][b])
  x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=' '.join(sentences),evidence=evidence)
 for m in x['members']:
  own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems']);selectors=m['highlight_symbols']+m['highlight_phrases']
  assert any(s in own for s in selectors),(m['local_id'],'missing source highlight')
  assert all(s in linked for s in selectors),(m['local_id'],'unmatched selector')
attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
(ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
print('Finalized and independently validated; final source audit remains.')
