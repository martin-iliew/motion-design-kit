# Animation Transcript — SOLL Wellness Landing Page

## Task
Animate a wellness landing page with a calm, nature-rooted brand feel. Motion should feel like breathing, not bouncing. Add scroll-triggered reveals for each section and a subtle parallax on the hero.

## Libraries Added
- **GSAP 3.12.5** (core) via CDN
- **ScrollTrigger** plugin via CDN

## Animations Applied

### Hero Section (on page load)
- **Sequenced timeline** revealing the tagline, heading, body text, buttons, stats, and hero image in order
- Each element fades in (`autoAlpha: 0` to visible) with a gentle upward slide (`y: 20-30px`)
- Hero image uses a slight scale-up (0.96 to 1) for a gentle "breathing in" effect
- **Parallax**: The hero image drifts upward by 40px as the user scrolls past the hero, using `scrub: 1.5` for a smooth, lagging parallax feel

### Rituals Section (scroll-triggered)
- Section header fades in and slides up when scrolled into view (trigger at 85% viewport)
- Three ritual cards stagger in with 150ms delay between each, fading up from 40px below

### Products Section (scroll-triggered)
- Section header fades in with upward slide
- Four product cards stagger in with 120ms delay, fading up from 35px below

### Manifest/Quote Section (scroll-triggered)
- The quote text fades in with a gentle upward slide and very subtle scale (0.98 to 1)
- The author attribution follows shortly after

### Journal Section (scroll-triggered)
- Section header fades in with upward slide
- Three journal cards stagger in with 150ms delay

### CTA Section (scroll-triggered)
- Sequenced timeline: heading, body text, button (with slight scale), and note text reveal one after another
- Button has a subtle scale-up (0.95 to 1) to draw gentle attention

### Footer (scroll-triggered)
- Footer content fades in softly
- Footer bottom bar fades in after

## Design Decisions
- **Easing**: Used `power2.out` throughout for a natural deceleration that matches the "breathing" feel — nothing snappy or bouncy
- **`autoAlpha`** used instead of bare `opacity` so elements are both invisible and non-interactive before they animate in (sets `visibility: hidden` when opacity is 0)
- **Durations** range from 0.6s to 1.2s — deliberately slower than typical web animations to match the calm, meditative brand tone
- **`y` offsets** kept modest (15-40px) — enough to create gentle movement without feeling jarring
- **Parallax** is subtle (40px travel) with `scrub: 1.5` for a soft, laggy drift rather than a sharp 1:1 scroll lock
- **`toggleActions: "play none none none"`** — animations play once and stay; no reverse on scroll-up, keeping the experience serene rather than fidgety
- **`ScrollTrigger.refresh()`** called on window load to ensure correct trigger positions after all assets settle

## Files
- `12-health-wellness.html` — Animated version of the wellness landing page
