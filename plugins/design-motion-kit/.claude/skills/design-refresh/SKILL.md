---
name: design-refresh
description: >
  Rescore and rerank the existing non-code design library against current landing-page practice.
  Trigger on requests to refresh the catalog, rebuild runtime outputs, or check which existing
  patterns are still current. Do not trigger for adding new patterns (design-discover) or page
  implementation work (design-build or design-upgrade).
---

# design-refresh

This skill rescales existing design-library entries and regenerates the compiled runtime layer.

## Workflow

1. Research current baselines on official company sites and first-party design guidance.
2. Update trend-facing fields in `.claude/design-library/catalog.yaml`.
3. Regenerate:
   - `scores.yaml`
   - `site-baselines.yaml`
   - `trend-watchlist.yaml`
4. Do not add missing patterns here; report them as discovery gaps for `/design-discover`.

## Validation

Run:

```bash
python .claude/scripts/validate_design_library.py --expected-count <current-catalog-size>
python .claude/scripts/validate_runtime_trends.py
```

## Final response

Use the `design-refresh` contract from `.claude/shared/output-contracts.md`.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
