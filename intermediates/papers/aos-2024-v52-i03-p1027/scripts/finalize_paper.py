"""Derive all five theorem dependency sets from their statements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
BASE={'D1':'The theorem explicitly invokes the scalar BEKK model (1.1).','D6':'Assumption 1 supplies all four Gaussian, population-spectrum, norm and aspect-ratio conditions.'}
DIRECT={
 '1':{**BASE,'D10':'The displayed eta-to-zero hypothesis is the source reducible case, with eta defined by (2.1).','D9':'The conclusion applies the Levy distance L to two empirical spectral distributions.','D5':'F raised to each sample covariance denotes its equal-weight eigenvalue distribution.','D4':'The two distributions in the conclusion belong to the dynamic and coupled iid sample covariance matrices.'},
 '2':{**BASE,'D11':'The eta>c hypothesis is the source non-reducible case, with eta defined by (2.1).','D12':'The conclusion compares E(M_2^p) and E(M_2^{0,p}), the expected second moments of the two empirical eigenvalue distributions.'},
 '3':{**BASE,'D15':'The hypothesis constrains M_p, the lag count in the projection matrix (2.5).','D17':'The first distribution in the conclusion belongs to the adjusted sample covariance (2.6).','D4':'The second distribution uses the coupled iid comparison covariance S_n^0.','D5':'Both F expressions denote the empirical spectral distribution of the indicated matrix.','D9':'The conclusion measures their difference with the Levy distance L.'},
 '4':{**BASE,'D15':'The hypothesis constrains M_p, the projection lag count, to diverge more slowly than sqrt(p).','D24':'The theorem additionally restricts the limiting support of H and the bounded function g.','D20':'The random quantity Theta_n^g(z) is the population-weighted resolvent trace (2.11).','D18':'The displayed limiting integral uses m_F(z), specified by (2.8) and the Marchenko–Pastur equation (2.9).'},
 '5':{'D1':'The assumptions inherited from Theorem 4 require model (1.1).','D6':'The inherited Assumption 1 retains all four Gaussian, spectral and dimension conditions.','D15':'The inherited Theorem 4 lag-growth condition concerns M_p in the projection matrix (2.5).','D24':'The reference to the assumptions of Theorem 4 retains its limiting-support and bounded-g restrictions.','D22':'The left-hand matrix tilde-Sigma is the TV-adj NLS construction from the external Ledoit–Wolf algorithm.','D23':'The comparison matrix tilde-Sigma with superscript or is the separate population-law oracle (2.13).','D8':'The conclusion uses the Frobenius norm with its explicit external factor p^{-1/2}.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned 49-page arXiv:2211.10203v2. Main text and references through page 36 only; attached supplement from page 37 excluded.',
     normalization_policy='Preserve all five complete Theorems and source formulas, including the printed QMLE optimization direction, y versus inverse-y transform coefficients, ordinary oracle square and companion notation. Record ambiguities separately.',
     semantic_ranking_policy='Count statement prerequisites and recursive source definitions only. Resolve every inherited assumption, but do not import the conclusions of Theorem 4 into Theorem 5 or proof-only external results.',
     build_order_policy='Keep the two eta regimes distinct; archive the unnamed eta formula and contextual generalized ESD locally. Derive the dependency DAG from the paper-local edges without inferring library availability.')
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
