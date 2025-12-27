# Scripts Guide

Quick setup and usage for local tools in `scripts/`.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Common Commands

```bash
# Consistency checks (Agent D)
python scripts/consistency_guardian.py --all
python scripts/consistency_guardian.py --changed

# Frontmatter validation
python scripts/validate_frontmatter.py

# Broken link scan for official_sources
python scripts/find_broken_links.py
```

See [scripts/README_CONSISTENCY.md](README_CONSISTENCY.md) for full Consistency Guardian usage (LLM options, outputs, exit codes).

## Local Web Server (preferred)

```bash
bundle exec jekyll serve --livereload
```

## Tips
- Always activate the virtualenv before running Python scripts.
- Dependencies live in `requirements.txt` (includes `pyyaml`, `requests`).
- If HEAD requests fail for a source, re-run `find_broken_links.py` after fixing URLs.
