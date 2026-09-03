# Lecture 1: authoritative sources and maintenance

## Edit here

The authoritative, editable lecture deck is [lecture-1-2026-native.tex](lecture-1-2026-native.tex). It assembles the deck from the local `slides/` folder, the local `assets/` library, and the maintained shared library at `../abw-shared`.

The presentation class is [../abw-shared/abwlecture.cls](../abw-shared/abwlecture.cls). Course destinations are centralized in [course-links.tex](course-links.tex). Do not edit a compiled PDF.

## PowerPoint authority

The protected visual reference is [Lecture 1a - 2026.pptx](references/Lecture%201a%20-%202026.pptx). It is the authority for the legacy PowerPoint composition and visual intent. It is not the editable source of this Beamer delivery and is deliberately left unmodified.

Named visual assets extracted or restored from that PowerPoint live in `assets/visuals/lecture-1/`. Their provenance and reuse status are in [GRAPHIC-ATTRIBUTION-REGISTER.md](GRAPHIC-ATTRIBUTION-REGISTER.md), [ASSET-PROVENANCE.txt](ASSET-PROVENANCE.txt), and `assets/visuals/lecture-1/ATTRIBUTIONS.md`.

## Build and release routine

From this directory, compile with:

```powershell
lualatex -interaction=batchmode -halt-on-error lecture-1-2026-native.tex
```

Inspect the resulting PDF. When approved, publish the reviewed PDF as a release or course-delivery artifact. Keep generated PDFs and rendered page checks out of the source tree.

## Support tools

Reusable asset/audit utilities are in `tools/`. They are retained as provenance and maintenance tools; they are not required for an ordinary LaTeX compilation.

## What is retained

- `lecture-1-2026-native.tex` (within the private `teaching` repository), `../abw-shared/abwlecture.cls`, `course-links.tex`
- `slides/`, `assets/`, and the shared ABW source library
- attribution and visual-comparison records
- the original PowerPoint reference
- the current delivery PDF

Generated output is intentionally excluded from version control.
