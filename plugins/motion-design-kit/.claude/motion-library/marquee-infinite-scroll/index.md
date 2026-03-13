# Marquee / Infinite Scroll Text

**Framework:** GSAP (or CSS-only for simple cases)
**Category:** ambient
**2026 Relevance:** Horizontal text and logo loops are ubiquitous on modern marketing sites, agency portfolios, and SaaS landing pages. The pattern provides ambient motion that fills visual weight without demanding user attention. GSAP's `modifiers` plugin enables seamless infinite loops with speed control impossible in pure CSS.

## Description

A continuous horizontal scrolling strip of text, logos, or icons that loops infinitely. The content is duplicated in the DOM so the loop appears seamless — when the first copy scrolls fully off-screen, it wraps back to the start position. Used for partner logo strips, testimonial tickers, award badges, or decorative kinetic typography.

## Do's

- Duplicate the track content in JS (not manually in HTML) to ensure the loop is seamless
- Use `gsap.utils.unitize()` with modifiers for true infinite looping without timeline restarts
- Add `aria-hidden="true"` to the duplicated content to prevent screen readers from reading it twice
- Respect `prefers-reduced-motion` — show content statically without scrolling
- Use `ease: "none"` (linear) for constant-speed scrolling

## Don'ts

- Don't use CSS `marquee` tag or `animation: marquee` with `translateX(-100%)` — it creates a visible gap at the loop point
- Don't animate at high speeds (>100px/s) — it becomes distracting and reduces readability
- Don't use on mobile if the content is important for comprehension — small screens make scrolling text hard to read
- Don't add scroll-driven behavior — marquees should be ambient and independent of scroll position
