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
  'D1':'The statement explicitly quantifies over memory bounded estimation algorithms with resource profile (N,T,s), defined by sequential passes and finite-bit updates in Definition 1.',
  'D2':'The k-TPCA problem supplies the Gaussian tensor observation law, the sphere-valued parameter V, lambda and the family of probabilities P_V used in the bound.'},
 '2':{
  'D1':'The statement again restricts the estimator to Definition 1 with resource profile (N,T,s); its memory exponent is named b in this theorem.',
  'D3':'The k-ATPCA problem supplies the rank-one tensor parameter space, its Gaussian observation law and signal lambda. The tensor norm is interpreted by the Section 2.1 entry-stacking convention.'},
 '3':{
  'D1':'The theorem explicitly requires a memory bounded estimation algorithm with profile (N,T,s), using Definition 1.',
  'D5':'The named k-NGCA problem refers to Section 6.1.1: the first k-1 scalar moments match a Gaussian and lambda is the absolute kth-moment difference.',
  'D9':'The first enumerated hypothesis is the Moment Matching Assumption, printed as Assumption 1.',
  'D10':'The second enumerated hypothesis imposes Assumption 2 with bounded K and signal parameter lambda.',
  'D11':'The third enumerated hypothesis imposes Assumption 3 with bounded K and kappa; the same kappa occurs in the restriction on gamma.'},
 '4':{
  'D1':'The theorem explicitly requires Definition 1 with resource profile (N,T,s).',
  'D12':'The named k-CCA problem supplies the k-view cross-moment model, the rank-one parameter tensor and its signal parameter.',
  'D13':'The final sentence says the bound holds even when the sampling law satisfies (30), the specified sign-perturbed Gaussian density.',
  'D14':'The final sentence also includes promise (31), restricting V to a scaled tensor product of standard basis vectors.'}
}

def main():
    save_passages()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Pinned arXiv:2204.07526v2. All four main-text Theorems and relevant source passages reviewed against the PDF; supplementary material excluded.',
        normalization_policy='Preserve printed wording, formulas, labels and source inconsistencies; expand macros and normalize line wrapping and typographic emphasis only.',
        semantic_ranking_policy='All four inventoried Theorems retained; direct demand counted once per theorem and interface, independently of proof use.',
        build_order_policy='Derive from the acyclic same-paper dependency graph; each problem retains its own model and signal assumptions.')
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
