# Audit Report: index.html

**File:** `index.html` (980 lines)
**Type:** Single-page static HTML — KINETIC motion design patterns landing page
**Libraries detected:** Tailwind CSS v4 (browser CDN)
**Animation libraries detected:** None

---

## Dimension Analysis

### 1. DEPENDENCIES

The page references **no animation libraries whatsoever**. There is exactly one `<script>` tag on the entire page:

```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

- **No GSAP CDN** loaded (no `gsap.min.js`, no `ScrollTrigger.min.js`)
- **No CSS animation or transition declarations** anywhere in the `<style>` block
- **No inline JavaScript** or `<script>` blocks for animation logic
- The page talks extensively *about* GSAP patterns (ScrollTrigger, SplitText, quickTo, Flip, autoAlpha) in its marketing copy but does not actually implement any of them

This is the most fundamental finding: the page is entirely static. Every element that *should* animate is frozen in its initial state.

### 2. MODERNITY

The page scores **zero** on modernity signals:

- No scroll-driven reveals (`ScrollTrigger` or `animation-timeline`)
- No kinetic typography (SplitText)
- No micro-interactions on buttons or cards
- No stagger reveals on the bento card grid
- No magnetic hover on CTAs
- No parallax depth layers
- No custom cursor animation (the `#cursor` and `#cursor-ring` elements exist in HTML but have no JS driving them)
- No hero entrance timeline
- No navbar hide/show on scroll
- No footer reveal animation
- No marquee animation (the `.marquee-track` is static)

This is especially problematic because the page's entire *content* is about motion design quality -- the disconnect between messaging and execution is total.

### 3. PERFORMANCE

With no animations present, there are no active performance issues. However, structural concerns exist:

- The `#cursor` and `#cursor-ring` divs are in the DOM with `position: fixed` but have no `will-change` hint and no JS controlling them -- they are invisible dead elements on desktop (visible via `lg:block` but stuck at `top:0 left:0`)
- The `overflow-x: hidden` on `<body>` is fine for a landing page but should be paired with `overscrollBehavior` if scroll-driven animations are added later
- Tailwind's `scroll-smooth` class on `<html>` will conflict with GSAP's `ScrollTrigger` smooth scroll if added later -- this should be removed before implementing scroll animations

### 4. CONFLICT

No conflicts exist because there is no animation code. However, preventive notes:

- The `scroll-smooth` CSS (from the `scroll-smooth` class on `<html>`) will interfere with ScrollTrigger's pin/scrub calculations -- must be removed before adding GSAP scroll animations
- No CSS `transition` properties detected that would conflict with future GSAP animations

### 5. CONSISTENCY

Not applicable -- there is no motion system to evaluate for consistency. The page has zero durations, zero easings, and zero stagger values.

---

## Severity Table

| # | Issue | Severity | Location | Fix |
|---|-------|----------|----------|-----|
| 1 | No GSAP library loaded -- page has zero animation capability despite being an animation showcase | CRITICAL | `<head>` (missing) | Add `<script src="https://cdn.jsdelivr.net/npm/gsap@3.14/dist/gsap.min.js"></script>` and `<script src="https://cdn.jsdelivr.net/npm/gsap@3.14/dist/ScrollTrigger.min.js"></script>` before `</body>` |
| 2 | No hero entrance timeline -- hero badge, headline, subtitle, CTAs, and stats all load statically | CRITICAL | lines 144-219 | Implement a GSAP timeline with 4+ chained `.fromTo()` calls using `autoAlpha`, stagger for metrics, and `power3.out` easing |
| 3 | No scroll-triggered reveals on any section -- bento cards, process steps, performance pillars, CTA, and footer all appear statically | CRITICAL | lines 273-920 | Add `ScrollTrigger`-based `gsap.from()` with `autoAlpha:0, y:30` to all `.card`, `.process-step`, `.performance-card`, `.cta-body`, and footer elements |
| 4 | No `prefers-reduced-motion` guard anywhere -- when animations are added, accessibility will be unhandled | CRITICAL | entire file | Wrap all future GSAP code in `gsap.matchMedia()` with `"(prefers-reduced-motion: no-preference)"` |
| 5 | Custom cursor elements (`#cursor`, `#cursor-ring`) exist in DOM but have no JS -- they render as dead dots at top-left on desktop | CRITICAL | lines 66-73 | Either implement cursor follower with `gsap.quickTo()` (with touch guard) or remove the HTML elements entirely |
| 6 | Marquee track (`.marquee-track`) is static -- no CSS animation or GSAP tween to create scrolling motion | WARNING | lines 238-269 | Add a GSAP `to()` tween with `xPercent: -50, repeat: -1, ease: "none"` for infinite marquee or use CSS `@keyframes` |
| 7 | `scroll-smooth` class on `<html>` will conflict with ScrollTrigger pin/scrub calculations | WARNING | line 2 | Remove `scroll-smooth` class from `<html>` before implementing ScrollTrigger-based animations |
| 8 | Tailwind CDN uses floating version `@4` instead of pinned version (e.g., `@4.1.0`) | WARNING | line 9 | Pin to specific version: `https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.1.0` |
| 9 | No `will-change` on any element that should animate (cards, hero elements, cursor) | INFO | throughout | Add `will-change: transform, opacity` dynamically via GSAP or as a CSS class on elements that will be animated |
| 10 | Section labels, titles, and body text (`.section-label`, `.section-title`, `.section-body`) have no entrance animations | INFO | lines 276-288, 664-673 | These are ideal candidates for section reveal (Pattern 6) with `power2.out` easing |
| 11 | No magnetic hover effect on CTA buttons (`.magnetic-btn`, `.cta-magnetic-btn`) despite class names suggesting it | INFO | lines 172, 896 | Implement `gsap.quickTo()` magnetic effect with touch device guard |
| 12 | No spring hover on bento grid cards despite `.card` class being present | INFO | lines 294-656 | Add Pattern 7 (spring hover with `back.out(1.7)` scale) to all `.card` elements |
| 13 | No navbar scroll reactivity (hide on scroll-down, show on scroll-up) | INFO | lines 76-118 | Implement Pattern 2 (smart hide/show navbar) with ScrollTrigger |
| 14 | No footer reveal animation | INFO | lines 924-978 | Add Pattern 8 (footer reveal) with ScrollTrigger when footer enters viewport |

**Summary:** 5 critical, 3 warnings, 6 info

---

## Proposed Changes

### Fix #1 -- No GSAP Library Loaded

**Before:**
```html
</body>
</html>
```

**After:**
```html
    <!-- GSAP Core + Plugins (pinned version) -->
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14/dist/gsap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14/dist/ScrollTrigger.min.js"></script>
    <script>
      gsap.registerPlugin(ScrollTrigger);
    </script>
</body>
</html>
```

**Why:** The page cannot animate anything without GSAP loaded -- this is the prerequisite for every other fix.

---

### Fix #2 -- No Hero Entrance Timeline

**Before:**
```html
<!-- Hero elements are static with no animation -->
<div class="hero-badge ...">...</div>
<h1 id="hero-title" ...>...</h1>
<p class="hero-subtitle ...">...</p>
<div class="flex flex-wrap items-center gap-4 hero-ctas">...</div>
<div class="flex flex-wrap gap-8 mt-16 hero-metrics">...</div>
```

**After:** (add inside a `<script>` block before `</body>`)
```js
gsap.matchMedia().add("(prefers-reduced-motion: no-preference)", () => {
  const heroTl = gsap.timeline({ defaults: { ease: "power3.out" } });

  heroTl
    .fromTo(".hero-badge",
      { autoAlpha: 0, y: 20 },
      { autoAlpha: 1, y: 0, duration: 0.6 })
    .fromTo("#hero-title span",
      { autoAlpha: 0, y: 40 },
      { autoAlpha: 1, y: 0, duration: 0.8, stagger: 0.15 }, "-=0.3")
    .fromTo(".hero-subtitle",
      { autoAlpha: 0, y: 20 },
      { autoAlpha: 1, y: 0, duration: 0.6 }, "-=0.4")
    .fromTo(".hero-ctas > *",
      { autoAlpha: 0, y: 20 },
      { autoAlpha: 1, y: 0, duration: 0.5, stagger: 0.1 }, "-=0.3")
    .fromTo(".hero-metrics > div",
      { autoAlpha: 0, y: 15 },
      { autoAlpha: 1, y: 0, duration: 0.4, stagger: 0.09 }, "-=0.2");

  // Scroll indicator pulse
  gsap.fromTo(".scroll-line",
    { scaleY: 0 },
    { scaleY: 1, duration: 1, ease: "power2.inOut", repeat: -1, yoyo: true });
});
```

**Why:** The hero section is the first thing users see -- a staggered entrance timeline with `autoAlpha` prevents invisible flash bugs and creates an impactful first impression.

---

### Fix #3 -- No Scroll-Triggered Section Reveals

**Before:**
```html
<!-- All sections load fully visible with no entrance animation -->
```

**After:** (add inside the same `matchMedia` callback)
```js
// Bento cards stagger reveal
gsap.from(".card", {
  autoAlpha: 0,
  y: 40,
  duration: 0.6,
  ease: "power2.out",
  stagger: 0.09,
  scrollTrigger: {
    trigger: "#card-grid",
    start: "top 80%",
  }
});

// Process steps stagger reveal
gsap.from(".process-step", {
  autoAlpha: 0,
  y: 30,
  duration: 0.6,
  ease: "power2.out",
  stagger: 0.09,
  scrollTrigger: {
    trigger: "#process",
    start: "top 75%",
  }
});

// Performance pillars stagger reveal
gsap.from(".performance-card", {
  autoAlpha: 0,
  y: 30,
  duration: 0.6,
  ease: "power2.out",
  stagger: 0.09,
  scrollTrigger: {
    trigger: "#performance",
    start: "top 75%",
  }
});

// CTA section reveal
gsap.from(".cta-body", {
  autoAlpha: 0,
  y: 40,
  duration: 0.8,
  ease: "power2.out",
  scrollTrigger: {
    trigger: "#contact",
    start: "top 80%",
  }
});

// Section labels and titles
gsap.utils.toArray(".section-label, .section-title, .section-body").forEach(el => {
  gsap.from(el, {
    autoAlpha: 0,
    y: 20,
    duration: 0.6,
    ease: "power2.out",
    scrollTrigger: {
      trigger: el,
      start: "top 85%",
    }
  });
});

// ScrollTrigger.refresh on load
window.addEventListener("load", () => ScrollTrigger.refresh());
```

**Why:** Scroll-triggered reveals are the baseline expectation for a 2026-quality site -- without them, the page feels like a static wireframe.

---

### Fix #4 -- No `prefers-reduced-motion` Guard

**Before:**
```html
<!-- No JavaScript exists, so no accessibility guard exists -->
```

**After:**
```js
// All animation code must be wrapped in:
gsap.matchMedia().add("(prefers-reduced-motion: no-preference)", () => {
  // All animation code goes here
});
```

**Why:** Users with vestibular disorders or motion sensitivity rely on this OS-level preference -- WCAG 2.1 SC 2.3.3 requires respecting it.

---

### Fix #5 -- Dead Custom Cursor Elements

**Before:**
```html
<div id="cursor" class="fixed top-0 left-0 w-2 h-2 rounded-full bg-violet-500 pointer-events-none z-[9999] hidden lg:block"></div>
<div id="cursor-ring" class="fixed top-0 left-0 w-7 h-7 rounded-full border border-violet-400/40 pointer-events-none z-[9999] hidden lg:block"></div>
```

**After:** (implement cursor follower with touch guard)
```js
// Inside matchMedia "(prefers-reduced-motion: no-preference)" block
const isTouch = "ontouchstart" in window || navigator.maxTouchPoints > 0;

if (!isTouch) {
  const cursor = document.getElementById("cursor");
  const cursorRing = document.getElementById("cursor-ring");

  const moveCursor = gsap.quickTo(cursor, "css", {
    duration: 0.15,
    ease: "power2.out",
  });
  const xTo = gsap.quickTo(cursor, "x", { duration: 0.15, ease: "power2.out" });
  const yTo = gsap.quickTo(cursor, "y", { duration: 0.15, ease: "power2.out" });
  const ringXTo = gsap.quickTo(cursorRing, "x", { duration: 0.35, ease: "power2.out" });
  const ringYTo = gsap.quickTo(cursorRing, "y", { duration: 0.35, ease: "power2.out" });

  document.addEventListener("mousemove", (e) => {
    xTo(e.clientX - 4);
    yTo(e.clientY - 4);
    ringXTo(e.clientX - 14);
    ringYTo(e.clientY - 14);
  });
}
```

**Why:** The cursor and ring divs are visible on desktop (`lg:block`) but stuck at `(0, 0)` with no movement -- they create visual noise without any interactivity.

---

### Fix #6 (WARNING) -- Static Marquee Track

**Before:**
```html
<div class="marquee-track flex whitespace-nowrap gap-10 ...">
  <span class="marquee-content ...">...</span>
  <span class="marquee-content ...">...</span>
</div>
```

**After:**
```js
// Infinite marquee
gsap.to(".marquee-track", {
  xPercent: -50,
  duration: 30,
  ease: "none",
  repeat: -1,
});
```

**Why:** The marquee has duplicated content (two `.marquee-content` spans) clearly intended for infinite scroll looping, but no animation drives the movement.

---

### Fix #7 (WARNING) -- `scroll-smooth` Conflicts with ScrollTrigger

**Before:**
```html
<html lang="en" class="scroll-smooth">
```

**After:**
```html
<html lang="en">
```

**Why:** CSS `scroll-behavior: smooth` interferes with ScrollTrigger's scroll position calculations, causing pin jumps and miscalculated scrub positions.

---

### Fix #8 (WARNING) -- Floating Tailwind CDN Version

**Before:**
```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

**After:**
```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4.1.0"></script>
```

**Why:** Floating version tags risk silent breaking changes when the CDN resolves to a new minor/patch version.

---

## Overall Assessment

This page is a **fully static HTML document with zero animation implementation**. It contains well-structured, semantically meaningful HTML with clear class names that map directly to animation patterns (`.hero-badge`, `.magnetic-btn`, `.card`, `.process-step`, `.scroll-line`, `.marquee-track`, `.section-label`, `#cursor`), but none of these are wired to any animation logic.

The page is essentially a perfect candidate for the `motion-dev` skill -- all the HTML hooks are in place, the design system is clean, and the class naming conventions align with standard GSAP pattern selectors. However, from an audit perspective, it fails every motion quality dimension because there is nothing to evaluate.

**Recommendation:** Run `motion-dev` on this file to generate a complete GSAP animation layer. The HTML structure is already well-organized for it.

---

> Want me to apply all CRITICAL fixes directly to `index.html`? I'll make the changes and re-run the audit to confirm they're resolved.

---

_Metrics unavailable -- run `python .claude/scripts/query_cost.py --since <start-timestamp>` manually._
