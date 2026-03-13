# 2026 Motion Trend Quality Criteria

This file defines what makes a web animation pattern genuinely "2026-quality" vs. outdated.
Use it when evaluating discovered trends and when grading audit findings.

---

## The 2026 Motion Manifesto (4 Core Principles)

### 1. Physics Over Timing Functions
2026 animations feel *real*, not mechanical. They borrow from physics:
- Spring/elastic easings (`elastic.out`, `CustomEase` with organic curves) over `ease-in-out`
- Momentum and overshoot on micro-interactions
- Resistance on drag and scroll interactions
- Mass simulation: heavier elements move slower, lighter elements snap

**Outdated signal:** Every animation uses `ease-in-out 0.3s` — predictable, flat, mechanical.
**2026 signal:** Button clicks have a tiny elastic overshoot. Cards feel like they have weight.

### 2. Scroll-Driven Storytelling
The page is a timeline. Scroll position is the playhead.
- `ScrollTrigger` (GSAP) or CSS `animation-timeline: scroll()` for every major section
- Parallax that enhances depth, not just decoration
- Pinned sections with scrubbed animations for key product moments
- Progress indicators driven by scroll (not fake timers)

**Outdated signal:** Animations trigger on page load with a 0.5s delay per section.
**2026 signal:** Every reveal is tied to the user's scroll position — they control the pace.

### 3. Fluid State Transitions
Elements don't appear/disappear — they *transform* from one state to another.
- FLIP animations for layout changes (gsap.utils FLIP or View Transitions API)
- Shared-element transitions between pages/views
- Morphing icons (hamburger → close, play → pause)
- Text that crossfades without layout jump

**Outdated signal:** `display: none` toggled with `opacity: 0` fade.
**2026 signal:** Card expands from click position. Nav icon morphs. List items slide out rather than vanish.

### 4. Micro-Interaction Density
2026 interfaces are "alive" at the detail level — not just big hero animations:
- Buttons have tactile press feedback (`scale: 0.97` on `:active`)
- Form fields have entrance + focus animations
- Icons animate when their parent is hovered
- Cursor changes / magnetic effects on key CTAs
- Loading states that are themselves animated (skeleton + subtle pulse)

**Outdated signal:** The only animation is a fade-in hero image.
**2026 signal:** Every interactive element has a reaction. The interface breathes.

---

## Technology Signals

### Strong 2026 Indicators
- GSAP 3.12+ with `ScrollTrigger`, `SplitText`, `Flip`
- CSS `animation-timeline: scroll()` / `view()`
- `@starting-style` for enter transitions (native CSS)
- View Transitions API for page transitions
- `CustomEase` for branded easing curves
- `gsap.matchMedia()` for responsive + reduced-motion handling

### Outdated / Deprecated
- jQuery `.animate()`
- CSS `transition: all` (performance trap)
- AOS (Animate On Scroll) library — replaced by ScrollTrigger
- Animate.css for scroll reveals — replaced by native CSS
- WOW.js — abandoned
- GreenSock's old TweenMax/TweenLite API (use unified `gsap` object)

---

## Quality Checklist for Generated Content

Every trend file in `.claude/motion-library/` should pass these checks:

- [ ] Code snippet uses GPU-safe properties only (`transform`, `opacity`)
- [ ] GSAP code includes `gsap.registerPlugin()` call
- [ ] GSAP code includes `prefers-reduced-motion` guard
- [ ] Code snippet is complete and runnable (not pseudocode)
- [ ] "Don'ts" include the most common mistake for this pattern
- [ ] "Best Practices" covers accessibility
- [ ] Framework choice is appropriate (don't use GSAP for a pure CSS hover effect)
