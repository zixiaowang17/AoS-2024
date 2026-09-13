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
WORK=Path('[local path omitted]')/ROOT.name
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
    main=(WORK/'main.tex').read_text()
    preamble=main.split(r'\begin{document}')[0]
    # Pandoc expands the author's macros; package/layout commands are irrelevant.
    macros=preamble.split(r'\title{')[0]
    combined=main
    for f in FILES:
        s=(WORK/f).read_text()
        combined=combined.replace(r'\input{'+f.removesuffix('.tex')+'}',s).replace(r'\input{'+f+'}',s)
    assert r'\input{' not in combined
    uncommented=re.sub(r'(?<!\\)%[^\n]*','',combined)
    envs=re.findall(r'\\begin\{theorem\}(.*?)\\end\{theorem\}',uncommented,re.S)
    assert len(envs)==4
    claims=[]
    for i,(raw,pages) in enumerate(zip(envs,[[19,20],[26],[35],[40]]),1):
        claims.append(dict(claim_id=ROOT.name+'/T'+str(i),paper_id=ROOT.name,claim_kind='theorem',
            label='Theorem '+str(i),source_order=i,statement_original=convert(raw,macros),
            evidence=[dict(page=p,location='Theorem '+str(i)+(' — continued' if j else '')) for j,p in enumerate(pages)]))
    paper=dict(paper_id=ROOT.name,title='Statistical-computational trade-offs in tensor PCA and related problems via communication complexity',
        version='arXiv:2204.07526v2',source_url='https://arxiv.org/pdf/2204.07526v2',pdf_pages=149,
        pdf_sha256=digest(WORK/'source.pdf'),main_text_last_pdf_page=45,
        main_text_boundary=dict(location='The main text ends after Remark 7 on PDF page 45. Appendix A, Proofs of the Information Bound and Geometric Inequalities, starts below it on the same page.',shared_page_with_appendix=True),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    write('theorem-inventory.json',dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims))
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)
    (ROOT/'evidence/main-only.tex').write_text(combined)
    (ROOT/'evidence/macros.tex').write_text(macros)
    for f in FILES:shutil.copy2(WORK/f,ROOT/'evidence'/f)
    for n in [19,20,26,35,40]:shutil.copy2(WORK/f'page-{n:02}.png',ROOT/'evidence'/f'page-{n:02}.png')
    d=fitz.open(WORK/'source.pdf');p=d[44]
    block=next(b for b in p.get_text('blocks') if 'Proofs of the Information Bound and Geometric Inequalities' in b[4])
    p.get_pixmap(matrix=fitz.Matrix(1.3,1.3),clip=fitz.Rect(0,0,p.rect.width,block[3]+1)).save(ROOT/'evidence/main-boundary.png')
    write('evidence/enumeration.json',dict(paper_id=ROOT.name,source_pdf_sha256=paper['pdf_sha256'],
        matching_tex_archive_sha256=digest(WORK/'source.tar.gz'),method='Four theorem environments in the expanded main source before the appendix command. Checked all four printed labels and complete statements against PDF pages 19-20, 26, 35 and 40.',
        theorems=[dict(label=c['label'],evidence=c['evidence'],original_tex=raw) for c,raw in zip(claims,envs)]))
    write('inventory-review.json',dict(paper_id=ROOT.name,status='complete',source_checked=True,validator_status='passed',
        reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),theorem_count=4,inventory_sha256=digest(ROOT/'theorem-inventory.json'),notes=[
            'Theorem 1 continues from page 19 onto page 20. Its resource inequality contains the ceiling of (k+1)/2.',
            'Theorem 2 uses memory exponent b, eta > 0 and threshold t^2/d^k; those are not replaced by the conventions of Theorems 1 and 3.',
            'Theorem 3 imposes small lambda, whereas Theorem 4 imposes small lambda squared. Both conditions and their distinct gamma thresholds are preserved.',
            'The final sentence of Theorem 4 retains its additional promises (31) and (30); their contents remain for interface extraction.',
            'An initial boundary search mistook a wrapped Appendix F reference on page 20 for an endpoint. The corrected boundary is the Appendix A heading below Remark 7 on page 45. During boundary location a heading scan reached pages 46-47 and an initial crop exposed the first appendix sentence. That material was not used for theorem extraction. Final evidence is cropped to the heading, and subsequent extraction is restricted to the main source.']))
    write('checkpoint.json',dict(paper_id=ROOT.name,stage='interface_extraction',inventory_status='validated',
        source_pdf_path=str(WORK/'source.pdf'),source_pdf_sha256=paper['pdf_sha256'],
        remaining_work='Extract the four problem definitions, memory-bounded resource model, NGCA assumptions and CCA promises; resolve main-text statement dependencies, then source-check and validate the census. Do not inspect appendices.'))
    print('Saved four complete Theorems; interface extraction remains.')

if __name__=='__main__':main()
