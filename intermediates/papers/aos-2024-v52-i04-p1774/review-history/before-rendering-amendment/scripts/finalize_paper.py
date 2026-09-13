"""Finalize the paper-local source graph without changing theorem statements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
1:{'D3':'The existence assertion and optimality characterization concern the minimizers of (1.1), the NPMLE definition.',
   'D9':'The two optimality conditions explicitly compare delta ell_N(rho-hat)(x) with -1.',
   'D4':'The candidate rho-hat ranges over P(R^d), with no finite-moment or density restriction.'},
2:{'D4':'The initialization is explicitly a member of P(R^d).',
   'D5':'The hypothesis supp(rho_0)=R^d uses the closed full-measure support definition.',
   'D10':'The iterates are explicitly the ordered WFR measure updates (3.7).',
   'D7':'The theorem assumes rho_n converges weakly to rho-hat before identifying that limit.',
   'D3':'The conclusion says that the weak limit minimizes the NPMLE objective (1.1).'},
3:{'D1':'Both particle ODEs use the Gaussian density phi evaluated at the observed data minus particle locations.',
   'D11':'The atomic curve is asserted to be the WFR likelihood flow, explicitly a solution of (3.6).',
   'D8':'The conclusion calls the atomic curve a distributional solution, whose meaning is defined in the Notation paragraph.'},
4:{'D4':'The initialization is explicitly a probability measure in P(R^d).',
   'D5':'The hypothesis supp(rho_0)=R^d requires full support.',
   'D13':'The source explicitly selects Fisher-Rao measure iteration (3.12), written with step gamma in its definition.',
   'D7':'The theorem assumes weak convergence of rho_n to rho-hat.',
   'D3':'Its conclusion identifies rho-hat as an NPMLE, meaning any minimizer of (1.1).'},
5:{'D1':'The weight ODE uses the Gaussian density phi at fixed particle locations.',
   'D12':'The weighted atomic curve is asserted to be the Fisher-Rao likelihood flow solving (3.11).',
   'D8':'The conclusion expressly uses the source distributional-solution convention.'},
6:{'D1':'The position ODE uses the Gaussian density phi at the moving locations.',
   'D14':'The equal-weight atomic curve is asserted to be the Wasserstein likelihood flow solving (3.18).',
   'D8':'The final assertion is that (3.20) is a distributional solution of the cited PDE.'}}
EDGES={
'D1':{'D4':'The Gaussian convolution is mixed against a probability distribution over R^d.'},
'D2':{'D1':'The likelihood evaluates the convolution with the source isotropic Gaussian density at the observed sample.'},
'D3':{'D2':'NPMLE minimizes the empirical negative log-likelihood ell_N.','D4':'Its minimization domain is all probability measures P(R^d).'},
'D5':{'D4':'The support is defined for a probability measure rho.'},
'D6':{'D4':'The pushforward takes a probability measure as input and assigns its mass to inverse images.'},
'D7':{'D4':'Weak convergence is defined for a sequence and limit of probability measures.'},
'D8':{'D4':'The distributional PDE convention pairs a curve of probability measures with spatial test functions.'},
'D9':{'D2':'The first variation is the displayed representative for the likelihood functional ell_N.','D1':'Its numerator and convolution denominator use the Gaussian density phi.','D4':'The variation is evaluated at a probability measure rho.'},
'D10':{'D4':'The two-stage iteration updates probability measures, beginning with an RN density change.','D6':'Its second step transports the intermediate measure by a pushforward.','D9':'The weight update evaluates delta ell_N at rho_n; transport evaluates its spatial gradient at rho-tilde_n.'},
'D11':{'D4':'The source defines this continuous-time flow on P2(R^d).','D9':'Both reaction and transport terms use the source first variation.','D8':'The displayed reaction-transport PDE is interpreted with the main-text distributional-solution convention.','D15':'The named geometric flow specializes the preceding gradient-flow construction for ell_N.','D18':'The definition explicitly specifies the Wasserstein-Fisher-Rao distance as its geometry.'},
'D12':{'D4':'The reaction flow is a curve of probability measures.','D9':'Its reaction coefficient is minus one minus delta ell_N.','D8':'The source identifies the flow by a PDE, using its distributional-solution convention.','D15':'The named Fisher-Rao flow uses the geometric gradient-flow construction introduced in Section 3.1.','D16':'Its Fisher-Rao geometry is the centered reaction-action distance defined in (3.2).'},
'D13':{'D4':'The update is a density change between consecutive probability measures.','D9':'Its density multiplier uses the explicit first variation delta ell_N.'},
'D14':{'D4':'The transport flow evolves probability measures.','D9':'Its velocity is minus the spatial gradient of delta ell_N.','D8':'The main-text PDE is read in the defined distributional sense.','D15':'The flow under the Wasserstein geometry specializes the Section 3.1 gradient construction.','D17':'The named Wasserstein geometry uses the quadratic coupling and transport distance from Section 3.1.'},
'D15':{'D4':'The linearized proximal minimization ranges over P(R^d).','D9':'Its linear term integrates the explicit likelihood first variation against a signed measure difference.'},
'D16':{'D4':'The centered reaction action ranges over curves of probability measures linking its endpoints.','D8':'Admissibility is a reaction PDE, a special case of the stated distributional convention with zero velocity.'},
'D17':{'D4':'The static cost ranges over couplings of two probability measures.','D8':'The dynamic formulation constrains curves by a continuity PDE, with zero reaction field.'},
'D18':{'D4':'The action uses probability-measure curves with centered reaction fields.','D8':'Admissibility is the transport-plus-reaction PDE in the source distributional sense.'}}

def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All six main-text Theorems; separate conditional limit identification from particle-flow characterizations.',build_order_policy='Topological ordering of the source-backed paper-local definition graph.')
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
    print('Census structurally validated; independent source review remains pending.')
if __name__=='__main__':main()
