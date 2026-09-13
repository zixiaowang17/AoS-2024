"""Derive all seven theorem dependency sets from source-checked statements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '3.1':{'D3':'The theorem explicitly assumes the true regression function belongs to the signed-measure MARS class.','D5':'The true function must satisfy the MARS complexity bound V_mars(f*)<=V.','D12':'The theorem explicitly requires the lattice design (15), including its lower spacing parameter rho.','D13':'The surrounding fixed-design setup (16) supplies the independent mean-zero sub-Gaussian errors and parameter sigma appearing in the bound.','D6':'The bound concerns the exact constrained estimator hat-f_{n,V}^{d,s} from (7).','D14':'The left side is its fixed-design expected empirical risk R_F.'},
 '3.2':{'D15':'The entropy bound is for the signed-hinge integral class D_m defined immediately before the theorem.','D22':'The left side log N(epsilon,D_m,L2) is the metric entropy named by the preceding prose.'},
 '3.4':{'D3':'The theorem explicitly restricts f* to the original signed-measure MARS class.','D5':'The true function satisfies V_mars(f*)<=V.','D12':'The theorem explicitly assumes lattice design (15).','D13':'Section 3.1 supplies the fixed-design sub-Gaussian regression model and its sigma.','D11':'The bound concerns the fixed-grid approximate estimator tilde-f_{n,V}^{d,s}.','D14':'Its performance is measured by the fixed-design empirical risk R_F.','D8':'The approximation remainder uses N=min_k N_k, the minimum of the preselected knot-grid resolutions.'},
 '3.5':{'D3':'The true function is explicitly in the signed-measure MARS class.','D5':'Its complexity is at most V.','D6':'The rate is for the exact constrained estimator hat-f_{n,V}^{d,s}.','D16':'The random-design section assumes iid covariates with density p0 bounded above by B.','D17':'The section also assumes the independent iid mean-zero errors with finite L^{5,1} norm in (20)–(21).','D18':'The squared norm on the left side is population L2 error under p0 from (22), bounded in probability.'},
 '3.6':{'D15':'The bracketing bound concerns the same class D_m of signed-hinge integrals.','D21':'The theorem explicitly identifies N_{[ ]}(epsilon,D_m,L2) as its bracketing number.'},
 '3.8':{'D3':'The theorem explicitly places f* in the original MARS class.','D5':'It explicitly bounds V_mars(f*) by V.','D11':'The rate concerns the approximate estimator tilde-f_{n,V}^{d,s}.','D8':'The stated growth condition applies to the minimum of the preselected resolutions N_k.','D16':'The random-design density p0 and its upper bound B come from Section 3.2.','D17':'The rate uses the random-design regression and L^{5,1} noise setup (20)–(21).','D18':'The left side is squared population L2 error under p0, rather than expected risk.'},
 '3.9':{'D19':'The left side is fraktur M_{n,V}^{d,s}, the infimum of the worst expected population loss over all data-based estimators.','D20':'The immediately preceding paragraph adds Gaussian noise with variance sigma^2 and the stated positive lower-density restriction, supplying b,B,sigma in the bound.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned 108-page arXiv:2111.11694v5. Main text and references occupy pages 1–25; all appendix material from page 26 is excluded.',
     normalization_policy='Preserve all seven full Theorems and original main-text definitions. Keep fraktur minimax M, script F,D,R, exact versus approximate estimators, half-open versus closed knot domains and all source conditions distinct.',
     semantic_ranking_policy='Count statement prerequisites and recursive definitions only. Entropy bounds do not inherit regression sampling conditions; risk statements do not inherit entropy or Brownian-sheet proof machinery.',
     build_order_policy='Derive paper-local dependencies without adding appendix proofs or alternative Hardy–Krause characterizations. Reuse coefficient objective and reconstruction formulas with the explicitly stated approximate-grid instantiation.')
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
    finalized=json.loads((ROOT/'ranked-interfaces.json').read_text())
    passages=dict(paper_id=PID,members=[m for x in finalized['interfaces'] for m in x['members']])
    (ROOT/'source-passages.json').write_text(json.dumps(passages,indent=2,ensure_ascii=False)+'\n')

if __name__ == "__main__":
    main()
