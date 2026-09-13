"""Connect the independently saved inventory to inspected, paper-local source passages."""
import copy
import json
import subprocess
import sys
from extract_interfaces import ROOT, PAPER_ID, SKILL, interfaces, members, edges, main as save_passages
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory

DIRECT = {
 '2.2': {
  'D2':'Part (a) specifies the unprojected orbit recovery model (2.1).',
  'D3':'Part (b) specifies the projected orbit recovery model (2.2).',
  'D8':'The function expanded in both parts is the population negative log-likelihood R(theta) from (2.5).',
  'D9':'Part (a) places q_k and s_k in the degree-generated invariant subalgebras; the remainder is also group-invariant.',
  'D10':'Equation (2.8) contains the unprojected moment tensor T_k at the candidate and true signals.',
  'D11':'Part (b) uses the projected tensor in its expansion and in the defining discrepancy (2.11).',
  'D12':'Part (b) places q_k, the entries of P_k, and the leading term in projected-moment subalgebras.',
  'D13a':'Part (a) defines s_k by (2.8) and uses it in the expansion (2.7).',
  'D13b':'Part (b) defines the projected leading term by (2.11) and uses it in (2.10).'},
 '2.7': {
  'D2':'Part (a) concerns the unprojected observation model.',
  'D3':'Part (b) transfers the spectral conclusions to the projected observation model.',
  'D6':'The first sentence quantifies over generic true signals, in the sense of Definition 2.3.',
  'D7':'Part (b) explicitly assumes condition (2.4).',
  'D9':'The rank, gradient spans and polynomial-functional bound use the full and degree-generated invariant algebras.',
  'D12':'Part (b) replaces the degree-generated algebra by the projected-moment subalgebra.',
  'D15':'All three conclusions concern the spectrum, eigenspaces or pseudoinverse of I(theta_*), the matrix defined in Section 2.3.',
  'D16':'Part (a1) states its rank using the transcendence degree of the invariant algebra.',
  'D17a':'Part (a1) explicitly defines K through Proposition 2.6(a).',
  'D17b':'Part (b) explicitly defines the projected order through Proposition 2.6(b).',
  'D18':'The identity rank I(theta_*)=d-d0 uses the maximum orbit dimension from (2.12).',
  'D19a':'The multiplicities d_k and the cumulative dimensions of the leading eigenspaces use (2.12).',
  'D19b':'Part (b) replaces these multiplicities by the projected increments in (2.13).',
  'D33':'Remark 2.9 explicitly identifies the gradient-span condition used for the generic signals in Theorem 2.7.'},
 '2.11': {
  'D2':'Part (a) concerns the unprojected model.', 'D3':'Part (b) concerns the projected model.',
  'D4':'Part (a) assumes the final moment variety equals the orbit of the true signal.',
  'D5':'Part (b) identifies its final moment variety using projected-orbit equivalence, including equality of induced laws.',
  'D6':'The opening hypothesis is for generic true signals.', 'D7':'Part (b) explicitly assumes (2.4).',
  'D8':'The conclusions assert benign minimization of the population negative log-likelihood R(theta).',
  'D13a':'Part (a) assumes benign minimization of each unprojected discrepancy s_k.',
  'D13b':'Part (b) uses the projected discrepancy in the corresponding constrained problems.',
  'D17a':'Part (a) defines K by Proposition 2.6(a).', 'D17b':'Part (b) defines its terminal order by Proposition 2.6(b).',
  'D20':'Both the hypotheses on the moment problems and the conclusions on R use globally benign in Definition 2.10.',
  'D21a':'Part (a) assumes constant rank of the derivative of M_k, the vector in (2.15).',
  'D21b':'Part (b) imposes constant rank on the projected moment vector from (2.16).',
  'D22a':'Part (a) imposes rank and minimization conditions on the fibers in (2.17), including the terminal fiber equality.',
  'D22b':'Part (b) uses the projected fibers in (2.18).',
  'D33':'Remark 2.9 names Theorem 2.11 among the results using its specified generic-gradient-span condition.'},
 '2.13': {
  'D2':'Part (a) concerns the unprojected model.', 'D3':'Part (b) prescribes replacements for the projected model.',
  'D6':'The statement opens with generic true signals.', 'D7':'Part (b) explicitly requires (2.4).',
  'D8':'The local minimizers compared in both directions include those of the population negative log-likelihood R(theta).',
  'D13a':'Part (a) compares local minimizers with the terminal discrepancy s_K, and assumes benign lower-order s_k problems.',
  'D13b':'Part (b) replaces s_k by the projected leading term defined in (2.11).',
  'D17a':'The index K retains the unprojected terminal order fixed in Proposition 2.6(a) and the preceding landscape setup.',
  'D17b':'Part (b) replaces K by the projected terminal order from Proposition 2.6(b).',
  'D20':'The lower-order moment minimizations in the hypothesis must be globally benign as in Definition 2.10.',
  'D21a':'The constant-rank hypothesis is on the derivative of the concatenated vector M_k.',
  'D21b':'Part (b) replaces M_k by its projected counterpart.',
  'D22a':'Part (a) uses both the order-k fibers and the order-(K-1) constraint manifold.',
  'D22b':'Part (b) prescribes the projected moment varieties as replacement constraint sets.',
  'D23':'Part (a1) requires a non-degenerate local minimizer up to orbit; (a2) requires every terminal critical point to satisfy Definition 2.12. Part (b) gives the projected replacements.',
  'D33':'Remark 2.9 explicitly says its generic-gradient-span condition is used in Theorem 2.13.'},
 '3.1': {
  'D9':'All three equalities concern the invariant subalgebras through degrees one, two and three, and the full invariant algebra.',
  'D16':'The quantities evaluated are the transcendence degrees of those algebras.',
  'D24':'Section 3 fixes the circle-rotation representation (3.4) and d=2L+1 used in these equalities.'},
 '3.3': {
  'D13a':'The left sides s_1, s_2 and s_3 are the unprojected discrepancies defined in (2.8).',
  'D24':'The real Fourier coordinates theta^(0), the bandlimit L and the group representation come from the circle model in Section 3.',
  'D25':'The right sides use the complex coefficients, their magnitudes, the triple products and phase differences defined immediately above this theorem.'},
 '3.4': {
  'D4':'The concluding local minimizer lies outside the orbit of the true signal.',
  'D6':'The first assertion is stated for generic true signals; the later assertion instead quantifies over a nonempty open subset.',
  'D13a':'The three objectives are s_1, s_2 and s_3 from the unprojected discrepancy definition (2.8).',
  'D20':'The first assertion says the order-one and order-two constrained problems are globally benign.',
  'D22a':'The constraints are the unprojected moment varieties of orders zero, one and two from (2.17).',
  'D23':'The concluding spurious local minimizer is required to be non-degenerate up to orbit, as in Definition 2.12.',
  'D24':'The two bandlimit thresholds L>=1 and L>=30 refer to the fixed continuous-MRA representation.'},
 '4.1': {
  'D9':'The result evaluates the degree-one, degree-two and degree-three invariant subalgebras and the full invariant algebra.',
  'D16':'The numerical equalities are statements about transcendence degree.',
  'D26':'Section 4.1 fixes the spherical-harmonic representation, bandlimit L and dimension d=(L+1)^2.'},
 '4.4': {
  'D13a':'The three left sides are the unprojected discrepancies from (2.8).',
  'D26':'The formulas use the spherical-registration model and its bandlimit L.',
  'D27':'The first two formulas use the complex spherical vectors u^(l), defined across pages 14-15.',
  'D28':'The third formula contains B_(l,l-prime,l-double-prime), the contraction defined by (4.2).'},
 '4.6': {
  'D9':'The displayed identities use the full invariant algebra and its degree-generated subalgebras.',
  'D16':'The algebraic quantities on the left are transcendence degrees.',
  'D29':'The group action, radial bandlimits S_l and dimension d=sum_l (2l+1)S_l are those of the unprojected cryo-EM representation (4.3)-(4.7).'},
 '4.9': {
  'D13a':'The left sides s_1, s_2 and s_3 use the unprojected discrepancy definition (2.8).',
  'D29':'The bandlimits and real parameter vector belong to the unprojected cryo-EM model of Section 4.2.',
  'D30':'The right sides use the frequency-pair vectors u^(ls) from (4.8) and the radially indexed contraction B from (4.9).'},
 '4.10': {
  'D9':'The theorem compares the projected degree counts to the unprojected invariant algebras and uses the full invariant algebra in the last equality.',
  'D12':'The left sides contain the subalgebras generated by projected moments through orders one, two and three.',
  'D16':'The quantities evaluated and compared are transcendence degrees.',
  'D29':'The final sentence explicitly compares to the unprojected setting of Theorem 4.6, with the same 3D bandlimits and dimension.',
  'D31':'Section 4.3 fixes the tomographic projection and projected-basis conventions behind the projected algebras.'}
}

def main():
    save_passages()
    inventory=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=copy.deepcopy(inventory)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Pinned arXiv:2107.01305v2; main-text PDF reviewed against matching TeX, stopping above Appendix A on page 21.',
        normalization_policy='Preserve original wording, mathematical content and printed labels; expand TeX macros and normalize line wrapping and emphasis typography.',
        semantic_ranking_policy='Deduplicate direct uses by theorem and interface; retain all 12 original theorem records.',
        build_order_policy='Derive canonical ordering from the inspected acyclic paper-local dependencies; projected and unprojected members keep distinct paths.')
    data['interfaces']=copy.deepcopy(interfaces)
    by_claim={c['claim_id']:c for c in data['claims']}
    for claim in data['claims']:
        number=claim['label'].removeprefix('Theorem ')
        direct=DIRECT[number]
        claim['depends_on']=list(direct)
        for item in data['interfaces']:
            used=[m['local_id'] for m in item['members'] if m['local_id'] in direct]
            if used:
                item['central_claim_uses'].append(dict(use_id=claim['claim_id']+'-'+item['interface_id'].split('/')[-1],
                    paper_id=PAPER_ID,claim_id=claim['claim_id'],use_kind='statement_dependency',
                    reason=' '.join(direct[lid] for lid in used),evidence=claim['evidence']))
    derived=canonical_dependencies(data)
    for item in data['interfaces']:
        item['dependencies']=derived[item['interface_id']]
    derive_metrics(data)
    for item in data['interfaces']:
        for record in item['related_theorems']:
            cid=record['claim_id'];path=record['via_local_ids']
            number=by_claim[cid]['label'].removeprefix('Theorem ')
            explanation=[DIRECT[number][path[0]]]
            evidence=list(by_claim[cid]['evidence'])
            for lid in path:
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
            for start,end in zip(path,path[1:]):
                explanation.append(edges[start][end])
            if len(path)==1:
                extra=[m['local_id'] for m in item['members'] if m['local_id']!=path[0] and m['local_id'] in DIRECT[number]]
                explanation.extend(DIRECT[number][lid] for lid in extra)
            item['theorem_explanations'][cid]=dict(paper_id=PAPER_ID,via_local_ids=path,text=' '.join(explanation),evidence=evidence)
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Finalized and independently validated; source audit record still requires completion review.')

if __name__=='__main__':
    main()
