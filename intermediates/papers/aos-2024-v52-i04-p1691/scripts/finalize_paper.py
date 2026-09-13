"""Build theorem demand from the reviewed paper-local source graph."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
'3.1':{
'D1':'Theorem 3.1 explicitly assumes finite first moments of signal and error laws.',
'D2':'The projected densities f_Y,v and f_0Y,v in (3.5) use the unit-direction image measures.',
'D3':'Both branches compare the signal and observation laws using W1.',
'D4':'The single-coordinate error law is required to satisfy Assumption 3.1.',
'D5':'Only the additional-regularity branch assumes Assumption 3.2 for the true signal law.',
'D6':'Only that additional branch requires a kernel K as in condition (a).',
'D7':'The additional branch bounds the projected CDF bias in (3.6).',
'D9':'The statement defines mu_Y and mu_0Y by convolution with the common product error law.'},
'4.1':{
'D1':'Theorem 4.1 imposes finite (4+delta)-moments and an observation-law moment sieve.',
'D3':'Both posterior conclusions concern W1 distance from the true signal law.',
'D4':'The single-coordinate error distribution explicitly satisfies Assumption 3.1.',
'D5':'The second branch adds Assumption 3.2 on the true mixing distribution.',
'D6':'The second branch explicitly selects a kernel as in (a).',
'D7':'The second branch uniformly bounds b_FX,v(h_n) for every signal law in the sieve.',
'D11':'The theorem explicitly assumes the moment sieve and three prior conditions displayed in (4.1).',
'D12':'The conclusions use the posterior Pi_n conditional on the observed sample.'},
'4.2':{
'D8':'Theorem 4.2 specifies the standard Laplace error density.',
'D9':'Its iid observations have convolution density f_0Y=f_epsilon*f_0X.',
'D11':'It explicitly concludes that the conditions in (4.1) hold at the stated rate.',
'D12':'Its conclusion is an induced observation-law posterior probability for L1 density error.',
'D15':'The prior is induced by the product Dirichlet and scale law for the normal-mixture model.',
'D16':'The base measure H0 is required to verify Assumption 4.1.',
'D17':'The scale prior Pi_sigma is required to verify Assumption 4.2.',
'D18':'The true mixing density explicitly satisfies Assumption 4.3.'},
'4.3':{
'D3':'Theorem 4.3 controls posterior W1 error for the signal law.',
'D8':'The sampling density uses standard Laplace errors.',
'D9':'The data are iid from f_0Y=f_epsilon*f_0X.',
'D12':'The displayed limit concerns the posterior signal law conditional on the sample.',
'D15':'The stated product prior induces the Dirichlet normal-mixture signal model.',
'D16':'Theorem 4.3 imposes Assumption 4.1 with the stronger restriction iota>1.',
'D17':'It imposes Assumption 4.2 with the stronger restriction varpi>1.',
'D18':'It explicitly assumes the global univariate mixing-density tail bound in Assumption 4.3.'},
'4.4':{
'D8':'Theorem 4.4 specifies standard Laplace errors.',
'D9':'The observations are iid from the stated convolution density.',
'D11':'The theorem asserts that the three prior conditions in (4.1) hold at its adaptive density rate.',
'D12':'The posterior conclusion measures observation-density L1 error.',
'D15':'The same product Dirichlet and scale prior induces the normal-mixture model.',
'D16':'The base measure explicitly verifies Assumption 4.1.',
'D17':'The scale prior explicitly verifies Assumption 4.2.',
'D18':'The list Assumptions 4.3–4.5 includes the global exponential tail bound.',
'D19':'That list includes the two exponential-tilt Sobolev condition in Assumption 4.4.',
'D20':'That list includes the Holder-envelope and weighted ratio condition in Assumption 4.5.'},
'4.5':{
'D3':'Theorem 4.5 gives a W1 posterior contraction rate for the signal law.',
'D8':'Its inherited assumptions on f_0Y from Theorem 4.4 include standard Laplace errors.',
'D9':'The inherited sampling density and observations use the iid convolution model of Theorem 4.4.',
'D12':'The displayed probability is the posterior signal law conditional on the sample.',
'D15':'The phrase same prior retains the product Dirichlet and Gaussian-scale mixture prior.',
'D16':'The same prior is strengthened to iota>1 in Assumption 4.1.',
'D17':'It is also strengthened to varpi>1 in Assumption 4.2.',
'D18':'The inherited assumptions on f_0Y retain Assumption 4.3 for the mixing density.',
'D19':'The inherited assumptions retain Assumption 4.4, with alpha governing the displayed rate.',
'D20':'The inherited assumptions retain Assumption 4.5; no additional general-theorem assumption is imported.'},
'5.1':{
'D1':'Theorem 5.1 defines its parameter class using the bounded first-moment class P1(R^d,M).',
'D3':'Its minimax expected loss is W1 between an arbitrary estimator and the candidate signal law.',
'D9':'The expectation is under the n-fold sampling law formed by product-error convolution.',
'D21':'The parameter class intersects the moment class with the isotropic Sobolev ball S_d(alpha,L).',
'D32':'Hypothesis (5.1) explicitly bounds derivatives through order two of the error Fourier transform, rather than reciprocal derivatives.'},
'5.2':{
'D3':'Theorem 5.2 bounds W1 error of the probability-valued estimator.',
'D8':'The statement specifies the standard Laplace density, with beta=2 in the preceding bandwidth formula.',
'D9':'The estimator uses the standing iid convolution observations described in Sections 1–2 and Section 5.2.',
'D24':'The estimator mu-tilde_1n is the approximate minimizer defined immediately before Theorem 5.2.',
'D28':'The statement itself imposes the exponential tail condition (5.2), only for sufficiently large norm.'}}
EDGES={
'D2':{'D1':'The image-measure passage restricts its input to a finite-p-moment law and retains the projected moment bound.'},
'D3':{'D1':'The Wasserstein definition requires finite pth moments.','D25':'Its infimum ranges over couplings with the two prescribed marginals.'},
'D4':{'D1':'Assumption 3.1 includes the first-moment requirement on the error law.','D29':'Its two bounds concern the reciprocal transform and its first derivative.'},
'D5':{'D1':'Assumption 3.2 includes finite first moment of the true signal law.','D2':'Both regularity bounds range over its unit-direction projections.','D32':'The weighted transform and fractional derivative use the Fourier convention in Section 2.'},
'D6':{'D32':'The kernel restriction is stated through its Fourier transform and Fourier support.'},
'D7':{'D2':'The multivariate bias uses the projected law and its CDF; signed kernel projection is an explicit source convention.'},
'D8':{'D32':'The Laplace law is identified here by its source-normalized Fourier transform.'},
'D10':{'D26':'The KL-neighborhood restriction includes the source KL divergence.'},
'D11':{'D1':'The sieve is restricted by an observation-law moment bound.','D9':'Its entropy is for the induced convolution family F(P_n).','D10':'Its prior lower-mass condition is on the KL neighborhood.','D27':'Its entropy condition uses the packing number D.'},
'D12':{'D9':'The posterior likelihood uses densities of the observation convolution family.'},
'D15':{'D14':'The mixing law is sampled from the named Dirichlet process.','D31':'The signal density convolves that law with the Gaussian scale kernel.','D9':'Its observation law is the convolution of that signal density with the error.','D8':'The section and product-prior specification fix the standard Laplace error density.'},
'D19':{'D32':'Assumption 4.4 uses the Fourier transform of both exponentially tilted densities.'},
'D21':{'D32':'The Sobolev class is defined by weighted square integrals of the Fourier transform.'},
'D22':{'D32':'The source specifies the Fourier transform of tau and derivatives of that transform.'},
'D23':{'D29':'The deconvolution integral multiplies by the product reciprocal error transform.','D22':'Its kernel is K=hat(tau) from the source cutoff passage.'},
'D24':{'D1':'Comparison laws are explicitly restricted to P1(R^d).','D2':'The comparison integrates CDF differences for each unit-direction projected law.','D23':'The signed target CDF comes from the raw Fourier deconvolution estimator.'},
'D27':{'D30':'The source packing metric may be the separately defined Hellinger distance; L1 is ambient.'},
'D29':{'D32':'The reciprocal is formed from the error Fourier transform using the same source convention.'}}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,source_policy='Registered local arXiv:2309.15300v1; main-text pages 1–29 only.',
        normalization_policy='Preserve all eight original statements and stable IDs; record source scope and notation issues separately.',
        semantic_ranking_policy='Use paper-local statement dependencies, keeping conditional branches, source kinds and distinct tail conditions separate. Retired D13 is auxiliary context, not an interface.',
        build_order_policy='Derive canonical edges and theorem reach from reviewed local dependencies without changing the inventory.')
    data['interfaces']=copy.deepcopy(interfaces);claim_by_id={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGES.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split(':theorem-')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            for m in x['members']:
                lid=m['local_id']
                if lid in DIRECT[n]:
                    ev=copy.deepcopy(c['evidence'])+copy.deepcopy(m['evidence'])
                    if n=='4.5':ev.append(dict(page=17,location='Theorem 4.4 — inherited assumptions'))
                    if n=='5.2':ev.append(dict(page=5,location='Section 2 — standing iid convolution setup'))
                    x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],
                        use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=ev))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];n=cid.split(':theorem-')[-1];path=r['via_local_ids']
            text=[DIRECT[n][path[0]]]+[EDGES[a][b] for a,b in zip(path,path[1:])]
            ev=copy.deepcopy(claim_by_id[cid]['evidence'])
            if n=='4.5':ev.append(dict(page=17,location='Theorem 4.4 — inherited assumptions'))
            for lid in path:
                ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=' '.join(text),evidence=ev)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
            linked=own+' '+' '.join(claim_by_id[r['claim_id']]['statement_original'] for r in x['related_theorems'])
            selectors=m.get('highlight_symbols',[])+m.get('highlight_phrases',[])
            assert any(s in own for s in selectors),(m['local_id'],'no source match')
            assert all(s in linked for s in selectors),(m['local_id'],'unmatched selector')
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    print('Census structure validated; independent full source review remains separate.')
if __name__=='__main__':main()
