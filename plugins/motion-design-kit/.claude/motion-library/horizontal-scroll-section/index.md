# Horizontal Scroll Section

**Framework:** GSAP + ScrollTrigger
**Category:** scroll
**2026 Relevance:** Horizontal scroll sections have become a signature pattern for immersive storytelling, product showcases, and portfolio galleries. Pinning a container and scrolling its children horizontally while the user scrolls vertically creates a cinematic, deliberate pacing that breaks the monotony of vertical scrolling.

## Description

Pins a full-viewport section and translates its inner track horizontally as the user scrolls vertically. The scroll distance is proportional to the track width, creating a 1:1 feel between vertical scroll input and horizontal content movement. Each panel within the track can have its own entrance animation triggered by horizontal position.

## Do's

- Use `pin: true` with `scrub: 0.5` for smooth, scroll-tied horizontal movement
- Set `end: () => "+=" + (track.scrollWidth - container.offsetWidth)` dynamically so it adapts to content length
- Add `invalidateOnRefresh: true` to recalculate on resize
- Give the container `overflow: hidden` in CSS
- Respect `prefers-reduced-motion` — show all panels stacked vertically or in a scrollable overflow container

## Don'ts

- Don't use on mobile unless the horizontal content is short (3-4 panels max) — long horizontal scrolls feel broken on touch
- Don't nest horizontal scroll inside another pinned section — causes ScrollTrigger conflicts
- Don't animate layout properties on the panels — use `x`, `autoAlpha`, `scale` only
- Don't forget to clean up ScrollTriggers in SPAs — stale pins cause page height miscalculations
