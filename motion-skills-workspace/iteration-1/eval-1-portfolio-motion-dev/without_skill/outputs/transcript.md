# Animation Transcript — 02-portfolio-minimal.html

## Task
Add GSAP animations to a minimal designer portfolio. Goal: subtle, premium feel with scroll-responsive animations and kinetic typography on the hero heading.

## Step-by-step Process

### Step 1: Read & Analyze Input HTML
- Read `02-portfolio-minimal.html` — a single-page portfolio for "Mara Chen, Designer & Art Director"
- Identified key sections: nav, hero (large heading + subtitle), projects list (6 items), about (text + skills list), contact (email CTA), footer
- Noted the design language: monospace accents, minimal borders, large typography, warm off-white background
- No existing JavaScript or animation libraries present

### Step 2: Plan Animation Strategy
Mapped each section to an animation approach that supports "subtle and premium":
1. **Nav** — Delayed fade-down entrance (appears after hero starts animating)
2. **Hero H1** — Kinetic typography: line-by-line clip-reveal sliding up, plus scroll-linked horizontal parallax shift per line (alternating directions) for kinetic feel
3. **Hero subtitle** — Word-by-word reveal, timed to overlap with end of heading animation
4. **Projects header** — Simple fade-up on scroll
5. **Project items** — Individual scroll-triggered timelines: fade in + title slides from left, meta/year fade in sequentially; hover adds subtle rightward title shift
6. **About text** — Word-by-word clip-reveal on scroll (same technique as subtitle)
7. **Skills list** — Staggered fade-up items
8. **Contact** — Label fades up, email scales up with slight fade; magnetic hover effect on email link
9. **Footer** — Simple fade-in for copyright and social links

### Step 3: Implement Animations

**Libraries loaded:**
- GSAP 3.12.5 (core)
- ScrollTrigger plugin

**Utility functions created:**
- `wrapLines(el)` — Splits hero H1 content on `<br>` tags and wraps each line in `.hero-line > .hero-line-inner` spans for overflow-clip reveal
- `splitWords(el)` — Wraps each word in `.word > .word-inner` spans for word-level reveal animations

**Animation sections implemented:**

1. **Nav (entrance):** `autoAlpha` fade + `y: -20` slide, delayed 1.4s so hero starts first. Nav links stagger at 0.1s intervals.

2. **Hero kinetic typography:**
   - Lines wrapped via `wrapLines()`, set to `yPercent: 110` + `rotate: 2` (pushed below clip)
   - Timeline reveals each line with `power4.out` easing, 1.2s duration, 0.12s stagger
   - Scroll-linked parallax: each line shifts horizontally (alternating +60px / -60px) as user scrolls past hero, scrubbed at 0.8

3. **Hero subtitle:** Words split via `splitWords()`, each `.word-inner` starts at `yPercent: 100`, revealed with 0.02s stagger overlapping hero timeline end.

4. **Projects header:** `autoAlpha: 0, y: 30` initial state, triggers at `top 85%`.

5. **Project items:** Each item gets its own ScrollTrigger timeline. Title slides from `x: -30`, meta and year fade in sequentially. Hover listeners add `x: 12` shift on title with `power2.out` easing.

6. **About section:**
   - Label fades up at `top 75%`
   - About text uses word-split reveal with 0.015s stagger
   - Capabilities label fades up separately
   - Skills list items stagger in with 0.08s intervals

7. **Contact:** Label fades up, email fades + scales from 0.95 to 1. Magnetic hover effect tracks mouse position within email bounding box, shifting element proportionally. Mouse leave snaps back with `elastic.out(1, 0.4)`.

8. **Footer:** Copyright and social links fade in with stagger.

### Step 4: Accessibility & Polish
- Added `prefers-reduced-motion` check: if user prefers reduced motion, timeline jumps to end and all ScrollTriggers are killed
- Added `ScrollTrigger.refresh()` on window load to ensure proper trigger positions
- Used `autoAlpha` (visibility + opacity) instead of bare `opacity` throughout to keep elements out of tab order when hidden
- Added `will-change` hints on animated elements via CSS
- All `toggleActions` set to `"play none none none"` — animations play once, never reverse (clean, not repetitive)

### Step 5: Output
- Saved animated HTML to outputs directory
- All animations are self-contained in a single HTML file (no external JS files needed beyond CDN)

## Design Decisions
- **Easing:** Primarily `power3.out` and `power4.out` — smooth deceleration that feels refined
- **Timing:** Hero starts at 0.3s delay, nav at 1.4s — creates a deliberate reveal sequence
- **Scroll triggers:** All start between 75-85% viewport — elements animate well before user reaches them
- **Kinetic typography:** Scroll-linked horizontal shift creates a parallax layering effect on the large hero text without being distracting
- **Magnetic hover:** Only on the contact email CTA — reserved for the most important interactive moment
- **No FLIP, no 3D transforms, no color changes** — kept motion vocabulary minimal to match the site's design philosophy
