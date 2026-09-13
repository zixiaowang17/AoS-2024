"""Resolve all seven theorem statements through the paper-local source graph."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={}
labels={'D2':'(E1)','D3':'(E2)','D4':'(F1)','D5':'(L1)','D6':'(L2)','D8':"(L1')",'D15':'(R1)','D16':'(R2)','D17':"(L2')",'D21':'(RE1)','D22':'(RE2)'}
for n in ['1','2','4','6','7','9']:
 base=['D2','D3','D4','D5','D15']
 base+=['D6'] if n in ['1','2'] else ['D16','D17']
 if n in ['6','7','9']:base+=['D8','D21']
 if n=='9':base+=['D22']
 DIRECT[n]={lid:(('The opening of Theorem '+n+' imports all assumptions of Theorem '+('4' if n=='6' else '6')+', including '+labels[lid]+'.') if n in ['6','7','9'] and lid not in (['D21'] if n=='6' else ['D22'] if n=='9' else []) else 'The theorem explicitly assumes '+labels[lid]+'.') for lid in base}
 if n=='2':
  for lid in base:DIRECT[n][lid]='Theorem 2 applies '+labels[lid]+' to all M chosen random samples, with the sample-local dimensions and scales of Section 3.3.1.'
for n in ['1','2','4']:
 DIRECT[n]['D8']="The final eigenvector-alignment clause adds (L1'); this distinctness condition is not imposed on the preceding Q-hat convergence assertion."
 DIRECT[n]['D7']='The differences use the normalized loading matrix Q_k and, in the final clause, the first z_k columns of the ordered SVD matrix U_k in (3.8).'
DIRECT['1'].update(D10='The estimator Q-hat-k-(z_k) and eigenvalue matrix V-double-dot-k are the full-fiber PCA quantities defined immediately before Theorem 1.',D9='The displayed transformation H-double-dot-k uses the normalized factor-sum matrix F-double-dot-k from (3.9).')
DIRECT['2'].update(D14='Q-hat-k-pre-(z_k), V-double-dot-k-pre and s_-k,pre are the selected-sample aggregate quantities in Section 3.3.2.',D11='The rate and transformation use sample-local d_-k,m, s_-k,m and normalized factor sums for every selected sample.')
DIRECT['4'].update(D11='The opening quantifies over random samples with n_l rows in every other mode, using the sampling scheme of Section 3.3.1.',D12='The theorem explicitly selects samples by the eigenvalue ratios defined in (3.14).',D14='The first error and final aligned error use the pre-averaging estimator.',D13='The second error uses the maximum eigenvalue ratio estimator.',D18='The population-parameter restatement uses the preceding selected-sample convention s_l,m asymptotic to s_l,max.')
for n in ['6','7','9']:
 DIRECT[n]['D18']='The all-assumptions reference to Theorem 4, directly or through Theorem 6, retains the selected-sample scaling convention preceding Theorem 4.'
 DIRECT[n]['D7']='The target U_k or U_k,(1) is the ordered loading SVD basis in (3.8).'
 DIRECT[n]['D20']='The statement uses the iterative projection direction and covariance of Algorithm (4.4), including its pre-averaging initialization.'
DIRECT['6']['D17']='Theorem 6 imports (L2\') from Theorem 4 and uses c_j,max in b_k; c_j,max uses the maximum selected-sample scales of (3.17).'
DIRECT['8']={'D2':'The opening explicitly assumes (E1).','D4':'The opening explicitly assumes (F1).','D22':'The opening explicitly assumes (RE2), including its row-norm and noise-growth restrictions.','D23':'The correlation matrix defined in Theorem 8 normalizes the population-style covariance Sigma_y,m+1^(k) in (5.4).'}
DIRECT['9'].update(D23='The population correlation eigenvalues in the comparison are those of Theorem 8, defined by normalizing the covariance (5.4).',D24='The left-hand eigenvalues belong to the sample correlation matrix in (5.1).',D25='The final consistency assertion uses the core rank estimator r-hat_k defined in (5.2).')
inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
data['schema_version']='statistical-ranked-interfaces-v4'
data['scope'].update(paper_count=1,source_policy='Pinned arXiv:2208.04012v1, 80 PDF pages, main text pages 1-38 only. Seven printed Theorems, numbered 1, 2, 4, 6, 7, 8 and 9; appendices excluded.',normalization_policy='Preserve original statements and source inconsistencies; normalize line wrapping and mathematical typesetting only. Archive inferred resolutions and unresolved meanings separately.',semantic_ranking_policy='Retain every inventoried main-text Theorem. Count direct theorem demand independently of propagated dependency reach. No proof-only edges.',build_order_policy='Derive a DAG from paper-local mathematical dependencies; keep full-sum, sample-wise and selected-maximum assumptions distinct. Estimator definitions do not import assumptions used only for their rate analysis.')
data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
for c in data['claims']:
 n=c['claim_id'].split('/T')[-1];direct=DIRECT[n];c['depends_on']=list(direct)
 for x in data['interfaces']:
  lid=x['members'][0]['local_id']
  if lid in direct:x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=direct[lid],evidence=c['evidence']))
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
  own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems']);selectors=m['highlight_symbols']+m['highlight_phrases']
  assert any(s in own for s in selectors),(m['local_id'],'source highlight')
  assert all(s in linked for s in selectors),(m['local_id'],'unmatched selector')
attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
(ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
print('Census finalized and independently validated; final semantic source review remains.')
