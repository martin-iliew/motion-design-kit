---
name: web-build
description: >
  Expert landing-page design implementation skill for building, rewriting, modernizing, or
  explaining homepage and conversion-page structure in existing HTML, React, Vue, or Svelte
  files. Trigger when the user wants a hero, feature grid, pricing section, testimonial block,
  proof rail, FAQ, CTA band, or full landing page to feel more modern, clearer, more premium, or
  more enterprise-ready; asks for better layout, stronger hierarchy, better proof placement, or
  improved conversion flow; pastes a landing page and asks how to make it feel more like Stripe,
  Linear, Notion, Vercel, or other large product-company sites; or asks which landing-page
  patterns fit a specific section and wants them applied in code. Do not trigger for report-only
  audits with no edits (use web-audit); unattended audit-plus-fix passes across whole files or
  pages (use web-upgrade); or library trend research and catalog expansion (use web-discover).
---

# web-build

Canonical landing-page design generation skill. `.claude` is the source of truth for runtime selection, modes, guardrails, and output contracts.

## 0. Parse the request

1. If the request begins with `mode: fast`, `mode: balanced`, or `mode: premium`, strip that prefix and store the mode.
2. If no mode is supplied, default to `balanced`.
3. Treat the remaining text as the build request.
4. If the task is audit-only, redirect to `/web-audit`.
5. If the task is a full unattended audit-and-modernize pass, redirect to `/web-upgrade`.
6. If the task is pure trend research or catalog expansion, redirect to `/web-discover`.

## 1. Load shared policy first

Before choosing patterns or writing code, load:

- `.claude/skills/shared/runtime-selection.md`
- `.claude/skills/shared/execution-modes.md`
- `.claude/skills/shared/guardrails.md`
- `.claude/skills/shared/output-contracts.md`

Load `.claude/skills/shared/audit-rules.md` Parts A, C, D, and E when you need the section decision table or the default landing-page rhythm.

## 2. Route to the cheapest correct workflow

### Full-page or multi-section generation

1. Use the page branch from `runtime-selection.md`.
2. Scan for weak or missing surfaces.
3. Apply `execution-modes.md` before any escalation.
4. Convert the winners into an explicit Section Plan.
5. Load only the winning pattern folder `spec.yaml`, `index.md`, and `snippet.html` for each selected winner.

### Single section or targeted refinement

1. Read `.claude/design-library/scores.yaml`.
2. Choose the top safe match for the requested surface.
3. Load only the winning folder `spec.yaml`, `index.md`, and `snippet.html`.
4. Do not open `trends-overview.md` unless the shared mode rules allow escalation.

## 3. Implementation rules

Use the selected pattern folders as the primary implementation source.

Load additional references only when needed:

- `references/layout-patterns.md` for grid and rhythm decisions
- `references/section-recipes.md` for section ordering and section internals
- `references/copy-signals.md` for headline, CTA, and proof phrasing
- `references/live-sources.md` only when you need current external validation for a new trend claim

Do not read `catalog.yaml` during normal generation.

For `.html` targets, duplicate the file to `*-redesign.html` before editing unless the user explicitly asked for in-place changes. For component and app files, edit in place unless the user asked for a duplicate output.

## 4. Mode-aware selection boundaries

- `fast`: compiled selector layer only for page work; no `trends-overview.md`; no decorative extras
- `balanced`: compiled selector layer first; `trends-overview.md` only if needed; one extra polish move per page is allowed
- `premium`: stronger composition is allowed, but the page must still feel like a serious conversion surface

Never do live trend research during `web-build`. Trend freshness comes from `/web-refresh`.

## 5. Hard quality gates

Everything in `guardrails.md` is mandatory in every mode. In particular:

- the hero must clarify product, audience, and outcome
- the primary CTA must stay visible and specific
- proof must not be buried
- pricing, trust, or objections cannot be skipped on pages that need them
- do not introduce brutalism, anti-grid layouts, or novelty-first styling unless the user explicitly asks for it

## 6. Final response

Use the `web-build` contract from `.claude/skills/shared/output-contracts.md`.

Do not print query-cost metrics unless the user, a maintainer workflow, or a benchmark task explicitly asks for them.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
