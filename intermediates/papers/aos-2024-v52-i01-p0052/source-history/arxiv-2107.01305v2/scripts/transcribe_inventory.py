"""Transcribe matching-version main-text TeX; printed PDF labels were reviewed separately."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
WORK = Path('[local path omitted]')
PAPER_ID = ROOT.name
SOURCE = (WORK / 'main-only.tex').read_text()
PREAMBLE = SOURCE[:SOURCE.index(r'\makeatletter')]
PAGES = {'2.2': [7], '2.7': [8, 9], '2.11': [10], '2.13': [11],
         '3.1': [12], '3.3': [13], '3.4': [13], '4.1': [14],
         '4.4': [15], '4.6': [16], '4.9': [17], '4.10': [18]}
REFS = {'prop:Kdef': '2.6', 'eq:losslessPi': '2.4',
        'eq:remainderbound': '2.9', 'thm:cryoEM': '4.6'}
EQUATIONS = dict(zip(['eq:seriesexpansionunprojected', 'eq:sk',
                      'eq:remainderbound', 'eq:seriesexpansionprojected',
                      'eq:tildesk'], ['2.7', '2.8', '2.9', '2.10', '2.11']))

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def convert(body, refs=None, equation_numbers=None):
    refs = dict(REFS, **(refs or {}))
    equation_numbers = dict(EQUATIONS, **(equation_numbers or {}))
    body = re.sub(r'\\ref\{([^}]+)\}', lambda m: refs[m[1]], body)
    def equation(m):
        content = m[1]
        labels = re.findall(r'\\label\{([^}]+)\}', content)
        tags = [equation_numbers[x] for x in labels if x in equation_numbers]
        content = re.sub(r'\\label\{[^}]+\}', '', content).strip()
        if tags:
            content += r'\tag{' + tags[0] + '}'
        return r'\[' + content + r'\]'
    body = re.sub(r'\\begin\{equation\}(.*?)\\end\{equation\}', equation, body, flags=re.S)
    body = re.sub(r'\\label\{[^}]+\}', '', body)
    # An unnumbered aligned display is a single mathematical block.
    body = body.replace(r'\begin{align*}', r'\[\begin{aligned}').replace(
        r'\end{align*}', r'\end{aligned}\]')
    body = body.replace(r'{\footnotesize', '{')
    result = subprocess.run(['pandoc', '-f', 'latex', '-t', 'markdown', '--wrap=none'],
                            input=PREAMBLE + '\n\\begin{document}\n' + body + '\n\\end{document}',
                            text=True, capture_output=True, check=True).stdout.strip()
    assert 'reference-type' not in result and '\\ref{' not in result
    assert '\\begin{equation}' not in result
    return result

def main():
    drafts = json.loads((WORK / 'theorem-source-drafts.json').read_text())['theorems']
    actual = re.findall(r'\\begin\{theorem\}(.*?)\\end\{theorem\}', SOURCE, flags=re.S)
    assert len(actual) == 12
    assert [x.strip() for x in actual] == [t['body'].strip() for t in drafts]
    claims = []
    for order, t in enumerate(drafts, 1):
        number = t['number']
        claims.append({'claim_id': PAPER_ID + '/T' + number, 'paper_id': PAPER_ID,
                       'claim_kind': 'theorem', 'label': 'Theorem ' + number,
                       'source_order': order, 'statement_original': convert(t['body']),
                       'evidence': [{'page': p, 'location': 'Theorem ' + number +
                                     (' (continued)' if p != PAGES[number][0] else '')}
                                    for p in PAGES[number]]})
    paper = {'paper_id': PAPER_ID,
             'title': 'Maximum likelihood for high-noise group orbit estimation and single-particle cryo-EM',
             'version': 'arXiv:2107.01305v2', 'source_url': 'https://arxiv.org/pdf/2107.01305v2',
             'pdf_pages': 88, 'pdf_sha256': digest(WORK / 'source.pdf'),
             'main_text_last_pdf_page': 21,
             'main_text_boundary': {'location': 'Section 6, Conclusion, ends on PDF page 21 immediately above Appendix A. Main-text content occupies the region above y=244 PDF points.',
                                    'shared_page_with_appendix': True},
             'intake_review': {'status': 'complete',
                               'theorem_ids': [c['claim_id'] for c in claims],
                               'zero_theorems_confirmed': False}}
    inventory = {'schema_version': 'statistical-theorem-inventory-v1',
                 'scope': {'theorem_scope': 'main_text_only'}, 'papers': [paper], 'claims': claims}
    (ROOT / 'theorem-inventory.json').write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + '\n')
    enumeration = {'paper_id': PAPER_ID, 'source_pdf_sha256': paper['pdf_sha256'],
                   'matching_tex_archive_sha256': digest(WORK / 'source.tar.gz'),
                   'main_text_tex_sha256': digest(WORK / 'main-only.tex'),
                   'method': 'Enumerated uncommented theorem environments before the appendix command; matched source-order labels against the printed PDF. Shared theorem-family counter includes definitions, propositions and numbered remarks; only Theorem environments enter this inventory.',
                   'theorems': [{'label': 'Theorem ' + t['number'], 'pdf_pages': PAGES[t['number']],
                                 'original_tex': t['body']} for t in drafts],
                   'boundary_review': paper['main_text_boundary'], 'appendices_read': False}
    (ROOT / 'evidence' / 'enumeration.json').write_text(json.dumps(enumeration, indent=2, ensure_ascii=False) + '\n')
    print('Saved 12 theorem statements; main text ends on page 21 above Appendix A.')

if __name__ == '__main__':
    main()
