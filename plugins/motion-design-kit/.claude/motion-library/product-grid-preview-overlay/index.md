# Product Grid Preview Overlay

**Framework:** GSAP
**Category:** micro-interaction
**2026 Relevance:** Still active in March 2026 because it maps cleanly to current GSAP patterns and interface expectations.

## Description

Product Grid Preview Overlay is a GSAP pattern for grid, card surfaces that stages a
panel or overlay with coordinated depth and stagger.

portfolio storytelling, ecommerce conversion surfaces, creative showcase pages that need
clearer motion hierarchy across grid, card surfaces.

## Do's

- Keep reduced-motion behavior explicit and leave the static end state readable immediately.
- Scope selectors to the local section or component rather than targeting the whole page.
- Prefer transform and autoAlpha changes over layout-triggering properties.

## Don'ts

- Do not stack the same effect on every similar surface in the viewport.
- Do not leave decorative motion running without checking touch and reduced-motion behavior.
- Do not convert a state-change pattern into ambient motion just because the effect looks good.

## Best Practices

State-driven and tactile; movement should confirm the change in one controlled beat.

Low-value surfaces where the effect would add novelty but not clarity.

Use the pattern folder's spec and snippet as the primary implementation source. Only fall back to shared GSAP references when the page needs extra composition beyond this pattern's contract.
