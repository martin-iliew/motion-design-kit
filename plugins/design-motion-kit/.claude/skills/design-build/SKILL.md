---
name: design-build
description: >
  Canonical landing-page design implementation skill for building, rewriting, modernizing, or
  explaining homepage and conversion-page structure in existing HTML, React, Vue, or Svelte
  files. Trigger when the user wants stronger hierarchy, proof placement, CTA flow, section
  structure, or a full landing-page redesign. Do not trigger for report-only audits (use
  design-audit), unattended audit-plus-fix passes (use design-upgrade), or library expansion
  work (use design-discover).
---

# design-build

Designer-first orchestration skill for the merged `design-motion-kit`.

## 0. Parse the request

1. Strip a leading `mode: fast`, `mode: balanced`, or `mode: premium` prefix when present.
2. Default to `balanced`.
3. Redirect audit-only work to `/design-audit`.
4. Redirect unattended audit-and-modernize work to `/design-upgrade`.
5. Redirect pattern-library generation to `/design-discover`.

## 1. Load shared policy first

Load:

- `.claude/shared/execution-modes.md`
- `.claude/shared/bundle-loading.md`
- `.claude/shared/design-runtime-selection.md`
- `.claude/shared/design-guardrails.md`
- `.claude/shared/handoff-contracts.md`
- `.claude/shared/validation.md`
- `.claude/shared/output-contracts.md`

When you need the rubric, load:

- `.claude/shared/design-audit-rules.md`

## 2. Bootstrap the design-system pipeline

1. If the repo is greenfield and lacks an app shell, load `.claude/skills/internal/vite-react-bootstrap/SKILL.md`.
2. Load `.claude/skills/internal/design-system/SKILL.md`.
3. Run:

```bash
python .claude/scripts/build_design_artifacts.py --brief-dir brief --out-dir brief
```

4. Treat these generated files as required downstream inputs:
   - `brief/theme.css`
   - `brief/token-aliases.json`
   - `brief/design-decision-pack.yaml`
   - `brief/motion-hints.yaml`

## 3. Select patterns, then implement

1. Use `.claude/shared/design-runtime-selection.md` to choose the required design-library winners.
2. Read only the winning folder `spec.yaml`, `index.md`, and `composition.yaml`.
3. Use additional references only when needed:
   - `references/layout-patterns.md`
   - `references/section-recipes.md`
   - `references/copy-signals.md`
4. After the decision pack is current, load `.claude/skills/internal/design-coder/SKILL.md`.
5. Implement from the decision pack, not from raw prose.

## 4. Hard rules

- never do live trend research during `design-build`
- do not invent a design system when `brief/tokens.dtcg.json` exists
- do not emit raw implementation values when token aliases exist
- motion hints describe allowed motion, but motion implementation remains a downstream concern

## 5. Final response

Use the `design-build` contract from `.claude/shared/output-contracts.md`.

*Licensed under the Apache 2.0 License. See LICENSE.txt in the repository root.*
