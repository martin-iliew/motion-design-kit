---
name: web-discover
description: >
  Use this skill whenever the task involves discovering, researching, or cataloging landing-page
  design patterns for the shared design library rather than implementing a specific page. Trigger
  on: "find landing page trends", "expand my web design library", "document big-company SaaS
  patterns", "/web-discover", or any request to research and write new pattern entries for
  landing-page layouts, proof systems, pricing patterns, or CTA structures. Do not trigger for
  requests to redesign a specific page (use web-build or web-upgrade), reranking existing catalog
  patterns (use web-refresh), or report-only audits of page code (use web-audit).
---

# web-discover

Canonical discovery skill for researching, batching, and cataloging conversion-first landing-page patterns.
This skill owns research-only trend discovery and library expansion. Ordinary implementation requests should use `web-build` and consume the refreshed runtime layer.

## Workflow

### 1. Research candidates in batches

1. Load `.claude/skills/web-discover/references/trend-criteria.md`.
2. Use **WebSearch** and **WebFetch** to research current patterns on official company sites and recent first-party design articles.
3. Research candidates in 8-12 pattern batches.
4. Start with official product-company pages first.
5. Use third-party commentary only as secondary validation.

### 2. Deduplicate against the catalog

Before generating folders:

1. Read `.claude/design-library/catalog.yaml` if it exists.
2. Skip exact duplicates and obvious near-duplicates.
3. Reject novelty-only patterns that weaken clarity or conversion.

### 3. Generate only the missing patterns

- 1-2 new patterns: generate inline
- 3-12 new patterns: parallelize one agent per pattern
- 13+ new patterns: split into multiple batches

Use `.claude/skills/web-discover/references/catalog-contract.md` for the folder and metadata contract.

### 4. Refresh only when immediate usability matters

If the user expects the new patterns to be usable right away by `web-build` or `web-upgrade`, run `/web-refresh` after generation.

Discovery writes:

- new pattern folders under `.claude/design-library/`
- new or merged entries in `.claude/design-library/catalog.yaml`

Discovery does not hand-edit:

- `scores.yaml`
- `site-baselines.yaml`
- `trend-watchlist.yaml`

### 5. Validate before stopping

Run:

```bash
python .claude/scripts/validate_design_library.py --expected-count <current-catalog-size>
```

If validation fails, fix the corpus before reporting success.

## Final response

Write a `catalog-additions.md` file to `.claude/design-library/` listing all new patterns added in this run.

Then output a concise table:

```md
## Design Library Generated

| Pattern | Category | Folder | Snippet |
| --- | --- | --- | --- |
| ... | ... | ... | ... |

Total new patterns: N
Current catalog size: M
```

Do not print metrics unless the user or a benchmark workflow explicitly asks for them.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
