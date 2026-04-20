#!/usr/bin/env python3
"""
Parse link-check.json produced by find_broken_links.py and exit 1 if
definitively broken links are found.

Exit codes:
  0 — no broken links
  1 — broken links found (HTTP 404/410)

HTTP codes that are treated as warnings (not failures):
  401/403/429 — bot-blocking or auth-required
  500/502/503/504 — transient server errors

Network-level errors (status_code=None, e.g. connection refused, timeout,
DNS failure) are also treated as warnings.  These indicate the URL could not
be verified from the CI environment — a common occurrence for archive.org
and other hosts that block automated runners — rather than that the link is
definitively broken.  A human-visible warning is still emitted.
"""
import json
import pprint
import sys

# 401/403/429: bot-blocking or auth-required — warn but do not fail.
# 500/502/503/504: transient server errors — warn but do not fail.
# None (connection errors): network-level issues — warn but do not fail.
# 404/410: definitively broken content — fail.
UNCERTAIN_CODES = {401, 403, 429, 500, 502, 503, 504}

with open('link-check.json') as f:
    results = json.load(f)
bad = []
warn = []

for e in results:
    code = e.get('status_code')
    if code is None:
        # Network error (connection refused, timeout, DNS failure).
        # Treat as a warning so CI does not fail due to runner network
        # restrictions (e.g. web.archive.org blocked in GitHub Actions).
        warn.append(e)
    elif isinstance(code, int):
        if code in UNCERTAIN_CODES:
            warn.append(e)
        elif code >= 400:
            bad.append(e)

if warn:
    print(
        'WARNING — URLs that may be bot-blocked, require auth, or have transient server errors'
        ' (not counted as failures):'
    )
    pprint.pprint(warn[:20])

if bad:
    print('Broken official_sources detected (first 20):')
    pprint.pprint(bad[:20])
    sys.exit(1)

print('No broken official_sources found.')
