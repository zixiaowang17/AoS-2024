"""Record the completed visual/source revalidation of the registered p0001 PDF."""
import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[3]
PID = ROOT.name

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

source = Path(subprocess.check_output([sys.executable, str(REPO/'scripts/resolve_paper_pdf.py'), PID], text=True).strip())
register = json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())
entry = next(p for p in register['papers'] if p['paper_id'] == PID)
census = json.loads((ROOT/'ranked-interfaces.json').read_text())
inventory = json.loads((ROOT/'theorem-inventory.json').read_text())
audit = json.loads((ROOT/'paper-audit.json').read_text())
assert digest(source) == entry['sha256'] == audit['source']['pdf_sha256']
pdf = fitz.open(source)
assert len(pdf) == entry['pdf_pages'] == 50
assert 'John C. Duchi' in pdf[0].get_text() and 'Feng Ruan' in pdf[0].get_text()
assert '1806.05756v3' in pdf[0].get_text()
headings=[]
for n in range(1,38):
    page=pdf[n-1]
    clip=fitz.Rect(0,0,612,290) if n==37 else page.rect
    for block in page.get_text('dict',clip=clip)['blocks']:
        for line in block.get('lines',[]):
            text=''.join(s['text'] for s in line['spans'])
            m=re.match(r'^Theorem\s+(\d+)\.',text)
            if m and 'BX' in line['spans'][0]['font']:
                headings.append((n,m[1]))
assert headings == [(12,'1'),(22,'2')]
assert [c['claim_id'] for c in inventory['claims']] == [PID+'/T1',PID+'/T2']
assert [(c['evidence'][0]['page'],c['label'].split()[-1]) for c in inventory['claims']] == headings
assert 'Proofs of non-private minimax results' in pdf[36].get_text(clip=fitz.Rect(0,280,612,318))
for n in [2,3,5,12,21,22]:
    assert (ROOT/'evidence/revalidation'/f'page-{n:02}.txt').read_bytes().decode('utf8') == pdf[n-1].get_text()
direct = {c['label']: set(c['depends_on']) for c in census['claims']}
assert direct == {'Theorem 1': {'D2','D3','D6','D7'},
                  'Theorem 2': {'D2','D3','D6','D8','D11','D12'}}
members={m['local_id']:m for x in census['interfaces'] for m in x['members']}
assert set(members) == {f'D{i}' for i in range(1,13)}
assert set(members['D3']['depends_on']) == {'D1','D2'}
assert set(members['D6']['depends_on']) == {'D1','D5'}
assert set(members['D7']['depends_on']) == {'D2','D4'}
assert set(members['D11']['depends_on']) == {'D9','D10'}
for name in ['theorem-inventory.json','ranked-interfaces.json']:
    assert digest(ROOT/name) == audit['artifacts'][name]['sha256']
    subprocess.run([sys.executable,'skills/statistical-paper-census/scripts/validate_census.py',str(ROOT/name)],check=True)
findings=[
    'The fixed local PDF is byte-identical to the prior reviewed arXiv:1806.05756v3. Its title and both authors match. No alternative source or abstract was substituted.',
    'Fresh PDF heading enumeration before the Appendix A boundary gives exactly Theorem 1 on page 12 and Theorem 2 on page 22. The ordinary-font Theorem 2 reference is excluded. The shared final main-text page is clipped above the appendix at y=295.51.',
    'Both complete original theorem bodies were compared against newly rendered registered-PDF pages. Theorem 1 retains the order-two epsilon-squared privacy class, c_conv values 1 and 2, prefactor 1/(4 c_conv), and radius 1/(2 sqrt(2 n epsilon^2)).',
    'Theorem 2 retains its one-dimensional L1-differentiable submodel, vector-valued theta, score and influence function, N independent of loss, all-n>=N assertion, prefactor 1/8, scale 1/(6 sqrt(n epsilon^2)), and exact score pairing divided by E0[|g|]. No omitted nonzero-score condition was silently added.',
    'D1 and D2 were checked on page 2: the data are iid before privatization, releases may depend on previous private releases, and loss is symmetric quasiconvex and zero at zero. Ambient theta and Q-composed-with-P are resolved in the surrounding source text.',
    'D3 and D4 were checked on page 3: the supremum over P1 precedes the infimum over estimator/channel; the risk is a two-point maximum, and variation distance is the supremum of event-probability differences.',
    'D5 and D6 were checked on page 5: Renyi divergence retains its alpha=1 limit and alpha=infinity convention; Definition 2 bounds divergence of history-conditioned kernels. Its printed history domain Z rather than Z^(i-1) remains unchanged and flagged in the existing note.',
    'D7 was checked on page 12: the loss sees half the parameter difference and the supremum uses the total-variation constraint. The nonprivate Hellinger modulus and nearby Corollary 4 are not imported into this theorem dependency.',
    'D8 and D9 were checked on page 21: L1 differentiability uses total variation of the signed-measure remainder o(|h|), and the tangent space is the closed linear span of its scores. Comparison with quadratic-mean differentiability supplies no extra hypothesis.',
    'D10, D11 and D12 were checked on page 22: derivative continuity is relative to the L1 tangent space, the influence function has L-infinity coordinates, and the theorem estimates a C1 scalar functional with scalar symmetric quasiconvex loss. The source L1/private-influence naming correspondence is explicit.',
    'Reviewed direct dependencies and recursive source paths give seven interfaces for Theorem 1 and ten for Theorem 2. In particular Theorem 2 has no modulus/variation-distance interface merely because earlier results motivate its proof.',
    'All twelve natural-language keyword names, original source identities, selectors and seventeen same-paper explanations were read against their passages and theorem occurrences. Original census and inventory bytes are unchanged. This is source/statement revalidation, not proof verification or published-version equivalence.'
]
evidence=[dict(page=n,path=f'evidence/revalidation/page-{n:02}.png',sha256=digest(ROOT/'evidence/revalidation'/f'page-{n:02}.png')) for n in [2,3,5,12,21,22]]
evidence.append(dict(page=37,path='evidence/revalidation/main-text-end.png',before_main_text_end=True,location='Main-text endpoint and appendix heading only; appendix body not used.',sha256=digest(ROOT/'evidence/revalidation/main-text-end.png')))
review=dict(schema_version='registered-paper-source-review-v1',paper_id=PID,status='complete',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),method='source_content_revalidation',registered_pdf_path=str(source),registered_pdf_sha256=entry['sha256'],registered_pdf_pages=len(pdf),source_version=audit['source']['version'],checks={k:True for k in ['theorem_inventory','original_statements','source_passages','dependencies','names_and_highlights']},reviewed_artifacts={name:digest(ROOT/name) for name in ['paper-audit.json','theorem-inventory.json','ranked-interfaces.json']},findings=findings,evidence=evidence)
(ROOT/'registered-source-review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
print('Registered-source content revalidation complete: 2 Theorems, 12 interfaces, 17 related connections; original artifacts unchanged.')
