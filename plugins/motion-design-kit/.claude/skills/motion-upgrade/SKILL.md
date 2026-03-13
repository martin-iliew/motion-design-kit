---
name: motion-upgrade
description: >
  Use this skill whenever the task combines auditing existing animation code AND automatically
  applying all fixes and additions in a single unattended pass — no manual review step, no
  partial treatment. Trigger on: "upgrade my animations", "animation upgrade", "/motion-upgrade",
  or any request that merges audit with auto-applied fixes and/or new animations across a file or
  site. Key signals: "check for problems then fix them all", "audit and add what's missing",
  "fix all issues and add scroll reveals", "full animation pass", "process all my HTML files",
  "make it animated but check existing CSS first", "apply the improvements from the audit
  report", or wanting multiple files processed for animation upgrades in parallel. Also trigger
  when the user describes a comprehensive overhaul covering conflicts, missing animations, and
  performance in one request. DO NOT trigger for: audit-only requests that produce a report with
  no changes applied (use motion-audit); "tell me what's missing before I add it" requests with
  no changes applied (use motion-audit); adding a single targeted animation with no audit step
  (use motion-build); requests to fix only one category of issues such as performance-only or
  critical-only while leaving other issues for manual review — those are partial fixes, not full
  upgrades.
---

# motion-upgrade

Canonical unattended audit-and-enrich skill. `.claude` is the source of truth for the upgrade workflow.

## 0. Parse the request

1. If the request begins with `mode: fast`, `mode: balanced`, or `mode: premium`, strip that prefix and store the mode.
2. If no mode is supplied, default to `balanced`.
3. Treat the remaining arguments as the target file list.
4. If there is one target, use the single-file path.
5. If there are multiple distinct targets, process them in parallel after loading the shared inputs once.

For `.original.html` inputs, copy to `.enhanced.html` and work on the copy. Otherwise edit in place.

## 1. Load shared policy first

Before auditing or enriching, load:

- `.claude/skills/shared/runtime-selection.md`
- `.claude/skills/shared/execution-modes.md`
- `.claude/skills/shared/guardrails.md`
- `.claude/skills/shared/output-contracts.md`

Load `.claude/skills/shared/audit-rules.md` Parts B, C, and E for the audit pass. Load Part A only when enriching buckets after the fixes land.

## 2. Audit first

Read the target file and classify issues through the 5-dimension audit framework:

- `CRITICAL`
- `WARNING`
- `INFO`

Bucket-scan only what actually exists. Reuse the shared runtime-selection detection pass after the inline audit step.

## 3. Choose enrichments cheaply

After the audit:

1. Apply the shared runtime-selection algorithm.
2. Apply `execution-modes.md` before any escalation.
3. Carry forward only buckets that exist and do not conflict with existing GSAP ownership.
4. Load only the winning pattern folder `spec.yaml` plus snippet for each selected winner.

Use `../motion-build/references/gsap-patterns.md` only as fallback composition glue and `../motion-build/references/live-sources.md` only when plugin or API clarification is still needed.

Never do live trend research during `motion-upgrade`.

## 4. Fix, then enrich

### Phase A: Fix issues

- Fix all `CRITICAL` and `WARNING` issues automatically.
- Leave `INFO` items only when they are low-value, subjective, or risky to auto-apply.
- Apply the shared guardrails in every mode.

### Phase B: Add missing motion

- Prioritize the compiled runtime winners.
- Skip any bucket that is already animated in a conflicting way and mark it `ALREADY_ANIMATED`.
- `fast`: enrich only top-value buckets
- `balanced`: enrich all relevant non-conflicting buckets plus at most one cheap interaction enhancement
- `premium`: richer composition is allowed, but still respect the same guardrails

## 5. Verification

After editing:

1. Re-read the upgraded file.
2. Verify syntax and guardrail compliance.
3. Confirm that no CSS transition conflicts remain.
4. Confirm cleanup, reduced-motion handling, and stack ownership are correct.
5. Confirm page-level hero work passes the shared hero and section checks when applicable.

## 6. Final response

Use the `motion-upgrade` contract from `.claude/skills/shared/output-contracts.md`.

Do not ask whether to apply more changes. `motion-upgrade` is an unattended pass.
Do not print query-cost metrics unless the user, a maintainer workflow, or a benchmark task explicitly asks for them.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
