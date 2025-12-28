---
layout: policy
title: "EV-Ready & Right-to-Charge Ordinance"
type: generic-policy
summary: "A phased municipal policy mandating 100% EV-readiness in new buildings, establishing a binding Right-to-Charge process for renters and condo owners, and requiring fire-safe micromobility storage and charging."
hazard_type:
  - "transport emissions"
  - "tenant access inequity"
  - "electrical safety"
  - "lithium-ion fire risk"
policy_category: "transportation & housing"
implementation_level: "municipal"
related_policies:
  - "dynamic-urban-access-zones"
  - "community-retrofit-aggregation"
date: "2025-12-21"
slug: "right-to-charge"
keywords:
  - "EV-ready"
  - "right-to-charge"
  - "EV energy management"
  - "tenant protections"
  - "e-bike safety"
official_sources:
  - url: "https://web.archive.org/web/20241009201922/https://eur-lex.europa.eu/eli/reg/2023/1804/oj"
    title: "EU Regulation (EU) 2023/1804 on the deployment of alternative fuels infrastructure (AFIR) — archived 2024-10-09"
    accessed: "2025-12-28"
  - url: "https://web.archive.org/web/20230326025938/https://eur-lex.europa.eu/eli/dir/2014/94/oj"
    title: "EU Directive 2014/94/EU on the deployment of alternative fuels infrastructure — archived 2023-03-26"
    accessed: "2025-12-28"
  - url: "https://california.public.law/codes/civil_code_section_1947.6"
    title: "California Civil Code §1947.6 — tenant right to request EV charging station installation"
    accessed: "2025-12-28"
  - url: "https://www.quebec.ca/nouvelles/actualites/details/code-de-construction-et-code-de-securite-projets-de-reglement-en-electricite-publies-pour-commentaires-61404"
    title: "Gouvernement du Québec / RBQ — draft construction and electrical code amendments supporting EV supply equipment infrastructure in new multi-unit buildings"
    accessed: "2025-12-28"
  - url: "https://www.publicationsduquebec.gouv.qc.ca/fileadmin/gazette/pdf_encrypte/lois_reglements/2025A/107283.pdf"
    title: "Gazette officielle du Québec — draft Regulation text (EV supply equipment infrastructure requirements)"
    accessed: "2025-12-28"
  - url: "https://web.archive.org/web/20231204190754/https://www.nysenate.gov/legislation/bills/2023/A8134"
    title: "New York State Assembly Bill A8134 — prohibiting sale of uncertified lithium-ion batteries"
    accessed: "2025-12-28"
  - url: "https://www.nfpa.org/Education-and-Research/Electrical/Ebikes"
    title: "NFPA — e-bike and e-scooter lithium-ion battery safety guidance"
    accessed: "2025-12-28"
  - url: "https://www.ul.com/services/e-bikes-certificationevaluating-and-testing-ul-2849"
    title: "UL Solutions — UL 2849 certification overview (e-bike electrical systems safety)"
    accessed: "2025-12-28"
---

## Overview

As transportation electrifies, the main barrier is no longer vehicle range but **reliable home charging access**, especially for renters and condo owners. Retrofitting conduit after construction can cost four to six times more than planning for it at permit stage. At the same time, the rise of e-bikes and e-scooters has created a new fire risk when uncertified lithium-ion batteries charge inside living spaces.

This ordinance makes electric-vehicle access enforceable rather than aspirational. It mandates **100% electric-vehicle readiness at build time**, creates a legally defined **Right-to-Charge workflow** so residents cannot be stalled indefinitely, and requires **fire-safe micromobility rooms** with certified equipment.

**Key definitions used in this ordinance:**
- **Electric-vehicle-ready:** The parking space already includes conduit, pull strings, panel capacity, and a reserved pathway so charging equipment can be added without breaking finished surfaces.
- **Electric vehicle supply equipment:** Level-two charging equipment that meets national electrical code requirements.
- **Electric vehicle energy management system:** Hardware/software that balances load, enforces circuit limits, and generates auditable charging data.
- **Micromobility device:** An e-bike, e-scooter, or similar lithium-ion powered device subject to NFPA and UL2849 fire-safety guidance.

These definitions align local code enforcement with AFIR terminology and keep the Integrity Engine vocabulary consistent across related policies. Every mandate below references at least one agency so responsibility for verification is never ambiguous. The glossary in data/glossary.yaml shall be updated concurrently so translations and legal crosswalks remain synchronized.

Integrity Engine reviewers log each definition change with a timestamped note so audits can trace when terminology shifted and which downstream templates require updates.

## Policy 1: The "100% Electric-Vehicle Ready" Code (New Construction)

**Concept:**
Installing chargers in every space on day one is unnecessary; routing conduit and sizing panels everywhere is affordable and avoids the “charger lottery.”

**The Policy:**
All new residential and commercial buildings **with on-site parking** must meet the **100% electric-vehicle-ready standard**:
1. **Conduit Everywhere:** Designers shall route conduit (with pull strings) to one hundred percent of parking spaces so a future level-two circuit can be installed without opening finished walls.
2. **Capacity Planning:** Plan review must show load calculations that include the future charging-equipment demand consistent with AFIR and local electrical code methodology. Panel schedules shall reserve breaker positions and bus capacity for the eventual circuits.
3. **Energy Management Systems:** Buildings with more than twenty parking spaces shall install an electric-vehicle energy management system capable of allocating load across chargers, enforcing circuit limits, and logging kilowatt-hours for billing or sub-metering.
4. **Interoperability:** Backbone infrastructure must allow charger replacement without re-pulling conduit and shall support open protocols where available so properties are not locked into a single vendor.

**Compliance evidence:**
- Department of Buildings plan examiners shall require single-line diagrams and load calcs showing future electric-vehicle loads.
- Final inspections shall include as-built photo documentation of conduit terminations and management-system commissioning logs that demonstrate load balancing and data export capability.

**Metrics and reporting:**
- Building departments publish quarterly counts of permits that meet the electric-vehicle-ready checklist, including the share of parking spaces with verified conduit runs.
- Utilities receive anonymized load-calculation spreadsheets so they can forecast feeder upgrades and confirm that demand charges align with management-system design assumptions.
- Property owners must retain energy-management logs for five years so auditors can confirm that load-sharing features remain enabled after occupancy.

**Capital planning guidance:**
- Require transformer-sparing calculations that demonstrate how load management maintains diversity factors below utility thresholds.
- Document default conductor and breaker sizes for typical stall counts so small developers are not forced to re-engineer each project from scratch.
- Publish comparative cost data (per space) for conduit-first designs versus retrofits to make the economic case clear to finance teams.

**Evidence:**
Québec’s Régie du bâtiment (RBQ) has published draft code amendments requiring electric-vehicle-ready infrastructure in new multi-unit buildings, demonstrating feasibility and cost avoidance for future residents.

## Policy 2: The "Right-to-Charge" (Tenant Protections)

**Concept:**
Residents are willing to pay for chargers, but inconsistent landlord or homeowner association responses create an artificial barrier. A predictable workflow makes the right meaningful.

**The Policy:**
Landlords and homeowner associations **shall not unreasonably restrict** a resident from installing charging equipment in an assigned/deeded space when the following conditions are met:
1. **Cost Responsibility:** The resident funds equipment, installation, and electricity (via sub-meter, energy-management billing, or another verified method) and receives an itemized cost disclosure before work starts.
2. **Qualified Work:** A licensed contractor performs the installation, permits are closed, and the resident provides inspection sign-off plus proof of insurance where required.
3. **Restoration & Indemnity:** A standard lease or association addendum covers restoration at move-out and indemnification for resident-caused damage, using the city’s published template to avoid bespoke negotiations.

**Administrative Timelines:**
- Receipt acknowledgment due within **ten business days** plus a tracking number issued via the city’s online workflow tool.
- Approval or a technically specific denial due within **sixty days**. Failure to respond constitutes automatic approval subject to code compliance, and the city may issue a corrective order.

**Allowed Denials (Narrow):**
- No assigned/deeded space exists.
- Documented electrical capacity is insufficient **and** the resident declines to fund the upgrade.
- A licensed engineer certifies a material safety constraint or code violation.

**Equity & Anti-Retaliation:**
Rent increases, service reductions, or lease terminations in response to a Right-to-Charge request are prohibited and subject to fines. The housing department shall maintain a hotline and mediation program for renters whose landlords fail timelines or attempt retaliation.

**City Support Materials:**
The city publishes standard request forms, lease and association addenda, and a technical checklist so applicants, landlords, and inspectors have a common workflow, mirroring California Civil Code Section 1947.6. Materials shall include a transparent fee calculator, inspection close-out checklist, and sample billing language for the energy management platforms.

**Workflow for request handling:**
1. Residents submit the standardized form along with preliminary contractor estimates and proof of parking rights.
2. Landlords upload acknowledgements to the city portal, triggering automatic reminders as the ten-day and sixty-day milestones approach.
3. Approvals include a scope-of-work summary, insurance requirements, and any utility coordination steps so all parties have the same expectations.
4. Denials must cite the exact code section or engineering report supporting the rejection, and the city automatically schedules mediation within fifteen days.

**Documentation package:**
- Electrical drawings stamped by a licensed professional.
- Commissioning report demonstrating billing accuracy, including proof that the resident can view consumption data.
- Photos showing protective bollards, labeling, and tamper-resistant hardware when equipment is mounted in shared garages.

**Equity guardrails:**
- Require landlords to disclose any proposed rent adjustments related to charging installations and provide evidence that increases match actual utility pass-through costs.
- Mandate translation of request forms and dispute decisions into the top five local languages so immigrant renters can exercise the right without hiring counsel.
- Tie eligibility for city housing incentives to demonstrated compliance with Right-to-Charge timelines, preventing bad actors from accessing public subsidies.

## Policy 3: Micromobility & Fire Safety (The E-Bike Rules)

**Concept:**
Micromobility is essential for low-carbon trips, but uncertified lithium-ion batteries are causing fatal fires. Safe storage, certified devices, and clear enforcement authority are mandatory.

**The Policy:**
1. **Safe Storage Rooms:** Multi-family and commercial buildings with more than ten dwellings shall provide secure, ground-level or elevator-accessible micromobility rooms separated from primary egress paths.
2. **Minimum Safety Features:** Rooms must have one-hour fire-resistance construction, sprinkler or fire detection tied to the central alarm, mechanical ventilation, signage banning corridor charging, tamper-resistant receptacles, and lockable racks to prevent blockage of exits.
3. **Certified Devices Only:** Charging is limited to devices and batteries certified under UL2849 or another recognized standard. Non-certified or damaged batteries must be removed, mirroring New York enforcement actions that target uncertified sales statewide.
4. **Retail & Education Measures:** Where authority allows, the city restricts sale or lease of uncertified batteries/devices and publishes a tenant-facing NFPA-aligned safety guide plus multilingual notices for building lobbies.

**Verification:**
- Fire inspectors shall check sign-in logs for micromobility rooms, confirm certification labels, and document violations in a public-facing dashboard to deter serial offenders.
- Large buildings must file an annual micromobility management plan describing how they track occupant devices, enforce certified-battery rules, and coordinate disposal of damaged packs.
- Property managers retain maintenance logs for charging rooms, including ventilation inspections and alarm tests, for at least five years.

**Retail enforcement steps:**
- Licensing teams conduct quarterly sweeps of retailers and online marketplaces that sell into the jurisdiction, targeting uncertified battery kits.
- Repeat violators face escalating penalties, including product seizures and temporary closure orders.
- Public awareness campaigns highlight approved vendors and safe storage practices, aligning with NFPA guidance.

**Emergency coordination:**
Fire departments, housing agencies, and emergency management offices shall run joint drills on lithium-ion incident response, ensuring that evacuation plans account for the new storage rooms and that residents know where to report smoking or damaged devices.

***

## Implementation Roadmap (Phased Approach)

To allow the market to adapt, the policy follows a phased trigger timeline.

### Phase One: New Build Gate (Months one through twelve)
- Update building and electrical codes to require one hundred percent electric-vehicle-ready designs for permits filed after the effective date and publish inspection checklists.
- Adopt micromobility storage requirements for new multi-family buildings and begin retailer education on certified battery rules.
- Train permit reviewers on how to verify energy-management schematics so inconsistent interpretations do not slow approvals.
- Establish a shared dataset with the electric utility summarizing projected load by feeder so upgrades can be sequenced before occupancy.
- Offer technical assistance clinics for small developers so compliance knowledge is not limited to major firms.

### Phase Two: Right-to-Charge Activation (Months twelve through twenty-four)
- Protections apply to existing buildings with more than fifty units. Landlords must meet the ten-day acknowledgement and sixty-day decision timelines.
- City issues model request forms, lease and association addenda, and a dispute-resolution contact within the housing or buildings department.
- Launch a public tracker summarizing request volumes, approvals, denials, and median response times.
- Stand up a rapid-response ombudsperson team that can issue temporary work authorizations when landlords repeatedly miss deadlines.
- Pair the Right-to-Charge process with workforce grants so local electricians receive training on energy-management platforms and micromobility safety requirements.

### Phase Three: Retrofit Expansion (Year Three and beyond)
- Extend Right-to-Charge to smaller buildings and mixed-use sites.
- Launch conduit/panel upgrade incentives focused on older buildings with capacity constraints, prioritizing environmental justice districts.
- Require periodic inspections of micromobility rooms and publish annual compliance statistics so residents can verify progress.
- Integrate energy-management performance data into open-data portals so researchers can verify whether load-sharing is preventing transformer overloads.
- Evaluate whether bidirectional (vehicle-to-building) readiness requirements are warranted once adoption targets are met.

**Integrity Engine checkpoints:**
- Monthly dashboard review verifying that approvals, denials, and enforcement actions remain proportional across neighborhoods.
- Crosswalk of micromobility incident data against inspection logs to identify enforcement gaps.
- Randomized field audits comparing portal data to on-site conditions (conduit, signage, management-system logs).
- Publication of remediation timelines for every critical violation so the public can verify that penalties are not quietly waived.

**Community engagement requirements:**
- Host quarterly tenant and condo clinics that walk residents through the Right-to-Charge forms, highlight mediation outcomes, and collect feedback on enforcement pain points.
- Publish interactive maps showing which neighborhoods have achieved electric-vehicle-ready compliance, enabling watchdog groups to spot inequities.
- Partner with tenant unions and small-business groups to co-design dispute-resolution scripts so both renters and landlords understand their rights.
- Provide stipends for community-based organizations that help residents document micromobility hazards and submit evidence to the enforcement portal.

**Budget transparency:**
- The finance department publishes annual expenditure reports covering staffing, inspections, mediation, and incentive programs tied to this ordinance.
- Any proposed fee changes (permit surcharges, inspection fees) must include a cost-recovery rationale so ratepayers see how funds sustain enforcement capacity.

## Enforcement & Compliance

1. **Permit Holds (Buildings + Transportation Departments):** The Department of Buildings, in coordination with the transportation department, shall withhold Certificates of Occupancy until inspectors verify electric-vehicle-ready conduit, reserved panel capacity, management-system commissioning (where required), and micromobility room compliance with documented photos or checklists.
2. **Tenant Remedies (Housing Department):** Missing the ten-day acknowledgement or sixty-day decision triggers daily fines (recommended two hundred fifty currency units per day) and allows residents to escalate to the housing department, which can issue administrative orders or revoke rental registrations.
3. **Fire Code Authority (Fire Marshal):** The Fire Marshal may issue stop-use orders for non-compliant micromobility rooms, confiscate uncertified batteries under NYC-style authority, and require proof of remediation before reopening.
4. **Transparency & Audits:** The city publishes annual metrics on electric-vehicle-ready compliance rates, Right-to-Charge requests, approvals, denials, micromobility enforcement actions, and audit findings so the Integrity Engine can verify progress and target future inspections.
5. **Data retention:** Owners must store inspection photos, conduit test results, and mediation correspondence for at least ten years so auditors can reconstruct compliance history during disputes.
6. **Public integrity dashboard:** The municipality maintains an accessible dashboard showing complaint resolution times, fine collections, and micromobility enforcement sweeps, along with contacts for each responsible agency.
