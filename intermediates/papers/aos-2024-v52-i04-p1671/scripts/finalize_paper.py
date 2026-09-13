"""Attach paper-local statement dependencies and derive the census."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
'1':{'D1':'Theorem 1 asserts distributed group differential privacy, as defined for whole-machine replacement in Definition 1.',
     'D9':'The subject of the privacy assertion is the DPVote mechanism in Algorithm 2.'},
'2':{'D2':'The margin condition is evaluated for each row Q_l^r of the given sign matrix.',
     'D3':'The target in both the utility argument and conclusion is the non-private majority vector Q-bar from (2).',
     'D4':'The selection budget is compared with s-bar, the support size of the majority vector, rather than population sparsity s.',
     'D6':'Condition (6) uses f_l(Q_l^r,Q-bar_l) from (5); its null-sign utility is distinct from the signed peeling score f^S.',
     'D9':'The returned pair of support and signs is the Algorithm 2 output, with probability explicitly over algorithm randomness.'},
'3':{'D11':'The estimator Q-hat(X) is explicitly defined by Algorithm 3: thresholded local sample means followed by DPVote.',
     'D12':'The opening refers to the mean-law family from (10), printed as blackboard P in the theorem and calligraphic P in its definition. Its third absolute moment restriction belongs to that family.'},
'4':{'D14':'The random maximum of local penalties in (19) uses lambda_j from (15); the bound is required with probability tending to one.',
     'D15':'The estimator in the conclusion is explicitly the DPVote Lasso procedure in Algorithm 4.',
     'D16':'The sampling law is the joint distribution space (17), including spectral bounds, exponential square moments and independence of the residual.'}}
def extra(n):
    return []

def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
      source_policy='Verified local arXiv:2209.04419v2 PDF; main text and references on pages 1–28; appendix bodies excluded.',
      normalization_policy='Preserve four complete source Theorems, including Theorem 4 continuation. Do not repair ambiguous thresholds, output conventions or unquantified constants in original statements.',
      semantic_ranking_policy='Resolve explicit theorem objects and recursive algorithm bodies; distinguish majority support from population support and privacy claims from sign consistency. Do not import proof-only sensitivity or composition lemmas as dependencies.',
      build_order_policy='Derive all canonical edges and theorem reach from the inspected paper-local graph.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                evidence=list(c['evidence'])+extra(n)
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=evidence))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
            sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])+extra(n)
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
    finalized=json.loads((ROOT/'ranked-interfaces.json').read_text())
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=[m for x in finalized['interfaces'] for m in x['members']]),indent=2,ensure_ascii=False)+'\n')
    print('Census structurally valid; independent full source review remains pending.')
if __name__=='__main__':main()
