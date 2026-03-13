# Zoom Out Hero Exit

**Framework:** GSAP
**Category:** scroll
**2026 Relevance:** Still active in March 2026 because it maps cleanly to current GSAP patterns and interface expectations.

## Description

Zoom Out Hero Exit is a GSAP pattern for hero surfaces that scrubs transform-led motion
against scroll without breaking layout.

marketing launches, portfolio storytelling, creative showcase pages that need clearer
motion hierarchy across hero surfaces.

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

Low-value surfaces where the effect would add novelty but not clarity.

Use the pattern folder's spec and snippet as the primary implementation source. Only fall back to shared GSAP references when the page needs extra composition beyond this pattern's contract.
