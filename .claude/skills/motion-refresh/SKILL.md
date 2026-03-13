---
name: motion-refresh
description: >
  Use this skill whenever the task involves rescoring, reranking, or re-evaluating existing
  patterns in the motion library against current web animation trends — including full-library
  refreshes, subset rescores, or single-pattern relevance checks. Trigger on: "refresh the
  motion library scores", "rerank the animation patterns", "rescore everything against 2026
  standards", "update the trend scores for scroll patterns", "rebuild the runtime layer",
  "regenerate scores.yaml", "which of my patterns are still trending vs. stale?", "is this
  pattern still high quality in 2026?", "/motion-refresh", or any request to evaluate whether
  existing catalog entries are current and regenerate the lookup index consumed by the other
  motion skills. Also trigger when the user has just added patterns and now needs the whole
  library rescored. DO NOT trigger for: discovering or adding new patterns to the catalog (use
  motion-discover); implementing animations on a page (use motion-build or motion-upgrade);
  auditing animation code quality (use motion-audit); or general trend research questions with
  no intent to update library scores.
---

# motion-refresh

Canonical refresh skill for rescoring the catalog and regenerating the runtime selector layer consumed by the motion skills.

## Workflow

### 1. Research the current baseline

Use **WebSearch** and **WebFetch** to research what is current before scoring — this must be live research, not knowledge retrieval. Search for:

- GSAP changelog and recent showcases (greensock.com, gsap.com)
- Awwwards, Codrops, and CSS-Tricks posts from the last 6 months
- browser-native animation API updates (scroll-driven animations, View Transitions, @starting-style)

Capture:

- what is rising
- what is stable table stakes
- what feels noisy or dated
- which plugin families are appearing in premium builds

### 2. Refresh the catalog trend fields

Read:

- `.claude/motion-library/catalog.yaml`
- `.claude/motion-library/trends-overview.md`
- `.claude/motion-library/scores.yaml` (to get prev_score values for delta reporting)

Update only the trend-facing fields unless metadata repair is required:

- `trend_score`
- `status`
- `popularity_signal`
- `last_reviewed`
- `sources` when missing or stale

Respect `manual_override: true`.

After rescoring, write the updated `catalog.yaml` back to disk and write a new `trends-overview.md` with the updated scores and statuses. Both files must be written — not just read.

### 3. Regenerate runtime outputs

Use `.claude/skills/motion-refresh/references/runtime-outputs.md` as the contract for:

- `scores.yaml`
- `site-baselines.yaml`
- `trend-watchlist.yaml`

Use the existing scripts to rebuild the generated surfaces instead of retyping their logic in this skill file.

### 4. Detect gaps

If research surfaces current patterns that are missing from `catalog.yaml`:

- report them as gaps
- recommend `/motion-discover`
- do not auto-generate them here unless the user explicitly requested both discovery and refresh

### 5. Validate before stopping

Run:

```bash
python .claude/scripts/validate_motion_library.py --expected-count <current-catalog-size>
```

If validation fails, fix the catalog, overview, or generated outputs before reporting success.

## Final response

Report only:

- catalog size
- number of patterns rescored
- whether runtime outputs were regenerated
- notable movers
- declining patterns worth deprecating
- discovery gaps worth generating next

Do not print metrics unless the user or a benchmark workflow explicitly asks for them.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
