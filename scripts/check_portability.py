"""Catch unsafe path characters and common text-encoding damage.

Unicode prose is welcome. Keep repository paths ASCII and preserve historical
archive bytes rather than silently repairing them.
"""
import json
from pathlib import Path
import re

TEXT_SUFFIXES = {'.md', '.ipynb', '.json', '.py', '.yml', '.yaml', '.txt', '.svg'}
MOJIBAKE = re.compile(r'\ufffd|\u00e2[\u0080\u20ac]|[\u00c2\u00c3][\u0080-\u00bf]')
RESERVED = re.compile(r'(?i)^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)')
GENERATED_LATEX_SUFFIXES = {'.aux', '.log', '.nav', '.out', '.snm', '.toc'}


def check(root):
    errors = []
    names = {}
    for path in root.rglob('*'):
        relative = path.relative_to(root)
        if any(part == '__pycache__' or (part.startswith('.') and part not in
               {'.github', '.gitignore', '.gitattributes', '.editorconfig'})
               for part in relative.parts):
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() in GENERATED_LATEX_SUFFIXES:
            continue
        name = relative.as_posix()
        # A reference deck is an opaque, source-faithful visual asset.  Its
        # filename is not used by notebooks, links, or generated teaching
        # materials, so it does not impose a portability requirement.
        is_reference_asset = len(relative.parts) >= 3 and relative.parts[0] == 'presentations' and 'references' in relative.parts
        is_presentation_pdf = relative.parts[0] == 'presentations' and path.suffix.lower() == '.pdf'
        if (not (is_reference_asset or is_presentation_pdf) and not re.fullmatch(r'[A-Za-z0-9_./-]+', name)) or any(
                part.endswith('.') or RESERVED.match(part) for part in relative.parts):
            errors.append(f'Non-portable filename: {name}')
        folded = name.casefold()
        if folded in names and names[folded] != name:
            errors.append(f'Case-colliding filenames: {names[folded]} and {name}')
        names[folded] = name
        if relative.parts[0] == 'archive' or path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding='utf-8')
            if path.suffix == '.ipynb':
                text = '\n'.join(''.join(c['source']) for c in json.loads(text)['cells'])
        except (UnicodeError, ValueError, KeyError) as error:
            errors.append(f'Invalid UTF-8/text document: {name}: {error}')
            continue
        if MOJIBAKE.search(text):
            errors.append(f'Possible garbled text: {name}')
        if any(char in text for char in ['\u200b', '\ufeff', '\x00']):
            errors.append(f'Unexpected invisible character: {name}')
    return errors
