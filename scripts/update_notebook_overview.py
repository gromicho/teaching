"""Generate student navigation from the notebook catalogue, without manual counts."""
import argparse
import json
from pathlib import Path


def render(catalog):
    descriptions = {
        'core': 'Checked offline',
        'live-network': 'Needs live services; not routinely executed',
        'specialist': 'Specialist; not routinely executed',
        'archive': 'Historical reading; do not Run all',
    }
    lines = ['# Notebook overview', '',
             'Browse all catalogued notebooks here. Course pages and Canvas determine the teaching sequence.', '',
             '“Checked offline” refers to automated execution, not a guarantee about every explanation or a student’s edited copy.', '',
             'Instructor solutions are distributed separately by the teaching team.', '']
    labels = {'abw': 'ABW', 'aabw': 'AABW', 'foundations': 'Foundations',
              'heuristics': 'Heuristics', 'historical': 'Historical reference'}
    groups = sorted({item['collection'].casefold() for item in catalog['notebooks']})
    for group in groups:
        lines += [f'## {labels.get(group, group)}', '', '| Notebook | Type | Execution checks |', '| --- | --- | --- |']
        items = sorted((i for i in catalog['notebooks'] if i['collection'].casefold() == group),
                       key=lambda i: (i['title'].casefold(), i['path']))
        for item in items:
            title = item['title'].replace('|', r'\|')
            kind = item['kind'].replace('-', ' ')
            status = descriptions.get(item['execution_profile'], item['execution_profile'])
            lines.append(f"| [{title}](../{item['path']}) | {kind} | {status} |")
        lines.append('')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    catalog = json.loads((args.root / 'catalog.json').read_text(encoding='utf-8'))
    (args.root / 'docs/NOTEBOOKS.md').write_text(render(catalog), encoding='utf-8')


if __name__ == '__main__':
    main()
