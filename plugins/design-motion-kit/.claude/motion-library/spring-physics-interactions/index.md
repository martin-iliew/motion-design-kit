# Spring Physics Interactions

**Framework:** GSAP
**Category:** micro-interaction
**2026 Relevance:** As interfaces become more tactile and expressive, spring-based motion signals responsiveness and physicality that flat, linear animations cannot convey. In 2026, users increasingly expect UI elements to feel "alive" — elastic and back easings in GSAP deliver that organic, momentum-driven quality across buttons, modals, tooltips, and drag interactions.

## Description

Spring physics interactions simulate the behavior of a real elastic system: an element overshoots its target position and oscillates before settling, exactly as a spring or rubber band would. In GSAP, this is primarily achieved through `elastic.out` and `back.out` easings. `elastic.out(amplitude, period)` controls both the intensity of the overshoot (amplitude) and the speed of oscillation (period), while `back.out(overshoot)` produces a single, clean overshoot-and-return without the oscillation — making it ideal for UI elements that need personality without visual noise.

The distinction between these two easings is important for practical use. `elastic.out` is best reserved for deliberate attention-grabbing moments: a success state icon snapping into place, a notification badge appearing, or a floating action button expanding. The oscillation draws the eye and communicates energy. `back.out` is more versatile for everyday micro-interactions — button presses, card hovers, modal entrances — where a subtle overshoot adds tactile feel without distracting from the content.

Parameter tuning is where spring interactions go from generic to polished. For `elastic.out`, the defaults (`elastic.out(1, 0.3)`) are a strong starting point: amplitude `1` keeps the overshoot proportional, and period `0.3` produces a fast, tight oscillation. Increasing the period (e.g., `0.5`) creates a slower, looser wobble. For `back.out`, the classic value is `1.7` — enough overshoot to feel physical without looking broken. Always pair these easings with short-to-medium durations (0.4–0.8s); longer durations make elastic motion feel sluggish rather than springy.

## Do's

- Use `elastic.out(1, 0.3)` as your baseline and tune amplitude/period per element size — smaller elements tolerate tighter periods; larger elements need looser values.
- Pair spring easings exclusively with `transform` properties (`scale`, `x`, `y`, `rotation`) and `opacity` — these are GPU-composited and won't trigger layout reflow.
- Apply `back.out` on entrances and returns; use `power2.in` / `power3.in` on exits — spring motion on exit feels wrong and delays perceived responsiveness.
- Always wrap animation blocks in `gsap.matchMedia()` with a `prefers-reduced-motion: no-preference` condition and a `gsap.set()` fallback in the `reduce` branch.
- Use `clearProps: "scale,y"` after spring animations complete to prevent stale inline styles conflicting with CSS hover states.

## Don'ts

- Do not animate `width`, `height`, `top`, `left`, `margin`, or `padding` with spring easings — layout properties cause expensive reflows regardless of easing quality.
- Do not use `elastic.out` on exit/leave animations — oscillating elements leaving the screen look broken; use `power3.in` or `expo.in` instead.
- Do not set `duration` above 0.8s for most spring interactions — beyond this the motion reads as slow rather than elastic, disrupting interaction flow.
- Do not apply spring easings globally via `gsap.defaults()` — reserve them for intentional accent moments; overuse destroys the motion hierarchy and fatigues users.
- Do not mix CSS `transition: transform` with GSAP tweens on the same property — the two systems will fight for ownership of the value, producing erratic results.

## Best Practices

Accessibility must be the first constraint, not an afterthought. The `gsap.matchMedia()` pattern is the correct GSAP-native solution: all spring animation code lives inside the `(prefers-reduced-motion: no-preference)` branch, and a `(prefers-reduced-motion: reduce)` branch uses `gsap.set()` to instantly establish the final visible state. Users with vestibular disorders or motion sensitivity never see oscillating elements. Keyboard interactions (Enter, Space) must also trigger the same spring feedback that mouse events produce, ensuring the tactile quality is not pointer-exclusive.

Performance with spring physics in GSAP is reliable because all easing curves — including elastic and back — are computed via pre-calculated mathematical lookup tables rather than frame-by-frame physics simulation. This means they carry no additional per-frame cost over `power2.out`. The performance ceiling is determined entirely by which CSS properties you animate. Stick to `transform` and `opacity`; if you need to animate color as part of a spring interaction, do so as a separate tween using `power2.out` so the composited transform channel remains clean. On mobile, reduce amplitude and stagger counts — a period of `0.3` on desktop may feel loose on 60Hz mobile; `0.25` is a safer cross-device default.

For component-based frameworks (React, Vue, Svelte), always scope GSAP contexts to the component's root ref using `gsap.context(() => { ... }, rootRef)` and call `ctx.revert()` in the cleanup/unmount lifecycle hook. This prevents animation state from leaking between renders or route changes. When spring interactions are triggered by user events, kill any in-progress tween before starting a new one — `gsap.killTweensOf(target)` prevents compounding animations when users interact faster than the duration allows. Define spring easing strings as named constants (`const SPRING = "back.out(1.7)"`) so the motion vocabulary remains consistent and centrally adjustable.
