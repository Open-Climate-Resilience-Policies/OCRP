# How to Contribute to OCRaP.ai

**We don't need you to be a coder. We need you to be angry, accurate, and active.**

This project is a coalition of the willing. Whether you are a python dev, a tenant lawyer, or just someone tired of bad policy, we need you.

## 🚦 Choose Your Lane

### 🟢 Lane 1: The "Drive-By" Fixer
**I see a typo, a broken link, or a lie.**
* Don't worry about GitHub code.
* 👉 [Click here to file a "Loophole Report"](../../issues/new?template=1-loophole-report.yml).
* *We will fix it and credit you.*

### 🟡 Lane 2: The "Expert Witness"
**I have a better citation or study.**
* If you see a claim like *"Green roofs save money"* without a source:
* Go to the **Evidence** tab of that policy.
* Upload your PDF or URL. Our AI will verify it.

### 🔴 Lane 3: The "Policy Wonk"
**I want to rewrite the law.**
* We use **"Amendments"** (Pull Requests) to change policy text.
* **Rule:** You must explain *why* your change makes the policy stronger/fairer in the PR description.
* **Constraint:** You must pass the "CFO Agent" stress test (Is it economically viable?).

---

## 🏆 Badges & Gamification
We track impact, not just commits.
* 🕵️ **Truth Seeker:** Found a hallucination in a government doc.
* 🛡️ **Librarian:** Archived 10+ dead links.
* 🤖 **Automator:** Improved a Python script.

*Join the Discussion on [Discord] to meet other citizen lobbyists.*

---

## ✅ Behavior-Driven Guardrails for UX/Tool Changes

If your PR changes user-visible behavior (navigation, page flow, search, pagination, tool logic, form behavior, or UI controls), you must update behavior specs and tests:

1. Update `/home/runner/work/OCRP/OCRP/FEATURES.md` with Story ID traceability.
2. Add or update a scenario in `/home/runner/work/OCRP/OCRP/features/*.feature`.
3. Add or update matching Playwright behavior tests in `/home/runner/work/OCRP/OCRP/tests/behavior/`.

Required rule: **new feature = new scenario + test + traceability entry**.

PRs that modify feature specs without matching behavior tests (or behavior tests without feature specs) are rejected by CI.
