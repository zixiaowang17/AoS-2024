"""Finalize the source-local transport census; a separate source audit is still required."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{'D1':'Theorem 1 is under the standing Euclidean support condition (S1) in Section 2.1.','D2':'Its hypotheses distinguish absolutely continuous P from arbitrary probability Q.','D3':'Both assertions concern the Monge optimal map and the pushforward equation.','D7':'Part (ii) uses the conjugate potential and its gradient.','D8':'Part (i) explicitly requires the potential to solve semi-dual problem (12).'},
 '3':{'D1':'The theorem explicitly assumes condition (S1).','D9':'The regularity conclusions concern the population Brenier potential varphi_0.','D11':'Both density hypotheses and potential conclusions use the declared Hölder spaces, including the interior norm.'},
 '5':{'D15':'P and Q are absolutely continuous torus measures with the displayed density bounds.','D18':'The norm conclusion concerns the convex lift varphi_0 of the torus optimal map, introduced in Proposition 4 and reused in Section 4.3.','D11':'The density hypotheses use the torus Hölder class and the conclusion uses a Hölder norm on the unit cube.'},
 '6':{'D1':'Section 3 explicitly retains (S1) for its deterministic stability statement.','D2':'The theorem allows an arbitrary estimated probability law but assumes absolutely continuous population laws.','D3':'The hatted map is defined inline as the optimal map from P to the estimated target.','D9':'T_0 is the population optimal map induced by the Brenier potential.','D10':'The remainder subtracts the integral of the target Kantorovich potential psi_0.','D20':'The theorem explicitly requires A1(lambda), the two-sided population Hessian condition.','D5':'Both sides of (16) use Euclidean Wasserstein costs.'},
 '10':{'D1':'The one-sample section retains (S1), here with the unit cube explicitly specified.','D21':'The expectation is over the iid target sample in the one-sample observation model.','D25':'Theorem 10 analyzes the wavelet specialization of the plugin map (26).','D9':'Both assertions concern the population map and its convex potential.','D20':'Part (i) explicitly assumes A1(lambda).','D12':'Part (ii) puts the conjugate potential in the norm-only Hölder ball with bound lambda.','D13':'The target density belongs to the positive Hölder ball with bounds M and gamma.','D7':'Part (ii) refers to the Legendre-Fenchel conjugate varphi_0-star.','D10':'The variance term is that of the target Kantorovich potential psi_0(Y).','D5':'The second assertion estimates the squared Euclidean Wasserstein distance.'},
 '18':{'D15':'The population laws are absolutely continuous torus measures.','D18':'The risk compares the estimated map with the population torus optimal map T_0.','D19':'The second risk bound contains the variances of the torus Kantorovich potentials phi_0(X) and psi_0(Y).','D13':'Both density hypotheses use the positive Hölder ball on the torus.','D26':'The two iid samples are explicitly independent in the Section 4.3 preamble.','D27':'The distance estimates use the normalized periodic kernel density measures.','D28':'The theorem explicitly requires K1(2alpha,kappa).','D29':'The map estimate is the optimal transport map between those kernel measures.','D17':'The Wasserstein target and estimates use torus cost (15).'},
 '20':{'D30':'The theorem explicitly assumes the generic smooth-domain condition (C1).','D31':'Only its two-sample assertion additionally assumes (C2).','D35':'Both densities belong to the constrained positive Hölder ball with Neumann conditions.','D33':'The constant explicitly depends on the smooth cutoff tau used in the estimators.','D36':'The two risks concern the barred population-source map and hatted estimated-source map built from the spectral density estimates.','D9':'The one-sample regularity assumption and both targets refer to the Euclidean population Brenier potential and map.','D12':'Part (i) places varphi_0 in the norm-only C2 ball with bound M.','D40':'The expectations use the smooth-domain iid observation model stated before the spectral expansion.'},
 '22':{'D2':'The Euclidean branch assumes absolutely continuous population laws.','D15':'The torus branches use absolutely continuous torus laws.','D11':'The density and potential hypotheses use Hölder and C2 spaces.','D9':'The hypercube and empirical Euclidean cases refer to the population Brenier potential.','D18':'The torus case uses the convex lift of the population map.','D7':'The additional hypercube condition for (39) concerns the conjugate potential.','D22':'Part (iii) specifies the two empirical measures.','D24':'Part (ii) specifies the boundary-corrected wavelet measures.','D27':'Part (i) specifies the periodic kernel density measures.','D28':'The Section 5.1 preamble requires K1(2alpha,kappa) for the kernel branch.','D26':'The Section 5.1 preamble explicitly uses two independent iid samples.','D37':'All three assertions invoke the original central limits (38) and (39).'},
 '24':{'D15':'Both population distributions and their perturbations are measures on the torus.','D13':'The population and perturbed densities lie in positive Hölder balls with different bounds.','D19':'The lower bounds are the variances of the torus Kantorovich potentials.','D38':'The one-sample target Phi_Q is the fixed-target cost functional, here instantiated on the torus.','D39':'Both assertions use the differentiable paths identified in the immediately preceding main-text paragraph.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned arXiv:2107.12364v3, 99 pages. Main text ends above y=637.536865234375 on shared page 29. Appendix mathematics and later references are excluded.',
     normalization_policy='Preserve all nine complete Theorems, the two phi glyphs, barred constants and maps, original estimator formulas, named conditions and appendix-only unresolved references.',
     semantic_ranking_policy='Count only statement dependencies and recursively used main-text definitions. Distinguish Euclidean from torus costs, deterministic stability from sampling models, and assumptions from proof results.',
     build_order_policy='Derive the graph from paper-local definitions. Keep the three density estimators and their conditions separate. Do not import Theorem 18 kernel assumptions into Theorem 20 merely because it reuses the rate notation.')
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
    finalized=json.loads((ROOT/'ranked-interfaces.json').read_text())
    passages=dict(paper_id=PID,members=[m for x in finalized['interfaces'] for m in x['members']])
    (ROOT/'source-passages.json').write_text(json.dumps(passages,indent=2,ensure_ascii=False)+'\n')
    print('Finalized and independently validated; final source audit remains.')


if __name__ == "__main__":
    main()
