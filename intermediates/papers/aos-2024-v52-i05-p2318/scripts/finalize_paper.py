"""Build graphon theorem dependencies without importing proof-only priors or runtime conjectures."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'1':[1,3,5,6],'2':[1,3,5,8],'3':[1,3,8,9],'4':[2,3,5,12],'5':[1,5,8,13,14],'6':[1,3,5,15],'7':[16,19,20,21]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'The latent graphon f and positions xi induce the matrix of probabilities for the conditional independent Bernoulli sampling experiment.'},
'D5':{'D4':'Each matrix entry is a real scalar polynomial of total degree at most D, instantiating the Section2.1 polynomial space to observed adjacency coordinates.'},
'D8':{'D7':'The iid uniform-label prior is supported on the homogeneous p,q SBM class (13), whose off-diagonal entries depend only on label equality.'},
'D11':{'D10':'The symmetric Holder class uses the exact norm with floor(gamma) derivatives and gamma−floor(gamma) increment exponent on the lower triangle.'},
'D12':{'D11':'The smooth graphon class F_gamma(L) restricts the Holder class H_gamma(L) to values between zero and one.'},
'D13':{'D7':'ZM is defined from a matrix in the homogeneous SBM class using (Mij−q)/(p−q) off diagonal.'},
'D16':{'D17':'The Gaussian observation model explicitly supplies a signal in the rectangular biclustering parameter space M_(k1,k2).'},
'D19':{'D18':'The biclustering prior is supported on the diagonal block-level subset with value lambda on matched row/column labels and zero otherwise.'},
'D21':{'D4':'Each rectangular estimator entry belongs to the same scalar degree-D polynomial space, now on all Gaussian observation coordinates Y.'}}
def direct_reason(n,lid):
    label='Theorem '+n
    if lid=='D1':return label+(' evaluates worst-case expected loss under the conditional independent Bernoulli sampling law (1) for each fixed matrix M.' if n in ['1','6'] else ' uses the joint SBM experiment: draw M from the stated prior, then sample symmetric Bernoulli edges conditionally independently with zero diagonal. For T3 the algorithm adds independent auxiliary randomness.')
    if lid=='D2':return 'Theorem4 uses Mf_ij=f(xi_i,xi_j) and a supremum over the arbitrary latent-position distribution Pxi, with iid positions and the corresponding conditional graphon sampling law.'
    if lid=='D3':return label+' uses the empirical off-diagonal loss (2), normalized by binomial(n,2). The second matrix argument is '+('the sampled graphon target Mf.' if n=='4' else 'M; evaluating the same arithmetic discrepancy on M does not require a latent-position representation.')
    if lid=='D5':return label+' takes the infimum over entrywise degree-D polynomials in A, using the matrix convention stated in Theorem1 and repeated in Theorem2. No symmetry or range constraint on the estimator is added.'
    if lid=='D6':return 'Theorem1 supremizes over the full k-class matrix space Mk in (10), with arbitrary symmetric block probability matrix Q and arbitrary labels. Its proof prior is not a restriction on this parameter space.'
    if lid=='D8':return label+' explicitly uses P_SBM(p,q), the distribution induced by iid uniform labels and the homogeneous two-level connectivity formula. The prior does not condition on balanced or nonempty classes.'
    if lid=='D9':return 'Theorem3 explicitly refers to Algorithm1 for its estimator. This imports the diagonal fill, independent Gaussian sketch, power iteration and gradient recurrence; the theorem supplies its own r,t1,t2,eta and sample-size conditions.'
    if lid=='D12':return 'Theorem4 supremizes over F_gamma(L), the probability-valued symmetric Holder class defined immediately before it, and imposes gamma>0.5. It does not assume the homogeneous SBM used in the proof construction.'
    if lid=='D13':return 'Theorem5 estimates ZM from (23), the off-diagonal co-membership matrix determined by M,p,q. Numeric label permutations do not affect this target.'
    if lid=='D14':return 'Theorem5 uses the Section5 pairwise squared loss ell(Zhat,ZM), normalized over unordered off-diagonal pairs. It is not label Hamming loss.'
    if lid=='D15':return 'Theorem6 takes a supremum over M_(k,rho), the sparse probability-matrix class in (26), whose entries and block probabilities lie in [0,rho]. Its lower bound assumes the additional displayed lower bound on rho.'
    if lid=='D16':return 'Theorem7 uses the Section6.2 observation model Y=M+E with iid standard Gaussian entries in E. The expectation combines this experiment with the specified signal prior.'
    if lid=='D19':return 'Theorem7 averages over P_BC(lambda), with independent row and column labels each uniform on the same min(k1,k2) classes, producing Mij=lambda when the labels match.'
    if lid=='D20':return 'Theorem7 uses the rectangular squared loss averaged over all n1*n2 entries, distinct from the earlier off-diagonal graph losses.'
    if lid=='D21':return 'Theorem7 takes the infimum over n1-by-n2 matrix-valued degree-D polynomials in Y; its Gaussian observation space is separate from the adjacency-matrix experiment.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All seven main-text Theorems retained, including the randomized upper bound and every in-particular clause.',build_order_policy='Preserve fixed-parameter versus prior risks, conditional Bernoulli versus rectangular Gaussian observations, matrix-loss normalizations and algorithm-specific dependencies. No proof-only prior, cumulant or runtime conjecture becomes a theorem premise.')
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
