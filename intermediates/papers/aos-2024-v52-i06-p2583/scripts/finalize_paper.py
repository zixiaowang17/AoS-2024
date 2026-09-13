"""Build source-specific theorem relationships without mixing algorithm branches."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'1':[1,2,5,8,10,11,12,13,24],'2':[1,2,5,8,10,12,13,25,31],'3':[1,2,5,6,8,12],'4':[1,2,5,8,14,30],'5':[10,11,13,14,15,16,24,25,31],'6':[10,11,13,14,17,18,24,25,31],'7':[3,8,11,14,19,20,27,28,31],'8':[10,11,13,14,21,22,24,25,31],'9':[23],'10':[2,4,5,29]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D4':{'D2':'The Tucker decomposition uses the mode unfolding M_k and its rank tuple.','D3':'Its factor U_k is explicitly the leading-left-singular-vector matrix SVD_{r_k}(M_k(A)).'},
'D5':{'D2':'The best approximation is constrained by Tucker rank r and measured in the Frobenius norm defined in Section1.5.','D4':'Its formula projects the tensor by mode products along every mode.'},
'D6':{'D1':'The loss f(X) is half the squared residual norm for Y=A(X*)+E.','D2':'The feasible set in(3) is the componentwise Tucker-rank inequality Tucrank(X)≤r.'},
'D7':{'D2':'The manifold is the exact-Tucker-rank set, and its projector uses mode matricization and reverse tensorization.','D3':'The row factor V_k is the Q part of QR(M_k(S)^top), with singular subspaces defined in Section1.5.','D4':'The tangent projector is expressed in terms of the Tucker core and mode factors, with tensor-matrix products.'},
'D8':{'D1':'The adjoint is defined against the regression contraction operator A and has the explicit sample-sum formula in Section7.'},
'D9':{'D1':'The line search uses the regression residual A(X^t)-Y and the sampling operator A.','D7':'Both numerator and denominator contain the tangent projector P_{T_X}.','D8':'The projected gradient in the line-search ratio applies the Euclidean adjoint A* to the residual.'},
'D10':{'D7':'The named retractions return an update to the fixed-rank manifold M_r; the distinction from bounded-rank geometry is preserved.'},
'D11':{'D1':'The RGD branch consumes the observed tensor responses and covariates and their contraction residual.','D2':'Algorithm1’s input rank and initialization use the paper’s Tucker-rank convention.','D7':'The RGD update projects its gradient onto T_X M_r and uses a retraction onto the same manifold.','D8':'The RGD update forms A*(A(X^t)-Y).','D9':'The RGD branch explicitly references the stepsize alpha_t in equation6.'},
'D12':{'D2':'Definition1 quantifies all tensors with Tucker rank at most the specified tuple.'},
'D13':{'D2':'Lambda is minimized over all mode matricizations M_k(X*) at the true Tucker ranks r_k*.','D3':'Each term is the r_k*th ordered singular value, not a singular value at the over-specified input rank.'},
'D14':{'D1':'Definition2 imposes independent Gaussian design and noise on the tensor regression model(1).'},
'D15':{'D1':'Equation10 is the scalar-response specialization m=0 of model1.','D2':'The coefficient has the stated order-d Tucker rank r*.'},
'D16':{'D3':'Algorithm2 uses leading left singular-vector matrices SVD_{r_k} both before and after its one update.','D4':'Its update and reconstruction multiply the tensor by mode-factor matrices and their transposes.','D8':'The tensor to initialize from is the regression adjoint A*(y).','D15':'The inputs are the scalar responses and order-d covariates of model10.'},
'D17':{'D1':'Equation11 is model1 with vector covariates, so d=1.','D2':'The coefficient tensor has the stated Tucker rank r*.','D4':'The model expresses the observation by a mode1 tensor-matrix product.'},
'D18':{'D3':'Algorithm3 uses the QR factors of A and leading singular subspaces of the whitened tensor.','D4':'Whitening, HOOI updates, reconstruction and the inverse-R transformation all use mode products.','D17':'Algorithm3 consumes the stacked vector-covariate matrix and tensor responses defined in model11.'},
'D19':{'D1':'Matrix trace regression is the m=0,d=2 contraction model, with matrix coefficient and scalar observations.'},
'D20':{'D3':'The best-rank matrix reconstruction retains the first r singular vectors and singular values of its matrix argument.'},
'D21':{'D1':'Equation13 rewrites model1 with an outer-product rank-one coefficient and splits its stacked responses into two halves.'},
'D22':{'D3':'Algorithm4 initializes and updates every mode factor using SVD_1.','D4':'The final HOOI update and reconstructed tensor use mode products with the estimated vectors.','D8':'The final update and reconstruction use A*(Y) from all observations.','D21':'Its Y^1, two sample halves, response modes and rank-one factors are those defined immediately before13.'},
'D24':{'D12':'The RGD closeness threshold uses the restricted isometry constants R_{2r} and R_{2r+r*}.','D13':'The threshold is scaled by the source-defined signal strength lambda.'},
'D25':{'D12':'The RGN closeness threshold uses 1-R_{2r} and 1+R_{2r+r*}-R_{2r}.','D13':'The RGN initialization threshold is scaled by the same true-rank signal strength lambda.'},
'D27':{'D3':'Corollary1’s matrix RGD threshold is scaled by sigma_{r*}(X*).','D12':'The scalar matrix-rank restricted-isometry constants appear in the sharper RGD threshold.'},
'D28':{'D3':'Corollary1’s matrix RGN threshold is scaled by sigma_{r*}(X*).','D12':'The matrix RGN threshold contains R_{2r} and R_{2r+r*}, with the printed factor8.'},
'D29':{'D2':'OHOOI takes an input Tucker rank tuple and unfolds each mode of the tensor.','D3':'Its update returns SVD_{r_k}, the matrix of leading left singular vectors.','D4':'OHOOI uses mode products in the update and projection reconstruction.'},
'D30':{'D1':'Theorem3’s referenced estimator qualification concerns residuals in the original regression model.','D2':'The estimator is constrained to Tucker rank at most r.','D12':'The original qualification explicitly starts with the2rTRIP hypothesis; this belongs to T4’s referenced upper-estimator clause.','D6':'The qualification compares the loss at the estimator to the loss at the true coefficient, using the loss in(3).'},
'D31':{'D1':'The RGN branch solves a least-squares problem using the observed regression responses and sampling operator.','D2':'Its input and initialization use the Tucker rank r.','D7':'The minimization is over the tangent space T_X M_r and applies its projector; a retraction returns the update to M_r.'}}
REASONS={
'1':{1:'Theorem1 concerns the coefficient X*, operator A and error E of model1/2; Gaussian sampling is not assumed.',2:'Theorem1 states the true Tucker rank r* and input rank r≥r*.',5:'Theorem1 explicitly recalls the best Tucker2r approximation of A*(E) in its noise term.',8:'Theorem1’s noise term applies the regression adjoint A* to E.',10:'Theorem1 selects the tensor RGD setting of Algorithm1 with the tensor retractions described in Section2.2.',11:'Theorem1 is the convergence statement for Algorithm1’s RGD branch and its iterates X^t.',12:'Theorem1 assumes2rTRIP and states explicit conditions involving R_{2r} and R_{2r+r*}.',13:'Theorem1 defines lambda from the least nonzero singular values of all true coefficient matricizations.',24:'Theorem1 assumes the exact RGD initialization-distance inequality retained in D24.'},
'2':{1:'Theorem2 uses the regression model’s X*, A and E without a Gaussian hypothesis.',2:'Theorem2 states true Tucker rank r* and input rank r≥r*.',5:'Theorem2’s noise floor uses the best Tucker2r approximation of A*(E).',8:'Theorem2’s error bound contains the adjoint noise A*(E).',10:'Theorem2 uses the tensor retraction choices of Section2.2 for the RGN iterates.',12:'Theorem2 explicitly assumes2rTRIP and uses its constants in the initialization and error bounds.',13:'Theorem2’s lambda is the signal-strength object defined in Theorem1; no additional RGD condition is imported.',25:'Theorem2 assumes the RGN initialization inequality retained in D25, with the factor4(d+m)(sqrt(d+m)+1).',31:'Theorem2 selects Algorithm1’s RGN branch. It does not use the RGD stepsize.'},
'3':{1:'Theorem3 compares regression residuals at Xhat and X* and bounds their coefficient error.',2:'Theorem3 requires Tucrank(Xhat)≤r under the standing true-rank feasibility convention.',5:'Theorem3’s error bound contains the best Tucker2r approximation of A*(E).',6:'Theorem3 explicitly compares residual-loss values, using the least-squares loss(3).',8:'Theorem3’s bound uses the adjoint noise tensor A*(E).',12:'Theorem3 explicitly assumes2rTRIP and cites Definition1.'},
'4':{1:'Theorem4 explicitly considers tensor-on-tensor regression problem(1).',2:'Theorem4 defines its parameter space by Tucrank(X)≤r and binds the dimension formula df.',5:'Theorem4’s first upper bound controls the best Tucker2r approximation of A*(E).',8:'Theorem4’s Gaussian noise bound contains the regression adjoint A*(E).',14:'Theorem4 explicitly imposes Gaussian ensemble design and cites Definition2.',30:'Only Theorem4’s upper estimator clause refers to Xhat in Theorem3, whose rank/loss/TRIP qualification is retained in D30; the minimax lower branch remains unrestricted over estimators.'},
'5':{10:'Theorem5 runs the tensor RGD/RGN procedures using Section2.2’s tensor retraction choices.',11:'Theorem5’s second conclusion gives an iteration threshold and error bound for RGD.',13:'Theorem5’s sample-size and iteration bounds use lambda from the true-rank singular-value definition.',14:'Theorem5 explicitly assumes Gaussian ensemble design with Definition2’s scaling.',15:'Theorem5 explicitly concerns over-parameterized scalar-on-tensor regression, model10.',16:'Theorem5’s first conclusion refers to X0 returned by Algorithm2, and its second starts both methods there.',24:'Theorem5 guarantees the Theorem1 initialization property for the output X0; this is a conclusion, not an assumed good starting point.',25:'Theorem5 also guarantees the Theorem2 initialization property for X0.',31:'Theorem5 separately gives the RGN double-logarithmic iteration threshold and final error.'},
'6':{10:'Theorem6 uses the tensor RGD/RGN retraction choices in Section2.2.',11:'Theorem6’s output conclusion includes RGD with its logarithmic iteration threshold.',13:'Theorem6’s sample-size and iteration bounds use the source-defined lambda.',14:'Theorem6 explicitly assumes Gaussian ensemble design.',17:'Theorem6 concerns the over-parameterized tensor-on-vector model11 with d=1.',18:'Theorem6 explicitly takes X0 from Algorithm3, the QR-whitened initialization.',24:'Theorem6 guarantees the Theorem1 initialization-distance property for Algorithm3’s output.',25:'Theorem6 guarantees the separate Theorem2 initialization-distance property for the same output.',31:'Theorem6’s output conclusion separately includes RGN and its double-logarithmic iteration threshold.'},
'7':{3:'Theorem7’s sample condition and iteration counts explicitly use the true-rank singular value sigma_{r*}(X*).',8:'Theorem7 defines its initializer using the adjoint A*(y).',11:'Theorem7 runs RGD with the matrix retraction P_r, and states its logarithmic iteration threshold.',14:'Theorem7 explicitly assumes Gaussian ensemble design, specialized to matrix covariates and scalar errors.',19:'Theorem7 explicitly concerns over-parameterized matrix trace regression, model12.',20:'Theorem7 sets X0=P_r(A*(y)); Section4.3 also specifies P_r as the matrix retraction for RGD/RGN.',27:'Theorem7 guarantees the RGD initialization-distance condition in Corollary1 for its output X0.',28:'Theorem7 also guarantees Corollary1’s distinct RGN initialization-distance condition.',31:'Theorem7 runs the RGN branch with matrix P_r and states the double-logarithmic iteration threshold.'},
'8':{10:'Theorem8 uses the tensor RGD/RGN procedures with the Section2.2 retraction choices.',11:'Theorem8’s second conclusion covers RGD and its iteration threshold.',13:'Theorem8 uses lambda as signal strength, with the rank-one amplitude convention of13; the missing explicit factor normalization is recorded.',14:'Theorem8 explicitly assumes Gaussian ensemble design.',21:'Theorem8 explicitly references the rank-one model(13), whose context fixes rank-one input and an even sample split.',22:'Theorem8 explicitly takes X0 from Algorithm4 and starts both refinement methods there.',24:'Theorem8 guarantees Theorem1’s initialization-distance condition for the output of Algorithm4.',25:'Theorem8 guarantees the separate Theorem2 initialization-distance condition for the same output.',31:'Theorem8’s second conclusion separately covers RGN with its double-logarithmic iteration threshold.'},
'9':{23:'Theorem9 explicitly references hypothesis test14. Its normalized polynomial supremum compares expectation under that planted H1 with centering and variance under that H0; it does not use Definition2’s1/n-scaled design.'},
'10':{2:'Theorem10 states the true Tucker rank r*, input rank r≥r* and their tensor dimensions.',4:'Theorem10 explicitly writes T as a Tucker core times orthonormal mode factors.',5:'Theorem10’s deterministic error bound contains Z_max(r), the best rank-r Tucker approximation of the perturbation.',29:'Theorem10 explicitly specifies OHOOI and calls its estimator the output of Algorithm5.'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Retain all ten original main-text Theorems. Preserve tensor/matrix model specializations, distinct algorithm branches, output initialization guarantees and deterministic/testing scope.',build_order_policy='Derive same-paper dependencies from actual source formulas and statement references. Exclude proof-only theorem references and supplement bodies. RGD/RGN have separate branch entries; matrix retractions do not inherit tensor-only choices.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGE_TEXT.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=DIRECT[n]
        assert set(REASONS[n])==set(DIRECT_NUMS[n])
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
