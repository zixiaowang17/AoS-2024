"""Rebuild published-version passages and connections after printed-source review.

The old extraction supplies a checked scaffold. Source wording, notation, passage
locations and theorem identities are replaced before deriving a new census.
"""
import ast
import copy
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parents[1]
PID = PAPER.name
HISTORY = PAPER / 'source-history/arxiv-2107.01305v2'
OLD = HISTORY if (HISTORY / 'paper-audit.json').exists() else PAPER
SKILL = Path('skills/statistical-paper-census/scripts')
sys.path.insert(0, str(SKILL))
from canonical_dependencies import canonical_dependencies
from census_metrics import derive_metrics

PAGES = {
    'D1': [5], 'D2': [5], 'D3': [5], 'D4': [5], 'D5': [6], 'D6': [8],
    'D7': [6], 'D8': [6], 'D9': [6, 7], 'D10': [7], 'D11': [7], 'D12': [7],
    'D13a': [7], 'D13b': [8], 'D15': [8], 'D16': [8], 'D17a': [9], 'D17b': [9],
    'D18': [9], 'D19a': [9], 'D19b': [9], 'D20': [11], 'D21a': [11], 'D21b': [11],
    'D22a': [11], 'D22b': [11], 'D23': [12], 'D24': [14], 'D25': [15],
    'D26': [16, 17], 'D27': [17], 'D28': [17], 'D29': [18, 19], 'D30': [19],
    'D31': [20], 'D32': [17], 'D33': [10],
}
NAMING_PAGES = {'D9': [6], 'D13a': [8], 'D13b': [8], 'D26': [16], 'D29': [18]}


def load(name):
    return json.loads((OLD / name).read_text())


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def replace(member, before, after):
    assert before in member['statement_original'], (member['local_id'], before)
    member['statement_original'] = member['statement_original'].replace(before, after)


def wording(text):
    return (text.replace('non-degenerate', 'nondegenerate')
            .replace('Non-degenerate', 'Nondegenerate')
            .replace('multi-reference', 'multireference')
            .replace('Clebsch-Gordan', 'Clebsch–Gordan'))


def main():
    inventory = json.loads((ROOT / 'theorem-inventory.json').read_text())
    data = copy.deepcopy(inventory)
    data['schema_version'] = 'statistical-ranked-interfaces-v4'
    data['scope'].update(
        paper_count=1,
        source_policy='Verified local published PDF, DOI 10.1214/23-AOS2292; all twelve Theorems visually reviewed. Main text ends on PDF 24; separate appendices excluded.',
        normalization_policy='Preserve published wording, formulas and numbering; normalize line wrapping and equivalent LaTeX typesetting. Keep source irregularities and record them separately.',
        semantic_ranking_policy='Deduplicate direct uses by theorem and interface; retain the entire independent theorem inventory.',
        build_order_policy='Derive dependencies from same-paper local paths; preserve distinct projected and unprojected members.')
    data['interfaces'] = copy.deepcopy(load('ranked-interfaces.json')['interfaces'])
    members = {m['local_id']: m for it in data['interfaces'] for m in it['members']}
    for lid, m in members.items():
        m['evidence'] = [{'page': p, 'location': wording(m['source_heading'])} for p in PAGES[lid]]
        for key in ['statement_original', 'source_heading', 'local_label']:
            m[key] = wording(m[key])
        m['highlight_phrases'] = [wording(x) for x in m['highlight_phrases']]
        if 'variant_note' in m:
            m['variant_note'] = wording(m['variant_note']).replace('(D.11)', '(D.S11)').replace('(D.31)', '(D.S31)').replace('(D.57)', '(D.S57)')
        for context in m.get('naming_context', []):
            # Existing naming passages had literal double-escaped TeX commands.
            context['text'] = wording(context['text'].replace('\\\\', '\\'))
            context['evidence'] = [{'page': p, 'location': 'Naming context for ' + m['source_heading']}
                                   for p in NAMING_PAGES.get(lid, PAGES[lid])]
    replace(members['D2'], r'i=1,\ldots,n\tag{2.1}', r'i=1,\ldots,n,\tag{2.1}')
    replace(members['D3'], r'\Pi(g_i \cdot \theta_*)', r'\Pi \cdot g_i \cdot \theta_*')
    replace(members['D3'], r'i=1,\ldots,n\tag{2.2}', r'i=1,\ldots,n,\tag{2.2}')
    members['D3']['highlight_symbols'] = [r'\Pi \cdot g_i \cdot \theta_*']
    replace(members['D4'], 'i.e.\u00a0it', 'that is, it')
    replace(members['D8'], r'\log p_\theta(Y_i),$$', r'\log p_\theta(Y_i),$$')
    replace(members['D8'], r'\Pi(g \cdot \theta)', r'\Pi \cdot g \cdot \theta')
    replace(members['D8'], r'$\Pi=\mathop{\mathrm{Id}}$', r'$\Pi=\mathrm{Id}$')
    replace(members['D8'], r'\mathbb{E}[\log p_\theta(Y)],', r'\mathbb{E}[\log p_\theta(Y)],')
    replace(members['D6'], 'non-zero', 'nonzero')
    replace(members['D10'], r'\times d}\tag{2.6}', r'\times d},\tag{2.6}')
    replace(members['D10'], r'$k^\text{th}$-order', '$k$th-order')
    replace(members['D16'], 'non-zero', 'nonzero')
    replace(members['D17a'], ', There is', ',\n\n(a) there is')
    replace(members['D17b'], r', $\Pi$', ',\n\n(b) $\\Pi$')
    for lid in ['D17a', 'D17b']:
        members[lid]['naming_context'][0]['text'] = members[lid]['naming_context'][0]['text'].replace('well-defined', 'well defined')
    replace(members['D20'], 'over $\\mathcal{V}$, or', 'over $\\mathcal{V}$, or')
    replace(members['D21a'], r'+d^k}\tag{2.15}', r'+d^k},\tag{2.15}')
    replace(members['D22a'], r'=\mathbb{R}^d\tag{2.17}', r'=\mathbb{R}^d,\tag{2.17}')
    replace(members['D33'], 'Theorem 2.7, and', 'Theorem 2.7 and')
    replace(members['D33'], 'to follow, is', 'to follow is')
    # The journal display omits dt here; retain that source form and flag it.
    replace(members['D24'], r'$$f_\mathfrak{g}(t)\mathrm{d}t+\sigma', r'$$f_\mathfrak{g}(t)+\sigma')
    replace(members['D24'], r'\mathrm{d}W(t)$$ where', r'\mathrm{d}W(t),$$ where')
    replace(members['D24'], 'i.e.\u00a0$f$', 'that is, $f$')
    replace(members['D26'], 'i.e.\u00a0it', 'that is, it')
    replace(members['D26'], r'\mathrm{d}W(\phi_1,\phi_2)$$ where', r'\mathrm{d}W(\phi_1,\phi_2),$$ where')
    replace(members['D27'], '(D.11)', '(D.S11)')
    replace(members['D28'], r'(\theta)\tag{4.2}', r'(\theta),\tag{4.2}')
    c = members['D28']['naming_context'][0]
    c['text'] = c['text'].replace('$s_2(\\theta)$, and', '$s_2(\\theta)$ and')
    replace(members['D29'], r'\mathrm{d}W(x)$$ where', r'\mathrm{d}W(x),$$ where')
    replace(members['D29'], '(D.31)', '(D.S31)')
    replace(members['D31'], '(D.57)', '(D.S57)')
    replace(members['D31'], 'Further details of the setup are described', 'Further details of the setup described')
    replace(members['D31'], 'Appendix\u00a0D.4', 'Appendix D.4')
    replace(members['D32'], 'three-fold products', 'three-fold products')
    replace(members['D32'], r'$3^\text{rd}$-order', 'third-order')
    for it in data['interfaces']:
        it['name'] = wording(it['name'])
        for kw in it['source_keywords']:
            kw['source_text'] = wording(kw['source_text'])
            kw['label'] = wording(kw['label'])
        it['central_claim_uses'] = []
        it['dependencies'] = []
        it['theorem_explanations'] = {}
    # The original finite-orbit prose is inside math text. Select its actual
    # projected-orbit notation and condition reference, not an invisible prose match.
    members['D7']['highlight_symbols'] = [r'\Pi(\mathcal{O}_{\theta})', r'\Pi(\mathcal{O}_{\theta_*})']
    members['D7']['highlight_phrases'] = ['(2.4)']
    # Obtain the explicit reviewed direct-dependency table without executing the
    # old extraction module or reading any old TeX source at import time.
    tree = ast.parse((OLD / 'scripts/finalize_paper.py').read_text())
    direct = next(ast.literal_eval(node.value) for node in tree.body
                  if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'DIRECT' for t in node.targets))
    direct['4.8'] = direct.pop('4.9')
    direct['4.9'] = direct.pop('4.10')
    direct['4.4']['D27'] = 'The first two formulas use the complex spherical vectors u^(l), defined on published PDF page 17.'
    edges = load('interface-draft.json')['local_edge_explanations']
    by_claim = {c['claim_id']: c for c in data['claims']}
    for c in data['claims']:
        reasons = direct[c['label'].removeprefix('Theorem ')]
        c['depends_on'] = list(reasons)
        for it in data['interfaces']:
            used = [m['local_id'] for m in it['members'] if m['local_id'] in reasons]
            if used:
                it['central_claim_uses'].append({
                    'use_id': c['claim_id'] + '-' + it['interface_id'].split('/')[-1],
                    'paper_id': PID, 'claim_id': c['claim_id'], 'use_kind': 'statement_dependency',
                    'reason': wording(' '.join(reasons[lid] for lid in used)), 'evidence': c['evidence']})
    derived = canonical_dependencies(data)
    for it in data['interfaces']:
        it['dependencies'] = derived[it['interface_id']]
    derive_metrics(data)
    for it in data['interfaces']:
        for rel in it['related_theorems']:
            cid, path = rel['claim_id'], rel['via_local_ids']
            reasons = direct[by_claim[cid]['label'].removeprefix('Theorem ')]
            text = [reasons[path[0]]]
            evidence = list(by_claim[cid]['evidence'])
            for lid in path:
                evidence.extend(e for e in members[lid]['evidence'] if e not in evidence)
            for start, end in zip(path, path[1:]):
                text.append(edges[start][end])
            if len(path) == 1:
                text.extend(reasons[m['local_id']] for m in it['members']
                            if m['local_id'] != path[0] and m['local_id'] in reasons)
            it['theorem_explanations'][cid] = dict(paper_id=PID, via_local_ids=path,
                                                  text=wording(' '.join(text)), evidence=evidence)
    ambient = load('ambient-conventions.json')
    ambient['source_passages'][0]['evidence'] = [{'page': 5, 'location': 'Notation, including local-chart derivatives'}]
    ambient['source_passages'][1]['evidence'] = [{'page': 7, 'location': 'Tensor inner product and squared norm before Theorem 2.2'}]
    for passage in ambient['source_passages']:
        passage['statement_original'] = passage['statement_original'].replace('inner-product', 'inner product')
    save('ambient-conventions.json', ambient)
    save('source-passages.json', {'paper_id': PID, 'members': list(members.values())})
    save('interface-draft.json', {'paper_id': PID, 'interfaces': data['interfaces'], 'local_edge_explanations': edges})
    save('unfinalized-census.json', data)
    subprocess.run([sys.executable, '-B', str(SKILL / 'finalize_census.py'), str(ROOT / 'unfinalized-census.json'),
                    str(ROOT / 'ranked-interfaces.json'), '--inventory', str(ROOT / 'theorem-inventory.json')], check=True)
    subprocess.run([sys.executable, '-B', str(SKILL / 'validate_census.py'), str(ROOT / 'ranked-interfaces.json')], check=True)


if __name__ == '__main__':
    main()
