---
name: motion-build
description: >
  Expert web motion implementation skill for building, writing, fixing, translating, or
  explaining animation and motion code for a specific element, component, or page. Trigger when
  the user wants to animate something or wants a UI to feel more alive, tactile, or fluid. Do
  not trigger for audit-only requests (motion-audit), unattended audit-plus-fix passes
  (motion-upgrade), or catalog discovery work (motion-discover).
---

# motion-build

Canonical downstream motion skill for the merged `design-motion-kit`.

## 0. Parse the request

1. Strip a leading `mode:` prefix when present.
2. Default to `balanced`.
3. Redirect audit-only work to `/motion-audit`.
4. Redirect unattended audit-and-fix work to `/motion-upgrade`.
5. Redirect catalog research to `/motion-discover`.

## 1. Load shared policy first

Load:

- `.claude/shared/execution-modes.md`
- `.claude/shared/bundle-loading.md`
- `.claude/shared/handoff-contracts.md`
- `.claude/shared/motion-runtime-selection.md`
- `.claude/shared/motion-guardrails.md`
- `.claude/shared/validation.md`
- `.claude/shared/output-contracts.md`

When you need the rubric, load:

- `.claude/shared/motion-audit-rules.md`

## 2. Consume design outputs before selecting motion

If the repo has a `brief/` directory, read these first:

- `brief/design-decision-pack.yaml`
- `brief/motion-hints.yaml`
- `brief/token-aliases.json`

Use the motion hints to reject motion families that design has not allowed.

## 3. Route to the cheapest correct workflow

### Page or multi-section work

1. Use `.claude/shared/motion-runtime-selection.md`.
2. Detect only buckets that actually exist.
3. Choose winners that survive the design-hint constraints.
4. Load only the winning pattern folder `spec.yaml` plus snippet.
5. Convert the survivors into an explicit Animation Plan before editing.

### Single component or isolated element work

1. Read `.claude/motion-library/scores.yaml`.
2. Choose the top safe match for the requested element.
3. Load only the winning folder `spec.yaml` plus snippet.

## 4. Hard rules

- motion must stay downstream from design when the handoff files exist
- never animate elements missing from the design decision pack
- never violate the allowed families or intensity from `motion-hints.yaml`
- use token-derived timing and easing when the project exposes them

## 5. Final response

Use the `motion-build` contract from `.claude/shared/output-contracts.md`.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
