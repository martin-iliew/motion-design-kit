# Animation Transcript — 02-portfolio-minimal.html

## Task
Add GSAP animations to a minimal designer portfolio. Goal: subtle, premium feel — not flashy. Scroll-responsive with kinetic typography on the hero heading.

## Libraries Used
- GSAP 3.12.5 (Core)
- GSAP ScrollTrigger plugin

## Animations Added

### 1. Navigation
- Fade in from top on page load (opacity 0 + y:-20, 0.8s duration, power2.out)

### 2. Hero — Kinetic Typography (Main Feature)
- **Line-by-line reveal:** Restructured the `<h1>` into three `<span class="hero-line">` wrappers with inner spans. Each line slides up from 110% below with a slight 3-degree rotation, staggered by 0.12s. Uses `power4.out` easing for a confident, decelerating entrance.
- **Subtitle:** Fades in and rises after the heading lines finish (overlapping by 0.4s).
- **Scroll parallax:** As the user scrolls past the hero, the heading drifts upward at a different rate (yPercent: -15, scrubbed to scroll position) creating a parallax depth effect.
- **Letter-spacing morph:** The hero heading's letter-spacing subtly widens from -0.04em to 0.02em as the user scrolls, a kinetic typography detail.
- **Subtitle fade-out:** The subtitle fades out and shifts up as user scrolls past 60% of the hero section.

### 3. Projects Section
- **Header:** Fades in and rises when scrolled into view (triggered at 85% viewport).
- **Project items:** Each item has a staggered scroll reveal — rising 60px with a subtle horizontal offset that alternates direction (odd items shift from left, even from right). Each triggered independently.
- **Hover interaction:** On mouseenter, the project title slides 16px to the right; returns on mouseleave. CSS color transition to accent already existed; this adds spatial movement.

### 4. About Section
- **Labels:** Fade up with stagger (0.15s between the two labels).
- **Text block:** Fades up 40px, triggered at 85% viewport.
- **Skills list:** Each `<li>` staggers in from the left (x:-20, 0.07s stagger) for a typewriter-like cascade.

### 5. Contact Section
- Timeline: label fades in first, then email link rises up with overlap.

### 6. Footer
- Simple fade-in when entering viewport.
- Social links stagger upward (0.08s each).

### 7. Performance Considerations
- Used `will-change: transform` on animated elements.
- `overflow: hidden` on hero line wrappers for clean clip reveals.
- `ScrollTrigger.refresh()` called on window load.
- `toggleActions: "play none none none"` — animations play once, no reverse, keeping it clean.

## HTML Modifications
- Wrapped each hero heading line in `<span class="hero-line"><span class="hero-line-inner">...</span></span>` to enable the masked slide-up reveal (the original used `<br />` tags).
- Added two new CSS rules for `.hero-line` and `.hero-line-inner`.
- Added `will-change` to `.project-item`.
- All original styles and markup preserved.

## Design Philosophy
Kept everything understated: no bouncing, no spinning, no particle effects. Easing curves are smooth power3/power4 decelerations. Stagger values are tight (0.07–0.15s) so sequences feel cohesive rather than sluggish. The kinetic typography on the hero is the boldest moment — three large text lines cascading in with rotation — then everything else stays quiet and functional.
