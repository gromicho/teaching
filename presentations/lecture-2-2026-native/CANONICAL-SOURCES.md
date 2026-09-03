# Lecture 2: native Beamer source

## Edit here

The editable source is `lecture-2-2026-native.tex`. It determines the order of the deck and loads 83 separate, editable frames from `slides/source-faithful/`.

The shared visual and layout class is `abwlecture.cls`, copied from the maintained Lecture 1 native deck. Local assets exported from the original PowerPoint are in `assets/source/`; the raw embedded PowerPoint media is retained in `assets/visuals/lecture-2/`.

## Visual authority

`../../slides/authoritative/Lecture 2 - 2025-2026.pptx` is the protected PowerPoint visual authority. It is retained unchanged. `powerpoint-objects.json`, `powerpoint-template-objects.json`, and `powerpoint-table-dimensions.json` record the source geometry used in this conversion.

## Current draft

`Lecture 2 - 2025-2026 - native draft.pdf` is the current compiled draft. The draft is fully native LaTeX: it does not place exported screenshots of complete PowerPoint slides.

## Known conversion work

Most text, shapes, tables, and individual exported images reproduce directly. Legacy mathematical glyphs have been translated into native LaTeX math. The remaining review task is typographic: restore subscripts, superscripts, and equation grouping in the perceptron and neural-network diagrams. Do not replace those whole slides with screenshots.

## Build

Run, from this directory:

```powershell
lualatex -interaction=batchmode -halt-on-error lecture-2-2026-native.tex
```

