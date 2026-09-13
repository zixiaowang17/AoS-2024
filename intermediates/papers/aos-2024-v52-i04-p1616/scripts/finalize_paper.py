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
'1':{'D6':'The left side S_epsilon^2 is the second component of the decomposition (8), introduced under the Section 3.2 centering convention.',
     'D3':'The variational objective contains the EOT problem OT_A,epsilon defined by (4).',
     'D7':'The theorem explicitly binds the cost c_A used in that EOT problem.',
     'D10':'The opening uses the finite fourth-moment classes, and M_mu,nu is the geometric mean of the second absolute moments.'},
'2':{'D5':'Both errors concern the entropic GW functional S_epsilon from Section 2.2.',
     'D8':'The one- and two-sample errors use the empirical measures defined just before the theorem.',
     'D9':'Both population distributions are explicitly 4-sub-Weibull with a common parameter sigma squared.'},
'3':{'D4':'The bounds estimate the squared quadratic GW distance D squared, with an additional unsquared clause for separated populations.',
     'D8':'The errors compare the population functional to one- and two-sample empirical measures.'}}
def extra(n):
    return [dict(page=8,location='Section 3.2 centering and decomposition convention')] if n=='1' else []

def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
      source_policy='Registered arXiv:2212.12848v3 PDF, 47 pages; main paper and references on pages 1-28 only.',
      normalization_policy='Preserve all three original Theorems and their existing stable IDs. Distinguish the decomposition component from a square and retain complete rate bounds and clauses.',
      semantic_ranking_policy='Resolve source moments, coupling, entropy, transport, empirical measures and the centered decomposition. Keep proof-only OT potentials, empirical-process classes and lower-bound constructions out of theorem dependencies.',
      build_order_policy='Derive edges and reach from paper-local dependencies without altering the independent inventory.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split(':theorem-')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split(':theorem-')[-1];c['depends_on']=list(DIRECT[n])
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
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split(':theorem-')[-1]
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
