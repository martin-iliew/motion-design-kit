---
name: web-audit
description: >
  Use this skill whenever the task is to analyze or review existing landing-page markup, styles,
  and section structure and produce a written report with no code changes made. Trigger on:
  "audit my homepage", "review this landing page", "tell me what is weak before I change it",
  "does this page feel modern enough", or any request to inspect hierarchy, proof, CTA clarity,
  pricing readability, trust, or conversion friction without editing files. Do not trigger when
  the user wants fixes applied automatically after the audit (use web-upgrade), or when the user
  wants targeted section design work applied directly (use web-build).
---

# web-audit

Canonical report-first audit skill for analyzing landing-page code across five quality dimensions.
This surface does not edit files.

## 0. Load shared policy first

Before auditing, load:

- `.claude/skills/shared/audit-rules.md`
- `.claude/skills/shared/output-contracts.md`

Use `.claude/skills/shared/audit-rules.md` Parts B, C, D, and E for the rubric and hard rules.

## 1. Read and parse

Read the target file. If it exceeds 400 lines, process it in sections: structure first, then CSS, then JS or component logic only if it affects the landing-page surface.

## 2. Analyze the five dimensions

Evaluate the page against the shared audit rubric:

**MESSAGE** — does the first screen explain product, audience, and outcome?

**HIERARCHY** — can the page be scanned quickly, or does everything look equally loud?

**PROOF** — are logos, metrics, testimonials, trust, and evidence present where needed?

**CONVERSION** — is the CTA path obvious, repeated, and low-friction?

**POLISH** — does the page feel current and enterprise-safe without chasing trends?

## 3. Output the audit report

Severity definitions:

- **CRITICAL**: confusing offer, absent CTA path, unreadable pricing or trust gap
- **WARNING**: weak proof density, generic sections, poor grouping, outdated visual system
- **INFO**: meaningful polish opportunity

Use the `web-audit` contract from `.claude/skills/shared/output-contracts.md`.

## 4. Proposed changes

For every CRITICAL and WARNING item, show a concrete patch direction:

```text
### Fix #1 - [Issue Name]

Before:
[exact code or structure summary]

After:
[clear patch-ready guidance]

Why:
[one-sentence explanation]
```

## 5. Handoff rules

Stop after the report.

- Do not edit the target file in `web-audit`.
- If the user wants automatic fixes applied, redirect to `/web-upgrade`.
- If the user wants targeted design work applied, redirect to `/web-build`.

## 6. Self-clarity check

Before finalizing:

- every fix must be self-contained
- every "after" suggestion must be actionable
- the summary counts must match the actual findings
- the reasoning must make sense without the rubric file open

Do not print query-cost metrics unless the user, a maintainer workflow, or a benchmark task explicitly asks for them.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
