---
name: motion-audit
description: >
  Use this skill whenever the task involves auditing or reviewing existing animation code
  and producing a report — without automatically applying fixes. Trigger on: "audit my
  animations", "check my GSAP code", "review this animation", "animation health check",
  "/motion-audit", or any request to analyze web animation or micro-interaction code for
  quality, performance, conflicts, and consistency. Also trigger for: diagnosing animation
  jank or flickering; checking if animations will cause layout thrashing or paint issues;
  verifying prefers-reduced-motion / reduced-motion handling; checking if CSS transitions
  and GSAP are conflicting; "tell me what's wrong before I fix it". DO NOT trigger when
  the user wants fixes applied automatically (use motion-enhance) or wants new animations
  added (use motion-dev).
---

# motion-audit

Professional animation audit skill for analyzing web animation code across five quality dimensions.

---

## Workflow: Audit

When `/motion-audit [file]` triggers (or the user asks to review/check animation code), follow this workflow:

### Pre-flight — Start timer

Run via Bash and save the output as `TASK_START`:
```
TASK_START=$(python .claude/scripts/query_cost.py --stamp)
```

### Step 1: Read and Parse

Read the target file. If it exceeds 400 lines, process it in sections: structure/HTML first, then CSS, then JS/GSAP.

Load `.claude/skills/shared/audit-rules.md` Parts B, C, E — you need them for the five audit dimensions, hard rules, and token reference.

### Step 2: Analyze Five Dimensions

Evaluate every animation and transition against:

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

### Step 3: Output Severity Table

```
## Audit Report: [filename]

| # | Issue | Severity | Location | Fix |
|---|-------|----------|----------|-----|
| 1 | ...   | CRITICAL | line 42  | ... |
| 2 | ...   | WARNING  | line 88  | ... |
| 3 | ...   | INFO     | line 103 | ... |

**Summary:** N critical, N warnings, N info
```

### Metrics

Run via Bash:
```
python .claude/scripts/query_cost.py --since "$TASK_START"
```
Output the result line directly. If unavailable: _Metrics unavailable — run `python .claude/scripts/query_cost.py --since <start-timestamp>` manually._

Severity definitions:

- **CRITICAL**: Will cause visible jank, layout shift, or broken animation state
- **WARNING**: Suboptimal — hurts performance or creates inconsistency
- **INFO**: Stylistic improvement opportunity

### Step 4: Proposed Changes

For every CRITICAL and WARNING item, show a concrete patch:

```
### Fix #1 — [Issue Name]

**Before:**
[exact code from file]

**After:**
[corrected code]

**Why:** [1-sentence explanation]
```

### Step 5: Feedback Loop

After the full report, ask:

> "Want me to apply all CRITICAL fixes directly to `[filename]`? I'll make the changes and re-run the audit to confirm they're resolved."

If yes:

1. Apply each CRITICAL fix to the file
2. Re-run the audit (Steps 1-3 only)
3. Confirm: "All CRITICAL issues resolved. Remaining: N warnings, N info."

If no: end the audit and let the user decide what to apply manually.

### Step 5.5: Self-Clarity Check

Before finalizing the report, verify mentally (no tool calls needed):

- [ ] Every "Fix" cell in the table is self-contained — no "see above" references
- [ ] Every "After" code patch is copy-paste-ready — no `[placeholder]` text
- [ ] CRITICAL count in the summary line matches the actual CRITICAL rows counted
- [ ] Each "Why" sentence in the patches makes sense without reading the audit rules file

10-second scan. If any check fails, fix the report before outputting.

---

## General Rules

- Always respect `prefers-reduced-motion`. Any generated GSAP code must include a matchMedia guard.
- Never animate layout-triggering properties (`width`, `height`, `top`, `left`, `margin`). Only animate `transform` and `opacity` for GPU-composited performance.
- When generating code, use `gsap.context()` for React/component cleanup.
- Easing vocabulary: use `power2.out` for entrances, `power2.inOut` for transitions, `elastic.out(1, 0.3)` for playful micro-interactions, `CustomEase` for branded motion.

---

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
