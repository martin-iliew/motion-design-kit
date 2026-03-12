# GSAP Pattern Templates

17 complete, copy-paste GSAP patterns with token comments, autoAlpha, gsap.matchMedia(), and touch guards. Use these to implement full-page animations — never substitute with CSS keyframe classes when a pattern exists for your element type.

---

## CDN — All Plugins Free (GSAP 3.13+, May 2025)

Webflow acquired GreenSock and released all GSAP plugins for free in May 2025. SplitText, ScrambleTextPlugin, MorphSVG, DrawSVG, Flip, Draggable, Inertia, and all others are now 100% free including commercial use.

```html
<!-- Core (always) -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14/dist/ScrollTrigger.min.js"></script>
<!-- Add when using kinetic typography on headings -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14/dist/SplitText.min.js"></script>
<!-- Add when using scramble effect on badges/labels -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14/dist/ScrambleTextPlugin.min.js"></script>
<!-- Add when using FLIP layout animations -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14/dist/Flip.min.js"></script>
```

---

## Pattern 1 — Hero Entrance Timeline

Use for hero sections with badge, heading, body, CTAs, and supporting notes. Creates a staggered cascade effect with `gsap.timeline()`.

```js
gsap.registerPlugin(ScrollTrigger);
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const heroTl = gsap.timeline({ defaults: { ease: "power3.out" } }); 
  heroTl
    .fromTo(".hero-badge",   { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.6 })  
    .fromTo(".hero-heading", { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 0.8 }, "-=0.3")
    .fromTo(".hero-body",    { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.6 }, "-=0.4")
    .fromTo(".hero-ctas",    { autoAlpha: 0, y: 20 }, { autoAlpha: 1, y: 0, duration: 0.5 }, "-=0.3")
    .fromTo(".hero-note",    { autoAlpha: 0 },         { autoAlpha: 1, duration: 0.4 }, "-=0.2");
  return () => heroTl.kill();
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set([".hero-badge", ".hero-heading", ".hero-body", ".hero-ctas", ".hero-note"], { clearProps: "all" });
});
```

---

## Pattern 2 — Smart Navbar Hide/Show

Use for navbar that hides on scroll-down and reveals on scroll-up. Velocity-driven using ScrollTrigger.

```js
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const st = ScrollTrigger.create({
    start: "top top",
    onUpdate: (self) => {
      if (self.direction === 1) {
        gsap.to("nav", { yPercent: -100, duration: 0.3, ease: "power2.in" }); 
      } else {
        gsap.to("nav", { yPercent: 0, duration: 0.3, ease: "power2.out" }); 
      }
    }
  });
  return () => st.kill();
});
```

---

## Pattern 3 — Magnetic CTA Button (Desktop-Only)

Use for primary CTA buttons that follow cursor on hover. Desktop-only with touch guard.

```js
const isTouch = "ontouchstart" in window || navigator.maxTouchPoints > 0;
if (!isTouch) {
  document.querySelectorAll(".btn-primary, [data-magnetic]").forEach(btn => {
    const xTo = gsap.quickTo(btn, "x", { duration: 0.4, ease: "power3.out" }); 
    const yTo = gsap.quickTo(btn, "y", { duration: 0.4, ease: "power3.out" });
    btn.addEventListener("mousemove", e => {
      const { left, top, width, height } = btn.getBoundingClientRect();
      xTo((e.clientX - (left + width / 2)) * 0.35);
      yTo((e.clientY - (top + height / 2)) * 0.35);
    });
    btn.addEventListener("mouseleave", () => { xTo(0); yTo(0); });
  });
}
```

---

## Pattern 4 — Card/Grid Stagger Scroll Reveal

Use for feature cards, pricing cards, logo grids, or any list that reveals on scroll. Stagger reveals with ScrollTrigger.

```js
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const cards = gsap.utils.toArray(".card, .feature-card, .pricing-card");
  cards.forEach((card, i) => {
    gsap.fromTo(card,
      { autoAlpha: 0, y: 40 },
      {
        autoAlpha: 1, y: 0,
        duration: 0.6,      
        ease: "power3.out", 
        delay: i * 0.09,    
        scrollTrigger: { trigger: card, start: "top 85%", toggleActions: "play none none none" }
      }
    );
  });
  return () => ScrollTrigger.getAll().forEach(t => t.kill());
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(".card, .feature-card, .pricing-card", { clearProps: "all" });
});
```

---

## Pattern 5 — Parallax Background Scrub

Use for hero backgrounds, glow elements, or large background shapes that move with scroll. Desktop-only.

```js
const isTouch = "ontouchstart" in window || navigator.maxTouchPoints > 0;
if (!isTouch) {
  const mm = gsap.matchMedia();
  mm.add("(prefers-reduced-motion: no-preference)", () => {
    gsap.to(".hero-glow, .hero-bg", {
      yPercent: -20,
      ease: "none",  
      scrollTrigger: { trigger: "body", start: "top top", end: "bottom bottom", scrub: 1.5 }
    });
  });
}
```

---

## Pattern 6 — Section Label + Heading Scroll Reveal

Use for section labels, headings, and body copy that reveal as you scroll into view. Individual element triggers.

```js
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  gsap.utils.toArray(".section-label, .section-heading, .section-body").forEach(el => {
    gsap.fromTo(el,
      { autoAlpha: 0, y: 30 },
      {
        autoAlpha: 1, y: 0,
        duration: 0.65,     
        ease: "power3.out", 
        scrollTrigger: { trigger: el, start: "top 85%", toggleActions: "play none none none" }
      }
    );
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(".section-label, .section-heading, .section-body", { clearProps: "all" });
});
```

---

## Pattern 7 — Spring Hover on Cards (Dynamic will-change)

Use for any card that should lift and scale slightly on hover with spring easing. Dynamic will-change for performance.

```js
document.querySelectorAll(".card, .feature-card").forEach(card => {
  card.addEventListener("mouseenter", () => {
    card.style.willChange = "transform";
    gsap.to(card, { y: -8, scale: 1.02, duration: 0.3, ease: "back.out(1.7)" }); 
  });
  card.addEventListener("mouseleave", () => {
    gsap.to(card, {
      y: 0, scale: 1,
      duration: 0.3,       
      ease: "power2.out", 
      onComplete: () => { card.style.willChange = "auto"; }
    });
  });
});
```

---

## Pattern 8 — Footer Scroll Reveal

Use for footers, final sections, or CTAs at the bottom of the page. Reveals as footer enters viewport.

```js
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  gsap.fromTo("footer",
    { autoAlpha: 0, y: 40 },
    {
      autoAlpha: 1, y: 0,
      duration: 0.8,      
      ease: "power2.out", 
      scrollTrigger: { trigger: "footer", start: "top 95%" }
    }
  );
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("footer", { clearProps: "all" });
});
```

---

## Pattern 9 — SplitText Kinetic Heading (Free since GSAP 3.13)

Use for hero headings, section headings, or any display text that should animate word-by-word from below a line mask. Requires `SplitText.min.js`.

```js
// Requires: <script src="https://cdn.jsdelivr.net/npm/gsap@3.14/dist/SplitText.min.js"></script>
gsap.registerPlugin(ScrollTrigger, SplitText);

const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll(".hero-heading, .section-heading[data-split]").forEach(el => {
    const split = new SplitText(el, {
      type: "lines,words",
      mask: "lines",      // words slide up from below the clipping line — no overflow visible
      autoSplit: true,    // re-splits on resize and font-load events automatically
      aria: true,         // adds aria-label on parent, aria-hidden on split children
      onSplit(self) { buildTl(self); }
    });

    let tl;
    function buildTl(s) {
      if (tl) tl.kill();
      const hasScrollTrigger = el.closest("section") !== null;
      tl = gsap.timeline({
        ...(hasScrollTrigger ? {
          scrollTrigger: { trigger: el, start: "top 85%", toggleActions: "play none none none" }
        } : {})
      });
      tl.from(s.words, {
        yPercent: 110,
        autoAlpha: 0,
        duration: 0.8,      
        ease: "power3.out", 
        stagger: { each: 0.05, from: "start" },
      });
    }
    buildTl(split);

    return () => { if (tl) tl.kill(); split.revert(); };
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(".hero-heading, .section-heading[data-split]", { clearProps: "all" });
});
```

---

## Pattern 10 — ScrambleText Badge/Label (Free since GSAP 3.13)

Use for hero badges, section labels, or short announcement text. Characters scramble through random glyphs before locking into the final word. Requires `ScrambleTextPlugin.min.js`.

```js
// Requires: <script src="https://cdn.jsdelivr.net/npm/gsap@3.14/dist/ScrambleTextPlugin.min.js"></script>
gsap.registerPlugin(ScrambleTextPlugin);

const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  document.querySelectorAll(".hero-badge [data-scramble], [data-scramble-label]").forEach(el => {
    const finalText = el.dataset.scramble || el.textContent.trim();
    gsap.fromTo(el,
      { autoAlpha: 0 },
      {
        autoAlpha: 1,
        duration: 1.2,    
        ease: "none",
        scrambleText: {
          text: finalText,
          chars: "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#",
          speed: 0.4,
          revealDelay: 0.25,
        }
      }
    );
  });
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set("[data-scramble], [data-scramble-label]", { clearProps: "all" });
});
```

---

## Pattern 4b — ScrollTrigger.batch() for Large Lists

Use instead of Pattern 4 when there are 10+ repeating elements (cards, list items, grid cells). More performant than individual ScrollTriggers.

```js
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  gsap.set(".card", { autoAlpha: 0, y: 30 });
  ScrollTrigger.batch(".card", {
    onEnter: (elements) => {
      gsap.to(elements, {
        autoAlpha: 1, y: 0,
        duration: 0.6,        
        ease: "power2.out",  
        stagger: 0.09,        
        overwrite: true,
      });
    },
    start: "top 85%",
  });
  return () => ScrollTrigger.getAll().forEach(t => t.kill());
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(".card", { clearProps: "all" });
});
```

---

## Pattern 11 — Pinned Section with Scrub Timeline

Use for multi-step feature walkthroughs, product tours, or storytelling sections pinned to the viewport. Steps fade in/out sequentially as user scrolls.

```js
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: ".feature-section",
      pin: true,
      scrub: 0.5,
      start: "top top",
      end: "+=300%",
      invalidateOnRefresh: true,
    },
  });

  tl.fromTo(".step-1", { autoAlpha: 1 }, { autoAlpha: 0, duration: 1 })
    .fromTo(".step-2", { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 1, ease: "power2.out" }) 
    .fromTo(".step-2", { autoAlpha: 1 }, { autoAlpha: 0, duration: 1 })
    .fromTo(".step-3", { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 1, ease: "power2.out" }); 

  return () => { tl.kill(); ScrollTrigger.getAll().forEach(t => t.kill()); };
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  gsap.set(".step-1, .step-2, .step-3", { autoAlpha: 1, clearProps: "y" });
});
```

---

## Pattern 12 — FLIP Layout Reflow

Use for grid filter/sort animations. Animates layout changes without touching width/height — uses the Flip plugin to capture state before and after a DOM change.

```js
// Requires: Flip.min.js
gsap.registerPlugin(Flip);

function filterItems(category) {
  const state = Flip.getState(".grid-item");

  document.querySelectorAll(".grid-item").forEach(item => {
    item.classList.toggle("hidden",
      category !== "all" && !item.dataset.category.includes(category)
    );
  });

  Flip.from(state, {
    duration: 0.6,            
    ease: "power2.inOut",    
    stagger: 0.05,            
    absolute: true,
    onEnter: elements =>
      gsap.fromTo(elements, { autoAlpha: 0, scale: 0.8 }, { autoAlpha: 1, scale: 1, duration: 0.6 }),
    onLeave: elements =>
      gsap.to(elements, { autoAlpha: 0, scale: 0.8, duration: 0.3 }),
  });
}
```

---

## Pattern 13 — Number Counter

Use for stat counters, KPI sections, or any number that should animate up from 0 on scroll. Uses `snap` for integer display.

```js
const mm = gsap.matchMedia();
mm.add("(prefers-reduced-motion: no-preference)", () => {
  gsap.utils.toArray(".stat-number").forEach(el => {
    gsap.fromTo(el,
      { innerText: 0 },
      {
        innerText: parseInt(el.dataset.target),
        duration: 1.5,          
        ease: "power2.out",     
        snap: { innerText: 1 },
        scrollTrigger: {
          trigger: el.closest("section") || el,
          start: "top 75%",
          toggleActions: "play none none none",
        },
      }
    );
  });
  return () => ScrollTrigger.getAll().forEach(t => t.kill());
});
mm.add("(prefers-reduced-motion: reduce)", () => {
  document.querySelectorAll(".stat-number").forEach(el => {
    el.textContent = el.dataset.target;
  });
});
```

HTML: `<span class="stat-number" data-target="1500">0</span>`

---

## Pattern 14 — Custom Cursor Follower (Desktop-Only)

Use for portfolio/creative sites. Dot follows cursor instantly, ring follows with smooth lag. Scales up on interactive elements.

```js
const isTouch = "ontouchstart" in window || navigator.maxTouchPoints > 0;
if (!isTouch) {
  const dot = document.querySelector(".cursor-dot");
  const ring = document.querySelector(".cursor-ring");

  const xTo = gsap.quickTo(dot, "x", { duration: 0.15, ease: "power2.out" });  
  const yTo = gsap.quickTo(dot, "y", { duration: 0.15, ease: "power2.out" });
  const ringX = gsap.quickTo(ring, "x", { duration: 0.35, ease: "power2.out" }); 
  const ringY = gsap.quickTo(ring, "y", { duration: 0.35, ease: "power2.out" });

  window.addEventListener("mousemove", (e) => {
    xTo(e.clientX); yTo(e.clientY);
    ringX(e.clientX); ringY(e.clientY);
  });

  document.querySelectorAll("a, button").forEach(el => {
    el.addEventListener("mouseenter", () =>
      gsap.to(ring, { scale: 2, duration: 0.3, ease: "back.out(1.7)" }) 
    );
    el.addEventListener("mouseleave", () =>
      gsap.to(ring, { scale: 1, duration: 0.3, ease: "power2.out" })   
    );
  });
}
```

CSS for cursor elements:
```css
.cursor-dot, .cursor-ring {
  position: fixed; top: 0; left: 0; pointer-events: none; z-index: 9999;
  transform: translate(-50%, -50%);
}
.cursor-dot { width: 8px; height: 8px; background: currentColor; border-radius: 50%; }
.cursor-ring { width: 40px; height: 40px; border: 1.5px solid currentColor; border-radius: 50%; opacity: 0.5; }
```

---

## Pattern 15 — 3D Card Tilt (Desktop-Only)

Use for portfolio cards, product cards, or interactive elements that tilt toward the cursor. Desktop-only.

```js
const isTouch = "ontouchstart" in window || navigator.maxTouchPoints > 0;
if (!isTouch) {
  document.querySelectorAll(".tilt-card").forEach(card => {
    gsap.set(card, { transformPerspective: 800 });

    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      gsap.to(card, {
        rotationY: x * 20,
        rotationX: y * -20,
        duration: 0.3,             
        ease: "power2.out",        
        transformOrigin: "center",
      });
    });

    card.addEventListener("mouseleave", () => {
      gsap.to(card, {
        rotationX: 0, rotationY: 0,
        duration: 0.6,           
        ease: "elastic.out(1, 0.3)", 
      });
    });
  });
}
```

---

## Pattern 16 — Ripple Click Effect

Use for buttons that should show a material-style expanding circle from the click coordinates. Pure GSAP, no CSS animations.

```js
document.querySelectorAll(".ripple-btn").forEach(btn => {
  btn.style.position = "relative";
  btn.style.overflow = "hidden";

  btn.addEventListener("click", (e) => {
    const rect = btn.getBoundingClientRect();
    const ripple = document.createElement("span");
    ripple.style.cssText = `
      position: absolute; border-radius: 50%; background: rgba(255,255,255,0.3);
      width: 10px; height: 10px; pointer-events: none;
      left: ${e.clientX - rect.left}px; top: ${e.clientY - rect.top}px;
      transform: translate(-50%, -50%) scale(0);
    `;
    btn.appendChild(ripple);

    gsap.to(ripple, {
      scale: 20,
      autoAlpha: 0,
      duration: 0.6,            
      ease: "power2.out",       
      onComplete: () => ripple.remove(),
    });
  });
});
```

---

## Always Call This at End

Every full-page animation must call `ScrollTrigger.refresh()` on page load to recalculate scroll positions:

```js
window.addEventListener("load", () => ScrollTrigger.refresh());
```

---

## Usage Rules

1. **NEVER substitute CSS keyframe classes** when a pattern exists for that element type.
2. **ALWAYS use `autoAlpha`** (not bare `opacity`) in all from/fromTo calls.
3. **ALWAYS use `gsap.matchMedia()`** — never raw `if (!prefersReduced)`.
4. **REMOVE CSS `transition`** on any property GSAP will own (ownership conflict).
5. **Use `gsap.fromTo()`** (not `gsap.from()`) when element may start hidden (prevents flash bug).
6. **Adjust selectors** (`.hero-badge`, `.feature-card`, etc.) to match your HTML structure.
7. **Adjust classNames** in stagger selectors as needed (Pattern 4 is `.card, .feature-card, .pricing-card`).
8. **Use Pattern 4b** (ScrollTrigger.batch) instead of Pattern 4 when there are 10+ repeating elements.
9. **Touch guard** interactive patterns (3, 5, 14, 15) — skip on touch devices to avoid broken UX.

---

## Token Reference

| Token | Value | Use |
|---|---|---|
| `micro` | 0.15s | Cursor response, ripple start |
| `fast` | 0.3s | Hover feedback, state transitions |
| `base` | 0.6s | Standard reveals, entrance animations |
| `slow` | 1.0s | Hero animations, page transitions |
| `epic` | 1.5s | Cinematic moments, number counters |
| `entrance` | `power2.out` | Standard reveals, default easing |
| `impact` | `power3.out` | Fast, snappy entrances (sharper than `entrance`) |
| `transition` | `power2.inOut` | FLIP layout changes, shared-element transitions |
| `exit` | `power3.in` | Elements leaving the screen |
| `spring` | `back.out(1.7)` | Tactile, bouncy micro-interactions |
| `elastic` | `elastic.out(1, 0.3)` | Pronounced wobble — badges, playful UI |
| `scrub` | `none` (linear) | Scroll-tied animations |
| `tight` | 0.05s | Character-level stagger, kinetic typography |
| `medium` | 0.09s | List/card stagger delay |
| `loose` | 0.13s | Card/grid sections stagger |

All patterns include `gsap.matchMedia()` guards for `prefers-reduced-motion: reduce`.
