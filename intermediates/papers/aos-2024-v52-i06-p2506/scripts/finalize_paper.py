"""Finalize separate algebraic tensor and statistical identification dependencies."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'5.3':[2,7,9,10,11],'5.5':[1,6,8,10,11],'5.10':[2,7,9,10,12],'5.14':[1,6,8,10,12,13]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D4':{'D2':'The moment tensor is an element of the real fully symmetric order-r tensor space.','D3':'The original moment-entry formula also expresses its value through derivatives of the moment generating function M_X at zero.'},
'D5':{'D2':'The classical cumulant tensor has the same fully symmetric order-r array domain.','D3':'Its defining derivatives are taken from K_X, the log moment generating function.'},
'D6':{'D4':'The source h_r notation may select the raw moment tensor mu_r; this is one alternative, not an additional simultaneous requirement.','D5':'The same h_r notation may instead select the classical cumulant tensor kappa_r; the two choices are kept distinct.'},
'D7':{'D2':'The multilinear action applies one real matrix in every mode of a real symmetric tensor and preserves symmetry.'},
'D8':{'D1':'The observational ambiguity is derived for the invertible linear system AY=epsilon with the observed Y distribution and centered unit-covariance hidden vector.'},
'D9':{'D2':'The defining binders are T in an allowed subset V of the symmetric tensor space.','D7':'Admissible transformations are orthogonal Q for which the same-matrix tensor action Q bullet T lies in V; they need not fix T itself.'},
'D11':{'D2':'Definition5.1 restricts symmetric tensor entries to the all-equal index pattern and defines the corresponding diagonal subspace.'},
'D12':{'D2':'Definition5.8 restricts symmetric tensor entries to patterns with even multiplicity of each coordinate index, retaining its zero-tensor odd-order case.'},
'D13':{'D2':'Condition(14) sums entries of the symmetric order-r tensor over repeated index pairs, leaving two equal coordinate slots to compare.'}}
def direct_reason(n,lid):
    reasons={
'5.3':{'D2':'Theorem5.3 explicitly quantifies an arbitrary T in S^r(R^d); it does not require T to be a realizable moment or cumulant tensor.','D7':'Its conclusion explicitly uses the multilinear action Q bullet T, with Q restricted to the standing orthogonal transformation domain.','D9':'The equality G_T(Vdiag)=SP(d) refers to the set of orthogonal transformations taking the fixed tensor into the diagonal subspace, not an exact stabilizer.','D10':'The conclusion is precisely the signed-permutation set SP(d), which contains 2^d d! matrices of the form DP.','D11':'The hypothesis says T is diagonal and the conclusion requires Q bullet T in Vdiag, both in the entrywise sense of Definition5.1. The nonzero and r=2 distinctness conditions are bound separately in the theorem.'},
'5.5':{'D1':'Theorem5.5 explicitly invokes model(1), AY=epsilon with invertible A and observed Y, and adds zero mean and unit covariance for the hidden components.','D6':'Its h_r(epsilon) is the paper’s notation for either a selected order-r moment tensor or a selected classical cumulant tensor, with r≥3; both need not satisfy the restriction simultaneously.','D8':'The conclusion concerns population identification from the Y distribution. Under the theorem’s normalization, alternative admissible parameter matrices lie in the orthogonal left orbit {QA}, as explained in Section4.','D10':'Permuting and swapping signs of the rows of A is exactly left multiplication by a signed-permutation matrix DP as defined in Section4.1.','D11':'Theorem5.5 explicitly requires the chosen h_r(epsilon) to be diagonal in the Definition5.1 sense, with at most one zero diagonal entry as an additional inline condition.'},
'5.10':{'D2':'Theorem5.10 explicitly quantifies T in S^r(R^d) at even order; it is a deterministic tensor statement with no probabilistic model premise.','D7':'The conclusion applies Q bullet T using the original same-matrix action in every tensor mode.','D9':'The conclusion G_T(Vrefl)=SP(d) concerns transformations into the whole reflectional subspace, not the smaller stabilizer of the fixed tensor.','D10':'The identified transformation set is SP(d), allowing row/coordinate permutations as well as diagonal sign changes.','D12':'Theorem5.10 explicitly assumes reflectional invariance and asks whether Q bullet T remains in Vrefl, the even-index-multiplicity space in Definition5.8. Its contraction genericity condition is separately bound inline.'},
'5.14':{'D1':'Theorem5.14 explicitly uses the normalized linear model(1) with centered hidden components and covariance I_d.','D6':'Its h_r(epsilon) selects either a moment tensor or a classical cumulant tensor at some even order; the original notation does not combine the two objects.','D8':'Identification concerns alternative representations with the same observed Y distribution, whose normalized parameter matrices lie in {QA:Q in O(d)}.','D10':'The surviving ambiguity described as permuting and swapping row signs is the left signed-permutation action on A.','D12':'The chosen h_r(epsilon) must be reflectionally invariant in the entrywise Definition5.8 sense, allowing even-index off-diagonal patterns.','D13':'Theorem5.14 explicitly references condition(14), the distinct repeated-pair contractions defined within Theorem5.10, applied here to the chosen h_r(epsilon).'}}
    return reasons[n][lid]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All four complete main-text Theorems retained. Source definitions keep diagonal and reflectional restrictions separate, with moment/cumulant notation resolved as alternatives.',build_order_policy='Separate arbitrary algebraic tensors from statistical moment/cumulant tensors and observational model identification. Preserve orthogonal domains, row signed-permutation ambiguity and the two distinct genericity conditions. No proof-only polynomial or estimator dependencies.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGE_TEXT.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=DIRECT[n]
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                ev=copy.deepcopy(c['evidence'])+copy.deepcopy(members[lid]['evidence'])
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=direct_reason(n,lid),evidence=ev))
    edges=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=edges[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for rel in x['related_theorems']:
            cid=rel['claim_id'];n=cid.split('/T')[-1];path=rel['via_local_ids']
            reason=' '.join([direct_reason(n,path[0])]+[EDGE_TEXT[a][b] for a,b in zip(path,path[1:])])
            ev=copy.deepcopy(claims[cid]['evidence'])
            for lid in path:ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=reason,evidence=ev)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors) and all(s in linked for s in selectors),(m['local_id'],[s for s in selectors if s not in linked])
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Census structurally validated; independent source review remains pending.')
if __name__=='__main__':main()
