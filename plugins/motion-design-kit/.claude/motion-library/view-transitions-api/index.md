# View Transitions API

**Framework:** CSS
**Category:** transition
**2026 Relevance:** The View Transitions API has reached full cross-browser support in 2025–2026 (Chrome, Edge, Safari, and Firefox), making native page and component transitions a production-ready default rather than a framework luxury. As teams prioritise performance budgets and reduced JavaScript payloads, this API enables app-quality animation with zero framework overhead.

## Description

The View Transitions API is a browser-native mechanism for animating between two visual states of a page — either within the same document (SPA-style) or across a full page navigation (MPA-style). At its core it works by capturing a screenshot of the current state, rendering the new state offscreen, and then crossfading the two using CSS animations that are fully customisable via the `::view-transition-*` family of pseudo-elements. The JavaScript entry point is `document.startViewTransition()`, which accepts a callback that performs your DOM update; the browser handles the before/after capture and animation automatically.

Within a component or single-page context, named view transitions allow individual elements — a card, a hero image, a navigation item — to morph smoothly from one position and size to another. Assigning `view-transition-name` to matched elements on both the old and new state tells the browser to animate that element independently from the root crossfade, producing the "shared element" transitions familiar from native mobile apps. This makes it possible to build list-to-detail expansions, persistent header elements, and image galleries without a single animation library.

The feeling this creates is one of spatial continuity: the user never loses track of where content came from or where it went. Rather than abrupt cuts that demand mental re-orientation, transitions communicate hierarchy and relationship — a card expanding into a detail view, or a page sliding in from the direction of navigation. When applied with restraint this elevates perceived performance and polish to a level previously associated only with native applications.

## Do's

- **Feature-detect before calling.** Always check `if (document.startViewTransition)` and apply the DOM update directly as a fallback — the API is progressive enhancement, not a hard dependency.
- **Fetch data before starting the transition.** Call `document.startViewTransition()` only after async data is ready so the frozen-frame period is as short as possible and the animation plays on complete content.
- **Use unique `view-transition-name` values per element.** Duplicate names in the same document at the same time cause the transition to be skipped silently; treat them like element `id` values.
- **Clean up dynamic `view-transition-name` assignments.** After `transition.finished` resolves, reset any programmatically set `view-transition-name` to `''` or `none` to avoid capturing unintended elements in future transitions.
- **Scope named transitions to elements that actually move or morph.** Apply `view-transition-name` selectively — hero images, navigation bars, persistent cards — rather than every element on the page, to keep the capture surface small and animations meaningful.

## Don'ts

- **Don't assign the same `view-transition-name` to multiple visible elements simultaneously.** The browser can only capture one element per name; duplicates cause the transition for that name to be silently dropped.
- **Don't ignore `prefers-reduced-motion`.** Users with vestibular disorders can experience nausea from motion-heavy transitions. Never assume animation is universally safe — always provide an instant or near-instant fallback.
- **Don't put slow or blocking work inside the `startViewTransition` callback.** The browser freezes the old state until the callback resolves; heavy synchronous work extends this frozen-frame window and makes transitions feel janky rather than smooth.
- **Don't rely on View Transitions as a substitute for actual performance optimisation.** Transitions mask latency; they do not reduce it. Large payloads, render-blocking resources, and layout shifts will still degrade the experience once the animation ends.
- **Don't apply `view-transition-name` to elements with `position: fixed` or complex stacking contexts without testing.** Capture behaviour can be surprising with fixed elements; verify that the captured snapshot matches the actual visual at both ends of the transition.

## Best Practices

### Accessibility and `prefers-reduced-motion`

The `prefers-reduced-motion` media query is the single most important accessibility consideration for this API. Users with vestibular disorders, epilepsy sensitivities, or simply a preference for less motion have opted into a system-level setting that must be respected. The correct approach is to collapse all `::view-transition-*` animation durations to an effectively instant value (`0.01ms`) inside a `@media (prefers-reduced-motion: reduce)` block, rather than disabling transitions entirely — this preserves the content swap while eliminating the motion. Do not rely on frameworks like Astro's `ClientRouter` to handle this for you in custom implementations; apply the guard explicitly in your own stylesheets. Note that a default View Transitions crossfade is already relatively gentle, but named shared-element transitions that involve scale, position, and rotation changes are far more likely to cause discomfort and warrant stricter motion reduction.

### Browser Support and Fallbacks

As of early 2026, same-document View Transitions (`document.startViewTransition`) are supported across Chrome 111+, Edge 111+, Safari 18+, and Firefox 144+, covering the substantial majority of global browser market share. Cross-document transitions via the `@view-transition { navigation: auto; }` CSS at-rule have slightly narrower support — Chrome 126+, Edge 126+, and Safari 18.2+ — while Firefox's cross-document support is still maturing. The correct strategy is progressive enhancement: always write the DOM update logic to work without the API, wrap the transition call in a feature check, and treat the animation as a cosmetic layer. For cross-document MPA transitions, both the outgoing and incoming documents must include the `@view-transition` at-rule and must share the same origin; cross-origin navigations cannot use this feature by design.

### Performance

The browser imposes a timeout on view transitions — Chrome will skip a transition with a `TimeoutError` if the callback takes longer than four seconds to resolve. This is a safety mechanism, but it means that genuinely slow navigations will silently lose their transitions in production. The performance best practice is therefore to decouple data fetching from the transition itself: fetch first, then call `startViewTransition`. Additionally, keep the number of named `view-transition-name` elements low. Each named element requires the browser to capture a separate layer as a GPU texture; large pages with many named elements can create memory pressure, especially on mobile devices. Benchmark transitions with Chrome DevTools' Animations panel and Layers view, and prefer animating two or three key elements over attempting to capture the entire page as a mosaic of named parts.
