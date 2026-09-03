import json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
man=json.loads((root/'assets/visuals/lecture-1/manifest.json').read_text())
tex='\n'.join(p.read_text(encoding='utf8',errors='ignore') for p in root.rglob('*.tex'))
by={}
for e in man:
    used=e['file'].replace('assets/visuals/lecture-1/','') in tex
    by.setdefault((e['source_slide'],e['source_slide_title'].strip()),[]).append((e['file'].split('/')[-1],used,e['attribution_status']))
for (s,t), xs in by.items():
    used=sum(v[1] for v in xs)
    print(f'{s:02}: {t[:52]:52}  {used}/{len(xs)} assets used')
    if used < len(xs): print('    unused:', ', '.join(x[0] for x in xs if not x[1]))
