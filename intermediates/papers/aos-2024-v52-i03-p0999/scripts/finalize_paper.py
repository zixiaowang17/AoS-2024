"""Derive the four theorem dependency sets without importing proof-only prerequisites."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
ASSUMPTIONS={
 'D2':'Assumption 1 imposes the regression model and conditional mean-zero errors.',
 'D3':'Assumption 1a supplies the time-varying coefficient sparsity bound.',
 'D4':'Assumption 1b supplies the jump-size upper bound and minimum spacing.',
 'D34':'The Assumption 1 preamble fixes K and defines each signed and normalized jump vector.',
 'D12':'The Assumption 2 preamble specifies mean-zero stationary covariates and their covariance.',
 'D13':'Assumption 2a requires fourth-moment uniform covariate dependence decay.',
 'D14':'Assumption 2b requires the uniform directional tail bound.',
 'D15':'Assumption 2c requires a positive covariance lower bound and supplies the limiting drift varpi_k.',
 'D16':'The Assumption 3 preamble specifies stationary mean-zero noise with positive marginal variance.',
 'D17':'Assumption 3a requires the noise fourth-moment dependence decay.',
 'D18':'Assumption 3b supplies the scalar noise tail bound.',
 'D21':'Assumption 4b strengthens (24), retaining its baseline signal-spacing requirement.'
}
TUNING={
 'D19':'The inherited DPDU tuning exponent gamma is defined by (23).',
 'D25':'The preliminary change-point estimates are required to be outputs of DPDU in Algorithm 1.',
 'D22':'The interval coefficient estimates are the Lasso fits (14) on the preliminary segments.',
 'D26':'The source local intervals are constructed by (18).'
}
DIRECT={
 '3':{**ASSUMPTIONS,**TUNING,'D27':'The theorem analyzes the final local refinement estimators (17).','D28':'The vanishing-regime limit uses sigma_infty(k), the long-run standard deviation defined by (25).','D33':'Part b explicitly studies the vanishing jump regime.'},
 '4':{'D10':'The theorem explicitly requires a possibly nonstationary process of the form (10).','D11':'It explicitly uses the cumulative functional dependence measure (11) at q=2.'},
 '8':{**ASSUMPTIONS,**TUNING,'D28':'The consistency target is the long-run variance (25).','D29':'The theorem explicitly supplies the jump-size estimates (30) to the variance algorithm.','D30':'The variance estimates are the outputs of Algorithm 2 under the displayed block-count growth condition.','D33':'Section 4 restricts this variance inference procedure to the vanishing jump regime.'},
 '10':{**ASSUMPTIONS,**TUNING,'D28':'The limiting distribution uses the population long-run standard deviation sigma_infty(k).','D29':'The left-hand side is scaled by the squared jump estimator from (30) and its nonzero indicator.','D30':'The assumptions inherited from Theorem 8 require the specified Algorithm 2 variance estimate and block-count growth.','D32':'The simulated minimizer u-hat^(1) is defined by (32), here with M=infinity.','D33':'Section 4.1 develops this inference procedure under the vanishing jump regime.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned 112-page arXiv:2207.12453v3 artifact, margin date 1 October 2023 and title-page date 3 October 2023. Main text and references end on page 33; appendices from page 34 are excluded.',
     normalization_policy='Preserve all four complete Theorems, original algorithm indices, the separate noise/innovation symbols, Brownian typography, regime-specific limits and all inherited assumptions.',
     semantic_ranking_policy='Count only statement prerequisites and recursive main-text definitions. Theorem 4 has no regression-model or estimator prerequisites. Theorems 8 and 10 inherit assumptions, not the conclusions of Theorem 3.',
     build_order_policy='Keep stationary covariate, stationary noise and nonstationary scalar dependence measures distinct. Generic innovation replacement is archived as ambient context. Preserve each algorithm as printed and record its indexing ambiguities.')
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
    finalized=json.loads((ROOT/'ranked-interfaces.json').read_text())
    passages=dict(paper_id=PID,members=[m for x in finalized['interfaces'] for m in x['members']])
    (ROOT/'source-passages.json').write_text(json.dumps(passages,indent=2,ensure_ascii=False)+'\n')
    print('Finalized and independently validated; final source audit remains.')


if __name__ == "__main__":
    main()
