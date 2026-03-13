# Circular Text Orbit Scroll

**Framework:** GSAP
**Category:** typography
**2026 Relevance:** Current in March 2026 because it is appearing in premium GSAP-heavy builds without becoming a default trope yet.

## Description

Circular Text Orbit Scroll is a GSAP pattern for text surfaces that moves an accent or
media element along a defined path.

marketing launches, portfolio storytelling, creative showcase pages that need clearer
motion hierarchy across text surfaces.

## Do's

- Keep reduced-motion behavior explicit and leave the static end state readable immediately.
- Scope selectors to the local section or component rather than targeting the whole page.
- Prefer transform and autoAlpha changes over layout-triggering properties.

## Don'ts

- Do not stack the same effect on every similar surface in the viewport.
- Do not leave decorative motion running without checking touch and reduced-motion behavior.
- Do not convert a state-change pattern into ambient motion just because the effect looks good.

## Best Practices

Editorial and legible; the flourish should resolve into readable type quickly.

Long-form body copy, dense instructional text, or layouts already carrying multiple text
treatments.

Use the pattern folder's spec and snippet as the primary implementation source. Only fall back to shared GSAP references when the page needs extra composition beyond this pattern's contract.
