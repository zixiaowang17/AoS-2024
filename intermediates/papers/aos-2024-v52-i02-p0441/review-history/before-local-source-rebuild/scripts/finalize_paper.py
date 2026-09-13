"""Derive the two-theorem same-paper census from the reviewed source inventory."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '4.2':{'D1':'The theorem explicitly draws the training pairs from data model (2.1), whose tau squared enters the scalar noise formula.','D2':'The fitted function belongs to the random features class (2.2), and the limit probability includes the randomness in W.','D3':'The theorem explicitly specifies shifted ReLU activation.','D4':'Assumption 1 supplies both proportional dimensions and signal normalization.','D5':'Part (b) characterizes AR of the fitted random features model, the squared-loss risk (4.2) at test radius epsilon_test.','D6':'Theta-hat with superscript epsilon is explicitly the robust ERM fit (4.3).','D7':'S in both the definition of sigma squared and the nested scalar supremum is explicitly the function (4.4).'},
 '6.9':{'D1':'Both objectives use responses and covariates generated according to (2.1), and their quadratic penalty contains the signal vector beta.','D2':'Phi_A evaluates the random feature map sigma(W x_i), and both objectives depend on W.','D3':'The section uses the shifted ReLU activation fixed in (4.1); the Gaussian surrogate coefficients are its specified moments.','D8':'The theorem explicitly assumes the event E_W in (6.2).','D9':'Both objectives contain the norm of J theta, where J is defined in Section 6.2 and (6.10).','D11':'The vectors f_i in Phi_B are the i.i.d. noisy linear features (6.15), as specified immediately after (6.16).','D12':'The probability limits use the section-wide proportional-growth convention stated on page 16. The theorem does not explicitly repeat Assumption 1(b); this scope limitation is recorded.'}
}
inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
data['schema_version']='statistical-ranked-interfaces-v4'
data['scope'].update(paper_count=1,source_policy='Pinned arXiv:2201.05149v2, main pages 1-25; both printed Theorems 4.2 and 6.9 retained. Supplementary pages 26-86 excluded.',normalization_policy='Preserve complete original theorem bodies, including source discrepancies and inline scalar optimization definitions. Record interpretation separately.',semantic_ranking_policy='Separate direct demand from recursive same-paper reach. Proof devices are not statement dependencies of Theorem 4.2.',build_order_policy='Use the acyclic local source graph. General feature classes and scalar activation definitions are separate. Keep the conditioned Gaussian-comparison statement separate from the unconditional adversarial-risk limit.')
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
