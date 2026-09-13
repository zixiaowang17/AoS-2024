# -*- coding: utf-8 -*-
"""Build the twenty-Theorem census; source review is a separate completion gate."""
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
'D4':'The opening hypothesis excludes the empty signal configuration from the prior Psi.',
'D5':'Part (ii) specializes the prior to Psi_m,m, the exactly-m instance of the cardinality family.',
'D9':'Both conclusions assert membership in the two-tolerance pure-isolation class C_Psi(gamma,delta).',
'D20':'Here chi-star is the pure-isolation test of Subsection 3.2.1, because the prior excludes the empty set.',
'D41':'Both threshold bounds use a_e and b_e, the projected-family cardinalities in (7).'},
'3.2':{
'D4':'The opening hypothesis permits the empty signal configuration in Psi.',
'D10':'Part (i) states membership in the pure-detection class D_Psi(alpha,beta).',
'D11':'Part (ii) states membership in the familywise class E_Psi(gamma,delta).',
'D12':'Part (iii) states membership in the four-error class C_Psi(alpha,beta,gamma,delta).',
'D22':'Part (i) concerns the pure-detection test chi-star_det.',
'D23':'Part (iii) concerns the joint test chi-star from Subsection 3.2.3.',
'D24':'Part (ii) concerns chi-star_fwer, with the paired thresholds of Subsection 3.2.4.',
'D41':'Parts (i)-(ii) use all four cardinalities a_e,b_e,c_e,d_e; part (iii) recalls only the numerical threshold choices from Theorem 3.1, not its nonempty-prior hypothesis.'},
'4.1':{
'D4':'The theorem binds a compatible global law P in P_Psi and excludes the empty configuration.',
'D3':'The two maxima range over the signal set A(P) and its complement among units.',
'D13':'The two denominators use the global opposite-hypothesis families H_Psi,e and G_Psi,e.',
'D20':'T-star denotes the pure-isolation stopping rule in the nonempty-prior case.',
'D25':'The logarithmic gamma/delta bound uses the standing threshold selection (8) from Subsection 3.4.',
'D29':'The opening sentence explicitly assumes only the lower-tail condition (12).',
'D30':'The denominators use the subsystem information notation I(P,H_Psi,e;s-prime_e) and I(P,G_Psi,e;s-prime_e).'},
'4.2':{
'D4':'The opening and the two branches distinguish P in H0 from P in P_Psi outside H0.',
'D3':'The non-null bounds range separately over signals A(P) and nonsignals.',
'D13':'The bounds use the global families G_Psi,e and H_Psi,e.',
'D22':'The bounds for T-star_det concern the pure-detection test.',
'D23':'The bounds for T-star concern the joint detection/isolation test.',
'D24':'The bounds for T-star_fwer concern the paired-threshold familywise test.',
'D26':'The standing selection (9) supplies error-class admissibility and logarithmic threshold calibration; each displayed limit retains its own tolerance path.',
'D29':'The opening sentence explicitly selects condition (12), without adding condition (11).',
'D30':'The denominators are information quantities against projected law families and the global null.'},
'4.3':{
'D3':'The sample-size maxima use the true signal set A(P) and its complement.',
'D13':'The conclusion explicitly uses global H_Psi,e and G_Psi,e, beyond their occurrence inside (15)-(16).',
'D4':'The theorem assumes a compatible global P with the empty configuration excluded.',
'D5':'The final specialization uses the exactly-m prior Psi_m,m.',
'D9':'Both optimal sample-size comparisons take an infimum over C_Psi(gamma,delta).',
'D20':'The expected sample size is that of the pure-isolation T-star.',
'D25':'The pure-isolation threshold calibration (8) is standing in this subsection.',
'D28':'Subsection 4.4 explicitly assumes (11)-(12) throughout, including this theorem.',
'D29':'Subsection 4.4 explicitly retains the lower-tail condition (12).',
'D30':'The sample-size formulas use full-data information, including I(P,P_Psi minus {P}) in the fixed-cardinality branch.',
'D31':'The hypothesis displays the signal-isolation subsystem equality (15).',
'D32':'The hypothesis separately displays the nonsignal-isolation equality (16).'},
'4.4':{
'D13':'The three conclusion formulas explicitly use the global signal families G_Psi,e.',
'D4':'The theorem is evaluated under a global-null law P in H0.',
'D10':'The first optimum is over the pure-detection class D_Psi(alpha,beta).',
'D11':'The final optimum is over the familywise class E_Psi(gamma,delta).',
'D12':'The middle optimum is over the four-error joint class.',
'D22':'The first expected sample size uses T-star_det.',
'D23':'The middle expected sample size uses joint T-star.',
'D24':'The final expected sample size uses T-star_fwer.',
'D26':'Subsection 3.4 supplies selection (9); the middle conclusion expressly permits fixed gamma and delta.',
'D28':'The standing Subsection 4.4 hypothesis includes (11).',
'D29':'The standing Subsection 4.4 hypothesis includes (12).',
'D30':'All three bounds use the full-data information against G_Psi,e.',
'D33':'The hypothesis displays the minimum detection-information equality (17).'},
'4.5':{
'D3':'The displayed maximum and the final familywise expression range over the signal set A(P).',
'D13':'The familywise conclusion explicitly uses H_Psi,e as an opposite-hypothesis family.',
'D4':'The opening hypothesis selects a non-null compatible law P.',
'D10':'The first optimality comparison uses the pure-detection class.',
'D11':'Only the last, additional-condition branch compares to the familywise class.',
'D12':'The second optimality comparison uses the four-error joint class.',
'D22':'The first conclusion evaluates T-star_det.',
'D23':'The second conclusion evaluates joint T-star under the stated dominant-alpha regime.',
'D24':'The last conclusion evaluates T-star_fwer under the additional isolation condition and dominant-gamma regime.',
'D26':'The detection-case threshold selection (9) remains standing.',
'D28':'The Subsection 4.4 standing assumptions include (11).',
'D29':'The Subsection 4.4 standing assumptions include (12).',
'D30':'The bounds contain full-data information against H0 and H_Psi,e.',
'D31':'The final familywise branch explicitly adds (15); it is not required by the first two conclusions.',
'D34':'The opening hypothesis displays the maximum signal detection-information equality (18).'},
'4.6':{
'D3':'Both conclusions range over A(P) and its complement.',
'D13':'Both conclusions explicitly use H_Psi,e and G_Psi,e.',
'D4':'The opening selects a compatible law outside H0.',
'D11':'The first optimum is over E_Psi(gamma,delta).',
'D12':'The second optimum is over C_Psi(alpha,beta,gamma,delta).',
'D23':'The second expected sample size concerns joint T-star.',
'D24':'The first expected sample size concerns T-star_fwer.',
'D26':'The standing detection-case threshold selection is (9).',
'D28':'Subsection 4.4 assumes (11) throughout.',
'D29':'Subsection 4.4 assumes (12) throughout.',
'D30':'Both conclusions use the specified full-data information quantities.',
'D31':'The hypothesis references the signal-isolation condition (15).',
'D32':'The hypothesis references the nonsignal-isolation condition (16).',
'D34':'The hypothesis references the detection condition (18).'},
'5.1':{
'D5':'The bounds l,u in the statement come from the standing Psi_l,u prior in Subsection 5.1.',
'D18':'The conclusion explicitly identifies D_iso(T), including its empty-set boundary case.',
'D19':'The formula uses ordered indices i_j(T) and the local-statistic count p(T) from (5).',
'D20':'For l greater than zero, T-star is the pure-isolation stopping rule.',
'D23':'For l=0, T-star is the joint stopping rule.',
'D24':'The conclusion also names T-star_fwer; its use outside the l=0 definition domain is recorded as a source convention issue.',
'D25':'Selection (8) is the standing calibration for the l greater than zero branch.',
'D26':'Selection (9) is the standing calibration for the l=0 branch.',
'D27':'Common thresholds (10) are the standing implementation convention for Subsection 5.1.',
'D35':'Subsection 5.1 assumes independence (21) even though this theorem does not repeat it.',
'D37':'Section 5 specializes units to singleton sources and retains (11)-(12).'},
'5.2':{
'D5':'The theorem restricts the standing cardinality prior Psi_l,u to l at least one and splits at u=K.',
'D19':'Every branch uses the local ordered likelihood ratios and p(n) from (5).',
'D20':'The formula rewrites the pure-isolation T-star; T1 through T6 are bound inside this theorem.',
'D25':'The nonempty-prior threshold selection (8) remains standing.',
'D27':'A and B are the common thresholds from (10).',
'D35':'The independence restriction (21) is standing in Subsection 5.1.',
'D37':'The singleton-source model and (11)-(12) are standing in Section 5.'},
'5.3':{
'D5':'The theorem takes l=0 in the standing Psi_l,u prior and distinguishes u<K from u=K.',
'D19':'Its displays use ordered local statistics, their products and p(n).',
'D21':'The first sentence explicitly recalls T0 and T_det from Subsection 3.2.2.',
'D23':'The additional s-prime_k=[K] branch rewrites T_joint from the joint test.',
'D26':'Selection (9) applies in the l=0 detection setting.',
'D27':'The displayed A,B,C,D are the common thresholds (10).',
'D35':'The result inherits independence (21) from Subsection 5.1.',
'D37':'The result uses the singleton-source model and standing (11)-(12).'},
'5.4':{
'D4':'The optimality assertion is for every compatible P in P_Psi.',
'D5':'The two branches use the standing Psi_0,u family, with u=K or u<K.',
'D11':'Asymptotic optimality of chi-star_fwer refers to the familywise error-control class.',
'D19':'The stopping rules use local likelihood ratios, their order and p(n).',
'D24':'The named test is chi-star_fwer with paired thresholds.',
'D26':'Familywise admissibility and log calibration are supplied by the standing selection (9).',
'D27':'The displayed A and B are the common unit thresholds of (10).',
'D35':'Subsection 5.1 imposes independence (21).',
'D37':'Section 5 supplies singleton units and (11)-(12).'},
'5.5':{
'D2':'The equality branches require one source independent of all other sources under the fixed P, using the full-sequence independence convention of Section 2.2.',
'D4':'The theorem assumes a compatible non-null P and a prior permitting no signals.',
'D3':'The bound uses A(P), local H^k,G^k, and sourcewise independence only in its sufficient-condition branches.',
'D5':'The equality cases additionally impose Psi=Psi_0,u and the stated signal-count inequalities.',
'D13':'The numerators involve H_Psi,k or G_Psi,k, the singleton instances of the global hypothesis families.',
'D23':'The result evaluates the joint test chi-star with the specified local isolation subsystems.',
'D26':'Standing threshold selection (9) supplies the calibrated family as tolerances vanish.',
'D30':'Both efficiency bounds use local and global information quantities.',
'D36':'Both conclusions use the ARE ratio from (22), along the separately stated dominant-gamma or dominant-delta paths.',
'D37':'The standing singleton-source model retains (11)-(12); Subsection 5.2 expressly drops global independence (21).'},
'5.6':{
'D2':'Each equality branch requires a particular source independent of the others under P; this does not assert the stronger all-source, all-law condition (21).',
'D4':'The branches distinguish a non-null P from P in H0, with the empty configuration allowed.',
'D3':'The displayed local hypothesis families H^k,G^k and signal indices use singleton units.',
'D5':'Only the final sufficient condition requires Psi_1,1 to be included in Psi.',
'D13':'The null-case numerator involves the global signal family G_Psi,k.',
'D23':'The theorem chooses singleton detection subsystems for joint chi-star.',
'D26':'The calibrated family is that of (9); part (ii) explicitly allows gamma and delta fixed.',
'D30':'The displayed information ratios compare full-data and singleton data.',
'D36':'The quantity bounded is ARE from (22), with a separate tolerance path in each part.',
'D37':'The standing Section 5 model is singleton-source testing with (11)-(12), not the independence setting of Subsection 5.1.'},
'6.1':{
'D7':'The opening explicitly selects the disjoint-signal prior Psi_dis.',
'D19':'The formula uses the ordered local pair statistics, their indices and p(n) from (5).',
'D21':'The conclusion explicitly refers to T0 and T_det from Subsection 3.2.2.',
'D26':'The detection-case threshold selection (9) remains standing.',
'D27':'The displayed C and D use the common-threshold convention (10), which expressly names Theorem 6.1.',
'D38':'Section 6 supplies pair units and the independence/dependence local hypotheses, with standing (11)-(12).',
'D39':'The opening expressly assumes the group-independence equivalence (23).'},
'6.2':{
'D2':'The second sufficient-condition bullet requires an entire pair independent of all remaining source sequences under P.',
'D4':'The theorem assumes P outside H0 and a prior that includes the empty configuration.',
'D3':'Part (ii) compares information against the local pair-null family H^e and ranges over signals.',
'D6':'The second sufficient-condition alternative allows Psi_clus.',
'D7':'Both sufficient-condition alternatives allow Psi_dis.',
'D13':'The bound uses the non-null global family H_Psi,e.',
'D23':'The conclusions concern the joint test with either containing or local isolation subsystems.',
'D26':'The standing calibrated threshold family is (9).',
'D30':'The ratio contains full-data and pairwise information quantities.',
'D36':'ARE is the expected-sample-size ratio (22), here in the dominant-gamma regime.',
'D38':'The pairwise dependence-testing model and (11)-(12) are standing.',
'D39':'Condition (23) is required only in the first sufficient-condition bullet of part (ii), not the second alternative or part (i).',
'D40':'Part (i) uses the blocks v_l and L(P); the second sufficient-condition bullet also uses L(P).'},
'6.3':{
'D2':'The final sufficient condition requires a pair independent of the remaining data sources under P.',
'D4':'The theorem fixes a non-null compatible P and allows an empty configuration in Psi.',
'D3':'The four containment cases and the ratio range over nonsignal pairs, with local alternative family G^e.',
'D6':'The final sufficient condition allows the cluster prior Psi_clus.',
'D7':'The final sufficient condition also allows the disjoint prior Psi_dis.',
'D13':'The numerator uses the global signal family G_Psi,e.',
'D23':'The result concerns the joint test with the displayed isolation subsystems.',
'D26':'The standing threshold calibration is (9).',
'D30':'The bound compares global and pairwise information.',
'D36':'ARE is evaluated in the dominant-delta tolerance regime.',
'D38':'Section 6 supplies the pairwise model and (11)-(12).',
'D40':'All four cases in part (i) use v0 or the dependent blocks v_l; the printed set-membership anomaly is preserved.'},
'6.4':{
'D2':'The equality condition names a dependent pair independent of all remaining data sources under P.',
'D4':'The theorem assumes a compatible law P outside H0.',
'D3':'The local bound uses pair null families H^e and a minimum over signals.',
'D23':'The theorem selects detection subsystems for joint chi-star.',
'D26':'The threshold family remains calibrated by (9).',
'D30':'The bound uses information against H0 and local H^e.',
'D36':'The efficiency ratio is ARE from (22) in the dominant-alpha regime.',
'D38':'The standing model tests dependence of pairs and assumes (11)-(12).',
'D39':'Condition (23) appears only in the final example of the one-independent-pair sufficient condition.',
'D40':'Part (i) requires a detection subsystem containing the union of blocks v1 through v_L(P).'},
'6.5':{
'D2':'The equality condition requires a pair independent of all other data sources under the specified P.',
'D4':'The theorem operates under a global-null P and permits the empty configuration.',
'D3':'The denominator uses the local alternative families G^e over all pair units.',
'D5':'The equality condition additionally assumes Psi_1,1 is included in Psi.',
'D13':'The numerator uses the global family G_Psi,e.',
'D23':'The theorem uses joint chi-star with local detection subsystems.',
'D26':'Selection (9) is standing, while this theorem expressly permits fixed gamma and delta.',
'D30':'The inequality compares full-data and pairwise information.',
'D36':'The bounded quantity is ARE from (22) along the stated alpha/beta limit.',
'D38':'Section 6 supplies pair units, local dependence hypotheses and (11)-(12).',
'D39':'The final phrase cites (23) as an example ensuring the independent-pair sufficient condition.'},
'6.6':{
'D2':'The hypothesis requires a hardest nonsignal pair independent of all other source sequences under P.',
'D4':'The statement permits any compatible P in P_Psi.',
'D3':'The minimization is over nonsignal pairs with local alternative family G^e.',
'D7':'The hypothesis fixes Psi=Psi_dis.',
'D11':'Asymptotic optimality is for familywise error control as gamma and delta vanish.',
'D24':'The named test is chi-star_fwer, with both subsystems local.',
'D26':'Its familywise admissibility and threshold calibration are standing in (9).',
'D30':'The hardest independent pair is identified using I(P^e,G^e).',
'D38':'The result inherits the pairwise model and conditions (11)-(12).',
'D39':'Unlike optional examples in earlier theorems, (23) is explicitly assumed here.'}}
EDGES={
'D2':{'D1':'Global laws are laws of the complete observation sequence X, and P^s restricts them to the subsystem sigma-field F^s.'},
'D3':{'D2':'Each local null and alternative is a subfamily of the projected plausible laws P^e.'},
'D4':{'D3':'Compatibility uses H^e,G^e and the signal set A(P), for every unit e.'},
'D8':{'D1':'The stopping and measurability conditions use the global observation filtration F_n.','D4':'The terminal decision must take values in the specified prior family Psi.'},
'D9':{'D8':'The pure-isolation class restricts tests (T,D) in C_Psi.','D3':'Its error events use the true signal set A(P).','D4':'Its probability requirements range over compatible P_Psi, in the nonempty-prior case.'},
'D10':{'D8':'The pure-detection class restricts tests in C_Psi.','D4':'The two constraints range separately over H0 and P_Psi outside H0.'},
'D11':{'D8':'The familywise class restricts tests in C_Psi.','D3':'Its two error events compare D with the true set A(P).','D4':'Both constraints range over all compatible laws P_Psi.'},
'D12':{'D9':'The source intersection references the pure-isolation class on the non-null prior; its decision-domain ambiguity is retained separately.','D10':'The other factor is the pure-detection class D_Psi(alpha,beta).'},
'D13':{'D3':'The two global families distinguish whether e lies in A(P).','D4':'They restrict compatible P_Psi; H_Psi,e explicitly excludes H0.'},
'D14':{'D1':'Mutual absolute continuity is required only after restriction to each finite-time subsystem sigma-field.','D2':'The condition compares subsystem laws P^s and Q^s.','D13':'Its allowed global law pairs are specified using G_Psi,e and H_Psi,e.','D4':'The law-pair domain also includes the global-null family H0.'},
'D15':{'D14':'The finite-time Radon-Nikodym likelihood ratio is introduced under the preceding mutual-absolute-continuity assumption.'},
'D16':{'D13':'The detection numerator maximizes over projected global laws in G_Psi,e.','D4':'The denominator and reference measure use the projected global-null family H0.','D15':'Both maxima evaluate the finite-time likelihood ratio Lambda_n.'},
'D17':{'D13':'The isolation ratio maximizes over projected G_Psi,e and H_Psi,e.','D15':'Its numerator and denominator evaluate Lambda_n against the reference law P0-prime.'},
'D18':{'D17':'D_iso(n) selects units whose isolation statistic is strictly greater than one.'},
'D19':{'D3':'The local ratio maximizes over the original local G^e and H^e.','D15':'Each term in those maxima is Lambda_n; the same passage defines ordering and the count above one.'},
'D20':{'D17':'Pure-isolation stopping requires each isolation statistic to exit its interval.','D18':'The rule checks D_iso(n) in Psi and reports D_iso at stopping.','D9':'The source chooses its thresholds to place chi-star in C_Psi(gamma,delta).'},
'D21':{'D16':'T0 checks all detection statistics below their lower bounds, while T_det checks at least one above its upper bound.'},
'D22':{'D21':'The pure-detection rule stops at the minimum of T0 and T_det.','D10':'The source calibrates this test for the pure-detection class; its output distinguishes empty from nonempty.'},
'D23':{'D16':'T_joint requires at least one detection statistic above its upper threshold.','D17':'T_joint also requires all isolation statistics to exit their intervals.','D18':'T_joint constrains D_iso(n), and the nonempty decision is D_iso(T-star).','D21':'The joint stopping time is the minimum of T0 and T_joint.','D12':'The source calibrates the four thresholds for the joint error-control class.'},
'D24':{'D23':'The familywise procedure specializes joint chi-star by A_e=C_e and B_e=D_e.','D11':'Its intended class is familywise error control E_Psi(gamma,delta).'},
'D25':{'D20':'Selection (8) calibrates the pure-isolation chi-star.','D9':'It explicitly requires membership in C_Psi(gamma,delta) at every tolerance pair.'},
'D26':{'D22':'Selection (9) includes calibration of chi-star_det.','D23':'The same source display also calibrates joint chi-star.','D24':'The same display includes familywise chi-star_fwer; the shared-threshold notation is documented as a source issue.','D10':'The first admissibility requirement in (9) is membership in D_Psi(alpha,beta).','D11':'The second requirement in (9) is membership in E_Psi(gamma,delta).','D12':'The third requirement in (9) is membership in the four-error class.'},
'D28':{'D15':'Condition (11) bounds the running maxima of log likelihood ratios Z_m.','D13':'The law quantifiers use G_Psi,e and H_Psi,e.','D2':'The likelihoods are based on subsystem restrictions P^s,Q^s.'},
'D29':{'D15':'Condition (12) sums lower-tail probabilities of Z_n.','D13':'The same law quantifiers use G_Psi,e and H_Psi,e.','D2':'The log likelihoods compare subsystem laws P^s,Q^s.'},
'D30':{'D2':'The information-family notation uses projected laws P^s,Q^s and projected families.','D4':'Its stated domain is P in P_Psi and Q-family contained in P_Psi; the positive information parameters are separately bound in (11)-(12).'},
'D31':{'D30':'Condition (15) compares subsystem and full-data information minima.','D13':'Both sides minimize information against the global H_Psi,e family over signals.'},
'D32':{'D30':'Condition (16) compares subsystem and full-data information minima.','D13':'Both sides use the global G_Psi,e family and nonsignal units.'},
'D33':{'D30':'Condition (17) equates subsystem and full-data information minima over all units.','D13':'The alternatives in (17) are the global G_Psi,e families.'},
'D34':{'D30':'Condition (18) compares a maximum of subsystem information with full-data information.','D4':'Both sides measure information against the global-null family H0; A(P) is the compatible law\'s signal set.'},
'D35':{'D2':'Equation (21) factors the full-sequence law into singleton marginal laws.','D4':'The factorization is required for every compatible P in P_Psi.'},
'D36':{'D23':'The numerator of (22) is the expected stopping time of joint chi-star; subsection-specific subsystem choices remain separate scope context.','D12':'The denominator is the optimal expected sample size in the four-error class C_Psi(alpha,beta,gamma,delta).'},
'D37':{'D3':'Section 5 specializes the units and local hypotheses to individual sources.','D28':'The Section 5 model passage explicitly retains distributional assumption (11).','D29':'It also explicitly retains (12).'},
'D38':{'D3':'Section 6 specializes units to pairs with null independence and alternative dependence.','D28':'The Section 6 model explicitly retains condition (11).','D29':'It also explicitly retains condition (12).'},
'D39':{'D2':'The left side of (23) concerns independence of complete sequences from two source groups.','D3':'The right side excludes all cross-pairs from A(P).','D4':'The condition is stated under every compatible law P in P_Psi.'},
'D40':{'D2':'The partition factors the full law P into independent marginal block laws.','D4':'The partition is assigned for each compatible law P in P_Psi.'},
'D41':{'D2':'The coefficients count distinct projected laws, using the subsystem family operation.','D13':'The coefficients a_e,b_e,d_e count projected H_Psi,e or G_Psi,e.','D4':'The coefficient c_e counts projected global-null laws H0.'}}

def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(semantic_ranking_policy='All twenty main-text Theorems; source alternatives and subsection assumptions retain their original scope.',build_order_policy='Source-backed same-paper paths; keep (11) separate from (12), the four error-control formulations distinct, and subsection independence local.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    for lid,m in members.items():assert set(m['depends_on'])==set(EDGES.get(lid,{})),lid
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            local=[m for m in x['members'] if m['local_id'] in DIRECT[n]]
            if local:
                reason=' '.join(DIRECT[n][m['local_id']] for m in local)
                ev=copy.deepcopy(c['evidence'])
                for m in local:ev.extend(e for e in m['evidence'] if e not in ev)
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+x['interface_id'].split('/')[-1],paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=reason,evidence=ev))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for rel in x['related_theorems']:
            cid=rel['claim_id'];n=cid.split('/T')[-1];path=rel['via_local_ids']
            ex=' '.join([DIRECT[n][path[0]]]+[EDGES[a][b] for a,b in zip(path,path[1:])])
            ev=copy.deepcopy(claims[cid]['evidence'])
            for lid in path:ev.extend(e for e in members[lid]['evidence'] if e not in ev)
            x['theorem_explanations'][cid]=dict(paper_id=PID,via_local_ids=path,text=ex,evidence=ev)
        for m in x['members']:
            own=m['statement_original']+' '+m['local_label']
            linked=own+' '+' '.join(claims[t['claim_id']]['statement_original'] for t in x['related_theorems'])
            selectors=m['highlight_symbols']+m['highlight_phrases']
            assert any(s in own for s in selectors) and all(s in linked for s in selectors),m['local_id']
    attach_inventory(data,ROOT/'theorem-inventory.json',ROOT/'ranked-interfaces.json')
    (ROOT/'unfinalized-census.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    subprocess.run([sys.executable,str(SKILL/'finalize_census.py'),str(ROOT/'unfinalized-census.json'),str(ROOT/'ranked-interfaces.json'),'--inventory',str(ROOT/'theorem-inventory.json')],check=True)
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    check=json.loads((ROOT/'ranked-interfaces.json').read_text())
    assert [{k:v for k,v in c.items() if k!='depends_on'} for c in check['claims']]==inv['claims']
    print('Census structurally validated; full independent source review remains pending.')
if __name__=='__main__':main()
