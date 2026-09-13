"""Derive all ten theorem dependency sets from source-checked statements."""
import copy,json,subprocess,sys
from pathlib import Path
from extract_interfaces import ROOT,PID,interfaces,members,edges
SKILL=Path('skills/statistical-paper-census/scripts');sys.path.insert(0,str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics
from publication_contract import attach_inventory
DIRECT={
 '3.1':{'D2':'The opening hypothesis is A0, the bounded continuous real-RKHS setting.','D5':'Both rejection rules use the original squared-MMD U-statistic.','D11':'The power infimum and uniform source-norm hypothesis range over the separated class P.','D33':'The uniform bound (3.3) uses the inverse spectral power T^{-theta}.','D9':'The final alternative branch uses bounded RKHS representatives phi_i and permits any decay of the eigenvalues lambda_i.'},
 '3.2':{'D2':'Section 3 explicitly makes A0 the throughout-paper kernel setting for this minimax statement.','D9':'The decay hypothesis lambda_i asymp L(i) and the optional sup_k norm(phi_k) bound refer to the spectral system defined in Section 3.','D6':'The minimax infimum ranges over the exact level-alpha test class Phi_{N,M,alpha}.','D11':'The risk bound takes the worst type-II error over the separated alternative class P.'},
 '4.1':{'D2':'The matrix representation uses the throughout-paper real-RKHS kernel setting A0.','D19':'The left side is the regularized statistic etahat_lambda defined in (4.6).','D17':'The matrix sizes n,m,s are the remaining and reserved sample sizes from Section 4.1.','D18':'K_s and the cross-Gram matrices use the mixture observations Z_i from the covariance-estimation construction.'},
 '4.2':{'D2':'The theorem explicitly assumes A0.','D21':'The theorem explicitly includes A1 and its constant C1 in gamma.','D22':'The theorem explicitly includes A2 and its constant C2 in gamma.','D19':'The null rejection event uses the regularized statistic etahat_lambda.','D15':'The upper bound on lambda is the operator norm of the mixture covariance Sigma_PQ.','D25':'The oracle threshold uses N2(lambda), while the optional sample bound uses N1(lambda).','D9':'The optional branch defines C as the uniform sup-norm bound on the RKHS eigenfunction representatives phi_i.','D17':'The bounds and threshold use the split sizes n,m,s.'},
 '4.3':{'D2':'The theorem explicitly assumes A0.','D21':'The A0–A4 hypothesis includes the scalar multiplier bound A1.','D22':'The A0–A4 hypothesis includes the lambda-scaled bound A2.','D23':'The A0–A4 hypothesis includes the restricted residual condition A3 and its qualification xi.','D24':'The A0–A4 hypothesis includes the positive shifted multiplier bound A4.','D26':'The theorem explicitly requires sample-size assumption B.','D17':'The reserved size is chosen as s=d1 N=d2 M, and gamma uses the remaining n,m.','D11':'The uniform source-norm bound and power infimum use the separated class P.','D33':'The uniform bound uses the inverse spectral power T^{-theta}.','D15':'The chosen lambda is bounded above by the covariance operator norm.','D25':'The general and optional power conditions use N2 and N1, with distinct inequalities.','D19':'The power conclusion concerns etahat_lambda at the displayed oracle threshold.','D9':'The optional branch explicitly requires C=sup_i norm(phi_i)_infinity finite.'},
 '4.6':{'D2':'The displayed etahat_lambda is constructed in the paper-wide RKHS setting A0; the following prose explains that the permutation level argument extends to any statistic.','D19':'The displayed rejection event uses the regularized statistic etahat_lambda, without adding A1–A4.','D29':'The random threshold is the empirical permutation quantile qhat^{B,lambda} at level 1-w alpha.'},
 '4.7':{'D2':'The theorem explicitly assumes A0.','D21':'The A0–A4 hypothesis includes the scalar multiplier bound A1.','D22':'The A0–A4 hypothesis includes the lambda-scaled bound A2.','D23':'The A0–A4 hypothesis includes A3 and the qualification xi in tilde-theta.','D24':'The A0–A4 hypothesis includes the positive lower bound A4.','D26':'The theorem explicitly assumes sample-size comparability B.','D17':'The theorem chooses the reserved sample size s=d1 N=d2 M.','D11':'The uniform hypothesis and power infimum range over the separated class P.','D33':'The hypothesis bounds the inverse spectral power applied to u.','D15':'The selected lambda must not exceed the mixture covariance operator norm.','D25':'The separation conditions use N2, and the optional eigenfunction branch also uses N1.','D19':'The power event uses the regularized statistic etahat_lambda.','D9':'The optional branch requires uniformly bounded RKHS eigenfunction representatives phi_i.','D29':'The power event compares the statistic with the empirical permutation quantile at 1-w alpha.'},
 '4.10':{'D2':'The displayed statistics use the throughout-paper RKHS setting A0; this level result adds no regularizer inequalities.','D19':'Each member of the rejection union uses etahat_lambda from (4.6).','D29':'Each threshold is the sampled permutation quantile at 1-w alpha/|Lambda|.','D30':'The rejection union and the lower bound on the permutation count use the finite regularization grid Lambda.'},
 '4.11':{'D2':'The theorem explicitly assumes A0.','D21':'The A0–A4 hypothesis includes A1.','D22':'The A0–A4 hypothesis includes A2.','D23':'The A0–A4 hypothesis includes A3 and qualification xi in both tilde-theta and grid endpoints.','D24':'The A0–A4 hypothesis includes A4.','D26':'The theorem explicitly assumes sample-size comparability B.','D17':'The split is chosen as s=e1 N=e2 M.','D33':'The uniform-in-theta condition uses the inverse spectral power T^{-theta}.','D11':'The uniform condition and adaptive power infimum use P for the corresponding theta.','D9':'The polynomial and exponential branches constrain lambda_i, and their optional versions constrain the sup-norms of phi_i.','D15':'Both primary branches compare the upper grid endpoint with the covariance operator norm.','D19':'The adaptive rejection event is a union of regularized statistic exceedances.','D29':'The exceedance thresholds are empirical permutation quantiles adjusted by |Lambda|.','D30':'The theorem specifies the grid endpoints and uses the grid cardinality in its permutation budget and quantile levels.'},
 '4.12':{'D2':'The theorem explicitly assumes A0 for each kernel in the family.','D21':'The A0–A4 hypothesis includes A1 for the regularizer.','D22':'The A0–A4 hypothesis includes A2.','D23':'The A0–A4 hypothesis includes A3 and its qualification xi in the rate branches.','D24':'The A0–A4 hypothesis includes A4.','D26':'The theorem explicitly assumes sample-size comparability B.','D17':'The reserved sample size is s=e1 N=e2 M.','D33':'The triple uniform bound uses the inverse spectral power of the operator for the corresponding kernel.','D31':'The power infimum and uniform source-norm bound use the kernel-indexed alternative class tilde-P.','D9':'Each kernel-specific rate branch constrains the eigenvalues lambda_i and optionally the eigenfunction representatives phi_i.','D15':'The branch conditions compare lambda_U with the covariance norm for the current kernel.','D30':'The theorem chooses the regularization grid endpoints and adjusts the permutation budget by |Lambda|.','D32':'The conclusion is the joint union test over (lambda,K), with its kernel-specific statistic and empirical quantile adjusted by |Lambda||K|.'}
}
def main():
    import extract_interfaces
    extract_interfaces.ROOT=ROOT
    extract_interfaces.main()
    inv=json.loads((ROOT/'theorem-inventory.json').read_text());data=copy.deepcopy(inv)
    data['schema_version']='statistical-ranked-interfaces-v4'
    data['scope'].update(paper_count=1,
     source_policy='Pinned 75-page arXiv:2212.09201v3. Main text includes numbered Section 7, Proofs, and references through page 55 above Appendix A; all appendix mathematics excluded.',
     normalization_policy='Preserve all ten full Theorems and distinct optional branches, source operator and sample typography, and unresolved printed ambiguities without silent repair.',
     semantic_ranking_policy='Count statement prerequisites and recursive source definitions only. Keep regularizer assumptions separate; generic permutation level statements do not inherit A1–A4 or power-specific conditions.',
     build_order_policy='Derive same-paper edges from original constructions and their source definitions. Do not import appendix lemmas, proof-only population calculations or illustrative kernel choices.')
    data['interfaces']=copy.deepcopy(interfaces);claims={c['claim_id']:c for c in data['claims']}
    assert set(DIRECT)=={c['claim_id'].split('/T')[-1] for c in data['claims']}
    for c in data['claims']:
        n=c['claim_id'].split('/T')[-1];c['depends_on']=list(DIRECT[n])
        for x in data['interfaces']:
            lid=x['members'][0]['local_id']
            if lid in DIRECT[n]:
                x['central_claim_uses'].append(dict(use_id=c['claim_id']+'-'+lid,paper_id=PID,claim_id=c['claim_id'],use_kind='statement_dependency',reason=DIRECT[n][lid],evidence=c['evidence']))
    derived=canonical_dependencies(data)
    for x in data['interfaces']:x['dependencies']=derived[x['interface_id']]
    derive_metrics(data)
    for x in data['interfaces']:
        for r in x['related_theorems']:
            cid=r['claim_id'];path=r['via_local_ids'];n=cid.split('/T')[-1]
            sentences=[DIRECT[n][path[0]]];evidence=list(claims[cid]['evidence'])
            for lid in path:
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
                for ctx in members[lid].get('application_context',[]):
                    evidence.extend(e for e in ctx['evidence'] if e not in evidence)
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
    passages=dict(paper_id=PID,members=[m for x in finalized['interfaces'] for m in x['members']])
    (ROOT/'source-passages.json').write_text(json.dumps(passages,indent=2,ensure_ascii=False)+'\n')
    print('Finalized and independently validated; final source audit remains.')


if __name__ == "__main__":
    main()
