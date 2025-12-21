#!/usr/bin/env python3
import glob, re, sys, os
import yaml

POL_DIR = os.path.join(os.path.dirname(__file__), '..', '_policies')

ALLOWED_SCALAR = (str, int, float, bool)

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
    files = sorted(glob.glob(os.path.join(POL_DIR, '*.md')))
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
    print('Frontmatter validation passed: all values use simple YAML types')

if __name__ == "__main__":
    main()
