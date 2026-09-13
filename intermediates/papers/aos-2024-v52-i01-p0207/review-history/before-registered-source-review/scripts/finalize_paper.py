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

DIRECT={'1': {'D14': 'The supremum is over the general parameter space Pi(K,beta,alpha,gamma,kappa) defined at the end of Section 2.2.', 'D4': 'The bounded quantity is expected regret E[R_nQ(pi)] defined in (2).', 'D23': 'The statement explicitly specifies the policy given by Algorithm 1.'}, '2': {'D14': 'The supremum ranges over the general parameter space Pi(K,beta,alpha,gamma,kappa) of Section 2.2.', 'D4': 'The lower bound concerns expected regret E[R_nQ(pi)] from (2).', 'D6': 'The infimum over pi is interpreted by the admissible-policy passage immediately following Theorem 2.'}, '3': {'D27': 'The supremum uses the self-similar space Pi(K,beta,alpha,gamma,kappa,l0,b) defined in Section 4.1.', 'D4': 'The bounded quantity is expected regret E[R_nQ(pi^a)] from (2).', 'D31': 'The statement explicitly specifies the adaptive policy pi^a yielded by Algorithm 2.', 'D13': 'The opening hypothesis requires kappa asymptotically comparable to one; kappa is the exploration coefficient of Definition 2.'}, '4': {'D27': 'The supremum uses the self-similar space Pi(K,beta,alpha,gamma,kappa,l0,b) of Section 4.1, with the existence and constant dependence of b stated in this theorem.', 'D4': 'The lower bound concerns expected regret E[R_nQ(pi)] from (2).', 'D6': 'The paragraph after Theorem 4 explicitly identifies the infimum with the admissible policies of Theorem 2.', 'D7': 'The constant b may depend on C_beta, the common Holder constant in Assumption 1.', 'D10': 'The specified dependence of b includes q-under and q-over, the two ball-mass constants in Assumption 3.'}}

def main():
    save_passages()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Pinned arXiv:2211.12612v2 PDF with matching-version TeX assistance. All four main-text Theorems and relevant passages checked against printed pages; appendices excluded.',
        normalization_policy='Preserve printed wording, formulas, labels and source inconsistencies; expand macros and normalize line wrapping and typographic emphasis. The matching TeX is archived; mathematical expressions and equation numbers are checked against the PDF.',
        semantic_ranking_policy='All four inventoried Theorems retained; direct demand counted once per theorem and interface, independently of proof use.',
        build_order_policy='Derive from the acyclic same-paper dependency graph; known-parameter and adaptive algorithm dependencies remain distinct at the paper-local member level.')
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
