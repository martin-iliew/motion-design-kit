# Magnetic Cursor Pull Effect

**Framework:** GSAP
**Category:** cursor
**2026 Relevance:** As websites compete for deeper engagement, the magnetic cursor pull effect has become a defining micro-interaction of 2026 — transforming passive pointer movement into a tactile, elastic experience that signals interactivity before a click ever occurs. It is now a standard expectation on award-winning and portfolio sites, and increasingly adopted in product marketing pages seeking to communicate premium quality.

## Description

The Magnetic Cursor Pull Effect makes interactive elements — buttons, links, icons, nav items — appear to exert a gravitational field around themselves. When the user's cursor enters a defined radius, the element smoothly deforms toward the pointer using `x`/`y` transforms driven by GSAP. The element snaps back with elastic easing once the cursor leaves, giving the interaction a satisfying, springy quality that reads as physical and alive.

In practice the effect is achieved by listening to `mousemove` on each magnetic element, calculating the offset of the cursor from the element's center, scaling that offset by a strength multiplier (typically 0.3–0.6), and feeding the result into a `gsap.to()` call targeting `x` and `y`. On `mouseleave`, a separate tween returns both properties to zero using an elastic or back ease. The inner content — such as a label or icon — often receives an additional, subtler transform to create a parallax depth layer within the button itself.

The feeling this creates is one of direct manipulation and responsiveness. Users instinctively associate elastic, physics-like feedback with high craftsmanship. When implemented with restraint it guides attention without demanding it, reinforcing affordance and making clickable elements feel genuinely inviting rather than merely styled.

## Do's

- **Use `x` and `y` GSAP properties exclusively** — they map to `translateX`/`translateY` which are composited on the GPU and never trigger layout recalculation.
- **Apply `overwrite: "auto"`** on every `gsap.to()` call targeting the same element so rapidly repeated `mousemove` events do not stack competing tweens and cause stuttering.
- **Tune strength per element size** — larger buttons tolerate a strength of 0.5–0.6; small icon links should stay at 0.2–0.3 to avoid feeling chaotic.
- **Add a distance threshold** (`maxDist`) so the pull only activates within a defined proximity zone, preventing jitter as the user moves across the page.
- **Wrap all effect logic inside `gsap.matchMedia()`** to cleanly scope and automatically revert animations for users who prefer reduced motion, without manual media-query listeners.

## Don'ts

- **Never animate `left`, `top`, `margin`, or `padding`** to achieve the pull movement — these trigger synchronous layout recalculation on every frame, causing jank even on high-end hardware.
- **Don't attach `mousemove` to `document` or `window`** for per-element magnetic effects — scope the listener to the element itself or its nearest container to avoid unnecessary per-frame calculations across the entire page.
- **Avoid `will-change: transform` set permanently in CSS** — add it dynamically on `mouseenter` and remove it on the elastic snap-back completion to prevent the browser from maintaining expensive compositor layers for offscreen elements.
- **Don't skip the `mouseleave` snap-back** — without it, elements remain displaced when the cursor exits, breaking layout flow visually and confusing keyboard-only users who tab past the element.
- **Don't use overly aggressive elastic easing (e.g., amplitude > 1.5)** on the snap-back — it can cause elements to clip overflow bounds or overlap adjacent content, especially in tightly spaced navigation rows.

## Best Practices

**Accessibility and `prefers-reduced-motion`:** The magnetic cursor pull effect is inherently motion-heavy — it fires on every `mousemove` event and produces continuous position changes. Always gate the full implementation behind GSAP's `gsap.matchMedia()` with the `(prefers-reduced-motion: no-preference)` condition. The `matchMedia` API in GSAP 3.11+ automatically reverts registered effects and removes event listeners when the media condition changes at runtime (for example, when a user toggles their OS setting mid-session). For a belt-and-suspenders approach, consider also exposing a UI toggle that adds a `data-reduce-motion` attribute to `<html>`, which your GSAP contexts can read as an additional condition. Remember that touch and pointer devices without a persistent hover state (tablets, mobile) should not receive these listeners at all — guard with `window.matchMedia("(hover: hover) and (pointer: fine)")`.

**Performance and GPU-safe properties:** GSAP already applies `force3D: "auto"` by default, promoting animated elements to their own compositor layer via `translate3d()` during active tweens and then dropping back to 2D at rest to conserve GPU memory. Always prefer animating `x`, `y`, `scale`, and `rotation` (GSAP's shorthand transform properties) over any box-model property. If you need to animate more than 20–30 magnetic elements simultaneously — for example a grid of cards — consider throttling the `mousemove` handler with `gsap.ticker` rather than the raw DOM event, since `gsap.ticker` fires in sync with the browser's render loop and naturally coalesces rapid pointer events. Use `gsap.quickTo()` (introduced in GSAP 3.10) as a drop-in upgrade for the `gsap.to()` calls inside `mousemove` — `quickTo` creates a pre-configured setter function with zero object allocation overhead on each call, measurably reducing main-thread pressure in pointer-heavy animations.

**Integration tips:** When combining the magnetic effect with a custom cursor (a common 2026 pattern), ensure the magnetic element moves independently of the cursor element to preserve the visual illusion of attraction — if both move toward the same point simultaneously the effect is lost. For React or Vue projects, initialize the effect inside a `useEffect` / `onMounted` hook and store the `gsap.matchMedia()` context in a ref so you can call `ctx.revert()` on component unmount to prevent listener leaks. In Webflow or other CMS environments where GSAP is loaded globally, use `document.querySelectorAll(".mag-btn")` inside a `DOMContentLoaded` listener and consider using GSAP's `ScrollTrigger.refresh()` after any dynamic content injection that changes element positions, since `getBoundingClientRect()` relies on current layout state.
