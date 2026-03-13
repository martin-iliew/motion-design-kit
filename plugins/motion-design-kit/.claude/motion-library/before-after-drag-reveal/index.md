# Before After Drag Reveal

**Framework:** GSAP
**Category:** micro-interaction
**2026 Relevance:** Still active in March 2026 because it maps cleanly to current GSAP patterns and interface expectations.

## Description

Before After Drag Reveal is a GSAP pattern for gallery, carousel surfaces that lets a
draggable handle reveal two media states inside one frame.

portfolio storytelling, ecommerce conversion surfaces, creative showcase pages that need
clearer motion hierarchy across gallery, carousel surfaces.

## Do's

- Keep reduced-motion behavior explicit and leave the static end state readable immediately.
- Scope selectors to the local section or component rather than targeting the whole page.
- Prefer transform and autoAlpha changes over layout-triggering properties.

## Don'ts

- Do not stack the same effect on every similar surface in the viewport.
- Do not leave decorative motion running without checking touch and reduced-motion behavior.
- Do not convert a state-change pattern into ambient motion just because the effect looks good.

## Best Practices

Direct-manipulation first; the motion should feel physical without fighting the user.

Critical data surfaces or any flow where accidental drag would hurt basic usability.

Use the pattern folder's spec and snippet as the primary implementation source. Only fall back to shared GSAP references when the page needs extra composition beyond this pattern's contract.
