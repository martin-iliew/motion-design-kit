---
name: motion-discover
description: >
  Use this skill whenever the user wants to discover, research, or document web
  animation trends. Trigger on: "find animation trends", "what motion patterns are
  modern in 2026", "document animation trends", "/motion-discover", or any request
  involving discovering, researching, or generating web motion patterns and trends.
---

# motion-discover

Professional discovery and documentation skill for researching and cataloging 2026 web animation trends and patterns.

---

## Workflow: Discovery

When `/motion-discover` triggers (or the user asks about discovering animation trends), follow this workflow:

### Pre-flight — Start timer

Run via Bash and save the output as `TASK_START`:
```
TASK_START=$(python .Codex/scripts/query_cost.py --stamp)
```

### Step 1: Research

Search the web for current 2026 micro-interaction and animation trends. Target **12 trends minimum**, covering a spread of:

- Scroll-driven / ScrollTrigger animations
- Physics-based / spring interactions
- Kinetic typography
- Micro-interactions (buttons, forms, icons)
- Transition / navigation patterns
- Cursor / pointer effects
- Bento grid and layout motion
- Ambient / idle animations

**Before evaluating trends,** load `.Codex/skills/motion-discover/references/trend-criteria.md`. Use the 4 Core Principles to assess whether each discovered trend is genuinely 2026-quality (not outdated or derivative). Apply the Quality Checklist when generating each pattern file in Step 2.

### Step 1b: Duplicate Detection

Before generating new patterns:

1. Check if `.Codex/motion-library/catalog.yaml` exists
2. **If it does not exist (library is empty / first run):** skip duplicate checking — all 12 trends are new. Go directly to [Parallel Agent Generation](#parallel-agent-generation).
3. **If it exists:** load it and check each discovered trend against patterns with `status: trending | evergreen | emerging`
   - If a match exists (same technique, same name), **skip generating** — flag it as "already in library, consider refreshing scores"
   - If a `declining` pattern matches, flag it: "This trend replaced [old-pattern] — consider deprecating the old one"
   - Only keep patterns with **no existing match** in the library

This prevents duplicate entries and helps maintain library hygiene.

### Step 1c: Routing (existing library only)

**After duplicate detection, count the new patterns remaining:**

- **12 trends remaining (all new):** go to [Parallel Agent Generation](#parallel-agent-generation) — spawn 12 agents simultaneously.
- **3-11 new patterns:** go to [Parallel Agent Generation](#parallel-agent-generation) — spawn one agent per new pattern simultaneously.
- **1-2 new patterns:** use Fast Path — write all files inline in this conversation. No sub-agents. ~3-5x faster.

---

### Step 2: Generate Library Files (Fast Path — 1-2 patterns only)

For each trend, create a folder `.Codex/motion-library/<kebab-case-name>/` containing three files:

Every folder must contain exactly these three files:

**File 1: `index.md`** - prose only, no code blocks:

```markdown
# [Trend Name]

**Framework:** CSS | Tailwind | GSAP
**Category:** [scroll / micro-interaction / typography / transition / ambient]
**2026 Relevance:** [1-2 sentence explanation of why this pattern is current]

## Description

[2-3 paragraphs: what it is, where it fits, what feeling it creates]

## Do's

- [3-5 specific, actionable items]

## Don'ts

- [3-5 specific, actionable items -- especially common mistakes]

## Best Practices

[2-3 paragraphs covering: accessibility (prefers-reduced-motion), performance (GPU-safe
properties), and integration tips (how to combine with other patterns)]
```

**File 2: `spec.yaml`** - Motion Spec, no imports or code:

```yaml
version: "1"
type: tween | procedural | browser-native # choose one
id: "[kebab-case-pattern-id]"
# ... fields appropriate for the type (see .Codex/motion-spec.md for schema)
a11y:
  reduced_motion: instant-final | skip
```

**File 3: `snippet.css` or `snippet.js`** - pure behavior code only:

- Extension: `.css` for CSS-only patterns, `.js` for GSAP/JS patterns
- **Zero import statements**, zero CDN script tags, zero HTML boilerplate
- Only the animation logic itself, assuming dependencies are already loaded

### Step 3: Update catalog.yaml

After all pattern folders are written, append each new pattern to `.Codex/motion-library/catalog.yaml`. If the file does not exist, create it. Format:

```yaml
version: "1"
patterns:
  - id: [kebab-case-id]
    name: "[Trend Name]"
    type: tween | procedural | browser-native
    category:
      [scroll | micro-interaction | typography | transition | ambient | cursor]
    framework: CSS | GSAP | Tailwind
    description: "[One-line description]"
    folder: [kebab-case-id]
    snippet: snippet.css | snippet.js
    trend_score: null              # Will be filled in by /motion-refresh
    status: emerging               # New patterns start as "emerging"
    popularity_signal: null        # Will be populated by /motion-refresh
    last_reviewed: [current month] # YYYY-MM (today's date)
    sources: []                    # Will be populated by /motion-refresh
    manual_override: false
    notes: "Newly generated from /motion-discover"
```

Do **not** write directly to `.Codex/motion-library/scores.yaml` here. It is an auto-generated inverted index owned by `/motion-refresh`.

These placeholder trend fields allow `/motion-refresh` to discover and score the new pattern on the next run.

**Note:** After generating new patterns, run `/motion-refresh` to regenerate the `scores.yaml` inverted index. New patterns are discoverable from `catalog.yaml` immediately but will not appear in element-type lookups until the refresh runs.

### Step 4: Summary Table

After all files are written and catalog.yaml is updated, output:

```
## Motion Library Generated

| Trend | Framework | Folder | Snippet |
|-------|-----------|--------|---------|
| ...   | ...       | ...    | ...     |

Total: N trends documented.
```

### Metrics

Run via Bash:
```
python .Codex/scripts/query_cost.py --since "$TASK_START"
```
Output the result line directly. If unavailable: _Metrics unavailable — run `python .Codex/scripts/query_cost.py --since <start-timestamp>` manually._

**Reference:** Only load `.Codex/skills/motion-discover/references/gsap-cheatsheet.md` when generating GSAP-based snippets. Do not load it for CSS-only trends.

---

## Parallel Agent Generation

Use this path when 3+ new patterns need writing (including all first-run / blank-library cases).

Spawn all agents simultaneously in a single message — never wait for one before spawning the next.

Each agent receives:

```
Write a motion library pattern for ONE trend.

TREND NAME: [name]
PATTERN ID: [kebab-case-id]
FRAMEWORK: CSS | GSAP | Tailwind

OUTPUT FOLDER: .Codex/motion-library/[kebab-case-id]/

Create exactly 3 files:
1. index.md - prose only, no code blocks. Sections: Description, Do's, Don'ts, Best Practices.
2. spec.yaml - Motion Spec YAML with version, type, id, and a11y.reduced_motion fields.
3. snippet.css OR snippet.js - pure animation logic only. Zero imports, zero CDN tags, zero HTML.

TOKEN QUICK REF:
duration: micro=0.15 fast=0.3 base=0.6 slow=1.0 epic=1.5
easing:   entrance=power2.out  impact=power3.out  spring=back.out(1.7)  exit=power3.in
stagger:  tight=0.05  medium=0.09  loose=0.13

RULES:
- Use token values above for all durations, easings, and stagger delays — add // token: <name> comments
- No import statements in any file
- snippet extension: .css for CSS-only patterns, .js for GSAP/JS patterns
- Reduced-motion guard required in all GSAP snippets (gsap.matchMedia)
- GPU-safe properties only: x, y, scale, rotation, opacity, autoAlpha
```

After all agents complete, run Steps 3-4 (catalog.yaml update + summary table) inline.

---

## General Rules

- Always respect `prefers-reduced-motion`. Any generated GSAP code must include a matchMedia guard.
- Never animate layout-triggering properties (`width`, `height`, `top`, `left`, `margin`). Only animate `transform` and `opacity` for GPU-composited performance.
- Easing vocabulary: use `power2.out` for entrances, `power2.inOut` for transitions, `elastic.out(1, 0.3)` for playful micro-interactions, `CustomEase` for branded motion.

---

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
