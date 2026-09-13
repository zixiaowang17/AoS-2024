"""Finalize the six-Theorem census without altering inventoried statements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
'1.9':{'D5':'The moment and weak-convergence conclusions concern the empirical spectral measure mu_N from (5).','D11':'The general comparison and Case 1 use free additive convolution of the indicated Bernoulli measures.','D12':'The general comparison measure uses the finite-N mu_t from Section 1.2; Case 1 separately binds its limiting Bernoulli laws.','D13':'The hypothesis explicitly references Assumption 1.6, including all-order uniform entry moments.','D14':'The hypothesis explicitly references Assumption 1.7 for dimensional ratios and their limits.','D19':'Case 2 explicitly defines mu_mp,hat-y in (16), with the printed density retained.'},
'1.11':{'D4':'The statistic is evaluated at the matrix H defined by the sum of projections in (4).','D8':'The conclusion uses Tr f(H), the linear spectral statistic from Definition 1.4.','D9':'The opening sentence identifies m_boxplus as the Stieltjes transform used throughout the mean and variance.','D10':'The mean and variance contain omega_t and its derivatives, the subordination functions of Proposition 1.5.','D11':'The opening sentence recalls the free convolution mu_boxplus that centers the statistic.','D12':'The recalled mu_boxplus is the convolution of the finite-N Bernoulli projection laws mu_t.','D13':'The statement assumes Assumption 1.6.','D14':'The statement assumes Assumption 1.7 and selects contour regimes using the limiting ratio hat-y.','D16':'The analytic-function hypothesis and both mean/variance integrals use the contours gamma_1^0,gamma_2^0 or their general-regime replacements.'},
'1.17':{'D4':'The statistic is evaluated at the projection-sum matrix H from (4).','D8':'Tr f(H) is the linear spectral statistic of Definition 1.4.','D9':'The opening sentence defines m_y as the Stieltjes transform of the finite-y Marchenko-Pastur measure.','D13':'The statement explicitly retains Assumption 1.6.','D14':'Assumption 1.7 is explicit; the additional pmax threshold is bound directly in this theorem.','D16':'Its analyticity hypothesis and mean/variance integrals use the two specified contour regimes.','D19':'The center uses mu_mp,y, the finite-y instance of the law named after (16); the source normalization issue remains documented.'},
'1.18':{'D2':'The inline H-hat matrix uses the centered data Y-hat and its blocks from Section 1.1.','D3':'The opening sentence names B-hat, and the final sentence substitutes that unknown-mean matrix in both inherited Corollaries.','D8g':'Tr f(H-hat) uses the extension of Definition 1.4 to any square matrix; it is not the H-specific empirical measure formula.','D9':'The source identifies m-tilde_boxplus as the Stieltjes transform of its inline tilde measure.','D10':'The theorem explicitly identifies omega-tilde_t through Proposition 1.5 with the tilde Bernoulli inputs.','D11':'The theorem defines mu-tilde_boxplus by the generic free-convolution operation on its newly bound p_t/(N-1) Bernoulli laws.','D13':'The theorem explicitly assumes Assumption 1.6.','D14':'It explicitly assumes Assumption 1.7, retaining separate dimensional regimes for the inherited Corollaries.','D16':'The theorem uses the previously specified gamma contours in both analytic hypotheses and tilde integrals.'},
'1.20':{'D2':'The explicit inheritance of Theorem 1.18 includes its centered data and H-hat construction.','D3':'The inherited Theorem 1.18 includes B-hat and its substituted Schott/Wilks conclusions.','D4':'The inherited Theorems 1.11 and 1.17 use H from (4).','D8':'The inherited Theorems 1.11 and 1.17 concern Tr f(H) from Definition 1.4.','D8g':'The inherited Theorem 1.18 also uses the generic spectral statistic at H-hat.','D9':'The inherited centers and variances use the original, finite-y and tilde Stieltjes transforms in their respective branches.','D10':'The inherited 1.11 and 1.18 formulas use their respective subordination functions.','D11':'The inherited 1.11 and 1.18 results use free-convolution centers with different Bernoulli parameters.','D12':'The inherited 1.11 result uses the original finite-N projection measures mu_t.','D14':'Theorem 1.20 explicitly retains dimensional Assumption 1.7.','D15':'Theorem 1.20 explicitly invokes Assumption 1.19 as the replacement entry condition; the full all-moment Assumption 1.6 is not retained.','D16':'The inherited analytic CLTs retain their contour regimes and analyticity restrictions.','D19':'The inherited Theorem 1.17 retains its finite-y Marchenko-Pastur center and its pmax restriction.','D20':'The explicitly inherited Corollaries 1.14 and 1.15 include the original zero-mean B statistics, in addition to the centered variants inherited through 1.18.'},
'5.3':{'D1':'Its alpha_t and the auxiliary product Q_t use the normalized blocks X_t from (3); Q_t is saved in auxiliary passage A11.','D4':'The statistic uses H and the kernel contains the block projections P_t from (4).','D6':'The centering, alpha/beta formulas and K use the resolvent G(z)=(H-z)^(-1).','D7':'Equation (88) and K use lower-case tr, which is normalized by N even for (X_t X_t prime)^(-1).','D8':'Its normalized random variable contains Tr f(H), the linear spectral statistic from Definition 1.4.','D13':'Theorem 5.3 explicitly assumes Assumption 1.6.','D14':'Theorem 5.3 explicitly assumes Assumption 1.7 and chooses a regime by hat-y.','D16':'The analytic-function hypothesis names gamma_1^0 and gamma_2^0, with the general-regime replacements at the end.','D17':'The actual centering and variance integrals use the barred contours, truncated near the real axis in Section 4.','D18':'The source expectation E^chi appears in alpha, beta, the center and K, referring to (22)-(23).'}}
EDGES={
'D3':{'D2':'Definition 1.1 constructs B-hat from the centered observations Y-hat and its blocks.'},
'D4':{'D1':'The projection formula X_t prime (X_t X_t prime)^(-1) X_t uses normalized blocks (3).'},
'D5':{'D4':'The empirical measure takes all eigenvalues of the particular H from (4).'},
'D6':{'D4':'The resolvent is (H-z)^(-1).','D5':'Equation (6) identifies its trace with the transform of the empirical law mu_N.','D7':'The displayed normalized trace uses N^-1 Tr.'},
'D8':{'D5':'The original H-specific LSS formula integrates against mu_N from (5).','D7':'Definition 1.4 uses the unnormalized trace Tr in its spectral sum.'},
'D8g':{'D7':'The explicitly stated extension to other square matrices uses the same trace convention.'},
'D10':{'D9':'Proposition 1.5 characterizes subordination using the negative reciprocal Stieltjes transforms F_mu_t.'},
'D11':{'D9':'The definition identifies F_boxplus as a negative reciprocal Stieltjes transform.','D10':'Equations (12)-(13) define the convolution through the omega_t functions of Proposition 1.5.'},
'D12':{'D4':'The source Bernoulli measure is the ESD of each projection P_t from (4).'},
'D13':{'D1':'Assumption 1.6 explicitly refers to the matrix X in (3).'},
'D15':{'D1':'Assumption 1.19 constrains the entries of the same normalized X while replacing the all-moment bullet.'},
'D16':{'D11':'Contour separation is required also for the images under m_boxplus and for the support of mu_boxplus.','D12':'The support and transform here belong to the original finite-N convolution of the projection laws, as recalled before Theorem 1.11.'},
'D17':{'D16':'The barred contours are explicitly defined by cutting off the previously specified contours (18).'},
'D18':{'D1':'The cutoff product involves each normalized block covariance X_t X_t prime.','D7':'Its cutoff arguments are lower-case traces, normalized by N.'}}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All six main-text Theorems; inherited claims retain their branch conditions and replacement assumptions.',build_order_policy='Source-backed same-paper paths; distinguish generic versus H-specific spectral statistics and never propagate the replaced all-moment assumption.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGES.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            local=[m for m in x['members'] if m['local_id'] in DIRECT[n]]
            if local:
                reason=' '.join(DIRECT[n][m['local_id']] for m in local)
                ev=copy.deepcopy(c['evidence'])
                for m in local:ev.extend(e for e in m['evidence'] if e not in ev)
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+x['interface_id'].split('/')[-1],paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=reason,evidence=ev))
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
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
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
