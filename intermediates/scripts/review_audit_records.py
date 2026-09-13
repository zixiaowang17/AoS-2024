#!/usr/bin/env python3
"""Checkpoint audit provenance and rendering checks without renewing source certification."""
import argparse,datetime,hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
CENSUS_SKILL=Path('skills/statistical-paper-census/scripts')
HTML_SKILL=Path('skills/statistical-census-html/scripts')
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--renderer-script-dir',type=Path,default=HTML_SKILL)
parser.add_argument('--output',type=Path,default=ROOT/'audit-record-review.json')
args=parser.parse_args()
HTML_SKILL=args.renderer_script_dir.resolve()
OUTPUT=args.output.resolve()
sys.path.insert(0,str(CENSUS_SKILL))
sys.path.insert(0,str(HTML_SKILL))
from refresh_progress import inspect_paper
import build_report

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(data):
    fd,name=tempfile.mkstemp(prefix='.audit-record-review-',dir=OUTPUT.parent)
    try:
        with os.fdopen(fd,'w') as f:
            f.write(json.dumps(data,indent=2,ensure_ascii=False)+'\n');f.flush();os.fsync(f.fileno())
        os.replace(name,OUTPUT)
    finally:Path(name).unlink(missing_ok=True)
def evidence_items(node):
    if isinstance(node,dict):
        if node.get('path'):yield node
        for value in node.values():yield from evidence_items(value)
    elif isinstance(node,list):
        for value in node:yield from evidence_items(value)
def main():
    corpus=json.loads((ROOT/'corpus.json').read_text())
    register={p['paper_id']:p for p in json.loads((REPO/'corpus/aos/2024/local-pdf-manifest.json').read_text())['papers']}
    out=OUTPUT
    old=json.loads(out.read_text()) if out.exists() else {}
    previous={p['paper_id']:p for p in old.get('papers',[])}
    data=dict(schema_version='aos-audit-record-review-v1',status='in_progress',checked_at=None,
        scope='All 113 corpus papers: current validation, registered source, pinned review artifacts, evidence files, reproduction evidence, and statement/highlight rendering.',
        limits='Automated checks retain or reject existing review provenance; they do not perform a new mathematical source review, establish equivalence, or certify a mathlib comparison. Corpus grouping review and final HTML checks remain separate.',
        renderer_sha256=digest(HTML_SKILL/'build_report.py'),preflight_sha256=digest(Path(__file__)),validator_hashes={p.name:digest(p) for p in CENSUS_SKILL.glob('*.py')},papers=[])
    for paper in corpus['papers']:
        pid=paper['paper_id'];folder=ROOT/'papers'/pid
        # Source resolution is required even when only reviewing retained audit records.
        resolved=subprocess.run([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),pid],capture_output=True,text=True)
        files={str(p.relative_to(folder)):digest(p) for p in [folder/'paper-audit.json',folder/'registered-source-review.json',folder/'ranked-interfaces.json',folder/'theorem-inventory.json',folder/'evidence/rebuild-check.json'] if p.is_file()}
        # Include current evidence bytes and scripts so a previously passed row
        # cannot survive an edited/deleted image, changed extractor or new check.
        referenced={}
        for name in ['paper-audit.json','registered-source-review.json']:
            path=folder/name
            if path.is_file():
                doc=json.loads(path.read_text())
                for item in evidence_items(doc):
                    target=folder/item['path']
                    referenced[str(target)]=digest(target) if target.is_file() else None
        files.update({str(p.relative_to(folder)):digest(p) for p in (folder/'scripts').glob('*.py')})
        fingerprint=hashlib.sha256(json.dumps([files,referenced,register[pid],data['renderer_sha256'],data['preflight_sha256'],data['validator_hashes']],sort_keys=True).encode()).hexdigest()
        prior=previous.get(pid)
        if prior and prior.get('fingerprint')==fingerprint and resolved.returncode==0 and prior.get('automated_status')=='passed':
            data['papers'].append(prior)
        else:
            row=dict(paper_id=pid,title=paper['title'],fingerprint=fingerprint,reviewed_artifact_hashes=files,record_errors=[],rendering_errors=[],reproduction_errors=[],source_review_renewed=False,release_review_status='pending')
            if resolved.returncode:row['record_errors'].append(resolved.stderr.strip() or resolved.stdout.strip())
            state=inspect_paper(paper,register[pid])
            row['source_audit_status']=state['status'];row['record_errors']+=state.get('errors',[])
            if state['status']=='complete':
                census=json.loads((folder/'ranked-interfaces.json').read_text())
                audit=json.loads((folder/'paper-audit.json').read_text())
                review=json.loads((folder/'registered-source-review.json').read_text())
                row.update(theorem_count=len(census['claims']),interface_count=len(census['interfaces']),source_member_count=sum(len(x['members']) for x in census['interfaces']))
                for name,record in audit.get('artifacts',{}).items():
                    path=folder/record.get('path',name)
                    if not path.is_file():row['record_errors'].append('Missing audited artifact: '+str(path))
                    elif record.get('sha256') and digest(path)!=record['sha256']:row['record_errors'].append('Changed audited artifact: '+str(path))
                evidence_paths=set()
                for item in evidence_items([audit.get('evidence',[]),review.get('evidence',[])]):
                    if isinstance(item,dict) and item.get('path'):
                        path=folder/item['path'];evidence_paths.add(str(path))
                        if not path.is_file():row['record_errors'].append('Missing review evidence: '+str(path))
                        elif item.get('sha256') and digest(path)!=item['sha256']:row['record_errors'].append('Changed review evidence: '+str(path))
                row['evidence_files_checked']=len(evidence_paths)
                if not evidence_paths:row['record_errors'].append('Review records contain no inspectable evidence file paths.')
                reproduction_ref=review.get('reproduction_check',{})
                rebuild=folder/reproduction_ref.get('path','evidence/rebuild-check.json')
                row['reproduction_evidence_path']=str(rebuild.relative_to(folder))
                if not (folder/'scripts/rebuild.py').is_file():row['reproduction_errors'].append('Missing per-paper rebuild entrypoint.')
                if not rebuild.is_file():row['reproduction_errors'].append('Missing saved full-content reproduction check.')
                else:
                    report=json.loads(rebuild.read_text())
                    if reproduction_ref.get('sha256') and digest(rebuild)!=reproduction_ref['sha256']:
                        row['reproduction_errors'].append('Reproduction evidence differs from its registered review hash.')
                    comparisons=report.get('comparisons',[])
                    if len(comparisons)!=6:row['reproduction_errors'].append('Reproduction does not cover all six content JSONs.')
                    for comparison in comparisons:
                        path=folder/comparison['artifact']
                        if not path.is_file() or not comparison.get('matches_saved_bytes') or digest(path)!=comparison.get('saved_sha256') or comparison.get('saved_sha256')!=comparison.get('regenerated_sha256'):
                            row['reproduction_errors'].append('Stale or failed reproduction: '+comparison['artifact'])
                for claim in census['claims']:
                    try:build_report.render_statement(claim['statement_original'])
                    except Exception as error:row['rendering_errors'].append(dict(claim_id=claim['claim_id'],error=str(error)))
                for interface in census['interfaces']:
                    try:
                        build_report.verify_highlights(dict(census,interfaces=[interface]))
                        for explanation in interface['theorem_explanations'].values():build_report.render_statement(explanation['text'])
                    except Exception as error:row['rendering_errors'].append(dict(interface_id=interface['interface_id'],error=str(error)))
                ambient=folder/'ambient-prerequisites.json'
                if ambient.is_file():
                    a=json.loads(ambient.read_text());row['source_issues']=len(a.get('source_issues',[]));row['unresolved_prerequisites']=a.get('unresolved_external_prerequisites',[])
                row['automated_status']='needs_repair' if any(row[k] for k in ['record_errors','rendering_errors','reproduction_errors']) else 'passed'
            else:row['automated_status']='pending_paper_census'
            row['record_errors']=list(dict.fromkeys(row['record_errors']))
            row['checked_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
            data['papers'].append(row)
        data['checked_at']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        data['counts']={k:sum(p['automated_status']==k for p in data['papers']) for k in ['passed','needs_repair','pending_paper_census']}
        data['processed_papers']=len(data['papers'])
        save(data)
        row=data['papers'][-1]
        print(json.dumps(dict(paper_id=pid,status=row['automated_status'],record_errors=len(row.get('record_errors',[])),rendering_errors=len(row.get('rendering_errors',[])),reproduction_errors=len(row.get('reproduction_errors',[])))),flush=True)
    data['status']='automated_pass_complete' if data['counts']['passed']==113 else 'repairs_or_pending_work'
    save(data)
    print(json.dumps(dict(counts=data['counts'],release_complete=False)),flush=True)
if __name__=='__main__':main()
