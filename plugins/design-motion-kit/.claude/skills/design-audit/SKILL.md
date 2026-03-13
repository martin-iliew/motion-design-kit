---
name: design-audit
description: >
  Report-first landing-page design audit skill for hierarchy, proof, CTA flow, section quality,
  and design-system usage. Trigger when the user wants findings without direct edits. Do not
  trigger for unattended fixes (use design-upgrade) or targeted redesign work (use design-build).
---

# design-audit

## Load

- `.claude/shared/design-audit-rules.md`
- `.claude/shared/output-contracts.md`

Load `brief/design-decision-pack.yaml` and `brief/token-aliases.json` when they exist so you can detect drift from the intended system.

## Audit focus

- message clarity
- hierarchy and scanability
- proof density and placement
- CTA continuity
- design-system adoption vs raw values

## Rules

- do not edit files in `design-audit`
- if the user wants automatic fixes, redirect to `/design-upgrade`
- if the user wants targeted redesign work, redirect to `/design-build`

## Final response

Use the `design-audit` contract from `.claude/shared/output-contracts.md`.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
