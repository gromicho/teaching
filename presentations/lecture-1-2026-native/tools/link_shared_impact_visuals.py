from pathlib import Path
base=Path(__file__).resolve().parents[2] / "abw-shared" / "slides" / "impact"
changes={
'sustainable-development-goals.tex': [(r'{\includegraphics[width=727.091bp,height=363.546bp]{\ABWSharedAsset{source/slide-40-object-002.png}}}',r'{\href{https://www.un.org/sustainabledevelopment/news/communications-material/}{\includegraphics[width=727.091bp,height=363.546bp]{\ABWSharedAsset{source/slide-40-object-002.png}}}}')],
'dike-heights.tex': [(r'{\includegraphics[width=461.713bp,height=340.464bp]{\ABWSharedAsset{source/slide-41-object-001.png}}}',r'{\href{https://doi.org/10.1287/opre.1110.1028}{\includegraphics[width=461.713bp,height=340.464bp]{\ABWSharedAsset{source/slide-41-object-001.png}}}}'),(r'{\includegraphics[width=425.579bp,height=340.464bp]{\ABWSharedAsset{source/slide-41-object-003.png}}}',r'{\href{https://doi.org/10.1287/opre.1110.1028}{\includegraphics[width=425.579bp,height=340.464bp]{\ABWSharedAsset{source/slide-41-object-003.png}}}}')],
'zero-hunger.tex': [(r'{\includegraphics[width=528.908bp,height=347.862bp]{\ABWSharedAsset{source/slide-42-object-003.png}}}',r'{\href{https://www.wfp.org/supply-chain}{\includegraphics[width=528.908bp,height=347.862bp]{\ABWSharedAsset{source/slide-42-object-003.png}}}}')],
'timor-leste.tex': [(r'{\includegraphics[width=456.862bp,height=334.942bp]{\ABWSharedAsset{source/slide-43-object-001.png}}}',r'{\href{https://github.com/gromicho/teaching/blob/main/foundations/cases/timor-leste-preparation.ipynb}{\includegraphics[width=456.862bp,height=334.942bp]{\ABWSharedAsset{source/slide-43-object-001.png}}}}')]
}
for name,pairs in changes.items():
 p=base/name;s=p.read_text(encoding='utf8')
 for old,new in pairs:
  if old not in s: raise RuntimeError(name+' expected asset not found')
  s=s.replace(old,new,1)
 p.write_text(s,encoding='utf8')
print('Linked evidence from four shared impact frames')
