"""Create a human-readable, attributed visual library from the Lecture 1 PPTX.

The source PPTX and assets/source are retained unchanged.  This script creates
copies under assets/visuals/lecture-1 and a machine-readable manifest that
records the original deck, slide and object for every visual.
"""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "powerpoint-objects.json"
SOURCE_DECK = ROOT / "references" / "Lecture 1a - 2026.pptx"
DESTINATION = ROOT / "assets" / "visuals" / "lecture-1"

# Use a specific name when the visual has a well-known teaching role.  Other
# figures receive a stable title-based name instead of an opaque object number.
KNOWN_NAMES = {
    "slide-01-object-005.png": "welcome-amsterdam-canal",
    "slide-01-object-006.png": "analytics-for-a-better-world-logo",
    "slide-04-object-001.png": "dick-den-hertog-portrait",
    "slide-05-object-001.png": "joaquim-gromicho-portrait",
    "slide-13-object-005.png": "casio-fx-82ms-calculator",
    "slide-14-object-003.png": "informs-analytics-definition-logo",
    "slide-15-object-001.png": "gartner-analytics-ascendancy-model",
    "slide-16-object-002.png": "covid-descriptive-analytics-case",
    "slide-17-object-003.png": "vaccination-perceptions-survey",
    "slide-18-object-003.png": "covid-predictive-analytics-case",
    "slide-19-object-003.png": "covid-prescriptive-analytics-case",
    "slide-26-object-002.png": "four-vs-of-data",
    "slide-27-object-002.png": "large-hadron-collider-events",
    "slide-27-object-003.png": "walmart-daily-transactions",
    "slide-28-object-004.png": "internet-in-one-minute-2023",
    "slide-29-object-002.png": "internet-of-things-connected-devices",
    "slide-30-object-002.png": "historical-data-storage-cost",
    "slide-31-object-002.png": "moores-law-transistors",
    "slide-35-object-002.png": "tsp-100-million-stars",
    "slide-35-object-003.png": "tsp-42-city-tour",
    "slide-35-object-004.png": "tsp-13509-city-tour",
    "slide-35-object-007.png": "tsp-24978-city-tour",
    "slide-35-object-009.png": "tsp-532-city-tour",
    "slide-40-object-002.png": "un-sustainable-development-goals",
}


def slug(text: str) -> str:
    text = text.lower().replace("&", "and")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "untitled-visual"


def slide_text(slide: dict) -> str:
    paragraphs: list[str] = []
    for obj in slide["objects"]:
        for paragraph in obj.get("paragraphs") or []:
            if paragraph.get("text"):
                paragraphs.append(paragraph["text"])
    return " ".join(paragraphs)


def title_for(slide: dict) -> str:
    for obj in slide["objects"]:
        if obj.get("placeholderType") == 1:
            text = " ".join(p.get("text", "") for p in obj.get("paragraphs") or [])
            if text:
                return text
    return f"slide {slide['slide']}"


def attribution_for(slide: dict) -> tuple[str, str]:
    text = slide_text(slide)
    snippets = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if re.search(r"\bsource\b|https?://|www\.", sentence, re.IGNORECASE)
    ]
    if snippets:
        return (" ".join(snippets), "inherited-from-original-slide")
    return (
        "No source line was present on the original slide. Confirm creator, licence and preferred attribution before reuse outside this course.",
        "needs-rights-review",
    )


def main() -> None:
    catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    DESTINATION.mkdir(parents=True, exist_ok=True)
    manifest: list[dict] = []
    used_names: set[str] = set()

    for slide in catalogue["slides"]:
        title = title_for(slide)
        attribution, attribution_status = attribution_for(slide)
        image_index = 0
        for obj in slide["objects"]:
            asset = obj.get("asset")
            if not asset:
                continue
            image_index += 1
            source = ROOT / asset
            if not source.exists():
                continue
            base = KNOWN_NAMES.get(source.name, f"slide-{slide['slide']:02d}-{slug(title)}-visual-{image_index:02d}")
            filename = f"{base}{source.suffix.lower()}"
            suffix = 2
            while filename in used_names:
                filename = f"{base}-{suffix}{source.suffix.lower()}"
                suffix += 1
            used_names.add(filename)
            target = DESTINATION / filename
            shutil.copy2(source, target)
            manifest.append(
                {
                    "id": f"lecture-1-s{slide['slide']:02d}-o{obj['object']:03d}",
                    "file": target.relative_to(ROOT).as_posix(),
                    "source_deck": str(SOURCE_DECK),
                    "source_slide": slide["slide"],
                    "source_slide_title": title,
                    "source_object": obj["name"],
                    "original_asset": asset,
                    "attribution": attribution,
                    "attribution_status": attribution_status,
                }
            )

    (DESTINATION / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [
        "# Lecture 1 visual library",
        "",
        "These are named copies of individual embedded PowerPoint graphics. The original PPTX and `assets/source` are retained unchanged.",
        "",
        "| File | Original slide | Attribution status |",
        "|---|---:|---|",
    ]
    lines.extend(f"| `{item['file'].split('/')[-1]}` | {item['source_slide']} | {item['attribution_status']} |" for item in manifest)
    (DESTINATION / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Created {len(manifest)} named visual files in {DESTINATION}")


if __name__ == "__main__":
    main()
