# Custom Cursor Follower

**Framework:** GSAP
**Category:** cursor
**2026 Relevance:** Custom cursors have matured from a novelty into a mainstream branding and UX tool, with modern browsers providing reliable support and design systems increasingly treating them as a first-class interaction layer. In 2026, the expectation for premium web experiences includes cursors that morph, trail, and react contextually — turning every hover into a micro-interaction signal.

## Description

A Custom Cursor Follower replaces or augments the browser's default pointer with one or more DOM elements that track mouse movement with deliberate lag, creating a fluid trailing effect that feels tactile and alive. The primary "dot" snaps near-instantly to the real cursor position, while a larger "ring" or "blob" follows behind with a softer easing curve — the gap between the two creates the characteristic elastic, organic feel that defines the pattern.

Beyond pure aesthetics, the cursor becomes a live UI component. On hover over links, buttons, images, or cards it can scale up, blend-mode invert, change color, display a label, or morph shape entirely — giving users a visual preview of interactivity before they click. This removes ambiguity from dense layouts and rewards exploratory browsing, turning passive navigation into something closer to play.

The feeling this creates is one of tactile responsiveness and craft. When executed well, a cursor follower signals that every detail of an experience has been considered. It is a hallmark of agency portfolio sites, creative studios, luxury e-commerce, and editorial publications — anywhere the brand message centers on quality and attention to detail.

## Do's

- Use `gsap.quickTo()` for the `mousemove` handler — it pre-compiles the property setter and avoids the per-call overhead of `gsap.to()`, keeping frame time well under 1 ms even on mid-range devices.
- Set `will-change: transform` on cursor elements and animate only `x`/`y` (CSS `transform`) — never `top`/`left`, which force layout recalculation and cause jank.
- Apply `pointer-events: none` to both cursor elements so they never accidentally block clicks or hover events on the underlying content.
- Use `aria-hidden="true"` on cursor DOM elements so screen readers and assistive technology completely ignore them.
- Give the ring a noticeably longer `duration` than the dot (e.g. `0.15s` vs `0.5s`) — this asymmetry is what produces the satisfying elastic trail. Too similar and the effect reads as lag rather than personality.

## Don'ts

- Don't forget to restore the native cursor (`cursor: auto` or `cursor: pointer`) when `prefers-reduced-motion` is active or when a touch/coarse-pointer device is detected — failing to do so leaves users with an invisible cursor on systems where your custom element is hidden.
- Don't animate `width`, `height`, `border-radius`, or `opacity` inside the `mousemove` handler — reserve those for hover state transitions driven by `mouseenter`/`mouseleave`, so the move path stays purely GPU-composited `transform`.
- Don't hardcode element selectors at module initialisation — use event delegation or `MutationObserver` to catch dynamically injected interactive elements (React portals, SPA route changes, modal dialogs).
- Don't create multiple competing `mousemove` listeners from different components. Centralise cursor position updates in a single shared service or context provider; let other components only modify the cursor's visual state via CSS classes or data attributes.
- Don't skip the `mouseleave`/`mouseenter` window listeners. Without them the cursor element freezes in place when the user's pointer exits the viewport, creating a visual ghost that breaks immersion.

## Best Practices

Accessibility must be the first consideration, not an afterthought. Wrap all cursor logic inside `gsap.matchMedia()` with both `(hover: hover) and (pointer: fine)` and `(prefers-reduced-motion: reduce)` conditions. The `(hover: hover) and (pointer: fine)` media query reliably identifies true mouse devices and excludes touch screens, styluses on tablets, and game controllers. When either condition fails, GSAP automatically reverts all animations created inside that scope — no manual teardown code needed. Additionally, ensure the native cursor is never hidden via CSS until you have confirmed JavaScript has successfully initialised the replacement; a brief flash of the default cursor is far preferable to an invisible pointer.

Performance discipline is non-negotiable for a feature that fires on every mouse movement. The golden rule is: only `transform` and `opacity` inside animation calls during `mousemove`. Both properties are handled entirely by the GPU compositor thread without triggering layout or paint. If you need shape changes on hover (scaling, border-radius morph) drive them with CSS `transition` on the hover class, not a `gsap.to()` call inside the move handler. Profile with Chrome DevTools Performance tab and confirm that frame time stays under 4 ms at 120 Hz — most GSAP quickTo implementations land between 0.3–0.8 ms.

For framework integration, treat cursor state as a lightweight global store rather than per-component state. In React, expose a `CursorContext` that components can read to set cursor mode (`'default' | 'hover' | 'drag' | 'hidden'`); a single `useEffect` in the cursor component responds to mode changes with GSAP tweens. In Vue, a composable (`useCursor`) follows the same pattern. Always initialize the cursor component at the app root (outside router views) so it persists across page transitions, and pair it with GSAP's `gsap.context()` for clean disposal on unmount. For SPA route changes, tween the cursor to `autoAlpha: 0` at the start of a page transition and back to `1` once the new page is fully mounted — this prevents the cursor element from awkwardly sitting over an animating layout.
