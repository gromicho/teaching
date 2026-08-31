"""Validate a teaching catalogue and optionally execute its offline notebooks.

Run from any checkout: python /path/to/check_resources.py --root . --execute
Execution uses disposable copies and never writes outputs to source notebooks.
Archive and live-network notebooks are explicitly reported, not counted as passes.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import time

import nbformat
from IPython.core.inputtransformer2 import TransformerManager
from nbclient import NotebookClient

sys.path.insert(0, str(Path(__file__).resolve().parent))
from publication_policy import public_notebook_error


def check(root, execute=False, run_setup=False, public_root=None):
    catalog = json.loads((root/'catalog.json').read_text(encoding='utf-8'))
    report = {'repository':catalog['repository'],'python':sys.version.split()[0],
              'setup_mode': 'execute' if run_setup else 'preinstalled',
              'results':[], 'errors':[]}
    paths = set()
    for item in catalog['notebooks']:
        relative = item['path']
        path = (root/relative).resolve()
        if not path.is_relative_to(root) or relative in paths:
            report['errors'].append(f'Unsafe or duplicate catalogue path: {relative}')
            continue
        paths.add(relative)
        profile = item['execution_profile']
        record = {'path':relative,'profile':profile,'structure':'pending','execution':'not requested'}
        report['results'].append(record)
        try:
            nb = nbformat.read(path,as_version=4)
            nbformat.validate(nb)
            if catalog['visibility'] == 'public':
                error = public_notebook_error(item)
                if error:
                    raise ValueError(error)
                if re.search(r'(?i)(solution|answer.?key|instructor)',relative):
                    raise ValueError('Suspicious public file name')
            for cell in nb.cells:
                if cell.cell_type != 'code':
                    continue
                if cell.outputs or cell.execution_count is not None:
                    raise ValueError('Saved outputs/execution counts must be cleared')
                if profile != 'archive':
                    ast.parse(TransformerManager().transform_cell(cell.source))
                    if re.search(r"(apt-get|NEOS_EMAIL|D:/src/solvers|SolverFactory\(['\"]cbc)",cell.source):
                        raise ValueError('Obsolete or remote solver setup in maintained notebook')
            record['structure'] = 'pass'
            if profile in ['archive','live-network','specialist']:
                record['execution'] = f'excluded: {profile}'
                continue
            if not execute:
                continue
            started = time.monotonic()
            with tempfile.TemporaryDirectory(prefix='teaching-check-') as temporary:
                work = Path(temporary)
                resource_root = public_root or root
                for folder in ['data','assets','support']:
                    if (resource_root/folder).exists():
                        shutil.copytree(resource_root/folder,work/folder)
                # Dependencies have been installed as a reproducible test environment.
                for cell in nb.cells:
                    if not run_setup and 'package-install' in cell.metadata.get('tags',[]):
                        cell.source = '# Dependencies are supplied by the test environment.'
                        continue
                    if not run_setup and 'setup' in cell.metadata.get('tags',[]):
                        # Keep imports/configuration that share an installation cell.
                        cell.source = '\n'.join(line for line in cell.source.splitlines()
                                                if not line.lstrip().startswith('%pip '))
                kernel_env = dict(os.environ, IPYTHONDIR=str(work/'ipython'),
                                  MPLCONFIGDIR=str(work/'matplotlib'),
                                  JUPYTER_RUNTIME_DIR=str(work/'jupyter-runtime'))
                NotebookClient(nb,timeout=180,kernel_name='python3',allow_errors=False,
                               resources={'metadata':{'path':str(work)}}).execute(env=kernel_env)
            record['execution'] = 'pass'
            record['seconds'] = round(time.monotonic()-started,2)
        except Exception as error:
            record['error'] = str(error)[-4000:]
            report['errors'].append(f'{relative}: {error.__class__.__name__}: {str(error)[-500:]}')
        print(relative, record.get('error','')[-250:] or record['execution'], flush=True)
    actual = {str(p.relative_to(root)).replace('\\','/') for p in root.rglob('*.ipynb')
              if not any(part.startswith('.') for part in p.relative_to(root).parts)}
    if actual != paths:
        report['errors'].append(f'Catalogue/file mismatch: {sorted(actual ^ paths)}')
    manifest = root/'data/manifest.json'
    if manifest.exists():
        for item in json.loads(manifest.read_text(encoding='utf-8'))['files']:
            path = (root/item['path']).resolve()
            if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                report['errors'].append(f'Dataset checksum mismatch: {item["path"]}')
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path('.'))
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--public-root',type=Path,
                        help='Read shared public resources from this sibling checkout when testing private keys')
    parser.add_argument('--run-setup',action='store_true',
                        help='Execute installation cells too; requires --execute and package-index access')
    parser.add_argument('--report',type=Path,default=Path('validation-report.json'))
    args = parser.parse_args()
    if args.run_setup and not args.execute:
        parser.error('--run-setup requires --execute')
    report = check(args.root.resolve(),args.execute,args.run_setup,
                   args.public_root.resolve() if args.public_root else None)
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({'checked':len(report['results']),'errors':report['errors']},indent=2))
    raise SystemExit(bool(report['errors']))


if __name__ == '__main__':
    main()
