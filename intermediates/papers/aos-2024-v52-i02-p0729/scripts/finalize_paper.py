"""Derive all five theorem connections without importing proof-only requirements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{'D1':'The opening assumption states Gaussian columns with covariance S-star, using the population principal-subspace model (1.1)-(1.2).','D2':'The theorem explicitly requires Omega to follow the random sampling model in Section 1.1.','D4':'The ground-truth matrix X is identified by the explicit reference to (2.1a).','D6':'Kappa, sigma_r-star and the diagonal square-root matrix Sigma-star are the population spectral quantities in (3.1)-(3.2).','D7':'The mu appearing in the bounded-parameter regime is the incoherence parameter introduced in Definition 1; its row bound is the standing meaning of mu.','D8':'The theorem defines R by sgn(U^T U-star), using the matrix sign from (1.4).','D9':'The theorem expressly requires Assumption 1 and uses its omega_max and kappa_omega.','D10':'The subspace estimate U and its iteration count are those of Algorithm 2.'},
 '2':{'D1':'The reference to the conditions of Theorem 1 retains the Gaussian population model, and the target is its eigenspace U-star.','D2':'The sampling assumption and permitted probability regime are inherited from Theorem 1.','D4':'The inherited Gaussian-column condition concerns X from (2.1a).','D6':'The inherited spectral/noise and iteration bounds use kappa, sigma_r-star and the population spectral scales.','D7':'The inherited bounded-mu condition refers to Definition 1’s incoherence property.','D8':'The displayed rotation is sgn(U^T U-star), using the source matrix-sign definition.','D9':'The inherited Assumption 1 controls the noise variance ratio and defines omega_max and kappa_omega.','D11':'The confidence regions CR are explicitly the outputs of Algorithm 3, including its estimated covariance and chi-square ball.'},
 '3':{'D1':'The result remains in the Section 3 PCA model, with population covariance S-star and eigenspace U-star from (1.1)-(1.2).','D2':'The explicit restriction on p refers to the common Bernoulli sampling probability in the standing model.','D6':'The comparability regime and both noise-to-signal restrictions use the population spectral quantities from (3.1)-(3.2).','D7':'The theorem explicitly assumes U-star is mu-incoherent, which is the row condition in Definition 1.','D9':'The statement expressly assumes Assumption 1 and uses its maximum noise level.','D10':'The covariance estimate S is explicitly the output of Algorithm 2, with the referenced iteration condition (3.6).','D12':'The normalizing variance v-star_i,j is defined by the two cases (3.10)-(3.11) immediately before the theorem.'},
 '4':{'D1':'The conditions inherited from Theorem 3 retain the Section 3 population covariance model.','D2':'The inherited and additional sampling restrictions concern p from the common Bernoulli observation model.','D6':'The spectral scales and bounded kappa regime remain inherited from Theorem 3.','D7':'Theorem 3’s mu-incoherence and selected-row condition remain hypotheses of this result.','D9':'Assumption 1 and the noise-to-signal restrictions are inherited from Theorem 3.','D13':'The statement explicitly concerns the interval CI computed by Algorithm 4, retaining its literal printed formulas.'},
 '5':{'D14':'The target U-natural, right singular vectors V-natural, singular scales Sigma-natural, dimensions and condition number belong to the separate matrix model (6.1)-(6.4).','D15':'The theorem explicitly assumes Assumption 2, including both singular-space row bounds and the entrywise signal bound.','D16':'The theorem explicitly assumes Assumption 3; its global and row scales define the zeta quantities (6.10).','D17':'The estimates in Section 6 are the outputs of HeteroPCA Algorithm 5, with the displayed iteration restriction.','D18':'The aligned error uses R_U as defined by the orthogonal minimization in (6.9).','D5':'The inline second-order term in Z explicitly applies P_off-diag to E E^T.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Published journal PDF, Annals of Statistics 52(2), pp.729-756, 28 main-paper pages. Preserve every printed Theorem 1-5. The supplement notice links to a separate unopened document.',
     normalization_policy='Preserve complete original statements and all source definitions/algorithm formulas. Keep the random-column PCA and general rectangular-matrix models distinct; document printed formula and dimension mismatches separately.',
     semantic_ranking_policy='Direct statement uses and recursive same-paper prerequisites only. Proof expansions and comparisons with prior results do not import conditions from another theorem or model.',
     build_order_policy='Keep the two incoherence notions, noise models, spectral condition numbers and HeteroPCA scalings separate. Follow the actual source references and preserve all local edges.')
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
