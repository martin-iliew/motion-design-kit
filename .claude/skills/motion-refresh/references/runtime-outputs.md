# Runtime Outputs Contract

`motion-refresh` owns the runtime-facing generated files:

- `.claude/motion-library/scores.yaml`
- `.claude/motion-library/site-baselines.yaml`
- `.claude/motion-library/trend-watchlist.yaml`

## `scores.yaml`

- Include every component bucket represented in `catalog.yaml`.
- Exclude `status: declining` entries from ranked lists.
- Sort ranked lists by `trend_score` descending.
- Preserve the site-context personality block.
- Keep expanded component families available for runtime lookups.

## `site-baselines.yaml`

- Derive from `scores.yaml` plus `trends-overview.md`.
- Keep only top candidates per site-type and bucket.
- Default max per bucket:
  - `1` primary
  - `1` fallback
  - `1` optional interaction enhancement
- Keep candidates ordered and conditional via `pattern` plus `when`.

## `trend-watchlist.yaml`

- Store runtime avoid rules distilled from current research and `trends-overview.md`.
- Capture overused patterns, accessibility-first exclusions, dense utility-page exclusions, and premium-only warnings.
- Use `avoid_when` lists so `motion-upgrade` can cheaply reject unsuitable winners at runtime.

## Refresh Boundaries

- `motion-refresh` may update trend fields in `catalog.yaml` and align `trends-overview.md`.
- `motion-refresh` should not rewrite pattern folders unless metadata repair is required.
- `motion-build` and `motion-upgrade` consume these generated files; they do not research trends live.
