"""Finalize the inspected local graph; source review and reproduction are separate gates."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
1:{'D1':'The dagger specialization (22) concerns the observed-target risk; Delta_v also explicitly conditions on A=0, leaving a separate notation issue for an unobserved target.',
'D2':'The general estimator targets r_*=E_Q ell from Section 3, where the target Q need not be observed.',
'D3':'Delta_v and the empirical expansion explicitly use sequential histories bar Z_k and component indices k.',
'D4':'The final additional clause assumes DS.0 to conclude Delta=0; preceding branches retain their drift correction.',
'D7':'The nuisance list, ratio-error bounds and true D_GSC arguments use lambda_* and its fitted estimates.',
'D8':'The drift and empirical expansion explicitly use true and fitted marginal population probabilities pi.',
'D9':'The opening nuisance list and dagger expansion (22) use the conditional odds theta and their fitted estimates.',
'D10':'The nuisance list and pseudo-loss evaluations explicitly use the backward conditional means ell_* and their fitted estimates.',
'D11':'Expansion (19) explicitly evaluates T-tilde at true and fitted nuisance collections.',
'D13':'The expansion, third-moment condition and (21) explicitly use D_GSC from (8).',
'D14':'The dagger expansion (22) explicitly uses D_SC from (9).',
'D15':'The confidence bound names sigma_*,GSC and explicitly references (10).',
'D16':'The statement selects general Algorithm 1 and its Line 9 output; the algorithm body is in the excluded supplement and remains unresolved.',
'D17':'The statement also selects Algorithm 1-dagger and its Line 9 output, defined by the complete main-text recipe.',
'D18':'The drift and confidence hypotheses explicitly use oracle regressions h_v^{k-1}.',
'D19':'The statement sums B_{k,v}; for the general algorithm this is the product-bias expression (12).',
'D20':'For the selected dagger algorithm, the same B_{k,v} has the transformed expression (13), with the corresponding branch of the rate conditions.',
'D21':'The efficiency branch expressly assumes ST.1 with its matching general or dagger formulas.',
'D22':'The consistency branch expressly assumes ST.2 with weaker stochastic rates.',
'D26':'The final additional DS.0 clause describes the estimator as RAL and efficient, using the main-text terminology.'},
2:{'D1':'The statement expressly takes the observed-target risk r_* from (1).',
'D6':'The common hypothesis expressly names DS.1, feature independence X independent of A in the one-source setup.',
'D23':'The final efficient branch identifies E_infinity with the conditional target-risk function E_*; the earlier branch permits a different limit.',
'D24':'The leading term and remainder explicitly use D_Xcon from (23), including evaluation at a possibly inconsistent limit E_infinity.',
'D25':'The estimator is expressly the Line 5 output of the Section 4 Algorithm 1, with out-of-fold regression and in-fold target proportion.',
'D26':'The conclusion calls the estimator RAL and then gives an efficiency branch, using the Section 2 terminology.'}}
EDGES={
'D3':{'D2':'The sequential component histories belong to the general target-Q setup.'},
'D4':{'D2':'DS.0 compares source laws with the target law Q.','D3':'Its domination and equality requirements use histories and target supports.'},
'D5':{'D4':'DS.0-dagger explicitly requires DS.0 and additionally includes the target index in every relevant-population set.'},
'D6':{'D1':'DS.1 uses the feature and population variables from the observed-data setup, with the separately retained binary convention.'},
'D7':{'D2':'The numerator history law is induced by the general target Q.','D3':'The density ratio is defined on histories through k-1.'},
'D8':{'D3':'Conditional population probabilities are indexed by histories; k=0 yields marginal probabilities.'},
'D9':{'D8':'The odds are ratios of conditional population probabilities; (4) also uses marginal pi.','D7':'Equation (4) identifies the history density ratio by an odds transformation.','D5':'The source qualifies identity (4) by DS.0-dagger; this is not a global assumption on every theorem branch.'},
'D10':{'D2':'The recursive loss uses ell and its stated conditional-risk identity uses Q.','D3':'The recursion evaluates sequential histories on their target supports, with arbitrary extensions outside.'},
'D11':{'D3':'The general pseudo-loss evaluates successive component histories.','D7':'Its generic lambda arguments correspond to the history density ratios.','D8':'Its weights contain sums of marginal population probabilities.','D10':'Its generic ell arguments correspond to backward conditional mean losses.'},
'D12':{'D3':'The odds pseudo-loss evaluates successive component histories.','D8':'Its weights contain pi^0 and the marginal-probability expression theta^0.','D9':'Its inverse-odds factors use the relevant-source conditional odds.','D10':'Its increments compare successive conditional mean loss arguments.'},
'D13':{'D11':'D_GSC subtracts a weighted r from T-tilde.','D8':'Its centering weight sums marginal population probabilities over S-prime_1.'},
'D14':{'D12':'D_SC subtracts a weighted r from T.','D8':'Its centering factor uses pi^0 and the separately retained generic theta^0 convention.'},
'D15':{'D13':'The general variance is the second moment of D_GSC at the true nuisances and risk.','D14':'The adjacent dagger specialization is the second moment of D_SC.','D2':'Both variance formulas evaluate the influence functions at the target risk r_*.','D26':'The efficient-bound wording uses the source RAL and efficiency terminology.'},
'D16':{'D2':'The available sentence places the unresolved general algorithm in the target-Q setup.'},
'D17':{'D1':'The algorithm title identifies the observed-target conditional risk.','D3':'Its loops and predictors use sequential histories.','D5':'Its title motivates the recipe under DS.0-dagger; Theorem 1 also studies drift when that condition fails.','D8':'Line 4 estimates marginal population probabilities in-fold.','D9':'Line 3 estimates population odds out-of-fold.','D10':'Lines 5–7 recursively estimate conditional mean losses.','D12':'Line 8 evaluates T to obtain the fold estimate.'},
'D18':{'D3':'The oracle regression conditions on the preceding history.','D10':'It targets the preceding conditional mean loss using the next fitted regression as response.'},
'D19':{'D2':'The correction in (12) integrates the regression discrepancy under Q.','D7':'The first factor compares fitted and true density ratios.','D8':'Both terms use true and estimated marginal population probabilities.','D10':'The error factor includes the fitted previous conditional mean loss.','D18':'The other error-factor term is the oracle regression h_v^{k-1}.'},
'D20':{'D1':'The dagger correction integrates conditional on the observed target A=0.','D8':'The formula uses true and estimated marginal population probabilities.','D9':'Its density-ratio discrepancy is written using the odds transformation (4).','D10':'It includes the fitted previous conditional mean loss.','D18':'Its product factor includes the oracle regression h_v^{k-1}.'},
'D21':{'D8':'The L2 discrepancies are weighted by sums of marginal population probabilities.','D11':'Equation (15) compares fitted and true T-tilde.','D12':'Equation (16) compares fitted and true T.','D19':'The general bias-sum branch uses B_{k,v} from (12).','D20':'The dagger bias-sum branch uses B_{k,v} from (13).'},
'D22':{'D21':'ST.2 replaces the two stochastic rates in ST.1 while retaining the matching branch formulas.'},
'D23':{'D1':'E_* is the conditional mean of the given loss in the observed target population.'},
'D24':{'D1':'D_Xcon evaluates observed loss and population index; its generic E argument is not assumed to equal E_*.'},
'D25':{'D1':'The specialized fold estimates average corrected loss to estimate the observed-target risk.','D23':'Its regression step targets E_*, while the theorem permits convergence to a different function.'}}

def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Both complete main-text Theorems; preserve all algorithm and condition branches and unresolved general algorithm references.',build_order_policy='Topological ordering of inspected local definitions, with missing supplement dependencies explicitly unresolved.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGES.get(lid,{})),lid
    for c in data['claims']:
        n=int(c['claim_id'].split('/T')[-1]);c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            m=x['members'][0];lid=m['local_id']
            if lid in DIRECT[n]:x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']+m['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for rel in x['related_theorems']:
            cid=rel['claim_id'];n=int(cid.split('/T')[-1]);path=rel['via_local_ids']
            explanation=' '.join([DIRECT[n][path[0]]]+[EDGES[a][b] for a,b in zip(path,path[1:])])
            ev=copy.deepcopy(claims[cid]['evidence'])
            for lid in path:ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=explanation,evidence=ev)
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
    print('Census structurally validated; original claims and footnote retained; independent source review remains pending.')
if __name__=='__main__':main()
