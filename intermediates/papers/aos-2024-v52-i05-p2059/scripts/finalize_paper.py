"""Build the census while preserving generic substitution and concrete CI construction scopes."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'3.3':[1,2,3,5,6],'4.4':[1,2,9,11]}
DIRECT={n:['D'+str(i) for i in ids] for n,ids in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'Assumption 1.1 concerns the error vector of model (1).'},
'D3':{'D1':'The row-permutation convention identifies x and Z from the model features.'},
'D4':{'D3':'The column-space projection notation uses the original and row-permuted design matrices.'},
'D5':{'D3':'Condition 3.1 uses the row action on epsilon, permutation inverses and composition recorded with D3 and A1-A2.'},
'D6':{'D1':'The p-value recipe identifies the model coefficient null H0: beta=0; its paired inputs are supplied separately.'},
'D7':{'D3':'Equation (3) uses x_pi and Z_pi from the row-permutation convention.','D4':'Both residual norms in (3) use the specified column-space projections.'},
'D8':{'D6':'The inversion function f(beta) uses the same comparison weights and the (1+sum)/(B+1) recipe.','D7':'Its beta-dependent pair replaces y by y-x beta in the concrete residual statistics (3). The printed Algorithm 2 reference is a recorded discrepancy.'},
'D9':{'D8':'Corollary 4.1 defines the interval endpoints from the strict superlevel set of the inversion function f(beta).'},
'D10':{'D3':'The endpoints s_b,u_b and set A1 come from the row-permuted coefficients in A4-A5.','D4':'Those coefficients and roots use the projection formulas retained in Lemma 4.3, A4.','D8':'The reduced function f_A1 is defined in A5 as a sum of the beta-dependent comparison weights from D8; the printed counting identity is separately preserved in A6.'},
'D11':{'D3':'Algorithm 2 requests coefficients from Lemma 4.3, which use row-permuted feature arrays.','D4':'Those coefficients are formed from the original projection formulas retained in A4.','D10':'Algorithm 2 consumes the ordered critical values, multiplicities and recurrence (7), with threshold gamma from A5.'}}
def direct_reason(n,lid):
    if lid=='D1':return ('Theorem 3.3 refers to H0 and the model parameters x,Z,epsilon, retained in the linear model (1).' if n=='3.3' else 'Theorem 4.4 covers the model coefficient beta using Algorithm 2 on the linear-model observations y,x,Z.')
    if lid=='D2':return ('The Section 3 opener A3 states exchangeable noise for the general guarantee; this is standing Assumption 1.1, although the theorem does not repeat it.' if n=='3.3' else 'The confidence coverage assertion is in the same linear-model setting under standing Assumption 1.1 on exchangeable errors; no Gaussian or iid-error premise is added.')
    if lid=='D3':return 'Theorem 3.3 explicitly samples permutations of [n] and evaluates its function at the identity pi_0; the row action and identity are retained in D3 and A1.'
    if lid=='D5':return 'Theorem 3.3 explicitly requires Condition 3.1, the universal transfer of a noise permutation to right-composition by its inverse in both statistic arguments.'
    if lid=='D6':return 'Theorem 3.3 substitutes its own paired T evaluations into Algorithm 1. Its p_val therefore uses the half-tie comparison and (1+sum)/(B+1) recipe, without inheriting the PALMRT residual-statistic construction.'
    if lid=='D9':return 'Theorem 4.4 names CI_alpha defined in Lemma 4.1; the actual interval definition is printed as Corollary 4.1, retained in D9 with its infimum and supremum of f(beta)>alpha.'
    if lid=='D11':return 'Theorem 4.4 explicitly concerns the interval constructed by Algorithm 2. All instructions and supporting formulas are retained, including the source discrepancies; this census does not certify their correctness.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Both complete main-text Theorems; retain generic statistic substitution separately from concrete PALMRT and its interval construction.',build_order_policy='Same-paper source dependencies with explicit expansion of auxiliary coefficient, root and threshold formulas; proof-only citations do not supply statement edges.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGE_TEXT.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=DIRECT[n]
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                ev=copy.deepcopy(c['evidence'])+copy.deepcopy(members[lid]['evidence'])
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=direct_reason(n,lid),evidence=ev))
    edges=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=edges[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for rel in x['related_theorems']:
            cid=rel['claim_id'];n=cid.split('/T')[-1];path=rel['via_local_ids']
            reason=' '.join([direct_reason(n,path[0])]+[EDGE_TEXT[a][b] for a,b in zip(path,path[1:])])
            ev=copy.deepcopy(claims[cid]['evidence'])
            for lid in path:ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=reason,evidence=ev)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label'];linked=own+' '+' '.join(claims[r['claim_id']]['statement_original'] for r in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors) and all(s in linked for s in selectors),(m['local_id'],[s for s in selectors if s not in linked])
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Census structurally validated; independent source review remains pending.')
if __name__=='__main__':main()
