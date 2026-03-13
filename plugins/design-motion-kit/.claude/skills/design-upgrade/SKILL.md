---
name: design-upgrade
description: >
  Canonical landing-page design modernization skill for unattended audit-and-fix passes across
  existing HTML, React, Vue, or Svelte files. Trigger when the user wants the page reviewed and
  upgraded in one pass. Do not trigger for report-only reviews (use design-audit), targeted
  section redesigns (use design-build), or library maintenance tasks (use design-discover or
  design-refresh).
---

# design-upgrade

Designer-first upgrade workflow for the merged `design-motion-kit`.

## 0. Parse the request

1. Strip a leading `mode:` prefix when present.
2. Default to `balanced`.
3. Redirect report-only review work to `/design-audit`.
4. Redirect single targeted redesign work to `/design-build`.

## 1. Load shared policy first

Load:

- `.claude/shared/execution-modes.md`
- `.claude/shared/bundle-loading.md`
- `.claude/shared/design-runtime-selection.md`
- `.claude/shared/design-guardrails.md`
- `.claude/shared/handoff-contracts.md`
- `.claude/shared/validation.md`
- `.claude/shared/output-contracts.md`
- `.claude/shared/design-audit-rules.md`

## 2. Refresh bundle artifacts before editing

1. Load `.claude/skills/internal/design-system/SKILL.md`.
2. Run:

```bash
python .claude/scripts/build_design_artifacts.py --brief-dir brief --out-dir brief
```

3. Use the existing `brief/design-decision-pack.yaml` as the starting plan and update it when the audit changes the chosen surfaces.

## 3. Upgrade workflow

1. Audit the target files with `.claude/shared/design-audit-rules.md`.
2. Fix clarity, hierarchy, proof, conversion, and token-usage issues first.
3. Use `.claude/shared/design-runtime-selection.md` for any missing or weak surfaces.
4. Open only the winning pattern folders: `spec.yaml`, `index.md`, and `composition.yaml`.
5. Load `.claude/skills/internal/design-coder/SKILL.md` and implement from the updated decision pack.

## 4. Hard rules

- `design-upgrade` is unattended once it begins
- never skip the design-system pass when `brief/tokens.dtcg.json` exists
- never add motion code here
- never leave raw values behind when token aliases exist

## 5. Final response

Use the `design-upgrade` contract from `.claude/shared/output-contracts.md`.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
