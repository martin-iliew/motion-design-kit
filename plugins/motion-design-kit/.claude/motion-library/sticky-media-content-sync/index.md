# Sticky Media Content Sync

**Framework:** GSAP
**Category:** scroll
**2026 Relevance:** Still active in March 2026 because it maps cleanly to current GSAP patterns and interface expectations.

## Description

Sticky Media Content Sync is a GSAP pattern for timeline, section, media surfaces that
pins a sequence and hands focus from one beat to the next as the user scrolls.

portfolio storytelling, ecommerce conversion surfaces, creative showcase pages that need
clearer motion hierarchy across timeline, section, media surfaces.

## Do's

- Keep reduced-motion behavior explicit and leave the static end state readable immediately.
- Scope selectors to the local section or component rather than targeting the whole page.
- Prefer transform and autoAlpha changes over layout-triggering properties.

## Don'ts

- Do not stack the same effect on every similar surface in the viewport.
- Do not leave decorative motion running without checking touch and reduced-motion behavior.
- Do not convert a state-change pattern into ambient motion just because the effect looks good.

## Best Practices

Scroll-coupled and intentional; the motion should track reading pace instead of
hijacking it.

Dense utility pages, long legal copy, or contexts where native scrolling must stay
untouched.

Use the pattern folder's spec and snippet as the primary implementation source. Only fall back to shared GSAP references when the page needs extra composition beyond this pattern's contract.
