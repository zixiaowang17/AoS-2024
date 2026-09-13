"""Derive and validate this paper's census from its reviewed inventory and local graph."""
import copy
import json
import subprocess
import sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges,main as save_passages

SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory

DIRECT={'3.1': {'D1': 'The asymptotic law concerns statistics of the iid sample with continuous marginals specified in Section 1.', 'D4': 'The first assertion explicitly assumes H_5 and the joint assertion H_(4m-3), both instances of equation (1.4).', 'D9': 'Both limits use the subset aggregations T_n(k) defined in equation (3.1).', 'D10': 'The theorem centers by nu_n(k), scales by delta_n(k), and ends with the printed bar-delta_n(m) replacement from equation (3.2).'}, '6.5': {'D11': 'The theorem quantifies over a zero-mean square-integrable martingale array, defines its differences X_n,r, and requires cross-row inclusion of its filtrations.', 'D12': 'The first conditional convergence hypothesis is precisely the displayed Lindeberg condition (6.24), including its printed first power of X_n,r.', 'D13': 'The final clause asserts that the conditional fourth-moment Lyapunov condition (6.26) suffices for (6.24); it is not imposed in addition to (6.24).'}}

def main():
    save_passages()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Pinned arXiv:2204.01803v1, 51 PDF pages. Two main-text Theorems and extracted passages checked against pages 1-30; supplementary appendices beginning on page 31 excluded.',
        normalization_policy='Preserve printed wording, formulas, labels and source inconsistencies; transcribe mathematical expressions into LaTeX and normalize line wrapping and typographic emphasis only. The printed PDF supplies original wording and numbering; possible source errors remain explicit review notes.',
        semantic_ranking_policy='Both inventoried Theorems retained; direct demand counted once per theorem and interface, independently of proof use.',
        build_order_policy='Derive from the acyclic same-paper dependency graph; the rank-based copula statistic and generic martingale-array theorem retain separate dependencies; a proof use does not add a statement dependency.')
    data['interfaces']=copy.deepcopy(interfaces)
    claims={c['claim_id']:c for c in data['claims']}
    for c in data['claims']:
        number=c['claim_id'].split('/T')[-1]
        direct=DIRECT[number]
        c['depends_on']=list(direct)
        for x in data['interfaces']:
            used=[m['local_id'] for m in x['members'] if m['local_id'] in direct]
            if used:
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+x['interface_id'].split('/')[-1],
                    paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=' '.join(direct[lid] for lid in used),evidence=c['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];number=cid.split('/T')[-1]
            sentences=[DIRECT[number][path[0]]]
            evidence=list(claims[cid]['evidence'])
            for lid in path:
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
            for a,b in zip(path,path[1:]):sentences.append(edges[a][b])
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=' '.join(sentences),evidence=evidence)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
            linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors),(m['local_id'],'no source highlight')
            assert all(s in linked for s in selectors),(m['local_id'],'unmatched selectors',[s for s in selectors if s not in linked])
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('All source highlight selectors matched. Census finalized and independently validated; final source-audit record remains.')

if __name__=='__main__':main()
