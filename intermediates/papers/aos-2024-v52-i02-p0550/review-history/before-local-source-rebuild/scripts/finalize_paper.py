"""Derive all eleven theorem connections from reviewed, conditional source requirements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
BASE={
 'D5':'Assumption 3.1 requires the locally stationary process, its causal representation, uniform moments and summable dependence measure (3.2).',
 'D6':'Assumption 3.2 requires the stationary approximants and both Hilbert-norm and coordinate-summed dependence conditions, including (3.3). The S2-only relaxation is not used.',
 'D7':'Assumption 3.3 requires weighted coordinate summability and twice Frechet differentiability in time of the spectral density, for almost every frequency.',
 'D10':'Assumption 3.4 supplies the even, bounded, piecewise continuous lag window and its order at zero.',
 'D11':'Assumption 3.5 fixes zeta=1 and the N, M and b_f growth conditions, retaining both kappa regimes and their shared endpoint.',
 'D14':'Assumption 3.6 gives all three operator-field conditions and its additional clause when Upsilon depends on the spectral family.',
 'D16':'The mapping G_Upsilon is the transformed operator field (3.23), with the specified phi and exponent x.',
 'D17':'L_UM and L in the convergence statement are the discrete and continuous integration maps (3.25)-(3.26).',
 'D9':'F-hat is the sequential estimator (3.6), with the lag weights, local block index and zero-floor convention retained.',
 'D2':'F is the population time-varying spectral density (2.2), constructed from the local second-order operators.',
 'D12':'rho_T is the normalization (3.11); the source k_f versus kappa_f notation is retained.',
 'D13':'U_M is the increasingly dense grid (3.15) used for the discrete average.',
}
NONLINEAR={
 'D15':'The nonlinear branch explicitly requires F in D_1, the separated-spectrum domain (3.21), and analytic phi on the containing domain.',
 'D18':'Only the nonlinear branch additionally requires the coordinate dependence tail (3.28), with some 0<rho<1, and p such that the separately archived condition (3.30) holds.',
}
PIVOTAL={
 'D19':'The reference to Corollary 3.1 requires k Frechet differentiable outer mappings Psi_j:C_S1 to C_W; its complete inherited conditions are archived in A5.',
 'D20':'T_j,T and T_j are the compositions (3.31) used in the centered statistic. Their source expansions (3.32) are preserved separately without harmonizing eta and h.',
 'D21':'Equation (3.34) is the required factorization of the derivative limit into sigma g(eta) B(eta), with independent real or proper complex Brownian coordinates.',
 'D22':'Equation (3.35) is the required scaling identity for T_j, with known f_j and f_j(1)=1; the source word linear is not interpreted as additivity.',
 'D23':'D-hat and V are defined in (3.36)-(3.37). The required nonsingularity of limiting U is stated in Theorem 3.2 itself, with conjugation on the second factor.',
}
DIRECT={}
def base(n,route):
    DIRECT[n]={lid:route+' '+reason for lid,reason in BASE.items()}
    DIRECT[n].update({lid:route+' '+reason for lid,reason in NONLINEAR.items()})
def pivotal(n,route):
    base(n,route+' Through Corollary 3.1, the applicable branch of Theorem 3.1 is required for each mapping; nonlinear-only conditions below remain conditional.')
    DIRECT[n].update({lid:route+' '+reason for lid,reason in PIVOTAL.items()})
base('3.1','The theorem states Assumptions 3.1-3.6 and the following objects, with separate identity and nonlinear phi branches.')
pivotal('3.2','The theorem expressly requires the conditions of Corollary 3.1 and equations (3.34)-(3.35).')
for n in ['3.3','3.4','3.5','3.6']:
    base(n,'The theorem explicitly requires Theorem 3.1(b), so its common and nonlinear-branch conditions are inherited.')
DIRECT['3.3'].update({
 'D3':'The ordered lambda values are the eigenvalues of F from (2.3); the hatted values are the corresponding eigenvalues of F-hat, as explained after (3.14). The theorem adds uniform ordered positivity.',
 'D25':'The difference in (3.42) is the empirical and population principal-component variation ratio (2.7), here using an integrated trace denominator. Its simple-spectrum scope is retained.'
})
DIRECT['3.4'].update({
 'D26':'The ordered delta values and their empirical counterparts are the rearranged separable scores (2.9), not the original spectral eigenvalues lambda.',
 'D27':'The displayed difference in (3.44) is the empirical and population squared-score separability ratio (2.10). The original defining display and theorem retain their respective differential order.'
})
DIRECT['3.5'].update({
 'D28':'The marginal eigenvalues lambda_ii,d in the assumptions belong to the component spectral blocks on H1 direct-sum H2.',
 'D29':'R_d in (3.45) is the canonical coherence ratio defined in Section 2.2.3; Section 3.5.3 gives its sequential squared-ratio estimator. The nu_d assumptions concern cross-block singular values.'
})
DIRECT['3.6'].update({
 'D32':'The entire displayed difference is r-hat_d(eta)-r_d(eta), defined immediately before the theorem using the restricted spectra, square root distance and mean-root targets in (3.46).'
})
for n in ['4.1','4.2','4.3','4.4','4.5']:
    pivotal(n,'The theorem expressly assumes Theorem 3.2, applied to the relevant real scalar functional or accuracy functionals.')
DIRECT['4.1'].update({
 'D24':'The theorem defines q_beta as the quantile of T in (4.1); the same scalar specialization gives r-hat and V used in interval (4.2).',
 'D33':'The theorem explicitly assumes r=T(F)>0, the general deviation functional (2.14), without selecting a particular structural model.'
})
DIRECT['4.2'].update({
 'D34':'The theorem explicitly names hypotheses (2.15), the deviation null r<=Delta and alternative r>Delta, with Delta>0.',
 'D37':'The test is expressly rule (4.3), comparing r-hat against Delta minus the lower quantile times V.'
})
DIRECT['4.3'].update({
 'D35':'The estimator setting in Section 4.2 uses the increasing model classes and their accuracy sequence s_d from Section 2.4.',
 'D36':'The two error events and the consistency conclusion compare d-hat with the minimal model complexity d* defined by (2.18).',
 'D40':'The estimator is expressly (4.8), the first threshold-centered statistic above q_alpha. Its additional varying-alpha conclusion retains the printed unrestricted alpha_T-to-zero claim.'
})
DIRECT['4.4'].update({
 'D35':'The testing setting uses the nested model classes and accuracy sequence introduced in Section 2.4.',
 'D36':'The theorem expressly tests (2.19), H0:d*<=d0 versus d*>d0, where d* is the strict first-exceedance complexity (2.18).',
 'D40':'The rejection event uses d-hat from estimator (4.8), as specified in Section 4.2.2 immediately before this theorem.'
})
DIRECT['4.5'].update({
 'D35':'The theorem explicitly names the accuracy hypotheses (2.17), using the nested-model accuracy s_d0 and threshold nu.',
 'D36':'The other named hypotheses (4.9) use d* from (2.18). With the strict threshold and monotonicity, their null is equivalent to s_d0<=nu.',
 'D41':'The theorem expressly selects decision rule (4.11), which uses s-hat_d0, the upper application-specific quantile and V_d0,d0. It does not use estimator d-hat.'
})
inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
data['schema_version']='statistical-ranked-interfaces-v4'
data['scope'].update(
 paper_count=1,
 source_policy='Pinned arXiv:2208.10158v3, main text and references on pages 1-30. Appendix A begins separately on page 31; only its heading crop was inspected. All eleven main-text Theorems retained.',
 normalization_policy='Preserve complete original statements, source types, branch conditions, definitions and discrepancies. Keep source expansions and analysis separate; do not repair formulas or infer appendix-only definitions.',
 semantic_ranking_policy='Direct statement requirements and deduplicated recursive same-paper reach. Conditional branch requirements are labeled in explanations. Proof-only results and subsequent inference applications do not create statement dependencies.',
 build_order_policy='Keep causal model, operator assumptions, generic transformations, self-normalization, individual application measures and model-selection definitions separate. Preserve the acyclic paper-local graph.')
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
