---
name: web-refresh
description: >
  Use this skill whenever the task involves rescoring, reranking, or re-evaluating existing
  patterns in the design library against current landing-page practice, including full-library
  refreshes, subset rescoring, or single-pattern relevance checks. Trigger on: "refresh the web
  design library", "rerank the landing-page patterns", "rebuild the runtime layer",
  "regenerate scores.yaml", "which of these patterns are still current?", or "/web-refresh". Do
  not trigger for adding new patterns to the catalog (use web-discover), implementing page
  changes (use web-build or web-upgrade), or report-only page audits (use web-audit).
---

# web-refresh

Canonical refresh skill for rescoring the catalog and regenerating the runtime selector layer consumed by the web design skills.

## Workflow

### 1. Research the current baseline

Use **WebSearch** and **WebFetch** to research what is current before scoring. Search official product-company homepages and recent first-party design guidance.

Capture:

- what is stable table stakes
- what is rising but still conversion-safe
- what feels noisy or outdated
- which section patterns appear repeatedly across serious company sites

### 2. Refresh the catalog trend fields

Read:

- `.claude/design-library/catalog.yaml`
- `.claude/design-library/trends-overview.md`
- `.claude/design-library/scores.yaml`

Update only the trend-facing fields unless metadata repair is required:

- `trend_score`
- `status`
- `conversion_signal`
- `last_reviewed`
- `sources` when missing or stale

Respect `manual_override: true`.

### 3. Regenerate runtime outputs

Use `.claude/skills/web-refresh/references/runtime-outputs.md` as the contract for:

- `scores.yaml`
- `site-baselines.yaml`
- `trend-watchlist.yaml`

Use the existing scripts to rebuild the generated surfaces instead of retyping their logic in this skill file.

### 4. Detect gaps

If research surfaces current patterns that are missing from `catalog.yaml`:

- report them as gaps
- recommend `/web-discover`
- do not auto-generate them here unless the user explicitly requested both discovery and refresh

### 5. Validate before stopping

Run:

```bash
python .claude/scripts/validate_design_library.py --expected-count <current-catalog-size>
```

If validation fails, fix the catalog, overview, or generated outputs before reporting success.

## Final response

Report only:

- catalog size
- number of patterns rescored
- whether runtime outputs were regenerated
- notable movers
- patterns drifting toward novelty or overuse
- discovery gaps worth generating next

Do not print metrics unless the user or a benchmark workflow explicitly asks for them.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
