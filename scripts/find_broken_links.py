#!/usr/bin/env python3
"""
Scan `_policies/` for `official_sources` URLs, check reachability, and suggest Wayback snapshots for unreachable links.
Outputs a JSON list of {file, index, url, status, suggestion} to stdout.
No files are modified by this script.
"""
import re
import yaml
import json
import requests
from pathlib import Path
from urllib.parse import quote


POLICIES_DIR = Path('_policies')
TIMEOUT = 8


def extract_frontmatter(text: str):
    parts = re.split(r'^---\s*$', text, flags=re.MULTILINE, maxsplit=2)
    if len(parts) < 3:
        return None, text
    front = yaml.safe_load(parts[1]) or {}
    body = parts[2]
    return front, body


def check_url(url: str):
    try:
        # Try HEAD first
        resp = requests.head(url, timeout=TIMEOUT, allow_redirects=True)
        code = resp.status_code
        if code == 405 or code == 403:
            # Some servers disallow HEAD; try GET
            resp = requests.get(url, timeout=TIMEOUT, allow_redirects=True)
            code = resp.status_code
        return code, resp.url
    except Exception as e:
        return None, str(e)


def wayback_suggestion(url: str):
    try:
        api = f'https://archive.org/wayback/available?url={quote(url, safe="")}'
        r = requests.get(api, timeout=TIMEOUT)
        if r.ok:
            data = r.json()
            snap = data.get('archived_snapshots', {}).get('closest')
            if snap and 'url' in snap:
                return snap['url']
        return None
    except Exception:
        return None


def main():
    results = []
    for md in sorted(POLICIES_DIR.glob('*.md')):
        text = md.read_text(encoding='utf-8')
        front, _ = extract_frontmatter(text)
        if not front:
            continue
        sources = front.get('official_sources', [])
        for i, src in enumerate(sources):
            if isinstance(src, dict) and 'url' in src:
                url = src['url']
                code, info = check_url(url)
                entry = {'file': str(md), 'index': i, 'url': url, 'status_code': code}
                if code is None or (isinstance(code, int) and code >= 400):
                    entry['suggestion'] = wayback_suggestion(url)
                results.append(entry)

    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
