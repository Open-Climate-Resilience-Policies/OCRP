# Accessibility Commitment (ACCESSIBILITY.md)

## 1. Our Commitment
We believe accessibility is a subset of quality, and a prerequisite for true transparency in our climate policies. This project commits to **WCAG 2.2 AA** standards for all public-facing pages and interactive tools. We track our progress publicly to remain accountable to our users.

## 2. Real-Time Health Metrics
| Metric | Status / Value |
| :--- | :--- |
| **Open A11y Issues** | [View Accessibility Issues](https://github.com/Open-Climate-Resilience-Policies/OCRP/issues?q=is%3Aopen+label%3Aaccessibility) |
| **Automated Test Framework** | Playwright + axe-core (`npm run test:accessibility`) |
| **Color Contrast Target** | WCAG 2.2 AA |

## 3. Contributor Requirements (The Guardrails)
To contribute to OCRP, you must follow our core accessibility requirements (`AGENTS.md` section 6):

### Keyboard and Focus
- Every interactive element must be reachable by keyboard.
- Visible focus indicators must be maintained (do not remove `outline`).
- No keyboard traps.
- Tab order must match the visual order.

### Labels and Names
- Every input requires a programmatic label (`<label for>`, or `aria-label`/`aria-labelledby`).
- Buttons and links must have accessible names matching visible labels.
- Icon-only controls must have accessible names.

### Errors and Dynamic Updates
- Validation errors must be specific, actionable, tied to the offending input (`aria-describedby`), and shown in text (not color-only).
- Dynamic result updates must be announced via `role="status"` or `aria-live="polite"`.

### Semantics and Touch Targets
- One `<h1>` per page.
- Use landmarks: `<header>`, `<main>`, `<footer>`.
- Prefer native controls (`button`/`input`/`select`). Avoid div-as-button.
- Touch targets must be sized/spaced to prevent mis-taps (minimum 24×24 CSS pixels per WCAG 2.2).

## 4. Reporting & Severity Taxonomy
If you encounter an accessibility barrier, please [Report an Issue on GitHub](https://github.com/Open-Climate-Resilience-Policies/OCRP/issues/new). We prioritize based on:
- **Critical:** Prevents a user from completing a core task (e.g., "Cannot navigate policy text").
- **High:** Significant difficulty, but a workaround exists.
- **Medium:** Annoyance or inconsistent experience.

## 5. Automated Check Coverage
We rely on automated checks to prevent regressions. All changes to the site's layout or tools must pass our `accessibility-test.js` script. 
- **Tests command:** `npm run test:accessibility`
- Please remember that automated testing only catches ~30% of accessibility issues. Manual keyboard and screen reader verification is strictly required for new interactive components.
