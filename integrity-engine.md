---
layout: default
title: The Integrity Engine
permalink: /integrity-engine/
date: 2026-05-03
slug: integrity-engine
summary: How AI agents and open-source code work together to keep every policy accurate, binding, and trustworthy — and how you can verify it yourself.
keywords: [integrity, transparency, ai-agents, verification, workflow]
official_sources:
  - url: "https://github.com/Open-Climate-Resilience-Policies/OCRP/blob/main/scripts/consistency_guardian.py"
    title: "Consistency Guardian — source code"
    accessed: "2026-05-03"
  - url: "https://github.com/Open-Climate-Resilience-Policies/OCRP/blob/main/AGENTS.md"
    title: "AGENTS.md — agent protocol specification"
    accessed: "2026-05-03"
---

# The Integrity Engine

<p class="ie-lead">We don't ask you to <em>trust us</em>. We show you the work. Every policy in this library passes through a four-stage verification pipeline before it reaches you — and every gate is open-source, auditable, and logged.</p>

---

## The Core Question: How Do We Trust It?

Three things make this library different from a random climate blog:

1. **The pipeline is public.** Every rule the AI follows is written in [`AGENTS.md`](https://github.com/Open-Climate-Resilience-Policies/OCRP/blob/main/AGENTS.md) and enforced by open-source Python scripts anyone can read, run, or fork.
2. **Humans are in the loop.** AI agents flag problems; humans approve changes to the main branch. No AI can merge content autonomously.
3. **We use "Verification", not "Truth".** Claims are either *substantiated by cited evidence* or *flagged as unsubstantiated*. There is no middle ground.

---

## The Four Agents

<div class="ie-agents" role="list" aria-label="Integrity Engine agents">

  <div class="ie-agent" role="listitem">
    <div class="ie-agent-icon" aria-hidden="true">🔬</div>
    <div class="ie-agent-body">
      <h3 class="ie-agent-name">Agent A — The Scientist</h3>
      <p class="ie-agent-role"><strong>Role:</strong> Physical-reality check</p>
      <p class="ie-agent-trigger"><strong>Trigger:</strong> Any claim about emissions, health outcomes, or engineering specifications</p>
      <p>Cross-references every factual claim against the cited evidence source. If the physics doesn't support the claim, the policy is flagged <strong>Unsubstantiated</strong> and cannot proceed until the citation is corrected or the claim is removed.</p>
    </div>
  </div>

  <div class="ie-agent" role="listitem">
    <div class="ie-agent-icon" aria-hidden="true">📊</div>
    <div class="ie-agent-body">
      <h3 class="ie-agent-name">Agent B — The CFO</h3>
      <p class="ie-agent-role"><strong>Role:</strong> Economic stress test</p>
      <p class="ie-agent-trigger"><strong>Trigger:</strong> Any mandate involving procurement timelines, construction, or cost estimates</p>
      <p>Reviews supply-chain lead times and flags "Unfunded Mandates". Catches vague economic language — "strive to be cost-effective" → rejected; "shall not exceed $X per unit" → accepted. Timelines must reference a specific trigger event, not an absolute date.</p>
    </div>
  </div>

  <div class="ie-agent" role="listitem">
    <div class="ie-agent-icon" aria-hidden="true">🌡️</div>
    <div class="ie-agent-body">
      <h3 class="ie-agent-name">Agent C — The Sleep Doctor</h3>
      <p class="ie-agent-role"><strong>Role:</strong> Public-health impact analysis</p>
      <p class="ie-agent-trigger"><strong>Trigger:</strong> Any housing code, heat plan, or air-quality policy</p>
      <p>Checks that every indoor-environment policy defines a <strong>Maximum Indoor Temperature for Nighttime Recovery</strong>. Policies that affect sleep and health without quantified thresholds are returned for revision — a number without a unit, or a unit without a source, fails this check.</p>
    </div>
  </div>

  <div class="ie-agent" role="listitem">
    <div class="ie-agent-icon" aria-hidden="true">🛡️</div>
    <div class="ie-agent-body">
      <h3 class="ie-agent-name">Agent D — The Consistency Guardian</h3>
      <p class="ie-agent-role"><strong>Role:</strong> Structure, citations, overlap, and enforcement language</p>
      <p class="ie-agent-trigger"><strong>Trigger:</strong> Every new or edited policy, plus a monthly full-library audit</p>
      <p>Runs eight checks: frontmatter completeness, binding language, numeric threshold validity, overlap with existing policies, citation link health, geographic compatibility, readability, and an adversarial "red team" stress test. The script is open-source: <a href="https://github.com/Open-Climate-Resilience-Policies/OCRP/blob/main/scripts/consistency_guardian.py"><code>scripts/consistency_guardian.py</code></a>.</p>
    </div>
  </div>

</div>

---

## The Full Workflow

The diagram below shows the complete lifecycle of a policy — from first draft to published page.

<div class="ie-workflow" role="img" aria-label="Policy workflow diagram: draft enters the pipeline, passes through four agent checks, reaches human review, then is published or returned for revision">

  <div class="ie-flow">

    <div class="ie-step ie-step--input">
      <span class="ie-step-icon" aria-hidden="true">📄</span>
      <span class="ie-step-label">Policy Draft</span>
      <span class="ie-step-sub">Markdown file in <code>_policies/</code></span>
    </div>

    <div class="ie-arrow" aria-hidden="true">↓</div>

    <div class="ie-step ie-step--trigger">
      <span class="ie-step-icon" aria-hidden="true">⚡</span>
      <span class="ie-step-label">Pull Request</span>
      <span class="ie-step-sub">GitHub PR opens; agents triggered automatically</span>
    </div>

    <div class="ie-arrow" aria-hidden="true">↓</div>

    <div class="ie-stage" role="group" aria-label="AI agent review stage">
      <div class="ie-stage-label">AI Agent Review Chain</div>
      <div class="ie-stage-agents">

        <div class="ie-mini-agent ie-mini-agent--a">
          <span aria-hidden="true">🔬</span>
          <span>Agent A</span>
          <span class="ie-mini-sub">Science check</span>
        </div>

        <div class="ie-mini-arrow" aria-hidden="true">→</div>

        <div class="ie-mini-agent ie-mini-agent--b">
          <span aria-hidden="true">📊</span>
          <span>Agent B</span>
          <span class="ie-mini-sub">Economic test</span>
        </div>

        <div class="ie-mini-arrow" aria-hidden="true">→</div>

        <div class="ie-mini-agent ie-mini-agent--c">
          <span aria-hidden="true">🌡️</span>
          <span>Agent C</span>
          <span class="ie-mini-sub">Health audit</span>
        </div>

        <div class="ie-mini-arrow" aria-hidden="true">→</div>

        <div class="ie-mini-agent ie-mini-agent--d">
          <span aria-hidden="true">🛡️</span>
          <span>Agent D</span>
          <span class="ie-mini-sub">Consistency</span>
        </div>

      </div>
    </div>

    <div class="ie-arrow" aria-hidden="true">↓</div>

    <div class="ie-gate">
      <div class="ie-gate-inner">
        <span class="ie-gate-icon" aria-hidden="true">🚦</span>
        <div>
          <div class="ie-gate-title">Review Report Generated</div>
          <div class="ie-gate-sub">PASSED checks, WARNINGS, and CRITICAL ISSUES listed</div>
        </div>
      </div>
    </div>

    <div class="ie-branch">
      <div class="ie-branch-path ie-branch-path--fail">
        <div class="ie-branch-label" aria-label="If issues found">⚠️ Issues found</div>
        <div class="ie-step ie-step--return">
          <span class="ie-step-icon" aria-hidden="true">↩️</span>
          <span class="ie-step-label">Returned for revision</span>
          <span class="ie-step-sub">PR blocked; author notified with specific fixes required</span>
        </div>
      </div>

      <div class="ie-branch-divider" aria-hidden="true">or</div>

      <div class="ie-branch-path ie-branch-path--pass">
        <div class="ie-branch-label" aria-label="If all checks pass">✅ All checks pass</div>
        <div class="ie-step ie-step--human">
          <span class="ie-step-icon" aria-hidden="true">👤</span>
          <span class="ie-step-label">Human Review Required</span>
          <span class="ie-step-sub">No AI can merge autonomously — a human maintainer approves</span>
        </div>
      </div>
    </div>

    <div class="ie-arrow" aria-hidden="true">↓</div>

    <div class="ie-step ie-step--backup">
      <span class="ie-step-icon" aria-hidden="true">💾</span>
      <span class="ie-step-label">Backup Created</span>
      <span class="ie-step-sub">Timestamped <code>.bak</code> file saved to <code>archive/</code> before merge</span>
    </div>

    <div class="ie-arrow" aria-hidden="true">↓</div>

    <div class="ie-step ie-step--publish">
      <span class="ie-step-icon" aria-hidden="true">🌐</span>
      <span class="ie-step-label">Published</span>
      <span class="ie-step-sub">Jekyll builds the page; policy is live with full audit trail</span>
    </div>

  </div>

</div>

---

## Trust Mechanisms at Each Stage

<div class="ie-trust-grid">

  <div class="ie-trust-card">
    <h3>Open-Source Scripts</h3>
    <p>Every automated check is implemented in public Python code in the <a href="https://github.com/Open-Climate-Resilience-Policies/OCRP/tree/main/scripts"><code>scripts/</code> directory</a>. You can read it, run it locally, and open an issue if you disagree with a rule.</p>
  </div>

  <div class="ie-trust-card">
    <h3>Binding Language Enforcement</h3>
    <p>The Guardian script rejects vague verbs. "Encourage" → blocked. "Strive to" → blocked. Only "shall", "must", and "required to" pass. This is not optional — it is a hard filter in code.</p>
  </div>

  <div class="ie-trust-card">
    <h3>Citation Link Auditing</h3>
    <p>Every URL in <code>official_sources</code> is checked for HTTP 200. Dead links are flagged immediately. When a link dies, <a href="https://github.com/Open-Climate-Resilience-Policies/OCRP/blob/main/scripts/apply_wayback_replacements.py">the Wayback Machine archiver</a> automatically proposes a replacement.</p>
  </div>

  <div class="ie-trust-card">
    <h3>No Autonomous Publishing</h3>
    <p>AI agents produce reports; they do not merge PRs. A human maintainer must approve every change to the main branch. This is enforced by GitHub branch protection rules, not just policy.</p>
  </div>

  <div class="ie-trust-card">
    <h3>Versioned Backups</h3>
    <p>Before any AI-assisted edit that changes &gt;20% of a policy, a timestamped <code>.bak</code> file is saved to <code>archive/</code>. The commit message must record which agent performed the edit and why.</p>
  </div>

  <div class="ie-trust-card">
    <h3>Public Audit Trail</h3>
    <p>Every change is a Git commit with a documented reason. The full history is publicly visible on GitHub. You can compare any version to any other version and see exactly what changed.</p>
  </div>

</div>

---

## What the AI Does and Does Not Do

<div class="ie-dos-donts">
  <div class="ie-does">
    <h3>✅ AI does</h3>
    <ul>
      <li>Reformat raw policy text into the standard structure</li>
      <li>Flag vague enforcement language for human correction</li>
      <li>Check whether citations are reachable and from authoritative domains</li>
      <li>Detect overlap with existing policies</li>
      <li>Run adversarial "red team" tests to find loopholes</li>
      <li>Generate a structured review report for human decision-making</li>
    </ul>
  </div>
  <div class="ie-does-not">
    <h3>🚫 AI does not</h3>
    <ul>
      <li>Invent citations or fabricate data</li>
      <li>Publish or merge content autonomously</li>
      <li>Weaken enforcement language (doing so is a hard build failure)</li>
      <li>Remove official source citations</li>
      <li>Change numeric thresholds or safety factors without a flagged human review</li>
      <li>Access user data or send information to third-party services</li>
    </ul>
  </div>
</div>

---

## Known Limitations

No automated system is perfect. Known failure modes include:

- A cited source may be misrepresented or summarized inaccurately — the agent checks the URL resolves, not the full content of every paper.
- Numeric thresholds may be transcribed incorrectly from tables or mixed-format documents.
- Legal terminology may not translate correctly across jurisdictions (Common Law vs. Civil Code).
- The adversarial stress test is only as strong as the patterns it has been trained to look for.

**We treat every credible correction as a priority.** Use the button below or [open a GitHub Issue directly](https://github.com/Open-Climate-Resilience-Policies/OCRP/issues/new?labels=content-error&template=content_error.md&title=Content+error%3A+).

---

## Run It Yourself

The full pipeline is reproducible locally:

```bash
# 1. Set up
python3 -m venv venv && source venv/bin/activate
pip install -r scripts/requirements.txt

# 2. Check all policies
python scripts/consistency_guardian.py --all

# 3. Check only policies you've changed
python scripts/consistency_guardian.py --changed

# 4. Auto-archive any dead links
python scripts/consistency_guardian.py --update-redirects --all
```

Source: [`scripts/consistency_guardian.py`](https://github.com/Open-Climate-Resilience-Policies/OCRP/blob/main/scripts/consistency_guardian.py)

---

*Last verified: 2026-05-03 · <a href="{{ '/about/#quality-assurance' | relative_url }}">Back to About →</a>*

<style>
/* ─── Integrity Engine page styles ─────────────────────────────────────── */

/* Component-level custom properties — allows dark-mode overrides without
   hardcoding hex values in every rule */
.ie-workflow,
.ie-dos-donts {
  --ie-error:     #c0392b;
  --ie-error-bg:  #fde8e8;
  --ie-pass:      var(--color-accent);
  --ie-pass-bg:   #e8f8ec;
}

/* Per-agent accent colors (intentional visual differentiation) */
.ie-agent-a-accent { --ie-agent-color: #2980b9; }
.ie-agent-b-accent { --ie-agent-color: #8e44ad; }
.ie-agent-c-accent { --ie-agent-color: #e67e22; }

/* Dark-mode overrides for component variables */
@media (prefers-color-scheme: dark) {
  .ie-workflow,
  .ie-dos-donts {
    --ie-error:    #f08080;
    --ie-error-bg: #3d1515;
    --ie-pass:     var(--color-accent);
    --ie-pass-bg:  #0d2e14;
  }
}

:root[data-theme="dark"] .ie-workflow,
:root[data-theme="dark"] .ie-dos-donts {
  --ie-error:    #f08080;
  --ie-error-bg: #3d1515;
  --ie-pass:     var(--color-accent);
  --ie-pass-bg:  #0d2e14;
}

.ie-lead {
  font-size: 1.2rem;
  color: var(--color-text-light);
  line-height: 1.7;
  margin-bottom: var(--spacing-lg);
}

/* Four-agent cards */
.ie-agents {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-md);
  margin: var(--spacing-lg) 0;
}

.ie-agent {
  display: flex;
  gap: var(--spacing-sm);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: var(--spacing-md);
}

.ie-agent-icon {
  font-size: 2rem;
  line-height: 1;
  flex-shrink: 0;
}

.ie-agent-name {
  margin: 0 0 0.25rem;
  font-size: 1.1rem;
  color: var(--color-primary);
}

.ie-agent-role,
.ie-agent-trigger {
  margin: 0.15rem 0;
  font-size: 0.9rem;
  color: var(--color-text-light);
}

.ie-agent-body p:last-child {
  margin-bottom: 0;
}

/* Workflow diagram */
.ie-workflow {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: var(--spacing-lg);
  margin: var(--spacing-lg) 0;
  overflow-x: auto;
}

.ie-flow {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  min-width: 300px;
}

.ie-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 8px;
  border: 2px solid var(--color-border);
  background: var(--color-bg);
  width: 100%;
  max-width: 480px;
  gap: 0.2rem;
}

.ie-step-icon {
  font-size: 1.5rem;
}

.ie-step-label {
  font-weight: 600;
  font-size: 1rem;
  color: var(--color-text);
}

.ie-step-sub {
  font-size: 0.85rem;
  color: var(--color-text-light);
}

.ie-step--input  { border-color: var(--color-primary-light); }
.ie-step--trigger { border-color: var(--color-primary); }
.ie-step--return { border-color: var(--ie-error); max-width: 280px; }
.ie-step--human  { border-color: var(--color-accent); max-width: 280px; }
.ie-step--backup { border-color: var(--color-primary-light); }
.ie-step--publish { border-color: var(--color-accent); background: color-mix(in srgb, var(--color-accent) 8%, var(--color-bg)); }

.ie-arrow {
  font-size: 1.5rem;
  color: var(--color-text-muted);
  line-height: 1;
  padding: 0.1rem 0;
}

/* Agent stage */
.ie-stage {
  width: 100%;
  max-width: 640px;
  border: 2px solid var(--color-primary);
  border-radius: 8px;
  padding: var(--spacing-sm);
  background: var(--color-bg);
}

.ie-stage-label {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--color-primary);
  text-align: center;
  margin-bottom: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.ie-stage-agents {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.25rem;
}

.ie-mini-agent {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  border: 1px solid var(--color-border);
  background: var(--color-bg-secondary);
  font-size: 0.85rem;
  font-weight: 600;
  gap: 0.1rem;
  min-width: 72px;
}

.ie-mini-sub {
  font-weight: 400;
  font-size: 0.75rem;
  color: var(--color-text-light);
}

.ie-mini-agent--a { border-color: #2980b9; }
.ie-mini-agent--b { border-color: #8e44ad; }
.ie-mini-agent--c { border-color: #e67e22; }
.ie-mini-agent--d { border-color: var(--color-accent); }

.ie-mini-arrow {
  font-size: 1.1rem;
  color: var(--color-text-muted);
}

/* Gate */
.ie-gate {
  width: 100%;
  max-width: 480px;
  border: 2px solid var(--color-warning-border);
  background: var(--color-warning-bg);
  border-radius: 8px;
  padding: var(--spacing-sm) var(--spacing-md);
}

.ie-gate-inner {
  display: flex;
  align-items: flex-start;
  gap: var(--spacing-sm);
}

.ie-gate-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.ie-gate-title {
  font-weight: 600;
  color: var(--color-text);
}

.ie-gate-sub {
  font-size: 0.85rem;
  color: var(--color-text-light);
  margin-top: 0.15rem;
}

/* Branch */
.ie-branch {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: var(--spacing-md);
  width: 100%;
  max-width: 640px;
  flex-wrap: wrap;
}

.ie-branch-path {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  min-width: 220px;
}

.ie-branch-label {
  font-size: 0.9rem;
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  text-align: center;
}

.ie-branch-path--fail .ie-branch-label  { background: var(--ie-error-bg); color: var(--ie-error); }
.ie-branch-path--pass .ie-branch-label  { background: var(--ie-pass-bg); color: var(--ie-pass); }

.ie-branch-divider {
  font-size: 0.9rem;
  color: var(--color-text-muted);
  font-style: italic;
  align-self: center;
  padding: 0 0.5rem;
}

/* Trust grid */
.ie-trust-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: var(--spacing-md);
  margin: var(--spacing-lg) 0;
}

.ie-trust-card {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-left: 4px solid var(--color-accent);
  border-radius: 4px;
  padding: var(--spacing-md);
}

.ie-trust-card h3 {
  margin-top: 0;
  font-size: 1rem;
  color: var(--color-primary);
}

.ie-trust-card p {
  margin: 0;
  font-size: 0.95rem;
}

/* Dos and don'ts */
.ie-dos-donts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  margin: var(--spacing-lg) 0;
}

.ie-does,
.ie-does-not {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: var(--spacing-md);
}

.ie-does h3 {
  margin-top: 0;
  color: var(--color-accent);
}

.ie-does-not h3 {
  margin-top: 0;
  color: var(--ie-error);
}

.ie-does ul,
.ie-does-not ul {
  padding-left: 1.25rem;
  margin: 0;
}

.ie-does li,
.ie-does-not li {
  margin-bottom: 0.4rem;
  font-size: 0.95rem;
}

/* Mobile responsiveness */
@media (max-width: 600px) {
  .ie-dos-donts {
    grid-template-columns: 1fr;
  }

  .ie-stage-agents {
    flex-direction: column;
    align-items: stretch;
  }

  .ie-mini-arrow {
    transform: rotate(90deg);
    align-self: center;
  }
}
</style>
