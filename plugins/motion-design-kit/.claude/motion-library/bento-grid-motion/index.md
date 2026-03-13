# Bento Grid Motion

**Framework:** CSS | GSAP
**Category:** micro-interaction
**2026 Relevance:** Bento grid layouts have become the dominant product-showcase pattern of 2025–2026, and motion is now the expected differentiator — static grids read as unfinished. The shift to "Bento 2.0" means interactive lift, expand, and reveal behaviours are a baseline expectation, not an enhancement.

## Description

Bento Grid Motion is the practice of adding coordinated, physics-aware micro-interactions to CSS grid-based "bento" card layouts — those puzzle-piece arrangements of differently-sized tiles popularised by Apple and now ubiquitous in SaaS landing pages, portfolios, and dashboards. Each card responds to hover with a layered animation sequence: a vertical lift driven by `translateY`, a subtle scale increase, and a shadow that deepens to create perceived elevation off the page. When a card expands (either via hover or click), its siblings gracefully yield space through GSAP Flip or CSS grid column/row transitions, making the entire grid feel like a single living surface rather than a collection of isolated boxes.

The pattern fits squarely into the micro-interaction category because each animation is scoped to a discrete user gesture — there is no ambient looping or auto-play motion. This makes the technique respectful of user attention and straightforward to guard with `prefers-reduced-motion`. The visual vocabulary borrows from Material Design's elevation system: shadows grow more diffuse and offset as cards "rise," reinforcing spatial metaphor without resorting to 3D transforms that can feel gimmicky or cause compositing issues on lower-end hardware.

The feeling produced is one of tactile responsiveness — the interface behaves as though cards have physical weight and can be picked up. When done well with carefully tuned easing curves (cubic-bezier ease-out on enter, relaxed ease-in-out on exit), the grid reads as calm and considered rather than flashy. This makes Bento Grid Motion especially effective for trust-building contexts: product feature showcases, pricing grids, portfolio pieces, and data dashboard widgets where the user needs to feel in control.

## Do's

- Animate only `transform` and `opacity` for hover states — these are the only CSS properties the browser can handle on the compositor thread without triggering layout or paint, guaranteeing smooth 60 fps on mid-range devices.
- Use a slightly springy cubic-bezier (e.g. `cubic-bezier(0.34, 1.56, 0.64, 1)`) for the enter state and a softer ease-in-out for exit — the asymmetry makes interactions feel physically plausible and alive.
- Use GSAP Flip for any expand/collapse interaction that causes the grid to reflow; Flip captures the DOM before and after, then animates the delta, completely avoiding the jarring snap that raw CSS grid transitions produce.
- Apply `will-change: transform` to cards sparingly and only while interaction is likely — you can add and remove it on `mouseenter`/`mouseleave` in JS to avoid wasting GPU memory on the full grid simultaneously.
- Guard every animation block with a `prefers-reduced-motion: reduce` media query and a matching JavaScript `window.matchMedia` check so that users with vestibular disorders receive a functional, non-animated experience.

## Don'ts

- Do not animate `box-shadow` directly in high-frequency interactions — it triggers a repaint on every frame. Fake the shadow change by animating the `opacity` of a `::after` pseudo-element, or accept a single transition at the transition end for low-frequency hover states.
- Do not apply `will-change: transform` to every card in the grid at page load — this promotes all elements to separate GPU layers simultaneously, consuming memory and potentially degrading performance on the very devices you're trying to optimise for.
- Do not rely on `:hover` alone for expanded/active states — touch devices have no hover, so interactive cards need a separate tap/click handler; omitting it produces a broken experience for mobile users who represent the majority of traffic on many sites.
- Do not skip `focus-visible` styles — keyboard users navigating bento grids need a clear focus indicator; removing the outline without a replacement violates WCAG 2.4.7 (Focus Visible) and the European Accessibility Act, which became enforceable in mid-2025.
- Do not set easing curves to `linear` or `ease-in` for lift animations — they read as mechanical and cheap; always use ease-out or a spring curve on enter so the motion decelerates naturally, as if the card has mass.

## Best Practices

Accessibility must be designed in from the start, not bolted on. The `prefers-reduced-motion: reduce` media query should wrap every animated CSS rule that produces spatial displacement — translates, scales, and fly-ins — with a `transform: none` or a simplified cross-fade replacement. Critically, the same check must be replicated in JavaScript for GSAP-driven animations: `window.matchMedia("(prefers-reduced-motion: reduce)").matches` should short-circuit timeline playback before `gsap.to()` is called. Providing an alternative is not about removing polish — a shadow depth change or a gentle opacity shift is still perceived as a response without inducing discomfort in users with vestibular disorders. As of 2026, meeting WCAG 2.2 and the European Accessibility Act for motion is a legal baseline for sites targeting EU users, not an optional nicety.

Performance on the compositor is the single most important technical constraint. Bento grids can easily have 6–12 simultaneously hoverable cards; if each hover triggers a layout or paint operation, frame drops compound quickly. The golden rule is: `transform` and `opacity` only during animation. Shadow depth is the most common trap — `box-shadow` changes cause repaints on every interpolated frame. The recommended workaround is to pre-render the elevated shadow state as a `::after` pseudo-element at full opacity during normal state and animate only its `opacity` to `0` at rest and `1` on hover. This isolates the shadow change to the composite step. Reserve `will-change: transform` as a surgical tool, adding it on `mouseenter` and removing it after the transition ends with a `transitionend` listener, rather than declaring it statically on every card in the stylesheet.

For integration, the simplest starting point is pure CSS for hover lift and shadow, with GSAP Flip added only when expand/collapse re-flows the grid. This layered approach lets you ship quickly and progressively enhance. When integrating into component frameworks such as React or Vue, scope the GSAP initialisation inside an effect hook (`useEffect`, `onMounted`) and always clean up event listeners and GSAP contexts on unmount to prevent memory leaks. In design systems, expose the easing curve and lift distance as CSS custom properties (`--card-lift-y`, `--card-enter-ease`) so individual product teams can adapt the motion language to their brand without forking the component. Container Queries — now baseline-supported across all major browsers as of 2025 — pair naturally with Bento Motion because they let individual tiles adapt their internal layout and animation intensity based on their own rendered width rather than the viewport, enabling truly self-contained, reusable tile components.
