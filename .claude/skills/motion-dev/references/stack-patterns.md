# Stack Patterns — Boilerplate Scaffolds

Load this file when a specific stack has been identified. Each scaffold is a minimal working skeleton. Replace `/* TOKEN */` comments with resolved values from motion-tokens.md.

---

## Vanilla HTML + GSAP

The canonical pattern for all non-framework projects.

```html
<!-- Include GSAP before closing </body> -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
<!-- Add plugin scripts as needed: ScrollTrigger, SplitText, Flip, etc. -->
```

```js
// 1. Register plugins (once, at module level)
gsap.registerPlugin(ScrollTrigger); // add others as needed

// 2. Accessibility guard — wrap ALL animation code in matchMedia
const mm = gsap.matchMedia();

mm.add("(prefers-reduced-motion: no-preference)", () => {
  // ── Your animation code here ──────────────────────────────────
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: ".section",
      start: "top 80%",
      toggleActions: "play none none reverse",
    },
  });

  tl.fromTo(
    ".hero-title",
    { autoAlpha: 0, y: 40 },
    { autoAlpha: 1, y: 0, duration: 0.6, ease: "power2.out" } 
  ).fromTo(
    ".hero-subtitle",
    { autoAlpha: 0, y: 24 },
    { autoAlpha: 1, y: 0, duration: 0.6, ease: "power2.out" }, 
    "-=0.3"
  );
  // ── End animation code ────────────────────────────────────────

  // Return cleanup function
  return () => {
    tl.kill();
    ScrollTrigger.getAll().forEach(t => t.kill());
  };
});

mm.add("(prefers-reduced-motion: reduce)", () => {
  // Instant final state — elements visible without animation
  gsap.set(".hero-title, .hero-subtitle", { autoAlpha: 1, clearProps: "y" });
});
```

**Key rules:**
- Always `gsap.registerPlugin()` before first use
- Always `gsap.matchMedia()` wrapping all animation code
- Always return cleanup from the `no-preference` callback
- Never animate deny-list properties (width, height, top, left)

---

## React (with `@gsap/react`)

The preferred React pattern. Replaces manual `useLayoutEffect` + `gsap.context()`.

```tsx
// Install: npm install gsap @gsap/react
import { useRef } from "react";
import { useGSAP } from "@gsap/react";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(useGSAP, ScrollTrigger); // register once at module level

interface Props {
  items: string[];
}

export function AnimatedSection({ items }: Props) {
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      // All code here is auto-scoped to containerRef and cleaned up on unmount.
      // gsap.matchMedia() is still required for prefers-reduced-motion.
      const mm = gsap.matchMedia();

      mm.add("(prefers-reduced-motion: no-preference)", () => {
        gsap.fromTo(
          ".item",
          { autoAlpha: 0, y: 24 },
          {
            autoAlpha: 1,
            y: 0,
            duration: 0.6,    
            ease: "power2.out", 
            stagger: { each: 0.09, from: "start" }, 
          }
        );
        return () => gsap.killTweensOf(".item");
      });

      mm.add("(prefers-reduced-motion: reduce)", () => {
        gsap.set(".item", { autoAlpha: 1, clearProps: "y" });
      });
    },
    { scope: containerRef } // scopes all selectors to this container
  );

  return (
    <div ref={containerRef}>
      {items.map((item, i) => (
        <div key={i} className="item">{item}</div>
      ))}
    </div>
  );
}
```

**For event-triggered animations in React** (hover, click), use `contextSafe()`:

```tsx
useGSAP(
  () => {
    const { contextSafe } = useGSAP({ scope: containerRef });

    const handleHover = contextSafe(() => {
      gsap.to(".btn", { scale: 1.05, duration: 0.3, ease: "back.out(1.7)" }); // fast / spring
    });

    document.querySelector(".btn")?.addEventListener("mouseenter", handleHover);
    return () => document.querySelector(".btn")?.removeEventListener("mouseenter", handleHover);
  },
  { scope: containerRef }
);
```

**Key rules:**
- `gsap.registerPlugin(useGSAP, ...)` at module level (outside component)
- `useGSAP({ scope: containerRef })` — always provide scope
- Never use bare `useLayoutEffect` or `useEffect` for GSAP code
- `contextSafe()` for any event-triggered tween inside `useGSAP`

---

## Vue 3 (Composition API)

```vue
<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger); // once at module level

const containerRef = ref<HTMLElement | null>(null);
let ctx: gsap.Context;

onMounted(() => {
  ctx = gsap.context(() => {
    const mm = gsap.matchMedia();

    mm.add("(prefers-reduced-motion: no-preference)", () => {
      gsap.fromTo(
        ".item",
        { opacity: 0, y: 24 },
        {
          opacity: 1,
          y: 0,
          duration: 0.6,        
          ease: "power2.out",   
          stagger: { each: 0.09, from: "start" }, 
          scrollTrigger: {
            trigger: containerRef.value,
            start: "top 80%",
          },
        }
      );
      return () => gsap.killTweensOf(".item");
    });

    mm.add("(prefers-reduced-motion: reduce)", () => {
      gsap.set(".item", { autoAlpha: 1, clearProps: "y" });
    });
  }, containerRef.value); // scope to container
});

onUnmounted(() => {
  ctx.revert(); // kills all tweens, ScrollTriggers, and matchMedia listeners
});
</script>

<template>
  <div ref="containerRef">
    <div v-for="(item, i) in items" :key="i" class="item">
      {{ item }}
    </div>
  </div>
</template>
```

**Reusable Vue composable pattern** (for animations used across multiple components):

```ts
// composables/useScrollReveal.ts
import { ref, onMounted, onUnmounted } from "vue";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

export function useScrollReveal(selector: string) {
  const containerRef = ref<HTMLElement | null>(null);
  let ctx: gsap.Context;

  onMounted(() => {
    ctx = gsap.context(() => {
      const mm = gsap.matchMedia();
      mm.add("(prefers-reduced-motion: no-preference)", () => {
        gsap.fromTo(
          selector,
          { autoAlpha: 0, y: 24 },
          { autoAlpha: 1, y: 0, duration: 0.6, ease: "power2.out", // base / entrance
            scrollTrigger: { trigger: containerRef.value, start: "top 80%" } }
        );
      });
      mm.add("(prefers-reduced-motion: reduce)", () => {
        gsap.set(selector, { autoAlpha: 1, clearProps: "y" });
      });
    }, containerRef.value);
  });

  onUnmounted(() => ctx.revert());

  return { containerRef };
}
```

**Key rules:**
- `gsap.registerPlugin()` once at module level, not inside `onMounted`
- Always store `gsap.context()` result; call `ctx.revert()` in `onUnmounted`
- Scope `gsap.context()` to the component's root element

---

## Vanilla CSS (no JS)

For simple animations that don't require scroll or interaction triggers.

```css
/* 1. Define keyframes */
@keyframes fade-up {
  from {
    opacity: 0;
    transform: translateY(1.5rem); /* ~24px */
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes spring-in {
  from {
    opacity: 0;
    transform: scale(0.85);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 2. Apply animation */
.reveal {
  animation: fade-up 600ms cubic-bezier(0.0, 0.0, 0.2, 1) forwards; /* base / entrance */
}

.card {
  animation: spring-in 300ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards; /* fast / spring */
}

/* 3. Stagger via CSS custom property */
.card:nth-child(1) { --delay-index: 0; }
.card:nth-child(2) { --delay-index: 1; }
.card:nth-child(3) { --delay-index: 2; }
/* Or set --delay-index via inline style in HTML/template */

.card {
  animation-delay: calc(var(--delay-index, 0) * 90ms); /* token: medium stagger */
}

/* 4. Accessibility guard — ALWAYS present */
@media (prefers-reduced-motion: reduce) {
  .reveal,
  .card {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```

**For scroll-driven CSS animations** (Chrome/Edge/Safari 18+):

```css
/* Progress bar tied to page scroll */
#progress-bar {
  transform-origin: left;
  animation: grow-x linear forwards;
  animation-timeline: scroll(root block);
}

@keyframes grow-x {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}

/* Element that animates as it enters viewport */
.section-card {
  opacity: 0;
  transform: translateY(2rem);
  animation: fade-up 600ms cubic-bezier(0,0,0.2,1) forwards; /* base / entrance */
  animation-timeline: view(block);
  animation-range: entry 10% entry 50%;
}

@media (prefers-reduced-motion: reduce) {
  .section-card {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
```

---

## Tailwind CSS

Use Tailwind's built-in `motion-safe:` and `motion-reduce:` variants with custom token config.

```html
<!-- Fade-up reveal -->
<div class="motion-safe:animate-fade-up motion-reduce:opacity-100 opacity-0">
  Content
</div>

<!-- Spring-in with stagger (use inline style for delay index) -->
<div
  class="motion-safe:animate-spring-in motion-reduce:opacity-100 opacity-0"
  style="--delay-index: 0; animation-delay: calc(var(--delay-index) * 90ms);"
>
  Card 1
</div>

<!-- Hover interaction -->
<button class="transition-transform duration-fast ease-spring hover:scale-105 active:scale-95">
  Click me
</button>
```

Requires the token config extension from [motion-tokens.md](../../motion-tokens.md) `theme.extend`.

**With arbitrary values** (no config needed):
```html
<div class="motion-safe:animate-[fade-up_600ms_cubic-bezier(0,0,0.2,1)_forwards]">
  Content
</div>
```

---

## Svelte 5

```svelte
<script>
  import { gsap } from "gsap";
  import { ScrollTrigger } from "gsap/ScrollTrigger";
  import { onMount } from "svelte";

  gsap.registerPlugin(ScrollTrigger);

  let containerEl = $state(null);
  let { items } = $props();

  onMount(() => {
    const ctx = gsap.context(() => {
      const mm = gsap.matchMedia();

      mm.add("(prefers-reduced-motion: no-preference)", () => {
        gsap.fromTo(
          ".item",
          { autoAlpha: 0, y: 24 },
          {
            autoAlpha: 1,
            y: 0,
            duration: 0.6,        
            ease: "power2.out",   
            stagger: { each: 0.09, from: "start" }, 
            scrollTrigger: {
              trigger: containerEl,
              start: "top 80%",
            },
          }
        );
        return () => gsap.killTweensOf(".item");
      });

      mm.add("(prefers-reduced-motion: reduce)", () => {
        gsap.set(".item", { autoAlpha: 1, clearProps: "y" });
      });
    }, containerEl);

    return () => ctx.revert();
  });
</script>

<div bind:this={containerEl}>
  {#each items as item, i}
    <div class="item">{item}</div>
  {/each}
</div>
```

**Reusable `use:` action** (animation directive):

```svelte
<script>
  import { gsap } from "gsap";
  import { ScrollTrigger } from "gsap/ScrollTrigger";

  gsap.registerPlugin(ScrollTrigger);

  function scrollReveal(node) {
    const ctx = gsap.context(() => {
      const mm = gsap.matchMedia();
      mm.add("(prefers-reduced-motion: no-preference)", () => {
        gsap.fromTo(node,
          { autoAlpha: 0, y: 24 },
          { autoAlpha: 1, y: 0, duration: 0.6, ease: "power2.out", // base / entrance
            scrollTrigger: { trigger: node, start: "top 80%" } }
        );
      });
      mm.add("(prefers-reduced-motion: reduce)", () => {
        gsap.set(node, { autoAlpha: 1, clearProps: "y" });
      });
    }, node);

    return { destroy() { ctx.revert(); } };
  }
</script>

<div use:scrollReveal>Content</div>
```

**Key rules:**
- `gsap.registerPlugin()` at module level, outside component
- Always store `gsap.context()` result; call `ctx.revert()` in cleanup return from `onMount`
- Scope `gsap.context()` to the component's root element via `bind:this`
- Svelte 5: use `$state` for refs, `$props()` for component props
- For `use:` actions, return `{ destroy() { ctx.revert(); } }` for cleanup

---

## Astro (Islands Architecture)

```astro
---
// Component runs at build time — no JS by default
// GSAP must be in a <script> tag to run client-side
---

<section class="hero" id="hero-section">
  <h1 class="hero-title">Welcome</h1>
  <p class="hero-subtitle">Subtitle text</p>
</section>

<script>
  import { gsap } from "gsap";
  import { ScrollTrigger } from "gsap/ScrollTrigger";

  gsap.registerPlugin(ScrollTrigger);

  const mm = gsap.matchMedia();

  mm.add("(prefers-reduced-motion: no-preference)", () => {
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: "#hero-section",
        start: "top 80%",
        toggleActions: "play none none reverse",
      },
    });

    tl.fromTo(
      ".hero-title",
      { autoAlpha: 0, y: 40 },
      { autoAlpha: 1, y: 0, duration: 0.6, ease: "power2.out" } 
    ).fromTo(
      ".hero-subtitle",
      { autoAlpha: 0, y: 24 },
      { autoAlpha: 1, y: 0, duration: 0.6, ease: "power2.out" }, 
      "-=0.3"
    );

    return () => {
      tl.kill();
      ScrollTrigger.getAll().forEach(t => t.kill());
    };
  });

  mm.add("(prefers-reduced-motion: reduce)", () => {
    gsap.set(".hero-title, .hero-subtitle", { autoAlpha: 1, clearProps: "y" });
  });
</script>
```

**For Astro View Transitions** (re-init GSAP after page navigation):

```astro
<script>
  import { gsap } from "gsap";
  import { ScrollTrigger } from "gsap/ScrollTrigger";

  gsap.registerPlugin(ScrollTrigger);

  function initAnimations() {
    ScrollTrigger.getAll().forEach(t => t.kill()); // Kill stale triggers from previous page

    const mm = gsap.matchMedia();
    mm.add("(prefers-reduced-motion: no-preference)", () => {
      gsap.fromTo(".content",
        { autoAlpha: 0, y: 24 },
        { autoAlpha: 1, y: 0, duration: 0.6, ease: "power2.out" } 
      );
    });
    mm.add("(prefers-reduced-motion: reduce)", () => {
      gsap.set(".content", { autoAlpha: 1, clearProps: "y" });
    });
  }

  initAnimations();
  document.addEventListener("astro:page-load", initAnimations);
</script>
```

**Key rules:**
- Astro `<script>` tags are bundled and deduped — safe to import GSAP in each component
- Always clean up ScrollTriggers on `astro:page-load` (View Transitions reuse the DOM)
- Use `id` selectors for hero/unique elements (class selectors may match across pages)
- For React/Vue/Svelte islands in Astro, use that framework's pattern with `client:visible` or `client:load`
