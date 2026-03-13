---
name: motion-upgrade
description: >
  Canonical unattended motion audit-and-modernize skill for existing frontend files. Trigger when
  the user wants motion quality fixed and enriched in one pass. Do not trigger for report-only
  audits (motion-audit), targeted new motion work (motion-build), or library maintenance tasks
  (motion-discover or motion-refresh).
---

# motion-upgrade

Downstream motion upgrade workflow for the merged `design-motion-kit`.

## 0. Parse the request

1. Strip a leading `mode:` prefix when present.
2. Default to `balanced`.
3. Redirect report-only review work to `/motion-audit`.
4. Redirect targeted implementation work to `/motion-build`.

## 1. Load shared policy first

Load:

- `.claude/shared/execution-modes.md`
- `.claude/shared/bundle-loading.md`
- `.claude/shared/handoff-contracts.md`
- `.claude/shared/motion-runtime-selection.md`
- `.claude/shared/motion-guardrails.md`
- `.claude/shared/validation.md`
- `.claude/shared/output-contracts.md`
- `.claude/shared/motion-audit-rules.md`

## 2. Consume design outputs first

When present, read:

- `brief/design-decision-pack.yaml`
- `brief/motion-hints.yaml`
- `brief/token-aliases.json`

## 3. Upgrade workflow

1. Audit the files with `.claude/shared/motion-audit-rules.md`.
2. Fix ownership, reduced-motion, cleanup, and performance problems first.
3. Use `.claude/shared/motion-runtime-selection.md` to choose non-conflicting winners.
4. Load only the winning pattern folders.
5. Skip any bucket blocked by the design handoff.

## 4. Hard rules

- `motion-upgrade` is unattended once it begins
- design hints take precedence over decorative motion ideas
- never add motion to elements the design layer did not create

## 5. Final response

Use the `motion-upgrade` contract from `.claude/shared/output-contracts.md`.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
