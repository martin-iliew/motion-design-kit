---
name: motion-build
description: >
  Expert web animation implementation skill for building, writing, fixing, translating, or
  explaining animation and motion code for a specific element, component, or page. Trigger when
  the user wants to animate something (hero, nav, drawer, modal, card list, button, tooltip,
  section, etc.); asks how to make UI feel "more alive", "bouncy", "fluid", or "tactile"; needs
  scroll reveals, page transitions, micro-interactions, hover effects, stagger effects, or a
  non-trivial loading animation (e.g., a button loading state, animated progress indicator);
  pastes animation code for improvement, debugging, or library translation; asks about GPU-safe
  properties, animation performance, or GSAP API concepts (e.g., "what is the difference between
  fromTo and from?"); asks which motion patterns fit a specific element and wants them applied in
  code. Also trigger for any intent to animate a named element or component regardless of library
  or framework. DO NOT trigger for: audit-only requests with no code changes (use motion-audit);
  site-wide "fix everything and add what's missing" passes where the scope covers the whole app,
  all files, or every section with both fixing and adding (use motion-upgrade); pure
  trend-discovery or catalog-expansion requests (use motion-discover); trivial one-liner CSS
  spinners explicitly described as needing only a single line; or layout-shift / CLS debugging
  where animation is only a possible cause and no animation task is stated.
---

# motion-build

Canonical motion generation skill. `.claude` is the source of truth for runtime selection, modes, guardrails, and output contracts.

## 0. Parse the request

1. If the request begins with `mode: fast`, `mode: balanced`, or `mode: premium`, strip that prefix and store the mode.
2. If no mode is supplied, default to `balanced`.
3. Treat the remaining text as the actual build request.
4. If the task is audit-only, redirect to `/motion-audit`.
5. If the task is upgrade-and-fix-all, redirect to `/motion-upgrade`.
6. If the task is pure trend discovery, catalog expansion, or research with no implementation target, redirect to `/motion-discover`.

## 1. Load shared policy first

Before choosing patterns or writing code, load:

- `.claude/skills/shared/runtime-selection.md`
- `.claude/skills/shared/execution-modes.md`
- `.claude/skills/shared/guardrails.md`
- `.claude/skills/shared/output-contracts.md`

Load `.claude/skills/shared/audit-rules.md` Parts A, C, D, and E only when you need the element decision table, hard rules, easing table, or token quick reference.

## 2. Route to the cheapest correct workflow

### Full-page or multi-section generation

1. Use the page branch from `runtime-selection.md`.
2. Run the shared bucket scan, site classification, and signal detection.
3. Apply `execution-modes.md` before any escalation.
4. Convert surviving winners into an explicit Animation Plan.
5. Load only the winning pattern folder `spec.yaml` plus snippet for each selected winner.

### Single component, isolated element, or pattern inspiration

1. Read `.claude/motion-library/scores.yaml`.
2. Choose the top safe match for the requested element or component.
3. Load only the winning pattern folder `spec.yaml` plus snippet.
4. Do not open `trends-overview.md` unless the shared mode rules permit escalation.

### Translation requests

1. Identify the current stack and target stack with `guardrails.md`.
2. Load `.claude/motion-spec.md`.
3. Load `references/motion-spec-translation-guide.md`.
4. Output only the translated target-stack code unless the user explicitly asks for the spec.

## 3. Implementation rules

Use the selected pattern folders as the primary implementation source.

Load additional references only when needed:

- `references/stack-patterns.md` for stack-native scaffolding
- `references/gsap-patterns.md` for composition glue when the winning snippet is too narrow
- `references/css-patterns.md` for CSS-only implementation paths
- `references/live-sources.md` only when plugin or API clarification is still needed

Do not read `catalog.yaml` during normal generation.

For `.html` targets, duplicate the file to `*-animated.html` before editing unless the user explicitly asked for in-place changes. For component and app files, edit in place unless the user asked for a duplicate output.

## 4. Mode-aware selection boundaries

- `fast`: compiled selector layer only for page work; no page-level `scores.yaml`, no `trends-overview.md`, no decorative extras
- `balanced`: compiled selector layer first; page-level `scores.yaml` only if needed; one cheap optional interaction enhancement is allowed
- `premium`: explicit only; shared escalation rules may allow `trends-overview.md` and one GSAP doc fetch when necessary

Never do live trend research during `motion-build`. Trend freshness comes from `/motion-refresh`.

## 5. Hard quality gates

Everything in `guardrails.md` is mandatory in every mode. In particular:

- reduced-motion handling is required
- only GPU-safe properties may be animated
- cleanup must match the detected stack
- no CSS transition conflicts with GSAP-owned properties
- hidden elements use `fromTo` or `autoAlpha` correctly
- page-level work must pass the shared self-verification checklist before you stop
- **parallax effects must be desktop-only**: always wrap parallax ScrollTriggers in a `gsap.matchMedia()` condition that includes both `(prefers-reduced-motion: no-preference)` AND `(min-width: 1024px)` — parallax on mobile causes scroll jank and UX issues

## 6. Final response

Use the `motion-build` contract from `.claude/skills/shared/output-contracts.md`.

Do not print query-cost metrics unless the user, a maintainer workflow, or a benchmark task explicitly asks for them.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
