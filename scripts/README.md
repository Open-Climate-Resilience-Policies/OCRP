# Scripts - Quality Assurance & Maintenance Tools

## Directory Structure

```
scripts/
├── consistency_guardian.py          # Agent D quality checker (main tool)
├── validate_frontmatter.py          # YAML validation
├── find_broken_links.py             # Scan official_sources URLs
├── detect_redundancy.py             # Find policy overlap
├── build_taxonomy.py                # Generate policy taxonomy
├── apply_wayback_replacements.py    # Auto-archive dead links
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── README_CONSISTENCY.md            # Full consistency_guardian docs
├── __pycache__/                     # Python cache (git-ignored)
└── tools/                           # Experimental/legacy tools
    ├── extract_claims.py            # Claim extraction (deprecated)
    ├── verify_harness_template.py   # LLM verification skeleton (deprecated)
    ├── ensure_overviews.py          # Overview generation helper
    ├── preview_server.py            # Dev server utility
    └── move_improvements_to_frontmatter.py  # Metadata migration
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r scripts/requirements.txt
```

## Primary Tools (Use These)

### Consistency Guardian (Agent D)
```bash
# Full quality audit across all policies
python scripts/consistency_guardian.py --all

# Check only modified policies
python scripts/consistency_guardian.py --changed

# Auto-update HTTP→HTTPS redirects and domain migrations
python scripts/consistency_guardian.py --update-redirects --all

# Check specific policy
python scripts/consistency_guardian.py _policies/solar-parking.md
```

**What it checks:**
- ✅ Frontmatter completeness (mandatory fields)
- ✅ Content structure (problem → mandate → implementation)
- ✅ Enforcement language (no vague "encourage" or "strive to")
- ✅ Enforcement mechanisms (penalties, permits, compliance tracking)
- ✅ Inline examples & links (validation + redirect detection)
- ✅ Geographic compatibility (units, legal system terms)
- ✅ Adversarial review (loopholes, liability, anti-corruption)
- ✅ Citation integrity (URLs accessible, sources authoritative)

See [README_CONSISTENCY.md](README_CONSISTENCY.md) for full documentation.

### Frontmatter Validation
```bash
python scripts/validate_frontmatter.py
```

Validates all `_policies/` files for required YAML fields and syntax.

### Find Broken Links
```bash
python scripts/find_broken_links.py
```

Scans all `official_sources` URLs for dead or inaccessible links (4xx/5xx status).

### Detect Redundancy
```bash
python scripts/detect_redundancy.py
```

Identifies overlapping policies by keyword and title similarity.

## Legacy Tools (Experimental, Don't Use)

Located in `scripts/tools/` - not actively maintained:
- `extract_claims.py` - Claim extraction (replaced by consistency_guardian)
- `verify_harness_template.py` - LLM verification (skeleton, incomplete)
- `ensure_overviews.py` - Overview generation helper
- `preview_server.py` - Development server utility

These are kept for reference but should not be used in standard workflow.

## Before Committing

**Always run this first:**
```bash
python scripts/consistency_guardian.py --all
```

Fix any **Critical Issues** (missing enforcement, dead links, etc.). Warnings may be addressed separately.

## Local Web Server (Preferred)

```bash
bundle exec jekyll serve --livereload
```

Site builds at `http://localhost:4000` with live reload on changes.

## Tips
- Always activate the virtualenv before running Python scripts: `source venv/bin/activate`
- Dependencies in `requirements.txt` include `pyyaml`, `requests`, `urllib3`
- URL validation uses 5-second timeout; network errors are reported as critical
- Redirect detection automatically updates source files (use `--update-redirects` flag)
