import json
from pathlib import Path
p=Path(__file__).resolve().parents[1] / 'powerpoint-objects.json'
d=json.loads(p.read_text(encoding="utf-8-sig"))
print("slides",d["slideCount"])
for s in d["slides"]:
    texts=[]
    for o in s.get("objects",[]):
        for q in o.get("paragraphs",[]):
            t=(q.get("text") or "").strip()
            if t: texts.append(t)
    print(f"{s['slide']:02d}: {' | '.join(texts)[:260]}")
