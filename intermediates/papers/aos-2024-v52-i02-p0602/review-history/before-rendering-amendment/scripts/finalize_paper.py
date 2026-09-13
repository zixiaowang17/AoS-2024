"""Resolve each theorem against its own source model, then derive the census."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{
  'D2':'The comparison is under the null hypothesis of no jumps, stated at the start of Section 2.1.',
  'D8':'The theorem compares the distribution of Q_n, the maximum of the centered squared standardized contrast in (8).',
  'D9':'The comparison maximum uses Z_i from the explicit centered Gaussian vector (11)-(12).',
  'D10':'The opening Assumptions 1-3 include the iid innovation moment condition in Assumption 1.',
  'D11':'The opening Assumptions 1-3 include the normalized VMA coefficient tail condition in Assumption 2.',
  'D12':'The opening Assumptions 1-3 include diagonal coefficient matrices in Assumption 3; the source p=tilde-p convention applies in this section.'
 },
 '2':{
  'D1':'The true break count K and jump vectors gamma_k in every conclusion refer to the observation and trend model (1)-(2).',
  'D5':'The hypotheses and estimation rates use the diagonal long-run standard-deviation matrix Lambda defined in (5).',
  'D7':'Part (iii) subtracts bar-c, the exact sum of contrast-coordinate variances in (7).',
  'D10':'The theorem explicitly invokes Assumptions 1-4, including the iid innovation moment condition with q at least eight.',
  'D11':'The theorem explicitly invokes Assumptions 1-4, including the linear temporal-dependence condition of Assumption 2.',
  'D12':'The theorem explicitly invokes Assumptions 1-4, including the diagonal-filter condition of Assumption 3.',
  'D13':'The hypothesis b much smaller than kappa_n uses Definition 1, and tau_k=n u_k is given immediately before it.',
  'D14':'The signal condition and final error bound use delta_p, the minimum normalized jump size (21).',
  'D15':'K-hat, tau-hat_k, gamma-hat_k and delta-hat_p are the outputs of Algorithm 1. Omega is its input threshold, subject here to the printed rate conditions.',
  'D16':'The opening Assumptions 1-4 include the gap-times-signal requirement of Assumption 4. Its source index beginning at k=0 is preserved.'
 },
 '3':{
  'D10':'The theorem expressly invokes Assumptions 1-3 and 5, including the iid linear-innovation moment condition.',
  'D11':'The theorem expressly invokes Assumptions 1-3 and 5, including the VMA temporal coefficient tail condition.',
  'D12':'The theorem expressly invokes Assumptions 1-3 and 5, including cross-sectional independence through diagonal filters.',
  'D17':'The error terms and extra convergence condition use the minimum neighborhood size |L_min| defined in (23).',
  'D19':'The null hypothesis is the absence of the localized jumps introduced with model (24) in Section 3.1.',
  'D20':'Assumption 5 is expressly named and requires the maximum and minimum neighborhood sizes to be comparable.',
  'D22':'The distribution being approximated is that of Q_n^diamond, the neighborhood-normalized statistic (27).',
  'D23':'The Gaussian maximum uses Z_phi^diamond, whose centered vector and printed covariance are specified in (30)-(32). The product index in (33) is archived as ambient notation.'
 },
 '4':{
  'D25':'The exponent v in the approximation error is the fixed spatial dimension introduced at the start of Section 4; p counts locations in the enclosing rectangle.',
  'D26':'The null means no jumps in the spatial trend (43), as explained before the centering formula (46).',
  'D27':'The rate c_(p,n) uses B_min, the minimum spatial neighborhood mass from Definition 6, which also imposes mass comparability.',
  'D28':'The theorem expressly invokes Assumptions 8-12, beginning with the spatial-location density condition in Assumption 8.',
  'D29':'The theorem expressly invokes Assumptions 8-12, including the bounded rectangle shape ratio in Assumption 9.',
  'D35':'The theorem compares the law of Q-tilde_n, the generalized Two-Way MOSUM statistic (47).',
  'D36':'The theorem expressly invokes Assumptions 8-12, including q>=8 moments of the nonlinear noise in Assumption 10.',
  'D37':'The theorem expressly invokes Assumptions 8-12, including the temporal functional-dependence condition in Assumption 11.',
  'D38':'Assumption 12 supplies the weak spatial-dependence condition and its exponent xi>1, which occurs in c_(p,n).',
  'D40':'The Gaussian comparison maximum uses Z-tilde_phi from (54)-(56); its source covariance omissions are recorded separately, and no linear covariance law is substituted.'
 }
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned arXiv:2208.13074v2; main text and references on pages 1-37 only. Appendix A begins separately on page 38, established with a heading-only crop. Preserve all four main-text Theorems.',
     normalization_policy='Keep original statements, rates, covariance formulas, source labels and conditions. Record ambiguous signs, domains and notation separately without repairing the source.',
     semantic_ranking_policy='Direct statement dependencies and deduplicated recursive same-paper reach. Optional calibration and proof constructions do not create theorem demand.',
     build_order_policy='Keep the temporal, linear-neighborhood and general nonlinear spatial constructions distinct. In particular, Theorem 4 does not inherit VMA or diagonal independence assumptions.')
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


if __name__ == '__main__':
    main()
