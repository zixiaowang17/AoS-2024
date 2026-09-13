"""Finalize this paper's source-backed graph, preserving the original theorem inventory."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
'3.3':{'D1':'The probability bound concerns the iid regression observations with signal f0 and noise epsilon.',
'D2':'The statement explicitly assumes Condition 1 for the design support and bound on f0.',
'D3':'The statement explicitly assumes Condition 2, here with the stronger restriction p>=2.',
'D10':'The statement explicitly sets F_n=F_n(d,L-bar,N-bar,M).',
'D11':'Its displayed approximate-minimizer set uses the empirical Huber loss R-hat_tau.',
'D13':'The approximation term and concentration event both use the population L2 norm.',
'D16':'The statement defines S_n,tau(delta) and uniformly bounds the errors of its members.'},
'3.5':{'D1':'The uniform probability bound is over regression signals and conditional mean-zero noise under the standing iid model.',
'D2':'The statement explicitly assumes Condition 1 and retains the output bound M.',
'D3':'The supremum explicitly restricts conditional mean and absolute p-th moment, and v2 and v_p retain their source moment meanings.',
'D6':'The supremum ranges over f0 in the hierarchical composition class H(d,l,P).',
'D7':'The statement explicitly takes beta-star, d-star and gamma-star from (2.6).',
'D10':'The theorem explicitly selects the truncated class F_n(d,L-bar,N-bar,M).',
'D13':'The error inside the probability is measured by the population L2 norm.',
'D16':'The inner supremum is over S_n,tau_n(delta_n,AH), the approximate-minimizer set defined in Theorem 3.3.',
'D21':'The theorem explicitly defines its architecture through (3.15) and the constants from Proposition 3.4.'},
'3.6':{'D1':'The least-squares bound is for the standing iid regression experiment.',
'D2':'The statement explicitly assumes Condition 1.',
'D3':'The supremum specifies zero conditional noise mean and conditional p-th moment bounded by v_p; v2 is also bounded in the hypothesis.',
'D6':'The regression functions range over H(d,l,P).',
'D7':'The statement expressly references (2.6) for beta-star, d-star and gamma-star.',
'D10':'The statement names F_n(d,L-bar,N-bar,M) as the network class.',
'D13':'The concentration bound controls the population L2 error.',
'D16':'Its estimator set is S_n,infinity(delta_n,LS), using the squared-tolerance convention from Theorem 3.3.',
'D21':'Its width and depth are explicitly required to satisfy (3.15).'},
'3.7':{'D1':'The symmetric-noise error bound concerns the same iid nonparametric regression observations.',
'D2':'The statement explicitly assumes Condition 1.',
'D4':'The statement explicitly assumes Condition 3, which provides conditional symmetry and first-moment control.',
'D6':'The supremum prints H(l,d,P), referring to the earlier hierarchical composition model with transposed argument notation retained.',
'D7':'The rate and architecture depend on gamma-star, the component smoothness ratio defined in (2.6).',
'D10':'The theorem expressly sets F_n=F_n(d,L-bar,N-bar,M).',
'D13':'The displayed error uses the population L2 norm.',
'D16':'The displayed S(delta_n,H) is read in the preceding approximate-Huber-estimator setting of S_n,tau(delta); the omitted subscripts remain documented as a source ambiguity.',
'D21':'The theorem expressly requires the architecture (3.15).'},
'4.1':{'D1':'The data-generating triples and empirical losses are interpreted through the standing iid regression model.',
'D10':'The displayed set uses the truncated network class F_n(d,L-bar,N-bar,1).',
'D11':'The two eligibility branches in (4.3) compare empirical Huber losses.',
'D13':'Both lower-bound events use the population L2 norm.',
'D15':'The first branch in (4.3) compares empirical loss to that of the population minimizer f0,tau from (3.7).',
'D17':'The hypothesis imposes the intrinsic dimension-adjusted smoothness property of Definition 4.1 on F0.',
'D18':'The theorem defines U(d,p,F), then takes suprema over U(d,p,F0).',
'D19':'The bad-estimator existence events range over the distinct S_HN set defined in (4.3).'},
'4.2':{'D13':'The two lower-bound events use the population L2 norm.',
'D17':'The explicit reference to F0 as in Theorem 4.1 carries its intrinsic dimension-adjusted smoothness condition and zero-function membership.',
'D18':'The theorem expressly imports U(d,p,F) from Theorem 4.1 and specializes the displayed suprema to F0.',
'D19':'The theorem expressly imports S_HN from Theorem 4.1 and evaluates it at tau=infinity.'},
'4.3':{'D10':'The approximation infimum ranges over the expressly specified F_n(d,L-bar,N-bar,1).',
'D13':'The statement explicitly identifies the L2 norm under the uniform design law.',
'D17':'Its F0 hypothesis uses intrinsic dimension-adjusted smoothness as defined in Definition 4.1.'},
'4.5':{'D9':'The conclusion constructs two deep ReLU networks, with the source width/depth convention and without an asserted global output truncation.',
'D20':'The theorem defines the grid size, indexed values and Q_alpha(Delta) regions in (4.8).'},
'4.6':{'D9':'Both constructed functions are deep ReLU neural networks in the source architecture convention.',
'D20':'The hypotheses explicitly refer to Q_alpha(Delta1) from (4.8), and the conclusion uses their union Q.'}}
EDGES={
'D6':{'D5':'The recursive components are explicitly required to be (beta,C)-smooth.'},
'D7':{'D6':'The minimum ratio uses the smoothness/arity index set P of the hierarchical composition model.'},
'D10':{'D9':'The truncated class is T_M applied to the untruncated class of deep ReLU networks.'},
'D11':{'D1':'The residuals use Yi and Xi from the iid additive regression model.','D8':'Each residual is evaluated by the Huber loss ell_tau.'},
'D12':{'D1':'Population expectation is taken under the regression law of X,Y.','D8':'The integrand is the Huber loss ell_tau.'},
'D14':{'D2':'The measurable comparison class uses the same M>=1 and supremum-norm convention as Condition 1.'},
'D15':{'D12':'The selected minimizer minimizes the population Huber risk R_tau.','D14':'Its minimization domain is Theta, the bounded measurable class.'},
'D16':{'D10':'The approximate minimizers belong to the chosen truncated network class.','D11':'The defining inequality compares empirical Huber risks with objective tolerance delta squared.'},
'D17':{'D1':'The defining Gaussian experiment uses Yi=f0(Xi)+epsilon_i and iid observations, with its expressly specified special design and noise laws.','D13':'The defining minimax risk is expectation of the squared population L2 error.'},
'D18':{'D1':'The triples specify the components of the additive regression experiment whose iid samples generate the data.'},
'D19':{'D10':'The admissible candidate functions lie in the truncated network class at M=1.','D11':'Both eligibility branches compare empirical Huber loss values.','D15':'The first branch contains the empirical loss evaluated at the population Huber minimizer f0,tau.'},
'D21':{'D6':'The named constants c3,c4 are those of Proposition 3.4 and depend on the hierarchical composition parameters; their source statement is retained as auxiliary context.','D10':'The architecture specifies the width and depth of the explicitly named truncated class F_n(d,L-bar,N-bar,M).'}}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All nine original main-text Theorems; preserve upper/lower estimator sets, moment/symmetry alternatives and approximation-only results.',build_order_policy='Source-backed same-paper definition graph; do not use Figure 2 proof arrows as statement edges.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGES.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            m=x['members'][0];lid=m['local_id']
            if lid in DIRECT[n]:x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']+m['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for rel in x['related_theorems']:
            cid=rel['claim_id'];n=cid.split('/T')[-1];path=rel['via_local_ids']
            ex=' '.join([DIRECT[n][path[0]]]+[EDGES[a][b] for a,b in zip(path,path[1:])])
            ev=copy.deepcopy(claims[cid]['evidence'])
            for lid in path:ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=ex,evidence=ev)
        m=x['members'][0];own=m['statement_original']+' '+m['local_label']
        linked=own+' '+' '.join(claims[t['claim_id']]['statement_original'] for t in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors) and all(s in linked for s in selectors),m['local_id']
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    check=json.loads((ROOT/'ranked-interfaces.json').read_text())
    assert [{k:v for k,v in c.items() if k!='depends_on'} for c in check['claims']]==inv['claims']
    print('Census structurally validated; full independent source review remains pending.')
if __name__=='__main__':main()
