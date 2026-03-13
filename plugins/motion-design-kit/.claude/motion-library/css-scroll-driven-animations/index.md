# CSS Scroll-Driven Animations

**Framework:** CSS
**Category:** scroll
**2026 Relevance:** Native CSS scroll-driven animations have reached broad browser support across Chromium and Safari, making JavaScript-based scroll watchers largely obsolete for common patterns. In 2026 this API is the standard approach for performant, declarative scroll-linked motion — no library required.

## Description

CSS Scroll-Driven Animations are a native browser API that links CSS `@keyframes` animations to the progress of a scroll gesture rather than to clock time. Instead of firing once at a fixed moment, the animation scrubs forward and backward in lock-step with the user's scroll position. The two core functions — `scroll()` and `view()` — provide two complementary models: `scroll()` maps animation progress to the total scrollable distance of a container, while `view()` maps it to how much of a specific element has entered or passed through the viewport.

This approach slots directly into the existing CSS animation system. You write a normal `@keyframes` block, then swap the default time-based timeline for a scroll-driven one by setting `animation-timeline: scroll()` or `animation-timeline: view()`. All the properties you already know — easing, fill modes, iteration count — continue to work exactly as before. The `animation-range` property gives you fine-grained control over which slice of the scroll journey triggers the animation, for example `animation-range: entry 0% entry 100%` to animate only while an element enters the viewport.

The feeling these animations create is one of physicality and user agency. Because the motion is directly coupled to the user's hand (or scroll wheel), the interface feels tangible and responsive rather than automated. Used with restraint — fading in sections, parallax depth, a reading-progress indicator — they reinforce spatial orientation and guide attention without demanding it.

## Do's

- Use `animation-range: entry 0% entry 100%` (or similar) to scope `view()` animations tightly to the element's viewport entry — this prevents mid-page elements from appearing half-animated on load.
- Always wrap scroll-driven animation declarations inside `@supports (animation-timeline: scroll())` so that unsupported browsers fall back gracefully without broken states.
- Prefer animating `transform`, `translate`, `scale`, `rotate`, and `opacity` — these run on the compositor thread and stay off the main thread, guaranteeing smooth 60 fps.
- Use named scroll timelines (`scroll-timeline-name: --my-timeline`) when you need a child element to track a specific ancestor scroller that is not its nearest scroll container.
- Test both mouse-scroll and touch-scroll on real devices; scroll velocity differs and can expose easing choices that feel unnatural.

## Don'ts

- Do not animate layout-triggering properties (`width`, `height`, `margin`, `top`) with scroll timelines — these force synchronous layout on the main thread and destroy performance.
- Do not assume Firefox support without a fallback; as of early 2026 Firefox has partial implementation behind a flag; always use `@supports` for progressive enhancement.
- Do not set a fixed `animation-duration` on scroll-driven animations — duration is controlled by scroll range, and a numeric duration value will conflict or be ignored.
- Do not rely on scroll-driven animations alone to convey critical information (e.g., a progress step that only reveals when scrolled to); content must be readable even when animations are disabled.
- Do not stack too many `view()` animations on a single page without profiling — while the animations themselves are cheap, the browser still needs to track each element's intersection state.

## Best Practices

**Accessibility and prefers-reduced-motion.** Always wrap scroll-driven animation declarations in a `@media (prefers-reduced-motion: no-preference)` block, or explicitly reset animations inside `@media (prefers-reduced-motion: reduce)`. Users who have enabled the reduced-motion system preference include people with vestibular disorders, migraines, or attention sensitivities; scroll-linked motion that moves continuously as the user scrolls can be particularly disorienting for them. The safest pattern is to set `opacity: 1` and `translate: 0 0` as defaults outside the `@supports` block, then layer animation on top — meaning users without support, or with reduced-motion enabled, always see fully visible, static content.

**Browser support and progressive enhancement.** As of March 2026, `animation-timeline: scroll()` and `view()` have full support in Chrome 115+, Edge 115+, Opera 101+, and Safari 18+. Firefox support remains behind a flag. The `@supports (animation-timeline: scroll())` guard is the correct progressive-enhancement boundary — browsers that do not support the property simply skip the block and render the baseline styles. For projects that require broader coverage, the `scroll-timeline` polyfill from the WICG can be loaded conditionally, but for most production use cases the native baseline is now sufficient to deploy without a polyfill.

**Performance benefits over JavaScript.** Traditional scroll-linked animations built with `window.addEventListener('scroll', ...)` run on the main thread, blocking during heavy script execution and causing jank. CSS scroll-driven animations that animate only `transform` and `opacity` are promoted to the compositor thread by the browser, running entirely outside the main thread. This eliminates layout thrashing, removes the need for `requestAnimationFrame` throttling, and maintains smooth animation even when JavaScript is executing expensive work. Replacing Intersection Observer + class-toggling patterns with native `view()` timelines also reduces code surface area and removes the need for cleanup on unmount in framework components.
