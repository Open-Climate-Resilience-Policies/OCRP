#!/usr/bin/env python3
"""
Apply Wayback snapshot replacements suggested by `find_broken_links.py`.

For each `official_sources` entry with a `suggestion` (Wayback URL),
- create a timestamped backup of the original policy in `archive/` per project rules
- update the frontmatter URL to the Wayback snapshot
- preserve other frontmatter fields

This script is conservative: it only modifies entries where a `suggestion` URL exists.
"""
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import re
import yaml


ROOT = Path('.')
ARCHIVE_DIR = ROOT / 'archive'
ARCHIVE_DIR.mkdir(exist_ok=True)


def run_finder():
    proc = subprocess.run(['python3', 'scripts/find_broken_links.py'], capture_output=True, text=True)
    if proc.returncode != 0:
        print('find_broken_links.py failed:', proc.stderr)
        sys.exit(1)
    return json.loads(proc.stdout)


def backup_file(path: Path):
    ts = datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')
    target = ARCHIVE_DIR / f"{path.name}.{ts}.bak"
    target.write_text(path.read_text(encoding='utf-8'), encoding='utf-8')
    return target


def update_frontmatter_file(path: Path, index: int, new_url: str):
    text = path.read_text(encoding='utf-8')
    # Simple frontmatter extraction: find the first two '---' markers
    parts = text.split('---')
    if len(parts) < 3:
        raise RuntimeError(f'Cannot parse frontmatter for {path}')
    # parts[0] may be preamble, parts[1] is frontmatter, parts[2:] is body
    fm_text = parts[1]
    body = '---'.join(parts[2:])
    fm = yaml.safe_load(fm_text) or {}
    sources = fm.get('official_sources', [])
    if index < 0 or index >= len(sources):
        raise IndexError('official_sources index out of range')
    if not isinstance(sources[index], dict) or 'url' not in sources[index]:
        raise RuntimeError('unexpected official_sources item format')
    sources[index]['url'] = new_url
    fm['official_sources'] = sources
    # Dump YAML preserving block style
    new_fm = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
    new_text = '---\n' + new_fm + '---\n\n' + body.lstrip('\n')
    path.write_text(new_text, encoding='utf-8')


def main():
    print('Running find_broken_links.py to collect suggestions...')
    results = run_finder()
    candidates = [r for r in results if r.get('suggestion')]
    if not candidates:
        print('No Wayback suggestions found; nothing to apply.')
        return

    applied = []
    for entry in candidates:
        file = Path(entry['file'])
        index = entry['index']
        suggestion = entry.get('suggestion')
        if not file.exists():
            print('Skipping missing file', file)
            continue
        print(f'Backing up {file}...')
        backup = backup_file(file)
        print(f'Updating {file} official_sources[{index}] -> {suggestion}')
        try:
            update_frontmatter_file(file, index, suggestion)
            applied.append({'file': str(file), 'index': index, 'new_url': suggestion, 'backup': str(backup)})
        except Exception as e:
            print('Failed to update', file, e)

    print('\nApplied replacements:')
    print(json.dumps(applied, indent=2))

    print('\nRe-running frontmatter validator...')
    subprocess.run(['python3', 'scripts/validate_frontmatter.py'])

    print('\nRe-running consistency guardian (links check)...')
    subprocess.run(['python3', 'scripts/consistency_guardian.py', '--check-links', '--policies-dir', '_policies'])


if __name__ == '__main__':
    main()
