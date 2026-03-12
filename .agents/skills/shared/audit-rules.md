# Shared Audit Rules — Motion Skills

Unified reference for motion-dev (element audit + code generation) and motion-audit (quality review). Load the parts you need:

- **motion-dev** → Parts A, C, D, E
- **motion-audit** → Parts B, C, E
- **motion-enhance** → Parts B, C, E

---

## Part A: Element Decision Table

Scan HTML top-to-bottom. For each element, apply the matching GSAP pattern. **NEVER** substitute CSS keyframes when a GSAP pattern exists.

### Global Checks (run first)

1. **Reduced-motion:** `const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches`
2. **Touch device:** `const isTouch = "ontouchstart" in window || navigator.maxTouchPoints > 0`
3. **CSS transition conflicts:** Find elements with `transition:` on properties GSAP will animate — remove the CSS transition
4. **GSAP loaded:** Verify GSAP CDN script + `gsap.registerPlugin(ScrollTrigger)` exists

### Element → Pattern Map

| Element Pattern | Trigger | GSAP Pattern | Guard | Notes |
|---|---|---|---|---|
| `<nav>` without scroll reactivity | "navbar", "navigation" | Smart hide/show — Pattern 2 | none | Hides on scroll-down, shows on scroll-up |
| Hero `<h1>` / `<h2>` static on load | "hero heading", "page title" | Hero entrance timeline — Pattern 1 | `prefersReduced` | 4+ chained `.fromTo` calls |
| Hero badge / label / subtext | "hero badge", "hero label" | Add to hero timeline stagger | `prefersReduced` | Part of Pattern 1 timeline |
| Primary CTA button (desktop only) | "hero cta", "main button" | Magnetic quickTo — Pattern 3 | `isTouch` | Desktop-only with touch guard |
| Hero background / glow element | "hero background", "hero glow" | Parallax scrub — Pattern 5 | `isTouch + prefersReduced` | Moves on scroll; desktop-only |
| Feature cards / grid | "cards", "features", "grid" | Stagger scroll reveal — Pattern 4 | `prefersReduced` | Stagger 0.09s per card (token: medium) |
| Pricing cards | "pricing", "plans", "tiers" | Stagger scroll reveal — Pattern 4 | `prefersReduced` | Same as feature cards |
| Section labels / headings | "section-label", "section-heading" | Section reveal — Pattern 6 | `prefersReduced` | Reveals as you scroll into view |
| Body copy / description | "section-body", "copy" | Section reveal — Pattern 6 | `prefersReduced` | Part of Pattern 6 |
| `.card` without entrance | "card", "item", "box" | Spring hover — Pattern 7 | `prefersReduced` | Lifts on hover; dynamic will-change |
| Logo names / brand list | "logo-list", "partners" | Scale-in stagger (Pattern 4 variant) | `prefersReduced` | Use Pattern 4 with stagger: 0.09 |
| `<footer>` without arrival animation | "footer", "bottom section" | Footer reveal — Pattern 8 | `prefersReduced` | Reveals as footer enters viewport |
| Stat / counter numbers | "stat", "counter", "metric" | Number counter — Pattern 13 | `prefersReduced` | Scroll-triggered counting with snap |
| Pinned feature walkthrough | "features", "steps", "showcase" | Pinned scrub — Pattern 11 | `prefersReduced` | Multi-step pin + scrub timeline |
| Filterable / sortable grid | "filter", "portfolio grid" | FLIP layout — Pattern 12 | `prefersReduced` | Animate layout changes with Flip plugin |
| Custom cursor (portfolio/creative) | site-wide | Cursor follower — Pattern 14 | `isTouch` | Desktop-only dot + ring with quickTo |
| Tiltable cards (portfolio) | "tilt-card", "interactive card" | 3D tilt — Pattern 15 | `isTouch` | rotationX/Y from cursor position |
| Click-feedback buttons | "ripple", "click effect" | Ripple click — Pattern 16 | none | Expanding circle from click coords |

### Implementation Checklist

- [ ] Element matched to correct GSAP pattern from decision table
- [ ] Pattern code copied from `gsap-patterns.md` (exact)
- [ ] Selectors adjusted to match HTML classNames/IDs
- [ ] `gsap.matchMedia()` wrapping all animations
- [ ] `autoAlpha` used instead of bare `opacity`
- [ ] Token comments on all `duration` and `ease` values
- [ ] No CSS `transition` on GSAP-owned properties
- [ ] Touch guards applied where needed (Patterns 3, 5, 7, 14, 15)
- [ ] `ScrollTrigger.refresh()` called at end via `window.addEventListener("load", ...)`

---

## Part B: 5-Dimension Audit Framework

### Dimension 1: DEPENDENCIES

- GSAP version >= 3.13 when using formerly-premium plugins (SplitText, MorphSVG, DrawSVG, ScrambleText, CustomEase, Physics2D) — all free since May 2025
- Plugin `<script>` tags placed BEFORE code that calls `gsap.registerPlugin()`
- CDN URL uses a pinned version (e.g. `gsap@3.14`), not floating (`@latest`, `@3`)
- `new SplitText()` or any DOM-measuring call placed after `document.fonts.ready`

### Dimension 2: MODERNITY

**Stale patterns (CRITICAL):**
- Site has zero scroll animations
- Only `opacity` is ever animated (no `transform` usage)

**Stale patterns (WARNING):**
- `transition: all 0.3s ease` as a global reset
- Every animation is 0.3s (no duration hierarchy)
- Only hover color changes, no transform micro-interactions
- All animations run on page load with no scroll/interaction trigger

**2026-quality signals:**
- Scroll-driven reveals with `ScrollTrigger` or CSS `animation-timeline: scroll()`
- Physics-based spring easings (`elastic.out`, `CustomEase`)
- Kinetic typography (word/char splits, staggered reveals)
- Micro-interactions on interactive elements (buttons scale, icons morph)
- State-driven motion (enter, exit, idle, active)
- Fluid navigation transitions (shared-element / FLIP)

### Dimension 3: PERFORMANCE

**Layout-triggering properties (CRITICAL):** `width`, `height`, `min-width`, `max-width`, `top`, `left`, `right`, `bottom`, `margin`, `padding`, `border-width`, `font-size`

**GPU-safe alternatives:** `transform: translate()` for position, `scale()` for size, `opacity` for visibility, `rotate()` for rotation.

**Bad animation APIs (CRITICAL):** `setInterval()`/`setTimeout()` for animation, jQuery `.animate()`.

**Performance warnings (WARNING):** missing `will-change` on heavy animated elements, `-webkit-` prefixed transforms (obsolete), `requestAnimationFrame` loop updating non-composited properties.

**Missing accessibility (CRITICAL):** GSAP animations without `gsap.matchMedia()` or `prefers-reduced-motion` guard.

### Dimension 4: CONFLICT

**GSAP anti-patterns (CRITICAL):**
- `gsap.from()` + `gsap.to()` on same element/property — use `fromTo` instead
- `gsap.from()` on opacity-0 elements (invisible flash bug) — use `fromTo` or `set` + `to`
- Multiple timelines animating same CSS property simultaneously
- CSS `transition` + GSAP on same property — remove CSS transition

**ScrollTrigger conflicts (WARNING):**
- Two `scrub: true` triggers on same element
- `pin: true` on parent AND child simultaneously
- Missing `invalidateOnRefresh: true` when layout can change

### Dimension 5: CONSISTENCY

**Duration system:** Professional sites use a named scale, not random values. Flag (WARNING) if >4 distinct durations without a system.

**Easing system:** Sites should use one easing family consistently (GSAP Power or CSS cubic-bezier). Flag (WARNING) if mixing GSAP power easings with CSS `ease-in-out` on related elements. Flag (INFO) if using `linear` for entrance animations.

**Stagger system:** Stagger should follow a formula. Flag (INFO) if values don't follow a consistent pattern.

---

## Part C: Hard Rules

Non-negotiable rules for all motion skills:

1. **No CSS keyframe substitution** — never write `@keyframes` when a GSAP pattern exists for that element type
2. **Always `autoAlpha`** — never bare `opacity` in `gsap.from()`/`gsap.fromTo()` calls; `autoAlpha` handles both opacity AND visibility
3. **Always `gsap.matchMedia()`** — never raw `if/else` for reduced-motion; always wrap in `mm.add("(prefers-reduced-motion: no-preference)", ...)`
4. **Remove CSS `transition` on GSAP-owned properties** — dual control causes jank
5. **Use `gsap.fromTo()` on hidden elements** — `gsap.from()` on opacity-0 elements causes invisible flash bug
6. **`ScrollTrigger.refresh()` on load** — every full-page animation must call `ScrollTrigger.refresh()` on `window.load`
7. **GPU-safe only** — never animate `width`, `height`, `top`, `left`, `margin`, `padding`; use `transform` and `opacity`
8. **Pinned GSAP version** — CDN URLs must use pinned versions (e.g. `gsap@3.14`), never `@latest`

---

## Part D: Easing Decision Table

| Context | Easing | Token | Notes |
|---|---|---|---|
| Scroll reveal entrance | `power2.out` | `entrance` | Default for any element entering viewport via ScrollTrigger |
| Hero headline impact | `power3.out` | `impact` | Sharper deceleration for hero timelines, key product moments |
| Layout transition (Flip) | `power2.inOut` | `transition` | Symmetric ease for FLIP layout changes, shared-element transitions |
| Element exit / dismiss | `power3.in` | `exit` | Quick acceleration out — modals closing, elements leaving viewport |
| Tactile button press | `back.out(1.7)` | `spring` | Subtle overshoot on release — buttons, toggles, micro-interactions |
| Playful bounce | `elastic.out(1, 0.3)` | `elastic` | Pronounced wobble — badges, notifications, playful UI |
| Scroll-scrubbed | `none` (linear) | `scrub` | 1:1 scroll position mapping — parallax, progress bars, pinned sections |

**Rule of thumb:** If unsure, use `entrance` (`power2.out`). Reserve `impact` and `spring` for intentional emphasis.

---

## Part E: Token Quick Reference

```
duration:  micro=0.15  fast=0.3  base=0.6  slow=1.0  epic=1.5
easing:    entrance=power2.out  impact=power3.out  transition=power2.inOut
           exit=power3.in  spring=back.out(1.7)  elastic=elastic.out(1,0.3)
           scrub=none
stagger:   tight=0.05  medium=0.09  loose=0.13
```
