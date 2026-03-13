# design-motion-kit Setup

Setup and maintainer guide for `design-motion-kit`.

## Install

```bash
claude plugin marketplace add --scope user martin-iliew/design-motion-kit
claude plugin install --scope user design-motion-kit@design-motion-kit
```

Inside Claude Code, the slash-command equivalent is:

```bash
/plugin marketplace add martin-iliew/design-motion-kit
/plugin install design-motion-kit@design-motion-kit
```

## Project Permissions Profile

Create `.claude/settings.json` in the target app repo:

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "allow": [
      "Bash(rg:*)",
      "Bash(ls:*)",
      "Bash(dir:*)",
      "Bash(Get-ChildItem:*)",
      "Bash(cat:*)",
      "Bash(type:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git ls-files:*)",
      "Bash(git rev-parse:*)",
      "Bash(npm run build:*)",
      "Bash(npm run lint:*)",
      "Bash(npm run test:*)",
      "Bash(pnpm run build:*)",
      "Bash(pnpm run lint:*)",
      "Bash(pnpm run test:*)",
      "Bash(yarn build:*)",
      "Bash(yarn lint:*)",
      "Bash(yarn test:*)",
      "Bash(bun run build:*)",
      "Bash(bun run lint:*)",
      "Bash(bun run test:*)"
    ]
  }
}
```

## Runtime Model

The public command surface is:

- `/design-build`
- `/design-upgrade`
- `/design-audit`
- `/design-discover`
- `/design-refresh`
- `/motion-build`
- `/motion-upgrade`
- `/motion-audit`
- `/motion-discover`
- `/motion-refresh`

Build and upgrade commands support:

- `mode: fast`
- `mode: balanced`
- `mode: premium`

Default mode is `balanced`.

## Brief Bundle

The canonical upstream input is a repo-local `brief/` directory containing:

- `brief.json`
- `copy.md`
- `images.json`
- `tokens.dtcg.json`

Generated downstream artifacts:

- `theme.css`
- `token-aliases.json`
- `design-decision-pack.yaml`
- `motion-hints.yaml`

## Validation

Run after changing commands, skills, library contracts, or the design-system transformer:

```bash
claude plugin validate plugins/design-motion-kit
claude plugin validate plugins/design-motion-kit/.claude-plugin/plugin.json
python plugins/design-motion-kit/.claude/scripts/validate_design_surfaces.py
python plugins/design-motion-kit/.claude/scripts/validate_motion_surfaces.py
python plugins/design-motion-kit/.claude/scripts/validate_design_library.py --expected-count 11
python plugins/design-motion-kit/.claude/scripts/validate_motion_library.py --expected-count 75
python plugins/design-motion-kit/.claude/scripts/validate_runtime_trends.py
python plugins/design-motion-kit/.claude/scripts/validate_design_pipeline.py
```

## Compatibility Policy

`motion-design-kit` and `web-design-kit` remain in the repo as deprecated compatibility packages for one release cycle. Do not add new features there.

**Last updated:** March 13, 2026
