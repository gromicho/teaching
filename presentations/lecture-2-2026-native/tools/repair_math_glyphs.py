from pathlib import Path
ROOT=Path(r"C:\local\projects\modernize ABW\beamer\lecture-2-2026-native\slides\source-faithful")
repl={
"𝑤":r"\ensuremath{w}", "𝑥":r"\ensuremath{x}", "−":r"\ensuremath{-}",
"×":r"\ensuremath{\times}", "ℎ":r"\ensuremath{h}", "𝑧":r"\ensuremath{z}",
"…":r"\ldots{}", "𝑫":r"\ensuremath{\mathit{D}}", "𝒘":r"\ensuremath{\mathbf{w}}",
"𝒙":r"\ensuremath{\mathbf{x}}", "𝑇":r"\ensuremath{T}", "𝑎":r"\ensuremath{a}",
"𝑖":r"\ensuremath{i}", "≥":r"\ensuremath{\ge}", "𝑜":r"\ensuremath{o}",
"𝑗":r"\ensuremath{j}", "𝒙":r"\ensuremath{\mathbf{x}}", "𝜎":r"\ensuremath{\sigma}",
"𝑒":r"\ensuremath{e}", "Τ":r"\ensuremath{T}", "→":r"\ensuremath{\rightarrow}",
" ":" ", "":""
}
changed=0
for p in ROOT.glob('*.tex'):
    s=p.read_text(encoding='utf8')
    out=s
    for a,b in repl.items(): out=out.replace(a,b)
    if out!=s:
        p.write_text(out,encoding='utf8')
        changed+=1
print('Updated',changed,'slide sources')
