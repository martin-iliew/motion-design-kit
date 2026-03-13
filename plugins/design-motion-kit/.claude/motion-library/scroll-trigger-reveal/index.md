# ScrollTrigger Reveal Animations

**Framework:** GSAP
**Category:** scroll
**2026 Relevance:** Scroll-driven reveal animations remain the dominant motion pattern in modern web design, with GSAP ScrollTrigger establishing itself as the de-facto standard for performance-grade, accessible implementations. As CSS Scroll-Driven Animations gain traction but remain limited in browser support and expressiveness, GSAP ScrollTrigger continues to be the production choice for teams requiring fine-grained control, stagger sequencing, and robust accessibility tooling.

## Description

ScrollTrigger reveal animations are entrance effects that fire when an element scrolls into the viewport — typically animating opacity from 0 to 1 combined with a translate or scale transform. The pattern transforms static pages into guided visual narratives, directing user attention sequentially as content becomes visible. In 2026, the technique has matured well beyond simple fade-ins: staggered card grids, clip-path reveals, SplitText character cascades, and scrubbed timeline storytelling are all canonical ScrollTrigger patterns deployed at production scale.

The core architecture involves attaching a `scrollTrigger` configuration object directly to a GSAP tween or timeline, declaring a `trigger` element, `start`/`end` scroll positions, and `toggleActions` that control play/pause/reverse behavior. For pages with many repeating elements — feature grids, testimonial cards, blog listings — `ScrollTrigger.batch()` provides a performance-optimized path that groups multiple element triggers into a single scroll listener, preventing the overhead of hundreds of individual `IntersectionObserver`-equivalent calculations.

Integration with smooth-scroll libraries like Lenis has become a standard pairing in 2026 agency and product work. Lenis provides momentum-based scroll inertia, while ScrollTrigger handles the animation logic. Synchronization is achieved by piping Lenis scroll events into `ScrollTrigger.update()` and adding the Lenis RAF loop to GSAP's ticker — a well-documented pattern that eliminates micro-stutters that arise when two independent scroll systems compete for the same frame budget. When building with React, Next.js, or Astro, scoping all ScrollTrigger instances inside `gsap.context()` and reverting the context on component unmount is essential to prevent memory leaks and stale trigger positions across route transitions.

## Do's

- Always call `gsap.registerPlugin(ScrollTrigger)` once at the module level before any tween or trigger is created.
- Wrap all animation code in `gsap.matchMedia()` with a `(prefers-reduced-motion: no-preference)` condition, and provide a `gsap.set()` fallback for the `reduce` branch.
- Use `ScrollTrigger.batch()` when revealing 10 or more repeating elements — it consolidates scroll listeners and dramatically reduces layout thrashing compared to individual triggers per element.
- Set `invalidateOnRefresh: true` on pinned or viewport-dependent ScrollTriggers so measurements recalculate correctly after browser resize.
- Scope all ScrollTrigger instances inside `gsap.context()` when working in component-based frameworks (React, Vue, Astro), and call `ctx.revert()` on unmount to prevent ghost triggers.

## Don'ts

- Do not animate layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`) — always animate `x`, `y`, `scale`, `rotation`, and `opacity` to keep compositing on the GPU and avoid forced reflows.
- Do not mix CSS `transition` and GSAP tweens on the same property on the same element — both systems will fight over the value, causing visual jitter.
- Do not create ScrollTriggers outside of a cleanup-aware context in SPAs; stale triggers from unmounted components persist in memory, accumulate across navigations, and fire against detached DOM nodes.
- Do not set overly aggressive `start` values like `"top 100%"` — triggers that fire the moment an element enters the very bottom pixel of the viewport cause animations to begin before users visually register the element.
- Do not rely on `ScrollTrigger.refresh()` as a catch-all fix for wrong positions — diagnose the root cause (usually font loading, image loading, or dynamic content insertion before triggers initialize) and use `ScrollTrigger.refresh()` after those async operations complete explicitly.

## Best Practices

Accessibility is non-negotiable in 2026: vestibular disorders affect a significant percentage of users, and the `prefers-reduced-motion: reduce` OS setting is their primary mitigation tool. The `gsap.matchMedia()` API is the correct GSAP-native mechanism — it automatically reverts all animations and kills all ScrollTriggers registered within a `no-preference` block when the media query stops matching (e.g., when a user toggles the OS setting at runtime). The `reduce` branch should always call `gsap.set()` to ensure every animated element reaches its final visible state immediately, preventing invisible content for users who never receive the entrance animation.

For performance, the key discipline is limiting what ScrollTrigger has to measure. Call `ScrollTrigger.refresh()` only once after all page content (images, fonts, dynamic data) has fully loaded — not repeatedly in response to resize events, which GSAP handles internally. When building scroll reveals for long-feed pages (news, e-commerce listings), use `ScrollTrigger.batch()` with conservative `start` values around `"top 88%"` so animations trigger with comfortable visual margin. Avoid creating one trigger per element in a loop: the batch pattern is 3–5× more efficient for element counts above 20. Additionally, keep animation durations between 0.5s and 1.0s; anything longer creates the perception of sluggishness and delays user interaction with just-revealed content.

For framework integration, the `gsap.context()` scoping API is the correct solution for React and Vue component lifecycles — it automatically tracks all GSAP animations and ScrollTriggers created within its callback and reverts them all with a single `ctx.revert()` call on unmount. When using route-transition libraries (Barba.js, Astro View Transitions, Next.js App Router), kill all ScrollTriggers in the route-leave hook via `ScrollTrigger.getAll().forEach(t => t.kill())` before the new page mounts, then re-initialize fresh instances after the new DOM is in place. When pairing with Lenis, always disable GSAP's built-in lag smoothing with `gsap.ticker.lagSmoothing(0)` — Lenis owns the smoothing layer, and GSAP's competing smoothing will cause double-interpolation and visual drift.
