"""Derive source-specific tensor-estimation and lower-bound theorem dependencies."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'3.1':[5,8,14,17,18,19,20,21,23,24,25,26],'3.2':[5,8,15,17,18,20,22,27,28,29],'3.3':[5,8,16,18,23,25,26,27],'3.4':[5,31,32],'3.5':[5,32]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D1':{'D2':'Model(1.2) forms the signal by successive mode products with the loading matrices A_k.'},
'D7':{'D6':'The order-four operator norm maximizes over two matrices normalized by the source Hilbert Schmidt norm.'},
'D8':{'D1':'Projection(2.2) uses the full-column-rank loading A_k and its left singular matrix U_k from the general factor model.'},
'D9':{'D4':'Sample lag tensor(2.3) averages the full tensor outer products of X_(t-h) and X_t.'},
'D10':{'D3':'TOPUP unfolds each lagged order-2K tensor along mode k.','D9':'TOPUP concatenates the sample lag tensors Sigma-hat_h defined in(2.3).'},
'D12':{'D3':'TIPUP forms matrix products from the mode-k unfoldings of two time-lagged observations.'},
'D13':{'D2':'Algorithm1 forms each projected data tensor Z by sequential mode products with the transposed other-mode estimates.','D5':'The stopping rule bounds the maximum spectral norm of differences between consecutive estimated projections.'},
'D14':{'D13':'iTOPUP is the explicitly named specialization of the generic sequential Algorithm1.','D35':'Both its INIT and ITER operators are the TOPUP truncated-SVD estimator(2.5).'},
'D15':{'D13':'iTIPUP specializes the same generic sequential Algorithm1.','D36':'Both its INIT and ITER operators are the TIPUP estimator(2.8).'},
'D16':{'D13':'TIPUP-iTOPUP uses the original sequential Algorithm1 with two different supplied operators.','D35':'Its ITER step is the TOPUP truncated-SVD operator.','D36':'Its INIT step is the TIPUP truncated-SVD operator.'},
'D17':{'D1':'Bar-E conditions on the latent factor block F1,...,FT from the general model.'},
'D18':{'D1':'Assumption1 constrains the model noise E_t conditionally on its factor process.','D17':'The displayed noise second-moment bound uses the source conditional expectation bar-E.'},
'D19':{'D1':'Theta_(k,h) uses the noiseless signal M_t from X_t=M_t+E_t and the factor representation.','D3':'Each lagged signal is unfolded along mode k before multiplication.','D4':'The unfolded signal matrices are combined by the full tensor outer product.'},
'D20':{'D1':'Theta-star_(k,h) averages lagged products of the model signal M_t.','D3':'Its definition contracts the mode-k signal unfoldings by ordinary matrix multiplication.'},
'D21':{'D3':'The unstarred signal strength uses singular values of mode-one unfolded lag tensors.','D10':'The first displayed expression for tau_(k,m) uses the TOPUP matrix.','D17':'That TOPUP expression is averaged with bar-E conditional on the factor block.','D19':'The second expression uses the lag collection Theta_(k,1:h0).','D33':'The third expression uses the canonical outer-product tensor Phi^(cano)_(k,1:h0).'},
'D22':{'D12':'The first definition of tau-star_(k,m) takes a singular value of the TIPUP matrix mean.','D17':'Its matrix mean is taken under the source bar-E.','D20':'The second equal representation uses the lag collection of Theta-star matrices.','D34':'The third equal representation uses the canonical inner-product matrix collection Phi-star-cano.'},
'D23':{'D5':'The initial TOPUP rate contains the spectral norm of Theta-star_(k,0).','D7':'It also contains the source order-four operator norm of Theta_(k,0).','D19':'Theta_(k,0) supplies the unstarred signal tensor in that rate.','D20':'Theta-star_(k,0) supplies the inner-product signal matrix in that rate.','D21':'The rate is scaled by the inverse square of the unstarred signal strength lambda_k.'},
'D24':{'D23':'Definition(3.9) contains the square of the initial TOPUP rate R_k^(0).','D37':'Its other summand is the separately defined auxiliary term Rcal_k2 from(3.8).'},
'D25':{'D5':'The Rcal_k1 summand uses the spectral norm of Theta-star_(k,0).','D7':'It also uses the order-four operator norm of Theta_(k,0).','D19':'The ideal rate contains the signal outer-product tensor at lag zero.','D20':'It contains the corresponding signal inner-product matrix at lag zero.','D21':'Rcal_k1 has inverse-square unstarred strength lambda_k.','D23':'The source explicitly describes constructing the ideal rate by replacing other-mode dimensions in R_k^(0) with their ranks.','D37':'R_k^(ideal) is the sum of Rcal_k2 and the square of Rcal_k1; it does not use the separate R_TOPUP formula.'},
'D26':{'D21':'Additional TOPUP error(3.11) is scaled by lambda_k^(-2); its dimension sum is independently defined in the same passage.'},
'D27':{'D5':'The initial TIPUP rate takes the spectral norm of Theta-star_(k,0).','D20':'Its signal contribution is the square root of that lag-zero matrix norm.','D22':'The initial TIPUP rate uses inverse-square starred strength lambda-star_k.'},
'D28':{'D5':'The ideal TIPUP expression contains the spectral norm of Theta-star_(k,0).','D20':'Its signal component is the lag-zero inner-product matrix Theta-star_(k,0).','D22':'The rate uses inverse-square starred signal strength, independently of unstarred lambda_k.'},
'D29':{'D28':'Additional TIPUP error(3.18) multiplies R_k-star-ideal by sqrt(dstar_-k/dk).'},
'D31':{'D30':'HypothesisI explicitly refers to HPC detection problem(3.32), whose null and planted hypergraph laws define its two error probabilities.'},
'D32':{'D2':'The separate lower-bound model(3.34) applies mode products with its orthonormal matrices U_k to lambda times the factor tensor.'},
'D33':{'D1':'Canonical Phi uses the original noiseless signal M_t.','D2':'It projects M_t by mode products with every U_k transpose.','D3':'The projected lagged signals are unfolded along mode k.','D4':'Their unfoldings are combined by the tensor outer product.','D8':'The coordinates use the loading-space matrices U_k from the source SVD of A_k.'},
'D34':{'D1':'The second canonical inner-product representation uses signal M_t from the factor model.','D2':'It projects the signal by all loading-coordinate mode products.','D3':'The projected signals are unfolded along mode k.','D8':'The canonical coordinates are defined using loading-space matrices U_k.','D20':'The first representation is U_k transpose times Theta-star_(k,h) times U_k.'},
'D35':{'D3':'The TOPUP estimator unfolds each sample lag tensor along mode k.','D9':'Its input matrices use the explicitly defined Sigma-hat_h sample lag products.','D10':'The text specifies SVD of the TOPUP lag-matrix construction(2.4).','D11':'The estimator applies LSVD_m to select the first m left singular vectors.'},
'D36':{'D3':'The TIPUP estimator builds its lagged matrices from mode-k unfoldings.','D11':'It applies the source LSVD_m operator to the concatenated lag matrices.'},
'D37':{'D5':'Rcal_k2 contains the spectral norm of Theta-star_(k,0).','D7':'It contains the order-four operator norm of Theta_(k,0).','D19':'The lag-zero outer-product tensor is the unstarred signal input.','D20':'The lag-zero inner-product matrix is the starred signal input.','D21':'The entire auxiliary expression is scaled by inverse-square lambda_k.'}}
REASONS={
'3.1':{5:'Theorem3.1 bounds the spectral norm of P-hat_k^(m)-P_k, including a maximum in its conditional-risk conclusion.',8:'Theorem3.1 explicitly identifies P_k by projection formula(2.2).',14:'Its m-step estimator is explicitly the iTOPUP algorithm, using TOPUP for both initialization and iteration.',17:'The terminal risk in(3.14) is written with the conditional expectation bar-E from Section3.1.',18:'Its first sentence explicitly assumes Assumption1 on the noise process.',19:'It explicitly imports Theta_(k,0) from(3.1).',20:'It explicitly imports Theta-star_(k,0) from(3.3).',21:'It explicitly imports the unstarred signal strength lambda_k from(3.5).',23:'Its R^(0) is the maximum of the initial rates R_k^(0) in(3.7).',24:'Its R^(TOPUP) is the maximum of the sharper TOPUP rates in(3.9).',25:'Its R^(ideal) is the maximum of the ideal rates in(3.10).',26:'Its R^(add) is the maximum of the additional TOPUP errors in(3.11).'},
'3.2':{5:'Theorem3.2 bounds the spectral projection error and uses a spectral Theta-star norm in its initial condition.',8:'Theorem3.2 explicitly takes P_k from projection formula(2.2).',15:'Its m-step estimator is explicitly iTIPUP, which uses TIPUP for both steps.',17:'The terminal risk in(3.21) is a bar-E conditional expectation.',18:'Theorem3.2 explicitly assumes Assumption1.',20:'It explicitly takes Theta-star_(k,0) from(3.3), including its norm in the initial condition.',22:'It explicitly takes lambda-star_k from(3.6), with its square in the initial-condition ratio.',27:'Its R-star-(0) is the maximum of initial TIPUP rates(3.16).',28:'Its R-star-(ideal) is the maximum of the ideal TIPUP rates(3.17).',29:'Its R-star-(add) is the maximum of additional TIPUP errors(3.18).'},
'3.3':{5:'Theorem3.3 bounds the spectral projection error simultaneously over all modes and iterations.',8:'Its P_k is the common loading-space projection defined by(2.2); only P-hat is newly bound in its opening sentence.',16:'Its estimator is explicitly the TIPUP-iTOPUP mixed algorithm, with TIPUP initialization and TOPUP iterations.',18:'Its opening sentence explicitly states Assumption1 holds.',23:'It explicitly names R^(0) as in Theorem3.1, although that unstarred rate is not used in its displayed inequalities.',25:'It imports the unstarred ideal rate from Theorem3.1 for both contraction control and its error bound.',26:'It imports the unstarred additional error from Theorem3.1 for contraction control.',27:'It imports starred R^(0) from Theorem3.2 for initialization and its contracted initial-error term.'},
'3.4':{5:'Theorem3.4 uses the squared spectral norm of projection error in a minimum over all modes.',31:'Theorem3.4 explicitly assumes HypothesisI for some delta in(0,1/2).',32:'Its worst-case probability is taken over the source class P(T,d1,...,dK,lambda) from(3.35), with model(3.34).'},
'3.5':{5:'Theorem3.5 lower-bounds the expected unsquared spectral norm of projection error.',32:'Its minimax supremum uses the same lower-bound class P(T,d1,...,dK,lambda) in(3.35); it does not assume computational hardness.'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Retain all five original main-text Theorems. Preserve distinct iterative algorithms, starred/unstarred rates, and the separate lower-bound probability class.',build_order_policy='Derive same-paper paths from original definitions and explicit references. Separate rate definitions from surrounding guarantees, preserve computational versus statistical hypotheses, and exclude proof-only or implication-only imports.')
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
