---
name: motion-discover
description: >
  Use this skill whenever the task involves discovering, researching, or cataloging web
  animation trends and patterns for a motion library — not for implementing animations on
  a specific page or site. Trigger on: "find animation trends", "expand my motion library",
  "research current animation patterns", "catalog this technique", "document the View
  Transitions API pattern", "/motion-discover", or any request to research live web animation
  trends and write new pattern entries to the catalog. Also trigger when the user wants to
  document specific animation techniques or APIs (e.g., scroll-driven animations, View
  Transitions) as library entries, or asks what browser-native animation APIs are gaining
  traction. DO NOT trigger for: requests to add animations to a specific page or site (use
  motion-build or motion-upgrade); requests asking "what should I add to my site?" without
  clear library catalog intent; rescoring or reranking existing catalog patterns (use
  motion-refresh); auditing animation code (use motion-audit). The core signal is intent to
  expand the shared motion pattern catalog, not to implement animations on the user's site.
---

# motion-discover

Canonical discovery skill for researching, batching, and cataloging modern web animation patterns.
This skill owns research-only trend discovery and library expansion. Ordinary implementation requests should use `motion-build` and consume the refreshed runtime layer.

## Workflow

### 1. Research candidates in batches

1. Load `.claude/skills/motion-discover/references/trend-criteria.md`.
2. Use **WebSearch** and **WebFetch** to research current trends — this is live research, not knowledge retrieval. Search for recent GSAP showcases, Awwwards/Codrops posts, and browser-native animation API updates from the last 6 months.
3. Research candidates in 10-15 pattern batches.
4. Start with official GSAP references first.
5. Use recent community examples only as validation that a pattern still feels current.

### 2. Deduplicate against the catalog

Before generating folders:

1. Read `.claude/motion-library/catalog.yaml` if it exists.
2. Skip exact duplicates and obvious near-duplicates.
3. Note declining patterns that have a clearer modern replacement.

### 3. Generate only the missing patterns

- 1-2 new patterns: generate inline
- 3-15 new patterns: parallelize one agent per pattern
- 16+ new patterns: split into multiple 10-15 pattern batches

Use `.claude/skills/motion-discover/references/catalog-contract.md` for the folder and metadata contract.

### 4. Refresh only when immediate usability matters

If the user expects the new patterns to be usable right away by `motion-build` or `motion-upgrade`, run `/motion-refresh` after generation.

Discovery writes:

- new pattern folders under `.claude/motion-library/`
- new or merged entries in `.claude/motion-library/catalog.yaml`

Discovery does not hand-edit:

- `scores.yaml`
- `site-baselines.yaml`
- `trend-watchlist.yaml`

### 5. Validate before stopping

Run:

```bash
python .claude/scripts/validate_motion_library.py --expected-count <current-catalog-size>
```

If validation fails, fix the corpus before reporting success.

## Final response

Write a `catalog-additions.md` file to `.claude/motion-library/` listing all new patterns added in this run. This serves as the handoff record for `/motion-refresh` and for auditing what changed.

Then output a concise table:

```md
## Motion Library Generated

| Pattern | Framework | Folder | Snippet |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

Total new patterns: N
Current catalog size: M

catalog-additions.md written to .claude/motion-library/
```

Do not print metrics unless the user or a benchmark workflow explicitly asks for them.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
