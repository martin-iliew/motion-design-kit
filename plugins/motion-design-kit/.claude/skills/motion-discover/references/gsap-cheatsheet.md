# GSAP Cheatsheet — motion-discover Reference

**Progressive disclosure:** Load this file only when generating GSAP-based animation code.
Source: https://gsap.com/llms.txt (fetched and curated for 2026 patterns)

---

## Core API

```js
// Register plugins (always do this before using them)
gsap.registerPlugin(ScrollTrigger, SplitText, Flip, CustomEase);

// Basic tweens
gsap.to(".el", { x: 100, autoAlpha: 1, duration: 0.6, ease: "power2.out" });
gsap.fromTo(".el", { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 0.6, ease: "power2.out" });
gsap.fromTo(".el", { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 0.6 });
gsap.set(".el", { autoAlpha: 0, y: 40 }); // instant set, no animation

// Timelines
const tl = gsap.timeline({ defaults: { ease: "power2.out", duration: 0.6 } });
tl.fromTo(".heading", { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0 })
  .fromTo(".subheading", { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0 }, "-=0.3")  // overlap by 0.3s
  .fromTo(".cta", { autoAlpha: 0, scale: 0.9 }, { autoAlpha: 1, scale: 1 }, "<0.2"); // 0.2s after prev starts

// Stagger
gsap.fromTo(".card", { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, stagger: 0.1, duration: 0.5 });
gsap.fromTo(".word", { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, stagger: { each: 0.05, from: "start" } });
```

---

## ScrollTrigger — Core Patterns

```js
// Basic scroll reveal
gsap.fromTo(".section", {
  autoAlpha: 0,
  y: 60
}, {
  scrollTrigger: {
    trigger: ".section",
    start: "top 80%",
    end: "bottom 20%",
    toggleActions: "play none none reverse"
  },
  autoAlpha: 1,
  y: 0,
  duration: 0.8
});

// Scrubbed (tied to scroll position)
gsap.to(".parallax-bg", {
  scrollTrigger: {
    trigger: ".hero",
    start: "top top",
    end: "bottom top",
    scrub: 1  // smoothing amount (seconds)
  },
  y: -200
});

// Pinned section with scrub
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".pinned-section",
    pin: true,
    start: "top top",
    end: "+=800",
    scrub: 1,
    invalidateOnRefresh: true
  }
});
tl.fromTo(".panel-1", { autoAlpha: 0, x: -100 }, { autoAlpha: 1, x: 0 })
  .fromTo(".panel-2", { autoAlpha: 0, x: 100 }, { autoAlpha: 1, x: 0 }, "<");

// Batch (performance optimized for many elements)
ScrollTrigger.batch(".card", {
  onEnter: (elements) => gsap.fromTo(elements, { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, stagger: 0.1 }),
  start: "top 85%"
});
```

---

## SplitText — Kinetic Typography

```js
const split = new SplitText(".headline", { type: "chars,words,lines" });

// Chars stagger in
gsap.fromTo(split.chars, {
  autoAlpha: 0,
  y: 40,
  rotationX: -90,
}, {
  autoAlpha: 1,
  y: 0,
  rotationX: 0,
  stagger: 0.02,
  duration: 0.6,
  ease: "power3.out"
});

// Words reveal with clip
gsap.fromTo(split.words, {
  autoAlpha: 0,
  yPercent: 100,
}, {
  autoAlpha: 1,
  yPercent: 0,
  stagger: 0.05,
  duration: 0.7,
  ease: "power2.out"
});

// Cleanup (important for React/rerenders)
split.revert();
```

---

## Flip — Layout Animations

```js
// Animate between two layout states
const state = Flip.getState(".card"); // capture before state
container.classList.toggle("expanded"); // change layout
Flip.from(state, {
  duration: 0.6,
  ease: "power2.inOut",
  stagger: 0.05,
  absolute: true
});
```

---

## CustomEase — Branded Motion

```js
// Create once, reuse by name
CustomEase.create("brandBounce", "M0,0 C0.126,0.382 0.282,0.674 0.44,0.822 0.632,1.002 0.818,1.001 1,1");
CustomEase.create("snap", "M0,0 C0.6,0,0.4,1 1,1");

gsap.to(".el", { y: -20, ease: "brandBounce", duration: 0.8 });
```

---

## Accessibility — Required Pattern

Always wrap animations in matchMedia:

```js
const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: no-preference)", () => {
  // All animation code here
  gsap.fromTo(".hero-title", { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 1 });

  // Return cleanup function
  return () => {
    // kill ScrollTriggers, split text revert, etc.
  };
});

mm.add("(prefers-reduced-motion: reduce)", () => {
  // Optional: instant state without animation
  gsap.set(".hero-title", { autoAlpha: 1, clearProps: "y" });
});
```

---

## React / Component Cleanup

```tsx
// Install: npm install gsap @gsap/react
import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(useGSAP, ScrollTrigger); // register once at module level

function Component() {
  const containerRef = useRef(null);

  useGSAP(() => {
    // All code auto-scoped to containerRef and cleaned up on unmount
    gsap.from(".el", { autoAlpha: 0, y: 30, duration: 0.6, ease: "power2.out" });
    // For event-triggered animations, use contextSafe()
  }, { scope: containerRef });

  return <div ref={containerRef}>{/* ... */}</div>;
}
// NEVER use bare useLayoutEffect or useEffect for GSAP — always useGSAP
```

---

## Easing Reference

| Ease | Use Case |
|------|----------|
| `power2.out` | Standard entrance, most elements |
| `power3.out` | Fast, impactful entrances |
| `power2.inOut` | State transitions, layout changes |
| `power4.in` | Elements exiting (fast disappear) |
| `elastic.out(1, 0.3)` | Playful micro-interactions, spring feel |
| `back.out(1.7)` | Overshoot on small elements |
| `expo.out` | Velocity-heavy, snappy entrances |
| `none` / `linear` | Scrubbed scroll animations only |
| `CustomEase` | Brand-specific curves |

---

## Common Pitfalls to Avoid

```js
// BAD: gsap.from on element with CSS opacity:0 — will flash on completion
// GOOD: use gsap.set() then gsap.to(), or gsap.fromTo()

// BAD: multiple tweens on same property
gsap.from(".el", { x: 0 });
gsap.to(".el", { x: 100 }); // fight!

// BAD: CSS transition + GSAP on same property
// .el { transition: transform 0.3s; }
// gsap.to(".el", { scale: 1.1 }); — competing owners

// BAD: animating layout properties
gsap.to(".el", { width: 200, height: 100 }); // causes reflow!

// GOOD: only animate transform + opacity
gsap.to(".el", { scaleX: 1.5, scaleY: 1.2 }); // GPU-composited
```
