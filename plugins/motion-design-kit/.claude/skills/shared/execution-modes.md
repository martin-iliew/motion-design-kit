# Shared Execution Modes

Load this reference before any `motion-build` or `motion-upgrade` implementation work.

`.claude` is the source of truth for mode behavior.

---

## Mode Syntax

Supported leading syntax:

- `/motion-build mode: fast <file> <request>`
- `/motion-build mode: balanced <file> <request>`
- `/motion-build mode: premium <file> <request>`
- `/motion-upgrade mode: fast <file...>`
- `/motion-upgrade mode: balanced <file...>`
- `/motion-upgrade mode: premium <file...>`

Parsing rules:

1. If the request begins with `mode: <value>`, strip that prefix and store the value.
2. Allowed values are `fast`, `balanced`, and `premium`.
3. If the prefix is absent, default to `balanced`.
4. Never silently upgrade a request to `premium`; `premium` must be explicit or clearly required by a showcase/premium brief.

---

## Shared Mode Contract

### `fast`

Primary goal: lowest token and time cost that still ships safe, modern motion.

- Use the compiled selector layer only.
- Do not open `scores.yaml` for page-level selection.
- Do not open `trends-overview.md`.
- Do not do live trend research.
- Only fetch GSAP docs when a plugin or API detail is genuinely required to avoid incorrect code.
- Enrich only top-value buckets.
- Do not add optional decorative interaction layers.
- Keep summaries concise.

Top-value buckets:

- `hero`
- `nav`
- primary `cta`
- first major `card` or `pricing` group
- first major `section` reveal block

### `balanced`

Primary goal: default production mode for cost-efficient, trend-aware output.

- Start with the compiled selector layer.
- Open `scores.yaml` only when the compiled selector layer cannot choose safely.
- Do not open `trends-overview.md` unless an escalation rule from `runtime-selection.md` applies.
- Do not do live trend research.
- Enrich all relevant non-conflicting buckets.
- Allow one optional interaction enhancement total for `hero`, `nav`, or primary `cta` when it is cheap and stack-safe.
- Keep summaries concise.

### `premium`

Primary goal: showcase-grade motion when the user explicitly wants more range.

- Start with the compiled selector layer.
- `scores.yaml` is allowed when the compiled layer is insufficient.
- `trends-overview.md` is allowed only when the shared escalation rules apply.
- One official GSAP doc fetch is allowed when a plugin or API detail is needed.
- Allow richer composition and one optional interaction enhancement per high-value bucket.
- Summary can be slightly richer than `fast` or `balanced`, but still focused.

---

## Escalation Permissions

Apply these before loading more sources:

| Source | `fast` | `balanced` | `premium` |
| --- | --- | --- | --- |
| `site-baselines.yaml` + `trend-watchlist.yaml` | yes | yes | yes |
| `scores.yaml` for isolated lookups | yes | yes | yes |
| `scores.yaml` for page fallback | no | yes | yes |
| `trends-overview.md` | no | conditional | conditional |
| live GSAP docs for plugin/API clarification | conditional | conditional | yes |
| live trend research | no | no | no |
| `catalog.yaml` during normal build/upgrade | no | no | no |

`motion-refresh` is the only skill that should refresh trend knowledge for normal runtime consumption.

---

## Mode-Safe Defaults

- Default mode for both canonical commands is `balanced`.
- All hard guardrails remain mandatory in every mode.
- If the request is narrow, stay narrow even in `premium`.
- If the request is large, `fast` may leave lower-value buckets untouched rather than adding noisy motion.
