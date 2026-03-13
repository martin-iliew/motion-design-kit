# Catalog Contract

New pattern folders live in `.claude/motion-library/<pattern-id>/` and contain exactly:

1. `index.md`
2. `spec.yaml`
3. `snippet.css` or `snippet.js`

Rules:

- `index.md` is prose only.
- `spec.yaml` must include `version`, `type`, `id`, and `a11y.reduced_motion`.
- `snippet.*` is behavior-only code: no imports, no HTML, no CDN tags, no setup boilerplate.
- GSAP snippets must use `gsap.matchMedia()` with a reduced-motion branch.
- Prefer GPU-safe properties unless a plugin-specific vector/path API is genuinely required.

Every `catalog.yaml` entry must include:

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

- `catalog.yaml` is the authoritative metadata store.
- `scores.yaml`, `site-baselines.yaml`, and `trend-watchlist.yaml` are generated surfaces owned by `motion-refresh`.
- Discovery writes new folders plus `catalog.yaml` entries; refresh makes them runtime-usable.
