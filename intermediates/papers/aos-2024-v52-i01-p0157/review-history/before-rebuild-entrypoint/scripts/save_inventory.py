"""Source-checked inventory of every main-text Theorem in arXiv:2208.06685v3."""
import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
WORK=Path('[local path omitted]')/ROOT.name
SKILL=Path('skills/statistical-paper-census/scripts')
REFS={'as:newexch':'2','as:noties':'3','as:exchangeable0':'1','emppvalues':'10',
      'constrainedg':'8','equnew':'11','thm:FDRBONuS':'3.4','equboundsadaptive':'14',
      'def:Di':'13','as:indep':'4','equ-marg':'5','equLR':'18','th:SCextended':'4.1',
      'equNP':'27','equDelta':'28','equfgamma':'17','equlconstraint':'29',
      'rejectsalot':'30','highpower':'31','equGbar':'33','powerBONuSstar':'36',
      'funcdelta':'34','diffscore':'35'}
RECORDS=[('3.3',[9]),('3.4',[10]),('3.6',[10,11]),('4.1',[13]),('5.1',[18]),('5.4',[20])]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')

def convert(raw,macros):
    raw=re.sub(r'(?<!\\)%[^\n]*','',raw)
    raw=re.sub(r'\\eqref\{([^}]+)\}',lambda m:'('+REFS[m[1]]+')',raw)
    raw=re.sub(r'\\ref\{([^}]+)\}',lambda m:REFS[m[1]],raw)
    def display(m):
        rows=re.split(r'\\\\',m[2])
        results=[]
        for row in rows:
            labels=re.findall(r'\\label\{([^}]+)\}',row)
            assert len(labels)==1,labels
            body=re.sub(r'\\label\{[^}]+\}','',row).replace('&','').strip()
            results.append(r'\['+body+r'\tag{'+REFS[labels[0]]+r'}\]')
        return '\n\n'.join(results)
    raw=re.sub(r'\\begin\{(align|equation)\}(.*?)\\end\{\1\}',display,raw,flags=re.S)
    raw=re.sub(r'\\label\{[^}]+\}','',raw)
    # Printed (i)/(ii) subpart labels, not generated bullet labels.
    raw=raw.replace(r'\begin{itemize}','').replace(r'\end{itemize}','')
    raw=re.sub(r'\\item\[([^]]+)\]',lambda m:'\n\n'+m[1]+' ',raw)
    out=subprocess.run(['pandoc','-f','latex','-t','markdown','--wrap=none'],input=macros+'\n\\renewcommand{\\rev}[1]{#1}\n\\begin{document}\n'+raw+'\n\\end{document}',text=True,capture_output=True,check=True).stdout.strip()
    out=re.sub(r'\$\$(.*?)\$\$',lambda m:'\n\\[\n'+m[1]+'\n\\]\n',out,flags=re.S)
    out=out.replace(r'\(i\)','(i)').replace(r'\(ii\)','(ii)')
    assert 'reference-type' not in out and '[^' not in out
    return out

def main():
    tex=(WORK/'main-only.tex').read_text()
    clean=re.sub(r'(?<!\\)%[^\n]*','',tex)
    macros=clean.split(r'\begin{document}')[0]
    envs=re.findall(r'\\begin\{theorem\}(.*?)\\end\{theorem\}',clean,re.S)
    assert len(envs)==6
    claims=[]
    for order,((number,pages),raw) in enumerate(zip(RECORDS,envs),1):
        claims.append(dict(claim_id=ROOT.name+'/T'+number,paper_id=ROOT.name,claim_kind='theorem',label='Theorem '+number,source_order=order,
            statement_original=convert(raw,macros),evidence=[dict(page=p,location='Theorem '+number+(' — continued' if j else '')) for j,p in enumerate(pages)]))
    paper=dict(paper_id=ROOT.name,title='Adaptive novelty detection with false discovery rate guarantee',version='arXiv:2208.06685v3',source_url='https://arxiv.org/pdf/2208.06685v3',pdf_pages=58,pdf_sha256=digest(WORK/'source.pdf'),main_text_last_pdf_page=27,
        main_text_boundary=dict(location='Conclusion and acknowledgements end on page 25, followed by references through page 27. Appendix A starts on page 28; only its heading was used to confirm the boundary.',shared_page_with_appendix=False),
        intake_review=dict(status='complete',theorem_ids=[c['claim_id'] for c in claims],zero_theorems_confirmed=False))
    write('theorem-inventory.json',dict(schema_version='statistical-theorem-inventory-v1',scope=dict(theorem_scope='main_text_only'),papers=[paper],claims=claims))
    subprocess.run([sys.executable,str(SKILL/'validate_census.py'),str(ROOT/'theorem-inventory.json')],check=True)
    (ROOT/'evidence/main-only.tex').write_text(tex)
    (ROOT/'evidence/macros.tex').write_text(macros)
    for n in ['page-09.png','page-10.png','page-11.png','page-13.png','page-18.png','page-20.png','page-27.png','appendix-heading.png']:shutil.copy2(WORK/n,ROOT/'evidence'/n)
    write('evidence/enumeration.json',dict(paper_id=ROOT.name,source_pdf_sha256=paper['pdf_sha256'],matching_tex_archive_sha256=digest(WORK/'source.tar.gz'),
        method='Enumerated six uncommented theorem environments before the appendix command and checked full statements and printed numbers against the main-text PDF. Proof headings, citations, corollaries and lemmas are not theorem entries.',
        theorems=[dict(label=c['label'],evidence=c['evidence'],original_tex=raw) for c,raw in zip(claims,envs)],appendix_content_used=False))
    write('inventory-review.json',dict(paper_id=ROOT.name,status='complete',source_checked=True,validator_status='passed',reviewed_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        theorem_count=6,inventory_sha256=digest(ROOT/'theorem-inventory.json'),notes=[
            'Theorem 3.6 spans pages 10 and 11; its setting reference to Theorem 3.4 and the distribution (13) are preserved.',
            'Theorem 4.1 prints higher TPR and explicitly assumes the exact-mFDR threshold exists. Neither wording nor existence condition is silently changed.',
            'Theorem 5.1 retains both subparts, the constants depending only on delta, every condition in (29), and both conclusions (30) and (31).',
            'Theorem 5.4 retains the event R, the complement on the inclusion event, the enlarged alpha-prime and the further statement for oracle BH p-values.',
            'The appendix was excluded; its heading alone confirmed the endpoint.']))
    write('checkpoint.json',dict(paper_id=ROOT.name,stage='interface_extraction',inventory_status='validated',source_pdf_path=str(WORK/'source.pdf'),source_pdf_sha256=paper['pdf_sha256'],
        remaining_work='Extract all relevant main-text definitions and Assumptions 1-5, empirical p-values and AdaDetect/BH constructions, PRDS, conditional distribution D_i, likelihood-ratio score, ERM risks and optimizers, oracle tail and discrepancy quantities. Resolve the setting references without copying theorem conclusions as assumptions. Source-check and validate the completed census.'))
    print('Saved six complete main-text Theorems; interface extraction remains.')

if __name__=='__main__':main()
