"""Resolve the four original spectral-EL Theorems against their main-text prerequisites."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '1':{'D12':'The opening sentence explicitly assumes Assumption 1 on the process and mixing.','D13':'The opening sentence explicitly assumes Assumption 2 on the estimating functions.','D15':'The opening sentence explicitly assumes Assumption 3 on the spectral covariance matrix.','D4':'The true parameter explicitly satisfies spectral moment condition (2).','D7':'The displayed block-size condition uses b from the nonoverlapping block construction.','D10':'The conclusion is the chi-square limit of the SEL log-ratio ell_n(theta0) from (7).'},
 '2':{'D12':'The theorem explicitly imports Assumption 1.','D13':'The theorem explicitly imports Assumption 2.','D15':'It imports Assumption 3 and explicitly uses V_theta0 in the limiting covariance.','D4':'Its true parameter is required to satisfy (2).','D16':'The solution sequence hat-theta_n is the spectral M-estimator defined immediately above by (11).','D17':'Conditions (i)–(iv) are fully stated in this theorem, including the definition of D_theta0.'},
 '3':{'D12':'The reference to the assumptions of Theorem 2 imports Assumption 1.','D13':'The same reference imports Assumption 2.','D15':'The same reference imports Assumption 3.','D17':'The same reference imports the four neighborhood regularity conditions in Theorem 2.','D4':'The imported assumptions require theta0 to satisfy (2).','D16':'The bootstrap CDF is evaluated at the full-data spectral M-estimator hat-theta_n.','D7':'The block-size condition uses the block length b of SEL and its bootstrap.','D10':'The sampling CDF is that of the baseline SEL log-ratio ell_n(theta0).','D22':'The conditional bootstrap CDF is that of ell_n^*(hat-theta_n), defined on page 12.'},
 '4':{'D12':'The reference to the assumptions of Theorem 3 recursively imports Assumption 1.','D13':'That reference imports Assumption 2.','D15':'That reference imports Assumption 3.','D17':'It imports the neighborhood regularity conditions of Theorem 2 through Theorem 3.','D4':'The imported assumptions require the underlying theta0 to satisfy the spectral moment condition.','D7':'The block-size expression uses b from the block construction; the printed limit here is infinity, conflicting with the imported zero limit.','D23':'The left statistic ell_n(vartheta0) is the smooth-function SEL profile defined in Section 7.','D24':'The bootstrap statistic is evaluated at hat-vartheta_n=h(hat-theta_n).','D26':'Its conditional bootstrap CDF uses the smooth-function bootstrap profile log-ratio.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned 26-page published article, DOI 10.1214/24-AOS2388. Main text is pages 1-22 above the Appendix A heading on page 22; appendices are excluded.',
     normalization_policy='Preserve complete published statements, printed numbering and source terminology. Retain the OL periodogram normalization and infinite block-size limit, recording the conflicts separately.',
     semantic_ranking_policy='Count statement prerequisites and their paper-local definition dependencies. Keep nonoverlapping SEL blocks distinct from overlapping bootstrap blocks and full-data M-estimation. Do not import proof-only propositions or application-specific models.',
     build_order_policy='Derive canonical edges from local definitions. Distinguish evaluated resampling at the fitted parameter from resampling entire parameter-indexed block-statistic functions.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                evidence=list(c['evidence'])
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=evidence))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
            sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])
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
    print('Structural validation passed; independent full source audit remains pending.')
    finalized=json.loads((ROOT/'ranked-interfaces.json').read_text())
    passages=dict(paper_id=PID,members=[m for x in finalized['interfaces'] for m in x['members']])
    (ROOT/'source-passages.json').write_text(json.dumps(passages,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
