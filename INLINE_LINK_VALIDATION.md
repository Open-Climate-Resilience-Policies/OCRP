# Inline Link Validation in Consistency Guardian

## Overview

The `consistency_guardian.py` script now includes automated validation of **real-world example links** within policy markdown content (Check 5.5). This ensures that all policies maintain quality citations to real-world precedents and case studies that demonstrate policy implementation.

## What It Checks

### 1. **Inline Link Presence**
   - Detects markdown-formatted links: `[example text](https://url)`
   - Warns if no real-world examples are cited (policies should cite 2-4 precedents)
   - Does not count unlinked text mentions as valid examples

### 2. **URL Accessibility**
   - Validates each inline URL with HTTP HEAD request
   - Reports dead links (4xx, 5xx status) as **critical issues**
   - Timeout: 5 seconds per URL (configurable via `CG_TIMEOUT_SECONDS`)
   - Gracefully handles network errors and redirects

### 3. **Source Diversity**
   - Tracks all unique domains cited in inline examples
   - **Warning**: If all examples cite the same domain
   - Encourages cross-domain citations for credibility

### 4. **Authoritative Sources**
   - Checks for presence of authoritative domains:
     - `.gov` - Government sources
     - `.edu` - Educational institutions
     - `europa.eu` - European Commission
     - `legislation.*` - Legal repositories
     - `parliament.*` - Parliamentary sources
     - `.org` (non-news) - Established organizations
   - **Warning**: If inline examples contain no authoritative sources

## Example Output

```
✅ PASSED
- Inline examples: 3 links, 2 unique domains

⚠️ WARNINGS
- Only 2 inline examples found; policies should cite 2-4 real-world precedents
- All inline examples cite same domain (example.gov); consider diverse sources

🚫 CRITICAL
- Dead inline link: [Retrofit Program](https://example.org) - 404
```

## Policy Standards

All policies **should** include:
- ✅ 2-4 real-world examples with inline markdown links
- ✅ Examples from diverse authoritative sources
- ✅ At least one government (.gov/.edu) or official (.europa.eu) source
- ✅ Links to actual precedent implementations, not just news coverage

## Usage

### Check a Single Policy
```bash
python scripts/consistency_guardian.py _policies/solar-parking.md
```

### Check All Policies
```bash
python scripts/consistency_guardian.py --all
```

### Integration with Git Workflow
```bash
python scripts/consistency_guardian.py --changed  # Check only modified files
```

## When To Fix

**Fix immediately if:**
- Policy has **0 inline links** (add real-world examples)
- Policy has **dead links** (404, 403 errors) - replace with working URLs
- All examples cite **single domain** - add examples from other jurisdictions

**Consider improving if:**
- Only 1 example cited (add 1-2 more)
- No authoritative sources in examples (prefer .gov, .edu, legislation sites)
- All examples from similar geographic region (diversify globally)

## Example Fixes

### ❌ Before (No Links)
```markdown
Many cities have implemented solar parking requirements following 
the model established in France, with adoption spreading across Europe.
```

### ✅ After (With Links)
```markdown
Many cities have implemented solar parking requirements following the 
model established by [France's national solar parking mandate](https://www.example.org/...). 
[Portugal](https://www.example.org/...) and [Spain](https://www.example.org/...) 
have adopted similar approaches, with adoption spreading across Europe.
```

## Real-World Example

The [solar-parking policy](../../_policies/solar-parking.md) demonstrates inline link validation:

```
### Real-World Implementation Examples

**France's National Mandate:**
- [Legislation approved by French Senate](https://www.theguardian.com/world/2022/nov/09/france-to-require-all-large-car-parks-to-be-covered-by-solar-panels)
  requires all large car parks covered by solar panels
```

This policy now:
- ✅ Passes all URL accessibility checks
- ✅ Cites authoritative source (The Guardian + legislation)
- ✅ Links directly to verifiable precedents
- ✅ Demonstrates implementation across multiple jurisdictions

## Technical Notes

### URL Validation Method
Uses Python's `requests` library with:
```python
response = requests.head(url, timeout=5, allow_redirects=True)
if response.status_code >= 400:
    # Report as dead link
```

### Network Resilience
- Timeout: 5 seconds (prevents hanging on unresponsive servers)
- Redirects: Followed automatically
- Exceptions: Caught and reported with error details

### Edge Cases Handled
- Fragment links (`#section`) - Skipped (internal navigation)
- Relative links (`/path/page`) - Skipped (local site navigation)
- HTTP → HTTPS redirects - Followed, accepted
- Rate limiting - Reported with HTTP status

## Integration with CI/CD

When automated checks are enabled (Phase 2), dead inline links will:
1. **Fail the build** if marked as critical
2. **Warn during review** if only 1 example cited
3. **Pass** if 2+ diverse, authoritative sources present

## Future Enhancements

Possible expansions:
- [ ] Archive check: Propose Wayback Machine snapshots for dead links
- [ ] Domain classification: Automate categorization (gov/edu/org/news)
- [ ] Example quality metrics: Score based on authority and diversity
- [ ] Snapshot integration: Auto-archive examples at submission time
- [ ] LLM analysis: Use local LLM to verify example relevance to policy

---

**Maintained by:** Agent D (Consistency Guardian)  
**Last Updated:** 2025-12-28  
**Status:** Production (Check 5.5)
