"""Derive all four theorem connections from their main-text definitions and hypotheses."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
C1={'D3':'Condition 1(a) specifies the common covariance and standardized innovation designs.','D4':'Condition 1(b) specifies the known population blocks and aligned design submatrices.','D5':'Condition 1(c) defines the population ESDs and their limiting spectral laws H_l,H.','D6':'Condition 1(d) specifies the three global and block aspect-ratio limits.'}
DIRECT={
 '1':{**C1,'D10':'Both trace conclusions use the block training covariance Sigma-hat_B.','D13':'Both trace conclusions use the full training covariance Sigma-hat.','D19':'Theorem 1 names the sample law M_l and its transform m_l and uses m_l(-lambda).'},
 '2':{**C1,'D2':'The theorem explicitly assumes the polygenic model (1).','D7':'The theorem explicitly requires Condition 2 on the causal fraction.','D8':'The theorem explicitly requires Condition 3 on random effects and noise.','D22':'The theorem explicitly requires Condition 4 on the two training trace ratios.','D9':'Both accuracy formulas and lambda-star use h_beta^2, defined from training signal and noise energies.','D14':'The target A_B^2 is the prediction accuracy of beta-hat_B by the sentence immediately preceding the theorem.','D17':'A_B^2 instantiates the out-of-sample accuracy functional with the training-block ridge estimate.','D19':'R_3 explicitly uses the training sample transforms m_l and m_h.'},
 '3':{**C1,'D11':'The two traces and the K_l definition use reference covariance Sigma-hat_BW_l.','D20':'The K_l definition explicitly uses the companion reference transform v_w_l(-lambda).'},
 '4':{**C1,'D2':'The theorem explicitly assumes the polygenic model (1).','D7':'The theorem explicitly requires Condition 2 on the causal fraction.','D8':'The theorem explicitly requires Condition 3 on effects and noise.','D23':'The theorem explicitly requires Condition 5, with its four reference/testing matrix ratios.','D9':'Both accuracy expressions use the training heritability h_beta^2.','D15':'A_BW^2 is the accuracy of the external-reference ridge estimator, as stated immediately before the theorem.','D16':'A_BZ^2 is the accuracy of the testing-panel ridge estimator, as stated immediately before the theorem.','D17':'Both targets are instances of the same squared-cosine out-of-sample accuracy.','D20':'The Q_2 and Q_3 formulas use K_l, whose definition in Theorem 3 involves v_w_l(-lambda).'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned 60-page arXiv:2203.12003v1 artifact with margin date 22 March 2022 and title-page date 13 June 2025. Main text and references are pages 1–27; attached supplementary mathematics on pages 28–60 is excluded.',
     normalization_policy='Preserve all four full Theorems, all conditions and original definitions. Keep bold matrix/scalar labels, nested indices, printed sample-size factors and derivative signs.',
     semantic_ranking_policy='Use only direct statement dependencies and recursive local definitions. Trace-only Theorems 1 and 3 must not acquire response, effect, heritability or ridge-estimation hypotheses.',
     build_order_policy='Keep the three covariance sources and their estimators distinct. Condition 5 reuses only the causal-submatrix notation from Condition 4, not its separate assumptions. Local scalar trace abbreviations remain in the complete statements.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
            sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])
            for lid in path:
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                for ctx in members[lid].get('application_context',[]):
                    evidence.extend(e for e in ctx['evidence'] if e not in evidence)
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
    print('Finalized and independently validated; final source audit remains.')


if __name__ == "__main__":
    main()
