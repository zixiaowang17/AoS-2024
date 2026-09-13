"""Build the census while preserving all labeled theorem occurrences and their exact source definitions."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'4.1-overview':[4,5,6],'5.8-overview':[4,5,10],'5.1-overview':[1,2,4,8,9],'3.1':[1,2,4,5,11,12,13],'4.1':[1,2,4,5,17,18],'5.1':[1,2,4,8,9],'5.4':[1,2,4,5,8,9,11,13,19,21,22,23],'5.7':[1,2,4,5,8,9,19,21],'5.8':[1,2,4,5,8,9,19,21]}
DIRECT={n:['D'+str(i) for i in ids] for n,ids in DIRECT_NUMS.items()}
EDGE_TEXT={
'D2':{'D1':'The source pushforward convention specifies a torus map in H_K^(beta+1).'},
'D4':{'D1':'The IPM takes the supremum over the unit Holder ball H_1^gamma.'},
'D5':{'D1':'Equation (1.3) specifies Holder-bounded generator and discriminator classes.','D2':'Its resulting measure estimator is the uniform-latent pushforward ghat_#U.'},
'D6':{'D1':'Model 1 requires the target map to lie in H_K^(beta+1).','D2':'Its target distribution is gstar_#U from the uniform latent cube/torus.'},
'D8':{'D1':'Definition 2.1 opens with a map in H_K^(beta+1).','D7':'Part (i) requires image reach strictly greater than K^{-1}, under the projection-based reach definition.'},
'D9':{'D1':'Part (ii) shares Definition 2.1 opening Holder-map binder and lower-bounds its differential singular values.'},
'D10':{'D1':'Model 3 starts with a Holder map g-star.','D2':'The target equals its uniform-latent pushforward.','D8':'Model 3 imposes K-manifold regularity, including injectivity and reach.','D9':'Model 3 separately imposes the K-density lower singular-value condition.'},
'D11':{'D2':'Delta_G compares uniform-latent pushforward laws for candidate and target maps.','D4':'Its approximation cost is d_H_1^gamma.'},
'D12':{'D2':'Delta_D compares candidate and target uniform-latent pushforwards.','D3':'The second discrepancy in (3.2) is the arbitrary-class d_D from (1.1).','D4':'The reference discrepancy in (3.2) is the Holder IPM.'},
'D14':{'D1':'The scaling and wavelet functions are assumed to lie in H^(floor(beta)+3).'},
'D15':{'D14':'The Besov norm is defined from the specified wavelet coefficients and basis.'},
'D16':{'D1':'The approximation precision uses a Holder norm and C_eta compares the Holder and Besov norms.','D14':'The class is a finite expansion in neural approximations of the periodized wavelets; the exact hat-wavelet implementation is appendix-only.','D15':'Its C_eta constant is fixed through the Holder-to-Besov norm inequality and the class approximates a Besov truncation.'},
'D17':{'D16':'Equation (4.1) instantiates the periodic neural class at eta=beta+1, resolution n^(-1/(2beta+d)) and precision L^{-1}=n^{-1}.'},
'D18':{'D1':'The selected pairwise discriminator maximizes over H_1^gamma.','D2':'The pairwise comparisons are between generator pushforwards, with the printed U/u mismatch retained.','D13':'The pairwise generator indices come from a minimal 1/n-cover.','D17':'The cover is of the Model-1 generator class fixed in (4.1).'},
'D19':{'D16':'The manifold generator class restricts the periodic neural class at the stated resolution; its numerical constraint is defined only in the appendix.'},
'D20':{'D1':'The inherited approximation precision and C_eta convention use Holder regularity.','D14':'The nonperiodic expansion uses the tensor-product Daubechies wavelet convention, with hat functions referred to the appendix.','D15':'C_eta and the target low-frequency comparison class use the inherited Besov norm convention.'},
'D21':{'D20':'Equation (5.3) instantiates the nonperiodic neural class at capped regularity tilde-beta+1 and its specified resolution.'},
'D22':{'D13':'For each fixed generator, the composed discriminator class uses the supremum-norm covering convention (3.3).','D19':'The supremum ranges over the manifold generator class (5.1).','D21':'The composed discriminators belong to the class (5.3).'},
'D23':{'D2':'The candidate discrepancy evaluates discriminators on the candidate and target pushforwards.','D15':'D_g-star is optimal in a radius-C Besov ball and its approximation minimizes a B^0 norm.','D19':'The candidate g ranges over the current manifold generator class.','D21':'The approximation Dbar_g is chosen from the current capped network discriminator class.'}}
def direct_reason(n,lid):
    label='Theorem '+n.replace('-overview',' (overview)')
    if lid=='D1':return label+' explicitly uses the Holder class H_K^(beta+1) for its maps or H_1^gamma for its discriminator domain; D1 retains the original norm and integer-smoothness convention.'
    if lid=='D2':return label+' writes candidate/target laws as g_#U, gstar_#U or ghat_#U, meaning pushforwards of the uniform latent variable on the torus representatives.'
    if lid=='D4':return label+' measures discrepancy with d_H_1^gamma (or its beta+1/tilde-beta+1 instance), defined in (2.1) through the unit Holder-ball supremum.'
    if lid=='D5':return label+' explicitly names the GAN estimator (1.3), which optimizes the paired empirical discriminator objective over its supplied generator/discriminator classes.'
    if lid=='D6':return 'The overview of Theorem 4.1 explicitly assumes Model 1, allowing any H_K^(beta+1) torus pushforward without manifold or lower singular-value conditions.'
    if lid=='D8':return label+' invokes the K-manifold regularity condition from Definition 2.1(i): injectivity and image manifold with reach greater than K^{-1}.'
    if lid=='D9':return label+' invokes the K-density regularity condition from Definition 2.1(ii). '+('The overview imposes it on both g and g-star.' if n=='5.1-overview' else 'The formal interpolation theorem imposes it only on g-star.' if n=='5.1' else 'Here it is a hypothesis on the target map g-star, not a density condition added to every fitted generator.')
    if lid=='D10':return 'The overview of Theorem 5.8 explicitly assumes Model 3, combining the smooth torus pushforward with the two distinct regularity conditions.'
    if lid=='D11':return label+' subtracts Delta_G, the best generator approximation error (3.1), at '+('the current capped tilde-beta+1 IPM regularity.' if n=='5.4' else 'the stated gamma IPM regularity.')
    if lid=='D12':return 'Theorem 3.1 subtracts Delta_D from (3.2), the supremum over candidate generators of the difference between the Holder and class-D discrepancies.'
    if lid=='D13':return label+' uses 1/n covering cardinalities, interpreted through the minimal supremum-norm cover in (3.3).'
    if lid=='D17':return 'Theorem 4.1 explicitly specifies G by (4.1), including the periodic neural wavelet class, n-dependent cutoff and L^{-1}=n^{-1} precision.'
    if lid=='D18':return 'Theorem 4.1 explicitly specifies D by (4.2), selected Holder-optimal discriminators between pairs of generators in the 1/n net. The source describes this class as not computable in practice.'
    if lid=='D19':return label+' explicitly specifies G by (5.1), retaining the neural generator class and appendix-defined chi-numerical regularity constraint; its exact appendix formula is not supplied by this census.'
    if lid=='D21':return label+' explicitly specifies D by (5.3), with tilde-beta+1=min(beta+1,d/2) and tilde-delta_n from (5.2). The printed low-dimensional denominator issue is recorded separately.'
    if lid=='D22':return 'Theorem 5.4 uses |(D_G)_{1/n}|, the supremum over g of the covering number of {D composed with g}; it is not a covering of the union over generators.'
    if lid=='D23':return 'Theorem 5.4 subtracts E[Delta_D^ghat], the candidate-specific discrepancy defined using D_g-star and its B^0 approximation Dbar_g, evaluated at the random fitted generator.'
    raise ValueError((n,lid))
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Six formal main-text Theorems and three separately labeled overview statements; distinct occurrences preserve different ranges and assumptions.',build_order_policy='Same-paper theorem and definition dependencies, distinguishing arbitrary classes from later specified network classes and uniform from candidate-specific approximation errors. Appendix-only construction details remain explicit unresolved references.')
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
