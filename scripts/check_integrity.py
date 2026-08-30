"""Check publication boundaries, selections and shared-resource integrity.

These are safeguards, not a substitute for instructor review of public content.
Initial import hashes are historical snapshots: check them explicitly at migration,
not on every later edit. Archive hashes remain enforced to preserve provenance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_portability import check as check_portability


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(root, public_root=None, verify_import_snapshot=False):
    errors=check_portability(root)
    catalog=read(root/'catalog.json')
    visibility=catalog['visibility']
    expected='gromicho/teaching' if visibility=='public' else 'gromicho/teaching-solutions'
    if catalog['repository']!=expected:
        errors.append('Repository identity does not match declared publication boundary')
    imports=read(root/'provenance/imports.json')
    paths={n['path'] for n in catalog['notebooks']}
    ids=[n['id'] for n in catalog['notebooks']]
    if len(ids)!=len(set(ids)):
        errors.append('Duplicate catalogue IDs')
    for record in imports['imports']:
        relative=record['path']
        target=(root/relative).resolve()
        if not target.is_relative_to(root) or not target.is_file():
            errors.append(f'Unsafe or absent import: {relative}')
            continue
        if visibility=='public' and record['source_visibility']!='public':
            errors.append(f'Private source in public import: {relative}')
        if verify_import_snapshot or relative.startswith('archive/'):
            if sha(target)!=record['destination_sha256']:
                errors.append(f'Import snapshot checksum mismatch: {relative}')
    if visibility=='public':
        for path in root.rglob('*'):
            rel=path.relative_to(root)
            if not path.is_file() or any(x.startswith('.') for x in rel.parts):
                continue
            if re.search(r'(?i)(solution|answer.?key|instructor|archive|\.pem$|\.key$)',rel.as_posix()):
                errors.append(f'Public file needs private-boundary review: {rel}')
            if path.suffix in ['.md','.ipynb','.py','.json','.yml']:
                try:
                    text=path.read_text(encoding='utf-8')
                except UnicodeError:
                    continue  # Already reported by the portability check.
                if re.search(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}',text):
                    errors.append(f'Possible credential in {rel}')
        for manifest in root.glob('courses/*/editions/*.json'):
            edition=read(manifest)
            for relative in edition['foundations']+edition['course_resources']:
                if relative not in paths:
                    errors.append(f'Course selection missing from catalogue: {relative}')
            for record in edition['datasets']:
                if sha(root/record['path'])!=record['sha256']:
                    errors.append(f'Course dataset checksum mismatch: {record["path"]}')
    if visibility=='private':
        for record in read(root/'shared-solutions.json')['items']:
            if record['path'] not in paths:
                errors.append(f'Shared solution selection is absent: {record["path"]}')
        if public_root:
            for record in read(root/'public-resources.json')['files']:
                if sha(public_root/record['path'])!=record['sha256']:
                    errors.append(f'Public data changed: {record["path"]}')
    return errors


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path('.'))
    parser.add_argument('--public-root',type=Path)
    parser.add_argument('--verify-import-snapshot',action='store_true')
    args=parser.parse_args()
    errors=check(args.root.resolve(),args.public_root.resolve() if args.public_root else None,
                 args.verify_import_snapshot)
    print(json.dumps({'errors':errors},indent=2))
    raise SystemExit(bool(errors))
