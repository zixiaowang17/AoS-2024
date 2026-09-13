"""Derive the two-model theorem/interface census from the reviewed inventory."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '2.1':{'D3':'The first comparison bounds the white-noise minimizer risk R_z in (1.2).','D4':'The second comparison bounds the white-noise minimum risk R_m in (1.3).','D6':'The third comparison bounds the minimizer interval benchmark L_z,alpha in (1.6).','D7':'The fourth comparison bounds the minimum interval benchmark L_m,alpha in (1.7).','D8':'All four bounds use the local L2 moduli omega_z or omega_m, with epsilon/3 in the interval lower bounds.'},
 '2.2':{'D1':'The product inequalities hold for every convex function f in the class F.','D3':'The first product contains the minimizer risk R_z.','D4':'The first product contains the square of the minimum risk R_m.','D6':'The second product contains the minimizer interval benchmark L_z,alpha.','D7':'The second product contains the square of the minimum interval benchmark L_m,alpha.'},
 '2.3':{'D1':'Both super-efficiency implications compare the extremum functionals at f_0 and another function f_1 in F.','D3':'The first premise and conclusion use the minimizer benchmark R_z.','D4':'The second premise and conclusion use the minimum benchmark R_m.'},
 '3.1':{'D1':'The loss is for the minimizer Z(f), uniformly over f in F.','D14':'Z-hat is explicitly the white-noise midpoint estimator (3.5).','D10':'The first risk bound uses the horizontal geometric quantity rho_z.','D3':'The second bound compares the risk to R_z.'},
 '3.2':{'D1':'Coverage is for Z(f), and the length bound is uniform over f in F.','D15':'CI_z,alpha is explicitly the white-noise interval (3.6).','D5':'The first assertion guarantees the white-noise confidence-interval coverage property.','D10':'The displayed expected-length bound uses rho_z.','D6':'The final comparison is to the white-noise length benchmark L_z,alpha.'},
 '3.3':{'D1':'The loss is for the minimum M(f), uniformly over f in F.','D17':'M-hat is explicitly the shifted white-noise block estimator (3.7).','D9':'The first risk bound uses the vertical geometric quantity rho_m.','D4':'The second comparison is to the minimum risk R_m.'},
 '3.4':{'D1':'The coverage target is M(f), and the length bound is uniform over F.','D19':'CI_m,alpha is the white-noise multiscale interval (3.10).','D5':'The first assertion gives its white-noise coverage property.','D9':'The length bound uses the vertical clipping quantity rho_m.','D7':'The final comparison is to L_m,alpha from (1.7).'},
 '4.1':{'D1':'The estimator targets Z(f) for every f in F.','D30':'Z-hat is explicitly the two-branch regression estimator in (4.5).','D22':'The risk is compared to the discrete-design benchmark R-tilde_z,n(sigma;f).'},
 '4.2':{'D1':'The interval covers Z(f) for every f in F.','D32':'CI_z,alpha is explicitly the regression interval (4.7), with both stopping branches.','D21':'The first assertion is a regression-model confidence-interval coverage property.','D24':'Its expected length is compared to the regression benchmark L-tilde_z,alpha,n.'},
 '4.3':{'D1':'M-hat estimates the minimum M(f) for every f in F.','D33':'M-hat is explicitly the regression block estimator (4.9), including its branch selection (4.8).','D23':'Its risk is compared to R-tilde_m,n(sigma;f) from the regression experiment.'},
 '4.4':{'D1':'The function-uniform assertion uses the same class F and the minimum target of (4.11).','D36':'CI_m,alpha is explicitly the regression interval (4.11), including Algorithm 2 when the finest scale is reached.','D21':'The coverage property belongs to the regression confidence-interval class.','D25':'The length is bounded by L-tilde_m,alpha,n from (4.2).'}
}
inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
data['schema_version']='statistical-ranked-interfaces-v4'
data['scope'].update(paper_count=1,source_policy='Pinned arXiv:2305.00164v2, 26 main-document pages, all eleven printed Theorems retained. The separate supplement is excluded.',normalization_policy='Preserve original statements, formulas and source discrepancies; normalize line wrapping and mathematical typesetting only. Source scope and interpretive issues are recorded separately.',semantic_ranking_policy='Direct theorem demand is distinct from propagated reach. Theorem proofs and performance intuitions do not create statement-dependency edges.',build_order_policy='Use the acyclic local graph and preserve separate white-noise and regression procedures. Shared Gaussian calibration quantities have no observation-model dependency; the two regression endpoint algorithms retain every printed branch.')
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
  for lid in path:evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
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
