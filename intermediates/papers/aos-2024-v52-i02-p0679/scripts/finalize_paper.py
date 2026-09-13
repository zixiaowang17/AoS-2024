"""Derive all seven theorem connections without importing proof-only requirements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
BASE={
 'D3':'The statement expressly assumes positivity (I), the strict lower propensity bound.',
 'D4':'The statement expressly assumes causal consistency (II).',
 'D5':'The statement expressly assumes sequential ignorability (III).',
 'D7':'The statement expressly assumes the three integrability requirements in (IV).'
}
DIRECT={
 '1':{'D16':'The conclusion is failure of Fisher consistency for two-stage DTR, using the sequential all-laws definition in Definition 1.','D17':'The first hypothesis calls psi closed, defined immediately before the theorem as upper semicontinuity.','D18':'The theorem assumes strict concavity, with the printed preceding source convention archived separately.'},
 '2':{**BASE,'D8':'The stage conclusions compare the surrogate rules with the optimal rules d_1*,d_2* from (4).','D12':'The rules with tildes are induced by surrogate maximizing scores as specified in (8).','D20':'The first-stage branch is determined by the strict reward comparison (13).','D29':'The theorem explicitly chooses the bivariate hinge function psi(x,y)=min(x,y,1).'},
 '3':{**BASE,'D13':'The inequality compares true regret V*-V with surrogate regret V_psi*-V_psi.','D19':'The stated product psi(x,y)=phi(x)phi(y) uses Condition 2 and its constant C_phi.'},
 '4':{**BASE,'D13':'The conclusions bound the surrogate regret at the two scaled approximating scores.','D14':'The approximation condition explicitly uses eta_1 and eta_2 from (9) and (10).','D24':'The hypothesis explicitly includes the outcome upper bound in Assumption A.','D25':'The hypothesis includes Assumption B with its small-noise coefficient alpha.','D27':'The first conclusion assumes phi of type A from Definition 2 and separates cases at kappa=2+alpha.','D28':'The continuation on page 24 gives the separate conclusion for phi of type B from Definition 2.'},
 '5':{**BASE,'D13':'The bound concerns population surrogate regret of the fitted classifiers.','D14':'Condition (22) explicitly approximates eta_1-1/2 and eta_2-1/2.','D19':'The Section 4 convention fixes the product surrogate with phi satisfying Condition 2 throughout these later results.','D22':'The fitted pair and the approximating pair belong to the product search class U_n.','D23':'The maximum in the bound includes the empirical optimization error Opt_n.','D24':'The theorem expressly assumes the outcome upper bound A.','D25':'The theorem expressly assumes the small-noise condition B with alpha>0.','D31':'The opening sentence requires the sup-norm bracketing condition (21) with the displayed extra growth restrictions.'},
 '6':{**BASE,'D13':'The approximation assumption and the conclusion both use surrogate regret relative to V_psi*.','D19':'The Section 4 product-surrogate convention with Condition 2 remains in force.','D22':'The supremum and fitted pair range over U_n, with its stage factors specified in Section 6.','D23':'The theorem explicitly requires Opt_n<1/2 and retains Opt_n in its upper bound.','D24':'The assumptions include the outcome bound A.','D26':'The theorem assumes C, the printed strong-separation condition, instead of B.','D30':'The referenced condition (23) is a bound on log N_[ ] with empirical L2 norm; the exact formula is archived as an auxiliary passage.'},
 '7':{**BASE,'D13':'Both (25) and the final inequality concern surrogate regret relative to V_psi*.','D19':'The Section 4 product-surrogate convention with Condition 2 remains in force.','D22':'The theorem assumes the fitted pair belongs to U_n and takes a population supremum over that class.','D23':'Its probability bound retains the empirical optimization gap Opt_n without adding the Opt_n<1/2 restriction of Theorem 6.','D24':'The theorem expressly assumes the outcome bound A.','D26':'It expressly assumes the printed strong-separation condition C.','D30':'The inline condition (24) bounds the bracketing number N_[ ] itself in empirical L2, unlike the logarithmic bound (23).'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned arXiv:2111.02826v4, all 50 main-paper pages. The supplement linked on physical page 43 is a separate document and was not opened. Preserve exactly seven printed Theorems in source order.',
     normalization_policy='Keep full original statements, source labels, causal assumptions, value formulas and derivative/entropy conditions. Preserve inconsistent source coding and domain conventions in separate notes.',
     semantic_ranking_policy='Direct statement dependencies and recursive same-paper reach. Statistical examples, proof-only assumptions and conclusions that imply another property do not create statement dependencies.',
     build_order_policy='Keep generic surrogate values separate from the later product-surrogate family; distinguish small noise, literal strong separation, derivative types and the three bracketing conditions.')
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
