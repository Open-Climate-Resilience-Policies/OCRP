#!/usr/bin/env python3
"""
Scan `_policies/` for `official_sources` URLs, check reachability, and (optionally)
emit per-policy stats useful for spotting thin or under-cited policies.

Usage examples:
    python scripts/find_broken_links.py --mode links   # (default) link health JSON
    python scripts/find_broken_links.py --mode stats   # policy stats JSON
    python scripts/find_broken_links.py --mode both    # combined payload
"""
import argparse
import re
import yaml
import json
import requests
from pathlib import Path
from urllib.parse import quote, urlparse


POLICIES_DIR = Path('_policies')
TIMEOUT = 8
SECTION_KEYWORDS = {
    'problem/context': ['problem', 'context', 'overview', 'background'],
    'mandate/requirements': ['mandate', 'policy', 'requirements', 'obligation'],
    'implementation guidance': ['implementation', 'roadmap', 'program', 'steps'],
    'metrics/verification': ['metrics', 'verification', 'monitoring', 'success', 'compliance']
}
ENFORCEMENT_TERMS = ['shall', 'must', 'penalty', 'inspection', 'report', 'revoked', 'license', 'permit']
SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': 'OCRaP-LinkChecker/1.0 (+https://ocrap.ai/tools/link-checker)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
})


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
        resp = SESSION.head(url, timeout=TIMEOUT, allow_redirects=True)
        code = resp.status_code
        if code in (405, 403):
            # Some servers disallow HEAD; fall back to GET
            resp = SESSION.get(url, timeout=TIMEOUT, allow_redirects=True)
            code = resp.status_code
        return code, resp.url
    except requests.exceptions.Timeout:
        # Retry once with a longer timeout before reporting as unreachable
        try:
            resp = SESSION.get(url, timeout=TIMEOUT * 3, allow_redirects=True)
            return resp.status_code, resp.url
        except Exception as e:
            return None, str(e)
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


def policy_stats(md: Path, front: dict, body: str):
    non_empty_lines = sum(1 for line in body.splitlines() if line.strip())
    sources = front.get('official_sources', []) or []
    source_count = sum(1 for src in sources if isinstance(src, dict) and 'url' in src)
    domains_set = set()
    for src in sources:
        if isinstance(src, dict) and 'url' in src and src['url']:
            parsed = urlparse(src['url'])
            domain = parsed.netloc or parsed.path.split('/')[0]
            if domain:
                domains_set.add(domain)
    domains = sorted(domains_set)
    headings = [title.strip().lower() for _, title in re.findall(r'^(#{1,6})\s+(.*)', body, re.MULTILINE)]
    missing_sections = []
    for label, keywords in SECTION_KEYWORDS.items():
        if not any(any(keyword in heading for keyword in keywords) for heading in headings):
            missing_sections.append(label)

    content_lower = body.lower()
    has_enforcement = any(term in content_lower for term in ENFORCEMENT_TERMS)

    return {
        'file': str(md),
        'non_empty_lines': non_empty_lines,
        'official_sources_count': source_count,
        'unique_source_domains': len(domains),
        'missing_sections': missing_sections,
        'has_enforcement_language': has_enforcement
    }


def save_policy(md: Path, front: dict, body: str):
    """Rewrite markdown file with updated frontmatter while preserving body."""
    front_dump = yaml.safe_dump(front, sort_keys=False).strip()
    body_content = body if body.startswith('\n') else '\n' + body
    md.write_text(f"---\n{front_dump}\n---{body_content}", encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Check official_sources links and emit policy stats')
    parser.add_argument('--mode', choices=['links', 'stats', 'both'], default='links',
                        help='links = broken link report (default); stats = policy metadata; both = combined payload')
    parser.add_argument('--update-redirects', action='store_true',
                        help='Rewrite official_sources URLs to their final redirect destinations when safe')
    args = parser.parse_args()

    results = []
    stats = []
    pending_writes = []

    for md in sorted(POLICIES_DIR.glob('*.md')):
        text = md.read_text(encoding='utf-8')
        front, body = extract_frontmatter(text)
        if not front:
            continue

        if args.mode in ('links', 'both'):
            sources = front.get('official_sources', [])
            front_changed = False
            for i, src in enumerate(sources):
                if isinstance(src, dict) and 'url' in src:
                    url = src['url']
                    code, final_url = check_url(url)
                    entry = {'file': str(md), 'index': i, 'url': url, 'status_code': code}
                    if code is None:
                        entry['error'] = final_url
                    else:
                        entry['final_url'] = final_url
                        if final_url and final_url != url:
                            entry['redirected'] = True
                            if args.update_redirects and 200 <= code < 400:
                                src['url'] = final_url
                                front_changed = True
                    if code is None or (isinstance(code, int) and code >= 400):
                        entry['suggestion'] = wayback_suggestion(url)
                    results.append(entry)
            if front_changed and body is not None:
                pending_writes.append((md, front, body))

        if args.mode in ('stats', 'both') and body is not None:
            stats.append(policy_stats(md, front, body))

    if args.update_redirects:
        for md, front, body in pending_writes:
            save_policy(md, front, body)

    if args.mode == 'links':
        print(json.dumps(results, indent=2))
    elif args.mode == 'stats':
        print(json.dumps(stats, indent=2))
    else:
        print(json.dumps({'links': results, 'policy_stats': stats}, indent=2))


if __name__ == '__main__':
    main()
