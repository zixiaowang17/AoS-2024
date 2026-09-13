"""Build statement-only dependencies for the lattice paper's six Theorems."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'1':[1,2,3,4],'2':[12,15,16,17],'3':[8,9,12,18],'4':[10,13,18],'5':[10,14,18,19,20],'6':[11,13,18,19,21]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'BV(U) consists of L1 functions with finite TV defined by the infinity-norm-constrained test fields in(17).'},
'D7':{'D5':'The stacked Kronecker matrix acts on vectors indexed by the N-by-...-by-N lattice with n=N^d.','D6':'Each coordinate block uses the shrinking-row difference matrix D_N^(k+1) from(4), with identity matrices in the other positions.'},
'D8':{'D7':'The KTV seminorm is the one-norm of the stacked Kronecker difference matrix applied to theta.'},
'D9':{'D7':'The KTF squared-loss objective in(7) penalizes the one-norm of D_(n,d)^(k+1) theta, using the matrix definition(8).'},
'D10':{'D8':'The KTV class is the positive-radius ball of the discrete KTV seminorm.'},
'D11':{'D7':'The discrete Sobolev class uses the two-norm of the same stacked coordinatewise difference matrix; it does not include all mixed partial differences.'},
'D13':{'D12':'R(K) takes expectation in the Gaussian mean-vector model(29), before the supremum over theta_0 and infimum over estimators.'},
'D14':{'D12':'R_L(K) takes the same Gaussian-experiment expectation but restricts the estimator to a fixed linear transformation S y.'},
'D19':{'D7':'The projection V_Q V_Q^T uses selected right singular vectors of the KTF penalty matrix, including its zero modes.'}}
def direct_reason(n,lid):
    label='Theorem '+n
    if lid=='D1':return 'Theorem1 identifies TV(f;U) from the anisotropic test-field definition(17) with the integral of essential variations on coordinate slices. The constraint is the infinity norm of the test field, not the Euclidean norm.'
    if lid=='D2':return 'Theorem1 explicitly assumes f belongs to BV(U), meaning f is integrable with finite anisotropic total variation, without assuming weak differentiability.'
    if lid=='D3':return 'Theorem1 explicitly says its one-dimensional integrand uses essential variation as in(19), whose partitions contain only approximate-continuity points.'
    if lid=='D4':return 'Theorem1 explicitly defines the coordinate projection U_-j, fiber interval endpoints and restricted function f(.,x_-j) used by its slicing integral.'
    if lid=='D8':return 'Theorem3 defines C_n=||D_(n,d)^(k+1) theta_0||_1>0, the source KTV seminorm of the mean vector, and uses this quantity in its tuning and error bound.'
    if lid=='D9':return 'Theorem3 explicitly uses the KTF estimator in(7), the unnormalized squared-loss objective with the matrix difference penalty.'
    if lid=='D10':return label+' explicitly concerns the KTV class in(23), a discrete one-norm difference ball'+(' with C_n≤n and no canonical scaling imposed.' if n=='4' else ' with C_n≤sqrt(n), under the restriction to linear estimators.')
    if lid=='D11':return 'Theorem6 explicitly concerns the discrete Sobolev class in(24), with radius B_n≤sqrt(n), measuring only coordinate-aligned differences in the two-norm.'
    if lid=='D12':return label+' explicitly invokes the independent Gaussian data model(29), with common fixed variance and mean vector theta_0.'
    if lid=='D13':return label+' uses R, the infimum over all estimators of worst-case expected squared empirical loss'+(' over the KTV class, retaining all three lower-bound terms.' if n=='4' else ' over the discrete Sobolev class, retaining the 1/n term and the nonparametric term.')
    if lid=='D14':return 'Theorem5 uses R_L, minimizing worst-case expected error only over estimators S y with fixed linear S; the result is not a restriction to a particular kernel or projection family.'
    if lid=='D15':return 'Theorem2 explicitly defines the generalized-lasso solution(30) for D in R^(r×n), without requiring a lattice or the KTF operator.'
    if lid=='D16':return 'Theorem2 explicitly bounds selected left singular vectors by mu/sqrt(n), excluding I, and uses the nonzero singular values outside I in its tuning and rate.'
    if lid=='D17':return 'Theorem2’s first error term is nullity(D)/n, with nullity defined on page11 as the dimension of the matrix null space; |I| is a separate term.'
    if lid=='D18':return label+' uses s=(k+1)/d, the effective smoothness defined immediately before Theorem3'+(' to choose its three tuning regimes.' if n=='3' else ' in its lower-bound exponent.' if n=='4' else ' to distinguish three minimax linear regimes and prescribe truncation.' if n=='5' else ' in the Sobolev rate and the spectral truncation order.')
    if lid=='D19':return label+' explicitly identifies the projection estimator(34) as attaining its upper rate, with Q=[tau]^d and the stated radius-dependent size'+('; its small-s case also uses the polynomial projection Q=[k+1]^d.' if n=='5' else '.')
    if lid=='D20':return 'Theorem5 explicitly specifies projection onto all multivariate polynomials of max degree k. Footnote4 defines this as each coordinate exponent≤k, allowing mixed monomials beyond total degree k.'
    if lid=='D21':return 'Theorem6’s last sentence explicitly invokes B_n-star from(27), the canonical Sobolev radius n^(1/2−(k+1)/d), when B_n is comparable to L_n times that radius. The omission of the parametric floor in its simplified rate is separately noted.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All six main-text Theorems retained, including the credited Theorem2 and complete T5–T6 attainment paragraphs.',build_order_policy='Keep analytic BV slicing, general-matrix estimation, lattice KTF, unrestricted minimax and minimax linear scopes distinct. Preserve source definitions without proof-only or implication-only edges.')
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
