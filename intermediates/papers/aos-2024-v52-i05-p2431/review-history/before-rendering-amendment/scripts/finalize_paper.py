"""Build model-local dependencies without turning conditional hardness into a theorem."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'2.2':[4,7,8,10,14],'3.1':[4,7,14],'3.3':[4,5,8,9,10,14],'4.1':[2,4,5,8,11,12],'4.2':[4,5,6,7,8,9,13]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D4':{'D1':'Definition1 generates edges according to the conditional independent Bernoulli multi-layer model(1).','D2':'Its node and layer priors are uniform over exactly balanced binary assignment sets S_n and S_T.','D3':'Each layer uses B^(tau_t), one of the two fixed assortative/disassortative matrices with probabilities rho/2 and3rho/2.'},
'D7':{'D2':'The recovery estimator is required to output a balanced binary vector in S_n.','D4':'The recovery probability is evaluated under the joint balanced-mixture law of (A,sigma,tau).','D6':'Its vanishing-error criterion uses the normalized Hamming loss after the optimal global label swap.'},
'D8':{'D4':'The alternative testing error is evaluated on an A-measurable test under the balanced-mixture observation marginal.','D5':'The null testing error uses the independent Bernoulli-rho observation law.'},
'D10':{'D4':'Conjecture3.2 restricts the alternative to the specific balanced mixture in Definition1.','D5':'Its polynomial normalization and centering are under the independent-edge null law.','D8':'The conjectured conclusion rules out distinguishability, meaning vanishing sum of testing errors, by efficient tests.','D9':'The conjecture explicitly assumes the layer/density regime in Assumption1.','D14':'Its computational conclusion uses the paper’s runtime convention of a polynomial in n.'},
'D11':{'D2':'The conditioning layer identity ranges over the balanced set S_Tn, and the fixed-label law also indexes sigma in S_n.','D4':'The conditional law is derived from P1,n by fixing tau; the theorem then takes its A marginal, leaving sigma latent.'},
'D13':{'D2':'The joint edge-count optimization ranges over balanced node and layer labels, S_n and S_Tn.'}}
def direct_reason(n,lid):
    label='Theorem '+n
    if lid=='D2':return 'Theorem4.1 explicitly quantifies its conditional divergence bound over every balanced layer assignment tau in S_Tn.'
    if lid=='D4':return label+' concerns P1,n, the balanced two-community mixture of Definition1'+('; its recovery probability uses the latent joint law, whereas its testing interpretation uses the observation marginal.' if n in ['2.2','4.2'] else ', with unknown balanced node and layer labels.' if n in ['3.1','3.3'] else ', whose A-marginal chi-square divergence from the null is asserted to vanish.')
    if lid=='D5':return label+' explicitly uses P0,n, the independent Bernoulli-rho graph-tensor null'+(' in its computational detection impossibility.' if n=='3.3' else ' as the chi-square reference and indistinguishability null.' if n=='4.1' else ' in its concluding distinguishability statement.')
    if lid=='D6':return 'Theorem4.2 explicitly uses the Definition2 loss ell_n(sigma-hat_mle,sigma), the normalized Hamming distance minimized over the two global node-label permutations.'
    if lid=='D7':return label+' asserts recoverability in the precise Definition2 sense of a vanishing mislabeled fraction under the mixture prior'+('; the first bullet has no runtime constraint, while the second concerns polynomial-time estimators.' if n=='2.2' else ' using a polynomial-time estimator.' if n=='3.1' else ' for the sigma component of the joint MLE, not exact recovery of both latent vectors.')
    if lid=='D8':return label+(' explicitly extends both threshold statements to detection, meaning the strong distinguishability criterion of Definition2.' if n=='2.2' else ' states that no polynomial-time test can achieve Definition2’s vanishing total error, conditional on Conjecture3.2.' if n=='3.3' else ' concludes indistinguishability after its vanishing chi-square bounds; the converse is not asserted.' if n=='4.1' else ' concludes that the model is distinguishable from P0,n in Definition2’s strong-testing sense.')
    if lid=='D9':return label+(' explicitly invokes Assumption1 and also assumes Conjecture3.2, which requires the full (T_n,rho_n) regime.' if n=='3.3' else ' explicitly requires (T_n,rho_n) to satisfy Assumption1 in addition to n*T_n*rho_n tending to infinity.')
    if lid=='D10':return label+(' assumes the low-degree polynomial conjecture in its computational bullet only; its information-theoretic bullet remains unconditional.' if n=='2.2' else ' explicitly assumes Conjecture3.2, including uniform boundedness over all centered, null-L2-normalized polynomials of degree at most log^1.01(n). The conjecture is not certified by this census.')
    if lid=='D11':return 'Theorem4.1 bounds d_chi2(P1,tau,n,P0,n) for known balanced tau. Its explicit sum over A uses the observation marginal of the conditional joint law of (A,sigma), leaving sigma unobserved.'
    if lid=='D12':return 'Theorem4.1 explicitly uses directed chi-square divergence, with P0,n(A) in the denominator and alternative A-marginal mass squared in the numerator. The preceding prose’s reversed p/q naming is preserved separately.'
    if lid=='D13':return 'Theorem4.2 applies ell_n to sigma-hat_mle from(4), the sigma component of the joint balanced-label argmax of edge counts on even-parity triples; no polynomial-time implementation is asserted.'
    if lid=='D14' and n=='3.1':return 'Theorem3.1 asserts polynomial-time recovery. The n-based runtime convention is stated later in the lower-bound discussion; the complete T-dependent runtime of the externally credited upper-bound algorithm is not given locally.'
    if lid=='D14':return label+' uses polynomial-time as polynomial in the node count n'+(' for its second bullet only.' if n=='2.2' else ' in its algorithmic upper bound.' if n=='3.1' else ', with polynomial input size under its actual negative-log threshold; the sign mismatch in surrounding prose is separately retained.')
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All five main-text Theorems retained, including the simplified summary and credited upper bound; Conjecture3.2 remains an assumed source passage.',build_order_policy='Keep latent joint laws distinct from observed-data marginals, approximate recovery distinct from strong detection, and conjectural computational lower bounds distinct from unconditional information-theoretic results. No proof-only or implication-only graph edges.')
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
