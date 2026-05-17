# FEATURES.md

Canonical index of user-visible behavior for OCRP.  
Each behavior must be:

1. Written as a user story with a stable Story ID.
2. Captured in Gherkin (`/home/runner/work/OCRP/OCRP/features/*.feature`).
3. Covered by executable Playwright behavior tests (`/home/runner/work/OCRP/OCRP/tests/behavior/`).

## Story Index

| Story ID | User Story | Gherkin Feature | Playwright Coverage | Status |
|---|---|---|---|---|
| BDD-001 | As a visitor, I can search the policy library so I can quickly find relevant policies. | `/home/runner/work/OCRP/OCRP/features/search-policies.feature` | `/home/runner/work/OCRP/OCRP/tests/behavior/core-user-journeys.spec.js` (`BDD-001`) | Pilot |
| BDD-002 | As a visitor, I can open a policy detail page from the library so I can read full requirements and sources. | `/home/runner/work/OCRP/OCRP/features/view-policy-details.feature` | `/home/runner/work/OCRP/OCRP/tests/behavior/core-user-journeys.spec.js` (`BDD-002`) | Pilot |
| BDD-003 | As a visitor, I can paginate the policy library so I can browse all entries in manageable pages. | `/home/runner/work/OCRP/OCRP/features/browse-policy-library.feature` | `/home/runner/work/OCRP/OCRP/tests/behavior/core-user-journeys.spec.js` (`BDD-003`) | Pilot |

## Traceability Rules

- Any change to user-facing behavior in templates, pages, policies index, or tools must update this file.
- Any new Story ID must include:
  - at least one `.feature` scenario;
  - at least one Playwright behavior test;
  - a mapping row in this index.
- CI enforces parity between feature specs and behavior tests to prevent drift.

## Scope for Current Pilot

- Search journey: `/search/`
- Policy detail journey: `/policies/` -> specific policy page
- Interactive library journey: `/policies/` pagination controls

