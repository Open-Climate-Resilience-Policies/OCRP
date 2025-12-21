# AGENTS.md

> **⚠️ INSTRUCTION FOR AI AGENTS & CONTRIBUTORS:**
> Read this file before generating code, content, or PRs. This project has strict architectural patterns. Violating these rules will result in `git reset --hard`.

---

## 1. Project Identity
* **Name:** OCRaP.ai
* **Mission:** To move governance from "Trust Us" to **"Verify Everything."**
* **Tone:**
    * **Code:** Robust, secure, accessible.
    * **Content:** Cheeky, rebellious, but strictly accurate.
    * **Policy Text:** Legally sound, scientifically verified, economically persuasive.

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

## 4. Workflows

### The "Policy Bundle" Pattern
Every policy is a folder, not a file.
* `/policies/{slug}/index.md` (Core Text)
* `/policies/{slug}/evidence/` (PDFs/txt)
* `/policies/{slug}/implementations/` (Local YAML overlays)

### The "Watchdog" Workflow
* **Never** generate a URL you haven't visited.
* **Always** submit new URLs to the Wayback Machine API upon ingestion.

---

*Verified by OCRaP.ai Command.*

## 5. Agent Responsibilities: Metadata, Filenames, and Safe Edits

1. Filename Conventions:
    - Use short, descriptive, country-neutral slugs for policy filenames (e.g., `solar-parking.md` not `france-solar-parking.md`).
    - Filenames should be lowercase, dash-separated, and match the `slug` frontmatter exactly.

2. Mandatory Frontmatter Keys (every policy):
    - `date`: ISO date string for the document revision (YYYY-MM-DD).
    - `slug`: short string matching the filename (no country prefix unless the policy is jurisdiction-specific).
    - `keywords`: a short array of 2–5 tags for discovery.
    - `official_sources`: an array of authoritative citation objects or an empty array if none found.

3. Edit Checklist for Agents (pre-commit):
    - Ensure the `slug` matches the filename and contains no spaces or uppercase characters.
    - Ensure `date` is today's revision date when adding metadata.
    - Add `official_sources` entries when available; prefer primary legal sources.
    - Remove any `improvements` bullets that only request metadata already added.
    - When renaming a file to remove country tokens, create the new file and delete the old one in the same patch to avoid duplication.

4. Review Triggers:
    - Agent A (The Scientist): Trigger when `hazard_type` includes health or engineering claims — verify citations.
    - Agent B (The CFO): Trigger when `fiscal_profile` or cost estimates exist — verify assumptions.
    - Agent C (The Sleep Doctor): Trigger when indoor temperature guidance exists — verify public health thresholds.

Agents must follow this checklist to keep the policy corpus consistent and machine-readable.