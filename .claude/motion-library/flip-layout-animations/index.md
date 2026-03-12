# FLIP Layout Animations

**Framework:** GSAP
**Category:** transition
**2026 Relevance:** As CSS-native view transitions mature, GSAP's Flip plugin remains the production standard for cross-browser, framework-agnostic shared-element and layout-change animations — particularly in React/Vue SPAs where DOM mutations from state changes would otherwise cause jarring jumps. Responsive grid reflows, filtering/sorting interfaces, and card expansion patterns are among the most common interaction paradigms of 2026, and Flip handles all of them with a consistent, declarative API.

## Description

The FLIP technique — coined by Google engineer Paul Lewis — is a performance pattern that sidesteps the browser's expensive layout recalculation pipeline by converting positional changes into GPU-composited `transform` and `opacity` animations. The four stages are: **First** (record where elements are now), **Last** (apply the DOM/class change that moves them), **Invert** (instantly offset each element back to its recorded position so it *appears* unchanged), and **Play** (animate the removal of those offsets). Because only `transform` is animated, no reflow occurs during playback — the browser never recalculates layout after the initial DOM mutation.

GSAP's Flip plugin automates the entire FLIP pipeline behind two calls: `Flip.getState()` captures position, size, rotation, and skew for every matched element before you mutate the DOM, and `Flip.from()` performs the invert-and-play steps automatically, returning a standard GSAP timeline you can sequence, pause, or reverse like any other animation. Elements are correlated between states via a `data-flip-id` attribute — either set manually for predictable shared-element transitions, or auto-assigned by the plugin. This makes the technique trivially composable with existing GSAP timelines, ScrollTrigger sequences, and stagger patterns.

In 2026 the most prevalent use cases are: filter/sort-and-reflow grids (where CSS Grid column count changes), expanding list items into full-screen detail views (shared-element hero transitions without the Page Transitions API), and drag-and-drop list reordering. The `absolute: true` option is essential for flex/grid containers — it briefly takes elements out of flow during the animation so sibling elements do not snap to their final positions mid-flight. The `nested: true` option is required when both a parent and its children are in the state capture to prevent double-counting transforms from ancestor elements.

## Do's

- Always call `Flip.getState()` **immediately before** the DOM/class mutation — any delay between capture and mutation introduces drift because the browser may have already reflowed.
- Use `absolute: true` when flipping items inside CSS flex or grid containers so siblings animate to their new positions independently rather than snapping.
- Assign stable `data-flip-id` attributes to elements involved in shared-element transitions (e.g., a card expanding into a detail panel) so Flip can reliably correlate the two states across re-renders.
- Wrap all Flip calls in `gsap.matchMedia()` with a `(prefers-reduced-motion: no-preference)` condition and provide an instant fallback in the `(prefers-reduced-motion: reduce)` branch.
- In React, use `contextSafe()` from `useGSAP` for any Flip calls triggered by event handlers or state changes — this ensures the resulting tweens are registered in the current GSAP context and cleaned up on unmount.

## Don'ts

- Do not call `Flip.getState()` and `Flip.from()` across an `async` boundary (e.g., after an `await` or `setTimeout`) — the DOM may have already changed, causing Flip to invert against stale coordinates.
- Do not animate layout-triggering CSS properties (e.g., `width`, `height`, `top`, `left`, `margin`) with `gsap.to()` directly alongside a Flip animation on the same elements — competing transform owners will produce jittery results.
- Do not omit `nested: true` when a parent and one or more of its children are both included in the same `Flip.getState()` call; without it, child transforms are double-counted against the parent's movement.
- Do not set CSS `transition` on any property that Flip animates (`transform`, `opacity`) — browser transitions and GSAP tweens will fight each other, creating unpredictable timing.
- Do not reuse a saved state snapshot; call `Flip.getState()` fresh for every interaction, as a stale snapshot reflects outdated coordinates and produces incorrect inversions.

## Best Practices

**Accessibility.** The prefers-reduced-motion media query is non-negotiable for layout animations — large positional changes can trigger vestibular disorders and motion sickness. The `gsap.matchMedia()` pattern is the cleanest implementation: all Flip logic lives in the `no-preference` branch, while the `reduce` branch applies instant `gsap.set()` calls to finalize state without interpolation. Beyond motion, ensure interactive trigger elements (cards, filter buttons) are keyboard-accessible — add `tabindex="0"` and keydown listeners for Enter/Space on non-semantic elements, or prefer wrapping content in `<button>` elements natively. ARIA live regions (`aria-live="polite"`) should announce filter result counts after a grid reflow so screen reader users know how many items are displayed.

**Performance.** Because Flip only animates `transform` and `opacity`, it stays entirely on the GPU compositor thread after the initial DOM mutation. The `prune: true` option on `Flip.from()` tells the plugin to silently skip elements whose recorded and final states are identical, eliminating unnecessary tweens when only a subset of items move. For very large grids (50+ cards), consider batching `Flip.getState()` to a subset of visible elements using `ScrollTrigger.batch()` patterns rather than capturing the entire DOM subtree. Avoid capturing state on elements inside a CSS `will-change: transform` container — the composited layer causes coordinate discrepancies.

**React and component cleanup.** The `@gsap/react` package's `useGSAP()` hook is the recommended integration point; it creates a `gsap.context()` scoped to a container ref and calls `ctx.revert()` automatically on unmount, which also kills any active Flip timelines. For Flip animations triggered by state changes (where React re-renders the DOM before your handler resumes), the reliable pattern is to capture state synchronously, update React state, then schedule `Flip.from()` inside `requestAnimationFrame()` so it runs after React's commit phase. Avoid calling `Flip.getState()` inside `useEffect()` — by the time the effect fires, React has already committed the new DOM and the "First" state is lost. Always use `useLayoutEffect()` (or `useGSAP()`) to capture state synchronously after paint but before the browser composites the frame.
