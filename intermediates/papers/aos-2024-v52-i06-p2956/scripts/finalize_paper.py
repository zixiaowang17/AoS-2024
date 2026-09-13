"""Derive source-backed statement relationships for both crossed-model Theorems."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'1':[3,5,8,11,12,13,14,15,16,17],'3':[3,5,8,11,12,13,14,15,16,17,18,19]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'The covariate means use the balanced g by h by m observation indices and n=ghm.'},
'D3':{'D1':'Model (4) retains the original four crossed random-effect families.','D2':'Its separate slope vectors correspond to the four original covariate levels.'},
'D4':{'D2':'The fixed-effect design repeats the four original covariate blocks at their specified levels.','D3':'The matrix equation represents model (4) and its fixed-effect parameter grouping.','D20':'Its random-effect terms use the original incidence matrices Z0 through Z3.'},
'D5':{'D1':'Eta uses the original row and column counts.','D3':'Tau uses the row and column variance components in the original parameter vector.'},
'D6':{'D2':'Centered quantities use the original marginal means and covariate hierarchy.'},
'D7':{'D6':'The enlarged Gram matrices stack the original centered covariate quantities.'},
'D8':{'D1':'The four normalizations use the original g, h, gh and n sample sizes.','D7':'D1-D4 are limits of the indicated diagonal blocks of the original sums of squares.'},
'D9':{'D3':'The working likelihood is parameterized by the original interleaved parameter vector.','D4':'Its residual is the original stacked observation vector minus the fixed-effect design times its coefficients.','D10':'The objective uses the original balanced dispersion inverse and determinant.'},
'D10':{'D1':'The covariance eigenvalues depend on balanced counts and the original four variance components.','D20':'The inverse is that of the original variance-component dispersion matrix V.'},
'D11':{'D3':'The score differentiates in the original order of regression and variance parameters.','D9':'The original definition explicitly differentiates likelihood (6) to form psi.'},
'D13':{'D1':'Condition A3 applies moment and independence requirements to the four original random-effect families.','D2':'Condition A4 uses the original row and column covariate means.','D3':'Condition A1 explicitly assumes model (4) and its true parameter.','D6':'The empirical covariate moments use the original centered quantities.','D7':'Condition A4 requires positive definite limits of the enlarged capital-X Gram matrices.','D12':'Its moment inequalities use the source Euclidean norm.'},
'D14':{'D1':'The rate matrix uses the four sample sizes g, h, gh and n.','D2':'Its block dimensions are determined by the four covariate levels.'},
'D15':{'D1':'The influence components use the original row, column, interaction and error variables.','D2':'The regression components use their own original level-specific covariates.','D3':'Variance centering and denominators use true parameter components.','D5':'The first, row and column components use eta and the combined true variance dot-tau.','D6':'Interaction and within components use the original c-subscripted covariates.'},
'D16':{'D1':'The asymptotic covariance uses third and fourth moments of the original random effects.','D2':'The row-column covariance uses the original covariate means.','D3':'The scale factors are the original true variance components.','D5':'The row-column cross block depends on eta and the combined variance.','D8':'All regression covariance blocks use the original limiting D1-D4 matrices.'},
'D17':{'D3':'The expected score derivative is evaluated at the true model parameter.','D5':'Its explicit row-column blocks use eta and dot-tau.','D8':'Its slope blocks contain the original limiting D matrices.','D11':'B is the limit of the normalized expected derivative of the original likelihood score.','D14':'Its normalization uses the same four-rate K matrix.'},
'D18':{'D3':'The profile criterion regroups the original regression and variance parameters and restores their original order in omega-hat-R.','D4':'The profiled GLS expression uses the original fixed design X.','D9':'The profile and adjustment start from the original working likelihood.','D11':'The profiled regression solution is identified by the original score equations (8).','D20':'The criterion uses the variance-component dispersion V.'},
'D19':{'D3':'The adjusted objective uses the original full parameter vector.','D4':'The log-determinant correction uses the original fixed design X.','D9':'The adjusted objective subtracts its determinant correction from the original working likelihood.','D11':'Its regression scores equal the original scores and its variance scores adjust those original components.','D18':'The source presents this adjusted objective as an alternative route to the original REML estimator.','D20':'All four printed variance corrections use the original incidence matrices and dispersion V.'},
'D20':{'D1':'The incidence and dispersion matrices encode the four independent crossed effects and balanced observation indices.'}}
REASONS={'1':{
3:'Theorem 1 centers the estimator at dot-omega and specifies the full regression/variance parameter ordering.',
5:'The theorem distinguishes finite eta and the eta=infinity reordering; its influence and covariance formulas explicitly use dot-tau.',
8:'The full covariance formula contains D1 inverse through D4 inverse, whose definitions are the normalized Gram-block limits on page 4.',
11:'The first sentence explicitly identifies omega-hat as a solution of the original estimating equations psi(omega)=0.',
12:'The local stochastic bound is expressed using the original Euclidean norm.',
13:'The theorem begins by requiring the complete original Condition A.',
14:'The theorem defines and uses K with all four rates and their original block dimensions.',
15:'The asymptotic representation explicitly uses the nine-component vector phi defined in equation (10).',
16:'The limiting Gaussian law explicitly uses the full matrix F defined in the theorem continuation.',
17:'The representation explicitly binds B by reference to equation (13) in main-text Lemma 4.'},
'3':{
3:'Theorem 3 centers the REML root at the same true parameter dot-omega and compares it with the ML root.',
5:'The final sentence applies Theorem 1 to REML, including its finite/infinite eta regimes and dot-tau-dependent formulas.',
8:'The final sentence applies Theorem 1 and therefore its covariance with the original D1-D4 limits.',
11:'The displayed difference uses omega-hat, the original ML score root from Theorem 1.',
12:'The local REML rate is expressed using the original Euclidean norm.',
13:'The theorem explicitly requires the complete original Condition A.',
14:'Both displayed normalized errors use the original four-rate K matrix.',
15:'The statement explicitly says Theorem 1 applies, including its asymptotic representation using phi in (10).',
16:'The statement explicitly says Theorem 1 applies, including its limiting Gaussian covariance F.',
17:'Applying Theorem 1 includes its representation with B from main-text equation (13).',
18:'The theorem identifies omega-hat-R as the REML estimator using the original criterion and parameter reassembly.',
19:'The root in the first sentence solves the REML estimating equations, whose adjusted objective and derivative components are printed immediately before the theorem.'}}
def direct_reason(n,lid):return REASONS[n][int(lid[1:])]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv);data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Preserve both original main-text Theorems numbered 1 and 3 and the crossed-model source definitions.',build_order_policy='Resolve model, Condition A, score, asymptotic matrix and REML dependencies from main text. Theorem 3 explicitly applies Theorem 1; keep source inconsistencies and appendix-only meanings unresolved.')
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
