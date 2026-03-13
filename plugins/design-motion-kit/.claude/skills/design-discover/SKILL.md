---
name: design-discover
description: >
  Research and catalog new non-code landing-page patterns for the shared design library. Trigger
  on requests to expand the design library, document current homepage pattern baselines, or add
  new design entries without implementing a page directly. Do not trigger for page work
  (design-build or design-upgrade) or rescoring existing entries (design-refresh).
---

# design-discover

This skill owns research-only expansion of the non-code design library.

## Workflow

1. Load `.claude/skills/design-discover/references/trend-criteria.md`.
2. Research official company pages and recent first-party design guidance.
3. Deduplicate against `.claude/design-library/catalog.yaml`.
4. Generate only missing patterns using `.claude/skills/design-discover/references/catalog-contract.md`.
5. Create pattern folders with:
   - `spec.yaml`
   - `index.md`
   - `composition.yaml`
6. Do not generate code snippets in the design library.

If immediate usability matters, run `/design-refresh` after adding the new patterns.

## Validation

Run:

```bash
python .claude/scripts/validate_design_library.py --expected-count <current-catalog-size>
```

## Final response

Use the `design-discover` contract from `.claude/shared/output-contracts.md`.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
