"""Derive all four theorem connections from their main-text definitions and hypotheses."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '3.2':{'D4':'The arbitrary family consists of intersection tests for all subsets of the hypothesis indices.','D6':'The first hypothesis explicitly requires each intersection test to have level alpha.','D8':'The closed decision is defined inline by the minimum over all intersections containing the individual index.','D3':'The first conclusion is strong familywise error control over all true hypotheses.','D5':'The second assertion adds online measurability for each intersection test.','D7':'The second assertion additionally requires the predictable-family property from Definition 3.1.','D2':'The conclusion of the second assertion is that the resulting decisions form an online procedure from Definition 2.1.'},
 '3.5':{'D2':'The input d is explicitly an online procedure, and the resulting closed procedure reproduces its adapted decisions.','D3':'The input procedure explicitly has strong familywise error control.','D4':'The maximum construction defines a test for every intersection hypothesis, retaining the standing empty-test convention.','D5':'The constructed family is asserted to consist of online intersection tests.','D6':'The constructed tests are asserted to have level alpha under their intersection nulls.','D7':'The constructed family is asserted to be predictable in the sense of Definition 3.1.','D8':'The equality d-phi=d uses the same closure operation defined in Theorem 3.2.'},
 '3.9':{'D7':'The family is expressly assumed predictable in the rejection-persistence sense.','D5':'Its members are expressly assumed to be online intersection tests.','D6':'Each member is explicitly required to have level alpha.','D9':'The theorem explicitly assumes the consonance property (2).','D8':'The first procedure compared is the all-intersections closure d-phi from Theorem 3.2.','D2':'The first procedure is described as online, and the equal shortcut has the same adapted decisions.'},
 '4.2':{'D13':'The threshold families are assumed predictable in the exact equality sense of Definition 4.1.','D12':'The family phi is explicitly the threshold-union construction in equation (3).','D6':'The theorem separately assumes that this constructed family consists of alpha-level intersection tests.','D9':'The theorem explicitly requires the consonance property.','D8':'The first of the three equivalent procedures is the closure d-phi.','D11':'The third procedure is the online alpha-adjustment using threshold alpha_i^{I_i}.','D10':'The recursion and final decision use the p-values p_j and p_i from the Section 4 setting.'}
}
inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
data['schema_version']='statistical-ranked-interfaces-v4'
data['scope'].update(paper_count=1,
 source_policy='Pinned arXiv:2211.11400v3, margin stamp 21 December 2023 and title-page date 22 December 2023. Main text ends on page 16, before the Appendix on page 17.',
 normalization_policy='Preserve all four original Theorems and the original definitions of procedures, FWER, intersection tests, closure, consonance and threshold families. Keep measurability conventions and distinct forms of predictability explicit.',
 semantic_ranking_policy='Only direct statement uses and recursive paper-local definition prerequisites; proofs, admissibility propositions and later spending-rule applications do not automatically add dependencies.',
 build_order_policy='Keep decision adaptedness separate from level control and future-extension predictability; keep threshold equality under future extensions separate from rejection persistence.')
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
