"""Attach paper-local statement dependencies and derive the census."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
ASSUMPTIONS = {
'D11':'The reference I1 imposes consistency between the observed and potential outcomes.',
'D12':'The reference I2 imposes uniform positivity of the conditional treatment density.',
'D13':'The reference I3 imposes mean ignorability.',
'D14':'The reference D1 requires compact treatment support.',
'D15':'The reference D2 requires twice continuously differentiable effect and marginal-density functions.',
'D16':'The reference D3 requires bounded true nuisance functions.',
'D17':'The reference D4 imposes the original conditional-variance and continuity-set conditions.',
'D20':'The reference E(A).1 imposes the printed bandwidth condition.',
'D21':'The reference E(A).2 imposes convergence to nuisance limits with at least one correct limit.',
'D22':'The reference E(A).3 imposes kernel symmetry, continuity, support and covering conditions.',
'D23':'The reference E(A).4 imposes the mixed-norm product-rate condition.',
}
DIRECT = {
'3.1':dict(ASSUMPTIONS, **{
 'D24':'Theorem 3.1 explicitly requires E(B)_3, the nuisance-class condition at entropy order three.',
 'D25':'The distribution approximation is expressed with the Dudley metric d from (3.1).',
 'D27':'The statement explicitly uses sigma squared from (3.2) in the normal mean and variance.',
 'D26':'Formula (3.4) uses the second and fourth convolution products of K evaluated at zero.',
 'D3':'The mean and variance in (3.4) divide by the marginal treatment density varpi_0.',
 'D10':'The statement names T_n and cites (J.1); the matching main-text integrated statistic is displayed as (2.5).',
 'D6':'The null H_0 is the constant causal curve, displayed in (2.1) and described with the printed reference (M.4) before (2.5).'}),
'3.2':dict(ASSUMPTIONS, **{
 'D27':'The theorem explicitly names sigma squared from (3.2) and the normal quantile with parameters in (3.4).',
 'D26':'The referenced normal quantile uses b_0h and V from (3.4), which contain convolution values K^(2)(0) and K^(4)(0).',
 'D3':'The referenced normal parameters use varpi_0; the separate centering constraint prints varpi without a zero subscript, retained as a source notation issue.',
 'D10':'The rejection event uses T_n; its printed reference is (J.1), while the main-text statistic is (2.5).',
 'D6':'The alternative binds the causal curve theta_0 to a constant plus the stated local perturbation.',
 'D7':'The constant c_0 is defined as the population expectation of xi at the true nuisance functions.',
 'D4':'The constant c_0 uses the blackboard-P population integration notation from Section 2.1.'}),
'3.3':dict({k:'The inherited assumptions of Theorem 3.1 include this condition: '+v for k,v in ASSUMPTIONS.items()}, **{
 'D24':'Theorem 3.3 inherits E(B)_3 from Theorem 3.1; it does not explicitly add J4, despite the surrounding proof discussion.',
 'D6':'The inherited null setting is a constant causal effect curve.',
 'D25':'The conclusion measures conditional-law approximation using the Dudley metric d.',
 'D27':'The normal target uses V from Theorem 3.1, hence sigma squared from (3.2); b_h is retained as printed, without asserting a verified equality to b_0h.',
 'D26':'The target variance V from (3.4) contains the fourth convolution K^(4)(0).',
 'D3':'The inherited target variance V divides by the marginal treatment density varpi_0.',
 'D28':'The conclusion uses the conditional law L* given the original observations.',
 'D29':'The definition of T_n* explicitly points to the preceding paragraph, which specifies null-centered Rademacher residuals.'}),
'3.4':dict({k:'The inherited assumptions of Theorem 3.1 include this condition: '+v for k,v in ASSUMPTIONS.items()}, **{
 'D24':'Theorem 3.4 inherits E(B)_3 and its named nuisance classes from Theorem 3.1.',
 'D18':'The additional displayed assumption requires J4(1,F,L2) finite for both F_mu and F_pi.',
 'D6':'The inherited null setting is a constant causal effect curve.',
 'D25':'The conclusion measures conditional-law approximation using the Dudley metric d.',
 'D27':'The target uses V from (3.4), hence sigma squared from (3.2); the distinct printed mean symbol b_h remains unresolved.',
 'D26':'The target variance V contains the fourth convolution K^(4)(0).',
 'D3':'The target variance V uses the marginal treatment density varpi_0.',
 'D28':'The law L* is conditional on the full original sample.',
 'D30':'The preceding paragraph replaces null-centered residuals by xi-hat minus the fitted local linear curve; it retains the Rademacher resampling rule.'})
}
def extra(n):
    return [dict(page=17,location="Theorem 3.1 inherited assumptions and formula (3.4)")] if n != "3.1" else []

def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
      source_policy='Registered arXiv:2202.03369v2 PDF, 93 pages; pages 1-27 and the acknowledgements above Appendix A on page 28 only.',
      normalization_policy='Preserve all four original Theorems and source notation, including appendix-labelled references and distinct bootstrap residual rules. Record source issues separately.',
      semantic_ranking_policy='Resolve the original causal model, estimators, separately numbered assumptions and bootstrap procedures. Do not import proof-only fourth-order entropy into Theorem 3.3 or sample splitting into the main-text statistic.',
      build_order_policy='Derive edges and reach from paper-local dependencies without altering the independent inventory.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                evidence=list(c['evidence'])+extra(n)
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=evidence))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
            sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])+extra(n)
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
    finalized=json.loads((ROOT/'ranked-interfaces.json').read_text())
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=[m for x in finalized['interfaces'] for m in x['members']]),indent=2,ensure_ascii=False)+'\n')
    print('Census structurally valid; independent full source review remains pending.')
if __name__=='__main__':main()
