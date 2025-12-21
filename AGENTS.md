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