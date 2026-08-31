"""Narrow publication exception approved by the maintainer on 31 August 2026."""

PUBLIC_HISTORICAL_NOTEBOOKS = frozenset({
    'archive/jeff-kantor-solver-installation-legacy.ipynb',
})
PUBLIC_HISTORICAL_FILES = PUBLIC_HISTORICAL_NOTEBOOKS | {'archive/README.md'}


def public_notebook_error(item):
    path = item['path']
    if path in PUBLIC_HISTORICAL_NOTEBOOKS:
        if (item['kind'] != 'historical-reference'
                or item['execution_profile'] != 'archive'
                or item.get('collection') != 'historical'):
            return 'Approved historical notebook must remain a non-executed archive reference'
        return None
    if item['kind'] in ['solution', 'historical-reference']:
        return 'Private material marked for public publication'
    if path.startswith('archive/'):
        return 'Unapproved public historical notebook'
    return None
