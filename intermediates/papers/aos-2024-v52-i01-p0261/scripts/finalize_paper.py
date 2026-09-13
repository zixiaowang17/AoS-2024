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

DIRECT={'2.1': {'D4': 'The minimax risk is the expected loss L from (6), minimized over a shared circular rotation.', 'D5': 'The supremum explicitly ranges over the power-law magnitude class Theta_beta of (7).', 'D6': 'The paragraph following Theorems 2.1 and 2.2 defines the expectation, all-estimator infimum and the constants allowed in the asymptotic comparison.'}, '2.2': {'D4': 'The risk is the expected rotation-invariant loss L from (6).', 'D5': 'The supremum is over the same two-sided magnitude class Theta_beta of (7).', 'D6': 'The shared convention following both minimax theorems defines the sampling expectation, estimator infimum and asymptotic comparison.'}, '4.1': {'D3': 'The expected loss uses the model (5); Section 4 explicitly abbreviates E_theta-star as E.', 'D4': 'The bounded risk is E[L(theta-hat,theta-star)], using (6).', 'D2': 'The explicit assumption r_k>=r-under>0 concerns the Fourier magnitudes defined by the polar coefficient representation.', 'D10': 'One explicitly permitted estimator is theta-hat-oracle, with the true-phase argument choice of Section 4.1.', 'D11': 'The other explicitly permitted estimator is theta-hat-opt, with the pilot optimization and argument lift of Section 4.2.'}, '5.2': {'D3': 'E_theta-star is expectation under the rotated Gaussian sequence model (5).', 'D4': 'The conclusion bounds the expected rotation-invariant loss L.', 'D12': 'The assertion explicitly concerns theta-hat-MLE, defined in Section 5 by minimizing the negative empirical marginal log-likelihood.', 'D13': 'The opening sentence explicitly invokes Assumption 5.1 and the constants are allowed to depend only on its c_gen.'}}

def main():
    save_passages()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Published DOI 10.1214/23-AOS2346 PDF, 24 pages. Four main-text Theorems and all extracted passages checked against the printed source. Separate supplement excluded.',
        normalization_policy='Preserve printed wording, formulas, labels and source inconsistencies; transcribe mathematical expressions into LaTeX and normalize line wrapping and typographic emphasis only. The printed PDF supplies original wording, numbering and algorithm nesting.',
        semantic_ranking_policy='All four inventoried Theorems retained; direct demand counted once per theorem and interface, independently of proof use.',
        build_order_policy='Derive from the acyclic same-paper dependency graph; minimax all-estimator statements, oracle/optimization estimator choices and the general likelihood assumption retain their separate local dependencies.')
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
