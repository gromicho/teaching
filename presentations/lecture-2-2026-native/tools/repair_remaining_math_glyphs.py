from pathlib import Path
root=Path(r"C:\local\projects\modernize ABW\beamer\lecture-2-2026-native\slides\source-faithful")
repl={chr(0x1D431):r"\ensuremath{\mathbf{x}}", chr(0x1D437):r"\ensuremath{D}"}
for p in root.glob('*.tex'):
 s=p.read_text(encoding='utf8')
 for a,b in repl.items(): s=s.replace(a,b)
 p.write_text(s,encoding='utf8')
