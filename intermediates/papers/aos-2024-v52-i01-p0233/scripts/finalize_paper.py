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

DIRECT={'1': {'D3': 'The loss uses the initial-distribution value V^(pi-hat)(rho), defined by (10)-(12).', 'D5': 'The benchmark V-star(rho) specializes the value to the fixed optimal policy in (15).', 'D12': 'The statement explicitly specifies the policy returned by Algorithm 1 and its required iteration count.', 'D11': 'The sufficient condition explicitly invokes the Bernstein-style penalty (28) and its constant c_b.', 'D8': 'The sample-size bound (35) explicitly uses C-star-clipped from Definition 2.', 'D7': 'The final sentence explicitly also permits C-star from Definition 1 in place of C-star-clipped.'}, '2': {'D1': 'The constructed objects M_0 and M_1 are discounted MDPs with the stated gamma and S.', 'D3': 'The two error probabilities use the initial-distribution value of the estimated policy.', 'D5': 'Both errors compare that value to the optimal benchmark V-star(rho).', 'D6': 'The statement explicitly constructs a batch data set of N independent samples, with the Section 2.1 sampling convention.', 'D8': 'Its premise and sample-size inequality use the single-policy clipped concentrability coefficient from Definition 2.'}, '3': {'D15': 'The assertion concerns V_1^(pi-hat)(rho), the step-one weighted value defined in (38)-(40).', 'D17': 'The benchmark V_1-star(rho) uses the optimal deterministic finite-horizon policy.', 'D24': 'The statement explicitly invokes the policy returned by Algorithm 3, including its subsampling stage.', 'D22': 'The hypothesis explicitly requires the Bernstein-style penalty quantity (55) and a sufficiently large c_b.', 'D20': 'The trajectory-count bound (59) explicitly uses C-star-clipped from Definition 4.', 'D19': 'The last sentence explicitly allows C-star from Definition 3 as an alternative.'}, '4': {'D13': 'The constructed family consists of finite-horizon MDPs with parameters H and S.', 'D15': 'The error event uses the estimated policy value V_1^(pi-hat)(rho).', 'D17': 'The same event compares against V_1-star(rho), the optimal finite-horizon value.', 'D18': 'The statement explicitly specifies K independent trajectories each of length H and the total transition count N=KH.', 'D20': 'The premise C-star-clipped>=8/S and the bound (61) use the finite-horizon clipped concentrability coefficient of Definition 4.'}}

def main():
    save_passages()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Published DOI 10.1214/23-AOS2342 PDF, 28 pages. Four main-text Theorems and all extracted passages checked against the printed source. Separate supplement excluded.',
        normalization_policy='Preserve printed wording, formulas, labels and source inconsistencies; transcribe mathematical expressions into LaTeX and normalize line wrapping and typographic emphasis only. The printed PDF supplies original wording, numbering and algorithm nesting.',
        semantic_ranking_policy='All four inventoried Theorems retained; direct demand counted once per theorem and interface, independently of proof use.',
        build_order_policy='Derive from the acyclic same-paper dependency graph; discounted and finite-horizon models, sampling laws, penalties and coefficients remain separate at the paper-local level.')
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
