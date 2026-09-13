"""Derive the ten diffusion-theorem dependency sets from original main-text statements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '3.1':{'D2':'The reference drift b0 inherits the Section 3 restriction Sigma(C/2,A,gamma,sigma).','D4':'The tightness assertion is under the stationary reference-drift law P_b0.','D5':'The theorem bounds the kernel by its pointwise norm on [-1,1].','D7':'The two displayed empirical scales contain the localized kernel K_y,h.','D8':'The opening sentence invokes the standardized local score Psi defined above in (3.2).','D9':'The displayed family takes a supremum over the rational location-bandwidth set script T.','D10':'The theorem defines and uses the two empirical scales hat-sigma_T and hat-sigma_T,max.','D11':'The theorem explicitly defines Upsilon and the zero-over-zero convention for its argument.'},
 '4.1':{'D2':'The theorem assumes b0 lies in the tightened Sigma(C/2-eta,A,gamma+eta/sigma^2,sigma) class.','D4':'The left-hand probabilities are under the stationary diffusion law P_b.','D15':'The uniform supremum ranges over the composite null H0(b0,eta).','D17':'The theorem explicitly invokes the similarity statistic T_T^eta in (4.3).','D18':'Its right side uses U1 and U2, both fully defined in the statement.','D26':'The opening sentence imposes the nonnegative continuous bounded-variation kernel condition with norm at most one.','D3':'Both displayed Gaussian statistics explicitly use q_b0+eta and q_b0-eta.','D7':'The Gaussian integrands contain localized K_y,h.','D9':'Both Gaussian suprema explicitly range over script T.','D11':'Both Gaussian suprema explicitly subtract Upsilon at deterministic variance ratios.'},
 '5.1':{'D2':'The reference drift satisfies the tightened Sigma condition stated in the opening sentence.','D4':'Both uniform level and worst-case power use the stationary drift-indexed expectations E_b.','D15':'The test is uniformly level alpha over H0, and the power infimum ranges over H1.','D21':'The alternatives are separated by the weighted distance Delta_J from (5.1).','D22':'The drift deviations are restricted to the original Holder class H(beta,L).','D23':'The threshold contains the separation rate delta_T.','D24':'The below-boundary threshold uses the sharp constant c_*.'},
 '5.2':{'D2':'The theorem explicitly imposes the tightened reference-drift class.','D4':'Power is measured by the stationary diffusion probability P_b.','D15':'The infimum runs over the similarity alternative H1(b0,eta).','D20':'The claimed power concerns phi_T^eta explicitly identified by (4.7).','D21':'The alternative separation is stated in Delta_J.','D22':'The drift deviation is restricted to H(beta,L).','D23':'The separation bound scales with delta_T.','D24':'The final beta<=1 assertion sets the sufficient constant equal to c_*.','D25':'That same final assertion explicitly chooses K=K_beta.','D27':'The theorem states the nonnegative bounded-variation kernel condition with supremum norm exactly one.'},
 '5.3':{'D2':'The opening reference to b0 as in Theorem 5.2 imports its tightened drift-class condition.','D4':'Both adaptivity assertions use the stationary diffusion probabilities P_b.','D15':'Both infima range over H1(b0,eta).','D20':'The two power assertions concern the similarity test phi_T^eta.','D21':'Both alternative restrictions use Delta_J.','D22':'Both formulas restrict the deviations to H(beta,L), with the displayed parameter infima.','D23':'Both thresholds use the rate delta_T(beta).','D24':'The sharp-L-adaptivity formula explicitly uses c_*(beta,L).','D27':'The opening reference to K as in Theorem 5.2 imports that theorem’s kernel condition.'},
 '5.4':{'D2':'The reference to b0 as in Theorem 5.2 imports its reference-drift condition, in the surrounding eta=0 simple-null setting.','D4':'The power statement is under P_b, the stationary diffusion law.','D6':'Its alternatives are H_ne from the original two-sided testing problem.','D14':'The theorem explicitly invokes the two-sided test phi_T^b0 given in (3.6).','D21':'The printed separation condition uses Delta_J, with eta=0 from the surrounding paragraph.','D22':'The deviations are required to lie in H(beta,L).','D23':'The threshold uses the rate delta_T.','D24':'The printed minus-epsilon threshold uses the sharp constant c_*.','D25':'The test kernel is explicitly chosen as K_beta.'},
 '6.1':{'D30':'The domain of the claimed continuous map is D_A,T.','D33':'The map in the theorem is the pathwise extended statistic tilde-T_T^eta defined immediately above.'},
 '6.3':{'D2':'All three uniform probability assertions range over drifts in Sigma(C,A,gamma,sigma).','D22':'The same uniform range restricts drifts to H(1,L).','D30':'The theorem conditions on both solution paths belonging to D_A,T.','D33':'The random quantities compared are evaluations of tilde-T_T^eta.','D37':'X^{H,b} and X^b are the common-noise coupled solutions with fixed initial x0 from the immediately preceding setup.'},
 '6.5':{'D2':'The opening sentence imposes the tightened reference-drift class.','D15':'Uniform size is over H0 and the worst power infimum is over H1.','D21':'The displayed alternatives satisfy a lower bound on Delta_J.','D22':'The deviations lie in H(beta,L) in the displayed infimum.','D23':'The separation threshold uses delta_T, distinct from the locally bound Hurst neighborhood delta(T).','D24':'The threshold uses c_* from (5.2).','D37':'The arbitrary tests are evaluated on X^{H,b} from the Section 6 fixed-initial-value fractional experiment, under the common expectation E.'},
 '7.1':{'D2':'The convergence is uniform over the full drift class Sigma(C,A,gamma,sigma).','D3':'The Gaussian integral and both normalizers explicitly use the invariant density q_b.','D4':'The distribution of T_T^b(X) is the stationary drift-b law marked by b in the metric.','D7':'The Gaussian integrand and local normalizer explicitly contain K_y,h.','D9':'The definition of S_b takes a supremum over script T.','D11':'The definition of S_b subtracts the same correction Upsilon at its deterministic scale ratio.','D12':'The compared observed statistic T_T^b(X) is (3.4) with the reference drift instantiated by b.','D26':'The opening reference requires the kernel conditions from Theorem 4.1.','D38':'The convergence is measured by d_BL^b, explained in the following main-text paragraph.'}
}
inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
data['schema_version']='statistical-ranked-interfaces-v4'
data['scope'].update(paper_count=1,
 source_policy='Pinned 153-page arXiv:2203.13776v3. Main text and references occupy pages 1–31; the separately titled supplement begins on page 32 and is excluded.',
 normalization_policy='Preserve every full main-text Theorem and original source passage. Keep stationary and fixed-initial-value experiments, different kernel conditions, strict lower integer notation and printed source discrepancies separate.',
 semantic_ranking_policy='Count theorem statement prerequisites and recursively needed original definitions. Do not inherit proof-only results or impose a stationary start on the pathwise or fractional experiment.',
 build_order_policy='Derive edges from paper-local definition dependencies. Appendix-only bandwidth, fractional coupling kernel and metric normalization remain explicitly unresolved, with no invented substitute.')
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
