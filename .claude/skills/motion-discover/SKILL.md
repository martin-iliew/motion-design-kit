---
name: motion-discover
description: >
  Use this skill whenever the user wants to discover, research, or document web
  animation trends. Trigger on: "find animation trends", "what motion patterns are
  modern in 2026", "document animation trends", "/motion-discover", or any request
  involving discovering, researching, or generating web motion patterns and trends.
---

# motion-discover

Professional discovery and documentation skill for researching, batching, and cataloging modern web animation patterns.

---

## Workflow: Discovery

When `/motion-discover` triggers, follow this workflow.

### Pre-flight — Start timer

Run via Bash and save the output as `TASK_START`:
```
TASK_START=$(python .claude/scripts/query_cost.py --stamp)
```

### Step 1: Research by batch

Research the next batch of motion patterns before writing files.

Rules:
- Work in batches of **10-15 candidate patterns** at a time. Never hardcode the total library size.
- Start with **official GSAP references first**: `https://gsap.com/llms.txt` plus the specific plugin pages relevant to the batch.
- Use recent design-community examples second (Codrops, Awwwards-adjacent examples, strong agency references) only to validate that a pattern still feels current.
- Before evaluating trends, load `.claude/skills/motion-discover/references/trend-criteria.md` and apply the 4 Core Principles plus the Quality Checklist.

Typical batch mixes:
- Scroll storytelling / pinned narratives
- Typography / SplitText / text treatment
- Navigation / UI state / forms
- Media / gallery / drag interactions
- SVG / path / icon / loader motion

### Step 2: Duplicate detection

Before generating patterns:

1. Check whether `.claude/motion-library/catalog.yaml` exists.
2. If it exists, compare each candidate against `catalog.yaml` entries with `status: trending | evergreen | emerging`.
3. Skip exact duplicates or obvious near-duplicates that solve the same interaction with the same technique.
4. If a declining pattern has a clear modern replacement, flag that relationship in your notes.

### Step 3: Route by remaining count

After duplicate detection:

- **1-2 new patterns:** Fast path. Write the folders inline in this conversation.
- **3-15 new patterns:** One agent per pattern, all spawned in parallel.
- **16+ new patterns:** Split into multiple 10-15 pattern batches and process each batch independently.

### Step 4: Pattern folder contract

Each new pattern folder must be `.claude/motion-library/<pattern-id>/` and contain exactly 3 files:

1. `index.md`
2. `spec.yaml`
3. `snippet.css` or `snippet.js`

Rules:
- `index.md` is prose only. No code fences.
- `spec.yaml` is a Motion Spec document. `type` is free-form, but every spec must include `version`, `type`, `id`, and `a11y.reduced_motion`.
- `snippet.*` is pure behavior code only: no imports, no CDN tags, no HTML, no setup boilerplate.
- Every GSAP snippet must use `gsap.matchMedia()` with a reduced-motion branch.
- Only animate GPU-safe properties unless the specific pattern truly depends on a plugin-specific vector/path API.

### Step 5: Catalog schema

After writing the folders, add or merge each new pattern into `.claude/motion-library/catalog.yaml` using the live schema below.

Every catalog entry must include:

```yaml
- id: kebab-case-id
  name: "Human Name"
  type: tween | procedural | browser-native | any future type
  category: scroll | typography | micro-interaction | transition | ambient | cursor | svg
  framework: GSAP | CSS | Tailwind | Mixed
  triggers: [scroll, hover, click]
  components: [hero, card, nav]
  folder: kebab-case-id
  snippet: snippet.js
  description: "One-line description"
  trend_score: 1-10 | null
  status: trending | evergreen | emerging | declining
  popularity_signal: high | medium | low | null
  last_reviewed: YYYY-MM
  sources: [https://...]
  manual_override: false
  notes: "Why this entry exists or what replaced it"
```

Important:
- Keep `type` open-ended. Do not coerce new pattern types into a smaller enum.
- `catalog.yaml` is the authoritative metadata store.
- `scores.yaml` is an auto-generated inverted index. Do **not** hand-edit it here.

### Step 6: Refresh immediately when usability matters

If the user wants the new patterns to be usable right away by `motion-dev` or `motion-enhance`, run `/motion-refresh` in the same pass after generation.

Use this rule:
- If you added patterns and the user expects the library to be immediately consumable, refresh now.
- If the user only asked for raw discovery artifacts, it is acceptable to stop after updating `catalog.yaml` and tell them refresh is still required.

### Step 7: Output

After each batch, output:

```
## Motion Library Generated

| Pattern | Framework | Folder | Snippet |
|---------|-----------|--------|---------|
| ...     | ...       | ...    | ...     |

Total new patterns: N
Current catalog size: M
```

Before closing the task, validate the corpus:
```
python .claude/scripts/validate_motion_library.py --expected-count <current-catalog-size>
```
If it fails, fix the corpus before reporting success.

### Metrics

Run via Bash:
```
python .claude/scripts/query_cost.py --since "$TASK_START"
```
Output the result line directly. If unavailable: _Metrics unavailable — run `python .claude/scripts/query_cost.py --since <start-timestamp>` manually._

---

## General Rules

- Prefer official GSAP sources first, then recent community validation.
- Respect `prefers-reduced-motion` in every generated snippet.
- Never animate layout-triggering properties when a transform-based alternative exists.
- Keep counts dynamic. Do not write instructions that assume a fixed catalog size, fixed template count, or fixed number of pattern folders.

---

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
