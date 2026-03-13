# Motion Spec Translation Guide

Lookup-optimized translation rules for converting a Motion Spec document into each output target. Motion Spec files live at `.claude/motion-library/<pattern-name>/spec.yaml`. The catalog is at `.claude/motion-library/catalog.yaml`. For the full schema, see [motion-spec.md](../../../motion-spec.md). For value resolution, see [motion-tokens.md](../../../motion-tokens.md).

---

## Step 1: Resolve Tokens

Before translating, resolve all token references to concrete values:

```
timing.duration token → lookup in motion-tokens.md Duration Scale
  micro → GSAP: 0.15  |  CSS: 150ms
  fast  → GSAP: 0.30  |  CSS: 300ms
  base  → GSAP: 0.60  |  CSS: 600ms
  slow  → GSAP: 1.00  |  CSS: 1000ms
  epic  → GSAP: 1.50  |  CSS: 1500ms

timing.easing token → lookup in motion-tokens.md Easing Vocabulary
  entrance   → GSAP: "power2.out"              |  CSS: cubic-bezier(0.0, 0.0, 0.2, 1)
  impact     → GSAP: "power3.out"              |  CSS: cubic-bezier(0.0, 0.0, 0.1, 1)
  transition → GSAP: "power2.inOut"            |  CSS: cubic-bezier(0.4, 0.0, 0.2, 1)
  exit       → GSAP: "power3.in"               |  CSS: cubic-bezier(0.4, 0.0, 1.0, 1.0)
  spring     → GSAP: "back.out(1.7)"           |  CSS: cubic-bezier(0.34, 1.56, 0.64, 1)
  elastic    → GSAP: "elastic.out(1, 0.3)"     |  CSS: NOT AVAILABLE — use spring fallback
  scrub      → GSAP: none (scrub handles it)   |  CSS: linear

stagger.tier token → per-element delay
  tight  → GSAP: each: 0.05  |  CSS: calc(var(--i) * 50ms)
  medium → GSAP: each: 0.09  |  CSS: calc(var(--i) * 90ms)
  loose  → GSAP: each: 0.13  |  CSS: calc(var(--i) * 130ms)
```

If `duration_raw` or `easing_raw` is present, it takes precedence over the token.

---

## Translation: Motion Spec → Vanilla CSS

```
from/to properties:
  opacity → @keyframes: opacity: [value]
  x       → @keyframes: transform: translateX([value]px)
  y       → @keyframes: transform: translateY([value]px)
  xPercent → @keyframes: transform: translateX([value]%)
  yPercent → @keyframes: transform: translateY([value]%)
  scale   → @keyframes: transform: scale([value])
  scaleX  → @keyframes: transform: scaleX([value])
  scaleY  → @keyframes: transform: scaleY([value])
  rotation → @keyframes: transform: rotate([value]deg)
  NOTE: Combine multiple transforms in one transform: declaration

timing.duration → animation-duration: [css value]
timing.easing   → animation-timing-function: [css cubic-bezier]
timing.delay    → animation-delay: [value]s

trigger.type:
  load   → apply class immediately, or use animation directly on element
  scroll → animation-timeline: view() / scroll() with animation-range
  hover  → :hover selector (no JS needed)
  focus  → :focus-visible selector

stagger.tier → animation-delay: calc(var(--delay-index, 0) * [ms]ms)
  Set --delay-index via inline style or :nth-child selectors in HTML/template

a11y.reduced_motion:
  ANY value → ALWAYS add:
    @media (prefers-reduced-motion: reduce) {
      .selector {
        animation: none;
        opacity: 1;         /* or whatever the "to" opacity is */
        transform: none;    /* reset to natural state */
      }
    }

sequence.position → NOT TRANSLATABLE to CSS — output as separate animation with delay offset
```

**Output structure:**
```css
@keyframes [id] {
  from { [from properties as CSS] }
  to   { [to properties as CSS] }
}

.[selector-class] {
  animation: [id] [duration] [easing] [delay] forwards;
  /* For scroll: animation-timeline: view(); animation-range: entry 10% entry 50%; */
}

@media (prefers-reduced-motion: reduce) {
  .[selector-class] { animation: none; opacity: 1; transform: none; }
}
```

---

## Translation: Motion Spec → Tailwind CSS

```
from/to properties:
  opacity:0 → class: opacity-0
  opacity:1 → class: opacity-100 (or remove opacity-0 class)
  scale: 0.9 → class: scale-90 (Tailwind scale utilities use integers: scale-90 = 0.9)
  y: 24 → class: translate-y-6 (Tailwind uses rem: 6 = 1.5rem ≈ 24px)
  NOTE: For precise pixel values, use arbitrary: translate-y-[24px]

timing.duration → class: duration-[token] (from token config) or duration-[600ms] (arbitrary)
timing.easing   → class: ease-[token] (from token config) or ease-[cubic-bezier(...)] (arbitrary)

trigger.type:
  hover   → hover:scale-105 hover:opacity-100 etc.
  focus   → focus-visible:... variants
  scroll  → NOT natively supported — requires JS or Intersection Observer setup
  load    → Tailwind animation utilities: animate-[keyframe-name]

stagger → inline style: style="animation-delay: calc(var(--delay-index) * 90ms)"
  Set --delay-index via template binding (React: style={{...}}, Vue: :style="{...}")

a11y.reduced_motion → prefix classes with motion-safe: and motion-reduce:
  opacity-0 motion-safe:animate-fade-up motion-reduce:opacity-100

sequence.position → NOT TRANSLATABLE to Tailwind — use animation-delay as offset
```

**Output structure:**
```html
<!-- Single element -->
<div class="opacity-0 motion-safe:animate-fade-up motion-reduce:opacity-100">
  Content
</div>

<!-- Stagger group (React example) -->
{items.map((item, i) => (
  <div
    key={i}
    className="opacity-0 motion-safe:animate-fade-up motion-reduce:opacity-100"
    style={{ animationDelay: `${i * 90}ms` }}
  >
    {item}
  </div>
))}
```

Requires keyframe definitions in `tailwind.config.js`. See motion-tokens.md Tailwind section.

---

## Translation: Motion Spec → GSAP HTML (Vanilla JS)

```
from block → first argument of gsap.fromTo() or a preceding gsap.set() when the element starts hidden
to block   → second argument (vars object)
  x, y, xPercent, yPercent → direct GSAP properties
  scale, scaleX, scaleY → direct GSAP properties
  rotation, rotationX, rotationY → direct GSAP properties
  opacity → translate to autoAlpha for entrances and visibility toggles; use raw opacity only when visibility must stay untouched
  autoAlpha → preferred GSAP property for visibility state changes

timing.duration → duration: [resolved value]  
timing.easing   → ease: "[resolved GSAP string]"  
timing.delay    → delay: [value]

stagger.tier → stagger: { each: [resolved value], from: "[stagger.from]" }  

trigger.type:
  load   → no scrollTrigger, tween fires immediately (optionally wrap in window DOMContentLoaded)
  scroll → add scrollTrigger: { trigger: "[selector]", start: "[scroll_start]",
             toggleActions: "[toggle_actions]", scrub: [scroll_scrub],
             pin: [scroll_pin] }
  hover  → addEventListener("mouseenter") / ("mouseleave") on target
  click  → addEventListener("click") on target
  focus  → addEventListener("focus") on target

physics override → replace easing_raw with "elastic.out([amplitude], [period])"

a11y.reduced_motion:
  ANY value → wrap entire tween in gsap.matchMedia():
    mm.add("(prefers-reduced-motion: no-preference)", () => { /* tween */ return () => { /* cleanup */ }; });
    mm.add("(prefers-reduced-motion: reduce)", () => { gsap.set(selector, { clearProps: "all" }); });
    (if skip: don't add reduce branch — purely decorative)
    (if instant-final: gsap.set(selector, { autoAlpha:to.opacity, y:to.y, ... }))
    (if instant-start: gsap.set(selector, { autoAlpha:from.opacity, y:from.y, ... }))

sequence.position → use as 3rd argument in timeline:
  tl.to(selector, vars, "[sequence.position]")
```

**Output structure:**
```js
gsap.registerPlugin(ScrollTrigger); // if scroll trigger used

const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: no-preference)", () => {
  gsap.fromTo(
    "[target.selector]",
    { autoAlpha: [from.opacity], y: [from.y] },
    {
      autoAlpha: [to.opacity],
      y: [to.y],
      duration: [resolved duration], 
      ease: "[resolved ease]",       
      stagger: { each: [resolved stagger], from: "[stagger.from]" }, // if group
      scrollTrigger: { ... }, // if scroll trigger
    }
  );
  return () => { gsap.killTweensOf("[target.selector]"); };
});

mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[target.selector]", { autoAlpha: 1, clearProps: "y" }); // instant-final
});
```

---

## Translation: Motion Spec → GSAP React (TSX)

Same as GSAP HTML translation rules, with these differences:

```
Wrap in useGSAP({ scope: containerRef }) instead of bare script:
  - All selectors resolve relative to containerRef
  - useGSAP auto-cleans on unmount — no manual cleanup needed
  - Still require gsap.matchMedia() inside useGSAP for reduced-motion

Event-triggered tweens (hover, click, focus):
  - Use contextSafe() wrapper:
    const handleEnter = contextSafe(() => { gsap.to(...) });
    element.addEventListener("mouseenter", handleEnter);
    return () => element.removeEventListener("mouseenter", handleEnter);

Register plugins once at module level (outside component):
  gsap.registerPlugin(useGSAP, ScrollTrigger);

Import useGSAP:
  import { useGSAP } from "@gsap/react";
```

**Output structure:**
```tsx
import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(useGSAP, ScrollTrigger);

export function [ComponentName]() {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      const mm = gsap.matchMedia();
      mm.add("(prefers-reduced-motion: no-preference)", () => {
        gsap.fromTo("[target.selector]", { ... }, { ..., scrollTrigger: { ... } });
        return () => gsap.killTweensOf("[target.selector]");
      });
      mm.add("(prefers-reduced-motion: reduce)", () => {
        gsap.set("[target.selector]", { autoAlpha: 1, clearProps: "y" });
      });
    },
    { scope: containerRef }
  );

  return <div ref={containerRef}>{/* ... */}</div>;
}
```

---

## Translation: Motion Spec → GSAP Vue (Composition API)

Same as GSAP HTML translation rules, with these differences:

```
Wrap in gsap.context() inside onMounted:
  - Scope to component root: gsap.context(() => { ... }, containerRef.value)
  - Store result: let ctx = gsap.context(...)
  - Call ctx.revert() in onUnmounted

Event-triggered tweens:
  - Register listeners in onMounted
  - Remove listeners in onUnmounted (or use ctx.revert() if tween is in context)

Consider extracting to composable if used in 2+ components.
```

**Output structure:**
```vue
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

const containerRef = ref<HTMLElement | null>(null);
let ctx: gsap.Context;

onMounted(() => {
  ctx = gsap.context(() => {
    const mm = gsap.matchMedia();
    mm.add("(prefers-reduced-motion: no-preference)", () => {
      gsap.fromTo("[target.selector]", { ... }, { ..., scrollTrigger: { ... } });
      return () => gsap.killTweensOf("[target.selector]");
    });
    mm.add("(prefers-reduced-motion: reduce)", () => {
      gsap.set("[target.selector]", { autoAlpha: 1, clearProps: "y" });
    });
  }, containerRef.value);
});

onUnmounted(() => { ctx.revert(); });
</script>

<template>
  <div ref="containerRef"><!-- ... --></div>
</template>
```

---

## Non-Translatable Motion Spec Fields

Some Motion Spec fields cannot be expressed in certain output targets:

| Motion Spec Field | Not translatable to | Reason | Fallback |
|----------|---------------------|--------|----------|
| `sequence.position` | CSS, Tailwind | No native timeline sequencing | Use `animation-delay` offset |
| `trigger.type: scroll` | Tailwind | No GSAP dependency | Use IntersectionObserver + class toggle |
| `timing.easing: elastic` | CSS | No native spring curves | Use `spring` token (cubic-bezier) instead |
| `physics.amplitude/period` | CSS, Tailwind | Computed at runtime | Use spring token as approximation |
| `stagger.from: random` | CSS | Not reproducible in CSS | Use sequential delay with nth-child |

When a non-translatable field is encountered, document the limitation in a comment in the output and apply the closest fallback.

---

## Procedural Patterns (type: procedural)

Procedural patterns (particles, text scramble, cursor following) cannot be expressed as from→to tweens. Their spec.yaml uses a `config` block and `behavior` description instead of `from`/`to` blocks.

**Translation approach:** Do not attempt to map `config` fields to tween properties. Instead:
- Read the `behavior` field to understand what the animation does
- Read the `config` block for parameters (count, speed, size ranges, etc.)
- Generate idiomatic code for the target stack that replicates the described behavior
- Use `config` values directly as constants or variables in the generated code

**a11y for procedural patterns:**
- `reduced_motion: skip` → the entire animation is omitted; the element is hidden or static
- `reduced_motion: instant-final` → show the final state immediately, no animation

---

## Browser-Native Patterns (type: browser-native)

Browser-native patterns (CSS scroll-driven animations, View Transitions API) use a `properties` array and `mechanism` field instead of `from`/`to` blocks.

**Translation approach:**
- The `mechanism` field identifies the API: `css-scroll-timeline`, `css-view-timeline`, `view-transitions-api`
- The `properties` array maps to `@keyframes` from/to values or `::view-transition-*` pseudo-element styles
- The `trigger` block describes when the animation fires; for `view-transitions-api`, the trigger is always manual (`document.startViewTransition()`)
- These patterns are **not translatable to GSAP** without significant restructuring — note this limitation in a comment and provide the closest GSAP fallback if the user specifically requests it

**Non-translatable fields for browser-native patterns:**

| Field | Not translatable to | Reason | Fallback |
|-------|---------------------|--------|----------|
| `mechanism: view-transitions-api` | GSAP | Requires browser capture API | GSAP FLIP or manual opacity crossfade |
| `trigger.range` (CSS view-timeline) | GSAP vanilla | Uses CSS animation-range syntax | ScrollTrigger with equivalent start/end |
| `::view-transition-old/new` pseudo | GSAP | Pseudo-elements not animatable by GSAP | Use GSAP on actual elements instead |
