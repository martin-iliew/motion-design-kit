---
name: web-upgrade
description: >
  Use this skill whenever the task combines auditing existing landing-page design code and
  automatically applying all fixes and additions in a single unattended pass. Trigger on:
  "upgrade my landing page", "modernize this homepage", "audit and fix the page", "make this
  feel more enterprise", "apply the improvements automatically", or any request that merges audit
  with auto-applied fixes and missing-section work across one or more files. Do not trigger for
  report-only reviews with no edits (use web-audit); a single targeted section redesign with no
  audit step (use web-build); or pattern-library research and rescoring tasks (use web-discover
  or web-refresh).
---

# web-upgrade

Canonical unattended audit-and-enrich skill. `.claude` is the source of truth for the upgrade workflow.

## 0. Parse the request

1. If the request begins with `mode: fast`, `mode: balanced`, or `mode: premium`, strip that prefix and store the mode.
2. If no mode is supplied, default to `balanced`.
3. Treat the remaining arguments as the target file list.
4. If there is one target, use the single-file path.
5. If there are multiple distinct targets, process them together after loading the shared inputs once.

For `.original.html` inputs, copy to `.enhanced.html` and work on the copy. Otherwise edit in place.

## 1. Load shared policy first

Before auditing or enriching, load:

- `.claude/skills/shared/runtime-selection.md`
- `.claude/skills/shared/execution-modes.md`
- `.claude/skills/shared/guardrails.md`
- `.claude/skills/shared/output-contracts.md`

Load `.claude/skills/shared/audit-rules.md` Parts A, B, C, D, and E for the audit pass.

## 2. Audit first

Read the target file and classify issues through the 5-dimension audit framework:

- `CRITICAL`
- `WARNING`
- `INFO`

Scan for missing sections, weak hierarchy, missing proof, weak CTA flow, and outdated styling.

## 3. Choose enrichments cheaply

After the audit:

1. Apply the shared runtime-selection algorithm.
2. Apply `execution-modes.md` before any escalation.
3. Carry forward only patterns that fix real weaknesses and do not fight the existing stack.
4. Load only the winning folder `spec.yaml`, `index.md`, and `snippet.html` for each selected winner.

Use `../web-build/references/layout-patterns.md`, `section-recipes.md`, and `copy-signals.md` only as fallback implementation glue.

Never do live trend research during `web-upgrade`.

## 4. Fix, then enrich

### Phase A: Fix issues

- Fix all `CRITICAL` and `WARNING` issues automatically.
- Leave `INFO` items only when they are low-value, subjective, or risky to auto-apply.
- Apply the shared guardrails in every mode.

### Phase B: Add missing design structure

- Prioritize the compiled runtime winners.
- Skip any section that already exists in a strong form and mark it `ALREADY_STRONG`.
- `fast`: enrich only the highest-value gaps
- `balanced`: enrich all relevant non-conflicting gaps
- `premium`: allow stronger restructuring, but keep the page commercially serious

## 5. Verification

After editing:

1. Re-read the upgraded file.
2. Verify syntax and component structure.
3. Confirm hierarchy, proof, and CTA flow improved.
4. Confirm mobile readability for pricing, testimonials, and FAQ sections.

## 6. Final response

Use the `web-upgrade` contract from `.claude/skills/shared/output-contracts.md`.

Do not ask whether to apply more changes. `web-upgrade` is an unattended pass.
Do not print query-cost metrics unless the user, a maintainer workflow, or a benchmark task explicitly asks for them.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
