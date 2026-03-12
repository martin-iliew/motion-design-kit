---
name: motion-enhance
description: >
  Use this skill whenever the task involves both auditing existing animation code AND
  automatically applying all fixes and additions in one unattended pass — no manual review
  step. Trigger on: "enhance my animations", "fix and add animations", "upgrade this site's
  animations", "animation upgrade", "/motion-enhance", or any request that combines auditing
  with auto-applying fixes and/or adding missing animations. Key signals: "check for problems
  then fix them", "audit and add what's missing", "fix all issues and add scroll reveals",
  "process all my HTML files and add animations", "make it animated — but check existing CSS
  first". Also trigger when the user wants to process multiple files for animation upgrades in
  parallel. DO NOT trigger for: audit-report-only requests with no changes applied (use
  motion-audit); requests to add a single new animation without fixing anything (use
  motion-dev); requests to fix only critical issues while leaving warnings for manual review.
---

# motion-enhance

Professional animation enhancement skill for analyzing and automatically fixing animation quality issues.

---

## Pre-flight — Start timer

Run via Bash and save the output as `TASK_START`:
```
TASK_START=$(python .Codex/scripts/query_cost.py --stamp)
```

---

## Routing

- **1 file → Fast Path** (below): audit + edit directly, no sub-agents
- **2+ files → [Parallel Agents](#multi-file-parallel-agents)**: one agent per file, spawned simultaneously

### Step 0 — Prepare Target File

If file ends with `.original.html`: copy to `.enhanced.html` in the same folder, work on the copy. Otherwise: edit in place.

---

### Step 1 — Quick Read & Inline Audit

Read the target file. Load `.Codex/skills/shared/audit-rules.md` Parts B, C, E and scan against the 5-dimension audit framework:

1. **DEPENDENCIES** — GSAP version pinned? Plugins load before `registerPlugin()`? All GSAP plugins are FREE since 3.13 (May 2025) — do NOT flag as 404. `SplitText` before `document.fonts.ready` → WARNING.
2. **MODERNITY** — Zero scroll animations → CRITICAL. Only opacity animated → CRITICAL. No kinetic typography on hero → CRITICAL (portfolio/marketing).
3. **PERFORMANCE** — Animating layout properties (`width/height/top/left/margin/padding`) → CRITICAL. `setTimeout`/`setInterval` for animation → CRITICAL.
4. **CONFLICT** — CSS `transition` + GSAP on same property → CRITICAL. `gsap.from()` on opacity-0 elements → CRITICAL. No `gsap.matchMedia()` → CRITICAL.
5. **CONSISTENCY** — All durations identical → WARNING. Mixed easing families → WARNING.

Bucket issues: CRITICAL / WARNING / INFO. Only load reference files for issue types you found (see Step 1b and Step 2).

### Step 1b — Site-Type Detection & Trend Prioritization

Before loading pattern files:

1. **Classify the page** by HTML signals: `marketing-landing` (hero+CTA+pricing/logos), `portfolio` (work grid, case studies), `saas-app` (auth, sidebar, data tables), `docs-blog` (article, code blocks, TOC), `e-commerce` (product grid, cart), `unknown`.

2. Load `.Codex/motion-library/scores.yaml` — it is already pre-sorted by `/motion-refresh` from highest-priority to lowest-priority candidates for each element bucket.

**For blank-slate files (0 animations), derive the Pattern Baseline dynamically** from `scores.yaml` and `trends-overview.md`.

**Dynamic Baseline Derivation:**
1. Load `.Codex/motion-library/scores.yaml` — read the `site_contexts` block to find which patterns the detected site type prefers/avoids
2. Load `.Codex/motion-library/trends-overview.md` — read the "When NOT to use" line for each candidate pattern to filter appropriately
3. From `scores.yaml`, collect all patterns listed in element-type buckets for the detected site context (e.g. `hero.saas`, `card.saas`, `nav.any`)
4. Preserve the order from `scores.yaml` — it is already sorted by trend priority
5. Treat the first viable pattern per element bucket as the CRITICAL baseline and later viable fallbacks as WARNING or CONSIDER, depending on how strongly they fit the page
6. If you need pattern metadata beyond the ID and order, read only the shortlisted entries from `catalog.yaml`
7. Cross-check each candidate against trends-overview.md "When NOT to use" — if the current site matches an avoid condition, downgrade or skip it

**This approach automatically updates** when `/motion-refresh` changes pattern scores, instead of relying on stale hardcoded lists.

**Guard note:** If the target element for a pattern does not exist (e.g., no badge for text-scramble-decode), mark that pattern as N/A rather than inventing a container.

**Tiebreaker:** When ambiguous between marketing-landing and portfolio, choose marketing-landing if pricing/social proof is present; portfolio if work/case-study links dominate.

### Step 2 — Load Only What You Need

Use this expanded lookup. Read patterns triggered by either audit-driven issues (MODERNITY findings) OR site-type enrichment (from Step 1b baseline). For blank-slate files, the baseline determines what to read.

| Pattern | Read when (audit-driven) | Also apply for site-type enrichment |
|---|---|---|
| `motion-tokens.md` | Any GSAP added | **Always read first if adding any GSAP** |
| `scroll-trigger-reveal` | Zero scroll animations | All site types baseline |
| `kinetic-typography-splittext` | No kinetic typography on hero `<h1>` | marketing-landing (CRITICAL), portfolio (CRITICAL) |
| `text-scramble-decode` | Badge/label is static, decorative | marketing-landing (CRITICAL), portfolio (CONSIDER) |
| `idle-breathing-pulse` | Primary CTA has no ambient animation | marketing-landing (CRITICAL), saas-app status indicators (WARNING) |
| `spring-physics-interactions` | Hover = color only, cards feel flat | marketing-landing, portfolio, e-commerce (CRITICAL) |
| `parallax-depth-layers` | Hero bg layer has no depth | marketing-landing (CRITICAL), portfolio (WARNING) |
| `morphing-button-states` | Primary CTA no loading/success states | marketing-landing, saas-app, e-commerce (CRITICAL) |
| `magnetic-cursor-pull` | Interactive elements lack spatial hover feedback | marketing-landing (WARNING), portfolio (WARNING) |
| `ambient-floating-particles` | Hero feels static, no atmospheric layer | marketing-landing (WARNING), portfolio (CONSIDER) |
| `css-scroll-driven-animations` | No scroll animations AND no GSAP on page | docs/blog (CRITICAL for reading progress) |
| `custom-cursor-follower` | Brand is design-agency or highly visual | portfolio (CONSIDER) — skip for SaaS/docs |
| `bento-grid-motion` | Bento grid layout confirmed in HTML | Only when structure detected |
| `flip-layout-animations` | Dynamic layout reordering present | Only when confirmed |
| `view-transitions-api` | Multi-page or SPA routing present | Only for MPAs/SPAs |
| File read fails, site type undetectable, pattern prerequisites missing, agent error | Error handling reference | `references/error-handling.md` |

**For blank-slate files:**
1. Load `.Codex/motion-library/scores.yaml` and `.Codex/motion-library/trends-overview.md`
2. Read `motion-tokens.md` + only the pattern folders for patterns in your derived baseline
3. Preserve the ranking order from `scores.yaml`
4. Read `catalog.yaml` only if you need metadata for shortlisted patterns that the index does not provide
5. Use trends-overview.md for pattern context (feel, avoid); only read full `index.md` when you need deep implementation details beyond what gsap-patterns.md provides.

### Step 3 — Two-Phase Fix & Enrich

#### Phase A: Fix Issues
Edit the file yourself. No sub-agents.

Rules:
- Fix CRITICALs and WARNINGs automatically.
- Leave INFOs for the user to decide.
- Annotate every token-resolved value: `duration: 0.6,`
- Wrap all motion code in `gsap.matchMedia("(prefers-reduced-motion: no-preference)", ...)` with a `clearProps: "all"` fallback in the `reduce` branch.
- Remove CSS `transition` on any property that GSAP will own.
- Use `gsap.quickTo()` for any handler that fires on `mousemove`.
- Dynamic `willChange`: set on `mouseenter`, remove `onComplete`.

#### Phase B: Add Missing Animations

After fixing issues, enrich with animations using `.Codex/skills/shared/audit-rules.md` Part A (Element Decision Table) and `references/gsap-patterns.md` templates. Prioritize by site-type baseline from Step 1b.

**Key rule:** Never add animations that conflict with existing GSAP. If an element is already animated, mark as ALREADY_ANIMATED and skip.

**Result:** File goes from "has issues" → "fixed + enriched" (issue fixes + new animations)

### Step 3.5 — Syntax Spot-Check

After all edits, re-read the enhanced file and verify:

- [ ] No unclosed `{` or `(` in any added GSAP block
- [ ] No `[placeholder]` text left from pattern application
- [ ] `gsap.registerPlugin(...)` present if any GSAP plugin was added
- [ ] `gsap.matchMedia("(prefers-reduced-motion: no-preference)", ...)` guard present with `reduce` fallback
- [ ] No CSS `transition` remains on any property GSAP now owns

If any check fails: fix inline, then proceed to Step 4. Do not spawn a sub-agent for this.

### Step 3.6 — Code Verification

Verify no animation conflicts remain:
- No CSS `transition` on GSAP-owned properties
- No duplicate animation handlers on same element
- `clearProps` in `prefers-reduced-motion: reduce` branch matches all animated properties
- No animation code runs before DOM is ready

If issues found: fix inline, then proceed. Note "Code validation: PASSED" or "FAILED (fixed)" in summary.

### Step 4 — Summary Report

Output:

```
## Enhancement Complete

### [filename]
- Site type detected: [marketing-landing | portfolio | saas-app | docs-blog | e-commerce | unknown]
- **Phase A (Fix Issues):**
  - Fixed: N CRITICAL, N WARNING
  - Code validation: ✅ PASSED | ⚠️ FAILED (errors fixed, re-run to confirm)
- **Phase B (Add Animations):** [NEW]
  - Elements enhanced with motion-dev patterns:
    - nav → smart hide/show (Pattern 2) | ADDED | SKIPPED — [reason] | ALREADY_ANIMATED
    - hero h1 → hero timeline (Pattern 1) | ADDED | SKIPPED — [reason] | ALREADY_ANIMATED
    - feature cards → stagger reveal (Pattern 4) | ADDED | SKIPPED — [reason] | ALREADY_ANIMATED
    - [etc for each element scanned]
  - Total new animations added: N
  - Total elements enriched: N
- Patterns considered from site-type baseline (derived from scores.yaml order and any shortlisted catalog entries):
  - [For each pattern in the derived baseline, output a line:]
  - {pattern-id} .................. APPLIED | SKIPPED — [reason] | N/A
- Remaining: N INFO items (not auto-applied — ask if wanted)

---

### Metrics

Run via Bash:
```
python .Codex/scripts/query_cost.py --since "$TASK_START"
```
Output the result line directly. If unavailable: _Metrics unavailable — run `python .Codex/scripts/query_cost.py --since <start-timestamp>` manually._

Legend:
- **APPLIED** = used pattern or fixed issue
- **SKIPPED** = applicable but actively decided against [reason]
- **N/A** = structure/context not present in file
- **ALREADY_ANIMATED** = element has existing GSAP (skipped to avoid conflicts)
- **✅ PASSED** = code runs without errors and has no animation conflicts

Then ask: "Want me to apply the remaining INFO-level improvements or add animations to other elements? I'll show you each one first."

---

## Multi-File Parallel Agents

Only use this path when 2+ distinct files are passed. The value here is true parallelism.

### Step 0 — Prepare Target Files

For each `.original.html`, copy to `.enhanced.html` in the same folder.

### Step 1 — Audit all files, produce brief issue lists per file.

### Step 2 — Read `motion-tokens.md` once + only the pattern files needed across all files.

### Step 3 — Spawn Agents (all in one turn)

Group issues by file. Spawn all agents simultaneously. Each agent receives:

```
Fix animation issues in ONE file.
FILE: [absolute path]
ISSUES (sorted by line): [issue list]
TOKEN QUICK REF:
  duration: micro=0.15 fast=0.3 base=0.6 slow=1.0 epic=1.5
  easing:   entrance=power2.out  impact=power3.out  spring=back.out(1.7)  exit=power3.in
  stagger:  tight=0.05  medium=0.09  loose=0.13
  GPU-safe: x y scale rotation opacity  (NOT: top left width height margin)
PATTERN NOTES: [relevant patterns only]
RULES: Read first. Edit one issue at a time. Token comments. Remove CSS transition conflicts. Run syntax check when done.
```

### Step 4 — Summary Report (same format as fast path)

---

## Token Budget Guide

| Scenario | Max pattern files |
|---|---|
| Blank-slate marketing-landing | 7 |
| Blank-slate other site type | 5 |
| Existing GSAP with issues | 4 |
| Minor issues only | 2 |

For patterns applied earlier in the session, `catalog.yaml` description suffices — only read full `index.md` for deep implementation details.

---

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
