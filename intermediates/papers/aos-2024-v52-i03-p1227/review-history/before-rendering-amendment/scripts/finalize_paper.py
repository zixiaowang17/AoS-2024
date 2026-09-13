"""Attach source-reviewed theorem-to-interface paths and finalize this paper."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{'D1':'The conclusion covers the estimands theta_gamma under the underlying model law.','D2':'Both the nested union and the coverage event use the selected set Gamma-hat.','D3':'The hypothesis requires simultaneous confidence regions, and the conclusion uses them at level alpha-nu.','D4':'The theorem explicitly invokes monotonicity, Assumption 1.','D5':'The expanded union uses accepted observations in A_nu(P-prime).','D6':'The first union uses the fixed-distribution plausible targets Gamma_nu(P-prime).','D7':'The outer union ranges over B_nu(y), the inverted distribution confidence region.'},
 '2':{'D1':'The coverage event concerns the original target estimands theta_gamma.','D2':'Coverage is simultaneous over the selected set Gamma-hat.','D4':'The theorem explicitly invokes Assumption 1 and writes the monotonicity of the corrections under subset inclusion.','D8':'The theorem explicitly reuses the augmented set from Theorem 1, equation (2).','D9':'The confidence intervals are required to satisfy Assumption 2, centered intervals.','D10':'Both the chosen acceptance region and the final confidence interval use C_gamma(q); the calibrated correction is minimized over the two stated choices.'},
 '3':{'D11':'The probabilities are under P_mu and the targets are location coordinates mu_gamma in the Section 3.1 model.','D12':'The first bullet explicitly refers to winner selection (3), which defines hat-gamma.','D13':'The second bullet explicitly refers to threshold selection (4), which defines Gamma-hat.','D14':'The plausible-set margins and final interval widths use q at specified levels and index subsets.'},
 '4':{'D15':'Section 3.2 fixes iid bounded vector observations and the mean vector theta.','D16':'The first bullet explicitly refers to winner selection from empirical means, equation (5).','D17':'The second bullet refers to thresholded empirical means, equation (6).','D18':'The plausible-set margins use the scalar deviation bound w_n at level nu/m.','D19':'The theorem imposes error-level nesting on the marginal confidence regions C_gamma and uses them at the random-cardinality correction level.'},
 '5':{'D20':'The displayed neighborhood uses the fixed design matrix and response vector from Section 4.','D21':'The neighborhood radius is twice q^nu evaluated on the design-column contrast set.','D22':'The model map M-hat(y-prime) is the support selected by the original LASSO problem.','D30':'The theorem asserts the exact model set returned by Algorithm 1, including its screening subroutine calls.'},
 '6':{'D31':'The theorem uses the loss, iid dataset, empirical risks, fixed hypothesis class and empirical minimizer from Section 5.','D32':'The conclusion bounds the population risk R(hat-f,P).','D33':'The plausible hypothesis set and risk bound use Gap_n on the full class and on the displayed data-dependent subclass.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Registered local arXiv:2212.09009v6 PDF, 36 pages; use only main-text/reference pages 1-27 before Appendix A on page 28.',
        normalization_policy='Preserve all six original theorem bodies, both bullets of Theorems 3 and 4, and all of main-text Algorithm 1. Keep each statistical setting and original source passage distinct.',
        semantic_ranking_policy='Count only statement dependencies and original local definition paths. Proof applications of the general theory do not import its entire interface family into specialized theorem statements.',
        build_order_policy='Preserve same-paper dependencies, separate the two q quantiles and the two selection experiments, and record appendix screening subroutines as unresolved beyond their main-text descriptions.')
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
