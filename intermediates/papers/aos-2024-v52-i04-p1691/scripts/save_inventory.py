"""Reproduce the eight source-reviewed original main-text Theorems.

Statements were independently compared with the registered PDF. This script
reproduces that transcription; it does not perform a fresh semantic review.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=next(p for p in ROOT.parents if (p/'scripts/resolve_paper_pdf.py').is_file())
PID='aos-2024-v52-i04-p1691'
SHA='d8a846505214e608346b123e55283166647fd710618859935405b3d6c1f2b8dc'
INVENTORY={'schema_version': 'statistical-theorem-inventory-v1',
 'scope': {'paper_count': 1,
           'theorem_scope': 'main_text_only',
           'source_policy': 'Verified registered local PDF, main text only; printed PDF Theorem '
                            'labels control inventory.',
           'normalization_policy': 'Retain original wording and formulas; normalize layout and equation '
                                   'alignment only. Merge exact shared concepts; preserve distinct '
                                   'local variants and dependency paths.',
           'semantic_ranking_policy': 'All main-text Theorems; deduplicated direct uses with propagated '
                                      'reach kept separate.',
           'build_order_policy': 'Topological ordering of definition dependencies.'},
 'papers': [{'paper_id': 'aos-2024-v52-i04-p1691',
             'title': 'Wasserstein convergence in Bayesian and frequentist deconvolution models',
             'version': 'arXiv:2309.15300v1, 26 September 2023',
             'pdf_pages': 67,
             'pdf_sha256': 'd8a846505214e608346b123e55283166647fd710618859935405b3d6c1f2b8dc',
             'source_url': 'https://arxiv.org/pdf/2309.15300v1',
             'main_text_last_pdf_page': 29,
             'main_text_boundary': {'location': 'Section 7 and Acknowledgements end on PDF page 29, '
                                                'with ERC grant agreement No. 834175. Separate '
                                                'Supplementary Material starts on PDF page 30; no '
                                                'supplement or appendix body is admitted.',
                                    'shared_page_with_appendix': False},
             'intake_review': {'status': 'complete',
                               'theorem_ids': ['aos-2024-v52-i04-p1691:theorem-3.1',
                                               'aos-2024-v52-i04-p1691:theorem-4.1',
                                               'aos-2024-v52-i04-p1691:theorem-4.2',
                                               'aos-2024-v52-i04-p1691:theorem-4.3',
                                               'aos-2024-v52-i04-p1691:theorem-4.4',
                                               'aos-2024-v52-i04-p1691:theorem-4.5',
                                               'aos-2024-v52-i04-p1691:theorem-5.1',
                                               'aos-2024-v52-i04-p1691:theorem-5.2'],
                               'zero_theorems_confirmed': False,
                               'method': 'Independent small-cap Theorem-heading enumeration on pages '
                                         '1–29 and visual comparison of all eight full statements '
                                         'against the registered PDF.'},
             'authors': ['Judith Rousseau', 'Catia Scricciolo']}],
 'claims': [{'claim_id': 'aos-2024-v52-i04-p1691:theorem-3.1',
             'paper_id': 'aos-2024-v52-i04-p1691',
             'claim_kind': 'theorem',
             'label': 'Theorem 3.1',
             'source_order': 1,
             'statement_original': 'Let $\\mu_{X},\\,\\mu_{0X}\\in\\mathcal{P}_{1}(\\mathbb{R}^{d})$, '
                                   '$d\\geq 1$, and let the error distribution\n'
                                   '$\\mu_{\\varepsilon}^{\\otimes d}$ have single coordinate measure\n'
                                   '$\\mu_{\\varepsilon}\\in\\mathcal{P}_{1}(\\mathbb{R})$\n'
                                   'satisfying Assumption 3.1 for $\\beta>0$.\n'
                                   'Then, for probability measures\n'
                                   '$\\mu_{Y}:=\\mu_{\\varepsilon}^{\\otimes d}\\ast\\mu_{X}$, '
                                   '$\\mu_{0Y}:=\\mu_{\\varepsilon}^{\\otimes d}\\ast\\mu_{0X}$,\n'
                                   'having densities $f_{Y}$, $f_{0Y}$, respectively, and a '
                                   'sufficiently small $h>0$,\n'
                                   '\n'
                                   '\\[\n'
                                   'W_{1}(\\mu_{X},\\,\\mu_{0X})\\lesssim '
                                   'h+W_{1}(\\mu_{Y},\\,\\mu_{0Y})+T,\n'
                                   '\\]\n'
                                   '\n'
                                   'with\n'
                                   '\n'
                                   '\\[\n'
                                   '\\begin{split}T&=|\\log '
                                   'h|\\max_{\\mathsf{v}\\in\\mathbb{S}^{d-1}}\\bigg(|\\log '
                                   'h|\\mathbbm{1}_{(\\beta|I_{h}^{\\ast}(\\mathsf{v})|\\leq '
                                   '1)}+h^{-\\beta|I_{h}^{\\ast}(\\mathsf{v})|+1}\\prod_{j\\in '
                                   'I_{h}^{\\ast}(\\mathsf{v})}|v_{j}|^{\\beta}\\mathbbm{1}_{(\\beta|I_{h}^{\\ast}(\\mathsf{v})|>1)}\\bigg)\\\\\n'
                                   '&\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\qquad\\times\\|f_{Y,\\mathsf{v}}-f_{0Y,\\mathsf{v}}\\|_{1},\\end{split}\n'
                                   '\\]\n'
                                   '(3.5)\n'
                                   '\n'
                                   'where, for each $\\mathsf{v}\\in\\mathbb{S}^{d-1}$, we let '
                                   '$I_{h}^{\\ast}(\\mathsf{v}):=\\{j\\in[d]:\\,|v_{j}|>h\\}$.\n'
                                   '\n'
                                   'If, in addition, $\\mu_{0X}$ satisfies Assumption 3.2 for '
                                   '$\\alpha>0$ and\n'
                                   'there exist a constant $C_{1}>0$ and a kernel $K$ as in (a) such '
                                   'that\n'
                                   '\n'
                                   '\\[\n'
                                   '\\max_{\\mathsf{v}\\in\\mathbb{S}^{d-1}}\\|b_{F_{X,\\mathsf{v}}}(h)\\|_{1}\\leq '
                                   'C_{1}h^{\\alpha+1},\n'
                                   '\\]\n'
                                   '(3.6)\n'
                                   '\n'
                                   'then\n'
                                   '\n'
                                   '\\[\n'
                                   'W_{1}(\\mu_{X},\\,\\mu_{0X})\\lesssim '
                                   'h^{\\alpha+1}+W_{1}(\\mu_{Y},\\,\\mu_{0Y})+T,\n'
                                   '\\]\n'
                                   '\n'
                                   'with $T$ as in (3.5).',
             'evidence': [{'page': 10,
                           'location': 'Theorem 3.1; complete original statement before following '
                                       'remark, proof or commentary'}]},
            {'claim_id': 'aos-2024-v52-i04-p1691:theorem-4.1',
             'paper_id': 'aos-2024-v52-i04-p1691',
             'claim_kind': 'theorem',
             'label': 'Theorem 4.1',
             'source_order': 2,
             'statement_original': 'Let $\\Pi_{n}$ be a prior distribution on '
                                   '$\\mathscr{P}(\\mathbb{R}^{d})$, $d\\geq 1$. Suppose that,\n'
                                   'for $\\delta>0$, we have\n'
                                   '$\\mu_{0X}\\in\\mathcal{P}_{4+\\delta}(\\mathbb{R}^{d})$ and the '
                                   'error distribution is $\\mu_{\\varepsilon}^{\\otimes d}$, with '
                                   'single coordinate distribution '
                                   '$\\mu_{\\varepsilon}\\in\\mathcal{P}_{4+\\delta}(\\mathbb{R})$ '
                                   'satisfying Assumption 3.1 for some $\\beta>0$.\n'
                                   'Furthermore, for a sequence '
                                   '$\\tilde{\\epsilon}_{n}\\geq\\sqrt{(\\log n)/n}$ such that\n'
                                   '$\\tilde{\\epsilon}_{n}\\rightarrow 0$,\n'
                                   'constants $c_{1},\\,c_{2},\\,c_{3},\\,c_{4},\\,K^{\\prime}>0$ and '
                                   'sets '
                                   '$\\mathscr{P}_{n}\\subseteq\\{\\mu_{X}:\\,M_{4+\\delta}(\\mu_{Y})\\leq '
                                   'K^{\\prime}\\tilde{\\epsilon}_{n}^{-2}\\}$,\n'
                                   '\n'
                                   '\\[\n'
                                   '\\begin{split}\\log '
                                   'D(\\tilde{\\epsilon}_{n},\\,\\mathscr{F}(\\mathscr{P}_{n}),\\,d)&\\leq '
                                   'c_{1}n\\tilde{\\epsilon}^{2}_{n},\\\\[-3.0pt]\n'
                                   '\\Pi_{n}(\\mathscr{P}_{n}^{c})&\\leq '
                                   'c_{3}\\exp{(-(c_{2}+4)n\\tilde{\\epsilon}^{2}_{n})},\\\\[-3.0pt]\n'
                                   '\\Pi_{n}(B_{\\mathrm{KL}}(P_{0Y};\\,\\tilde{\\epsilon}_{n}^{2}))&\\geq '
                                   'c_{4}\\exp{(-c_{2}n\\tilde{\\epsilon}^{2}_{n})}.\\end{split}\n'
                                   '\\]\n'
                                   '(4.1)\n'
                                   '\n'
                                   'Then, for $\\epsilon_{n}:=[\\tilde{\\epsilon}_{n}(\\log '
                                   'n)^{1+\\mathbbm{1}_{(\\beta d\\leq 1)}}]^{1/(\\beta d\\vee 1)}$ and '
                                   'sufficiently large constant $\\bar{C}>0$,\n'
                                   '\n'
                                   '\\[\n'
                                   '\\Pi_{n}(\\mu_{X}:\\,W_{1}(\\mu_{X},\\,\\mu_{0X})>\\bar{C}\\epsilon_{n}\\mid\\mathsf{Y}^{(n)})\\rightarrow '
                                   '0\\mbox{ in $P_{0Y}^{n}$-probability.}\n'
                                   '\\]\n'
                                   '\n'
                                   'If, in addition, $\\mu_{0X}$ satisfies Assumption 3.2 for '
                                   '$\\alpha>0$ and\n'
                                   'there exist a constant $C_{1}>0$ and a kernel $K$ as in (a) such '
                                   'that, for every $\\mu_{X}\\in\\mathscr{P}_{n}$,\n'
                                   '\n'
                                   '\\[\n'
                                   '\\max_{\\mathsf{v}\\in\\mathbb{S}^{d-1}}\\|b_{F_{X,\\mathsf{v}}}(h_{n})\\|_{1}\\leq '
                                   'C_{1}h_{n}^{\\alpha+1},\\quad\\mbox{ with '
                                   '}\\,h_{n}=[\\tilde{\\epsilon}_{n}(\\log n)^{1+\\mathbbm{1}_{(\\beta '
                                   'd\\leq 1)}}]^{1/[\\alpha+(\\beta d\\vee 1)]},\n'
                                   '\\]\n'
                                   '\n'
                                   'then, for $\\epsilon_{n,\\alpha}:=[\\tilde{\\epsilon}_{n}(\\log '
                                   'n)^{1+\\mathbbm{1}_{(\\beta d\\leq '
                                   '1)}}]^{(\\alpha+1)/[\\alpha+(\\beta d\\vee 1)]}$ and '
                                   '$C_{\\alpha}>0$ large enough,\n'
                                   '\n'
                                   '\\[\n'
                                   '\\Pi_{n}(\\mu_{X}:\\,W_{1}(\\mu_{X},\\,\\mu_{0X})>C_{\\alpha}\\epsilon_{n,\\alpha}\\mid\\mathsf{Y}^{(n)})\\rightarrow '
                                   '0\\mbox{ in $P_{0Y}^{n}$-probability.}\n'
                                   '\\]',
             'evidence': [{'page': 13,
                           'location': 'Theorem 4.1; complete original statement before following '
                                       'remark, proof or commentary'}]},
            {'claim_id': 'aos-2024-v52-i04-p1691:theorem-4.2',
             'paper_id': 'aos-2024-v52-i04-p1691',
             'claim_kind': 'theorem',
             'label': 'Theorem 4.2',
             'source_order': 3,
             'statement_original': 'Let $Y_{1},\\,\\ldots,\\,Y_{n}$ be i.i.d. observations from\n'
                                   '$f_{0Y}:=f_{\\varepsilon}\\ast f_{0X}$, where $f_{\\varepsilon}$ is '
                                   'the density of the\n'
                                   'standard Laplace distribution and $f_{0X}$ satisfies Assumption '
                                   '4.3.\n'
                                   'Let $\\Pi$ be the prior distribution induced by '
                                   '$\\mathscr{D}_{H_{0}}\\otimes\\Pi_{\\sigma}$, where\n'
                                   '${H_{0}}$ verifies Assumption 4.1 and $\\Pi_{\\sigma}$ verifies\n'
                                   'Assumption 4.2.\n'
                                   'Then, the conditions in (4.1) are satisfied for '
                                   '$\\tilde{\\epsilon}_{n}=n^{-2/5}(\\log n)^{\\varphi}$,\n'
                                   'with some $\\varphi>0$, and there exists $D$ large enough so that\n'
                                   '\n'
                                   '\\[\n'
                                   '\\Pi(\\mu_{Y}:\\,\\|f_{Y}-f_{0Y}\\|_{1}>D\\tilde{\\epsilon}_{n}\\mid '
                                   'Y^{(n)})\\rightarrow 0\\,\\mbox{ in $P_{0Y}^{n}$-probability}.\n'
                                   '\\]',
             'evidence': [{'page': 15,
                           'location': 'Theorem 4.2; complete original statement before following '
                                       'remark, proof or commentary'}]},
            {'claim_id': 'aos-2024-v52-i04-p1691:theorem-4.3',
             'paper_id': 'aos-2024-v52-i04-p1691',
             'claim_kind': 'theorem',
             'label': 'Theorem 4.3',
             'source_order': 4,
             'statement_original': 'Let $Y_{1},\\,\\ldots,\\,Y_{n}$ be i.i.d. observations from\n'
                                   '$f_{0Y}:=f_{\\varepsilon}\\ast f_{0X}$, where $f_{\\varepsilon}$ is '
                                   'the density of the\n'
                                   'standard Laplace distribution and $f_{0X}$ satisfies Assumption '
                                   '4.3.\n'
                                   'Let $\\Pi$ be the prior distribution induced by '
                                   '$\\mathscr{D}_{H_{0}}\\otimes\\Pi_{\\sigma}$, where\n'
                                   '${H_{0}}$ verifies Assumption 4.1 for $\\iota>1$ and '
                                   '$\\Pi_{\\sigma}$ verifies\n'
                                   'Assumption 4.2 with $\\varpi>1$. Then,\n'
                                   'there exist $K$ large enough and $\\kappa>0$ so that\n'
                                   '\n'
                                   '\\[\n'
                                   '\\Pi(\\mu_{X}:\\,W_{1}(\\mu_{X},\\,\\mu_{0X})>Kn^{-1/5}(\\log '
                                   'n)^{\\kappa}\\mid Y^{(n)})\\rightarrow 0\\,\\mbox{ in '
                                   '$P_{0Y}^{n}$-probability.}\n'
                                   '\\]',
             'evidence': [{'page': 16,
                           'location': 'Theorem 4.3; complete original statement before following '
                                       'remark, proof or commentary'}]},
            {'claim_id': 'aos-2024-v52-i04-p1691:theorem-4.4',
             'paper_id': 'aos-2024-v52-i04-p1691',
             'claim_kind': 'theorem',
             'label': 'Theorem 4.4',
             'source_order': 5,
             'statement_original': 'Let $Y_{1},\\,\\ldots,\\,Y_{n}$ be i.i.d. observations from\n'
                                   '$f_{0Y}:=f_{\\varepsilon}\\ast f_{0X}$, where $f_{\\varepsilon}$ is '
                                   'the density of the\n'
                                   'standard Laplace distribution and $f_{0X}$\n'
                                   'satisfies Assumptions 4.3–4.5.\n'
                                   'Let $\\Pi$ be the prior distribution induced by '
                                   '$\\mathscr{D}_{H_{0}}\\otimes\\Pi_{\\sigma}$, where\n'
                                   '${H_{0}}$ verifies Assumption 4.1 and $\\Pi_{\\sigma}$ verifies\n'
                                   'Assumption 4.2.\n'
                                   'Then, the conditions in (4.1) are satisfied for\n'
                                   '$\\tilde{\\epsilon}_{n}=n^{-(\\alpha+2)/(2\\alpha+5)}(\\log '
                                   'n)^{\\varphi^{\\prime}}$,\n'
                                   'with some $\\varphi^{\\prime}>0$, and there exists $D^{\\prime}$ '
                                   'large enough so that\n'
                                   '\n'
                                   '\\[\n'
                                   '\\Pi(\\mu_{Y}:\\,\\|f_{Y}-f_{0Y}\\|_{1}>D^{\\prime}\\tilde{\\epsilon}_{n}\\mid '
                                   'Y^{(n)})\\rightarrow 0\\,\\mbox{ in $P_{0Y}^{n}$-probability}.\n'
                                   '\\]',
             'evidence': [{'page': 17,
                           'location': 'Theorem 4.4; complete original statement before following '
                                       'remark, proof or commentary'}]},
            {'claim_id': 'aos-2024-v52-i04-p1691:theorem-4.5',
             'paper_id': 'aos-2024-v52-i04-p1691',
             'claim_kind': 'theorem',
             'label': 'Theorem 4.5',
             'source_order': 6,
             'statement_original': 'Granted the assumptions of Theorem 4.4 on $f_{0Y}$ and considered\n'
                                   'the same prior with $\\iota>1$ and $\\varpi>1$,\n'
                                   'there exist $M^{\\prime}$ large enough and $\\kappa^{\\prime}>0$ so '
                                   'that\n'
                                   '\n'
                                   '\\[\n'
                                   '\\Pi(\\mu_{X}:\\,W_{1}(\\mu_{X},\\,\\mu_{0X})>M^{\\prime}n^{-(\\alpha+1)/(2\\alpha+5)}(\\log '
                                   'n)^{\\kappa^{\\prime}}\\mid Y^{(n)})\\rightarrow 0\\,\\mbox{ in '
                                   '$P_{0Y}^{n}$-probability.}\n'
                                   '\\]',
             'evidence': [{'page': 18,
                           'location': 'Theorem 4.5; complete original statement before following '
                                       'remark, proof or commentary'}]},
            {'claim_id': 'aos-2024-v52-i04-p1691:theorem-5.1',
             'paper_id': 'aos-2024-v52-i04-p1691',
             'claim_kind': 'theorem',
             'label': 'Theorem 5.1',
             'source_order': 7,
             'statement_original': 'Assume that there exists $\\beta>0$ such that, for every '
                                   '$l=0,\\,1,\\,2$,\n'
                                   '\n'
                                   '\\[\n'
                                   '|\\hat{f}_{\\varepsilon}^{(l)}(t)|\\leq '
                                   'd_{l}(1+|t|)^{-(\\beta+l)},\\quad t\\in\\mathbb{R},\n'
                                   '\\]\n'
                                   '(5.1)\n'
                                   '\n'
                                   'with $d_{l}>0$. For any $d\\geq 1$, given $\\alpha,\\,L,\\,M>0$, '
                                   'let '
                                   '$\\mathcal{D}_{d}:=\\mathcal{P}_{1}(\\mathbb{R}^{d},\\,M)\\cap\\mathcal{S}_{d}(\\alpha,\\,L)$ '
                                   'and\n'
                                   '\n'
                                   '\\[\n'
                                   '\\psi_{n}:=n^{(\\alpha+1)/[2\\alpha+(2\\beta d\\vee 1)+1]}.\n'
                                   '\\]\n'
                                   '\n'
                                   'Then, there exists $C>0$ such that, for any estimator '
                                   '$\\hat{\\mu}_{n}$,\n'
                                   '\n'
                                   '\\[\n'
                                   '\\mathop{\\underline{\\lim}}_{n\\to\\infty}\\psi_{n}\\sup_{\\mu\\in\\mathcal{D}_{d}}\\mathbb{E}^{n}_{(\\mu\\ast\\mu_{\\varepsilon}^{\\otimes '
                                   'd})}W_{1}(\\hat{\\mu}_{n},\\,\\mu)>C.\n'
                                   '\\]',
             'evidence': [{'page': 20,
                           'location': 'Theorem 5.1; complete original statement before following '
                                       'remark, proof or commentary'}]},
            {'claim_id': 'aos-2024-v52-i04-p1691:theorem-5.2',
             'paper_id': 'aos-2024-v52-i04-p1691',
             'claim_kind': 'theorem',
             'label': 'Theorem 5.2',
             'source_order': 8,
             'statement_original': 'Let $f_{\\varepsilon}$ be the standard Laplace density.\n'
                                   'Assume that $f_{0X}$ has exponential tails, that is, there exists a '
                                   'constant $c_{2}>0$ such that\n'
                                   '\n'
                                   '\\[\n'
                                   'f_{0X}(\\mathsf{x})\\lesssim '
                                   'e^{-c_{2}|\\mathsf{x}|},\\quad\\text{for $|\\mathsf{x}|$ large '
                                   'enough}.\n'
                                   '\\]\n'
                                   '(5.2)\n'
                                   '\n'
                                   'Then, for suitable $q>0$,\n'
                                   '\n'
                                   '\\[\n'
                                   'W_{1}(\\tilde{\\mu}_{1n},\\,\\mu_{0X})=O_{\\mathsf{P}}(n^{-1/(4d+1)}(\\log '
                                   'n)^{q}).\n'
                                   '\\]',
             'evidence': [{'page': 21,
                           'location': 'Theorem 5.2; complete original statement before following '
                                       'remark, proof or commentary'}]}]}
claims=INVENTORY['claims']
def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==SHA
    ROOT.mkdir(parents=True,exist_ok=True)
    (ROOT/'theorem-inventory.json').write_text(json.dumps(INVENTORY,indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path);a=p.parse_args()
    if a.output_dir:ROOT=a.output_dir.resolve()
    main()
