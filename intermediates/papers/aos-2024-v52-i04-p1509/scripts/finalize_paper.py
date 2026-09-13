"""Attach source-reviewed theorem-to-interface paths and finalize this paper."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={'1':{
'D1':'The explicitly incorporated limits (2) and (7) take the greatest convex minorant of G_x+M_x^q on the real line.',
'D3':'The common limiting random variable in (2) and (7) is the left derivative of that greatest convex minorant at zero.',
'D4':'Equation (8) compares errors of the original generalized Grenander estimator theta-hat_n at the fixed point.',
'D5':'The incorporated equations (2) and (7) use r_n=n^(q/(1+2q)) and the q-dependent drift; q is the first nonzero derivative order.',
'D6':'The limiting distributions in the referenced equations (2) and (7) contain the deterministic monomial M_x^q from (3).',
'D7':'The theorem expressly invokes every clause A1-A3 of Assumption A.',
'D9':'Equation (8) uses the proposed drift-corrected bootstrap estimator theta-tilde-star, defined by the transformed primitive on page 6.',
'D12':'The theorem expressly invokes all seven clauses of Assumption B, including the bootstrap and original process conditions.',
'D14':'The theorem expressly invokes Assumption C, governing the estimated drift and its localized transformation.',
'D15':'The common limit in equations (2) and (7) uses the centered Gaussian process G_x whose covariance is specified in B1.'}}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Verified registered arXiv:2303.13598v3 PDF, 66 pages; main text through the simulation discussion on page 20, above Appendix A.',
        normalization_policy='Preserve the sole original Theorem 1 exactly, including references to equations (2) and (7); retain those complete source formulas in auxiliary passages without rewriting the theorem.',
        semantic_ranking_policy='Resolve the generalized Grenander estimator, generic bootstrap inputs, corrected primitive, all of Assumptions A-C, and the referenced limit laws. Save unnamed bootstrap-process formulas as auxiliary context; do not invent display names or import implementation assumptions and appendix results.',
        build_order_policy='Derive all edges and reach from the original local dependency graph; keep the independent theorem inventory unchanged.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                evidence=list(c['evidence'])+[dict(page=5,location='Equation (2), incorporated by Theorem 1'),dict(page=7,location='Equation (7), incorporated by Theorem 1')]
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=evidence))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
            sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])+[dict(page=5,location='Equation (2), incorporated by Theorem 1'),dict(page=7,location='Equation (7), incorporated by Theorem 1')]
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

if __name__ == "__main__":
    main()
