---
name: design-system
description: >
  Internal skill for converting the scraper-provided DTCG bundle into the derived Tailwind v4
  theme layer used by design and implementation workflows. Trigger only from design or coder
  workflows that have a `brief/tokens.dtcg.json` input.
---

# design-system

This is an internal skill. It is not a public command surface.

## Workflow

1. Validate `brief/tokens.dtcg.json`.
2. Run:

```bash
python .claude/scripts/dtcg_to_tailwind_theme.py --input brief/tokens.dtcg.json --out-css brief/theme.css --out-aliases brief/token-aliases.json
```

3. Treat `brief/theme.css` and `brief/token-aliases.json` as required downstream inputs.
4. Use vendored references only when they help refine the theme quality:
   - `.claude/skills/vendor/anthropic/theme-factory/SKILL.md`
   - `.claude/skills/vendor/anthropic/frontend-design/SKILL.md`

## Rules

- DTCG is the canonical source of truth
- Tailwind v4 theme output is derived, never hand-authored first
- preserve aliases instead of flattening away design intent
- emit ASCII-safe CSS and JSON
