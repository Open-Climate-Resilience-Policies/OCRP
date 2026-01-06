#!/usr/bin/env python3
import glob, re, sys, os
import yaml
from datetime import date, datetime

REPO_ROOT = os.path.join(os.path.dirname(__file__), '..')
POL_DIR = os.path.join(REPO_ROOT, '_policies')

# Root-level pages that must have valid frontmatter
CRITICAL_PAGES = ['about.md', 'contribute.md', 'index.md']

ALLOWED_SCALAR = (str, int, float, bool, date, datetime)

def is_allowed(value):
    if isinstance(value, ALLOWED_SCALAR):
        return True
    if value is None:
        return True
    if isinstance(value, list):
        return all(is_allowed(v) for v in value)
    if isinstance(value, dict):
        return all(isinstance(k, str) and is_allowed(v) for k,v in value.items())
    return False

def extract_frontmatter(text):
    if not text.startswith('---'):
        return None
    parts = text.split('---',2)
    if len(parts) < 3:
        return None
    return parts[1]

def main():
    errors = []
    # Scan policy files
    files = sorted(glob.glob(os.path.join(POL_DIR, '*.md')))
    # Add critical root-level pages
    for page in CRITICAL_PAGES:
        page_path = os.path.join(REPO_ROOT, page)
        if os.path.exists(page_path):
            files.append(page_path)
    
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            s = fh.read()
        fm_text = extract_frontmatter(s)
        if fm_text is None:
            errors.append((f, 'no frontmatter'))
            continue
        try:
            fm = yaml.safe_load(fm_text) or {}
        except Exception as e:
            errors.append((f, f'yaml parse error: {e}'))
            continue
        for k,v in fm.items():
            if not is_allowed(v):
                errors.append((f, f'field {k!r} has unsupported type: {type(v)}'))
    if errors:
        print('Frontmatter validation failed for some files:')
        for f,msg in errors:
            print(f'- {f}: {msg}')
        sys.exit(2)
    print(f'✅ Frontmatter validation passed: {len(files)} files checked')

if __name__ == "__main__":
    main()
