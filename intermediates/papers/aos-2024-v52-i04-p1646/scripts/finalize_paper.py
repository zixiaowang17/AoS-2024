"""Attach paper-local statement dependencies and derive the census."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
'1':{'D5':'Theorem 1 explicitly assumes C1, the unchanged training-period loading space.',
     'D6':'Theorem 1 explicitly assumes C2, the monitoring-horizon growth condition.',
     'D11':'The opening explicitly requires the transformation rate condition (3.17).',
     'D12':'The conclusions use conditional distribution D* and probability P*, and hold for almost all original-data realizations.',
     'D14':'Part (i) uses the weighted functional (3.19), with eta below one half.',
     'D15':'Part (ii) uses the standardized partial-sum maximum (3.20), with the auxiliary alpha_Tm and beta_Tm normalization.',
     'D16':'Part (iii) uses the Renyi statistic (3.21), including the diverging trimming sequence r_Tm.'},
'2':{'D5':'Theorem 2 explicitly assumes C1, the unchanged training loading space.',
     'D6':'Theorem 2 explicitly assumes C2, the growth of Tm.',
     'D11':'The opening requires g to satisfy (3.17); the extra power conditions are bound in each part of the theorem.',
     'D12':'The divergence statements and rejection probability use P* conditional on the full data.',
     'D14':'Part (i) studies the same eta-below-one-half weighted functional.',
     'D15':'Part (ii) studies the standardized partial sums with auxiliary alpha_Tm,beta_Tm.',
     'D16':'Part (iii) uses the trimmed Renyi statistic and its r_Tm normalization.',
     'D7':'The opening names (3.7), and parts (ii) and (iii) explicitly restrict their conclusions to this fixed-count loading-space change.',
     'D8':'The opening also names (3.9), the additional-factor alternative. Parts (ii) and (iii) repeat only (3.7), so the broader opening is not silently extended to them.'},
'3':{'D6':'Theorem 3 explicitly assumes C2, while its printed list does not include C1.',
     'D11':'The theorem requires g to satisfy (3.17); its additional alternative rate is stated in (3.33).',
     'D12':'Both limits are for the conditional probability P*, almost surely with respect to the original data.',
     'D17':'The normalized variable Z_Tm is the one-sided maximum of randomized observations in (3.31).',
     'D18':'The normalization uses the maximum-statistic sequences a_Tm and b_Tm introduced immediately before the theorem.',
     'D7':'The alternative statement explicitly includes the factor-space change (3.7).',
     'D8':'The alternative statement also explicitly includes the additional-factor model (3.9).'}}
def extra(n):
    return [dict(page=9,location='Delta tuning and transformation definitions'),dict(page=10,location='Conditional-law and monitoring conventions')]

def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
      source_policy='Registered arXiv:2112.13479v1 PDF, 45 pages; pages 1-30 and references above Appendix A on page 31 only.',
      normalization_policy='Preserve all three complete original Theorems, their continued subparts, printed equalities and exact assumption lists. Keep B1-B4 supplementary references unresolved.',
      semantic_ranking_policy='Resolve the source matrix model, projected eigenvalues, transformation, randomization, monitoring statistics, conditional law and alternative branches. Preserve auxiliary tuning and normalization formulas. Do not silently add C3 to Theorem 2 or C1 to Theorem 3.',
      build_order_policy='Derive edges and reach from paper-local dependencies without altering the independent inventory.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                evidence=list(c['evidence'])+extra(n)
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=evidence))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
            sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])+extra(n)
            for lid in path:evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
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
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=[m for x in finalized['interfaces'] for m in x['members']]),indent=2,ensure_ascii=False)+'\n')
    print('Census structurally valid; independent full source review remains pending.')
if __name__=='__main__':main()
