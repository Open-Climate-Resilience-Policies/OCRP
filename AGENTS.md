# AGENTS.md

> **⚠️ INSTRUCTION FOR AI AGENTS & CONTRIBUTORS:**
> Read this file before generating code, content, or PRs. This project has strict architectural patterns. Violating these rules will result in `git reset --hard`.

---

## 1. Project Identity & Scope

* **Name:** OCRaP.ai
* **Mission:** To move governance from "Trust Us" to **"Verify Everything."**
* **Repository Type:** Public GitHub Pages site built with Jekyll
* **Content:** Climate resilience policy library (markdown in `_policies/`) and public-facing interactive tools (static HTML/CSS/JS)
* **Tone:**
    * **Code:** Robust, secure, accessible.
    * **Content:** Cheeky, rebellious, but strictly accurate.
    * **Policy Text:** Legally sound, scientifically verified, economically persuasive.

### Non-negotiables
- **No fake UI:** If a control exists, it works. If it does not work, remove it.
- **No fabricated data:** No fake sources or claims. Citations must be real and verifiable.
- **No tracking:** No fingerprinting or "phone home" behavior in tools.
- **Progressive enhancement:** Core content and primary actions must work without JS when feasible.
- **Accessibility:** Target WCAG 2.2 AA for all public-facing pages and tools.

---

## 2. The "Integrity Engine" Protocols

We do not use the words "Truth" or "Fact" (which are politicized). We use **"Verification"** and **"Integrity."**

### Agent A: "The Scientist" (Validation)
* **Role:** Check physical reality.
* **Trigger:** Any claim regarding emissions, health, or engineering.
* **Instruction:** "Cross-reference claim X against provided Evidence Source Y. If not supported, flag as 'Unsubstantiated'."

### Agent B: "The CFO" (Stress Test)
* **Role:** Check economic viability.
* **Trigger:** Any mandate involving timelines, construction, or procurement.
* **Instruction:** "Review for supply chain lead times and 'Unfunded Mandates'. Flag vague terms like 'strive to' or 'encourage' as Liability Risks."

### Agent C: "The Sleep Doctor" (Health)
* **Role:** Public health impact analysis.
* **Trigger:** Housing codes, heat plans, air quality.
* **Instruction:** "Flag any housing policy that does not define a 'Maximum Indoor Temperature' (Nighttime Recovery)."

---

## 3. Localization & i18n Guidelines

> **CORE PRINCIPLE:** We do not translate words; we adapt **concepts**.

1.  **Legal System Check:**
    * Determine if target is **Common Law** or **Civil Code**.
    * Swap terms accordingly via `data/glossary.yaml` (e.g., *Easement* $\leftrightarrow$ *Servitude*).
2.  **Unit Hygiene:**
    * **Store:** Metric (SI).
    * **Display:** Use smart spans `<span data-measure="temp" data-value="28">28°C</span>`.
3.  **No "US-Defaultism":**
    * Do not assume "Summer" = "Hot" (Global South users exist). Use specific climate terms ("Dry Season").

---

## 4. Repository Technical Standards (Jekyll)

### Structure
- **Policies:** `_policies/` as markdown with required frontmatter
- **Layouts:** `_layouts/` for page templates
- **Assets:** `assets/` for CSS, JS, images
- **Tools:** Static HTML/CSS/JS pages for interactive calculators and utilities

### Conventions
- Keep additions consistent with existing navigation and page structure
- Maintain lightweight, usable, accessible design
- Test at both mobile and desktop widths before committing

---

## 5. Interactive Tools Standards

### Required Sections (every tool page)
1. **Clear page title** and one-sentence purpose
2. **Instructions** for inputs
3. **Results area** with appropriate ARIA live regions
4. **Error handling** section (user-visible)
5. **Limitations/assumptions** section
6. **"Sources / last verified"** section if referencing external facts

### Reliability Requirements
- **No uncaught exceptions** on page load
- **Wrap risky logic** in `try/catch` with user-visible error messages
- **If using `fetch`:**
  - Degrade gracefully when offline or blocked
  - Show loading and error states
  - Avoid sending user-entered content to third parties

### Privacy and Security
- Do not access `window.parent` or `window.top`
- Avoid localStorage/sessionStorage unless strictly required and documented
- **No third-party analytics** or tracking

---

## 6. Accessibility Requirements (WCAG 2.2 AA)

### Keyboard and Focus
- Every interactive element is reachable by keyboard
- Visible focus indicator (do not remove outlines)
- No keyboard traps
- Tab order matches visual order

### Labels and Names
- Every input has a programmatic label (`<label for>`, or `aria-label`/`aria-labelledby`)
- Buttons and links have accessible names matching visible labels
- Icon-only controls must have accessible names

### Errors and Dynamic Updates
- Validation errors must be:
  - Specific and actionable
  - Tied to the offending input (`aria-describedby`)
  - Shown in text (not color-only)
- Dynamic result updates must be announced via `role="status"` or `aria-live="polite"`

### Semantics
- One `<h1>` per page
- Use landmarks: `<header>`, `<main>`, `<footer>`
- Prefer native controls (`button`/`input`/`select`). Avoid div-as-button

### Touch Targets (WCAG 2.2)
- Controls must be sized/spaced to prevent mis-taps (minimum 24×24 CSS pixels)

---

## 7. Data Integrity and "Freshness" Rules

If a tool or policy references:
- Laws/regulations, standards versions (including WCAG)
- "Current" statistics, pricing, schedules, role-holders
- Recent events or temporary conditions

Then:
- **Cite an authoritative source** in-page, OR
- **Label content as unverified** and avoid definitive language
- **Include:** "Last verified: YYYY-MM-DD" when verified

### Content Creation Using AI
AI can be used to normalize policy text into the project's generic policy format, but:
- Result must remain consistent with contribution structure
- Must include resource links back to original sources
- Must not fabricate citations or data

---

## 8. Workflows

### The "Policy Bundle" Pattern
Every policy is a folder, not a file:
* `/policies/{slug}/index.md` (Core Text)
* `/policies/{slug}/evidence/` (PDFs/txt)
* `/policies/{slug}/implementations/` (Local YAML overlays)

### The "Watchdog" Workflow
* **Never** generate a URL you haven't visited
* **Always** submit new URLs to the Wayback Machine API upon ingestion

---

## 9. Agent Responsibilities: Metadata, Filenames, and Safe Edits

### 1. Filename Conventions
- Use short, descriptive, country-neutral slugs (e.g., `solar-parking.md` not `france-solar-parking.md`)
- Filenames should be lowercase, dash-separated, and match the `slug` frontmatter exactly

### 2. Mandatory Frontmatter Keys (every policy)
- `date`: ISO date string for the document revision (YYYY-MM-DD)
- `slug`: short string matching the filename (no country prefix unless jurisdiction-specific)
- `keywords`: a short array of 2–5 tags for discovery
- `official_sources`: an array of authoritative citation objects or an empty array if none found

### 3. Edit Checklist (pre-commit)
- Ensure the `slug` matches the filename and contains no spaces or uppercase characters
- Ensure `date` is today's revision date when adding metadata
- Add `official_sources` entries when available; prefer primary legal sources
- Remove any `improvements` bullets that only request metadata already added
- When renaming a file to remove country tokens, create the new file and delete the old one in the same patch to avoid duplication

### 4. Review Triggers
- **Agent A (The Scientist):** Trigger when `hazard_type` includes health or engineering claims — verify citations
- **Agent B (The CFO):** Trigger when `fiscal_profile` or cost estimates exist — verify assumptions
- **Agent C (The Sleep Doctor):** Trigger when indoor temperature guidance exists — verify public health thresholds

---

## 10. Definition of Done (for any new tool or major change)

Before merging/publishing:
- [ ] Manual keyboard pass: tab through, activate controls, verify focus visibility
- [ ] Verify labels, errors, and result announcements
- [ ] Test at mobile width and desktop width
- [ ] Confirm no fabricated data or unstated assumptions
- [ ] Confirm no third-party calls or tracking
- [ ] Run accessibility checks (automated + manual)
- [ ] Verify all citations are real and reachable

---

*Verified by OCRaP.ai Command.*