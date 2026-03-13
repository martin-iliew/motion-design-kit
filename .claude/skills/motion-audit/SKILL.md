---
name: motion-audit
description: >
  Use this skill whenever the task is to analyze or review existing animation code and
  produce a written report — with no code changes made. Trigger on: "audit my animations",
  "check my GSAP code", "animation health check", or any request to inspect web animation
  or micro-interaction code for quality, performance, conflicts, and consistency. Also
  trigger for: diagnosing animation jank or flickering; detecting layout-thrashing or
  paint-triggering properties; verifying prefers-reduced-motion / accessibility compliance;
  checking whether CSS transitions and GSAP conflict on the same elements; any "tell me
  what's wrong before I fix it" framing; animation-related accessibility reviews described
  as report-only. DO NOT trigger when: the user wants fixes applied automatically after
  the audit (use motion-upgrade); the user wants new animations added (use motion-build);
  the request ends with "then fix X" or "then apply the changes" even if it starts as an
  audit — that is motion-upgrade territory; or the request mixes animation audit with
  non-animation refactoring or logic changes.
---

# motion-audit

Canonical report-first audit skill for analyzing web animation code across five quality dimensions.
This surface does not edit files.

## 0. Load shared policy first

Before auditing, load:

- `.claude/skills/shared/audit-rules.md`
- `.claude/skills/shared/output-contracts.md`

Use `.claude/skills/shared/audit-rules.md` Parts B, C, and E for the audit rubric, hard rules, and token reference.

## 1. Read and parse

Read the target file. If it exceeds 400 lines, process it in sections: structure/HTML first, then CSS, then JS/GSAP.

## 2. Analyze the five dimensions

Evaluate every animation and transition against the shared audit rubric:

**DEPENDENCIES** — Will the page actually load its animation libraries?

- Look for: GSAP version < 3.13 using formerly-premium plugins (SplitText, MorphSVG, DrawSVG, ScrambleText, CustomEase, Physics2D) — all plugins are FREE since GSAP 3.13 (May 2025, Webflow acquisition). Do NOT flag these as 404 errors on versions >= 3.13
- Look for: plugin `<script>` tags placed AFTER code that calls `gsap.registerPlugin()` — plugin must load before registration
- Look for: floating version tags (`gsap@3`, `gsap@latest`) instead of pinned versions (e.g. `gsap@3.14`) — risks silent breaking changes
- Look for: `new SplitText()` or any DOM-measuring call before `document.fonts.ready` — web fonts measured against fallback font cause misaligned split/mask regions
- A CDN 404 that kills JS execution makes the rest of the audit moot — always check this first

**MODERNITY** — Are these 2023-style generic fades, or 2026-quality fluid interactions?

- Look for: `transition: all`, uniform 0.3s durations everywhere, `opacity` only animations, no easing variation

**PERFORMANCE** — Will this cause jank, layout shifts, or battery drain?

- Look for: animating `width`, `height`, `top`, `left`, `margin`, `padding` (layout-triggering)
- Look for: `setTimeout`/`setInterval` used for animation instead of GSAP or CSS
- Look for: missing `will-change` on heavy animated elements
- Look for: `transform3d` forced via `-webkit-` prefixes (obsolete)

**CONFLICT** — Do animations fight each other?

- Look for: `gsap.from()` + `gsap.to()` on the same element/property
- Look for: multiple timelines animating the same CSS property simultaneously
- Look for: CSS transitions active on properties that GSAP is also controlling
- Look for: nested ScrollTriggers that share the same scrub target

**CONSISTENCY** — Does the motion feel unified?

- Look for: mixed easing (e.g., `ease-in-out` in CSS, `power2.out` in GSAP on same site)
- Look for: inconsistent durations (0.2s, 0.3s, 0.8s, 1.2s all used without a system)
- Look for: stagger values that don't follow a pattern

## 3. Output the audit report

Severity definitions:

- **CRITICAL**: Will cause visible jank, layout shift, or broken animation state
- **WARNING**: Suboptimal — hurts performance or creates inconsistency
- **INFO**: Stylistic improvement opportunity

Use the `motion-audit` contract from `.claude/skills/shared/output-contracts.md`.

## 4. Proposed changes

For every CRITICAL and WARNING item, show a concrete patch:

```
### Fix #1 — [Issue Name]

**Before:**
[exact code from file]

**After:**
[corrected code]

**Why:** [1-sentence explanation]
```

## 5. Handoff rules

Stop after the report.

- Do not edit the target file in `motion-audit`.
- If the user wants automatic fixes applied, redirect to `/motion-upgrade`.
- If the user wants targeted new motion, translation, or selective implementation work, redirect to `/motion-build`.

## 6. Self-clarity check

Before finalizing the report, verify mentally (no tool calls needed):

- [ ] Every "Fix" cell in the table is self-contained — no "see above" references
- [ ] Every "After" code patch is copy-paste-ready — no `[placeholder]` text
- [ ] CRITICAL count in the summary line matches the actual CRITICAL rows counted
- [ ] Each "Why" sentence in the patches makes sense without reading the audit rules file

10-second scan. If any check fails, fix the report before outputting.

---

## General rules

- Always respect `prefers-reduced-motion`. Any generated GSAP code must include a matchMedia guard.
- Never animate layout-triggering properties (`width`, `height`, `top`, `left`, `margin`). Only animate `transform` and `opacity` for GPU-composited performance.
- When generating code, use `gsap.context()` for React/component cleanup.
- Easing vocabulary: use `power2.out` for entrances, `power2.inOut` for transitions, `elastic.out(1, 0.3)` for playful micro-interactions, `CustomEase` for branded motion.
- Do not mutate files from `motion-audit`.

Do not print query-cost metrics unless the user, a maintainer workflow, or a benchmark task explicitly asks for them.

---

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
