"""Persist the completed source review after independent census validation."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
WORK=Path('[local path omitted]')/ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def main():
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'ranked-interfaces.json')],check=True)
    inv=json.loads((ROOT/'theorem-inventory.json').read_text())
    data=json.loads((ROOT/'ranked-interfaces.json').read_text())
    paper=inv['papers'][0]
    assert digest(WORK/'source.pdf')==paper['pdf_sha256']
    assert len(data['claims'])==3 and len(data['interfaces'])==22
    assert sum(len(x['members']) for x in data['interfaces'])==23
    assert sum(len(x['central_claim_uses']) for x in data['interfaces'])==18
    assert sum(len(x['related_theorems']) for x in data['interfaces'])==49
    for n in [3,4,5,6,7,8,9,10,11,12,14,18,19]:
        shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    artifacts={name:dict(path=name,sha256=digest(ROOT/name)) for name in [
        'theorem-inventory.json','unfinalized-census.json','ranked-interfaces.json',
        'source-passages.json','ambient-conventions.json','inventory-review.json']}
    evidence={p.name:dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in sorted((ROOT/'evidence').iterdir()) if p.is_file()}
    write('paper-audit.json',dict(schema_version='statistical-paper-audit-v1',paper_id=ROOT.name,
        status='complete',audit_kind='source_review',completed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        source=dict(pdf_path=str(WORK/'source.pdf'),source_url=paper['source_url'],version=paper['version'],
            pdf_sha256=paper['pdf_sha256'],pdf_pages=67,main_text_last_pdf_page=25,
            matching_tex_archive_sha256=digest(WORK/'source.tar.gz')),
        enumeration=dict(theorem_ids=[c['claim_id'] for c in inv['claims']],
            method='Enumerated all three uncommented mythm environments in the matching-version main source; scanned PDF pages 1-25 up to the Supplementary Material heading and visually checked pages 16 and 20 and the endpoint crop.',
            excluded_result_types=['Lemma','Proposition','Corollary'],supplementary_material_used=False),
        validation=dict(status='passed',validator=str(SKILL/'validate_census.py'),checks=[
            'The complete three-Theorem inventory was checked against PDF wording and formulas, then validated independently before extraction.',
            'All 23 extracted local source passages and five ambient passages were checked against the main-text PDF, including all subparts of Definitions 4.13, 5.2 and 5.4.',
            'A separate validator process checked the finalized census against its hash-pinned inventory and derived graph.',
            'All highlight selectors have exact source matches and each local member has a visible source-body or label selector.',
            'The 18 direct uses and 49 related-theorem paths were reviewed. Definition 4.2 parts 3 and 4 only enter Theorem 3 through its background knowledge; their consequences for ts-DMAGs are not turned into extra hypotheses of Theorems 1 and 2.']),
        counts=dict(theorems=3,interfaces=22,source_members=23,direct_theorem_uses=18,related_theorem_connections=49),
        source_notes=[
            'Source version is arXiv:2112.08417v2, dated 5 October 2023; no identity with publisher numbering is assumed.',
            'Theorems 1 and 2 print the time-index bound 0 <= t <= p, while Definitions 3.6/4.13 and Section 4.2 use the bound on tau. The printed theorem statements are preserved.',
            'Definition 3.4 does not impose a finite maximum edge lag; that restriction is not imported from the structural-process motivation.',
            'Section 3.3 explicitly separates causal interpretation from the graphical results. Stationary stochastic solutions, causal Markov and causal faithfulness are not added as theorem-statement dependencies.',
            'The directed mixed graph in Theorem 2 is not assumed ancestral or maximal. DMAG enters its dependency closure through the target ts-DMAG and projection definitions, not as an extra input hypothesis.',
            'Definition 4.13 provides its own complete construction. Standard canonical DAGs in Definition 4.11 are motivation and are not added as a dependency of that construction.',
            'Definition 4.13 retains both distinct latent-parent time shifts exactly as printed. It uses stationarified edges, not all edges of the input graph.',
            'Stationarification is defined for all four edge types, including circles, which is needed when Theorem 3 applies it to DPAGs.',
            'Repeating orientations requires agreement only when the shifted adjacency exists. Repeating ancestral relationships is a separate condition, not merged with it.',
            'All four background knowledges in Definition 5.4 remain distinct cases in their original source statement; no equivalence between them is inferred.',
            'Definition 5.3 comparisons, time series DPAGs from Definition 5.7, and Algorithm 1 are not needed to state these three Theorems. Lemmas and proof-only machinery are excluded from the theorem inventory.',
            'The source paragraph on projection switches from DAG G to D; this printed notation is preserved.'],
        unresolved_source_references=[
            dict(source='Definition 3.6 and Section 3.4',meaning='The full MAG latent-projection construction is cited to Zhang (2008a, pp. 1442-3), not reproduced in the main text.',action='Retain the cited construction, its input/output and stated preservation properties; do not invent a complete definition or inspect supplementary material.'),
            dict(source='Sections 3.3, 3.4 and 5.1',meaning='The full d-separation and m-separation path criteria are external; Markov equivalence is characterized by equal m-separations.',action='Archive the exact main-text characterization and flag the external separation criteria as unresolved source prerequisites.'),
            dict(source='Definition 5.2',meaning='An arbitrary background knowledge may leave an empty equivalence subclass; the main text does not give a total construction or existence convention for that case.',action='Preserve all four definition parts without adding an existence assertion. Theorem 3 restricts the background choices explicitly.')],
        ambient_resolution=[
            dict(notation='Graphs, adjacencies, skeletons, directed graphs, subgraphs, walks, paths, colliders, ancestry, time windows and lags',resolution='Original source conventions are archived in ambient-conventions.json. Ancestry includes the vertex itself; path length counts vertices as printed.'),
            dict(notation='M, G, D, time window p and reference time t',resolution='Bound in the original Theorems and resolved through Definitions 3.1, 3.4, 3.6 and the Section 4.2 notation. The unusual printed bound on t remains a source inconsistency.'),
            dict(notation='A, A^stat, A_to, A_ta, A_D and A_D^stat',resolution='Theorem 3 binds the pair by the three stated alternatives; Definition 5.4 supplies all four named Boolean restrictions.'),
            dict(notation='Ordinary integers, finite sets, Cartesian products, equality, set inclusion and Boolean functions',resolution='Ambient mathematical operations; no library-availability judgment is made.')],
        artifacts=artifacts,evidence=evidence,
        review_limits=['This records main-text statements and their dependencies, not a verification of the proofs.',
                       'Supplementary material was not read or used. Externally cited definitions remain explicitly unresolved.']))
    write('checkpoint.json',dict(paper_id=ROOT.name,stage='complete',inventory_status='validated',
        census_status='validated',source_pdf_path=str(WORK/'source.pdf'),source_pdf_sha256=paper['pdf_sha256'],
        remaining_work=None))
    print('Paper source review completed: 3 Theorems, 22 interfaces, 23 source members.')

if __name__=='__main__':main()
