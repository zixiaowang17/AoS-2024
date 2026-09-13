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
  'D1':'The statement explicitly requires continuous x and y, and uses the random-sample convention fixed in Section 2.1.',
  'D14':'The hypothesis explicitly invokes Assumption 1 with its four dimension-dependent moment limits.',
  'D18':'The assertion is explicitly under H0 in (1), independence between the two vectors.',
  'D8':'The numerator of the displayed normal limit is exactly the aggregate statistic (4).',
  'D10':'The displayed limit divides by the null variance scale S described around (5).'},
 '2':{
  'D1':'The conditions of Theorem 1 include continuous sampled vectors from Section 2.1.',
  'D14':'The opening reference to the conditions of Theorem 1 includes Assumption 1, not its normal-limit conclusion.',
  'D18':'The inherited conditions of Theorem 1 include the vector-independence null H0.',
  'D11':'The assertion concerns S-hat squared from (6), the explicit six-index estimate.',
  'D10':'The denominator S squared and unbiasedness expression use the null variance term in Section 2.2.',
  'D12':'The final assertion concerns the normalized statistic T-hat defined at the end of Section 2.2.'},
 '3':{
  'D1':'The reference to the conditions of Theorem 1 includes continuous sampled vectors.',
  'D14':'The reference to the conditions of Theorem 1 imports Assumption 1.',
  'D18':'The reference to the conditions of Theorem 1 imports H0, independence between vectors.',
  'D12':'The probability in the normal-approximation bound is the cdf of the normalized statistic T-hat.',
  'D15':'The right-hand side uses V(z1,z2) and its cyclic fourth product, defined in the immediately preceding paragraph.'},
 '4':{
  'D1':'The random-sample and continuous-vector convention at the start of Section 2.1 applies to this later statement.',
  'D2':'The opening sentence explicitly quantifies over coordinate-pair U-statistics with a common kernel h.',
  'D7':'The centering and scaling expression explicitly uses Delta-h and the kernel order d from Section 2.2.',
  'D16':'The displayed sum subtracts theta-h^(kl), the kernel expectation defined in Section 2.4.',
  'D17':'The opening sentence explicitly requires (8)-(10); the following S_h definition supplies the variance scale S used in the normal limit under local alternatives.'},
 '5':{
  'D2':'The expectation in part (1) is that of the coordinate-pair U-statistic defined in Section 2.1.',
  'D3':'Parts (1) and (3) explicitly treat the kernel h^(D), the Hoeffding kernel in Definition 1(a).',
  'D4':'Parts (1) and (3) explicitly treat the kernel h^(R), the Blum-Kiefer-Rosenblatt kernel in Definition 1(b).',
  'D5':'Parts (1) and (3) explicitly treat the kernel h^(tau-star), the Bergsma-Dassios-Yanagimoto kernel in Definition 1(c).'}
}

def main():
    save_passages()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Pinned PMC11064990 author manuscript, PDF created 2023-11-29. All five main-text Theorems and relevant passages checked against the PDF; separate supplement excluded.',
        normalization_policy='Preserve printed wording, formulas, labels and source inconsistencies; expand macros and normalize line wrapping and typographic emphasis only.',
        semantic_ranking_policy='All five inventoried Theorems retained; direct demand counted once per theorem and interface, independently of proof use.',
        build_order_policy='Derive from the acyclic same-paper dependency graph; null conditions and local-alternative variance conventions remain distinct.')
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
