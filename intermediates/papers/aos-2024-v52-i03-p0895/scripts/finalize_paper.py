"""Derive all three theorem connections from their main-text definitions and hypotheses."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{'D1':'The theorem concerns a sequence of true sampling laws L_n.','D4':'It explicitly introduces learned laws and uses learned-kernel variances and conditional resampling moments.','D3':'NDG2 contains the true response conditional mean mu_n,y, alongside its fitted counterpart.','D6':'Both conclusions concern the four-argument resampled residual-product statistic.','D8':'NDG1 and the standardized statistic use the conditional resampling standard deviation S-hat_n.','D9':'The second conclusion is convergence of the conditional quantile Q_{1-alpha}.','D11':'The first conclusion uses the d,p conditional distribution convergence defined in Definition 1.','D12':'The second displayed nondegeneracy property is the full condition labeled NDG2.'},
 '2':{'D2':'The theorem explicitly assumes L_n belongs to the conditional-independence null class.','D18':'The first referenced regression-rate condition is the strengthened SP1-prime.','D15':'The theorem explicitly references the residual-product moment condition SP2.','D12':'The theorem explicitly references NDG2, without separately assuming NDG1.','D16':'It explicitly requires the variance consistency property (23).','D3':'The displayed Lyap-2 condition uses the true response conditional mean mu_n,y.','D4':'Lyap-2 includes a learned-law conditional moment of the resampled predictor.','D8':'The numerator of variance ratio (25) is the conditional resampling variance.','D7':'The denominator of (25) and the GCM decision in (26) are defined in (8)-(10).','D10':'Decision equality (26) uses the infinite-resampling dCRT defined in Section 2.'},
 '3':{'D2':'The null class R is explicitly a subset of the conditional-independence class L^0.','D14':'Condition (35) explicitly requires SP1 for laws in R.','D15':'Condition (35) explicitly requires SP2 for laws in R.','D7':'The asserted optimal test and its displayed power are those of the GCM decision in (8).','D20':'The theorem explicitly invokes the GPLM family (29), its nuisance subspace, log-partition function and fixed predictor/covariate law.','D21':'Conditions (38) and the power conclusion use the local paths theta_n(h); s(theta_0) is defined in (34).','D22':'The problem (32) and conclusion LAUMP(S) use the full optimality definition, including its null-level comparison class.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned arXiv:2211.14698v2, margin stamp 8 February 2023 and title-page date 10 February 2023. Main text and references end above y=288.68743896484375 on shared PDF page 34. All appendix mathematics is excluded.',
     normalization_policy='Preserve all three complete Theorems and original source definitions. Distinguish bold population variables from plain sample arrays, script law classes from calligraphic individual laws, and resampling variance from GCM empirical variance.',
     semantic_ranking_policy='Only direct statement uses and recursive local prerequisites. Inline NDG1 and Lyap-1/Lyap-2 remain in the complete theorem statements; no appendix result or proof-only optimality construction is imported.',
     build_order_policy='Keep sample and null-law definitions separate. The raw fitted-mean statistic used by GCM does not require a resampling kernel; preserve the extra learned-law requirements only on the dCRT paths. Keep SP1-prime distinct from SP1.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
            sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])
            for lid in path:
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                for ctx in members[lid].get('application_context',[]):
                    evidence.extend(e for e in ctx['evidence'] if e not in evidence)
            for a,b in zip(path,path[1:]):sentences.append(edges[a][b])
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=' '.join(sentences),evidence=evidence)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
            linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors),(m['local_id'],'missing source highlight')
            assert all(s in linked for s in selectors),(m['local_id'],'unmatched selector')
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Finalized and independently validated; final source audit remains.')


if __name__ == "__main__":
    main()
