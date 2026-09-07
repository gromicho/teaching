"""Dataset-specific preparation for the ABW fruit lectures.

These corrections encode the two known teaching-data entry mistakes. They are
not a general outlier-removal procedure and must be applied only once to raw data.
Importing this module does not load data or modify a dataframe.
"""


def fix_fruit_outliers(fruits):
    """Return a corrected copy while preserving the caller's index and raw data."""
    corrected = fruits.copy(deep=True)
    short_label = corrected['Length'].idxmin()
    wide_label = corrected['Width'].idxmax()
    corrected.loc[wide_label, ['Length', 'Width']] = corrected.loc[
        wide_label, ['Width', 'Length']
    ].to_numpy()
    corrected.loc[short_label, ['Length', 'Width']] *= 10
    return corrected
