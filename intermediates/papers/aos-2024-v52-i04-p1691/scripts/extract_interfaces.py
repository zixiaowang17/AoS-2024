"""Reproduce original source passages with explicit scope corrections.

Full source/dependency review is a separate stage. No old completion status
or old theorem-demand counts are imported.
"""
import json
from pathlib import Path
from save_inventory import PID
ROOT=Path(__file__).resolve().parents[1]
interfaces=[{'interface_id': 'absolute-moments',
  'rank_group': 'all',
  'name': 'Moments',
  'lean_role': 'definition',
  'type_shape': 'Absolute moments and moment classes: definition over the measures/functions specified in '
                'the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D1',
               'local_label': '§2, M_p and P_p',
               'statement_original': 'Let $\\mathscr{P}(\\mathbb{R}^{d})$ stand for the set of probability '
                                     'measures on $(\\mathbb{R}^{d},\\,\\mathcal{B}(\\mathbb{R}^{d}))$ and\n'
                                     '$\\mathscr{P}_{0}(\\mathbb{R}^{d})$ for the subset of Lebesgue '
                                     'absolutely continuous distributions on $\\mathbb{R}^{d}$.\n'
                                     'For $p\\geq 1$, define $\\mathcal{P}_{p}(\\mathbb{R}^{d})$ to be the '
                                     'set of probability measures on $\\mathbb{R}^{d}$ having finite $p$th '
                                     'moments, i.e. if\n'
                                     '$M_{p}(\\mu):=\\int_{\\mathbb{R}^{d}}|\\mathsf{x}|^{p}\\mu(\\mathrm{d}\\mathsf{x})<\\infty$. '
                                     'In symbols,\n'
                                     '$\\mathcal{P}_{p}(\\mathbb{R}^{d})=\\{\\mu\\in\\mathscr{P}(\\mathbb{R}^{d}):\\,M_{p}(\\mu)<\\infty\\}$.\n'
                                     'For $M>0$, let '
                                     '$\\mathcal{P}_{p}(\\mathbb{R}^{d},\\,M)=\\{\\mu\\in\\mathscr{P}(\\mathbb{R}^{d}):\\,M_{p}(\\mu)\\leq '
                                     'M\\}$\n'
                                     'be the subset of $\\mathcal{P}_{p}(\\mathbb{R}^{d})$ consisting of '
                                     'probability measures having $p$th moments uniformly bounded by $M$.',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 5, 'location': '§2, M_p and P_p'}],
               'variant_note': 'Also defines the bounded subclass P_p(R^d, M); real p ≥ 1 is allowed.',
               'highlight_symbols': ['M_{p}',
                                     '\\mathcal{P}_{p}',
                                     '\\mathcal{P}_{1}',
                                     '\\mathcal{P}_{4+\\delta}',
                                     'M_{4+\\delta}'],
               'highlight_phrases': [],
               'source_kind': 'definition',
               'source_heading': 'Definition'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D1',
                       'source_text': 'moments',
                       'label': 'Moments',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D9',
  'rank_group': 'all',
  'name': 'Multivariate convolution model',
  'lean_role': 'definition',
  'type_shape': 'Convolution mixture model: definition over the measures/functions specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D9',
               'local_label': '§2, μ_Y, f_Y and F(P₁)',
               'statement_original': 'We denote by $\\mathscr{F}$ the class of probability measures '
                                     '$\\mu_{Y}=\\mu_{\\varepsilon}^{\\otimes d}\\ast\\mu_{X}$, with '
                                     '$\\mu_{X}\\in\\mathscr{P}(\\mathbb{R}^{d})$.\n'
                                     'Since $\\mu_{Y}$ is Lebesgue absolutely continuous, we denote by '
                                     '$f_{Y}=f_{\\varepsilon}^{\\otimes d}\\ast\\mu_{X}$ its density.\n'
                                     'For any subset '
                                     '$\\mathscr{P}_{1}\\subseteq\\mathscr{P}(\\mathbb{R}^{d})$, let '
                                     '$\\mathscr{F}(\\mathscr{P}_{1})$ stand for the set of probability '
                                     'measures\n'
                                     '$\\mu_{Y}=\\mu_{\\varepsilon}^{\\otimes d}\\ast\\mu_{X}$, with '
                                     '$\\mu_{X}\\in\\mathscr{P}_{1}$.',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 5, 'location': '§2, μ_Y, f_Y and F(P₁)'}],
               'highlight_symbols': ['\\mu_{Y}', 'f_{Y}', '\\mathscr{F}', '\\mu_{0Y}', 'f_{0Y}'],
               'highlight_phrases': [],
               'source_kind': 'definition',
               'source_heading': 'Definition',
               'naming_context': [{'context_id': 'S2.p1.1',
                                   'text': 'We observe a sample '
                                           '$\\mathsf{Y}^{(n)}=(\\mathsf{Y}_{1},\\,\\dots,\\,\\mathsf{Y}_{n})$ '
                                           'of $n$ i.i.d. random vectors $\\mathsf{Y}_{i}$ of '
                                           '$\\mathbb{R}^{d}$ from the multivariate convolution model '
                                           '$\\mathsf{Y}_{i}=\\mathsf{X}_{i}+\\bm{\\varepsilon}_{i}$ in ( '
                                           '1.1 ),\n'
                                           'where the random vectors $\\mathsf{X}_{i}$ are i.i.d. according '
                                           'to an unknown probability measure $\\mu_{0X}$ . In case of '
                                           'errors with independent and identically distributed '
                                           'coordinates,\n'
                                           'the random vectors $\\bm{\\varepsilon}_{i}$ are i.i.d. according '
                                           'to the $d$ -fold product probability measure '
                                           '$\\mu_{\\varepsilon}^{\\otimes d}$ of the known distribution '
                                           '$\\mu_{\\varepsilon}$ having Lebesgue density $f_{\\varepsilon}$ '
                                           ', which is\n'
                                           'assumed to be ordinary smooth of order $\\beta>0$ , i.e. , for '
                                           'constants $d_{0}>0$ ,\n'
                                           'its Fourier transform $\\hat{f}_{\\varepsilon}$ verifies',
                                   'evidence': [{'page': 5,
                                                 'location': 'Main-text naming context #S2.p1.1'}]}]}],
  'source_keywords': [{'context_id': 'S2.p1.1',
                       'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D9',
                       'source_text': 'multivariate convolution model',
                       'label': 'Multivariate convolution model',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'couplings',
  'rank_group': 'all',
  'name': 'Couplings',
  'lean_role': 'definition',
  'type_shape': 'Couplings of probability measures: definition over the measures/functions specified in the '
                'source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D25',
               'local_label': '§1, transport plans Γ(μ,ν)',
               'statement_original': 'where $|\\mathsf{x}-\\mathsf{y}|$ is the Euclidean distance between '
                                     '$\\mathsf{x},\\,\\mathsf{y}\\in\\mathbb{R}^{d}$ and '
                                     '$\\Gamma(\\mu,\\,\\nu)$ denotes the set of all couplings or transport '
                                     'plans having marginal distributions $\\mu$ and $\\nu$.',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 2, 'location': '§1, transport plans Γ(μ,ν)'}],
               'variant_note': 'Same marginal constraint; Γ replaces Π.',
               'highlight_symbols': ['\\Gamma'],
               'highlight_phrases': ['couplings', 'transport plans'],
               'source_kind': 'definition',
               'source_heading': 'Definition'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D25',
                       'source_text': 'couplings',
                       'label': 'Couplings',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D3',
  'rank_group': 'all',
  'name': 'Wasserstein distance',
  'lean_role': 'definition',
  'type_shape': 'L¹-Wasserstein distance W₁: definition over the measures/functions specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D3',
               'local_label': '§1 and §2, W_p and equation (2.2)',
               'statement_original': 'For probability measures $\\mu,\\,\\nu$ on $\\mathbb{R}^{d}$ having '
                                     'finite $p$th moments, the $L^{p}$-Wasserstein distance '
                                     '$W_{p}(\\mu,\\,\\nu)$ is defined as\n'
                                     '\n'
                                     '\\[\n'
                                     'W_{p}(\\mu,\\,\\nu):=\\inf_{\\gamma\\in\\Gamma(\\mu,\\,\\nu)}\\left(\\int_{\\mathbb{R}^{d}\\times\\mathbb{R}^{d}}|\\mathsf{x}-\\mathsf{y}|^{p}\\,\\gamma(\\mathrm{d}\\mathsf{x},\\,\\mathrm{d}\\mathsf{y})\\right)^{1/p},\n'
                                     '\\]\n'
                                     '\n'
                                     'where $|\\mathsf{x}-\\mathsf{y}|$ is the Euclidean distance between '
                                     '$\\mathsf{x},\\,\\mathsf{y}\\in\\mathbb{R}^{d}$ and '
                                     '$\\Gamma(\\mu,\\,\\nu)$ denotes the set of all couplings or transport '
                                     'plans having marginal distributions $\\mu$ and $\\nu$.\n'
                                     '\n'
                                     'For $p=1$,\n'
                                     '\n'
                                     '\\[\n'
                                     'W_{1}(\\mu,\\,\\nu)=\\int_{0}^{1}|F_{\\mu}^{-1}(s)-F_{\\nu}^{-1}(s)|\\,\\mathrm{d}s=\\int_{\\mathbb{R}}|F_{\\mu}(x)-F_{\\nu}(x)|\\,\\mathrm{d}x=\\|F_{\\mu}-F_{\\nu}\\|_{1}.\n'
                                     '\\]\n'
                                     '(2.2)',
               'relation': 'exact',
               'depends_on': ['D1', 'D25'],
               'evidence': [{'page': 2, 'location': '§1 and §2, W_p and equation (2.2)'},
                            {'page': 6, 'location': '§2, equation (2.2), one-dimensional CDF expression'}],
               'variant_note': 'The first formula defines W_p; the interface used by these theorems is p = '
                               '1, including the one-dimensional CDF identity.',
               'highlight_symbols': ['W_{p}', 'W_{1}'],
               'highlight_phrases': [],
               'source_kind': 'definition',
               'source_heading': 'Definition'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D3',
                       'source_text': 'Wasserstein distance',
                       'label': 'Wasserstein distance',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D18',
  'rank_group': 'all',
  'name': 'Exponential tails',
  'lean_role': 'predicate',
  'type_shape': 'Exponential-tail mixing density: predicate over the measures/functions specified in the '
                'source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D18',
               'local_label': 'Assumption 4.3',
               'statement_original': 'The mixing distribution $\\mu_{0X}\\in\\mathscr{P}_{0}(\\mathbb{R})$\n'
                                     'has density $f_{0X}(x)\\lesssim e^{-(1+C_{0})|x|}$, '
                                     '$x\\in\\mathbb{R}$, with some constant $C_{0}>0$.',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 15, 'location': 'Assumption 4.3'}],
               'highlight_symbols': ['f_{0X}(x)\\lesssim e^{-(1+C_{0})|x|}'],
               'highlight_phrases': ['Assumption 4.3', 'Assumptions 4.3–4.5'],
               'source_kind': 'assumption',
               'source_heading': 'Assumption 4.3'},
              {'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D28',
               'local_label': 'Theorem 5.2, equation (5.2)',
               'statement_original': 'Assume that $f_{0X}$ has exponential tails, that is, there exists a '
                                     'constant $c_{2}>0$ such that\n'
                                     '\n'
                                     '\\[\n'
                                     'f_{0X}(\\mathsf{x})\\lesssim e^{-c_{2}|\\mathsf{x}|},\\quad\\text{for '
                                     '$|\\mathsf{x}|$ large enough}.\n'
                                     '\\]\n'
                                     '(5.2)',
               'relation': 'distinct',
               'depends_on': [],
               'evidence': [{'page': 21, 'location': 'Theorem 5.2, equation (5.2)'}],
               'variant_note': 'Multivariate tail condition outside a compact set, with any c₂ > 0; distinct '
                               'from the univariate Assumption 4.3.',
               'highlight_symbols': ['f_{0X}(\\mathsf{x})\\lesssim e^{-c_{2}|\\mathsf{x}|}'],
               'highlight_phrases': ['exponential tails'],
               'source_kind': 'theorem_excerpt',
               'source_heading': 'Theorem 5.2 — assumption'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D28',
                       'source_text': 'exponential tails',
                       'label': 'Exponential tails',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D8',
  'rank_group': 'all',
  'name': 'Laplace error distribution',
  'lean_role': 'definition',
  'type_shape': 'Standard Laplace distribution: definition over the measures/functions specified in the '
                'source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D8',
               'local_label': '§4.2, standard Laplace error',
               'statement_original': 'In this section, we study the problem of density deconvolution on the '
                                     'real line for mixtures with a Laplace error distribution, whose '
                                     'Fourier transform is given by '
                                     '$\\hat{f}_{\\varepsilon}(t)=(1+t^{2})^{-1}$, $t\\in\\mathbb{R}$.',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 14, 'location': '§4.2, standard Laplace error'}],
               'variant_note': 'The main-text passage specifies the standard Laplace characteristic function '
                               '(1+t²)⁻¹.',
               'highlight_symbols': ['\\hat{f}_{\\varepsilon}(t)=(1+t^{2})^{-1}'],
               'highlight_phrases': ['Laplace'],
               'source_kind': 'source_passage',
               'source_heading': 'Source passage'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D8',
                       'source_text': 'Laplace error distribution',
                       'label': 'Laplace error distribution',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D12',
  'rank_group': 'all',
  'name': 'Posterior measure',
  'lean_role': 'definition',
  'type_shape': 'Posterior distribution in the convolution model: definition over the measures/functions '
                'specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D12',
               'local_label': '§2, posterior formula',
               'statement_original': 'We consider a prior distribution $\\Pi_{n}$ on '
                                     '$\\mathscr{P}(\\mathbb{R}^{d})$ and denote by '
                                     '$\\Pi_{n}(\\cdot\\mid\\mathsf{Y}^{(n)})$\n'
                                     'the corresponding posterior measure\n'
                                     '\n'
                                     '\\[\n'
                                     '\\Pi_{n}(B\\mid\\mathsf{Y}^{(n)})=\\frac{\\int_{B}\\prod_{i=1}^{n}f_{Y}(\\mathsf{Y}_{i})\\,\\mathrm{d}\\Pi_{n}(\\mu_{X})}{\\int\\prod_{j=1}^{n}f_{Y}(\\mathsf{Y}_{j})\\,\\mathrm{d}\\Pi_{n}(\\mu_{X})}.\n'
                                     '\\]',
               'relation': 'exact',
               'depends_on': ['D9'],
               'evidence': [{'page': 5, 'location': '§2, posterior formula'}],
               'highlight_symbols': ['\\Pi_{n}', '\\Pi(\\mu_{Y}', '\\Pi(\\mu_{X}'],
               'highlight_phrases': ['posterior measure'],
               'source_kind': 'definition',
               'source_heading': 'Definition'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D12',
                       'source_text': 'posterior measure',
                       'label': 'Posterior measure',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D16',
  'rank_group': 'all',
  'name': 'Base measure',
  'lean_role': 'predicate',
  'type_shape': 'Base-measure tail condition: predicate over the measures/functions specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D16',
               'local_label': 'Assumption 4.1',
               'statement_original': 'The base measure $H_{0}$ has a continuous and positive density $h_{0}$ '
                                     'on $\\mathbb{R}$ such that,\n'
                                     'for constants $b_{0},\\,b_{0}^{\\prime},\\,c_{0},\\,c_{0}^{\\prime}>0$ '
                                     'and $\\iota>0$,\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\\[\n'
                                     'c_{0}\\exp{(-b_{0}|u|^{\\iota})}\\leq h_{0}(u)\\leq '
                                     'c_{0}^{\\prime}\\exp{(-b_{0}^{\\prime}|u|^{\\iota})},\\quad '
                                     'u\\in\\mathbb{R}.\n'
                                     '\\]',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 15, 'location': 'Assumption 4.1'}],
               'highlight_symbols': ['h_{0}', 'H_{0}'],
               'highlight_phrases': ['Assumption 4.1'],
               'source_kind': 'assumption',
               'source_heading': 'Assumption 4.1'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D16',
                       'source_text': 'base measure',
                       'label': 'Base measure',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D17',
  'rank_group': 'all',
  'name': 'Scale parameter · Prior distribution',
  'lean_role': 'predicate',
  'type_shape': 'Scale-prior condition: predicate over the measures/functions specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D17',
               'local_label': 'Assumption 4.2',
               'statement_original': 'The prior distribution $\\Pi_{\\sigma}$ for $\\sigma$ has a '
                                     'continuous\n'
                                     'density $\\pi_{\\sigma}$ on $(0,\\,\\infty)$\n'
                                     'such that, for constants $D_{1},\\,D_{2}>0$ and '
                                     '$s_{1},s_{2},\\,t_{1},\\,t_{2}\\geq 0$,\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\\[\n'
                                     '\\sigma^{-s_{1}}\\exp{(-D_{1}\\sigma^{-1}|\\log\\sigma|^{t_{1}})}\\lesssim\\pi_{\\sigma}(\\sigma)\\lesssim\\sigma^{-s_{2}}\\exp{(-D_{2}\\sigma^{-1}|\\log\\sigma|^{t_{2}})}\n'
                                     '\\]\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     'for all $\\sigma$ in a neighborhood of $0$. Furthermore, for constants '
                                     '$D_{3},\\,\\varpi>0$,\n'
                                     'the tail probability '
                                     '$\\Pi_{\\sigma}((\\bar{\\sigma},\\infty))\\lesssim\\exp{(-D_{3}\\bar{\\sigma}^{\\varpi})}$ '
                                     'as $\\bar{\\sigma}\\rightarrow\\infty$.',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 15, 'location': 'Assumption 4.2'}],
               'highlight_symbols': ['\\Pi_{\\sigma}', '\\pi_{\\sigma}'],
               'highlight_phrases': ['Assumption 4.2'],
               'source_kind': 'assumption',
               'source_heading': 'Assumption 4.2',
               'naming_context': [{'context_id': 'S4.SS2.p4.1',
                                   'text': 'The first part of Assumption 4.2 on the scale parameter '
                                           '$\\sigma$ of the Gaussian kernel has become common in the '
                                           'literature since the articles [ 62 , 19 , 44 ] .\n'
                                           'Here we consider in addition the tail condition for large values '
                                           'of $\\sigma$ , which requires $\\Pi_{\\sigma}$ to have\n'
                                           'an exponentially decaying tail also at infinity. Examples of '
                                           'densities satisfying these two conditions are inverse Gamma '
                                           'distribution restricted to $(0,\\,\\bar{\\sigma}]$ ,\n'
                                           'for $0<\\bar{\\sigma}<\\infty$ . An example of distribution '
                                           'supported on $(0,\\,\\infty)$ that verifies Assumption 4.2 is '
                                           'given in [ 56 ] , p. 291, where $\\pi_{\\sigma}$ is\n'
                                           'proportional to an inverse-gamma $\\mathrm{IG}(1,\\,\\zeta)$ on '
                                           '$(0,\\,1]$ and to a Weibull $W(\\zeta,\\,\\nu)$ on '
                                           '$(1,\\,\\infty)$ ,\n'
                                           'where $\\zeta>0$ is the scale parameter and $\\nu>0$ the shape '
                                           'parameter.\n'
                                           'Then, $s_{1}=s_{2}=\\zeta+1$ , $t_{1}=t_{2}=0$ and '
                                           '$\\varpi=\\nu$ .\n'
                                           'The assumption on the upper tail of $\\Pi_{\\sigma}$ is used to '
                                           'guarantee that condition ( B.4 ) is satisfied,\n'
                                           'which, in virtue of Theorem B.1 , allows to control '
                                           '$W_{1}(\\mu_{Y},\\,\\mu_{0Y})$ in terms of '
                                           '$\\|f_{Y}-f_{0Y}\\|_{1}$ .',
                                   'evidence': [{'page': 15,
                                                 'location': 'Main-text naming context #S4.SS2.p4.1'}]}]}],
  'source_keywords': [{'context_id': 'S4.SS2.p4.1',
                       'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D17',
                       'source_text': 'scale parameter',
                       'label': 'Scale parameter',
                       'kind': 'term'},
                      {'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D17',
                       'source_text': 'prior distribution',
                       'label': 'Prior distribution',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D14',
  'rank_group': 'all',
  'name': 'Dirichlet process',
  'lean_role': 'predicate',
  'type_shape': 'Dirichlet process with base measure H₀: predicate over the measures/functions specified in '
                'the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D14',
               'local_label': '§4.2, D_H₀',
               'statement_original': 'with\n'
                                     '$\\mu_{H}\\sim\\mathscr{D}_{H_{0}}$, a Dirichlet process with finite, '
                                     'positive base measure $H_{0}$ on $\\mathbb{R}$,',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 14, 'location': '§4.2, D_H₀'}],
               'variant_note': 'The main text invokes the standard Dirichlet process without expanding its '
                               'finite-partition definition.',
               'highlight_symbols': ['\\mathscr{D}_{H_{0}}'],
               'highlight_phrases': ['Dirichlet process'],
               'source_kind': 'source_passage',
               'source_heading': 'Source passage'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D14',
                       'source_text': 'Dirichlet process',
                       'label': 'Dirichlet process',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D15',
  'rank_group': 'all',
  'name': 'Dirichlet process mixture-of-normals prior',
  'lean_role': 'definition',
  'type_shape': 'Dirichlet-process Gaussian mixture prior: definition over the measures/functions specified '
                'in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D15',
               'local_label': '§4.2, prior on the mixing density',
               'statement_original': 'We use a Dirichlet process mixture-of-normals prior on the mixing '
                                     'density\n'
                                     '$f_{X}=\\phi_{\\sigma}\\ast\\mu_{H}$, so that the model density is '
                                     '$f_{Y}=f_{\\varepsilon}\\ast '
                                     'f_{X}=f_{\\varepsilon}\\ast(\\phi_{\\sigma}\\ast\\mu_{H})$, with\n'
                                     '$\\mu_{H}\\sim\\mathscr{D}_{H_{0}}$, a Dirichlet process with finite, '
                                     'positive base measure $H_{0}$ on $\\mathbb{R}$,\n'
                                     'and $\\sigma\\sim\\Pi_{\\sigma}$.',
               'relation': 'exact',
               'depends_on': ['D14'],
               'evidence': [{'page': 14, 'location': '§4.2, prior on the mixing density'}],
               'variant_note': 'The Gaussian mixture is the prior on f_X; the Laplace error law belongs to '
                               'the observation model.',
               'highlight_symbols': ['\\mathscr{D}_{H_{0}}',
                                     '\\Pi_{\\sigma}',
                                     'f_{X}=\\phi_{\\sigma}\\ast\\mu_{H}'],
               'highlight_phrases': ['Dirichlet process mixture-of-normals prior'],
               'source_kind': 'source_passage',
               'source_heading': 'Prior specification'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D15',
                       'source_text': 'Dirichlet process mixture-of-normals prior',
                       'label': 'Dirichlet process mixture-of-normals prior',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D2',
  'rank_group': 'all',
  'name': 'Image measure',
  'lean_role': 'definition',
  'type_shape': 'Sliced measure, density and distribution function: definition over the measures/functions '
                'specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D2',
               'local_label': '§2, projections and equation (2.3)',
               'statement_original': 'Let '
                                     '$\\mathbb{S}^{d-1}:=\\{\\mathsf{v}\\in\\mathbb{R}^{d}:\\,|\\mathsf{v}|=1\\}\\subset\\mathbb{R}^{d}$ '
                                     'be the unit sphere. For $\\mu\\in\\mathcal{P}_{p}(\\mathbb{R}^{d})$\n'
                                     'and $\\mathsf{v}\\in\\mathbb{S}^{d-1}$, we set '
                                     '$\\mu_{\\mathsf{v}}:=\\mu\\circ\\mathsf{v}_{\\ast}^{-1}$ to be the '
                                     'image measure of $\\mu$ by\n'
                                     '$\\mathsf{v}_{\\ast}$, where '
                                     '$\\mathsf{v}_{\\ast}:\\,\\mathbb{R}^{d}\\rightarrow\\mathbb{R}$ is the '
                                     'map defined by '
                                     '$\\mathsf{v}_{\\ast}(\\mathsf{x}):=\\mathsf{v}\\cdot\\mathsf{x}=\\sum_{j=1}^{d}v_{j}x_{j}$.\n'
                                     'Then, $\\mu_{\\mathsf{v}}\\in\\mathcal{P}_{p}(\\mathbb{R})$ because\n'
                                     '\n'
                                     '\\[\n'
                                     'M_{p}(\\mu_{\\mathsf{v}})=\\int_{\\mathbb{R}}|x|^{p}\\mu_{\\mathsf{v}}(\\mathrm{d}x)=\\int_{\\mathbb{R}^{d}}|\\mathsf{v}\\cdot\\mathsf{x}|^{p}\\mu(\\mathrm{d}\\mathsf{x})\\leq\\int_{\\mathbb{R}^{d}}|\\mathsf{x}|^{p}\\mu(\\mathrm{d}\\mathsf{x})=M_{p}(\\mu)<\\infty.\n'
                                     '\\]\n'
                                     '(2.3)',
               'relation': 'exact',
               'depends_on': ['D1'],
               'evidence': [{'page': 6, 'location': '§2, projections and equation (2.3)'}],
               'highlight_symbols': ['\\mu_{\\mathsf{v}}',
                                     '\\mathsf{v}_{\\ast}',
                                     'f_{Y,\\mathsf{v}}',
                                     'f_{0Y,\\mathsf{v}}'],
               'highlight_phrases': [],
               'source_kind': 'definition',
               'source_heading': 'Definition'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D2',
                       'source_text': 'image measure',
                       'label': 'Image measure',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'kl-divergence',
  'rank_group': 'all',
  'name': 'Kullback-Leibler divergence',
  'lean_role': 'definition',
  'type_shape': 'Kullback–Leibler divergence: definition over the measures/functions specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D26',
               'local_label': '§2, KL(P; Q)',
               'statement_original': 'Letting $Pf$ stand for the expected value $\\int f\\mathrm{d}P$, where '
                                     'the integral extends over the entire domain,\n'
                                     'we define the Kullback-Leibler divergence of $Q$ from $P$ as '
                                     '$\\mathrm{KL}(P;\\,Q):=P\\log(f_{P}/f_{Q})$.',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 6, 'location': '§2, KL(P; Q)'}],
               'variant_note': 'Density formulation with common reference measure; the neighbourhood is a '
                               'separate composite definition.',
               'highlight_symbols': ['\\mathrm{KL}(P;\\,Q)'],
               'highlight_phrases': ['Kullback-Leibler divergence'],
               'source_kind': 'definition',
               'source_heading': 'Definition'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D26',
                       'source_text': 'Kullback-Leibler divergence',
                       'label': 'Kullback-Leibler divergence',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D10',
  'rank_group': 'all',
  'name': 'Hellinger distance · Kullback-Leibler type neighbourhood',
  'lean_role': 'definition',
  'type_shape': 'Hellinger distance and KL-type neighbourhood: definition over the measures/functions '
                'specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D10',
               'local_label': '§2, d_H and B_KL',
               'statement_original': 'We now introduce some notation that will be used throughout the '
                                     'article.\n'
                                     'For probability measures '
                                     '$P,\\,Q\\in\\mathscr{P}_{0}(\\mathbb{R}^{d})$, with respective '
                                     'densities $f_{P},\\,f_{Q}$ relative to some reference measure,\n'
                                     'let '
                                     '$d_{\\mathrm{H}}(f_{P},\\,f_{Q}):=\\|\\sqrt{f_{P}}-\\sqrt{f_{Q}}\\|_{2}$ '
                                     'be the Hellinger distance between $f_{P}$ and $f_{Q}$,\n'
                                     'where $\\|f_{P}\\|_{r}$ is the $L^{r}$-norm of $f_{P}$, for $r\\geq '
                                     '1$.\n'
                                     'Letting $Pf$ stand for the expected value $\\int f\\mathrm{d}P$, where '
                                     'the integral extends over the entire domain,\n'
                                     'we define the Kullback-Leibler divergence of $Q$ from $P$ as '
                                     '$\\mathrm{KL}(P;\\,Q):=P\\log(f_{P}/f_{Q})$ and, for $\\epsilon>0$,\n'
                                     'the $\\epsilon$-Kullback-Leibler type neighbourhood of $P$ as\n'
                                     '\n'
                                     '\\[\n'
                                     'B_{\\mathrm{KL}}(P;\\,\\epsilon^{2})=\\left\\{Q\\in\\mathscr{P}_{0}(\\mathbb{R}^{d}):\\,\\mathrm{KL}(P;\\,Q)\\leq\\epsilon^{2},\\,\\,\\,P\\left(\\log\\frac{f_{P}}{f_{Q}}\\right)^{2}\\leq\\epsilon^{2}\\right\\}.\n'
                                     '\\]',
               'relation': 'exact',
               'depends_on': ['D26'],
               'evidence': [{'page': 6, 'location': '§2, d_H and B_KL'}],
               'highlight_symbols': ['d_{\\mathrm{H}}', 'B_{\\mathrm{KL}}'],
               'highlight_phrases': ['Hellinger distance', 'Kullback-Leibler type neighbourhood'],
               'source_kind': 'definition',
               'source_heading': 'Definition'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D10',
                       'source_text': 'Hellinger distance',
                       'label': 'Hellinger distance',
                       'kind': 'term'},
                      {'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D10',
                       'source_text': 'Kullback-Leibler type neighbourhood',
                       'label': 'Kullback-Leibler type neighbourhood',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D27',
  'rank_group': 'all',
  'name': 'Packing number',
  'lean_role': 'definition',
  'type_shape': 'Packing number: definition over the measures/functions specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D27',
               'local_label': '§2, D(ε, B, d)',
               'statement_original': 'For $\\epsilon>0$, let $D(\\epsilon,\\,B,\\,d)$ be the '
                                     '$\\epsilon$-packing number of a set $B$ with\n'
                                     'metric $d$, that is, the maximal number of points in $B$ such that the '
                                     '$d$-distance between every pair is at least $\\epsilon$,\n'
                                     'where $d$ can be either the Hellinger or the $L^{1}$-distance.',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 7, 'location': '§2, D(ε, B, d)'}],
               'highlight_symbols': ['D(\\epsilon,\\,B,\\,d)',
                                     'D(\\tilde{\\epsilon}_{n},\\,\\mathscr{F}(\\mathscr{P}_{n}),\\,d)'],
               'highlight_phrases': ['packing number'],
               'source_kind': 'definition',
               'source_heading': 'Definition'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D27',
                       'source_text': 'packing number',
                       'label': 'Packing number',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D11',
  'rank_group': 'all',
  'name': 'Entropy and remaining mass conditions',
  'lean_role': 'predicate',
  'type_shape': 'Prior-sieve entropy and mass conditions: predicate over the measures/functions specified in '
                'the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D11',
               'local_label': 'Theorem 4.1, equation (4.1)',
               'statement_original': 'Furthermore, for a sequence $\\tilde{\\epsilon}_{n}\\geq\\sqrt{(\\log '
                                     'n)/n}$ such that\n'
                                     '$\\tilde{\\epsilon}_{n}\\rightarrow 0$,\n'
                                     'constants $c_{1},\\,c_{2},\\,c_{3},\\,c_{4},\\,K^{\\prime}>0$ and sets '
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
                                     '(4.1)',
               'relation': 'exact',
               'depends_on': ['D1', 'D9', 'D10', 'D27'],
               'evidence': [{'page': 13, 'location': 'Theorem 4.1, equation (4.1)'}],
               'highlight_symbols': ['\\mathscr{P}_{n}'],
               'highlight_phrases': ['(4.1)'],
               'source_kind': 'theorem_excerpt',
               'source_heading': 'Theorem 4.1 — assumptions',
               'naming_context': [{'context_id': 'S4.SS3.p3.1',
                                   'text': 'We argue that the conditions in ( 4.1 ) are\n'
                                           'satisfied for $\\tilde{\\epsilon}_{n}$ as in the statement.\n'
                                           'The small ball prior probability estimate in the third '
                                           'inequality of ( 4.1 )\n'
                                           'is verified taking into account Remark B.2 and Lemma C.3 ,\n'
                                           'which is based on the construction of an approximation of '
                                           '$f_{0Y}$ by '
                                           '$f_{\\varepsilon}\\ast(\\phi_{\\sigma}\\ast\\mu_{H})$ , for a '
                                           'carefully chosen probability measure $\\mu_{H}$ .\n'
                                           'This construction adapts the proof of Lemma 2 of [ 34 ] , pp. '
                                           '615–616, to obtain an approximation error of the order '
                                           '$O(\\tilde{\\epsilon}_{n})$ ,\n'
                                           'as shown in Lemma C.2 .\n'
                                           'The entropy and remaining mass conditions, the first two '
                                           'inequalities in ( 4.1 ),\n'
                                           'are consequences of Theorem 5 of [ 59 ] , p. 631, because, for '
                                           'any pair of densities $f_{1}$ and $f_{2}$ , we have '
                                           '$\\|f_{\\varepsilon}\\ast(f_{1}-f_{2})\\|_{1}\\leq\\|f_{1}-f_{2}\\|_{1}$ '
                                           '.\n'
                                           'Finally, since $\\mu_{X}$ has density '
                                           '$\\phi_{\\sigma}\\ast\\mu_{H}$ so that $X=\\sigma Z+U$ ,\n'
                                           'with $Z\\sim N(0,\\,1)$ and $U\\sim\\mu_{H}$ , we have '
                                           '$M_{1}(\\mu_{X})\\leq\\sigma\\mathbb{E}[|Z|]+M_{1}(\\mu_{H})<\\infty$ '
                                           ', that is, $\\mu_{X}\\in\\mathcal{P}_{1}(\\mathbb{R})$ almost '
                                           'surely,\n'
                                           'because '
                                           '$\\mathscr{D}_{H_{0}}(\\mu_{H}:\\,M_{1}(\\mu_{H})=\\infty)=0$ .\n'
                                           'The assertion follows.\n'
                                           '∎',
                                   'evidence': [{'page': 16,
                                                 'location': 'Main-text naming context #S4.SS3.p3.1'}]}]}],
  'source_keywords': [{'context_id': 'S4.SS3.p3.1',
                       'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D11',
                       'source_text': 'entropy and remaining mass conditions',
                       'label': 'Entropy and remaining mass conditions',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D29',
  'rank_group': 'all',
  'name': 'Reciprocal · Fourier transform',
  'lean_role': 'definition',
  'type_shape': 'Reciprocal error characteristic function: definition over the measures/functions specified '
                'in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D29',
               'local_label': '§3.1, equation (3.1)',
               'statement_original': 'If $|\\hat{f}_{\\varepsilon}(t)|\\neq 0$, $t\\in\\mathbb{R}$, then the '
                                     'reciprocal of $\\hat{f}_{\\varepsilon}$,\n'
                                     '\n'
                                     '\\[\n'
                                     'r_{\\varepsilon}(t):=\\frac{1}{\\hat{f}_{\\varepsilon}(t)},\\quad '
                                     't\\in\\mathbb{R},\n'
                                     '\\]\n'
                                     '(3.1)\n'
                                     '\n'
                                     'is well defined. For an $l$-times differentiable Fourier transform\n'
                                     '$\\hat{f}_{\\varepsilon}$, with $l\\in\\mathbb{N}_{0}$, the $l$th '
                                     'derivative of $r_{\\varepsilon}$ is denoted by '
                                     '$r^{(l)}_{\\varepsilon}$,\n'
                                     'with $r_{\\varepsilon}^{(0)}\\equiv r_{\\varepsilon}$.',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 7, 'location': '§3.1, equation (3.1)'}],
               'highlight_symbols': ['r_{\\varepsilon}', 'r^{(l)}_{\\varepsilon}', 'r_{\\varepsilon}^{(0)}'],
               'highlight_phrases': [],
               'source_kind': 'definition',
               'source_heading': 'Definition'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D29',
                       'source_text': 'reciprocal',
                       'label': 'Reciprocal',
                       'kind': 'term'},
                      {'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D29',
                       'source_text': 'Fourier transform',
                       'label': 'Fourier transform',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D7',
  'rank_group': 'all',
  'name': 'Bias · Distribution function',
  'lean_role': 'definition',
  'type_shape': 'Smoothed CDF bias: definition over the measures/functions specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D7',
               'local_label': '§3.1, bias and equation (3.4)',
               'statement_original': 'For $h>0$, we define $K_{h}(\\cdot):=(1/h)K(\\cdot/h)$ as the rescaled '
                                     'kernel and\n'
                                     '$b_{F_{X}}(h):=F_{X}-F_{X}\\ast K_{h}$ as the “bias” of the '
                                     'distribution function $F_{X}$\n'
                                     'of a probability measure $\\mu_{X}$ on $\\mathbb{R}$.\n'
                                     'In general, for $d\\geq 1$, we consider a multivariate kernel on '
                                     '$\\mathbb{R}^{d}$ with independent coordinates defined as\n'
                                     '\n'
                                     '\\[\n'
                                     'K^{\\otimes '
                                     'd}(\\mathsf{x}):=\\prod_{j=1}^{d}K(x_{j}),\\quad\\mathsf{x}\\in\\mathbb{R}^{d}.\n'
                                     '\\]\n'
                                     '(3.4)\n'
                                     '\n'
                                     'For $\\mu_{X}\\in\\mathcal{P}_{1}(\\mathbb{R}^{d})$ and '
                                     '$\\mathsf{v}\\in\\mathbb{S}^{d-1}$, let\n'
                                     '$b_{F_{X,\\mathsf{v}}}(h):=F_{X,\\mathsf{v}}-F_{X,\\mathsf{v}}\\ast(K^{\\otimes '
                                     'd}_{h})_{\\mathsf{v}}$ be the bias of the distribution function\n'
                                     '$F_{X,\\mathsf{v}}$ associated to '
                                     '$\\mu_{X,\\mathsf{v}}\\in\\mathcal{P}_{1}(\\mathbb{R})$.',
               'relation': 'exact',
               'depends_on': ['D2'],
               'evidence': [{'page': 9, 'location': '§3.1, bias and equation (3.4)'}],
               'highlight_symbols': ['b_{F_{X}}', 'b_{F_{X,\\mathsf{v}}}'],
               'highlight_phrases': [],
               'source_kind': 'definition',
               'source_heading': 'Definition'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D7',
                       'source_text': 'bias',
                       'label': 'Bias',
                       'kind': 'term'},
                      {'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D7',
                       'source_text': 'distribution function',
                       'label': 'Distribution function',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D5',
  'rank_group': 'all',
  'name': 'Global Sobolev regularity',
  'lean_role': 'predicate',
  'type_shape': 'Sliced Sobolev regularity of the mixing law: predicate over the measures/functions '
                'specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D5',
               'local_label': 'Assumption 3.2',
               'statement_original': 'The mixing distribution '
                                     '$\\mu_{0X}\\in\\mathscr{P}_{0}(\\mathbb{R}^{d})\\cap\\mathcal{P}_{1}(\\mathbb{R}^{d})$\n'
                                     'is such that there exists $\\alpha>0$ for which\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\\[\n'
                                     '\\max_{\\mathsf{v}\\in\\mathbb{S}^{d-1}}\\int_{\\mathbb{R}}|t|^{\\alpha}|\\hat{\\mu}_{0X}(t\\mathsf{v})|\\,\\mathrm{d}t<\\infty\\quad\\mbox{and}\\quad\\max_{\\mathsf{v}\\in\\mathbb{S}^{d-1}}\\|D^{\\alpha}f_{0X,\\mathsf{v}}\\|_{1}<\\infty,\n'
                                     '\\]\n'
                                     '(3.3)\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     'where $D^{\\alpha}f_{0X,\\mathsf{v}}$ is the inverse Fourier transform '
                                     'of $(-\\imath\\cdot)^{\\alpha}\\hat{\\mu}_{0X}(\\cdot\\mathsf{v})$.',
               'relation': 'exact',
               'depends_on': ['D1', 'D2'],
               'evidence': [{'page': 8, 'location': 'Assumption 3.2'}],
               'highlight_symbols': ['D^{\\alpha}f_{0X,\\mathsf{v}}'],
               'highlight_phrases': ['Assumption 3.2'],
               'source_kind': 'assumption',
               'source_heading': 'Assumption 3.2',
               'naming_context': [{'context_id': 'S3.SS1.p9.1',
                                   'text': 'Thus, when $d=1$ , when we consider smoothness assumptions of '
                                           '$f_{0X}$ , we assume that $f_{0X}$ belongs to either\n'
                                           'a Sobolev or a Hölder class of densities, which are common '
                                           'nonparametric classes of regular functions.\n'
                                           'With Assumption 3.3 , the density $f_{0X}$ is required to be '
                                           'locally Hölder smooth, namely, it has $\\ell$ derivatives,\n'
                                           'for $\\ell$ the largest integer strictly smaller than $\\alpha$ '
                                           ',\n'
                                           'with the $\\ell$ th derivative being Hölder of order '
                                           '$\\alpha-\\ell$ and integrable envelope $L_{0}$ ,\n'
                                           'the latter condition being used to bound the $L^{1}$ -norm of '
                                           'the bias of $F_{0X}$ , cf. Lemma A.3 .\n'
                                           'With Assumption 3.2 , instead, $f_{0X}$ is required to have '
                                           'global Sobolev regularity $\\alpha$ . Requiring that '
                                           '$D^{\\alpha}\\hskip-1.0ptf_{0X}\\in L^{2}(\\mathbb{R})$ is '
                                           'equivalent to\n'
                                           'imposing that $f_{0X}\\in\\mathcal{S}(\\alpha,\\,L)$ for some '
                                           '$L>0$ , the difference being that '
                                           '$D^{\\alpha}\\hskip-1.0ptf_{0X}$ is here assumed\n'
                                           'to be in $L^{1}(\\mathbb{R})$ .',
                                   'evidence': [{'page': 9,
                                                 'location': 'Main-text naming context #S3.SS1.p9.1'}]}]}],
  'source_keywords': [{'context_id': 'S3.SS1.p9.1',
                       'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D5',
                       'source_text': 'global Sobolev regularity',
                       'label': 'Global Sobolev regularity',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D20',
  'rank_group': 'all',
  'name': 'Hölder smooth · Envelope function',
  'lean_role': 'predicate',
  'type_shape': 'Local Hölder condition with integrable envelope: predicate over the measures/functions '
                'specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D20',
               'local_label': 'Assumption 4.5',
               'statement_original': 'For given $\\alpha>0$, there exist $0<\\upsilon\\leq 1$, $L_{0}\\in '
                                     'L^{1}(\\mathbb{R})$ and $R\\geq(2m/\\upsilon)$, with the smallest '
                                     'integer $m\\geq[2\\vee(\\alpha+2)/2]$, such that $f_{0X}$\n'
                                     'satisfies\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\\[\n'
                                     '|f_{0X}(x+\\zeta)-f_{0X}(x)|\\leq '
                                     'L_{0}(x)|\\zeta|^{\\upsilon}\\,\\mbox{ for every '
                                     '}x,\\,\\zeta\\in\\mathbb{R},\n'
                                     '\\]\n'
                                     '(4.3)\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     'and\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\\[\n'
                                     '\\int_{\\mathbb{R}}e^{|x|/2}f_{0X}(x)\\left(\\frac{L_{0}}{f_{0X}}(x)\\right)^{R}\\mathrm{d}x<\\infty.\n'
                                     '\\]\n'
                                     '(4.4)',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 17, 'location': 'Assumption 4.5'}],
               'highlight_symbols': ['L_{0}',
                                     '|f_{0X}(x+\\zeta)-f_{0X}(x)|\\leq L_{0}(x)|\\zeta|^{\\upsilon}'],
               'highlight_phrases': ['Assumption 4.5', 'Assumptions 4.3–4.5'],
               'source_kind': 'assumption',
               'source_heading': 'Assumption 4.5',
               'naming_context': [{'context_id': 'S4.SS4.p2.1',
                                   'text': 'Assumption 4.4 requires that, for $b=\\mp\\frac{1}{2}$ , the '
                                           'function $e^{b\\cdot}f_{0X}$ is $\\alpha$ -Sobolev regular, '
                                           'while Assumption 4.5 requires that $f_{0X}$ is locally '
                                           '$\\upsilon$ -Hölder smooth, with envelope function $L_{0}$ '
                                           'satisfying the integrability condition ( 4.4 ).\n'
                                           'The model '
                                           '$f_{Y}=f_{\\varepsilon}\\ast(\\phi_{\\sigma}\\ast\\mu_{H})$ acts '
                                           'as an approximation scheme\n'
                                           'for automatic posterior rate adaptation to the global regularity '
                                           'of $f_{0Y}$ , without any knowledge of\n'
                                           'the regularity of $f_{0X}$ being used in the prior '
                                           'specification.\n'
                                           'We show that a rate-adaptive estimation procedure for Laplace '
                                           'mixtures\n'
                                           'can be obtained if the prior distribution is properly '
                                           'constructed, for instance, as a mixture of Laplace-normal '
                                           'convolutions, with\n'
                                           'an inverse-gamma type bandwidth and a Dirichlet process on the '
                                           'mixing distribution.',
                                   'evidence': [{'page': 17,
                                                 'location': 'Main-text naming context #S4.SS4.p2.1'}]}]}],
  'source_keywords': [{'context_id': 'S4.SS4.p2.1',
                       'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D20',
                       'source_text': 'Hölder smooth',
                       'label': 'Hölder smooth',
                       'kind': 'term'},
                      {'context_id': 'S4.SS4.p2.1',
                       'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D20',
                       'source_text': 'envelope function',
                       'label': 'Envelope function',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D4',
  'rank_group': 'all',
  'name': 'Ordinary smooth error densities',
  'lean_role': 'predicate',
  'type_shape': 'Ordinary-smooth error law: predicate over the measures/functions specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D4',
               'local_label': 'Assumption 3.1',
               'statement_original': 'The single coordinate error distribution '
                                     '$\\mu_{\\varepsilon}\\in\\mathscr{P}_{0}(\\mathbb{R})\\cap\\mathcal{P}_{1}(\\mathbb{R})$\n'
                                     'has Fourier transform\n'
                                     '$|\\hat{f}_{\\varepsilon}(t)|\\neq 0$, $t\\in\\mathbb{R}$.\n'
                                     'Furthermore, there exists $\\beta>0$ such that, for $l=0,\\,1$,\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\\[\n'
                                     '|r_{\\varepsilon}^{(l)}(t)|\\lesssim(1+|t|)^{\\beta-l},\\quad '
                                     't\\in\\mathbb{R}.\n'
                                     '\\]\n'
                                     '(3.2)',
               'relation': 'exact',
               'depends_on': ['D1', 'D29'],
               'evidence': [{'page': 7, 'location': 'Assumption 3.1'}],
               'highlight_symbols': ['|r_{\\varepsilon}^{(l)}(t)|\\lesssim(1+|t|)^{\\beta-l}'],
               'highlight_phrases': ['Assumption 3.1'],
               'source_kind': 'assumption',
               'source_heading': 'Assumption 3.1',
               'naming_context': [{'context_id': 'S1.p7.2',
                                   'text': 'where $\\mu_{0X}$ is the true mixing distribution, '
                                           '$\\Pi(\\cdot\\mid\\mathsf{Y}^{(n)})$ is the posterior '
                                           'distribution\n'
                                           'and $d(\\cdot,\\,\\cdot)$ is some semi-metric on probability '
                                           'measures.\n'
                                           'In their seminal papers [ 36 , 37 ] , the authors propose an '
                                           'elegant strategy to study posterior concentration rates which '
                                           'has\n'
                                           'been successful for a wide range of models and prior '
                                           'distributions under certain metrics or loss functions and, '
                                           'although more adapted to losses for direct problems in the form '
                                           '$d(f_{Y},\\,f_{0Y})$ , it\n'
                                           'has been applied also to inverse problems by [ 48 , 50 ] .\n'
                                           'This approach, however, does not seem to easily lead to sharp '
                                           'upper bounds on posterior convergence rates for $\\mu_{X}$ in '
                                           'deconvolution.\n'
                                           'An alternative approach is to obtain posterior convergence rates '
                                           'for the direct problem, i.e. , for $\\|f_{Y}-f_{0Y}\\|_{1}$ , '
                                           'and then combine them with an inversion inequality that\n'
                                           'translates an upper bound on $\\|f_{Y}-f_{0Y}\\|_{1}$ into an '
                                           'upper bound on $W_{1}(\\mu_{X},\\,\\mu_{0X})$ .\n'
                                           'Using such an inversion inequality, posterior contraction rates '
                                           'in $L^{p}$ -Wasserstein metrics, for $p\\geq 1$ , have been '
                                           'derived by [ 34 ] in the univariate case with the Laplace noise, '
                                           'when $\\mu_{0X}$ has bounded support. This result has been '
                                           'extended to the case of unbounded support by [ 58 ] , but the '
                                           'rates obtained in both papers are sub-optimal.\n'
                                           'Similarly, an inversion inequality is proposed by [ 47 ] in '
                                           'general mixture models, which is used to obtain $L^{2}$ '
                                           '-Wasserstein posterior convergence rates for the mixing '
                                           'distribution. However, in the deconvolution model with ordinary '
                                           'smooth error densities, the obtained rates are suboptimal. '
                                           'Therefore, the construction of Bayesian minimax-optimal '
                                           'procedures for estimating $\\mu_{0X}$ under Wasserstein metrics '
                                           'in a multivariate setting remains an open issue, with the '
                                           'sharpest results obtained in [ 34 , 58 ] . Recently, [ 60 ] '
                                           'studied density deconvolution under $W_{2}$ , subject to '
                                           'heteroscedastic errors as well as symmetry about zero and shape '
                                           'constraints, in particular, unimodality. They proved posterior '
                                           'consistency for Dirichlet location-mixture of gamma densities, '
                                           'but did not study convergence rates.',
                                   'evidence': [{'page': 3,
                                                 'location': 'Main-text naming context #S1.p7.2'}]}]}],
  'source_keywords': [{'context_id': 'S1.p7.2',
                       'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D4',
                       'source_text': 'ordinary smooth error densities',
                       'label': 'Ordinary smooth error densities',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D19',
  'rank_group': 'all',
  'name': 'Sobolev regular mixing density',
  'lean_role': 'predicate',
  'type_shape': 'Tilted Sobolev regularity: predicate over the measures/functions specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D19',
               'local_label': 'Assumption 4.4',
               'statement_original': 'There exists $\\alpha>0$ such that\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\n'
                                     '\\[\n'
                                     '\\forall\\,b=\\mp\\frac{1}{2},\\quad\\int_{\\mathbb{R}}|t|^{2\\alpha}|\\widehat{(e^{b\\cdot}f_{0X})}(t)|^{2}\\,\\mathrm{d}t<\\infty.\n'
                                     '\\]',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 17, 'location': 'Assumption 4.4'}],
               'highlight_symbols': ['\\widehat{(e^{b\\cdot}f_{0X})}'],
               'highlight_phrases': ['Assumption 4.4', 'Assumptions 4.3–4.5'],
               'source_kind': 'assumption',
               'source_heading': 'Assumption 4.4',
               'naming_context': [{'context_id': 'S4.SS4.p1.1',
                                   'text': 'In this section, we focus on the case where the sampling density '
                                           '$f_{0Y}$ is a mixture of\n'
                                           'Laplace densities with a Sobolev regular mixing density.\n'
                                           'We still consider the prior distribution $\\Pi$ induced on '
                                           '$\\mathscr{F}$ by the product measure '
                                           '$\\mathscr{D}_{H_{0}}\\otimes\\Pi_{\\sigma}$ for the parameter '
                                           '$(\\mu_{H},\\,\\sigma)$ of '
                                           '$f_{Y}=f_{\\varepsilon}\\ast(\\phi_{\\sigma}\\ast\\mu_{H})$ ,\n'
                                           'with a standard Laplace error density $f_{\\varepsilon}$ . Let '
                                           'the corresponding posterior distribution $\\Pi(\\cdot\\mid '
                                           'Y^{(n)})$ be based on i.i.d. observations '
                                           '$Y_{1},\\,\\ldots,\\,Y_{n}$ from $f_{0Y}=f_{\\varepsilon}\\ast '
                                           'f_{0X}$ , which is a Laplace mixture with mixing density '
                                           '$f_{0X}$ satisfying the following conditions.',
                                   'evidence': [{'page': 17,
                                                 'location': 'Main-text naming context #S4.SS4.p1.1'}]}]}],
  'source_keywords': [{'context_id': 'S4.SS4.p1.1',
                       'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D19',
                       'source_text': 'Sobolev regular mixing density',
                       'label': 'Sobolev regular mixing density',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D6',
  'rank_group': 'all',
  'name': 'Superkernel',
  'lean_role': 'predicate',
  'type_shape': 'Flat-top kernel of type (a): predicate over the measures/functions specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D6',
               'local_label': '§3.1, kernel (a)',
               'statement_original': 'We consider $K\\in L^{1}(\\mathbb{R})\\cap L^{2}(\\mathbb{R})$, with '
                                     '$zK(z)\\in L^{1}(\\mathbb{R})$, such that\n'
                                     '\n'
                                     '(a)\n'
                                     '\n'
                                     'under Assumption 3.2, $K$ is symmetric\n'
                                     'with $\\hat{K}$ supported on $[-2,\\,2]$, while $\\hat{K}\\equiv 1$ on '
                                     '$[-1,\\,1]$;',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 9, 'location': '§3.1, kernel (a)'}],
               'highlight_symbols': ['\\hat{K}'],
               'highlight_phrases': ['as in (a)'],
               'source_kind': 'condition',
               'source_heading': 'Kernel condition (a)',
               'naming_context': [{'context_id': 'S6.SS1.p5.1',
                                   'text': '$\\bullet$ Case 2: smoothness Assumption 3.2 on $\\mu_{0X}$ is '
                                           'in force If Assumption 3.2 holds true, then $K\\in '
                                           'L^{1}(\\mathbb{R})\\cap L^{2}(\\mathbb{R})$ is taken to be a '
                                           'superkernel with $zK(z)\\in L^{1}(\\mathbb{R})$ and '
                                           '$\\int_{\\mathbb{R}}z^{2}|K(z)|\\,\\mathrm{d}z<\\infty$ when '
                                           '$d\\geq 2$ .\n'
                                           'Since $\\hat{K}\\equiv 1$ on $[-1,\\,1]$ , while '
                                           '$\\hat{K}\\equiv 0$ on $[-2,\\,2]^{c}$ ,\n'
                                           'by taking $\\hat{K}(\\cdot/2)$ the support reduces to '
                                           '$[-1,\\,1]$ .\n'
                                           'Note that, as $K$ need not be a probability density, the '
                                           'triangular inequality for the Wasserstein metric in ( 6.2 )\n'
                                           'does not necessarily hold. Nevertheless, by the inequality on '
                                           'the right-hand side of ( 2.4 ) and\n'
                                           'the representation of $W_{1}$ , when $d=1$ , as the $L^{1}$ '
                                           '-distance between distribution functions,\n'
                                           'we have',
                                   'evidence': [{'page': 24,
                                                 'location': 'Main-text naming context #S6.SS1.p5.1'}]}]}],
  'source_keywords': [{'context_id': 'S6.SS1.p5.1',
                       'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D6',
                       'source_text': 'superkernel',
                       'label': 'Superkernel',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D21',
  'rank_group': 'all',
  'name': 'Sobolev spaces',
  'lean_role': 'predicate',
  'type_shape': 'Isotropic Sobolev class S_d(α, L): predicate over the measures/functions specified in the '
                'source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D21',
               'local_label': '§2, Sobolev classes',
               'statement_original': 'For global estimation, we consider Sobolev spaces.\n'
                                     'For $\\bm{\\alpha}=(\\alpha_{1},\\,\\ldots,\\,\\alpha_{d})^{t}$, let '
                                     'the anisotropic Sobolev space $\\mathcal{S}_{d}(\\bm{\\alpha},\\,L)$ '
                                     'be defined as the class of integrable functions '
                                     '$f:\\,\\mathbb{R}^{d}\\rightarrow\\mathbb{R}$ satisfying\n'
                                     '\n'
                                     '\\[\n'
                                     '\\sum_{j=1}^{d}\\int_{\\mathbb{R}^{d}}|\\hat{f}(\\mathsf{t})|^{2}(1+t_{j}^{2})^{\\alpha_{j}}\\,\\mathrm{d}\\mathsf{t}\\leq '
                                     'L^{2}.\n'
                                     '\\]\n'
                                     '\n'
                                     'In the isotropic case, for $\\alpha_{1}=\\ldots=\\alpha_{d}=\\alpha$, '
                                     'we simply write $\\mathcal{S}_{d}(\\alpha,\\,L)$ and '
                                     '$\\mathcal{H}_{d}(\\alpha,\\,L)$.\n'
                                     'The Sobolev and Hölder spaces of dimension one are denoted by '
                                     '$\\mathcal{S}(\\alpha,\\,L)$ and $\\mathcal{H}(\\alpha,\\,L)$, '
                                     'respectively.',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 6, 'location': '§2, Sobolev classes'}],
               'variant_note': 'The class uses the sum of coordinate Fourier weights and an explicit radius '
                               'L; Theorem 5.1 uses equal coordinate exponents.',
               'highlight_symbols': ['\\mathcal{S}_{d}'],
               'highlight_phrases': ['isotropic'],
               'source_kind': 'definition',
               'source_heading': 'Definition'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D21',
                       'source_text': 'Sobolev spaces',
                       'label': 'Sobolev spaces',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D22',
  'rank_group': 'all',
  'name': 'Fourier transform · Infinitely differentiable',
  'lean_role': 'predicate',
  'type_shape': 'Bourgain flat bump τ: predicate over the measures/functions specified in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D22',
               'local_label': '§4.4.1, τ and equation (4.5)',
               'statement_original': 'where $|\\hat{\\tau}(x)|\\leq(16^{2}/15)e^{-\\sqrt{|x|/15}}$, '
                                     '$x\\in\\mathbb{R}$, is the Fourier transform of\n'
                                     '$\\tau:\\,\\mathbb{R}\\rightarrow[0,\\,1]$ defined in Theorem 25 of '
                                     '[6], p. 29, such that\n'
                                     '\n'
                                     '\\[\n'
                                     '\\tau(u)=\\left\\{\\begin{array}[]{ll}1,&\\quad\\text{if '
                                     '}|u|<1,\\\\[3.0pt]\n'
                                     '0,&\\quad\\text{if }|u|>17/15.\\end{array}\\right.\n'
                                     '\\]\n'
                                     '\n'
                                     'The function $\\tau$ is such that $\\hat{\\tau}$ is infinitely '
                                     'differentiable and\n'
                                     '\n'
                                     '\\[\n'
                                     '\\mbox{for any '
                                     '$i\\in\\mathbb{N}_{0}$,}\\quad|\\hat{\\tau}^{(i)}(x)|=O(|x|^{-\\nu})\\quad\\mbox{for '
                                     'large $|x|$ and every $\\nu>0$.}\n'
                                     '\\]\n'
                                     '(4.5)',
               'relation': 'exact',
               'depends_on': [],
               'evidence': [{'page': 18, 'location': '§4.4.1, τ and equation (4.5)'}],
               'highlight_symbols': ['\\tau', '\\hat{\\tau}'],
               'highlight_phrases': [],
               'source_kind': 'source_passage',
               'source_heading': 'Source passage'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D22',
                       'source_text': 'Fourier transform',
                       'label': 'Fourier transform',
                       'kind': 'term'},
                      {'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D22',
                       'source_text': 'infinitely differentiable',
                       'label': 'Infinitely differentiable',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D23',
  'rank_group': 'all',
  'name': 'Kernel type deconvolution estimator',
  'lean_role': 'definition',
  'type_shape': 'Deconvolution kernel estimator (f̃ₙ, μ̃ₙ): definition over the measures/functions specified '
                'in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D23',
               'local_label': '§5.2, Fourier deconvolution estimator',
               'statement_original': 'Let $b_{n}=n^{-1/(2\\beta d+1)}$ and define $\\tilde{f}_{n}$ as the '
                                     'inverse Fourier transform of\n'
                                     '$\\hat{K}_{b_{n}}^{\\otimes d}\\phi_{n}r_{\\varepsilon}^{\\otimes d}$, '
                                     'where '
                                     '$\\phi_{n}(\\mathsf{t}):=\\mathbb{P}_{n}(e^{\\imath\\mathsf{t}\\cdot\\mathsf{Y}})$ '
                                     'is the empirical characteristic function and the kernel '
                                     '$K=\\hat{\\tau}$ is defined in Section 4.4.1. In symbols,\n'
                                     '\n'
                                     '\\[\n'
                                     '\\tilde{f}_{n}(\\mathsf{x}):=\\frac{1}{(2\\pi)^{d}}\\int_{\\mathbb{R}^{d}}e^{-\\imath\\mathsf{t}\\cdot\\mathsf{x}}\\hat{K}_{b_{n}}^{\\otimes '
                                     'd}(\\mathsf{t})\\phi_{n}(\\mathsf{t})r_{\\varepsilon}^{\\otimes '
                                     'd}(\\mathsf{t})\\,\\mathrm{d}\\mathsf{t},\\quad\\mathsf{x}\\in\\mathbb{R}^{d}.\n'
                                     '\\]',
               'relation': 'exact',
               'depends_on': ['D29', 'D22'],
               'evidence': [{'page': 21, 'location': '§5.2, Fourier deconvolution estimator'}],
               'variant_note': 'μ̃ₙ is the signed measure with density f̃ₙ; it is not the final '
                               'probability-valued estimator μ̃₁ₙ.',
               'highlight_symbols': ['\\tilde{f}_{n}', '\\phi_{n}'],
               'highlight_phrases': [],
               'source_kind': 'definition',
               'source_heading': 'Definition',
               'naming_context': [{'context_id': 'S1.p6.1',
                                   'text': 'State-of-the-art results on Wasserstein convergence rates for '
                                           'univariate deconvolution models\n'
                                           'are given in [ 20 ] , where a minimum distance estimator of '
                                           '$\\mu_{0X}$ is constructed that attains optimal convergence '
                                           'rates\n'
                                           'under $W_{1}$ , when the error distribution is known and '
                                           'ordinary smooth of order $\\beta\\geq\\frac{1}{2}$ .\n'
                                           'In the multivariate case, minimax estimation under Wasserstein '
                                           'metrics has only been studied in the case where the distribution '
                                           'of the errors is\n'
                                           'supersmooth, see [ 21 ] . Convergence rates in the multivariate '
                                           'deconvolution model have been obtained by [ 12 ] under the '
                                           '$L^{2}$ -Wasserstein loss, but they lead to rather slow '
                                           'convergence rates. Until now, the question of minimax rates '
                                           'under $L^{p}$ -Wasserstein metrics in the multivariate '
                                           'deconvolution problem with ordinary smooth noise remains open. '
                                           'In this paper, we partially fill this gap by providing lower '
                                           'bounds (see Theorem 5.1 ) and proposing a kernel type '
                                           'deconvolution estimator which achieves the optimal rates, up to '
                                           'a log-factor, for any $d\\geq 1$ under the $1$ -Wasserstein '
                                           'distance, see Section 5 .',
                                   'evidence': [{'page': 3,
                                                 'location': 'Main-text naming context #S1.p6.1'}]}]}],
  'source_keywords': [{'context_id': 'S1.p6.1',
                       'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D23',
                       'source_text': 'kernel type deconvolution estimator',
                       'label': 'Kernel type deconvolution estimator',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}},
 {'interface_id': 'deconv-D24',
  'rank_group': 'all',
  'name': 'Max-sliced · Distance',
  'lean_role': 'predicate',
  'type_shape': 'Approximate max-sliced L¹ projection μ̃₁ₙ: predicate over the measures/functions specified '
                'in the source',
  'semantic_boundary': 'Use the exact paper-local statement and assumptions below; no proof-only '
                       'dependencies.',
  'members': [{'paper_id': 'aos-2024-v52-i04-p1691',
               'local_id': 'D24',
               'local_label': '§5.2, approximate projection',
               'statement_original': 'Since $\\tilde{f}_{n}$ is not necessarily non-negative and\n'
                                     '$F_{\\tilde{\\mu}_{n}}$ is not necessarily a distribution function,\n'
                                     'we define $\\tilde{\\mu}_{1n}$ to be the probability measure such that '
                                     'the corresponding distribution function\n'
                                     '$F_{\\tilde{\\mu}_{1n}}$ is, up to a term of order $O(n^{-1/2})$, the '
                                     'closest one\n'
                                     'to $F_{\\tilde{\\mu}_{n}}$ in the max-sliced $L^{1}$-distance, that '
                                     'is,\n'
                                     'for every $\\mu\\in\\mathcal{P}_{1}(\\mathbb{R}^{d})$,\n'
                                     '\n'
                                     '\\[\n'
                                     '\\sup_{\\mathsf{v}\\in\\mathbb{S}^{d-1}}\\|F_{\\tilde{\\mu}_{n,\\mathsf{v}}}-F_{\\tilde{\\mu}_{1n,\\mathsf{v}}}\\|_{1}\\leq\\sup_{\\mathsf{v}\\in\\mathbb{S}^{d-1}}\\|F_{\\tilde{\\mu}_{n,\\mathsf{v}}}-F_{\\mu_{\\mathsf{v}}}\\|_{1}+O(n^{-1/2}).\n'
                                     '\\]',
               'relation': 'exact',
               'depends_on': ['D1', 'D2', 'D23'],
               'evidence': [{'page': 21, 'location': '§5.2, approximate projection'}],
               'highlight_symbols': ['\\tilde{\\mu}_{1n}'],
               'highlight_phrases': ['max-sliced'],
               'source_kind': 'definition',
               'source_heading': 'Definition'}],
  'source_keywords': [{'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D24',
                       'source_text': 'max-sliced',
                       'label': 'Max-sliced',
                       'kind': 'term'},
                      {'paper_id': 'aos-2024-v52-i04-p1691',
                       'local_id': 'D24',
                       'source_text': 'distance',
                       'label': 'Distance',
                       'kind': 'term'}],
  'central_claim_uses': [],
  'dependencies': [],
  'theorem_explanations': {}}]
members={m['local_id']:m for x in interfaces for m in x['members']}
by_local={m['local_id']:x for x in interfaces for m in x['members']}

members['D1']['statement_original']='For $p'+members['D1']['statement_original'].split('For $p',1)[1]
members['D3']['statement_original']=members['D3']['statement_original'].split('\n\nFor $p=1$')[0]
members['D3']['evidence']=[dict(page=2,location='Section 1 — general Wasserstein distance and coupling definition')]
members['D21']['evidence']=[dict(page=6,location='Section 2 — anisotropic Sobolev space'),dict(page=7,location='Section 2 — isotropic notation')]
members['D7']['depends_on']=['D2']
members['D15']['depends_on']=['D14','D31','D9','D8']
members['D6']['depends_on']=['D32']
members['D8']['depends_on']=['D32']
members['D27']['depends_on']=['D30']
for lid in ['D5','D19','D21','D22','D29']:
    members[lid]['depends_on'].append('D32')
for lid in ['D18','D28']:
    members[lid]['relation']='distinct'
    members[lid]['variant_note']='Assumption 4.3 is univariate and global with rate 1+C0>1; Theorem 5.2 has an arbitrary positive exponential rate outside a compact set in dimension d. These conditions are not interchangeable.'
hell=members['D10']['statement_original'].split('Letting $Pf$')[0].strip()
members['D10']['statement_original']='Letting $Pf$'+members['D10']['statement_original'].split('Letting $Pf$')[1]
by_local['D10']['source_keywords']=[k for k in by_local['D10']['source_keywords'] if k['label']!='Hellinger distance']
by_local['D10']['name']='Kullback-Leibler type neighbourhood'
members['D10']['highlight_symbols']=[r'B_{\mathrm{KL}}(P;\,\epsilon^{2})']
members['D10']['highlight_phrases']=[]
members['D10']['source_heading']=members['D10']['local_label']='Section 2 — Kullback-Leibler type neighbourhood'

def new(lid,term,body,page,heading,symbols,shape):
    m=dict(paper_id=PID,local_id=lid,local_label=heading,source_heading=heading,source_kind='definition',
        statement_original=body,relation='exact',depends_on=[],evidence=[dict(page=page,location=heading)],
        highlight_symbols=symbols,highlight_phrases=[])
    x=dict(interface_id='deconv-'+lid,rank_group='all',name=term[0].upper()+term[1:],lean_role='definition',
        type_shape=shape,semantic_boundary=shape,members=[m],source_keywords=[dict(paper_id=PID,local_id=lid,
            source_text=term,label=term[0].upper()+term[1:],kind='term')],
        central_claim_uses=[],dependencies=[],theorem_explanations={})
    interfaces.append(x);members[lid]=m;by_local[lid]=x
new('D30','Hellinger distance',hell,6,'Section 2 — Hellinger distance',
    [r'd_{\mathrm{H}}(f_{P},\,f_{Q})'],'Hellinger norm without a 1/sqrt(2) factor; separate from the KL neighborhood.')
new('D31','Gaussian random variable',r'''We denote by $\phi(x)=(2\pi)^{-1/2}e^{-x^2/2}$, $x\in\mathbb R$, the density of a standard Gaussian random variable and by $\phi_{\mu,\sigma}(x)=(1/\sigma)\phi((x-\mu)/\sigma)$, $x\in\mathbb R$, its recentered and rescaled version.''',
    7,'Section 2 — Gaussian density and location-scale version',[r'\phi_{\mu,\sigma}(x)'],
    'Gaussian location-scale kernel. Later phi_sigma denotes its centered version; a positive scale is implicit.')
new('D32','Fourier transform',r'''For $f\in L^1(\mathbb R^d)$, let $\hat f(\mathsf t):=\int_{\mathbb R^d}e^{\imath\mathsf t\cdot\mathsf x}f(\mathsf x)\,\mathrm d\mathsf x$, $\mathsf t\in\mathbb R^d$, be its Fourier transform. When $d=1$, for $\alpha\ge0$ and $f\in L^1(\mathbb R)$ such that $\int_{\mathbb R}|t|^\alpha|\hat f(t)|\,\mathrm dt<\infty$, we define the $\alpha$th fractional derivative of $f$ as $D^\alpha f(x):=(2\pi)^{-1}\int_{\mathbb R}e^{-\imath tx}(-\imath t)^\alpha\hat f(t)\,\mathrm dt$, with $D^0f\equiv f$.''',
    6,'Section 2 — Fourier transform and fractional derivative',[r'\hat f(\mathsf t)',r'D^\alpha f(x)'],
    'Positive-exponent Fourier transform and inverse-transform fractional derivative. The complex-power branch is not specified in this passage.')

def naming(lid,terms,text,page):
    m=members[lid];m['naming_context']=[dict(context_id=lid+'/name',text=text,
        evidence=[dict(page=page,location='Source naming context for '+lid)])]
    by_local[lid]['source_keywords']=[dict(paper_id=PID,local_id=lid,source_text=t,
        label=t[0].upper()+t[1:],kind='term',context_id=lid+'/name') for t in terms]
    by_local[lid]['name']=' · '.join(k['label'] for k in by_local[lid]['source_keywords'])
naming('D9',['multivariate convolution model'],r'We observe a sample $\mathsf Y^{(n)}=(\mathsf Y_1,...,\mathsf Y_n)$ of $n$ i.i.d. random vectors $\mathsf Y_i$ of $\mathbb R^d$ from the multivariate convolution model $\mathsf Y_i=\mathsf X_i+\bm\varepsilon_i$ in (1.1), where the random vectors $\mathsf X_i$ are i.i.d. according to an unknown probability measure $\mu_{0X}$.',5)
naming('D4',['ordinary smooth error densities'],'Assumption 3.1 is satisfied for ordinary smooth error densities covering the following examples.',8)
naming('D5',['global Sobolev regularity'],r'With Assumption 3.2, instead, $f_{0X}$ is required to have global Sobolev regularity $\alpha$.',9)
naming('D6',['kernel'],r'To prove the inversion inequalities of Theorem 3.1 below we use a kernel whose choice depends on the type of regularity of $f_{0X}$.',9)
naming('D11',['entropy and remaining mass conditions','small ball prior probability estimate'],
    r'The entropy and remaining mass conditions, as well as the small ball prior probability estimate in (4.1), are satisfied for $\tilde\epsilon_n$ as in the statement.',18)
naming('D17',['scale parameter','prior distribution'],
    r'The first part of Assumption 4.2 on the scale parameter $\sigma$ of the Gaussian kernel has become common in the literature since the articles [62, 19, 44].',15)
by_local['D17']['source_keywords'][1].pop('context_id')
naming('D19',['Sobolev regular mixing density'],'In this section, we focus on the case where the sampling density $f_{0Y}$ is a mixture of Laplace densities with a Sobolev regular mixing density.',17)
naming('D20',['Hölder smooth','envelope function'],r'Assumption 4.4 requires that, for $b=\mp\frac12$, the function $e^{b\cdot}f_{0X}$ is $\alpha$-Sobolev regular, while Assumption 4.5 requires that $f_{0X}$ is locally $\upsilon$-Hölder smooth, with envelope function $L_0$ satisfying the integrability condition (4.4).',17)
naming('D23',['kernel type deconvolution estimator'],'Note that the rate obtained for the kernel type deconvolution estimator easily extends to any other ordinary smooth noise distribution under additional moment assumptions.',29)
naming('D24',['approximate minimizer'],r'Here, instead, we choose the estimator as an approximate minimizer over all distribution functions of the max-sliced $L^1$-distance.',21)
by_local['D3']['semantic_boundary']='General p-Wasserstein definition on finite-moment probability measures. The one-dimensional quantile/CDF identity is preserved separately as auxiliary source context.'
by_local['D10']['semantic_boundary']='KL neighborhood requiring both the first log-likelihood ratio moment and its raw second moment; not centered log variance. Hellinger is the separate D30 definition.'
by_local['D24']['semantic_boundary']='Probability-valued approximate minimizer of projected CDF L1 errors, with O(n^-1/2) slack uniformly over candidate measures. Signed raw-kernel CDFs require a signed-measure interpretation; existence and measurable selection are not supplied here.'

DESCRIPTIONS={
'D1':'Finite absolute pth moments and their bounded subclasses for p>=1. The underlying probability and absolute-continuity spaces are ambient source definitions, not moment assumptions on every measure.',
'D2':'One-dimensional projection of a finite-p-moment probability law along a unit vector. The corresponding density and CDF notation is inherited. Signed kernel projections require the separately recorded signed interpretation.',
'D3':'General p-Wasserstein distance on finite-moment probability laws, defined using couplings and the Euclidean cost. Its one-dimensional quantile/CDF formulas are auxiliary passages with the dimensional premise preserved.',
'D4':'Assumption 3.1: absolutely continuous error with first moment, nonvanishing Fourier transform, and reciprocal derivative growth for l=0,1. This is not the distinct Fourier-derivative decay hypothesis in Theorem 5.1.',
'D5':'Assumption 3.2: uniformly over unit projections, weighted Fourier L1 integrability and L1 fractional derivative control. It appears only in the additional-regularity branches of Theorems 3.1 and 4.1.',
'D6':'Kernel condition (a): integrable and square-integrable symmetric kernel with integrable first absolute weighted kernel and Fourier support [-2,2], equal to one on [-1,1]. This condition is separate from the definition of bias for a supplied kernel.',
'D7':'CDF convolution bias for a supplied rescaled kernel, including product-kernel projections. A kernel is an input to this definition; condition (a) is separately required by the relevant theorem branches. Signed kernels need not be probability measures.',
'D8':'The standard Laplace error law identified by Fourier transform (1+t^2)^(-1). Its ordinary-smooth order is beta=2 in the source. The general Fourier convention is D32.',
'D9':'Class of observation laws and densities obtained by convolution of an arbitrary signal law with the fixed iid-coordinate error product. Density/measure identification and the iid sampling model are retained as source conventions.',
'D10':'KL neighborhood with bounds on KL divergence and the raw second log-ratio moment. It is separate from Hellinger distance, now D30. Absolute continuity and log-ratio integrability conventions remain ambient.',
'D11':'Theorem 4.1 excerpt: moment-bounded observation-law sieve, packing entropy, prior outside mass, and KL small-ball mass. It is an assumption in Theorem 4.1 and an asserted conclusion in Theorems 4.2 and 4.4.',
'D12':'Posterior probability obtained by integrating iid mixture likelihoods against the prior on signal laws. The prior may depend on n; positive finite evidence is an implicit domain requirement. Later observation-law posteriors are induced pushforwards.',
'D14':'Named Dirichlet process law with finite positive base measure. This source passage specifies the prior family, not a new predicate or its finite-dimensional construction.',
'D15':'Product prior for independent Dirichlet mixing law and positive Gaussian scale, inducing a normal-mixture signal density and a Laplace-convolved observation density. Tail restrictions on the base measure and scale law are separate assumptions.',
'D16':'Assumption 4.1: continuous positive base density bounded above and below by exponential-power tails, globally on R. Theorems 4.3 and 4.5 strengthen iota>0 to iota>1.',
'D17':'Assumption 4.2: two-sided inverse-scale density bounds near zero and an exponential-power upper tail at infinity. Theorems 4.3 and 4.5 strengthen varpi>0 to varpi>1.',
'D18':'Two distinct original tail conditions indexed by a shared source keyword: global univariate rate 1+C0 in Assumption 4.3, versus arbitrary positive multivariate rate outside a compact set in Theorem 5.2. No equivalence is asserted.',
'D19':'Assumption 4.4: Sobolev Fourier square-integrability for both exponential tilts b=minus/plus one half. This is not the unweighted isotropic Sobolev ball or Assumption 3.2.',
'D20':'Assumption 4.5: pointwise Holder increments with an integrable envelope, plus an exponentially weighted envelope-ratio moment; preserve the dependence of R and the smallest integer m on alpha and upsilon.',
'D21':'Anisotropic Sobolev ball with sum of coordinate Fourier weights bounded by L^2, with its isotropic specialization. Theorem 5.1 uses its intersection with a bounded first-moment probability class.',
'D22':'Source-specified smooth cutoff tau and decay of its Fourier transform. The transition values are not supplied; the external construction is not imported. This passage supplies K=hat(tau) for the frequentist estimator.',
'D23':'Raw Fourier deconvolution estimator with bandwidth n^(-1/(2 beta d+1)), empirical characteristic function, product kernel and reciprocal error transform. Preserve the printed integral without adding a real-part operation or claiming nonnegativity.',
'D24':'Probability-valued approximate minimizer of projected CDF L1 errors, with O(n^-1/2) slack uniformly over candidate measures. Signed raw-kernel CDFs require a signed-measure interpretation; existence and measurable selection are not supplied here.',
'D25':'Couplings or transport plans with the specified two probability marginals, used in the Wasserstein definition.',
'D26':'KL divergence of Q from P, using expectation under P of log(f_P/f_Q). This is not a symmetric distance.',
'D27':'Packing number with pairwise separation at least epsilon; its metric may be Hellinger or L1. The metric symbol d is distinct from the dimension symbol.',
'D29':'Reciprocal of a nonvanishing error Fourier transform and its derivative notation. Differentiability and nonvanishing are explicit prerequisites; transform normalization comes from D32.',
'D30':'Hellinger norm without a 1/sqrt(2) factor; separate from the KL neighborhood.',
'D31':'Gaussian location-scale kernel. Later phi_sigma denotes its centered version; a positive scale is implicit.',
'D32':'Positive-exponent Fourier transform and inverse-transform fractional derivative. The complex-power branch is not specified in the source passage.'
}
for x in interfaces:
    lid=x['members'][0]['local_id']
    x['type_shape']=x['semantic_boundary']=DESCRIPTIONS[lid]
    x['lean_role']='hypothesis' if x['members'][0]['source_kind'] in ('assumption','condition','theorem_excerpt') else 'definition'
for lid,m in members.items():
    if m['source_heading'] in ('Definition','Source passage','Prior specification'):
        m['source_heading']=m['local_label']='Section '+(
            '1' if lid in ('D3','D25') else '4.2' if lid in ('D8','D14','D15') else
            '3.1' if lid in ('D7','D29') else '4.4.1' if lid=='D22' else
            '5.2' if lid in ('D23','D24') else '2')+' — '+by_local[lid]['name']

def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    for m in members.values():
        assert all(lid in members for lid in m['depends_on'])
    (ROOT/'interface-extraction.json').write_text(json.dumps(dict(paper_id=PID,interfaces=interfaces,
        review_status='source_passages_reviewed',retired_local_ids=['D13']),indent=2,ensure_ascii=False)+'\n')
    (ROOT/'source-passages.json').write_text(json.dumps(dict(paper_id=PID,members=list(members.values())),
        indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__':main()
