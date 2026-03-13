# Shared Output Contracts

Use these response shapes for the canonical motion skills.

Default behavior is concise. Metrics are maintainer diagnostics, not default user-facing output.

---

## `motion-build`

### Default (`fast` and `balanced`)

Report only:

- target file created or edited
- mode used
- detected stack or site type when relevant
- short Animation Plan or pattern list
- one sentence on major guardrails respected

Recommended format:

```md
## Motion Build Complete

- File: [path]
- Mode: balanced
- Stack/Site: marketing-landing, vanilla HTML
- Plan: nav -> scroll-velocity-navbar; hero -> kinetic-typography-splittext; pricing -> scroll-trigger-reveal
- Guardrails: reduced-motion, cleanup, and ownership checks applied
```

### `premium`

May include one extra line covering richer composition or premium-only escalation used.

Do not append a follow-up sales question.

---

## `motion-upgrade`

### Default (`fast` and `balanced`)

Report only:

- target file(s)
- mode used
- detected site type when relevant
- issue counts fixed (`CRITICAL`, `WARNING`)
- motion added or skipped per major bucket
- remaining `INFO` count when relevant

Recommended format:

```md
## Motion Upgrade Complete

- File: [path]
- Mode: balanced
- Site type: portfolio
- Fixed: 2 critical, 1 warning
- Added: hero -> kinetic-typography-splittext, projects -> scroll-trigger-reveal
- Skipped: footer -> already animated
- Remaining: 1 info
```

### `premium`

May include one extra line summarizing premium-only enhancements or escalation used.

Do not ask whether to apply more changes. `motion-upgrade` is an unattended pass.

---

## `motion-audit`

### Default

Report only:

- target file
- structured severity table
- summary counts for `CRITICAL`, `WARNING`, and `INFO`
- concrete fix patches for every `CRITICAL` and `WARNING`

Recommended format:

```md
## Audit Report: [filename]

| # | Issue | Severity | Location | Fix |
| --- | --- | --- | --- | --- |
| 1 | ... | CRITICAL | line 42 | ... |

**Summary:** 2 critical, 3 warnings, 1 info

### Fix #1 — [Issue Name]

**Before:**
...

**After:**
...

**Why:** ...
```

`motion-audit` stops after the report. If the user later asks for changes, route unattended fixes to `motion-upgrade` and targeted implementation work to `motion-build`.

---

## Diagnostics

Only include `query_cost.py` metrics when one of these is true:

- the user explicitly asked for cost or token reporting
- a maintainer workflow explicitly requested metrics
- a benchmark or evaluation task requires them

When metrics are needed:

- `motion-build` single-element: `motion-build-single`
- `motion-build` page-level: `motion-build-page`
- `motion-upgrade` single-file: `motion-upgrade-single`
