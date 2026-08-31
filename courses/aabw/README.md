# Advanced Analytics for a Better World (AABW)

**2026/27 is in preparation, not frozen.** The [edition manifest](editions/2026-2027.json) records the developing selection; Canvas supplies the required sequence and release dates.

## Shared preparation

Python, descriptive and predictive analytics, Caroline, Alice, Elizabeth and network examples now live in [foundations](../../foundations/README.md), outside any advanced-course folder. The [Feed Calculator](../../foundations/cases/feed-calculator-preparation.ipynb) and [Timor-Leste](../../foundations/cases/timor-leste-preparation.ipynb) preparation is shared with ABW.

## Advanced cases

| Notebook | Open | Check profile |
| --- | --- | --- |
| [Sudoku — optimization-model starter](notebooks/sudoku/starter.ipynb) | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/courses/aabw/notebooks/sudoku/starter.ipynb) | core |
| [WFP Syria — robust optimization companion](notebooks/wfp-syria/robust-optimization-companion.ipynb) | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/courses/aabw/notebooks/wfp-syria/robust-optimization-companion.ipynb) | specialist |
| [WFP Syria — data exploration and model starter](notebooks/wfp-syria/starter-data-visualization.ipynb) | [Colab](https://colab.research.google.com/github/gromicho/teaching/blob/main/courses/aabw/notebooks/wfp-syria/starter-data-visualization.ipynb) | specialist |

The two WFP notebooks were migrated with their data and helper links. They are marked **specialist**: a complete solver-dependent execution review is still required and they are not included in the routine execution claim. The robust conic model needs a suitable solver; no licence or credentials are embedded.

The Sudoku starter was recovered from the course exercise export supplied on 31 August 2026. It retains the original puzzle and prepares the input without installing a solver or revealing a solution. The older exercise variants and research material from that export are preserved in the private instructor recovery archive; they do not replace maintained notebooks here. The supplied Feed Calculator and Syria workbooks matched the canonical datasets exactly, so no duplicate data copies were added.

The external [Gurobi food-supply example](https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/food_program/food_supply.ipynb) remains maintained by its original authors. It is not an imported or routinely tested notebook in this collection.

Datasets now have one home in [data](../../data/README.md), including WFP Syria. Instructor solutions remain in a separate private repository. [Jeff Kantor's historical solver-installation notebook](../../archive/README.md) is preserved publicly with his attribution, for reading rather than current setup or automatic execution. The predecessor GitHub repositories have been removed; see [migration](../../docs/MIGRATION.md), [setup](../../docs/SETUP.md) and [maintenance](../../docs/MAINTENANCE.md).
