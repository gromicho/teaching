# Shared datasets

The fruit table, height–weight teaching table, Feed Calculator and Timor-Leste workbooks, and three WFP Syria workbooks are consolidated without changing their bytes. [manifest.json](manifest.json) records the source and SHA-256 of the maintained datasets. These match the existing public teaching copies; older URLs are retained for now, but corrections should be made here.

Dataset provenance beyond the source teaching repositories is incomplete. No new blanket data licence is asserted. The height–weight example must not be used as medical advice or as a normative description of a population. The feed workbook is a modelling exercise, not approved nutritional guidance. Consult the original case documentation before making real-world decisions.

Notebook loaders prefer checked-in files locally. In Colab they fetch the current development resources and reject a checksum mismatch before using the data. Update the expected hash when deliberately revising a dataset. Before releasing an annual edition, pin both notebook and download links to its reviewed revision. This prevents an unrelated file with a similar name from being silently substituted while leaving 2026/27 open for development.

## Iris

[iris.data](iris.data) preserves the original UCI file used by the ABW perceptron lecture, without corrections to its two documented historical discrepancies. Credit: Fisher, R. (1936), *Iris*, [UCI Machine Learning Repository](https://doi.org/10.24432/C56C76), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Downloaded 7 September 2026; checksum and source URL are recorded in the manifest. This dataset-specific licence does not change the status of the other teaching data.
