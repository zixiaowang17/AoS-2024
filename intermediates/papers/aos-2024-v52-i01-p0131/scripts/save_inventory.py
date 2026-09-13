"""Independently reviewed main-text inventory of arXiv:2204.07526v2."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import fitz

ROOT=Path(__file__).resolve().parents[1]
PID=ROOT.name
REPO=ROOT.parents[3]
EVIDENCE_ROOT=ROOT/'evidence'
SKILL=Path('skills/statistical-paper-census/scripts')
FILES=['prelims.tex','tensorPCA.tex','ATPCA.tex','NGCA.tex','CCA.tex']
REFS={'ass: moment-matching':'1','ass: bounded-snr':'2','ass: locally-bounded-LLR':'3',
      'eq:kCCA-coordprior':'31','eq:kCCA-likelihood':'30'}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def convert(raw,macros):
    text=re.sub(r'(?<!\\)%[^\n]*','',raw)
    text=re.sub(r'\\label\{[^}]+\}','',text)
    text=re.sub(r'\\eqref\{([^}]+)\}',lambda m:'('+REFS[m[1]]+')',text)
    text=re.sub(r'\\ref\{([^}]+)\}',lambda m:REFS[m[1]],text)
    text=re.sub(r'\\begin\{align\*\}(.*?)\\end\{align\*\}',lambda m:r'\['+m[1].replace('&','').strip()+r'\]',text,flags=re.S)
    out=subprocess.run(['pandoc','-f','latex','-t','markdown','--wrap=none'],input=macros+'\n\\begin{document}\n'+text+'\n\\end{document}',text=True,capture_output=True,check=True).stdout.strip()
    out=out.replace(r'\bm',r'\boldsymbol')
    out=re.sub(r'\$\$(.*?)\$\$',lambda m:'\n\\[\n'+m[1]+'\n\\]\n',out,flags=re.S)
    assert '[^' not in out
    return out

def main():
    source=Path(subprocess.check_output([sys.executable,str(REPO/'scripts/resolve_paper_pdf.py'),PID],text=True).strip())
    assert digest(source)=='9f5ac87cf7baade850642cc6d947f457466296ede93e3d53840fb97f6432c434'
    assert digest(EVIDENCE_ROOT/'main-only.tex')=='30b090a3ed89378551abf007df2ca4f091b5dd77f1ec3f0cfc09b4833062f698'
    combined=(EVIDENCE_ROOT/'main-only.tex').read_text()
    macros=(EVIDENCE_ROOT/'macros.tex').read_text()
    assert r'\input{' not in combined
    uncommented=re.sub(r'(?<!\\)%[^\n]*','',combined)
    envs=re.findall(r'\\begin\{theorem\}(.*?)\\end\{theorem\}',uncommented,re.S)
    assert len(envs)==4
    claims=[]
    for i,(raw,pages) in enumerate(zip(envs,[[19,20],[26],[35],[40]]),1):
        claims.append(dict(claim_id=PID+'/T'+str(i),paper_id=PID,claim_kind='theorem',
            label='Theorem '+str(i),source_order=i,statement_original=convert(raw,macros),
            evidence=[dict(page=p,location='Theorem '+str(i)+(' — continued' if j else '')) for j,p in enumerate(pages)]))
    paper=dict(paper_id=PID,title='Statistical-computational trade-offs in tensor PCA and related problems via communication complexity',
        version='arXiv:2204.07526v2',source_url='https://arxiv.org/pdf/2204.07526v2',pdf_pages=149,
        pdf_sha256=digest(source),main_text_last_pdf_page=45,
        main_text_boundary=dict(location='The main text ends after Remark 7 on PDF page 45. Appendix A, Proofs of the Information Bound and Geometric Inequalities, starts below it on the same page.',shared_page_with_appendix=True),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    write('theorem-inventory.json',dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims))
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)

if __name__=='__main__':main()
