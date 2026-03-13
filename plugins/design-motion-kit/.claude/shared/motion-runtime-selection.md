# Motion Runtime Selection

Use this reference whenever `motion-build` or `motion-upgrade` needs page-level pattern selection.

## 1. Load shared inputs first

Always start with:

- target file
- `.claude/motion-library/site-baselines.yaml`
- `.claude/motion-library/trend-watchlist.yaml`

If present, load these before selecting motion:

- `brief/design-decision-pack.yaml`
- `brief/motion-hints.yaml`

## 2. Detect only real buckets

Scan the file top-to-bottom and detect only buckets that actually exist:

`nav`, `menu`, `hero`, `heading`, `badge`, `card`, `button`, `cta`, `section`, `footer`, `background`, `logos`, `pricing`, `stat`, `label`, `grid`, `tabs`, `accordion`, `modal`, `drawer`, `toast`, `tooltip`, `form`, `input`, `gallery`, `carousel`, `media`, `image`, `video`, `svg`, `icon`, `loader`, `timeline`, `progress-bar`, `hotspot`

## 3. Obey design hints before ranking

For each detected bucket:

1. Confirm the element exists in the design decision pack.
2. Check whether `motion-hints.yaml` exposes allowed families or intensity limits.
3. Reject candidates that violate the hint contract.

## 4. Select patterns cheaply

1. Use compiled baselines first.
2. Read `.claude/motion-library/scores.yaml` only when the compiled layer is not enough.
3. Open only the winning pattern folder `spec.yaml` plus snippet.

## 5. Output expectations

- `motion-build`: turn winners into an explicit Animation Plan
- `motion-upgrade`: fix issues first, then apply non-conflicting winners
- never animate buckets marked absent, unsupported, or out-of-scope by the design handoff
