# Shared Runtime Selection — Motion Build and Motion Upgrade

Load this reference whenever page-level motion or upgrade enrichment needs trend-aware pattern selection.

Apply `.claude/skills/shared/execution-modes.md` before any escalation beyond the compiled selector layer.

---

## Core Inputs

Always start with:

- target file
- `.claude/motion-library/site-baselines.yaml`
- `.claude/motion-library/trend-watchlist.yaml`

Use the compiled selector layer first. Treat `scores.yaml`, `catalog.yaml`, and `trends-overview.md` as escalation-only inputs.

---

## Detection Pass

### Bucket scan

Scan top-to-bottom and detect only buckets that actually exist:

`nav`, `menu`, `hero`, `heading`, `badge`, `card`, `button`, `cta`, `section`, `footer`, `background`, `logos`, `pricing`, `stat`, `label`, `grid`, `tabs`, `accordion`, `modal`, `drawer`, `toast`, `tooltip`, `form`, `input`, `gallery`, `carousel`, `media`, `image`, `video`, `svg`, `icon`, `loader`, `timeline`, `progress-bar`, `hotspot`

### Site classification

Classify the page as one of:

- `marketing-landing`
- `portfolio`
- `docs-blog`
- `ecommerce`
- `saas-app`
- `unknown`

### Required page signals

Detect these signals from the file itself:

- `has_fixed_nav`
- `has_active_nav_state`
- `has_large_display_heading`
- `simple_heading`
- `card_has_media`
- `card_grid_present`
- `hover_relevant`
- `desktop_interaction_ok`
- `numeric_stats_present`
- `hero_has_background_layers`
- `expressive_brand`
- `accessibility_first_page`
- `dense_utility_page`
- `non_portfolio_page`
- `non_expressive_brand`
- `touch_heavy_audience`
- `badge_present`
- `cta_present`
- `gallery_present`
- `pricing_cards_present`
- `footer_present`
- `tabs_present`
- `form_present`
- `timeline_present`

Guard notes:

- Mark missing target buckets as `N/A`; do not invent containers.
- When ambiguous between `marketing-landing` and `portfolio`, choose `marketing-landing` if pricing/social proof dominates and `portfolio` if work/case-study links dominate.
- Treat `unknown` as conservative; escalate before decorative or premium-only patterns.

---

## Selection Algorithm

1. Look up the detected site type in `site-baselines.yaml`.
2. For each detected bucket, inspect candidates in order.
3. Choose the first candidate whose `when` conditions all pass.
4. Reject that candidate if a matching `trend-watchlist.yaml` `avoid_when` condition is active.
5. Fall through to the next candidate.
6. If nothing survives for that bucket, skip it.

For `motion-build`, convert the surviving candidates into an explicit Animation Plan before implementation.

For `motion-upgrade`, use the surviving candidates only after the audit pass and skip any bucket that already has conflicting GSAP ownership.

---

## Pattern Loading Rules

1. Read only the winning pattern folder's `spec.yaml` plus snippet from `.claude/motion-library/[pattern-id]/`.
2. Treat the winning pattern folder as the primary implementation source.
3. Use `.claude/skills/motion-build/references/gsap-patterns.md` only when the folder snippet is too narrow or multiple winners must be stitched together.
4. Use `.claude/skills/motion-build/references/live-sources.md` plus official GSAP docs only when plugin or API clarification is still needed.
5. Do not open the whole pattern library.
6. Do not apply more than `1` primary motion pattern per bucket plus `1` optional interaction enhancement per bucket.

---

## Escalation Rules

- Read `.claude/motion-library/scores.yaml` only when the compiled layer cannot make a safe page-specific choice.
- Read `.claude/motion-library/trends-overview.md` only when:
  - page type is ambiguous
  - the request is premium/showcase/creative-direction-heavy
  - a selected winner is blocked and fallback needs deeper judgment
  - the user explicitly asks for trend context
- Read `.claude/motion-library/catalog.yaml` only when the compiled files are insufficient.

Never use `catalog.yaml` as the default selection surface for normal page generation or upgrade work.

---

## Output Expectations

### `motion-build`

- Output an Animation Plan that maps selected buckets to winning patterns.
- Implement every selected winner.
- Use `scores.yaml` directly only for isolated element or single-component lookups.

### `motion-upgrade`

- Apply the same selection flow after the audit pass.
- Fix issues first, then enrich only with non-conflicting additions.
- Record each selected pattern as `APPLIED`, `SKIPPED`, `N/A`, or `ALREADY_ANIMATED` in the final summary.
