# Observer Section Slider

**Framework:** GSAP
**Category:** scroll
**2026 Relevance:** Current in March 2026 because it is appearing in premium GSAP-heavy builds without becoming a default trope yet.

## Description

Observer Section Slider is a GSAP pattern for section surfaces that turns section
changes into an Observer-driven presentation flow.

marketing launches, portfolio storytelling, creative showcase pages that need clearer
motion hierarchy across section surfaces.

## Do's

- Keep reduced-motion behavior explicit and leave the static end state readable immediately.
- Scope selectors to the local section or component rather than targeting the whole page.
- Prefer transform and autoAlpha changes over layout-triggering properties.

## Don'ts

- Do not stack the same effect on every similar surface in the viewport.
- Do not leave decorative motion running without checking touch and reduced-motion behavior.
- Do not convert a state-change pattern into ambient motion just because the effect looks good.

## Best Practices

Deliberate and lightweight; the motion should add hierarchy before it adds spectacle.

Dense utility pages, long legal copy, or contexts where native scrolling must stay
untouched.

Use the pattern folder's spec and snippet as the primary implementation source. Only fall back to shared GSAP references when the page needs extra composition beyond this pattern's contract.
