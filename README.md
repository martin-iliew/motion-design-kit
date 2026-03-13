# design-motion-kit

Canonical Claude Code plugin for merged design and motion work.

It combines:

- a non-code `design-library`
- the existing `motion-library`
- mirrored public command families
- a DTCG JSON to Tailwind v4 `@theme` pipeline
- internal designer, coder, and greenfield bootstrap skills
- vendored Anthropic reference skills under `plugins/design-motion-kit/.claude/skills/vendor/anthropic/`

## Install

```bash
claude plugin marketplace add --scope user martin-iliew/design-motion-kit
claude plugin install --scope user design-motion-kit@design-motion-kit
```

## Public Commands

Design:

- `/design-build`
- `/design-upgrade`
- `/design-audit`
- `/design-discover`
- `/design-refresh`

Motion:

- `/motion-build`
- `/motion-upgrade`
- `/motion-audit`
- `/motion-discover`
- `/motion-refresh`

`/design-build`, `/design-upgrade`, `/motion-build`, and `/motion-upgrade` support `mode: fast|balanced|premium`. Default is `balanced`.

## Brief Bundle Contract

Upstream scraper output is expected in `brief/`:

- `brief/brief.json`
- `brief/copy.md`
- `brief/images.json`
- `brief/tokens.dtcg.json`

Design workflows generate:

- `brief/theme.css`
- `brief/token-aliases.json`
- `brief/design-decision-pack.yaml`
- `brief/motion-hints.yaml`

Motion workflows consume the decision pack and motion hints when they exist.

## Maintainer Validation

```bash
claude plugin validate plugins/design-motion-kit
claude plugin validate plugins/design-motion-kit/.claude-plugin/plugin.json
python plugins/design-motion-kit/.claude/scripts/validate_design_surfaces.py
python plugins/design-motion-kit/.claude/scripts/validate_motion_surfaces.py
python plugins/design-motion-kit/.claude/scripts/validate_design_library.py --expected-count 11
python plugins/design-motion-kit/.claude/scripts/validate_motion_library.py --expected-count 75
python plugins/design-motion-kit/.claude/scripts/validate_design_pipeline.py
```

## Compatibility Packages

The following packages remain in the repo for one release cycle only:

- `motion-design-kit`
- `web-design-kit`

They are documentation-led compatibility paths. All new development belongs in `plugins/design-motion-kit`.

**Last updated:** March 13, 2026
