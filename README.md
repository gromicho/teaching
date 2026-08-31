# Teaching

Public teaching materials for **Analytics for a Better World (ABW)**, **Advanced Analytics for a Better World (AABW)** and **Heuristics** at the University of Amsterdam.

One repository, with folders for courses and foundations shared between them. Open notebooks in Colab and save your own working copy; no knowledge of Git is required. GitHub maintains the sources and their history, Colab runs notebooks, and Canvas organizes enrolled students, deadlines and approved releases.

## Start here

| Collection | What belongs here |
| --- | --- |
| [Foundations](foundations/README.md) | Python, data analysis, optimization and networks used across courses |
| [ABW](courses/abw/README.md) | Course exercises, preparation and assessment guidance |
| [AABW](courses/aabw/README.md) | Advanced cases and selected shared preparation |
| [Heuristics](courses/heuristics/README.md) | Course selections and shared network examples |

Datasets are maintained once in [data](data/README.md), supporting figures in `assets/`, and shared workbook utilities in `support/`. Do not duplicate a common notebook in a course folder; link to it.

**2026/27 is in preparation, not frozen.** The course manifests describe the developing selection. The teaching team will agree the final course edition and dates before distribution.

## Setup and quality checks

Use Colab's scientific libraries; do not install the full maintenance environment over them. Optimization notebooks retain only the relevant solver setup. See [setup and verification](docs/SETUP.md).

Routine checks execute 19 public offline notebooks in two environments: the maintenance baseline and the relevant library versions from Colab's published 2026.07 CPU snapshot. The optional street-network lesson and two solver-dependent WFP notebooks are explicitly excluded from that execution claim; their files and links are still checked. Jeff Kantor's [historical solver-installation notebook](archive/README.md) is preserved for reading and attribution only, and is never automatically executed. See the [catalogue](catalog.json) for each notebook's status.

Instructor solutions and instructor recovery archives are maintained in a **separate private repository**, never in a folder or branch here. The explicitly approved historical Jeff Kantor reference is not an instructor key and does not broaden that boundary. A public folder cannot provide private access. Canvas controls approved cohort releases.

See [maintenance](docs/MAINTENANCE.md), [migration and provenance](docs/MIGRATION.md), and [attribution and rights](NOTICE.md). Public availability does not imply a collection-wide licence.
