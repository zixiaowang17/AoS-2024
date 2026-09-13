"""Derive the three-theorem same-paper census from the reviewed source inventory."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{
  'D1':'Mu is the conditional response mean and n,p refer to the sample and covariate dimensions fixed in Section 1.1.',
  'D3':'The numerator contains inverse split-success probabilities P_A_t(kappa), and the bound contains the candidate sparsity d and slackness kappa from Section 2.2.',
  'D4':'The depth-K estimator and its internal-node index [T_K] use the recursive oblique tree construction with the search-space convention on page 10.',
  'D5':'Mu-hat(T_K) and mu-hat(T_opt) are the node-average predictions defined by (2).',
  'D8':'The oracle infimum is over F and contains the global L1 variation norm of f, both defined in Section 2.1.',
  'D9':'The second inequality evaluates the penalized pruned tree T_opt and specifies the size of its penalty lambda_n.',
  'D10':'The theorem expressly requires Assumption 2, whose c1,c2,gamma,M determine the positive constant C and logarithmic exponent.'},
 '4':{
  'D1':'Mu is the conditional mean and p,n are the covariate dimension and sample size of the observation model.',
  'D3':'The theorem expressly sets d=p, kappa=1 and P_A_t(kappa)=1, fixing the full-optimization parameters from Section 2.2.',
  'D4':'The risk bound is for the depth-K oblique tree T_K defined by recursive splitting.',
  'D5':'Both inequalities evaluate the terminal-node mean output mu-hat of their fitted trees.',
  'D9':'The second inequality concerns the penalized pruned tree T_opt and its coefficient lambda_n.',
  'D10':'Assumption 2 is explicitly required and supplies the tail parameters in C and the exponent 4/gamma+1.',
  'D11':'Assumption 3 is explicitly required and supplies V and the fixed exponent q in both rates.',
  'D12':'Assumption 4 is explicitly required and supplies the node-count bound A in both rates.'},
 '5':{
  'D1':'Mu and p refer to the same conditional mean and covariate dimension as the underlying sample model.',
  'D3':'The bound contains d, kappa and the inverse split-success probabilities P_A_t(kappa). These are applied to subsampled data, as specified after the theorem.',
  'D4':'The RHS uses the internal nodes [T_K] of a depth-K tree, trained on the size-N subsample in this section.',
  'D8':'The oracle infimum is over F and penalizes the global L1 variation of f.',
  'D10':'The theorem explicitly requires Assumption 2; its exponent gamma enters the subsample complexity term.',
  'D13':'Mu-hat(bold Theta) is explicitly the oblique random forest output, and N is its subsample size from Section 4.'}
}
inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
data['schema_version']='statistical-ranked-interfaces-v4'
data['scope'].update(paper_count=1,source_policy='Pinned arXiv:2210.14429v2; main pages 1-17 and page 18 above Appendix A. All three printed Theorems retained; appendix bodies excluded.',normalization_policy='Preserve complete source theorem bodies and original prerequisite passages. Keep source ambiguities in separate analysis fields.',semantic_ranking_policy='Derive direct demand and recursive same-paper reach from statement dependencies; no proof-only lemmas or corollary-only assumptions.',build_order_policy='Acyclic local source graph. Resolve the finite ridge norm before the library and its L2 closure/relaxed norm; record the source notation ambiguity rather than changing the definitions.')
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
