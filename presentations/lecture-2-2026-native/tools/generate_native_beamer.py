from __future__ import annotations

import json
import math
import re
from pathlib import Path


ROOT = Path(r"C:\local\projects\modernize ABW")
OUT = ROOT / "beamer" / "lecture-2-2026-native"
META = OUT / "powerpoint-objects.json"
TEMPLATE_META = OUT / "powerpoint-template-objects.json"
TABLE_META = OUT / "powerpoint-table-dimensions.json"
TEX = OUT / "lecture-2-2026-native.tex"

SLIDE_W = 960.0
SLIDE_H = 540.0

PORTRAIT_OVERRIDES = {
    (4, "001"): "assets/portraits/dick.jpg",
    (5, "001"): "assets/portraits/joaquim.jpg",
    (6, "002"): "assets/portraits/anh.jpg",
    (7, "002"): "assets/portraits/lars.jpg",
    (8, "001"): "assets/portraits/mats.jpg",
    (9, "002"): "assets/portraits/nicole.jpg",
}

PERSON_SLIDE_INPUTS = {
    4: r"\input{slides/people/04-dick-den-hertog.tex}",
    5: r"\input{slides/people/05-joaquim-gromicho.tex}",
    6: r"\input{slides/people/06-do-quynh-anh-ngo.tex}",
    7: r"\input{slides/people/07-lars-boon.tex}",
    8: r"\input{slides/people/08-mats-van-der-vlugt.tex}",
    9: r"\input{slides/people/09-nicole-guarnieri.tex}",
}

NATIVE_SLIDE_INPUTS = {
    2: "slides/learning/02-what-you-will-learn.tex",
    3: "slides/learning/03-learning-journey.tex",
    10: "slides/learning/10-lectures-coordination.tex",
    11: "slides/learning/11-tutorials-table.tex",
    13: "slides/learning/13-assessment.tex",
    15: "slides/learning/15-four-jobs-of-analytics.tex",
    17: "slides/learning/17-vaccination-diagnostic.tex",
    22: "slides/learning/22-data-calculations.tex",
    23: "slides/learning/23-small-data-big-calculations.tex",
    24: "slides/learning/24-combinatorial-growth.tex",
    25: "slides/learning/25-enablers.tex",
    26: "slides/learning/26-four-vs.tex",
    27: "slides/learning/27-world-events.tex",
    28: "slides/learning/28-datafication.tex",
    29: "slides/learning/29-iot-update.tex",
    32: "slides/learning/32-predictive-algorithms.tex",
    33: "slides/learning/33-prescriptive-speedup.tex",
    35: "slides/learning/35-tsp-milestones.tex",
    36: "slides/learning/36-two-sides.tex",
    38: "slides/learning/38-model-risks.tex",
    39: "slides/learning/39-deployment-risks.tex",
    48: "slides/learning/48-python-part-goals.tex",
    49: "slides/learning/49-hands-on.tex",
    50: "slides/learning/50-why-python.tex",
    51: "slides/learning/51-python-and-ai.tex",
    52: "slides/learning/52-notebook-environment.tex",
    53: "slides/learning/53-colab-browser.tex",
    54: "slides/learning/54-open-notebook.tex",
    55: "slides/learning/55-colab-responsibility.tex",
    56: "slides/learning/56-without-colab.tex",
    57: "slides/learning/57-learning-python.tex",
    58: "slides/learning/58-self-study.tex",
    59: "slides/learning/59-weekly-assignments.tex",
    60: "slides/learning/60-find-codegrade.tex",
    61: "slides/learning/61-completing-codegrade.tex",
    62: "slides/learning/62-submitting-codegrade.tex",
    63: "slides/learning/63-codegrade-feedback.tex",
    65: "slides/learning/65-daughter-driving.tex",
    66: "slides/learning/66-af447.tex",
    67: "slides/learning/67-taking-over.tex",
    68: "slides/learning/68-training-simulators.tex",
    69: "slides/learning/69-why-learn-python.tex",
    70: "slides/learning/70-part-two-recap.tex",
    71: "slides/learning/71-part-one-recap.tex",
}

PORTRAIT_OVERRIDES = {}
SOURCE_CREDITS = {
    40: (
        r"\ABWArtCredit{Official artwork: \href{https://www.un.org/sustainabledevelopment/news/communications-material/}"
        r"{United Nations Sustainable Development Goals communications materials}. Follow the UN usage guidance for non-UN entities.}"
    ),
}


def fmt(value: float) -> str:
    if abs(value) < 0.0005:
        value = 0.0
    return f"{value:.3f}".rstrip("0").rstrip(".")


def tex_escape(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\x0b", "\n")
    text = text.strip("\n")
    text = text.replace("---", "—").replace("--", "–")
    replacements = {
        "\\": r"\textbackslash{}",
        "{": r"\{",
        "}": r"\}",
        "$": r"\$",
        "&": r"\&",
        "#": r"\#",
        "_": r"\_",
        "%": r"\%",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(ch, ch) for ch in text).replace("\n", r"\\")


URL_RE = re.compile(r"https?://[^\s]+")


def tex_text(text: str) -> str:
    """Escape text and make intact URL tokens clickable."""
    pieces: list[str] = []
    cursor = 0
    for match in URL_RE.finditer(text):
        pieces.append(tex_escape(text[cursor : match.start()]))
        raw = match.group(0)
        trail = ""
        while raw and raw[-1] in ".,;)":
            trail = raw[-1] + trail
            raw = raw[:-1]
        url_arg = raw.replace("%", r"\%")
        pieces.append(r"\href{" + url_arg + r"}{\nolinkurl{" + raw + "}}")
        pieces.append(tex_escape(trail))
        cursor = match.end()
    pieces.append(tex_escape(text[cursor:]))
    return "".join(pieces)


def color_name(value: str | None) -> str:
    if not value or not value.startswith("#"):
        return "c000000"
    return "c" + value[1:].upper()


def font_command(name: str | None) -> str:
    lookup = {
        "Times New Roman": r"\TimesNR",
        "Calibri": r"\CalibriFont",
        "Arial": r"\ArialFont",
        "Helvetica": r"\HelveticaFont",
    }
    return lookup.get(name or "", r"\TimesNR")


def style_text(paragraph: dict, override_text: str | None = None) -> str:
    font = paragraph.get("font") or {}
    size = float(font.get("size") or 18.0)
    leading = max(size * 1.12, size + 1.0)
    declarations = [
        font_command(font.get("name")),
        rf"\fontsize{{{fmt(size)}}}{{{fmt(leading)}}}\selectfont",
        rf"\color{{{color_name(font.get('color'))}}}",
    ]
    if font.get("bold"):
        declarations.append(r"\bfseries")
    if font.get("italic"):
        declarations.append(r"\itshape")
    text = tex_text(paragraph.get("text", "") if override_text is None else override_text)
    if font.get("underline") and text:
        text = r"\underline{" + text + "}"
    align = {1: r"\raggedright", 2: r"\centering", 3: r"\raggedleft", 4: r"\justifying"}.get(
        int(paragraph.get("alignment") or 1), r"\raggedright"
    )
    level = max(1, int(paragraph.get("level") or 1))
    bullet = bool(paragraph.get("bullet"))
    prefix = ""
    if bullet:
        indent = 10.0 + 18.0 * (level - 1)
        prefix = rf"\hspace*{{{fmt(indent)}bp}}\makebox[12bp][l]{{\textbullet}}"
    elif level > 1:
        prefix = rf"\hspace*{{{fmt(18.0 * (level - 1))}bp}}"
    if not text:
        return "{" + "".join(declarations) + rf"\vphantom{{Ag}}\par}}"
    return "{" + "".join(declarations) + align + " " + prefix + text + r"\par}"


def box_text(obj: dict, output_number: int | None = None) -> str:
    paragraphs = obj.get("paragraphs") or []
    if not paragraphs:
        return ""
    margins = obj.get("margins") or {}
    valid_margin = lambda v: isinstance(v, (int, float)) and -1 < float(v) < 100
    ml = float(margins.get("left") or 0.0) if valid_margin(margins.get("left")) else 0.0
    mr = float(margins.get("right") or 0.0) if valid_margin(margins.get("right")) else 0.0
    mt = float(margins.get("top") or 0.0) if valid_margin(margins.get("top")) else 0.0
    mb = float(margins.get("bottom") or 0.0) if valid_margin(margins.get("bottom")) else 0.0
    x = float(obj.get("left") or 0.0) + ml
    y = float(obj.get("top") or 0.0) + mt
    w = max(1.0, float(obj.get("width") or 1.0) - ml - mr)
    h = max(1.0, float(obj.get("height") or 1.0) - mt - mb)
    if w < 400 and any("http" in str(paragraph.get("text", "")) for paragraph in paragraphs):
        w = max(w, min(600.0, SLIDE_W - x - 35.0))
    vertical = int(obj.get("verticalAnchor") or 1)
    inner = "c" if vertical == 3 else ("b" if vertical == 4 else "t")
    body_parts = []
    for index, paragraph in enumerate(paragraphs):
        replacement = None
        if output_number is not None and int(obj.get("placeholderType") or 0) == 13:
            replacement = str(output_number)
        body_parts.append(style_text(paragraph, replacement))
    rotation = -float(obj.get("rotation") or 0.0)
    rotate_opt = f",rotate={fmt(rotation)}" if abs(rotation) > 0.01 else ""
    return (
        rf"\node[anchor=north west,inner sep=0pt,outer sep=0pt{rotate_opt}] "
        rf"at ({fmt(x)},-{fmt(y)}) "
        rf"{{\begin{{minipage}}[t][{fmt(h)}bp][{inner}]{{{fmt(w)}bp}}"
        r"\setlength{\parindent}{0pt}\setlength{\parskip}{0pt}"
        + "".join(body_parts)
        + r"\end{minipage}};"
    )


def draw_shape(obj: dict) -> list[str]:
    if int(obj.get("type") or 0) not in (1, 17, 14):
        return []
    if not obj.get("fillVisible") and not obj.get("lineVisible"):
        return []
    x = float(obj.get("left") or 0.0)
    y = float(obj.get("top") or 0.0)
    w = float(obj.get("width") or 0.0)
    h = float(obj.get("height") or 0.0)
    auto = int(obj.get("autoShapeType") or 0)
    fill = color_name(obj.get("fillColor"))
    line = color_name(obj.get("lineColor"))
    opacity = 1.0 - min(1.0, max(0.0, float(obj.get("fillTransparency") or 0.0)))
    weight = max(0.2, float(obj.get("lineWeight") or 0.75))
    options = []
    if obj.get("fillVisible"):
        options.extend([f"fill={fill}", f"fill opacity={fmt(opacity)}"])
    else:
        options.append("fill=none")
    if obj.get("lineVisible"):
        options.extend([f"draw={line}", f"line width={fmt(weight)}bp"])
        if int(obj.get("lineDash") or 1) not in (0, 1):
            options.append("dashed")
    else:
        options.append("draw=none")
    if int(obj.get("beginArrow") or 1) > 1 and int(obj.get("endArrow") or 1) > 1:
        options.append("{Stealth}-{Stealth}")
    elif int(obj.get("beginArrow") or 1) > 1:
        options.append("{Stealth}-")
    elif int(obj.get("endArrow") or 1) > 1:
        options.append("-{Stealth}")
    opt = ",".join(options)
    rotation = -float(obj.get("rotation") or 0.0)
    if auto == 9:
        return [
            rf"\draw[{opt},rotate around={{{fmt(rotation)}:({fmt(x+w/2)},-{fmt(y+h/2)})}}] "
            rf"({fmt(x+w/2)},-{fmt(y+h/2)}) ellipse [x radius={fmt(w/2)}bp,y radius={fmt(h/2)}bp];"
        ]
    if auto == -2 or (w < 8 and h > 8):
        return [rf"\draw[{opt}] ({fmt(x)},-{fmt(y)}) -- ({fmt(x+w)},-{fmt(y+h)});"]
    rotate = f",rotate={fmt(rotation)}" if abs(rotation) > 0.01 else ""
    return [
        rf"\node[anchor=north west,minimum width={fmt(w)}bp,minimum height={fmt(h)}bp,inner sep=0pt,{opt}{rotate}] "
        rf"at ({fmt(x)},-{fmt(y)}) {{}};"
    ]


def draw_asset(obj: dict, source_slide: int) -> str:
    asset = PORTRAIT_OVERRIDES.get((source_slide, str(obj.get("path")))) or obj.get("asset")
    if not asset:
        return ""
    path = str(asset).replace("\\", "/")
    x = float(obj.get("left") or 0.0)
    y = float(obj.get("top") or 0.0)
    w = float(obj.get("width") or 0.0)
    h = float(obj.get("height") or 0.0)
    rotation = -float(obj.get("rotation") or 0.0)
    rotate_opt = f",rotate={fmt(rotation)}" if abs(rotation) > 0.01 else ""
    return (
        rf"\node[anchor=north west,inner sep=0pt,outer sep=0pt{rotate_opt}] at ({fmt(x)},-{fmt(y)}) "
        rf"{{\includegraphics[width={fmt(w)}bp,height={fmt(h)}bp]{{{path}}}}};"
    )


def load_table_dimensions() -> dict[tuple[int, str], dict]:
    if not TABLE_META.exists():
        return {}
    records = json.loads(TABLE_META.read_text(encoding="utf-8-sig"))
    return {(int(item["slide"]), str(item["path"])): item for item in records}


TABLE_DIMENSIONS = load_table_dimensions()


def draw_table(obj: dict, source_slide: int) -> list[str]:
    table = obj.get("table")
    if not table:
        return []
    rows = int(table.get("rows") or 0)
    cols = int(table.get("columns") or 0)
    if not rows or not cols:
        return []
    x = float(obj.get("left") or 0.0)
    y = float(obj.get("top") or 0.0)
    w = float(obj.get("width") or 0.0)
    h = float(obj.get("height") or 0.0)
    dimensions = TABLE_DIMENSIONS.get((source_slide, str(obj.get("path")))) or {}
    raw_rows = dimensions.get("rowHeights") or [1.0] * rows
    raw_cols = dimensions.get("columnWidths") or [1.0] * cols
    row_heights = [h * float(value) / sum(raw_rows) for value in raw_rows]
    col_widths = [w * float(value) / sum(raw_cols) for value in raw_cols]
    row_tops = [y]
    for value in row_heights[:-1]:
        row_tops.append(row_tops[-1] + value)
    col_lefts = [x]
    for value in col_widths[:-1]:
        col_lefts.append(col_lefts[-1] + value)
    out: list[str] = []
    visited: set[tuple[int, int]] = set()
    for r, row in enumerate(table.get("cells") or []):
        for c, cell in enumerate(row):
            if (r, c) in visited:
                continue
            cell = row[c]
            span_h = 1
            span_v = 1
            cell_text = str(cell.get("text") or "")
            while (
                cell_text
                and c + span_h < len(row)
                and str(row[c + span_h].get("text") or "") == cell_text
                and row[c + span_h].get("fillColor") == cell.get("fillColor")
            ):
                span_h += 1
            cells = table.get("cells") or []
            while cell_text and r + span_v < len(cells):
                next_row = cells[r + span_v]
                if c + span_h > len(next_row):
                    break
                if not all(
                    str(next_row[column].get("text") or "") == cell_text
                    and next_row[column].get("fillColor") == cell.get("fillColor")
                    for column in range(c, c + span_h)
                ):
                    break
                span_v += 1
            for rr in range(r, r + span_v):
                for cc in range(c, c + span_h):
                    visited.add((rr, cc))
            cx = col_lefts[c]
            cy = row_tops[r]
            cw = sum(col_widths[c : c + span_h])
            rh = sum(row_heights[r : r + span_v])
            fill = color_name(cell.get("fillColor"))
            out.append(
                rf"\draw[fill={fill},draw=white,line width=1bp] ({fmt(cx)},-{fmt(cy)}) rectangle "
                rf"({fmt(cx+cw)},-{fmt(cy+rh)});"
            )
            pseudo = {
                "left": cx + 2,
                "top": cy + 1.5,
                "width": cw - 4,
                "height": rh - 3,
                "verticalAnchor": 3,
                "margins": {"left": 0, "right": 0, "top": 0, "bottom": 0},
                "paragraphs": cell.get("paragraphs") or [],
                "placeholderType": 0,
                "rotation": 0,
            }
            if pseudo["paragraphs"]:
                out.append(box_text(pseudo))
    return out


def is_visible(obj: dict) -> bool:
    x = float(obj.get("left") or 0.0)
    y = float(obj.get("top") or 0.0)
    w = float(obj.get("width") or 0.0)
    h = float(obj.get("height") or 0.0)
    return not (x >= SLIDE_W or y >= SLIDE_H or x + w <= 0 or y + h <= 0)


def render_object(obj: dict, source_slide: int, output_number: int) -> list[str]:
    if not is_visible(obj):
        return []
    if int(obj.get("type") or 0) == 6:
        result: list[str] = []
        for child in sorted(obj.get("children") or [], key=lambda item: int(item.get("z") or 0)):
            result.extend(render_object(child, source_slide, output_number))
        return result
    result = []
    result.extend(draw_shape(obj))
    if obj.get("table"):
        result.extend(draw_table(obj, source_slide))
    asset_cmd = draw_asset(obj, source_slide)
    if asset_cmd:
        result.append(asset_cmd)
    text_cmd = box_text(obj, output_number)
    if text_cmd:
        result.append(text_cmd)
    return result


def frame_start() -> list[str]:
    return [r"\begin{abwframe}"]


def frame_end() -> list[str]:
    return [r"\end{abwframe}"]


def native_input(path: str, output_number: int) -> str:
    return (
        rf"\begingroup\def\ABWInsertedPageNumber{{{output_number}}}"
        rf"\input{{{path}}}\endgroup"
    )


def render_source_frame(slide: dict, output_number: int) -> str:
    source_slide = int(slide["slide"])
    lines = frame_start()
    objects = sorted(slide.get("objects") or [], key=lambda item: int(item.get("z") or 0))
    # The exported SDG composite on source slide 40 has an opaque white top
    # margin. PowerPoint shows the title above it, so restore that visible
    # stacking order instead of allowing the bitmap to mask the title.
    if source_slide == 40:
        objects = sorted(
            objects,
            key=lambda item: (
                str(item.get("name") or "").lower().startswith(("title", "titel")),
                int(item.get("z") or 0),
            ),
        )
    for obj in objects:
        lines.extend(render_object(obj, source_slide, output_number))
    if source_slide in SOURCE_CREDITS:
        lines.append(SOURCE_CREDITS[source_slide])
    lines.extend(frame_end())
    return "\n".join(lines)


def tsp_footer(number: int) -> list[str]:
    return [
        r"\node[anchor=west,inner sep=0pt] at (56.693,-505.7) "
        r"{{\TimesNR\fontsize{10}{11}\selectfont\color{c7F7F7F}Analytics for a Better World, Lecture 1}};",
        rf"\node[anchor=east,inner sep=0pt] at (903.307,-505.7) "
        rf"{{\TimesNR\fontsize{{10}}{{11}}\selectfont\bfseries\color{{c7F7F7F}}{number}}};",
    ]


def tsp_question_frame(number: int) -> str:
    lines = [rf"\begin{{abwquestionframe}}{{Traveling Salesman Problem: question}}{{{number}}}"]
    lines += [
        r"\node[anchor=north west,inner sep=0pt] at (55,-135) "
        r"{\includegraphics[width=348bp,height=348bp]{assets/tsp/tsp-question.pdf}};",
        r"\node[anchor=north west,inner sep=0pt] at (455,-143) "
        r"{\begin{minipage}[t][292bp][t]{440bp}\TimesNR\fontsize{24}{29}\selectfont\raggedright{}"
        r"Visit every one of the 25 locations exactly once and return to the start.\par\vspace{18bp}"
        r"Suppose your laptop can evaluate \textbf{1,000,000 complete routes per second}.\par\vspace{18bp}"
        r"Fix one starting location and count a tour and its reverse only once.\par\vspace{24bp}"
        r"\color{cBC0031}\bfseries How long would brute force take?\par"
        r"\end{minipage}};",
        r"\node[anchor=west,inner sep=0pt] at (455,-465) "
        r"{{\TimesNR\fontsize{15}{18}\selectfont\color{c7F7F7F}25-node instance, seed 2023}};",
    ]
    lines += [r"\end{abwquestionframe}"]
    return "\n".join(lines)


def tsp_answer_frame(number: int) -> str:
    lines = [rf"\begin{{abwanswerframe}}{{Traveling Salesman Problem: answer}}{{{number}}}"]
    lines += [
        r"\node[anchor=north west,inner sep=0pt] at (55,-135) "
        r"{\includegraphics[width=348bp,height=348bp]{assets/tsp/tsp-answer.pdf}};",
        r"\node[anchor=north west,inner sep=0pt] at (455,-137) "
        r"{\begin{minipage}[t][310bp][t]{445bp}\TimesNR\fontsize{23}{28}\selectfont\raggedright{}"
        r"Unique routes:\par\vspace{5bp}"
        r"\hspace*{18bp}$N=\dfrac{24!}{2}=310{,}224{,}200{,}866{,}619{,}719{,}680{,}000$\par\vspace{17bp}"
        r"At $10^6$ routes per second:\par\vspace{5bp}"
        r"\hspace*{18bp}$t=\dfrac{N}{10^6}\approx 3.102\times10^{17}$ seconds\par\vspace{7bp}"
        r"\hspace*{18bp}$t\approx 9.83\times10^9$ years\par\vspace{21bp}"
        r"{\fontsize{31}{35}\selectfont\bfseries\color{cBC0031}About 9.8 billion years}\par\vspace{18bp}"
        r"{\fontsize{20}{24}\selectfont Optimal tour cost: \textbf{395}}\par"
        r"\end{minipage}};",
        r"\node[anchor=west,inner sep=0pt,text width=445bp] at (455,-472) "
        r"{{\TimesNR\fontsize{12}{14}\selectfont\color{c7F7F7F}Instance and formulation: "
        r"\href{https://mobook.github.io/MO-book/notebooks/04/08-traveling-salesman-problem.html}{MO-book TSP notebook}}};",
    ]
    lines += [r"\end{abwanswerframe}"]
    return "\n".join(lines)


def collect_colors(data: dict) -> set[str]:
    colors = {"#000000", "#FFFFFF", "#BC0031", "#7F7F7F"}

    def walk(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if key in {"fillColor", "lineColor", "color"} and isinstance(item, str) and item.startswith("#"):
                    colors.add(item.upper())
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(data)
    return colors


def preamble(colors: set[str]) -> str:
    definitions = "\n".join(
        rf"\definecolor{{{color_name(value)}}}{{HTML}}{{{value[1:]}}}" for value in sorted(colors)
    )
    return rf"""\documentclass{{abwlecture}}
{definitions}
\begin{{document}}
"""


def main() -> None:
    data = json.loads(META.read_text(encoding="utf-8-sig"))
    json.loads(TEMPLATE_META.read_text(encoding="utf-8-sig"))
    slides = {int(item["slide"]): item for item in data["slides"]}
    out_dir = OUT / "slides" / "source-faithful"
    out_dir.mkdir(parents=True, exist_ok=True)
    inputs: list[str] = []
    for output_number, source_number in enumerate(range(1, 84), 1):
        filename = f"{source_number:02d}-source-faithful.tex"
        (out_dir / filename).write_text(render_source_frame(slides[source_number], output_number) + "\n", encoding="utf-8")
        inputs.append(rf"\input{{slides/source-faithful/{filename}}}")
    head = preamble(collect_colors(data)).replace("\\begin{document}", "\\ABWSetFooterText{Analytics for a Better World, Lecture 2}\n\\begin{document}")
    TEX.write_text(head + "\n".join(inputs) + "\n\\end{document}\n", encoding="utf-8")
    print(f"Wrote {TEX}")
    print(f"Slide sources: {len(inputs)}")


if __name__ == "__main__":
    main()

