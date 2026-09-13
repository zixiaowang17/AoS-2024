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
 '3.1':{
  'D6':'The U and V in the tail-probability ratio are the centered Gaussian vectors fixed immediately before Theorem 3.1.',
  'D7':'Both the scaling assumption and the bound contain Delta-infinity, the maximum covariance-entry difference defined in the preceding paragraph.'},
 '3.3':{
  'D6':'The Gaussian vectors and covariance entries are those fixed at the start of Section 3; this theorem adds unit variances and its own common zero-block partition.',
  'D8':'The right side uses Delta-zero, which counts all differing covariance entries as defined at the start of Section 3.'},
 '4.2':{
  'D2':'The two conclusions bound FDP and FDR, with the rejection-count and expectation conventions in Section 2.',
  'D5':'The theorem explicitly calls for the StarTrek procedure in Algorithm 2.',
  'D9':'The dimensions d1 and d2, coefficient matrix and sample-size limit refer to the multitask regression model fixed in Section 4.',
  'D10':'The additional scaling condition contains s, the maximum row sparsity defined before the estimator.',
  'D11':'The theorem explicitly selects the estimator in (4.2), including its M construction from (4.3).',
  'D4b':'The theorem explicitly specifies the Gaussian quantile approximation (4.6).',
  'D13':'Its first words impose Assumption 4.1, including the random-design, covariance and tuning conditions.',
  'D14a':'The scaling restriction and the bound q*d0/d1 use the null-response count d0 and signal fraction rho defined around (4.8).'},
 '5.2':{
  'D2':'The two conclusions bound the FDP and its expectation FDR defined in Section 2.',
  'D5':'The theorem explicitly uses Algorithm 2 for hub selection.',
  'D15':'The observations, true precision matrix and initial estimator belong to the Gaussian graphical-model setup of Section 5.',
  'D16':'The theorem explicitly supplies the standardized one-step estimator (5.1) to StarTrek.',
  'D4c':'The stated quantile approximation is (5.2), the Gaussian precision-model multiplier calibration.',
  'D19':'The opening hypothesis invokes all of Assumption 5.1, including its separate signal and graph-dependence conditions.',
  'D14b':'The displayed factor d0/d uses the graphical-model null count defined in Section 5; its signal fraction rho also enters the invoked assumption.'},
 '6.3':{
  'D2':'The printed conclusions both contain FDP. Its rejection-count definition is retained; the second occurrence is not changed to FDR.',
  'D5':'The procedure in the statement is explicitly Algorithm 2.',
  'D20':'The generic estimator in the statement refers to the edgewise asymptotic linear representation introduced at the start of Section 6.',
  'D4d':'The theorem specifies the generic conditional multiplier quantiles (6.1), whose actual bootstrap statistic is subject to Assumption 6.1.',
  'D21':'The opening clause explicitly imposes Assumption 6.1, including both data and conditional multiplier approximation bounds and moment restrictions.',
  'D23':'The opening clause also imposes the complete scaling condition in Assumption 6.2.',
  'D14b':'The bound q*d0/d uses the same d0 convention that Assumption 6.2 explicitly imports from Section 5; that assumption also reuses rho.'}
}

def main():
    save_passages()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
        source_policy='Pinned arXiv:2108.09904v2. All five main-text Theorems and relevant source passages reviewed against the PDF; supplementary material excluded.',
        normalization_policy='Preserve printed wording, formulas, labels and source inconsistencies; expand macros and normalize line wrapping and typographic emphasis only.',
        semantic_ranking_policy='All five inventoried Theorems retained; direct demand counted once per theorem and interface, independently of proof use.',
        build_order_policy='Derive from the acyclic same-paper dependency graph; each model-specific member retains its own path.')
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
