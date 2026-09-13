"""Corrections for two documented entry errors in the ABW fruit dataset.

This is not a general outlier detector. Match the recorded erroneous values,
including the fruit name, rather than modifying new extrema on every call.
Importing this module neither loads data nor changes a dataframe.
"""


def fix_fruit_outliers(fruits):
    """Return a corrected copy; leave other records, columns and labels unchanged.

    Banana (2.5, 7.2) has transposed dimensions. Apple (0.253, 0.277)
    has a factor-of-ten entry error. Already-corrected records do not match
    either condition, so applying this function again leaves them unchanged.
    These exact comparisons refer to the recorded teaching-data values only.
    """
    corrected = fruits.copy(deep=True)
    swapped = (
        fruits['Name'].eq('Banana')
        & fruits['Length'].eq(2.5)
        & fruits['Width'].eq(7.2)
    )
    scaled = (
        fruits['Name'].eq('Apple')
        & fruits['Length'].eq(0.253)
        & fruits['Width'].eq(0.277)
    )
    # Own the array before assigning: a pandas 3 view can alias the destination.
    corrected.loc[swapped, ['Length', 'Width']] = fruits.loc[
        swapped, ['Width', 'Length']
    ].to_numpy(copy=True)
    corrected.loc[scaled, ['Length', 'Width']] = (
        fruits.loc[scaled, ['Length', 'Width']] * 10
    ).to_numpy(copy=True)
    return corrected
