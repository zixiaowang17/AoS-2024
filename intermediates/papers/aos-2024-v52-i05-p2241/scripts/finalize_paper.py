"""Build source-local relationships, preserving clause-specific assumption scopes."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'3.1':[1,2,3,4,11],'3.4':[2,3,4,11],'4.2':[10,11,12,14],'4.4':[5,6,8,9,13,15,16,17],'4.7':[5,8,9,11,12,13,15,16,17,18],'4.9':[4,12,19],'5.3':[5,9,11,12,15,16,20,21],'5.5':[11,12,16,21],'6.1':[1,2,3,4,11],'6.2':[2,3,4,11],'6.7':[2,4,22,23]}
DIRECT={n:['D'+str(i) for i in v] for n,v in DIRECT_NUMS.items()}
EDGE_TEXT={
'D9':{'D5':'The maximal/maximum distinction is defined with respect to convex order, not the usual setwise order.'},
'D13':{'D12':'The law gamma in (4) uses the Radon–Nikodym derivatives dP_i/dQ, under the null-to-alternative absolute continuity (AC).'},
'D14':{'D1':'The optimization (3) requires the e-variable to have one common distribution under all nulls.','D2':'The optimization (3) ranges over exact e-variables and maximizes the log-expectation e-power.'},
'D15':{'D5':'Membership in M_gamma requires convex-order domination by gamma.','D8':'Membership in M_gamma requires probability one on the nonnegative diagonal I_L^+.','D13':'The upper measure in the definition of M_gamma is the law under Q of the null density-ratio vector (4).'},
'D16':{'D13':'Assumption (N) forbids mass on any hyperplane for the specific density-ratio law gamma from (4).'},
'D17':{'D7':'Proposition 4.3 requires the barycenters of the two complementary split measures to lie on the diagonal.','D8':'The split half-space excludes the whole positive diagonal and has boundary passing through x times the all-ones vector.'},
'D18':{'D5':'The constraint in (7) compares the repeated target density-ratio law with the original law in convex order.','D13':'The upper distribution in (7) is precisely gamma from (4), evaluated under Q.'},
'D20':{'D7':'The SHINE recursion splits at the current barycenter and places the child masses at their barycenters.','D8':'The child barycenters and output measures lie on the positive diagonal.','D13':'The initial unsplit measure in SHINE is gamma from (4).','D17':'Each SHINE step explicitly applies the split construction of Proposition 4.3 to every component.'},
'D21':{'D20':'The SHINE martingale couples the first-coordinate distributions of the recursive measures (11) using child-to-parent mass ratios (12).'}}
EDGE_TEXT['D23']={'D2':'The T6.7 passage strengthens the pointwise positive log e-power definition to a uniform positive infimum while retaining exactness and boundedness.','D4':'The T6.7 passage applies total-variation closures to linear span and convex hull, extending the finite notation without identifying either operation.'}
def direct_reason(n,lid):
    label='Theorem '+n
    if lid=='D1':return label+' refers to a pivotal random variable: its law is common to all null distributions. Exactness of an e-variable alone does not imply this property.'
    if lid=='D2':return label+(' requires exact bounded e-variables with a uniformly positive infimum of log e-power; this is stronger than the pointwise positive e-power definition.' if n=='6.7' else ' compares existence of e-variables, their expectation nontriviality and positive log e-power; exactness and boundedness are imposed only in the explicitly named clauses.')
    if lid=='D3':return label+' includes existence of a nontrivial p-variable, with validity at every threshold and improvement at some threshold for each alternative'+('; its exact-p clause additionally requires equality under every null.' if n in ['3.1','6.1'] else '.')
    if lid=='D4':return label+({'3.1':' uses Q outside the linear span of the finite null family.','3.4':' uses Q outside the convex hull of the finite null family.','4.9':' states separation of pure product laws from the span and hence convex hull of the product null family.','6.1':' compares the null span with the alternative convex hull; its pivotal-law clause also uses a convex hull of alternative laws.','6.2':' compares the two convex hulls, without printed closure bars; the additional infinite-family clause and its source limitation are recorded separately.','6.7':' uses total-variation closures of span and convex hull, with an additional outer closure of their sum; these extend the finite-set notation and are preserved in D23.'}[n])
    if lid=='D5':return label+' explicitly uses convex order between measures'+('; its separate monotonicity condition on mu_x instead uses the usual setwise order.' if n=='4.4' else '.')
    if lid=='D6':return 'Theorem 4.4(b) requires mu_x ≤ mu_y for x ≤ y in the usual order: inequality on every Borel set, not convex order.'
    if lid=='D8':return label+' specifies support on the positive diagonal I^+, which includes the zero vector.'
    if lid=='D9':return label+(' guarantees a maximal limit under (N), and convergence to a maximum only if one exists; those are different notions.' if n=='5.3' else ' asserts a unique maximum in convex order, which dominates all feasible measures, rather than merely an undominated maximal measure.')
    if lid=='D10':return 'Theorem 4.2 explicitly requires Y in the simultaneous transport-map set T((P_1,...,P_L,Q),(F,...,F,G)); one map transports all nulls to F and the alternative to G.'
    if lid=='D11':return label+(' inherits the joint atomlessness assumption (JA) through its reference to the conditions of Theorem 5.3.' if n=='5.5' else ' assumes (JA), applying Definition 2.2 to the combined null/alternative tuple.')+(' Its final (c)–(e) equivalence explicitly removes (JA).' if n=='6.1' else ' Its final (c)–(d) equivalence explicitly removes (JA).' if n=='6.2' else '')
    if lid=='D12':return label+(' imposes (AC) only in the additional linearly-independent refinement yielding k=1 or 2; the initial finite-k claim does not require it.' if n=='4.9' else ' inherits (AC) from Theorem 5.3, in the direction P_i absolutely continuous with respect to Q.' if n=='5.5' else ' explicitly assumes (AC): every null P_i is absolutely continuous with respect to the simple alternative Q.')
    if lid=='D13':return label+' explicitly uses gamma, the law under Q of the vector (dP_1/dQ,...,dP_L/dQ) from (4), not the vector itself.'
    if lid=='D14':return 'Theorem 4.2 states existence of a maximizer to (3), whose feasible variables are both pivotal and exact and whose objective is E_Q[log X].'
    if lid=='D15':return label+' refers to M_gamma from (8): diagonal-supported probability measures below gamma in convex order.'
    if lid=='D16':return label+(' adds (N) only for its almost-sure convergence/maximality clause, not the preceding convex-order progress claim.' if n=='5.3' else ' invokes the conditions of Theorem 5.3 for the convergent construction; the preceding context selects its (N) branch. The source does not repeat that assumption separately.' if n=='5.5' else ' assumes (N), which prohibits mass on any affine hyperplane under gamma; it is stronger than atomlessness.')
    if lid=='D17':return label+' names mu_x from Proposition 4.3'+(' in its usual-order monotonicity criterion.' if n=='4.4' else ' in the formula mu([0,x]^2)=mu_x(R^2), with L=2.')+' The source defines the closed half-space, its closed complement and both split measures.'
    if lid=='D18':return 'Theorem 4.7 concludes that distinct F,G attain (7), with the repeated law of dF/dG under G equal to the maximum diagonal measure mu.'
    if lid=='D19':return 'Theorem 4.9 uses P^k={P_1^k,...,P_L^k} and Q^k from the iid product experiment. Its conclusion concerns span separation of measures; the e-variable motivation supplies no additional theorem premise.'
    if lid=='D20':return 'Theorem 5.3 names the SHINE construction and its outputs mu^(s), defined by the repeated splitting and barycenter aggregation in (11).'
    if lid=='D21':return label+(' describes its limit as almost-sure convergence; the preceding construction gives that meaning through the explicitly coupled first-coordinate SHINE martingale (12).' if n=='5.3' else ' explicitly names the SHINE martingale X_k from (12) and defines EP_k=E_Q[-log X_k]. X_k is the reciprocal-coordinate process, not the e-variable itself.')
    if lid=='D22':return 'Theorem 6.7 requires one probability measure R to dominate every null and alternative; it does not assume the simple-alternative domination (AC).'
    if lid=='D23':return 'Theorem 6.7 uses a uniformly positive infimum over all alternatives and total-variation closures; the additional disjoint-closed-sets criterion is conditional on tightness of Q.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All eleven main-text Theorems retained, including every equivalence clause and assumption exception.',build_order_policy='Preserve exactness versus pivotality, convex versus setwise order, maximal versus maximum, conditional JA/AC/N scopes, pure product laws, and pointwise versus uniform log e-power.')
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
