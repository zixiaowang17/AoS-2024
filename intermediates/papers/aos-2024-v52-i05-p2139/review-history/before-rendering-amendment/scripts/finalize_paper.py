"""Build the census while preserving the original privacy definitions, distinct regularity assumptions and complete estimators."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'3.3':[1,3,5,6,7],'3.5':[1,3,5,6],'4.1':[],'4.2':[1,2,5,8],'4.3':[4,9],'4.11':[1,2,6,10,11,12,13,14],'4.12':[1,2,3,6,10,11,12,15]}
DIRECT={n:['D'+str(i) for i in ids] for n,ids in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'Q_alpha consists of Markov kernels with the printed eventwise privacy inequality.'},
'D3':{'D1':'The joint sanitized law is built by composing conditional Markov kernels.','D2':'Every conditional kernel at every sanitized history belongs to the marginal private channel class.'},
'D4':{'D1':'The non-interactive mechanism is a tensor product of marginal Markov kernels.','D2':'Each marginal kernel must belong to Q_alpha; the marginals need not be identical.'},
'D6':{'D5':'Fisher information is the second moment of the score supplied by DQM at the specified parameter.'},
'D8':{'D1':'The private model density integrates q(z|x) against p_theta(x) under kernel action.','D2':'The fixed marginal channel is required to belong to Q_alpha(X).','D4':'The observations in this likelihood are sanitized non-interactively, with a common fixed marginal channel.'},
'D10':{'D5':'Condition C1 imposes Definition 1 at every parameter with a common dominating measure.'},
'D11':{'D5':'Condition C2 imposes joint measurability on the density and score versions of the DQM model.'},
'D12':{'D5':'Condition C3 requires L2 continuity of the DQM score multiplied by the square-root density.'},
'D13':{'D10':'Definition 3 explicitly assumes Condition C1 and uses dot p_theta=s_theta p_theta in its histogram error.'},
'D15':{'D1':'The two-step procedure uses kernel composition Qhat That and integrated conditional densities.','D2':'Its preliminary Q0 is a marginal alpha-private channel.','D4':'The first stage and conditional second stage sanitize their respective samples non-interactively.','D5':'The input statistical model is regular, meaning DQM at every parameter under the page-9 convention.','D6':'Step 4 maximizes the scalar Fisher information at the preliminary estimate.','D13':'Step 3 uses Definition 3 with m=n1, including its parameter-dependent quantizer and finite alphabet.','D14':'Step 4 optimizes over the privacy-constrained column stochastic matrix domain M_alpha(khat,khat).'}}
def direct_reason(n,lid):
    if lid=='D1':return 'Theorem '+n+' uses private distributions or models written QP, Q^(n)P^n or Qhat That P, with kernel action and deterministic composition defined in Section 1.2.'
    if lid=='D2':return 'Theorem '+n+' explicitly uses Q_alpha(X) or Q_alpha(X->Z0), the all-input marginal private channel class (1.4)-(1.5); scalar unrestricted-output suprema use the footnote-1 convention A2.'
    if lid=='D3':return 'Theorem '+n+' names the alpha-sequentially interactive mechanism Q^(n), defined by conditional private kernels in (1.6). '+('For the two-step estimator, A13 retains its specific protocol (4.3).' if n=='4.12' else 'The countably generated sigma-fields and all-history conditions remain explicit.')
    if lid=='D4':return 'Theorem 4.3 asserts non-interactive alpha-privacy for the estimator formed from independently sanitized Z_i; (1.7) specifies the product mechanism behind that assertion.'
    if lid=='D5':return 'Theorem '+n+' explicitly assumes DQM '+('at every theta; A3 supplies the all-parameter convention and the source explicitly notes that Theta is open.' if n=='4.2' else 'at its specified parameter theta, with the score and quadratic-mean remainder of Definition 1.')
    if lid=='D6':return 'Theorem '+n+' uses I_theta of original or privatized models, the score second-moment information from Section 3.1. '+('A6 retains the average conditional information Sigma_n,theta referenced from Theorem 3.3; importing that definition does not import its LAMN conclusion.' if n=='3.5' else 'Scalar-valued information is restricted to the theorems that explicitly assume p=1 or Theta contained in R.')
    if lid=='D7':return 'Theorem 3.3 concludes LAMN with delta_n=J_p/sqrt(n), its displayed Delta_n,theta and Sigma_n,theta. Definition 2 requires joint mixed-normal convergence and allows singular limiting information.'
    if lid=='D8':return 'Theorem 4.2 names the non-interactive alpha-private MLE from Section 4.1.1: a measurable maximizer of the sum of log integrated private densities. The convergence event remains intersected with each compact K.'
    if lid=='D9':return 'Theorem 4.3 uses Pi_tau_n[g(X_i)], the page-15 hard truncation to zero outside the l1 ball, before adding independent Laplace noise; it does not project onto the ball boundary.'
    if lid=='D10':return 'Theorem '+n+' explicitly assumes Condition C1: DQM at every parameter with score s_theta and dominating measure mu.'
    if lid=='D11':return 'Theorem '+n+' explicitly assumes Condition C2: joint measurability in x and theta of the chosen density and score.'
    if lid=='D12':return 'Theorem '+n+' explicitly assumes Condition C3: continuity of theta->s_theta sqrt(p_theta) into L2. Positive-definite Fisher information is not part of C3.'
    if lid=='D13':return 'Theorem 4.11 explicitly references Definition 3 for T_m,k_m and Delta_n1(tilde theta_n1). Its error uses histogram approximations and a square-root tail term and must vanish along every convergent parameter sequence.'
    if lid=='D14':return 'Theorem 4.11 names M_alpha(khat,khat) from Lemma 4.5 as the feasible matrix domain, with unit column sums and privacy ratios across each fixed row.'
    if lid=='D15':return 'Theorem 4.12 names the two-step MLE theta_hat_n2 and the mechanism described immediately above it. The six steps retain a consistent private preliminary estimator, adaptive quantizer, measurable Fisher maximizer and second-group conditional likelihood, including the arbitrary fallback if no maximizer exists.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All seven complete main-text Theorems, including the classical raw-data likelihood result and the two scalar privacy results.',build_order_policy='Same-paper statement dependencies with separate C1-C3 assumptions, complete quantizer and estimator construction; proof-only references do not add dependencies.')
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
