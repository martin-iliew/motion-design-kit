# Cross-Skill Handoff Contracts

## Design Ownership

`design-build` and `design-upgrade` own:

- page context selection
- section ordering
- chosen design-library patterns
- token domain mapping
- component inventory
- motion readiness decisions

They must write:

- `brief/design-decision-pack.yaml`
- `brief/motion-hints.yaml`

## Motion Ownership

`motion-build` and `motion-upgrade` own:

- selecting motion-library patterns
- adapting motion to the detected stack
- reduced-motion and cleanup behavior
- honoring intensity and family limits from `motion-hints.yaml`

They must not:

- animate elements that are not present in the design decision pack
- choose motion families excluded by design hints
- introduce raw timing or easing values outside the token layer

## Code Ownership

The internal `design-coder` skill owns:

- translating the decision pack into clean React/Tailwind code
- using `brief/theme.css` and `brief/token-aliases.json`
- enforcing the no-raw-values rule
- keeping implementation aligned with existing components where possible
