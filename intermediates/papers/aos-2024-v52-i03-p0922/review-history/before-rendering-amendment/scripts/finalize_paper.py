"""Derive all eight theorem connections from their main-text definitions and hypotheses."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={}
BASE={'D2':'The homogeneous iid experiment in Section 1 supplies the sampling law for this theorem.','D3':'The identification conditions (a)–(d) in Section 2.1 are stated to hold for the entire paper.'}
A={f'D{k+4}':f'The theorem requires Assumption {k}, whose full statement is retained separately.' for k in range(1,6)}
for n in ['3.1','3.3','3.4']:
    DIRECT[n]={**BASE,**A}
    if n=='3.1': DIRECT[n]['D11']='The normalized estimator in (9) is the averaged SMSE defined in (6).'
    else: DIRECT[n]['D13']='The estimated coefficient is the multiround update from Algorithm 1; its initial error is a hypothesis, not a fixed local fitting method.'
    if n=='3.4':
        for k in A:DIRECT[n][k]='Theorem 3.4 explicitly inherits the assumptions of Theorem 3.3, including '+A[k].split('requires ')[1]
for n,last in [('4.1','D20'),('4.2','D21')]:
    DIRECT[n]={'D14':'This theorem is stated under Section 4.1 covariate shift, with common coefficient and machine-specific laws and local sample sizes.','D3':BASE['D3'],'D5':'The theorem explicitly requires Assumption 1 on the integrated kernel.','D9':'The theorem explicitly requires Assumption 5 on covariate exponential moments.'}
    for lid,num in [('D15',6),('D16',7),('D17',8),('D18',9)]:DIRECT[n][lid]=f'The theorem explicitly requires Assumption {num}, in its machine-indexed form.'
    DIRECT[n][last]='The displayed estimate is '+('the weighted average of local SMSEs in (16).' if n=='4.1' else 'the weighted Newton update (18), using derivatives of local objectives.')
DIRECT['4.3']={'D22':'Section 4.2 changes the model to coefficient shift and targets beta-star_1, with (1-epsilon)L target-equal machines.','D3':BASE['D3'],**{k:'The reference to Theorem 3.3 retains '+v.split('requires ')[1]+' Section 4.2 supplies the active coefficient-shift setting.' for k,v in A.items()},'D23':'The rate concerns beta-hat_1^(t) produced by Algorithm 2, including selection and complementary-sample updates.'}
for n in ['5.1','5.2']:
    DIRECT[n]={**BASE,**{k:v for k,v in A.items() if k!='D9'},'D24':'The parameter has s nonzero coordinates by the standing sparse-model convention in Section 5.','D25':'The estimated coefficient is the constrained l1 minimizer (26) in Algorithm 3, with a global gradient and a single-machine Hessian.'}
    if n=='5.2':
        for k in ['D5','D6','D7','D8']:DIRECT[n][k]='Theorem 5.2 inherits the assumptions of Theorem 5.1, which requires '+A[k].split('requires ')[1]
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned arXiv:2210.08393v4, 102 pages, stamped 15 August 2024. Main text and references occupy pages 1–40; all appendix mathematics is excluded.',
     normalization_policy='Preserve all eight complete printed Theorems and source passages, including interrupted continuations, barred quantities, strict eigenvalue inequalities, and differing rate logarithms.',
     semantic_ranking_policy='Use direct statement requirements and recursive same-paper definitions only. Preserve inherited hypotheses via source excerpts, while keeping unnamed constants and appendix-only tuning outside ranked APIs.',
     build_order_policy='Keep homogeneous sampling, unequal-batch covariate shift, coefficient shift and sparse updates distinct. Regularity assumptions are separate from computational definitions; sparse and weighted updates must not inherit the dense Newton inverse algorithm.')
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
