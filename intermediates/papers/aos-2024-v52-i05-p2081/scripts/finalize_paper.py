"""Build the census while preserving prior alternatives and deterministic approximation scope."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT_NUMS={'3.1':[1,3,6,9,11,12,13,14,15,16,17,18],'3.4':[2,3,6,7,8,9,19]}
DIRECT={n:['D'+str(i) for i in ids] for n,ids in DIRECT_NUMS.items()}
EDGE_TEXT={
'D4':{'D3':'Definition 2.1 uses the weighted order <k,alpha> and scalar beta from (1).'},
'D5':{'D4':'Remark 1 defines isotropic regularity as the equal-coordinate specialization of Definition 2.1.'},
'D6':{'D5':'The charts have uniform isotropic regularity (3), retained in A3, with the coordinatewise map convention A11.'},
'D7':{'D2':'The extended chart is restricted to the tau/2-offset.','D5':'The normal-isometry field and the extended chart have the isotropic regularities stated in (4).','D6':'The offset chart is built over the original Psi_x0 and its tangent-domain V_x0.'},
'D8':{'D7':'The rescaled chart is the offset chart with only its normal argument multiplied by delta.'},
'D9':{'D2':'Definition 2.2 requires support in the delta-offset.','D3':'Its tangent/normal regularity vector is normalized by (5), the specialization retained in A1.','D4':'The normalized chart pullbacks must belong to the anisotropic class of Definition 2.1.','D8':'The pullbacks and local envelopes are composed with the rescaled offset chart.'},
'D11':{'D10':'The mixture (7) integrates the normalized Gaussian density with covariance O^T Lambda O.'},
'D14':{'D10':'Partial mixtures integrate Gaussian densities with shared eigenvalues and component-specific orientations.','D12':'In the DPM alternative, P over location and orientation has the Dirichlet-process construction.','D13':'In the MFM alternative, P instead has finitely many random atoms and Dirichlet weights.'},
'D15':{'D11':'Hybrid densities use the full mixture (7) with component-specific eigenvalue atoms.','D12':'Conditionally on Q2, the DPM alternative uses its product base measure.','D13':'Conditionally on Q2, the MFM alternative uses the same product base with the finite-mixture law.'},
'D17':{'D14':'Condition (11) constrains the shared eigenvalue vector of the partial-mixture branch, not the hybrid random base.'},
'D18':{'D15':'Conditions (12)-(13) constrain the random eigenvalue base Q2 and its law in the hybrid construction.','D16':'The hybrid paragraph explicitly requires H1 to satisfy the location-orientation density bounds (10).'},
'D19':{'D2':'The operator integrates over the tau-offset.','D3':'Its covariance uses alpha_0 and alpha_perp through Delta_(sigma,delta), retained in A7.','D6':'The tangent/normal frame in A7 is taken at the nearest manifold projection, in the standing reach-controlled geometry.','D10':'Its kernel at location y is the Gaussian with covariance Sigma(y).'}}
def direct_reason(n,lid):
    reasons={
    'D1':'The posterior event in Theorem 3.1 is measured with d_H, the unscaled Hellinger distance from Section 1.4.',
    'D2':'Theorem 3.4 uses the indicator and packing region M^tau, the source offset notation.',
    'D3':'The theorem uses beta, alpha_0 and alpha_perp from (5); A1 retains this tangent/normal specialization of the effective-smoothness definition (1).',
    'D6':'The regularity and reach setting is given by the charts Psi_x0 and equation (3), with the main-result conditions in A3-A4. Theorem 3.4 explicitly cites (3); Theorem 3.1 uses the standing geometry of Section 3.1.',
    'D7':'Theorem 3.4 explicitly uses the inverse offset chart bar-Psi_xj in z_(j,x). The main text only defines local inverses; the locality and packing-center issues are retained.',
    'D8':'Theorem 3.4 differentiates the normalized pullback of chi_j f0, whose normal rescaling is defined by bar-Psi_(x0,delta) in Section 2.2.',
    'D9':'The original assumptions (14)-(15), fully retained in A5, require the manifold-anisotropic class from Definition 2.2 and its normalized pullback derivatives. Theorem 3.4 also names the class explicitly.',
    'D11':'Theorem 3.1 uses f_P, the Gaussian location-scale mixture (7); the partial branch uses its shared-eigenvalue specialization (8).',
    'D12':'Theorem 3.1 explicitly allows the Dirichlet process mixture as one weight-prior alternative. This does not require the MFM law at the same time.',
    'D13':'Theorem 3.1 explicitly allows the mixture of finite mixtures as the other weight-prior alternative. Table 1 additionally imposes the count-law condition (9), retained in A6, only for this alternative.',
    'D14':'Theorem 3.1 permits the partial location-scale mixture, whose eigenvalues are shared across components. The hybrid construction is an alternative.',
    'D15':'Theorem 3.1 also permits the hybrid location-scale mixture, with random eigenvalue base Q2. It is not an additional requirement on the partial mixture.',
    'D16':'Table 1, explicitly referenced by Theorem 3.1, requires the base-measure density bounds (10) for either weight family and either scale family.',
    'D17':'For the partial-scale alternative of Theorem 3.1, Table 1 requires condition (11), including the polynomial upper-eigenvalue tail. It does not apply to the hybrid alternative.',
    'D18':'For the hybrid-scale alternative of Theorem 3.1, Table 1 requires (12)-(13), including random-base small-ball mass and exponential expected tails. It does not import the partial condition (11).',
    'D19':'Theorem 3.4 approximates f0 by K_Sigma g. Section 3.2 defines this location-dependent Gaussian integral and its geometric covariance, retained in A7.'}
    return reasons[lid]
def main():
    import extract_interfaces,save_ambient
    extract_interfaces.ROOT=ROOT;extract_interfaces.main();save_ambient.ROOT=ROOT;save_ambient.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='Both complete main-text Theorems; prior alternatives retain their conditional applicability and the deterministic approximation retains its source-defined geometry.',build_order_policy='Same-paper statement dependencies with auxiliary conditions and parameter formulas expanded; union reach across prior alternatives does not mean conjunction. Proof-only approximation and KL references do not create statement edges.')
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
