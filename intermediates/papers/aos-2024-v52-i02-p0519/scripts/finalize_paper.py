"""Derive the twelve-theorem same-paper census from the reviewed source inventory."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{
  'D4':'The hypothesis equates P_(D,f1) and P_(D,f2), the transition operators (4) for the two positive coefficients. The coefficients and their near-boundary agreement are bound in the theorem.'},
 '2':{
  'D1':'The observations explicitly come from diffusion (2), whose initial law is uniform.',
  'D2':'The theorem explicitly requires a bounded smooth convex state domain.',
  'D4':'Both the consistency target P_(t,f0) and its fitted counterpart belong to transition family (4).',
  'D8':'E^Pi[theta | data] is the posterior expectation for the same transition likelihood (16), expressed in theta coordinates. The theorem uses Pi for the theta prior, whereas (16)-(17) use its pushforward to f.',
  'D9':'The appropriate Gaussian process prior is resolved by the source instruction immediately after Theorem 2 to see Theorems 9 and 10 for details; their construction is the cutoff Gaussian field on page 10. This resolves the introductory statement without asserting consistency for arbitrary Gaussian priors.',
  'D10':'The inline map f_theta=(1+exp(theta))/4 is exactly the link in (17). Here it is evaluated at the posterior mean of theta, as the theorem explicitly states; it is not the posterior mean of f.'},
 '3':{
  'D1':'The data explicitly follow reflected model (2), at fixed D with uniform initial distribution.',
  'D2':'The theorem explicitly states the bounded convex smooth domain condition.',
  'D4':'P_(D,f0) in the operator estimation error is the transition operator (4).',
  'D11':'The theorem explicitly selects the estimator P-hat_J from (63), with J_N of the displayed order.'},
 '4':{
  'D1':'The setting of Theorem 3 supplies the same stationary observations at fixed D; the infimum is over all estimators measurable in those observations.',
  'D2':'The lower bound asserts existence of a bounded convex smooth domain, within the setting of Theorem 3.',
  'D4':'The estimand P_(D,f) is transition operator (4). The measurable operator-valued estimator is quantified inline and is not required to equal (63).'},
 '5':{
  'D2':'The theorem explicitly assumes a bounded convex smooth domain.',
  'D4':'The logarithmic stability bound and injectivity conclusion use transition operators P_(D,f) and P_(D,f0).'},
 '6':{
  'D2':'The reference to the hypotheses of Theorem 5 inherits its bounded convex smooth domain, alongside the coefficient bounds and compact-interior agreement retained in the ambient resolution.',
  'D4':'The right-hand side is the H2-to-H2 norm of the difference of transition operators (4).',
  'D16':'The theorem states the full eigenfunction condition (10), with positive mu,c0 and a scalar vector iota. Its separate Hs bound and inherited Theorem 5 conditions are not folded into (10).'},
 '7':{
  'D2':'The hypotheses of Theorem 6 inherit the bounded convex smooth domain through Theorem 5.',
  'D4':'The theorem compares transition operators at times 0<t<D in Hilbert-Schmidt and L2 operator norms.',
  'D16':'The reference to all hypotheses of Theorem 6 includes condition (10), as well as the separate pairwise regularity and agreement bounds.'},
 '8':{
  'D13':'Part A uses the domains O_(m,w) defined by (15), with w>=2, and compact subsets of the original rectangle O_(w).',
  'D3':'Parts A and B explicitly use the Neumann Laplacian -L_1 and its variable-coefficient replacement -L_f0.',
  'D5':'The simple first positive eigenvalue and its eigenfunction use the Neumann eigen-pair convention, now indexed by the enlarged domain m.',
  'D16':'The conclusion is that the selected eigenfunction satisfies (10). This imports the eigenfunction condition only, not Theorem 6\'s pairwise f,f0 hypotheses.'},
 '9':{
  'D1':'The theorem explicitly uses discrete observations from (2) at fixed D and a uniform initial law.',
  'D2':'The state domain is explicitly bounded, convex and smooth.',
  'D4':'The posterior event is an L2 operator-norm error for P_(D,f).',
  'D8':'The posterior distribution is expressly (16).',
  'D10':'The prior is expressly (17), with K of the stated order and the given smoothness s. The truth equals one half outside O_00, the smaller cutoff set from the field construction.'},
 '10':{
  'D1':'The setting of Theorem 9 supplies the stationary fixed-D observations from model (2).',
  'D2':'The setting of Theorem 9 includes its bounded convex smooth state domain.',
  'D4':'The second posterior event concerns the Hilbert-Schmidt error for P_(t,f), for any fixed t>0.',
  'D8':'Both contractions concern the posterior (16) inherited from Theorem 9.',
  'D10':'The setting of Theorem 9 includes its specific prior (17), its truncation choice and the same truth restrictions.',
  'D16':'Only the additional algebraic-rate branch requires (10) at f0. The baseline logarithmic-rate conclusion does not assume this condition.'},
 '11':{
  'D2':'The reference to Proposition 2B includes its bounded convex smooth domain. Its C1 positivity and Hs bounds are transcribed separately as inherited hypotheses.',
  'D4':'The middle quantity in (45) is the Hilbert-Schmidt difference of the two transition operators.',
  'D6':'The right-hand side uses the continuous dual of H_c^1, where subscript c means compact support within O; it is distinguished from H_0^1 in the source paragraph before Theorem 11.',
  'D14':'KL(f,f0) is exactly the one-transition divergence (44), with expectation at the true coefficient f0.'},
 '12':{
  'D1':'The tests are functions of X_0,...,X_ND and their errors are evaluated under the respective diffusion laws at f and f0.',
  'D7':'The prior sequence and sieves live on the general parameter space F, explicitly recalled at the start of Section 3.6.1.',
  'D8':'The conclusion concerns the posterior distribution from the same likelihood (16), now for the arbitrary sequence Pi_N.',
  'D15':'The mass condition (75) uses the set B_delta_N defined in Lemma 3 immediately before the theorem. The variance ratio is preserved as printed, including its identical numerator and denominator.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT = ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,source_policy='Pinned arXiv:2210.13008v3, all 34 pages. Sections 1-3 and references form the main text; no appendices are attached. All twelve Theorems retained.',normalization_policy='Preserve complete source bodies, nested hypotheses, source types and distinct posterior, operator-norm and spectral conditions. Record ambiguities separately without repairing formulas.',semantic_ranking_policy='Direct statement dependencies and recursive same-paper reach. Proof-only constructions do not count as statement requirements.',build_order_policy='Acyclic local definitions. Keep the general parameter space and posterior separate from the concrete Gaussian field and its pushforward prior; retain the spectral condition independently of pairwise stability hypotheses.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for c in data['claims']:
     n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
     for x in data['interfaces']:
      lid=x['members'][0]['local_id']
      if lid in DIRECT[n]:x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
     for r in x['related_theorems']:
      cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1];sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])
      for lid in path:
       evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
       for ctx in members[lid].get('application_context',[]):evidence.extend(e for e in ctx['evidence'] if e not in evidence)
      for a,b in zip(path,path[1:]):sentences.append(edges[a][b])
      x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=' '.join(sentences),evidence=evidence)
     for m in x['members']:
      own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems']);selectors=m['highlight_symbols']+m['highlight_phrases']
      assert any(s in own for s in selectors),(m['local_id'],'missing source highlight')
      assert all(s in linked for s in selectors),(m['local_id'],'unmatched selector')
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Finalized and independently validated; final source audit remains.')


if __name__ == '__main__':
    main()
