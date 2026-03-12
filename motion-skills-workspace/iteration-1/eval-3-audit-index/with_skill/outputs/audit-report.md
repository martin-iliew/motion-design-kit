# Audit Report: index.html

**File:** `index.html` (980 lines)
**Audited:** 2026-03-12
**Skill:** motion-audit v1

---

## Audit Report: index.html

| # | Issue | Severity | Location | Fix |
|---|-------|----------|----------|-----|
| 1 | No GSAP library loaded — zero `<script>` tags for GSAP core or any plugins | CRITICAL | entire file | Add `<script src="https://cdn.jsdelivr.net/npm/gsap@3.13/dist/gsap.min.js"></script>` and required plugin scripts before `</body>` |
| 2 | No ScrollTrigger plugin loaded — scroll-driven animations impossible | CRITICAL | entire file | Add `<script src="https://cdn.jsdelivr.net/npm/gsap@3.13/dist/ScrollTrigger.min.js"></script>` after GSAP core |
| 3 | No animation JavaScript at all — page is 100% static; zero scroll reveals, zero micro-interactions, zero entrance animations | CRITICAL | entire file | Add a `<script>` block implementing GSAP animations for hero, cards, sections, footer, cursor, and marquee |
| 4 | No `prefers-reduced-motion` guard — accessibility requirement is unmet (no JS means no `gsap.matchMedia()`) | CRITICAL | entire file | Wrap all future animations in `gsap.matchMedia()` with `"(prefers-reduced-motion: no-preference)"` |
| 5 | No `ScrollTrigger.refresh()` on window load — when animations are added, ScrollTrigger measurements will be stale if not refreshed | CRITICAL | entire file | Add `window.addEventListener("load", () => ScrollTrigger.refresh())` at end of animation script |
| 6 | Custom cursor elements (`#cursor`, `#cursor-ring`) exist in HTML but have no JS driving them — they will render as static dots stuck at (0,0) | CRITICAL | lines 66-73 | Implement cursor follower pattern using `gsap.quickTo()` on mousemove, with touch-device guard |
| 7 | Marquee track (`.marquee-track`) has no CSS animation or GSAP tween — it will not scroll | CRITICAL | lines 238-269 | Add infinite horizontal scroll via `gsap.to(".marquee-track", { xPercent: -50, duration: 20, ease: "none", repeat: -1 })` or CSS `@keyframes` |
| 8 | Hero elements (`.hero-badge`, `#hero-title`, `.hero-subtitle`, `.hero-ctas`, `.hero-metrics`) have descriptive class names suggesting animation but zero entrance motion | WARNING | lines 145-218 | Implement hero entrance timeline with chained `.fromTo()` calls using stagger |
| 9 | Cards (`.card` class, 8 total) have a gradient overlay with `opacity-0` suggesting a hover reveal, but no CSS `:hover` transition or GSAP hover handler exists | WARNING | lines 294-656 | Add spring hover effect (Pattern 7) or CSS `group-hover:opacity-100 transition-opacity` on the gradient overlay |
| 10 | Magnetic button classes (`.magnetic-btn`, `.cta-magnetic-btn`) exist in HTML but no magnetic/quickTo behavior is implemented | WARNING | lines 172, 896 | Implement magnetic hover using `gsap.quickTo()` with touch-device guard |
| 11 | Section labels (`.section-label`), section titles (`.section-title`), and section body (`.section-body`) have no scroll-triggered reveal | WARNING | lines 276-288, 664-673 | Add ScrollTrigger-driven `fromTo` reveals for each section heading group |
| 12 | Process steps (`.process-step`, 4 total) are static — no staggered entrance on scroll | WARNING | lines 678-760 | Add staggered scroll reveal (Pattern 4) with `stagger: 0.09` |
| 13 | Performance cards (`.performance-card`, 3 total) are static — no entrance animation | WARNING | lines 769-856 | Add staggered scroll reveal (Pattern 4) with ScrollTrigger |
| 14 | CTA section body (`.cta-body`) has no entrance animation | WARNING | lines 875-918 | Add scroll-triggered reveal for CTA content |
| 15 | Footer has no arrival animation | WARNING | lines 924-978 | Implement footer reveal (Pattern 8) with ScrollTrigger |
| 16 | Scroll indicator (`.scroll-line`) has no pulsing or scaling animation to draw attention | WARNING | lines 223-230 | Add a repeating scaleY or opacity tween to the scroll indicator line |
| 17 | Stat numbers ("8", "200ms", "100%", "0") in hero metrics are plain text — no counter/reveal animation | INFO | lines 198-218 | Consider number counter pattern (Pattern 13) for stats, or at minimum a staggered reveal |
| 18 | Footer links have no hover micro-interaction (no color transition, no underline animation) | INFO | lines 940-967 | Add subtle `transition: color 0.2s` or GSAP hover effect on footer links |
| 19 | Nav links (`.nav-item`) have no hover animation or active state transition | INFO | lines 84-116 | Add hover color transition or underline reveal micro-interaction |
| 20 | `scroll-smooth` on `<html>` may conflict with future ScrollTrigger smooth scrolling — test before adding a smooth-scroll plugin | INFO | line 2 | Remove `scroll-smooth` class if implementing GSAP-based smooth scrolling |

**Summary:** 7 critical, 9 warnings, 4 info

---

## Dimension Analysis

### DEPENDENCIES

**Verdict: FAILED**

The page loads zero animation libraries. There is exactly one `<script>` tag in the entire file: the Tailwind CSS v4 browser runtime (line 9). No GSAP core, no ScrollTrigger, no SplitText, no Flip plugin. This is the most fundamental failure -- without libraries loaded, no animation can execute.

The HTML structure references animation concepts extensively (magnetic buttons, custom cursor, marquee, scroll-driven storytelling), but none of the required JavaScript exists to deliver on those promises.

### MODERNITY

**Verdict: PRE-2020 LEVEL (Static Page)**

This page has zero animations of any kind -- no CSS transitions, no CSS keyframes, no GSAP, no Web Animations API. Every element is completely static. The content *describes* modern animation patterns (scroll-driven storytelling, kinetic typography, magnetic hover, parallax depth) but does not *implement* any of them. This is a brochure about motion that itself has no motion.

Stale pattern indicators present:
- Zero scroll animations
- Zero transform usage in animation context
- Zero interaction feedback (hover, click, focus)
- All content visible immediately on load with no entrance sequencing

### PERFORMANCE

**Verdict: N/A (No Animations to Evaluate)**

Since there are no animations, there are no performance issues in the traditional sense. However, two structural concerns exist:

1. The custom cursor elements (`#cursor`, `#cursor-ring`) are rendered in the DOM but serve no purpose without JS. They will appear as tiny static shapes at position (0,0), potentially confusing on desktop.

2. The `overflow-x: hidden` on `body` (line 27) is appropriate for preventing horizontal scroll from animated elements, but currently unnecessary.

When animations are eventually added, the HTML structure is well-prepared: elements use classes like `.card`, `.magnetic-btn`, `.section-label` that map cleanly to animation selectors.

### CONFLICT

**Verdict: NO CONFLICTS (No Animations Exist)**

With zero CSS transitions and zero GSAP tweens, there are no conflicts to report. The page is conflict-free by virtue of having nothing that could conflict.

One potential future conflict to note: the `scroll-smooth` class on `<html>` (line 2) uses native CSS smooth scrolling, which can interfere with ScrollTrigger's scroll position calculations if a GSAP smooth-scroll solution (like ScrollSmoother) is later added.

### CONSISTENCY

**Verdict: N/A (No Motion System to Evaluate)**

There is no duration system, no easing system, and no stagger system because there are no animations. When animations are added, the audit recommends establishing:

- A duration scale: `micro=0.15s`, `fast=0.3s`, `base=0.6s`, `slow=1.0s`
- An easing vocabulary: `power2.out` for entrances, `power2.inOut` for transitions, `back.out(1.7)` for micro-interactions
- A stagger pattern: `tight=0.05s`, `medium=0.09s`, `loose=0.13s`

---

## Proposed Changes

### Fix #1 -- No GSAP Library Loaded

**Before:**
```html
  </footer>
</body>
</html>
```

**After:**
```html
  </footer>

  <!-- GSAP Core + Plugins (pinned version) -->
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.13/dist/gsap.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.13/dist/ScrollTrigger.min.js"></script>

  <script>
    gsap.registerPlugin(ScrollTrigger);
    // Animation code goes here
  </script>
</body>
</html>
```

**Why:** Without GSAP loaded, zero animations can execute -- the page is entirely static despite its HTML structure being animation-ready.

---

### Fix #2 -- No prefers-reduced-motion Guard

**Before:**
```js
// (no animation code exists)
```

**After:**
```js
gsap.registerPlugin(ScrollTrigger);

const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  // All animations go inside this block
  // They will be automatically killed if the user enables reduced motion
});
```

**Why:** All animations must be wrapped in a `matchMedia` guard so users who prefer reduced motion are not subjected to non-essential animation. This is both an accessibility requirement and a hard rule.

---

### Fix #3 -- No ScrollTrigger.refresh() on Load

**Before:**
```js
// (no load handler exists)
```

**After:**
```js
window.addEventListener("load", () => {
  ScrollTrigger.refresh();
});
```

**Why:** ScrollTrigger calculates trigger positions based on element positions at measurement time. Fonts, images, and lazy content can shift layout after initial paint. Calling `refresh()` on the `load` event ensures all measurements are accurate.

---

### Fix #4 -- Custom Cursor Stuck at (0,0)

**Before:**
```html
<div id="cursor" class="fixed top-0 left-0 w-2 h-2 rounded-full bg-violet-500 pointer-events-none z-[9999] hidden lg:block"></div>
<div id="cursor-ring" class="fixed top-0 left-0 w-7 h-7 rounded-full border border-violet-400/40 pointer-events-none z-[9999] hidden lg:block"></div>
<!-- No JavaScript to move these elements -->
```

**After:**
```js
// Inside gsap.matchMedia() block
mm.add("(pointer: fine)", () => {
  const cursor = document.getElementById("cursor");
  const ring = document.getElementById("cursor-ring");

  const xTo = gsap.quickTo(cursor, "x", { duration: 0.15, ease: "power2.out" });
  const yTo = gsap.quickTo(cursor, "y", { duration: 0.15, ease: "power2.out" });
  const ringX = gsap.quickTo(ring, "x", { duration: 0.35, ease: "power2.out" });
  const ringY = gsap.quickTo(ring, "y", { duration: 0.35, ease: "power2.out" });

  document.addEventListener("mousemove", (e) => {
    xTo(e.clientX - 4);
    yTo(e.clientY - 4);
    ringX(e.clientX - 14);
    ringY(e.clientY - 14);
  });
});
```

**Why:** The cursor and ring elements are in the DOM positioned at (0,0) with `fixed` positioning. Without JS to track the mouse, they appear as static dots in the top-left corner on desktop, which is a visible rendering artifact.

---

### Fix #5 -- Marquee Not Scrolling

**Before:**
```html
<div class="marquee-track flex whitespace-nowrap gap-10 ...">
  <span class="marquee-content ...">...</span>
  <span class="marquee-content ...">...</span>
</div>
<!-- No animation driving horizontal scroll -->
```

**After:**
```js
gsap.to(".marquee-track", {
  xPercent: -50,
  duration: 25,
  ease: "none",
  repeat: -1,
});
```

**Why:** The marquee has two duplicate content spans (a common infinite-scroll setup), but without a tween to move the track left, the second copy is hidden off-screen and the marquee is static.

---

### Fix #6 -- Hero Elements Have No Entrance Animation

**Before:**
```html
<!-- All hero elements render immediately with no entrance sequencing -->
<div class="hero-badge ...">...</div>
<h1 id="hero-title" ...>...</h1>
<p class="hero-subtitle ...">...</p>
<div class="hero-ctas ...">...</div>
<div class="hero-metrics ...">...</div>
```

**After:**
```js
// Inside matchMedia "(prefers-reduced-motion: no-preference)" block
const heroTl = gsap.timeline({ defaults: { ease: "power3.out" } });

heroTl
  .fromTo(".hero-badge", { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.6 })
  .fromTo("#hero-title span", { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 0.8, stagger: 0.15 }, "-=0.3")
  .fromTo(".hero-subtitle", { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.6 }, "-=0.4")
  .fromTo(".hero-ctas", { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.5 }, "-=0.3")
  .fromTo(".hero-metrics > div", { autoAlpha: 0, y: 15 }, { autoAlpha: 1, y: 0, duration: 0.4, stagger: 0.08 }, "-=0.2");
```

**Why:** The hero section is the first thing visitors see. Without entrance animation, the page feels flat and static. A sequenced timeline creates visual hierarchy and directs attention through the content.

---

### Fix #7 -- Cards Have No Hover or Scroll Reveal

**Before:**
```html
<div class="card ... group ...">
  <div class="absolute inset-0 bg-gradient-to-br from-violet-700/12 to-transparent opacity-0 pointer-events-none"></div>
  <!-- Gradient overlay has opacity-0 but nothing ever changes it -->
</div>
```

**After:**
```js
// Scroll reveal for cards
gsap.fromTo(".card",
  { autoAlpha: 0, y: 40 },
  {
    autoAlpha: 1, y: 0,
    duration: 0.6,
    ease: "power2.out",
    stagger: 0.09,
    scrollTrigger: {
      trigger: "#card-grid",
      start: "top 80%",
    }
  }
);

// Spring hover for cards
document.querySelectorAll(".card").forEach(card => {
  const overlay = card.querySelector(".absolute");
  card.addEventListener("mouseenter", () => {
    gsap.to(card, { y: -4, scale: 1.015, duration: 0.3, ease: "back.out(1.7)" });
    gsap.to(overlay, { autoAlpha: 1, duration: 0.3 });
  });
  card.addEventListener("mouseleave", () => {
    gsap.to(card, { y: 0, scale: 1, duration: 0.4, ease: "power2.out" });
    gsap.to(overlay, { autoAlpha: 0, duration: 0.3 });
  });
});
```

**Why:** The 8 bento grid cards are the primary content of the page. Without scroll reveal, they appear instantly without visual hierarchy. The gradient overlay with `opacity-0` was clearly intended for hover interaction but has no handler to activate it.

---

## Overall Assessment

This page is a **well-structured, animation-ready HTML template that currently has zero animation implementation**. The HTML uses semantic class names (`.hero-badge`, `.magnetic-btn`, `.section-label`, `.marquee-track`, `.card`) that map directly to GSAP animation patterns, and the layout is designed to support scroll-driven reveals, hover interactions, and entrance timelines. However, the JavaScript layer is entirely absent.

The 7 CRITICAL issues all stem from the same root cause: **no animation library is loaded and no animation code exists**. This makes the page functionally a static brochure about animation that demonstrates none of it.

**Recommended next step:** Run the `motion-dev` skill on this file to generate a complete GSAP animation layer, which would resolve all 7 CRITICAL and most WARNING issues in a single pass.

---

> Want me to apply all CRITICAL fixes directly to `index.html`? I'll make the changes and re-run the audit to confirm they're resolved.

---

_Metrics unavailable -- run `python .claude/scripts/query_cost.py --since <start-timestamp>` manually._
