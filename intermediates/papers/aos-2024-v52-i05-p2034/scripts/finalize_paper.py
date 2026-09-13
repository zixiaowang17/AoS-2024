"""Build the census while preserving score versions and theorem subpart scopes."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'1':[1,2,3,8,9,10,11],'2':[1,9,10,12,13,14]}
DIRECT={n:['D'+str(i) for i in ids] for n,ids in DIRECT_NUMS.items()}
EDGE_TEXT={
 'D2':{'D1':'The iid observations and tested coefficient vector belong to the linear regression model (1).'},
 'D3':{'D1':'The population score uses the model covariate/response and their population means.','D2':'Its residual uses the known null coefficient beta_0 from (2).'},
 'D4':{'D1':'The practical score is formed from the linear-model observations.','D2':'The shared sample means use the iid sample and the score residual uses known beta_0.'},
 'D5':{'D4':'The statistic (4) uses the sample-centered scores introduced immediately before it; the population-centered comparison is separate.'},
 'D6':{'D4':'Sigma-hat_Z is the sample covariance of those score vectors.'},
 'D7':{'D4':'Equation (6) forms ordered off-diagonal outer products of the same score vectors.'},
 'D8':{'D5':'The numerator of T_n is n times W_n.','D6':'The estimated trace includes the squared quadratic form in the sample covariance Sigma-hat_Z.','D7':'Its first two terms use the separate estimator of Sigma_Z squared from (6).'},
 'D9':{'D1':'Assumption A1 represents the model covariates using their mean and covariance square root.'},
 'D10':{'D1':'Assumption A2 concerns the error epsilon_i and variance sigma squared from model (1).'},
 'D11':{'D1':'The local alternative specifies a displacement of the regression coefficient.','D2':'Its center is the known null vector beta_0.'},
 'D12':{'D1':'The random-effects prior is placed on the linear-model coefficient vector beta.'},
 'D13':{'D8':'The rejection rule compares the proposed statistic T_n with a right-tail normal critical value.'},
 'D14':{'D2':'Its first term is the rejection probability under the coefficient null.','D12':'Its second term averages nonrejection under the REM prior pi.'}}
def direct_reason(n,lid):
    if lid=='D1':return 'The spectral condition uses Sigma_X, the covariance matrix in model (1); the regression coefficient and error variance retain that model setting.'
    if lid=='D2':return 'Theorem 1(i) refers to H_0 in (2), and part (ii) defines delta_z using the known null coefficient beta_0.'
    if lid=='D3':return 'Theorem 1(ii) centers T_n using tr(Omega^2). The original Omega formula is retained in A1, and its Sigma_Z is the population-score covariance identified by the adjacent variance formula A2 and pages 8-10.'
    if lid=='D8':return 'Both parts of Theorem 1 concern T_n, the studentized statistic (5), whose estimated denominator is distinct from the population trace in the local-alternative shift.'
    if lid=='D9':return 'The preamble explicitly assumes A1: the covariance-square-root representation and coordinate moment factorization only through total degree four.'
    if lid=='D10':return ('The preamble assumes A2; Gaussian errors are added only in Theorem 2(i), while part (ii) retains the original fourth-moment error condition.' if n=='2' else 'The preamble explicitly assumes A2, the iid mean-zero errors with variance sigma squared and bounded fourth moments.')
    if lid=='D11':return 'Theorem 1(ii) explicitly refers to H_a in (7), with the n^{-1/2} coefficient displacement, bounded scalar delta and unit direction; part (i) is instead under H_0.'
    if lid=='D12':return 'Theorem 2 explicitly invokes the REM, using S and gamma squared from the uniform-support sub-Gaussian coefficient prior and restricting s to [0,1/2].'
    if lid=='D13':return 'The proposed test in Theorem 2(ii) is the rule T_n>z_a defined on page 6. The power discussion on page 17 identifies divergence of T_n under the alternative; this does not import every Theorem 1 assumption.'
    if lid=='D14':return 'The all-tests powerless assertion in Theorem 2(i) is interpreted using the average-risk definition supplied in its main-text explanation on page 13: null rejection plus prior-averaged nonrejection. The likelihood-ratio proof object is not required to define that risk.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Both complete main-text Theorems; keep original score versions, estimator definitions and alternative hypotheses separate.',build_order_policy='Same-paper source dependencies with explicit expansion of the unnamed population normalization; proof-only citations do not supply statement edges.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGE_TEXT.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=DIRECT[n]
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                ev=copy.deepcopy(c['evidence'])+copy.deepcopy(members[lid]['evidence'])
                if lid=='D3':ev.extend([dict(page=4,location='Population variance in A2'),dict(page=5,location='Original Omega formula A1')])
                if lid=='D13':ev.append(dict(page=17,location='Meaning of powerfulness for the proposed rule'))
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
            if 'D3' in path:ev.extend([dict(page=4,location='Population variance formula'),dict(page=5,location='Original Omega formula A1')])
            if 'D13' in path:ev.append(dict(page=17,location='Proposed-test powerfulness criterion'))
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
