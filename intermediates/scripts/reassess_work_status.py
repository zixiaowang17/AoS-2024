#!/usr/bin/env python3
"""Assess mathematical work from completed comparison evidence, preserving research.

This is an effort assessment, not a new library search or a Lean compilation claim.
Evidence rules identify explicit sufficiency and elementary expression work;
reviewed exceptions distinguish core constructions from separate paper proofs.
"""
import copy
import hashlib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / 'aggregate'
POLICY = {
    'id':'mathematical-work-v2',
    'use_mathlib':'An inspected interface, or direct composition of existing operations, expresses the archived interface with matching meaning, domains and assumptions.',
    'small_adaptation':'Existing mathematics supports the interface; a thin wrapper, representation conversion, bounded convention clarification or local connecting proof remains.',
    'new_infrastructure':'A substantive construction, essential theory, or core algorithm required by the interface remains to be developed or supplied.',
    'scope':'Assess the archived interface and its variants, not the difficulty of proving every related paper theorem. Do not add unrequested structure laws to a scalar definition.',
    'boundary':'Classify by missing mathematical content, not code length, a missing same-name API, or legacy availability categories.',
    'method':'Reassessment of the completed declaration, variant and gap evidence, using explicit sufficiency/expression criteria and reviewed construction exceptions. These are planning estimates, not compiled Lean implementations or fresh searches.',
    'limits':'Retain source caveats and domain obligations. Yellow is not an absence claim; red must identify a substantive missing construction. Unsearched or indeterminate work stays pending in working data.'
}

# Positions refer to the frozen, ordered 2486-interface census, checked at intake.
# These gaps describe essential constructions, rather than only downstream proofs.
CORE = {53,55,56,227,240,290,308,405,409,411,503,588,722,734,745,811,841,
        876,878,910,913,1002,1110,1155,1175,1180,1181,1186,1187,1193,1285,
        1307,1412,1421,1441,1449,1454,1592,1594,1595,1681,1736,2006,2101,
        2278,2307,2309,2364,2400,2411,2462,2465,2476,2478,2479}
# Older searches explicitly rejected generic Lean syntax as a *named* statistical
# match. That is not a barrier to expressing these elementary formulas/predicates.
ELEMENTARY = {347,454,517,535,571,600,789,958,965,972,1015,1042,1072,1129,
              1190,1200,1201,1218,1223,1417,1457,1488,1596,1621,1626,1630,
              1725,1759,1760,1766,1799,1895,1910,1939,2023,2035,2041,2098,2195}
# Additional construction gaps reviewed from the complete construction/proof queue.
CORE.update({13,45,48,50,58,67,69,148,191,228,253,277,295,406,407,408,438,478,555,
             657,669,670,685,690,697,812,824,825,838,880,911,914,935,961,1000,1005,
             1044,1059,1063,1071,1081,1114,1144,1151,1176,1192,1202,1240,1248,
             1318,1319,1331,1359,1360,1397,1450,1452,1455,1549,1574,1640,1686,
             1723,1750,1751,1868,1869,1914,1923,1931,1950,1981,1990,2005,2047,
             2084,2085,2087,2118,2163,2174,2175,2179,2180,2181,2186,2232,2279,
             2314,2377,2378,2379,2383,2407,2408,2432,2477})
ELEMENTARY.update({105,152,154,164,166,183,185,209,221,231,256,265,275,278,289,
                   309,341,353,361,363,436,440,441,466,472,494,500,507,509,510,
                   524,534,547,551,556,569,573,585,623,647,659,660,666,674,698,699,
                   707,723,729,752,762,768,807,809,844,846,854,862,865,867,871,
                   874,885,889,892,893,896,903,905,918,937,944,946,949,950,980,
                   988,993,994,996,997,1009,1017,1022,1025,1027,1031,1043,1057,
                   1078,1083,1089,1099,1100,1106,1107,1109,1111,1119,1120,1136,
                   1142,1145,1165,1170,1183,1185,1238,1241,1242,1256,1263,1274,
                   1286,1292,1297,1299,1322,1329,1333,1347,1370,1383,1392,1395,
                   1400,1407,1414,1433,1434,1448,1465,1486,1532,1537,1541,1543,
                   1548,1554,1556,1582,1587,1589,1624,1639,1643,1668,1670,1688,
                   1694,1733,1738,1740,1743,1749,1763,1772,1775,1781,1808,1815,
                   1820,1821,1828,1832,1839,1840,1845,1855,1859,1880,1885,1898,
                   1899,1902,1905,1922,1925,1932,1943,1949,1958,1964,1979,2004,
                   2010,2024,2034,2039,2043})
CORE.update({1332,2109})
# Source-statement review: these formulas/predicates need no downstream theorem proof.
ELEMENTARY.update({777,1374,1478,1544,1684})
CAUTION = re.compile(r'coordinate packaging|coordinate identification|index identif|after indexing|translat|conversion|version hypoth|measurab.*selection|estimator.selection|zero.ratio behavior|projection identities|representation|unfolding|unresolved|resolve|unprinted|unstated|missing|discrepanc|inconsisten|ambig|opaque|outside.*scope|not specified|unprovided|singular|exceptional|boundary convention|domain convention|zero.denominator|normalization factor|representative',re.I)
SUFFICIENT = re.compile(r'directly (?:express|defin)|express(?:es|ible)?\b.*\bdirectly|suffice(?:s)? (?:to (?:define|express|state|encode|construct)|for|once)|already (?:suppl|provid)|express the (?:stated|exact|displayed)|primitives express|operations express|arithmetic.*(?:defin|express)|expressible (?:as|by|from|with)',re.I)
FORMULA = re.compile(r'(?:finite (?:sum|arithmetic|matrix|product|averag|count|filter)|scalar (?:arithmetic|operation)|indicator|dot product|inner product|set (?:union|intersection)|function types|set images).*(?:express|defin|formula|compos)|(?:express|defin|compos).*(?:finite (?:sum|arithmetic|averag|count)|scalar (?:formula|arithmetic)|indicator|dot product)',re.I)
LOCAL_NOTE = 'The recorded remaining work is assessed as interface assembly or local compatibility work using the inspected components; no new core construction is identified in this comparison.'

def sha(value):return hashlib.sha256(value).hexdigest()
def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True).encode()
def decision(i,interface):
    a=interface['library_audit'];gap=a['gap']
    if i in CORE:
        return 'new_infrastructure','reviewed_core_construction','The comparison identifies an essential construction or core theory that existing components do not yet supply: '+gap
    if i in ELEMENTARY:
        return 'use_mathlib','reviewed_elementary_expression','The archived formula, supplied-map specification or quantified condition can use existing operations and Lean syntax directly; a same-name library declaration and proofs of the related statistical results are not required to state this interface.'
    if a['status']=='exact_reuse':
        return 'use_mathlib','retained_exact_comparison','The completed type/domain comparison already establishes reuse of the inspected interface for the recorded variants.'
    if not CAUTION.search(gap) and SUFFICIENT.search(gap):
        return 'use_mathlib','explicit_sufficiency','The completed comparison explicitly supports direct expression with existing components. Instantiation of its supplied parameters does not require a new foundational API.'
    if not CAUTION.search(gap) and FORMULA.search(gap):
        return 'use_mathlib','elementary_composition','The recorded construction uses existing finite arithmetic, sums, sets or linear operations; expressing this source-specific formula does not require developing new mathematical infrastructure.'
    return 'small_adaptation','recorded_local_gap',LOCAL_NOTE+' Recorded obligation: '+gap

def main():
    snapshot=ROOT/'before-three-status';snapshot.mkdir(exist_ok=True)
    for n in ['audited.json','mathlib-search-progress.json','work-status-audit.json','work-status-validation.json','mathlib-validation.json','html-verification.json','html-structure-verification.json','html-regression-verification.json','html-reproduction-verification.json']:
        p=snapshot/n
        if not p.exists():p.write_bytes((ROOT/n).read_bytes())
    old=json.loads((snapshot/'audited.json').read_text())
    assert old['source_census_sha256']=='056be068fc87b5aa1cda5af17abed6dfb7e2c006751246ab7571ce9a4fc5596f'
    data=copy.deepcopy(old);progress=json.loads((snapshot/'mathlib-search-progress.json').read_text())
    by_id={r['interface_id']:r for r in progress['completed']}
    rows=[]
    for i,x in enumerate(data['interfaces']):
        a=x['library_audit'];previous=copy.deepcopy(a)
        value,basis,reason=decision(i,x)
        available='; '.join(d['name']+': '+d['provides'] for d in a['related_declarations']) or 'Ordinary Lean functions, predicates and arithmetic where identified by the completed comparison; no specialized declaration was verified.'
        remaining=('No new foundational API is needed to express this interface. Preserve the recorded domains and treat separate statistical guarantees independently.' if value=='use_mathlib' else a['gap'])
        review={'basis':basis,'available':available,'remaining':remaining,'comparison_evidence':a['gap'],'scope':POLICY['scope'],
                'variant_review_count':len(by_id[x['interface_id']]['variant_reviews']),
                'prior_review_sha256':sha(canonical(previous))}
        a.update(work_status=value,work_status_reason=reason,work_status_review=review)
        by_id[x['interface_id']]['library_audit']=copy.deepcopy(a)
        rows.append({'index':i,'interface_id':x['interface_id'],'name':x['name'],'work_status':value,'basis':basis,'reason':reason,'specific_gap':a['gap'],'review':review})
    now=datetime.now(timezone.utc).isoformat();data['work_status_policy']=POLICY;progress['work_status_policy']=POLICY;progress['updated_at']=now
    result={'status':'assessed','checked_at':now,'policy':POLICY,'source_audit_sha256':sha((snapshot/'audited.json').read_bytes()),'source_census_sha256':data['source_census_sha256'],'counts':dict(Counter(r['work_status'] for r in rows)),'interfaces':rows}
    (ROOT/'three-status-assessment.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result['counts']))
    if '--apply' in sys.argv:
        for n,obj in [('audited.json',data),('mathlib-search-progress.json',progress)]:
            target=ROOT/n;temp=target.with_suffix('.three-status.tmp');temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n');temp.replace(target)
        result.update(status='complete',audited_sha256=sha((ROOT/'audited.json').read_bytes()))
        (ROOT/'work-status-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__':main()
