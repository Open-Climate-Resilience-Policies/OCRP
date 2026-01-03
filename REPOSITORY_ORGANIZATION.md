# Repository Organization Guide

## Directory Hierarchy Overview

This document explains the purpose and organization of OCRaP.ai's directory structure, with emphasis on maintaining clarity, accessibility, and ease of contribution.

---

## Root-Level Decisions

### Why we organize this way:

1. **Separation of Concerns**: Content (_policies/) is separate from tooling (scripts/)
2. **Public vs. Private**: Publishable assets (assets/) are distinct from development tools
3. **Clarity**: Tool purpose is obvious from location
4. **Scalability**: New contributors understand where to add files

---

## Primary Directories

### `/scripts` - Quality Assurance & Maintenance Tools

**Purpose**: Python automation for policy validation, link checking, and consistency enforcement.

**Structure**:
```
scripts/
├── (Production tools - used in standard workflow)
├── consistency_guardian.py      Main quality checker (Agent D)
├── validate_frontmatter.py      YAML validation
├── find_broken_links.py         URL scanner for official_sources
├── detect_redundancy.py         Policy overlap detection
├── build_taxonomy.py            Taxonomy generation
├── apply_wayback_replacements.py Dead link archiving
├── requirements.txt             Python dependencies
├── README.md                    Usage guide
├── README_CONSISTENCY.md        Detailed documentation
│
└── tools/                       (Experimental/Legacy tools)
    ├── extract_claims.py        Claim extraction (experimental)
    ├── verify_harness_template.py LLM verification (skeleton)
    ├── ensure_overviews.py      Overview generation helper
    ├── preview_server.py        Development server
    └── ...                      Other helpers
```

**Key Principle**: 
- **Root level** = Active, maintained tools (used every commit)
- **`tools/` subdirectory** = Experimental, not yet integrated (reference only)

**When to use**:
- Always run `consistency_guardian.py --all` before committing
- Use `validate_frontmatter.py` to audit new policies
- Use `find_broken_links.py` for periodic link health checks

**When NOT to use**:
- Don't use `scripts/tools/` items—they're incomplete/legacy
- Don't manually edit policies without running checks

---

### `/_policies` - Policy Content (Core)

**Purpose**: Authoritative source files for all climate resilience policies.

**Structure**:
```
_policies/
├── solar-parking.md             31 policies total
├── urban-forest-management-model.md
├── thermal-energy-network.md
├── ... (one file per policy)
└── README.md                    Policy authoring template
```

**Key Principle**:
- **One policy = One markdown file** with required frontmatter
- Every policy must pass `consistency_guardian.py` checks
- All inline links must be working (validated by Check 5.5)

**New Policy Checklist**:
1. Create `_policies/{slug}.md` (slug = lowercase, dashes, no spaces)
2. Add required frontmatter (date, slug, keywords, official_sources)
3. Include 2–5 specific, working inline examples
4. Run `python scripts/consistency_guardian.py _policies/{slug}.md`
5. Commit with reference to enforcement mechanism or local practice

---

### `/assets` - Public-Facing Static Assets

**Purpose**: CSS, JavaScript, images served to website visitors (published to `_site/assets/`).

**Structure**:
```
assets/
├── css/                         Stylesheets
│   ├── main.css
│   ├── responsive.css
│   └── ...
├── js/                          Client-side scripts
│   ├── accessibility-test.js    WCAG 2.2 AA compliance tests
│   ├── connectivity.js          Network utilities
│   ├── policy-engine.js         Policy filtering/display
│   ├── share.js                 Social sharing
│   └── ...
├── images/                      Static images and icons
├── img/                         Picture assets
├── manifest/                    Web app manifest files
└── ...
```

**Key Principle**:
- **All public JS goes here**: accessibility-test.js, policy-engine.js, etc.
- **No user data collection**: No tracking, no phone-home behavior
- **Progressive enhancement**: Core features work without JavaScript
- **Accessibility first**: Every interactive element tested with axe-core

**Organization principle for `/js`**:
- Alphabetical by function, not by author or date
- One logical feature per file (policy-engine.js not policy-filters.js + policy-display.js)
- Clear, descriptive names

---

### `/_layouts` - Jekyll Templates

**Purpose**: HTML templates for rendering markdown policies into website pages.

**Structure**:
```
_layouts/
├── default.html                 Base page template
├── policy.html                  Policy-specific template (extends default)
└── ...
```

**When to edit**:
- Change site navigation → edit `default.html`
- Change policy display format → edit `policy.html`

---

## Supporting Directories

### `/archive` - Deprecated Content & Backups

**Purpose**: Preserve history, support Wayback Machine integration, store backups.

**Structure**:
```
archive/
├── clean-heat-standard.md       Deprecated policies (removed, kept for history)
├── climate-risk-disclosure.md
├── cool-pavement.md.2025-12-27-152324.bak  Timestamped backups before major edits
├── tools-deprecated/            (If /scripts/tools ever fully deprecated)
├── ...
└── README.md                    Archive guide
```

**Key Principle**:
- **Never delete policies**—move to archive with `.YYYY-MM-DD.bak` suffix
- **Backup on substantial edits** (>20% content change or mandate modification)
- **Document reason** in commit message when archiving

---

### `/templates` - Authoring Resources

**Purpose**: Guides and templates for new policy authors.

**Structure**:
```
templates/
├── policy-template.md           Starting template for new policies
├── POLICY_AUTHORING_GUIDE.md   Step-by-step contribution guide
├── FRONTMATTER_REQUIRED_FIELDS.md
└── ...
```

**When to use**:
- New contributor writing first policy → copy `policy-template.md`
- Questions about enforcement language → see authoring guide

---

### `/evidence` - Supporting Documentation

**Purpose**: PDFs, source documents, research files that back up claims in policies.

**Structure**:
```
evidence/
├── official_sources/            Archived versions of cited sources
├── research/                    Academic papers, reports
├── climate-data/                Raw climate datasets
└── ...
```

**Key Principle**:
- Organize by policy name (e.g., `evidence/solar-parking/`)
- Link from policy to evidence files when needed
- Document source URLs in README

---

### `/data` - Structured Metadata

**Purpose**: Taxonomies, indices, and computed datasets.

**Structure**:
```
data/
├── taxonomy.json                Policy categories, keywords (auto-generated)
├── policy-index.json            Master index with all metadata
├── locales/                     Internationalization support
└── ...
```

**Key Principle**:
- Auto-generated from policies (don't edit manually)
- Used by policy-engine.js for filtering/display
- Regenerate after policy changes: `python scripts/build_taxonomy.py`

---

### `/.github` - GitHub Configuration

**Purpose**: CI/CD workflows, issue templates, GitHub Actions.

**Structure**:
```
.github/
├── workflows/
│   ├── quality.yml              (Planned) Automated quality checks
│   ├── deploy.yml               (Planned) Build and deploy to Pages
│   └── ...
├── ISSUE_TEMPLATE/
├── PULL_REQUEST_TEMPLATE.md
└── ...
```

---

### `/src` - Source Code (Non-Policy)

**Purpose**: Custom extensions, JavaScript bundles, or generated code.

**Structure**:
```
src/
├── data/                        Generated data files
├── js/                          Custom JavaScript (pre-bundling)
└── ...
```

**Note**: Minimize use; prefer `/assets/` for public code.

---

## File-Level Best Practices

### Policy Files (`_policies/*.md`)

**Naming Convention**:
- Lowercase, dash-separated, no spaces
- Match `slug` field in frontmatter exactly
- Example: `solar-parking.md`, `urban-forest-management-model.md`

**File Size**:
- Aim for 500–2000 words per policy
- If >2500 words, consider splitting into related policies

**Version Control**:
- Every policy edit gets a commit
- Major edits (>20% change) get a `.bak` in `/archive/`
- Commit message references enforcement mechanism or specific change

### Python Tools (`scripts/*.py`)

**Style**:
- Follow PEP 8
- Document with docstrings
- Include usage examples in README

**Dependencies**:
- Always in `scripts/requirements.txt`
- Pin versions for reproducibility

**Testing**:
- Run against all 31 policies before committing
- Document known limitations

### JavaScript Files (`assets/js/*.js`)

**Accessibility First**:
- Every interactive element is keyboard-reachable
- ARIA labels for dynamic content
- No color-only indicators (for status, errors)

**Privacy & Security**:
- No third-party trackers
- No unexpected network calls (document what you fetch)
- No localStorage without explicit user action

**Error Handling**:
- Wrap risky code in try/catch
- User-visible error messages (not console.error only)
- Graceful degradation if network fails

### CSS Files (`assets/css/*.css`)

**Scope**:
- One concern per file (layout.css, typography.css, interactive.css)
- Use consistent naming conventions (BEM or simple class names)

**Mobile First**:
- Base styles for mobile, @media (min-width) for larger screens
- Test at 320px, 768px, 1200px minimum

**Accessibility**:
- No text smaller than 14px
- Sufficient color contrast (WCAG AA minimum: 4.5:1 for text)
- Focus indicators visible (don't remove outlines)

---

## Workflow Examples

### Adding a New Policy

1. **Copy template**:
   ```bash
   cp templates/policy-template.md _policies/my-new-policy.md
   ```

2. **Edit frontmatter & content**:
   ```markdown
   ---
   date: 2025-01-03
   slug: my-new-policy
   keywords: [keyword1, keyword2, keyword3]
   official_sources:
     - url: https://example.org/policy
       title: Official Policy Doc
   ---
   ```

3. **Validate**:
   ```bash
   python scripts/consistency_guardian.py _policies/my-new-policy.md
   ```

4. **Fix any critical issues**, then commit:
   ```bash
   git add _policies/my-new-policy.md
   git commit -m "Add policy: My New Policy

   - Enforces X requirement
   - References [source](url)
   - Includes 3 working inline examples"
   ```

### Updating an Existing Policy

1. **Edit the markdown**:
   ```bash
   vim _policies/solar-parking.md
   ```

2. **Check for issues** (especially if >20% content change):
   ```bash
   # Create backup if major change
   cp _policies/solar-parking.md archive/solar-parking.md.2025-01-03-143000.bak
   
   # Validate
   python scripts/consistency_guardian.py _policies/solar-parking.md
   ```

3. **Fix broken links automatically**:
   ```bash
   python scripts/consistency_guardian.py --update-redirects _policies/solar-parking.md
   ```

4. **Commit with clear message**:
   ```bash
   git add _policies/solar-parking.md [archive backup if created]
   git commit -m "Update: Solar Parking Mandate - clarify penalty structure

   - Replaced vague 'encouraged' language with 'required'
   - Added enforcement mechanism (Section 4)
   - Fixed dead link: [EnergyHop](url)"
   ```

### Fixing Multiple Broken Links Across the Repository

1. **Run full audit**:
   ```bash
   python scripts/consistency_guardian.py --all
   ```

2. **Auto-update all redirects**:
   ```bash
   python scripts/consistency_guardian.py --update-redirects --all
   ```

3. **Manually fix remaining 404s**:
   ```bash
   # Consistency guardian output will show which policies have dead links
   # Find replacement URLs (use Wayback Machine if needed)
   # Edit policies directly, then re-run validation
   ```

4. **Commit in batches**:
   ```bash
   git add _policies/
   git commit -m "Fix broken links across policies

   - Auto-updated 12 HTTP→HTTPS redirects
   - Replaced 3 municipal website restructures (Aurora, Toronto)
   - Archived 1 Wikipedia link (403 Forbidden)
   
   Validation: 31/31 policies pass consistency_guardian"
   ```

---

## Quick Reference: Where to Put Things

| What | Where | Tools/Checks |
| --- | --- | --- |
| New policy text | `_policies/` | `consistency_guardian.py --all` |
| Policy example link | Inline in `_policies/*.md` | Check 5.5 validates automatically |
| CSS styling | `assets/css/` | Manual WCAG AA review |
| Interactive JS | `assets/js/` | `accessibility-test.js` tests |
| Python QA tool | `scripts/` | Peer review + testing on all 31 policies |
| Experimental tool | `scripts/tools/` | Keep, document, but don't use in workflow |
| Archived policy | `archive/` with `.YYYY-MM-DD.bak` | Link to evidence in README |
| Research PDF | `evidence/{policy-name}/` | Cite in official_sources |
| New issue template | `.github/ISSUE_TEMPLATE/` | Sync with DISCUSSION_GUIDELINES.md |
| Site navigation | `_layouts/default.html` | Update Jekyll config if structure changes |

---

## Summary: Organization Philosophy

**Three Core Principles**:

1. **Content First**: Policies are the product. Everything else serves the policies.
   - `_policies/` is primary; scripts exist to validate policies.

2. **Clarity at Scale**: 31+ policies + multiple contributors requires obvious structure.
   - Each directory has one purpose.
   - Naming is explicit (not abbreviated).
   - Experimental code is visibly separated from production.

3. **Integrity by Design**: Tools are built into workflow, not optional.
   - You can't commit a policy without running consistency_guardian.
   - Broken links are caught, not discovered by users.
   - Accessibility is tested, not assumed.

**Result**: A repository where anyone can find what they're looking for, understand what it does, and know how to contribute safely.

---

*Last updated: 2025-01-03*
