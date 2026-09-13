"""Attach source-reviewed theorem-to-interface paths and finalize this paper."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT = {'2.1': {'D1': 'The conclusion explicitly concerns the ESD of S_n Theta_n.', 'D2': 'The limit F is named the limiting spectral distribution.', 'D3': 'The statement characterizes the Stieltjes transform m(z) of F.', 'D6': 'The matrix S_n is the masked-observation Gram matrix defined in Section 2.1.', 'D7': 'The spectral argument includes the auxiliary matrix Theta_n.', 'D10': 'The opening Assumptions A-D explicitly includes the latent sub-Gaussian assumption A.', 'D11': 'The opening Assumptions A-D explicitly includes independence and nonrandomness in B.', 'D12': 'Assumption C supplies y in the fixed-point equation.', 'D13': 'Assumption D supplies the limiting law H in the equation.', 'D16': 'Convergence of the ESD with high probability has exactly the meaning in Definition 2.2.'}, '2.2': {'D6': 'The statement concerns eigenvalues of the original Gram matrix S_n times Theta_n.', 'D7': 'The matrix product explicitly includes the auxiliary Theta_n.', 'D14': 'The no-eigenvalue conclusion is stated with high probability, using the event convention on page 3.', 'D17': 'The support exclusion names the limiting and finite-parameter laws; the printed c and c_n are retained as notation inconsistencies relative to y and y_n in the preceding paragraph.', 'D10': 'Section 2.5 continues the model and Assumptions A-D of Section 2.2; A is an inherited model condition, not repeated in the printed theorem.', 'D11': 'The same Section 2 model inherits the independence and deterministic-auxiliary condition B; it is not an additional phrase in the original body.', 'D12': 'The high-dimensional regime is inherited from Section 2 Assumption C; the body switches notation to c and c_n.', 'D13': 'The laws used in the support condition are the IPSD-based laws from the standing Assumption D.'}, '2.3': {'D6': 'The CLT vector is evaluated at the original Gram matrix S_n.', 'D7': 'The vector argument and the displayed spectral interval both contain auxiliary Theta_n.', 'D10': 'The statement explicitly assumes A-D and uses nu_4 from A in both limiting parameters.', 'D11': 'The statement explicitly includes B through Assumptions A-D.', 'D12': 'The aspect ratio y in the interval and integrals is from Assumption C.', 'D13': 'Assumption D supplies H, Psi_n and the covariance sequence in the formulas.', 'D17': 'The underlined transform in the mean and covariance is the limiting companion-transform notation associated with the preceding finite-transform relations; its unindexed definition is an unresolved source convention recorded separately.', 'D18': 'The CLT vector explicitly uses centralized L^c as defined at the start of Section 2.6.', 'D19': 'The inline definitions of a(z) and d_2(z_1,z_2) evaluate the original I_2 functional.', 'D20': 'The same two limiting parameters evaluate the original II functional with factor nu_4-3.'}, '3.1': {'D22': 'The opening Under H_0 refers to the covariance-equality null in Section 3.1.', 'D24': 'The two limit statements concern the calligraphic T_L and T_F statistics defined immediately above.', 'D23': 'All four centering and variance formulas use the scalar a_P,Sigma defined in Corollary 2.1; the bold/plain Sigma variation is preserved in the originals.', 'D12': 'The centering and variance formulas use y_n=p/n from the section convergence regime.', 'D10': 'Section 3.1 adopts the previous data model, and the preceding renormalized CLT assumes Theorem 2.3 conditions; A is retained as inherited context, rather than inserted into the printed Under H_0 statement.', 'D11': 'The Section 3 test application retains data-mask independence from the preceding model; its normalization matrix is fixed under the given covariance null. This is inherited context for B.', 'D13': 'The test application follows the renormalized CLT built under the preceding population spectral assumptions; D is retained as inherited context and its T_n also occurs in the defining scalar a_P,Sigma.'}}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Verified registered published PDF, 22 pages, DOI 10.1214/24-AOS2392; external supplementary material excluded.',
        normalization_policy='Preserve all four complete original Theorem statements, including the page-11 contour continuation. Keep source notation inconsistencies separate from the untouched statements.',
        semantic_ranking_policy='Count direct and recursively resolved same-paper statement dependencies. Distinguish explicitly named Assumptions A-D from assumptions inherited through the section model; exclude proof-only epsilon-net and martingale tools.',
        build_order_policy='Derive the graph from original local definitions, retain source conditions and unresolved meanings, and do not infer library availability.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                evidence=list(c['evidence'])
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=evidence))
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
            own=m['statement_original']+' '+m['local_label']
            linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors),(m['local_id'],'missing source highlight')
            assert all(s in linked for s in selectors),(m['local_id'],'unmatched selector')
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Structural validation passed; independent full source audit remains pending.')
    finalized=json.loads((ROOT/'ranked-interfaces.json').read_text())
    passages=dict(paper_id=PID,members=[m for x in finalized['interfaces'] for m in x['members']])
    (ROOT/'source-passages.json').write_text(json.dumps(passages,indent=2,ensure_ascii=False)+'\n')

if __name__ == "__main__":
    main()
