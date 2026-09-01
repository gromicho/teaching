# Shared ABW / AABW Beamer source

This directory is the canonical source for presentation components reused by
**Analytics for a Better World (ABW)** and
**Advanced Analytics for a Better World (AABW)**.

The shared layer contains only material that can be maintained without course-
specific assumptions:

- the `abwlecture` Beamer class and UvA/ABS visual components;
- the Dick den Hertog and Joaquim Gromicho introduction frames;
- technology trends, optimization progress, TSP, and impact examples;
- general Python, Jupyter, Colab, and AI-assistant guidance.

Each course deck remains responsible for its own title, administration,
teaching team, assessment, timetable, assignment instructions, and case
sequence. In particular, AABW's Feed Calculator slides and its two linked
videos remain in the AABW lecture source.

## Using the shared source

Set the root after loading the class, then input only the slides needed by the
course and in the course's own order:

```tex
\ABWSetSharedRoot{path/to/teaching/presentations/abw-shared}
\input{\ABWSharedRoot/slides/technology/internet-of-things.tex}
```

Shared slides use `\insertframenumber`; they do not carry ABW- or AABW-specific
page numbers. Assets are resolved through `\ABWSharedAsset{...}`.

## Multimedia policy

A shared multimedia slide should contain a stable online link, a clear visual
click target, and source attribution. Downloaded video files are not stored in
this public repository unless their licence explicitly permits redistribution.
Course-owned offline backups stay with the relevant local course deck.
