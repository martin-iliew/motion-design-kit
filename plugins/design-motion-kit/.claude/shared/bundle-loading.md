# Brief Bundle Loading

The upstream scraper hands design work to this plugin through a repo-local `brief/` directory.

## Required Inputs

- `brief/brief.json`
- `brief/copy.md`
- `brief/images.json`
- `brief/tokens.dtcg.json`

## First-Step Workflow

1. Validate that the four required files exist.
2. Load the internal `design-system` skill before selecting patterns or writing code.
3. Run:

```bash
python .claude/scripts/build_design_artifacts.py --brief-dir brief --out-dir brief
```

4. Treat the generated artifacts as the shared source of truth for downstream work.

## Generated Artifacts

- `brief/theme.css`
- `brief/token-aliases.json`
- `brief/design-decision-pack.yaml`
- `brief/motion-hints.yaml`

If the bundle is incomplete, stop and report the missing file(s) instead of inventing equivalent inputs.
