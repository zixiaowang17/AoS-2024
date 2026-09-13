"""Attach paper-local statement dependencies and derive the census."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts')
sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
'1':{'D2':'The theorem explicitly uses the sparse asymptotics (3).','D8':'The model is Gaussian location as specified in Example 1.','D9':'The parameter class is Theta_b=Theta(a_b,s_n) from (10).','D6':'The displayed loss is the combined testing risk, Fraktur R.','D7':'The conclusion gives its infimum-over-procedures worst-case value.'},
'2':{'D2':'The existence and risk statement is under sparse asymptotics (3).','D8':'The opening specifies the Gaussian location model.','D9':'The uniform risk is over the boundary class Theta_b.','D3':'The theorem first asserts existence of a multiple testing procedure independent of s_n and b.','D6':'The asserted loss is the combined risk.','D10':'Condition (12) is additionally required for the BH branch.','D11':'The BH branch concerns the procedure referenced as (S-18), described in Section 1.6.','D12':'The empirical Bayes branch concerns the posterior null-probability rule (S-29), described in Section 1.6.'},
'3':{'D2':'The theorem retains the sparse asymptotics (3).','D8':'The setting of Theorem 1 fixes Gaussian location noise.','D9':'Its parameter class remains Theta_b from Theorem 1.','D5':'The minimized loss is FNR alone.','D13':'The infimum is restricted to S_B(Theta_b), defined in Definition 1.'},
'4':{'D1':'The opening invokes the independent sparse sequence model (1).','D2':'The opening invokes sparsity and the sequence regime (2)-(3).','D15':'The first alternative uses Assumption 1A.','D16':'The second alternative uses Assumption 1B.','D18':'The class Theta(a,s_n) with a vector of strengths is explicitly defined by (21).','D19':'Both branch values are expressed using Lambda_n(a) from (22).','D6':'Both minimax statements use the combined testing loss.','D7':'The theorem asserts the minimax combined risk and gives an attaining threshold rule.'},
'5':{'D1':'The opening invokes the sequence model (1).','D2':'The opening invokes sparsity and asymptotics (2)-(3).','D15':'The first part assumes 1A.','D16':'The final sentence replaces the first part by the alternative assumption 1B.','D20':'The level is explicitly required to obey (24).','D11':'All bounds concern the BH procedure.','D18':'The uniform bound uses the heterogeneous-strength class Theta(a,s_n).','D19':'The pointwise and uniform bounds use Lambda_n(theta) and Lambda_n(a).','D6':'The quantity bounded is combined testing risk.'},
'6':{'D1':'The inherited setting of Theorem 4 includes the independent sequence model.','D2':'The inherited setting includes sparse asymptotics (1)-(3).','D15':'Theorem 4 first branch, inherited here, is under Assumption 1A.','D16':'Theorem 4 alternative second branch, inherited here, is under Assumption 1B.','D18':'The procedure class and supremum use Theta(a,s_n) from Theorem 4.','D19':'The inherited risk targets are Lambda_n(a) and 2 Lambda_n(a)-1 in their respective branches.','D5':'The theorem explicitly replaces combined risk by FNR.','D13':'The infimum is restricted to sparsity-preserving procedures S_B from Definition 1.'},
'7':{'D2':'The model uses the paper-wide sparse sequence regime, and s_n is the upper sparsity bound in the normalization.','D8':'The opening specifies Gaussian location noise.','D9':'The class in (31) is a union of the beta-min classes Theta(a_b,s), with a_b fixed using s_n.','D21':'Both displayed risks are expected classification loss L_C divided by s_n.','D10':'The BH branch additionally invokes polynomial sparsity (12).','D11':'The attaining BH alternative is the source procedure (S-18).','D12':'The other attaining alternative is the empirical Bayes null-probability rule (S-29).'},
'8':{'D17':'The opening assumes the Subbotin location model with shape zeta>1.','D22':'The parameter set is the large-signal class (32)-(33).','D6':'The first rate statement bounds the combined risk of the threshold rule.','D7':'The same display identifies the optimal minimax combined-risk rate.','D21':'The final sentence gives the analogous classification-risk result, normalized by n^(1-beta).'},
'9':{'D8':'The inherited model is explicitly specialized to Gaussian noise.','D17':'The setting of Theorem 8 is the Subbotin model, here at zeta=2.','D22':'All four adaptation statements concern the large-signal class Theta(r,beta).','D6':'One target criterion is the combined risk inherited from Theorem 8.','D7':'Adaptation concerns the minimax rate stated in Theorem 8.','D21':'The same adaptation statements apply to normalized classification risk.'}
}
def extra(n):
    if n=='6':return [dict(page=15,location='Theorem 4 branches incorporated into Theorem 6'),dict(page=16,location='Theorem 4 threshold-attainment continuation')]
    if n=='7':return [dict(page=22,location='Union class (31) and classification normalization')]
    if n=='9':return [dict(page=23,location='Theorem 8 model and large-signal class'),dict(page=24,location='Theorem 8 rate and Theorem 9 summary')]
    return []
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT;extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
      source_policy='Registered arXiv:2109.13601v2 PDF, 86 pages; main paper and references on pages 1-33 only.',
      normalization_policy='Preserve nine complete original Theorems, including continued statements and all alternative branches. Keep supplementary references unresolved where main-text details are absent.',
      semantic_ranking_policy='Resolve original loss definitions, sparse models, parameter classes and procedure restrictions. Keep alternative noise branches distinct, do not import replaced combined loss into FNR-only results, and do not import proof assumptions or supplementary algorithms.',
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
