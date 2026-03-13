---
name: design-coder
description: >
  Internal implementation skill that translates the design decision pack into clean React and
  Tailwind v4 code using the derived theme artifacts. Trigger only from design workflows after
  the decision pack and token aliases exist.
---

# design-coder

This is an internal skill. It is not a public command surface.

## Inputs

- `brief/theme.css`
- `brief/token-aliases.json`
- `brief/design-decision-pack.yaml`

## Workflow

1. Read the decision pack and map each selected pattern to existing components or new components.
2. Import or reference `brief/theme.css` before writing component-level styles.
3. Use `brief/token-aliases.json` for spacing, color, radius, shadow, typography, and timing values.
4. Prefer clean React/Tailwind implementations over verbose explanation.
5. Use vendored references when they improve implementation quality:
   - `.claude/skills/vendor/anthropic/frontend-design/SKILL.md`
   - `.claude/skills/vendor/anthropic/web-artifacts-builder/SKILL.md`

## Hard Rules

- no raw spacing, color, radius, shadow, typography, or timing values
- keep component boundaries coherent
- reuse existing design-system primitives where they already exist
- do not write motion code here; leave that to `motion-*`
