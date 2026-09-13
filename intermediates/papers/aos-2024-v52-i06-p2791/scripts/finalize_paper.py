"""Derive original same-paper statement relationships and validate the census."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'3.1':[1,3,4,5,6,7,8,9,10],'3.3':[1,2,6,10,11,13,14,15],'3.4':[1,2,3,6,10,11,14,15],'3.5':[1,2,6,10,11,14,15,16],'3.6':[1,2,6,10,11,14,15,18],'4.1':[6,11,23,24],'4.5':[2,5,17,20,21],'4.11':[2,7,14,15,19,22]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D3':{'D2':'The simultaneous bounded-Lipschitz class consists of convex functions onOmega.'},
'D4':{'D2':'The Lipschitz-only class is the stated subclass of all convex functions.'},
'D5':{'D2':'The bounded-only class restricts the same convex-function class by its absolute bound.'},
'D9':{'D8':'Loss4 integrates against the uniform design law P specified immediately before it.'},
'D10':{'D1':'The subscript on expectation specifies the true regression function and observation law from model1.'},
'D13':{'D2':'Class9 requires its members to be convex onOmega.','D11':'Its distance-to-affine constraint uses the unsquared empirical distance from8.','D12':'The comparison infimum ranges over all affine functions in A(Omega).'},
'D14':{'D7':'After the slab representation14 the source explicitly imposes the normalized domain condition3.'},
'D15':{'D7':'The grid size relation16 and small-delta convention are stated under domain condition3.'},
'D16':{'D2':'The piecewise-affine class is explicitly a subclass of C(Omega).','D15':'Its partition is imposed on intersections with the regular grid S from15.'},
'D18':{'D3':'Lemma3.2 requires its chosen approximation to belong to C_(C_d)^(C_d), the bounded-Lipschitz class.','D7':'Lemma3.2 explicitly imposes domain condition3.','D17':'Its cells are full-dimensional simplices and carry the stated shared-facet conditions.'},
'D21':{'D5':'The local Lp ball42 consists of functions from the Gamma-bounded convex class.'},
'D22':{'D15':'The discrete norm sums over the grid-domain intersection, with n its cardinality.','D19':'The following sentence defines N(epsilon,F,ell_S) as the covering number for this induced metric.'},
'D23':{'D11':'The local supremum is restricted by empirical distance ell_(P_n)(f,g)<=t.'},
'D24':{'D23':'The radius t_f is defined as the maximizing argument of H_f(t,F) over nonnegative t.'}}
REASONS={
'3.1':{1:'The risk concerns the Gaussian convex regression observations of model1.',3:'Its first branch includes the class C_L^B(Omega) with B>=L.',4:'The alternative first-branch class is the Lipschitz-only C_L(Omega).',5:'Its additional polytopal branch uses the bounded-only class C^B(Omega).',6:'Each displayed risk evaluates the least-squares estimator hat f_n on the indicated class.',7:'The first sentence requires the convex body to satisfy3.',8:'This is the random-design result in3.1 under the iid uniform design convention on3.',9:'Both inequalities use squared population loss ell_P².',10:'The risk expectation E_f averages observations under the true regression function f.'},
'3.3':{1:'Section3.2 explicitly imports the Gaussian regression setup from2.2.',2:'The estimator ranges over the unrestricted class C(Omega).',6:'The displayed estimator is hat f_n(C(Omega)), the minimizer defined in2.',10:'E_f is the source risk expectation under true function f.',11:'The bound is for the squared empirical loss ell_(P_n)².',13:'The supremum is over the distance-to-affine class F^frakturL defined in9.',14:'The imported2.2 domain is the slab polytope14; its slab count F appears in the logarithmic powers.',15:'The imported2.2 fixed-design points are precisely the small-delta lattice intersection15–16.'},
'3.4':{1:'The rate uses the Gaussian model in the fixed-design setup imported at the start of3.2.',2:'The fitted function is the unrestricted convex LSE over C(Omega).',3:'The supremum is over the bounded-Lipschitz class with both bounds equal to L.',6:'The displayed hat f_n(C(Omega)) is the least-squares selection from2.',10:'E_f is expectation under the true function f.',11:'The squared error in22 is the empirical loss ell_(P_n)².',14:'The Section3.2 standing domain is the normalized slab polytope of14.',15:'The standing design enumerates the grid points inOmega as in15–16.'},
'3.5':{1:'The adaptive risk bound uses the Gaussian observations in the standing fixed-design setup.',2:'Its estimator fits over all convex functions C(Omega).',6:'The estimator is the original unrestricted least-squares selection.',10:'E_f averages the squared error under regression function f.',11:'The displayed loss is the squared empirical metric from8.',14:'Section3.2 assumes the slab-polytope domain of2.2.',15:'The observations use the regular grid15 with the small-resolution convention16.',16:'The supremum class C_(k,h)(Omega) is defined immediately above by affine pieces on a grid partition.'},
'3.6':{1:'The lower bound retains the Gaussian noise variance sigma² from the standing regression model.',2:'The estimator is fit over unrestricted C(Omega).',6:'The displayed hat f_n(C(Omega)) is the least-squares selection.',10:'The subscript tilde f_k on E specifies this chosen true regression function.',11:'The error measured in25 is squared empirical loss ell_(P_n)².',14:'The theorem is in3.2, which imports the polytopal domain14.',15:'The fixed-design points and n follow the regular grid15–16.',18:'The last sentence explicitly identifies tilde f_k as the function from Lemma3.2.'},
'4.1':{6:'The statement explicitly invokes the LSE defined in2 over its own convex class F.',11:'Its localized supremum and both risk inequalities use empirical distance ell_(P_n).',23:'The statement defines H_f as the expected local Gaussian supremum minus t²/2.',24:'It defines t_f as the argmax of H_f and bounds the LSE error using this radius.'},
'4.5':{2:'The center and members of42 are convex functions onOmega.',5:'The local class42 uses C^Gamma(Omega), the uniformly bounded convex class.',17:'The assumed Delta_i are d-simplices, defined in3.1 as hulls of d+1 affinely independent points.',20:'The last sentence specifies that43 bounds bracketing entropy in Lp on the simplex union.',21:'The bound is for the local class B_p^Gamma(tilde f,t,Omega) defined in42.'},
'4.11':{2:'The covering class in52 consists of f inC(Omega) subject to a discrete norm bound.',7:'The first sentence explicitly requires condition3.',14:'It explicitly requiresOmega to have the slab form14, which supplies the exponent F.',15:'The resolution delta is that of the regular grid15, with the small-delta convention16 stated in preceding context.',19:'The expression logN in52 is the covering entropy, using the original closed-ball convention.',22:'Both the norm constraint and covering metric are the discrete Lp metric ell_S defined immediately before the theorem in51.'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Preserve all eight original main-text Theorems and original convex regression classes, design conditions, losses and entropy conventions.',build_order_policy='Derive same-paper paths from the original statement definitions. Separate fixed and random design, empirical and population losses, deterministic entropy and stochastic risk. Proof-only Gaussian supremum and entropy bounds do not become rate-theorem hypotheses.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGE_TEXT.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=DIRECT[n];assert set(REASONS[n])==set(DIRECT_NUMS[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=direct_reason(n,lid),evidence=copy.deepcopy(c['evidence'])+copy.deepcopy(members[lid]['evidence'])))
    edges=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=edges[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for rel in x['related_theorems']:
            cid=rel['claim_id'];n=cid.split('/T')[-1];path=rel['via_local_ids']
            reason=' '.join([direct_reason(n,path[0])]+[EDGE_TEXT[a][b] for a,b in zip(path,path[1:])]);ev=copy.deepcopy(claims[cid]['evidence'])
            for lid in path:ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=reason,evidence=ev)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems']);selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors) and all(s in linked for s in selectors),(m['local_id'],[s for s in selectors if s not in linked])
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Census structurally validated; independent source review remains pending.')
if __name__=='__main__':main()
