"""Finalize theorem-local model variants, conditional hypotheses and source paths."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'1':[1,2,6,8,17],'2':[1,2,6,8],'3':[1,2,7,8],'4':[1,2,8,10,13],'5':[2,8,10,14,15,16],'6':[1,2,5,8,9,21],'7':[1,2,3,5,9,10],'8':[1,2,8],'9':[1,2,17],'10':[1,2,20],'11':[1,2,8,22],'12':[1,2,8,23],'13':[1,2,24,25],'14':[6]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D3':{'D1':'Definition1 optimizes over history-adapted experimental actions and final estimators in the sequential observation experiment.','D2':'Its risk is evaluated under the ridge mean f(inner product), with the default known link, sphere parameter and ball action domain.'},
'D4':{'D1':'The cumulative regret compares the expected rewards of a sequential policy to the best fixed action in the same experiment.'},
'D5':{'D1':'Definition2 takes an infimum over history-adapted policies and a supremum over fixed unknown sphere parameters.','D2':'Its mean-reward comparator and realized action means use the ridge link.','D4':'The minimax objective is the expected cumulative regret, with the comparator variable correctly bound in Definition2.'},
'D6':{'D3':'Definition3 sets the burn-in cost to Tstar(f,d,1/2), the constant-accuracy expected signed-correlation minimax complexity.'},
'D7':{'D3':'Definition4 calls the same minimax sample complexity at accuracy1-epsilon; its use beyond the printed Definition1 domain is recorded explicitly.'},
'D11':{'D1':'The Eluder-UCB least-squares objective uses the past action/reward history, with no future observations.','D2':'Its residuals use the known ridge link on sphere-constrained parameter candidates.'},
'D12':{'D2':'The confidence set compares ridge predictions on the past actions.','D11':'Its center is the past-history sphere-constrained least-squares estimate, not Algorithm4’s final cap-constrained estimator.'},
'D13':{'D1':'The Eluder-UCB policy selects each action using the past-history confidence construction.','D2':'The optimistic reward maximized over candidate parameters is f(inner product).','D12':'The inner maximization is over the prediction-discrepancy confidence set C_t in(4).'},
'D14':{'D2':'The online error guarantee compares true ridge means with the sequence of oracle predictions, using f at each round’s output.'},
'D15':{'D2':'The offline error guarantee compares true ridge means with predictions from a single current output across all past actions.'},
'D16':{'D1':'The oracle model is explicitly a replacement of the original reward transcript: this reference identifies the experiment being replaced, not an additional raw-reward observation channel.','D14':'One allowed transcript model is the online guarantee(5), using an improper oracle in Theorem5.','D15':'The alternative is the offline guarantee(6), using a proper sphere-valued oracle in Theorem5; both alternatives are not imposed simultaneously.'},
'D17':{'D1':'Algorithm1 queries a sequential Gaussian oracle and samples candidate directions between queries.','D2':'Its known-link oracle and certification steps use the ridge mean function; even-link modifications are deferred to an excluded appendix.','D18':'The initial epochs call InitialActionHypTest with error delta/L and accuracy kappa1/4.','D19':'Subsequent epochs call GoodActionHypTest with previous direction/progress and the same scaled accuracy argument.','D20':'Algorithm1’s reference to Theorem9 supplies only kappa1,kappa2,c0,d0 and the associated parameter block, not the theorem’s performance conclusion.'},
'D18':{'D1':'The initial test repeatedly queries the Gaussian observation oracle and averages its samples.','D2':'Its finite-difference scale and projection feasibility test evaluate the known ridge link f.'},
'D19':{'D1':'The recursive test queries the two translated actions and forms two sample averages.','D2':'Its finite-difference maximization and common z,x feasibility test evaluate the known link f.'},
'D20':{'D2':'The parameter block defines finite differences of the ridge link. Theorem10 uses those mathematical quantities while explicitly withholding knowledge of f from the learner.'},
'D21':{'D1':'Algorithm4 first collects noisy rewards along a deterministic cyclic design and then commits to its estimate.','D2':'The cap-constrained least-squares objective uses the known ridge mean function.','D9':'The design and exploration budget use gamma and c_f from the local-linearity Assumption2; Theorem6 separately supplies the stronger initial correlation.'},
'D22':{'D1':'Nonadaptive sampling restricts the sequential policy by requiring all actions to be selected before observing the history.'},
'D24':{'D1':'The unit-ball variant retains the sequential observation and policy framework.','D2':'It retains the ridge mean function while explicitly replacing the default sphere parameter domain by the unit ball.','D4':'The objective is the minimax version of the same expected cumulative regret, now taking the worst parameter over the ball as stated in Theorem13.'}}
def direct_reason(n,lid):
    if lid=='D1':return f'Theorem{n} uses the sequential experiment of Section1: a fixed unknown parameter, history-adapted actions and Gaussian reward observations. Its explicit restrictions or information changes are retained in the theorem-local scope record.'
    if lid=='D2':
        override={'10':'Theorem10 keeps the ridge observation formula but explicitly removes knowledge of f, overriding the default known-link convention. Its continuous strictly increasing link is stated in the theorem.','12':'Theorem12 retains ridge rewards and sphere parameters but explicitly restricts the action domain to an existentially chosen finite subset of the ball.','13':'Theorem13 retains the ridge reward formula while explicitly changing the unknown parameter domain from sphere to ball.','5':'Theorem5’s oracle predictions and error bounds use the ridge mean formula; the learner receives the oracle transcript instead of noisy rewards.'}
        return override.get(n,f'Theorem{n} concerns the ridge bandit mean f(inner product), with the default link and geometric conventions of Section1 except where its statement explicitly specializes them.')
    if lid=='D8':return ('Only the regret branch of Theorem6 additionally assumes Assumption1; its estimation branch requires Assumption2 and the supplied initial action.' if n=='6' else f'Theorem{n} explicitly assumes Assumption1, retaining both normalized scale and its alternative monotonicity branches. Any extra even/odd or Lipschitz restriction is stated separately in that theorem.')
    if lid=='D6':return ('Theorem14 evaluates the Definition3 burn-in cost at the inline linear link id(x)=x; it retains the expected signed-correlation target at accuracy1/2.' if n=='14' else f'Theorem{n} explicitly bounds Tstar_burn-in(f,d), the Definition3 specialization of minimax estimation complexity at accuracy1/2.')
    if lid=='D10':return ('Theorem7 explicitly assumes the global L-Lipschitz condition in Assumption3, and allows its lower-bound constant to depend on L.' if n=='7' else f'Theorem{n} quantifies every Lipschitz link f. Assumption3 records the same global finite-L inequality on[-1,1]; no fixed numerical L or positive lower slope is added.')
    if lid=='D17':return f'Theorem{n} explicitly identifies Algorithm1 as its attaining procedure. The complete main-text algorithm and both certification calls are preserved; parameter references do not import a theorem conclusion as a premise.'
    if lid=='D9':return f'Theorem{n} explicitly assumes Assumption2, the differentiable locally linear regime near1 with c_f,C_f and gamma. This is not a global derivative lower bound.'
    if lid=='D5':return ('Theorem6’s regret branch uses the minimax-regret notation from Definition2 for the upper bound achieved by Algorithm4; this is distinct from its estimation guarantee.' if n=='6' else 'Theorem7’s second inequality lower-bounds the Definition2 minimax cumulative regret over sphere parameters and adaptive policies.')
    reasons={
('3','D7'):'Theorem3 explicitly bounds Tstar_burn-in(f,d,epsilon), the Definition4 minimax learning trajectory, with separate upper and lower branches.',
('4','D13'):'Theorem4 explicitly refers to (El-UCB) and asserts existence of a tie-breaking rule for that optimistic action maximization.',
('5','D14'):'One Theorem5 alternative is an improper online regression oracle satisfying(5), whose error sum uses the sequence of predictions theta_hat_s.',
('5','D15'):'The other Theorem5 alternative is a proper offline oracle satisfying(6), whose error sum uses the current theta_hat_t for every past action.',
('5','D16'):'Theorem5 quantifies every learner under the selected oracle transcript model; its proper/improper convention and replacement of reward observations are stated immediately beforehand.',
('6','D21'):'Theorem6 explicitly names Algorithm4 for both its estimator and regret guarantee; the source algorithm contains separate exploration budgets and a cap-constrained final least-squares fit.',
('7','D3'):'Theorem7’s first inequality uses Tstar(f,d,epsilon), the Definition1 minimax expected signed-correlation estimation complexity.',
('10','D20'):'Theorem10 explicitly imports the setting of Theorem9, including its target, failure probability, numerical parameters and finite-difference epsilon_i sequence. It replaces the known-link algorithm requirement by existence of an algorithm without knowledge of f.',
('11','D22'):'Theorem11 restricts to nonadaptive learners, whose actions are chosen in advance as defined in Section4.1, and separately imposes a uniform-sphere prior.',
('12','D23'):'Theorem12 asserts existence of a hard finite action set A of cardinality K; Section4.2 specifies A as a finite subset of the unit ball, not an arbitrary unbounded set.',
('13','D24'):'Theorem13 explicitly takes minimax regret over theta-star in the unit ball, the parameter-domain variant introduced in Section4.3. The sphere supremum in Definition2 is not imported literally.',
('13','D25'):'Theorem13 references only the monotonicity condition in Assumption1. D25 preserves exactly that item, without adding the separate normalized-scale requirement.'}
    return reasons[(n,lid)]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All fourteen original main-text Theorems retained, including weaker versions and both branches. Preserve source definitions, assumptions, algorithms and distinct observation/parameter variants.',build_order_policy='Derive local paths from source references, distinguishing conditional regret assumptions, alternative oracle models and algorithm parameter blocks from conclusions. Keep Bayes/minimax, adaptive/nonadaptive and sphere/ball scopes distinct. Exclude appendix bodies and preserve unresolved source references.')
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
    for x in data['interfaces']:
        for obj in [*x['central_claim_uses'],*x['theorem_explanations'].values()]:
            for e in obj.get('evidence',[]):
                if e.get('page')==29:e['before_main_text_end']=True
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Census structurally validated; independent source review remains pending.')
if __name__=='__main__':main()
