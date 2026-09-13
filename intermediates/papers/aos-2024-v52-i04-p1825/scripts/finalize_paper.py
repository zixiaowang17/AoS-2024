"""Finalize source-specific definition relationships without rewriting original Theorems."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
1:{'D3':'Both stability estimates and the inverse-Poincare hypothesis use the source L2 norms.',
'D4':'The initial conditions lie in V and their V norms are bounded by U.',
'D9':'The statement expressly selects strong solutions of the reduced Navier-Stokes equations (10).',
'D10':'The solution class is explicitly C([0,T],V), the source time-continuity convention.',
'D16':'Part B expressly introduces the named inverse-Poincare ratio (15) as an additional hypothesis.'},
2:{'D2':'The initial conditions explicitly belong to C-infinity(Omega)^2.',
'D3':'The displayed comparisons use H2 and L2 norms, with the source vector-valued shorthand.',
'D4':'The initial conditions also explicitly lie in the divergence-free zero-mean space V.',
'D9':'The sequence consists of strong solutions of (10), specialized to nu=1/2 and f=0.'},
3:{'D3':'Both posterior events and the posterior-mean conclusion use the vector-space L2(Omega)^2 norm.',
'D4':'The posterior events range over theta in V and the Bochner mean is also asserted to lie in V.',
'D9':'The forward trajectories are expressly solutions of (10), including the trajectory from the posterior mean initial condition.',
'D11':'The theorem explicitly selects observations (19) and their true-data law P_theta0^N, retaining both observation-window cases.',
'D12':'The prior and base RKHS are explicitly those of Condition 1, with alpha>=2 and truth in calligraphic H.',
'D14':'The concentration assertions explicitly use the posterior distribution (21).',
'D15':'The final clause defines the Bochner posterior mean and controls its initial-condition and plug-in trajectory errors.'},
4:{'D3':'The parameter ball uses an H2 norm and the error event uses an L2 norm.',
'D4':'Both the parameter space and all measurable estimators take values in V.',
'D9':'The periodic solutions are those of (10) with the explicitly fixed viscosity 1/2 and zero forcing.',
'D11':'The data Z^(N) and experiment P_theta^N are those of (19), restricted here to T0>0.'},
5:{'D3':'The eigenbasis is L2-orthonormal, and the explicitly inherited Theorem 3 conclusions use L2 errors.',
'D4':'The basis lies in V and is a basis of H; the inherited posterior events and mean also use V.',
'D6':'The theorem explicitly names the Stokes operator A whose eigenvalues order the basis.',
'D9':'Theorem 5 explicitly inherits the Theorem 3 trajectory and posterior-mean trajectory conclusions for equation (10).',
'D11':'The expressly inherited Theorem 3 probability conclusions use the same observation experiment (19), not the strictly positive-time minimax restriction.',
'D12':'The theorem explicitly takes the prior from Condition 1 before projecting it and uses its RKHS for the truth condition.',
'D13':'The eigenfunctions are explicitly referenced to (20).',
'D14':'Theorem 5 inherits both Theorem 3 posterior concentration events, with the projected prior and replacement rate.',
'D15':'Theorem 5 also inherits the Theorem 3 posterior-mean and plug-in trajectory conclusion, not only its posterior mass statement.',
'D17':'The theorem defines the projected prior and finite spectral truth condition, with J_N=O(log log N).'}}
EDGES={
'D2':{'D1':'The smooth functions are periodic on the specified flat torus.'},
'D3':{'D1':'The L2 and Sobolev spaces are defined on the periodic fundamental domain Omega.'},
'D4':{'D3':'H and V impose divergence and zero-mean constraints on L2 and H1 vector fields, with the stated inner products.'},
'D5':{'D3':'The projector has domain L2(Omega)^2.','D4':'Its image is the divergence-free zero-mean space H.'},
'D6':{'D1':'The equality A=-Delta is restricted to the periodic boundary conditions.','D3':'Its operator domain and graph norm use H2 and L2.','D4':'Its domain intersects H2 vector fields with V.','D5':'Its definition A=-P Delta uses the Helmholtz-Leray projector.'},
'D7':{'D4':'The bilinear form takes V arguments and values in the topological dual V-prime.','D5':'The convective field is projected by P.'},
'D8':{'D1':'The physical PDE is posed on the periodic domain Omega.','D4':'Both forcing and initial condition lie in V, with divergence-free and zero-mean constraints.'},
'D9':{'D4':'The reduced equation is stated in V-prime, with strong equality in H and values in V.','D6':'Its viscous term is nu A u.','D7':'Its nonlinear term is B(u,u).','D8':'Its viscosity, forcing, periodicity and initial data are those of the preceding physical system (9).'},
'D10':{'D1':'The time-dependent maps are vector fields over the same spatial domain Omega.'},
'D11':{'D1':'The spatial design is uniform on Omega.','D4':'The initial condition lies in V.','D9':'The regression signal is the strong PDE solution with that initial condition.'},
'D12':{'D3':'The base prior is supported in H2 and its RKHS embeds in H^alpha.','D4':'The support and RKHS embedding also impose the V constraint.'},
'D13':{'D1':'The Fourier fields use the periodic lattice and domain.','D4':'The source describes the modes as H-orthonormal.','D6':'They are the eigenfunctions of the Stokes operator.'},
'D14':{'D4':'The posterior is a random probability measure on V.','D9':'Its likelihood evaluates the nonlinear PDE forward map.','D11':'Its Gaussian residual likelihood is for the data experiment (19).','D12':'Bayesian weighting starts from the Gaussian prior in Condition 1.'},
'D15':{'D4':'The posterior mean initial condition is asserted to lie in V.','D9':'The plug-in trajectory solves (10) at that posterior mean initial condition.','D14':'The Bochner mean integrates theta against the posterior distribution.'},
'D16':{'D3':'The denominator is the L2 discrepancy of the initial conditions.','D4':'The numerator is their V-norm discrepancy.'},
'D17':{'D3':'The stated basis is L2-orthonormal.','D4':'It is a basis of H contained in V.','D6':'Increasing Stokes eigenvalues specify its ordering.','D12':'The prior to be projected and its RKHS are those of Condition 1.','D13':'The basis functions are explicitly the modes referenced in (20).'}}

def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All five main-text Theorems; preserve stability branches, minimax scope and the explicit Theorem 5 inheritance of Theorem 3 conclusions.',build_order_policy='Topological ordering of the source-backed local PDE, prior, observation and posterior definitions; proof-only theorem references excluded.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGES.get(lid,{})),lid
    for c in data['claims']:
        n=int(c['claim_id'].split('/T')[-1]);c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            m=x['members'][0];lid=m['local_id']
            if lid in DIRECT[n]:x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']+m['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for rel in x['related_theorems']:
            cid=rel['claim_id'];n=int(cid.split('/T')[-1]);path=rel['via_local_ids']
            explanation=' '.join([DIRECT[n][path[0]]]+[EDGES[a][b] for a,b in zip(path,path[1:])])
            ev=copy.deepcopy(claims[cid]['evidence'])
            for lid in path:ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=explanation,evidence=ev)
        m=x['members'][0];own=m['statement_original']+' '+m['local_label']
        linked=own+' '+' '.join(claims[t['claim_id']]['statement_original'] for t in x['related_theorems'])
        selectors=m['highlight_symbols']+m['highlight_phrases']
        assert any(s in own for s in selectors) and all(s in linked for s in selectors),m['local_id']
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    check=json.loads((ROOT/'ranked-interfaces.json').read_text())
    assert [{k:v for k,v in c.items() if k!='depends_on'} for c in check['claims']]==inv['claims']
    print('Census structurally validated; original claims retained; independent source review remains pending.')
if __name__=='__main__':main()
