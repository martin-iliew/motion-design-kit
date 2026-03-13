# Validation

## Design Validation

Before stopping a `design-build` or `design-upgrade` run:

- required brief bundle files exist
- `brief/theme.css` was generated from DTCG
- `brief/token-aliases.json` exists
- `brief/design-decision-pack.yaml` exists
- `brief/motion-hints.yaml` exists
- every selected design pattern exists in `.claude/design-library`
- generated code uses token aliases or CSS variables instead of raw values

## Motion Validation

Before stopping a `motion-build` or `motion-upgrade` run:

- consume `brief/design-decision-pack.yaml` when present
- consume `brief/motion-hints.yaml` when present
- every selected motion pattern exists in `.claude/motion-library`
- allowed families and intensities are respected
- reduced-motion and cleanup requirements are satisfied for the detected stack

## Library Validation

Maintainer checks live in `.claude/scripts/` and should be run after changing:

- plugin surfaces
- design-library contracts
- motion-library contracts
- DTCG transformation logic
