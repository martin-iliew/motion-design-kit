# Motion Tokens — Guard Rails

Single source of truth for all animation values. Every skill and generated code snippet **must** resolve values from this file. Never write a raw duration number, easing string, or stagger value without referencing a token.

---

## Duration Scale

| Token | GSAP `duration` | CSS `animation-duration` | Canonical use |
|-------|----------------|--------------------------|---------------|
| `micro` | `0.15` | `150ms` | Hover feedback, cursor response, icon flickers |
| `fast` | `0.3` | `300ms` | Button states, badge appearances, tooltip enter |
| `base` | `0.6` | `600ms` | Card reveals, modal entrances, section reveals |
| `slow` | `1.0` | `1000ms` | Hero animations, page transitions, drawer open |
| `epic` | `1.5` | `1500ms` | Cinematic moments, splash screens, brand intros |

**Usage rule:** Always add a comment beside the value: `duration: 0.6,`

**Deviating from the scale:** Allowed only for scroll-scrubbed animations (where `duration` is overridden by `scrub`) or physics-driven interactions where period/amplitude control pacing. Document the reason inline.

---

## Easing Vocabulary

| Token | GSAP | CSS `cubic-bezier` | Use |
|-------|------|--------------------|-----|
| `entrance` | `power2.out` | `cubic-bezier(0.0, 0.0, 0.2, 1)` | Standard reveals, fade-ins, scroll triggers |
| `impact` | `power3.out` | `cubic-bezier(0.0, 0.0, 0.1, 1)` | Fast, impactful entrances, hero elements |
| `transition` | `power2.inOut` | `cubic-bezier(0.4, 0.0, 0.2, 1)` | State changes, tab switches, layout shifts |
| `exit` | `power3.in` | `cubic-bezier(0.4, 0.0, 1.0, 1.0)` | Elements leaving, closing, dismissing |
| `spring` | `back.out(1.7)` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Tactile micro-interactions, button presses |
| `elastic` | `elastic.out(1, 0.3)` | GSAP only | Expressive spring moments, icon pop-ins |
| `scrub` | `none` | `linear` | Scroll-tied scrub animations only |
| `brand` | `CustomEase("brand", "...")` | Define per project | Branded motion signature |

**Usage rule:** Add a comment beside the value: `ease: "power2.out", `

**GSAP elastic customization:** `elastic.out(amplitude, period)` — amplitude `1` = proportional overshoot, period `0.3` = tight/fast oscillation. Increase period (e.g., `0.5`) for looser wobble. Never increase amplitude above `1.5` for UI elements.

**No spring/elastic on exit:** Exit animations must use `exit` token (`power3.in`). Oscillating elements leaving the screen look broken, not physical.

---

## Stagger Scale

| Token | Per-element delay | Use |
|-------|------------------|-----|
| `tight` | `0.05s` | Character-level (SplitText), kinetic typography |
| `medium` | `0.09s` | List items, batch scroll reveals, icon groups |
| `loose` | `0.13s` | Cards, grid sections, feature blocks |

**Usage rule:** `stagger: { each: 0.09, from: "start" },`

**GSAP stagger options:**
- `from: "start"` — left-to-right, top-to-bottom (default reveals)
- `from: "center"` — expands outward from middle (hero grids)
- `from: "end"` — right-to-left, bottom-to-top (exit choreography)
- `from: "random"` — organic, non-uniform (ambient/particle effects)
- `from: "edges"` — converges to center (focus moments)

---

## GPU-Safe Property List

### Allow (compositor-thread — zero layout cost)
- `x`, `y`, `xPercent`, `yPercent` — translates (use instead of `left`/`top`)
- `scale`, `scaleX`, `scaleY` — use instead of `width`/`height`
- `rotation`, `rotationX`, `rotationY`, `skewX`, `skewY`
- `opacity`, `autoAlpha` — GSAP's `autoAlpha` also handles `visibility`
- `transformOrigin` — controls pivot, no layout impact

### Deny (layout-triggering — causes reflow)
- `width`, `height` → use `scaleX`/`scaleY` instead
  - **WHY:** Triggers full document reflow; recalculates layout for all siblings. Scale is compositor-optimized.
- `top`, `left`, `right`, `bottom` → use `x`/`y` (translateX/Y) instead
  - **WHY:** Position-based properties force layout recalculation every frame. Transform properties bypass layout entirely.
- `margin`, `padding` → use `x`/`y` offset instead
  - **WHY:** Margin/padding changes affect sibling layout. Use transform-based translation instead.
- `border-width` → use `scale` + `outline-offset` workaround
  - **WHY:** Animating border-width causes constant repaint and reflow. Alternative: `outline` with dynamic `outline-offset` and opacity.
- `font-size` → use `scale` instead
  - **WHY:** Font-size changes reflow text, recalculate metrics, break layout. Use transform: scale() for visual size changes.

### Caution (paint-only — acceptable with care)
- `border-radius` — causes repaint, not reflow; acceptable for state transitions
- `background-color`, `color` — paint only; fine for short durations (<0.3s)
- `box-shadow` — triggers repaint on every frame; **prefer the pseudo-element opacity hack** for animated shadows:

```css
/* Preferred: animate the shadow's opacity, not the shadow itself */
.card::after {
  content: '';
  box-shadow: 0 20px 40px rgba(0,0,0,0.3);
  opacity: 0;
  transition: opacity 0.3s ease; /* token: fast / entrance */
}
.card:hover::after { opacity: 1; }
```

---

## will-change Policy

| Scenario | Policy | Why |
|----------|--------|-----|
| Idle/ambient animations (breathing, particles) | **Permanent CSS** — set in stylesheet | Animates on page load with no interaction; constant promotion acceptable |
| Scroll-triggered animations | **Dynamic JS** — set on `onEnter`, remove on `onLeaveBack` | Only promoted during active scroll window |
| Hover/interaction animations | **Dynamic JS** — set on `mouseenter`/`focus`, remove on `transitionend` | Short bursts; permanent would waste GPU memory |
| Canvas-based animations | **Never** — canvas composites itself | Applying will-change to canvas or its parent creates a new stacking context, breaking z-index |
| Any pool > 8 elements simultaneously | **Never** — use `gsap.set()` + remove after | Browsers cap compositor layer memory; > 8 promotions simultaneously causes layer eviction jank |

**Dynamic will-change pattern (GSAP):**
```js
element.addEventListener("mouseenter", () => {
  element.style.willChange = "transform, opacity";
  gsap.to(element, { scale: 1.05, duration: 0.3, ease: "power2.out" }); 
});
element.addEventListener("mouseleave", () => {
  gsap.to(element, {
    scale: 1,
    duration: 0.3,
    ease: "power2.out", 
    onComplete: () => { element.style.willChange = "auto"; }
  });
});
```

---

## Cleanup Standard (one canonical pattern per stack)

### Vanilla HTML / Plain JS
```js
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  // all animation code here
  return () => {
    // cleanup: kill tweens, revert splits, remove listeners
    gsap.killTweensOf(targets);
  };
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(targets, { clearProps: "all" }); // instant final state
});
```

### React (preferred — `@gsap/react`)
```tsx
import { useGSAP } from "@gsap/react";
import { useRef } from "react";

function Component() {
  const containerRef = useRef(null);
  useGSAP(() => {
    // all animation code — auto-cleaned on unmount
    // use contextSafe() for event-triggered animations
  }, { scope: containerRef });
  return <div ref={containerRef}>{/* ... */}</div>;
}
```
**Rule:** Never use bare `useLayoutEffect` for GSAP. Never use `useEffect` for GSAP. Always `useGSAP`.

### Vue 3 (Composition API)
```ts
import { onMounted, onUnmounted, ref } from "vue";
import { gsap } from "gsap";

const containerRef = ref(null);
let ctx: gsap.Context;

onMounted(() => {
  ctx = gsap.context(() => {
    // all animation code
  }, containerRef.value);
});

onUnmounted(() => {
  ctx.revert();
});
```
**Composable pattern:** For reuse across components, extract into `useAnimation(target, config)`.

### SPA Route Transitions (Barba, Next.js, Astro)
```js
// In route-leave hook / beforeUnmount / beforePageLeave:
ScrollTrigger.getAll().forEach(t => t.kill());
gsap.killTweensOf("*");
```

---

## Tailwind CSS Token Mapping

Add to `tailwind.config.js` `theme.extend` to use token names as utility classes:

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      transitionDuration: {
        'micro': '150ms',
        'fast': '300ms',
        'base': '600ms',
        'slow': '1000ms',
        'epic': '1500ms',
      },
      transitionTimingFunction: {
        'entrance': 'cubic-bezier(0.0, 0.0, 0.2, 1)',
        'impact':   'cubic-bezier(0.0, 0.0, 0.1, 1)',
        'transition': 'cubic-bezier(0.4, 0.0, 0.2, 1)',
        'exit':     'cubic-bezier(0.4, 0.0, 1.0, 1.0)',
        'spring':   'cubic-bezier(0.34, 1.56, 0.64, 1)',
      },
      keyframes: {
        // Add named keyframes here for Tailwind animate- utilities
        'fade-up': {
          '0%': { opacity: '0', transform: 'translateY(1.5rem)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        'spring-in': {
          '0%': { opacity: '0', transform: 'scale(0.85)' },
          '100%': { opacity: '1', transform: 'scale(1)' },
        },
      },
      animation: {
        'fade-up': 'fade-up 600ms cubic-bezier(0.0, 0.0, 0.2, 1) forwards',    // base / entrance
        'fade-in': 'fade-in 600ms cubic-bezier(0.0, 0.0, 0.2, 1) forwards',    // base / entrance
        'spring-in': 'spring-in 300ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards', // fast / spring
      },
    },
  },
};
```

**Usage in markup:**
```html
<!-- motion-safe: applies only when no prefers-reduced-motion -->
<div class="motion-safe:animate-fade-up motion-reduce:opacity-100">
  Content
</div>
```

**Arbitrary value syntax** (no config needed):
```html
<div class="duration-[600ms] ease-[cubic-bezier(0,0,0.2,1)]">...</div>
```

---

## Quick Reference Card

```
DURATION  micro=0.15  fast=0.3  base=0.6  slow=1.0  epic=1.5
EASING    entrance=power2.out  impact=power3.out  transition=power2.inOut
          exit=power3.in  spring=back.out(1.7)  elastic=elastic.out(1,0.3)
STAGGER   tight=0.05  medium=0.09  loose=0.13
ANIMATE   transform+opacity only  |  will-change: dynamic for interactions
CLEANUP   HTML: gsap.matchMedia()  React: useGSAP()  Vue: onMounted/onUnmounted
```
