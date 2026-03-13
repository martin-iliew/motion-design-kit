# Motion Design Kit Setup

Setup and maintainer guide for `motion-design-kit`.

---

## Install

Install at user scope:

```bash
claude plugin marketplace add --scope user martin-iliew/motion-design-kit
claude plugin install --scope user motion-design-kit@motion-design-kit
```

Inside Claude Code, the slash-command equivalent is:

```bash
/plugin marketplace add martin-iliew/motion-design-kit
/plugin install motion-design-kit@motion-design-kit
```

---

## Project Permissions Profile

In the app repo Claude will edit, create `.claude/settings.json` with this profile:

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

This is the same profile stored in [`.claude/settings.json`](./.claude/settings.json).

---

## Canonical Runtime Model

The only public command surface is:

- `/motion-build`
- `/motion-upgrade`
- `/motion-audit`
- `/motion-discover`
- `/motion-refresh`

`/motion-build` and `/motion-upgrade` support an optional leading mode prefix:

- `mode: fast`
- `mode: balanced`
- `mode: premium`

Default mode is `balanced`.

`.claude` is the source of truth for:

- skill behavior
- runtime selector logic
- execution modes
- guardrails
- output contracts

`.agents` exists only for local compatibility wrappers.

---

## Validation

Run before publishing or after changing commands, skills, or runtime data:

```bash
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
python .claude/scripts/validate_motion_surfaces.py
python .claude/scripts/validate_motion_library.py --expected-count 75
python .claude/scripts/validate_runtime_trends.py
```

---

## Library Maintenance

Use:

- `/motion-discover` to add new pattern folders and `catalog.yaml` entries
- `/motion-refresh` to rescore the catalog and regenerate:
  - `scores.yaml`
  - `site-baselines.yaml`
  - `trend-watchlist.yaml`

Normal `motion-build` and `motion-upgrade` runs should consume the compiled runtime layer. They should not do live trend research.

---

## Eval Maintenance

Keep evaluation metadata aligned with the canonical surface and maintain mode-aware examples in build and upgrade coverage.

If benchmark artifacts are regenerated, keep the labels aligned with the canonical names and mode coverage.

**Last updated:** March 2026
