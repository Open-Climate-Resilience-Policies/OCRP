#!/usr/bin/env python3
"""
Move 'improvements:' sections that are located after the YAML frontmatter into the frontmatter.
Backs up the original file to .bak before modifying.

Usage:
    python3 tools/move_improvements_to_frontmatter.py _policies/*.md
"""
import sys
from pathlib import Path
import re


def process_file(p: Path):
    text = p.read_text(encoding='utf-8')
    if not text.startswith('---'):
        return False, 'no frontmatter'
    parts = text.split('---', 2)
    if len(parts) < 3:
        return False, 'invalid frontmatter split'
    fm = parts[1]
    body = parts[2]
    # find 'improvements:' in body
    m = re.search(r"(?m)^improvements:\n(?:\s*- .*\n)+", body)
    if not m:
        return False, 'no improvements in body'
    improvements_block = m.group(0)
    # remove from body
    new_body = body[:m.start()] + body[m.end():]
    # ensure frontmatter ends with a newline
    if not fm.endswith('\n'):
        fm = fm + '\n'
    # append improvements to frontmatter if not present
    if 'improvements:' in fm:
        # already has improvements in frontmatter, skip
        return False, 'improvements already in frontmatter'
    new_fm = fm + improvements_block
    new_text = '---' + new_fm + '---' + new_body
    # backup
    bak = p.with_suffix(p.suffix + '.bak')
    p.rename(bak)
    p.write_text(new_text, encoding='utf-8')
    return True, f'moved to frontmatter, backup: {bak.name}'


def main(argv):
    if len(argv) < 2:
        print('Usage: move_improvements_to_frontmatter.py files...')
        return
    for fp in argv[1:]:
        p = Path(fp)
        if not p.exists():
            print(fp, 'not found')
            continue
        ok, msg = process_file(p)
        print(fp, msg)

if __name__ == '__main__':
    main(sys.argv)
