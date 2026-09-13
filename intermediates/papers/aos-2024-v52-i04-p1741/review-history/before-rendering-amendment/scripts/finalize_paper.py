"""Build the source-backed graph without changing inventoried theorem statements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
1:{'D4':'The centered test tuples and all error terms use the empirical density p-hat and its marginals.',
   'D9':'Both sides of (2.16) and the radius R use the density-weighted L2 norm.',
   'D10':'The conclusion bounds the penalized objective L_n^pen relative to its minimizer f-hat; the level-set radius R in (2.15) uses this same loss.',
   'D15':'The iterates f-hat^(r) and initial tuple f-hat^(0) are the sequential updates of Algorithm 1.'},
2:{'D17':'The explicit (A1)–(A6) hypothesis includes the marginal-density bounds and derivatives in (A1).',
   'D18':'The explicit (A1)–(A6) hypothesis includes the pair-density bounds and Lipschitz condition in (A2).',
   'D19':'The explicit (A1)–(A6) hypothesis includes active-component smoothness in (A3).',
   'D20':'The explicit (A1)–(A6) hypothesis includes the baseline kernel conditions in (A4).',
   'D21':'The theorem cites the bandwidths from (A5) and adds (2.20).',
   'D22':'The explicit (A1)–(A6) hypothesis includes the conditional subexponential bound in (A6).',
   'D24':'The hypothesis phi>0, the bandwidth restriction and the error bound use the compatibility constant defined before the theorem.',
   'D16':'Both (2.20) and the final rate use the true significant-component count |S|.',
   'D10':'The conclusion concerns the penalized estimator f-hat_j.',
   'D1':'The estimation errors subtract the true additive components f_j.',
   'D9':'The error is measured in the population density-weighted norm.'},
3:{'D17':'The (A1)–(A7) hypothesis includes the marginal-density condition (A1).',
   'D18':'The (A1)–(A7) hypothesis includes the pair-density condition (A2).',
   'D19':'The (A1)–(A7) hypothesis includes component smoothness (A3).',
   'D20':'The (A1)–(A7) hypothesis includes the kernel condition (A4).',
   'D21':'The (A1)–(A7) hypothesis includes the bandwidth condition (A5).',
   'D22':'The (A1)–(A7) hypothesis includes the conditional error bound (A6).',
   'D31':'The theorem explicitly assumes (A7), including discrepancy smoothness and the gamma bound.',
   'D24':'Phi is required to be bounded away from zero and also enters the cited bandwidth restriction (2.20).',
   'D16':'The cited bandwidth condition (2.20) contains the true active-set size |S|.',
   'D28':'The maximum error concerns the debiased-fLasso-SBF component estimates.',
   'D1':'The target of the debiased estimator is each true additive component f_j.',
   'D9':'The displayed error uses the population weighted L2 norm.',
   'D30':'The rate includes s1, the maximum row sum of population inverse-kernel suprema.'},
4:{'D17':'The inherited conditions of Theorem 3 include the marginal-density condition (A1).',
   'D18':'The inherited conditions of Theorem 3 include the pair-density condition (A2).',
   'D19':'The inherited conditions of Theorem 3 include component smoothness (A3).',
   'D20':'The inherited conditions of Theorem 3 include the kernel condition (A4).',
   'D21':'The inherited conditions of Theorem 3 include the bandwidth condition (A5), which also defines h_j in the scaling.',
   'D22':'The inherited conditions of Theorem 3 include the conditional error bound (A6).',
   'D31':'The inherited conditions of Theorem 3 include (A7).',
   'D24':'The inherited compatibility condition and the explicit reference to (2.20) use phi.',
   'D16':'The new bandwidth restriction (3.11), as well as (2.20), uses |S|.',
   'D28':'The left side of the pointwise expansion uses the debiased component estimate.',
   'D1':'The pointwise expansion subtracts the true component f_j(x_j).',
   'D27':'The leading stochastic term contains the estimated row operator Theta-hat_j from (3.7).',
   'D30':'The three bandwidth upper bounds in (3.11) use s1, the maximum population inverse-kernel row sum defined before (A7).',
   'D32':'The leading stochastic term applies the estimated inverse row to the noise smoother m-hat-A.'},
5:{'D17':'The inherited conditions of Theorem 3 include the marginal-density condition (A1).',
   'D18':'The inherited conditions of Theorem 3 include the pair-density condition (A2).',
   'D19':'The inherited conditions of Theorem 3 include component smoothness (A3).',
   'D20':'The inherited conditions of Theorem 3 include the kernel condition (A4).',
   'D21':'The inherited conditions of Theorem 3 include (A5), and h_j occurs in the uniform scaling.',
   'D22':'The inherited conditions of Theorem 3 include the conditional error bound (A6).',
   'D31':'The inherited conditions of Theorem 3 include (A7).',
   'D24':'The inherited compatibility condition and the explicitly cited (2.20) use phi.',
   'D16':'The cited bandwidth condition (2.20) depends on |S|.',
   'D28':'The uniform expansion is for the debiased component estimates.',
   'D1':'The errors subtract the true additive components f_j(x_j).',
   'D27':'The stochastic approximation uses the estimated inverse row Theta-hat_j.',
   'D30':'The extra undersmoothing assumption is (1+s1 squared) n h cubed tending to zero.',
   'D32':'The uniform remainder subtracts the inverse-row transform of m-hat-A.'},
6:{'D17':'The theorem expressly assumes the marginal-density condition (A1).',
   'D18':'The theorem expressly assumes the pair-density condition (A2).',
   'D20':'The theorem expressly assumes the baseline kernel condition (A4).',
   'D21':'The theorem expressly assumes the bandwidth condition (A5).',
   'D31':'The theorem expressly assumes (A7); (A3) and (A6) are not listed.',
   'D27':'Both branches estimate the inverse through (3.7), and gamma occurs in their error rates.',
   'D29':'Theta_j and Theta_jk are the population inverse targets in the error and smoothness bounds.',
   'D26':'The first conclusion uses the mixed row norm with subscript 1,max.',
   'D30':'Both branches use the population inverse row size s1.',
   'D33':'The second branch uses the kernel sup norm and second derivatives in the kernel coordinate x_k.',
   'D34':'The final error bound uses s_q, defined in the theorem as a row sum of powered kernel sup norms.',
   'D35':'Only the second branch imposes the additional candidate-kernel derivative constraint in (3.7).'},
7:{'D33':'The density-ratio decay hypothesis (4.1) uses the sup norm on a two-variable kernel.',
   'D34':'The conclusion bounds both inverse-kernel summaries s_q and s_q star.'}}
EDGES={
'D2':{},
'D3':{},
'D4':{'D3':'The empirical joint and marginal densities average products of the normalized kernels K_h.'},
'D5':{'D2':'The loss is minimized over tuples of coordinate functions in the source additive spaces.','D3':'The loss integrates squared residuals against products of normalized kernels.','D4':'The centering constraints use the empirical marginal densities.'},
'D6':{'D3':'The marginal regression numerator uses normalized kernel weights.','D4':'It divides by the empirical marginal density p-hat_j.'},
'D7':{'D3':'The empirical pair density uses two normalized kernels with the same observation index.'},
'D8':{'D2':'The projection has domain L2 and coordinate-function codomain H_j.','D4':'Its conditional-density kernel is the empirical joint density divided by its marginal.'},
'D10':{'D5':'The penalized objective adds to the integrated loss L_n; the same empirical centering convention is retained.','D9':'The penalty and threshold use component density-weighted norms.','D4':'Those penalty norms are weighted by p-hat.','D6':'The threshold residual uses the marginal regression estimate m-hat_j.','D8':'The threshold characterization uses the coordinate projection of the other fitted components.'},
'D11':{'D2':'Coordinate integral kernels act on the source spaces H_k and H_j, and the block operator acts on their product.'},
'D12':{'D8':'The uncentered off-diagonal blocks restrict the empirical projection to another coordinate space.','D7':'Their explicit conditional-density kernels use p-hat_jk.','D4':'The denominators are empirical marginal densities.','D11':'The blocks are assembled using the generic integral-operator construction (2.10).'},
'D13':{'D10':'The penalty subgradient is evaluated at the penalized minimizer.','D9':'Its normalization and unit-ball case use the weighted norm.','D12':'The stationarity equation uses the original uncentered empirical operator from Section 2.','D6':'Its right side contains the marginal regression vector.','D2':'The zero-component subgradient belongs to the coordinate space H_j.'},
'D14':{'D12':'The partial-residual map subtracts the uncentered operator row applied to a tuple.','D6':'The remaining data-dependent term is the marginal regression estimate m-hat_j.'},
'D15':{'D14':'Each sequential update thresholds the partial-residual map Pi-hat_j^ominus.','D9':'The threshold uses its weighted norm.','D4':'The norm and initial centering are with respect to the empirical densities.'},
'D16':{'D1':'Significance is defined by the true additive component functions.','D9':'S and S_n are defined by nonzero weighted norms.','D4':'The second set S_n and the sufficient equality condition use empirical densities.'},
'D17':{'D1':'The marginal densities belong to the source additive-regression covariates.'},
'D19':{'D1':'The smooth functions are the true additive components.','D16':'The condition is restricted to the significant index set S.'},
'D22':{'D1':'The error is the response minus its additive conditional mean.'},
'D23':{'D4':'p^h is the expectation of the empirical joint density, with expected empirical marginals.'},
'D24':{'D23':'The compatibility ratio and centering use the expected smoothed density p^h.','D9':'The numerator is a weighted norm of a sum; the denominator sums weighted component norms.','D16':'The cone and denominator distinguish S from its complement.','D2':'The admissible tuple has each component in H_k.'},
'D25':{'D7':'The centered off-diagonal kernel uses the empirical pair density.','D4':'It divides by p-hat_j and subtracts p-hat_k.','D11':'The new kernel is assembled into a block integral operator with the same zero diagonal.'},
'D26':{'D11':'The row norms and mixed kernel norm are defined for generic coordinate integral operators.'},
'D27':{'D26':'Its constraint measures a row with the 1,max mixed kernel norm.','D25':'The approximate-inverse residual uses the centered empirical Pi-hat from (3.1).','D16':'The prescribed gamma in (3.6) depends on |S|.','D11':'The optimization variable Xi is a block integral operator.'},
'D28':{'D10':'The correction starts from the fLasso-SBF penalized estimator.','D13':'It applies the approximate inverse to the stationarity-compatible penalty subgradient.','D27':'The correction uses the proposed estimated inverse obtained from (3.7).'},
'D29':{'D11':'The population conditional-density kernels form a block integral operator and its inverse.'},
'D30':{'D29':'s1 and the discrepancy use the population inverse kernels Theta_jk and operator Pi.','D25':'The discrepancy subtracts the centered empirical operator Pi-hat.'},
'D31':{'D30':'(A7) differentiates the one-variable discrepancy magnitude delta-tilde_jk and uses s1.','D27':'Its rate restriction explicitly refers to gamma at (3.6).'},
'D32':{'D6':'Both components are the same marginal regression estimator with the response replaced.','D1':'The replacements are the additive conditional mean and its residual error.'},
'D33':{'D11':'The sup norm and derivative convention apply to a coordinate integral kernel.'},
'D34':{'D29':'The row and column summaries are formed from the population inverse kernels Theta_jk.','D33':'Each summand is a power of the kernel sup norm.'},
'D35':{'D27':'The added condition restricts the candidates in optimization (3.7).','D33':'The double prime means the derivative in the second kernel coordinate x_k.'}}

def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All seven source Theorems; distinguish explicit assumptions, definition dependencies and ambient notation.',build_order_policy='Topological ordering of source-backed paper-local dependencies.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGES.get(lid,{})),lid
    for c in data['claims']:
        n=int(c['claim_id'].split('/T')[-1]);c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            m=x['members'][0];lid=m['local_id']
            if lid in DIRECT[n]:x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']+m['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for rel in x['related_theorems']:
            cid=rel['claim_id'];n=int(cid.split('/T')[-1]);path=rel['via_local_ids']
            explanation=' '.join([DIRECT[n][path[0]]]+[EDGES[a][b] for a,b in zip(path,path[1:])])
            ev=copy.deepcopy(claims[cid]['evidence'])
            for lid in path:ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=explanation,evidence=ev)
        m=x['members'][0];own=m['statement_original']+' '+m['local_label']
        linked=own+' '+' '.join(claims[t['claim_id']]['statement_original'] for t in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors) and all(s in linked for s in selectors),m['local_id']
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Census structurally validated; independent source review remains pending.')
if __name__=='__main__':main()
