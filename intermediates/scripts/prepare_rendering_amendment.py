"""Apply explicit, source-inspected rendering edits; keep their review pending."""
import argparse,ast,hashlib,json,shutil
from pathlib import Path
from review_rendering_amendment import differences
BASE=Path(__file__).resolve().parents[1]
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('configuration',type=Path);args=ap.parse_args()
    config=json.loads(args.configuration.read_text());root=BASE/'papers'/config['paper_id']
    files=config.get('content_files')
    if files is None:
        tree=ast.parse((root/'scripts/rebuild.py').read_text())
        files=next(ast.literal_eval(node.value) for node in tree.body
                   if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='ARTIFACTS' for t in node.targets))
    assert len(files)==6 and all((root/name).is_file() for name in files)
    recipe=root/config.get('recipe','scripts/extract_interfaces.py');text=recipe.read_text()
    assert '\ndef main():' in text
    if config.get('recipe_edits'):
        for edit in config['recipe_edits']:
            assert text.count(edit['before'])==1,edit['before']
            text=text.replace(edit['before'],edit['after'])
    history=root/'review-history/before-rendering-amendment';history.mkdir(parents=True)
    for p in root.glob('*.json'):shutil.copy2(p,history/p.name)
    shutil.copytree(root/'scripts',history/'scripts')
    fields=config['members']
    assert all(set(values)<= {'highlight_symbols','highlight_phrases','statement_original'} for values in fields.values())
    def amend(value):
        if isinstance(value,dict):
            result={k:amend(v) for k,v in value.items()}
            if value.get('local_id') in fields and 'statement_original' in value:
                result.update(fields[value['local_id']])
            return result
        if isinstance(value,list):return [amend(v) for v in value]
        return value
    changes=[]
    for name in files:
        before=json.loads((root/name).read_text());after=amend(before)
        changes.extend(dict(artifact=name,path=list(p),before=x,after=y) for p,x,y in differences(before,after))
        if before!=after:(root/name).write_text(json.dumps(after,indent=2,ensure_ascii=False)+'\n')
    insertion='\n# Source-inspected rendering amendment; see the explicit saved review plan.\n'
    for lid,values in fields.items():
        for key,value in values.items():insertion+=f'members[{lid!r}][{key!r}] = {value!r}\n'
    if config.get('recipe_edits'):
        recipe.write_text(text)
    else:
        at=text.index('\ndef main():');recipe.write_text(text[:at]+insertion+text[at:])
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    evidence=[dict(**item,sha256=digest(root/item['path'])) for item in config['evidence']]
    plan=dict(paper_id=root.name,history=str(history.relative_to(root)),
        source_pdf_sha256=json.loads((root/'theorem-inventory.json').read_text())['papers'][0]['pdf_sha256'],
        scope=config['scope'],finding=config['finding'],content_files=files,changes=changes,evidence=evidence,
        reproduction_check='evidence/rendering-review/rebuild-check.json')
    (root/'scripts/rendering-amendment.json').write_text(json.dumps(plan,indent=2,ensure_ascii=False)+'\n')
    (root/'scripts/review_rendering_amendment.py').write_text('"""Check the recorded source-backed rendering amendment."""\nimport subprocess,sys\nfrom pathlib import Path\nROOT=Path(__file__).resolve().parents[1]\nsubprocess.run([sys.executable,str(ROOT.parents[1]/"scripts/review_rendering_amendment.py"),ROOT.name],check=True)\n')
    print('Amendment prepared; source review and reproduction checks remain required.')
if __name__=='__main__':main()
