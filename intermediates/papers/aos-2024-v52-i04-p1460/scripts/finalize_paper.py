"""Attach source-reviewed theorem-to-interface paths and finalize this paper."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
'3.1':{
'D3':'The theorem explicitly works under the strong signal model (4).',
'D5':'The opening specifies finite second-moment matrices Q_Lambda and Q_Theta.',
'D6':'The opening requires nonsingularity and Q_Theta=q_Theta I_r, citing Remark 3.1.',
'D7':'Claim 1 uses the prescribed top-r spectral estimate Lambda-hat_s.',
'D8':'Claim 1 asserts convergence in the subspace loss L^sin defined in (5).',
'D9':'Claim 3 adds the absence of a nonidentity orthogonal distributional symmetry of Lambda_0.'},
'3.2':{
'D3':'The opening specifies the strong signal model (4).',
'D5':'Both lower bounds use Q_Lambda^(1/2) in the conditional Gaussian expectation.',
'D6':'The theorem expressly assumes the setting of Remark 3.1, including nonsingular second moments and the Theta normalization.'},
'3.3':{
'D3':'The reference to Theorem 3.1 claim 3 retains its strong-signal experiment and diverging aspect ratio.',
'D5':'Both limiting error expressions use Q_Lambda^(1/2) and the Theta moment scale q_Theta.',
'D6':'The referenced theorem has the common second-moment and normalization hypotheses of Remark 3.1.',
'D9':'The theorem explicitly imports the identifiability hypothesis of Theorem 3.1 claim 3, rather than its subspace-loss conclusion.'},
'4.1':{
'D12':'The second conclusion gives the limiting Bayesian MMSE from (11) for the symmetric experiment.',
'D13':'The first conclusion gives the limiting normalized mutual information from (12).',
'D14':'The first formula optimizes F(q_Theta^2,Q) over positive semidefinite Q.',
'D15':'The second formula uses Q-star(s) from (14); the source leaves s unbound in this theorem.'},
'4.2':{
'D4':'The theorem specifies the weak signal model (9).',
'D5':'The risk bounds use the Theta second-moment scale q_Theta and its mean.',
'D6':'The opening expressly assumes the setting of Remark 3.1. It does not invoke the later zero-mean Assumption 4.1.'},
'4.3':{
'D4':'The first sentence identifies the asymmetric model (9).',
'D13':'The theorem explicitly recalls mutual information (12) in the symmetric model.',
'D17':'The dimension limit is taken within Assumption 4.1: zero Theta first and third moments and sub-Gaussian laws for both factors.',
'D18':'The theorem defines the asymmetric normalized mutual information by (16) and uses it in the concluding equality.',
'D25':'The additional normalization printed in the theorem is Q_Theta=q_Theta I_r, with a citation to Remark 3.1.'},
'4.4':{
'D4':'The inherited Theorem 4.3 conditions and the modified-model paragraph both specify the weak-signal A from (9).',
'D12':'Both bounds compare against the symmetric-model MMSE (11).',
'D16':'The first bound uses the unperturbed asymmetric risk (15).',
'D17':'The reference to the conditions of Theorem 4.3 imports Assumption 4.1, not its mutual-information conclusion.',
'D19':'The second part explicitly adds the independent symmetric observation Y-prime(epsilon).',
'D20':'The second inequality concerns the corresponding augmented-observation risk, with epsilon sent to zero after the high-dimensional limit.',
'D25':'The inherited Theorem 4.3 hypotheses include its explicit Theta second-moment normalization.'},
'4.5':{
'D4':'The inherited Theorem 4.3 conditions fix the weak-signal experiment with d/n tending to infinity.',
'D12':'The limiting comparison on the right is the symmetric-model MMSE (11).',
'D16':'The left side is the unperturbed asymmetric matrix risk (15).',
'D17':'The conditions of Theorem 4.3 include Assumption 4.1 in every alternative.',
'D21':'Alternative (c) explicitly defines the scalar-channel information and Psi, then requires its printed global maximum to be the first stationary point.',
'D25':'The inherited normalization is Q_Theta=q_Theta I_r as stated in Theorem 4.3.'},
'5.1':{
'D22':'The opening invokes the equal-weight Gaussian mixture and the preceding assumptions on its random centers from Section 5.2.',
'D23':'Both conclusions are expressed in the permutation-invariant overlap of the estimated and true label encodings.',
'D24':'Both cases compare q_Theta with the information threshold defined by the strict free-energy improvement in (26).'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Verified registered arXiv:2211.00488v1 PDF, 74 pages; main text and references on pages 1-28, with appendix bodies excluded.',
        normalization_policy='Preserve all nine original Theorems 3.1-3.3, 4.1-4.5 and 5.1, including continued statements, conditional claims and all alternative hypotheses. Keep literal source anomalies separate from explanatory notes.',
        semantic_ranking_policy='Resolve exact strong/weak/symmetric model normalizations, original estimation losses, fixed prior conventions, assumption references, and information/free-energy objects. A reference to theorem conditions does not import the referenced conclusion or proof-only constructions. Keep explicit Theta normalization separate from the full earlier Remark 3.1.',
        build_order_policy='Derive all edges and reach from the original local dependency graph; keep the independent theorem inventory unchanged.')
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
