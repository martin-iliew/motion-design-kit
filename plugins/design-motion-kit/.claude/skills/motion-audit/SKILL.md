---
name: motion-audit
description: >
  Report-first motion audit skill for frontend files. Trigger when the user wants findings about
  animation quality, performance, conflicts, reduced-motion, or cleanup behavior without direct
  edits. Do not trigger for unattended fixes (motion-upgrade) or targeted new implementation
  work (motion-build).
---

# motion-audit

## Load

- `.claude/shared/motion-audit-rules.md`
- `.claude/shared/output-contracts.md`

Load `brief/motion-hints.yaml` when it exists so you can report violations of the design handoff.

## Audit focus

- reduced-motion coverage
- stack-appropriate cleanup
- property safety and ownership conflicts
- timing consistency
- compliance with `motion-hints.yaml` when present

## Rules

- do not edit files in `motion-audit`
- if the user later wants unattended fixes, redirect to `/motion-upgrade`
- if the user wants targeted implementation work, redirect to `/motion-build`

## Final response

Use the `motion-audit` contract from `.claude/shared/output-contracts.md`.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
