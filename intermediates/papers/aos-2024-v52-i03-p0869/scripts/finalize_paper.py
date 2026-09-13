"""Derive all four theorem connections from their main-text definitions and hypotheses."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '2.4':{'D1':'The statement compares the original target sequence pi_n under its data law Q^(n) with the limiting target.','D2':'P_n and the limiting tilde-P are the exact deterministic-scan Gibbs kernels introduced in Sections 2.1-2.2.','D3':'Both suprema run over the explicitly written warm-start classes N(pi_n,M) and N(tilde-pi,M).','D4':'The sole numbered hypothesis is (A1), which supplies the coordinatewise transformations and limiting target.'},
 '3.1':{'D5':'The opening sentence explicitly invokes the fixed-dimensional iid Bayesian model (11).','D6':'The displayed error conditions (12) use a sequence of tests u_n; the next-page remark defines these as measurable [0,1]-valued functions.','D7':'The theorem explicitly imposes square-root density differentiability and nonsingular continuous Fisher Information I(psi), whose inverse appears in the limiting Gaussian law.'},
 '4.2':{'D9':'The theorem explicitly starts with the hierarchical model (13), under the standing local-prior restriction in Section 4.','D10':'It explicitly specifies the two-block Gibbs sampler in (15).','D12':'The mixing-time argument is M and the statement quantifies over every fixed M>=1, so it uses the worst-case warm-start definition.','D14':'The reference (B1)-(B6) includes B1, specifying the iid marginal data law, identifiability, regularity and positive prior density.','D15':'The reference (B1)-(B6) includes B2, the uniform testing condition outside a compact neighborhood.','D17':'The reference (B1)-(B6) includes B3, nonsingularity and continuity of marginal Fisher information.'},
 '6.1':{'D9':'The same setting of Theorem 4.2 retains its hierarchical model and standing local-prior assumptions.','D10':'The same setting retains the exact ordered two-block kernel (15).','D11':'Here the second mixing-time argument is the specified initial law mu_J, rather than a warm-start constant M.','D14':'The same setting of Theorem 4.2 includes B1 and its correctly specified iid group data law and prior regularity.','D15':'The same setting includes the B2 testing assumption.','D17':'The same setting includes B3 for the marginal Fisher information.','D19':'The initial law is expressly defined by (35), and the bound depends on its fixed ball-radius constant c.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned arXiv:2304.06993v2, margin stamp 30 October 2023 and title-page date 31 October 2023. Main text and references end on page 27; all appendix mathematics on pages 28-80 is excluded.',
     normalization_policy='Preserve all four original Theorems, exact ordered kernels, distinct start conventions, original hypothesis labels and source notation. B4-B6 are referenced in main text but defined only in excluded Appendix B; retain them as unresolved references without fabricating statements.',
     semantic_ranking_policy='Only direct statement uses and recursive paper-local definition prerequisites. Do not import the proof-only dimensionality reduction, conditional CLT, spectral-gap bounds or example-specific models.',
     build_order_policy='Keep the general fixed-space kernel sequence separate from the growing-dimensional hierarchical sampler. Keep specified-start mixing separate from worst-case warm-start mixing. Define the marginal likelihood before its testing, information and initializer uses.')
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
