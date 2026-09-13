"""Derive and validate this paper's census from its reviewed inventory and local graph."""
import copy
import json
import subprocess
import sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges,main as save_passages

SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory

DIRECT={
 '1':{
  'D5':'The opening hypothesis requires M to be a DMAG, with the ancestral and maximality conditions specified in Section 2.',
  'D7':'The opening hypothesis explicitly requires time series structure and supplies its time-index set.',
  'D10':'The characterization quantifies over a ts-DAG D, whose definition requires a DAG on all integer times with time order and repeating edges.',
  'D13p':'The ts-DMAG characterization and MAG latent projection are expressed using M^p(D), the regular-sampling notation fixed in Section 4.2.',
  'D16':'The fixed-point criterion uses the canonical ts-DAG D_c(M) from Definition 4.13.'},
 '2':{
  'D2':'The graph G in the opening hypothesis is a directed mixed graph; unlike Theorem 1 it is not assumed ancestral or maximal.',
  'D7':'The statement explicitly supplies time series structure and its time-index set.',
  'D3':'The right side of the equivalence explicitly requires G to be acyclic, using the directed-cycle convention in Section 2.',
  'D10':'The left side quantifies over a ts-DAG D as in Definition 3.4.',
  'D13p':'The ts-DMAG and fixed-point assertions use M^p(D), the regular-sampling projection notation from Section 4.2.',
  'D16':'The equality on the right uses the canonical construction D_c(G) in Definition 4.13.'},
 '3':{
  'D10':'The opening hypothesis requires D to be a ts-DAG.',
  'D22':'The three permitted pairs of background knowledges use all four Boolean restrictions from Definition 5.4.',
  'D13p':'The conclusions use the regularly sampled graph M^p(D).',
  'D15':'The conclusions also use its stationarification M^p_st(D), abbreviated in Section 4.4.',
  'D14':'Parts 1 and 3 apply stat to the refined DPAG P(M^p(D),A); this is the four-edge-type operation from Definition 4.6.',
  'D19':'Every conclusion compares maximally informative DPAGs P(M,A) constructed using Definition 5.2.',
  'D6':'All four conclusions concern non-circle endpoint marks, defined in Section 2 as heads or tails.'}
}

def main():
    save_passages()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Pinned arXiv:2112.08417v2. All three main-text Theorems and relevant source passages reviewed against the PDF; supplementary material excluded.',
        normalization_policy='Preserve printed wording, formulas, labels and source inconsistencies; expand macros and normalize line wrapping and typographic emphasis only.',
        semantic_ranking_policy='All three inventoried Theorems retained; direct demand counted once per theorem and interface, independently of proof use.',
        build_order_policy='Derive from the acyclic same-paper dependency graph; the regular-sampling abbreviation retains its own path to the general ts-DMAG definition.')
    data['interfaces']=copy.deepcopy(interfaces)
    claims={c['claim_id']:c for c in data['claims']}
    for c in data['claims']:
        number=c['claim_id'].split('/T')[-1]
        direct=DIRECT[number]
        c['depends_on']=list(direct)
        for x in data['interfaces']:
            used=[m['local_id'] for m in x['members'] if m['local_id'] in direct]
            if used:
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+x['interface_id'].split('/')[-1],
                    paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=' '.join(direct[lid] for lid in used),evidence=c['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];number=cid.split('/T')[-1]
            sentences=[DIRECT[number][path[0]]]
            evidence=list(claims[cid]['evidence'])
            for lid in path:
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
            for a,b in zip(path,path[1:]):sentences.append(edges[a][b])
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=' '.join(sentences),evidence=evidence)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
            linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors),(m['local_id'],'no source highlight')
            assert all(s in linked for s in selectors),(m['local_id'],'unmatched selectors',[s for s in selectors if s not in linked])
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('All source highlight selectors matched. Census finalized and independently validated; final source-audit record remains.')

if __name__=='__main__':main()
