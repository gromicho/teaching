from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EDITION = json.loads((ROOT / "course-edition.json").read_text(encoding="utf-8"))
EXPECTED_ID = str(EDITION["canvas_course_id"])
URL_RE = re.compile(r"https://canvas\.uva\.nl/courses/(\d+)[^\s}\]]*")


def main() -> None:
    problems: list[str] = []
    links_file = ROOT / "course-links.tex"
    links_text = links_file.read_text(encoding="utf-8")

    found = URL_RE.findall(links_text)
    if not found:
        problems.append("course-links.tex contains no Canvas course URL")
    wrong = sorted({course_id for course_id in found if course_id != EXPECTED_ID})
    if wrong:
        problems.append(f"course-links.tex contains old Canvas course IDs: {', '.join(wrong)}")

    for tex in sorted(ROOT.rglob("*.tex")):
        if tex == links_file:
            continue
        text = tex.read_text(encoding="utf-8")
        hard_coded = URL_RE.findall(text)
        if hard_coded:
            rel = tex.relative_to(ROOT)
            problems.append(
                f"{rel} hard-codes Canvas course URL(s); use a macro from course-links.tex"
            )

    main_tex = (ROOT / "lecture-1-2026-native.tex").read_text(encoding="utf-8")
    if r"\input{course-links.tex}" not in main_tex:
        problems.append("lecture source does not input course-links.tex")

    if problems:
        raise SystemExit("\n".join(f"ERROR: {item}" for item in problems))

    print(
        f"Canvas link configuration OK: {EDITION['academic_year']}, "
        f"course {EXPECTED_ID}, verified {EDITION['verified']}"
    )


if __name__ == "__main__":
    main()
